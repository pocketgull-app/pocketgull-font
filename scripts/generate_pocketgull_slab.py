#!/usr/bin/env python3
"""
PocketGull Typefoundry: Warm Humanist Slab Generator v4.0.0
=========================================================
Synthesizes PocketGull-Slab-Regular (400) and PocketGull-Slab-Bold (700)
from pristine PocketGull sans masters using constructive Skia `pathops`
boolean unioning, warm quadratic bracketing (PMN Caecilia / Zilla Slab /
Bitter DNA), subtle felt-marker corner warmth, sculpted arm beaks, curved
terminal slabs, unified ISMP safeguards, and a tailored GPOS `kern` table.

Key Invariants Enforced:
- 1000 UPM em-square, 2-byte word alignment (loca[i] % 2 == 0, size % 2 == 0)
- Zero-VM TrueType posture (no fpgm/cvt/prep; glyph instructionLength == 0)
- Reserved bit-6/7 flag masking (flag & 0x3F)
- Strict CW outer / CCW hole contour winding via pathops.simplify(clockwise=True)
- Karen Cheng <= 65% slab-to-stem ratio & I >= 300 UPM width
- Ellen Lupton Sloan 5:1 aspect envelopes & ISMP disambiguation (I, l, 0, Z)
- Full 9,718-glyph host preservation, diacritic composite centering, and v4.0.0 metadata
"""

import copy
import hashlib
import base64
import json
import shutil
from pathlib import Path

import pathops
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables, otBase, ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.woff2 import compress
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
STAGE_DIR = ROOT_DIR / "distribution" / "windows-installer" / "stage_ttf"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

# ---------------------------------------------------------------------------
# Warm Humanist Slab Design Tokens (Derived from Measured Base Stems)
# Regular: Cap H stem = 90 UPM, lc n stem = 88 UPM
# Bold:    Cap H stem = 151 UPM, lc n stem = 151 UPM
# ---------------------------------------------------------------------------
DESIGN_PARAMS = {
    "Regular": {
        "src_sans": "PocketGull-Regular.ttf",
        "host_slab": "PocketGull-Slab-Regular.ttf",
        "weight_class": 400,
        "is_bold": False,
        "cap_h": 714,
        "asc_h": 760,
        "x_h": 536,
        "desc_y": -240,
        "stem_cap": 90,
        # Slab dimensions (55.6% cap / 52.3% lc of stem)
        "H_cap": 50,
        "taper_cap": 3,
        "H_br_cap": 20,
        "H_lc": 46,
        "taper_lc": 3,
        "H_br_lc": 18,
        "R_tip": 8,
        "R_tip_sm": 6,
        "top_slope": 5,
        # Overhangs
        "O_cap": 54,
        "O_cap_in": 46,
        "O_I": 110,          # 90 + 2*110 = 310 UPM (>= 300 Karen Cheng)
        "O_lc": 48,
        "O_lc_in": 38,
        "O_m_in": 32,
        "O_diag_out": 40,
        "O_diag_in": 26,
        "O_lc_diag_out": 34,
        "O_lc_diag_in": 20,
        # Arm Beaks (E, F, L, T, Z, z, 2, 7)
        "W_beak": 50,
        "L_beak": 122,       # Total vertical height from arm outer edge
        "R_br_beak": 22,
        "flare_beak": 5,
        # Curved Terminals (C, G, S, c, s)
        "W_term": 44,
        "L_term_cap": 126,
        "L_term_lc": 90,
        # Sidebearings
        "sb_stem": 40,
        "sb_narrow": 38,
        "sb_diag": 28,
        "sb_arm": 28,
        "sb_f_left": 32,
        "sb_f_right": 34,
        "kern_scale": 1.0,
    },
    "Bold": {
        "src_sans": "PocketGull-Bold.ttf",
        "host_slab": "PocketGull-Slab-Bold.ttf",
        "weight_class": 700,
        "is_bold": True,
        "cap_h": 714,
        "asc_h": 760,
        "x_h": 546,
        "desc_y": -240,
        "stem_cap": 151,
        # Slab dimensions (55.6% cap / 51.7% lc of stem)
        "H_cap": 84,
        "taper_cap": 5,
        "H_br_cap": 24,
        "H_lc": 78,
        "taper_lc": 4,
        "H_br_lc": 20,
        "R_tip": 10,
        "R_tip_sm": 7,
        "top_slope": 6,
        # Overhangs
        "O_cap": 60,
        "O_cap_in": 48,
        "O_I": 106,          # 151 + 2*106 = 363 UPM (>= 300 Karen Cheng)
        "O_lc": 52,
        "O_lc_in": 40,
        "O_m_in": 30,
        "O_diag_out": 44,
        "O_diag_in": 24,
        "O_lc_diag_out": 36,
        "O_lc_diag_in": 18,
        # Arm Beaks
        "W_beak": 78,
        "L_beak": 168,
        "R_br_beak": 26,
        "flare_beak": 6,
        # Curved Terminals
        "W_term": 68,
        "L_term_cap": 152,
        "L_term_lc": 112,
        # Sidebearings
        "sb_stem": 36,
        "sb_narrow": 34,
        "sb_diag": 24,
        "sb_arm": 26,
        "sb_f_left": 28,
        "sb_f_right": 30,
        "kern_scale": 0.92,
    },
}


# ---------------------------------------------------------------------------
# Geometry & Scanline Utilities
# ---------------------------------------------------------------------------
def clean_glyph_geometry(glyph: Glyph) -> None:
    if glyph.numberOfContours <= 0:
        return
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    end_pts = list(glyph.endPtsOfContours)
    new_coords, new_flags, new_end_pts = [], [], []
    start = 0
    for end in end_pts:
        pts = coords[start : end + 1]
        flgs = flags[start : end + 1]
        f_pts, f_flgs = [], []
        for pt, fl in zip(pts, flgs):
            fl_masked = fl & 0x3F
            if not f_pts or pt != f_pts[-1]:
                f_pts.append(pt)
                f_flgs.append(fl_masked)
        if len(f_pts) > 1 and f_pts[0] == f_pts[-1]:
            f_pts = f_pts[:-1]
            f_flgs = f_flgs[:-1]
        if len(f_pts) >= 3:
            new_coords.extend(f_pts)
            new_flags.extend(f_flgs)
            new_end_pts.append(len(new_coords) - 1)
        start = end + 1
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray(new_flags)
    glyph.endPtsOfContours = new_end_pts
    prog = ttProgram.Program()
    prog.fromBytecode(b"")
    glyph.program = prog


def contour_signed_area(pts) -> float:
    n = len(pts)
    if n < 3:
        return 0.0
    return sum(
        pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
        for i in range(n)
    ) / 2.0


def verify_cw_outer_winding(glyph: Glyph, gname: str) -> None:
    if glyph.numberOfContours <= 0:
        return
    pts = list(glyph.coordinates)
    start = 0
    areas = []
    for end in glyph.endPtsOfContours:
        areas.append(contour_signed_area(pts[start : end + 1]))
        start = end + 1
    # Largest contour by magnitude must be CW (negative signed area in y-up)
    largest = max(areas, key=lambda a: abs(a))
    if largest > 0:
        raise ValueError(f"Glyph {gname} inverted winding: largest contour area={largest}")


def flatten_glyph_segments(glyph_set, gname: str, steps: int = 16):
    rec = DecomposingRecordingPen(glyph_set)
    glyph_set[gname].draw(rec)
    segs = []
    cur = None
    start_pt = None
    for op, args in rec.value:
        if op == "moveTo":
            cur = args[0]
            start_pt = cur
        elif op == "lineTo":
            nxt = args[0]
            if cur is not None and nxt != cur:
                segs.append((cur, nxt))
            cur = nxt
        elif op == "qCurveTo":
            # FontTools qCurveTo may have multiple off-curve pts + final on-curve
            pts_seq = list(args)
            if pts_seq[-1] is None:
                # rare closed all-offcurve
                continue
            p0 = cur
            for idx in range(len(pts_seq) - 1):
                c = pts_seq[idx]
                if idx == len(pts_seq) - 2:
                    p2 = pts_seq[idx + 1]
                else:
                    nxt_c = pts_seq[idx + 1]
                    p2 = ((c[0] + nxt_c[0]) * 0.5, (c[1] + nxt_c[1]) * 0.5)
                prev = p0
                for s in range(1, steps + 1):
                    t = s / steps
                    mt = 1.0 - t
                    qx = mt * mt * p0[0] + 2 * mt * t * c[0] + t * t * p2[0]
                    qy = mt * mt * p0[1] + 2 * mt * t * c[1] + t * t * p2[1]
                    if (qx, qy) != prev:
                        segs.append((prev, (qx, qy)))
                        prev = (qx, qy)
                p0 = p2
            cur = pts_seq[-1]
        elif op == "curveTo":
            p0, c1, c2, p3 = cur, args[0], args[1], args[2]
            prev = p0
            for s in range(1, steps + 1):
                t = s / steps
                mt = 1.0 - t
                cx = (mt**3) * p0[0] + 3 * (mt**2) * t * c1[0] + 3 * mt * (t**2) * c2[0] + (t**3) * p3[0]
                cy = (mt**3) * p0[1] + 3 * (mt**2) * t * c1[1] + 3 * mt * (t**2) * c2[1] + (t**3) * p3[1]
                if (cx, cy) != prev:
                    segs.append((prev, (cx, cy)))
                    prev = (cx, cy)
            cur = p3
        elif op == "closePath":
            if cur is not None and start_pt is not None and cur != start_pt:
                segs.append((cur, start_pt))
            cur = start_pt
    return segs


def slice_x_intervals(segs, y_sample: float):
    """Returns sorted [(xl, xr), ...] filled x-intervals at horizontal scanline y_sample."""
    xs = []
    for (x0, y0), (x1, y1) in segs:
        if (y0 <= y_sample < y1) or (y1 <= y_sample < y0):
            t = (y_sample - y0) / (y1 - y0)
            xs.append(x0 + t * (x1 - x0))
    xs.sort()
    spans = []
    for i in range(0, len(xs) - 1, 2):
        if xs[i + 1] - xs[i] > 1.0:
            spans.append((xs[i], xs[i + 1]))
    return spans


def slice_y_intervals(segs, x_sample: float):
    """Returns sorted [(yb, yt), ...] filled y-intervals at vertical scanline x_sample."""
    ys = []
    for (x0, y0), (x1, y1) in segs:
        if (x0 <= x_sample < x1) or (x1 <= x_sample < x0):
            t = (x_sample - x0) / (x1 - x0)
            ys.append(y0 + t * (y1 - y0))
    ys.sort()
    spans = []
    for i in range(0, len(ys) - 1, 2):
        if ys[i + 1] - ys[i] > 1.0:
            spans.append((ys[i], ys[i + 1]))
    return spans


