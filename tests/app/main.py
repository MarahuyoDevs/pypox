from pypox.router import HTTPRouter
from starlette.applications import Starlette

app = Starlette()

app.mount(
    "/",
    HTTPRouter(directory="tests/app/resources", entry_point="endpoint"),
)
