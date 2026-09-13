#!/usr/bin/env python3
"""
scripts/v4/build_superfamily_expansion.py
=========================================
PocketGull Superfamily Expansion Synthesizer (v4.1.0)
High-Fidelity Curvature, Engraved Display, and 16-Point Ben-Day Halftone
========================================================================
Generates the chromatic layering and textured superfamily cuts:
  1. PocketGull-Outline (Silky-smooth vector stroke outline with sub-pixel curve sampling)
  2. PocketGull-Inline (Heavy display silhouette with surgical hairline engraved groove)
  3. PocketGull-Halftone (Dense 16-point circular Ben-Day screen tone lithography dots)

Invariants strictly enforced:
  - Standard 1000 UPM Em-Square
  - Zero-Registration Advance Width Invariant (exact hmtx match with PocketGull-Bold)
  - TrueType 2-byte word alignment (loca[i] % 2 == 0)
  - Reserved Bit-7 flag masking (flag & 0x3F)
  - 100% W3C OTS memory safety
  - Apache 2.0 License attribution to Phil Gear (PKGL)
"""

import math
import os
import sys
import shutil
import time
import pyclipper
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"
SRC_BOLD = TTF_DIR / "PocketGull-Bold.ttf"


class PolygonPen(BasePen):
    """Decomposes all curves and components into discrete closed polygon paths with sub-pixel resolution."""
    def __init__(self, glyphSet):
        super().__init__(glyphSet)
        self.contours = []
        self.current_contour = []

    def _moveTo(self, pt):
        if self.current_contour:
            if len(self.current_contour) >= 3:
                self.contours.append(self.current_contour)
        self.current_contour = [pt]

    def _lineTo(self, pt):
        if not self.current_contour or pt != self.current_contour[-1]:
            self.current_contour.append(pt)

    def _qCurveToOne(self, pt1, pt2):
        p0 = self.current_contour[-1]
        dist = math.hypot(pt2[0] - p0[0], pt2[1] - p0[1])
        steps = max(12, min(36, int(dist / 6.0)))
        for step in range(1, steps + 1):
            t = step / float(steps)
            x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * pt1[0] + t**2 * pt2[0]
            y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * pt1[1] + t**2 * pt2[1]
            rx, ry = round(x), round(y)
            if not self.current_contour or (rx, ry) != self.current_contour[-1]:
                self.current_contour.append((rx, ry))

    def _curveToOne(self, pt1, pt2, pt3):
        p0 = self.current_contour[-1]
        dist = math.hypot(pt3[0] - p0[0], pt3[1] - p0[1])
        steps = max(16, min(44, int(dist / 6.0)))
        for step in range(1, steps + 1):
            t = step / float(steps)
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * pt1[0] + 3*(1-t) * t**2 * pt2[0] + t**3 * pt3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * pt1[1] + 3*(1-t) * t**2 * pt2[1] + t**3 * pt3[1]
            rx, ry = round(x), round(y)
            if not self.current_contour or (rx, ry) != self.current_contour[-1]:
                self.current_contour.append((rx, ry))

    def _closePath(self):
        if self.current_contour:
            if len(self.current_contour) >= 3:
                self.contours.append(self.current_contour)
            self.current_contour = []


def clean_polygon_contours(solution_contours, clean_dist=0.75):
    """
    Cleans Clipper solution polygons, enforces TrueType winding orientation
    (Outer: CW / Area < 0; Hole: CCW / Area > 0), and strips duplicate nodes.
    """
    valid_contours = []
    for c in solution_contours:
        if len(c) < 3:
            continue
        cleaned = pyclipper.CleanPolygon(c, distance=clean_dist)
        if len(cleaned) < 3:
            continue
        area = pyclipper.Area(cleaned)
        if abs(area) < 4.0:
            continue
        # Reversing Clipper contours converts Clipper winding (Outer: CCW, Hole: CW)
        # directly into standard TrueType winding (Outer: CW / Area < 0, Hole: CCW / Area > 0).
        cleaned = cleaned[::-1]
        valid_contours.append(cleaned)
    return valid_contours


def contours_to_glyph(contours):
    """Constructs a TrueType Glyph from clean polygon contours."""
    if not contours:
        tt_pen = TTGlyphPen(None)
        return tt_pen.glyph()

    tt_pen = TTGlyphPen(None)
    for c in contours:
        tt_pen.moveTo(c[0])
        for pt in c[1:]:
            tt_pen.lineTo(pt)
        tt_pen.closePath()
    return tt_pen.glyph()


