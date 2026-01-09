# Catalog Demo API (Dummy Repository)

This repository is a **dummy / sanitized** example to demonstrate a layered architecture and documentation generation (e.g., DeepWiki).
It intentionally uses simplified domain concepts and small SQL samples.

## What this project demonstrates

- Layered structure:
  - `domain/` for business rules (Value Objects, Entities, domain errors)
  - `data_access/` for database session, SQLModel tables, repositories, SQL files, and mapping
  - `presentation/` for FastAPI routers and request/response schemas
- "Validate in domain first, then persist":
  - Category name and color are validated before hitting the database.
- Repository pattern using **SQL files** + `result.mappings()`.

## Quickstart (local)

1. Create `.env` from `.env.example` and set your DB URL.
2. Create database tables (Alembic) and run the app.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Alembic
alembic upgrade head

# Run
uvicorn main:app --reload
```

## Example API

- `GET /category`
- `POST /category` (body: `{"category_data": "{\"category\": \"Cafe\", \"color\": \"#005BAC\"}"}`)

Auth is mocked: send headers

- `x-demo-sub: alice`
- `x-demo-group: groupA`

See `docs/architecture.md` for diagrams.
