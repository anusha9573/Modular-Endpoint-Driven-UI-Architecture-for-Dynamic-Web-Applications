from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .models import BriefRequest, TaskResponse
from .agents.coordinator import Coordinator
import glob
import importlib.util
import zipfile
from fastapi.responses import FileResponse

app = FastAPI(title="AI Agent Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = Coordinator()

from . import database


@app.on_event('startup')
def on_startup():
    # ensure DB is initialized
    try:
        database.init_db()
    except Exception:
        pass
    # include any generated routers if present
    include_latest_generated_routers(app)


def include_latest_generated_routers(app: FastAPI):
    gen_root = Path(__file__).resolve().parent / 'generated'
    dirs = sorted([d for d in gen_root.iterdir() if d.is_dir()]) if gen_root.exists() else []
    if not dirs:
        return None
    latest = dirs[-1]
    # look for api/*.py modules and include their routers if present
    api_dir = latest / 'api'
    if api_dir.exists():
        for py in api_dir.glob('*.py'):
            module_name = f'backend.generated.{latest.name}.api.{py.stem}'
            spec = importlib.util.spec_from_file_location(module_name, str(py))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            # module should expose `router`
            if hasattr(mod, 'router'):
                app.include_router(mod.router)
    return latest


@app.get('/export_latest', include_in_schema=False)
def export_latest():
    gen_root = Path(__file__).resolve().parent / 'generated'
    dirs = sorted([d for d in gen_root.iterdir() if d.is_dir()]) if gen_root.exists() else []
    if not dirs:
        return {'detail': 'no generated output'}
    latest = dirs[-1]
    zip_path = latest.parent / f"{latest.name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in latest.rglob('*'):
            if f.is_file():
                zf.write(f, f.relative_to(latest))
    return FileResponse(str(zip_path), media_type='application/zip', filename=zip_path.name)


@app.get('/blueprint', include_in_schema=False)
def get_blueprint():
    gen_root = Path(__file__).resolve().parent / 'generated'
    dirs = sorted([d for d in gen_root.iterdir() if d.is_dir()]) if gen_root.exists() else []
    if not dirs:
        return {'detail': 'no generated output'}
    latest = dirs[-1]
    bp = latest / 'blueprint.json'
    if not bp.exists():
        return {'detail': 'blueprint not found'}
    return FileResponse(str(bp), media_type='application/json', filename=bp.name)

# Serve the frontend folder (sibling to the backend package)
static_dir = Path(__file__).resolve().parent.parent / "frontend"
if static_dir.exists():
    # Serve static assets under /static to avoid overriding API routes
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Serve generated artifacts under /generated
generated_root = Path(__file__).resolve().parent / 'generated'
if generated_root.exists():
    app.mount('/generated', StaticFiles(directory=str(generated_root)), name='generated')


@app.get("/", include_in_schema=False)
def serve_index():
    index = static_dir / "index.html"
    if index.exists():
        # serve the index.html from the frontend folder
        from fastapi.responses import FileResponse

        return FileResponse(str(index))
    return {"detail": "Index not found"}


@app.post("/generate_tasks", response_model=TaskResponse)
def generate_tasks(brief: BriefRequest, fast: bool = False):
    # If fast=True, skip LLM analysis to avoid model download latency
    result = coordinator.process_brief(brief.text, use_llm=not fast)
    # Coordinator may return a TaskResponse (preferred) or a plain list of tasks.
    if isinstance(result, TaskResponse):
        return result
    if isinstance(result, dict):
        # already shaped dict
        return TaskResponse(**result)
    # assume list/iterable of plain tasks
    if isinstance(result, (list, tuple)):
        return TaskResponse(tasks=list(result))
    # fallback
    return TaskResponse(tasks=[str(result)])
