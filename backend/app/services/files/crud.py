from sqlalchemy.ext.asyncio import AsyncSession
from core.models.file import File
from contracts.file.schemas import FileReturn, FileCreate
from services.s3_client import S3Client
from services import CRUD
import hashlib
from fastapi import UploadFile, Response
import mimetypes


async def create_file(session: AsyncSession, file: UploadFile, folder: str = "passports") -> FileReturn:
    s3_client = S3Client()
    raw_file = await file.read()
    object_name = hashlib.md5(raw_file).hexdigest()
    link = await s3_client.upload_file(file=raw_file, object_name=object_name, folder=folder, filename=file.filename)
    return await CRUD.create(session=session, model=File, data=FileCreate(link=link))

async def get_file_by_id(session: AsyncSession, file_id: int) -> Response:
    file_info = await CRUD.get(
        session=session,
        model=File,
        id=file_id
    )

    s3_client = S3Client()
    content = await s3_client.get_file(object_name=file_info.link)
    mime_type, _ = mimetypes.guess_type(file_info.link)
    return Response(
        content=content,
        media_type=mime_type or "application/octet-stream",
        headers={"Cache-Control": "public, max-age=86400"} # кеширование файла в браузере на 1 день
    )