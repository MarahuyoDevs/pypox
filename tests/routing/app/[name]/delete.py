from starlette.requests import Request
from starlette.responses import PlainTextResponse


async def endpoint(request: Request):
    return PlainTextResponse("DELETE request received.")
