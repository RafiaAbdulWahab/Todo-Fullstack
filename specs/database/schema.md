# Database Schema for Todo Full-Stack Web Application (Phase II)

This document defines the SQLModel tables for our Neon PostgreSQL database, outlining the structure for `users` and `tasks`, and their relationships.

---

## 1. Table: `users`

This table stores user information.

*   **id**: `str` (Primary Key)
    *   **Description**: Unique identifier for the user. This ID will be provided by the Better Auth system.
*   **email**: `str` (Unique)
    *   **Description**: The user's email address. Must be unique for each user.
*   **name**: `str` (Optional)
    *   **Description**: The user's display name.
*   **created_at**: `datetime`
    *   **Description**: Timestamp for when the user account was created.

---

## 2. Table: `tasks`

This table stores individual task items associated with users.

*   **id**: `int` (Primary Key, Auto-increment)
    *   **Description**: Unique identifier for the task. Automatically generated.
*   **user_id**: `str` (Foreign Key -> `users.id`)
    *   **Description**: Links the task to a specific user. This ensures user isolation, meaning users can only see and manage their own tasks.
*   **title**: `str` (Not null)
    *   **Description**: The main title or brief description of the task.
*   **description**: `str` (Nullable)
    *   **Description**: A more detailed description of the task.
*   **completed**: `bool` (Default: `False`)
    *   **Description**: Flag indicating whether the task has been completed.
*   **created_at**: `datetime`
    *   **Description**: Timestamp for when the task was created.
*   **updated_at**: `datetime`
    *   **Description**: Timestamp for when the task was last updated.

---

## 3. Relationships

### One-to-Many Relationship: User to Tasks

*   **Description**: One user (`users` table) can have multiple tasks (`tasks` table) associated with them.
*   **Mechanism**: The `user_id` column in the `tasks` table acts as a foreign key, referencing the `id` column in the `users` table. This establishes the link and enforces user isolation for task management.
