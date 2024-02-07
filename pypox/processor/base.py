"""
    This module contains the base processor class for handling encoding and decoding of data.
"""

from email.policy import default
from typing import (
    Iterable,
    NewType,
    Optional,
    Required,
    Self,
    TypeVar,
    Union,
    get_origin,
)
import asyncio
import inspect
from types import MappingProxyType, UnionType, coroutine
from typing import Any, Callable, Generic, Literal, Mapping, Sequence, get_args
from abc import ABC, abstractmethod
from pydantic import BaseModel
import starlette
from starlette.background import BackgroundTask
from starlette.requests import Request as StarletteRequest
from starlette.responses import (
    Response as StarletteResponse,
    JSONResponse,
    PlainTextResponse,
)
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocket
from starlette.datastructures import Address
from starlette.routing import BaseRoute, Route, WebSocketRoute, Router
from orjson import dumps
from orjson import loads
from pypox.openapi.main import (
    Components,
    MediaType,
    Parameter as OASParameter,
    RequestBody as OASRequestBody,
    Response as OASResponse,
)

from functools import wraps
from starlette.applications import Starlette


class Processor:
    pass


class Encoder[T](Processor):

    def __init__(
        self,
        name: str,
        content: T,
    ) -> None:
        self.name: str = name
        self.content: T = content

    def __call__(self, request: StarletteRequest, _type: type) -> Self:

        return self

    def __oas__(self):
        return "OAS"


class Response(Processor):
    pass


class RequestBody(Encoder):

    def __init__(self, name: str, content: Any, media_type: str) -> None:
        self.media_type = media_type
        self.request_type = media_type
        super().__init__(name, content)

    async def __call__(self, request: StarletteRequest, _type: type) -> Self:

        match self.request_type:
            case "body":
                print("test")
                self.content = await request.body()
            case "application/x-www-form-urlencoded":
                self.content = _type(**await request.form())
            case "application/json":
                self.content = _type(**await request.json())
            case "multipart/form-data":
                self.content = request.form()
            case "stream":
                self.content = request.stream()
        return self


class JSONBody[T](RequestBody):

    def __init__(self, name: str, content: T) -> None:
        super().__init__(name, content, "application/json")


class FormBody[T](RequestBody):

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content, "application/x-www-form-urlencoded")


class MultiPartBody[T](RequestBody):

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content, "multipart/form-data")


class Parameter[T](Encoder):

    request_type: str = ""

    def __init__(
        self,
        name: str,
        content: T,
        is_required: bool,
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.is_required = is_required
        self.description = description
        self.deprecated = deprecated
        self.allow_empty_value = allow_empty_value
        super().__init__(name, content)

    def __call__(self, request: StarletteRequest, _type: type) -> Self:
        data = getattr(request, self.request_type).get(
            self.name.lower().replace("_", "-")
        )
        self.content = _type(data)
        return self


class Query[T](Parameter):

    def __init__(
        self,
        name: str,
        content: Any,
        is_required: bool,
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "query_params"
        super().__init__(
            name, content, is_required, description, deprecated, allow_empty_value
        )


class Header[T](Parameter):

    def __init__(
        self,
        name: str,
        content: Any,
        is_required: bool,
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "headers"
        super().__init__(
            name, content, is_required, description, deprecated, allow_empty_value
        )


class Cookie[T](Parameter):

    def __init__(
        self,
        name: str,
        content: Any,
        is_required: bool,
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "cookies"
        super().__init__(
            name, content, is_required, description, deprecated, allow_empty_value
        )


class Path[T](Parameter):

    def __init__(
        self,
        name: str,
        content: Any,
        is_required: bool,
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "path_params"
        super().__init__(
            name, content, is_required, description, deprecated, allow_empty_value
        )


class Client(Encoder):

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content)


def processor(func):

    @wraps(func)
    async def wrapper(request: StarletteRequest):

        func_params = {}

        for name, params in inspect.signature(func).parameters.items():
            if params.annotation == StarletteRequest:
                func_params.update({name: request})
                continue
            if get_origin(params.annotation) == Client:
                func_params.update({name: Client(name, request.client)})
                continue
            if issubclass(get_origin(params.annotation), Parameter):
                param_data: Parameter = params.annotation(name, name, True)(
                    request, get_args(params.annotation)[0]
                )
                func_params.update({name: param_data})
            if issubclass(get_origin(params.annotation), RequestBody):
                encoder_data: RequestBody = await params.annotation(name, name)(
                    request, get_args(params.annotation)[0]
                )
                func_params.update({name: encoder_data})
        if inspect.iscoroutinefunction(func):
            return await func(**func_params)
        return func(**func_params)

    return wrapper


@processor
async def index(
    test: StarletteRequest,
    id: Query[str],
    user_agent: Header[str],
    name: Query[str],
):

    return PlainTextResponse(f"{user_agent.content} {name.content}")


app: Starlette = Starlette(routes=[Route("/", index, methods=["GET"])])
