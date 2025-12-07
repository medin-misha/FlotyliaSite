from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Transport
from core.database import database
from contracts.transport import TransportCreate, TransportReturn
from services.crud import CRUD

router = APIRouter(prefix="/transports", tags=["transports"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]

@router.post("/", response_model=TransportReturn)
async def create_transport(data: TransportCreate, session: SessionDep):
    return await CRUD.create(data=data, model=Transport, session=session)

@router.get("/", response_model=list[TransportReturn])
async def list_transports(session: SessionDep):
    return await CRUD.get(model=Transport, session=session)

@router.get("/{id}", response_model=TransportReturn)
async def get_transport(id: int, session: SessionDep):
    return await CRUD.get(model=Transport, session=session, id=id)

@router.patch("/{id}", response_model=TransportReturn)
async def update_transport(id: int, data: TransportCreate, session: SessionDep):
    return await CRUD.patch(new_data=data, model=Transport, session=session, id=id)

@router.delete("/{id}")
async def delete_transport(id: int, session: SessionDep):
    return await CRUD.delete(model=Transport, session=session, id=id)
