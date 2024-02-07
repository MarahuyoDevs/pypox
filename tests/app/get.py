from typing import Any, Hashable, Literal
from pydantic import BaseModel
import pandas as pd
from pypox.response.base import PlainTextResponse, HTMLResponse, JSONResponse, Responses
from pypox.processor.base import Cookie, JSONBody, Processor, Query, Header
from pypox import status
from pypox.response.pydantic import PydanticResponse
from pypox.processor.base import processor

data = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
}


class DataModel(BaseModel):
    first_name: str
    last_name: str
    request_header: str


class DataError(BaseModel):
    error: str


class DataRequest(BaseModel):
    id: str
    name: str


@processor
async def endpoint(
    accept: Header[str],
    first_name: Query[str],
    last_name: Query[str],
    session_cookie: Cookie[str],
) -> HTMLResponse:
    """
    This function represents an endpoint that retrieves data.

    Args:
        id (str, optional): The ID of the data. Defaults to "test".
        name (str, optional): The name of the data. Defaults to "karl".

    Returns:
        PydanticResponse[DataModel]: A response object containing the retrieved data.
    """
    return HTMLResponse("Hello baby, I love you!!!")
