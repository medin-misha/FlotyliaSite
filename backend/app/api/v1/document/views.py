from fastapi import APIRouter, status, Depends, Response, Request, UploadFile
from fastapi.responses import StreamingResponse
from services import CRUD
from core.models import Document
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.auth import utils as auth_utils
from contracts.document import DocumentCreate, DocumentReturn, DocumentUpdate
from contracts.admin.schemas import AdminReturn
from fastapi_cache.decorator import cache
from core.cache import cache_key_builder

router = APIRouter(prefix="/documents", tags=["Documents"])
sessionDep = Annotated[AsyncSession, Depends(database.get_session)]
adminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_document_view(document: DocumentCreate, session: sessionDep) -> DocumentReturn:
    return await CRUD.create(data=document, model=Document, session=session)

@router.patch("/{id}", response_model=DocumentReturn)
async def update_document_view(id: int, document: DocumentUpdate, session: sessionDep) -> DocumentReturn:
    return await CRUD.patch(new_data=document, model=Document, session=session, id=id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_view(id: int, session: sessionDep):
    return await CRUD.delete(id=id, model=Document, session=session)