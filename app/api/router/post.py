from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, services, models
from app.api import deps

router = APIRouter()

@router.post(
    "/", status_code=status.HTTP_201_CREATED
)
def create_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: schemas.PostCreate
):
    pass

@router.get(
    "/{post_id}", response_model=schemas.PostResponse, status_code=status.HTTP_200_OK
)
def get_post(
        *,
        db: Session = Depends(deps.get_db),
        post_id: int,
):
    pass

@router.put(
    "/{post_id}", status_code=status.HTTP_200_OK
)
def put_post_endpoint(
        *,
        db: Session = Depends(deps.get_db),
        post_id: int,
        post_in: schemas.PostUpdate
):
    pass

@router.delete(
    "/{post_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
        *,
        db: Session = Depends(deps.get_db),
        post_id: int,
):
    pass