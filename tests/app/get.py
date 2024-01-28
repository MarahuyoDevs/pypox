from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse
from pypox.processor.pydantic import PydanticResponse
from pydantic import BaseModel


class Model(BaseModel):
    message: str


async def endpoint(request: Request):
    return PydanticResponse(content=Model(message="Hello World! its from pydantic!!"))
