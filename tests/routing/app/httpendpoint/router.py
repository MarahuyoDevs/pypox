from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse


class Endpoints(HTTPEndpoint):

    async def get(self, request):
        return PlainTextResponse("GET")

    async def post(self, request):
        return PlainTextResponse("POST")

    async def put(self, request):
        return PlainTextResponse("PUT")

    async def delete(self, request):
        return PlainTextResponse("DELETE")

    async def patch(self, request):
        return PlainTextResponse("PATCH")

    async def head(self, request):
        return PlainTextResponse("HEAD")

    async def options(self, request):
        return PlainTextResponse("OPTIONS")
