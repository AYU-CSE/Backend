from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import base
from app.models.account_group import account_group

if TYPE_CHECKING:
    from .permission import Permission
    from .account import Account


class Group(base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(150))

    # Relationships
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", back_populates="group", cascade="all, delete-orphan"
    )
    accounts: Mapped[List["Account"]] = relationship(
        "Account", secondary=account_group, back_populates="groups"
    )

    def __repr__(self):
        return f"<Group(id={self.id}, name='{self.name}')>"
