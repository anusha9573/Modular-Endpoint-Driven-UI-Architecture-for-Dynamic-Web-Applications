from typing import List
from backend.models import TaskDetail


class BackendAgent:
    def generate_backend_tasks(self, parts: List[str]) -> List[str]:
        tasks = []
        for i, p in enumerate(parts, start=1):
            tasks.append(f"Backend Task {i}: Design API endpoint for: '{p}'")
            tasks.append(f"Backend Task {i}: Add validation and persistence for: '{p}'")
        if not tasks:
            tasks.append("Backend Task: Implement /generate_tasks POST endpoint and simple storage.")
        return tasks

    def generate_structured_tasks(self, parts: List[str]) -> List[TaskDetail]:
        structured = []
        for i, p in enumerate(parts, start=1):
            title = f"API: {p[:40]}"
            desc = f"Create a FastAPI endpoint and Pydantic model to accept and persist: {p}"
            filename = f"backend/api_{i}.py"
            code = (
                "from fastapi import APIRouter, HTTPException\n"
                "from pydantic import BaseModel\n\n"
                f"class Item{i}Request(BaseModel):\n    text: str\n\n"
                "router = APIRouter()\n\n"
                f"@router.post('/api/item{i}')\n"
                "def create_item(req: Item{i}Request):\n"
                "    # validation and persistence logic goes here\n"
                "    return {'status':'ok'}\n"
            )
            structured.append(TaskDetail(role='backend', title=title, description=desc, filename=filename, language='py', code=code))
        return structured

    def generate_code_from_entities(self, entities, actions) -> List[TaskDetail]:
        out = []
        for idx, e in enumerate(entities, start=1):
            name = e['name']
            fields = e.get('fields', [])
            # build pydantic model
            model_lines = [f"from pydantic import BaseModel\n\n"]
            model_lines.append(f"class {name}Model(BaseModel):\n")
            for f in fields:
                model_lines.append(f"    {f}: str\n")
            model_code = ''.join(model_lines)

            filename = f"models/{name.lower()}_model.py"
            out.append(TaskDetail(role='backend', title=f"Model: {name}", description=f"Pydantic model for {name}", filename=filename, language='py', code=model_code))

            # simple CRUD endpoint (sqlite-backed)
            ep_lines = [
                "from fastapi import APIRouter, HTTPException\n",
                "import sqlite3\n",
                "from backend import database\n",
                "from typing import List\n\n",
            ]
            ep_lines.append(f"from ..models import {name}Model\n\n")
            ep_lines.append("router = APIRouter()\n\n")
            # Build SQL columns and placeholders
            if fields:
                fields_sql = ', '.join([f"{fld} TEXT" for fld in fields])
                cols = ', '.join(fields)
                placeholders = ', '.join(['?'] * len(fields))
                values_tuple = ', '.join([f"item.{fld}" for fld in fields])
                ep_lines.append("@router.post('/" + name.lower() + "')\n")
                ep_lines.append("def create_" + name.lower() + "(item: " + name + "Model):\n")
                ep_lines.append("    conn = sqlite3.connect(database.DB_PATH)\n")
                ep_lines.append("    cur = conn.cursor()\n")
                ep_lines.append(f"    cur.execute('CREATE TABLE IF NOT EXISTS {name.lower()} (id INTEGER PRIMARY KEY AUTOINCREMENT, {fields_sql})')\n")
                ep_lines.append(f"    cur.execute('INSERT INTO {name.lower()} ({cols}) VALUES ({placeholders})', ({values_tuple},))\n")
                ep_lines.append("    conn.commit()\n")
                ep_lines.append("    conn.close()\n")
                ep_lines.append("    return {'status': 'ok'}\n")
            else:
                ep_lines.append("@router.post('/" + name.lower() + "')\n")
                ep_lines.append("def create_" + name.lower() + "(item: " + name + "Model):\n")
                ep_lines.append("    conn = sqlite3.connect(database.DB_PATH)\n")
                ep_lines.append("    cur = conn.cursor()\n")
                ep_lines.append("    cur.execute('CREATE TABLE IF NOT EXISTS " + name.lower() + " (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)')\n")
                ep_lines.append("    cur.execute('INSERT INTO " + name.lower() + " (data) VALUES (?)', (str(item),))\n")
                ep_lines.append("    conn.commit()\n")
                ep_lines.append("    conn.close()\n")
                ep_lines.append("    return {'status': 'ok'}\n")
            ep_code = ''.join(ep_lines)
            ep_file = f"api/{name.lower()}_api.py"
            out.append(TaskDetail(role='backend', title=f"Endpoint: {name}", description=f"CRUD API for {name}", filename=ep_file, language='py', code=ep_code))
        return out
