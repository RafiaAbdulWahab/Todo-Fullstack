# Technical Implementation Plan for Todo Full-Stack Web Application

This document outlines the technical implementation steps for setting up our monorepo, including backend and frontend setup, database connection, authentication, and the monorepo workflow.

---

## 1. Backend Setup

*   **Initialize `/backend` Folder:** Create a new directory named `backend` in the root of the monorepo.
*   **Virtual Environment:**
    *   Inside the `backend` folder, create a virtual environment using `uv`: `uv venv`.
    *   Activate the virtual environment: `source .venv/bin/activate` (for Linux/macOS) or `.venv\Scripts\activate` (for Windows).
*   **Install Dependencies:**
    *   Install FastAPI, SQLModel, and Uvicorn using `uv`:
        ```bash
        uv pip install fastapi sqlmodel uvicorn
        ```
*   **Initial Structure:** Create the initial directory structure for the FastAPI application (e.g., `main.py`, `models/`, `routers/`).

---

## 2. Frontend Setup

*   **Initialize `/frontend` Folder:**
    *   In the root of the monorepo, run the following command to create a new Next.js application in a `frontend` folder:
        ```bash
        npx create-next-app@latest frontend --typescript --tailwind --app
        ```
    *   This will set up a new Next.js 16+ project with TypeScript, Tailwind CSS, and the App Router.

---

## 3. Database Connection

*   **Environment Variable:** The FastAPI backend will connect to the Neon PostgreSQL database using a `DATABASE_URL` environment variable.
*   **`.env` File:** A `.env` file will be created in the `backend` directory to store the `DATABASE_URL` and other environment-specific variables. This file will be added to `.gitignore` to prevent committing secrets.
*   **SQLModel Engine:** The database connection will be managed by creating a SQLModel engine that reads the `DATABASE_URL` from the environment.

---

## 4. Authentication Plan

*   **Frontend (Better Auth):**
    *   The "Better Auth" library will be installed and configured in the Next.js application.
    *   It will handle user signup and signin forms, manage the user's authentication state, and store the JWT token securely (e.g., in an HttpOnly cookie).
*   **Backend (JWT Verification):
    *   The FastAPI backend will include a dependency for JWT token verification.
    *   A middleware or dependency injection system will be implemented to protect endpoints by requiring a valid JWT token in the `Authorization` header.
    *   The backend will decode the JWT token to get the user's ID for user isolation.

---

## 5. Monorepo Workflow

*   **Running Services Simultaneously:**
    *   **Backend:** Navigate to the `backend` directory and run the FastAPI application using Uvicorn:
        ```bash
        uvicorn main:app --reload
        ```
    *   **Frontend:** Navigate to the `frontend` directory and run the Next.js development server:
        ```bash
        npm run dev
        ```
*   **Package Management:** Each service (`backend` and `frontend`) will have its own dependency management (`uv` for backend, `npm` or `yarn` for frontend).

---

## 6. Phase 3: AI Chatbot Implementation Plan

This section outlines the technical steps for integrating the AI Chatbot into the existing FastAPI backend, based on the `specs/phase3-architecture.md` document.

### 6.1. Install AI/MCP SDKs

*   **Action**: Install necessary Python packages in the backend's virtual environment.
*   **Dependencies**:
    *   `openai`: For OpenAI Agents SDK.
    *   `python-dotenv`: (If not already present) for managing API keys and secrets.
    *   `official-mcp-sdk`: (Placeholder) for the Official MCP SDK (once available, replace with actual package name).
*   **Command Example**:
    ```bash
    cd backend
    .venv/Scripts/activate # or source .venv/bin/activate
    uv pip install openai python-dotenv official-mcp-sdk
    ```

### 6.2. Add New `Conversation` and `Message` SQLModel Tables

