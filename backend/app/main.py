from fastapi import FastAPI
import uvicorn
from api import main_router
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from config import settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(settings.redis_config.url)
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache_config.prefix,
    )
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_config.allow_origins.split(","),
    allow_credentials=settings.cors_config.allow_credentials,
    allow_methods=settings.cors_config.allow_methods.split(","),
    allow_headers=settings.cors_config.allow_headers.split(","),
)
print(settings.cors_config.allow_origins.split(","))
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)