def measure_stem_trapezoid(segs, y_tip: float, pos: str, span_idx: int, dy_near: float = 2.0, dy_far: float = 48.0):
    """
    Samples stem span `span_idx` at y_tip +- dy_near and y_tip +- dy_far,
    returning ((xl_tip, xr_tip), (xl_far, xr_far)) extrapolated exactly to y_tip.
    Handles both straight stems and diagonal legs seamlessly.
    """
    sign = 1.0 if pos in ("base", "descender") else -1.0
    y1 = y_tip + sign * dy_near
    y2 = y_tip + sign * dy_far
    s1 = slice_x_intervals(segs, y1)
    s2 = slice_x_intervals(segs, y2)
    if span_idx < 0:
        idx1 = len(s1) + span_idx
        idx2 = len(s2) + span_idx
    else:
        idx1, idx2 = span_idx, span_idx
    xl1, xr1 = s1[idx1]
    xl2, xr2 = s2[idx2]
    # Linear extrapolation back to y_tip
    k = -dy_near / (dy_far - dy_near)
    xl0 = xl1 + k * (xl2 - xl1)
    xr0 = xr1 + k * (xr2 - xr1)
    return (xl0, xr0), (xl2, xr2)


def union_paths_to_glyph(base_path: pathops.Path, addon_paths: list, gname: str) -> Glyph:
    if not addon_paths:
        out = pathops.Path(base_path)
    else:
        out = pathops.Path()
        pathops.union([base_path] + addon_paths, out.getPen())
    out.simplify(clockwise=True)
    tt_pen = TTGlyphPen(None)
    cu2qu = Cu2QuPen(tt_pen, max_err=0.75, reverse_direction=False)
    out.draw(cu2qu)
    new_g = tt_pen.glyph()
    clean_glyph_geometry(new_g)
    verify_cw_outer_winding(new_g, gname)
    return new_g


def glyph_to_path(glyph_set, gname: str) -> pathops.Path:
    p = pathops.Path()
    glyph_set[gname].draw(p.getPen())
    return p


# ---------------------------------------------------------------------------
# Constructive CW Slab, Beak, and Curved Terminal Builders
# ---------------------------------------------------------------------------
def make_slab_path(
    xl_0: float,
    xr_0: float,
    xl_in: float,
    xr_in: float,
    y: float,
    H: float,
    H_br: float,
    taper: float,
    R_tip: float,
    ol: float,
    or_: float,
    pos: str = "base",
    mode: str = "bilateral",
    slope: float = 0.0,
) -> pathops.Path:
    """
    Constructs a CW closed Skia Path for a Warm Humanist bracketed slab serif.
    - `pos`: 'base' (or 'descender', stem rises upward from y) or 'top' (stem descends from y)
    - `mode`: 'bilateral', 'left_only', 'right_only'
    - `taper`: thickness reduction from stem shoulder to outer tip (Caecilia refinement)
    - `slope`: subtle vertical drop on outer tip of `left_only` top entry flags
    - `R_tip`: felt-marker outer tip corner radius
    """
    p = pathops.Path()
    H_tot = H + H_br
    H_edge = max(12.0, H - taper)
    mid_x0 = 0.5 * (xl_0 + xr_0)
    mid_xin = 0.5 * (xl_in + xr_in)

    use_left = mode in ("bilateral", "left_only") and ol > 2.0
    use_right = mode in ("bilateral", "right_only") and or_ > 2.0

    r_l = min(R_tip, H_edge * 0.42, ol * 0.45) if use_left else 0.0
    r_r = min(R_tip, H_edge * 0.42, or_ * 0.45) if use_right else 0.0

    if pos in ("base", "descender"):
        y_in = y + H_tot
        x_l = xl_0 - ol
        x_r = xr_0 + or_

        # Start at bottom interior or bottom right, trace CW (bottom right->left, up left, across, down right)
        if use_right:
            p.moveTo(x_r - r_r, y)
        else:
            p.moveTo(mid_x0, y)

        if use_left:
            p.lineTo(x_l + r_l, y)
            if r_l > 0.5:
                p.quadTo(x_l, y, x_l, y + r_l)
            else:
                p.lineTo(x_l, y)
            p.lineTo(x_l, y + H_edge - r_l)
            if r_l > 0.5:
                p.quadTo(x_l, y + H_edge, x_l + r_l, y + H_edge)
            else:
                p.lineTo(x_l, y + H_edge)
            # Bracket up into stem left edge
            x_sh_l = min(xl_0, xl_in)
            p.lineTo(x_sh_l - min(H_br * 0.75, ol * 0.45), y + H)
            p.quadTo(xl_in, y + H, xl_in, y_in)
        else:
            p.lineTo(mid_x0, y)
            p.lineTo(mid_xin, y_in)

        if use_right:
            p.lineTo(xr_in, y_in)
            # Bracket down to right slab top shelf
            x_sh_r = max(xr_0, xr_in)
            p.quadTo(xr_in, y + H, x_sh_r + min(H_br * 0.75, or_ * 0.45), y + H)
            p.lineTo(x_r - r_r, y + H_edge)
            if r_r > 0.5:
                p.quadTo(x_r, y + H_edge, x_r, y + H_edge - r_r)
            else:
                p.lineTo(x_r, y + H_edge)
            p.lineTo(x_r, y + r_r)
            if r_r > 0.5:
                p.quadTo(x_r, y, x_r - r_r, y)
            else:
                p.lineTo(x_r, y)
        else:
            p.lineTo(mid_xin, y_in)
            p.lineTo(mid_x0, y)

        p.close()

    else:  # pos == 'top' (stem descends downward from y)
        y_in = y - H_tot
        x_l = xl_0 - ol
        x_r = xr_0 + or_
        sl_l = slope if (mode == "left_only" and ol > 2.0) else 0.0

        # CW in y-up: top edge left->right, right side down, bottom right->left, left side up
        if use_left:
            p.moveTo(x_l + r_l, y - sl_l)
            if sl_l > 0.5:
                p.lineTo(xl_0, y)
            else:
                p.lineTo(xl_0, y)
        else:
            p.moveTo(mid_x0, y)

        if use_right:
            p.lineTo(x_r - r_r, y)
            if r_r > 0.5:
                p.quadTo(x_r, y, x_r, y - r_r)
            else:
                p.lineTo(x_r, y)
            p.lineTo(x_r, y - H_edge + r_r)
            if r_r > 0.5:
                p.quadTo(x_r, y - H_edge, x_r - r_r, y - H_edge)
            else:
                p.lineTo(x_r, y - H_edge)
            x_sh_r = max(xr_0, xr_in)
            p.lineTo(x_sh_r + min(H_br * 0.75, or_ * 0.45), y - H)
            p.quadTo(xr_in, y - H, xr_in, y_in)
        else:
            p.lineTo(mid_x0, y)
            p.lineTo(mid_xin, y_in)

        if use_left:
            p.lineTo(xl_in, y_in)
            x_sh_l = min(xl_0, xl_in)
            p.quadTo(xl_in, y - H, x_sh_l - min(H_br * 0.75, ol * 0.45), y - H)
            p.lineTo(x_l + r_l, y - H_edge - sl_l * 0.4)
            if r_l > 0.5:
                p.quadTo(x_l, y - H_edge - sl_l * 0.4, x_l, y - H_edge - sl_l * 0.4 + r_l)
            else:
                p.lineTo(x_l, y - H_edge - sl_l * 0.4)
            p.lineTo(x_l, y - sl_l - r_l)
            if r_l > 0.5:
                p.quadTo(x_l, y - sl_l, x_l + r_l, y - sl_l)
            else:
                p.lineTo(x_l, y - sl_l)
        else:
            p.lineTo(mid_xin, y_in)
            p.lineTo(mid_x0, y)

        p.close()

    return p


def make_beak_path(
    x_outer: float,
    y_outer: float,
    y_inner: float,
    W_beak: float,
    L_beak: float,
    R_br: float,
    R_tip: float,
    side: str = "right",
    direction: str = "down",
    flare: float = 7.0,
) -> pathops.Path:
    """
    Constructs a CW closed Skia Path for a sculpted vertical arm beak (E, F, L, T, Z, z, 2, 7).
    - `side`: 'right' (arm extends from left to x_outer) or 'left' (arm extends from x_outer to right)
    - `direction`: 'down' (hangs downward from y_outer >= y_inner) or 'up' (rises upward from y_outer <= y_inner)
    - `flare`: subtle outward lean at the beak tip for calligraphic balance
    """
    p = pathops.Path()
    r = min(R_tip, W_beak * 0.35)
    r_in = min(R_tip * 0.7, W_beak * 0.28)
    overlap_in = 14.0

    if side == "right" and direction == "down":
        # Arm is to the left of x_outer; y_outer is top of arm, y_inner is bottom of arm
        y_tip = y_outer - L_beak
        x_tip_out = x_outer + flare
        x_in = x_tip_out - W_beak
        x_root = x_outer - W_beak + flare * 0.3
        x_arm_in = min(x_root, x_in) - R_br - overlap_in
        y_arm_mid = 0.5 * (y_outer + y_inner)

        # CW: top-left inside arm -> top-right -> down outer flared edge -> bottom tip -> up inner -> bracket -> arm underside
        p.moveTo(x_arm_in, y_outer)
        p.lineTo(x_outer - r, y_outer)
        p.quadTo(x_outer, y_outer, x_outer + flare * (r / max(1.0, L_beak)), y_outer - r)
        p.lineTo(x_tip_out - flare * (r / max(1.0, L_beak)), y_tip + r)
        p.quadTo(x_tip_out, y_tip, x_tip_out - r, y_tip)
        p.lineTo(x_in + r_in, y_tip)
        p.quadTo(x_in, y_tip, x_in, y_tip + r_in)
        p.lineTo(x_root, y_inner - R_br)
        p.quadTo(x_root, y_inner, x_root - R_br, y_inner)
        p.lineTo(x_arm_in, y_inner)
        p.lineTo(x_arm_in, y_arm_mid)
        p.close()

    elif side == "left" and direction == "down":
        # Arm is to the right of x_outer; y_outer is top of arm, y_inner is bottom of arm
        y_tip = y_outer - L_beak
        x_tip_out = x_outer - flare
        x_in = x_tip_out + W_beak
        x_root = x_outer + W_beak - flare * 0.3
        x_arm_in = max(x_root, x_in) + R_br + overlap_in

        # CW: arm underside -> bracket -> down inner -> bottom tip -> up outer edge -> top-left -> inside arm
        p.moveTo(x_outer + r, y_outer)
        p.lineTo(x_arm_in, y_outer)
        p.lineTo(x_arm_in, y_inner)
        p.lineTo(x_root + R_br, y_inner)
        p.quadTo(x_root, y_inner, x_root, y_inner - R_br)
        p.lineTo(x_in, y_tip + r_in)
        p.quadTo(x_in, y_tip, x_in - r_in, y_tip)
        p.lineTo(x_tip_out + r, y_tip)
        p.quadTo(x_tip_out, y_tip, x_tip_out + flare * (r / max(1.0, L_beak)), y_tip + r)
        p.lineTo(x_outer - flare * (r / max(1.0, L_beak)), y_outer - r)
        p.quadTo(x_outer, y_outer, x_outer + r, y_outer)
        p.close()

    elif side == "right" and direction == "up":
        # Arm is to the left of x_outer; y_outer is bottom of arm (e.g. 0), y_inner is top of arm (e.g. 79)
        y_tip = y_outer + L_beak
        x_tip_out = x_outer + flare
        x_in = x_tip_out - W_beak
        x_root = x_outer - W_beak + flare * 0.3
        x_arm_in = min(x_root, x_in) - R_br - overlap_in

        # CW: inside arm top -> bracket -> up inner -> top tip -> down outer edge -> bottom-right -> inside bottom
        p.moveTo(x_arm_in, y_inner)
        p.lineTo(x_root - R_br, y_inner)
        p.quadTo(x_root, y_inner, x_root, y_inner + R_br)
        p.lineTo(x_in, y_tip - r_in)
        p.quadTo(x_in, y_tip, x_in + r_in, y_tip)
        p.lineTo(x_tip_out - r, y_tip)
        p.quadTo(x_tip_out, y_tip, x_tip_out - flare * (r / max(1.0, L_beak)), y_tip - r)
        p.lineTo(x_outer + flare * (r / max(1.0, L_beak)), y_outer + r)
        p.quadTo(x_outer, y_outer, x_outer - r, y_outer)
        p.lineTo(x_arm_in, y_outer)
        p.close()

    elif side == "left" and direction == "up":
        y_tip = y_outer + L_beak
        x_tip_out = x_outer - flare
        x_in = x_tip_out + W_beak
        x_root = x_outer + W_beak - flare * 0.3
        x_arm_in = max(x_root, x_in) + R_br + overlap_in

        p.moveTo(x_outer + r, y_outer)
        p.quadTo(x_outer, y_outer, x_outer - flare * (r / max(1.0, L_beak)), y_outer + r)
        p.lineTo(x_tip_out + flare * (r / max(1.0, L_beak)), y_tip - r)
        p.quadTo(x_tip_out, y_tip, x_tip_out + r, y_tip)
        p.lineTo(x_in - r_in, y_tip)
        p.quadTo(x_in, y_tip, x_in, y_tip - r_in)
        p.lineTo(x_root, y_inner + R_br)
        p.quadTo(x_root, y_inner, x_root + R_br, y_inner)
        p.lineTo(x_arm_in, y_inner)
        p.lineTo(x_arm_in, y_outer)
        p.close()

    return p


