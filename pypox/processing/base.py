from functools import wraps
import inspect
from typing import Any, Callable, Awaitable
from starlette.requests import Request
from starlette.responses import Response
import asyncio
from pypox.processing.validators.base import Validator
from pypox.processing.validators.form import FormValidator
from pypox.processing.validators.json import JSONValidator
from pypox.processing.validators.query import QueryValidator
from pypox.processing.validators.path import PathValidator
from pypox.processing.validators.header import HeaderValidator
from pypox.processing.validators.cookies import CookieValidator
from pypox.processing.validators.htmx import HTMXValidator


def processor(
    validators: list = [],
) -> Callable:
    """Decorator function that adds validation to a request handler function.

    Args:
        validators (list, optional): A list of additional validators to apply. Defaults to [].

    Returns:
        Callable: A decorated request handler function.
    """

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
    """A class representing a Pypox processor.

    This class is responsible for processing requests and validating parameters.

    Attributes:
        _validators (list): A list of validators to be applied to the parameters.
        _func (Callable): The function to be executed for processing the request.

    """

    def __init__(
        self,
        func: Callable[[Any], Awaitable[Response] | Response],
        validators: list = [],
    ) -> None:
        self._validators = validators
        self._func = func

    async def validate(self, request: Request) -> dict:
        """Validates the request and returns the parameters.

        This method validates the given request by iterating through the parameters
        of the associated function and applying the registered validators. It returns
        a dictionary of parameters that have been validated.

        Args:
            request (Request): The request object to be validated.

        Returns:
            Any: A dictionary containing the validated parameters.

        """
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
                    break
        return params

    async def iterate_params(
        self, func: Callable[[Any], Awaitable[Response] | Response]
    ):
        for name, parameter in inspect.signature(func).parameters.items():
            yield name, parameter
            await asyncio.sleep(0)
