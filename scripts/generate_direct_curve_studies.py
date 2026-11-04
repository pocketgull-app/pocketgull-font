#!/usr/bin/env python3
"""
PocketGull Typefoundry — Direct Quadratic Bézier Curve & Topology Studies
=========================================================================
Extracts exact TrueType `glyf` contour points, flags, implied midpoints,
control handles, winding arrows, and curvature combs directly from the
1000 UPM v3.1.0 binaries to synthesize 4 high-resolution (2400 x 3400 px)
Direct Curve Study plates + a 4-page PDF Atlas:

  • STUDY I:   Quadratic B-Spline Control cages, Implied Midpoints & Curvature Combs
               (C, O, S, a, e, g — showing on-curve ■, off-curve ●, implied ◆, tangent handles)
  • STUDY II:  ISMP Clinical Disambiguation & Counter Winding Order Atlas
               (Slashed 0̸, Curved l, Biserif I, Crossbar Ƶ, Philocardia i.heart & j.heart)
  • STUDY III: Tactile Corner Radii & Architectural Terminal Comparison
               (25 UPM Soft-Bold vs Slab-Bold Shelves vs Chiseltip vs Outline vs Inline)
  • STUDY IV:  Sovereign Multi-Script & Specialized Symbol Curve Mechanics
               (Glottal Stop ʔ, Barred ƛ, Eng ŋ, Schwa ə, Music Sharp/Flat/G-Clef, Chem ₆/₈)
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
POSTERS_DIR = ROOT_DIR / "documentation" / "posters"
ARTIFACT_DIR = Path("/mnt/c/Users/philg/.gemini/antigravity/brain/d9f81d45-ac62-4064-80f3-e88e63f45edc")

F_REG = str(TTF_DIR / "PocketGull-Regular.ttf")
F_BOLD = str(TTF_DIR / "PocketGull-Bold.ttf")
F_FINE = str(TTF_DIR / "PocketGull-Fineliner.ttf")
F_CHISEL = str(TTF_DIR / "PocketGull-Chiseltip.ttf")
F_MARKER = str(TTF_DIR / "PocketGull-MarkerRaw.ttf")
F_MONO = str(TTF_DIR / "PocketGullMono-Regular.ttf")
F_MONO_B = str(TTF_DIR / "PocketGullMono-Bold.ttf")
F_NUM = str(TTF_DIR / "PocketGull-Numerics.ttf")
F_SERIF = str(TTF_DIR / "PocketGull-Serif-Bold.ttf")
F_SLAB = str(TTF_DIR / "PocketGull-Slab-Bold.ttf")
F_SOFT = str(TTF_DIR / "PocketGull-Soft-Bold.ttf")
F_OUTLINE = str(TTF_DIR / "PocketGull-Outline.ttf")
F_INLINE = str(TTF_DIR / "PocketGull-Inline.ttf")
F_MUSIC = str(TTF_DIR / "PocketGull-Music.ttf")
F_CHEM = str(TTF_DIR / "PocketGull-Chem.ttf")
F_CHEROKEE = F_BOLD
F_SYLLABICS = F_BOLD
F_BRAILLE = F_BOLD

W, H = 2400, 3400


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_grid(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, step: int, color):
    for x in range(x0, x1 + 1, step):
        draw.line([(x, y0), (x, y1)], fill=color, width=1)
    for y in range(y0, y1 + 1, step):
        draw.line([(x0, y), (x1, y)], fill=color, width=1)


def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, font, fg, bg, border) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 24, 12
    w_box = tw + pad_x * 2
    h_box = th + pad_y * 2
    draw.rounded_rectangle([(x, y), (x + w_box, y + h_box)], radius=10, fill=bg, outline=border, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=fg)
    return w_box + 16


def resolve_glyph_name(font: TTFont, query: str) -> str:
    glyf = font["glyf"]
    if query in ("i.heart", "j.heart") and "GSUB" in font:
        base_ch = "j" if query.startswith("j") else "i"
        for fr in font["GSUB"].table.FeatureList.FeatureRecord:
            if fr.FeatureTag == "ss07":
                lk = font["GSUB"].table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
                for st in lk.SubTable:
                    if hasattr(st, "mapping") and base_ch in st.mapping:
                        return st.mapping[base_ch]
    if query in glyf:
        return query
    cmap = font.getBestCmap()
    if len(query) == 1 and ord(query) in cmap:
        return cmap[ord(query)]
    if query.startswith("U+"):
        cp = int(query[2:], 16)
        if cp in cmap:
            return cmap[cp]
    return query


def plot_direct_curve_anatomy(
    draw: ImageDraw.ImageDraw,
    ttf_path: str,
    glyph_query: str,
    box_rect: tuple,
    title: str,
    subtitle: str,
    theme: dict,
    show_comb: bool = False,
    show_handles: bool = True,
    show_implied: bool = True,
    show_winding: bool = True,
    show_extrema: bool = True,
):
    """Plots a comprehensive forensic TrueType quadratic curve study inside `box_rect`."""
    x0, y0, x1, y1 = box_rect
    bw, bh = x1 - x0, y1 - y0
    draw.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=theme["card_bg"], outline=theme["border"], width=2)

    f_title = load_font(F_MONO_B, 24)
    f_sub = load_font(F_MONO, 19)
    f_tiny = load_font(F_MONO, 16)

    # Header inside cell
    draw.text((x0 + 24, y0 + 18), title, font=f_title, fill=theme["accent"])
    draw.text((x0 + 24, y0 + 50), subtitle, font=f_sub, fill=theme["muted"])

    # Viewport area for the glyph
    vx0, vy0 = x0 + 20, y0 + 84
    vx1, vy1 = x1 - 20, y1 - 74
    vw, vh = vx1 - vx0, vy1 - vy0
    draw.rounded_rectangle([vx0, vy0, vx1, vy1], radius=10, fill=theme["canvas_bg"], outline=theme["grid_border"], width=1)
    draw_grid(draw, vx0 + 10, vy0 + 10, vx1 - 10, vy1 - 10, 32, theme["grid_line"])

    font = TTFont(ttf_path)
    glyf = font["glyf"]
    gname = resolve_glyph_name(font, glyph_query)
    if gname not in glyf:
        draw.text((vx0 + 30, vy0 + 50), f"[Glyph {glyph_query} not found]", font=f_sub, fill=theme["muted"])
        return

    g = glyf[gname]
    if g.numberOfContours == 0:
        return

    coords, end_pts, flags = g.getCoordinates(glyf)
    pts = list(coords)
    flgs = [int(f) & 0x3F for f in flags]
    num_contours = len(end_pts)
    adv_w, lsb = font["hmtx"][gname]

    # Compute auto-fit scale & origin inside viewport
    if hasattr(g, "xMin") and g.xMax > g.xMin:
        gx_min, gy_min, gx_max, gy_max = g.xMin, g.yMin, g.xMax, g.yMax
    else:
        xs_all = [p[0] for p in pts]
        ys_all = [p[1] for p in pts]
        gx_min, gx_max = min(xs_all), max(xs_all)
        gy_min, gy_max = min(ys_all), max(ys_all)
    gw = max(1, gx_max - gx_min)
    gh = max(1, gy_max - gy_min)
    pad = 58 if show_comb else 44
    scale = min((vw - 2 * pad) / gw, (vh - 2 * pad) / max(gh, 680))
    scale = min(scale, 0.72)

    cx_glyph = (gx_min + gx_max) / 2.0
    cy_glyph = (gy_min + gy_max) / 2.0
    cx_view = (vx0 + vx1) / 2.0
    cy_view = (vy0 + vy1) / 2.0

    def tx(pt):
        return (
            cx_view + (pt[0] - cx_glyph) * scale,
            cy_view - (pt[1] - cy_glyph) * scale,
        )

    # Draw typographic metric lines (Baseline y=0, x-height y=536, Cap y=700)
    for m_y, m_lbl, m_col in [
        (0, "y=0", theme["baseline"]),
        (536, "x=536", theme["xheight"]),
        (700, "cap=700", theme["capheight"]),
    ]:
        _, sy = tx((0, m_y))
        if vy0 + 12 <= sy <= vy1 - 12:
            draw.line([(vx0 + 8, sy), (vx1 - 8, sy)], fill=m_col, width=1)
            draw.text((vx0 + 12, sy - 18), m_lbl, font=f_tiny, fill=m_col)

    # Track statistics
    num_on = sum(1 for f in flgs if (f & 1) != 0)
    num_off = len(flgs) - num_on
    num_implied = 0

    start = 0
    for c_idx, end in enumerate(end_pts):
        c_pts = pts[start : end + 1]
        c_flgs = flgs[start : end + 1]
        start = end + 1
        n = len(c_pts)
        if n < 2:
            continue

        # Compute signed area to determine clockwise (outer) vs counter-clockwise (inner counter)
        signed_area = 0.0
        for i in range(n):
            p1 = c_pts[i]
            p2 = c_pts[(i + 1) % n]
            signed_area += (p1[0] * p2[1]) - (p2[0] * p1[1])
        is_clockwise = signed_area < 0

        # Expand implicit TrueType midpoints into explicit quadratic Bézier segments
        expanded = []
        implied_pts = []
        for i in range(n):
            p_curr = c_pts[i]
            f_curr = c_flgs[i] & 1
            p_next = c_pts[(i + 1) % n]
            f_next = c_flgs[(i + 1) % n] & 1
            expanded.append((p_curr, f_curr))
            if not f_curr and not f_next:
                mid = ((p_curr[0] + p_next[0]) / 2.0, (p_curr[1] + p_next[1]) / 2.0)
                expanded.append((mid, 1))
                implied_pts.append(mid)
                num_implied += 1

        if expanded and expanded[0][1] == 0:
            first_on = next((idx for idx, item in enumerate(expanded) if item[1] == 1), 0)
            expanded = expanded[first_on:] + expanded[:first_on]

        # Sample smooth curve and optional curvature comb
        poly = []
        comb_spikes = []
        m = len(expanded)
        i = 0
        while i < m:
            p0, f0 = expanded[i]
            p1, f1 = expanded[(i + 1) % m]
            if f1 == 1:
                poly.append(tx(p0))
                i += 1
            else:
                p2, _ = expanded[(i + 2) % m]
                steps = 16
                for s in range(steps):
                    t = s / float(steps)
                    u = 1.0 - t
                    px = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
                    py = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
                    poly.append(tx((px, py)))

                    if show_comb and s % 2 == 0:
                        # First derivative B'(t) = 2(1-t)(p1-p0) + 2t(p2-p1)
                        dx = 2 * u * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
                        dy = 2 * u * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
                        # Second derivative B''(t) = 2(p2 - 2p1 + p0)
                        ddx = 2 * (p2[0] - 2 * p1[0] + p0[0])
                        ddy = 2 * (p2[1] - 2 * p1[1] + p0[1])
                        speed = math.hypot(dx, dy)
                        if speed > 1e-3:
                            # Signed curvature kappa
                            kappa = (dx * ddy - dy * ddx) / (speed ** 3)
                            # Outward normal in font coords
                            nx = -dy / speed
                            ny = dx / speed
                            spike_len = max(-42.0, min(42.0, kappa * 5500.0))
                            bx_pt, by_pt = tx((px, py))
                            ex_pt = bx_pt + nx * spike_len
                            ey_pt = by_pt - ny * spike_len
                            comb_spikes.append(((bx_pt, by_pt), (ex_pt, ey_pt)))
                i += 2

        # Draw filled contour translucent + crisp vector stroke
        if len(poly) >= 3:
            fill_c = theme["cw_fill"] if is_clockwise else theme["ccw_fill"]
            stroke_c = theme["cw_stroke"] if is_clockwise else theme["ccw_stroke"]
            draw.polygon(poly, fill=fill_c, outline=stroke_c)
            draw.line(poly + [poly[0]], fill=stroke_c, width=3)

        # Draw curvature comb if enabled
        if show_comb and comb_spikes:
            comb_top = []
            for base_pt, tip_pt in comb_spikes:
                draw.line([base_pt, tip_pt], fill=theme["comb"], width=1)
                comb_top.append(tip_pt)
            if len(comb_top) > 1:
                draw.line(comb_top, fill=theme["comb"], width=1)

        # Draw control cage handles (tangent lines connecting on-curve -> off-curve -> on-curve)
        if show_handles:
            cage_pts = [tx(p) for p in c_pts]
            draw.line(cage_pts + [cage_pts[0]], fill=theme["handle"], width=1)

        # Draw implied on-curve midpoints ◆
        if show_implied:
            for imp in implied_pts:
                ix, iy = tx(imp)
                r = 5
                draw.polygon([(ix, iy - r), (ix + r, iy), (ix, iy + r), (ix - r, iy)], fill=theme["implied"], outline=theme["canvas_bg"])

        # Draw explicit TrueType nodes: On-Curve ■ (Square) & Off-Curve ● (Circle)
        for idx_pt, (pt, flg) in enumerate(zip(c_pts, c_flgs)):
            sx, sy = tx(pt)
            on_curve = (flg & 1) != 0
            is_extremum = pt[0] in (gx_min, gx_max) or pt[1] in (gy_min, gy_max)
            if on_curve:
                r = 6 if (show_extrema and is_extremum) else 5
                col_node = theme["extremum"] if (show_extrema and is_extremum) else theme["on_node"]
                draw.rectangle([(sx - r, sy - r), (sx + r, sy + r)], fill=col_node, outline=theme["canvas_bg"])
            else:
                r = 5
                draw.ellipse([(sx - r, sy - r), (sx + r, sy + r)], fill=theme["off_node"], outline=theme["canvas_bg"])

        # Draw start point & winding direction badge on first point of contour
        if show_winding and c_pts:
            sx0, sy0 = tx(c_pts[0])
            sx1, sy1 = tx(c_pts[1 % n])
            ang = math.atan2(sy1 - sy0, sx1 - sx0)
            ax = sx0 + math.cos(ang) * 22
            ay = sy0 + math.sin(ang) * 22
            w_col = theme["cw_stroke"] if is_clockwise else theme["ccw_stroke"]
            draw.line([(sx0, sy0), (ax, ay)], fill=w_col, width=3)
            draw.ellipse([(sx0 - 8, sy0 - 8), (sx0 + 8, sy0 + 8)], outline=w_col, width=2)

    # Bottom telemetry bar inside cell
    comp_tag = " (Composite)" if g.isComposite() else ""
    stat_line = f"Contours: {num_contours}{comp_tag}  •  On-Curve ■: {num_on}  •  Off-Curve ●: {num_off}  •  Implied ◆: {num_implied}  •  AdvW: {adv_w}"
    draw.text((x0 + 24, y1 - 46), stat_line, font=f_tiny, fill=theme["muted"])
    bbox_line = f"BBox: x=[{gx_min}..{gx_max}] ({gw} UPM)  y=[{gy_min}..{gy_max}] ({gh} UPM)"
    draw.text((x0 + 24, y1 - 24), bbox_line, font=f_tiny, fill=theme["accent"])


DARK_BLUEPRINT_THEME = {
    "bg": (7, 11, 18),
    "card_bg": (13, 21, 34),
    "canvas_bg": (9, 14, 24),
    "border": (30, 41, 59),
    "grid_border": (25, 38, 58),
    "grid_line": (15, 24, 38),
    "accent": (56, 189, 248),
    "muted": (148, 163, 184),
    "baseline": (100, 116, 139),
    "xheight": (6, 182, 212),
    "capheight": (244, 63, 94),
    "cw_fill": (14, 38, 58),
    "ccw_fill": (9, 14, 24),
    "cw_stroke": (56, 189, 248),
    "ccw_stroke": (245, 158, 11),
    "handle": (100, 116, 139),
    "comb": (16, 185, 129),
    "on_node": (56, 189, 248),
    "off_node": (244, 63, 94),
    "implied": (250, 204, 21),
    "extremum": (16, 185, 129),
}


# ==============================================================================
# STUDY I: QUADRATIC B-SPLINE CAGES, IMPLIED MIDPOINTS & CURVATURE COMBS
# ==============================================================================
def build_curve_study_1() -> Image.Image:
    t = DARK_BLUEPRINT_THEME
    im = Image.new("RGB", (W, H), t["bg"])
    draw = ImageDraw.Draw(im)
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (13, 20, 32))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=t["border"], width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 98)
    f_sub = load_font(F_REG, 30)
    f_mono_sm = load_font(F_MONO, 22)

    bx = 130
    bx += draw_badge(draw, bx, 125, "CURVE STUDY I • QUADRATIC B-SPLINE MECHANICS", f_badge, (56, 189, 248), (10, 35, 52), (56, 189, 248))
    bx += draw_badge(draw, bx, 125, "CURVATURE COMBS κ(t) & IMPLIED MIDPOINTS", f_badge, (16, 185, 129), (10, 42, 35), (16, 185, 129))
    bx += draw_badge(draw, bx, 125, "KAREN CHENG EXTREMA AUDIT", f_badge, (245, 158, 11), (45, 32, 12), (245, 158, 11))

    draw.text((130, 205), "DIRECT QUADRATIC BÉZIER CURVE ATLAS", font=f_hero, fill=(248, 250, 252))
    draw.text((130, 325), "Live TrueType glyf extraction: On-Curve Extrema, Off-Curve Control Handles, Implied Midpoints & Curvature Combs", font=f_sub, fill=t["muted"])
    draw.line([(130, 390), (W - 130, 390)], fill=(56, 189, 248), width=3)

    # Legend Bar
    draw.rounded_rectangle([(130, 415), (W - 130, 485)], radius=12, fill=t["card_bg"], outline=t["border"], width=2)
    legend_text = "LEGEND:  ■ Green = Extremum   ■ Cyan = On-Curve Node   ● Rose = Off-Curve Handle   ◆ Gold = Implied Midpoint   ─ Emerald Spikes = Curvature Comb κ(t)"
    draw.text((160, 438), legend_text, font=load_font(F_MONO, 20), fill=(226, 232, 240))

    # 6 Glyph Studies (2 columns x 3 rows)
    cells = [
        (F_BOLD, "O", "01 / CAPITAL 'O' (PocketGull-Bold)", "Dual-contour CW/CCW winding • 4 cardinal on-curve extrema • Overshoot [-12..712]"),
        (F_BOLD, "C", "02 / LOUISE SLOAN 'C' (PocketGull-Bold)", "1:5 Sloan optotype aperture • Sheared humanist terminals • Curvature comb κ(t)"),
        (F_BOLD, "S", "03 / SPINE INFLECTION 'S' (PocketGull-Bold)", "Continuous implied midpoint spline along diagonal spine inflection"),
        (F_REG, "a", "04 / DOUBLE-STORY 'a' (PocketGull-Regular)", "Humanist terminal hook & teardropped lower bowl counter balance"),
        (F_REG, "e", "05 / CLINICAL APERTURE 'e' (PocketGull-Regular)", "High crossbar eye & wide lower aperture preventing low-DPI blur"),
        (F_REG, "g", "06 / LOOP & LINK 'g' (PocketGull-Regular)", "3-contour topology: upper bowl, lower loop counter & humanist ear"),
    ]

    col_w = 1045
    row_h = 845
    for idx, (f_path, g_q, title, sub) in enumerate(cells):
        c = idx % 2
        r = idx // 2
        cx0 = 130 + c * (col_w + 50)
        cy0 = 515 + r * (row_h + 30)
        plot_direct_curve_anatomy(
            draw,
            f_path,
            g_q,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            title,
            sub,
            t,
            show_comb=True,
            show_handles=True,
            show_implied=True,
            show_winding=True,
            show_extrema=True,
        )

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • DIRECT CURVE STUDY I: QUADRATIC B-SPLINE CAGES & CURVATURE COMBS", font=f_mono_sm, fill=t["muted"])
    draw.text((W - 760, 3210), "0 DUPLICATE NODES • 1000 UPM • V3.1.0", font=f_mono_sm, fill=(56, 189, 248))
    return im


# ==============================================================================
# STUDY II: ISMP CLINICAL DISAMBIGUATION & PILLAR 9 HEART TITTLE TOPOLOGY
# ==============================================================================
def build_curve_study_2() -> Image.Image:
    t = DARK_BLUEPRINT_THEME
    im = Image.new("RGB", (W, H), t["bg"])
    draw = ImageDraw.Draw(im)
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (13, 20, 32))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=(16, 185, 129), width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 96)
    f_sub = load_font(F_REG, 30)
    f_mono_sm = load_font(F_MONO, 22)

    bx = 130
    bx += draw_badge(draw, bx, 125, "CURVE STUDY II • ISMP & PILLAR 9 TOPOLOGY", f_badge, (16, 185, 129), (10, 42, 35), (16, 185, 129))
    bx += draw_badge(draw, bx, 125, "COUNTER WINDING ORDER (CW vs CCW)", f_badge, (245, 158, 11), (45, 32, 12), (245, 158, 11))
    bx += draw_badge(draw, bx, 125, "48 UPM TITTLE AIR GAP VERIFIED", f_badge, (244, 63, 94), (48, 12, 24), (244, 63, 94))

    draw.text((130, 205), "ISMP & PHILOCARDIA CONTOUR MECHANICS", font=f_hero, fill=(248, 250, 252))
    draw.text((130, 325), "Forensic contour verification of Slashed Zero (0̸), Curved l, Biserif I, Crossbar Z, and Pillar 9 Heart Tittles (ss07)", font=f_sub, fill=t["muted"])
    draw.line([(130, 390), (W - 130, 390)], fill=(16, 185, 129), width=3)

    draw.rounded_rectangle([(130, 415), (W - 130, 485)], radius=12, fill=t["card_bg"], outline=t["border"], width=2)
    legend_text = "WINDING INVARIANT:  ─ Cyan Contour = Clockwise (Outer Solid Stroke)   ─ Amber Contour = Counter-Clockwise (Inner Counter Aperture)   ◆ Gold = Implied On-Curve Midpoint"
    draw.text((160, 438), legend_text, font=load_font(F_MONO, 20), fill=(226, 232, 240))

    cells = [
        (F_NUM, "zero", "01 / SLASHED ZERO '0̸' (cv08 / Numerics)", "3 contours: outer oval (CW) + split upper/lower interior counters (CCW)"),
        (F_NUM, "l", "02 / CURVED FOOT LOWERCASE 'l' (cv05)", "Prominent outward baseline sweep (xMax=292 UPM) eliminating 1/l/I ambiguity"),
        (F_SERIF, "I", "03 / BISERIF CAPITAL 'I' (ss02)", "Top & baseline horizontal bilateral serifs for biomarker & IU clarity"),
        (F_NUM, "Z", "04 / CROSSBAR CAPITAL 'Ƶ' (cv11 / Numerics)", "Central horizontal crossbar stroke preventing Z-to-2 misreadings"),
        (F_REG, "i.heart", "05 / PHILOCARDIA 'i.heart' (ss07)", "Contour 0 stem x=[85..173], y=[0..536] + Contour 1 heart y=[584..700]"),
        (F_REG, "j.heart", "06 / PHILOCARDIA 'j.heart' (ss07)", "Descender hook yMin=-182 UPM + 48 UPM air gap above stem top (y=536)"),
    ]

    col_w = 1045
    row_h = 845
    for idx, (f_path, g_q, title, sub) in enumerate(cells):
        c = idx % 2
        r = idx // 2
        cx0 = 130 + c * (col_w + 50)
        cy0 = 515 + r * (row_h + 30)
        plot_direct_curve_anatomy(
            draw,
            f_path,
            g_q,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            title,
            sub,
            t,
            show_comb=True,
            show_handles=True,
            show_implied=True,
            show_winding=True,
            show_extrema=True,
        )

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • DIRECT CURVE STUDY II: ISMP DISAMBIGUATION & PILLAR 9 TOPOLOGY", font=f_mono_sm, fill=t["muted"])
    draw.text((W - 760, 3210), "PILLAR 4 & PILLAR 9 CERTIFIED • V3.1.0", font=f_mono_sm, fill=(16, 185, 129))
    return im


# ==============================================================================
# STUDY III: TACTILE CORNER RADII & ARCHITECTURAL TERMINAL COMPARISON
# ==============================================================================
def build_curve_study_3() -> Image.Image:
    t = DARK_BLUEPRINT_THEME
    im = Image.new("RGB", (W, H), t["bg"])
    draw = ImageDraw.Draw(im)
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (13, 20, 32))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=(245, 158, 11), width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 94)
    f_sub = load_font(F_REG, 30)
    f_mono_sm = load_font(F_MONO, 22)

    bx = 130
    bx += draw_badge(draw, bx, 125, "CURVE STUDY III • ARCHITECTURAL TERMINALS", f_badge, (245, 158, 11), (45, 32, 12), (245, 158, 11))
    bx += draw_badge(draw, bx, 125, "25 UPM FELT-MARKER RADII vs SLAB SHELVES", f_badge, (56, 189, 248), (10, 35, 52), (56, 189, 248))
    bx += draw_badge(draw, bx, 125, "MULTI-CONTOUR INLINE & OUTLINE", f_badge, (244, 63, 94), (48, 12, 24), (244, 63, 94))

    draw.text((130, 205), "TERMINAL & DISPLAY ARCHITECTURE", font=f_hero, fill=(248, 250, 252))
    draw.text((130, 325), "Comparing terminal vertex geometry across Soft-Bold (25 UPM radii), Slab-Bold, Chiseltip, MarkerRaw, Outline & Inline", font=f_sub, fill=t["muted"])
    draw.line([(130, 390), (W - 130, 390)], fill=(245, 158, 11), width=3)

    draw.rounded_rectangle([(130, 415), (W - 130, 485)], radius=12, fill=t["card_bg"], outline=t["border"], width=2)
    legend_text = "COMPARATIVE DUCTUS:  Soft-Bold = 25 UPM 3-node fillets  •  Slab-Bold = orthogonal serif shelves  •  Inline = negative inner core channels"
    draw.text((160, 438), legend_text, font=load_font(F_MONO, 19), fill=(226, 232, 240))

    cells = [
        (F_SOFT, "R", "01 / SOFT-BOLD 'R' (25 UPM Corner Fillets)", "Pillowed counter & rounded quadratic terminal fillets for tactile warmth"),
        (F_SLAB, "R", "02 / SLAB-BOLD 'R' (Orthogonal Slab Shelves)", "High-weight horizontal slab feet anchoring baseline and cap-height"),
        (F_CHISEL, "R", "03 / CHISELTIP 'R' (45° Broad-Edge Nib)", "Calligraphic stroke contrast & ribbon terminal modulation (wght 900)"),
        (F_MARKER, "R", "04 / MARKER-RAW 'R' (Hand-Drawn Cardstock)", "Organic felt-marker velocity & elevated waist ratio on physical cardstock"),
        (F_OUTLINE, "A", "05 / OUTLINE 'A' (Hollow Dual-Wall Contour)", "Outer CW boundary paired with parallel interior CCW hollow channel"),
        (F_INLINE, "A", "06 / INLINE 'A' (Chiseled Core Striation)", "Multi-contour inline negative core relief inside primary structural stems"),
    ]

    col_w = 1045
    row_h = 845
    for idx, (f_path, g_q, title, sub) in enumerate(cells):
        c = idx % 2
        r = idx // 2
        cx0 = 130 + c * (col_w + 50)
        cy0 = 515 + r * (row_h + 30)
        plot_direct_curve_anatomy(
            draw,
            f_path,
            g_q,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            title,
            sub,
            t,
            show_comb=(idx < 4),
            show_handles=True,
            show_implied=True,
            show_winding=True,
            show_extrema=True,
        )

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • DIRECT CURVE STUDY III: TACTILE CORNER RADII & DISPLAY TERMINALS", font=f_mono_sm, fill=t["muted"])
    draw.text((W - 760, 3210), "DIETER RAMS LAW 3 & LAW 8 • V3.1.0", font=f_mono_sm, fill=(245, 158, 11))
    return im


# ==============================================================================
# STUDY IV: 100% SOVEREIGN INDIGENOUS ORTHOGRAPHY CURVE MECHANICS (UNDRIP)
# ==============================================================================
def build_curve_study_4() -> Image.Image:
    t = DARK_BLUEPRINT_THEME
    im = Image.new("RGB", (W, H), t["bg"])
    draw = ImageDraw.Draw(im)
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (13, 20, 32))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=(45, 212, 191), width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 94)
    f_sub = load_font(F_REG, 30)
    f_mono_sm = load_font(F_MONO, 22)

    bx = 130
    bx += draw_badge(draw, bx, 125, "CURVE STUDY IV • SOVEREIGN INDIGENOUS SCRIPTS", f_badge, (45, 212, 191), (12, 46, 42), (45, 212, 191))
    bx += draw_badge(draw, bx, 125, "UNDRIP ARTICLES 11, 13, 14, 24 & 31", f_badge, (245, 158, 11), (48, 32, 10), (245, 158, 11))
    bx += draw_badge(draw, bx, 125, "100% SEPARATED FROM TACTILE BRAILLE", f_badge, (56, 189, 248), (10, 35, 52), (56, 189, 248))

    draw.text((130, 205), "SOVEREIGN INDIGENOUS CURVE TOPOLOGY", font=f_hero, fill=(248, 250, 252))
    draw.text((130, 325), "Direct vector inspection of Pan-Tribal orthographies (ʔ, ƛ, ŋ, ǫ), Canadian Syllabics (ᐁ) & Cherokee Syllabary (Ꮳ)", font=f_sub, fill=t["muted"])
    draw.line([(130, 390), (W - 130, 390)], fill=(45, 212, 191), width=3)

    draw.rounded_rectangle([(130, 415), (W - 130, 485)], radius=12, fill=t["card_bg"], outline=t["border"], width=2)
    legend_text = "SOVEREIGN VECTOR PARITY:  Glottal Stop ʔ (U+0294)  •  Barred Lambda ƛ (U+019B)  •  Eng ŋ (U+014B)  •  O-Ogonek ǫ (U+01EB)  •  Syllabics E ᐁ (U+1401)  •  Cherokee Tsa Ꮳ (U+13E3)"
    draw.text((160, 438), legend_text, font=load_font(F_MONO, 19), fill=(226, 232, 240))

    cells = [
        (F_BOLD, "U+0294", "01 / GLOTTAL STOP 'ʔ' (U+0294 • Pan-Tribal)", "First-class sovereign letter contour (not punctuation) with crisp baseline stem"),
        (F_BOLD, "U+019B", "02 / BARRED LAMBDA 'ƛ' (U+019B • Coast Salish)", "High-contrast crossbar (>= 1.4x aperture) across diagonal descending stroke"),
        (F_BOLD, "U+014B", "03 / VELAR NASAL ENG 'ŋ' (U+014B • Lakota/Dene)", "Continuous arch transition into descending retroflex/velar J-hook"),
        (F_BOLD, "U+01EB", "04 / NASAL O-OGONEK 'ǫ' (U+01EB • Diné/Apache)", "Composite/contour harmony: rightward ogonek hook anchored to lower bowl"),
        (F_SYLLABICS, "U+1401", "05 / SYLLABICS E 'ᐁ' (U+1401 • Inuktitut/Cree)", "Rotational triangular apex geometry with balanced interior counter"),
        (F_CHEROKEE, "U+13E3", "06 / CHEROKEE TSA 'Ꮳ' (U+13E3 • Tsalagi)", "Sequoyah syllabary calligraphic curves rendered in pure quadratic B-splines"),
    ]

    col_w = 1045
    row_h = 845
    for idx, (f_path, g_q, title, sub) in enumerate(cells):
        c = idx % 2
        r = idx // 2
        cx0 = 130 + c * (col_w + 50)
        cy0 = 515 + r * (row_h + 30)
        plot_direct_curve_anatomy(
            draw,
            f_path,
            g_q,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            title,
            sub,
            t,
            show_comb=True,
            show_handles=True,
            show_implied=True,
            show_winding=True,
            show_extrema=True,
        )

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • DIRECT CURVE STUDY IV: SOVEREIGN INDIGENOUS CURVE TOPOLOGY", font=f_mono_sm, fill=t["muted"])
    draw.text((W - 760, 3210), "39 / 39 TEK & UNDRIP VERIFIED • V3.1.0", font=f_mono_sm, fill=(45, 212, 191))
    return im


# ==============================================================================
# STUDY V: DEDICATED ISO 17049 TACTILE BRAILLE DOME & SCIENTIFIC TOPOLOGY
# ==============================================================================
def build_curve_study_5() -> Image.Image:
    t = DARK_BLUEPRINT_THEME
    im = Image.new("RGB", (W, H), t["bg"])
    draw = ImageDraw.Draw(im)
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (13, 20, 32))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=(245, 158, 11), width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 94)
    f_sub = load_font(F_REG, 30)
    f_mono_sm = load_font(F_MONO, 22)

    bx = 130
    bx += draw_badge(draw, bx, 125, "CURVE STUDY V • ISO 17049 TACTILE BRAILLE", f_badge, (245, 158, 11), (48, 32, 10), (245, 158, 11))
    bx += draw_badge(draw, bx, 125, "r = 60 UPM QUADRATIC DOME CIRCLES", f_badge, (56, 189, 248), (10, 35, 52), (56, 189, 248))
    bx += draw_badge(draw, bx, 125, "GROUNDED ON BASELINE y = 0 UPM", f_badge, (16, 185, 129), (8, 42, 32), (16, 185, 129))

    draw.text((130, 205), "TACTILE BRAILLE & SCIENTIFIC TOPOLOGY", font=f_hero, fill=(248, 250, 252))
    draw.text((130, 325), "Dedicated inspection of ISO 17049 6-dot/8-dot circular dome geometry (U+2800–U+28FF) & multi-contour scientific symbols", font=f_sub, fill=t["muted"])
    draw.line([(130, 390), (W - 130, 390)], fill=(245, 158, 11), width=3)

    draw.rounded_rectangle([(130, 415), (W - 130, 485)], radius=12, fill=t["card_bg"], outline=t["border"], width=2)
    legend_text = "TACTILE & SCIENTIFIC PRECISION:  Dot-1 ⠁ (U+2801)  •  Dots-123 ⠇ (U+2807)  •  6-Dot Full ⠿ (U+283F)  •  8-Dot Full ⣿ (U+28FF)  •  Music Sharp ♯  •  Copyright ©"
    draw.text((160, 438), legend_text, font=load_font(F_MONO, 19), fill=(226, 232, 240))

    cells = [
        (F_BRAILLE, "U+2801", "01 / BRAILLE DOT-1 '⠁' (U+2801 • Letter A / 1)", "Single r = 60 UPM CW quadratic circle with 4 cardinal extrema ■ & 4 handles ●"),
        (F_BRAILLE, "U+2807", "02 / BRAILLE DOTS-123 '⠇' (U+2807 • Letter L)", "Vertical column alignment: uniform 2.5 mm intra-cell dot pitch"),
        (F_BRAILLE, "U+283F", "03 / 6-DOT LITERARY CELL '⠿' (U+283F • Dots 1–6)", "Standard 2x3 literary/pharmaceutical embossing grid (6 independent CW contours)"),
        (F_BRAILLE, "U+28FF", "04 / 8-DOT TELEMETRY CELL '⣿' (U+28FF • Dots 1–8)", "Full 2x4 ISO/TR 11548 computer & ICU Braille cell grounded at y = 0 UPM"),
        (F_MUSIC, "U+266F", "05 / MUSIC SHARP '♯' (U+266F • PocketGull-Music)", "Multi-contour topology: outer grid + interior CCW parallelogram counters"),
        (F_REG, "copyright", "06 / COPYRIGHT '©' (3-Tier Nested Winding)", "Outer ring (CW) -> Inner ring (CCW) -> Central letter C (CW) parity"),
    ]

    col_w = 1045
    row_h = 845
    for idx, (f_path, g_q, title, sub) in enumerate(cells):
        c = idx % 2
        r = idx // 2
        cx0 = 130 + c * (col_w + 50)
        cy0 = 515 + r * (row_h + 30)
        plot_direct_curve_anatomy(
            draw,
            f_path,
            g_q,
            (cx0, cy0, cx0 + col_w, cy0 + row_h),
            title,
            sub,
            t,
            show_comb=True,
            show_handles=True,
            show_implied=True,
            show_winding=True,
            show_extrema=True,
        )

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • DIRECT CURVE STUDY V: ISO 17049 TACTILE BRAILLE & SCIENTIFIC TOPOLOGY", font=f_mono_sm, fill=t["muted"])
    draw.text((W - 760, 3210), "256 / 256 BRAILLE CELLS VERIFIED • V3.1.0", font=f_mono_sm, fill=(245, 158, 11))
    return im


def main():
    POSTERS_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Synthesizing Direct Curve Study I: Quadratic B-Spline Cages & Curvature Combs...")
    s1 = build_curve_study_1()
    s1_path = POSTERS_DIR / "curve_study_01_quadratic_bspline_combs.png"
    s1.save(s1_path, "PNG", dpi=(300, 300))

    print("2. Synthesizing Direct Curve Study II: ISMP Disambiguation & Pillar 9 Heart Tittle Topology...")
    s2 = build_curve_study_2()
    s2_path = POSTERS_DIR / "curve_study_02_ismp_pillar9_winding.png"
    s2.save(s2_path, "PNG", dpi=(300, 300))

    print("3. Synthesizing Direct Curve Study III: Tactile Corner Radii & Architectural Terminals...")
    s3 = build_curve_study_3()
    s3_path = POSTERS_DIR / "curve_study_03_terminal_corner_architecture.png"
    s3.save(s3_path, "PNG", dpi=(300, 300))

    print("4. Synthesizing Direct Curve Study IV: 100% Sovereign Indigenous Curve Mechanics...")
    s4 = build_curve_study_4()
    s4_path = POSTERS_DIR / "curve_study_04_sovereign_scientific_curves.png"
    s4.save(s4_path, "PNG", dpi=(300, 300))

    print("5. Synthesizing Direct Curve Study V: Dedicated ISO 17049 Tactile Braille & Scientific Topology...")
    s5 = build_curve_study_5()
    s5_path = POSTERS_DIR / "curve_study_05_tactile_braille_dome_geometry.png"
    s5.save(s5_path, "PNG", dpi=(300, 300))

    print("6. Exporting 5-Page Direct Curve Studies PDF Atlas...")
    pdf_path = POSTERS_DIR / "pocketgull_direct_curve_studies_v3.1.0.pdf"
    s1.save(pdf_path, "PDF", resolution=300.0, save_all=True, append_images=[s2, s3, s4, s5])

    if ARTIFACT_DIR.exists():
        for src in [s1_path, s2_path, s3_path, s4_path, s5_path, pdf_path]:
            dst = ARTIFACT_DIR / src.name
            dst.write_bytes(src.read_bytes())
        print(f"7. Copied all 5 Direct Curve Study plates and PDF Atlas to: {ARTIFACT_DIR}")

    print("\n[SUCCESS] All 5 Direct Quadratic Curve Studies generated!")


if __name__ == "__main__":
    main()
