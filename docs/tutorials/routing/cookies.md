Pypox leverages FastAPI's capabilities to handle cookies effectively within your API endpoints. Using Pypox conventions and FastAPI features, you can seamlessly manage cookies in your applications.

### Setting up Cookie Handling

To handle cookies, create a folder named `api` within your project. Inside this folder, set up a file named `get.py` to create a simple endpoint that interacts with cookies.

#### `get.py`

Within `get.py`, define an endpoint function that demonstrates cookie handling:

```python
from fastapi import Cookie

async def endpoint(cookie_id: str = Cookie(None)) -> dict:
    return {"Received Cookie ID": cookie_id}
```

### Utilizing Cookies in Endpoints

In the `get.py` file, the `endpoint` function receives the `cookie_id` parameter with the `Cookie` dependency from FastAPI. This parameter allows you to access the value of the incoming cookie, providing functionality to read and process cookies within your endpoint logic.

By following this convention, Pypox enables you to work with cookies effortlessly in your FastAPI-based application. The `Cookie` dependency from FastAPI simplifies the retrieval and handling of cookies within your API endpoints, allowing you to incorporate cookie-related functionality seamlessly.

learn more about how FastAPI handles Cookies [**Here**](https://fastapi.tiangolo.com/tutorial/cookie-params/).
