from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import Admin
from contracts.admin import AdminCreateForm, AdminReturn, AdminCreate
from services.crud import CRUD
from core.security import hash_password, verify_password


async def create_admin(data: AdminCreateForm, session: AsyncSession) -> AdminReturn:
    hashed_password = hash_password(data.password)
    form = data.model_dump()
    form.pop("password")
    form["hashed_password"] = hashed_password
    new_admin_form = AdminCreate(
        username=form["username"], hashed_password=hashed_password
    )
    admin = await CRUD.create(model=Admin, session=session, data=new_admin_form)
    return AdminReturn.model_validate(admin)


async def get_admin_by_username(username: str, session: AsyncSession) -> AdminReturn:
    stmt = select(Admin).where(Admin.username == username)
    result = await session.execute(stmt)
    admin = result.scalar_one_or_none()
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return AdminReturn.model_validate(admin)
