from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("")
def get_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    boards_count = db.query(models.Board).filter(
        models.Board.user_id == current_user.id
    ).count()

    total_tasks = db.query(models.Task).join(models.Board).filter(
        models.Board.user_id == current_user.id
    ).count()

    todo_count = db.query(models.Task).join(models.Board).filter(
        models.Board.user_id == current_user.id,
        models.Task.status == "todo"
    ).count()

    in_progress_count = db.query(models.Task).join(models.Board).filter(
        models.Board.user_id == current_user.id,
        models.Task.status == "in_progress"
    ).count()

    done_count = db.query(models.Task).join(models.Board).filter(
        models.Board.user_id == current_user.id,
        models.Task.status == "done"
    ).count()

    return {
        "boards": boards_count,
        "tasks": {
            "total": total_tasks,
            "todo": todo_count,
            "in_progress": in_progress_count,
            "done": done_count
        }
    }