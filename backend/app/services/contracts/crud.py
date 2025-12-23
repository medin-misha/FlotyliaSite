from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.contract import Contract
from contracts.contract.schemas import ContractCreate, ContractReturn
from services import CRUD
from fastapi import HTTPException, status

async def create_contract(session: AsyncSession, contract: ContractCreate) -> ContractReturn:
    stmt = select(Contract).where(Contract.transport_id == contract.transport_id, Contract.is_active == True)
    result = await session.execute(stmt)
    if len(result.scalars().all()) > 0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This transport already has an active contract."
            )
    return await CRUD.create(session=session, model=Contract, data=contract)