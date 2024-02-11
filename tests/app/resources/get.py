from starlette.requests import Request
from starlette.responses import JSONResponse
from pypox.processor.base import processor, Query, JSONBody, FormBody
from typing import Optional


@processor
async def endpoint(
    body: Optional[JSONBody[dict]] = JSONBody(
        content={"content": "Hello, World!"}, name="body"
    ),
    karl: Optional[Query[str]] = Query(content="arararara"),
):
    if not karl:
        return JSONResponse({"message": "Hello, World!"})
    if not body:
        return JSONResponse({"message": f"Hello, {karl.content}!"})

    return JSONResponse(body.content)
