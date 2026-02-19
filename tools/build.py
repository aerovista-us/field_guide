#!/usr/bin/env python3
"""
Build-time precompiler for Field Guide.
Bakes <div data-include="path"></div> into standalone HTML files.

Usage:
  python tools/build.py
  python tools/build.py --src . --out dist
"""
from __future__ import annotations
import argparse, re, shutil
from pathlib import Path

INCLUDE_RE = re.compile(
    r'<(?P<tag>\w+)(?P<attrs>[^>]*?)\sdata-include="(?P<path>[^"]+)"(?P<attrs2>[^>]*)>\s*</(?P=tag)>',
    re.IGNORECASE
)

def bake_includes(html: str, src_root: Path, current_file: Path, seen: set[Path], depth: int = 0) -> str:
    if depth > 40:
        raise RuntimeError(f"Include depth too deep near {current_file}")
    def repl(m: re.Match) -> str:
        rel = m.group("path").strip()
        inc_path = (src_root / rel).resolve()
        if not inc_path.exists():
            return f'<!-- Missing include: {rel} -->'
        if inc_path in seen:
            return f'<!-- Include cycle blocked: {rel} -->'
        seen.add(inc_path)
        content = inc_path.read_text(encoding="utf-8")
        baked = bake_includes(content, src_root, inc_path, seen, depth + 1)
        seen.remove(inc_path)
        return baked

    cur = html
    for _ in range(80):
        nxt = INCLUDE_RE.sub(repl, cur)
        if nxt == cur:
            break
        cur = nxt
    return cur

def copy_tree(src: Path, dst: Path, name: str) -> None:
    s = src / name
    if not s.exists():
        return
    d = dst / name
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(s, d)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=".", help="Source root (site folder)")
    ap.add_argument("--out", default="dist", help="Output folder")
    args = ap.parse_args()

    src_root = Path(args.src).resolve()
    out_root = (src_root / args.out).resolve()

    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # Copy static assets needed by baked pages
    copy_tree(src_root, out_root, "assets")
    if (src_root / "manifest.json").exists():
        shutil.copy2(src_root / "manifest.json", out_root / "manifest.json")

    # Bake only top-level pages (index, concept, chapters)
    html_files = sorted([p for p in src_root.glob("*.html") if p.is_file()])
    for f in html_files:
        raw = f.read_text(encoding="utf-8")
        baked = bake_includes(raw, src_root, f, seen=set())
        (out_root / f.name).write_text(baked, encoding="utf-8")

    print(f"Built {len(html_files)} pages into: {out_root}")

if __name__ == "__main__":
    main()
