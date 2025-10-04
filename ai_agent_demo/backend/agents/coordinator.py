from ..frontend_agent import FrontendAgent
from ..backend_agent import BackendAgent
from ..models import TaskResponse, TaskDetail
from ..generator import write_generated_files
from pathlib import Path
from .llm import analyze_brief_with_llm
import re
from typing import List, Dict, Any
from datetime import datetime


class Coordinator:
    def __init__(self):
        self.frontend = FrontendAgent()
        self.backend = BackendAgent()

    def process_brief(self, text: str, use_llm: bool = True):
        """Analyze the brief, extract entities/actions, ask agents for structured outputs,
        write generated files to disk and return TaskResponse with structured TaskDetails.
        """
        # sanitize input and split into meaningful sentences
        clean = text.replace('\u201c','"').replace('\u201d','"')
        # remove odd unicode quotes and fancy punctuation
        clean = re.sub(r"[\u2018\u2019\u201c\u201d]", '"', clean)
        parts = [p.strip().strip('"') for p in re.split(r'(?<=[.!?])\s+', clean) if p.strip()]

        # try an LLM-based analysis first, fall back to heuristics
        analysis = {}
        if use_llm:
            analysis = analyze_brief_with_llm(clean)
        if analysis and isinstance(analysis, dict) and analysis.get('entities'):
            entities = analysis.get('entities', [])
            actions = analysis.get('actions', [])
        else:
            entities = self._extract_entities(parts)
            actions = self._extract_actions(parts)

        # get plain tasks as before (kept for UI)
        ui_tasks = self.frontend.generate_ui_tasks(parts)
        backend_tasks = self.backend.generate_backend_tasks(parts)

        # structured outputs based on entities/actions
        structured_ui = self.frontend.generate_structured_tasks(parts)
        structured_backend = self.backend.generate_structured_tasks(parts)

        # also ask agents for entity-aware code generation
        entity_ui = self.frontend.generate_code_from_entities(entities, actions)
        entity_backend = self.backend.generate_code_from_entities(entities, actions)

        structured: List[TaskDetail] = []
        structured.extend(structured_ui)
        structured.extend(structured_backend)
        structured.extend(entity_ui)
        structured.extend(entity_backend)

        # write generated files to disk and update filenames to point to generated folder
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        out_dir = write_generated_files(structured, timestamp)

        # build a JSON blueprint describing the project with categorized outputs
        blueprint = {
            'project': clean[:140],
            'components': [],
            'apis': [],
            'models': [],
            'schemas': [],
            'workflows': [],
            'integration': {
                'flow': 'Frontend uploads file -> Backend parses and categorizes -> Backend returns JSON -> Frontend displays insights and recommendations',
                'tech_stack': 'FastAPI + SQLite + React (or simple JS) + Chart.js/Recharts'
            }
        }

        # classify structured outputs and provide relative generated paths
        for s in structured:
            # determine relative output path under the generated timestamp folder
            out_rel = ''
            try:
                # s.filename may be absolute (out_dir/path) or relative like 'components/x'
                fpath = Path(s.filename)
                if fpath.is_absolute() and str(fpath).startswith(str(out_dir)):
                    rel = fpath.relative_to(out_dir).as_posix()
                    out_rel = f"{out_dir.name}/{rel}"
                else:
                    out_rel = f"{out_dir.name}/{s.filename.lstrip('/')}"
            except Exception:
                out_rel = s.filename or ''

            entry = {
                'task': s.title,
                'description': s.description,
                'output': out_rel
            }

            lname = (s.filename or '').lower()
            if lname.startswith('components') or (s.role == 'frontend'):
                blueprint['components'].append(entry)
            elif lname.startswith('api') or '/api/' in (s.filename or '') or s.role == 'backend':
                # attempt to extract route paths from code
                routes = []
                try:
                    import re as _re
                    matches = _re.findall(r"@router\.(get|post|put|delete)\(\s*'([^']+)'", s.code or '')
                    for m in matches:
                        routes.append(m[1])
                except Exception:
                    pass
                entry['routes'] = routes
                blueprint['apis'].append(entry)
            elif lname.startswith('models'):
                blueprint['models'].append(entry)
            elif lname.endswith('.sql') or 'schema' in (s.filename or '').lower():
                blueprint['schemas'].append(entry)
            elif lname.endswith('.graphql') or lname.endswith('.gql'):
                blueprint['schemas'].append(entry)
            else:
                # fallback to workflows bucket for business logic descriptions
                blueprint['workflows'].append(entry)

            # update TaskDetail.filename to relative generated path for frontend links
            s.filename = out_rel

        # write blueprint.json to generated folder
        try:
            import json as _json
            bp_full = out_dir / 'blueprint.json'
            bp_full.write_text(_json.dumps(blueprint, indent=2), encoding='utf-8')
        except Exception:
            pass
        # adjust filenames to include output folder
        for s in structured:
            if s.filename:
                s.filename = str(out_dir / Path(s.filename))

        tasks = []
        tasks.extend(ui_tasks)
        tasks.extend(backend_tasks)
        if not tasks:
            tasks = ["No tasks generated from the brief. Provide more details."]

        return TaskResponse(tasks=tasks, structured=structured)

    def _extract_entities(self, parts: List[str]) -> List[Dict[str, Any]]:
        """Return a list of simple entity descriptors detected from the brief.

        Uses keyword heuristics (expenses, bank, user, authentication, statement, transaction).
        """
        text = ' '.join(parts).lower()
        entities = []
        if 'expense' in text or 'expenses' in text or 'transaction' in text:
            entities.append({'name': 'Expense', 'fields': ['date', 'amount', 'merchant', 'category', 'description']})
        if 'bank' in text or 'statement' in text or 'upload' in text:
            entities.append({'name': 'Statement', 'fields': ['file_path', 'uploaded_at', 'user_id']})
        if 'user' in text or 'authentication' in text or 'login' in text:
            entities.append({'name': 'User', 'fields': ['id', 'email', 'password_hash', 'created_at']})
        if not entities:
            # fallback generic entity
            entities.append({'name': 'Item', 'fields': ['id', 'text']})
        return entities

    def _extract_actions(self, parts: List[str]) -> List[str]:
        text = ' '.join(parts).lower()
        actions = []
        kws = {
            'upload': ['upload', 'uploaded', 'uploading'],
            'categorize': ['categorize', 'categorise', 'category', 'categorization'],
            'visualize': ['visual', 'visualize', 'dashboard', 'chart', 'graph', 'insights'],
            'recommend': ['recommend', 'recommendation', 'suggest'],
            'auth': ['authentication', 'login', 'signup', 'register', 'signin']
        }
        for act, keys in kws.items():
            if any(k in text for k in keys):
                actions.append(act)
        if not actions:
            actions.append('implement')
        return actions
