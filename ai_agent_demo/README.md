# AI Agent Demo — Professional End-to-end README

This repository is a compact, modular prototype that demonstrates how a natural-language project brief can be transformed into a set of prioritized tasks, structured design artifacts, and a small generated codebase. The system is intended for demonstration, prototyping, and as a foundation for automated project scaffolding.

Professional project description
--------------------------------
This project provides an automated, auditable bridge from high-level product briefs to starter code and implementation plans. Stakeholders can paste a natural-language brief and immediately receive: prioritized tasks for planning, reusable UI component skeletons, API and data-model scaffolds, and a downloadable project bundle. The blueprint output is both human-friendly and machine-readable, enabling integration into CI pipelines or downstream developer tooling. The prototype emphasizes traceability (every generated file is referenced in `blueprint.json`), modular outputs (clear separation between UI components and backend services), and fast iteration via a `fast` mode that skips heavy model work for demo and CI use.

Key features
------------
- Accepts a project brief and produces a set of plain-text tasks.
- Produces structured TaskDetail artifacts describing frontend components, backend APIs, Pydantic models, and simple workflows.
- Writes generated artifacts to `backend/generated/<timestamp>/` and exports them as a ZIP via `/export_latest`.
- Produces a categorized, human- and machine-readable `blueprint.json` (`/blueprint`) that summarizes Components, APIs, Models, Schemas, and Workflows.
- Frontend is modular (ES modules) and renders components, structured outputs, and a Project Start Summary with links to generated files.

Why this design
----------------
- Modularity: Components are segregated so they can be individually reused and extended.
- Traceability: Every generated artifact is referenced in `blueprint.json`, making it easy to navigate the generated code and map UI components to API endpoints.
- Fast feedback: `?fast=true` skips optional LLM analysis so the prototype is responsive for demos and local development.

Requirements
------------
- Python 3.11+ (the workspace was tested on 3.13)
- pip
- Optional: Node.js / npm if you want to build a React app from generated JSX files

Python dependencies
-------------------
Install dependencies with:

```cmd
pip install -r requirements.txt
```

The `requirements.txt` contains the runtime dependencies used by the backend (FastAPI, uvicorn, pydantic). Additional packages such as `transformers` and `torch` are optional and only required if you enable full LLM-based analysis.

Quick start (Windows cmd.exe)
-----------------------------
From the project root:

```cmd
cd /d c:\Users\addep\OneDrive\Desktop\IN\ai_agent_demo
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Open your browser to:

```
http://127.0.0.1:8000/
```

Use the UI to paste a brief and click "Generate Tasks". The frontend will post the brief and display:

- Plain tasks
- Structured TaskDetail cards (code snippets)
- A categorized Project Start Summary derived from `blueprint.json` (Components, APIs, Models, Schemas, Workflows)
- A Download button that triggers `/export_latest` and returns a ZIP of generated artifacts

Architecture (short)
--------------------
- backend/
   - `main.py` — FastAPI entry, static serving, blueprint and export endpoints.
   - `agents/coordinator.py` — orchestrates brief parsing and generation, writes artifacts and `blueprint.json`.
   - `agents/frontend_agent.py` — generates frontend TaskDetail artifacts and JSX skeletons.
   - `agents/backend_agent.py` — generates Pydantic models and API endpoint stubs.
   - `models.py` — request/response and `TaskDetail` Pydantic models.
   - `generator.py` — writes generated files and ensures generated package markers.

- frontend/
   - `index.html` — main HTML (serves the modular UI containers).
   - `main.js` — ES module entry that composes the modular components.
   - `components/` — ES modules: `BriefInput`, `TaskList`, `StructuredView`, `BlueprintView`, `DownloadButton`.

File layout
-----------

ai_agent_demo/
├─ backend/
│  ├─ main.py
│  ├─ agents/
│  │  ├─ coordinator.py
│  │  ├─ frontend_agent.py
│  │  └─ backend_agent.py
│  ├─ models.py
│  ├─ generator.py
│  └─ generated/  # created at runtime
├─ frontend/
│  ├─ index.html
│  ├─ main.js
│  └─ components/
│     ├─ BriefInput.js
│     ├─ TaskList.js
│     ├─ StructuredView.js
│     ├─ BlueprintView.js
│     └─ DownloadButton.js
├─ requirements.txt
└─ README.md

Important endpoints
-------------------
- POST /generate_tasks
   - Request: { "text": "<project brief>" }
   - Query: fast=true (optional) to skip heavy LLM work
   - Response: TaskResponse with `tasks` (List[str]) and `structured` (List[TaskDetail])

- GET /blueprint
   - Returns the latest `blueprint.json` (machine- and human-readable summary)

- GET /export_latest
   - Returns a ZIP archive of the latest generated artifacts

Development & testing notes
---------------------------
- Fast mode: add `?fast=true` when POSTing to `/generate_tasks` to skip LLM downloads and use heuristics; this is recommended for demos and CI.
- If you want to enable LLM analysis locally, install `transformers` and a compatible model and remove the `fast=true` flag.
- The generator currently creates simple endpoint and model stubs. Before using generated backend code in production, please:
   - Replace string-built SQL with parameterized queries.
   - Add input validation and authentication.
   - Add logging and error handling.

Extending the project
---------------------
- Add a React/Vite scaffold generator so generated JSX becomes a runnable frontend. The generator can write `package.json`, `index.html`, and a minimal `vite` or `create-react-app` structure inside `backend/generated/<timestamp>/`.
- Improve type inference for database schemas: detect field types from the brief or allow the user to edit the generated model before scaffolding the database.
- Add a CLI to run the generator headlessly and export artifacts without the UI.

Troubleshooting
---------------
- 404s for static assets: Ensure the server is run from project root so `backend.main` mounts the `frontend/` folder as `/static`.
- Slow response or timeouts: a local LLM model download may occur on first `/generate_tasks` calls without `fast=true`. Use `fast=true` for demos.
- Blueprint missing: if `backend/generated/` is empty, call `/generate_tasks` first. The generator writes `blueprint.json` as part of generation.

