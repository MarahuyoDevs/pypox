from fastapi import FastAPI


async def __call__(app: FastAPI):
    print("shutting down")
