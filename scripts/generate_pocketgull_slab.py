#!/usr/bin/env python3
"""
PocketGull Typefoundry: PocketGull Slab Generator v3.1
=====================================================
Engineers the fourth pillar of the superfamily: PocketGull Slab
(PocketGull-Slab-Regular and PocketGull-Slab-Bold) for high-impact
clinical reading, display titling, and telemetry legibility.

Features:
- Sturdy bracketed humanist slab serifs with optimal quadratic Bézier fillets (flag=0 off-curve brackets)
- ISMP character safeguards:
    * Capital 'I': Bilateral serifs top and bottom (ss02)
    * Lowercase 'l': Top entry spur + curved outward foot sweep (cv05)
    * Numeral '1': Angled beak flag + broad flat baseline slab
    * Slashed zero '0' (cv08)
    * Calibrated heart tittle grounding (cv09 / .philocardia-heart)
- Complete uppercase coverage: H, M, N, K, B, D, P, R, T, U, A, E, F, L, V, W, X, Y, Z
- Complete lowercase coverage: b, d, h, i, k, l, m, n, p, q, r, u, a, t, v, w, x, y, z
- Numerals: 1, 4, 7
- Corrected topological serifier:
    * D, B, b: Unilateral leftward stem serifs; 0 spurs cutting into or through bowls
    * d: Top entry spur at ascender; rightward baseline foot; clean round bowl
    * P, R: Top-left entry spur; bilateral baseline foot; clean bowls
    * q: Top entry spur at x-height; bilateral descender foot at -240 UPM; clean bowl
- 1000 UPM standard em-square, 2-byte word alignment (loca[i] % 2 == 0), bit-7 flag clearing
- Google Fonts Option 5 naming compliance (Version 3.100, fontRevision 3.1)
"""

import os
import sys
import copy
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.ttLib.woff2 import compress
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

try:
    import pathops
    HAS_PATHOPS = True
except ImportError:
    HAS_PATHOPS = False

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

def clean_glyph_geometry(glyph):
    if glyph.numberOfContours <= 0:
        return
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    endPts = list(glyph.endPtsOfContours)
    new_coords, new_flags, new_endPts = [], [], []
    start = 0
    for end in endPts:
        pts = coords[start:end+1]
        flgs = flags[start:end+1]
        filtered_pts, filtered_flgs = [], []
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
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray(new_flags)
    glyph.endPtsOfContours = new_endPts

