import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.database import base

if TYPE_CHECKING:
    from .account import Account


class Session(base):
    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, index=True
    )
    account_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("account.id"), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="sessions")

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, account_id={self.account_id}, expires_at={self.expires_at})>"
