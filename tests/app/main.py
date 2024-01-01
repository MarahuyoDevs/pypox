from fastapi import FastAPI
from pypox import Pypox
import os

app: FastAPI = Pypox(os.path.dirname(__file__))()
