import os
import random
from httpx import AsyncClient
from tests.app.main import app
import pytest
import faker


# test all routes

test_user: dict[str, dict] = {}
SIZE = 10


# test register rout
@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8000",
    ) as ac:
        fake_user_gen = faker.Faker()
        for _ in range(SIZE):
            fake_user = fake_user_gen.simple_profile()
            test_user[fake_user["username"]] = {
                "username": fake_user["username"],
                "password": f"{random.randint(0, 100000000)}",
                "name": fake_user["name"],
                "email": fake_user["mail"],
                "phone": f"{random.randint(0, 100000000000)}",
            }

        for key in test_user:
            response = await ac.post(
                "/auth/register/",
                json=test_user[key],
            )
            assert response.status_code == 200 or response.status_code == 409


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        for key in test_user:
            response = await ac.post(
                "/auth/login/",
                json={
                    "username": test_user[key]["username"],
                    "password": test_user[key]["password"],
                },
            )
            test_user[key]["id"] = response.text
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_postTodo():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        fake_user_gen = faker.Faker()
        for key in test_user:
            response = await ac.post(
                f"/todo/?user_id={test_user[key]['id']}",
                json={
                    "title": fake_user_gen.text(max_nb_chars=20),
                    "description": fake_user_gen.paragraph(nb_sentences=3),
                    "completed": False,
                },
            )
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_getTodo():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        for key in test_user:
            response = await ac.get(
                f"/todo/?user_id={test_user[key]['id']}",
            )
            test_user[key]["todo"] = response.json()
            assert response.status_code == 200


@pytest.mark.asyncio
async def test_updateTodo():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        for key in test_user:
            for todo in test_user[key]["todo"]:
                response = await ac.put(
                    f"/todo/{todo.get('id')}/?user_id={test_user[key]['id']}",
                    json={
                        "title": todo.get("title"),
                        "description": todo.get("description"),
                        "completed": True,
                    },
                )
                assert response.status_code == 200


@pytest.mark.asyncio
async def test_deleteTodo():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        for key in test_user:
            for todo in test_user[key]["todo"]:
                response = await ac.delete(
                    f"/todo/{todo.get('id')}/?user_id={test_user[key]['id']}",
                )
                assert response.status_code == 200
