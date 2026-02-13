from typing import TypeVar, Sequence, Optional
from sqlalchemy import select, String, or_, and_, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.mapper import Mapper
from services.crud import CRUD

ModelT = TypeVar("ModelT", bound=DeclarativeBase)

async def all_str_field_search(
    session: AsyncSession,
    query: Optional[str],
    model: type[ModelT],
    page: int = 1,
    limit: int = 10,
    include_fields: Optional[list[str]] = None,
) -> Sequence[ModelT]:
    """
    Search for a multi-word query across all or specified string fields of a model.
    Case-insensitive (ilike). Returns models that match ALL words in the query.
    """
    if not query:
        return await CRUD.get(session=session, model=model, page=page, limit=limit)
        
    offset = (page - 1) * limit
    mapper: Mapper = inspect(model)
    words = query.strip().split()
    
    # Identify string columns to search in
    searchable_columns = []
    for column in mapper.columns:
        if include_fields and column.key not in include_fields:
            continue
        if isinstance(column.type, String):
            searchable_columns.append(column)

    if not searchable_columns:
        return []

    # For each word, it must match at least one of the searchable columns
    word_conditions = []
    for word in words:
        word_pattern = f"%{word}%"
        field_conditions = [col.ilike(word_pattern) for col in searchable_columns]
        word_conditions.append(or_(*field_conditions))

    stmt = select(model).where(and_(*word_conditions)).limit(limit).offset(offset).order_by(model.id.desc())
    result: Result = await session.execute(stmt)
    return result.scalars().all()
