from fastapi import APIRouter, status, Depends
from services import CRUD
from services.receipts import get_monthly_statistics
from core.models import Receipt
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from contracts.receipt.schemas import ReceiptCreate, ReceiptReturn, ReceiptUpdate, MonthlyStat
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn


router = APIRouter(prefix="/receipts", tags=["receipts"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_receipt_view(receipt: ReceiptCreate, session: SessionDep, admin: AdminDep) -> ReceiptReturn:
    return await CRUD.create(data=receipt, model=Receipt, session=session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_receipts_view(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10, search: str | None = None, field: str | None = None
) -> list[ReceiptReturn] | None:
    return await CRUD.get(model=Receipt, session=session, page=page, limit=limit, search=search, field=field)


@router.get("/statistics/monthly", status_code=status.HTTP_200_OK)
async def get_monthly_statistics_view(session: SessionDep, admin: AdminDep) -> list[MonthlyStat]:
    return await get_monthly_statistics(session=session)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_receipt_view(session: SessionDep, id: int, admin: AdminDep) -> ReceiptReturn:
    return await CRUD.get(model=Receipt, session=session, id=id)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_receipt_view(
    session: SessionDep, id: int, receipt: ReceiptUpdate, admin: AdminDep
) -> ReceiptReturn:
    return await CRUD.patch(new_data=receipt, model=Receipt, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_receipt_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.delete(model=Receipt, session=session, id=id)
