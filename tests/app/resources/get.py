from starlette.requests import Request
from starlette.responses import JSONResponse
from pypox.processor.base import processor, Query


@processor
async def endpoint(name: Query[str] = Query(is_required=True)):
    return JSONResponse({"message": f"Hello, {name.content}!"})
