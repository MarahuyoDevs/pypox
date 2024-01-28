from pypox.processor.base import ProcessorRequest, Any
from starlette.responses import JSONResponse
from starlette.requests import Request

try:
    from pydantic import BaseModel
except ImportError as exc:
    raise exc


async def pydantic_processor(request: ProcessorRequest):
    if issubclass(request.annotation, BaseModel) and isinstance(
        request.request, Request
    ):
        return {request.name: request.annotation(**await request.request.json())}
    return None


class PydanticResponse(JSONResponse):
    def render(self, content: Any, **pydantic_kwargs) -> bytes:
        if isinstance(content, BaseModel):
            return content.model_dump_json(**pydantic_kwargs).encode("utf-8")
        return super().render(content)