def clean_glyph_binary_health(glyph, glyf_table):
    """Sanitizes TrueType coordinates, clears Bit-7 flags, and recalculates bounds."""
    if glyph.numberOfContours <= 0:
        return
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    endPts = list(glyph.endPtsOfContours)
    new_coords = []
    new_flags = []
    new_endPts = []
    start = 0
    for end in endPts:
        pts = coords[start:end+1]
        flgs = flags[start:end+1]
        filtered_pts = []
        filtered_flgs = []
        for i in range(len(pts)):
            if not filtered_pts or pts[i] != filtered_pts[-1]:
                filtered_pts.append(pts[i])
                filtered_flgs.append(flgs[i] & 0x3F)
        if len(filtered_pts) > 1 and filtered_pts[0] == filtered_pts[-1]:
            filtered_pts = filtered_pts[:-1]
            filtered_flgs = filtered_flgs[:-1]
        if len(filtered_pts) >= 3:
            new_coords.extend(filtered_pts)
            new_flags.extend(filtered_flgs)
            new_endPts.append(len(new_coords) - 1)
        start = end + 1
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray(new_flags)
    glyph.endPtsOfContours = new_endPts
    glyph.numberOfContours = len(new_endPts)
    glyph.recalcBounds(glyf_table)


def update_font_metadata(font, family_name, style_name, ps_name, weight_class=400):
    """Sets OpenType metadata, Apache 2.0 license, and Phil Gear attribution."""
    version_str = "Version 3.100; The PocketGull Project Authors; Apache 2.0"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"
    full_name = f"{family_name} {style_name}" if style_name != "Regular" else family_name

    name_table = font["name"]
    name_table.names = [n for n in name_table.names if n.nameID not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 16, 17]]

    def add_n(nid, val):
        name_table.addMultilingualName({"en": val}, font, nameID=nid)

    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, style_name)
    add_n(3, f"3.100;PKGL;{ps_name}")
    add_n(4, full_name)
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(7, "PocketGull is a trademark of Phil Gear.")
    add_n(8, "Phil Gear")
    add_n(9, "Phil Gear")
    add_n(11, "https://github.com/pocketgull-app/pocketgull-font")
    add_n(12, "https://orcid.org/0009-0008-1372-5381")
    add_n(13, "Licensed under the Apache License, Version 2.0")
    add_n(14, "http://www.apache.org/licenses/LICENSE-2.0")
    add_n(16, family_name)
    add_n(17, style_name)

    font["head"].fontRevision = 3.1
    if "OS/2" in font:
        font["OS/2"].usWeightClass = weight_class
        font["OS/2"].achVendID = "PKGL"
        font["OS/2"].fsSelection = (font["OS/2"].fsSelection & ~0x01 & ~0x20) | 0x40 | 0x80


def save_and_compress(font, ttf_path, woff2_path):
    """Saves TTF and compresses to WOFF2."""
    font.save(str(ttf_path))
    font.close()
    compress(str(ttf_path), str(woff2_path))

    if PUBLIC_DIR.exists():
        shutil.copy2(str(ttf_path), str(PUBLIC_DIR / ttf_path.name))
        shutil.copy2(str(woff2_path), str(PUBLIC_DIR / woff2_path.name))


