from typing import List
from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Contract
from core.database import database
from contracts.contract import ContractCreate, ContractReturn
from services.crud import CRUD
from services.contracts import create_contract
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn
from fastapi_cache.decorator import cache
from core.cache import cache_key_builder
from config import settings

router = APIRouter(prefix="/contracts", tags=["contracts"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", response_model=ContractReturn, status_code=status.HTTP_201_CREATED)
async def create_contract_view(
    data: ContractCreate, session: SessionDep, admin: AdminDep
) -> ContractReturn:
    return await create_contract(session=session, contract=data)


@router.get("/", response_model=list[ContractReturn], status_code=status.HTTP_200_OK)
async def list_contracts(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10, search: str = None
) -> List[ContractReturn]:
    return await CRUD.get(model=Contract, session=session, page=page, limit=limit, search=search)


@router.get("/{id}", response_model=ContractReturn, status_code=status.HTTP_200_OK)
async def get_contract(id: int, session: SessionDep, admin: AdminDep) -> ContractReturn:
    return await CRUD.get(model=Contract, session=session, id=id)


@router.patch("/{id}", response_model=ContractReturn, status_code=status.HTTP_200_OK)
async def update_contract(
    id: int, data: ContractCreate, session: SessionDep, admin: AdminDep
) -> ContractReturn:
    return await CRUD.patch(new_data=data, model=Contract, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contract(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.delete(model=Contract, session=session, id=id)
