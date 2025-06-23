from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Boolean, text, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "users"  # 👈 Custom table name
    id: int = Field(primary_key=True, index=True, nullable=False)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()")),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    posts: List["Post"] = Relationship(back_populates="owner")

class Post(SQLModel, table=True):
    __tablename__ = "posts"  # 👈 Custom table name
    id: int = Field(primary_key=True, index=True, nullable=False)
    title: str = Field(index=True, nullable=False, max_length=255)
    content: str = Field(default=None)
    is_published: bool = Field(
        sa_column=Column(Boolean, nullable=False, server_default=text("true")),
        default=True
    )
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text("NOW()")),
        default_factory=lambda: datetime.now(timezone.utc)
    )
    owner_id: int = Field(
        sa_column=Column(
            Integer, 
            ForeignKey("users.id", ondelete="CASCADE"), 
            nullable=False
        )
    )
    owner: Optional[User] = Relationship(back_populates="posts")


class Vote(SQLModel, table=True):
    __tablename__ = 'votes'
    user_id: int = Field(
        sa_column=Column(
            Integer, 
            ForeignKey("users.id", ondelete="CASCADE"), 
            primary_key=True,
            nullable=False
        )
    )
    post_id: int = Field(
        sa_column=Column(
            Integer, 
            ForeignKey("posts.id", ondelete="CASCADE"), 
            primary_key=True,
            nullable=False
        )
    )