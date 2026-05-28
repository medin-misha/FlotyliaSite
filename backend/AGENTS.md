# Backend API — Agent Reference

Machine-readable reference for AI agents working in this codebase.
Base URL: `http://localhost:8000` (dev) or the configured production domain.
All protected routes require `Authorization: Bearer <token>` (RS256 JWT, 2-day TTL).

---

## Auth

### Obtain a token

```
POST /api/v1/admin/login
Content-Type: application/json

{ "username": "string", "password": "string" }
```

Response `200`:
```json
{ "access_token": "...", "token_type": "bearer" }
```

Pass the token as `Authorization: Bearer <access_token>` on all protected routes.

---

## Health

```
GET /health
```
Response `200`: `{ "status": "ok" }`

---

## Admins — `/api/v1/admin`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/admin/` | public | Create admin |
| POST | `/api/v1/admin/login` | public | Login → JWT |
| GET | `/api/v1/admin/me` | JWT | Current admin info |
| GET | `/api/v1/admin/` | JWT | List admins |
| GET | `/api/v1/admin/{id}` | JWT | Get admin by id |
| DELETE | `/api/v1/admin/{id}` | JWT | Delete admin |

### POST `/api/v1/admin/`

```json
{ "username": "string", "password": "string" }
```

Response `201`: `AdminReturn`

```json
{
  "id": 1,
  "username": "string",
  "hashed_password": "string",
  "last_login_at": "2024-01-01T00:00:00Z | null",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## Users — `/api/v1/users`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/users/register` | public | Create user + 2 documents atomically (multipart) |
| POST | `/api/v1/users/` | public | Create user only (JSON) |
| GET | `/api/v1/users/` | JWT | List users |
| GET | `/api/v1/users/export` | JWT | Export users to Excel |
| POST | `/api/v1/users/import` | JWT | Bulk import users from Excel |
| GET | `/api/v1/users/{id}` | JWT | Get user by id |
| PATCH | `/api/v1/users/{id}` | JWT | Update user |
| DELETE | `/api/v1/users/{id}` | JWT | Delete user |

### POST `/api/v1/users/register` — atomic registration with documents

`Content-Type: multipart/form-data`

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `user_data` | string (Form) | yes | JSON-encoded `UserCreate` object |
| `file1` | file | yes | First document file (passport etc.) |
| `file2` | file | yes | Second document file |
| `file1_description` | string (Form) | no | Description for first document (default: `"document"`) |
| `file2_description` | string (Form) | no | Description for second document (default: `"document"`) |

`user_data` JSON shape — all `UserCreate` fields:

```json
{
  "name": "string (2–255)",
  "email": "user@example.com",
  "phone": "string (2–15)",
  "work_in": "string (2–50)",
  "how_found_it": "string | null",
  "desired_transport": "string | null",
  "birth_date": "YYYY-MM-DD | null",
  "invoice": "string | null",
  "status": "pending | active | inoperative | processing | in activation",
  "telegram": "string | null",
  "whatsapp": "string | null",
  "city": "string | null",
  "address": "string | null",
  "citizenship": "string | null",
  "consent": false
}
```

Response `201`: `UserReturn` (see below).

Atomicity guarantee: files are uploaded to S3, then `User` + 2 `File` records + 2 `Document` records are written in a single DB transaction. If the DB commit fails everything is rolled back.

### POST `/api/v1/users/`

`Content-Type: application/json` — accepts `UserCreate` fields (same schema as `user_data` above, but as a direct JSON body without files).

Response `201`: `UserReturn`

### UserReturn schema

```json
{
  "id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "name": "string",
  "email": "string",
  "phone": "string",
  "work_in": "string",
  "how_found_it": "string | null",
  "desired_transport": "string | null",
  "birth_date": "YYYY-MM-DD | null",
  "invoice": "string | null",
  "status": "pending",
  "telegram": "string | null",
  "whatsapp": "string | null",
  "city": "string | null",
  "address": "string | null",
  "citizenship": "string | null",
  "consent": false,
  "documents": [
    { "id": 1, "description": "string", "file_id": 1, "user_id": 1 }
  ]
}
```

User statuses: `pending`, `active`, `inoperative`, `processing`, `in activation`.

### GET `/api/v1/users/` query params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `limit` | int | 10 | Items per page |
| `search` | string | — | Full-text search across all string fields |
| `field` | string | — | Restrict search to this column name |

### POST `/api/v1/users/import`

