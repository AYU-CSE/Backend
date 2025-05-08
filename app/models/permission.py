from typing import TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import base

if TYPE_CHECKING:
    from .group import Group
    from .board import Board


class Permission(base):
    __tablename__ = "permission"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("group.id"), nullable=False
    )
    board_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("board.id"), nullable=False
    )
    can_list: Mapped[Optional[bool]] = mapped_column(Boolean)
    can_read: Mapped[Optional[bool]] = mapped_column(Boolean)
    can_write: Mapped[Optional[bool]] = mapped_column(Boolean)
    can_edit: Mapped[Optional[bool]] = mapped_column(Boolean)
    can_delete: Mapped[Optional[bool]] = mapped_column(Boolean)
    can_comment: Mapped[Optional[bool]] = mapped_column(Boolean)

    # Relationships
    group: Mapped["Group"] = relationship("Group", back_populates="permissions")
    board: Mapped["Board"] = relationship("Board", back_populates="permissions")

    def __repr__(self):
        return f"<Permission(id={self.id}, group_id={self.group_id}, board_id={self.board_id})>"
