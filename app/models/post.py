from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import base

if TYPE_CHECKING:
    from .account import Account
    from .board import Board
    from .comment import Comment
    from .like import Like


class Post(base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    board_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("board.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

    # Relationship
    author: Mapped["Account"] = relationship("Account", back_populates="posts")
    board: Mapped["Board"] = relationship("Board", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like", back_populates="post", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title})>"
