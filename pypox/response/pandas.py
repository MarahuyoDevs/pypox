from typing import Any, Mapping
import pandas as pd
from pydantic import BaseModel
from starlette.background import BackgroundTask
from pypox.response.base import JSONResponse


class PandasResponse[**T](JSONResponse):

    def __init__(
        self,
        content: pd.DataFrame | Any = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: pd.DataFrame) -> bytes:
        if issubclass(content.__class__, pd.DataFrame):
            return content.to_json(orient="records").encode("utf-8")
        return super().render(content)