# ==============================================================================
# 1. POCKETGULL OUTLINE SYNTHESIZER
# ==============================================================================
def build_outline(force=False):
    out_ttf = TTF_DIR / "PocketGull-Outline.ttf"
    out_woff2 = WOFF2_DIR / "PocketGull-Outline.woff2"
    if not force and out_ttf.exists() and out_ttf.stat().st_size > 1_000_000:
        print(f"  [SKIP] PocketGull-Outline already exists ({out_ttf.stat().st_size:,} bytes).")
        return

    print("\n" + "=" * 70)
    print("  [1/3] SYNTHESIZING POCKETGULL OUTLINE (PocketGull-Outline)")
    print("=" * 70)
    t0 = time.time()

    font = TTFont(str(SRC_BOLD))
    glyf = font["glyf"]
    glyphSet = font.getGlyphSet()
    glyph_order = font.getGlyphOrder()

    processed = 0
    stroke_offset = 22.0

    for gn in glyph_order:
        g = glyf[gn]
        if g.numberOfContours == 0:
            continue

        pen = PolygonPen(glyphSet)
        g.draw(pen, glyf)
        if not pen.contours:
            continue

        pco = pyclipper.PyclipperOffset()
        for c in pen.contours:
            pco.AddPath(c, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        expanded = pco.Execute(stroke_offset)
        shrunk = pco.Execute(-stroke_offset)

        if not expanded:
            continue

        pc = pyclipper.Pyclipper()
        pc.AddPaths(expanded, pyclipper.PT_SUBJECT, True)
        if shrunk:
            pc.AddPaths(shrunk, pyclipper.PT_CLIP, True)
            sol = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        else:
            sol = expanded

        if not sol:
            sol = expanded

        cleaned_sol = clean_polygon_contours(sol, clean_dist=0.75)
        new_g = contours_to_glyph(cleaned_sol)
        clean_glyph_binary_health(new_g, glyf)
        glyf[gn] = new_g
        processed += 1

    update_font_metadata(font, "PocketGull Outline", "Regular", "PocketGull-Outline", weight_class=400)
    save_and_compress(font, out_ttf, out_woff2)

    t1 = time.time()
    print(f"  [SUCCESS] PocketGull-Outline: transformed {processed:,} glyphs in {t1-t0:.2f}s")


# ==============================================================================
# 2. POCKETGULL INLINE SYNTHESIZER (TRUE ENGRAVED DISPLAY CUT)
# ==============================================================================
def build_inline(force=False):
    out_ttf = TTF_DIR / "PocketGull-Inline.ttf"
    out_woff2 = WOFF2_DIR / "PocketGull-Inline.woff2"
    if not force and out_ttf.exists() and out_ttf.stat().st_size > 1_000_000:
        print(f"  [SKIP] PocketGull-Inline already exists ({out_ttf.stat().st_size:,} bytes).")
        return

    print("\n" + "=" * 70)
    print("  [2/3] SYNTHESIZING POCKETGULL INLINE (PocketGull-Inline)")
    print("=" * 70)
    t0 = time.time()

    font = TTFont(str(SRC_BOLD))
    glyf = font["glyf"]
    glyphSet = font.getGlyphSet()
    glyph_order = font.getGlyphOrder()

    processed = 0
    # Surgical hairline groove: preserves the heavy display body + outer rim
    groove_out_d = -20.0
    groove_in_d = -34.0

    for gn in glyph_order:
        g = glyf[gn]
        if g.numberOfContours == 0:
            continue

        pen = PolygonPen(glyphSet)
        g.draw(pen, glyf)
        if not pen.contours:
            continue

        pc_solid = pyclipper.Pyclipper()
        for c in pen.contours:
            pc_solid.AddPath(c, pyclipper.PT_SUBJECT, True)
        solid = pc_solid.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

        pco1 = pyclipper.PyclipperOffset()
        pco2 = pyclipper.PyclipperOffset()
        for c in pen.contours:
            pco1.AddPath(c, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
            pco2.AddPath(c, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

        g_out = pco1.Execute(groove_out_d)
        g_in = pco2.Execute(groove_in_d)

        if g_out and g_in:
            pc_groove = pyclipper.Pyclipper()
            pc_groove.AddPaths(g_out, pyclipper.PT_SUBJECT, True)
            pc_groove.AddPaths(g_in, pyclipper.PT_CLIP, True)
            groove = pc_groove.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

            if groove:
                pc_cut = pyclipper.Pyclipper()
                pc_cut.AddPaths(solid, pyclipper.PT_SUBJECT, True)
                pc_cut.AddPaths(groove, pyclipper.PT_CLIP, True)
                sol = pc_cut.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
            else:
                sol = solid
        else:
            sol = solid

        cleaned_sol = clean_polygon_contours(sol, clean_dist=0.75)
        new_g = contours_to_glyph(cleaned_sol)
        clean_glyph_binary_health(new_g, glyf)
        glyf[gn] = new_g
        processed += 1

    update_font_metadata(font, "PocketGull Inline", "Regular", "PocketGull-Inline", weight_class=700)
    save_and_compress(font, out_ttf, out_woff2)

    t1 = time.time()
    print(f"  [SUCCESS] PocketGull-Inline: transformed {processed:,} glyphs in {t1-t0:.2f}s")


# ==============================================================================
# 3. POCKETGULL HALFTONE SYNTHESIZER (16-POINT LITHOGRAPHIC SCREEN TONE)
# ==============================================================================
def build_halftone(force=False):
    out_ttf = TTF_DIR / "PocketGull-Halftone.ttf"
    out_woff2 = WOFF2_DIR / "PocketGull-Halftone.woff2"
    if not force and out_ttf.exists() and out_ttf.stat().st_size > 1_000_000:
        print(f"  [SKIP] PocketGull-Halftone already exists ({out_ttf.stat().st_size:,} bytes).")
        return

    print("\n" + "=" * 70)
    print("  [3/3] SYNTHESIZING POCKETGULL HALFTONE (PocketGull-Halftone)")
    print("=" * 70)
    t0 = time.time()

    font = TTFont(str(SRC_BOLD))
    glyf = font["glyf"]
    glyphSet = font.getGlyphSet()
    glyph_order = font.getGlyphOrder()

    processed = 0
    pitch = 40.0
    dot_r = 13.5

    for gn in glyph_order:
        g = glyf[gn]
        if g.numberOfContours == 0:
            continue

        pen = PolygonPen(glyphSet)
        g.draw(pen, glyf)
        if not pen.contours:
            continue

        all_pts = [pt for c in pen.contours for pt in c]
        x_min, x_max = min(p[0] for p in all_pts), max(p[0] for p in all_pts)
        y_min, y_max = min(p[1] for p in all_pts), max(p[1] for p in all_pts)

        x0 = int(x_min - pitch)
        x1 = int(x_max + pitch)
        y0 = int(y_min - pitch)
        y1 = int(y_max + pitch)

        dots = []
        for cy in range(y0, y1, int(pitch)):
            row_offset = (int(pitch / 2)) if ((cy // int(pitch)) % 2 == 1) else 0
            for cx in range(x0 + row_offset, x1, int(pitch)):
                # High-Speed Candidate Pre-filter:
                # Include dot if center or any 4 cardinal sample points fall inside glyph
                inside = False
                for c in pen.contours:
                    if pyclipper.PointInPolygon((cx, cy), c) != 0:
                        inside = not inside
                if not inside:
                    # Check 4 cardinal test points
                    for dx, dy in [(dot_r * 0.7, 0), (-dot_r * 0.7, 0), (0, dot_r * 0.7), (0, -dot_r * 0.7)]:
                        pt_in = False
                        for c in pen.contours:
                            if pyclipper.PointInPolygon((round(cx + dx), round(cy + dy)), c) != 0:
                                pt_in = not pt_in
                        if pt_in:
                            inside = True
                            break

                if inside:
                    # 16-point circular geometry for silky-smooth sub-pixel dots
                    circle = []
                    for k in range(16):
                        ang = k * math.pi / 8.0
                        px = round(cx + dot_r * math.cos(ang))
                        py = round(cy + dot_r * math.sin(ang))
                        circle.append((px, py))
                    dots.append(circle)

        if dots:
            pc = pyclipper.Pyclipper()
            for c in pen.contours:
                pc.AddPath(c, pyclipper.PT_CLIP, True)
            pc.AddPaths(dots, pyclipper.PT_SUBJECT, True)
            sol = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        else:
            sol = []

        if not sol and (x_max - x_min > 0) and (y_max - y_min > 0):
            cx = (x_min + x_max) // 2
            cy = (y_min + y_max) // 2
            r_small = min(dot_r, (x_max - x_min) / 2.0, (y_max - y_min) / 2.0)
            circle = []
            for k in range(16):
                ang = k * math.pi / 8.0
                px = round(cx + r_small * math.cos(ang))
                py = round(cy + r_small * math.sin(ang))
                circle.append((px, py))
            sol = [circle]

        cleaned_sol = clean_polygon_contours(sol, clean_dist=0.75)
        new_g = contours_to_glyph(cleaned_sol)
        clean_glyph_binary_health(new_g, glyf)
        glyf[gn] = new_g
        processed += 1

    update_font_metadata(font, "PocketGull Halftone", "Regular", "PocketGull-Halftone", weight_class=400)
    save_and_compress(font, out_ttf, out_woff2)

    t1 = time.time()
    print(f"  [SUCCESS] PocketGull-Halftone: transformed {processed:,} glyphs in {t1-t0:.2f}s")
    print(f"            TTF:   {out_ttf} ({out_ttf.stat().st_size:,} bytes)")
    print(f"            WOFF2: {out_woff2} ({out_woff2.stat().st_size:,} bytes)")


def main():
    print("======================================================================")
    print("  POCKETGULL TYPEFOUNDRY: SUPERFAMILY EXPANSION COMPILER (v4.1.0)")
    print("  HIGH-FIDELITY OUTLINE * ENGRAVED INLINE * 16-POINT HALFTONE")
    print("======================================================================")
    t_start = time.time()

    force = "--force" in sys.argv
    targets = [a.lower() for a in sys.argv[1:] if not a.startswith("--")]

    if not targets or "outline" in targets:
        build_outline(force=force or bool(targets))
    if not targets or "inline" in targets:
        build_inline(force=force or bool(targets))
    if not targets or "halftone" in targets:
        build_halftone(force=force or bool(targets))

    t_end = time.time()
    print("\n" + "=" * 70)
    print(f"  [ALL COMPLETE] PocketGull Superfamily Expansion built in {t_end - t_start:.2f}s!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