def make_slab_nodes(xl, xr, y, O, H_slab, H_rise, mode, pos, going_rtl, O_left=None, O_right=None):
    """
    Constructs bracketed humanist slab serif nodes using optimal quadratic Bézier curves.
    At bracket transitions, an off-curve control point (flag=0) provides C1 tangency
    connecting the vertical stem to the horizontal serif shelf with 25 UPM felt-marker curvature.
    Supports asymmetric lateral overhangs (O_left, O_right) to prevent inner counter crowding.
    """
    ol = O_left if O_left is not None else O
    or_ = O_right if O_right is not None else O
    H_tot = H_slab + H_rise
    nodes = [] # tuples: ((x, y), flag)
    
    if H_rise == 0:
        if pos == 'base':
            if mode == 'bilateral':
                nodes = [
                    ((xl, y + H_slab), 1),
                    ((xl - ol, y + H_slab), 1),
                    ((xl - ol, y), 1),
                    ((xr + or_, y), 1),
                    ((xr + or_, y + H_slab), 1),
                    ((xr, y + H_slab), 1)
                ]
            elif mode == 'left_only':
                nodes = [
                    ((xl, y + H_slab), 1),
                    ((xl - ol, y + H_slab), 1),
                    ((xl - ol, y), 1),
                    ((xr, y), 1)
                ]
            elif mode == 'right_only':
                nodes = [
                    ((xl, y), 1),
                    ((xr + or_, y), 1),
                    ((xr + or_, y + H_slab), 1),
                    ((xr, y + H_slab), 1)
                ]
        elif pos == 'top':
            if mode == 'bilateral':
                nodes = [
                    ((xl, y - H_slab), 1),
                    ((xl - ol, y - H_slab), 1),
                    ((xl - ol, y), 1),
                    ((xr + or_, y), 1),
                    ((xr + or_, y - H_slab), 1),
                    ((xr, y - H_slab), 1)
                ]
            elif mode == 'left_only':
                nodes = [
                    ((xl, y - H_slab), 1),
                    ((xl - ol, y - H_slab), 1),
                    ((xl - ol, y), 1),
                    ((xr, y), 1)
                ]
            elif mode == 'right_only':
                nodes = [
                    ((xl, y), 1),
                    ((xr + or_, y), 1),
                    ((xr + or_, y - H_slab), 1),
                    ((xr, y - H_slab), 1)
                ]
        elif pos == 'descender':
            nodes = [
                ((xl, y + H_slab), 1),
                ((xl - ol, y + H_slab), 1),
                ((xl - ol, y), 1),
                ((xr + or_, y), 1),
                ((xr + or_, y + H_slab), 1),
                ((xr, y + H_slab), 1)
            ]
    elif pos == 'base':
        if mode == 'bilateral':
            nodes = [
                ((xl, y + H_tot), 1),
                ((xl, y + H_slab), 0), # quadratic bracket control point
                ((xl - ol, y + H_slab), 1),
                ((xl - ol, y), 1),
                ((xr + or_, y), 1),
                ((xr + or_, y + H_slab), 1),
                ((xr, y + H_slab), 0), # quadratic bracket control point
                ((xr, y + H_tot), 1)
            ]
        elif mode == 'left_only':
            nodes = [
                ((xl, y + H_tot), 1),
                ((xl, y + H_slab), 0),
                ((xl - ol, y + H_slab), 1),
                ((xl - ol, y), 1),
                ((xr, y), 1)
            ]
        elif mode == 'right_only':
            nodes = [
                ((xl, y), 1),
                ((xr + or_, y), 1),
                ((xr + or_, y + H_slab), 1),
                ((xr, y + H_slab), 0),
                ((xr, y + H_tot), 1)
            ]
    elif pos == 'top':
        if mode == 'bilateral':
            nodes = [
                ((xl, y - H_tot), 1),
                ((xl, y - H_slab), 0), # quadratic bracket control point
                ((xl - ol, y - H_slab), 1),
                ((xl - ol, y), 1),
                ((xr + or_, y), 1),
                ((xr + or_, y - H_slab), 1),
                ((xr, y - H_slab), 0), # quadratic bracket control point
                ((xr, y - H_tot), 1)
            ]
        elif mode == 'left_only':
            nodes = [
                ((xl, y - H_tot), 1),
                ((xl, y - H_slab), 0),
                ((xl - ol, y - H_slab), 1),
                ((xl - ol, y), 1),
                ((xr, y), 1)
            ]
        elif mode == 'right_only':
            nodes = [
                ((xl, y), 1),
                ((xr + or_, y), 1),
                ((xr + or_, y - H_slab), 1),
                ((xr, y - H_slab), 0),
                ((xr, y - H_tot), 1)
            ]
    elif pos == 'descender':
        nodes = [
            ((xl, y + H_tot), 1),
            ((xl, y + H_slab), 0),
            ((xl - ol, y + H_slab), 1),
            ((xl - ol, y), 1),
            ((xr + or_, y), 1),
            ((xr + or_, y + H_slab), 1),
            ((xr, y + H_slab), 0),
            ((xr, y + H_tot), 1)
        ]

    if going_rtl:
        nodes.reverse()
    return nodes

