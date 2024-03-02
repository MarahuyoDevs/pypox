from functools import wraps
import inspect
from typing import Any, Callable, Awaitable, NewType
from starlette.requests import Request
from starlette.responses import Response
import asyncio
from pypox._types import (
    QueryStr,
    QueryInt,
    QueryFloat,
    QueryBool,
    PathStr,
    PathInt,
    PathFloat,
    PathBool,
    HeaderStr,
    HeaderInt,
    HeaderFloat,
    HeaderBool,
    CookieStr,
    CookieInt,
    CookieFloat,
    CookieBool,
    BodyDict,
    BodyForm,
)
from pypox.processing.form import FormValidator
from pypox.processing.json import JSONValidator
from pypox.processing.query import QueryValidator
from pypox.processing.path import PathValidator
from pypox.processing.header import HeaderValidator
from pypox.processing.cookies import CookieValidator
from pypox.processing.htmx import HTMXHeaders, HTMXValidator


def processor(
    validators: list = [],
) -> Callable:

    def decorator(
        func: Callable,
    ) -> Callable[[Request], Awaitable[Response | Response]]:

        @wraps(func)
        async def wrapper(request: Request) -> Response:
            params = await PypoxProcessor(
                func,
                [
                    QueryValidator,
                    PathValidator,
                    HeaderValidator,
                    CookieValidator,
                    HTMXValidator,
                    JSONValidator,
                    FormValidator,
                ]
                + validators,
            ).validate(
                request,
            )
            if inspect.iscoroutinefunction(func):
                return await func(**params)
            else:
                return func(**params)

        return wrapper

    return decorator


class PypoxProcessor:

    def __init__(
        self,
        func: Callable[[Any], Awaitable[Response] | Response],
        validators: list = [],
    ) -> None:
        self._validators = validators
        self._func = func

    async def validate(self, request: Request) -> Any:
        params = {}
        for name, parameter in self.iterate_params(self._func):
            if parameter.annotation == Request:
                params[name] = request
                break
            for validator in self._validators:
                validator_obj = validator(name, request)
                if inspect.iscoroutinefunction(validator_obj.__call__):
                    data = await validator_obj(parameter.annotation)
                else:
                    data = validator_obj(parameter.annotation)
                if data:
                    params.update(data)
                    await asyncio.sleep(0)
                    break
        return params

    def iterate_params(self, func: Callable[[Any], Awaitable[Response] | Response]):
        for name, parameter in inspect.signature(func).parameters.items():
            yield name, parameter
