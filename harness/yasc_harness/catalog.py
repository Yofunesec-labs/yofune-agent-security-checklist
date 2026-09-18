from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml

ROOT=Path(__file__).resolve().parents[2]

def load_catalog() -> tuple[dict[str,Any],dict[str,Any],dict[str,Any]]:
    controls=yaml.safe_load((ROOT/'schema/controls.yaml').read_text(encoding='utf-8'))
    tests=yaml.safe_load((ROOT/'schema/tests.yaml').read_text(encoding='utf-8'))
    profiles=yaml.safe_load((ROOT/'schema/profiles.yaml').read_text(encoding='utf-8'))
    return controls,tests,profiles

def test_map() -> dict[str,dict[str,Any]]:
    return {t['id']:t for t in load_catalog()[1]['tests']}

def control_map() -> dict[str,dict[str,Any]]:
    return {c['id']:c for c in load_catalog()[0]['controls']}
