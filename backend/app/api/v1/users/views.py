from fastapi import APIRouter, status
from services import CRUD
from core.models import User
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from contracts.user.schemas import UserCreate
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_view(user: UserCreate, session: SessionDep, admin: AdminDep):
    return await CRUD.create(data=user, model=User, session=session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_view(session: SessionDep, admin: AdminDep):
    return await CRUD.get(model=User, session=session)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.get(model=User, session=session, id=id)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_user_view(
    session: SessionDep, id: int, user: UserCreate, admin: AdminDep
):
    return await CRUD.patch(new_data=user, model=User, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.delete(model=User, session=session, id=id)
