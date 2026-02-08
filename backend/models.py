from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    SQLModel for a User in the Todo application.
    Corresponds to the 'users' table in the database.
    """
    id: str = Field(primary_key=True, index=True)
    """Unique identifier for the user, provided by Better Auth."""
    email: str = Field(unique=True, index=True)
    """The user's email address, must be unique."""
    name: Optional[str] = Field(default=None)
    """The user's display name (optional)."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the user account was created."""

    tasks: List["Task"] = Relationship(back_populates="owner")
    """One-to-many relationship with Task: a user can have multiple tasks."""
    conversations: List["Conversation"] = Relationship(back_populates="user")
    """One-to-many relationship with Conversation: a user can have multiple conversations."""


class Task(SQLModel, table=True):
    """
    SQLModel for a Task in the Todo application.
    Corresponds to the 'tasks' table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    """Unique identifier for the task, auto-incremented."""
    title: str = Field(index=True)
    """The main title or brief description of the task."""
    description: Optional[str] = Field(default=None)
    """A more detailed description of the task (optional)."""
    completed: bool = Field(default=False)
    """Flag indicating whether the task has been completed."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the task was created."""
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the task was last updated."""

    user_id: str = Field(foreign_key="user.id", index=True)
    """Foreign key linking the task to its owner (User ID)."""
    owner: Optional[User] = Relationship(back_populates="tasks")
    """Many-to-one relationship with User: a task belongs to one user."""


class Conversation(SQLModel, table=True):
    """
    SQLModel for a Conversation in the AI Chatbot feature.
    Corresponds to the 'conversations' table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    """Unique identifier for the conversation, auto-incremented."""
    user_id: str = Field(foreign_key="user.id", index=True)
    """Foreign key linking the conversation to its owner (User ID)."""
    title: str = Field(index=True, default="New Conversation")
    """A brief title for the conversation (optional)."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the conversation was created."""
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the conversation was last updated."""

    user: Optional[User] = Relationship(back_populates="conversations")
    """Many-to-one relationship with User: a conversation belongs to one user."""
    messages: List["Message"] = Relationship(back_populates="conversation")
    """One-to-many relationship with Message: a conversation can have multiple messages."""


class Message(SQLModel, table=True):
    """
    SQLModel for a Message within a Conversation.
    Corresponds to the 'messages' table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    """Unique identifier for the message, auto-incremented."""
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    """Foreign key linking the message to its parent conversation."""
    role: str
    """The role of the sender (e.g., 'user', 'assistant')."""
    content: str
    """The text content of the message."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    """Timestamp for when the message was created."""

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
    """Many-to-one relationship with Conversation: a message belongs to one conversation."""
