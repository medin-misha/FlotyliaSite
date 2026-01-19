from fastapi import APIRouter, status, Depends, Response, Request, UploadFile
from fastapi.responses import StreamingResponse
from services import CRUD
from core.models import User
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from contracts.user.schemas import UserCreate, UserReturn
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn
from fastapi_cache.decorator import cache
from core.cache import cache_key_builder
from config import settings
from services.export import export_to_exel
from services.users.search import all_str_field_search


router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_view(user: UserCreate, session: SessionDep, admin: AdminDep):
    return await CRUD.create(data=user, model=User, session=session)


@router.get("/", status_code=status.HTTP_200_OK)
@cache(
    expire=60,
    key_builder=cache_key_builder,
    namespace=settings.cache_config.namespaces.users,
)
async def get_users_view(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10, search: str = ""
) -> list[UserReturn]:
    return await all_str_field_search(model=User, session=session, page=page, limit=limit, query=search)

@router.get("/export", status_code=status.HTTP_200_OK)
async def export_users_view(session: SessionDep) -> StreamingResponse:
    return await export_to_exel(session=session)

@router.get("/{id}", status_code=status.HTTP_200_OK)
@cache(
    expire=60,
    key_builder=cache_key_builder,
    namespace=settings.cache_config.namespaces.users,
)
async def get_user_view(session: SessionDep, id: int, admin: AdminDep) -> UserReturn:
    return await CRUD.get(model=User, session=session, id=id)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_user_view(
    session: SessionDep, id: int, user: UserCreate, admin: AdminDep
) -> UserReturn:
    return await CRUD.patch(new_data=user, model=User, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.delete(model=User, session=session, id=id)

