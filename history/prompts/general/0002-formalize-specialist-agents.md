---
id: 0002
title: Formalize Specialist Agents as Markdown Files
stage: misc
date: 2026-02-04
surface: agent
model: gemini-1.5-flash
feature: none
branch: (unknown)
user: (unknown)
command: write_file .specify/agents/orchestrator.md, write_file .specify/agents/spec-manager.md, write_file .specify/agents/backend-builder.md, write_file .specify/agents/frontend-builder.md, write_file .specify/agents/constitution-keeper.md
labels: [documentation, agent-roles]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/agents/orchestrator.md
 - .specify/agents/spec-manager.md
 - .specify/agents/backend-builder.md
 - .specify/agents/frontend-builder.md
 - .specify/agents/constitution-keeper.md
tests:
 - null
---

## Prompt

"I want to formalize our 5 specialist agents as Markdown files in .specify/agents/. Please create these 5 files with their respective roles and responsibilities based on Sir Mohsin's architecture: orchestrator.md: Main coordinator for SDD workflow. spec-manager.md: Specialist in UI/UX and Requirements. backend-builder.md: Specialist in FastAPI and SQLModel. frontend-builder.md: Specialist in Next.js and Better Auth. constitution-keeper.md: Enforcer of code quality and rules. Write these files now so our intelligence is fully documented.

## Response snapshot

Successfully created all 5 agent documentation files in `.specify/agents/`.

## Outcome

- ✅ Impact: Formalized 5 specialist agents as markdown files.
- 🧪 Tests: N/A
- 📁 Files: Created 5 new files in `.specify/agents/`.
- 🔁 Next prompts: Awaiting further instructions from the user.
- 🧠 Reflection: Successfully created all 5 agent documentation files as requested.

## Evaluation notes (flywheel)

- Failure modes observed: None observed.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
