from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import base

if TYPE_CHECKING:
    from .account import Account
    from .post import Post


class Like(base):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("post.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), nullable=False
    )
    liked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()"
    )

    # Unique constraint
    __table_args__ = (UniqueConstraint("post_id", "account_id"),)

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    def __repr__(self) -> str:
        return f"<Like(id={self.id}, post_id={self.post_id}, account_id={self.account_id}, liked_at={self.liked_at})>"
