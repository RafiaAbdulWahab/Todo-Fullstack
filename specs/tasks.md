# Phase 3: AI Chatbot Implementation Checklist

This document provides a detailed checklist for implementing the AI Chatbot functionality as outlined in `specs/plan.md`, focusing on small, actionable tasks.

## 1. Dependency Installation

*   **[T-301]**: Navigate to the `backend` directory. (COMPLETE)
    *   **Description**: Change the current working directory to the backend project folder.
    *   **Command**: `cd backend`
*   **[T-302]**: Activate the backend virtual environment. (COMPLETE)
    *   **Description**: Ensure the Python virtual environment is active for dependency installation.
    *   **Command (Windows)**: `.venv\Scripts\activate`
    *   **Command (Linux/macOS)**: `source .venv/bin/activate`
*   **[T-303]**: Install `openai` package. (COMPLETE)
    *   **Description**: Install the OpenAI Python client library for interacting with OpenAI Agents SDK.
    *   **Command**: `uv pip install openai`
*   **[T-304]**: Install `python-dotenv` package (if not already present). (COMPLETE)
    *   **Description**: Install the `python-dotenv` library for managing environment variables.
    *   **Command**: `uv pip install python-dotenv`
*   **[T-305]**: Install `official-mcp-sdk` (placeholder). (COMPLETE)
    *   **Description**: Install the placeholder for the Official MCP SDK. Replace with actual package name when available.
    *   **Command**: `uv pip install official-mcp-sdk`

## 2. Database Model Updates

*   **[T-306]**: Add `Conversation` SQLModel class to `backend/models.py`. (COMPLETE)
    *   **Description**: Define the `Conversation` model including `id`, `user_id`, `title`, `created_at`, `updated_at` fields, and relationships to `User` and `Message`.
    *   **File**: `backend/models.py`
*   **[T-307]**: Add `Message` SQLModel class to `backend/models.py`. (COMPLETE)
    *   **Description**: Define the `Message` model including `id`, `conversation_id`, `role`, `content`, `created_at` fields, and relationship to `Conversation`.
    *   **File**: `backend/models.py`
*   **[T-308]**: Update `User` SQLModel class in `backend/models.py` to include `conversations` relationship. (COMPLETE)
    *   **Description**: Add `conversations: List["Conversation"] = Relationship(back_populates="user")` to the `User` model.
    *   **File**: `backend/models.py`
*   **[T-309]**: Verify database table creation. (COMPLETE)
    *   **Description**: Ensure that `create_db_and_tables()` in `backend/db.py` (called by `main.py`'s lifespan) correctly creates the new `Conversation` and `Message` tables on startup.
    *   **Action**: Run backend and check database for new tables.

## 3. MCP Server Creation (`backend/mcp_server.py`)

*   **[T-310]**: Create `backend/mcp_server.py` file. (COMPLETE)
    *   **Description**: Create a new Python file to house the MCP tool functions.
    *   **File**: `backend/mcp_server.py`
*   **[T-311]**: Implement `add_task` tool in `backend/mcp_server.py`. (COMPLETE)
    *   **Description**: Create a function `add_task(user_id: str, title: str, description: Optional[str] = None) -> dict` that interacts with the database to create a new task.
    *   **File**: `backend/mcp_server.py`
*   **[T-312]**: Implement `list_tasks` tool in `backend/mcp_server.py`. (COMPLETE)
    *   **Description**: Create a function `list_tasks(user_id: str, status: Optional[str] = "all") -> List[dict]` that retrieves tasks from the database.
    *   **File**: `backend/mcp_server.py`
*   **[T-313]**: Implement `complete_task` tool in `backend/mcp_server.py`. (COMPLETE)
    *   **Description**: Create a function `complete_task(user_id: str, task_id: int) -> dict` that updates a task's status in the database.
    *   **File**: `backend/mcp_server.py`
*   **[T-314]**: Implement `delete_task` tool in `backend/mcp_server.py`. (COMPLETE)
    *   **Description**: Create a function `delete_task(user_id: str, task_id: int) -> dict` that removes a task from the database.
    *   **File**: `backend/mcp_server.py`
*   **[T-315]**: (Optional) Integrate Official MCP SDK within tools. (COMPLETE)
    *   **Description**: If `official-mcp-sdk` provides specific functionalities, integrate its calls within the `mcp_server.py` tools where appropriate.

## 4. Chat Endpoint Implementation (`POST /api/chat`)

*   **[T-316]**: Create `backend/routes/chat.py` file. (COMPLETE)
    *   **Description**: Create a new API router file for the chat endpoint.
    *   **File**: `backend/routes/chat.py`
*   **[T-317]**: Implement `AIChatService` in `backend/services/ai_chat_service.py`. (COMPLETE)
    *   **Description**: Create a new service file to encapsulate the AI agent logic, including interaction with OpenAI Agents SDK and tool calling.
    *   **File**: `backend/services/ai_chat_service.py`
*   **[T-318]**: Define `POST /api/chat` endpoint in `backend/routes/chat.py`. (COMPLETE)
    *   **Description**: Implement the asynchronous `chat_endpoint` function, accepting `conversation_id` and `user_message`.
    *   **File**: `backend/routes/chat.py`
*   **[T-319]**: Implement conversation history retrieval. (COMPLETE)
    *   **Description**: Within `chat_endpoint`, fetch existing `Message` records for a given `conversation_id` from the database to reconstruct conversation context.
    *   **File**: `backend/routes/chat.py`
*   **[T-320]**: Integrate `AIChatService` and OpenAI Agent. (COMPLETE)
    *   **Description**: Call `AIChatService.process_message()` with user message, history, and available MCP tools.
    *   **File**: `backend/routes/chat.py`, `backend/services/ai_chat_service.py`
*   **[T-321]**: Persist user message and AI response to the database. (COMPLETE)
    *   **Description**: Save the incoming user message and the generated AI response as new `Message` records.
    *   **File**: `backend/routes/chat.py`
*   **[T-322]**: Return AI response to the frontend. (COMPLETE)
    *   **Description**: Structure and return the AI's response and any tool outputs to the calling frontend.
    *   **File**: `backend/routes/chat.py`
*   **[T-323]**: Include `chat_router` in `backend/main.py`. (COMPLETE)
    *   **Description**: Add `from .routes.chat import router as chat_router` and `app.include_router(chat_router, prefix="/api")` to `backend/main.py`.
    *   **File**: `backend/main.py`
*   **[T-324]**: Implement authentication and authorization for `/api/chat`. (COMPLETE)
    *   **Description**: Ensure `get_current_user_id` dependency is used to secure the chat endpoint and link actions to the authenticated user.
    *   **File**: `backend/routes/chat.py`

## 5. Frontend Chat UI Implementation

*   **[T-325]**: Implement Frontend Chat UI. (Completed)
    *   **Description**: Create `frontend/src/app/chat/page.tsx` with a message input, scrollable history, send button using `fetchWithAuth`, and styling with Tailwind CSS.
    *   **File**: `frontend/src/app/chat/page.tsx`