from fastapi import APIRouter, BackgroundTasks, File, Form, status, Depends, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from services import CRUD
from core.models import User
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from typing import Annotated
from contracts.user.schemas import UserCreate, UserImportReport, UserReturn, UserUpdate, UserBulkStatusUpdate, UserBulkDelete
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn
from services.export import export_to_exel
from services.notifications import notify_new_application
from services.users.import_users import import_users
from services.users.register import register_user


router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user_view(
    session: SessionDep,
    background_tasks: BackgroundTasks,
    user_data: str = Form(..., description="JSON-строка UserCreate"),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    file1_description: str = Form(default="document"),
    file2_description: str = Form(default="document"),
) -> UserReturn:
    user = await register_user(
        session=session,
        user_data=user_data,
        file1=file1,
        file2=file2,
        file1_description=file1_description,
        file2_description=file2_description,
    )
    background_tasks.add_task(notify_new_application, UserReturn.model_validate(user).model_dump(mode="json"))
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_view(
    user: UserCreate,
    session: SessionDep,
    background_tasks: BackgroundTasks,
) -> UserReturn:
    created = await CRUD.create(data=user, model=User, session=session)
    background_tasks.add_task(notify_new_application, user.model_dump(mode="json"))
    return created


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users_view(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10, search: str | None = None, field: str | None = None
) -> list[UserReturn] | None:
    return await CRUD.get(model=User, session=session, page=page, limit=limit, search=search, field=field)

@router.get("/export", status_code=status.HTTP_200_OK)
async def export_users_view(session: SessionDep, admin: AdminDep) -> StreamingResponse:
    return await export_to_exel(session=session)


@router.post("/import", status_code=status.HTTP_200_OK, response_model=UserImportReport)
async def import_users_view(
    session: SessionDep, admin: AdminDep, file: UploadFile = File(...)
) -> UserImportReport:
    return await import_users(file=file, session=session)


@router.patch("/bulk-status", status_code=status.HTTP_200_OK)
async def bulk_update_status_view(
    data: UserBulkStatusUpdate, session: SessionDep, admin: AdminDep
) -> dict:
    if not data.ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ids list is empty")
    stmt = (
        update(User)
        .where(User.id.in_(data.ids))
        .values(status=data.status)
        .execution_options(synchronize_session=False)
    )
    result = await session.execute(stmt)
    await session.commit()
    return {"updated": result.rowcount}


@router.delete("/bulk", status_code=status.HTTP_200_OK)
async def bulk_delete_view(
    data: UserBulkDelete, session: SessionDep, admin: AdminDep
) -> dict:
    if not data.ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ids list is empty")
    stmt = select(User).where(User.id.in_(data.ids))
    result = await session.execute(stmt)
    instances = result.scalars().all()
    for inst in instances:
        await session.delete(inst)
    await session.commit()
    return {"deleted": len(instances)}


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user_view(session: SessionDep, id: int, admin: AdminDep) -> UserReturn:
    return await CRUD.get(model=User, session=session, id=id)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_user_view(
    session: SessionDep, id: int, user: UserUpdate, admin: AdminDep
) -> UserReturn:
    return await CRUD.patch(new_data=user, model=User, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.delete(model=User, session=session, id=id)
