from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, update as sqlmodel_update
from models import Task, User
from db import get_session
from auth import get_current_user_id
from backend.services.event_publisher import publish_event # Import event publisher

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
    publish_event("todo_created", task.dict()) # Publish event
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

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: Task, # Assuming Task model can be used for update with Optional fields
    current_user: User = Depends(get_user_from_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing task by its ID for the authenticated user.
    """
    db_task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not owned by user"
        )
    
    task_data = task_update.model_dump(exclude_unset=True) # Exclude fields not set in the request
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    publish_event("todo_updated", db_task.dict()) # Publish event
    return db_task

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
    publish_event("todo_deleted", {"id": task_id, "user_id": current_user.id}) # Publish event
    return