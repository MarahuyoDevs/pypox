"""
    This module contains the base processor class for handling encoding and decoding of data.
"""

import asyncio
import inspect
from types import coroutine
from typing import Any, Callable
from abc import ABC, abstractmethod
from starlette.requests import Request
from starlette.websockets import WebSocket


class ProcessorRequest:
    def __init__(
        self, request: Request | WebSocket, name: str, annotation: type
    ) -> None:
        self._request: Request | WebSocket = request
        self._name: str = name
        self._annotation: type = annotation

    @property
    def request(self) -> Request | WebSocket:
        return self._request

    @property
    def name(self) -> str:
        return self._name

    @property
    def annotation(self) -> type:
        return self._annotation


class ProcessorWrapper:
    def __init__(self, function: Callable, processor_func: list[Callable]) -> None:
        self._function = function
        self._processor_func = processor_func
        self._params = inspect.signature(function).parameters

    async def __call__(self, request: Request | WebSocket) -> Any:
        if inspect.iscoroutinefunction(self._function):
            return await self.render(await self._function(**await self.encode(request)))
        return await self.render(await self._function(await self.encode(request)))

    async def encode(self, request: Request | WebSocket):
        data = {}
        tasks = []

        for name, annotation in self._params.items():
            if annotation.annotation in [Request]:
                data.update({name: request})
            for processor in self._processor_func:
                task = asyncio.create_task(
                    processor(ProcessorRequest(request, name, annotation.annotation))
                )
                tasks.append(task)

        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                data.update(result)

        return data

    async def render(self, response: Any):
        return response


async def cookie_processor(request: ProcessorRequest):
    if request.annotation in [str] and request.name in request.request.cookies:
        return {request.name: request.annotation(request.request.cookies[request.name])}
    return None


async def header_processor(request: ProcessorRequest):
    if request.annotation in [str] and request.name in request.request.headers:
        return {
            request.name.replace("-", "_"): request.annotation(
                request.request.headers[request.name]
            )
        }
    return None


async def path_processor(request: ProcessorRequest):
    if (
        request.annotation in [int, float, str, bool]
        and request.name in request.request.path_params
    ):
        return {
            request.name: request.annotation(request.request.path_params[request.name])
        }
    return None


async def query_processor(request: ProcessorRequest):
    if (
        request.annotation in [int, float, str, bool]
        and request.name in request.request.query_params
    ):
        return {
            request.name: request.annotation(request.request.query_params[request.name])
        }
    return None


async def websocket_processor(request: ProcessorRequest):
    if request.annotation in [WebSocket]:
        return {request.name: request.annotation(request.request)}
    return None


async def json_processor(request: ProcessorRequest):
    if request.annotation in [dict] and isinstance(request.request, Request):
        return {request.name: request.annotation(await request.request.json())}
    return None
