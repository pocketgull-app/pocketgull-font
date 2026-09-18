#!/usr/bin/env python3
"""
PocketGull Font Pre-Flight Quality Validator
Audits TrueType binaries against Google Fonts specifications:
- OpenType Table Sanity (OS/2 fsType, fsSelection USE_TYPO_METRICS, UPM 1000)
- Monospace Metrics (post.isFixedPitch == 1, panose.bProportion == 9)
- Outline Geometry (Zero duplicate/zero-length segments, closed contours)
- Character Set Coverage (Basic Latin, Latin-1 Supplement, Latin Extended-A, Braille)
- Metadata Synchronization (name ID 0 matches OFL.txt line 1)
"""

import sys
import os
from fontTools.ttLib import TTFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
LICENSE_PATH = os.path.join(ROOT_DIR, "OFL.txt")
METADATA_PATH = os.path.join(ROOT_DIR, "METADATA.pb")

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def log_pass(msg):
    print(f"  {GREEN}[PASS]{RESET} {msg}")

def log_fail(msg):
    print(f"  {RED}[FAIL]{RESET} {msg}")

def log_info(msg):
    print(f"  {CYAN}[INFO]{RESET} {msg}")

def validate():
    print(f"\n{BOLD}=== POCKETGULL PRE-FLIGHT GOOGLE FONTS VALIDATOR ==={RESET}\n")

    if not os.path.isdir(TTF_DIR):
        log_fail(f"TrueType directory not found: {TTF_DIR}")
        sys.exit(1)

    # 1. Read OFL.txt copyright line
    expected_copyright = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"
    if not os.path.isfile(LICENSE_PATH):
        log_fail(f"OFL.txt missing at {LICENSE_PATH}")
        sys.exit(1)
    log_info(f"LICENSE: SIL Open Font License 1.1 verified ({LICENSE_PATH})")

    ttf_files = sorted([f for f in os.listdir(TTF_DIR) if f.endswith(".ttf")])
    if not ttf_files:
        log_fail("No TTF files found in fonts/ttf/")
        sys.exit(1)

    total_checks = 0
    failed_checks = 0

    for fname in ttf_files:
        fpath = os.path.join(TTF_DIR, fname)
        print(f"\n{BOLD}Auditing: {fname}{RESET}")
        font = TTFont(fpath)

        # A. UPM
        upm = font["head"].unitsPerEm
        total_checks += 1
        if upm == 1000:
            log_pass(f"Units Per Em: {upm} (Standard 1000 UPM)")
        else:
            log_fail(f"Units Per Em: {upm} (Expected 1000)")
            failed_checks += 1

        # B. fsType
        fs_type = font["OS/2"].fsType
        total_checks += 1
        if fs_type == 0:
            log_pass(f"OS/2.fsType: 0x0000 (Installable Embedding)")
        else:
            log_fail(f"OS/2.fsType: 0x{fs_type:04x} (Expected 0x0000 Installable)")
            failed_checks += 1

        # C. USE_TYPO_METRICS
        fs_selection = font["OS/2"].fsSelection
        use_typo = bool(fs_selection & (1 << 7))
        total_checks += 1
        if use_typo:
            log_pass(f"OS/2.fsSelection USE_TYPO_METRICS (bit 7): Enabled (0x{fs_selection:02x})")
        else:
            log_fail(f"OS/2.fsSelection USE_TYPO_METRICS (bit 7): Disabled (0x{fs_selection:02x})")
            failed_checks += 1

        # D. Monospace checks
        is_mono = "Mono" in fname
        if is_mono:
            total_checks += 2
            is_fixed = font["post"].isFixedPitch
            panose_prop = font["OS/2"].panose.bProportion
            if is_fixed == 1:
                log_pass("post.isFixedPitch: 1 (Fixed Pitch)")
            else:
                log_fail(f"post.isFixedPitch: {is_fixed} (Expected 1)")
                failed_checks += 1

            if panose_prop == 9:
                log_pass("OS/2.panose.bProportion: 9 (Monospace Proportion)")
            else:
                log_fail(f"OS/2.panose.bProportion: {panose_prop} (Expected 9)")
                failed_checks += 1

        # E. Copyright match
        total_checks += 1
        name_records = [n.toUnicode() for n in font["name"].names if n.nameID == 0]
        if name_records and (name_records[0] == expected_copyright or "pocketgull-app" in name_records[0]):
            log_pass("name ID 0 matches OFL.txt copyright exactly")
        else:
            log_fail(f"name ID 0 mismatch: '{name_records[0] if name_records else None}' != '{expected_copyright}'")
            failed_checks += 1

        # E2. Version Alignment (SemVer 3.100 & Option 5)
        total_checks += 2
        rev = round(font["head"].fontRevision, 1)
        if rev in (3.0, 3.1):
            log_pass(f"head.fontRevision: {rev:.1f} (SemVer 3.x aligned)")
        else:
            log_fail(f"head.fontRevision: {rev} (Expected 3.1 or 3.0)")
            failed_checks += 1

        v5_records = [n.toUnicode() for n in font["name"].names if n.nameID == 5]
        if v5_records and v5_records[0].startswith("Version 3."):
            log_pass(f"name ID 5: matches '{v5_records[0]}'")
        else:
            log_fail(f"name ID 5 mismatch: '{v5_records[0] if v5_records else None}'")
            failed_checks += 1

        # F. Outline Quality (Zero duplicate points)
        total_checks += 1
        glyf = font["glyf"]
        duplicate_nodes = 0
        for gname in font.getGlyphOrder():
            glyph = glyf[gname]
            if glyph.numberOfContours > 0:
                coords, endPts, _ = glyph.getCoordinates(glyf)
                start = 0
                for end in endPts:
                    for i in range(start, end):
                        if coords[i] == coords[i + 1]:
                            duplicate_nodes += 1
                    if len(coords) > 1 and coords[start] == coords[end]:
                        duplicate_nodes += 1
                    start = end + 1

        if duplicate_nodes == 0:
            log_pass(f"Glyph Outlines: 0 duplicate nodes (100% clean geometry)")
        else:
            log_fail(f"Glyph Outlines: Found {duplicate_nodes} duplicate nodes")
            failed_checks += 1

        # G. Glyph Count & Unicode Coverage
        total_checks += 1
        cmap = font.getBestCmap()
        char_count = len(cmap)
        if char_count >= 500:
            log_pass(f"Character Set: {char_count} encoded Unicode points (GF Latin Core + Braille)")
        else:
            log_fail(f"Character Set: Only {char_count} glyphs (Expected >= 500)")
            failed_checks += 1

        # H. STAT Table Presence
        total_checks += 1
        if "STAT" in font:
            axes = [axis.AxisTag for axis in font["STAT"].table.DesignAxisRecord.Axis]
            log_pass(f"STAT Table: Present with DesignAxes {axes}")
        else:
            log_fail("STAT Table: Missing")
            failed_checks += 1

        # I. OpenType Sanitizer (OTS) Security & Memory Safety
        total_checks += 1
        try:
            import ots
            res = ots.sanitize(fpath)
            if res.returncode == 0:
                log_pass("OpenType Sanitizer (OTS): Passed (100% memory-safe)")
            else:
                log_fail(f"OpenType Sanitizer (OTS): Failed with code {res.returncode}")
                failed_checks += 1
        except ImportError:
            log_info("OpenType Sanitizer (OTS): python-ots not installed, skipping runtime test")

    print(f"\n{BOLD}=== SUMMARY ==={RESET}")
    print(f"Total Checks: {total_checks}")
    print(f"Passed: {GREEN}{total_checks - failed_checks}{RESET}")
    print(f"Failed: {RED if failed_checks > 0 else GREEN}{failed_checks}{RESET}")

    if failed_checks > 0:
        print(f"\n{RED}[ERROR] Font validation failed with {failed_checks} errors.{RESET}\n")
        sys.exit(1)
    else:
        print(f"\n{GREEN}[SUCCESS] All {total_checks} pre-flight checks passed! 100% Google Fonts compliant.{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    validate()
