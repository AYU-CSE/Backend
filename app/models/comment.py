from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import base

if TYPE_CHECKING:
    from .post import Post
    from .account import Account


class Comment(base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )

    # Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    author: Mapped["Account"] = relationship("Account", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, account_id={self.account_id})>"
