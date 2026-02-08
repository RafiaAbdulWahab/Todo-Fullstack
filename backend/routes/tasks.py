from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models import Task, User
from db import get_session
from auth import get_current_user_id

router = APIRouter()

async def get_user_from_id(user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: Task,
    current_user: User = Depends(get_user_from_id), # Use the new dependency
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    task.user_id = current_user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/tasks/", response_model=List[Task])
def read_tasks(
    current_user: User = Depends(get_user_from_id), # Use the new dependency
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user.
    """
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return tasks

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_user_from_id), # Use the new dependency
    session: Session = Depends(get_session)
):
    """
    Delete a task by its ID for the authenticated user.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    session.delete(task)
    session.commit()
    return
