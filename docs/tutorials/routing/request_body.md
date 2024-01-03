Pypox leverages FastAPI's capabilities to effortlessly convert JSON request bodies into Pydantic models. By setting up a directory structure and creating necessary files following Pypox conventions, you can seamlessly handle request payloads and convert them into Pydantic models.

### Setting up the Folder Structure

Start by creating a folder named `api` within your project. Inside this folder, create two files: `post.py` and `schemas.py`. The `schemas.py` file will contain shared schemas across different route files.

#### `schemas.py`

In `schemas.py`, define a Pydantic model that represents the structure of the incoming JSON request body:

```python
from pydantic import BaseModel

class MyTable(BaseModel):
    name: str
    age: int
```

#### `post.py`

Within `post.py`, import the Pydantic model and set up your endpoint function:

```python
from python_project.api.schemas import MyTable

async def endpoint(body: MyTable) -> dict:
    return {"user data": {"name": body.name, "age": body.age}}
```

### Using Pydantic Models in Endpoints

By defining a Pydantic model (`MyTable`) to represent the expected structure of the JSON request body and using it as an argument in your endpoint function (`endpoint`), Pypox and FastAPI seamlessly handle the JSON payload.

By following this convention, Pypox simplifies the handling of request bodies, allowing you to easily define Pydantic models that represent the expected structure of the JSON data. This enables efficient validation and processing of incoming JSON payloads within your API endpoints.

learn more about how FastAPI handles request body [**Here**](https://fastapi.tiangolo.com/tutorial/body-multiple-params/).
