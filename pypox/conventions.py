from abc import abstractmethod
from importlib.machinery import ModuleSpec
from inspect import iscoroutinefunction, signature
from multiprocessing import process
from pydantic import BaseModel
import inspect
import os
from types import ModuleType
from typing import Any, Callable
from starlette.routing import Router, BaseRoute
from starlette.requests import Request
import importlib.util
from pypox.processor import BaseProcessor, encode_request, decode_response


class BaseConvention:
    
    name: str
    type: str
    files: list[str]
    callable: str
    directory: str

    def __init__(
        self,
        processor_func: list[BaseProcessor] | None,
        name: str,
        type: str,
        files: list[str],
        callable: str,
        directory: str,
    ) -> None:
        self.name = name
        self.type = type
        self.files: list[str] = files
        self.callable = callable
        self.directory = directory
        if not processor_func:
            self.processor_func: list[BaseProcessor] = []
        else:
            self.processor_func = processor_func

    def __call__(self) -> list[BaseRoute]:
        router = Router()

        for root, _, files in os.walk(self.directory):
            path_router = Router()
            for file in files:
                if file not in self.files:
                    continue
                module_name = file.split(".")[0]
                module_path = os.path.join(root, file)

                spec: ModuleSpec | None = importlib.util.spec_from_file_location(
                    module_name, module_path
                )
                if not spec:
                    continue
                module: ModuleType = importlib.util.module_from_spec(spec)
                if not spec.loader:
                    continue
                spec.loader.exec_module(module)
                if not hasattr(module, self.callable):
                    raise AttributeError("Callable not found in module")
                print(self.callable)
                router.add_route(
                    root.replace(self.directory, "")
                    .replace("\\", "/")
                    .replace("[", "{")
                    .replace("]", "}")
                    + "/",
                    self.processor(getattr(module, self.callable)),
                    methods=[file.split(".")[0].upper()],
                )

            """router.mount(
                root.replace(self.directory, "")
                .replace("\\", "/")
                .replace("[", "{")
                .replace("]", "}")
                + "/",
                path_router,
                name=root.replace(self.directory, ""),
            )"""

        return router.routes

    def processor(self, func) -> Any:
        async def wrapper(request: Request):
            if iscoroutinefunction(func):
                response = await func(
                    **(await encode_request(request, func, self.processor_func))
                )
            else:
                response = func(
                    **(await encode_request(request, func, self.processor_func))
                )
            return await decode_response(request, response, self.processor_func)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper


class HTTPConvetion(BaseConvention):
    def __init__(
        self, directory: str, processor_func: list[BaseProcessor] = []
    ) -> None:
        super().__init__(
            processor_func,
            "HTTPConvention",
            "http",
            ["get.py", "post.py", "put.py", "patch.py", "delete.py"],
            "endpoint",
            directory,
        )