def serify_stem(pts, flags, gname, O=52, H_slab=48, H_rise=18):
    n = len(pts)
    new_pts = []
    new_flgs = []
    i = 0
    H_tot = H_slab + H_rise

    while i < n:
        p0 = pts[i]
        p1 = pts[(i+1)%n]
        dx = abs(p0[0] - p1[0])
        dy = abs(p0[1] - p1[1])
        y_avg = (p0[1] + p1[1]) / 2.0
        xl = min(p0[0], p1[0])
        xr = max(p0[0], p1[0])
        going_rtl = p0[0] > p1[0]

        # Caps D, B: Left stem only (protecting right rounded bowls)
        if gname in ['D', 'B']:
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            elif abs(p1[1] - 0) <= 6 and p0[0] > p1[0] and abs(p0[1] - 0) <= 6 and p1[0] < 200:
                foot = [
                    (p1[0], 0),
                    (p1[0] - O, 0),
                    (p1[0] - O, H_slab),
                    (p1[0], H_tot)
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in foot:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue

        # Caps P, R: Top-left entry spur, bilateral baseline foot
        elif gname in ['P', 'R']:
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 220 and dx >= 60:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase b:
        elif gname == 'b':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_slab_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 200 and dx >= 50:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'left_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase d:
        elif gname == 'd':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_slab_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl >= 400 and dx >= 50:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase q:
        elif gname == 'q':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl >= 400 and dx >= 50:
                nodes = make_slab_nodes(xl, xr, 536, O, H_slab, H_rise, 'right_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - (-240)) <= 8 and dx >= 50:
                nodes = make_slab_nodes(xl, xr, -240, O, H_slab, H_rise, 'bilateral', 'descender', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Caps E, F:
        elif gname in ['E', 'F']:
            if dy <= 4 and abs(y_avg - 0) <= 6 and xl < 200 and 60 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Cap L:
        elif gname == 'L':
            if dy <= 4 and abs(y_avg - 714) <= 6 and xl < 200 and 60 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, 714, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Standard uppercase stems (H, M, N, K, T, U):
        elif gname in ['H', 'M', 'N', 'K', 'T', 'U']:
            if gname != 'T' and dy <= 4 and abs(y_avg - 714) <= 6 and 60 <= dx <= 180:
                if gname == 'K' and xl > 250:
                    pass  # Keep diagonal top arm of K clean (Roboto Slab paradigm)
                elif gname == 'M' and 250 < xl < 650:
                    pass  # Keep interior diagonals of M clean
                else:
                    ol = O if (gname not in ['M', 'U'] or xl < 300) else int(O * 0.65)
                    or_ = O if (gname not in ['M', 'U'] or xl > 500) else int(O * 0.65)
                    nodes = make_slab_nodes(xl, xr, 714, O, H_slab, H_rise, 'bilateral', 'top', going_rtl, O_left=ol, O_right=or_)
                    for pt, flg in nodes:
                        new_pts.append(pt)
                        new_flgs.append(flg)
                    i += 2
                    continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                if gname == 'K' and xl > 250:
                    pass  # CRITICAL: Don't serify diagonal leg of K! Only vertical stem (xl < 250) gets a slab foot!
                elif gname == 'M' and 250 < xl < 650:
                    pass  # CRITICAL: Don't serify center apex of M! Only left and right outer stems get slab feet!
                else:
                    ol = O if (gname not in ['M', 'U'] or xl < 300) else int(O * 0.65)
                    or_ = O if (gname not in ['M', 'U'] or xl > 500) else int(O * 0.65)
                    nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl, O_left=ol, O_right=or_)
                    for pt, flg in nodes:
                        new_pts.append(pt)
                        new_flgs.append(flg)
                    i += 2
                    continue

        # Lowercase ascenders (h, k):
        elif gname in ['h', 'k']:
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_slab_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                if gname == 'k' and xl > 250:
                    pass  # CRITICAL: Don't serify diagonal leg of k! Only vertical stem (xl < 250) gets a slab foot!
                else:
                    nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                    for pt, flg in nodes:
                        new_pts.append(pt)
                        new_flgs.append(flg)
                    i += 2
                    continue

        # Lowercase x-height stems (m, n, r):
        elif gname in ['m', 'n', 'r']:
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_slab_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                # Moderate inner serifs on m to ensure spacious arch counters
                if gname == 'm':
                    if xl < 280:
                        ol, or_ = O, int(O * 0.6)
                    elif xl > 550:
                        ol, or_ = int(O * 0.6), O
                    else:
                        ol, or_ = int(O * 0.55), int(O * 0.55)
                else:
                    ol, or_ = O, O
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl, O_left=ol, O_right=or_)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase p:
        elif gname == 'p':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_slab_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - (-240)) <= 8 and 60 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, -240, O, H_slab, H_rise, 'bilateral', 'descender', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase u:
        elif gname == 'u':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_slab_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and xl >= 380 and 50 <= dx <= 150:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase a:
        elif gname == 'a':
            if dy <= 4 and abs(y_avg - 0) <= 6 and xl >= 380 and 50 <= dx <= 150:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Capital A: Left and right baseline slab feet
        elif gname == 'A':
            if dy <= 4 and abs(y_avg - 0) <= 6 and 40 <= dx <= 160:
                ol = O if xl < 200 else int(O * 0.65)
                or_ = int(O * 0.65) if xl < 200 else O
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl, O_left=ol, O_right=or_)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Cap Y & Lowercase y: Top arms and baseline stem foot
        elif gname in ['Y', 'y']:
            if dy <= 5 and (abs(y_avg - 714) <= 8 or abs(y_avg - 536) <= 8) and 40 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'bilateral', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 5 and abs(y_avg - 0) <= 8 and 50 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase f: Baseline stem slab
        elif gname == 'f':
            if dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Numeral 1: Broad baseline slab foot
        elif gname == 'one':
            if dy <= 5 and abs(y_avg - 0) <= 6 and dx >= 80:
                nodes = make_slab_nodes(xl, xr, 0, int(O * 1.15), H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Numeral 4: Baseline vertical stem slab
        elif gname == 'four':
            if dy <= 5 and abs(y_avg - 0) <= 6 and xl > 300 and 50 <= dx <= 160:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Numeral 7: Baseline foot slab
        elif gname == 'seven':
            if dy <= 5 and abs(y_avg - 0) <= 6 and 50 <= dx <= 160:
                nodes = make_slab_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Exclamation mark: Top wedge horizontal shelf
        elif gname == 'exclam':
            if dy <= 5 and abs(y_avg - 714) <= 6 and 60 <= dx <= 160:
                nodes = make_slab_nodes(xl, xr, 714, int(O * 0.7), H_slab, H_rise, 'bilateral', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        new_pts.append(p0)
        new_flgs.append(flags[i])
        i += 1

    return new_pts, new_flgs

def process_slab_font(src_name, family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=400, is_bold=False):
    style_suffix = "Bold" if is_bold else "Regular"
    ps_name = f"{ps_family}-{style_suffix}"
    out_ttf = TTF_DIR / f"{ps_name}.ttf"
    out_woff2 = WOFF2_DIR / f"{ps_name}.woff2"
    public_ttf = PUBLIC_DIR / f"{ps_name}.ttf"
    public_woff2 = PUBLIC_DIR / f"{ps_name}.woff2"

    print(f"\n==================================================================")
    print(f"Generating {family_name} {style_suffix} (from {src_name})")
    print(f"==================================================================")

    font = TTFont(TTF_DIR / src_name)
    glyf = font['glyf']
    hmtx = font['hmtx']

    # Modern UI Unbracketed 90° Digital Slab Architecture (Roboto Slab / Noto Slab Paradigm)
    # Pure unbracketed 90° right angles (H_rise = 0) with crisp rectangular slab authority
    if is_bold:
        O = 82
        H_slab = 88
        H_rise = 0
    else:
        O = 68
        H_slab = 68
        H_rise = 0

    target_glyphs = [
        'H', 'M', 'N', 'K', 'B', 'D', 'P', 'R', 'T', 'U', 'E', 'F', 'L',
        'A', 'Y',
        'b', 'd', 'h', 'k', 'm', 'n', 'p', 'q', 'r', 'u', 'a',
        'f', 'y',
        'one', 'four', 'seven', 'exclam'
    ]
    transformed = 0

    for gname in target_glyphs:
        if gname not in glyf:
            continue
        g = glyf[gname]
        if g.numberOfContours <= 0:
            continue

        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)

        new_coords = []
        new_flags = []
        new_endPts = []
        start = 0

        for end in endPts:
            c_pts = coords[start:end+1]
            c_flgs = flags[start:end+1]
            s_pts, s_flgs = serify_stem(c_pts, c_flgs, gname, O=O, H_slab=H_slab, H_rise=H_rise)
            new_coords.extend(s_pts)
            new_flags.extend(s_flgs)
            new_endPts.append(len(new_coords) - 1)
            start = end + 1

        g.coordinates = GlyphCoordinates(new_coords)
        g.flags = bytearray(new_flags)
        g.endPtsOfContours = new_endPts
        clean_glyph_geometry(g)

        # Boolean union & overlap simplification
        if HAS_PATHOPS:
            try:
                p = pathops.Path()
                glyphSet = font.getGlyphSet()
                glyphSet[gname].draw(p.getPen())
                p.simplify()
                tt_pen = TTGlyphPen(None)
                cu2qu_pen = Cu2QuPen(tt_pen, max_err=1.0)
                p.draw(cu2qu_pen)
                new_g = tt_pen.glyph()
                clean_glyph_geometry(new_g)
                new_g.recalcBounds(glyf)
                glyf[gname] = new_g
                g = new_g
            except Exception:
                pass

        g.recalcBounds(glyf)

        target_lsb = 40 if is_bold else 45
        target_rsb = 40 if is_bold else 45

        # Optical sidebearing compensation (Roboto Slab paradigm):
        # Prevent serifs from eating into left whitespace (which caused 3 UPM LSB and collisions)
        if gname == 'T':
            # Mathematically center T crossbar
            t_side = 35 if is_bold else 40
            shift_x = t_side - g.xMin
            g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in g.coordinates])
            g.recalcBounds(glyf)
            hmtx[gname] = (int(g.xMax + t_side), g.xMin)
        else:
            orig_adv, orig_lsb = hmtx[gname]
            if g.xMin < target_lsb:
                shift_x = target_lsb - g.xMin
                g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in g.coordinates])
                g.recalcBounds(glyf)
            new_adv = max(orig_adv, int(g.xMax + target_rsb))
            hmtx[gname] = (new_adv, g.xMin)
        transformed += 1

    # ISMP Special Glyphs:
    # 1. Capital 'I': Copy from I.serif (authenticated ISMP bilateral serifs)
    if 'I.serif' in glyf:
        glyf['I'] = copy.deepcopy(glyf['I.serif'])
        clean_glyph_geometry(glyf['I'])
        g = glyf['I']
        g.recalcBounds(glyf)
        i_side = 45 if is_bold else 50
        if g.xMin < i_side:
            shift_x = i_side - g.xMin
            g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in g.coordinates])
            g.recalcBounds(glyf)
        hmtx['I'] = (int(g.xMax + i_side), g.xMin)
        print("  • Injected authenticated ISMP Capital 'I' (ss02 bilateral serifs)")

    # 2. Lowercase 'l': Keep curved foot (cv05) and add top entry spur
    if 'l' in glyf:
        g = glyf['l']
        coords = list(g.coordinates)
        flags = list(g.flags)
        s_pts, s_flgs = serify_stem(coords, flags, 'h', O=O, H_slab=H_slab, H_rise=H_rise)
        g.coordinates = GlyphCoordinates(s_pts)
        g.flags = bytearray(s_flgs)
        g.endPtsOfContours = [len(s_pts) - 1]
        clean_glyph_geometry(g)
        g.recalcBounds(glyf)
        l_side = 40 if is_bold else 45
        if g.xMin < l_side:
            shift_x = l_side - g.xMin
            g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in g.coordinates])
            g.recalcBounds(glyf)
        hmtx['l'] = (max(hmtx['l'][0], int(g.xMax + l_side)), g.xMin)
        print("  • Injected ISMP Lowercase 'l' (top entry spur + outward terminal curved foot)")

    # 3. Lowercase 'i': Base serif + top spur, preserves heart tittle
    if 'i' in glyf:
        g = glyf['i']
        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)
        if len(endPts) == 2:
            stem_pts = coords[:endPts[0]+1]
            stem_flgs = flags[:endPts[0]+1]
            dot_pts = coords[endPts[0]+1:]
            dot_flgs = flags[endPts[0]+1:]
            
            s_pts, s_flgs = serify_stem(stem_pts, stem_flgs, 'n', O=O, H_slab=H_slab, H_rise=H_rise)
            g.coordinates = GlyphCoordinates(s_pts + dot_pts)
            g.flags = bytearray(s_flgs + dot_flgs)
            g.endPtsOfContours = [len(s_pts) - 1, len(s_pts) + len(dot_pts) - 1]
            clean_glyph_geometry(g)
            g.recalcBounds(glyf)
            i_side = 40 if is_bold else 45
            if g.xMin < i_side:
                shift_x = i_side - g.xMin
                g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in g.coordinates])
                g.recalcBounds(glyf)
            hmtx['i'] = (max(hmtx['i'][0], int(g.xMax + i_side)), g.xMin)
            print("  • Injected ISMP Lowercase 'i' (calibrated tittle + base slab & entry spur)")

    print(f"  -> Transformed {transformed} letterforms with robust slab serifs.")

    # 4. OpenType Option 5 Metadata aligned to SemVer 3.1.0
    print("Updating OpenType metadata & Option 5 naming table...")
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = font['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]

    def add_name(name_id, text):
        name_table.addMultilingualName({'en': text}, font, nameID=name_id)

    add_name(0, copyright_str)
    add_name(1, family_name)
    add_name(2, style_suffix)
    add_name(3, f"3.100;POCK;{ps_name}")
    add_name(4, f"{family_name} {style_suffix}")
    add_name(5, version_str)
    add_name(6, ps_name)
    add_name(16, family_name)
    add_name(17, style_suffix)

    font['head'].fontRevision = 3.1
    font['head'].macStyle = 0x0001 if is_bold else 0x0000

    if 'OS/2' in font:
        font['OS/2'].usWeightClass = weight_class
        if is_bold:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x20 | 0x80
        else:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x40 | 0x80
        font['OS/2'].achVendID = 'POCK'
        font['OS/2'].fsType = 0x0000

    font.save(str(out_ttf))
    font.close()

    # Realign loca/glyf to 2-byte word boundaries
    font = TTFont(str(out_ttf))
    glyf = font['glyf']
    for gn in font.getGlyphOrder():
        glyph = glyf[gn]
        if hasattr(glyph, 'data') and glyph.data and len(glyph.data) % 2 != 0:
            glyph.data = glyph.data + b'\x00'
    font.save(str(out_ttf))
    font.close()

    # WOFF2 compression
    compress(str(out_ttf), str(out_woff2))

    # Sync to public mirror
    if PUBLIC_DIR.exists():
        shutil.copy2(str(out_ttf), str(public_ttf))
        shutil.copy2(str(out_woff2), str(public_woff2))

    print(f"[SUCCESS] Compiled {out_ttf}")
    print(f"[SUCCESS] Compressed {out_woff2} ({out_woff2.stat().st_size:,} bytes)")

def build_slab_superfamily():
    print("==================================================================")
    print("POCKETGULL TYPEFOUNDRY: SLAB MASTERFAMILY COMPILER (v3.1)")
    print("==================================================================")
    process_slab_font("PocketGull-Regular.ttf", family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=400, is_bold=False)
    process_slab_font("PocketGull-Bold.ttf", family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=700, is_bold=True)
    print("\n[ALL DONE] PocketGull Slab Regular and Bold successfully compiled!")

if __name__ == '__main__':
    build_slab_superfamily()
