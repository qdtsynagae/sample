# Architecture

This dummy repo follows a simple layered architecture.

## Layers

```mermaid
flowchart TB
  subgraph Presentation[presentation - FastAPI]
    R[Routers]
    S[Schemas]
  end

  subgraph Domain[domain - Business rules]
    M[Models: Value Objects and Entities]
    E[Domain Errors]
  end

  subgraph DataAccess[data_access - Persistence]
    DB[db/session.py]
    T[models - SQLModel tables]
    Repo[repositories - SQL and mapping]
  end

  R --> S
  R -->|Depends get_session| DB
  R -->|calls| SV[domain/services/mycategory_service.py]

  SV --> M
  SV -->|uses| Repo
  Repo -->|reads| SQLF[repositories/sql files]
  Repo --> T
  DB --> PG[(PostgreSQL)]
  Repo --> PG

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
