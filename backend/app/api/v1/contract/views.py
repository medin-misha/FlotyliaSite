from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Contract
from core.database import database
from contracts.contract import ContractCreate, ContractReturn
from services.crud import CRUD
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn

router = APIRouter(prefix="/contracts", tags=["contracts"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", response_model=ContractReturn, status_code=status.HTTP_201_CREATED)
async def create_contract(data: ContractCreate, session: SessionDep, admin: AdminDep):
    return await CRUD.create(data=data, model=Contract, session=session)


@router.get("/", response_model=list[ContractReturn], status_code=status.HTTP_200_OK)
async def list_contracts(session: SessionDep, admin: AdminDep):
    return await CRUD.get(model=Contract, session=session)


@router.get("/{id}", response_model=ContractReturn, status_code=status.HTTP_200_OK)
async def get_contract(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.get(model=Contract, session=session, id=id)


@router.patch("/{id}", response_model=ContractReturn, status_code=status.HTTP_200_OK)
async def update_contract(
    id: int, data: ContractCreate, session: SessionDep, admin: AdminDep
):
    return await CRUD.patch(new_data=data, model=Contract, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.delete(model=Contract, session=session, id=id)
