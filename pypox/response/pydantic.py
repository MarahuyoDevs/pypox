from typing import Any, Mapping
from pydantic import BaseModel
from starlette.background import BackgroundTask
from pypox.response.base import JSONResponse


class PydanticResponse[**T](JSONResponse):

    def __init__(
        self,
        content: BaseModel | Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: BaseModel) -> bytes:
        if issubclass(content.__class__, BaseModel):
            return content.model_dump_json().encode("utf-8")
        return super().render(content)
