from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import database
from core.models import Admin
from contracts.admin import AdminCreateForm, AdminReturn, JWToken
from services.admin import create_admin
from services.crud import CRUD
from core.auth import utils as auth_utils


router = APIRouter(prefix="/admin", tags=["Admin"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", response_model=AdminReturn, status_code=status.HTTP_201_CREATED)
async def create_admin_view(data: AdminCreateForm, session: SessionDep):
    return await create_admin(data=data, session=session)


@router.get("/", response_model=list[AdminReturn], status_code=status.HTTP_200_OK)
async def list_admins(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10
):
    return await CRUD.get(model=Admin, session=session, page=page, limit=limit)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=JWToken)
async def jwt_auth_admin(token: JWToken = Depends(auth_utils.jwt_auth_admin)):
    return token


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(admin: AdminDep):
    return admin


@router.get("/{id}", response_model=AdminReturn, status_code=status.HTTP_200_OK)
async def get_admin(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.get(model=Admin, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.delete(model=Admin, session=session, id=id)
