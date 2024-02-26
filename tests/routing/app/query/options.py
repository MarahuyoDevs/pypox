from starlette.requests import Request
from starlette.responses import PlainTextResponse


async def endpoint(request: Request):
    if not request.query_params.get("number", ""):
        return PlainTextResponse("OPTIONS request failed.", status_code=400)
    return PlainTextResponse("OPTIONS request received.")