def make_midbar_cap_path(x_end: float, y_bot: float, y_top: float, W: float, proj: float, R_br: float, R_tip: float) -> pathops.Path:
    """Bilateral vertical cap on the right end of E's center crossbar."""
    p = pathops.Path()
    r = min(R_tip, W * 0.32)
    x_root = x_end - W
    x_in = x_root - R_br - 12.0
    y_t = y_top + proj
    y_b = y_bot - proj

    # CW: inside top -> bracket -> up inner -> top cap -> down outer -> bottom cap -> up inner -> bracket -> inside bot
    p.moveTo(x_in, y_top)
    p.lineTo(x_root - R_br, y_top)
    p.quadTo(x_root, y_top, x_root, y_top + R_br * 0.7)
    p.lineTo(x_root, y_t - r * 0.7)
    p.quadTo(x_root, y_t, x_root + r * 0.7, y_t)
    p.lineTo(x_end - r, y_t)
    p.quadTo(x_end, y_t, x_end, y_t - r)
    p.lineTo(x_end, y_b + r)
    p.quadTo(x_end, y_b, x_end - r, y_b)
    p.lineTo(x_root + r * 0.7, y_b)
    p.quadTo(x_root, y_b, x_root, y_b + r * 0.7)
    p.lineTo(x_root, y_bot - R_br * 0.7)
    p.quadTo(x_root, y_bot, x_root - R_br, y_bot)
    p.lineTo(x_in, y_bot)
    p.close()
    return p


def make_upper_right_terminal_slab(
    pt_out, pt_in, y_arch_top: float, W_term: float, drop_below_in: float, R_br: float, R_tip: float, flare: float = 0.0
) -> pathops.Path:
    """
    Constructs a sculpted downward vertical terminal slab anchored flush onto
    the upper-right stroke cut (pt_out, pt_in) of C, G, S, c, s with zero shoulder bump
    and consistent downward projection `drop_below_in` past `y_in_cut`.
    """
    p = pathops.Path()
    x_out_cut, y_out_cut = pt_out
    x_in_cut, y_in_cut = pt_in

    y_top = min(y_arch_top - 8.0, y_out_cut + 2.0)
    x_outer_top = x_out_cut
    x_outer_bot = x_out_cut + flare
    y_bot = y_in_cut - drop_below_in
    x_inner_bot = x_outer_bot - W_term
    x_inner_mid = min(x_in_cut, x_outer_top - W_term + 2.0)

    x_overlap = min(x_in_cut, x_outer_top - W_term) - 32.0
    y_overlap_top = y_out_cut + 4.0
    y_overlap_bot = min(y_overlap_top - 10.0, 0.5 * (y_out_cut + y_in_cut) + 10.0)

    r_top = min(4.0, R_tip * 0.5)
    r = min(R_tip, W_term * 0.30)
    r_in = min(R_tip * 0.7, W_term * 0.24)

    # CW in y-up: overlap_top -> outer_top -> outer_bot -> inner_bot -> inner bracket -> overlap_bot
    p.moveTo(x_overlap, y_overlap_top)
    p.lineTo(x_outer_top - r_top, y_top)
    p.quadTo(x_outer_top, y_top, x_outer_top, y_top - r_top)
    p.lineTo(x_outer_bot, y_bot + r)
    p.quadTo(x_outer_bot, y_bot, x_outer_bot - r, y_bot)
    p.lineTo(x_inner_bot + r_in, y_bot)
    p.quadTo(x_inner_bot, y_bot, x_inner_bot, y_bot + r_in)
    p.lineTo(x_inner_mid, y_in_cut - R_br * 0.7)
    p.quadTo(x_inner_mid, y_in_cut + 2.0, x_overlap, y_overlap_bot)
    p.close()
    return p


def make_lower_left_terminal_slab(
    pt_out_bot, pt_in_top, y_arch_bot: float, W_term: float, rise_above_in: float, R_br: float, R_tip: float, flare: float = 0.0
) -> pathops.Path:
    """
    Constructs a sculpted upward vertical terminal slab anchored collinearly onto
    the lower-left stroke cut (pt_out_bot, pt_in_top) of S and s with zero bottom dent.
    """
    p = pathops.Path()
    x_cut, y_cut_bot = pt_out_bot
    _, y_cut_top = pt_in_top

    x_left_bot = x_cut
    x_left_top = x_left_bot - flare
    y_bot = y_cut_bot
    y_top = y_cut_top + rise_above_in
    x_right_top = x_left_top + W_term
    x_right_mid = max(x_cut + W_term - 2.0, x_left_bot + W_term - 2.0)

    x_overlap = x_right_mid + 34.0
    y_overlap_bot = y_cut_bot + 10.0
    y_overlap_top = max(y_overlap_bot + 10.0, 0.5 * (y_cut_bot + y_cut_top) - 6.0)

    r = min(R_tip, W_term * 0.30)
    r_in = min(R_tip * 0.7, W_term * 0.24)

    # CW in y-up: trace flush from (x_left_bot, y_bot) straight up outer cut -> top -> inner bracket -> overlap
    p.moveTo(x_left_bot, y_bot)
    p.lineTo(x_left_top, y_top - r)
    p.quadTo(x_left_top, y_top, x_left_top + r, y_top)
    p.lineTo(x_right_top - r_in, y_top)
    p.quadTo(x_right_top, y_top, x_right_top, y_top - r_in)
    p.lineTo(x_right_mid, y_cut_top + R_br * 0.7)
    p.quadTo(x_right_mid, y_cut_top - 2.0, x_overlap, y_overlap_top)
    p.lineTo(x_overlap, y_overlap_bot)
    p.lineTo(x_left_bot, y_bot)
    p.close()
    return p


def build_unified_I(cfg: dict) -> Glyph:
    """Builds a cohesive Capital I matching H's slab height, bracketing, taper, and warmth."""
    stem_w = cfg["stem_cap"]
    cap_h = cfg["cap_h"]
    O_I = cfg["O_I"]
    xl = float(O_I)
    xr = float(O_I + stem_w)

    stem_p = pathops.Path()
    stem_p.moveTo(xl, 0)
    stem_p.lineTo(xl, cap_h)
    stem_p.lineTo(xr, cap_h)
    stem_p.lineTo(xr, 0)
    stem_p.close()

    top_slab = make_slab_path(
        xl, xr, xl, xr, cap_h, cfg["H_cap"], cfg["H_br_cap"], cfg["taper_cap"],
        cfg["R_tip"], O_I, O_I, pos="top", mode="bilateral",
    )
    bot_slab = make_slab_path(
        xl, xr, xl, xr, 0, cfg["H_cap"], cfg["H_br_cap"], cfg["taper_cap"],
        cfg["R_tip"], O_I, O_I, pos="base", mode="bilateral",
    )
    return union_paths_to_glyph(stem_p, [top_slab, bot_slab], "I")


def build_warm_hooked_l(sans_l: Glyph, cfg: dict, gname: str) -> Glyph:
    """
    Preserves ISMP hooked clinical 'l' (cv05 / default cmap) while sculpting a
    Warm Humanist top entry flag and subtle warm inner fillet + softened foot tip.
    """
    pts = list(sans_l.coordinates)
    xs = sorted(set(p[0] for p in pts))
    xl = float(xs[0])
    xr_stem = float(xs[1])
    xr_foot = float(xs[2])
    ys = sorted(set(p[1] for p in pts))
    # ys = [0, y_hook, asc_h]
    y_hook = float(ys[1])
    asc_h = float(cfg["asc_h"])

    r_tip = cfg["R_tip_sm"]
    r_br = cfg["H_br_lc"]
    r_heel = 26.0 if not cfg["is_bold"] else 34.0
    target_ext = 64.0 if not cfg["is_bold"] else 70.0
    xr_new_foot = xr_stem + target_ext
    h_foot = float(cfg["H_lc"])

    p = pathops.Path()
    # Base CW stem with warm curved humanist outer heel + bracketed hooked foot
    p.moveTo(xl + r_heel, 0)
    p.quadTo(xl, 0, xl, r_heel)
    p.lineTo(xl, asc_h)
    p.lineTo(xr_stem, asc_h)
    p.lineTo(xr_stem, h_foot + r_br)
    p.quadTo(xr_stem, h_foot, xr_stem + min(r_br * 0.8, target_ext * 0.4), h_foot)
    p.lineTo(xr_new_foot - r_tip, h_foot - 2.0)
    p.quadTo(xr_new_foot, h_foot - 2.0, xr_new_foot, h_foot - 2.0 - r_tip)
    p.lineTo(xr_new_foot, r_tip)
    p.quadTo(xr_new_foot, 0, xr_new_foot - r_tip, 0)
    p.close()

    top_flag = make_slab_path(
        xl, xr_stem, xl, xr_stem, asc_h, cfg["H_lc"], cfg["H_br_lc"], cfg["taper_lc"],
        cfg["R_tip"], cfg["O_lc"], 0.0, pos="top", mode="left_only", slope=cfg["top_slope"],
    )
    return union_paths_to_glyph(p, [top_flag], gname)


