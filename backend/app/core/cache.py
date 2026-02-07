from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from contracts.admin.schemas import AdminReturn
import hashlib
from typing import Any, Callable, Dict, Tuple, Optional


def cache_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...] = (),
    kwargs: Dict[str, Any] = {}
) -> Optional[str]:
    safe_types = (int, float, str, bool, type(None))
    for key, value in kwargs.copy().items():
        if type(value) not in safe_types:
            kwargs.pop(key)
    hash = hashlib.md5(
        f"{func.__module__}:{func.__name__}:{args}:{kwargs}".encode()
    ).hexdigest()
    return f"{namespace}:{hash}"
