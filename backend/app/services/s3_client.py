from aiobotocore.session import get_session
from fastapi import HTTPException, status
from contextlib import asynccontextmanager
from config import settings
from services.error_handlers import S3ErrorHandler

class S3Client:
    def __init__(
        self,
        access_key: str = settings.bucket_config.access_key,
        secret_key: str = settings.bucket_config.secret_key,
        endpoint_url: str = settings.bucket_config.endpoint_url,
        bucket_name: str = settings.bucket_config.bucket_name,
    ):
        self.config: dict = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client(
            "s3",
            **self.config,
        ) as client:
            yield client
    
    async def upload_file(
        self,
        file: bytes,
        object_name: str,
        folder: str = None,
        filename: str = None,
    ) -> str: # link to file for File model
        async with self.get_client() as client:
            try:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=f"{folder}/{object_name+filename}" if folder else object_name,
                    Body=file,
                )
            except Exception as e:
                S3ErrorHandler.handle(e, action="uploading file")
            else:
                return f"{folder}/{object_name+filename}"

    async def get_file(self, object_name: str, folder: str = None):
        key = f"{folder}/{object_name}" if folder else object_name
        async with self.get_client() as client:
            try:
                response = await client.get_object(
                    Bucket=self.bucket_name,
                    Key=key,
                )
            except Exception as e:
                S3ErrorHandler.handle(
                    e, action="getting file"
                )
            else:
                async with response["Body"] as stream:
                    return await stream.read()