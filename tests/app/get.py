from typing import Any, Hashable, Literal
from pydantic import BaseModel
import pandas as pd
from pypox.response.base import PlainTextResponse, HTMLResponse, JSONResponse, Responses
from pypox.processor.base import Cookie, Processor, Query, Header
from pypox import status

data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
}


class DataModel(BaseModel):
    name: str
    data: list[dict[str, list[int]]]


class DataError(BaseModel):
    error: str


async def endpoint(
    id: Query[str] = Query("test"),
    name: Query[str] = Query("karl"),
    Content_Type: Header[str] = Header("application/json"),
    session_cookie: Cookie[str] = Cookie("session"),
) -> Responses[
    PlainTextResponse[status.HTTP_200_OK, DataModel],
    HTMLResponse[status.HTTP_404_NOT_FOUND],
    PlainTextResponse[status.HTTP_400_BAD_REQUEST, DataError],
]:
    """
    This function represents an endpoint that retrieves data.

    Args:
        id (str, optional): The ID of the data. Defaults to "test".
        name (str, optional): The name of the data. Defaults to "karl".

    Returns:
        PydanticResponse[DataModel]: A response object containing the retrieved data.
    """
    if id == "karl":
        return HTMLResponse("<h1>Not Found</h1>", status.HTTP_404_NOT_FOUND.code)
    return PlainTextResponse(
        f"{id.value} {name.value} {Content_Type.value} {session_cookie.value}"
    )
