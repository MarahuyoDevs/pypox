from starlette.requests import Request
from typing import Any
from pypox._types import BodyForm
from pypox.processing.validators.base import Validator


class FormValidator(Validator):

    async def validate(self, _type: type, request: Request) -> None:
        if not _type in [BodyForm]:
            return None
        return _type.__supertype__(await request.form())
