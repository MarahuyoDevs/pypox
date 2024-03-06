from contextlib import AbstractAsyncContextManager
from importlib.machinery import ModuleSpec
from typing import Any, Callable, Generator, Sequence
from starlette.middleware import Middleware
from starlette.routing import BaseRoute, Router, Route, WebSocketRoute
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint
from starlette.types import ASGIApp
from typing import MutableMapping, Awaitable, Mapping
from types import ModuleType
import importlib.util
import os


class BaseRouter(Router):
    """
    A base router class for handling HTTP and WebSocket routes.

    Args:
        Router (type): The base router class.

    Attributes:
        directory (str): The directory path where the routes are located.
        entry_point (str): The entry point for the routes.
        file (dict[str, str]): A dictionary mapping file names to their types.
        class_callable (str): The name of the class callable for router or websocket routes.
        _type (str): The type of the router (http or websocket).
        redirect_slashes (bool): Whether to redirect trailing slashes in the routes.
        default (Callable[[MutableMapping[str, Any], Callable[[], Awaitable[MutableMapping[str, Any]]], Callable[[MutableMapping[str, Any]], Awaitable[None]]], Awaitable[None]] | None): The default handler for routes.
        on_startup (Sequence[Callable[[], Any]] | None): A sequence of functions to be called on startup.
        on_shutdown (Sequence[Callable[[], Any]] | None): A sequence of functions to be called on shutdown.
        lifespan (Callable[[Any], AbstractAsyncContextManager[None]] | Callable[[Any], AbstractAsyncContextManager[Mapping[str, Any]]] | None): A callable that manages the lifespan of the router.
        middleware (Sequence[Middleware] | None): A sequence of middleware functions to be applied to the routes.
    """

    def __init__(
        self,
        directory: str,
        entry_point: str,
        file: dict[str, str],
        class_callable: str = "endpoints",
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
        middleware: Sequence[Middleware] | None = None,
    ) -> None:

        self._router_type = _type
        self._callable = entry_point
        self._class_callable = class_callable
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
        """Returns the directory associated with the router.

        Returns:
            str: The directory path.
        """
        return self._directory

    @property
    def callable(self) -> str:
        return self._callable

    @property
    def router_type(self) -> str:
        """Returns the type of the router.

        Returns:
            str: The type of the router.
        """
        return self._router_type

    def generate_routes(self) -> list[Route | WebSocketRoute]:
        """Generates routes based on the files in the directory.

        Returns:
            list[Route | WebSocketRoute]: A list of routes generated from the files.
        """
        router: list[Route | WebSocketRoute] = []

        for root, file in self.walk():
            module_name: str = file.split(".")[0]
            module_path: str = os.path.join(root, file)

            module: ModuleType = self.load_module(module_name, module_path)

            route_path: str = self.create_route_path(self.directory, root)

            if self._file[file] in ["router", "websocket"]:
                router.append(
                    self.create_route(
                        route_path,
                        getattr(module, self._class_callable),
                    )
                )
            else:
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
        if not hasattr(module, self.callable) and not hasattr(
            module, self._class_callable
        ):
            raise AttributeError(f"Callable {module_name} not found in module")
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
        self,
        route_path: str,
        obj: Callable | type[HTTPEndpoint] | type[WebSocketEndpoint],
        methods: list[str] = ["GET"],
    ) -> Route | WebSocketRoute:
        """
        Create a route with the given path and endpoint.

        Args:
            route_path (str): The path of the route.
            endpoint (Callable): The endpoint of the route.

        Returns:
            BaseRoute: The created route.
        """
        if issubclass(type(obj), WebSocketEndpoint):
            return WebSocketRoute(route_path, obj, name=obj.__name__)

        if issubclass(type(obj), HTTPEndpoint):
            return Route(route_path, obj, methods=methods)

        if self.router_type == "http":
            return Route(route_path, obj, methods=methods)

        if self.router_type == "websocket":
            return WebSocketRoute(route_path, obj, name=obj.__name__)

        raise ValueError("Invalid router type")


class HTTPRouter(BaseRouter):
    """A router class for handling HTTP requests.

    Args:
        BaseRouter (type): The base router class.

    Attributes:
        directory (str): The directory where the router files are located.
        callable (str): The name of the callable function in the router files.
        class_callable (str): The name of the class containing the router files.
        file (dict[str, str]): A dictionary mapping file names to HTTP methods.
        _type (str): The type of router (in this case, "http").
        redirect_slashes (bool): Whether to redirect trailing slashes in URLs.
        default (Callable): The default handler for requests that don't match any route.
        on_startup (Sequence[Callable]): A sequence of functions to run on startup.
        on_shutdown (Sequence[Callable]): A sequence of functions to run on shutdown.
        lifespan (Callable): A function that returns an async context manager for the router's lifespan.
        middleware (Sequence[Middleware]): A sequence of middleware functions to apply to requests.

    """

    def __init__(
        self,
        directory: str,
        callable: str = "endpoint",
        class_callable: str = "Endpoints",
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
        middleware: Sequence[Middleware] | None = None,
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
                "router.py": "router",
            }

        super().__init__(
            directory,
            callable,
            file,
            class_callable,
            _type,
            redirect_slashes,
            default,
            on_startup,
            on_shutdown,
            lifespan,
            middleware=middleware,
        )


class WebsocketRouter(BaseRouter):
    """
    A router for handling WebSocket connections.

    This router is responsible for handling WebSocket connections in a web application.

    Args:
        BaseRouter (type): The base router class to inherit from.

    Attributes:
        directory (str): The directory where the router is located.
        entry_point (str): The entry point for the router.
        class_callable (str): The name of the class that contains the endpoints.
        file (dict[str, str]): A dictionary mapping file names to file types.
        _type (str): The type of router.
        redirect_slashes (bool): Whether to redirect trailing slashes in URLs.
        default (Callable[[MutableMapping[str, Any], Callable[[], Awaitable[MutableMapping[str, Any]]], Callable[[MutableMapping[str, Any]], Awaitable[None]]], Awaitable[None]] | None): The default handler for requests.
        on_startup (Sequence[Callable[[], Any]] | None): A sequence of functions to run on application startup.
        on_shutdown (Sequence[Callable[[], Any]] | None): A sequence of functions to run on application shutdown.
        lifespan (Callable[[Any], AbstractAsyncContextManager[None]] | Callable[[Any], AbstractAsyncContextManager[Mapping[str, Any]]] | None): A function that returns an async context manager for managing the lifespan of the application.
        middleware (Sequence[Middleware] | None): A sequence of middleware functions to apply to requests.

    """

    def __init__(
        self,
        directory: str,
        entry_point: str = "endpoint",
        class_callable: str = "Endpoints",
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
        middleware: Sequence[Middleware] | None = None,
    ) -> None:

        if not file:
            file = {"websocket.py": "websocket"}
        super().__init__(
            directory,
            entry_point,
            file,
            class_callable,
            _type,
            redirect_slashes,
            default,
            on_startup,
            on_shutdown,
            lifespan,
            middleware=middleware,
        )
