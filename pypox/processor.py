import inspect
from typing import Any, Callable
from pydantic import BaseModel
from starlette.responses import Response, JSONResponse, HTMLResponse
from starlette.requests import Request
from jinja2 import Environment, FileSystemLoader, Template


class BaseProcessor:
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

    async def encode(self, request: Request, name: str, annotation: type):
        """
        Transform the request data into usable endpoint data.

        Args:
            request (Request): The request object.
            name (str): The name of the data.
            annotation (type): The type annotation of the data.

        Returns:
            dict: A dictionary containing the name and the transformed data.
        """
        pass

    async def decode(self, request: Request, response: Any):
        """
        Transform the response data into usable response data.

        Args:
            request (Request): The request object.
            response (Any): The response data.

        Returns:
            Response: A response class that can be used by the starlette app.
        """
        pass


class QueryProcessor(BaseProcessor):
    def __init__(
        self,
        types: list[type] = [],
        response_class: type[Response] | None = None,
    ):
        super().__init__([int, float, str, bool] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.query_params:
            return {name: annotation(request.query_params[name])}
        else:
            return None


class PathProcessor(BaseProcessor):
    def __init__(
        self,
        types: list[type] = [],
        response_class: type[Response] | None = None,
    ):
        super().__init__([int, float, str, bool] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.path_params:
            return {name: annotation(request.path_params[name])}
        else:
            return None


class JSONProcessor(BaseProcessor):
    def __init__(
        self,
        types: list[type] = [],
        response_class: type[Response] | None = JSONResponse,
    ) -> None:
        super().__init__([list, dict] + types, response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types:
            return {name: annotation(await request.json())}
        else:
            return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        if type(response) in self.types:
            if self.response_class:
                return self.response_class(content=response)
        return None


class CookieProcessor(BaseProcessor):
    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.cookies:
            return {name: annotation(request.cookies[name])}
        else:
            return None


class HeaderProcessor(BaseProcessor):
    def __init__(self, response_class: type[Response] | None = None):
        super().__init__([str], response_class)

    def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if annotation in self.types and name in request.headers:
            return {name.replace("-", "_"): annotation(request.headers[name])}
        else:
            return None


class PydanticProcessor(BaseProcessor):
    def __init__(
        self,
        response_class: type[Response] | None = JSONResponse,
    ):
        super().__init__([BaseModel], response_class)

    async def encode(
        self, request: Request, name: str, annotation: type
    ) -> dict[str, Any] | None:
        if issubclass(annotation, BaseModel):
            return {name: annotation(**(await request.json()))}
        else:
            return None

    async def decode(self, request: Request, response: Any) -> Response | None:
        if issubclass(type(response), BaseModel) and self.response_class:
            return self.response_class(content=response.model_dump())


class JinjaProcessor(BaseProcessor):
    def __init__(
        self, template_dir: str, response_class: type[Response] | None = HTMLResponse
    ):
        super().__init__([], response_class)
        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            line_statement_prefix="#",
            line_comment_prefix="##",
            enable_async=True,
        )
        self.convention: dict = {
            "page": "page.html",
            "layout": "layout.html",
            "error": "error.html",
        }

    def decode(self, request: Request, response: Any):
        if "text/html" in request.headers.get("accept", "").split(","):
            page: Template = self.environment.get_template(
                request.url.path + self.convention["page"]
            )
            if self.response_class:
                return self.response_class(content=page.render(**self.convention))
        return None


async def encode_request(
    request: Request, endpoint_func: Callable, processor_func: list[BaseProcessor]
):
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
    for processor in processor_func:
        decoded = await processor.decode(request, response)
        if decoded:
            return decoded
    return None
