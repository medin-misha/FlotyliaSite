from fastapi.responses import Response
from fastapi import Request
from config import settings

async def set_cache_control(request: Request, call_next) -> Response:
    route = request.scope.get("route")
    response = await call_next(request)
    tags = getattr(route, "tags", [])
    if "cache" in tags and request.method == "GET":
        response.headers["Cache-Control"] = f"max-age={settings.cache_config.age}"
    return response