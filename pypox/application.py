"""
    This module contains the implementation of the Pypox web application framework based on Starlette.

    The module defines two classes:
    - Pypox: The main application class that extends the Starlette class.
    - PypoxHTMX: A class representing the PypoxHTMX application, which is a subclass of BaseRouter.

    Both classes provide methods for adding routes, handling requests, and configuring the application.

    The Pypox class is used as the base class for creating Pypox applications, while the PypoxHTMX class is used for creating Pypox applications with HTMX support.
"""

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
    """
    A web application framework based on Starlette.

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
        """
        Initialize the Pypox application.

        Args:
            conventions (list[BaseRouter] | None, optional): The list of conventions. Defaults to None.
            debug (bool, optional): Flag indicating whether debug mode is enabled. Defaults to False.
            middleware (Sequence[Middleware] | None, optional): The middleware stack. Defaults to None.
            exception_handlers (Mapping[Any, ExceptionHandler] | None, optional): The exception handlers. Defaults to None.
            on_startup (Sequence[Callable[[], Any]] | None, optional): The startup functions. Defaults to None.
            on_shutdown (Sequence[Callable[[], Any]] | None, optional): The shutdown functions. Defaults to None.
            lifespan (Lifespan | None, optional): The lifespan of the application. Defaults to None.
            open_api_version (str, optional): The OpenAPI version. Defaults to "3.0.3".
            info (Info, optional): The information about the application. Defaults to Info(title="Pypox", version="0.0.1", license=License(name="MIT")).
            license (License, optional): The license information. Defaults to License(name="MIT").
            validators (list[Any], optional): A list of validators. Defaults to [].
        """

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
        """
        Handle incoming requests.

        Args:
            scope (Scope): The request scope.
            receive (Receive): The receive function.
            send (Send): The send function.

        Returns:
            None: No return value.
        """

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
        """
        Add a new route to the application.

        Args:
            path (str): The URL path for the route.
            route (Callable): The function or method to be executed when the route is accessed.
            methods (List[str] | None, optional): The HTTP methods allowed for the route. Defaults to None.
            name (str | None, optional): The name of the route. Defaults to None.
            include_in_schema (bool, optional): Whether to include the route in the API schema. Defaults to True.
            validators (List[Callable[[Request], Awaitable[Response]  |  Response]]  |  None, optional):
                A list of validators to be applied to the request before executing the route. Defaults to None.
        """

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
    """
    A class representing the PypoxHTMX application.

    Args:
        BaseRouter (type): The base router class.

    Attributes:
        _openapi_version (str): The OpenAPI version.
        _info (Info): The information about the application.
        _license (License): The license information.
    """

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
        """
        Initialize the PypoxHTMX application.

        Args:
            directory (str | None, optional): The directory for the application. Defaults to None.
            middleware (Sequence[Middleware] | None, optional): The middleware stack. Defaults to None.
            on_startup (Sequence[Callable[[], Any]] | None, optional): The startup functions. Defaults to None.
            on_shutdown (Sequence[Callable[[], Any]] | None, optional): The shutdown functions. Defaults to None.
            lifespan (Lifespan | None, optional): The lifespan of the application. Defaults to None.
            open_api_version (str, optional): The OpenAPI version. Defaults to "3.0.3".
            info (Info, optional): The information about the application. Defaults to Info(title="Pypox", version="0.0.1", license=License(name="MIT")).
            license (License, optional): The license information. Defaults to License(name="MIT").
        """

        self._openapi_version = open_api_version
        self._info = info
        self._license = license
        super().__init__(
            directory=directory or "", entry_point="page", file={"page.py": "GET"}
        )
        if self._directory:
            self._router = Starlette(
                routes=self.generate_routes(),
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
        """
        Handle incoming requests.

        Args:
            scope (MutableMapping[str, Any]): The request scope.
            receive (Callable[[], Awaitable[MutableMapping[str, Any]]]): The receive function.
            send (Callable[[MutableMapping[str, Any]], Awaitable[None]]): The send function.

        Returns:
            None: No return value.
        """

        if hasattr(self, "_router"):
            return await self._router(scope, receive, send)
        else:
            return await super().__call__(scope, receive, send)
