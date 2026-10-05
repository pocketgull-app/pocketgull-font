#!/usr/bin/env python3
"""
PocketGull Typefoundry: Precision Duplicate Node & Degenerate Contour Purger
===========================================================================
Eliminates consecutive identical points and drops degenerate (< 3 point)
zero-area micro-tick contours across all simple glyphs in fonts/ttf/:
- Preserves 100% of authentic curves, letterforms, and optotypes.
- Purges zero-area line segments and duplicate closing vertices (Dieter Rams Law 10).
- Updates numberOfContours and recalculates bounding boxes.
- Zero-Width format controls (uni200B, uni200C, uni200D, uni2060, uFEFF) are preserved at 0 advance width.
"""

from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def clean_font(ttf_path: Path):
    font = TTFont(str(ttf_path))
    glyf = font["glyf"]
    cleaned_glyphs = 0

    for name in font.getGlyphOrder():
        glyph = glyf[name]
        if glyph.isComposite() or glyph.numberOfContours <= 0:
            continue

        coords = list(glyph.coordinates)
        flags = list(glyph.flags)
        endPts = list(glyph.endPtsOfContours)

        new_coords = []
        new_flags = []
        new_endPts = []
        modified = False

        start = 0
        for end in endPts:
            c_coords = coords[start:end + 1]
            c_flags = flags[start:end + 1]

            filtered_coords = []
            filtered_flags = []
            for c, f in zip(c_coords, c_flags):
                if not filtered_coords or c != filtered_coords[-1]:
                    filtered_coords.append(c)
                    filtered_flags.append(f)
                else:
                    modified = True

            # Check loop closing duplicate
            if len(filtered_coords) > 1 and filtered_coords[0] == filtered_coords[-1]:
                filtered_coords.pop()
                filtered_flags.pop()
                modified = True

            # If contour has at least 3 unique points, keep it; otherwise drop degenerate 0-area contour
            if len(filtered_coords) >= 3:
                new_coords.extend(filtered_coords)
                new_flags.extend(filtered_flags)
                new_endPts.append(len(new_coords) - 1)
            else:
                # Dropping degenerate zero-area micro-tick
                modified = True

            start = end + 1

        if modified:
            glyph.coordinates = GlyphCoordinates(new_coords)
            glyph.flags = bytearray([f & 0x3F for f in new_flags])
            glyph.endPtsOfContours = new_endPts
            glyph.numberOfContours = len(new_endPts)
            glyph.recalcBounds(glyf)
            glyf[name] = glyph
            cleaned_glyphs += 1

    if cleaned_glyphs > 0:
        font.save(str(ttf_path))
        print(f"  • {ttf_path.name}: cured {cleaned_glyphs} glyphs")
    font.close()
    return cleaned_glyphs

def main():
    print("======================================================================")
    print("  POCKETGULL FOUNDRY: ZERO-DUPLICATE NODE & DEGENERATE PURGE PASS")
    print("======================================================================\n")

    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    total_cleaned = 0
    for ttf in ttf_files:
        total_cleaned += clean_font(ttf)

    print(f"\n[PURGE COMPLETE] Cured glyphs across {total_cleaned} files.")

if __name__ == "__main__":
    main()
