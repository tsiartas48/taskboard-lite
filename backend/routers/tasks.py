from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from auth import get_current_user
from cache import cache
import models
import schemas

router = APIRouter(tags=["Tasks"])

@router.get("/boards/{board_id}/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
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
    cache_key = f"tasks_{board_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    tasks = db.query(models.Task).filter(
        models.Task.board_id == board_id
    ).order_by(models.Task.position).all()
    cache.set(cache_key, tasks)
    return tasks

@router.post("/boards/{board_id}/tasks", response_model=schemas.TaskResponse)
def create_task(
    board_id: int,
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(models.Board).filter(
        models.Board.id == board_id,
        models.Board.user_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    count = db.query(models.Task).filter(models.Task.board_id == board_id).count()
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        board_id=board_id,
        position=count
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    cache.delete(f"tasks_{board_id}")
    return new_task

@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).join(models.Board).filter(
        models.Task.id == task_id,
        models.Board.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_data: schemas.TaskUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).join(models.Board).filter(
        models.Task.id == task_id,
        models.Board.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    db.commit()
    db.refresh(task)
    cache.delete(f"tasks_{task.board_id}")
    return task

@router.patch("/tasks/{task_id}/move", response_model=schemas.TaskResponse)
def move_task(
    task_id: int,
    move_data: schemas.TaskMove,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if move_data.status not in ["todo", "in_progress", "done"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    task = db.query(models.Task).join(models.Board).filter(
        models.Task.id == task_id,
        models.Board.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = move_data.status
    db.commit()
    db.refresh(task)
    cache.delete(f"tasks_{task.board_id}")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).join(models.Board).filter(
        models.Task.id == task_id,
        models.Board.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    board_id = task.board_id
    db.delete(task)
    db.commit()
    cache.delete(f"tasks_{board_id}")
    return {"message": "Task deleted"}