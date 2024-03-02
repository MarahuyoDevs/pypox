from starlette.requests import Request
from typing import Any
from pypox._types import PathStr, PathInt, PathFloat, PathBool


class PathValidator:

    def __init__(self, name: str, request: Request) -> None:
        self._request = request
        self._name = name

    def __call__(self, _type: type) -> Any:
        if _type not in [PathStr, PathInt, PathFloat, PathBool]:
            return
        if self._name.replace("_", "-") in self._request.path_params:
            self._value = self._request.path_params[self._name.replace("_", "-")]
        else:
            self._value = self._request.path_params[self._name.replace("-", "_")]
        return {self._name: self.validate(_type)}

    def validate(self, _type: type) -> Any:
        if _type == PathStr:
            return str(self._value)
        if _type == PathInt:
            return int(self._value)
        if _type == PathFloat:
            return float(self._value)
        if _type == PathBool:
            return bool(self._value)
