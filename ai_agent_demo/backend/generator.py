from pathlib import Path
from typing import List
from .models import TaskDetail
import os
import re


def write_generated_files(structured: List[TaskDetail], timestamp: str) -> Path:
    """Write each TaskDetail.code to disk under backend/generated/<timestamp>/

    Returns the relative output directory path.
    """
    base = Path(__file__).resolve().parent
    out = base / 'generated' / timestamp
    out.mkdir(parents=True, exist_ok=True)
    for s in structured:
        if s.filename and s.code:
            file_path = out / Path(s.filename)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(s.code, encoding='utf-8')

    # Ensure each folder in the generated tree is a package by creating __init__.py
    for dirpath, dirnames, filenames in os.walk(out):
        p = Path(dirpath)
        init = p / '__init__.py'
        if not init.exists():
            init.write_text('# generated package\n', encoding='utf-8')

    # Create models __init__.py that re-exports model classes for easier relative imports
    models_dir = out / 'models'
    if models_dir.exists():
        exports = []
        for py in models_dir.glob('*.py'):
            text = py.read_text(encoding='utf-8')
            m = re.search(r'class\s+(\w+)', text)
            if m:
                cls = m.group(1)
                exports.append((py.stem, cls))
        if exports:
            lines = [f"from .{stem} import {cls}\n" for stem, cls in exports]
            lines.append('\n__all__ = [' + ', '.join([f"\'{cls}\'" for _, cls in exports]) + ']\n')
            init_file = models_dir / '__init__.py'
            init_file.write_text(''.join(lines), encoding='utf-8')
    return out