# ---------------------------------------------------------------------------
# Per-Glyph Slab Sculpting Dispatcher
# ---------------------------------------------------------------------------
def build_sculpted_glyph(gname: str, sans_font: TTFont, sans_gset, cfg: dict) -> Glyph:
    if gname == "I":
        return build_unified_I(cfg)

    sans_g = sans_font["glyf"][gname]
    if gname == "l":
        return build_warm_hooked_l(sans_g, cfg, gname)

    segs = flatten_glyph_segments(sans_gset, gname)
    base_path = glyph_to_path(sans_gset, gname)
    addons = []

    H_cap, H_br_cap, taper_cap = cfg["H_cap"], cfg["H_br_cap"], cfg["taper_cap"]
    H_lc, H_br_lc, taper_lc = cfg["H_lc"], cfg["H_br_lc"], cfg["taper_lc"]
    R_tip, R_sm, slope = cfg["R_tip"], cfg["R_tip_sm"], cfg["top_slope"]
    O_cap, O_cap_in = cfg["O_cap"], cfg["O_cap_in"]
    O_lc, O_lc_in, O_m_in = cfg["O_lc"], cfg["O_lc_in"], cfg["O_m_in"]
    cap_h, asc_h, x_h, desc_y = cfg["cap_h"], cfg["asc_h"], cfg["x_h"], cfg["desc_y"]
    W_beak, L_beak, R_br_beak, flare_beak = cfg["W_beak"], cfg["L_beak"], cfg["R_br_beak"], cfg["flare_beak"]

    def add_stem_slab(y_tip, pos, span_idx, H, H_br, taper, r_t, ol, or_, mode, slp=0.0, dy_far=None):
        df = dy_far if dy_far is not None else min(H + H_br, 56.0)
        (xl0, xr0), (xli, xri) = measure_stem_trapezoid(segs, y_tip, pos, span_idx, dy_near=2.0, dy_far=df)
        addons.append(make_slab_path(xl0, xr0, xli, xri, y_tip, H, H_br, taper, r_t, ol, or_, pos=pos, mode=mode, slope=slp))

    # --- UPPERCASE ---
    if gname == "H":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap, H_br_cap, taper_cap, R_tip, O_cap_in, O_cap, "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(0, "base", 1, H_cap, H_br_cap, taper_cap, R_tip, O_cap_in, O_cap, "bilateral")

    elif gname == "M":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, int(O_cap * 0.56), "bilateral")
        add_stem_slab(cap_h, "top", -1, H_cap, H_br_cap, taper_cap, R_tip, int(O_cap * 0.56), O_cap, "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, int(O_cap * 0.62), "bilateral")
        add_stem_slab(0, "base", -1, H_cap, H_br_cap, taper_cap, R_tip, int(O_cap * 0.62), O_cap, "bilateral")

    elif gname == "N":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only")
        add_stem_slab(cap_h, "top", -1, H_cap, H_br_cap, taper_cap, R_tip, O_cap_in, O_cap, "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")

    elif gname == "U":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap, H_br_cap, taper_cap, R_tip, O_cap_in, O_cap, "bilateral")

    elif gname == "J":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")

    elif gname in ("B", "D"):
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)

    elif gname == "P":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")

    elif gname == "R":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(0, "base", -1, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, 0, cfg["O_diag_out"], "right_only")

    elif gname == "E":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        top_ys = slice_y_intervals(segs, sans_g.xMax - 12.0)
        # Top arm hanging beak, bottom arm rising beak
        addons.append(make_beak_path(sans_g.xMax, top_ys[-1][1], top_ys[-1][0], W_beak, L_beak, R_br_beak, R_sm, side="right", direction="down", flare=flare_beak))
        addons.append(make_beak_path(sans_g.xMax, top_ys[0][0], top_ys[0][1], W_beak, L_beak, R_br_beak, R_sm, side="right", direction="up", flare=flare_beak))
        # Sleek middle bar vertical cap (strictly filtered to middle y-band 200..550)
        mid_x = max(p[0] for p in sans_g.coordinates if 250 < p[1] < 500)
        mid_ys = [ys for ys in slice_y_intervals(segs, mid_x - 12.0) if 200 < 0.5 * (ys[0] + ys[1]) < 550]
        if mid_ys:
            yb_m, yt_m = mid_ys[0]
            addons.append(make_midbar_cap_path(mid_x, yb_m, yt_m, W_beak * 0.72, 14.0 if not cfg["is_bold"] else 16.0, 10.0, R_sm))

    elif gname == "F":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        top_ys = slice_y_intervals(segs, sans_g.xMax - 12.0)
        addons.append(make_beak_path(sans_g.xMax, top_ys[-1][1], top_ys[-1][0], W_beak, L_beak, R_br_beak, R_sm, side="right", direction="down", flare=flare_beak))

    elif gname == "L":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, 0, "left_only", dy_far=36.0)
        bot_ys = slice_y_intervals(segs, sans_g.xMax - 12.0)
        addons.append(make_beak_path(sans_g.xMax, bot_ys[0][0], bot_ys[0][1], W_beak, L_beak, R_br_beak, R_sm, side="right", direction="up", flare=flare_beak))

    elif gname == "T":
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap, "bilateral")
        arm_l_ys = slice_y_intervals(segs, sans_g.xMin + 12.0)
        arm_r_ys = slice_y_intervals(segs, sans_g.xMax - 12.0)
        addons.append(make_beak_path(sans_g.xMin, arm_l_ys[-1][1], arm_l_ys[-1][0], W_beak, L_beak, R_br_beak, R_sm, side="left", direction="down", flare=flare_beak))
        addons.append(make_beak_path(sans_g.xMax, arm_r_ys[-1][1], arm_r_ys[-1][0], W_beak, L_beak, R_br_beak, R_sm, side="right", direction="down", flare=flare_beak))

    elif gname in ("Z", "uni01B5"):
        pts = list(sans_g.coordinates)
        top_xs = sorted(p[0] for p in pts if p[1] >= cap_h - 6)
        bot_xs = sorted(p[0] for p in pts if p[1] <= 6)
        x_tl, x_br = float(top_xs[0]), float(bot_xs[-1])
        top_arm = slice_y_intervals(segs, x_tl + 12.0)[-1]
        bot_arm = slice_y_intervals(segs, x_br - 12.0)[0]
        addons.append(make_beak_path(x_tl, top_arm[1], top_arm[0], W_beak * 0.92, L_beak * 0.90, R_br_beak * 0.85, R_sm, side="left", direction="down", flare=flare_beak * 0.7))
        addons.append(make_beak_path(x_br, bot_arm[0], bot_arm[1], W_beak * 0.92, L_beak * 0.94, R_br_beak * 0.85, R_sm, side="right", direction="up", flare=flare_beak * 0.7))

    elif gname == "A":
        add_stem_slab(0, "base", 0, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_out"], cfg["O_diag_in"], "bilateral")
        add_stem_slab(0, "base", 1, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")

    elif gname == "K":
        add_stem_slab(cap_h, "top", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap_in, "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")
        add_stem_slab(0, "base", 1, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"] * 0.75, cfg["O_diag_out"], "bilateral")

    elif gname == "V":
        add_stem_slab(cap_h, "top", 0, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_out"], cfg["O_diag_in"], "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")

    elif gname == "W":
        o_arm_in = 18.0 if not cfg["is_bold"] else 14.0
        add_stem_slab(cap_h, "top", 0, H_cap * 0.90, H_br_cap * 0.78, taper_cap, R_sm, cfg["O_diag_out"], o_arm_in, "bilateral")
        if not cfg["is_bold"]:
            add_stem_slab(cap_h, "top", 1, H_cap * 0.86, H_br_cap * 0.65, taper_cap, R_sm, 16.0, 16.0, "bilateral")
        add_stem_slab(cap_h, "top", 2, H_cap * 0.90, H_br_cap * 0.78, taper_cap, R_sm, o_arm_in, cfg["O_diag_out"], "bilateral")

    elif gname == "X":
        add_stem_slab(cap_h, "top", 0, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_out"], cfg["O_diag_in"], "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")
        add_stem_slab(0, "base", 0, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_out"], cfg["O_diag_in"], "bilateral")
        add_stem_slab(0, "base", 1, H_cap * 0.92, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")

    elif gname == "Y":
        add_stem_slab(cap_h, "top", 0, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_out"], cfg["O_diag_in"], "bilateral")
        add_stem_slab(cap_h, "top", 1, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, cfg["O_diag_in"], cfg["O_diag_out"], "bilateral")
        add_stem_slab(0, "base", 0, H_cap, H_br_cap, taper_cap, R_tip, O_cap, O_cap, "bilateral")

    elif gname == "C":
        pts = list(sans_g.coordinates)
        pt_out = max([p for p in pts if p[0] > 450 and p[1] > 500], key=lambda p: p[0])
        pt_in = min([p for p in pts if p[0] > 450 and p[1] > 500], key=lambda p: p[1])
        drop_c = 68.0 if not cfg["is_bold"] else 72.0
        addons.append(make_upper_right_terminal_slab(pt_out, pt_in, sans_g.yMax, cfg["W_term"], drop_c, R_br_beak * 0.85, R_sm, flare=0.0))

    elif gname == "G":
        pts = list(sans_g.coordinates)
        pt_out = max([p for p in pts if p[0] > 450 and p[1] > 500], key=lambda p: p[0])
        pt_in = min([p for p in pts if p[0] > 450 and p[1] > 500], key=lambda p: p[1])
        drop_g = 68.0 if not cfg["is_bold"] else 72.0
        addons.append(make_upper_right_terminal_slab(pt_out, pt_in, sans_g.yMax, cfg["W_term"], drop_g, R_br_beak * 0.85, R_sm, flare=0.0))
        # Outward horizontal right_only shelf on the top-right edge of G's vertical spur (leaves counter open)
        bar_pts = [p for p in pts if p[0] >= sans_g.xMax - 6 and 280 < p[1] < 450]
        if bar_pts:
            y_bar_top = max(p[1] for p in bar_pts)
            x_bar_r = max(p[0] for p in bar_pts)
            g_spur_o = 34.0 if not cfg["is_bold"] else 38.0
            addons.append(make_slab_path(x_bar_r - 90.0, x_bar_r, x_bar_r - 90.0, x_bar_r, y_bar_top, H_cap * 0.78, H_br_cap * 0.65, taper_cap, R_sm, 0.0, g_spur_o, pos="top", mode="right_only"))

    elif gname == "S":
        pts = list(sans_g.coordinates)
        pt_out_tr = max([p for p in pts if p[0] > 380 and p[1] > 520], key=lambda p: p[0])
        pt_in_tr = min([p for p in pts if p[0] > 380 and p[1] > 520], key=lambda p: p[1])
        drop_s = 60.0 if not cfg["is_bold"] else 66.0
        addons.append(make_upper_right_terminal_slab(pt_out_tr, pt_in_tr, sans_g.yMax, cfg["W_term"], drop_s, R_br_beak * 0.80, R_sm, flare=0.0))

        x_min_bl = min(p[0] for p in pts if p[1] < 200)
        bl_edge = [p for p in pts if p[0] <= x_min_bl + 4 and p[1] < 220]
        pt_out_bl = min(bl_edge, key=lambda p: p[1])
        pt_in_bl = max(bl_edge, key=lambda p: p[1])
        rise_s = 64.0 if not cfg["is_bold"] else 68.0
        addons.append(make_lower_left_terminal_slab(pt_out_bl, pt_in_bl, sans_g.yMin, cfg["W_term"], rise_s, R_br_beak * 0.80, R_sm, flare=0.0))

    # --- LOWERCASE ---
    elif gname == "h":
        add_stem_slab(asc_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc_in, "bilateral")
        add_stem_slab(0, "base", 1, H_lc, H_br_lc, taper_lc, R_tip, O_lc_in, O_lc, "bilateral")

    elif gname == "k":
        add_stem_slab(asc_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc_in, "bilateral")
        add_stem_slab(x_h, "top", -1, H_lc * 0.92, H_br_lc * 0.8, taper_lc, R_sm, cfg["O_lc_diag_in"], cfg["O_lc_diag_out"], "bilateral")
        add_stem_slab(0, "base", 1, H_lc * 0.92, H_br_lc * 0.8, taper_lc, R_sm, cfg["O_lc_diag_in"] * 0.7, cfg["O_lc_diag_out"], "bilateral")

    elif gname == "m":
        add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_m_in, "bilateral")
        add_stem_slab(0, "base", 1, H_lc, H_br_lc, taper_lc, R_tip, O_m_in, O_m_in, "bilateral")
        add_stem_slab(0, "base", 2, H_lc, H_br_lc, taper_lc, R_tip, O_m_in, O_lc, "bilateral")

    elif gname == "n":
        add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc_in, "bilateral")
        add_stem_slab(0, "base", 1, H_lc, H_br_lc, taper_lc, R_tip, O_lc_in, O_lc, "bilateral")

    elif gname == "r":
        add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc, "bilateral")

    elif gname in ("dotlessi", "i"):
        # For 'i', sculpt contour 0 (stem) identically to dotlessi and keep dot centered above
        if gname == "dotlessi":
            add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
            add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc, "bilateral")
        else:
            # Handle 'i' via dotlessi + translated dot contour directly below
            pass

    elif gname in ("uni0237", "j"):
        if gname == "uni0237":
            add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
        else:
            pass

    elif gname == "b":
        add_stem_slab(asc_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
        add_stem_slab(0, "base", 0, H_lc * 0.94, H_br_lc * 0.85, taper_lc, R_sm, int(O_lc * 0.72), 0, "left_only", dy_far=36.0)

    elif gname == "d":
        add_stem_slab(asc_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope)
        add_stem_slab(0, "base", -1, H_lc * 0.94, H_br_lc * 0.85, taper_lc, R_sm, 0, O_lc, "right_only", dy_far=36.0)

    elif gname == "p":
        add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(desc_y, "descender", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, O_lc_in, "bilateral")

    elif gname == "q":
        # Top-right stays clean humanist round shoulder; bottom descender gets bilateral slab
        add_stem_slab(desc_y, "descender", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc_in, O_lc, "bilateral")

    elif gname == "u":
        add_stem_slab(x_h, "top", 0, H_lc, H_br_lc, taper_lc, R_tip, O_lc, 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(x_h, "top", 1, H_lc, H_br_lc, taper_lc, R_tip, int(O_lc * 0.70), 0, "left_only", slp=slope, dy_far=36.0)
        add_stem_slab(0, "base", -1, H_lc * 0.94, H_br_lc * 0.85, taper_lc, R_sm, 0, O_lc, "right_only", dy_far=36.0)

    elif gname == "a":
        # Tucked warm exit foot (NO sharp rectangular spike)
        add_stem_slab(0, "base", -1, H_lc * 0.88, H_br_lc * 0.8, taper_lc, R_sm, 0, 32.0 if not cfg["is_bold"] else 36.0, "right_only", dy_far=34.0)

    elif gname == "f":
        add_stem_slab(0, "base", 0, H_lc, H_br_lc, taper_lc, R_tip, 44.0 if not cfg["is_bold"] else 48.0, 46.0 if not cfg["is_bold"] else 50.0, "bilateral")

    elif gname == "v":
        add_stem_slab(x_h, "top", 0, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_out"], cfg["O_lc_diag_in"], "bilateral")
        add_stem_slab(x_h, "top", 1, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_in"], cfg["O_lc_diag_out"], "bilateral")

    elif gname == "w":
        o_arm_in = 14.0 if not cfg["is_bold"] else 10.0
        add_stem_slab(x_h, "top", 0, H_lc * 0.86, H_br_lc * 0.72, taper_lc, R_sm, cfg["O_lc_diag_out"], o_arm_in, "bilateral")
        if not cfg["is_bold"]:
            add_stem_slab(x_h, "top", 1, H_lc * 0.82, H_br_lc * 0.60, taper_lc, R_sm, 14.0, 14.0, "bilateral")
        add_stem_slab(x_h, "top", 2, H_lc * 0.86, H_br_lc * 0.72, taper_lc, R_sm, o_arm_in, cfg["O_lc_diag_out"], "bilateral")

    elif gname == "x":
        add_stem_slab(x_h, "top", 0, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_out"], cfg["O_lc_diag_in"], "bilateral")
        add_stem_slab(x_h, "top", 1, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_in"], cfg["O_lc_diag_out"], "bilateral")
        add_stem_slab(0, "base", 0, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_out"], cfg["O_lc_diag_in"], "bilateral")
        add_stem_slab(0, "base", 1, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_in"], cfg["O_lc_diag_out"], "bilateral")

    elif gname == "y":
        add_stem_slab(x_h, "top", 0, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_out"], cfg["O_lc_diag_in"], "bilateral")
        add_stem_slab(x_h, "top", 1, H_lc * 0.90, H_br_lc * 0.80, taper_lc, R_sm, cfg["O_lc_diag_in"], cfg["O_lc_diag_out"], "bilateral")

    elif gname in ("z", "uni01B6"):
        pts = list(sans_g.coordinates)
        top_xs = sorted(p[0] for p in pts if p[1] >= x_h - 6)
        bot_xs = sorted(p[0] for p in pts if p[1] <= 6)
        x_tl, x_br = float(top_xs[0]), float(bot_xs[-1])
        top_arm = slice_y_intervals(segs, x_tl + 12.0)[-1]
        bot_arm = slice_y_intervals(segs, x_br - 12.0)[0]
        addons.append(make_beak_path(x_tl, top_arm[1], top_arm[0], W_beak * 0.86, L_beak * 0.76, R_br_beak * 0.75, R_sm, side="left", direction="down", flare=flare_beak * 0.55))
        addons.append(make_beak_path(x_br, bot_arm[0], bot_arm[1], W_beak * 0.86, L_beak * 0.80, R_br_beak * 0.75, R_sm, side="right", direction="up", flare=flare_beak * 0.55))

    elif gname == "c":
        pts = list(sans_g.coordinates)
        pt_out = max([p for p in pts if p[0] > 320 and p[1] > 380], key=lambda p: p[0])
        pt_in = min([p for p in pts if p[0] > 320 and p[1] > 380], key=lambda p: p[1])
        drop_lc_c = 48.0 if not cfg["is_bold"] else 50.0
        addons.append(make_upper_right_terminal_slab(pt_out, pt_in, sans_g.yMax, cfg["W_term"] * 0.90, drop_lc_c, R_br_beak * 0.75, R_sm, flare=0.0))

    elif gname == "s":
        pts = list(sans_g.coordinates)
        pt_out_tr = max([p for p in pts if p[0] > 300 and p[1] > 380], key=lambda p: p[0])
        pt_in_tr = min([p for p in pts if p[0] > 300 and p[1] > 380], key=lambda p: p[1])
        drop_lc_s = 44.0 if not cfg["is_bold"] else 46.0
        addons.append(make_upper_right_terminal_slab(pt_out_tr, pt_in_tr, sans_g.yMax, cfg["W_term"] * 0.86, drop_lc_s, R_br_beak * 0.72, R_sm, flare=0.0))

        x_min_bl = min(p[0] for p in pts if p[1] < 200)
        bl_edge = [p for p in pts if p[0] <= x_min_bl + 4 and p[1] < 220]
        pt_out_bl = min(bl_edge, key=lambda p: p[1])
        pt_in_bl = max(bl_edge, key=lambda p: p[1])
        rise_lc_s = 46.0 if not cfg["is_bold"] else 48.0
        addons.append(make_lower_left_terminal_slab(pt_out_bl, pt_in_bl, sans_g.yMin, cfg["W_term"] * 0.86, rise_lc_s, R_br_beak * 0.72, R_sm, flare=0.0))

    # --- NUMERALS ---
    elif gname == "one":
        # Replace flat sans foot with sculpted Warm Humanist bracketed slab matching H & I
        (xl_s, xr_s), _ = measure_stem_trapezoid(segs, 250.0, "base", 0, dy_near=0.0, dy_far=40.0)
        clip_rect = pathops.Path()
        clip_rect.moveTo(-200, 140)
        clip_rect.lineTo(-200, 900)
        clip_rect.lineTo(1000, 900)
        clip_rect.lineTo(1000, 140)
        clip_rect.close()
        upper_one = pathops.Path()
        pathops.intersection([base_path], [clip_rect], upper_one.getPen())
        upper_one.simplify(clockwise=True)
        stem_ext = pathops.Path()
        stem_ext.moveTo(xl_s, 0)
        stem_ext.lineTo(xl_s, 160)
        stem_ext.lineTo(xr_s, 160)
        stem_ext.lineTo(xr_s, 0)
        stem_ext.close()
        foot_o = 86.0 if not cfg["is_bold"] else 94.0
        foot_slab = make_slab_path(
            xl_s, xr_s, xl_s, xr_s, 0, H_cap, H_br_cap, taper_cap,
            R_sm, foot_o, foot_o, pos="base", mode="bilateral",
        )
        return union_paths_to_glyph(upper_one, [stem_ext, foot_slab], gname)

    elif gname == "two":
        bot_ys = slice_y_intervals(segs, sans_g.xMax - 12.0)
        addons.append(make_beak_path(sans_g.xMax, bot_ys[0][0], bot_ys[0][1], W_beak * 0.90, L_beak * 0.86, R_br_beak * 0.85, R_sm, side="right", direction="up", flare=flare_beak * 0.6))

    elif gname == "four":
        add_stem_slab(0, "base", 0, H_cap * 0.94, H_br_cap * 0.85, taper_cap, R_sm, 42.0 if not cfg["is_bold"] else 44.0, 42.0 if not cfg["is_bold"] else 44.0, "bilateral")

    elif gname == "seven":
        top_ys = slice_y_intervals(segs, sans_g.xMin + 12.0)
        addons.append(make_beak_path(sans_g.xMin, top_ys[-1][1], top_ys[-1][0], W_beak * 0.90, L_beak * 0.88, R_br_beak * 0.85, R_sm, side="left", direction="down", flare=flare_beak * 0.6))
        add_stem_slab(0, "base", 0, H_cap * 0.90, H_br_cap * 0.80, taper_cap, R_sm, 34.0 if not cfg["is_bold"] else 38.0, 34.0 if not cfg["is_bold"] else 38.0, "bilateral")

    return union_paths_to_glyph(base_path, addons, gname)


# ---------------------------------------------------------------------------
# Optical Sidebearing Calibration
# ---------------------------------------------------------------------------
def apply_optical_sidebearings(gname: str, new_g: Glyph, sans_g: Glyph, sans_adv: int, cfg: dict) -> tuple[int, int]:
    """
    Shifts `new_g` horizontally for crisp optical sidebearings and returns `(new_adv, shift_x_from_sans)`.
    Preserves curved sans sidebearings on round sides while spacing slab tips accurately.
    """
    new_g.recalcBounds(None) if False else None
    # Calculate bounds directly from coordinates
    pts = list(new_g.coordinates)
    xMin = min(p[0] for p in pts)
    xMax = max(p[0] for p in pts)
    orig_lsb = sans_g.xMin
    orig_rsb = sans_adv - sans_g.xMax

    sb_stem = cfg["sb_stem"]
    sb_narrow = cfg["sb_narrow"]
    sb_diag = cfg["sb_diag"]
    sb_arm = cfg["sb_arm"]

    # Determine target LSB & RSB per anatomical class
    if gname in ("I",):
        target_lsb, target_rsb = sb_stem + 4, sb_stem + 4
    elif gname in ("H", "M", "N", "h", "k", "m", "n", "p"):
        target_lsb = sb_stem
        target_rsb = sb_diag if gname == "k" else sb_stem
    elif gname in ("dotlessi",):
        target_lsb, target_rsb = sb_narrow, sb_narrow
    elif gname in ("l",):
        target_lsb, target_rsb = sb_narrow, sb_diag + 4
    elif gname in ("uni0237",):
        # Preserve descender left overhang relative to stem
        target_lsb = orig_lsb
        target_rsb = sb_narrow
    elif gname in ("B", "D", "P", "b"):
        target_lsb = sb_stem
        target_rsb = orig_rsb
    elif gname in ("E", "L"):
        target_lsb, target_rsb = sb_stem, sb_arm
    elif gname in ("F", "K", "R"):
        target_lsb, target_rsb = sb_stem, sb_diag
    elif gname == "r":
        target_lsb = sb_stem
        target_rsb = 36 if not cfg["is_bold"] else 34
    elif gname in ("T", "Z", "uni01B5", "z", "uni01B6", "A", "V", "W", "X", "Y", "v", "w", "x", "y"):
        target_lsb, target_rsb = sb_diag, sb_diag
    elif gname in ("U",):
        target_lsb, target_rsb = sb_stem - 2, sb_stem - 2
    elif gname in ("J",):
        target_lsb, target_rsb = orig_lsb, sb_stem
    elif gname in ("C", "G", "S", "c", "s"):
        target_lsb = orig_lsb
        target_rsb = max(orig_rsb, sb_arm)
    elif gname in ("d", "q", "a"):
        target_lsb = orig_lsb
        target_rsb = sb_stem - 2 if gname != "a" else orig_rsb
    elif gname == "u":
        target_lsb, target_rsb = sb_stem - 4, sb_stem - 2
    elif gname == "f":
        # Tight right sidebearing relative to stem foot so f's upper hook naturally overhangs into vowels
        target_lsb = cfg["sb_f_left"]
        shift_x = target_lsb - xMin
        if shift_x != 0:
            new_g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in pts])
        # Compute foot xMax (points near y=0)
        foot_xmax = max(p[0] for p in new_g.coordinates if p[1] <= cfg["H_lc"] + 5)
        new_adv = max(int(foot_xmax + cfg["sb_f_right"]), int(max(p[0] for p in new_g.coordinates) - 34))
        return new_adv, int(shift_x)
    elif gname in ("one", "two", "four", "seven"):
        # Keep tabular/proportional digit width balanced
        shift_x = max(sb_diag, orig_lsb - 6) - xMin
        if gname == "one":
            # Center numeral 1 cleanly inside its original tabular advance width (or slightly expanded)
            new_w = xMax - xMin
            adv = max(sans_adv, int(new_w + 2 * sb_diag))
            shift_x = round((adv - new_w) * 0.5 - xMin)
            new_g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in pts])
            return adv, int(shift_x)
        new_g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in pts])
        new_xmax = xMax + shift_x
        return max(sans_adv, int(new_xmax + sb_diag)), int(shift_x)
    else:
        target_lsb, target_rsb = orig_lsb, orig_rsb

    shift_x = target_lsb - xMin
    if gname in ("I",):
        # I starts at O_I already, ensure clean symmetric padding
        shift_x = target_lsb - xMin
    if shift_x != 0:
        new_g.coordinates = GlyphCoordinates([(x + shift_x, y) for (x, y) in pts])
    new_xmax = xMax + shift_x
    new_adv = int(new_xmax + target_rsb)
    return new_adv, int(shift_x)


# ---------------------------------------------------------------------------
# Slab-Tailored GPOS Kerning Table
# ---------------------------------------------------------------------------
SLAB_KERN_PAIRS = {
    # Caps -> Caps
    ("A", "V"): -38, ("A", "W"): -30, ("A", "Y"): -46, ("A", "T"): -42,
    ("A", "C"): -16, ("A", "G"): -16, ("A", "O"): -18, ("A", "Q"): -18,
    ("F", "A"): -36, ("F", "J"): -28,
    ("K", "O"): -18, ("K", "C"): -18, ("K", "G"): -18, ("K", "Q"): -18,
    ("L", "T"): -42, ("L", "V"): -44, ("L", "W"): -34, ("L", "Y"): -52,
    ("P", "A"): -44, ("P", "J"): -22,
    ("R", "V"): -14, ("R", "W"): -10, ("R", "Y"): -20, ("R", "T"): -14,
    ("T", "A"): -42, ("T", "O"): -22, ("T", "C"): -22, ("T", "G"): -22, ("T", "Q"): -22,
    ("V", "A"): -38, ("V", "O"): -18, ("V", "C"): -16, ("V", "G"): -16,
    ("W", "A"): -30, ("W", "O"): -14, ("W", "C"): -12, ("W", "G"): -12,
    ("Y", "A"): -46, ("Y", "O"): -24, ("Y", "C"): -22, ("Y", "G"): -22,
    # Caps -> Lowercase
    ("F", "a"): -28, ("F", "e"): -26, ("F", "o"): -28, ("F", "c"): -24, ("F", "r"): -14, ("F", "s"): -18,
    ("K", "o"): -16, ("K", "e"): -14, ("K", "a"): -12, ("K", "u"): -10, ("K", "y"): -14,
    ("P", "a"): -24, ("P", "e"): -22, ("P", "o"): -22, ("P", "c"): -20,
    ("T", "a"): -36, ("T", "c"): -36, ("T", "e"): -38, ("T", "o"): -40, ("T", "r"): -28, ("T", "s"): -30, ("T", "u"): -28, ("T", "w"): -26, ("T", "y"): -26,
    ("V", "a"): -34, ("V", "c"): -32, ("V", "e"): -34, ("V", "o"): -34, ("V", "r"): -24, ("V", "s"): -26, ("V", "u"): -24,
    ("W", "a"): -28, ("W", "c"): -26, ("W", "e"): -28, ("W", "o"): -28, ("W", "r"): -18, ("W", "s"): -20, ("W", "u"): -18,
    ("Y", "a"): -40, ("Y", "c"): -38, ("Y", "e"): -40, ("Y", "o"): -42, ("Y", "r"): -30, ("Y", "s"): -32, ("Y", "u"): -30,
    # Lowercase -> Lowercase
    ("f", "a"): -16, ("f", "e"): -14, ("f", "o"): -16, ("f", "c"): -14, ("f", "d"): -12, ("f", "g"): -14,
    ("r", "a"): -16, ("r", "c"): -14, ("r", "d"): -16, ("r", "e"): -14, ("r", "g"): -14, ("r", "o"): -16, ("r", "q"): -16, ("r", "s"): -10,
    ("v", "a"): -20, ("v", "c"): -16, ("v", "e"): -18, ("v", "o"): -18, ("v", "s"): -12,
    ("w", "a"): -16, ("w", "c"): -14, ("w", "e"): -14, ("w", "o"): -16, ("w", "s"): -10,
    ("y", "a"): -22, ("y", "c"): -18, ("y", "e"): -20, ("y", "o"): -22, ("y", "s"): -14,
    ("k", "o"): -14, ("k", "e"): -12, ("k", "c"): -12,
    ("a", "v"): -14, ("a", "w"): -12, ("a", "y"): -14, ("e", "v"): -12, ("e", "y"): -14, ("o", "v"): -14, ("o", "x"): -14, ("o", "y"): -14,
    # Punctuation
    ("A", "period"): 0, ("F", "period"): -60, ("F", "comma"): -60,
    ("P", "period"): -72, ("P", "comma"): -72,
    ("T", "period"): -54, ("T", "comma"): -54,
    ("V", "period"): -56, ("V", "comma"): -56,
    ("W", "period"): -44, ("W", "comma"): -44,
    ("Y", "period"): -64, ("Y", "comma"): -64,
    ("r", "period"): -42, ("r", "comma"): -42,
    ("v", "period"): -44, ("v", "comma"): -44,
    ("w", "period"): -34, ("w", "comma"): -34,
    ("y", "period"): -48, ("y", "comma"): -48,
}


def build_slab_gpos_kern(font: TTFont, kern_scale: float) -> None:
    glyph_order = font.getGlyphOrder()
    glyph_set = set(glyph_order)
    gid_map = {gn: idx for idx, gn in enumerate(glyph_order)}

    grouped = {}
    for (g1, g2), val in SLAB_KERN_PAIRS.items():
        if g1 in glyph_set and g2 in glyph_set:
            sv = int(round(val * kern_scale))
            if sv != 0:
                grouped.setdefault(g1, []).append((g2, sv))

    first_sorted = sorted(grouped.keys(), key=lambda g: gid_map[g])
    pair_st = otTables.PairPos()
    pair_st.Format = 1
    pair_st.ValueFormat1 = 0x0004
    pair_st.ValueFormat2 = 0
    cov = otTables.Coverage()
    cov.glyphs = first_sorted
    pair_st.Coverage = cov

    pair_sets = []
    for g1 in first_sorted:
        pset = otTables.PairSet()
        pvrs = []
        for g2, sv in sorted(grouped[g1], key=lambda item: gid_map[item[0]]):
            pvr = otTables.PairValueRecord()
            pvr.SecondGlyph = g2
            vr = otBase.ValueRecord()
            vr.XAdvance = sv
            pvr.Value1 = vr
            pvr.Value2 = None
            pvrs.append(pvr)
        pset.PairValueRecord = pvrs
        pset.PairValueCount = len(pvrs)
        pair_sets.append(pset)

    pair_st.PairSet = pair_sets
    pair_st.PairSetCount = len(pair_sets)

    lkp = otTables.Lookup()
    lkp.LookupType = 2
    lkp.LookupFlag = 0
    lkp.SubTable = [pair_st]
    lkp.SubTableCount = 1

    gpos_tbl = otTables.GPOS()
    gpos_tbl.Version = 0x00010000

    lang_sys = otTables.LangSys()
    lang_sys.LookupOrder = None
    lang_sys.ReqFeatureIndex = 0xFFFF
    lang_sys.FeatureIndex = [0]
    lang_sys.FeatureCount = 1

    scripts = []
    for tag in ("DFLT", "latn"):
        sr = otTables.ScriptRecord()
        sr.ScriptTag = tag
        sr.Script = otTables.Script()
        sr.Script.DefaultLangSys = copy.deepcopy(lang_sys)
        sr.Script.LangSysRecord = []
        sr.Script.LangSysCount = 0
        scripts.append(sr)

    gpos_tbl.ScriptList = otTables.ScriptList()
    gpos_tbl.ScriptList.ScriptRecord = scripts
    gpos_tbl.ScriptList.ScriptCount = len(scripts)

    fr = otTables.FeatureRecord()
    fr.FeatureTag = "kern"
    fr.Feature = otTables.Feature()
    fr.Feature.FeatureParams = None
    fr.Feature.LookupListIndex = [0]
    fr.Feature.LookupCount = 1

    gpos_tbl.FeatureList = otTables.FeatureList()
    gpos_tbl.FeatureList.FeatureRecord = [fr]
    gpos_tbl.FeatureList.FeatureCount = 1

    gpos_tbl.LookupList = otTables.LookupList()
    gpos_tbl.LookupList.Lookup = [lkp]
    gpos_tbl.LookupList.LookupCount = 1

    wrapper = newTable("GPOS")
    wrapper.table = gpos_tbl
    font["GPOS"] = wrapper


# ---------------------------------------------------------------------------
# Main Compilation Pipeline
# ---------------------------------------------------------------------------
def compile_slab_cut(style_name: str, cfg: dict) -> None:
    sans_path = TTF_DIR / cfg["src_sans"]
    host_path = TTF_DIR / cfg["host_slab"]
    out_woff2 = WOFF2_DIR / f"{host_path.stem}.woff2"

    print(f"\n==================================================================")
    print(f"Sculpting Warm Humanist Slab: {host_path.stem} (from {sans_path.name})")
    print(f"==================================================================")

    sans_font = TTFont(str(sans_path))
    sans_gset = sans_font.getGlyphSet()
    sans_glyf = sans_font["glyf"]
    sans_hmtx = sans_font["hmtx"]

    font = TTFont(str(host_path))
    glyf = font["glyf"]
    hmtx = font["hmtx"]

    # Ensure Zero-VM bytecode posture
    for vm_tbl in ("fpgm", "cvt ", "prep"):
        if vm_tbl in font:
            del font[vm_tbl]

    sculpt_targets = [
        # Uppercase (24 serified; O & Q clean humanist bowls)
        "H", "I", "M", "N", "U", "J", "B", "D", "P", "R", "E", "F", "L", "T", "Z", "uni01B5",
        "A", "K", "V", "W", "X", "Y", "C", "G", "S",
        # Lowercase (23 serified; e, g, o clean humanist curves, t open humanist)
        "h", "k", "m", "n", "r", "dotlessi", "uni0237", "b", "d", "p", "q", "u", "a", "f",
        "l", "v", "w", "x", "y", "z", "uni01B6", "c", "s",
        # Numerals
        "one", "two", "four", "seven",
    ]

    # Map of base_gn -> (new_cx, sans_cx, new_adv, sans_adv)
    base_metrics_map = {}

    for gname in sculpt_targets:
        if gname not in sans_glyf or gname not in glyf:
            continue
        sans_g = sans_glyf[gname]
        sans_adv = sans_hmtx[gname][0]
        new_g = build_sculpted_glyph(gname, sans_font, sans_gset, cfg)
        new_adv, shift_x = apply_optical_sidebearings(gname, new_g, sans_g, sans_adv, cfg)
        new_g.recalcBounds(glyf)
        glyf[gname] = new_g
        hmtx[gname] = (new_adv, new_g.xMin)

        sans_cx = 0.5 * (sans_g.xMin + sans_g.xMax)
        new_cx = 0.5 * (new_g.xMin + new_g.xMax)
        base_metrics_map[gname] = (new_cx, sans_cx, new_adv, sans_adv)

    # Construct lowercase 'i' from sculpted 'dotlessi' + crisp centered dot from sans 'i'
    if "i" in sans_glyf and "dotlessi" in glyf:
        dot_g = sans_glyf["i"]
        stem_g = glyf["dotlessi"]
        dot_coords = list(dot_g.coordinates)[dot_g.endPtsOfContours[0] + 1 :]
        dot_flags = list(dot_g.flags)[dot_g.endPtsOfContours[0] + 1 :]
        sans_stem_cx = 0.5 * (sans_glyf["dotlessi"].xMin + sans_glyf["dotlessi"].xMax)
        stem_segs = flatten_glyph_segments(font.getGlyphSet(), "dotlessi")
        stem_spans = slice_x_intervals(stem_segs, 250.0)
        stem_axis_x = 0.5 * (stem_spans[0][0] + stem_spans[0][1]) if stem_spans else 0.5 * (stem_g.xMin + stem_g.xMax)
        dot_dx = round(stem_axis_x - sans_stem_cx)
        dot_shifted = [(x + dot_dx, y) for (x, y) in dot_coords]

        i_g = Glyph()
        i_g.numberOfContours = 2
        i_g.coordinates = GlyphCoordinates(list(stem_g.coordinates) + dot_shifted)
        i_g.flags = bytearray(list(stem_g.flags) + [fl & 0x3F for fl in dot_flags])
        i_g.endPtsOfContours = [
            len(stem_g.coordinates) - 1,
            len(stem_g.coordinates) + len(dot_shifted) - 1,
        ]
        clean_glyph_geometry(i_g)
        i_g.recalcBounds(glyf)
        glyf["i"] = i_g
        hmtx["i"] = hmtx["dotlessi"]
        base_metrics_map["i"] = (
            0.5 * (i_g.xMin + i_g.xMax),
            0.5 * (dot_g.xMin + dot_g.xMax),
            hmtx["i"][0],
            sans_hmtx["i"][0],
        )

    # Construct lowercase 'j' from sculpted 'uni0237' + centered dot from sans 'j'
    if "j" in sans_glyf and "uni0237" in glyf:
        j_sans = sans_glyf["j"]
        j_stem = glyf["uni0237"]
        dot_coords = list(j_sans.coordinates)[j_sans.endPtsOfContours[0] + 1 :]
        dot_flags = list(j_sans.flags)[j_sans.endPtsOfContours[0] + 1 :]
        j_new_spans = slice_x_intervals(flatten_glyph_segments(font.getGlyphSet(), "uni0237"), 250.0)
        j_old_spans = slice_x_intervals(flatten_glyph_segments(sans_gset, "uni0237"), 250.0)
        new_axis = 0.5 * (j_new_spans[0][0] + j_new_spans[0][1])
        old_axis = 0.5 * (j_old_spans[0][0] + j_old_spans[0][1])
        dot_dx = round(new_axis - old_axis)
        dot_shifted = [(x + dot_dx, y) for (x, y) in dot_coords]

        j_g = Glyph()
        j_g.numberOfContours = 2
        j_g.coordinates = GlyphCoordinates(list(j_stem.coordinates) + dot_shifted)
        j_g.flags = bytearray(list(j_stem.flags) + [fl & 0x3F for fl in dot_flags])
        j_g.endPtsOfContours = [
            len(j_stem.coordinates) - 1,
            len(j_stem.coordinates) + len(dot_shifted) - 1,
        ]
        clean_glyph_geometry(j_g)
        j_g.recalcBounds(glyf)
        glyf["j"] = j_g
        hmtx["j"] = hmtx["uni0237"]
        base_metrics_map["j"] = (
            0.5 * (j_g.xMin + j_g.xMax),
            0.5 * (j_sans.xMin + j_sans.xMax),
            hmtx["j"][0],
            sans_hmtx["j"][0],
        )

    # Sync GSUB alternates (`ss02` I, `cv05` hooked l, `cv09` / `ss07` heart-tittle i & j)
    gsub = font["GSUB"].table
    for fr in gsub.FeatureList.FeatureRecord:
        tag = fr.FeatureTag
        for li in fr.Feature.LookupListIndex:
            lkp = gsub.LookupList.Lookup[li]
            for st in lkp.SubTable:
                if not hasattr(st, "mapping"):
                    continue
                if tag == "ss02" and "I" in st.mapping:
                    alt_I = st.mapping["I"]
                    glyf[alt_I] = copy.deepcopy(glyf["I"])
                    hmtx[alt_I] = hmtx["I"]
                elif tag == "cv05" and "l" in st.mapping:
                    alt_l = st.mapping["l"]
                    glyf[alt_l] = copy.deepcopy(glyf["l"])
                    hmtx[alt_l] = hmtx["l"]
                elif tag in ("cv09", "ss07"):
                    for base_k, stem_k in (("i", "dotlessi"), ("j", "uni0237")):
                        if base_k in st.mapping and stem_k in glyf:
                            alt_gn = st.mapping[base_k]
                            alt_g = glyf[alt_gn]
                            if alt_g.numberOfContours >= 2:
                                stem_g = glyf[stem_k]
                                coords = list(alt_g.coordinates)
                                flags = list(alt_g.flags)
                                tittle_pts = coords[alt_g.endPtsOfContours[0] + 1 :]
                                tittle_flgs = flags[alt_g.endPtsOfContours[0] + 1 :]
                                # Center heart tittle horizontally over the vertical stem axis
                                s_spans = slice_x_intervals(flatten_glyph_segments(font.getGlyphSet(), stem_k), 250.0)
                                stem_axis = 0.5 * (s_spans[0][0] + s_spans[0][1])
                                t_xmin = min(p[0] for p in tittle_pts)
                                t_xmax = max(p[0] for p in tittle_pts)
                                t_dx = round(stem_axis - 0.5 * (t_xmin + t_xmax))
                                t_ymin = min(p[1] for p in tittle_pts)
                                min_t_y = cfg["x_h"] + 48
                                t_dy = max(0, min_t_y - t_ymin)
                                shifted_tittle = [(x + t_dx, y + t_dy) for (x, y) in tittle_pts]

                                new_alt = Glyph()
                                new_alt.numberOfContours = 2
                                new_alt.coordinates = GlyphCoordinates(list(stem_g.coordinates) + shifted_tittle)
                                new_alt.flags = bytearray(list(stem_g.flags) + [fl & 0x3F for fl in tittle_flgs])
                                new_alt.endPtsOfContours = [
                                    len(stem_g.coordinates) - 1,
                                    len(stem_g.coordinates) + len(shifted_tittle) - 1,
                                ]
                                clean_glyph_geometry(new_alt)
                                new_alt.recalcBounds(glyf)
                                glyf[alt_gn] = new_alt
                                hmtx[alt_gn] = hmtx[stem_k]

    # Rebuild ligatures `uniFB01` (fi) and `uniFB02` (fl) with crisp optical spacing
    f_adv = hmtx["f"][0]
    f_xmax = glyf["f"].xMax
    for lig_gn, comp2_gn in (("uniFB01", "i"), ("uniFB02", "l")):
        if lig_gn in glyf and glyf[lig_gn].isComposite():
            lg = glyf[lig_gn]
            c2_g = glyf[comp2_gn]
            # Place i/l so its tittle/ascender flag has crisp breathing room past f's hook
            min_clear_x = f_xmax + (14 if lig_gn == "uniFB01" else 20)
            desired_x = max(f_adv - 16, min_clear_x - c2_g.xMin)
            lg.components[0].x = 0
            lg.components[0].y = 0
            lg.components[1].x = int(round(desired_x))
            lg.components[1].y = 0
            lg.recalcBounds(glyf)
            hmtx[lig_gn] = (int(round(desired_x)) + hmtx[comp2_gn][0], lg.xMin)

    # Sync all Latin composite glyphs idempotently
    CENTERING_MARKS = {
        "acute", "grave", "circumflex", "caron", "tilde", "dotaccent",
        "dieresis", "uni02C9", "cedilla", "uni0326", "ring", "hungarumlaut",
        "breve", "macron",
    }
    for comp_gn in font.getGlyphOrder():
        if comp_gn in ("uniFB01", "uniFB02"):
            continue
        g = glyf[comp_gn]
        if not g.isComposite() or not g.components:
            continue
        base_gn = g.components[0].glyphName
        if base_gn not in base_metrics_map:
            continue

        new_cx, sans_cx, new_adv, sans_adv = base_metrics_map[base_gn]
        # Compute optical center over vertical body (use stem center for L/b/d/P/R/a or bbox center)
        if comp_gn in sans_glyf and sans_glyf[comp_gn].isComposite():
            # Reset verbatim from sans_donor, then translate diacritics cleanly
            sans_comp = sans_glyf[comp_gn]
            g.components = copy.deepcopy(sans_comp.components)
            shift_dx = round(new_cx - sans_cx)
            for comp in g.components[1:]:
                comp.x += shift_dx
            g.recalcBounds(glyf)
            hmtx[comp_gn] = (new_adv, g.xMin)
        else:
            # Host-only composite: center standard diacritics directly on new base center
            for comp in g.components[1:]:
                if comp.glyphName in CENTERING_MARKS and comp.glyphName in glyf:
                    mk = glyf[comp.glyphName]
                    mk_cx = 0.5 * (mk.xMin + mk.xMax)
                    comp.x = int(round(new_cx - mk_cx))
            g.recalcBounds(glyf)
            old_adv = hmtx[comp_gn][0]
            # Preserve extra advance width if a non-centering mark (e.g., uni0310) extends right
            if any(c.glyphName not in CENTERING_MARKS for c in g.components[1:]):
                hmtx[comp_gn] = (max(old_adv, new_adv), g.xMin)
            else:
                hmtx[comp_gn] = (new_adv, g.xMin)

    # Build tailored Warm Humanist Slab GPOS kern table
    build_slab_gpos_kern(font, cfg["kern_scale"])

    # Clean all modified glyphs & enforce bit-6/7 flag masking globally
    for gn in font.getGlyphOrder():
        gg = glyf[gn]
        if gg.numberOfContours > 0:
            gg.flags = bytearray([fl & 0x3F for fl in gg.flags])
            prog = ttProgram.Program()
            prog.fromBytecode(b"")
            gg.program = prog

    # Enforce v4.0.0 metadata, PKGL vendor ID, PANOSE Slab Serif classification
    font["head"].fontRevision = 4.0
    font["head"].macStyle = 0x0001 if cfg["is_bold"] else 0x0000
    os2 = font["OS/2"]
    os2.achVendID = "PKGL"
    os2.usWeightClass = cfg["weight_class"]
    os2.panose.bSerifStyle = 2  # Cove / Humanist Bracketed Serif (4 = Square Cove)
    os2.recalcAvgCharWidth(font)

    # Enforce 2-byte word alignment across all glyf/loca records
    font["glyf"].padding = 2
    font.save(str(host_path))
    font.close()
    sans_font.close()

    # Verify even byte size + even loca offsets
    raw_bytes = host_path.read_bytes()
    if len(raw_bytes) % 2 != 0:
        raise RuntimeError(f"{host_path.name} byte length {len(raw_bytes)} is odd!")
    chk = TTFont(str(host_path))
    odd_loca = [i for i, off in enumerate(chk["loca"].locations) if (off & 1) != 0]
    chk.close()
    if odd_loca:
        raise RuntimeError(f"{host_path.name} has {len(odd_loca)} odd loca offsets!")

    # Compress to WOFF2 (Brotli Q11)
    compress(str(host_path), str(out_woff2))

    # Sync mirrors
    if STAGE_DIR.exists():
        shutil.copy2(str(host_path), str(STAGE_DIR / host_path.name))
    if PUBLIC_DIR.exists():
        shutil.copy2(str(host_path), str(PUBLIC_DIR / host_path.name))
        shutil.copy2(str(out_woff2), str(PUBLIC_DIR / out_woff2.name))

    print(f"[SUCCESS] {host_path.name}: {len(raw_bytes):,} bytes (2-byte aligned, 0 odd loca)")
    print(f"[SUCCESS] {out_woff2.name}: {out_woff2.stat().st_size:,} bytes")


def update_slab_checksums() -> None:
    targets = [
        ("fonts/ttf/PocketGull-Slab-Bold.ttf", TTF_DIR / "PocketGull-Slab-Bold.ttf"),
        ("fonts/ttf/PocketGull-Slab-Regular.ttf", TTF_DIR / "PocketGull-Slab-Regular.ttf"),
        ("fonts/woff2/PocketGull-Slab-Bold.woff2", WOFF2_DIR / "PocketGull-Slab-Bold.woff2"),
        ("fonts/woff2/PocketGull-Slab-Regular.woff2", WOFF2_DIR / "PocketGull-Slab-Regular.woff2"),
    ]

    digests = {}
    for rel_key, fpath in targets:
        data = fpath.read_bytes()
        sha256_hex = hashlib.sha256(data).hexdigest()
        sha384_b64 = base64.b64encode(hashlib.sha384(data).digest()).decode("ascii")
        digests[rel_key] = {
            "size": len(data),
            "sha256": sha256_hex,
            "sri": f"sha384-{sha384_b64}",
        }

    # 1. fonts/sri-hashes.json
    sri_path = ROOT_DIR / "fonts" / "sri-hashes.json"
    if sri_path.exists():
        sri_data = json.loads(sri_path.read_text(encoding="utf-8"))
        for k, v in digests.items():
            sri_data[k] = v
        sri_path.write_text(json.dumps(sri_data, indent=2) + "\n", encoding="utf-8")

    # 2. fonts/SHA256SUMS
    sha_path = ROOT_DIR / "fonts" / "SHA256SUMS"
    if sha_path.exists():
        lines = sha_path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        for ln in lines:
            replaced = False
            for k, v in digests.items():
                if ln.endswith(" " + k):
                    new_lines.append(f"{v['sha256']}  {k}")
                    replaced = True
                    break
            if not replaced:
                new_lines.append(ln)
        sha_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # 3. CHECKSUMS.sha256
    chk_path = ROOT_DIR / "CHECKSUMS.sha256"
    if chk_path.exists():
        lines = chk_path.read_text(encoding="utf-8").splitlines()
        new_lines = []
        for ln in lines:
            replaced = False
            for k, v in digests.items():
                fname = Path(k).name
                if ln.endswith(" " + fname):
                    new_lines.append(f"{v['sha256']}  {fname}")
                    replaced = True
                    break
            if not replaced:
                new_lines.append(ln)
        chk_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print("[SUCCESS] Updated Slab entries in sri-hashes.json, SHA256SUMS, and CHECKSUMS.sha256")


def build_slab_superfamily() -> None:
    print("==================================================================")
    print("POCKETGULL TYPEFOUNDRY: WARM HUMANIST SLAB ENGINE (v4.0.0)")
    print("==================================================================")
    for style_name, cfg in DESIGN_PARAMS.items():
        compile_slab_cut(style_name, cfg)
    update_slab_checksums()
    print("\n[ALL DONE] PocketGull Slab Regular and Bold redesigned cleanly!")


if __name__ == "__main__":
    build_slab_superfamily()
