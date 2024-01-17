import os
from typing import Any, Callable, Mapping, Sequence, TypeVar, ParamSpec
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Route, Router, Mount
from starlette.types import ExceptionHandler, Lifespan

P = ParamSpec("P")


class Pypox(Starlette):
    def __init__(
        self,
        conventions: list,
        debug: bool = False,
        middleware: Sequence[Middleware] | None = None,
        exception_handlers: Mapping[Any, ExceptionHandler] | None = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan | None = None,
    ) -> None:
        routes = []

        for convention in conventions:
            routes.extend(convention())
        super().__init__(
            debug,
            routes,
            middleware,
            exception_handlers,
            on_startup,
            on_shutdown,
            lifespan,
        )
