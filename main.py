from __future__ import annotations

from fastapi import FastAPI
from dotenv import load_dotenv

from middleware import DemoAuthMiddleware
from presentation.routers.private.group.api_mycategory_router import router as mycategory_router
from data_access.db.session import init_db

load_dotenv()

app = FastAPI(title="Catalog Demo API (Dummy)")

# Middleware that sets request.state.sub and request.state.group_id
app.add_middleware(DemoAuthMiddleware)

# Routes
app.include_router(mycategory_router)

@app.on_event("startup")
async def _startup() -> None:
    # create engine + sessionmaker once and store in app.state
    init_db(app)
