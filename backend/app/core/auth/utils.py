from config import settings
from core.database import database
from contracts.admin import AdminAuth
from core.security import verify_password
from services.admin import get_admin_by_username
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contracts.admin import JWToken, RawJWTPayload, JWTPayload, AdminReturn
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError
from typing import Annotated
from datetime import timedelta
import time

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]
http_bearer = HTTPBearer()


def encode_jwt(
    payload: RawJWTPayload,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    # Автоматическое добавление времени жизни токена и времени создания
    raw_payload = payload.model_dump()
    payload = JWTPayload(
        **raw_payload,
        exp=time.time() + timedelta(days=2).total_seconds(),
        iat=time.time(),
    )
    encoded = jwt.encode(
        payload=payload.model_dump(),
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


async def jwt_auth_admin(admin_form: AdminAuth, session: SessionDep) -> JWToken:
    admin_instance = await get_admin_by_username(
        username=admin_form.username, session=session
    )
    if verify_password(
        plain_password=admin_form.password,
        hashed_password=admin_instance.hashed_password,
    ):
        payload = RawJWTPayload(sub=admin_instance.username)
        token = encode_jwt(payload=payload)
        return JWToken(access_token=token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )


def get_current_token_payload(token: HTTPAuthorizationCredentials) -> dict:
    try:
        decode_token = decode_jwt(token=token.credentials)
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    else:
        return decode_token


async def validate_auth_user_jwt(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(database.get_session),
) -> AdminReturn:
    payload: dict = get_current_token_payload(token)
    username: str | None = payload.get("sub")
    admin_instance = await get_admin_by_username(username=username, session=session)
    if admin_instance is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    else:
        return AdminReturn.model_validate(admin_instance)
