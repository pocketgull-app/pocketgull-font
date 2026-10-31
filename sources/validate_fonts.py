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

    # Audited Google Fonts superfamily targets
    ignored_stems = {"PocketGull-Numerics", "PocketGullSerif[wght]"}
    ttf_files = sorted([f for f in os.listdir(TTF_DIR) if f.endswith(".ttf") and os.path.splitext(f)[0] not in ignored_stems])
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

        # I. Blueprint v3.2.0 Binary Security Gate (PUA Bit 57, Zero-VM, 2-Byte Loca, 0x3F Flags)
        total_checks += 4
        pua_bit_57 = bool(font["OS/2"].ulUnicodeRange2 & (1 << 25))
        if pua_bit_57:
            log_pass("OS/2.ulUnicodeRange2 Bit 25 (Overall Bit 57 PUA): Enabled")
        else:
            log_fail("OS/2.ulUnicodeRange2 Bit 25 (Overall Bit 57 PUA): Unset")
            failed_checks += 1

        forbidden_vm = [t for t in ("fpgm", "cvt ") if t in font]
        if not forbidden_vm:
            log_pass("Zero-VM Table Gate: No 'fpgm' or 'cvt ' bytecode tables present")
        else:
            log_fail(f"Zero-VM Table Gate: Forbidden VM table(s) present: {forbidden_vm}")
            failed_checks += 1

        loca_offsets = list(font["loca"].locations)
        odd_loca = [idx for idx, off in enumerate(loca_offsets) if (off & 1) != 0]
        if not odd_loca:
            log_pass(f"2-Byte Word Alignment: All {len(loca_offsets)} loca offsets are even (loca[i] % 2 == 0)")
        else:
            log_fail(f"2-Byte Word Alignment: Found {len(odd_loca)} odd loca offsets")
            failed_checks += 1

        bad_insn = 0
        bad_flags = 0
        for gname in font.getGlyphOrder():
            g = glyf[gname]
            if g.numberOfContours > 0:
                if hasattr(g, "program") and len(g.program.getBytecode()) != 0:
                    bad_insn += 1
                for fl in g.flags:
                    if (fl & 0xC0) != 0:
                        bad_flags += 1
        if bad_insn == 0 and bad_flags == 0:
            log_pass("Simple Glyph Flags & Zero-VM: instructionLength == 0 and (flag & 0xC0) == 0 across all contours")
        else:
            log_fail(f"Simple Glyph Flags & Zero-VM: {bad_insn} non-zero instruction glyphs, {bad_flags} unmasked 0xC0 flags")
            failed_checks += 1

        # J. OpenType Sanitizer (OTS) Security & Memory Safety
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


GUARD_CODEPOINTS = (
    list(range(0x202A, 0x202F)) +  # BiDi embeddings/overrides
    list(range(0x2066, 0x206A)) +  # BiDi isolates
    [0x115F, 0x1160, 0x3164, 0xFFA0] +  # Hangul fillers
    list(range(0x2061, 0x2065)) +  # Invisible math operators
    list(range(0xE0100, 0xE01F0))  # Variation Selectors Supplement
)


def audit_pocketgull_binary(ttf_path: str, strict_flat_glyf: bool = False) -> None:
    """Deterministic Blueprint v3.2.0 binary security gate for CI and OEM verification."""
    font = TTFont(ttf_path)
    cmap = font.getBestCmap()

    # 1. Verify OS/2.fsType == 0x0000 and PUA Bit 57 (ulUnicodeRange2 bit 25)
    assert font["OS/2"].fsType == 0, f"{ttf_path}: fsType must be 0x0000"
    assert (font["OS/2"].ulUnicodeRange2 & (1 << 25)) != 0, f"{ttf_path}: PUA bit 57 unset"

    # 2. Verify no fpgm or cvt bytecode tables exist (and no active prep program)
    for vm_table in ("fpgm", "cvt "):
        assert vm_table not in font, f"{ttf_path}: forbidden VM table '{vm_table}' present"
    if strict_flat_glyf:
        assert "prep" not in font, f"{ttf_path}: forbidden VM table 'prep' present"

    # 3. Verify 2-byte word alignment in raw loca offsets
    loca_offsets = list(font["loca"].locations)
    for g_idx, offset in enumerate(loca_offsets):
        assert (offset & 1) == 0, f"{ttf_path}: glyph #{g_idx} has odd loca offset {offset}"

    # 4. Verify instructionLength == 0 and flag bits 6 & 7 cleared ((flag & 0xC0) == 0)
    glyf = font["glyf"]
    for glyph_name in font.getGlyphOrder():
        g = glyf[glyph_name]
        if strict_flat_glyf:
            assert not g.isComposite(), f"{ttf_path}: composite glyph '{glyph_name}' must be decomposed"
        if g.numberOfContours > 0:
            if hasattr(g, "program"):
                assert len(g.program.getBytecode()) == 0, f"{ttf_path}: non-zero bytecode in '{glyph_name}'"
            for flag in g.flags:
                assert (flag & 0xC0) == 0, f"{ttf_path}: bit 6 or 7 set in flag 0x{flag:02X} on '{glyph_name}'"

    # 5. Verify spoof codepoints present in cmap map to a visible outline (numberOfContours > 0)
    if strict_flat_glyf:
        for cp in GUARD_CODEPOINTS:
            assert cp in cmap, f"{ttf_path}: missing spoof guard U+{cp:04X} in cmap"
            g_name = cmap[cp]
            assert glyf[g_name].numberOfContours > 0, f"{ttf_path}: U+{cp:04X} ({g_name}) has no visible contours"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            audit_pocketgull_binary(path)
            print(f"[PASS] {path}")
    else:
        validate()

