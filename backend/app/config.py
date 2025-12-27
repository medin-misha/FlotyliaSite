from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path
from redis.asyncio import Redis

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs/jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs/jwt-public.pem"
    algorithm: str = "RS256"

class RedisDB(BaseModel):
    cache: int = 0

class CacheNameSpaces(BaseModel):
    users: str = "users"
    contracts: str = "contracts"
    transports: str = "transports"
    files: str = "files"

class CacheConfig(BaseModel):
    prefix: str = "cache"
    namespaces: CacheNameSpaces = CacheNameSpaces()

class RedisConfig(BaseModel):
    url: str = "redis://lochost:6379"
    db: RedisDB = RedisDB()

    @property
    def connection_string(self) -> str:
        return f"{self.url}/{self.db.cache}"

class BucketSettings(BaseModel):
    access_key: str = ""
    secret_key: str = ""
    endpoint_url: str = ""
    bucket_name: str = ""

class CORSConfig(BaseModel):
    allow_origins: str = "*"
    allow_credentials: bool = True
    allow_methods: str = "*"
    allow_headers: str = "*"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", # файл который читаем
        env_file_encoding="utf-8", # кодировка файла
        extra="ignore", # игнорируем лишние переменные
        env_nested_delimiter="__", # Если видишь двойное подчеркивание в имени переменной в .env, считай это вложенностью
        case_sensitive=False, # нечувствительность к регистру
    )
    debug: bool = False
    postgres_url: str
    auth_jwt: AuthJWT = AuthJWT()
    cache_config: CacheConfig = CacheConfig()
    redis_config: RedisConfig = RedisConfig()
    bucket_config: BucketSettings
    cors_config: CORSConfig = CORSConfig()

settings = Settings()
