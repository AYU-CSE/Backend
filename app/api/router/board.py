from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, services, models
from app.api import deps

router = APIRouter()

@router.post(
    "/", status_code=status.HTTP_201_CREATED
)
def create_board(
    *,
    db: Session = Depends(deps.get_db),
    board_in: schemas.BoardCreate
):
    pass

@router.get(
    "/{board_id}", response_model=schemas.PostResponse, status_code=status.HTTP_200_OK
)
def get_board(
        *,
        db: Session = Depends(deps.get_db),
        board_id: int,
):
    pass

@router.put(
    "/{board_id}", status_code=status.HTTP_200_OK
)
def put_board(
        *,
        db: Session = Depends(deps.get_db),
        board_id: int,
        post_in: schemas.BoardUpdate
):
    pass

@router.delete(
    "/{board_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_board(
        *,
        db: Session = Depends(deps.get_db),
        board_id: int,
):
    pass