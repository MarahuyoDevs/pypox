from pypox.application import Pypox
from pypox.router import HTTPRouter, WebsocketRouter
import os
from starlette.testclient import TestClient

app = Pypox(
    conventions=[
        HTTPRouter(os.path.dirname(__file__) + "/app"),
        WebsocketRouter(os.path.dirname(__file__) + "/app"),
    ]
)


class TestPypoxClient:
    client = TestClient(app)


class TestHTTP(TestPypoxClient):

    def test_get(self):
        assert self.client.get("/").status_code == 200

    def test_post(self):
        assert self.client.post("/").status_code == 200

    def test_put(self):
        assert self.client.put("/").status_code == 200

    def test_delete(self):
        assert self.client.delete("/").status_code == 200

    def test_patch(self):
        assert self.client.patch("/").status_code == 200

    def test_head(self):
        assert self.client.head("/").status_code == 200

    def test_options(self):
        assert self.client.options("/").status_code == 200


class TestHTTPParams(TestPypoxClient):

    def test_get(self):
        assert self.client.get("/1").status_code == 200

    def test_post(self):
        assert self.client.post("/1").status_code == 200

    def test_put(self):
        assert self.client.put("/1").status_code == 200

    def test_delete(self):
        assert self.client.delete("/1").status_code == 200

    def test_patch(self):
        assert self.client.patch("/1").status_code == 200

    def test_head(self):
        assert self.client.head("/1").status_code == 200

    def test_options(self):
        assert self.client.options("/1").status_code == 200


class TestHTTPQuery(TestPypoxClient):

    def test_get(self):
        assert self.client.get("/query/?number=1").status_code == 200

    def test_post(self):
        assert self.client.post("/query/?number=1").status_code == 200

    def test_put(self):
        assert self.client.put("/query/?number=1").status_code == 200

    def test_delete(self):
        assert self.client.delete("/query/?number=1").status_code == 200

    def test_patch(self):
        assert self.client.patch("/query/?number=1").status_code == 200

    def test_head(self):
        assert self.client.head("/query/?number=1").status_code == 200

    def test_options(self):
        assert self.client.options("/query/?number=1").status_code == 200


class TestHTTPEndpoint(TestPypoxClient):

    def test_get(self):
        assert self.client.get("/httpendpoint").status_code == 200

    def test_post(self):
        assert self.client.post("/httpendpoint").status_code == 200

    def test_put(self):
        assert self.client.put("/httpendpoint").status_code == 200

    def test_delete(self):
        assert self.client.delete("/httpendpoint").status_code == 200

    def test_patch(self):
        assert self.client.patch("/httpendpoint").status_code == 200

    def test_head(self):
        assert self.client.head("/httpendpoint").status_code == 200

    def test_options(self):
        assert self.client.options("/httpendpoint").status_code == 200


class TestWebSocketEndpoint(TestPypoxClient):

    def test_connection(self):
        with self.client.websocket_connect("/") as websocket:
            data = websocket.receive_text()
            assert data == "Hello, world!"
            # send data
            websocket.send_text("Hello, world!")
            assert websocket.receive_text() == "Message text was: Hello, world!"
