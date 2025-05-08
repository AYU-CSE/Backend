import uuid
from datetime import datetime, timedelta, UTC

from sqlalchemy.orm import Session

from app import models


def create_session(
    db: Session, *, account_id: int, expires_delta: timedelta(hours=1)
) -> models.Session:
    expires_at = datetime.now(UTC) + expires_delta
    session_id = uuid.uuid4()
    db_session = models.Session(
        id=session_id, account_id=account_id, expires_at=expires_at
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_session(db: Session, session_id: uuid.UUID) -> models.Session | None:
    return db.query(models.Session).filter(models.Session.id == session_id).first()


def delete_session(db: Session, *, session_id: uuid.UUID) -> models.Session | None:
    db_session = get_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
        return db_session
    return None


def delete_expired_sessions(db: Session) -> int:
    now = datetime.now(UTC)
    deleted_count = (
        db.query(models.Session).filter(models.Session.expires_at <= now).delete()
    )
    db.commit()

    return deleted_count
