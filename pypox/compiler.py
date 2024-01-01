from contextlib import asynccontextmanager
from types import ModuleType
import importlib.util
import os
from fastapi import APIRouter, FastAPI
from typing import Any, AsyncGenerator, Callable, Optional

from typing import List

FILE_CONVENTIONS: List[str] = [
    "socket.py",
    "config.py",
    "startup.py",
    "shutdown.py",
    "get.py",
    "post.py",
    "put.py",
    "delete.py",
    "patch.py",
    "options.py",
    "head.py",
    "license.md",
    "connection.py",
]

FASTAPI_PARAMETERS: List[str] = [
    "debug",
    "routes",
    "title",
    "summary",
    "description",
    "version",
    "openapi_url",
    "openapi_tags",
    "servers",
    "dependencies",
    "default_response_class",
    "redirect_slashes",
    "docs_url",
    "redoc_url",
    "swagger_ui_oauth2_redirect_url",
    "swagger_ui_init_oauth",
    "middleware",
    "exception_handlers",
    "on_startup",
    "on_shutdown",
    "lifespan",
    "terms_of_service",
    "contact",
    "license_info",
    "openapi_prefix",
    "root_path",
    "root_path_in_servers",
    "responses",
    "callbacks",
    "webhooks",
    "deprecated",
    "include_in_schema",
    "swagger_ui_parameters",
    "generate_unique_id_function",
    "separate_input_output_schemas",
]

API_ROUTER_PARAMETERS: List[str] = [
    "prefix",
    "tags",
    "dependencies",
    "default_response_class",
    "responses",
    "callbacks",
    "routes",
    "redirect_slashes",
    "default",
    "dependency_overrides_provider",
    "route_class",
    "deprecated",
    "include_in_schema",
    "generate_unique_id_function",
]

API_HTTP_VERBS: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

API_HTTP_PARAMETERS: List[str] = [
    "response_model",
    "status_code",
    "tags",
    "dependencies",
    "summary",
    "description",
    "response_description",
    "responses",
    "deprecated",
    "operation_id",
    "response_model_include",
    "response_model_exclude",
    "response_model_by_alias",
    "response_model_exclude_unset",
    "response_model_exclude_defaults",
    "response_model_exclude_none",
    "include_in_schema",
    "response_class",
    "name",
    "callbacks",
    "openapi_extra",
    "generate_unique_id_function",
]


