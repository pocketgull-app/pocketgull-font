#!/usr/bin/env python3
"""
scripts/fetch_clean_noto_sources.py
===================================
Automated clean-room fetcher for certified Google Noto (SIL OFL 1.1) font sources.
Downloads upstream open-source fonts directly from Google Fonts repository
into `sources/clean_upstream/` to decouple the foundry from proprietary OS fonts.
"""

import os
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CLEAN_DIR = ROOT_DIR / "sources" / "clean_upstream"

NOTO_SOURCES = [
    ("noto_inuktitut", "notosanscanadianaboriginal", "NotoSansCanadianAboriginal[wght].ttf"),
    ("noto_cherokee", "notosanscherokee", "NotoSansCherokee[wght].ttf"),
    ("noto_tifinagh", "notosanstifinagh", "NotoSansTifinagh-Regular.ttf"),
    ("noto_ethiopic", "notosansethiopic", "NotoSansEthiopic[wdth,wght].ttf"),
    ("noto_adlam", "notosansadlam", "NotoSansAdlam[wght].ttf"),
    ("noto_vai", "notosansvai", "NotoSansVai-Regular.ttf"),
    ("noto_duployan", "notosansduployan", "NotoSansDuployan-Regular.ttf"),
    ("noto_arabic", "notosansarabic", "NotoSansArabic[wdth,wght].ttf"),
    ("noto_hebrew", "notosanshebrew", "NotoSansHebrew[wdth,wght].ttf"),
    ("noto_devanagari", "notosansdevanagari", "NotoSansDevanagari[wdth,wght].ttf"),
    ("noto_bengali", "notosansbengali", "NotoSansBengali[wdth,wght].ttf"),
    ("noto_tamil", "notosanstamil", "NotoSansTamil[wdth,wght].ttf"),
    ("noto_telugu", "notosanstelugu", "NotoSansTelugu[wdth,wght].ttf"),
    ("noto_kannada", "notosanskannada", "NotoSansKannada[wdth,wght].ttf"),
    ("noto_malayalam", "notosansmalayalam", "NotoSansMalayalam[wdth,wght].ttf"),
    ("noto_gujarati", "notosansgujarati", "NotoSansGujarati[wdth,wght].ttf"),
    ("noto_gurmukhi", "notosansgurmukhi", "NotoSansGurmukhi[wdth,wght].ttf"),
    ("noto_oriya", "notosansoriya", "NotoSansOriya[wdth,wght].ttf"),
    ("noto_sinhala", "notosanssinhala", "NotoSansSinhala[wdth,wght].ttf"),
]

BASE_URL = "https://github.com/google/fonts/raw/main/ofl/"

def fetch_all():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    print("=" * 80)
    print("  FETCHING CLEAN-ROOM GOOGLE NOTO SOURCES (SIL OFL 1.1)")
    print(f"  Target Cache Directory: {CLEAN_DIR}")
    print("=" * 80)

    # 1. Fetch OFL License text from upstream
    ofl_dest = CLEAN_DIR / "OFL-Noto.txt"
    if not ofl_dest.exists() or ofl_dest.stat().st_size == 0:
        license_url = f"{BASE_URL}notosans/OFL.txt"
        print(f"  Downloading Noto OFL text from {license_url}...")
        try:
            req = urllib.request.Request(license_url, headers={"User-Agent": "PocketGullTypefoundry/3.1"})
            with urllib.request.urlopen(req, timeout=15) as res, open(ofl_dest, "wb") as f:
                f.write(res.read())
            print("  [OK] Saved OFL-Noto.txt")
        except Exception as e:
            print(f"  [WARN] Failed to fetch license: {e}")

    # 2. Fetch fonts
    success_count = 0
    for key, folder, filename in NOTO_SOURCES:
        dest = CLEAN_DIR / filename
        if dest.exists() and dest.stat().st_size > 5000:
            print(f"  [EXISTS] {key} -> {filename} ({dest.stat().st_size:,} bytes)")
            success_count += 1
            continue

        raw_name = filename.replace("[", "%5B").replace("]", "%5D")
        url = f"{BASE_URL}{folder}/{raw_name}"
        print(f"  [DOWNLOADING] {key} ({filename})...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PocketGullTypefoundry/3.1"})
            with urllib.request.urlopen(req, timeout=30) as res, open(dest, "wb") as f:
                content = res.read()
                f.write(content)
            print(f"  [OK] Saved {filename} ({len(content):,} bytes)")
            success_count += 1
        except Exception as e:
            print(f"  [FAIL] Failed to download {url}: {e}")

    print("\n" + "=" * 80)
    print(f"  COMPLETED: {success_count}/{len(NOTO_SOURCES)} Google Noto font sources verified in clean cache.")
    print("=" * 80)
    if success_count < len(NOTO_SOURCES):
        sys.exit(1)

if __name__ == "__main__":
    fetch_all()
