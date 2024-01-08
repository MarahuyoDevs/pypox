## Building OAuth2 Security Middleware with Pypox

This tutorial aims to guide you through creating a security middleware using the OAuth2 authentication code flow within the Pypox framework.

### Project Setup with Poetry Virtual Environment

To begin, let's set up the project within a Poetry virtual environment for better package management and isolation.

1. Start by creating a folder named `tutorials`. This folder will house our Pypox project.

2. Inside the `tutorials` folder, structure the following components:

   - An `__init__.py` file.
   - Subfolders:
     - `tests`
     - `basic_security`, which includes:
       - `main.py`
       - `startup.py`
       - `shutdown.py`
       - `middleware.py`
       - Subfolders:
         - `database`
         - `routes`
         - `templates` (for Jinja2 templates).

3. In the `main.py` file within the `basic_security` folder, add the provided code snippet:

```python
from fastapi import FastAPI
from pypox import Pypox
import os
from tutorials.basic_security.middleware import OAuth2Middleware

app: FastAPI = Pypox(os.path.dirname(__file__))()

app.add_middleware(
    OAuth2Middleware,
    authorize_url="/authorize/",
    token_url="/token/",
    encryption_key="encryption_key",
    decryption_key="decryption_key",
    template_dir=os.path.dirname(__file__) + "/templates",
)
```

This setup initializes our Pypox project and introduces the initial structure required for implementing OAuth2 security middleware using Pypox.

## Developing Custom OAuth2Middleware

Now, let's delve into crafting our custom `OAuth2Middleware` to manage OAuth2 authentication within our Pypox project.

### Importing Necessary Modules

Begin by importing essential modules and libraries required for our middleware:

```python
from uuid import uuid4
from fastapi import Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import AuthenticationError
from fastapi.templating import Jinja2Templates
from base64 import b64decode
from jose import jwt, JWTError
from urllib import parse
import datetime

class OAuth2Middleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        authorize_url: str,
        token_url: str,
        encryption_key: str,
        decryption_key: str,
        unprotected_routes: list = [],
        template_dir: str | None = None,
    ) -> None:
        super().__init__(app)
        # Set variables
        self.authorize_url: str = authorize_url
        self.token_url: str = token_url
        self.encryption_key: str = encryption_key
        self.decryption_key: str = decryption_key
        self.unprotected_routes: list = unprotected_routes
        # Create Jinja2Templates instance if template_dir is provided
        if template_dir:
            self.templates: Jinja2Templates = Jinja2Templates(directory=template_dir)
```

This code initializes our custom middleware class `OAuth2Middleware` and defines necessary variables essential for OAuth2 authentication handling within Pypox.

## Developing Request Dispatcher Function

To manage the flow of requests and handle OAuth2 authentication processes, we'll create an asynchronous function named `dispatch(self, request: Request, call_next)`.

```python
async def dispatch(self, request: Request, call_next) -> Response:
    if request.url.path == self.authorize_url:
        return await self.authorize(request)
    elif request.url.path == self.token_url:
        return await self.token(request)
    elif request.headers.get("Authorization"):
        return await self.protected(request, call_next)
    elif request.url.path in self.unprotected_routes:
        return await call_next(request)
    else:
        return Response()
```

This `dispatch` function serves as a central handler for incoming requests, directing them based on their paths:

- **Authorize Function (`/authorize/`)**: Handles HTTP GET method to initiate the OAuth2 flow process.
- **Token Function (`/token/`)**: Manages the HTTP POST method to generate and return the access token.
- **Protected Function**: Responsible for decrypting the access token and controlling access to protected routes.
- **Unprotected Routes**: Allows passage through for routes defined as unprotected.
- **Default Response**: Returns an empty response for other unspecified paths.

Each path is directed to its respective function for processing based on the URL provided in the incoming request. This structure forms the foundation for managing OAuth2 authentication within the middleware, guiding requests through the authentication flow and protected route access.

## **Implementing OAuth2 Routes**

Now, let's define three asynchronous functions: `authorize`, `token`, and `protected`, responsible for handling authentication within your system.

## Step-by-Step Guide to Implementing the Authorize Endpoint

### 1. Define the `authorize` Function

The `authorize` function initializes the OAuth2 flow process by handling the HTTP GET method.

```python
async def authorize(self, request: Request):
    # Retrieve query parameters
    # Check and render HTML if required
    # Generate and store authorization code
    return RedirectResponse(url=f"{redirect_uri}?code={code}&state={state}")
```

### 2. Extract Query Parameters

Retrieve essential query parameters from the incoming request:

```python
# code above
client_id = request.query_params.get("client_id")
redirect_uri = request.query_params.get("redirect_uri")
response_type = request.query_params.get("response_type")
state = request.query_params.get("state")
scope = request.query_params.get("scope")
show_dialog = request.query_params.get("show_dialog") or "true"
# code below
```

### 3. Validate Required Parameters

Ensure all mandatory parameters are present:

```python
if not all([client_id, redirect_uri, response_type]):
    return Response("Missing required parameters", status_code=400)
```

### 4. Implement Authorization Logic

Perform the necessary authorization logic according to your system requirements.

```python
# Check if show_dialog is true and render HTML if required
if show_dialog.lower() == "true":
    return self.templates.TemplateResponse(
        request=request,
        name="authorize.html",
        context={"scope": scope},
    )

# Generate a unique authorization code and store it
code = str(uuid4())

# store the code for temporary use ( this will be helpful later to verify code )
self.auth_codes[code] = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": response_type,
    "state": state,
    "scope": scope,
}

# Redirect with authorization code and state
return RedirectResponse(url=f"{redirect_uri}?code={code}&state={state}")
```

### Token Endpoint

The `token` function, an HTTP POST endpoint, manages the access token generation process.

```python
async def token(self, request: Request):
    # Validate client credentials
    # Generate access token and refresh token
    return JSONResponse(content={...})
```

### Protected Endpoint

Lastly, the `protected` function secures FastAPI routes by handling the security measures.

```python
async def protected(self, request: Request, call_next):
    # Verify bearer token and decrypt credentials
    return await call_next(request)
```

These functions cater to distinct stages of the OAuth2 flow: initiation, token generation, and secure access to protected routes within your FastAPI system.

## Managing Protected Routes

To exemplify handling protected routes, let's create a sample route at '/routes/protected/' within our FastAPI application.

```python
async def endpoint():
    return {"message":"Hello world!"}
```

Now, let's simulate a request to this protected endpoint using FastAPI's `TestClient`.

```python
from fastapi.testclient import TestClient
from tutorials.basic_security.main import app

client: TestClient = TestClient(app)

response = self.client.get(
    "/protected/",
    headers={
        "Authorization": f"Bearer {self.token['user']['access_token']}",
    },
)
print(response.json())
```

Upon execution, the output will be:

```bash
{"message":"Hello World!"}
```

You can seamlessly integrate this code snippet into your Pypox/FastAPI application to manage and secure protected routes effectively. This showcases how to make authenticated requests to protected endpoints within your system.
