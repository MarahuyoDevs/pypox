from functools import wraps
import inspect
from typing import Callable, Awaitable, NewType
from starlette.requests import Request
from starlette.responses import Response
import asyncio


def processor(func: Callable) -> Callable:

    @wraps(func)
    async def wrapper(request: Request) -> Response:
        params = await load_parameters(func, request)
        if inspect.iscoroutinefunction(func):
            return await func(**params)
        else:
            return func(**params)

    return wrapper


async def load_parameters(func: Callable[[], Awaitable], request: Request) -> dict:

    params = {}

    for name, annotation in inspect.signature(func).parameters.items():
        if annotation.annotation == Request:
            params[name] = request
        if annotation.annotation in [QueryStr, QueryInt, QueryFloat, QueryBool]:
            params[name.replace("-", "_")] = validate_query(
                request.query_params[name.replace("_", "-")], annotation.annotation
            )
        if annotation.annotation in [PathStr, PathInt, PathFloat, PathBool]:
            params[name.replace("-", "_")] = validate_path(
                request.path_params[name.replace("_", "-")], annotation.annotation
            )
        if annotation.annotation in [HeaderStr, HeaderInt, HeaderFloat, HeaderBool]:
            params[name.replace("-", "_")] = validate_header(
                request.headers[name.replace("_", "-")], annotation.annotation
            )
        if annotation.annotation in [CookieStr, CookieInt, CookieFloat, CookieBool]:
            params[name.replace("-", "_")] = validate_cookie(
                request.cookies[name.replace("_", "-")], annotation.annotation
            )
        if annotation.annotation in [BodyDict]:
            params[name.replace("-", "_")] = await request.json()
        await asyncio.sleep(0)
    return params


def validate_query(value, _type):
    if _type == QueryStr:
        return str(value)
    if _type == QueryInt:
        return int(value)
    if _type == QueryFloat:
        return float(value)
    if _type == QueryBool:
        return bool(value)


def validate_path(value, _type):
    if _type == PathStr:
        return str(value)
    if _type == PathInt:
        return int(value)
    if _type == PathFloat:
        return float(value)
    if _type == PathBool:
        return bool(value)


def validate_header(value, _type):
    if _type == HeaderStr:
        return str(value)
    if _type == HeaderInt:
        return int(value)
    if _type == HeaderFloat:
        return float(value)
    if _type == HeaderBool:
        return bool(value)


def validate_cookie(value, _type):
    if _type == CookieStr:
        return str(value)
    if _type == CookieInt:
        return int(value)
    if _type == CookieFloat:
        return float(value)
    if _type == CookieBool:
        return bool(value)


type QueryStr = str

QueryInt = NewType("QueryInt", int)
QueryFloat = NewType("QueryFloat", float)
QueryBool = NewType("QueryBool", bool)

PathStr = NewType("PathStr", str)
PathInt = NewType("PathInt", int)
PathFloat = NewType("PathFloat", float)
PathBool = NewType("PathBool", bool)

HeaderStr = NewType("HeaderStr", str)
HeaderInt = NewType("HeaderInt", int)
HeaderFloat = NewType("HeaderFloat", float)
HeaderBool = NewType("HeaderBool", bool)

CookieStr = NewType("CookieStr", str)
CookieInt = NewType("CookieInt", int)
CookieFloat = NewType("CookieFloat", float)
CookieBool = NewType("CookieBool", bool)

BodyDict = NewType("BodyDict", dict)
