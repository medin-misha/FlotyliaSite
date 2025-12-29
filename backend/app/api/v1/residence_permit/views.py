from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import ResidencePermit
from core.database import database
from contracts.residence_permit.schemas import (
    ResidencePermitBase,
    ResidencePermitCreate,
    ResidencePermitUpdate,
    ResidencePermitReturn,
)
from core.auth import utils as auth_utils
from fastapi_cache.decorator import cache
from core.cache import cache_key_builder
from config import settings
from services.crud import CRUD
from contracts.admin.schemas import AdminReturn

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]
router = APIRouter(prefix="/residence-permit", tags=["residence-permit"])


@router.post(
    "/", response_model=ResidencePermitReturn, status_code=status.HTTP_201_CREATED
)
async def create_residence_permit(
    residence_permit: ResidencePermitCreate, session: SessionDep, admin: AdminDep
):
    return await CRUD.create(
        model=ResidencePermit, session=session, data=residence_permit
    )


@router.get("/", response_model=list[ResidencePermitReturn])
@cache(
    expire=60,
    key_builder=cache_key_builder,
    namespace=settings.cache_config.namespaces.residence_permits,
)
async def get_residence_permit(session: SessionDep, page: int = 1, limit: int = 10):
    return await CRUD.get(
        model=ResidencePermit, session=session, page=page, limit=limit
    )


@router.patch("/{id}", response_model=ResidencePermitReturn)
async def update_residence_permit(
    id: int, residence_permit: ResidencePermitUpdate, session: SessionDep
):
    return await CRUD.patch(
        model=ResidencePermit, session=session, id=id, new_data=residence_permit
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_residence_permit(id: int, session: SessionDep):
    return await CRUD.delete(model=ResidencePermit, session=session, id=id)
