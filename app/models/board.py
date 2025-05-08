from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import base

if TYPE_CHECKING:
    from .post import Post
    from .permission import Permission


class Board(base):
    __tablename__ = "board"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="board")
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission", back_populates="board", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Board(id={self.id}, name={self.name})>"
