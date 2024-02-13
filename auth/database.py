from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer, TIMESTAMP
from sqlalchemy import ForeignKey

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column

from config import DB_HOST as hst
from config import DB_PASS as pas
from config import DB_NAME as nme
from config import DB_PORT as prt
from config import DB_USER as usr

from models.models import role

DATABASE_URL = f"postgresql+asyncpg://{usr}:{pas}@{hst}:{prt}/{nme}"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    # user id
    id: Mapped[int] = mapped_column(
        Integer(), primary_key=True)
    # username
    username: Mapped[str] = mapped_column(
        String(length=40), unique=True, nullable=False)
    # registered at
    registered_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(), default=datetime.utcnow)
    # role id
    role_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey(role.c.id))
    # user email
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False)
    # hashed password
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False)
    # is active
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False)
    # is superuser
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)
    # is verified
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(
        session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
