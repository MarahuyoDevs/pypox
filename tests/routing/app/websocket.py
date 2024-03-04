from starlette.endpoints import WebSocketEndpoint


class Endpoints(WebSocketEndpoint):

    async def on_connect(self, websocket):
        await websocket.accept()
        await websocket.send_text("Hello, world!")

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

    async def on_disconnect(self, websocket, close_code):
        pass
