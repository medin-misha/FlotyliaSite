from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, or_
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.utils import get_column_letter
import io
from services import CRUD
from core.models import User, Transport, Contract
from services.error_handlers import DBErrorHandler
from fastapi import HTTPException
from sqlalchemy import Result


async def _get_contracts(session: AsyncSession) -> list:
    try:
        # Subquery to find IDs that occur exactly once
        unique_subq = (
            select(Contract.user_id)
            .group_by(Contract.user_id)
            .having(func.count(Contract.user_id) == 1)
            .scalar_subquery()
        )

        stmt = (
            select(Contract)
            .options(
                joinedload(Contract.user),  # Подгрузить пользователя
                joinedload(Contract.transport),  # Подгрузить транспорт
            )
            .where(or_(Contract.is_active == True, Contract.user_id.in_(unique_subq)))
        )
        result: Result = await session.execute(stmt)
        data = result.scalars().all()
        return data
    except Exception as err:
        # Любая ошибка SQLAlchemy или инфраструктуры
        DBErrorHandler.handle(err=err, model=Contract)


async def _get_relation_users_contracts(session: AsyncSession, contracts: list) -> list:
    try:
        result = []
        for contract in contracts:
            # Fetch related user and transport
            user = contract.user
            transport = contract.transport

            if user and transport:
                result.append(
                    {
                        "Username": user.name,
                        "Email": user.email,
                        "Phone": user.phone,
                        "Work_in": user.work_in,
                        "Invoice": user.invoice,
                        "Status": user.status,
                        "Passport_url": user.passport_file
                        if user.passport_file
                        else None,
                        "Contract_url": f"api/v1/files/{contract.contract_file}"
                        if contract.contract_file
                        else None,
                        "Date_of_signing": f"{contract.date_of_signing}",
                        "Transport_number": transport.number,
                    }
                )
        return result
    except Exception as err:
        # Любая ошибка SQLAlchemy или инфраструктуры
        DBErrorHandler.handle(err=err, model=User)


async def _get_not_relation_users(session: AsyncSession) -> list:
    try:
        stmt = select(User).where(User.id.notin_(select(Contract.user_id).scalar_subquery()))
        result: Result = await session.execute(stmt)
        data = result.scalars().all()
        result = []
        for user in data:
            result.append(
                {
                    "Username": user.name,
                    "Email": user.email,
                    "Phone": user.phone,
                    "Work_in": user.work_in,
                    "Invoice": user.invoice,
                    "Status": user.status,
                    "Passport_url": user.passport_file
                    if user.passport_file
                    else None,
                }
            )
        return result
    except Exception as err:
        # Любая ошибка SQLAlchemy или инфраструктуры
        DBErrorHandler.handle(err=err, model=User)


async def _get_data(session: AsyncSession) -> list:
    contracts = await _get_contracts(session=session)
    database = []
    relation_users_contracts = await _get_relation_users_contracts(
        session=session, contracts=contracts
    )
    not_relation_users_contracts = await _get_not_relation_users(
        session=session
    )
    database.extend(relation_users_contracts)
    database.extend(not_relation_users_contracts)
    return database


async def export_to_exel(session: AsyncSession) -> StreamingResponse:
    data = await _get_data(session)
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Database")
        sheet = writer.sheets["Database"]
        fill = PatternFill(start_color="4B85E7", end_color="4B85E7", fill_type="solid")
        font = Font(color="FFFFFF", bold=True)
        for i in range(1, sheet.max_column + 1):
            symbol = get_column_letter(i)
            sheet.column_dimensions[symbol].width = 18  # ширина столбца в символах
        for cell in sheet[1]:
            cell.font = font
            cell.fill = fill

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=database.xlsx"},
    )
