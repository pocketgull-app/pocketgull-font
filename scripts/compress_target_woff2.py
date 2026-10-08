#!/usr/bin/env python3
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

TARGET_FONTS = [
    "PocketGull-Regular.ttf",
    "PocketGull-VF.ttf",
    "PocketGullMono-Regular.ttf",
    "PocketGullMono-Bold.ttf",
    "PocketGullMono-Italic.ttf",
    "PocketGull-Italic.ttf",
    "PocketGull-Soft.ttf",
    "PocketGull-Soft-Regular.ttf",
    "PocketGull-Soft-Bold.ttf",
]

print(f"Compressing {len(TARGET_FONTS)} target webfonts to WOFF2...")
for fname in TARGET_FONTS:
    src = TTF_DIR / fname
    if not src.exists():
        continue
    stem = src.stem
    dst = WOFF2_DIR / f"{stem}.woff2"
    compress(str(src), str(dst))
    print(f"  • {stem}.woff2 -> {dst} ({dst.stat().st_size:,} bytes)")
    if PUBLIC_DIR.exists():
        pub_dst = PUBLIC_DIR / f"{stem}.woff2"
        shutil.copy2(str(dst), str(pub_dst))
        print(f"    -> synced to {pub_dst}")

print("\n[SUCCESS] Targeted WOFF2 compression complete!")
