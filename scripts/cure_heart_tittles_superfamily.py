#!/usr/bin/env python3
"""
PocketGull Typefoundry — Master Philocardia Tittles, Punctuation & Variety Cure Engine
======================================================================================
Unifies and cures all 6 Philocardia tittle varieties across all 38 non-Sign superfamily cuts:
  - cv09 ("Philocardia Heart Tittles (i, j)"):                   i, j -> *.heart
  - cv10 ("Philocardia Heart Punctuation (!, ?, ¡, ¿)"):          !, ?, ¡, ¿ -> *.heart
  - cv19 ("Dotless Tittle Stems (i, j, !, ?, ¡, ¿)"):             i, j, ı, ȷ, !, ?, ¡, ¿ -> *.dotless
  - ss07 ("Philocardia Full Heart Suite (i, j, !, ?, ¡, ¿)"):     heart suite (cv09 + cv10)
  - ss08 ("Philocardia Blossom Tittles Suite (i, j, !, ?, ¡, ¿)"): *.blossom (✤)
  - ss09 ("Philocardia Nuqta Tittles Suite (i, j, !, ?, ¡, ¿)"):   *.nuqta (◆)
  - ss10 ("Philocardia Star Tittles Suite (i, j, !, ?, ¡, ¿)"):    *.star (✦)
  - ss11 ("Philocardia Droplet Tittles Suite (i, j, !, ?, ¡, ¿)"): *.droplet (💧)

Plus standalone monochrome symbol coverage (U+2665, U+2724, U+25C6, U+2726, U+25CF, U+1F4A7),
AxisHeight centering + math-italic dotless stems (U+1D6A4, U+1D6A5) in PocketGull-Math.ttf,
strict < min_liga GSUB lookup placement with LookupType 5/6 index remapping, and VF gvar/HVAR.
"""

from __future__ import annotations

import copy
import math
import shutil
import subprocess
import sys
from pathlib import Path

import pyclipper
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables as ot
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables._g_v_a_r import TupleVariation
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib.woff2 import compress
from fontTools.varLib.iup import iup_delta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

SKIP_FONTS = {
    "PocketGull-ASL.ttf",
    "PocketGull-Sign.ttf",
    "PocketGull-Sign-VF.ttf",
}

# Canonical 16-point clockwise (y-up) quadratic TrueType heart contour
# Normalized to x in [-0.5, +0.5], y in [0.0, 1.0], 36% central cleft, cushioned apex fillet.
NORM_HEART_PTS: list[tuple[float, float, int]] = [
    (0.00, 0.00, 1),   # bottom apex center
    (-0.07, 0.00, 0),  # left apex fillet (horizontal tangent)
    (-0.11, 0.04, 1),  # apex-to-left-flank transition
    (-0.46, 0.25, 0),  # lower left flank
    (-0.50, 0.56, 1),  # leftmost extremum
    (-0.50, 0.96, 0),  # left outer crown
    (-0.26, 1.00, 1),  # left crown peak extremum
    (-0.09, 1.00, 0),  # left inner crown
    (0.00, 0.64, 1),   # central cleft (36% depth)
    (0.09, 1.00, 0),   # right inner crown
    (0.26, 1.00, 1),   # right crown peak extremum
    (0.50, 0.96, 0),   # right outer crown
    (0.50, 0.56, 1),   # rightmost extremum
    (0.46, 0.25, 0),   # lower right flank
    (0.11, 0.04, 1),   # right-flank-to-apex transition
    (0.07, 0.00, 0),   # right apex fillet
]

NORM_BLOSSOM_PTS: list[tuple[float, float, int]] = [
    (0.00, 0.00, 1), (-0.26, 0.00, 0), (-0.17, 0.33, 1), (-0.50, 0.24, 0),
    (-0.50, 0.50, 1), (-0.50, 0.76, 0), (-0.17, 0.67, 1), (-0.26, 1.00, 0),
    (0.00, 1.00, 1), (0.26, 1.00, 0), (0.17, 0.67, 1), (0.50, 0.76, 0),
    (0.50, 0.50, 1), (0.50, 0.24, 0), (0.17, 0.33, 1), (0.26, 0.00, 0),
]

NORM_NUQTA_PTS: list[tuple[float, float, int]] = [
    (-0.06, 0.06, 1), (-0.44, 0.44, 1), (-0.50, 0.50, 0), (-0.44, 0.56, 1),
    (-0.06, 0.94, 1), (0.00, 1.00, 0), (0.06, 0.94, 1), (0.44, 0.56, 1),
    (0.50, 0.50, 0), (0.44, 0.44, 1), (0.06, 0.06, 1), (0.00, 0.00, 0),
]

NORM_STAR_PTS: list[tuple[float, float, int]] = [
    (0.00, 0.00, 1), (-0.11, 0.39, 0), (-0.50, 0.50, 1), (-0.11, 0.61, 0),
    (0.00, 1.00, 1), (0.11, 0.61, 0), (0.50, 0.50, 1), (0.11, 0.39, 0),
]

NORM_DROPLET_PTS: list[tuple[float, float, int]] = [
    (0.00, 0.00, 1), (-0.34, 0.00, 0), (-0.50, 0.34, 1), (-0.50, 0.58, 0),
    (-0.10, 0.93, 1), (-0.05, 1.00, 0), (0.00, 1.00, 1), (0.05, 1.00, 0),
    (0.10, 0.93, 1), (0.50, 0.58, 0), (0.50, 0.34, 1), (0.34, 0.00, 0),
]

NORM_DOT_PTS: list[tuple[float, float, int]] = [
    (0.00, 0.00, 1), (-0.50, 0.00, 0), (-0.50, 0.50, 1), (-0.50, 1.00, 0),
    (0.00, 1.00, 1), (0.50, 1.00, 0), (0.50, 0.50, 1), (0.50, 0.00, 0),
]

VARIETY_SHAPES: dict[str, list[tuple[float, float, int]]] = {
    "heart": NORM_HEART_PTS,
    "blossom": NORM_BLOSSOM_PTS,
    "nuqta": NORM_NUQTA_PTS,
    "star": NORM_STAR_PTS,
    "droplet": NORM_DROPLET_PTS,
}

VARIETY_ORDER = ("heart", "blossom", "nuqta", "star", "droplet")

# Standalone monochrome symbols added where missing from cmap
# (cp, gname, shape_key, std_w, std_h, std_ymin, math_w, math_h, math_ymin)
STANDALONE_SYMBOLS = [
    (0x2724, "uni2724", "blossom", 440.0, 440.0, 100.0, 400.0, 400.0, 60.0),
    (0x25C6, "uni25C6", "nuqta",   440.0, 440.0, 100.0, 400.0, 400.0, 60.0),
    (0x2726, "uni2726", "star",    460.0, 460.0,  90.0, 400.0, 400.0, 60.0),
    (0x1F4A7, "u1F4A7", "droplet", 360.0, 440.0, 100.0, 330.0, 400.0, 60.0),
    (0x25CF, "uni25CF", "dot",     400.0, 400.0, 120.0, 360.0, 360.0, 80.0),
]

BASE_SPECS = [
    # (cp, canonical_name, dot_pos, punct_or_letter)
    (0x0069, "i", "top", "letter"),
    (0x006A, "j", "top", "letter"),
    (0x0021, "exclam", "bottom", "punct"),
    (0x003F, "question", "bottom", "punct"),
    (0x00A1, "exclamdown", "top", "punct"),
    (0x00BF, "questiondown", "top", "punct"),
]

CV09_LABEL = "Philocardia Heart Tittles (i, j)"
CV10_LABEL = "Philocardia Heart Punctuation (!, ?, ¡, ¿)"
CV19_LABEL = "Dotless Tittle Stems (i, j, !, ?, ¡, ¿)"
SS07_LABEL = "Philocardia Full Heart Suite (i, j, !, ?, ¡, ¿)"
SS08_LABEL = "Philocardia Blossom Tittles Suite (i, j, !, ?, ¡, ¿)"
SS09_LABEL = "Philocardia Nuqta Tittles Suite (i, j, !, ?, ¡, ¿)"
SS10_LABEL = "Philocardia Star Tittles Suite (i, j, !, ?, ¡, ¿)"
SS11_LABEL = "Philocardia Droplet Tittles Suite (i, j, !, ?, ¡, ¿)"


def shoelace_area(pts: list[tuple[int, int]]) -> float:
    n = len(pts)
    if n < 3:
        return 0.0
    return sum(
        pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
        for i in range(n)
    ) / 2.0


