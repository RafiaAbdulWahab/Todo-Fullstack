# backend/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json

from datetime import datetime
import os # Added os import

# Local imports
from db import get_session
from models import User, Conversation, Message, Task # Task needed for tool interactions
from auth import get_current_user_id
import mcp_server # Our custom MCP tools

# OpenAI imports
from openai import OpenAI

router = APIRouter()

# Initialize OpenAI client
client = OpenAI()

# --- Pydantic Models for Request/Response ---
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    ai_response: str
    tool_outputs: Optional[List[Dict[str, Any]]] = None

# --- Helper function to get conversation history ---
def get_conversation_history(session: Session, conversation_id: int, user_id: str) -> List[Dict[str, str]]:
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()
    # Filter out tool messages from history shown to user, only LLM relevant ones
    history = []
    for m in messages:
        # Assuming we only want 'user' and 'assistant' roles for LLM context from DB
        # Tool messages (role='tool') will be added dynamically by the agent logic
        if m.role in ["user", "assistant"]:
            history.append({"role": m.role, "content": m.content})
    return history

# --- Tool Definitions for OpenAI Agent ---
# These will mimic the functions in mcp_server.py
# The agent will call these based on its understanding.

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Adds a new todo task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task."},
                    "description": {"type": "string", "description": "Optional description for the task."},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Lists all todo tasks for the user. Can filter by status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "completed", "pending"], "default": "all", "description": "Filter tasks by status. Defaults to 'all'."},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Marks a specific todo task as complete.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to complete."},
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Deletes a specific todo task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The ID of the task to delete."},
                },
                "required": ["task_id"],
            },
        },
    },
]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    # Safety check for OPENAI_API_KEY
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key or openai_api_key == "YOUR_KEY_HERE":
        return ChatResponse(
            conversation_id=chat_request.conversation_id if chat_request.conversation_id is not None else 0,
            ai_response="AI Chatbot is active, Please provide your OpenAI Key to enable full intelligence.",
            tool_outputs=[]
        )

    # 1. Handle new/existing conversation
    if chat_request.conversation_id is None:
        # Create a new conversation
        new_conversation = Conversation(user_id=current_user_id, title="New Chat", created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add(new_conversation)
        session.commit()
        session.refresh(new_conversation)
        conversation = new_conversation
    else:
        conversation = session.exec(
            select(Conversation)
            .where(Conversation.id == chat_request.conversation_id, Conversation.user_id == current_user_id)
        ).first()
        if not conversation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found or not owned by user")

    # 2. Retrieve conversation history from DB
    history_for_openai = get_conversation_history(session, conversation.id, current_user_id)

    # Add current user message to history and save it
    user_message_obj = Message(conversation_id=conversation.id, role="user", content=chat_request.message, created_at=datetime.utcnow())
    session.add(user_message_obj)
    session.commit()
    session.refresh(user_message_obj)
    history_for_openai.append({"role": "user", "content": chat_request.message})

    # 3. Interact with OpenAI Agent
    messages_for_openai = [{"role": "system", "content": "You are a helpful assistant that manages todo tasks. Use the available tools to assist the user. If you use a tool, please summarize its outcome in natural language."}] + history_for_openai

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125", # A newer model that handles tools well
            messages=messages_for_openai,
            tools=tools,
            tool_choice="auto",
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        ai_response_content = response_message.content
        tool_outputs = []

        if tool_calls:
            # Add assistant's tool calls to conversation messages for OpenAI
            messages_for_openai.append(response_message)

            # Execute tool calls
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Dynamically call the function from mcp_server.py
                if hasattr(mcp_server, function_name):
                    # Pass current_user_id to all MCP tool functions
                    tool_function = getattr(mcp_server, function_name)
                    # The mcp_server functions should handle session management if needed
                    # For simplicity, passing session here.
                    tool_result = tool_function(user_id=current_user_id, session=session, **function_args)
                    tool_outputs.append({"tool_name": function_name, "result": tool_result})
                    messages_for_openai.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(tool_result),
                        }
                    )
                else:
                    tool_outputs.append({"tool_name": function_name, "result": f"Error: Tool '{function_name}' not found."})
                    messages_for_openai.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": f"Error: Tool '{function_name}' not found.",
                        }
                    )

            # Get a new response from the model after tool execution
            second_response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages_for_openai,
            )
            ai_response_content = second_response.choices[0].message.content

        # 4. Save AI message to DB
        if ai_response_content:
            ai_message_obj = Message(conversation_id=conversation.id, role="assistant", content=ai_response_content, created_at=datetime.utcnow())
            session.add(ai_message_obj)
            session.commit()
            session.refresh(ai_message_obj)
            # Update conversation's updated_at timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

        # 5. Return AI response
        return ChatResponse(conversation_id=conversation.id, ai_response=ai_response_content, tool_outputs=tool_outputs)

    except Exception as e:
        # Log the exception for debugging
        print(f"AI processing error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AI processing error: {str(e)}")
