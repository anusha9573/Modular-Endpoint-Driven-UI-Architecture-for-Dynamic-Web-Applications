from typing import List
from backend.models import TaskDetail


class FrontendAgent:
    def generate_ui_tasks(self, parts: List[str]) -> List[str]:
        # legacy plain text tasks (kept for backward compatibility)
        tasks = []
        for i, p in enumerate(parts, start=1):
            tasks.append(f"UI Task {i}: Create input and display for: '{p}'")
            tasks.append(f"UI Task {i}: Validate and sanitize user input for: '{p}'")
        if not tasks:
            tasks.append("UI Task: Create a simple UI to accept a project brief and show tasks.")
        return tasks

    def generate_structured_tasks(self, parts: List[str]) -> List[TaskDetail]:
        structured = []
        for i, p in enumerate(parts, start=1):
            title = f"UI: {p[:40]}"
            desc = f"Build a React component that captures and displays: {p}"
            filename = f"components/BriefInput{i}.jsx"
            code = (
                "import React, {useState} from 'react';\n"
                f"// Component for: {p}\n"
                "export default function BriefInput() {\n"
                "  const [value, setValue] = useState('');\n"
                "  return (\n"
                "    <div>\n"
                "      <textarea value={value} onChange={e => setValue(e.target.value)} />\n"
                "    </div>\n"
                "  );\n"
                "}\n"
            )
            structured.append(TaskDetail(role='frontend', title=title, description=desc, filename=filename, language='jsx', code=code))
        return structured

    def generate_code_from_entities(self, entities, actions) -> List[TaskDetail]:
        results = []
        for e in entities:
            name = e['name']
            filename = f"components/{name}List.jsx"
            func_name = f"{name}List"
            code = (
                "import React from 'react';\n"
                f"// List component for {name}\n"
                f"export default function {func_name}({{ items }}) {{\n"
                "  return (<ul>{items.map((it,i)=> <li key={i}>{JSON.stringify(it)}</li>)}</ul>);\n"
                "}\n"
            )
            results.append(TaskDetail(role='frontend', title=f"Component: {name}", description=f"React list for {name}", filename=filename, language='jsx', code=code))
        return results
