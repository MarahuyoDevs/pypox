from fastapi import FastAPI
from pypox import Pypox
import os

from pypox.middleware import VanguardMiddleware

app: FastAPI = Pypox(os.path.dirname(__file__))()

app.add_middleware(
    VanguardMiddleware,
    route_dir=os.path.dirname(__file__) + "/routes",
    static_dir=os.path.dirname(__file__) + "/static",
    pyodide_dir=os.path.dirname(__file__) + "static/pyodide",
    enable_pyodide=False,
    base_html="index.html",
    error_html="error.html",
)
