import json
from starlette.responses import Response as StarletteResponse
from starlette.background import BackgroundTask
from typing import Any, Literal, Mapping, get_args


class Responses[**T](StarletteResponse):

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)


class PlainTextResponse[**T](Responses):
    media_type = "text/plain"

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        if isinstance(content, bytes):
            return content
        if isinstance(content, str):
            return content.encode("utf-8")
        else:
            return super().render(content)


class HTMLResponse[**T](Responses):
    media_type = "text/html"

    def __init__(
        self,
        content: Any = None,
        status_code=Literal[200],
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, 200, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        if isinstance(content, bytes):
            return content
        if isinstance(content, str):
            return content.encode("utf-8")
        else:
            return super().render(content)


class JSONResponse[**T](Responses):
    media_type = "application/json"

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: Any) -> bytes:
        return json.dumps(content).encode("utf-8")


try:
    import orjson

    class ORJSONResponse[**T](Responses):

        def __init__(
            self,
            content: Any = None,
            status_code: int = 200,
            headers: Mapping[str, str] | None = None,
            media_type: str | None = None,
            background: BackgroundTask | None = None,
        ) -> None:
            super().__init__(content, status_code, headers, media_type, background)

        def render(self, content: Any) -> bytes:
            return orjson.dumps(content)

except ImportError as e:
    raise e
