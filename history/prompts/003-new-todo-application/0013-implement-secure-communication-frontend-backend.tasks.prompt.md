---
ID: 0013
TITLE: Implement Secure Communication Frontend-Backend
STAGE: tasks
DATE_ISO: 2026-02-04
SURFACE: agent
MODEL: gemini-1.5-flash
FEATURE: 003-new-todo-application
BRANCH: main
USER: user
COMMAND: Create frontend/src/lib/api.ts, backend/auth.py, update backend/routes/tasks.py, create backend/.env, update specs/tasks.md
LABELS: ["frontend", "backend", "authentication", "JWT", "secure-communication"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - frontend/src/lib/api.ts
  - backend/auth.py
  - backend/routes/tasks.py
  - backend/.env
  - specs/tasks.md
TESTS_YAML: []
PROMPT_TEXT: "Now, let's complete the secure communication between frontend and backend. Please perform the following steps: 1. Create a centralized API client file at frontend/src/lib/api.ts that uses fetch and includes logic to automatically attach the Better Auth JWT token to the 'Authorization: Bearer' header for all requests. 2. Implement the Backend JWT verification middleware in a new file backend/auth.py using the same BETTER_AUTH_SECRET to verify tokens and extract the user_id. 3. Update backend/routes/tasks.py to apply this middleware to all task endpoints as a dependency, ensuring that only authenticated users can access their tasks. 4. Create a basic .env file in the /backend folder with a placeholder DATABASE_URL and BETTER_AUTH_SECRET. 5. Update our specs/tasks.md to mark this secure communication setup as complete. Ensure all code adheres to the specs/constitution.md and uses proper type hints. Execute this now."
RESPONSE_TEXT: "I have completed all the requested steps."
OUTCOME: Frontend API client created, Backend JWT middleware implemented, tasks.py updated, backend .env created, specs/tasks.md updated.
---