`Content-Type: multipart/form-data`, field `file` — Excel (.xlsx) file.

Response `200`:
```json
{
  "received": 100,
  "imported": 95,
  "skipped": 5,
  "errors": [{ "row": 3, "email": "bad@ex.com", "detail": "string" }]
}
```

### GET `/api/v1/users/export`

Returns an Excel file (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`).

---

## Transports — `/api/v1/transports`

All routes require JWT.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/transports/` | Create transport |
| GET | `/api/v1/transports/` | List transports |
| GET | `/api/v1/transports/{id}` | Get transport by id |
| PATCH | `/api/v1/transports/{id}` | Update transport |
| DELETE | `/api/v1/transports/{id}` | Delete transport |

### TransportCreate / TransportUpdate

```json
{
  "type": "string",
  "manufacturer": "string",
  "model": "string",
  "color": "string | null",
  "number": "string | null",
  "message": "string | null",
  "rental_price": 1750
}
```

`TransportUpdate` — all fields optional. `TransportReturn` adds `"id": int`.

---

## Contracts — `/api/v1/contracts`

All routes require JWT.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/contracts/` | Create contract |
| GET | `/api/v1/contracts/` | List contracts |
| GET | `/api/v1/contracts/{id}` | Get contract by id |
| PATCH | `/api/v1/contracts/{id}` | Update contract |
| DELETE | `/api/v1/contracts/{id}` | Delete contract |

### ContractCreate

```json
{
  "transport_id": 1,
  "user_id": 1,
  "contract_file": 5,
  "date_of_signing": "2024-01-01T00:00:00Z | null",
  "is_active": true
}
```

`contract_file` is a `File.id` (FK). Creating a contract raises `400` if `is_active=true` and the transport already has an active contract.

`ContractReturn` adds `"id": int`.

---

## Documents — `/api/v1/documents`

All routes are **public** (no JWT required).

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/documents/` | Create document record |
| PATCH | `/api/v1/documents/{id}` | Update document record |
| DELETE | `/api/v1/documents/{id}` | Delete document record |

### DocumentCreate

```json
{
  "description": "string",
  "file_id": 1,
  "user_id": 1
}
```

`DocumentReturn` adds `"id": int`.

---

## Files — `/api/v1/files`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/files/` | public | Upload file to S3 |
| GET | `/api/v1/files/{file_id}` | JWT | Download file from S3 |

### POST `/api/v1/files/`

`Content-Type: multipart/form-data`, field `file`.

Files are stored in S3 as `passports/{md5hex}{original_filename}`. The `File` model stores only the S3 object path, not a public URL.

Response `201`:
```json
{ "id": 1, "link": "passports/abc123filename.pdf", "created_at": "..." }
```

### GET `/api/v1/files/{file_id}`

Returns raw file bytes with guessed `Content-Type` and `Cache-Control: public, max-age=86400`.

---

## Products — `/api/v1/product`

All routes require JWT.

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/product/` | Create product |
| GET | `/api/v1/product/` | List products |
| GET | `/api/v1/product/{id}` | Get product by id |
| PATCH | `/api/v1/product/{id}` | Update product |
| DELETE | `/api/v1/product/{id}` | Delete product |

### ProductCreate

```json
{
  "name": "string (max 120)",
  "price": 0,
  "quantity": 0,
  "description": "string (max 500)",
  "contract_id": 1,
  "type": "damage | theft | other",
  "status": "open | closed | resolved | in_progress"
}
```

`ProductUpdate` — all fields optional. `ProductReturn` adds `"id": int`.

---

## Common patterns

### Pagination (all list endpoints)

Query params: `page=1&limit=10`

### Search

- `?search=text` — full-text ILIKE across all string columns (AND across words).
- `?search=value&field=column_name` — exact match on a specific column; type-coerced for boolean/date/int columns.
- Passing an invalid `field` name returns `400`.

### Error responses

| Code | When |
|------|------|
| 400 | Invalid data / DB integrity error / active contract conflict |
| 401 | Missing or invalid JWT |
| 403 | S3 access denied |
| 404 | Record not found / S3 key not found |
| 422 | Pydantic validation error (including malformed `user_data` JSON in `/register`) |
| 503 | DB or S3 temporarily unavailable |
| 500 | Unexpected server error |

### Relationships

```
User ──< Document >── File
Contract ──── File          (contract_file FK)
Contract >── User
Contract >── Transport
Contract ──< Product
```
