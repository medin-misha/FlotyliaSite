import logging
from typing import Type, TypeVar
from fastapi import HTTPException, status
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    OperationalError,
    InterfaceError,
    DisconnectionError,
)
from sqlalchemy.orm import DeclarativeBase

ModelT = TypeVar("ModelT", bound=DeclarativeBase)

logger = logging.getLogger(__name__)


class DBErrorHandler:
    """
    💡 Универсальный обработчик ошибок SQLAlchemy.
    Преобразует исключения в безопасные HTTP-ответы без утечек внутренней информации.
    """

    @staticmethod
    def handle(err: Exception, model: Type[ModelT], action: str = "processing") -> None:
        """
        Обрабатывает SQLAlchemy исключения и выбрасывает HTTPException с корректным статусом.
        """
        # Ошибки данных пользователя
        if isinstance(err, (IntegrityError, DataError)):
            logger.warning(
                f"Validation error in {model.__name__} during {action}", exc_info=False
            )
            logger.error(err)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data. Please check your request and try again.",
            )

        # Ошибки соединения / инфраструктуры
        elif isinstance(err, (OperationalError, InterfaceError, DisconnectionError)):
            logger.error(
                f"Database connection error in {model.__name__}", exc_info=False
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The service is temporarily unavailable. Please try again later.",
            )

        # Неизвестные ошибки
        else:
            logger.exception(f"Unexpected DB error in {model.__name__} during {action}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error. Please try again later.",
            )


class S3ErrorHandler:
    """
    💡 Универсальный обработчик ошибок S3 (botocore).
    """

    @staticmethod
    def handle(err: Exception, action: str = "processing") -> None:
        """
        Обрабатывает исключения botocore и выбрасывает HTTPException.
        """
        from botocore.exceptions import ClientError, EndpointConnectionError
        if isinstance(err, EndpointConnectionError):
            logger.error(f"S3 connection error during {action}: {err}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="S3 storage is temporarily unavailable. Please try again later.",
            )

        elif isinstance(err, ClientError):
            error_code = err.response.get("Error", {}).get("Code")
            logger.warning(f"S3 ClientError ({error_code}) during {action}: {err}")

            if error_code == "NoSuchBucket":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Storage configuration error: Bucket not found.",
                )
            elif error_code in ("AccessDenied", "AllAccessDisabled"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access to storage denied.",
                )
            elif error_code == "NoSuchKey":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="File not found in storage.",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"S3 storage error: {error_code or 'Unknown'}",
                )

        else:
            logger.exception(f"Unexpected S3 error during {action}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during storage operation.",
            )