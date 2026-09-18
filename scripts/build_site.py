#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "pages"
SITE = ROOT / "site"
VERSION = "1.0.0"

if OUT.exists():
    shutil.rmtree(OUT)
shutil.copytree(SITE, OUT)
(OUT / ".nojekyll").write_text("", encoding="utf-8")

downloads = OUT / "downloads"
downloads.mkdir(parents=True, exist_ok=True)
assets = [
    ROOT / "whitepaper" / f"YASC-Technical-Whitepaper-v{VERSION}.pdf",
    ROOT / "whitepaper" / f"YASC-Technical-Whitepaper-v{VERSION}.zh-CN.pdf",
    ROOT / "dist" / f"yasc-v{VERSION}.zip",
    ROOT / "dist" / f"yasc-v{VERSION}.sha256",
    ROOT / "examples" / "output" / f"YASC-Sample-Assessment-Report-v{VERSION}.pdf",
]
for src in assets:
    if src.exists():
        shutil.copy2(src, downloads / src.name)

notes = ROOT / "releases" / f"v{VERSION}" / "RELEASE_NOTES.md"
if notes.exists():
    shutil.copy2(notes, downloads / "RELEASE_NOTES.md")

manifest = json.loads((ROOT / "releases" / f"v{VERSION}" / "manifest.json").read_text(encoding="utf-8"))
(OUT / "release.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

links = []
for p in sorted(downloads.iterdir()):
    size = p.stat().st_size
    links.append(f'<li><a href="downloads/{html.escape(p.name)}">{html.escape(p.name)}</a> <small>{size:,} bytes</small></li>')
release_html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>YASC v{VERSION} Release — Yofune</title><link rel="stylesheet" href="styles.css"></head>
<body><header><div class="brand"><img src="yofune-mark.png" alt="Yofune"><strong>YASC</strong><span>v{VERSION} Release</span></div>
<div class="header-actions"><a href="index.html">Interactive checklist</a></div></header>
<main><section class="hero"><p class="eyebrow">V{VERSION} STABLE</p><h1>YASC v{VERSION} Release</h1>
<p>Stable Agent Security baseline, executable verification harness, evidence workflow, reports, CI gate, and real target adapters.</p></section>
<section class="filters" style="display:block"><h2>Release downloads</h2><ul>{''.join(links)}</ul>
<p><strong>Publisher:</strong> Chengdu Yofune Ariake Technology Co., Ltd.<br>
<strong>Contact:</strong> <a href="mailto:contact@yofunesec.com">contact@yofunesec.com</a><br>
<strong>Website:</strong> <a href="https://yofunesec.com/">yofunesec.com</a></p></section></main>
<footer>Yofune Security Research · YASC v{VERSION} · Docs CC BY 4.0 · Code/data Apache-2.0</footer></body></html>'''
(OUT / "release.html").write_text(release_html, encoding="utf-8")
print(f"Built GitHub Pages site: {OUT}")
