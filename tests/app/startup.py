import asyncio
from typing import AsyncGenerator
from click import Context
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from tests.app.database.SQLITE import TodoDatabase
from pypox.database import (
    createAsyncEngine,
    getAsyncEngine,
    init_database_async,
)

createAsyncEngine(TodoDatabase, "aiosqlite")


async def __call__(app: FastAPI) -> None:
    # create async engine
    print("starting system")
    await init_database_async(getAsyncEngine(TodoDatabase), TodoDatabase)
