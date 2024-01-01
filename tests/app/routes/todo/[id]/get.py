from sqlite3 import Row
from tests.app.database.SQLITE import TodoDatabase
from tests.app.routes.todo.schemas import UserTodo, UserTodoWithId
from sqlmodel import select
from fastapi import Depends, status, HTTPException
from pypox.database import asyncDbSession, AsyncSession


async def endpoint(user_id: str, id: str):
    "get todos"

    async with await asyncDbSession(TodoDatabase) as session:
        # find todo in the database
        todo = (
            await session.execute(
                select(TodoDatabase.Todo).where(
                    TodoDatabase.Todo.id == id, TodoDatabase.Todo.user_id == user_id
                )
            )
        ).one()
        return UserTodoWithId(**todo[0].model_dump())
