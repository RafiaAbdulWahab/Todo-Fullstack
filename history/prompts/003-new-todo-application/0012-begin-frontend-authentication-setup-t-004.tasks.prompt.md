---
ID: 0012
TITLE: Begin Frontend Authentication Setup (T-004)
STAGE: tasks
DATE_ISO: 2026-02-04
SURFACE: agent
MODEL: gemini-1.5-flash
FEATURE: 003-new-todo-application
BRANCH: main
USER: user
COMMAND: Rename CLAUDE.md, update GEMINI.md, update specs/tasks.md, install better-auth, create auth.ts, create .env
LABELS: ["frontend", "authentication", "better-auth", "Next.js", "T-004"]
LINKS:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
FILES_YAML:
  - frontend/CLAUDE.md (renamed to GEMINI.md)
  - frontend/GEMINI.md
  - specs/tasks.md
  - frontend/src/lib/auth.ts
  - frontend/.env
TESTS_YAML: []
PROMPT_TEXT: "First, please rename /frontend/CLAUDE.md to /frontend/GEMINI.md to match our project standards. Then, update the content of /frontend/GEMINI.md to include specific rules for Next.js 15: use Server Components by default, Client Components only when needed, and route all API calls through a centralized client. After that, please begin Task [T-004]: Authentication Setup. Install the better-auth package in the /frontend directory and create a basic configuration file frontend/src/lib/auth.ts. Also, create a placeholder .env file in the /frontend folder with a variable BETTER_AUTH_SECRET. Please update specs/tasks.md to mark Task [T-003] as complete and Task [T-004] as in-progress. Execute these steps now. If the npx command requires manual confirmation, please provide the command and wait for my input."
RESPONSE_TEXT: "I have completed all the requested steps."
OUTCOME: CLAUDE.md renamed to GEMINI.md and updated, specs/tasks.md updated, better-auth installed, auth.ts and .env created.
---
