Pypox, leveraging FastAPI's capabilities, allows you to handle forms within your API endpoints. By following FastAPI conventions, you can process form data elegantly.

!!! info

    To use forms, first install `python-multipart`.

    E.g. `pip install python-multipart.`

### Setting up Form Handling

Create a new folder named `api` within your project structure. Inside this folder, set up a new file named `post.py` to demonstrate handling form data in an endpoint.

#### `post.py`

Within the `post.py` file, define an endpoint function that handles form submissions:

```python
from fastapi import Form

async def endpoint(name: str = Form(), email: str = Form()) -> dict:
    return {"Name": name, "Email": email}
```

### Utilizing Forms in Endpoints

In the `post.py` file, the `endpoint` function utilizes the `Form` dependency from FastAPI to receive form data. The `name` and `email` parameters represent form fields, where `Form(...)` denotes required fields.

Following this convention in Pypox enables seamless handling of form data within your FastAPI-based application. By utilizing FastAPI's `Form` dependency, you can easily access and process form submissions within your API endpoints, facilitating efficient form handling operations.

learn more about how FastAPI handles Form Data [**Here**](https://fastapi.tiangolo.com/tutorial/request-forms/).
