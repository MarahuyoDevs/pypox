"""
    This module contains the base processor class for handling encoding and decoding of data.
"""

from typing import Iterable, TypeVar, get_origin
import asyncio
import inspect
from types import MappingProxyType, coroutine
from typing import Any, Callable, Generic, Literal, Mapping, Sequence, get_args
from abc import ABC, abstractmethod
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.requests import Request
from starlette.responses import Response as StarletteResponse
from starlette.websockets import WebSocket
from orjson import dumps
from orjson import loads
from pypox.openapi.main import Components, MediaType, Parameter, Response as OASResponse
from pypox.response.base import JSONResponse


class ProcessorEncoder[T](ABC):

    def __init__(self, content) -> None:
        self._content: T = content
        super().__init__()

    @property
    def value(self) -> T:
        return self._content

    @staticmethod
    @abstractmethod
    async def encode(
        var_name: str, _type: type, request: Request
    ) -> dict[str, "Processor"] | None:
        raise NotImplementedError()


class Processor:

    def __init__(
        self, function: Callable, processor_list: list[ProcessorEncoder]
    ) -> None:
        self._function = function
        self._processor_list = processor_list
        self._params = inspect.signature(function).parameters or None
        self._docstring = self._function.__doc__ or ""
        self._return_annotation = self._function.__annotations__.get("return", {})

    @property
    def function(self) -> Callable:
        return self._function

    @property
    def processor_list(self) -> list[ProcessorEncoder]:
        return self._processor_list

    @property
    def params(self) -> MappingProxyType[str, inspect.Parameter] | None:
        return self._params

    @property
    def docstring(self) -> str:
        return self._docstring

    @property
    def return_annotation(self) -> dict:
        return self._return_annotation

    async def __call__(self, request: Request, return_oas: bool = False) -> Any:
        if return_oas:
            return await self.render_oas(request)
        if inspect.iscoroutinefunction(self._function):
            return await self._function(**await self.encoder(request))
        return await self._function(await self.encoder(request))

    async def encoder(self, request: Request):
        data = {}
        tasks = []
        if not self.params:
            return data

        for name, annotation in self.params.items():
            for processor in self.processor_list:
                task = asyncio.create_task(
                    processor.encode(name, annotation.annotation, request)
                )
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        await asyncio.sleep(0)

        for result in results:
            if result:
                data.update(result)

        return data

    async def render_schema(self):

        schemas = {}

        for response in get_args(self._return_annotation):
            for single in response:
                response_data = get_args(single)
                if len(response_data) == 2:
                    # get the schema
                    schema: BaseModel = response_data[1]
                    schemas.update({schema.__name__: schema.model_json_schema()})
                await asyncio.sleep(0)
        return schemas

    async def render_responses(self, url_path: str):

        responses = {}

        for response in get_args(self._return_annotation):
            for single in response:
                response_data = get_args(single)
                if len(response_data) == 2:
                    # get the schema
                    schema: BaseModel = response_data[1]
                    status_code = response_data[0]
                    responses.update(
                        {
                            str(status_code.code): OASResponse(
                                description="",
                                content={
                                    single.media_type: MediaType(
                                        schema=schema.model_json_schema()
                                    )
                                },
                            )
                        }
                    )
        return responses

    async def render_parameters(self, url_path: str):
        parameters = {}
        if not self.params:
            return parameters
        for name, annotation in self.params.items():
            if annotation.annotation == inspect._empty:
                continue
            if get_origin(annotation.annotation) == Query:
                parameters.update(
                    {
                        name: Parameter(
                            name=name,
                            in_="query",
                            description="",
                            required=True,
                        )
                    }
                )
            if get_origin(annotation.annotation) == Header:
                parameters.update(
                    {
                        name: Parameter(
                            name=name,
                            in_="header",
                            description="",
                            required=True,
                        )
                    }
                )
            if get_origin(annotation.annotation) == Cookie:
                parameters.update(
                    {
                        name: Parameter(
                            name=name,
                            in_="cookie",
                            description="",
                            required=True,
                        )
                    }
                )
            if get_origin(annotation.annotation) == Path:
                parameters.update(
                    {
                        name: Parameter(
                            name=name,
                            in_="path",
                            description="",
                            required=True,
                        )
                    }
                )
            await asyncio.sleep(0)
        return parameters

    async def render_oas(self, request: Request):
        # create a oas component object for the endpoint
        # get schemas first
        url_path = request.url.path
        schemas = await self.render_schema()
        parameters = await self.render_parameters(url_path)
        responses = await self.render_responses(url_path)
        return JSONResponse(
            Components(
                parameters=parameters, schemas=schemas, responses=responses
            ).model_dump(exclude_defaults=True)
        )


class Query[T](ProcessorEncoder):

    def __init__(self, content: T) -> None:
        super().__init__(content)

    @staticmethod
    async def encode(
        var_name: str, _type: type, request: Request
    ) -> dict[str, "Query[T]"] | None:
        if request.query_params.get(var_name):
            return {var_name: _type(request.query_params[var_name])}


class Header[T](ProcessorEncoder):

    def __init__(self, content: T) -> None:
        super().__init__(content)

    @staticmethod
    async def encode(
        var_name: str, _type: type, request: Request
    ) -> dict[str, "Header[T]"] | None:
        if request.headers.get(var_name):
            return {var_name: _type(request.headers[var_name])}


class Cookie[T](ProcessorEncoder):

    def __init__(self, content: T) -> None:
        super().__init__(content)

    @staticmethod
    async def encode(
        var_name: str, _type: type, request: Request
    ) -> dict[str, "Cookie[T]"] | None:
        if request.cookies.get(var_name):
            return {var_name: _type(request.cookies[var_name])}


class Path[T](ProcessorEncoder):

    def __init__(self, content: T) -> None:
        super().__init__(content)

    @staticmethod
    async def encode(
        var_name: str, _type: type, request: Request
    ) -> dict[str, "Path[T]"] | None:
        if request.path_params.get(var_name):
            return {var_name: _type(request.path_params[var_name])}