def extract_contours(glyf, gname: str) -> list[dict]:
    g = glyf[gname]
    if g.isComposite() or g.numberOfContours <= 0:
        return []
    coords, endpts, flags = g.getCoordinates(glyf)
    res = []
    start = 0
    for ci, end in enumerate(endpts):
        pts = [(int(coords[k][0]), int(coords[k][1])) for k in range(start, end + 1)]
        fls = [int(flags[k]) & 0x3F for k in range(start, end + 1)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        res.append({
            "ci": ci,
            "pts": pts,
            "fls": fls,
            "xmin": min(xs),
            "xmax": max(xs),
            "ymin": min(ys),
            "ymax": max(ys),
            "w": max(xs) - min(xs),
            "h": max(ys) - min(ys),
            "area": shoelace_area(pts),
        })
        start = end + 1
    return res


def deduplicate_contour(pts: list[tuple[int, int]], fls: list[int]) -> tuple[list[tuple[int, int]], list[int]]:
    out_p: list[tuple[int, int]] = []
    out_f: list[int] = []
    for p, f in zip(pts, fls):
        if not out_p or p != out_p[-1]:
            out_p.append((int(p[0]), int(p[1])))
            out_f.append(int(f) & 0x3F)
    if len(out_p) > 1 and out_p[0] == out_p[-1]:
        out_p.pop()
        out_f.pop()
    return out_p, out_f


def build_shape_contour(
    norm_pts: list[tuple[float, float, int]],
    cx: float,
    y_min: float,
    width: float,
    height: float,
    italic_angle: float = 0.0,
) -> tuple[list[tuple[int, int]], list[int]]:
    """Builds a clockwise (y-up) quadratic TrueType contour from normalized coordinates."""
    cy = y_min + height * 0.5
    tan_a = math.tan(math.radians(-italic_angle)) if abs(italic_angle) > 1e-6 else 0.0
    pts: list[tuple[int, int]] = []
    fls: list[int] = []
    for nx, ny, on in norm_pts:
        y = y_min + ny * height
        x = cx + nx * width + (y - cy) * tan_a
        pts.append((int(round(x)), int(round(y))))
        fls.append(1 if on else 0)

    pts, fls = deduplicate_contour(pts, fls)
    if abs(italic_angle) > 1e-6 and pts:
        cur_cx = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2.0
        dx_fix = int(round(cx - cur_cx))
        if dx_fix != 0:
            pts = [(p[0] + dx_fix, p[1]) for p in pts]
    if shoelace_area(pts) > 0:
        pts = [pts[0]] + pts[1:][::-1]
        fls = [fls[0]] + fls[1:][::-1]
    return pts, fls


def build_heart_contour(
    cx: float,
    y_min: float,
    width: float,
    height: float,
    italic_angle: float = 0.0,
) -> tuple[list[tuple[int, int]], list[int]]:
    """Builds the canonical 16-point CW cushioned-apex quadratic TrueType heart contour."""
    return build_shape_contour(NORM_HEART_PTS, cx, y_min, width, height, italic_angle)


def sample_shape_polygon(
    norm_pts: list[tuple[float, float, int]],
    cx: float,
    y_min: float,
    width: float,
    height: float,
    italic_angle: float = 0.0,
    steps_per_seg: int = 10,
) -> list[tuple[int, int]]:
    """Samples a normalized quadratic contour into a Clipper-ready CCW polygon."""
    pts, fls = build_shape_contour(norm_pts, cx, y_min, width, height, italic_angle)
    n = len(pts)
    if n < 3:
        return list(pts)

    epts: list[tuple[float, float]] = []
    efls: list[int] = []
    for k in range(n):
        p0, f0 = pts[k], fls[k]
        p1, f1 = pts[(k + 1) % n], fls[(k + 1) % n]
        epts.append((float(p0[0]), float(p0[1])))
        efls.append(f0)
        if f0 == 0 and f1 == 0:
            epts.append(((p0[0] + p1[0]) * 0.5, (p0[1] + p1[1]) * 0.5))
            efls.append(1)

    m = len(epts)
    first_on = next((idx for idx, fl in enumerate(efls) if fl == 1), None)
    if first_on is None:
        return [(int(round(p[0])), int(round(p[1]))) for p in epts]
    if first_on != 0:
        epts = epts[first_on:] + epts[:first_on]
        efls = efls[first_on:] + efls[:first_on]

    poly: list[tuple[int, int]] = []
    i = 0
    while i < m:
        p0 = epts[i]
        nxt = (i + 1) % m
        if efls[nxt] == 1:
            rx, ry = int(round(p0[0])), int(round(p0[1]))
            if not poly or (rx, ry) != poly[-1]:
                poly.append((rx, ry))
            i += 1
        else:
            p1 = epts[nxt]
            p2 = epts[(i + 2) % m]
            for s in range(steps_per_seg):
                t = s / float(steps_per_seg)
                x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
                y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
                rx, ry = int(round(x)), int(round(y))
                if not poly or (rx, ry) != poly[-1]:
                    poly.append((rx, ry))
            i += 2
    if len(poly) > 1 and poly[0] == poly[-1]:
        poly.pop()
    # Clipper positive orientation is CCW (Area > 0 in y-up coords)
    if len(poly) >= 3 and pyclipper.Area(poly) < 0:
        poly = poly[::-1]
    return poly


def sample_heart_polygon(
    cx: float,
    y_min: float,
    width: float,
    height: float,
    italic_angle: float = 0.0,
    steps_per_seg: int = 10,
) -> list[tuple[int, int]]:
    return sample_shape_polygon(NORM_HEART_PTS, cx, y_min, width, height, italic_angle, steps_per_seg)


def clipper_paths_to_contours(sol_paths: list[list[tuple[int, int]]]) -> list[tuple[list[tuple[int, int]], list[int]]]:
    """Converts Clipper CCW-outer / CW-hole polygons to TrueType CW-outer / CCW-hole contours."""
    out = []
    for path in sol_paths:
        if len(path) < 3:
            continue
        cleaned = pyclipper.CleanPolygon(path, distance=0.75)
        if len(cleaned) < 3 or abs(pyclipper.Area(cleaned)) < 4.0:
            continue
        tt_pts = [(int(round(x)), int(round(y))) for x, y in cleaned[::-1]]
        tt_fls = [1] * len(tt_pts)
        tt_pts, tt_fls = deduplicate_contour(tt_pts, tt_fls)
        if len(tt_pts) >= 3:
            out.append((tt_pts, tt_fls))
    return out


def build_outline_unfused_stem(c1_pts: list[tuple[int, int]], c1_fls: list[int]) -> list[tuple[list[tuple[int, int]], list[int]]]:
    """Derives un-fused Outline outer stem (+44 UPM from inner CCW hole c1) and keeps c1 bit-identical."""
    c1_clip = list(c1_pts)
    if pyclipper.Area(c1_clip) < 0:
        c1_clip = c1_clip[::-1]
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(c1_clip, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
    exp = pco.Execute(44.0)
    outer_contours = clipper_paths_to_contours(exp)
    assert len(outer_contours) == 1, f"Expected 1 expanded stem contour in Outline, got {len(outer_contours)}"
    c1_clean_pts, c1_clean_fls = deduplicate_contour(c1_pts, c1_fls)
    return [outer_contours[0], (c1_clean_pts, c1_clean_fls)]


def build_specialty_shape_contours(
    font_name: str,
    norm_pts: list[tuple[float, float, int]],
    cx: float,
    y_min: float,
    w: float,
    h: float,
    italic_angle: float,
) -> list[tuple[list[tuple[int, int]], list[int]]]:
    """Builds style-authentic contours for Outline, Inline, and Kintsugi display cuts."""
    if font_name == "PocketGull-Outline.ttf":
        inner_w = max(92.0, w - 44.0)
        inner_h = max(92.0, h - 44.0)
        hp = sample_shape_polygon(norm_pts, cx, y_min + 22.0, inner_w, inner_h, italic_angle)
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(hp, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        exp = pco.Execute(22.0)
        shr = []
        for shrink_dist in (-22.0, -16.0, -12.0):
            cand = pco.Execute(shrink_dist)
            if len(cand) == 1:
                shr = cand
                break
            if cand and not shr:
                shr = cand
        pc = pyclipper.Pyclipper()
        pc.AddPaths(exp, pyclipper.PT_SUBJECT, True)
        if shr:
            pc.AddPaths(shr, pyclipper.PT_CLIP, True)
            sol = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
        else:
            sol = exp
        res = clipper_paths_to_contours(sol)
        if res:
            return res
        return [build_shape_contour(norm_pts, cx, y_min, w, h, italic_angle)]

    if font_name == "PocketGull-Inline.ttf":
        hp = sample_shape_polygon(norm_pts, cx, y_min, w, h, italic_angle)
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(hp, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        for outer_d, inner_d in ((-18.0, -30.0), (-13.0, -22.0)):
            go = pco.Execute(outer_d)
            gi = pco.Execute(inner_d)
            if go and gi:
                pc_g = pyclipper.Pyclipper()
                pc_g.AddPaths(go, pyclipper.PT_SUBJECT, True)
                pc_g.AddPaths(gi, pyclipper.PT_CLIP, True)
                groove = pc_g.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
                pc_c = pyclipper.Pyclipper()
                pc_c.AddPath(hp, pyclipper.PT_SUBJECT, True)
                pc_c.AddPaths(groove, pyclipper.PT_CLIP, True)
                sol = pc_c.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
                res = clipper_paths_to_contours(sol)
                if res:
                    return res
        return [build_shape_contour(norm_pts, cx, y_min, w, h, italic_angle)]

    if font_name == "PocketGull-Kintsugi.ttf":
        hp = sample_shape_polygon(norm_pts, cx, y_min, w, h, italic_angle)
        pco = pyclipper.PyclipperOffset()
        pco.AddPath(hp, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)
        for shell_d in (-24.0, -17.0):
            k_in = pco.Execute(shell_d)
            if k_in:
                pc_k = pyclipper.Pyclipper()
                pc_k.AddPath(hp, pyclipper.PT_SUBJECT, True)
                pc_k.AddPaths(k_in, pyclipper.PT_CLIP, True)
                sol = pc_k.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
                res = clipper_paths_to_contours(sol)
                if res:
                    return res
        return [build_shape_contour(norm_pts, cx, y_min, w, h, italic_angle)]

    return [build_shape_contour(norm_pts, cx, y_min, w, h, italic_angle)]


def build_specialty_heart_contours(
    font_name: str,
    cx: float,
    y_min: float,
    w: float,
    h: float,
    italic_angle: float,
) -> list[tuple[list[tuple[int, int]], list[int]]]:
    return build_specialty_shape_contours(font_name, NORM_HEART_PTS, cx, y_min, w, h, italic_angle)


def partition_stem_and_dot(
    font_name: str,
    canonical_name: str,
    dot_pos: str,
    contours: list[dict],
) -> tuple[list[tuple[list[tuple[int, int]], list[int]]], dict]:
    """
    Separates bit-identical stem contours from the dot region and computes dot bbox.
    Returns (stem_contours, dot_bbox_dict).
    """
    if font_name == "PocketGull-Halftone.ttf":
        if canonical_name in ("i", "j"):
            stem = [c for c in contours if c["ymax"] <= 555]
            dot = [c for c in contours if c["ymin"] >= 580]
        elif canonical_name in ("exclam", "question"):
            dot = [c for c in contours if c["ymax"] <= 165]
            stem = [c for c in contours if c["ymin"] >= 210]
        else:  # exclamdown, questiondown
            stem = [c for c in contours if c["ymax"] <= 320]
            dot = [c for c in contours if c["ymin"] >= 370]
        assert stem and dot, f"Halftone partition failed on {canonical_name}: stem={len(stem)}, dot={len(dot)}"
        assert len(stem) + len(dot) == len(contours), f"Halftone unpartitioned contour on {canonical_name}"
        dot_bbox = {
            "xmin": min(c["xmin"] for c in dot),
            "xmax": max(c["xmax"] for c in dot),
            "ymin": min(c["ymin"] for c in dot),
            "ymax": max(c["ymax"] for c in dot),
        }
        dot_bbox["w"] = dot_bbox["xmax"] - dot_bbox["xmin"]
        dot_bbox["h"] = dot_bbox["ymax"] - dot_bbox["ymin"]
        return [(c["pts"], c["fls"]) for c in stem], dot_bbox

    if font_name == "PocketGull-Outline.ttf" and canonical_name in ("i", "j"):
        # Base i/j in Outline has fused c0 + inner stem c1 + inner dot c2
        c1 = contours[1]
        c2 = contours[2]
        stem_contours = build_outline_unfused_stem(c1["pts"], c1["fls"])
        # Inner dot hole c2 is contracted -22 from Bold's dot; expand bbox by 22 to represent Outline's outer dot bounds
        dot_bbox = {
            "xmin": c2["xmin"] - 22,
            "xmax": c2["xmax"] + 22,
            "ymin": c2["ymin"] - 22,
            "ymax": c2["ymax"] + 22,
            "w": c2["w"] + 44,
            "h": c2["h"] + 44,
        }
        return stem_contours, dot_bbox

    if font_name == "PocketGull-Inline.ttf" and len(contours) == 6:
        # First 3 contours are stem, last 3 contours are dot
        stem = contours[:3]
        dot = contours[3:]
        dot_bbox = {
            "xmin": min(c["xmin"] for c in dot),
            "xmax": max(c["xmax"] for c in dot),
            "ymin": min(c["ymin"] for c in dot),
            "ymax": max(c["ymax"] for c in dot),
        }
        dot_bbox["w"] = dot_bbox["xmax"] - dot_bbox["xmin"]
        dot_bbox["h"] = dot_bbox["ymax"] - dot_bbox["ymin"]
        return [(c["pts"], c["fls"]) for c in stem], dot_bbox

    if font_name == "PocketGull-Outline.ttf" and len(contours) == 4:
        # c0, c1 are stem; c2, c3 are dot
        stem = contours[:2]
        dot = contours[2:]
        dot_bbox = {
            "xmin": min(c["xmin"] for c in dot),
            "xmax": max(c["xmax"] for c in dot),
            "ymin": min(c["ymin"] for c in dot),
            "ymax": max(c["ymax"] for c in dot),
        }
        dot_bbox["w"] = dot_bbox["xmax"] - dot_bbox["xmin"]
        dot_bbox["h"] = dot_bbox["ymax"] - dot_bbox["ymin"]
        return [(c["pts"], c["fls"]) for c in stem], dot_bbox

    if font_name == "PocketGull-Kintsugi.ttf" and canonical_name in ("i", "j"):
        # c0 outer stem + c3..c5 fracture cutouts (ymax <= 560); c1, c2 are dot (ymin >= 585)
        stem = [c for c in contours if c["ymax"] <= 560]
        dot = [c for c in contours if c["ymin"] >= 585]
        assert stem and dot and len(stem) + len(dot) == len(contours)
        dot_bbox = {
            "xmin": min(c["xmin"] for c in dot),
            "xmax": max(c["xmax"] for c in dot),
            "ymin": min(c["ymin"] for c in dot),
            "ymax": max(c["ymax"] for c in dot),
        }
        dot_bbox["w"] = dot_bbox["xmax"] - dot_bbox["xmin"]
        dot_bbox["h"] = dot_bbox["ymax"] - dot_bbox["ymin"]
        return [(c["pts"], c["fls"]) for c in stem], dot_bbox

    # Standard 2-contour fonts
    if len(contours) == 2:
        if dot_pos == "top":
            stem_c = min(contours, key=lambda c: c["ymin"])
            dot_c = max(contours, key=lambda c: c["ymax"])
        else:
            dot_c = min(contours, key=lambda c: c["ymin"])
            stem_c = max(contours, key=lambda c: c["ymax"])
        return [(stem_c["pts"], stem_c["fls"])], dict(dot_c)

    # Generic fallback partition if >2 contours
    if dot_pos == "top":
        dot_c = max(contours, key=lambda c: c["ymax"])
        stem = [c for c in contours if c["ci"] != dot_c["ci"]]
    else:
        dot_c = min(contours, key=lambda c: c["ymin"])
        stem = [c for c in contours if c["ci"] != dot_c["ci"]]
    return [(c["pts"], c["fls"]) for c in stem], dict(dot_c)


def compute_heart_box(
    font_name: str,
    canonical_name: str,
    dot_pos: str,
    stem_contours: list[tuple[list[tuple[int, int]], list[int]]],
    dot_bbox: dict,
    aw: int,
    italic_angle: float,
    f_metrics: tuple[int, int | None] | None,
) -> tuple[float, float, float, float]:
    """Returns (cx, y_min, w, h) optically calibrated to the base dot and stem clearance."""
    stem_ymin = min(p[1] for pts, _ in stem_contours for p in pts)
    stem_ymax = max(p[1] for pts, _ in stem_contours for p in pts)
    dot_cx = (dot_bbox["xmin"] + dot_bbox["xmax"]) / 2.0
    dot_h = max(80, dot_bbox["h"])
    is_mono = "Mono" in font_name or font_name in ("PocketGull-Algo.ttf", "PocketGull-Emoji.ttf", "PocketGull-Genome.ttf")

    if canonical_name in ("i", "j"):
        if font_name == "PocketGull-Outline.ttf":
            # Outline outer wall expanded +22 above Bold stem (to 568); 26 UPM outer-to-outer gap = 70 UPM centerline
            y_min = stem_ymax + 26.0
            h = 142.0
            w = 168.0
            return dot_cx, y_min, w, h

        y_min = float(stem_ymax + 48)
        h = float(max(124, min(148, int(round(max(dot_h * 1.12, 126))))))
        if font_name in ("PocketGull-Inline.ttf", "PocketGull-Kintsugi.ttf"):
            h = max(h, 138.0)
        w = float(int(round(h * 1.18)))
        if is_mono:
            w = min(w, 180.0)
        else:
            max_w_aw = float(max(138, aw - 72))
            if font_name in ("PocketGull-Inline.ttf", "PocketGull-Kintsugi.ttf"):
                max_w_aw = float(max(166, aw - 60))
            w = min(w, max_w_aw)

        # Prevent horizontal fi collision when 'i' follows 'f' (since cv09/ss07 runs before liga)
        if canonical_name == "i" and f_metrics is not None and not is_mono:
            f_aw, f_upper_xmax = f_metrics
            if f_upper_xmax is not None:
                min_fi_gap = 10.0 if abs(italic_angle) > 0.1 else 8.0
                # Heart left flank at mid-upper height ~ dot_cx - w/2 (sheared bbox widens ~4 UPM on italics)
                avail_from_f = (f_aw + dot_cx) - f_upper_xmax - min_fi_gap
                if avail_from_f > 56:
                    max_w_f = 2.0 * avail_from_f
                    if w > max_w_f:
                        if max_w_f < h * 1.08:
                            h = float(max(106, int(round(max_w_f / 1.12))))
                            w = float(int(round(h * 1.12)))
                        else:
                            w = max(max_w_f, h * 1.08)

        # Ensure harmonious aspect ratio (no pancake squash)
        if w / h > 1.32:
            w = round(h * 1.25)
        elif w / h < 1.08:
            w = round(h * 1.12)
        return dot_cx, y_min, w, h

    if canonical_name in ("exclam", "question"):
        y_min = float(dot_bbox["ymin"])
        if font_name == "PocketGull-Outline.ttf":
            max_h = float(stem_ymin - y_min - 26)
            h = float(max(140, min(max_h, 176)))
            w = float(min(max(160, aw - 12), int(round(h * 1.15))))
            return dot_cx, y_min, w, h

        max_h = float(stem_ymin - y_min - 44)
        h = float(max(116, min(max_h, int(round(dot_h * 1.08)))))
        w = float(min(max(132, aw - 20), int(round(h * 1.15))))
        if is_mono:
            w = float(int(round(h * 1.18)))
        if w / h < 1.08:
            w = float(int(round(h * 1.08)))
        return dot_cx, y_min, w, h

    # exclamdown, questiondown
    if font_name == "PocketGull-Outline.ttf":
        y_min = float(max(dot_bbox["ymin"], stem_ymax + 26))
        h = float(max(140, min(200, int(round(dot_h)))))
        w = float(min(max(160, aw - 12), int(round(h * 1.15))))
        return dot_cx, y_min, w, h

    y_min = float(max(dot_bbox["ymin"], stem_ymax + 48))
    h = float(max(116, min(190, int(round(dot_h * 1.08)))))
    w = float(min(max(132, aw - 20), int(round(h * 1.15))))
    if is_mono:
        w = float(int(round(h * 1.18)))
    if w / h < 1.08:
        w = float(int(round(h * 1.08)))
    return dot_cx, y_min, w, h


def compute_variety_box(
    font_name: str,
    canonical_name: str,
    dot_pos: str,
    stem_contours: list[tuple[list[tuple[int, int]], list[int]]],
    heart_box: tuple[float, float, float, float],
    shape_key: str,
) -> tuple[float, float, float, float]:
    """Derives optical (cx, y_min, w, h) for any tittle variety from the calibrated heart box."""
    cx, y_min, hw, hh = heart_box
    if shape_key == "heart":
        return heart_box
    if font_name == "PocketGull-Outline.ttf" and canonical_name in ("i", "j"):
        if shape_key in ("blossom", "nuqta", "star"):
            return cx, y_min, 156.0, 142.0
        if shape_key == "droplet":
            return cx, y_min, 134.0, 146.0
        return heart_box

    stem_ymin = min(p[1] for pts, _ in stem_contours for p in pts)
    gap_req = 26.0 if font_name == "PocketGull-Outline.ttf" else 44.0
    max_bot_h = (stem_ymin - y_min - gap_req) if dot_pos == "bottom" else 999.0

    if shape_key == "blossom":
        bh = float(hh)
        bw = min(float(hw), float(round(hh * 1.04)))
        return cx, y_min, bw, bh
    if shape_key == "nuqta":
        nh = float(hh)
        nw = min(float(hw), float(round(hh * 1.02)))
        return cx, y_min, nw, nh
    if shape_key == "star":
        sh = min(max_bot_h, float(round(hh * 1.06)))
        sh = max(sh, float(hh)) if dot_pos != "bottom" else max(sh, min(max_bot_h, 116.0))
        sw = min(float(hw), float(round(sh * 1.02)))
        return cx, y_min, sw, sh
    if shape_key == "droplet":
        dh = min(max_bot_h, float(round(hh * 1.04)))
        dh = max(dh, float(hh)) if dot_pos != "bottom" else max(dh, min(max_bot_h, 116.0))
        dw = min(float(hw), float(round(dh * 0.84)))
        return cx, y_min, dw, dh
    return heart_box


def assemble_glyph(contours: list[tuple[list[tuple[int, int]], list[int]]], glyf_table) -> Glyph:
    all_coords: list[tuple[int, int]] = []
    all_flags: list[int] = []
    end_pts: list[int] = []
    for pts, fls in contours:
        clean_p, clean_f = deduplicate_contour(pts, fls)
        if len(clean_p) < 3:
            continue
        all_coords.extend(clean_p)
        all_flags.extend(clean_f)
        end_pts.append(len(all_coords) - 1)

    g = Glyph()
    g.numberOfContours = len(end_pts)
    g.endPtsOfContours = end_pts
    g.coordinates = GlyphCoordinates(all_coords)
    g.flags = bytearray(all_flags)
    g.program = Program()
    g.recalcBounds(glyf_table)
    return g


def synthesize_vf_gvar_and_hvar(
    tt: TTFont,
    base_gn: str,
    target_gn: str,
    dot_pos: str,
    default_heart_pts: list[tuple[int, int]],
) -> None:
    """Synthesizes multi-axis TupleVariations in gvar & syncs HVAR for a 2-contour VF heart glyph."""
    if "gvar" not in tt or base_gn not in tt["gvar"].variations:
        return
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    vmtx = tt["vmtx"] if "vmtx" in tt else None

    bg = glyf[base_gn]
    bc, be, _ = bg.getCoordinates(glyf)
    ph = glyf._getPhantomPoints(base_gn, hmtx, vmtx)
    all_bc = list(bc) + ph
    c0_n = be[0] + 1
    c1_n = be[1] - be[0]
    stem0 = all_bc[:c0_n]
    dot0 = all_bc[c0_n : c0_n + c1_n]

    dx0_min = min(p[0] for p in dot0)
    dx0_max = max(p[0] for p in dot0)
    dy0_min = min(p[1] for p in dot0)
    dy0_max = max(p[1] for p in dot0)
    dcx0 = (dx0_min + dx0_max) / 2.0
    dcy0 = (dy0_min + dy0_max) / 2.0
    dw0 = max(1.0, float(dx0_max - dx0_min))
    dh0 = max(1.0, float(dy0_max - dy0_min))
    dot0_mid_y = dcy0

    new_tvs: list[TupleVariation] = []
    for tv in tt["gvar"].variations[base_gn]:
        dense = iup_delta(tv.coordinates, all_bc, list(be))
        stem_deltas = [(int(round(dx)), int(round(dy))) for dx, dy in dense[:c0_n]]
        dot_deltas = dense[c0_n : c0_n + c1_n]
        ph_deltas = [(int(round(dx)), int(round(dy))) for dx, dy in dense[-4:]]

        stem1 = [(p[0] + d[0], p[1] + d[1]) for p, d in zip(stem0, stem_deltas)]
        dot1 = [(p[0] + d[0], p[1] + d[1]) for p, d in zip(dot0, dot_deltas)]

        dx1_min = min(p[0] for p in dot1)
        dx1_max = max(p[0] for p in dot1)
        dy1_min = min(p[1] for p in dot1)
        dy1_max = max(p[1] for p in dot1)
        dcx1 = (dx1_min + dx1_max) / 2.0
        dcy1 = (dy1_min + dy1_max) / 2.0
        dw1 = max(1.0, float(dx1_max - dx1_min))
        dh1 = max(1.0, float(dy1_max - dy1_min))

        sx = max(0.55, min(1.90, dw1 / dw0))
        sy = max(0.55, min(1.90, dh1 / dh0))

        # Estimate horizontal slant shear delta from dot upper vs lower halves
        top_pairs = [(p, d) for p, d in zip(dot0, dot_deltas) if p[1] > dot0_mid_y + 0.1 * dh0]
        bot_pairs = [(p, d) for p, d in zip(dot0, dot_deltas) if p[1] < dot0_mid_y - 0.1 * dh0]
        d_shear = 0.0
        if top_pairs and bot_pairs:
            avg_top_y = sum(p[1] for p, _ in top_pairs) / len(top_pairs)
            avg_bot_y = sum(p[1] for p, _ in bot_pairs) / len(bot_pairs)
            avg_top_dx = sum(d[0] for _, d in top_pairs) / len(top_pairs)
            avg_bot_dx = sum(d[0] for _, d in bot_pairs) / len(bot_pairs)
            if avg_top_y - avg_bot_y > 10.0:
                d_shear = (avg_top_dx - avg_bot_dx) / (avg_top_y - avg_bot_y)

        # Transform default heart points into displaced space
        heart1 = []
        for hx, hy in default_heart_pts:
            nx = dcx1 + (hx - dcx0) * sx + (hy - dcy0) * d_shear
            ny = dcy1 + (hy - dcy0) * sy
            heart1.append((nx, ny))

        # Air-gap safety clamp at axis extremes so heart never touches stem
        stem1_ymin = min(p[1] for p in stem1)
        stem1_ymax = max(p[1] for p in stem1)
        h1_ymin = min(p[1] for p in heart1)
        h1_ymax = max(p[1] for p in heart1)

        dy_corr = 0.0
        min_gap = 42.0
        if dot_pos == "top":
            gap = h1_ymin - stem1_ymax
            if gap < min_gap:
                dy_corr = min_gap - gap
        else:
            gap = stem1_ymin - h1_ymax
            if gap < min_gap:
                dy_corr = -(min_gap - gap)

        heart_deltas = [
            (int(round(nx - hx)), int(round((ny + dy_corr) - hy)))
            for (hx, hy), (nx, ny) in zip(default_heart_pts, heart1)
        ]

        full_coords = stem_deltas + heart_deltas + ph_deltas
        new_tvs.append(TupleVariation(dict(tv.axes), full_coords))

    tt["gvar"].variations[target_gn] = new_tvs

    if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
        adv_map = tt["HVAR"].table.AdvWidthMap.mapping
        if base_gn in adv_map:
            adv_map[target_gn] = adv_map[base_gn]


def synthesize_vf_stem_only_gvar_and_hvar(
    tt: TTFont,
    base_gn: str,
    target_gn: str,
) -> None:
    """Synthesizes multi-axis TupleVariations in gvar & syncs HVAR for a 1-contour VF stem-only glyph."""
    if "gvar" not in tt or base_gn not in tt["gvar"].variations:
        return
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    vmtx = tt["vmtx"] if "vmtx" in tt else None

    bg = glyf[base_gn]
    bc, be, _ = bg.getCoordinates(glyf)
    ph = glyf._getPhantomPoints(base_gn, hmtx, vmtx)
    all_bc = list(bc) + ph
    c0_n = be[0] + 1

    new_tvs: list[TupleVariation] = []
    for tv in tt["gvar"].variations[base_gn]:
        dense = iup_delta(tv.coordinates, all_bc, list(be))
        stem_deltas = [(int(round(dx)), int(round(dy))) for dx, dy in dense[:c0_n]]
        ph_deltas = [(int(round(dx)), int(round(dy))) for dx, dy in dense[-4:]]
        new_tvs.append(TupleVariation(dict(tv.axes), stem_deltas + ph_deltas))

    tt["gvar"].variations[target_gn] = new_tvs

    if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
        adv_map = tt["HVAR"].table.AdvWidthMap.mapping
        if base_gn in adv_map:
            adv_map[target_gn] = adv_map[base_gn]


def map_codepoint_in_cmap(tt: TTFont, cp: int, gname: str) -> None:
    for sub in tt["cmap"].tables:
        if sub.format == 12:
            sub.cmap[cp] = gname
        elif cp <= 0xFFFF and sub.format == 4:
            sub.cmap[cp] = gname


def add_standalone_symbols(
    tt: TTFont,
    fname: str,
    gorder: list[str],
    cmap: dict[int, str],
) -> list[str]:
    """Synthesizes missing standalone monochrome variety symbols (✤ ◆ ✦ 💧 ●)."""
    is_mono = "Mono" in fname or fname in ("PocketGull-Algo.ttf", "PocketGull-Emoji.ttf", "PocketGull-Genome.ttf")
    sym_aw = 600 if is_mono else 700
    is_math = fname == "PocketGull-Math.ttf"
    has_gvar = "gvar" in tt
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    added: list[str] = []

    for cp, gname, shape_key, std_w, std_h, std_ymin, math_w, math_h, math_ymin in STANDALONE_SYMBOLS:
        if cp in cmap:
            continue
        norm_pts = NORM_DOT_PTS if shape_key == "dot" else VARIETY_SHAPES[shape_key]
        w, h, y_min = (math_w, math_h, math_ymin) if is_math else (std_w, std_h, std_ymin)
        cx = sym_aw / 2.0
        if fname in ("PocketGull-Outline.ttf", "PocketGull-Inline.ttf", "PocketGull-Kintsugi.ttf"):
            contours = build_specialty_shape_contours(fname, norm_pts, cx, y_min, w, h, 0.0)
        else:
            contours = [build_shape_contour(norm_pts, cx, y_min, w, h, 0.0)]

        new_g = assemble_glyph(contours, glyf)
        glyf[gname] = new_g
        hmtx[gname] = (sym_aw, new_g.xMin)
        if gname not in gorder:
            gorder.append(gname)
        map_codepoint_in_cmap(tt, cp, gname)
        cmap[cp] = gname
        added.append(gname)

        if has_gvar:
            tt["gvar"].variations[gname] = []
            if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
                ref_gn = cmap.get(0x2665)
                tt["HVAR"].table.AdvWidthMap.mapping[gname] = tt["HVAR"].table.AdvWidthMap.mapping.get(ref_gn, 0)

    return added


def synthesize_math_dotless_italic(
    tt: TTFont,
    fname: str,
    gorder: list[str],
    cmap: dict[int, str],
) -> list[str]:
    """Synthesizes U+1D6A4 (𝚤) and U+1D6A5 (𝚥) and registers them in the OpenType MATH table."""
    if fname != "PocketGull-Math.ttf" or "MATH" not in tt:
        return []
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    added: list[str] = []
    math_specs = [
        (0x1D6A4, "u1D6A4", 0x1D456, 154, 35),
        (0x1D6A5, "u1D6A5", 0x1D457, 154, 80),
    ]
    to_register: list[tuple[str, int, int]] = []
    for cp, tgt_gn, src_cp, top_accent, ital_corr in math_specs:
        src_gn = cmap.get(src_cp)
        if not src_gn or src_gn not in glyf:
            continue
        if cp not in cmap or tgt_gn not in glyf:
            src_cs = extract_contours(glyf, src_gn)
            stem_cs, _ = partition_stem_and_dot(fname, "i", "top", src_cs)
            new_g = assemble_glyph(stem_cs, glyf)
            glyf[tgt_gn] = new_g
            hmtx[tgt_gn] = (hmtx[src_gn][0], new_g.xMin)
            if tgt_gn not in gorder:
                gorder.append(tgt_gn)
            map_codepoint_in_cmap(tt, cp, tgt_gn)
            cmap[cp] = tgt_gn
        added.append(tgt_gn)
        to_register.append((tgt_gn, top_accent, ital_corr))

    return [t[0] for t in to_register]


def update_math_table_glyph_info(tt: TTFont) -> None:
    """Registers u1D6A4 & u1D6A5 in MATH TopAccentAttachment & ItalicsCorrection sorted by GlyphID."""
    if "MATH" not in tt:
        return
    m = tt["MATH"].table
    if not m.MathGlyphInfo:
        return
    gi = m.MathGlyphInfo
    gorder_idx = {gn: idx for idx, gn in enumerate(tt.getGlyphOrder())}
    targets = [
        ("u1D6A4", 154, 35),
        ("u1D6A5", 154, 80),
    ]
    present = [(gn, ta, ic) for gn, ta, ic in targets if gn in gorder_idx]
    if not present:
        return

    if gi.MathItalicsCorrectionInfo and gi.MathItalicsCorrectionInfo.Coverage:
        ic_info = gi.MathItalicsCorrectionInfo
        existing = dict(zip(ic_info.Coverage.glyphs, ic_info.ItalicsCorrection))
        for gn, _, ic_val in present:
            rec = ot.MathValueRecord()
            rec.Value = ic_val
            rec.DeviceTable = None
            existing[gn] = rec
        sorted_items = sorted(existing.items(), key=lambda kv: gorder_idx[kv[0]])
        ic_info.Coverage.glyphs = [k for k, _ in sorted_items]
        ic_info.ItalicsCorrection = [v for _, v in sorted_items]
        ic_info.ItalicsCorrectionCount = len(sorted_items)

    if gi.MathTopAccentAttachment and gi.MathTopAccentAttachment.TopAccentCoverage:
        ta_info = gi.MathTopAccentAttachment
        existing = dict(zip(ta_info.TopAccentCoverage.glyphs, ta_info.TopAccentAttachment))
        for gn, ta_val, _ in present:
            rec = ot.MathValueRecord()
            rec.Value = ta_val
            rec.DeviceTable = None
            existing[gn] = rec
        sorted_items = sorted(existing.items(), key=lambda kv: gorder_idx[kv[0]])
        ta_info.TopAccentCoverage.glyphs = [k for k, _ in sorted_items]
        ta_info.TopAccentAttachment = [v for _, v in sorted_items]
        ta_info.TopAccentAttachmentCount = len(sorted_items)


def find_existing_letter_targets(tt: TTFont, i_gn: str, j_gn: str) -> tuple[str | None, str | None, int | None, int | None]:
    """Finds existing ss07 / cv09 lookup indices and preferred letter target glyph names."""
    if "GSUB" not in tt or not tt["GSUB"].table.FeatureList:
        return None, None, None, None
    gsub = tt["GSUB"].table
    ss07_idx = None
    cv09_idx = None
    i_target = None
    j_target = None

    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag == "ss07":
            for lidx in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[lidx]
                for st in lk.SubTable:
                    mp = getattr(st, "mapping", None)
                    if mp and i_gn in mp and j_gn in mp:
                        if ss07_idx is None:
                            ss07_idx = lidx
                            i_target = mp[i_gn]
                            j_target = mp[j_gn]
        elif fr.FeatureTag == "cv09":
            for lidx in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[lidx]
                for st in lk.SubTable:
                    mp = getattr(st, "mapping", None)
                    if mp and i_gn in mp and j_gn in mp:
                        if cv09_idx is None:
                            cv09_idx = lidx

    return i_target, j_target, ss07_idx, cv09_idx


def ensure_win_name(nm, nid: int, val: str) -> None:
    nm.setName(val, nid, 3, 1, 0x0409)
    nm.names = [
        r for r in nm.names
        if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
    ]


def remap_gsub_lookup_indices(gsub, old_to_new: dict[int, int]) -> None:
    """Remaps LookupList indices across FeatureRecords and contextual LookupType 5/6/7 subtables."""
    for fr in gsub.FeatureList.FeatureRecord:
        fr.Feature.LookupListIndex = [old_to_new.get(li, li) for li in fr.Feature.LookupListIndex]
        fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)

    def remap_slr_list(slrs) -> None:
        if not slrs:
            return
        for slr in slrs:
            slr.LookupListIndex = old_to_new.get(slr.LookupListIndex, slr.LookupListIndex)

    def remap_subtable(st, ltype: int) -> None:
        if ltype == 7:
            ext = getattr(st, "ExtSubTable", None)
            if ext is not None:
                remap_subtable(ext, st.ExtensionLookupType)
            return
        if ltype not in (5, 6):
            return
        remap_slr_list(getattr(st, "SubstLookupRecord", None))
        for rs in getattr(st, "SubRuleSet", None) or []:
            if rs is not None:
                for rule in getattr(rs, "SubRule", None) or []:
                    remap_slr_list(getattr(rule, "SubstLookupRecord", None))
        for cs in getattr(st, "SubClassSet", None) or []:
            if cs is not None:
                for rule in getattr(cs, "SubClassRule", None) or []:
                    remap_slr_list(getattr(rule, "SubstLookupRecord", None))
        for crs in getattr(st, "ChainSubRuleSet", None) or []:
            if crs is not None:
                for rule in getattr(crs, "ChainSubRule", None) or []:
                    remap_slr_list(getattr(rule, "SubstLookupRecord", None))
        for ccs in getattr(st, "ChainSubClassSet", None) or []:
            if ccs is not None:
                for rule in getattr(ccs, "ChainSubClassRule", None) or []:
                    remap_slr_list(getattr(rule, "SubstLookupRecord", None))

    for lk in gsub.LookupList.Lookup:
        for st in lk.SubTable:
            remap_subtable(st, lk.LookupType)


def configure_gsub_and_gdef(
    tt: TTFont,
    heart_letter_map: dict[str, str],
    heart_punct_map: dict[str, str],
    dotless_map: dict[str, str],
    variety_maps: dict[str, dict[str, str]],
    extra_gdef_glyphs: list[str],
    ss07_lidx: int | None,
    cv09_lidx: int | None,
) -> None:
    """Wires cv09, cv10, cv19, ss07..ss11 strictly before liga, sorts FeatureList, sets FeatureParams & GDEF."""
    gsub = tt["GSUB"].table
    nm = tt["name"]
    target_tags = ("cv09", "cv10", "cv19", "ss07", "ss08", "ss09", "ss10", "ss11")

    def get_min_liga() -> int:
        liga_indices = []
        for fr in gsub.FeatureList.FeatureRecord:
            if fr.FeatureTag == "liga":
                liga_indices.extend(fr.Feature.LookupListIndex)
        return min(liga_indices) if liga_indices else len(gsub.LookupList.Lookup)

    def make_single_subst_lookup(mapping: dict[str, str]) -> ot.Lookup:
        st = ot.SingleSubst()
        st.Format = 1
        st.mapping = dict(mapping)
        lk = ot.Lookup()
        lk.LookupType = 1
        lk.LookupFlag = 0
        lk.SubTable = [st]
        lk.SubTableCount = 1
        return lk

    def find_tag_single_slot(tag: str) -> int | None:
        for fr in gsub.FeatureList.FeatureRecord:
            if fr.FeatureTag == tag:
                for li in fr.Feature.LookupListIndex:
                    if 0 <= li < len(gsub.LookupList.Lookup) and gsub.LookupList.Lookup[li].LookupType == 1:
                        return li
        return None

    cv10_existing = find_tag_single_slot("cv10")
    cv19_existing = find_tag_single_slot("cv19")
    ss08_existing = find_tag_single_slot("ss08")
    ss09_existing = find_tag_single_slot("ss09")
    ss10_existing = find_tag_single_slot("ss10")
    ss11_existing = find_tag_single_slot("ss11")

    used_slots: set[int] = set()
    allocated_refs: list[list[int]] = []

    def alloc_lookup_before_liga(mapping: dict[str, str], preferred: list[int | None]) -> int:
        cur_min_liga = get_min_liga()
        for cand in preferred:
            if cand is None or cand >= cur_min_liga or cand in used_slots:
                continue
            owners = [
                fr.FeatureTag for fr in gsub.FeatureList.FeatureRecord
                if cand in fr.Feature.LookupListIndex and fr.FeatureTag not in target_tags
            ]
            if not owners:
                gsub.LookupList.Lookup[cand] = make_single_subst_lookup(mapping)
                used_slots.add(cand)
                ref = [cand]
                allocated_refs.append(ref)
                return ref[0]

        insert_at = cur_min_liga
        old_len = len(gsub.LookupList.Lookup)
        gsub.LookupList.Lookup.insert(insert_at, make_single_subst_lookup(mapping))
        gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
        old_to_new = {old: (old + 1 if old >= insert_at else old) for old in range(old_len)}
        remap_gsub_lookup_indices(gsub, old_to_new)
        used_slots_shifted = {old_to_new.get(s, s) for s in used_slots}
        used_slots.clear()
        used_slots.update(used_slots_shifted)
        for ref in allocated_refs:
            ref[0] = old_to_new.get(ref[0], ref[0])
        used_slots.add(insert_at)
        new_ref = [insert_at]
        allocated_refs.append(new_ref)
        return new_ref[0]

    heart_letters_ref = [alloc_lookup_before_liga(heart_letter_map, [ss07_lidx, cv09_lidx])]
    # Track dynamic ref via allocated_refs[-1] pattern? Since all inserts happen strictly at cur_min_liga
    # and reused slots are always < cur_min_liga, no previously returned index EVER shifts upward.
    heart_letters_idx = heart_letters_ref[0]
    heart_punct_idx = alloc_lookup_before_liga(heart_punct_map, [cv10_existing, cv09_lidx])
    dotless_idx = alloc_lookup_before_liga(dotless_map, [cv19_existing])
    blossom_idx = alloc_lookup_before_liga(variety_maps["blossom"], [ss08_existing])
    nuqta_idx = alloc_lookup_before_liga(variety_maps["nuqta"], [ss09_existing])
    star_idx = alloc_lookup_before_liga(variety_maps["star"], [ss10_existing])
    droplet_idx = alloc_lookup_before_liga(variety_maps["droplet"], [ss11_existing])

    # Assign unique nameIDs for FeatureParams UI labels
    used_nids = {r.nameID for r in nm.names if r.nameID >= 256}

    def alloc_or_reuse_label(label_str: str, existing_fr: ot.FeatureRecord | None) -> int:
        if existing_fr is not None and existing_fr.Feature.FeatureParams is not None:
            fp = existing_fr.Feature.FeatureParams
            nid = getattr(fp, "FeatUILabelNameID", None) or getattr(fp, "UINameID", None)
            if nid and nid >= 256:
                ensure_win_name(nm, nid, label_str)
                return nid
        for r in nm.names:
            if r.nameID >= 256 and r.toUnicode() == label_str:
                return r.nameID
        nid = 720
        while nid in used_nids:
            nid += 1
        used_nids.add(nid)
        ensure_win_name(nm, nid, label_str)
        return nid

    def make_cv_params(nid: int, chars: list[int]) -> ot.FeatureParamsCharacterVariants:
        fp = ot.FeatureParamsCharacterVariants()
        fp.Format = 0
        fp.FeatUILabelNameID = nid
        fp.FeatUITooltipTextNameID = 0
        fp.SampleTextNameID = 0
        fp.NumNamedParameters = 0
        fp.FirstParamUILabelNameID = 0
        fp.CharCount = len(chars)
        fp.Character = list(chars)
        return fp

    def make_ss_params(nid: int) -> ot.FeatureParamsStylisticSet:
        fp = ot.FeatureParamsStylisticSet()
        fp.Version = 0
        fp.UINameID = nid
        return fp

    # Preserve single FeatureRecord per target tag or create cleanly
    existing_by_tag = {}
    kept_records = []
    for idx, fr in enumerate(gsub.FeatureList.FeatureRecord):
        if fr.FeatureTag in target_tags:
            if fr.FeatureTag not in existing_by_tag:
                existing_by_tag[fr.FeatureTag] = fr
                kept_records.append((idx, fr))
        else:
            kept_records.append((idx, fr))

    old_to_new_feat = {}
    new_records = []
    for new_i, (old_i, fr) in enumerate(kept_records):
        old_to_new_feat[old_i] = new_i
        new_records.append(fr)

    def remap_indices(indices: list[int]) -> list[int]:
        return sorted(set(old_to_new_feat[i] for i in indices if i in old_to_new_feat))

    if gsub.ScriptList is not None:
        for sr in gsub.ScriptList.ScriptRecord:
            if sr.Script.DefaultLangSys is not None:
                sr.Script.DefaultLangSys.FeatureIndex = remap_indices(sr.Script.DefaultLangSys.FeatureIndex)
                sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
            for ls in getattr(sr.Script, "LangSysRecord", []) or []:
                ls.LangSys.FeatureIndex = remap_indices(ls.LangSys.FeatureIndex)
                ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

    gsub.FeatureList.FeatureRecord = new_records
    gsub.FeatureList.FeatureCount = len(new_records)

    def upsert_feature(tag: str, lookup_indices: list[int], params) -> int:
        for idx, fr in enumerate(gsub.FeatureList.FeatureRecord):
            if fr.FeatureTag == tag:
                fr.Feature.LookupListIndex = list(lookup_indices)
                fr.Feature.LookupCount = len(lookup_indices)
                fr.Feature.FeatureParams = params
                return idx
        fr = ot.FeatureRecord()
        fr.FeatureTag = tag
        fr.Feature = ot.Feature()
        fr.Feature.LookupListIndex = list(lookup_indices)
        fr.Feature.LookupCount = len(lookup_indices)
        fr.Feature.FeatureParams = params
        gsub.FeatureList.FeatureRecord.append(fr)
        gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)
        return len(gsub.FeatureList.FeatureRecord) - 1

    cv09_nid = alloc_or_reuse_label(CV09_LABEL, existing_by_tag.get("cv09"))
    cv10_nid = alloc_or_reuse_label(CV10_LABEL, existing_by_tag.get("cv10"))
    cv19_nid = alloc_or_reuse_label(CV19_LABEL, existing_by_tag.get("cv19"))
    ss07_nid = alloc_or_reuse_label(SS07_LABEL, existing_by_tag.get("ss07"))
    ss08_nid = alloc_or_reuse_label(SS08_LABEL, existing_by_tag.get("ss08"))
    ss09_nid = alloc_or_reuse_label(SS09_LABEL, existing_by_tag.get("ss09"))
    ss10_nid = alloc_or_reuse_label(SS10_LABEL, existing_by_tag.get("ss10"))
    ss11_nid = alloc_or_reuse_label(SS11_LABEL, existing_by_tag.get("ss11"))

    f_cv09 = upsert_feature("cv09", [heart_letters_idx], make_cv_params(cv09_nid, [0x0069, 0x006A]))
    f_cv10 = upsert_feature("cv10", [heart_punct_idx], make_cv_params(cv10_nid, [0x0021, 0x003F, 0x00A1, 0x00BF]))
    f_cv19 = upsert_feature(
        "cv19",
        [dotless_idx],
        make_cv_params(cv19_nid, [0x0021, 0x003F, 0x0069, 0x006A, 0x00A1, 0x00BF, 0x0131, 0x0237]),
    )
    f_ss07 = upsert_feature("ss07", [heart_letters_idx, heart_punct_idx], make_ss_params(ss07_nid))
    f_ss08 = upsert_feature("ss08", [blossom_idx], make_ss_params(ss08_nid))
    f_ss09 = upsert_feature("ss09", [nuqta_idx], make_ss_params(ss09_nid))
    f_ss10 = upsert_feature("ss10", [star_idx], make_ss_params(ss10_nid))
    f_ss11 = upsert_feature("ss11", [droplet_idx], make_ss_params(ss11_nid))

    all_f_indices = (f_cv09, f_cv10, f_cv19, f_ss07, f_ss08, f_ss09, f_ss10, f_ss11)
    if gsub.ScriptList is not None:
        for sr in gsub.ScriptList.ScriptRecord:
            if sr.Script.DefaultLangSys is None:
                sr.Script.DefaultLangSys = ot.DefaultLangSys()
                sr.Script.DefaultLangSys.FeatureIndex = []
                sr.Script.DefaultLangSys.LookupOrder = None
                sr.Script.DefaultLangSys.ReqFeatureIndex = 0xFFFF
            for fi in all_f_indices:
                if fi not in sr.Script.DefaultLangSys.FeatureIndex:
                    sr.Script.DefaultLangSys.FeatureIndex.append(fi)
            sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
            for ls in getattr(sr.Script, "LangSysRecord", []) or []:
                for fi in all_f_indices:
                    if fi not in ls.LangSys.FeatureIndex:
                        ls.LangSys.FeatureIndex.append(fi)
                ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

    # Sort FeatureList alphabetically by FeatureTag (OpenType / HarfBuzz binary-search invariant)
    indexed = list(enumerate(gsub.FeatureList.FeatureRecord))
    indexed.sort(key=lambda item: item[1].FeatureTag)
    old_to_sorted = {old_idx: new_idx for new_idx, (old_idx, _) in enumerate(indexed)}
    gsub.FeatureList.FeatureRecord = [item[1] for item in indexed]
    gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)

    if gsub.ScriptList is not None:
        for sr in gsub.ScriptList.ScriptRecord:
            if sr.Script.DefaultLangSys is not None:
                sr.Script.DefaultLangSys.FeatureIndex = sorted(
                    set(old_to_sorted[i] for i in sr.Script.DefaultLangSys.FeatureIndex if i in old_to_sorted)
                )
                sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
            for ls in getattr(sr.Script, "LangSysRecord", []) or []:
                ls.LangSys.FeatureIndex = sorted(
                    set(old_to_sorted[i] for i in ls.LangSys.FeatureIndex if i in old_to_sorted)
                )
                ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

    # Register all synthesized glyphs as Base glyphs (class 1) in GDEF
    if "GDEF" not in tt:
        gdef_tbl = newTable("GDEF")
        gdef_tbl.table = ot.GDEF()
        gdef_tbl.table.Version = 0x00010000
        gdef_tbl.table.GlyphClassDef = ot.GlyphClassDef()
        gdef_tbl.table.GlyphClassDef.classDefs = {}
        gdef_tbl.table.AttachList = None
        gdef_tbl.table.LigCaretList = None
        gdef_tbl.table.MarkAttachClassDef = None
        tt["GDEF"] = gdef_tbl
    if tt["GDEF"].table.GlyphClassDef is None:
        tt["GDEF"].table.GlyphClassDef = ot.GlyphClassDef()
        tt["GDEF"].table.GlyphClassDef.classDefs = {}

    all_gdef = (
        list(heart_letter_map.values())
        + list(heart_punct_map.values())
        + list(dotless_map.values())
        + [gn for vm in variety_maps.values() for gn in vm.values()]
        + list(extra_gdef_glyphs)
    )
    for tgt in all_gdef:
        tt["GDEF"].table.GlyphClassDef.classDefs[tgt] = 1


def cure_font(ttf_path: Path) -> None:
    fname = ttf_path.name
    tt = TTFont(str(ttf_path))
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    cmap = tt.getBestCmap() or {}
    gorder = list(tt.getGlyphOrder())
    italic_angle = float(tt["post"].italicAngle) if "post" in tt else 0.0
    has_gvar = "gvar" in tt
    if has_gvar:
        _ = tt["gvar"].variations

    i_gn = cmap[0x0069]
    j_gn = cmap[0x006A]
    existing_i_tgt, existing_j_tgt, ss07_lidx, cv09_lidx = find_existing_letter_targets(tt, i_gn, j_gn)

    # Resolve f upper xMax for horizontal fi clearance checks
    f_metrics = None
    f_gn = cmap.get(0x0066)
    if f_gn and f_gn in glyf:
        f_aw = hmtx[f_gn][0]
        fc = extract_contours(glyf, f_gn)
        f_pts_hi = [p[0] for c in fc for p in c["pts"] if 540 <= p[1] <= 740]
        f_metrics = (f_aw, max(f_pts_hi) if f_pts_hi else glyf[f_gn].xMax)

    heart_letter_map: dict[str, str] = {}
    heart_punct_map: dict[str, str] = {}
    dotless_map: dict[str, str] = {}
    variety_maps: dict[str, dict[str, str]] = {
        vk: {} for vk in VARIETY_ORDER if vk != "heart"
    }

    for cp, canon, dot_pos, kind in BASE_SPECS:
        base_gn = cmap[cp]
        contours = extract_contours(glyf, base_gn)
        assert contours, f"{fname}: base glyph '{base_gn}' has no contours"
        aw, _ = hmtx[base_gn]

        stem_contours, dot_bbox = partition_stem_and_dot(fname, canon, dot_pos, contours)
        heart_box = compute_heart_box(fname, canon, dot_pos, stem_contours, dot_bbox, aw, italic_angle, f_metrics)

        # Synthesize bit-identical stem-only glyph (cv19) for all 6 base glyphs
        dl_gn = f"{canon}.dotless"
        if dl_gn not in gorder:
            gorder.append(dl_gn)
        dl_g = assemble_glyph(stem_contours, glyf)
        glyf[dl_gn] = dl_g
        hmtx[dl_gn] = (aw, dl_g.xMin)
        if has_gvar:
            synthesize_vf_stem_only_gvar_and_hvar(tt, base_gn, dl_gn)
        dotless_map[base_gn] = dl_gn
        if canon == "i" and 0x0131 in cmap:
            dotless_map[cmap[0x0131]] = dl_gn
        elif canon == "j" and 0x0237 in cmap:
            dotless_map[cmap[0x0237]] = dl_gn

        for variety_key in VARIETY_ORDER:
            if variety_key == "heart":
                if canon == "i":
                    target_gn = existing_i_tgt if (existing_i_tgt and existing_i_tgt in glyf) else "i.heart"
                elif canon == "j":
                    target_gn = existing_j_tgt if (existing_j_tgt and existing_j_tgt in glyf) else "j.heart"
                else:
                    target_gn = f"{canon}.heart"
            else:
                target_gn = f"{canon}.{variety_key}"

            if target_gn not in gorder:
                gorder.append(target_gn)

            cx, y_min, w, h = compute_variety_box(fname, canon, dot_pos, stem_contours, heart_box, variety_key)
            norm_pts = VARIETY_SHAPES[variety_key]

            if fname in ("PocketGull-Outline.ttf", "PocketGull-Inline.ttf") or (
                fname == "PocketGull-Kintsugi.ttf" and canon in ("i", "j")
            ):
                shape_contours = build_specialty_shape_contours(fname, norm_pts, cx, y_min, w, h, italic_angle)
            else:
                shape_contours = [build_shape_contour(norm_pts, cx, y_min, w, h, italic_angle)]

            all_contours = stem_contours + shape_contours
            new_g = assemble_glyph(all_contours, glyf)
            glyf[target_gn] = new_g
            hmtx[target_gn] = (aw, new_g.xMin)

            if has_gvar:
                assert len(shape_contours) == 1, f"VF {fname} expected 1 shape contour for {target_gn}"
                synthesize_vf_gvar_and_hvar(tt, base_gn, target_gn, dot_pos, shape_contours[0][0])

            if variety_key == "heart":
                if kind == "letter":
                    heart_letter_map[base_gn] = target_gn
                else:
                    heart_punct_map[base_gn] = target_gn
            else:
                variety_maps[variety_key][base_gn] = target_gn

    extra_gdef = add_standalone_symbols(tt, fname, gorder, cmap)
    math_added = synthesize_math_dotless_italic(tt, fname, gorder, cmap)
    extra_gdef.extend(math_added)

    tt.setGlyphOrder(gorder)
    update_math_table_glyph_info(tt)
    configure_gsub_and_gdef(
        tt,
        heart_letter_map,
        heart_punct_map,
        dotless_map,
        variety_maps,
        extra_gdef,
        ss07_lidx,
        cv09_lidx,
    )

    # Enforce Bit-7 flag clearing across all simple glyphs
    for gname in gorder:
        g = glyf[gname]
        if g.numberOfContours > 0:
            g.flags = bytearray(fl & 0x3F for fl in g.flags)

    # Recalc OS/2 xAvgCharWidth cleanly and save atomically (avoids Windows open-handle Errno 22)
    tt["OS/2"].recalcAvgCharWidth(tt)
    tmp_path = ttf_path.with_name(f"{ttf_path.stem}.__tmp.ttf")
    tt.save(str(tmp_path))
    tt.close()
    tmp_path.replace(ttf_path)


def distribute_and_sync(realign: bool = True, only_stems: set[str] | None = None) -> None:
    """Realigns TTF word boundaries, compresses WOFF2s, rebuilds Core subsets, and syncs mirrors."""
    woff2_dir = ROOT_DIR / "fonts" / "woff2"
    woff2_dir.mkdir(parents=True, exist_ok=True)
    targets = [
        p for p in sorted(TTF_DIR.glob("*.ttf"))
        if p.name not in SKIP_FONTS and (only_stems is None or p.stem in only_stems)
    ]

    if realign:
        print("\n• Enforcing 2-byte word alignment via Dart foundry CLI...", flush=True)
        subprocess.run(["dart", "run", "tool/pocketgull_foundry.dart", "realign"], cwd=str(ROOT_DIR), check=True)

    print(f"\n• Compressing {len(targets)} WOFF2 webfonts...", flush=True)
    for ttf_path in targets:
        w2_path = woff2_dir / f"{ttf_path.stem}.woff2"
        compress(str(ttf_path), str(w2_path))
        print(f"  [OK] {w2_path.name} ({w2_path.stat().st_size:,} bytes)", flush=True)

    core_map = {
        "PocketGull-Bold-Core.woff2": "PocketGull-Bold.ttf",
        "PocketGull-Fineliner-Core.woff2": "PocketGull-Fineliner.ttf",
        "PocketGull-Micro-Core.woff2": "PocketGull-Micro.ttf",
        "PocketGull-Regular-Core.woff2": "PocketGull-Regular.ttf",
    }
    if only_stems is not None:
        core_map = {k: v for k, v in core_map.items() if Path(v).stem in only_stems}
    if core_map:
        print(f"\n• Rebuilding {len(core_map)} Core WOFF2 subsets...", flush=True)
    required_cps = {
        0x0021, 0x003F, 0x0069, 0x006A, 0x00A1, 0x00BF,
        0x0131, 0x0237, 0x2665, 0x2724, 0x25C6, 0x2726, 0x25CF, 0x1F4A7,
    }
    for core_w2_name, src_ttf_name in core_map.items():
        w2_path = woff2_dir / core_w2_name
        if not w2_path.is_file():
            continue
        old_tt = TTFont(str(w2_path))
        unicodes = set(old_tt.getBestCmap().keys()) | required_cps
        old_tt.close()

        src_tt = TTFont(str(TTF_DIR / src_ttf_name))
        opts = Options()
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.name_legacy = False
        opts.name_languages = [0x0409]
        opts.notdef_outline = True
        opts.recalc_bounds = True
        opts.recalc_average_width = True
        subsetter = Subsetter(options=opts)
        subsetter.populate(unicodes=unicodes)
        subsetter.subset(src_tt)
        src_tt.flavor = "woff2"
        src_tt.save(str(w2_path))
        src_tt.close()
        print(f"  [OK] Subset {core_w2_name} ({w2_path.stat().st_size:,} bytes)", flush=True)

    print("\n• Synchronizing root, ofl/, apache/, and distribution/ mirrors...", flush=True)
    synced = 0
    for ext, src_dir in ((".ttf", TTF_DIR), (".woff2", woff2_dir)):
        for dst in sorted(ROOT_DIR.glob(f"PocketGull*{ext}")):
            if dst.name in SKIP_FONTS or (dst.stem + ".ttf") in SKIP_FONTS:
                continue
            if only_stems is not None and dst.stem not in only_stems:
                continue
            src = src_dir / dst.name
            if src.exists():
                shutil.copyfile(src, dst)
                synced += 1

    mirror_dirs = [
        ROOT_DIR / "ofl",
        ROOT_DIR / "apache",
        ROOT_DIR / "distribution" / "python" / "pocketgull_math" / "fonts",
        ROOT_DIR / "distribution" / "r" / "inst" / "fonts",
        ROOT_DIR / "distribution" / "upcycled",
    ]
    for sub_dir in mirror_dirs:
        if not sub_dir.exists():
            continue
        for ext, src_dir in ((".ttf", TTF_DIR), (".woff2", woff2_dir)):
            for dst in sorted(sub_dir.rglob(f"*{ext}")):
                if dst.name in SKIP_FONTS or (dst.stem + ".ttf") in SKIP_FONTS:
                    continue
                if only_stems is not None and dst.stem not in only_stems:
                    continue
                src = src_dir / dst.name
                if src.exists():
                    shutil.copyfile(src, dst)
                    synced += 1
    print(f"  [OK] Synchronized {synced} mirror binaries.")


def main() -> None:
    only_stems: set[str] | None = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        only_vals = []
        for tok in sys.argv[idx + 1:]:
            if tok.startswith("--"):
                break
            only_vals.append(Path(tok).stem)
        if only_vals:
            only_stems = set(only_vals)

    if "--distribute-only" in sys.argv:
        distribute_and_sync(realign="--no-realign" not in sys.argv, only_stems=only_stems)
        return

    targets = [
        p for p in sorted(TTF_DIR.glob("*.ttf"))
        if p.name not in SKIP_FONTS and (only_stems is None or p.stem in only_stems)
    ]
    print("=" * 78)
    print(f"  POCKETGULL PHILOCARDIA VARIETIES, PUNCTUATION & MATH CURE ({len(targets)} CUTS)")
    print("=" * 78)
    for idx, ttf_path in enumerate(targets, 1):
        cure_font(ttf_path)
        print(f"  [{idx:2d}/{len(targets)}] Cured {ttf_path.name}", flush=True)
    print(f"\n[OK] {len(targets)} superfamily TTF binaries cured (cv09, cv10, cv19, ss07..ss11 + symbols + VF).")
    if "--with-distribute" in sys.argv:
        distribute_and_sync(realign=True, only_stems=only_stems)


if __name__ == "__main__":
    main()
