
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Sync Database URL for Alembic (same database, different driver)
SYNC_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Sync engine for Alembic
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)


# As I am using alembic for migrations, there is no need for the init_db function to create the database when ever we create or run the app
# async def init_db():
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            print(e)
            raise e
        finally:
            await session.close()

# while True:
#     try:
#         conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='dumnevijay', row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)















# engine = create_async_engine(DATABASE_URL, echo=True)
# Create the AsyncEngine for PostgreSQL
# pool_size and max_overflow are often good to configure for production
# pool_recycle=3600 is still good practice.
# engine = AsyncEngine(create_engine(
#     DATABASE_URL,
#     echo=True,
#     pool_recycle=3600,
#     pool_size=10,        # Number of connections to keep in the pool
#     max_overflow=20      # Max additional connections to create beyond pool_size
# ))
# async_engine = create_async_engine(url=DATABASE_URL, echo=True)
# async_session = async_sessionmaker( bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)


# def get_session():
#     with Session(async_engine) as session:
#         yield session

# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     """Dependency to provide the session object"""
#     async_session = sessionmaker(
#         bind=async_engine, class_=AsyncSession, expire_on_commit=False
#     )

#     async with async_session() as session:
#         yield session





# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         try:
#             yield session
#         finally:
#             await session.close()

# async def get_session():
#     session = async_session()
#     try:
#         yield session
#     finally:
#         await session.close()

