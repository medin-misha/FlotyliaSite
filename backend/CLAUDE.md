# Backend — FastAPI

## Tech Stack

- **FastAPI** + **Uvicorn** (ASGI, port 8000)
- **SQLAlchemy async** + **asyncpg** (PostgreSQL)
- **Alembic** — migrations (`app/alembic/versions/`)
- **Pydantic Settings** — config from `.env` with `__` as nested delimiter
- **JWT RS256** — private/public keys in `certs/`
- **Argon2id** — password hashing
- **aiobotocore** — async S3/MinIO client
- **fastapi-cache2** + Redis — route-level caching (default TTL 60s)
- **pandas + openpyxl** — Excel export

## Running

```bash
cd backend
uv run uvicorn app.main:app --reload
```

## Project Layout

```
app/
├── main.py              # FastAPI app, CORS, router registration
├── config.py            # Settings (AuthJWT, BucketSettings, CORSConfig, CacheSettings)
├── api/v1/              # Routes: admin, users, transport, contract, document, files, product
├── core/
│   ├── models/          # SQLAlchemy ORM models
│   ├── auth/utils.py    # JWT encode/decode, AdminDep
│   ├── security.py      # hash_password / verify_password (Argon2)
│   ├── database.py      # AsyncSessionMaker, get_session
│   └── cache.py         # Cache key builder
├── contracts/           # Pydantic schemas (Base / Create / Update / Return per entity)
├── services/
│   ├── crud.py          # Universal CRUD (create/get/patch/delete)
│   ├── s3_client.py     # S3Client.upload_file / get_file
│   ├── export.py        # Multi-sheet Excel export
│   ├── error_handlers.py# DBErrorHandler, S3ErrorHandler
│   ├── admin/crud.py    # create_admin, get_admin_by_username
│   ├── contracts/crud.py# create_contract (validates no active contract on transport)
│   ├── files/crud.py    # create_file, get_file_by_id
│   ├── users/search.py  # Multi-word search across string fields
│   └── middlewares/     # cache_control middleware
└── alembic/             # DB migrations
```

## API — Base path `/api/v1`

| Router | Prefix | Auth |
|--------|--------|------|
| Admin | `/admin` | login public; rest JWT |
| Users | `/users` | create public; rest JWT |
| Transport | `/transports` | all JWT |
| Contract | `/contracts` | all JWT |
| Document | `/documents` | all public |
| Files | `/files` | upload public; download JWT |
| Product | `/product` | all JWT |

Health check: `GET /health → {"status": "ok"}`

## Auth Flow

1. `POST /api/v1/admin/login` → returns `Bearer <token>` (RS256, 2-day TTL)
2. Protected routes use `AdminDep = Annotated[AdminReturn, Depends(validate_auth_user_jwt)]`
3. Token validated via public key in `certs/jwt-public.pem`

## Key Patterns

### Universal CRUD (`services/crud.py`)
```python
CRUD.create(data, Model, session)
CRUD.get(Model, session, id=None, page=1, limit=50, search=None, field=None)
CRUD.patch(new_data, Model, session, id)
CRUD.delete(Model, session, id)
```
- `search` without `field` → full-text across all string columns
- `search` with `field` → type-aware single-column filter

### File Upload
Files are stored in S3/MinIO as `passports/{md5hash}{original_filename}`.
The `File` model only stores the S3 object path (`link`), not a public URL.

### Contract Constraint
A transport can have only one active contract at a time.
`create_contract` raises 400 if `is_active=True` contract already exists for that transport.

### Caching
Routes tagged `"cache"` get `Cache-Control` header injected by middleware.
Redis-backed `@cache()` decorator available via `fastapi-cache2`.

## Environment Variables (`.env`)

```env
postgres_url="postgresql+asyncpg://user:pass@host:5432/db"
bucket_config__access_key="..."
bucket_config__secret_key="..."
bucket_config__endpoint_url="https://..."
bucket_config__bucket_name="..."
cors_config__allow_origins="http://localhost:5173,http://localhost:5174"
cors_config__allow_credentials=true
cors_config__allow_methods="*"
cors_config__allow_headers="*"
debug=false
```

## Database Models

| Model | Key Fields |
|-------|-----------|
| User | name, email, phone, status (pending/active/inactive), consent, birth_date, desired_transport |
| Admin | username, hashed_password, last_login_at |
| Transport | type, manufacturer, model, color, number, rental_price (default 1750) |
| Contract | transport_id, user_id, is_active, contract_file (FK→File) |
| Document | user_id, file_id, description |
| File | link (S3 object path), created_at |
| Product | name, price, quantity, type (damage/theft/other), status (open/closed/resolved/in_progress), contract_id |

## Migrations

```bash
cd backend/app
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Tests

No tests currently. Recommended stack: `pytest` + `pytest-asyncio` + `httpx` (AsyncClient).
