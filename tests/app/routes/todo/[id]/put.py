from tests.app.database.SQLITE import TodoDatabase
from tests.app.routes.todo.schemas import UserTodo
from sqlmodel import select
from fastapi import Depends, status, HTTPException
from pypox.database import asyncDbSession, AsyncSession


async def endpoint(user_id: str, id: str, body: UserTodo):
    async with await asyncDbSession(TodoDatabase) as session:
        # find todo in the database
        todo = (
            await session.execute(
                select(TodoDatabase.Todo).where(
                    TodoDatabase.Todo.id == id, TodoDatabase.Todo.user_id == user_id
                )
            )
        ).one()

        # update the todo in the database
        todo[0].title = body.title or todo[0].title
        todo[0].description = body.description or todo[0].description
        todo[0].completed = body.completed

        session.add(todo[0])
        await session.commit()

        return "Successfully updated"
