from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import base
from app.models.account_group import account_group

if TYPE_CHECKING:
    from .post import Post
    from .comment import Comment
    from .like import Like
    from .session import Session
    from .group import Group

class Account(base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    student_number: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)

    # Relationships
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="account")
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="account", cascade="all, delete-orphan")
    groups: Mapped[list["Group"]] = relationship("Group", secondary=account_group, back_populates="accounts")

    def __repr__(self) -> str:
        return f"<Account(id={self.id}, username={self.username}, nickname={self.nickname})>"
