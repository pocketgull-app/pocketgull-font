#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIRS = [
    ROOT_DIR / "fonts" / "woff2",
    ROOT_DIR.parent / "pocketgull" / "public" / "fonts",
]

force = "--force" in sys.argv or "-f" in sys.argv

# Dynamically discover all TTF font files
ttf_files = sorted(TTF_DIR.glob("*.ttf"))

compressed_count = 0
for src in ttf_files:
    stem = src.stem
    for woff2_dir in WOFF2_DIRS:
        if woff2_dir.exists():
            dst = woff2_dir / f"{stem}.woff2"
            if force or not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                compress(str(src), str(dst))
                compressed_count += 1
                print(f"  • {stem}.woff2 -> {dst} ({dst.stat().st_size} bytes)")

print(f"\n[WOFF2] Recompression complete: {compressed_count} webfonts updated.")
