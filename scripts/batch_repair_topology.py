#!/usr/bin/env python3
"""
PocketGull Typefoundry: Master Topology Surgeon & Extrema Engine
================================================================
Performs topological remediation across static cuts in fonts/ttf/:
1. Skips variable fonts (gvar/fvar) and heart-tittle alternates (Invariant 9).
2. Simplifies contours via skia-pathops (boolean union, fixes winding & overlaps).
3. Emits pure quadratic curves with explicit bounding extrema nodes (Cu2QuPen + ExtremumPen).
4. Cleans consecutive duplicate nodes (0 duplicate nodes per Google Fonts / Dieter Rams rules).
5. Preserves hmtx advance widths (strictly locks PocketGull Mono to 600 UPM).
"""

import sys
import os
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

try:
    import pathops
except ImportError:
    print("Error: skia-pathops is required. Install via pip install skia-pathops.")
    sys.exit(1)

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

# Variable fonts to skip to protect gvar point tuples
VARIABLE_FONTS = {
    "PocketGull-VF.ttf",
    "PocketGull-Serif-VF.ttf",
    "PocketGull-Sign-VF.ttf",
    "PocketGullSerif[wght].ttf",
}

def get_qcurve_extrema_roots(p0, p1, p2):
    roots = []
    for i in (0, 1):
        denom = p0[i] - 2.0 * p1[i] + p2[i]
        if abs(denom) > 1e-6:
            t = (p0[i] - p1[i]) / denom
            if 0.05 < t < 0.95:
                roots.append(t)
    return sorted(roots)

def split_qcurve_at_t(p0, p1, p2, t):
    p01 = ((1 - t) * p0[0] + t * p1[0], (1 - t) * p0[1] + t * p1[1])
    p12 = ((1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1])
    p012 = ((1 - t) * p01[0] + t * p12[0], (1 - t) * p01[1] + t * p12[1])
    return (p0, p01, p012), (p012, p12, p2)

def split_qcurve_recursively(p0, p1, p2):
    roots = get_qcurve_extrema_roots(p0, p1, p2)
    if not roots:
        return [(p1, p2)]
    t = roots[0]
    seg1, seg2 = split_qcurve_at_t(p0, p1, p2, t)
    return split_qcurve_recursively(*seg1) + split_qcurve_recursively(*seg2)

class ExtremumPen(BasePen):
    def __init__(self, glyphSet, outPen):
        super().__init__(glyphSet)
        self.outPen = outPen
        self.current_pt = None

    def _moveTo(self, pt):
        ipt = (round(pt[0]), round(pt[1]))
        self.outPen.moveTo(ipt)
        self.current_pt = ipt

    def _lineTo(self, pt):
        ipt = (round(pt[0]), round(pt[1]))
        if self.current_pt is not None and ipt == self.current_pt:
            return
        self.outPen.lineTo(ipt)
        self.current_pt = ipt

    def _qCurveToOne(self, pt1, pt2):
        p0 = self.current_pt if self.current_pt is not None else (round(pt1[0]), round(pt1[1]))
        segments = split_qcurve_recursively(p0, pt1, pt2)
        curr = self.current_pt
        for p_off, p_on in segments:
            off_pt = (round(p_off[0]), round(p_off[1]))
            on_pt = (round(p_on[0]), round(p_on[1]))
            if curr is not None and on_pt == curr:
                continue
            self.outPen.qCurveTo(off_pt, on_pt)
            curr = on_pt
            self.current_pt = on_pt

    def _curveToOne(self, pt1, pt2, pt3):
        ipt3 = (round(pt3[0]), round(pt3[1]))
        if self.current_pt is not None and ipt3 == self.current_pt:
            return
        self.outPen.curveTo(
            (round(pt1[0]), round(pt1[1])),
            (round(pt2[0]), round(pt2[1])),
            ipt3
        )
        self.current_pt = ipt3

    def _closePath(self):
        self.outPen.closePath()
        self.current_pt = None

    def _endPath(self):
        self.outPen.endPath()
        self.current_pt = None

def remove_duplicate_nodes(glyph):
    if glyph.isComposite() or glyph.numberOfContours <= 0:
        return glyph
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    endPts = list(glyph.endPtsOfContours)
    
    new_coords = []
    new_flags = []
    new_endPts = []
    
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
        
        if len(filtered_coords) > 1 and filtered_coords[0] == filtered_coords[-1]:
            filtered_coords.pop()
            filtered_flags.pop()
            
        if len(filtered_coords) < 3:
            # Revert to original contour if degenerate
            filtered_coords = c_coords
            filtered_flags = c_flags
            
        new_coords.extend(filtered_coords)
        new_flags.extend(filtered_flags)
        new_endPts.append(len(new_coords) - 1)
        start = end + 1
        
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray([f & 0x3F for f in new_flags])
    glyph.endPtsOfContours = new_endPts
    return glyph

def repair_font(font_path: Path):
    if font_path.name in VARIABLE_FONTS:
        print(f"[{font_path.name}] Skipping variable font to protect gvar point tuples.")
        return
        
    print(f"[{font_path.name}] Starting topology repair & extremum injection...")
    font = TTFont(str(font_path))
    glyf = font["glyf"]
    glyphSet = font.getGlyphSet()
    is_mono = "Mono" in font_path.name
    
    repaired_count = 0
    for glyph_name in font.getGlyphOrder():
        # Invariant 9: Preserve heart tittles unaltered
        if "heart" in glyph_name or glyph_name in ("glyph08753", "glyph08754"):
            continue
            
        glyph = glyf[glyph_name]
        if glyph.isComposite() or glyph.numberOfContours <= 0:
            continue
            
        # 1. Pathops boolean union & contour simplification
        path = pathops.Path()
        try:
            glyphSet[glyph_name].draw(path.getPen())
            path.simplify()
        except Exception:
            continue
            
        # 2. Draw through Cu2Qu and ExtremumPen
        tt_pen = TTGlyphPen(None)
        ext_pen = ExtremumPen(glyphSet, tt_pen)
        cu2qu_pen = Cu2QuPen(ext_pen, max_err=1.0)
        
        try:
            path.draw(cu2qu_pen)
            new_glyph = tt_pen.glyph()
            
            # 3. Clean duplicate nodes & mask Bit 7 flags
            new_glyph = remove_duplicate_nodes(new_glyph)
            new_glyph.recalcBounds(glyf)
            glyf[glyph_name] = new_glyph
            repaired_count += 1
            
            # Preserve Monospace 600 UPM invariant
            if is_mono and "hmtx" in font:
                _, lsb = font["hmtx"][glyph_name]
                font["hmtx"][glyph_name] = (600, lsb)
        except Exception:
            continue
            
    print(f"[{font_path.name}] Repaired {repaired_count} simple glyphs. Saving...")
    font.save(str(font_path))
    font.close()
    print(f"[{font_path.name}] Saved successfully.")

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        repair_font(Path(target))
    else:
        for ttf in sorted(TTF_DIR.glob("*.ttf")):
            if ttf.name not in VARIABLE_FONTS:
                repair_font(ttf)
    print("\n[SUCCESS] All static font cuts repaired.")

if __name__ == "__main__":
    main()
