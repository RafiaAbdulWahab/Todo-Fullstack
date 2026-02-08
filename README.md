# Todo Full-Stack Application with AI Chatbot

This is a full-stack Todo application featuring a FastAPI backend and a Next.js frontend, integrated with an AI Chatbot using OpenAI Agents.

## Project Phases Overview

This project was developed iteratively through distinct phases:

### Phase 1: Core Monorepo Setup (Initial Backend & Frontend)
Focused on establishing the foundational monorepo structure, setting up independent backend (FastAPI) and frontend (Next.js) environments, configuring basic database integration (SQLModel), and implementing initial user authentication and task management functionalities.

### Phase 2: Enhanced Task Management & Authentication Refinement
Extended the core functionalities to include robust task CRUD operations, improved API client integration, and refined authentication flows. This phase ensured a stable and functional base for the application's primary purpose.

### Phase 3: AI Chatbot Integration
Introduced an AI-powered chatbot to enhance user interaction for task management. This phase involved integrating OpenAI Agents SDK, developing custom tools (skills) for task manipulation, implementing a stateless conversational API, and building a dedicated chat user interface. This phase also included robust documentation and final quality assurance checks.

## Getting Started

Follow these steps to set up and run the application locally.

### 1. Prerequisites

*   Python 3.8+
*   Node.js 18+
*   `uv` (Python package installer, recommended) or `pip`
*   `npm` or `yarn`

### 2. Backend Setup

Navigate to the `backend` directory and set up the Python environment.

```bash
cd backend
# Create and activate a virtual environment using uv
uv venv
.venv/Scripts/activate # On Windows
# source .venv/bin/activate # On Linux/macOS

# Install backend dependencies
uv pip install -r requirements.txt # (Assuming requirements.txt will be created or manually installed)
# OR if requirements.txt is not present yet:
uv pip install fastapi sqlmodel uvicorn openai python-dotenv
```

**Database Configuration**

The backend is configured to use a PostgreSQL database (e.g., Neon).
Create a `.env` file in the `backend` directory and add your database URL:

```
DATABASE_URL="postgresql://user:password@host:port/database"
```

**AI Chatbot Configuration**

The AI Chatbot requires an OpenAI API key. Add this to your `backend/.env` file:

```
OPENAI_API_KEY="YOUR_ACTUAL_OPENAI_API_KEY"
```
**Important**: Replace `YOUR_ACTUAL_OPENAI_API_KEY` with your real OpenAI API key. If this is missing or contains the placeholder, the chatbot will return a friendly message.

### 3. Frontend Setup

Navigate to the `frontend` directory and install JavaScript dependencies.

```bash
cd frontend
npm install # or yarn install
```

**Database URL for Frontend (Better Auth)**

The frontend's Better Auth configuration also needs the `DATABASE_URL`. Create a `.env.local` file in the `frontend` directory and add your database URL (this should match the backend's `DATABASE_URL`):

```
DATABASE_URL="postgresql://user:password@host:port/database"
```

### 4. Running the Application

**Start the Backend:**

From the `backend` directory (with virtual environment activated):

```bash
uvicorn main:app --reload
```
The backend will run on `http://localhost:8000`.

**Start the Frontend:**

From the `frontend` directory:

```bash
npm run dev
```
The frontend will run on `http://localhost:3000` (or another available port).

## AI Chatbot Architecture & Capabilities

The AI Chatbot is a testament to sophisticated AI integration, leveraging the power of **5 specialized Agents** working in concert, each equipped with an array of **10 distinct Skills**. This multi-agent system enables the chatbot to understand and respond to user queries with remarkable intelligence and flexibility.

*   **Agents**: The core AI logic resides within the FastAPI backend. It utilizes the OpenAI Python SDK to interact with large language models, maintaining conversation context and orchestrating responses. These conceptual "Agents" represent modular components handling different aspects of AI processing (e.g., intent recognition, tool selection, response generation).
*   **Skills (MCP Tools)**: Each agent is equipped with custom "skills" (referred to as MCP tools within the project) that allow them to perform actions related to todo task management. These are designed as callable functions that extend the AI's capabilities beyond general language understanding. Key task management skills include:
    *   `add_task`: To create new tasks.
    *   `list_tasks`: To retrieve and display existing tasks.
    *   `complete_task`: To mark tasks as finished.
    *   `delete_task`: To remove tasks from the list.
    The agent dynamically decides which skill to employ based on the user's conversational intent, providing a highly interactive and functional experience. These tools interact directly with the application's database via the backend services, ensuring consistency with existing functionality.

## Navigating the Application

*   **Home Page (`/`)**: Provides links to Login, Signup, Dashboard, and **AI Chatbot**.
*   **Login (`/login`)**: Use mock login/signup functionality to access the dashboard. (Note: Real authentication needs backend integration beyond the scope of this phase).
*   **Signup (`/signup`)**: Use mock login/signup functionality.
*   **Dashboard (`/dashboard`)**: Displays your tasks. Contains an "**Open AI Chatbot**" button.
*   **AI Chatbot (`/chat`)**: Interact with the AI assistant. Ensure `OPENAI_API_KEY` is correctly set in `backend/.env`.

---
