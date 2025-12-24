from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Transport
from core.database import database
from contracts.transport import TransportCreate, TransportReturn
from services.crud import CRUD
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn
from fastapi_cache.decorator import cache
from core.cache import cache_key_builder
from config import settings

router = APIRouter(prefix="/transports", tags=["transports"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", response_model=TransportReturn, status_code=status.HTTP_201_CREATED)
async def create_transport(data: TransportCreate, session: SessionDep, admin: AdminDep):
    return await CRUD.create(data=data, model=Transport, session=session)


@router.get("/", response_model=list[TransportReturn], status_code=status.HTTP_200_OK)
@cache(
    expire=60,
    key_builder=cache_key_builder,
    namespace=settings.cache_config.namespaces.transports,
)
async def list_transports(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10
):
    return await CRUD.get(model=Transport, session=session, page=page, limit=limit)


@router.get("/{id}", response_model=TransportReturn, status_code=status.HTTP_200_OK)
@cache(
    expire=60,
    key_builder=cache_key_builder,
    namespace=settings.cache_config.namespaces.transports,
)
async def get_transport(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.get(model=Transport, session=session, id=id)


@router.patch("/{id}", response_model=TransportReturn, status_code=status.HTTP_200_OK)
async def update_transport(
    id: int, data: TransportCreate, session: SessionDep, admin: AdminDep
):
    return await CRUD.patch(new_data=data, model=Transport, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transport(id: int, session: SessionDep, admin: AdminDep):
    return await CRUD.delete(model=Transport, session=session, id=id)
