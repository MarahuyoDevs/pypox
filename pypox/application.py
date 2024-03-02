import os
from typing import (
    Any,
    Awaitable,
    Callable,
    List,
    Mapping,
    MutableMapping,
    Sequence,
    TypeVar,
    ParamSpec,
)
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route, Router, Mount, BaseRoute
from starlette.types import ExceptionHandler, Lifespan, Receive, Scope, Send
from pypox.processing.base import PypoxProcessor, processor
from pypox.router import BaseRouter
from pypox.openapi.main import OpenAPI, Info, License


class Pypox(Starlette):
    """A web application framework based on Starlette.

    Args:
        Starlette (type): The base class for the Pypox application.

    Attributes:
        processor_func (list[BaseProcessor] | None): The list of processor functions.
        conventions (list[BaseConvention]): The list of conventions.
        debug (bool): Flag indicating whether debug mode is enabled.
        middleware (Sequence[Middleware] | None): The middleware stack.
        exception_handlers (Mapping[Any, ExceptionHandler] | None): The exception handlers.
        on_startup (Sequence[Callable[[], Any]] | None): The startup functions.
        on_shutdown (Sequence[Callable[[], Any]] | None): The shutdown functions.
        lifespan (Lifespan | None): The lifespan of the application.
    """

    def __init__(
        self,
        conventions: list[BaseRouter] | None = None,
        debug: bool = False,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan | None = None,
        open_api_version: str = "3.0.3",
        info: Info = Info(title="Pypox", version="0.0.1", license=License(name="MIT")),
        license: License = License(name="MIT"),
        validators: list[Any] = [],
    ) -> None:
        self._openapi_version = open_api_version
        self._info = info
        self._license = license
        self._validators = validators
        routes: list[BaseRoute] = []
        if conventions:
            for convention in conventions:
                endpoints = convention.generate_routes()
                for endpoint in endpoints:
                    endpoint.endpoint = PypoxProcessor(
                        endpoint.endpoint, validators
                    ).validate
                routes.extend(endpoints)
        super().__init__(
            debug,
            routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
            lifespan,
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["openapi"] = {
            "openapi": self._openapi_version,
            "info": self._info,
            "license": self._license,
        }
        return await super().__call__(scope, receive, send)

    def add_route(
        self,
        path: str,
        route: Callable,
        methods: List[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
        validators: (
            List[Callable[[Request], Awaitable[Response] | Response]] | None
        ) = None,
    ) -> None:

        self.routes.append(
            Route(
                path,
                processor(validators or [])(route),
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
            )
        )


class PypoxHTMX(BaseRouter):

    def __init__(
        self,
        directory: str | None = None,
        middleware: Sequence[Middleware] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan | None = None,
        open_api_version: str = "3.0.3",
        info: Info = Info(title="Pypox", version="0.0.1", license=License(name="MIT")),
        license: License = License(name="MIT"),
    ) -> None:
        self._openapi_version = open_api_version
        self._info = info
        self._license = license
        super().__init__(
            directory=directory or "", entry_point="page", file={"page.py": "GET"}
        )
        if self._directory:
            self._router = Router(
                self.generate_routes(),
                middleware=middleware,
                on_startup=on_startup,
                on_shutdown=on_shutdown,
                lifespan=lifespan,
            )

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[[], Awaitable[MutableMapping[str, Any]]],
        send: Callable[[MutableMapping[str, Any]], Awaitable[None]],
    ) -> None:
        if hasattr(self, "_router"):
            return await self._router(scope, receive, send)
        else:
            return await super().__call__(scope, receive, send)
