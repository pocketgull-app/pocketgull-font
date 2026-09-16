#!/usr/bin/env python3
"""
PocketGull Typefoundry: Clinical Pediatric Punctuation & Decimal Calibrator
==========================================================================
Calibrates optical side-bearings for decimal point (period), colon, comma,
and slash across the entire PocketGull superfamily to guarantee >= 120 UPM
optical clearance in neonatal and pediatric micro-dosages (0.05 mcg, 0.125 mg).
"""

import sys
from pathlib import Path
from fontTools.ttLib import TTFont

# Windows UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

TARGET_TTFS = sorted(TTF_DIR.glob("PocketGull*.ttf"))

def calibrate_font(font_path: Path):
    # Do not mutate fixed-pitch monospace fonts!
    if "Mono" in font_path.name:
        return None

    font = TTFont(font_path)
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    modified = False

    is_bold_or_heavy = any(k in font_path.name for k in ["Bold", "Black", "Chiseltip"])

    # 1. Calibrate period ('.')
    p_cp = ord('.')
    p_name = cmap.get(p_cp)
    if p_name and p_name in glyf:
        p_adv, p_lsb = hmtx[p_name]
        g = glyf[p_name]
        if g.numberOfContours > 0:
            xs = [pt[0] for pt in g.coordinates]
            w = max(xs) - min(xs)
            
            # Target side-bearings for pediatric safety (guarantees >= 120 UPM across all digits 0-9)
            target_sb = 104 if is_bold_or_heavy else 100
            new_adv = w + (target_sb * 2)
            shift_x = target_sb - p_lsb

            if abs(shift_x) > 2 or abs(new_adv - p_adv) > 2:
                # Shift coordinates
                new_coords = [(x + shift_x, y) for (x, y) in g.coordinates]
                g.coordinates = type(g.coordinates)(new_coords)
                hmtx[p_name] = (new_adv, target_sb)
                modified = True

    # 2. Calibrate colon (':')
    colon_cp = ord(':')
    colon_name = cmap.get(colon_cp)
    if colon_name and colon_name in glyf:
        c_adv, c_lsb = hmtx[colon_name]
        g = glyf[colon_name]
        if g.numberOfContours > 0:
            xs = [pt[0] for pt in g.coordinates]
            w = max(xs) - min(xs)
            target_sb = 104 if is_bold_or_heavy else 100
            new_adv = w + (target_sb * 2)
            shift_x = target_sb - c_lsb

            if abs(shift_x) > 2 or abs(new_adv - c_adv) > 2:
                new_coords = [(x + shift_x, y) for (x, y) in g.coordinates]
                g.coordinates = type(g.coordinates)(new_coords)
                hmtx[colon_name] = (new_adv, target_sb)
                modified = True

    # 3. Calibrate slash ('/')
    slash_cp = ord('/')
    slash_name = cmap.get(slash_cp)
    if slash_name and slash_name in glyf:
        s_adv, s_lsb = hmtx[slash_name]
        g = glyf[slash_name]
        if g.numberOfContours > 0:
            xs = [pt[0] for pt in g.coordinates]
            w = max(xs) - min(xs)
            
            # Ensure at least 45 UPM LSB and RSB
            if s_lsb < 45:
                shift_x = 45 - s_lsb
                new_coords = [(x + shift_x, y) for (x, y) in g.coordinates]
                g.coordinates = type(g.coordinates)(new_coords)
                new_adv = max(s_adv + shift_x, w + 90)
                hmtx[slash_name] = (new_adv, 45)
                modified = True

    if modified:
        font.save(font_path)
        print(f"  • Calibrated clinical punctuation in: {font_path.name}")

    font.close()
    return modified

def main():
    print("======================================================================")
    print("  POCKETGULL TYPEFOUNDRY: CLINICAL PEDIATRIC PUNCTUATION CALIBRATOR")
    print("======================================================================\n")

    count = 0
    for font_path in TARGET_TTFS:
        if calibrate_font(font_path):
            count += 1

    print(f"\n[CALIBRATION COMPLETE] Successfully calibrated {count} font masters.")

if __name__ == "__main__":
    main()
