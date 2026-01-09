from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class DemoAuthMiddleware(BaseHTTPMiddleware):
    """
    Dummy middleware:
    - reads `x-demo-sub` and `x-demo-group` headers
    - sets request.state.sub and request.state.group_id
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        request.state.sub = request.headers.get("x-demo-sub", "anonymous")
        request.state.group_id = request.headers.get("x-demo-group", "groupA")
        return await call_next(request)