*   **Action**: Define the `Conversation` and `Message` SQLModel classes in `backend/models.py`.
*   **Details**:
    *   `Conversation` model:
        ```python
        # backend/models.py (add to existing models)
        from datetime import datetime
        from typing import List, Optional
        from sqlmodel import Field, Relationship, SQLModel

        # ... (existing User model)

        class Conversation(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True, index=True)
            user_id: str = Field(foreign_key="user.id", index=True)
            title: str = Field(index=True, default="New Conversation")
            created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
            updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

            user: Optional["User"] = Relationship(back_populates="conversations")
            messages: List["Message"] = Relationship(back_populates="conversation")

        # Update User model to include relationship to Conversation
        # class User(SQLModel, table=True):
        #    ...
        #    conversations: List["Conversation"] = Relationship(back_populates="user")
        ```
    *   `Message` model:
        ```python
        # backend/models.py (add to existing models)
        # ... (imports as above)

        class Message(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True, index=True)
            conversation_id: int = Field(foreign_key="conversation.id", index=True)
            role: str # "user" or "assistant"
            content: str # The message text
            created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

            conversation: Optional["Conversation"] = Relationship(back_populates="messages")
        ```
*   **Verification**: Ensure `create_db_and_tables()` in `backend/db.py` is called (already handled in `main.py`'s lifespan) to automatically create these new tables upon application startup.

### 6.3. Create `backend/mcp_server.py` for MCP Tools

*   **Action**: Implement `backend/mcp_server.py` to host the 5 required MCP tools. These tools will serve as functions that the AI agent can call to interact with the Todo application's core functionalities.
*   **Details**: Each tool will perform a specific action (e.g., add a task, list tasks). These functions will interact with the database using `SQLModel` sessions and the existing `Task` model. They will need to accept parameters and return structured output for the AI agent to interpret.
*   **Tools**:
    *   `add_task(title: str, description: Optional[str]) -> dict`: Adds a new task.
    *   `list_tasks(status: Optional[str] = "all") -> List[dict]`: Retrieves tasks based on status.
    *   `complete_task(task_id: int) -> dict`: Marks a task as complete.
    *   `delete_task(task_id: int) -> dict`: Deletes a task.
    *   *(Note: The user specified 5 tools, but only 4 were explicitly listed in the requirements. I will plan for 4 and clarify if a fifth is needed later if it comes up.)*
*   **Example Structure for a tool (inside `mcp_server.py`)**:
    ```python
    # backend/mcp_server.py
    from sqlmodel import Session, select
    from db import get_session
    from models import Task, User # Assuming User is needed for context

    def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
        with next(get_session()) as session: # Get a session
            new_task = Task(title=title, description=description, user_id=user_id)
            session.add(new_task)
            session.commit()
            session.refresh(new_task)
            return {"status": "success", "task_id": new_task.id, "title": new_task.title}
    # ... similar functions for list_tasks, complete_task, delete_task
    ```

### 6.4. Implement the Stateless `POST /api/chat` Endpoint

*   **Action**: Create a new API router (e.g., `backend/routes/chat.py`) and implement the `POST /api/chat` endpoint.
*   **Details**:
    *   This endpoint will accept `conversation_id` (optional, for new conversations) and `message` from the user.
    *   It will retrieve the full conversation history from the database using `conversation_id`.
    *   It will initialize and interact with the OpenAI Agent, providing it the message history and the available MCP tools (`mcp_server.py` functions).
    *   The agent's response and any tool outputs will be parsed.
    *   Both the user's incoming message and the AI's response will be persisted to the database (`Message` table).
    *   The AI's response (and potentially tool outputs) will be returned to the frontend.
*   **Key Design Principle**: Stateless server operation; every request rebuilds context from the database.
*   **Structure**:
    ```python
    # backend/routes/chat.py
    from fastapi import APIRouter, Depends, HTTPException, status
    from sqlmodel import Session, select
    from db import get_session
    from models import User, Conversation, Message # New models
    from auth import get_current_user_id # For user authentication
    # from backend.services.ai_chat_service import AIChatService # To be implemented

    router = APIRouter()

    @router.post("/chat")
    async def chat_endpoint(
        conversation_id: Optional[int], # Example for input
        user_message: str,              # Example for input
        current_user_id: str = Depends(get_current_user_id),
        session: Session = Depends(get_session)
    ):
        # 1. Handle new/existing conversation
        # 2. Retrieve conversation history from DB
        # 3. Call AIChatService.process_message(...)
        # 4. Save user message and AI response to DB
        # 5. Return AI response
        pass # Implementation details will follow
    ```
*   **Integration**: Include this new router in `backend/main.py`.
    ```python
    # backend/main.py (add to existing imports and app.include_router)
    # from routes.chat import router as chat_router
    # app.include_router(chat_router, prefix="/api")
    ```

## 7. Phase 4: Kubernetes Deployment Plan

This section outlines the technical steps for deploying the Todo application to Kubernetes, using Minikube for local development and Helm Charts for streamlined deployment, based on the `specs/phase4-kubernetes.md` specification.

### 7.1. Optimized Dockerfiles for Backend and Frontend

*   **Action**: Create optimized `Dockerfile`s for both the FastAPI backend and the Next.js frontend services.
*   **Backend Dockerfile (`backend/Dockerfile`):**
    *   Use a multi-stage build process for smaller final images.
    *   `python:3.10-slim-buster` as base for build stage.
    *   Install `uv` in a build stage to manage Python dependencies.
    *   Install production dependencies only.
    *   Copy application code.
    *   Expose port `8000`.
    *   Define `CMD` to run `uvicorn`.
*   **Frontend Dockerfile (`frontend/Dockerfile`):**
    *   Use a multi-stage build process.
    *   `node:20-alpine` as base for build stage.
    *   Install dependencies and build the Next.js application.
    *   A lightweight server (e.g., `nginx:alpine` or `node:20-alpine` with `serve`) for the final image to serve static assets.
    *   Copy built Next.js output to the serving stage.
    *   Expose port `3000`.
    *   Define `CMD` to start the server.

### 7.2. Building Docker Images and Loading into Minikube

*   **Action**: Build the Docker images for both services and load them into the Minikube environment.
*   **Commands:**
    *   Build Backend Image: `docker build -t todo-backend:latest ./backend`
    *   Build Frontend Image: `docker build -t todo-frontend:latest ./frontend`
    *   Load into Minikube:
        *   `minikube image load todo-backend:latest`
        *   `minikube image load todo-frontend:latest`
*   **Verification**: Ensure images are available in Minikube's Docker daemon.

### 7.3. Creating Kubernetes Manifests (Deployment, Service, Secrets)

*   **Action**: Write Kubernetes manifest files (YAML) for the backend and frontend.
*   **Backend Manifests (`kubernetes/backend-deployment.yaml`, `kubernetes/backend-service.yaml`):**
    *   **Deployment**: Define a `Deployment` for the FastAPI backend, specifying the `todo-backend:latest` image, replica count, and resource requests/limits.
    *   **Service**: Define a `Service` (e.g., `ClusterIP` or `NodePort`) to expose the backend within the cluster.
*   **Frontend Manifests (`kubernetes/frontend-deployment.yaml`, `kubernetes/frontend-service.yaml`):**
    *   **Deployment**: Define a `Deployment` for the Next.js frontend, specifying the `todo-frontend:latest` image, replica count, and resource requests/limits.
    *   **Service**: Define a `Service` (e.g., `NodePort` or `LoadBalancer` if ingress is configured) to expose the frontend.
*   **Secrets Manifest (`kubernetes/secrets.yaml`):**
    *   Create a `Secret` for `DATABASE_URL` and `OPENAI_API_KEY`.
    *   Ensure these secrets are referenced correctly in the backend deployment.

### 7.4. Initializing a Helm Chart

*   **Action**: Initialize a Helm Chart for the entire Todo application.
*   **Command**: `helm create charts/todo-app`
*   **Chart Structure:**
    *   Move the Kubernetes manifests created in step 7.3 into the `charts/todo-app/templates` directory.
    *   Parameterize image names, tags, replica counts, and other configurable values in `values.yaml`.
    *   Update `Chart.yaml` with appropriate metadata.
*   **Verification**: Ensure the chart can be templated (`helm template charts/todo-app`) and installed locally (`helm install todo-app charts/todo-app`).