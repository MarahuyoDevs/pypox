#### `__init__`

```python
def __init__(directory: str) -> None:
```

**Purpose:** Initializes an instance of the class.

- **Parameters:**
  - `directory` (str): The directory path.
- **Returns:** None.

---

#### get_modules

```python
def get_modules(self) -> self
```

**Purpose:** Get the list of modules in the specified directory.

- **Returns:** The current instance of Pypox.

---

#### \_\_create_lifespan

```python
def __create_lifespan(modules: List[ModuleType]) -> Callable | None
```

**Purpose:** Creates a lifespan context manager function based on the provided modules.

- **Parameters:**
  - `modules` (List[ModuleType]): The list of modules to check for the presence of "startup" and "shutdown" functions.
- **Returns:** The lifespan context manager function if both "startup" and "shutdown" functions are present in the modules, otherwise None.

---

#### \_\_create_config

```python
def __create_config(modules: List[ModuleType], type: str) -> dict[str, Any]
```

**Purpose:** Generates a configuration dictionary based on the given modules and type.

- **Parameters:**
  - `modules` (List[Type[ModuleType]]): The list of modules to generate the configuration from.
  - `type` (str): The type of configuration to generate. Valid values are "FastAPI" and "API_ROUTER".
- **Returns:** The generated configuration dictionary.

---

#### \_\_get_endpoints

```python
def __get_endpoints(modules: list[ModuleType]) -> tuple[list[Callable], list[dict[str, Any]]]
```

**Purpose:** Generates a list of endpoints and their corresponding configurations based on a list of modules.

- **Parameters:**
  - `modules` (list[ModuleType]): A list of modules containing endpoint information.
- **Returns:** A tuple containing two lists: endpoints (A list of endpoint functions) and configs (A list of endpoint configurations).

---

#### \_\_call\_\_

```python
def __call__(*args: Any, **kwds: Any) -> FastAPI
```

**Purpose:** Execute the function when the class instance is called.

- **Parameters:**
  - `*args`: Variable length arguments.
  - `**kwds`: Keyword arguments.
- **Returns:** The return value of the function.

---
