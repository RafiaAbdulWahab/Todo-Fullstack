# Phase 3: AI Chatbot Architecture

## 1. Overview

This document details the architecture for integrating an AI Chatbot into the Todo Full-Stack application, aligning with Phase 3 goals. The chatbot will enable conversational interaction for managing todo tasks, leveraging the OpenAI Agents SDK and the Official MCP SDK. Key design principles include explicit database-driven history management (stateless server) and direct integration with existing task management functionality via AI tools.

## 2. Architectural Overview

The AI Chatbot will be implemented as a new, distinct module within the existing FastAPI backend. This module will introduce new API endpoints for chat interaction, new database tables to store conversation history, and an AI service layer that orchestrates the OpenAI Agents SDK and the Official MCP SDK. The server will be stateless, meaning all conversational context will be fetched from the database on each request.

```
+----------------+       +-------------------+       +-------------------+
|  Frontend App  | <---> |  FastAPI Backend  | <---> |    Database (DB)  |
| (React/Next.js)|       |  (Existing API)   |       | (Existing: User,  |
+----------------+       | +-----------------+       |    Task)          |
                         | | New AI Chatbot  |       | +-----------------+
                         | | Module          |       | | New: Conversation |
                         | | - /api/chat     |       | |      Message      |
                         | | - AI Service    |       | +-----------------+
                         | | - OpenAI Agents |       |
                         | | - MCP SDK       |       |
                         | +-----------------+       |
                         +-------------------+       +-------------------+
```

## 3. New Data Models

Two new SQLModel classes will be defined in `backend/models.py` to persist conversational data:

### `Conversation`

Represents a unique chat session between a user and the AI.

*   `id`: Primary key (e.g., `Optional[int] = Field(default=None, primary_key=True, index=True)`)
*   `user_id`: Foreign key linking to the `User` table (e.g., `str = Field(foreign_key="user.id", index=True)`)

### `Message`

Stores individual messages within a conversation, indicating the sender (user or AI) and content.

*   `id`: Primary key (e.g., `Optional[int] = Field(default=None, primary_key=True, index=True)`)
*   `conversation_id`: Foreign key linking to the `Conversation` table (e.g., `int = Field(foreign_key="conversation.id", index=True)`)
*   `content`: The text of the message (e.g., `str`)
*   `role`: Indicates who sent the message (e.g., `"user"` or `"assistant"`)

## 4. New API Endpoints

A new router (e.g., `backend/routes/chat.py`) will be created and included in `backend/main.py`.

*   **`POST /api/chat`**
    *   **Description**: Accepts a user message, processes it with the AI agent, and returns the AI's response. This endpoint will also manage conversation history by fetching it from the database and persisting new messages.
    *   **Request Body**:
        ```json
        {
          "conversation_id": "Optional[int] (If null, start a new conversation)",
          "message": "string (User's message)"
        }
        ```
    *   **Response Body**:
        ```json
        {
          "conversation_id": "int",
          "ai_response": "string (AI's reply)",
          "tool_outputs": "Optional[List[dict]] (Results from any tools used by AI)"
        }
        ```

## 5. AI Integration Strategy and Tools

A new service (e.g., `backend/services/ai_chat_service.py`) will encapsulate the AI logic.

*   **OpenAI Agents SDK**: This will be the core conversational engine, responsible for understanding user intent, managing dialogue flow, and deciding when to use specific tools.
*   **Official MCP SDK**: This SDK will provide specialized functionalities exposed to the OpenAI Agent as custom tools. It acts as an extension to the agent's capabilities beyond general language understanding.
*   **AI Tools for Task Management**: The OpenAI Agent will be configured to use the following tools, which will interact with the existing task management functionality (via internal calls to the database or existing backend services):
    *   `add_task(title: str, description: Optional[str])`: Creates a new todo task.
    *   `list_tasks(status: Optional[str] = "all")`: Retrieves the user's tasks (e.g., "all", "completed", "pending").
    *   `complete_task(task_id: int)`: Marks a specific task as completed.
    *   `delete_task(task_id: int)`: Removes a task from the list.

## 6. Stateless Server Architecture

*   **History Management**: For every `POST /api/chat` request:
    1.  The server will retrieve the full conversation history (all `Message` records for the given `conversation_id`) from the database.
    2.  This history, along with the new user message, will be passed to the OpenAI Agent.
    3.  After the AI processes the message and generates a response (potentially using tools), both the user's message and the AI's response will be saved back into the database as new `Message` records.
*   This approach ensures that the server itself does not maintain session state, simplifying horizontal scaling and improving fault tolerance.

## 7. Dependencies

New Python packages for the backend:

*   `openai`: For the OpenAI Agents SDK.
*   `python-dotenv`: (If not already present) for environment variables.
*   `official-mcp-sdk`: (Placeholder) The specific package name for the Official MCP SDK.

## 8. Authentication and Authorization

Existing authentication mechanisms will secure the `/api/chat` endpoint, ensuring that conversation history and task management tools are only accessible to the authenticated user. User identity (`user_id`) will be implicitly linked to `Conversation` and `Message` records.