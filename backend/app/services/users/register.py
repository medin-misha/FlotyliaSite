import hashlib
import json

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.user.schemas import UserCreate
from core.models.document import Document
from core.models.file import File
from core.models.user import User
from services.s3_client import S3Client


async def register_user(
    session: AsyncSession,
    user_data: str,
    file1: UploadFile,
    file2: UploadFile,
    file1_description: str,
    file2_description: str,
) -> User:
    try:
        user_schema = UserCreate(**json.loads(user_data))
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    s3 = S3Client()

    raw1 = await file1.read()
    link1 = await s3.upload_file(
        file=raw1,
        object_name=hashlib.md5(raw1).hexdigest(),
        folder="passports",
        filename=file1.filename,
    )

    raw2 = await file2.read()
    link2 = await s3.upload_file(
        file=raw2,
        object_name=hashlib.md5(raw2).hexdigest(),
        folder="passports",
        filename=file2.filename,
    )

    try:
        user_instance = User(**user_schema.model_dump())
        session.add(user_instance)
        await session.flush()

        file_record1 = File(link=link1)
        file_record2 = File(link=link2)
        session.add_all([file_record1, file_record2])
        await session.flush()

        session.add_all([
            Document(user_id=user_instance.id, file_id=file_record1.id, description=file1_description),
            Document(user_id=user_instance.id, file_id=file_record2.id, description=file2_description),
        ])

        await session.commit()
        await session.refresh(user_instance)
    except Exception:
        await session.rollback()
        raise

    return user_instance
