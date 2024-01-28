"""
This module defines the conventions used in the pypox library for defining HTTP and websocket endpoints.

Classes:
    BaseConvention: Base class for conventions in the pypox library.
    HTTPConvention: Represents a convention for HTTP endpoints.
    WebsocketConvention: Represents a convention for websocket endpoints.
"""
from importlib.machinery import ModuleSpec
from inspect import iscoroutinefunction
import os
from types import ModuleType
from typing import Any, Callable, Generator
import importlib.util
from starlette.routing import BaseRoute, Route, WebSocketRoute, Router
from starlette.requests import Request
from starlette.responses import Response
from pypox.processor.base import (
    ProcessorWrapper,
)


class BaseConvention:
    """
    Base class for conventions in the pypox library.

    Attributes:
        name (str): The name of the convention.
        type (str): The type of the convention.
        files (list[str]): The list of files associated with the convention.
        callable (str): The name of the callable function in the module.
        directory (str): The directory path where the convention is defined.

    Methods:
        __init__(self,
        processor_func: list[BaseProcessor] | None,
        name: str, type: str,
        files: list[str],
        callable: str,
        directory: str) -> None:
            Initializes a BaseConvention object.
        __call__(self) -> list[BaseRoute]:
            Calls the convention and returns a list of BaseRoute objects.
        processor(self, func) -> Any:
            Decorator function that wraps the callable function with additional processing logic.
    """

    def __init__(
        self,
        name: str,
        _type: str,
        files: dict[str, str],
        _callable: str,
        directory: str,
    ) -> None:
        self._name = name
        self._type = _type
        self._files: dict[str, str] = files
        self._callable = _callable
        self._directory = directory
        self._processor_func: list[Callable] = []

    def add_processor(self, processor_func: list[Callable] | Callable | None) -> None:
        """
        Sets the processor function.

        Args:
            processor_func (list[BaseProcessor] | BaseProcessor | None): The list of processor functions.
        """
        if isinstance(processor_func, list):
            self._processor_func.extend(processor_func)
        elif isinstance(processor_func, Callable):
            self._processor_func.append(processor_func)
        else:
            raise ValueError("Processor function cannot be None")

    @property
    def processor_func(self) -> list[Callable]:
        """
        The list of processor functions.
        """
        return self._processor_func

    @property
    def name(self) -> str:
        """
        The name of the convention.
        """
        return self._name

    @property
    def type(self) -> str:
        """
        The type of the convention.
        """
        return self._type

    @property
    def files(self) -> dict[str, str]:
        """
        The list of files associated with the convention.
        """
        return self._files

    @property
    def callable(self) -> str:
        """
        The name of the callable function in the module.
        """
        return self._callable

    @property
    def directory(self) -> str:
        """
        The directory path where the convention is defined.
        """
        return self._directory

    def __call__(self, processor_list: list[Callable]) -> Router:
        """
        Retrieves a list of BaseRoute objects based on the specified directory and files.

        Returns:
            A list of BaseRoute objects representing the routes defined in the specified directory and files.
        """
        self.add_processor(processor_list)
        router: list[BaseRoute] = []

        for root, file in self.walk():
            module_name: str = file.split(".")[0]
            module_path: str = os.path.join(root, file)

            module: ModuleType = self.load_module(module_name, module_path)

            route_path: str = self.create_route_path(self.directory, root)
            router.append(self.add_route(route_path, getattr(module, self.callable)))

        return Router(router)

    def add_route(
        self, route_path: str, func: Callable, methods: list[str] | None = None
    ) -> Route | WebSocketRoute:
        """Add a route to the application.

        This method is used to add a route to the application. It takes the route path,
        the handler function, and an optional list of HTTP methods as parameters.

        Args:
            route_path (str): # The path of the route.
            func (Callable): # The handler function for the route.
            methods (list[str] | None, optional): # The list of HTTP methods allowed for the route.
            If not provided, the default method is "GET". Defaults to None.
        Raises:
            ValueError: If the route type is invalid.

        Returns:
            Route | WebSocketRoute: The created route object.
        """
        if self.type == "http":
            if not methods:
                methods = ["GET"]
            return Route(
                route_path,
                endpoint=ProcessorWrapper(func, self.processor_func).__call__,
                methods=methods,
            )
        if self.type == "websocket":
            return WebSocketRoute(
                route_path,
                ProcessorWrapper(func, self.processor_func).__call__,
            )
        raise ValueError("Invalid route type")

    def walk(self) -> Generator[tuple[str, str], Any, None]:
        """Recursively walks through the directory and yields tuples of root and file names.

        Yields:
            Generator[tuple[str, str], Any, None]: A generator that yields tuples of root and file names.
        """
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file in self.files:
                    yield root, file

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


class HTTPConvetion(BaseConvention):
    """Represents a convention for HTTP endpoints.

    Args:
        BaseConvention (type): The base convention class.

    Attributes:
        name (str): The name of the convention.
        protocol (str): The protocol used by the convention.
        files (List[str]): The list of files associated with the convention.
        endpoint_type (str): The type of endpoint.
        directory (str): The directory where the convention is defined.
    """

    def __init__(
        self,
        directory: str,
    ) -> None:
        super().__init__(
            "HTTPConvention",
            "http",
            {
                "get.py": "GET",
                "post.py": "POST",
                "put.py": "PUT",
                "delete.py": "DELETE",
                "patch.py": "PATCH",
                "head.py": "HEAD",
                "options.py": "OPTIONS",
            },
            "endpoint",
            directory,
        )


class WebsocketConvention(BaseConvention):
    """
    A class representing a websocket convention.

    Args:
        BaseConvention (type): The base convention class.

    Attributes:
        directory (str): The directory where the convention is located.

    """

    def __init__(
        self,
        directory: str,
    ) -> None:
        """
        Initializes a new instance of the WebsocketConvention class.

        Args:
            directory (str): The directory where the convention is located.

        """
        super().__init__(
            "WebsocketConvention",
            "websocket",
            {"websocket.py": "WEBSOCKET"},
            "endpoint",
            directory,
        )


class HTMXConvention(BaseConvention):
    """
    A class representing the HTMX convention.

    Args:
        BaseConvention (type): The base convention class.
    """

    def __init__(self, directory: str) -> None:
        super().__init__(
            "HTMXConvention",
            "http",
            {"htmx.py": "GET"},
            "endpoint",
            directory,
        )
