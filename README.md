# TaskFlow

**AI-Powered Personal Task Manager** — manage your tasks through natural conversation.

## Demo

*Screenshots will be added after Version 2 is finalized.*

Expected views:
- Chat interface with the AI assistant
- Task list with completion status

## Product context

### End users

- Students balancing coursework, projects, and deadlines
- Developers who want a quick, low-friction way to track daily tasks
- Anyone who finds traditional to-do apps too rigid or time-consuming

### Problem that the product solves

People often forget tasks or feel overwhelmed by complex task management apps. Writing tasks in natural language (“finish lab report by Friday”) is much faster than filling out forms with dates, priorities, and categories. Most existing apps don't understand natural language — they force users into structured inputs.

### Our solution

TaskFlow combines a simple task manager with an AI agent that understands natural language. Users type what they want to do, and the agent handles the rest:

- “Add task: buy groceries”
- “Show me what I need to do today”
- “Mark lab report as done”

The agent uses an LLM to interpret intent, then calls backend tools to create, read, update, or delete tasks. The web interface provides both a chat for AI interaction and a traditional task list for quick overview.

## Implementation overview

### Architecture

| Component | Technology | Role |
|-----------|------------|------|
| Frontend | Flutter web | Chat interface + task list view |
| Backend | FastAPI | REST API for task CRUD |
| Database | PostgreSQL | Task storage |
| AI Agent | Nanobot + MCP | Intent routing and tool calling |
| LLM | OpenRouter / Qwen | Natural language understanding |
| Deployment | Docker Compose | Runs all services on Ubuntu VM |

**Communication flow:**

1. User types message in web chat
2. Message sent to Nanobot agent via WebSocket
3. Agent uses LLM to determine intent
4. Agent calls appropriate MCP tool (create_task, list_tasks, complete_task)
5. Tool calls backend API
6. Backend updates PostgreSQL
7. Response flows back to user via WebSocket

### Version 1

**Core feature: task creation and listing**

- User can create tasks by typing natural language
- Tasks stored in PostgreSQL with title, description, status, and timestamp
- User can view all tasks in a list
- Tasks can be marked as complete
- All interactions work through web chat interface

### Version 2

**Improvements and additional features**

- Edit and delete tasks
- Task prioritization (AI suggests priority based on description)
- Due date extraction (e.g., “submit homework by Friday”)
- Filter tasks by status (active / completed)
- Dockerized deployment with all services
- Improved UI with task cards and checkboxes

## Features

### Implemented (planned for Version 1)

- Single-user mode (no authentication) — all tasks belong to a default user.
- Natural language task creation
- List all tasks
- Mark tasks as complete
- Persistent storage in PostgreSQL
- Web chat interface

### Planned for Version 2

- Multi-user support with authentication (registration, login, user-specific task lists).
- Edit and delete tasks
- Due date extraction
- Task prioritization
- Status filtering
- Full Docker deployment

### Future possibilities

- Recurring tasks
- Email or browser notifications
- Mobile client

## Usage

### After deployment

1. Open the web application in a browser
2. Type a message in the chat:
   - “Add task: finish lab report”
   - “Show my tasks”
   - “Mark lab report as done”
3. View your tasks in the list below the chat
4. Use checkboxes to mark tasks complete without typing

### Example interactions

| User input | What happens |
|------------|--------------|
| “Add task: buy milk” | Creates task “buy milk” |
| “Show me what I need to do” | Lists all active tasks |
| “Add high priority task: submit proposal by Friday” | Creates task with priority and due date |
| “Task buy milk is done” | Marks that task as complete |

## Deployment

### VM operating system

**Ubuntu 24.04** (same as university VMs)

### Required software on the VM

- Git
- Docker Engine
- Docker Compose plugin
- curl (optional, for testing)

### Environment variables

Create `.env.docker.secret` in the project root based on `.env.docker.example`:

```env
# Database
POSTGRES_DB=taskflow
POSTGRES_USER=taskflow
POSTGRES_PASSWORD=your_password

# Backend
LMS_API_KEY=your_api_key

# LLM
LLM_API_KEY=your_openrouter_or_qwen_key
LLM_API_BASE_URL=https://openrouter.ai/api/v1
LLM_API_MODEL=meta-llama/llama-3.3-70b-instruct:free

# Agent
NANOBOT_ACCESS_KEY=your_access_key
```

### Prerequisites

- Ubuntu 24.04 VM
- Docker and Docker Compose installed
- Git installed

### Deployment steps

1. Clone the repository on the VM:

```bash
git clone https://github.com/YOUR_USERNAME/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

2. Create the environment file:
   
```bash
cp .env
```

3.Edit environment variables

```bash
nano .env
```

### Environment variables

- LLM_API_KEY 
- NANOBOT_ACCESS_KEY
- LMS_API_KEY 

4. Build and start all services:

```bash
docker compose --env-file .env up --build -d
```

Expected services: backend, caddy, postgres, nanobot, client-web-flutter, qwen-code-api, victorialogs, victoriatraces, otel-collector.

6.Open the application

http://10.93.25.240:42002

7. View logs if needed:

```bash
docker compose --env-file .env logs -f
```

8.Stop the application

```bash
docker compose --env-file .env down
```

## Repository notes

- Repository name: `se-toolkit-hackathon-Berezhnoy-Sergey`
- License: MIT
- All code must be pushed to GitHub.
- Final submission includes deployed Version 2 accessible for demonstration.

## Development notes

### Recommended stack

This project reuses the infrastructure from Lab 8, modified for task management:

| Layer | Technology | Source |
|-------|------------|--------|
| Frontend | Flutter web | `client-web-flutter/` from Lab 8 |
| Backend | FastAPI | `backend/` from Lab 8 |
| Database | PostgreSQL | `postgres` service from Lab 8 |
| AI Agent | Nanobot with MCP tools | `nanobot/` from Lab 8 |
| LLM | OpenRouter (free) or Qwen | Configured via `.env.docker.secret` |
| Deployment | Docker Compose | `docker-compose.yml` from Lab 8 |

### Key modifications from Lab 8

- Replace LMS models with Task models (title, description, status, priority, due_date)
- Replace LMS API endpoints with task CRUD endpoints
- Replace LMS MCP tools with task MCP tools (`create_task`, `list_tasks`, `complete_task`, etc.)
- Keep observability stack (VictoriaLogs, VictoriaTraces) — optional, can be removed if not needed
- Keep authentication disabled for Version 1 (single user mode)

### Why this stack works

- You already know all these technologies from Labs 4–8
- No need to learn new frameworks
- Docker Compose provides consistent deployment
- Flutter web client already has WebSocket support for agent communication
- Nanobot agent already supports MCP tools — just replace the tool implementations

### Getting started

1. Copy Lab 8 repository as a template
2. Remove LMS-specific code from `backend/app/models/`, `backend/app/routers/`
3. Add Task model and CRUD endpoints
4. Update `nanobot/config.json` to use new MCP tools
5. Modify `mcp/mcp-lms` to become `mcp/mcp-tasks`
6. Test locally with `docker compose up --build`
7. Deploy to VM