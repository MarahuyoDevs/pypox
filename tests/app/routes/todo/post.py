from uuid import uuid1
from tests.app.database.SQLITE import TodoDatabase
from tests.app.routes.todo.schemas import UserTodo
from sqlmodel import select
from fastapi import Depends, HTTPException, status
from pypox.database import asyncDbSession, AsyncSession


async def endpoint(user_id: str, body: UserTodo):
    """
    create a todo
    """
    async with await asyncDbSession(TodoDatabase) as session:
        session.add(
            TodoDatabase.Todo(id=str(uuid1()), **body.model_dump(), user_id=user_id)
        )

        await session.commit()
        return "Successfully created"
