from uuid import uuid1
from fastapi import Depends, HTTPException, status
from tests.app.database.SQLITE import TodoDatabase
from pypox.database import asyncDbSession, AsyncSession
from tests.app.routes.auth.register.schemas import UserRegister
from sqlmodel import select


async def endpoint(
    body: UserRegister,
):
    # check if user exist
    async with await asyncDbSession(TodoDatabase) as session:
        if (
            await session.execute(
                select(TodoDatabase.User).where(
                    TodoDatabase.User.username == body.username
                )
            )
        ).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="user already exist"
            )

        session.add(TodoDatabase.User(id=str(uuid1()), **body.model_dump()))
        await session.commit()
        # check user if exist in the database

        # create user in the database
        return "Successfully registered"
