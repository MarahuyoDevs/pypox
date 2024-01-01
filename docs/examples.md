### Example:

Let's consider an example directory structure adhering to these conventions:

```
/project_directory
    |-- socket.py
    |-- config.py
    |-- startup.py
    |-- shutdown.py
    |-- get.py
    |-- post.py
    |-- put.py
    |-- delete.py
    |-- other_module.py
    |-- ...
```

In this scenario:

- `socket.py` handles socket-related operations.
- `config.py` stores application configurations.
- `startup.py` contains procedures executed on application startup.
- `shutdown.py` contains procedures executed on application shutdown.
- `get.py`, `post.py`, `put.py`, `delete.py`, and potentially other similar files each define endpoints for handling GET, POST, PUT, DELETE requests, respectively.

Pypox will recognize and utilize these modules for building the FastAPI application and API routers based on their functionalities and the defined conventions.

# Complex Example

Creating a more complex example using Pypox involves setting up a directory structure and implementing modules adhering to the specified naming conventions. Here's a hypothetical example demonstrating how Pypox can dynamically generate a FastAPI application with different modules handling various functionalities:

Let's create a directory structure following the conventions:

```
/my_api_project
    |-- socket.py
    |-- config.py
    |-- startup.py
    |-- shutdown.py
    |-- main.py
    |-- users
    |    |-- get.py
    |    |-- post.py
    |    |-- put.py
    |    |-- delete.py
    |-- products
         |-- get.py
         |-- post.py
         |-- put.py
         |-- delete.py
```

### Implementation of Modules

#### `socket.py`

```python
# socket.py
from fastapi import WebSocket

async def socket(websocket: WebSocket):
    # Handle WebSocket connection logic
    pass
```

#### `startup.py`

```python
# startup.py

def __call__():
    # Execute startup procedures
    pass
```

#### `shutdown.py`

```python
# shutdown.py

def __call__():
    # Execute shutdown procedures
    pass
```

Pypox identifies `startup.py` and `shutdown.py` modules and attempts to invoke them as callable functions. For this purpose, it uses the `__call__` method within these modules to initiate the program at startup and gracefully shut down the program when required.

#### `main.py`

```python
# main.py
from fastapi import FastAPI
from pypox import Pypox
import os
app = Pypox(os.path.dirname(__file__))() # this will return a configured FastAPI Instance

# Any additional configurations for the FastAPI application
# For example: CORS settings, middleware, etc.
```

#### `users/get.py`

```python
# users/get.py
async def endpoint():
    # Logic to retrieve users
    pass
```

Similarly, implement `post.py`, `put.py`, and `delete.py` under the `users` directory with corresponding HTTP methods.

#### `products/get.py`, `post.py`, `put.py`, `delete.py`

Implement similar functions as in the `users` directory but for handling product-related endpoints.

### Usage Example

```python
# main.py
from pypox import Pypox
import uvicorn
import os

pypox_instance = Pypox(os.path.dirname(__file__))
fastapi_app = pypox_instance()

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
```

When run, Pypox will dynamically generate a FastAPI application based on the provided directory structure and module contents. It will recognize the configured WebSocket handling, endpoints for users and products, startup and shutdown procedures, and any additional configurations specified.

This demonstrates how Pypox can automate the setup of a FastAPI application by following naming conventions and organizing functionalities within modules.
