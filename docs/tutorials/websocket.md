In the previous tutorial, we explored how Pypox leverages its convention-based routing system to recognize valid HTTP endpoints. Now, let's dive into WebSocket endpoint creation with Pypox.

#### WebSocket Endpoint Basics

Similar to HTTP methods, Pypox uses its file-based convention to identify WebSocket routes. To create a WebSocket endpoint, utilize a file named `socket.py`.

lets use this file structure as an example.

```
project_root/
│
├─── get.py
├─── post.py
├─── put.py
├─── delete.py
├─── socket.py
```

#### Defining a WebSocket Endpoint

An essential aspect of WebSocket endpoints in Pypox is the requirement for an asynchronous function that supports the WebSocket connection. Here's an example of how you can define a WebSocket endpoint within a `socket.py` file:

```python
# Example socket.py file
from fastapi import WebSocket

async def endpoint(websocket: WebSocket):
    # Logic for handling WebSocket connection
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

#### Using the WebSocket Parameter

!!! note

    Note that in the `endpoint` function, the `websocket` parameter of type `WebSocket` is essential for handling WebSocket operations. By including `WebSocket` as a parameter type, both IntelliSense ( or your IDE ) and FastAPI can detect and validate the function as a valid WebSocket endpoint.

#### WebSocket Functionality

Inside the `endpoint` function, you can define the logic required to manage WebSocket connections. In this example, the function awaits incoming text messages from the client and sends a modified response back to the client.

#### Integration with Pypox

Once you've defined the `socket.py` file with the `endpoint` function utilizing the `WebSocket` parameter, Pypox will automatically recognize it as a valid WebSocket endpoint during initialization. Pypox dynamically sets up WebSocket routes, allowing seamless integration and management of WebSocket connections.

By following this convention for WebSocket endpoint creation, Pypox ensures straightforward handling of WebSocket connections, enabling real-time bidirectional communication between clients and the server.
