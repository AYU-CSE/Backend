from sqlalchemy.orm import Session
from app import models, schemas


def get_board(db: Session, board_id: int) -> models.Board | None:
    """ID로 게시판 정보를 조회합니다."""
    return db.get(models.Board, board_id)


def get_boards(db: Session, skip: int = 0, limit: int = 100) -> list[models.Board]:
    """게시판 목록을 조회합니다. (Paging 적용)"""
    return db.query(models.Board).offset(skip).limit(limit).all()


def create_board(db: Session, *, board_in: schemas.BoardCreate) -> models.Board:
    """새로운 게시판을 생성합니다."""
    create_data = board_in.model_dump()
    db_board = models.Board(**create_data)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board


def update_board(
    db: Session,
    *,
    db_board: models.Board,
    board_in: schemas.BoardUpdate,
) -> models.Board:
    """게시판 정보를 수정합니다."""
    update_data = board_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_board, key, value)
    db.commit()
    db.refresh(db_board)
    return db_board


def delete_board(db: Session, *, board_id: int) -> models.Board | None:
    """게시판을 삭제합니다."""
    db_board = get_board(db, board_id)

    if db_board is None:
        return None

    db.delete(db_board)
    db.commit()
    return db_board
