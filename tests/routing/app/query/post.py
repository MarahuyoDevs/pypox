from starlette.requests import Request
from starlette.responses import PlainTextResponse


async def endpoint(request: Request):
    if not request.query_params.get("number", ""):
        return PlainTextResponse("POST request failed.", status_code=400)
    return PlainTextResponse("POST request received.")