class Pypox:
    def __init__(self, directory: str) -> None:
        """
        Initializes an instance of the class.

        Parameters:
            directory (str): The directory path.

        Returns:
            None
        """
        self.directory: str = directory
        self.main_api: Optional[FastAPI] = None  # type: ignore
        self.python_modules: dict[str, List[ModuleType]] = {}
        self.get_modules()

    def get_modules(self) -> "Pypox":
        """
        Get the list of modules in the specified directory.

        Returns:
            Pypox: The current instance of Pypox.
        """
        for root, dirs, files in os.walk(f"{self.directory}"):
            folder_modules: List[ModuleType] = []
            for file in files:
                if file not in FILE_CONVENTIONS:
                    continue
                if ".py" in file:
                    module_name: str = os.path.splitext(file)[0]
                    module_path: str = os.path.join(root, file)
                    spec: ModuleType = importlib.util.spec_from_file_location(module_name, module_path)  # type: ignore
                    module: ModuleType = importlib.util.module_from_spec(spec)  # type: ignore
                    spec.loader.exec_module(module)  # type: ignore
                    folder_modules.append(module)

                    self.python_modules[
                        root.replace("[", "{")
                        .replace("]", "}")
                        .replace("\\routes\\", "/")
                    ] = folder_modules
        return self

    def __create_lifespan(self, modules: List[ModuleType]) -> Callable | None:
        """
        Creates a lifespan context manager function based on the provided modules.

        Parameters:
            modules (List[ModuleType]): The list of modules to check for the presence of "startup" and "shutdown" functions.

        Returns:
            Callable | None: The lifespan context manager function if both "startup" and "shutdown" functions are present in the modules, otherwise None.
        """
        if "startup" not in [x.__name__ for x in modules] or "shutdown" not in [
            x.__name__ for x in modules
        ]:
            return None

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
            await [x.__call__ for x in modules if x.__name__ == "startup"][0](app)
            yield
            await [x.__call__ for x in modules if x.__name__ == "shutdown"][0](app)

        return lifespan

    def __create_config(self, modules: List[ModuleType], type: str) -> dict[str, Any]:
        config: dict[str, Any] = {}
        """
        Generates a configuration dictionary based on the given modules and type.

        Args:
            modules (List[Type[ModuleType]]): The list of modules to generate the configuration from.
            type (str): The type of configuration to generate. Valid values are "FastAPI" and "API_ROUTER".

        Returns:
            Dict[str, Any]: The generated configuration dictionary.
        """
        parameters: List[str] = (
            FASTAPI_PARAMETERS if type == "FastAPI" else API_ROUTER_PARAMETERS
        )

        for module in modules:
            for parameter in parameters:
                if hasattr(module, parameter):
                    config[parameter] = getattr(module, parameter)

        return config

    def __get_endpoints(
        self, modules: list[ModuleType]
    ) -> tuple[list[Callable], list[dict[str, Any]]]:
        """
        Generates a list of endpoints and their corresponding configurations based on a list of modules.

        Args:
            modules (list[ModuleType]): A list of modules containing endpoint information.

        Returns:
            tuple[list[Callable], list[dict[str, Any]]]: A tuple containing two lists:
                - endpoints: A list of endpoint functions.
                - configs: A list of endpoint configurations.

        Raises:
            AssertionError: If an endpoint is not found in a module.
        """
        endpoints: list[Callable] = []
        configs: list[dict[str, Any]] = []
        for module in modules:
            if (
                module.__name__.upper() not in API_HTTP_VERBS
                and module.__name__ != "socket"
            ):
                continue

            assert hasattr(module, "endpoint"), "endpoint not found in module"
            endpoints.append(getattr(module, "endpoint"))
            api_config: dict[str, Any] = {
                key: getattr(module, key)
                for key in API_HTTP_PARAMETERS
                if hasattr(module, key)
            }
            api_config["methods"] = [module.__name__.upper()]
            configs.append(api_config)
        return endpoints, configs

    def __call__(self, *args: Any, **kwds: Any) -> FastAPI:
        """
        Execute the function when the class instance is called.

        Args:
            *args: Variable length arguments.
            **kwds: Keyword arguments.

        Returns:
            Any: The return value of the function.
        """
        for root, modules in self.python_modules.items():
            endpoints, configs = self.__get_endpoints(modules)
            if root == self.directory:
                lifespan: Callable[[], None] | None = self.__create_lifespan(modules)
                config: dict[str, Any] = self.__create_config(modules, "FastAPI")
                self.main_api: FastAPI = FastAPI(**config, lifespan=lifespan)  # type: ignore

            if self.main_api and root == self.directory:
                for endpoint, endpoint_config in zip(endpoints, configs):
                    if endpoint_config["methods"][0] == "SOCKET":
                        self.main_api.add_api_websocket_route(
                            path=root.replace(self.directory, "").replace("\\", "/")
                            + "/",
                            endpoint=endpoint,
                            **{
                                key: val
                                for key, val in endpoint_config.items()
                                if key != "methods"
                            },
                        )
                        continue
                    self.main_api.add_api_route(
                        path=root.replace(self.directory, "").replace("\\", "/") + "/",
                        name=f"{endpoint_config['methods'][0]}_Endpoint",
                        endpoint=endpoint,
                        **endpoint_config,
                    )
            elif self.main_api and root != self.directory:
                config: dict[str, Any] = self.__create_config(modules, "APIRouter")
                router: APIRouter = APIRouter(**config)
                for endpoint, endpoint_config in zip(endpoints, configs):
                    if endpoint_config["methods"][0] == "SOCKET":
                        self.main_api.add_api_websocket_route(
                            path=root.replace(self.directory, "").replace("\\", "/")
                            + "/",
                            endpoint=endpoint,
                            **{
                                key: val
                                for key, val in endpoint_config.items()
                                if key != "methods"
                            },
                        )
                        continue
                    router.add_api_route(
                        path=root.replace(self.directory, "").replace("\\", "/") + "/",
                        name=f"{endpoint_config['methods'][0]}_Endpoint",
                        endpoint=endpoint,
                        **endpoint_config,
                    )
                self.main_api.include_router(router)

        return self.main_api
