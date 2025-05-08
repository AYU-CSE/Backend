from sqlalchemy import Table, Column, BigInteger, ForeignKey
from app.database import base

account_group = Table(
    "account_group",
    base.metadata,
    Column("account_id", BigInteger, ForeignKey("account.id"), primary_key=True),
    Column("group_id", BigInteger, ForeignKey("group.id"), primary_key=True),
    extend_existing=True,
)
