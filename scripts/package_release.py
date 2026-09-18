#!/usr/bin/env python3
from pathlib import Path
import hashlib, shutil, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
subprocess.run(['python', str(ROOT / 'scripts/generate.py')], check=True)
name = 'yasc-v1.0.0'

with tempfile.TemporaryDirectory() as td:
    staging = Path(td) / name
    def ignore(path, names):
        ignored = {'.git', 'dist', 'build', 'runs', 'evidence', '__pycache__', '.pytest_cache', '.venv'}
        return [
            n for n in names
            if n in ignored
            or n.endswith('.pyc')
            or n.startswith('_render_')
            or n.startswith('_pairs_')
        ]
    shutil.copytree(ROOT, staging, ignore=ignore)
    archive = shutil.make_archive(str(DIST / name), 'zip', root_dir=Path(td), base_dir=name)

sha = hashlib.sha256(Path(archive).read_bytes()).hexdigest()
(DIST / (name + '.sha256')).write_text(f"{sha}  {Path(archive).name}\n", encoding='utf-8')
print(archive)
print(sha)
