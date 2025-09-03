# from fastapi.testclient import TestClient
# from app.main import app
# from app import schemes
# from app.config import settings
# from sqlmodel import create_engine
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.ext.asyncio import AsyncEngine
# from typing import AsyncGenerator
# from sqlalchemy.orm import sessionmaker
# from app.database import get_session, SQLModel
# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine


# DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

# Testing_engine = create_async_engine(DATABASE_URL, echo=True, future=True)



# async def init_db():
#     async with Testing_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# # create the database and tables
# asyncio.run(init_db())


# async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
#     async_session = sessionmaker(
#         Testing_engine, class_=AsyncSession, expire_on_commit=False
#     )
#     async with async_session() as session:
#         try:
#             yield session
#         except Exception as e:
#             await session.rollback()
#             print(e)
#             raise e
#         finally:
#             await session.close()




# app.dependency_overrides[get_session] = override_get_session




# client = TestClient(app)


# def test_read_users():
#     response = client.get("/")
#     assert response.json().get('message') == "Welcome to my API!"
#     assert response.status_code == 200


# def test_create_user():
#     response = client.post("/users/", json={"email": "sample@gmail.com", "password": "password123"})

#     new_user = schemes.UserOut(**response.json())
#     assert new_user.email == "sample@gmail.com"
#     assert response.status_code == 201


import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app import schemes
from app.database import get_session, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
Testing_engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(Testing_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="module", autouse=True)
async def create_test_db():
    # create tables before running tests
    async with Testing_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # drop tables after tests
    async with Testing_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.mark.anyio
async def test_read_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json().get("message") == "Welcome to my API!"
        


@pytest.mark.anyio
async def test_create_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "email": "sample@gmail.com",
            "password": "password123"
        })
        assert response.status_code == 201
        new_user = schemes.UserOut(**response.json())
        assert new_user.email == "sample@gmail.com"


        
