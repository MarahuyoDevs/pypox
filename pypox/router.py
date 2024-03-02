from contextlib import AbstractAsyncContextManager
from importlib.machinery import ModuleSpec
from typing import Any, Callable, Generator, Sequence
from starlette.middleware import Middleware
from starlette.routing import BaseRoute, Router, Route, WebSocketRoute
from starlette.types import ASGIApp
from typing import MutableMapping, Awaitable, Mapping
from types import ModuleType
import importlib.util
import os


class BaseRouter(Router):

    def __init__(
        self,
        directory: str,
        entry_point: str,
        file: dict[str, str],
        _type: str = "http",
        redirect_slashes: bool = True,
        default: (
            Callable[
                [
                    MutableMapping[str, Any],
                    Callable[[], Awaitable[MutableMapping[str, Any]]],
                    Callable[[MutableMapping[str, Any]], Awaitable[None]],
                ],
                Awaitable[None],
            ]
            | None
        ) = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: (
            Callable[[Any], AbstractAsyncContextManager[None]]
            | Callable[[Any], AbstractAsyncContextManager[Mapping[str, Any]]]
            | None
        ) = None,
        *,
        middleware: Sequence[Middleware] | None = None
    ) -> None:

        self._router_type = _type
        self._callable = entry_point
        self._directory = directory
        self._file = file
        super().__init__(
            self.generate_routes(),
            redirect_slashes,
            default,
            on_startup,
            on_shutdown,
            lifespan,
            middleware=middleware,
        )

    @property
    def directory(self) -> str:
        return self._directory

    @property
    def callable(self) -> str:
        return self._callable

    @property
    def router_type(self) -> str:
        return self._router_type

    def generate_routes(self) -> list[Route | WebSocketRoute]:
        router: list[Route | WebSocketRoute] = []

        for root, file in self.walk():
            module_name: str = file.split(".")[0]
            module_path: str = os.path.join(root, file)

            module: ModuleType = self.load_module(module_name, module_path)

            route_path: str = self.create_route_path(self.directory, root)
            router.append(
                self.create_route(
                    route_path,
                    getattr(module, self.callable),
                    methods=[self._file[file]],
                )
            )

        return router

    def walk(self) -> Generator[tuple[str, str], Any, None]:
        """Recursively walks through the directory and yields tuples of root and file names.

        Yields:
            Generator[tuple[str, str], Any, None]: A generator that yields tuples of root and file names.
        """
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file in self._file:
                    yield root, file

    def load_module(self, module_name: str, module_path: str) -> ModuleType:
        """
        Load a module from a file location.

        Args:
            module_name (str): The name of the module.
            module_path (str): The path to the module file.

        Raises:
            ModuleNotFoundError: If the module is not found.
            AttributeError: If the callable is not found in the module.

        Returns:
            ModuleType: The loaded module.
        """
        spec: ModuleSpec | None = importlib.util.spec_from_file_location(
            module_name, module_path
        )
        if not spec:
            raise ModuleNotFoundError("Module not found")
        module: ModuleType = importlib.util.module_from_spec(spec)
        if not spec.loader:
            raise ModuleNotFoundError("Module not found")
        spec.loader.exec_module(module)
        if not hasattr(module, self.callable):
            raise AttributeError("Callable not found in module")
        return module

    def create_route_path(self, directory: str, root: str) -> str:
        """
        Create a route path by replacing the directory in the root path and performing some string replacements.

        Args:
            directory (str): The directory to be replaced in the root path.
            root (str): The root path.

        Returns:
            str: The modified route path.
        """
        return (
            root.replace(directory, "")
            .replace("\\", "/")
            .replace("[", "{")
            .replace("]", "}")
            + "/"
        )

    def create_route(
        self, route_path: str, func: Callable, methods: list[str] = ["GET"]
    ) -> Route | WebSocketRoute:
        """
        Create a route with the given path and endpoint.

        Args:
            route_path (str): The path of the route.
            endpoint (Callable): The endpoint of the route.

        Returns:
            BaseRoute: The created route.
        """

        if self.router_type == "http":
            return Route(route_path, func, methods=methods)

        if self.router_type == "websocket":
            return WebSocketRoute(route_path, func, name=func.__name__)

        raise ValueError("Invalid router type")


class HTTPRouter(BaseRouter):

    def __init__(
        self,
        directory: str,
        entry_point: str = "endpoint",
        file: dict[str, str] = {},
        _type: str = "http",
        redirect_slashes: bool = True,
        default: (
            Callable[
                [
                    MutableMapping[str, Any],
                    Callable[[], Awaitable[MutableMapping[str, Any]]],
                    Callable[[MutableMapping[str, Any]], Awaitable[None]],
                ],
                Awaitable[None],
            ]
            | None
        ) = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: (
            Callable[[Any], AbstractAsyncContextManager[None]]
            | Callable[[Any], AbstractAsyncContextManager[Mapping[str, Any]]]
            | None
        ) = None,
        *,
        middleware: Sequence[Middleware] | None = None
    ) -> None:

        if not file:
            file = {
                "get.py": "GET",
                "post.py": "POST",
                "put.py": "PUT",
                "delete.py": "DELETE",
                "patch.py": "PATCH",
                "head.py": "HEAD",
                "options.py": "OPTIONS",
            }

        super().__init__(
            directory,
            entry_point,
            file,
            _type,
            redirect_slashes,
            default,
            on_startup,
            on_shutdown,
            lifespan,
            middleware=middleware,
        )


class WebsocketRouter(BaseRouter):

    def __init__(
        self,
        directory: str,
        entry_point: str = "endpoint",
        file: dict[str, str] = {},
        _type: str = "websocket",
        redirect_slashes: bool = True,
        default: (
            Callable[
                [
                    MutableMapping[str, Any],
                    Callable[[], Awaitable[MutableMapping[str, Any]]],
                    Callable[[MutableMapping[str, Any]], Awaitable[None]],
                ],
                Awaitable[None],
            ]
            | None
        ) = None,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: (
            Callable[[Any], AbstractAsyncContextManager[None]]
            | Callable[[Any], AbstractAsyncContextManager[Mapping[str, Any]]]
            | None
        ) = None,
        *,
        middleware: Sequence[Middleware] | None = None
    ) -> None:

        if not file:
            file = {"websocket.py": "WEBSOCKET"}
        super().__init__(
            directory,
            entry_point,
            file,
            _type,
            redirect_slashes,
            default,
            on_startup,
            on_shutdown,
            lifespan,
            middleware=middleware,
        )
