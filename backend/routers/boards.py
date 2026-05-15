from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_user
from cache import cache
import models
import schemas

router = APIRouter(prefix="/boards", tags=["Boards"])

@router.get("", response_model=List[schemas.BoardResponse])
def get_boards(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cache_key = f"boards_{current_user.id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    boards = db.query(models.Board).filter(models.Board.user_id == current_user.id).all()
    cache.set(cache_key, boards)
    return boards

@router.post("", response_model=schemas.BoardResponse)
def create_board(
    board: schemas.BoardCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_board = models.Board(
        title=board.title,
        description=board.description,
        user_id=current_user.id
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    cache.delete_pattern(f"boards_{current_user.id}")
    return new_board

@router.get("/{board_id}", response_model=schemas.BoardResponse)
def get_board(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.put("/{board_id}", response_model=schemas.BoardResponse)
def update_board(
    board_id: int,
    board_data: schemas.BoardUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board_data.title is not None:
        board.title = board_data.title
    if board_data.description is not None:
        board.description = board_data.description
    db.commit()
    db.refresh(board)
    cache.delete_pattern(f"boards_{current_user.id}")
    return board

@router.delete("/{board_id}")
def delete_board(
    board_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
    cache.delete_pattern(f"boards_{current_user.id}")
    return {"message": "Board deleted"}