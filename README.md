# Docker AI

This repository builds a Docker infrastructure monitoring and management platform with a FastAPI backend, a React/Vite frontend, and a custom Docker AI agent interface.

## Project overview

- `backend/` — FastAPI API server, database access, RBAC authentication, Docker/MCP agent integration, auditing, compliance, remediation, and monitoring.
- `frontend/` — React UI with Vite, dashboards, fleet views, agent chat, user management, and login flows.
- `requirements.txt` — Python backend dependencies.
- `frontend/package.json` — frontend dependencies and scripts.
- `.env` / `.env.example` — runtime settings for backend services.

## Architecture

### Backend

- Built with Python, FastAPI, SQLAlchemy, and PostgreSQL.
- Authentication is token-based using a custom HMAC-backed JWT-like token.
- Supports RBAC through roles: `viewer`, `operator`, `admin`.
- Contains Docker agent query route at `/docker-agent/query`.
- Uses `backend/config/settings.py` to load application settings from `.env`.

### Frontend

- Built with React, Vite, and TypeScript.
- Communicates with the backend using Axios.
- Stores auth state in `localStorage` and automatically sends bearer token headers.
- Includes pages for Dashboard, Fleet, Findings, Compliance, Drift, Incidents, Notifications, Agent, and Users.

## Directory structure

```
.
├── backend
│   ├── agent
│   ├── api
│   ├── approval
│   ├── cli
│   ├── compliance
│   ├── config
│   ├── database
│   ├── drift
│   ├── frontend
│   ├── hosts
│   ├── incidents
│   ├── monitoring
│   ├── mcp
│   ├── notifications
│   ├── policies
│   ├── realtime
│   ├── remediation
│   ├── security
│   ├── watcher
│   └── main_api.py
├── frontend
│   ├── public
│   ├── src
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── requirements.txt
├── package.json
└── README.md
```

## Required environment variables

Create a `.env` file in the project root or copy `.env.example`.

```env
# Backend API host and port
API_HOST=0.0.0.0
API_PORT=8090

# Database connection (PostgreSQL)
DATABASE_URL=postgresql://postgres:postgres@localhost/docker_agent

# Secret key for auth token signing
SECRET_KEY=CHANGE_THIS_SECRET_KEY

# Ollama model service
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:latest

# MCP service endpoint
MCP_HOST=192.168.29.225
MCP_PORT=8001

# Approval mode (cli or other configured mode)
APPROVAL_MODE=cli

# Docker host connection string
DOCKER_HOST=npipe:////./pipe/docker_engine
```

### Notes

- `SECRET_KEY` should be changed before production use.
- `DATABASE_URL` should point to a running PostgreSQL database.
- If you run Docker on Linux, change `DOCKER_HOST` from the Windows named pipe to `unix:///var/run/docker.sock`.
- `VITE_API_URL` can be passed to the frontend when running locally if the backend is hosted somewhere other than `http://127.0.0.1:8090`.

## Setup and run

### Backend

1. Create a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and update values.

4. Start the backend API:

```powershell
python backend/main_api.py

```powershell
python backend.main
```

or directly with Uvicorn:

```powershell
uvicorn backend.api.app:app --host 0.0.0.0 --port 8090 --reload
```

### Frontend

1. Go to the frontend folder:

```powershell
cd frontend
```

2. Install frontend dependencies:

```powershell
npm install
```

3. Start the development server:

```powershell
npm run dev
```

4. Open the URL shown by Vite in your browser.

### Optional frontend build

```powershell
cd frontend
npm run build
```

## How the project works

- The frontend authenticates users via `/auth/login` and stores the token in `localStorage`.
- Axios automatically adds the bearer token to requests via `frontend/src/services/api.ts`.
- The backend validates the token in `backend/security/auth.py` and authorizes requests.
- The Docker agent route at `/docker-agent/query` runs user queries through the backend agent graph.
- RBAC is enforced by checking the current user role for each tool request.

## Common commands

- Backend start: `python backend/main_api.py`
- Frontend dev: `cd frontend && npm run dev`
- Install backend deps: `pip install -r requirements.txt`
- Install frontend deps: `cd frontend && npm install`
- Build frontend: `cd frontend && npm run build`

## Testing and debugging

- Use a Python debugger or inspect backend logs on the console.
- Confirm the backend is reachable at `http://127.0.0.1:8090` before starting the frontend.
- If the frontend cannot authenticate, verify the token is saved in the browser and the backend `.env` `SECRET_KEY` matches the expected signing logic.

## Notes

- The backend includes a `backend/database/init_db.py` initializer that prepares application data on startup.
- The agent uses `backend/agent/executor.py` and `backend/agent/authorization.py` for execution and RBAC enforcement.
- For production, secure CORS settings and database credentials.
