import os
from typing import Any, Callable, Mapping, Sequence, TypeVar, ParamSpec
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route, Router, Mount, BaseRoute
from starlette.types import ExceptionHandler, Lifespan, Receive, Scope, Send
from pypox.conventions import BaseConvention


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
        processor_func: list[Callable] | None,
        conventions: list[BaseConvention],
        debug: bool = False,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan | None = None,
    ) -> None:
        routes: list[BaseRoute] = []
        for convention in conventions:
            if processor_func:
                routes.extend(convention(processor_func).routes)
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
        return await super().__call__(scope, receive, send)
