from typing import Any, Callable, Mapping, Sequence, Type
from jinja2.defaults import (
    BLOCK_END_STRING,
    BLOCK_START_STRING,
    COMMENT_END_STRING,
    COMMENT_START_STRING,
    KEEP_TRAILING_NEWLINE,
    LSTRIP_BLOCKS,
    TRIM_BLOCKS,
    VARIABLE_END_STRING,
    VARIABLE_START_STRING,
)
from jinja2.ext import Extension
from starlette.background import BackgroundTask
from starlette.requests import Request
from pydantic import BaseModel, field_validator, Field
from pypox.processing.base import HeaderValidator
from jinja2 import BaseLoader, BytecodeCache, Environment, FileSystemLoader, Undefined
from starlette.responses import HTMLResponse


class HTMXValidator(HeaderValidator):

    def __init__(self, name: str, _type: Type) -> None:
        super().__init__(name, _type)

    async def validate(self, _type: Type, request: Request) -> None:
        if _type not in [HTMXHeaders, HTMXResponseHeaders]:
            return None
        return _type(**request.headers)


class HTMXHeaders(BaseModel):

    boosted: str = Field(default="false", alias="hx-boosted")
    current_url: str = Field(default="", alias="hx-current-url")
    history_restored: str = Field(default="false", alias="hx-history-restored")
    prompt: str = Field(default="false", alias="hx-prompt")
    request: str = Field(default="false", alias="hx-request")
    target: str = Field(default="", alias="hx-target")
    trigger_name: str = Field(default="", alias="hx-trigger-name")
    trigger: str = Field(default="", alias="hx-trigger")

    @field_validator("request")
    def validate_request(cls, value):
        if value:
            return value
        else:
            raise ValueError("Request must be True")


class HTMXResponseHeaders(BaseModel):
    location: str = Field(
        default="", validation_alias="hx-location", serialization_alias="hx-location"
    )
    push_url: str = Field(
        default="", validation_alias="hx-push-url", serialization_alias="hx-push-url"
    )
    redirect: str = Field(
        default="", validation_alias="hx-redirect", serialization_alias="hx-redirect"
    )
    refresh: str = Field(
        default="", validation_alias="hx-refresh", serialization_alias="hx-refresh"
    )
    replace_url: str = Field(
        default="",
        validation_alias="hx-replace-url",
        serialization_alias="hx-replace-url",
    )
    reswap: str = Field(
        default="", validation_alias="hx-reswap", serialization_alias="hx-reswap"
    )
    retarget: str = Field(
        default="", validation_alias="hx-retarget", serialization_alias="hx-retarget"
    )
    reselect: str = Field(
        default="", validation_alias="hx-reselect", serialization_alias="hx-reselect"
    )
    trigger: str = Field(
        default="", validation_alias="hx-trigger", serialization_alias="hx-trigger"
    )
    trigger_after_settle: str = Field(
        default="",
        validation_alias="hx-trigger-after-settle",
        serialization_alias="hx-trigger-after-settle",
    )
    trigger_after_swap: str = Field(
        default="",
        validation_alias="hx-trigger-after-swap",
        serialization_alias="hx-trigger-after-swap",
    )
