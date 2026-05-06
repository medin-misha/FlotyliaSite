import json

from fastapi import HTTPException, UploadFile, status
from pydantic import ValidationError
from sqlalchemy import Result, func, select
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.user.schemas import UserImportCreate, UserImportError, UserImportReport
from core.models import User


async def import_users(file: UploadFile, session: AsyncSession) -> UserImportReport:
    try:
        payload = await _load_json_payload(file=file)
    finally:
        await file.close()

    errors: list[UserImportError] = []
    valid_rows: list[tuple[int, UserImportCreate, str]] = []

    for row_number, row in enumerate(payload, start=1):
        if not isinstance(row, dict):
            errors.append(
                UserImportError(row=row_number, detail="Each item in the JSON array must be an object.")
            )
            continue

        try:
            validated_row = UserImportCreate.model_validate(row)
        except ValidationError as exc:
            errors.append(
                UserImportError(
                    row=row_number,
                    email=_extract_email(row.get("email")),
                    detail="; ".join(error["msg"] for error in exc.errors()),
                )
            )
            continue

        normalized_email = _normalize_email(validated_row.email)
        if not normalized_email:
            errors.append(
                UserImportError(row=row_number, detail="Email is required for import.")
            )
            continue

        valid_rows.append((row_number, validated_row, normalized_email))

    existing_emails = await _get_existing_emails(
        session=session,
        emails=[normalized_email for _, _, normalized_email in valid_rows],
    )
    seen_in_request: set[str] = set()
    imported = 0

    for row_number, validated_row, normalized_email in valid_rows:
        if normalized_email in seen_in_request:
            errors.append(
                UserImportError(
                    row=row_number,
                    email=validated_row.email,
                    detail="Email is duplicated in the uploaded file.",
                )
            )
            continue

        seen_in_request.add(normalized_email)

        if normalized_email in existing_emails:
            errors.append(
                UserImportError(
                    row=row_number,
                    email=validated_row.email,
                    detail="User with this email already exists in the database.",
                )
            )
            continue

        user_data = validated_row.model_dump(exclude_none=True)
        user_data["email"] = validated_row.email.strip()
        instance = User(**user_data)
        session.add(instance)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            errors.append(
                UserImportError(
                    row=row_number,
                    email=validated_row.email,
                    detail="Database rejected the row, likely due to a duplicate email.",
                )
            )
            continue
        except DataError:
            await session.rollback()
            errors.append(
                UserImportError(
                    row=row_number,
                    email=validated_row.email,
                    detail="Database rejected the row due to an invalid value.",
                )
            )
            continue

        imported += 1
        existing_emails.add(normalized_email)

    return UserImportReport(
        received=len(payload),
        imported=imported,
        skipped=len(errors),
        errors=errors,
    )


async def _load_json_payload(file: UploadFile) -> list[dict]:
    try:
        raw_content = await file.read()
        text_content = raw_content.decode("utf-8")
        payload = json.loads(text_content)
    except UnicodeDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be valid UTF-8 JSON.",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must contain valid JSON.",
        ) from exc

    if not isinstance(payload, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded JSON must be an array of user records.",
        )

    return payload


async def _get_existing_emails(session: AsyncSession, emails: list[str]) -> set[str]:
    if not emails:
        return set()

    stmt = select(func.lower(User.email)).where(func.lower(User.email).in_(emails))
    result: Result = await session.execute(stmt)
    return set(result.scalars().all())


def _normalize_email(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    return normalized or None


def _extract_email(value: object) -> str | None:
    if value is None:
        return None
    return str(value).strip() or None
