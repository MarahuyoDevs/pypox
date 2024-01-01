Pypox introduces a distinctive convention-based approach for routing, setting it apart from conventional decorator-based routing systems found in frameworks like Flask and FastAPI. With Pypox, routing is facilitated through a file-based system, simplifying the process and enhancing organization.

#### File System Conventions

Pypox utilizes a file-based routing system starting from the `routes` folder. The base route corresponds to the `/` endpoint. Additionally, creating an `api` folder will generate an `/api` route.

Within these folders, you can organize your routes based on HTTP verbs or specific WebSocket routes:

- **HTTP Verbs**: Files named after HTTP verbs (e.g., `get.py`, `post.py`, `put.py`, `delete.py`, etc.) represent corresponding HTTP methods.
- **WebSocket Route**: To create a WebSocket route, utilize the file named `socket.py`.

#### Creating Routes

Each file representing an HTTP method or WebSocket route should contain an `endpoint` method. This method can be asynchronous (async) or a regular function, defining the functionality of the route.

#### Example Structure

For instance, consider the following folder structure:

```
project_root/
│
└─── routes/
    │
    ├─── get.py
    ├─── post.py
    ├─── put.py
    ├─── delete.py
    ├─── socket.py
```

In this structure:

- `get.py`, `post.py`, `put.py`, and `delete.py` represent HTTP methods.
- `socket.py` corresponds to a WebSocket route.

!!! note

    you can also not use `routes` as main route because `routes` is just a pypox convetion.

```
project_root/
│
├─── get.py
├─── post.py
├─── put.py
├─── delete.py
├─── socket.py
```

this is also a valid starting point when creating pypox application.

you can also use `/api` as a starting point

```
project_root/
│
└─── api/
    │
    ├─── get.py
    ├─── post.py
    ├─── put.py
    ├─── delete.py
    ├─── socket.py
```

it's the same as the previous example but we change the base folder to `api` giving us the endpoint `/api`

#### Defining Endpoints

Each of these files (`get.py`, `post.py`, etc.) would contain an `endpoint` method:

```python
# Example get.py file
async def endpoint():
    # Logic for handling GET requests
    return {"message": "This is a GET endpoint"}
```

This method defines the functionality associated with the respective HTTP method or WebSocket route.

#### Dynamic Route Creation

Pypox dynamically recognizes these files as valid HTTP or WebSocket routes based on their names and content. Upon initialization, Pypox automatically sets up these routes, allowing for seamless integration and efficient management of endpoints.

By leveraging this convention-based file system for routing, Pypox streamlines the process of organizing and defining routes, contributing to a cleaner, more structured approach to API development.
