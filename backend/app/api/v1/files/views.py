from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from core.database import database
from services.files.crud import create_file, get_file_by_id
from contracts.file.schemas import FileReturn
from core.cache import cache_key_builder
from fastapi_cache.decorator import cache
from fastapi_cache.coder import PickleCoder
from config import settings

router = APIRouter(prefix="/files", tags=["files"])

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post("/", response_model=FileReturn, status_code=status.HTTP_201_CREATED)
async def upload_file_view(
    session: SessionDep,
    file: UploadFile = File(...),
):
    """
    Загрузка файла в S3 и сохранение ссылки в БД.
    """
    return await create_file(session=session, file=file)


@router.get("/{file_id}")
async def get_file_view(
    session: SessionDep,
    file_id: int,
):
    return await get_file_by_id(session=session, file_id=file_id)
