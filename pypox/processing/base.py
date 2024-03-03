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
from pypox.processing.validators.base import Validator
from pypox.processing.validators.form import FormValidator
from pypox.processing.validators.json import JSONValidator
from pypox.processing.validators.query import QueryValidator
from pypox.processing.validators.path import PathValidator
from pypox.processing.validators.header import HeaderValidator
from pypox.processing.validators.cookies import CookieValidator
from pypox.processing.validators.htmx import HTMXHeaders, HTMXValidator
from pydantic import create_model


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
        async for name, parameter in self.iterate_params(self._func):
            if parameter.annotation == Request:
                params[name] = request
                break
            for validator in self._validators:
                validator_obj: Validator = validator(name, parameter.annotation)
                data = await validator_obj(request)
                if data:
                    params.update(data)
                    await asyncio.sleep(0)
                    break
        return params

    async def iterate_params(
        self, func: Callable[[Any], Awaitable[Response] | Response]
    ):
        for name, parameter in inspect.signature(func).parameters.items():
            yield name, parameter
            await asyncio.sleep(0)
