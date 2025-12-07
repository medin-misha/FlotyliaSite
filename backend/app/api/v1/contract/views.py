from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Contract
from core.database import database
from contracts.contract import ContractCreate, ContractReturn
from services.crud import CRUD

router = APIRouter(prefix="/contracts", tags=["contracts"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

@router.post("/", response_model=ContractReturn)
async def create_contract(data: ContractCreate, session: SessionDep):
    return await CRUD.create(data=data, model=Contract, session=session)

@router.get("/", response_model=list[ContractReturn])
async def list_contracts(session: SessionDep):
    return await CRUD.get(model=Contract, session=session)

@router.get("/{id}", response_model=ContractReturn)
async def get_contract(id: int, session: SessionDep):
    return await CRUD.get(model=Contract, session=session, id=id)

@router.patch("/{id}", response_model=ContractReturn)
async def update_contract(id: int, data: ContractCreate, session: SessionDep):
    return await CRUD.patch(new_data=data, model=Contract, session=session, id=id)

@router.delete("/{id}")
async def delete_contract(id: int, session: SessionDep):
    return await CRUD.delete(model=Contract, session=session, id=id)
