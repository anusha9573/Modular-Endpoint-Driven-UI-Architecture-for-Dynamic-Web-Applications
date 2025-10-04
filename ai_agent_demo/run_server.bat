@echo off
REM Run this from the ai_agent_demo folder
if exist .venv\Scripts\activate (
  call .venv\Scripts\activate
) else (
  echo Warning: virtual environment not found. Make sure Python and dependencies are installed.
)

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000 --app-dir .\backend
