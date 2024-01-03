## Using Query Parameters with Pypox

Pypox utilizes FastAPI's capabilities, enabling the seamless integration of query parameters into your API endpoints. By adding parameters to your endpoint function, Pypox and FastAPI will automatically recognize and handle them as query parameters.

### Implementing Query Parameters

Consider the following example where we define an endpoint in `/user/info` and expect a query parameter named `id`.

```python
# Example: Accessing /user/info?id=123
async def endpoint(id: int):
    return {"User Info": {"ID": id}}
```

In this case, if a request is made to `/user/info` with a query parameter `id` containing an integer value (e.g., `/user/info?id=123`), Pypox will automatically interpret and extract the `id` value from the query parameters. The endpoint function will then process this parameter and respond accordingly.

### Working with Query Parameters

Pypox simplifies handling query parameters by allowing you to directly include parameters in your endpoint function. FastAPI's underlying functionality handles the routing and parsing of these parameters seamlessly.

By defining parameters within your endpoint function's arguments, such as `id` in the above example, you can access these query parameters within your endpoint's logic.

---

By following this convention, you can effortlessly work with query parameters in your API endpoints, allowing for dynamic and flexible interaction with your API.

This feature adds versatility to your endpoints, enabling users to provide input or retrieve specific data by passing query parameters through the API's URLs.
