from fastapi import FastAPI
import uvicorn
from api import main_router
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from config import settings
from contextlib import asynccontextmanager

app = FastAPI()

# Trust Caddy's forwarded headers so FastAPI preserves the original HTTPS scheme.
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_config.allow_origins.split(","),
    allow_credentials=settings.cors_config.allow_credentials,
    allow_methods=settings.cors_config.allow_methods.split(","),
    allow_headers=settings.cors_config.allow_headers.split(","),
)
app.include_router(main_router)


@app.get("/health")
async def health():
    return {"status": "ok"} 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
