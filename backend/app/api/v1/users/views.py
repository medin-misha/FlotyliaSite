from fastapi import APIRouter
from services import CRUD
from core.models import User
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from contracts.user.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_view(user: UserCreate, session: SessionDep):
    return await CRUD.create(data=user, model=User, session=session)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_view(session: SessionDep):
    return await CRUD.get(model=User, session=session)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_view(session: SessionDep, id: int):
    return await CRUD.get(model=User, session=session, id=id)

@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_user_view(session: SessionDep, id: int, user: UserCreate):
    return await CRUD.patch(new_data=user, model=User, session=session, id=id)

@router.delete("/{id}", response_model=str, status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(session: SessionDep, id: int):
    return await CRUD.delete(model=User, session=session, id=id)
