"""
    This module contains the base processor class for handling encoding and decoding of data.
"""

from ast import Param
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
        content: T = None,
    ) -> None:
        self.name: str = name
        self.content: T = content

    def __call__(self, request: StarletteRequest, _type: type) -> Self:

        return self

    def __oas__(self):
        return "OAS"

    def __bool__(self):
        return bool(self.content)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, content={self.content})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Any) -> bool:
        return self.content == other


class Response(Processor):
    pass


class RequestBody[T](Encoder):

    request_type: str = "body"
    media_type: str = "body"

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content)

    async def __call__(self, request: StarletteRequest, _type: type) -> Self:
        try:
            match self.request_type:
                case "body":
                    self.content = await request.body()
                case "application/x-www-form-urlencoded":
                    self.content = _type(**await request.form())
                case "application/json":
                    self.content = _type(**await request.json())
                case "multipart/form-data":
                    self.content = request.form()
                case "stream":
                    self.content = request.stream()
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid request {self.__str__()}"
            )
        return self


class JSONBody[T](RequestBody):

    request_type = "application/json"
    media_type = "application/json"

    def __init__(self, name: str, content: T) -> None:
        super().__init__(
            name,
            content,
        )


class FormBody[T](RequestBody):

    request_type = "application/x-www-form-urlencoded"
    media_type = "application/x-www-form-urlencoded"

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content)


class MultiPartBody[T](RequestBody):

    request_type = "multipart/form-data"
    media_type = "multipart/form-data"

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content)


class Parameter[T](Encoder):

    request_type: str = ""

    def __init__(
        self,
        content: T = None,
        is_required: bool = True,
        name: str = "",
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.is_required = is_required
        self.description = description
        self.deprecated = deprecated
        self.allow_empty_value = allow_empty_value
        super().__init__(name=name, content=content)

    def __call__(self, request: StarletteRequest, _type: type) -> Self:
        data = getattr(request, self.request_type).get(
            self.name.lower().replace("_", "-")
        )
        if not data:
            if self.is_required:
                raise HTTPException(status_code=400, detail=f"{self.name} is required")
            return self
        self.content = _type(data)
        return self


class Query[T](Parameter):

    def __init__(
        self,
        content: T = None,
        is_required: bool = True,
        name: str = "",
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "query_params"
        super().__init__(
            content=content,
            is_required=is_required,
            name=name,
            description=description,
            deprecated=deprecated,
            allow_empty_value=allow_empty_value,
        )


class Header[T](Parameter):

    def __init__(
        self,
        content: Any,
        is_required: bool = True,
        name: str = "",
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "headers"
        super().__init__(
            content, is_required, name, description, deprecated, allow_empty_value
        )


class Cookie[T](Parameter):

    def __init__(
        self,
        content: Any,
        is_required: bool = True,
        name: str = "",
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "cookies"
        super().__init__(
            content, is_required, name, description, deprecated, allow_empty_value
        )


class Path[T](Parameter):

    def __init__(
        self,
        content: Any,
        is_required: bool = True,
        name: str = "",
        description: str = "",
        deprecated: bool = False,
        allow_empty_value: bool = False,
    ) -> None:
        self.request_type = "path_params"
        super().__init__(
            content, is_required, name, description, deprecated, allow_empty_value
        )


class Client(Encoder):

    def __init__(self, name: str, content: Any) -> None:
        super().__init__(name, content)


def processor(func):

    @wraps(func)
    async def wrapper(request: StarletteRequest):

        func_params = {}

        for name, params in inspect.signature(func).parameters.items():

            if await is_optional(params):
                annotation = get_args(params.annotation)[0]
            else:
                annotation = params.annotation

            if annotation == StarletteRequest:
                func_params.update({name: request})
                continue

            if annotation == Client:
                func_params.update({name: Client(name, request.client)})
                continue

            if issubclass(get_origin(annotation), Parameter):
                func_params.update(
                    {name: await convert_paramaters(request, name, params)}
                )

            if issubclass(get_origin(annotation), RequestBody):
                func_params.update(
                    {name: await convert_request_body(request, name, params)}
                )
        if inspect.iscoroutinefunction(func):
            return await func(**func_params)
        return func(**func_params)

    return wrapper


async def convert_paramaters(
    request: StarletteRequest, name: str, parameter: inspect.Parameter
) -> Parameter:
    # TODO:
    # 1. check if paramater has a default value
    # 2. if it does, check if the default value is an instance of the paramater type
    # 3. if it is, return the default value
    # 4. if it is not, raise an error
    # check if the parameter has a default value
    parameter_type, sub_type, optional = await get_parameter_type(parameter)

    if optional:
        if not parameter.default == inspect._empty:
            data: Parameter[Any] = parameter_type(
                content=parameter.default.content,
                name=parameter.default.name or name,
                is_required=parameter.default.is_required,
            )
        else:
            data: Parameter[Any] = parameter_type(
                content=None, name=name, is_required=False
            )(request, sub_type)
    else:
        data = parameter_type(content=None, name=name)(request, sub_type)

    return data


async def convert_request_body(
    request: StarletteRequest, name: str, parameter: inspect.Parameter
) -> RequestBody:

    parameter_type, sub_type, optional = await get_request_body_type(parameter)

    if optional:
        if not parameter.default == inspect._empty:
            data: RequestBody[Any] = parameter_type(
                content=parameter.default.content,
                name=parameter.default.name or name,
            )
        else:
            data: RequestBody[Any] = parameter_type(content=None, name=name)
        return data
    else:
        data = parameter_type(content=None, name=name)

    return await data(request, sub_type)


async def get_parameter_type(
    parameter: inspect.Parameter,
) -> tuple[type[Parameter], type, bool]:
    if await is_optional(parameter):
        parameter_type: type[Parameter] = get_origin(get_args(parameter.annotation)[0])
        sub_type = get_args(get_args(parameter.annotation)[0])[0]
        optional = True
    else:
        parameter_type: type[Parameter] = get_origin(parameter.annotation)
        sub_type = get_args(parameter.annotation)[0]
        optional = False
    return parameter_type, sub_type, optional


async def get_request_body_type(
    parameter: inspect.Parameter,
) -> tuple[type[RequestBody], type, bool]:
    if await is_optional(parameter):
        parameter_type: type[RequestBody] = get_origin(
            get_args(parameter.annotation)[0]
        )
        sub_type = get_args(get_args(parameter.annotation)[0])[0]
        optional = True
    else:
        parameter_type: type[RequestBody] = get_origin(parameter.annotation)
        sub_type = get_args(parameter.annotation)[0]
        optional = False
    return parameter_type, sub_type, optional


async def is_optional(parameter: inspect.Parameter) -> bool:
    return get_origin(parameter.annotation) == Union and type(None) in get_args(
        parameter.annotation
    )
