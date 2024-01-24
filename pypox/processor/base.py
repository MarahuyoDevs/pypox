"""
    This module contains the base processor class for handling encoding and decoding of data.
"""

import inspect
from typing import Any, Callable
from abc import ABC, abstractmethod
from starlette.responses import (
    Response,
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    StreamingResponse,
    FileResponse,
)
from starlette.requests import Request
from starlette.websockets import WebSocket


STARLETTE_RESPONSE = {
    Response,
    JSONResponse,
    HTMLResponse,
    RedirectResponse,
    PlainTextResponse,
    StreamingResponse,
    FileResponse,
}


class BaseProcessor(ABC):
    """
    Base class for processors that handle encoding and decoding of data.

    Args:
        types (list[type] | type): The types of data that the processor can handle.
            If a single type is provided, it will be converted to a list.
        response_class (type[Response] | None, optional): The response class to be used
            for decoding the response data. Defaults to None.

    Attributes:
        types (list[type]): The types of data that the processor can handle.
        response_class (type[Response] | None): The response class to be used for
            decoding the response data.
    """

    def __init__(
        self, types: list[type] | type, response_class: type[Response] | None = None
    ):
        if isinstance(types, type):
            types = [types]
        self.types = types
        self.response_class: type[Response] | None = response_class

    @abstractmethod
    async def encode(self, request: Request | WebSocket, name: str, annotation: type):
        """
        Transform the request data into usable endpoint data.

        Args:
            request (Request): The request object.
            name (str): The name of the data.
            annotation (type): The type annotation of the data.

        Returns:
            dict: A dictionary containing the name and the transformed data.
        """
        return None

    @abstractmethod
    async def decode(self, request: Request, response: Any):
        """
        Transform the response data into usable response data.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response: A response class that can be used by the starlette app.
        """
        if type(response) in STARLETTE_RESPONSE:
            return response
        if type(response) in [int, float, str, bool]:
            return Response(content=str(response))
        return None

    @abstractmethod
    async def exception(self, request: Request, exception: Exception):
        """
        Transform the exception data into usable response data.

        Args:
            request (Request): The request object.
            exception (Exception): The exception data.

        Returns:
            Response: A response class that can be used by the starlette app.
        """
        return None


async def encode_request(
    request: Request | WebSocket,
    endpoint_func: Callable,
    processor_func: list[BaseProcessor],
):
    """
    Encodes the request data for an endpoint.
    """
    data = {}

    params = inspect.signature(endpoint_func).parameters

    for name, annotation in params.items():
        if annotation.annotation in [Request]:
            data.update({name: request})
        for processor in processor_func:
            processed = await processor.encode(request, name, annotation.annotation)
            if processed:
                data.update(processed)

    return data


async def decode_response(
    request: Request, response: Any, processor_func: list[BaseProcessor]
) -> Response | None:
    """
    Decodes the response data for an endpoint.

    Args:
        request (Request): The request object.
        response (Any): The response object.
        processor_func (list[BaseProcessor]): A list of processor functions.

    Returns:
        Response | None:
    """
    for processor in processor_func:
        decoded = await processor.decode(request, response)
        if decoded:
            return decoded
    return None


async def exception_response(
    request: Request, exception: Exception, processor_func: list[BaseProcessor]
) -> Response | None:
    """Handles exceptions by passing them to a list of processor functions.

    Args:
        request (Request): The request object.
        exception (Exception): The exception that occurred.
        processor_func (list[BaseProcessor]): A list of processor functions.

    Returns:
        Response | None:
    """
    for processor in processor_func:
        decoded = await processor.exception(request, exception)
        if decoded:
            return decoded
    return None
