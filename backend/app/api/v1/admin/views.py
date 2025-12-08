from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import database
from core.models import Admin
from contracts.admin import AdminCreateForm, AdminReturn
from services.admin import create_admin
from services.crud import CRUD

router = APIRouter(prefix="/admin", tags=["Admin"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

@router.post("/", response_model=AdminReturn, status_code=status.HTTP_201_CREATED)
async def create_admin(data: AdminCreateForm, session: SessionDep):
    return await create_admin(data=data, session=session)

@router.get("/", response_model=list[AdminReturn], status_code=status.HTTP_200_OK)
async def list_admins(session: SessionDep):
    return await CRUD.get(model=Admin, session=session)

@router.get("/{id}", response_model=AdminReturn, status_code=status.HTTP_200_OK)
async def get_admin(id: int, session: SessionDep):
    return await CRUD.get(model=Admin, session=session, id=id)

@router.delete("/{id}", response_model=str, status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(id: int, session: SessionDep):   
    return await CRUD.delete(model=Admin, session=session, id=id)

