# Architecture

This dummy repo follows a simple layered architecture.

## Layers

```mermaid
flowchart TB
  subgraph Build[CI/CD and Release]
    SRC[Git repository]
    IMG[Build container image]
  end

  subgraph Migrations[Alembic schema versioning]
    ENV[alembic/env.py]
    VER[alembic/versions/*]
    CMD[alembic upgrade head]
  end

  subgraph App[Runtime application]
    API[FastAPI app]
    DBSESS[data_access/db/session.py]
    REPO[data_access/repositories]
  end

  PG[(PostgreSQL)]

  SRC --> IMG
  SRC --> VER
  ENV -->|loads metadata| META[SQLModel metadata]
  CMD -->|applies DDL| PG
  IMG --> API
  API --> DBSESS --> PG
  API --> REPO --> PG
  VER --> CMD
  META --> ENV
```
## Alembic

```mermaid
flowchart LR
  Dev[Developer] -->|commit migrations| VER[alembic/versions/*]
  VER -->|release| CD[Deploy pipeline]
  CD -->|alembic upgrade head| PG[(PostgreSQL schema)]
  PG -->|start app| API[FastAPI runtime]
```

## Request flow: Create category

```mermaid
sequenceDiagram
  participant C as Client
  participant API as FastAPI Router
  participant SC as Schemas (Pydantic)
  participant SV as Service
  participant DM as Domain Models
  participant RP as Repository
  participant PG as Postgres

  C->>API: POST /category
  API->>SC: parse and validate request body
  SC-->>API: validated input (dict)

  API->>SV: create(validated input)
  SV->>DM: CategoryName and CategoryColor validation
  DM-->>SV: validated values

  SV->>RP: insert(valid values)
  RP->>PG: SQL file and params
  PG-->>RP: inserted row
  RP-->>SV: domain object

  SV-->>API: domain object
  API->>SC: build response model
  SC-->>API: response DTO
  API-->>C: 200 OK (response)
```

## Key decisions

- **Validate before persistence**: we validate `category` and `color` in `domain/`.
- **SQL files in repo**: queries are stored under `data_access/repositories/sql/`.
- **Mapping**: repository converts DB rows into domain objects via mappers.
