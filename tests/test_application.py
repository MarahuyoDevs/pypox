import os
from pypox.application import Pypox
from pypox.conventions import HTTPConvetion
from starlette.testclient import TestClient
from pypox.processor import (
    QueryProcessor,
    PathProcessor,
    JSONProcessor,
    PydanticProcessor,
)


class TestApp:
    app: Pypox = Pypox(
        conventions=[
            HTTPConvetion(
                directory=os.path.dirname(__file__) + "/app",
                processor_func=[
                    QueryProcessor(),
                    PathProcessor(),
                    JSONProcessor(),
                    PydanticProcessor(),
                ],
            )
        ]
    )
    client = TestClient(app)

    def test_app(self):
        assert len(self.app.routes)

    # encoders
    def test_query(self):
        response = self.client.get("/?id=hello")
        assert response.json() == {"id": "hello"}

    def test_path_params(self):
        response = self.client.get("/person/karl/")
        assert response.json() == {"name": "karl"}

    # decoders
    def test_json(self):
        response = self.client.get(
            "/json?name=karl",
        )
        assert response.json() == {"name": "karl"}

    def test_pydantic(self):
        response = self.client.get("/pydantic?name=karl&age=20")
        assert response.json() == {"name": "karl", "age": 20}
