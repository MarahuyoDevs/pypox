from starlette.testclient import TestClient
import pytest
from starlette.templating import Jinja2Templates
import os


@pytest.fixture
def frontend_renderer():
    yield Jinja2Templates(os.path.dirname(__file__) + "/templates")
