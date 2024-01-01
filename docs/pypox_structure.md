# `Pypox` Class Structure

#### `__init__(self, directory: str)`

- **Purpose:** Initializes an instance of the `Pypox` class with the specified directory path.
- **Parameters:**
  - `directory` (str): The path to the directory containing Python modules following specific naming conventions.
- **Returns:** None

#### `get_modules(self) -> "Pypox"`

- **Purpose:** Retrieves the list of modules within the specified directory following predefined file naming conventions.
- **Returns:** Instance of `Pypox`
- **Note:** Iterates through the directory's content, identifying and loading modules that adhere to predefined file naming conventions (`FILE_CONVENTIONS`). It utilizes `importlib` to dynamically load these modules.

#### `__create_lifespan(self, modules: List[ModuleType]) -> Callable | None`

- **Purpose:** Creates a context manager function to manage the application's lifespan based on presence of "startup" and "shutdown" functions in discovered modules.
- **Parameters:**
  - `modules` (List[ModuleType]): List of modules to check for "startup" and "shutdown" functions.
- **Returns:** A lifespan context manager function if both "startup" and "shutdown" functions are present in the modules, otherwise `None`.

#### `__create_config(self, modules: List[ModuleType], type: str) -> dict[str, Any]`

- **Purpose:** Generates configuration dictionaries for FastAPI and API routers based on module contents.
- **Parameters:**
  - `modules` (List[ModuleType]): List of modules to generate the configuration from.
  - `type` (str): Type of configuration to generate, either "FastAPI" or "APIRouter".
- **Returns:** Configuration dictionary containing parameters defined in `FASTAPI_PARAMETERS` or `API_ROUTER_PARAMETERS`.

#### `__get_endpoints(self, modules: list[ModuleType]) -> tuple[list[Callable], list[dict[str, Any]]]`

- **Purpose:** Extracts endpoints and their configurations from a list of modules.
- **Parameters:**
  - `modules` (list[ModuleType]): List of modules containing endpoint information.
- **Returns:**
  - Tuple containing:
    - `endpoints`: A list of endpoint functions.
    - `configs`: A list of endpoint configurations.

#### `__call__(self, *args: Any, **kwds: Any) -> FastAPI`

- **Purpose:** Executes the instance as a function to generate and configure the FastAPI application and API routers.
- **Parameters:**
  - `*args` (Any): Variable length arguments.
  - `**kwds` (Any): Keyword arguments.
- **Returns:** The constructed FastAPI application based on discovered modules and configurations.

#### `Note`

- The `Pypox` class orchestrates the dynamic integration of modules into the FastAPI application and API routers based on naming conventions. It automates the creation of routes, configuration parameters, and execution of startup/shutdown routines, allowing for a streamlined API setup process.
- Utilizing this class involves instantiating `Pypox`, calling it as a function, and obtaining a configured `FastAPI` instance ready for use.
