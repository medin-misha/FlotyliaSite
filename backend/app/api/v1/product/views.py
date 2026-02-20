from fastapi import APIRouter, status, Depends
from services import CRUD
from core.models import Product
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from contracts.product.schemas import ProductCreate, ProductReturn, ProductUpdate
from core.auth import utils as auth_utils
from contracts.admin.schemas import AdminReturn


router = APIRouter(prefix="/product", tags=["product"])
SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
AdminDep = Annotated[AdminReturn, Depends(auth_utils.validate_auth_user_jwt)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_view(product: ProductCreate, session: SessionDep, admin: AdminDep) -> ProductReturn:
    return await CRUD.create(data=product, model=Product, session=session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_products_view(
    session: SessionDep, admin: AdminDep, page: int = 1, limit: int = 10, search: str | None = None, field: str | None = None
) -> list[ProductReturn] | None:
    return await CRUD.get(model=Product, session=session, page=page, limit=limit, search=search, field=field)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_view(session: SessionDep, id: int, admin: AdminDep) -> ProductReturn:
    return await CRUD.get(model=Product, session=session, id=id)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_product_view(
    session: SessionDep, id: int, product: ProductUpdate, admin: AdminDep
) -> ProductReturn:
    return await CRUD.patch(new_data=product, model=Product, session=session, id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_view(session: SessionDep, id: int, admin: AdminDep):
    return await CRUD.delete(model=Product, session=session, id=id)
