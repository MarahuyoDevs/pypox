## Working with Headers in Pypox

Pypox, built on FastAPI, allows you to handle HTTP headers conveniently within your API endpoints. Using Pypox conventions and FastAPI features, you can easily access and process headers in your application.

### Setting up Header Handling

To work with headers, create a folder named `api` within your project. Inside this folder, create a file named `get.py` to set up an endpoint that interacts with headers.

#### `get.py`

Within `get.py`, define an endpoint function that demonstrates header handling:

```python
from fastapi import Header

async def endpoint(user_agent: str = Header(None)) -> dict:
    return {"User Agent": user_agent}
```

### Using Headers in Endpoints

In the `get.py` file, the `endpoint` function receives the `user_agent` parameter with the `Header` dependency from FastAPI. This parameter enables you to access the value of the incoming header, providing functionality to read and utilize headers within your endpoint logic.

By adhering to this convention, Pypox streamlines the process of working with headers in your FastAPI-based application. Utilizing the `Header` dependency from FastAPI simplifies the retrieval and utilization of headers within your API endpoints, allowing you to handle header-related operations seamlessly.

learn more about how FastAPI handles Headers [**Here**](https://fastapi.tiangolo.com/tutorial/header-params/).
