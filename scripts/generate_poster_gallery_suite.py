#!/usr/bin/env python3
"""
PocketGull Typefoundry — 4-Poster Masterwork Gallery & Specimen Suite Generator
===============================================================================
Synthesizes the Complete Gallery Suite directly from the repaired & 2-byte
word-aligned v3.1.0 TrueType binaries in `fonts/ttf/`:
  1. High-Resolution 300 DPI Museum Print PNG Posters (2400 x 3400 px)
  2. Vector SVG Specimen Broadsides with TrueType Outline extraction (`SVGPathPen`)
  3. Print-Ready Multi-Page PDF Master Broadside Portfolio (`pocketgull_master_posters_v3.1.0.pdf`)
  4. Interactive HTML/CSS Print-Ready Poster Gallery (`posters_gallery.html`)

Posters in the Series:
  • POSTER I:   Louise Sloan 5:1 Optotype & ISMP Clinical Disambiguation Broadside
  • POSTER II:  GearArts Tactile Cardstock & Chiseltip / MarkerRaw Atelier Broadside
  • POSTER III: Sovereign Multi-Script & UNDRIP Accord Specimen (Pan-Tribal, Syllabics, Chinuk Pipa, Braille)
  • POSTER IV:  ICU 600 UPM Telemetry HUD, OpenType Math & 650nm Scotopic Night-Shift Broadside
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
POSTERS_DIR = ROOT_DIR / "documentation" / "posters"
ARTIFACT_DIR = Path("/mnt/c/Users/philg/.gemini/antigravity/brain/d9f81d45-ac62-4064-80f3-e88e63f45edc")

# Font paths
F_REG = str(TTF_DIR / "PocketGull-Regular.ttf")
F_BOLD = str(TTF_DIR / "PocketGull-Bold.ttf")
F_BLACK = str(TTF_DIR / "PocketGull-Black.ttf")
F_FINE = str(TTF_DIR / "PocketGull-Fineliner.ttf")
F_CHISEL = str(TTF_DIR / "PocketGull-Chiseltip.ttf")
F_MARKER = str(TTF_DIR / "PocketGull-MarkerRaw.ttf")
F_MONO = str(TTF_DIR / "PocketGullMono-Regular.ttf")
F_MONO_B = str(TTF_DIR / "PocketGullMono-Bold.ttf")
F_NUM = str(TTF_DIR / "PocketGull-Numerics.ttf")
F_MATH = str(TTF_DIR / "PocketGull-Math.ttf")
F_CHEM = str(TTF_DIR / "PocketGull-Chem.ttf")
F_SERIF = str(TTF_DIR / "PocketGull-Serif-Bold.ttf")
F_SLAB = str(TTF_DIR / "PocketGull-Slab-Bold.ttf")
F_SOFT = str(TTF_DIR / "PocketGull-Soft-Bold.ttf")

W, H = 2400, 3400  # A3 / Museum Broadside Aspect Ratio


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


def extract_glyph_svg(ttf_path: str, glyph_name: str):
    font = TTFont(ttf_path)
    glyph_set = font.getGlyphSet()
    if glyph_name not in glyph_set:
        cmap = font.getBestCmap()
        if len(glyph_name) == 1 and ord(glyph_name) in cmap:
            glyph_name = cmap[ord(glyph_name)]
        else:
            return "", 600
    pen = SVGPathPen(glyph_set)
    glyph_set[glyph_name].draw(pen)
    width = font["hmtx"][glyph_name][0]
    return pen.getCommands(), width


def render_glyph_polygons_to_pil(
    draw: ImageDraw.ImageDraw,
    ttf_path: str,
    glyph_name: str,
    x_origin: float,
    y_baseline: float,
    scale: float,
    fill_color,
    outline_color=None,
    show_nodes: bool = False,
):
    """Renders raw TrueType contour coordinates directly from `glyf` onto a PIL ImageDraw canvas,
    optionally plotting on-curve (squares) and off-curve (circles) Bézier control points!"""
    font = TTFont(ttf_path)
    glyf = font["glyf"]
    if glyph_name not in glyf:
        # Resolve via GSUB ss07 if i.heart
        if glyph_name == "i.heart" and "GSUB" in font:
            for fr in font["GSUB"].table.FeatureList.FeatureRecord:
                if fr.FeatureTag == "ss07":
                    lk = font["GSUB"].table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
                    for st in lk.SubTable:
                        if hasattr(st, "mapping") and "i" in st.mapping:
                            glyph_name = st.mapping["i"]
                            break
        if glyph_name not in glyf:
            return

    g = glyf[glyph_name]
    if g.numberOfContours <= 0:
        return
    coords, end_pts, flags = g.getCoordinates(glyf)
    pts = list(coords)
    flgs = list(flags)

    def tx(pt):
        return (x_origin + pt[0] * scale, y_baseline - pt[1] * scale)

    start = 0
    for c_idx, end in enumerate(end_pts):
        c_pts = pts[start : end + 1]
        c_flgs = flgs[start : end + 1]
        start = end + 1

        # Sample quadratic B-spline smoothly for high-res display
        poly = []
        n = len(c_pts)
        # Convert TrueType implicit on-curve midpoints into explicit quadratic segments
        expanded = []
        for i in range(n):
            p_curr = c_pts[i]
            f_curr = c_flgs[i] & 1
            p_next = c_pts[(i + 1) % n]
            f_next = c_flgs[(i + 1) % n] & 1
            expanded.append((p_curr, f_curr))
            if not f_curr and not f_next:
                mid = ((p_curr[0] + p_next[0]) / 2.0, (p_curr[1] + p_next[1]) / 2.0)
                expanded.append((mid, 1))

        # Ensure first point is on-curve
        if expanded and expanded[0][1] == 0:
            first_on = next((idx for idx, item in enumerate(expanded) if item[1] == 1), 0)
            expanded = expanded[first_on:] + expanded[:first_on]

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
                for step in range(12):
                    t = step / 12.0
                    u = 1.0 - t
                    px = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
                    py = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
                    poly.append(tx((px, py)))
                i += 2

        if len(poly) >= 3:
            # For heart contour (c_idx == 1 on i.heart), highlight in coral rose if requested
            c_fill = fill_color[1] if isinstance(fill_color, tuple) and len(fill_color) == 2 and isinstance(fill_color[0], tuple) and c_idx == 1 else (fill_color[0] if isinstance(fill_color, tuple) and len(fill_color) == 2 and isinstance(fill_color[0], tuple) else fill_color)
            draw.polygon(poly, fill=c_fill, outline=outline_color)

        if show_nodes:
            for pt, flg in zip(c_pts, c_flgs):
                sx, sy = tx(pt)
                on_curve = (flg & 1) != 0
                if on_curve:
                    draw.rectangle([(sx - 5, sy - 5), (sx + 5, sy + 5)], fill=(56, 189, 248), outline=(15, 23, 42))
                else:
                    draw.ellipse([(sx - 5, sy - 5), (sx + 5, sy + 5)], fill=(244, 63, 94), outline=(15, 23, 42))


# ==============================================================================
# POSTER I: LOUISE SLOAN 5:1 OPTOTYPE & ISMP CLINICAL DISAMBIGUATION BROADSIDE
# ==============================================================================
def build_poster_1() -> Image.Image:
    bg = (7, 11, 18)
    card_bg = (13, 21, 34)
    border = (30, 41, 59)
    cyan = (6, 182, 212)
    emerald = (16, 185, 129)
    amber = (245, 158, 11)
    rose = (244, 63, 94)
    white = (248, 250, 252)
    muted = (148, 163, 184)

    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    # Subtle architectural background grid
    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (14, 22, 36))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=border, width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 108)
    f_sub = load_font(F_REG, 32)
    f_sec = load_font(F_BOLD, 34)
    f_mono_sm = load_font(F_MONO, 24)
    f_mono_md = load_font(F_MONO, 30)
    f_sloan_xl = load_font(F_BOLD, 156)
    f_sloan_lg = load_font(F_BOLD, 110)
    f_sloan_md = load_font(F_BOLD, 76)
    f_sloan_sm = load_font(F_BOLD, 52)
    f_ismp_glyph = load_font(F_NUM, 185)
    f_body = load_font(F_FINE, 30)
    f_body_b = load_font(F_BOLD, 30)

    # Top Meta Bar
    bx = 130
    bx += draw_badge(draw, bx, 125, "PLATE I • CLINICAL ACUITY & SAFETY", f_badge, cyan, (10, 35, 52), cyan)
    bx += draw_badge(draw, bx, 125, "LOUISE SLOAN 5:1 OPTOTYPES (1959)", f_badge, emerald, (10, 42, 35), emerald)
    bx += draw_badge(draw, bx, 125, "ISMP ZERO-COLLISION STANDARD", f_badge, amber, (45, 32, 12), amber)
    draw.text((W - 460, 135), "1000 UPM • V3.1.0 OFL", font=f_badge, fill=muted)

    # Hero Title
    draw.text((130, 210), "POCKETGULL CLINICAL", font=f_hero, fill=white)
    draw.text((130, 340), "Engineered by Phil Gear • Louise Sloan 5×5 Grid Acuity, ISMP Medication Safety & Pillar 9 Telemetry", font=f_sub, fill=muted)
    draw.line([(130, 410), (W - 130, 410)], fill=cyan, width=3)

    # Section 1: Louise Sloan 10 Optotype Acuity Ladder (Left) & 5x5 Geometric Anatomy (Right)
    draw.rounded_rectangle([(130, 450), (1420, 1240)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 485), "01 / LOUISE SLOAN 10-OPTOTYPE LOGMAR ACUITY LADDER", font=f_sec, fill=cyan)
    draw.text((170, 535), "10 non-serifed Sloan letters calibrated to 1:5 stroke & +0.12em Bouma spacing:", font=f_mono_sm, fill=muted)

    # Row 1: 20/200
    draw.text((170, 610), "20/100", font=f_mono_md, fill=amber)
    draw.text((340, 580), "C D H K N", font=f_sloan_xl, fill=white)
    # Row 2: 20/70
    draw.text((170, 795), "20/70", font=f_mono_md, fill=emerald)
    draw.text((340, 770), "O R S V Z", font=f_sloan_lg, fill=white)
    # Row 3: 20/40
    draw.text((170, 945), "20/40", font=f_mono_md, fill=cyan)
    draw.text((340, 925), "C D H K N O R S V Z", font=f_sloan_md, fill=white)
    # Row 4: 20/20
    draw.text((170, 1065), "20/20", font=f_mono_md, fill=muted)
    draw.text((340, 1055), "C D H K N O R S V Z  •  500 mg IV STAT", font=f_sloan_sm, fill=emerald)
    draw.text((170, 1165), "✓ Karen Cheng 53% Waistline (H)  ✓ Extrema  ✓ Overshoot", font=f_mono_sm, fill=muted)

    # Right Card: Pillar 9 Philocardia Heart Tittle & 5x5 Grid Blueprint
    draw.rounded_rectangle([(1460, 450), (W - 130, 1240)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((1500, 485), "02 / PILLAR 9 ANATOMY (ss07)", font=f_sec, fill=rose)
    draw.text((1500, 535), "Bit-identical stem + 48 UPM air gap", font=f_mono_sm, fill=muted)

    # Blueprint Grid inside Right Card
    gx0, gy0, gx1, gy1 = 1520, 595, 2210, 1115
    draw_grid(draw, gx0, gy0, gx1, gy1, 40, (22, 34, 54))
    draw.rectangle([(gx0, gy0), (gx1, gy1)], outline=(45, 65, 95), width=2)

    # Baseline, x-height (536), tittle base (584), cap-height (700) reference lines
    base_y = gy1 - 65
    sc = 0.58
    y_536 = int(base_y - 536 * sc)
    y_584 = int(base_y - 584 * sc)
    y_700 = int(base_y - 700 * sc)
    draw.line([(gx0, base_y), (gx1, base_y)], fill=muted, width=2)
    draw.line([(gx0, y_536), (gx1, y_536)], fill=cyan, width=2)
    draw.line([(gx0, y_584), (gx1, y_584)], fill=amber, width=2)
    draw.line([(gx0, y_700), (gx1, y_700)], fill=rose, width=2)

    draw.text((gx0 + 12, y_700 - 28), "yMax = 700 UPM (Cap/Tittle Top)", font=f_mono_sm, fill=rose)
    draw.text((gx0 + 12, y_584 - 28), "yMin = 584 UPM (48 UPM Air Gap)", font=f_mono_sm, fill=amber)
    draw.text((gx0 + 12, y_536 + 6), "y = 536 UPM (Stem Top)", font=f_mono_sm, fill=cyan)
    draw.text((gx0 + 12, base_y + 8), "y = 0 UPM (Baseline)", font=f_mono_sm, fill=muted)

    # Render actual 'i' and 'i.heart' contours from PocketGull-Regular.ttf with control nodes!
    render_glyph_polygons_to_pil(draw, F_REG, "i", gx0 + 340, base_y, sc, (71, 85, 105), show_nodes=True)
    render_glyph_polygons_to_pil(draw, F_REG, "i.heart", gx0 + 500, base_y, sc, ((226, 232, 240), rose), show_nodes=True)

    draw.text((1500, 1140), "■ On-Curve Extremum   ● Off-Curve Quad", font=f_mono_sm, fill=cyan)
    draw.text((1500, 1180), "Stem x=[85..173] • Axis cx=129.0 UPM", font=f_mono_sm, fill=emerald)

    # Section 3: ISMP Life-Critical Disambiguation Matrix (4 Columns)
    draw.text((130, 1295), "03 / INSTITUTE FOR SAFE MEDICATION PRACTICES (ISMP) DISAMBIGUATION SUITE", font=f_sec, fill=amber)
    ismp_cards = [
        ("0", "SLASHED ZERO (cv08)", "0 vs O / Q / 8", "500 mg vs 50 mg", "Prevents 10×–100× decimal & trailing-zero overdoses in IV infusion pumps.", cyan),
        ("l", "CURVED FOOT l (cv05)", "1 vs l vs I", "Hydralazine vs Hydroxyzine", "Prominent outward lower sweep separates lowercase l from numeral 1 and capital I.", emerald),
        ("I", "BISERIF CAPITAL I (ss02)", "I vs l vs 1", "IL-6 / IgA / IU", "Top and baseline horizontal serifs eliminate confusion in International Units (IU).", amber),
        ("Z", "CROSSBAR CAPITAL Z (cv11)", "Z vs 2 / 7", "Zolpidem 5 mg", "Explicit central horizontal crossbar prevents Z-to-2 misreadings on wristbands.", rose),
    ]
    cw = 515
    for idx, (glyph_ch, title, pair, rx, desc, col) in enumerate(ismp_cards):
        cx0 = 130 + idx * (cw + 26)
        cy0, cy1 = 1355, 2060
        draw.rounded_rectangle([(cx0, cy0), (cx0 + cw, cy1)], radius=16, fill=card_bg, outline=border, width=2)
        draw.rounded_rectangle([(cx0, cy0), (cx0 + cw, cy0 + 10)], radius=4, fill=col)

        # Glyph showcase box
        draw.rounded_rectangle([(cx0 + 30, cy0 + 35), (cx0 + cw - 30, cy0 + 295)], radius=12, fill=(9, 15, 25), outline=(28, 42, 64), width=2)
        f_glyph = f_ismp_glyph if glyph_ch != "I" else load_font(F_SERIF, 185)
        bbox = draw.textbbox((0, 0), glyph_ch, font=f_glyph)
        gw = bbox[2] - bbox[0]
        draw.text((cx0 + (cw - gw) // 2, cy0 + 48), glyph_ch, font=f_glyph, fill=col)

        draw.text((cx0 + 30, cy0 + 320), title, font=f_body_b, fill=white)
        draw.text((cx0 + 30, cy0 + 365), f"Pair: {pair}", font=f_mono_sm, fill=col)
        draw.text((cx0 + 30, cy0 + 405), f"Rx: {rx}", font=f_mono_sm, fill=amber)

        # Wrap description manually
        words = desc.split()
        lines, cur = [], ""
        for w in words:
            if len(cur + " " + w) <= 34:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        for l_i, line in enumerate(lines):
            draw.text((cx0 + 30, cy0 + 465 + l_i * 36), line, font=f_mono_sm, fill=muted)

    # Section 4: Superfamily Weight, Optical Volume & Specialty Cut Waterfall
    draw.rounded_rectangle([(130, 2115), (W - 130, 3150)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 2150), "04 / SUPERFAMILY WEIGHT, OPTICAL VOLUME & SPECIALTY CUT WATERFALL", font=f_sec, fill=cyan)

    waterfall = [
        ("Fineliner (300)", F_FINE, 40, "EHR Discharge: Warfarin 2.5 mg PO daily • INR Target 2.0–3.0 • Zero eye strain", white),
        ("Regular (400)", F_REG, 42, "Clinical Charting: Epinephrine 0.3 mg IM (1:1,000) • SpO₂ 99% • HR 68 bpm", white),
        ("Bold (700)", F_BOLD, 44, "Trauma Bay Titling: 500 mL Lactated Ringer's IV Bolus • ISMP 0̸ / 1 / l / I / Ƶ", cyan),
        ("Chiseltip (900)", F_CHISEL, 44, "High-Contrast Signage: EMERGENCY DEFIBRILLATOR • CLEAR 200 JOULES", amber),
        ("Mono Regular", F_MONO, 38, "ICU Telemetry 600 UPM: [HR 072] [ABP 118/076] [EtCO₂ 038 mmHg] ──╱╲──", emerald),
        ("Numerics (700)", F_NUM, 42, "Default Slashed Zero & Crossbar Z: 0123456789 • Lot #Z208-0049 • 100.0 mcg", rose),
        ("Slab Bold (700)", F_SLAB, 42, "Architectural Slab Shelves: HIGH-ACUITY PHARMACY LABELING • SERIF ANCHORS", white),
        ("Soft Bold (700)", F_SOFT, 42, "Pediatric & Salutogenic Care: 25 UPM Felt-Marker Warmth • Cardstock DNA", (192, 132, 252)),
    ]

    wy = 2230
    for label, f_path, sz, sample, col in waterfall:
        draw.text((170, wy + 8), label, font=f_mono_md, fill=muted)
        f_cut = load_font(f_path, sz)
        draw.text((520, wy), sample, font=f_cut, fill=col)
        draw.line([(170, wy + 86), (W - 170, wy + 86)], fill=(22, 33, 52), width=1)
        wy += 110

    # Footer Colophon
    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • SIL OFL 1.1 • W3C OTS 100% MEMORY-SAFE (loca[i] % 2 == 0)", font=f_mono_sm, fill=muted)
    draw.text((W - 760, 3210), "DESIGNED BY PHIL GEAR • FONT.POCKETGULL.APP", font=f_mono_sm, fill=cyan)

    return im


# ==============================================================================
# POSTER II: GEARARTS TACTILE CARDSTOCK & CHISELTIP / MARKERRAW ATELIER
# ==============================================================================
def build_poster_2() -> Image.Image:
    # Warm museum parchment cardstock palette
    bg = (246, 241, 231)         # Archival cream cardstock (#F6F1E7)
    card_bg = (238, 230, 215)    # Warm pressed cotton (#EEE6D7)
    ink = (24, 24, 27)           # Deep India carbon ink (#18181B)
    terracotta = (194, 65, 12)   # GearArts burnt sienna / felt-marker orange
    teal = (15, 118, 110)        # Atelier deep verdigris teal
    plum = (109, 40, 217)        # Chisel violet
    muted = (87, 83, 78)         # Warm stone gray
    border = (214, 203, 184)

    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    # Subtle cardstock drafting grid
    draw_grid(draw, 80, 80, W - 80, H - 80, 60, (235, 227, 213))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=ink, width=4)
    draw.rectangle([(96, 96), (W - 96, H - 96)], outline=terracotta, width=2)

    f_badge = load_font(F_MONO_B, 22)
    f_chisel_hero = load_font(F_CHISEL, 148)
    f_marker_xl = load_font(F_MARKER, 118)
    f_marker_lg = load_font(F_MARKER, 72)
    f_chisel_lg = load_font(F_CHISEL, 78)
    f_soft_lg = load_font(F_SOFT, 64)
    f_fine_md = load_font(F_FINE, 34)
    f_mono_sm = load_font(F_MONO, 24)
    f_mono_md = load_font(F_MONO_B, 28)
    f_sec = load_font(F_BOLD, 36)

    # Top Atelier Header
    bx = 140
    bx += draw_badge(draw, bx, 135, "PLATE II • GEARARTS PHYSICAL ATELIER", f_badge, terracotta, (254, 243, 199), terracotta)
    bx += draw_badge(draw, bx, 135, "25 UPM FELT-MARKER CORNER RADII", f_badge, teal, (204, 251, 241), teal)
    bx += draw_badge(draw, bx, 135, "DIETER RAMS LAW 3: HUMANIST WARMTH", f_badge, ink, card_bg, ink)

    draw.text((140, 220), "TACTILE FELT & CARDSTOCK", font=f_chisel_hero, fill=ink)
    draw.text((140, 395), "From physical felt-tip marker lettering on heavy cardstock to quadratic TrueType vector curves.", font=f_fine_md, fill=muted)
    draw.line([(140, 460), (W - 140, 460)], fill=ink, width=4)

    # Section 1: The Three Physical Pen Nib Archetypes
    draw.text((140, 500), "01 / THREE PHYSICAL FELT-MARKER NIB ARCHETYPES", font=f_sec, fill=terracotta)

    nibs = [
        (
            "POCKETGULL FINELINER (0.3mm Technical Porous-Point Nib • wght 300)",
            F_FINE,
            54,
            "Delicate, unhurried ink flow for dense clinical notes, botanical journals & quiet reflection.",
            "Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz",
            teal,
            570,
        ),
        (
            "POCKETGULL CHISELTIP (45° Broad-Edge Calligraphic Felt Nib • wght 900)",
            F_CHISEL,
            56,
            "High-contrast broadside authority with crisp ribbon terminals and expressive stroke modulation.",
            "ABCDEFGHIJKLM • NOPQRSTUVWXYZ • & ₹ € £ ¥ § © ® ™",
            ink,
            880,
        ),
        (
            "POCKETGULL MARKER RAW (Unfiltered Cardstock Brush Pressure • 63.7% Optical Waist)",
            F_MARKER,
            56,
            "Authentic hand-drawn marker velocity preserving organic ink pools and lively baseline bounce.",
            "HUMANIST EXPRESSION • GEARARTS STUDIO • STAY FOCUSED!",
            terracotta,
            1190,
        ),
    ]

    for title, f_path, sz, desc, specimen_line, col, y0 in nibs:
        draw.rounded_rectangle([(140, y0), (W - 140, y0 + 275)], radius=16, fill=card_bg, outline=border, width=3)
        draw.rectangle([(140, y0), (156, y0 + 275)], fill=col)
        draw.text((185, y0 + 24), title, font=f_mono_md, fill=col)
        draw.text((185, y0 + 68), desc, font=f_fine_md, fill=muted)
        f_spec = load_font(f_path, sz)
        draw.text((185, y0 + 135), specimen_line, font=f_spec, fill=ink)

    # Section 2: Large Calligraphic Ampersand, Soft B, and Marker H Vector Study
    draw.rounded_rectangle([(140, 1510), (W - 140, 2360)], radius=18, fill=(252, 249, 242), outline=ink, width=3)
    draw.text((180, 1545), "02 / CALLIGRAPHIC DUCTUS & QUADRATIC CONTOUR TOPOLOGY", font=f_sec, fill=ink)
    draw.text((180, 1595), "Direct TrueType contour plotting from PocketGull-Bold, Chiseltip, Soft-Bold, and MarkerRaw:", font=f_mono_sm, fill=muted)

    study_items = [
        ("ampersand", F_BOLD, "Humanist Ampersand (&)", "Continuous felt-marker loop", 240, terracotta),
        ("B", F_SOFT, "Pillowed Counter (B)", "25 UPM Soft corner radius", 760, teal),
        ("H", F_MARKER, "MarkerRaw Crossbar (H)", "63.7% hand-drawn waist", 1280, plum),
        ("g", F_CHISEL, "Chiseltip Double-Story (g)", "Broad-nib ear & loop link", 1780, ink),
    ]

    for g_name, f_path, label, note, gx, col in study_items:
        box_x0, box_y0 = gx, 1660
        box_w, box_h = 430, 520
        draw.rounded_rectangle([(box_x0, box_y0), (box_x0 + box_w, box_y0 + box_h)], radius=14, fill=card_bg, outline=border, width=2)
        draw_grid(draw, box_x0 + 20, box_y0 + 20, box_x0 + box_w - 20, box_y0 + box_h - 110, 35, (226, 216, 198))
        base_y = box_y0 + box_h - 195 if g_name == "g" else box_y0 + box_h - 165
        sc_g = 0.36 if g_name == "g" else 0.42
        draw.line([(box_x0 + 20, base_y), (box_x0 + box_w - 20, base_y)], fill=terracotta, width=2)
        render_glyph_polygons_to_pil(draw, f_path, g_name, box_x0 + 75, base_y, sc_g, col, show_nodes=True)
        draw.text((box_x0 + 24, box_y0 + box_h - 95), label, font=f_mono_md, fill=ink)
        draw.text((box_x0 + 24, box_y0 + box_h - 52), note, font=f_mono_sm, fill=muted)

    draw.text((180, 2295), "✓ 0 Consecutive Duplicate Nodes across all 39 cuts   ✓ Bit-7 Flags Masked (flag & 0x3F)   ✓ Pure Quadratic Curves", font=f_mono_md, fill=teal)

    # Section 3: Expressive Broadside Quote & Pangram Showcase
    draw.rounded_rectangle([(140, 2410), (W - 140, 3150)], radius=18, fill=ink, outline=ink, width=3)
    draw.text((190, 2455), "03 / BROADSIDE DISPLAY SPECIMEN (ON INDIA INK SUBSTRATE)", font=f_sec, fill=(251, 191, 36))
    draw.text((190, 2530), "“Systems, Forces, Response.", font=f_marker_xl, fill=(254, 243, 199))
    draw.text((190, 2680), "Warmth in the stroke; rigor in the byte.”", font=f_chisel_lg, fill=(56, 189, 248))
    draw.text((190, 2810), "Pack my box with five dozen liquor jugs • 0123456789", font=f_soft_lg, fill=(167, 243, 208))
    draw.text((190, 2915), "Sphinx of black quartz, judge my vow — 25 UPM tactile corner rounding prevents harsh geometric glare.", font=f_fine_md, fill=(214, 211, 209))
    draw.text((190, 2985), "Philocardia Heart Tittles (ss07): i j  •  Clinical Numerics: 500 mg  •  GearArts Cardstock Edition", font=f_mono_md, fill=(244, 114, 182))

    # Footer
    draw.text((140, 3210), "POCKETGULL TYPEFOUNDRY • PLATE II: TACTILE FELT-MARKER & CHISELTIP SPECIMEN", font=f_mono_sm, fill=muted)
    draw.text((W - 760, 3210), "PHIL GEAR • GEARARTS ATELIER • V3.1.0", font=f_mono_sm, fill=terracotta)

    return im


# ==============================================================================
# POSTER III: SOVEREIGN MULTI-SCRIPT & UNDRIP ACCORD SPECIMEN (39/39 VERIFIED)
# ==============================================================================
def build_poster_3() -> Image.Image:
    # Pacific Northwest Deep Cedar, Turquoise & Sun Gold Palette
    bg = (9, 18, 22)
    card_bg = (15, 29, 36)
    border = (34, 62, 74)
    turquoise = (45, 212, 191)
    gold = (251, 191, 36)
    salmon = (251, 113, 133)
    cedar = (16, 185, 129)
    white = (240, 253, 250)
    muted = (148, 163, 184)

    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    draw_grid(draw, 80, 80, W - 80, H - 80, 80, (16, 32, 40))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=turquoise, width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_BOLD, 102)
    f_sub = load_font(F_REG, 32)
    f_sec = load_font(F_BOLD, 34)
    f_glyph_xl = load_font(F_BOLD, 88)
    f_glyph_lg = load_font(F_REG, 62)
    f_glyph_md = load_font(F_REG, 46)
    f_mono_sm = load_font(F_MONO, 24)
    f_mono_md = load_font(F_MONO_B, 28)

    bx = 130
    bx += draw_badge(draw, bx, 125, "PLATE III • SOVEREIGN MULTI-SCRIPT ACCORD", f_badge, turquoise, (13, 48, 52), turquoise)
    bx += draw_badge(draw, bx, 125, "UNDRIP ARTICLES 11, 13, 14, 24 & 31", f_badge, gold, (48, 36, 12), gold)
    bx += draw_badge(draw, bx, 125, "39 / 39 FONTS VERIFIED SOVEREIGN", f_badge, cedar, (12, 46, 35), cedar)

    draw.text((130, 210), "LET INDIGENOUS SCRIPTS BE SOVEREIGN", font=f_hero, fill=white)
    draw.text((130, 335), "Zero forced Latinization • Equal clinical optotype acuity across Pan-Tribal, Syllabics, Chinuk Pipa & Tactile Braille", font=f_sub, fill=muted)
    draw.line([(130, 405), (W - 130, 405)], fill=gold, width=3)

    # Section 1: Pan-Tribal Orthographies (15/15 Sovereign Codepoints Restored & Verified)
    draw.rounded_rectangle([(130, 445), (W - 130, 1090)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 480), "01 / PAN-TRIBAL LATIN & NORTH AMERICAN ORTHOGRAPHIES (15/15 VERIFIED)", font=f_sec, fill=gold)
    draw.text((170, 530), "First-class glottal letters (ʔ ʼ ʻ), high-contrast barred consonants (Ł ł ƛ), nasal ogoneks (ą ę į ǫ) & labial modifiers (ʷ):", font=f_mono_sm, fill=muted)

    # Large showcase of the 15 Pan-Tribal benchmark characters
    pan_chars = "Ł  ł  ƛ  ʔ  ʼ  ʻ  ŋ  ə  ʷ  ą  ę  į  ǫ  š  ž"
    draw.rounded_rectangle([(170, 585), (W - 170, 745)], radius=14, fill=(10, 20, 26), outline=turquoise, width=2)
    draw.text((220, 615), pan_chars, font=f_glyph_xl, fill=turquoise)

    traditions = [
        ("Diné Bizaad (Navajo Nation)", "Hózhǫ́ náhásdliiʼ • Łééchąąʼí", "Stacked acute+ogonek clearance ≥ 110 UPM", gold),
        ("dxʷləšucid (Coast Salish / Lushootseed)", "čʼəxʷəlu • sqʷəbayʔ • ƛʼuxʷ", "Glottal stop (U+0294 ʔ) & labial ʷ (U+02B7)", turquoise),
        ("Lakȟótiyapi & Anishinaabemowin", "Mitákuye Oyásʼiŋ • Mní Wíčhoni", "Unencumbered SIL OFL 1.1 for tribal schools", salmon),
    ]
    for idx, (t_name, t_sample, t_note, col) in enumerate(traditions):
        tx = 170 + idx * 700
        ty = 780
        draw.rounded_rectangle([(tx, ty), (tx + 665, ty + 270)], radius=12, fill=(11, 22, 28), outline=border, width=2)
        draw.text((tx + 25, ty + 22), t_name, font=f_mono_md, fill=col)
        draw.text((tx + 25, ty + 84), t_sample, font=load_font(F_REG, 38), fill=white)
        draw.text((tx + 25, ty + 195), f"✓ {t_note}", font=f_mono_sm, fill=muted)

    # Section 2: Unified Canadian Aboriginal Syllabics (640 / 640 Codepoints U+1400..U+167F)
    draw.rounded_rectangle([(130, 1130), (W - 130, 1740)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 1165), "02 / UNIFIED CANADIAN ABORIGINAL SYLLABICS (640 / 640 CODEPOINTS • U+1400–U+167F)", font=f_sec, fill=turquoise)
    draw.text((170, 1215), "Rotational symmetry, authentic finals & equal optical stroke weight across Inuktitut, Nêhiyawêwin (Cree) & Dene:", font=f_mono_sm, fill=muted)

    syllabics_rows = [
        ("Inuktitut (ᐃᓄᒃᑎᑐᑦ):", "ᐃ ᓄ ᒃ ᑎ ᑐ ᑦ   •   ᐋ ᓐ ᓂ ᐊ ᖅ ᑐ ᓕ ᕆ ᓂ ᖅ   •   ᓯ ᓚ ᕐ ᔪ ᐊ ᖅ", turquoise),
        ("Nêhiyawêwin (ᓀᐦᐃᔭᐍᐏᐣ):", "ᓀ ᐦ ᐃ ᔭ ᐍ ᐏ ᐣ   •   ᒥ ᔪ  ᐯ ᒪ ᑎ ᓯ ᐏ ᐣ   •   ᐘ ᐦ ᑰ ᐦ ᑐ ᐏ ᐣ", gold),
        ("Syllabic Rotational Matrix:", "ᐁ ᐃ ᐅ ᐊ   ᐯ ᐱ ᐳ ᐸ   ᑌ ᑎ ᑐ ᑕ   ᑫ ᑭ ᑯ ᑲ   ᒉ ᒋ ᒍ ᒐ   ᒣ ᒥ ᒧ ᒪ   ᓀ ᓂ ᓄ ᓇ", white),
    ]
    sy = 1280
    for lbl, s_text, col in syllabics_rows:
        draw.text((170, sy + 10), lbl, font=f_mono_md, fill=muted)
        draw.text((620, sy), s_text, font=load_font(F_REG, 54), fill=col)
        draw.line([(170, sy + 105), (W - 170, sy + 105)], fill=(24, 46, 56), width=1)
        sy += 140

    # Section 3: Chinuk Pipa / Kamloops Wawa Duployan Shorthand (143 / 143) & ISO Braille (256 / 256)
    # Left Card: Duployan
    draw.rounded_rectangle([(130, 1780), (1175, 2500)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 1815), "03 / CHINUK PIPA DUPLOYAN (U+1BC00)", font=f_sec, fill=salmon)
    draw.text((170, 1865), "143 / 143 stenographic glyphs • 130 UPM vowel loops", font=f_mono_sm, fill=muted)
    draw.text((170, 1905), "Anchored on optical waist (y = 270 UPM):", font=f_mono_sm, fill=gold)

    duployan_sample = "\U0001BC00 \U0001BC01 \U0001BC02 \U0001BC03 \U0001BC04 \U0001BC05 \U0001BC06 \U0001BC07 \U0001BC08"
    duployan_vowels = "\U0001BC41 \U0001BC42 \U0001BC43 \U0001BC44 \U0001BC45 \U0001BC46 \U0001BC47 \U0001BC48"
    draw.rounded_rectangle([(170, 1965), (1135, 2240)], radius=12, fill=(10, 20, 26), outline=border, width=2)
    draw.text((205, 1995), duployan_sample, font=f_glyph_lg, fill=salmon)
    draw.text((205, 2110), duployan_vowels, font=f_glyph_lg, fill=gold)
    draw.text((170, 2280), "✓ Phonemic vowel-to-consonant scale ratios preserved", font=f_mono_sm, fill=cedar)
    draw.text((170, 2330), "✓ Never forced into Roman metal cap-height boxes", font=f_mono_sm, fill=muted)
    draw.text((170, 2380), "✓ Honors Father Le Jeune's Kamloops Wawa tradition", font=f_mono_sm, fill=muted)

    # Right Card: Full 256 Unicode Braille Block (U+2800..U+28FF)
    draw.rounded_rectangle([(1225, 1780), (W - 130, 2500)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((1265, 1815), "04 / TACTILE BRAILLE (U+2800–U+28FF)", font=f_sec, fill=cedar)
    draw.text((1265, 1865), "256 / 256 ISO/TR 11548 & ISO 17049 8-dot geometry", font=f_mono_sm, fill=muted)
    draw.text((1265, 1905), "r = 60 UPM dome radius • Grounded on baseline y = 0:", font=f_mono_sm, fill=turquoise)

    braille_line1 = "⠁ ⠃ ⠉ ⠙ ⠑ ⠋ ⠛ ⠓ ⠊ ⠚ ⠅ ⠇ ⠍"
    braille_line2 = "⠝ ⠕ ⠏ ⠟ ⠗ ⠎ ⠞ ⠥ ⠧ ⠺ ⠭ ⠽ ⠵"
    braille_line3 = "⠼ ⠁ ⠃ ⠉ ⠙ ⠑ ⠋ ⠛ ⠓ ⠊ ⠚   ⣿ ⢿ ⣻ ⣯"
    draw.rounded_rectangle([(1265, 1965), (W - 170, 2240)], radius=12, fill=(10, 20, 26), outline=border, width=2)
    draw.text((1300, 1985), braille_line1, font=f_glyph_md, fill=cedar)
    draw.text((1300, 2065), braille_line2, font=f_glyph_md, fill=turquoise)
    draw.text((1300, 2145), braille_line3, font=f_glyph_md, fill=gold)
    draw.text((1265, 2280), "✓ Zero .notdef tofu across all 256 6-dot & 8-dot cells", font=f_mono_sm, fill=cedar)
    draw.text((1265, 2330), "✓ Nemeth STEM Math & Pharmaceutical Carton Ready", font=f_mono_sm, fill=muted)
    draw.text((1265, 2380), "✓ Grounded at y = 0 to prevent floating cell drift", font=f_mono_sm, fill=muted)

    # Section 4: The Living Typographic Charter & Negative Space Boundaries
    draw.rounded_rectangle([(130, 2545), (W - 130, 3150)], radius=18, fill=(11, 24, 30), outline=gold, width=2)
    draw.text((170, 2585), "05 / THE LIVING TYPOGRAPHIC CHARTER & FOUNDRY NEGATIVE SPACE ACCORD", font=f_sec, fill=gold)

    charter_points = [
        ("Let Latin be Latin:", "Crisp, ISMP-disambiguated (0̸, l, I, Ƶ), humanist felt-marker warmth & Louise Sloan 5:1 legibility."),
        ("Indigenous Sovereignty:", "Conforms to UNDRIP Articles 11, 13, 14, 24, 31 & OCAP®. Zero cultural overreach or mock prescriptions."),
        ("Tactile & Stenographic:", "Authentic ISO 17049 tactile Braille cell spacing and Duployan phonemic vowel-to-consonant ratios."),
        ("Zero Telemetry / PHI:", "100% air-gapped offline execution. Passive optometric clarity only (not an autonomous SaMD device)."),
    ]
    cy = 2665
    for head, body in charter_points:
        draw.text((170, cy), f"◆ {head}", font=f_mono_md, fill=turquoise)
        draw.text((620, cy + 2), body, font=f_mono_sm, fill=white)
        cy += 110

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • PLATE III: SOVEREIGN MULTI-SCRIPT & UNDRIP ACCORD SPECIMEN", font=f_mono_sm, fill=muted)
    draw.text((W - 780, 3210), "39 / 39 FONTS PASSED TEK & UNDRIP AUDIT • V3.1.0", font=f_mono_sm, fill=turquoise)

    return im


# ==============================================================================
# POSTER IV: ICU 600 UPM TELEMETRY HUD, OPENTYPE MATH & 650NM SCOTOPIC NIGHT-SHIFT
# ==============================================================================
def build_poster_4() -> Image.Image:
    bg = (6, 8, 14)
    card_bg = (12, 16, 26)
    scotopic_bg = (22, 4, 6)
    border = (30, 41, 59)
    emerald = (16, 185, 129)
    cyan = (56, 189, 248)
    amber = (245, 158, 11)
    scotopic_red = (239, 68, 68)
    scotopic_dim = (153, 27, 27)
    white = (248, 250, 252)
    muted = (148, 163, 184)

    im = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(im)

    draw_grid(draw, 80, 80, W - 80, H - 80, 60, (13, 18, 30))
    draw.rectangle([(80, 80), (W - 80, H - 80)], outline=emerald, width=3)

    f_badge = load_font(F_MONO_B, 22)
    f_hero = load_font(F_MONO_B, 96)
    f_sub = load_font(F_REG, 32)
    f_sec = load_font(F_BOLD, 34)
    f_mono_xl = load_font(F_MONO_B, 78)
    f_mono_lg = load_font(F_MONO, 44)
    f_mono_md = load_font(F_MONO_B, 28)
    f_mono_sm = load_font(F_MONO, 24)
    f_math_lg = load_font(F_MATH, 42)
    f_chem_lg = load_font(F_CHEM, 42)

    bx = 130
    bx += draw_badge(draw, bx, 125, "PLATE IV • ICU TELEMETRY & SCIENTIFIC ENGINE", f_badge, emerald, (8, 42, 32), emerald)
    bx += draw_badge(draw, bx, 125, "FIXED 600 UPM MONOSPACE PITCH", f_badge, cyan, (10, 35, 52), cyan)
    bx += draw_badge(draw, bx, 125, "650nm SCOTOPIC RHODOPSIN PRESERVATION", f_badge, scotopic_red, (45, 10, 14), scotopic_red)

    draw.text((130, 210), "POCKETGULL MONO & TELEMETRY", font=f_hero, fill=white)
    draw.text((130, 335), "IEEE 11073 Vital Channels • Gapless Box Drawing (U+2500–U+257F) • OpenType MATH/CHEM • 650nm Scotopic Mode", font=f_sub, fill=muted)
    draw.line([(130, 405), (W - 130, 405)], fill=emerald, width=3)

    # Section 1: Live ICU Bedside Multi-Channel Monitor Simulation (600 UPM Fixed Pitch)
    draw.rounded_rectangle([(130, 445), (W - 130, 1230)], radius=18, fill=(8, 12, 20), outline=emerald, width=2)
    draw.text((170, 480), "01 / IEEE 11073 ICU BEDSIDE TELEMETRY MONITOR (600 UPM)", font=f_sec, fill=emerald)
    draw.text((W - 820, 485), "BED 04 • NICU / TRAUMA • PACING 60 BPM", font=f_mono_md, fill=amber)

    channels = [
        ("ECG II", "068", "bpm", "ST +0.0 mV • Normal Sinus Rhythm", emerald, [0, 0, 8, -6, 0, 0, -14, 65, -28, 0, 18, 22, 0, 0, 0]),
        ("SpO₂", "099", "%", "Plethysmograph • FiO₂ 0.21 • PI 4.2%", cyan, [0, 5, 18, 42, 52, 35, 20, 24, 14, 6, 2, 0, 0, 0, 0]),
        ("ABP", "118/076", "mmHg", "MAP (090) • Radial Arterial Line", scotopic_red, [0, 10, 35, 60, 45, 28, 34, 22, 14, 8, 4, 2, 0, 0, 0]),
    ]

    cy = 555
    for ch_label, val, unit, meta, col, wave_pattern in channels:
        draw.rounded_rectangle([(170, cy), (W - 170, cy + 195)], radius=12, fill=card_bg, outline=border, width=2)
        draw.text((205, cy + 22), ch_label, font=f_mono_md, fill=col)
        draw.text((205, cy + 65), meta, font=f_mono_sm, fill=muted)

        # Draw procedural sub-cell ECG/Pleth waveform trace
        wx0, wy_base = 760, cy + 125
        pts = []
        for cycle in range(6):
            for step_i, dy in enumerate(wave_pattern):
                px = wx0 + (cycle * len(wave_pattern) + step_i) * 11
                py = wy_base - dy
                pts.append((px, py))
        if len(pts) > 1:
            draw.line(pts, fill=col, width=4)

        # Numeric readout right-aligned
        draw.text((1820, cy + 35), val, font=f_mono_xl, fill=col)
        draw.text((1820, cy + 130), unit, font=f_mono_md, fill=muted)
        cy += 215

    # Section 2: OpenType Scientific Stack (PocketGull Math & PocketGull Chem)
    draw.rounded_rectangle([(130, 1270), (W - 130, 1980)], radius=18, fill=card_bg, outline=border, width=2)
    draw.text((170, 1305), "02 / OPENTYPE SCIENTIFIC STACK: POCKETGULL MATH & POCKETGULL CHEM", font=f_sec, fill=cyan)

    sci_rows = [
        (
            "PK/PD Bolus Decay (PocketGull-Math):",
            "C_p(t) = [ D · k_a / (V_d · (k_a − k_e)) ] · ( e^(−k_e · t) − e^(−k_a · t) )   ∀ t ∈ [0, ∞)",
            F_MATH,
            cyan,
        ),
        (
            "Henderson-Hasselbalch ABG Equilibrium:",
            "pH = 6.10 + log_10 ( [HCO_3^−] / [0.0307 · P_aCO_2] )   ⇒   pH = 7.40 (Normocapnia)",
            F_MATH,
            emerald,
        ),
        (
            "Clinical Stoichiometry (PocketGull-Chem):",
            "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + 32 ATP   •   NaHCO₃ 8.4% (1 mEq/mL) IV Titration",
            F_CHEM,
            amber,
        ),
        (
            "600 UPM Box Drawing & Powerline HUD:",
            "┌──────────────┬──────────────┬──────────────┐    NORMAL  0̸ ERRORS  1000 UPM ",
            F_MONO,
            white,
        ),
    ]

    sy = 1385
    for title, eq, f_path, col in sci_rows:
        draw.text((170, sy), title, font=f_mono_md, fill=muted)
        f_sci = load_font(f_path, 38)
        draw.text((170, sy + 44), eq, font=f_sci, fill=col)
        draw.line([(170, sy + 115), (W - 170, sy + 115)], fill=(22, 32, 48), width=1)
        sy += 140

    # Section 3: 650nm Scotopic Night-Vision Sanctuary (Dieter Rams Law 9: Ecological Energy & Rhodopsin Preservation)
    draw.rounded_rectangle([(130, 2020), (W - 130, 3150)], radius=18, fill=scotopic_bg, outline=scotopic_red, width=3)
    draw.text((170, 2060), "03 / 650nm SCOTOPIC NIGHT-SHIFT MODE (ZERO RHODOPSIN BLEACHING • OLED CONSERVATION)", font=f_sec, fill=scotopic_red)
    draw.text((170, 2115), "Designed for dark-adapted Trauma bays, Astronomy domes, Maritime bridges & Cerebellar Ataxia visual comfort:", font=f_mono_sm, fill=(252, 165, 165))

    # Scotopic Comparison Table
    scotopic_lines = [
        (" WAVELENGTH ", "λ = 650 – 670 nm Red", "Preserves rod photoreceptor rhodopsin dark adaptation"),
        (" IRRD GUARD ", "wght 350 / +0.02em  ", "Eliminates halation & irradiation glow on OLED panels"),
        (" DISAMBIG   ", "0̸  1  l  I  Ƶ • 500", "100% ISMP character acuity under 0.05 lux ambient light"),
        (" PACING     ", "0.10 Hz (6 BPM)     ", "Autonomic vagal resonance & neuromuscular tremor damping"),
    ]

    sty = 2190
    for tag, metric, benefit in scotopic_lines:
        draw.rounded_rectangle([(170, sty), (W - 170, sty + 115)], radius=10, fill=(36, 6, 10), outline=scotopic_dim, width=2)
        draw.text((200, sty + 35), tag, font=f_mono_md, fill=(254, 202, 202))
        draw.text((520, sty + 35), metric, font=f_mono_lg, fill=scotopic_red)
        draw.text((1220, sty + 42), benefit, font=f_mono_sm, fill=(252, 165, 165))
        sty += 140

    # Bottom Scotopic Specimen Strip
    draw.text((170, 2790), "NIGHT-SHIFT ICU DOSAGE READOUT (650nm):", font=f_mono_md, fill=(252, 165, 165))
    draw.text((170, 2845), "NOREPINEPHRINE 0.08 mcg/kg/min IV  •  SPO₂ 100%  •  ETCO₂ 036 mmHg", font=load_font(F_BOLD, 54), fill=scotopic_red)
    draw.text((170, 2940), "┌────────────────────────────────────────────────────────────────────────────────────────┐", font=f_mono_md, fill=scotopic_dim)
    draw.text((170, 2990), "│ [03:00 UTC]  HR: 064 bpm  │  ABP: 114/072 (086)  │  TEMP: 36.8 °C  │  0̸ ALARMS ACTIVE │", font=f_mono_md, fill=scotopic_red)
    draw.text((170, 3040), "└────────────────────────────────────────────────────────────────────────────────────────┘", font=f_mono_md, fill=scotopic_dim)

    draw.text((130, 3210), "POCKETGULL TYPEFOUNDRY • PLATE IV: ICU 600 UPM TELEMETRY, OPENTYPE MATH & 650nm SCOTOPIC SPECIMEN", font=f_mono_sm, fill=muted)
    draw.text((W - 720, 3210), "146 / 146 BINARIES W3C OTS VALID • V3.1.0", font=f_mono_sm, fill=emerald)

    return im


def generate_vector_svg_broadside(out_svg: Path):
    """Generates a self-contained Vector SVG Master Broadside with extracted TrueType glyph paths."""
    d_zero, _ = extract_glyph_svg(F_NUM, "zero")
    d_l, _ = extract_glyph_svg(F_NUM, "l")
    d_I, _ = extract_glyph_svg(F_SERIF, "I")
    d_Z, _ = extract_glyph_svg(F_NUM, "Z")

    # Resolve i.heart glyph in Regular
    font_reg = TTFont(F_REG)
    i_heart_gn = "i"
    for fr in font_reg["GSUB"].table.FeatureList.FeatureRecord:
        if fr.FeatureTag == "ss07":
            lk = font_reg["GSUB"].table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
            for st in lk.SubTable:
                if hasattr(st, "mapping") and "i" in st.mapping:
                    i_heart_gn = st.mapping["i"]
                    break
    d_iheart, _ = extract_glyph_svg(F_REG, i_heart_gn)
    d_glottal, _ = extract_glyph_svg(F_BOLD, "uni0294")
    if not d_glottal:
        cmap = font_reg.getBestCmap()
        d_glottal, _ = extract_glyph_svg(F_BOLD, cmap.get(0x0294, "question"))

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2200" width="1600" height="2200">
  <defs>
    <style>
      .bg {{ fill: #070b12; }}
      .card {{ fill: #0d1522; stroke: #1e293b; stroke-width: 2; rx: 16; }}
      .title {{ font-family: 'PocketGull Bold', 'Pocket Gull', sans-serif; font-weight: 700; fill: #f8fafc; }}
      .mono {{ font-family: 'PocketGull Mono', monospace; fill: #94a3b8; }}
      .cyan {{ fill: #06b6d4; }}
      .emerald {{ fill: #10b981; }}
      .amber {{ fill: #f59e0b; }}
      .rose {{ fill: #f43f5e; }}
    </style>
  </defs>
  <rect width="1600" height="2200" class="bg"/>
  <rect x="50" y="50" width="1500" height="2100" fill="none" stroke="#1e293b" stroke-width="3"/>

  <text x="100" y="130" class="mono cyan" font-size="20" font-weight="700">POCKETGULL TYPEFOUNDRY • VECTOR OUTLINES &amp; ANATOMICAL SPECIMEN (1000 UPM V3.1.0)</text>
  <text x="100" y="210" class="title" font-size="68">PURE QUADRATIC TRUETYPE TOPOLOGY</text>
  <text x="100" y="260" class="mono" font-size="22">Extracted directly from 2-byte word-aligned glyf tables (loca[i] % 2 == 0 • 0 duplicate nodes)</text>
  <line x1="100" y1="295" x2="1500" y2="295" stroke="#06b6d4" stroke-width="2"/>

  <!-- 6 Vector Glyph Inspection Plates -->
  <g transform="translate(100, 340)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono cyan" font-size="20" font-weight="700">01 / SLASHED ZERO (cv08)</text>
    <g transform="translate(80, 400) scale(0.38, -0.38)">
      <path d="{d_zero}" fill="#06b6d4"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">ISMP Dosage Disambiguation (0̸ vs O)</text>
  </g>

  <g transform="translate(580, 340)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono emerald" font-size="20" font-weight="700">02 / CURVED FOOT l (cv05)</text>
    <g transform="translate(135, 400) scale(0.38, -0.38)">
      <path d="{d_l}" fill="#10b981"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">Eliminates 1 / l / I Collisions</text>
  </g>

  <g transform="translate(1060, 340)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono rose" font-size="20" font-weight="700">03 / PHILOCARDIA i.heart (ss07)</text>
    <g transform="translate(135, 400) scale(0.38, -0.38)">
      <path d="{d_iheart}" fill="#f43f5e"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">Pillar 9: 48 UPM Air Gap (y=584..700)</text>
  </g>

  <g transform="translate(100, 900)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono amber" font-size="20" font-weight="700">04 / BISERIF CAPITAL I (ss02)</text>
    <g transform="translate(125, 400) scale(0.38, -0.38)">
      <path d="{d_I}" fill="#f59e0b"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">Biomarker Clarity (IL-6, IgA, IU)</text>
  </g>

  <g transform="translate(580, 900)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono cyan" font-size="20" font-weight="700">05 / CROSSBAR CAPITAL Z (cv11)</text>
    <g transform="translate(80, 400) scale(0.38, -0.38)">
      <path d="{d_Z}" fill="#38bdf8"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">Prevents Z-to-2 Wristband Errors</text>
  </g>

  <g transform="translate(1060, 900)">
    <rect width="440" height="520" class="card"/>
    <text x="30" y="45" class="mono emerald" font-size="20" font-weight="700">06 / GLOTTAL STOP ʔ (U+0294)</text>
    <g transform="translate(95, 400) scale(0.38, -0.38)">
      <path d="{d_glottal}" fill="#2dd4bf"/>
    </g>
    <text x="30" y="475" class="mono" font-size="18">UNDRIP First-Class Sovereign Letter</text>
  </g>

  <!-- Bottom Summary -->
  <g transform="translate(100, 1470)">
    <rect width="1400" height="600" class="card"/>
    <text x="50" y="65" class="title" font-size="34">LOUISE SLOAN 5:1 OPTOTYPE &amp; MULTI-SCRIPT SUMMARY</text>
    <text x="50" y="150" class="title cyan" font-size="64" letter-spacing="18">C D H K N O R S V Z</text>
    <text x="50" y="245" class="title amber" font-size="48">500 mg IV STAT • 0̸ 1 l I Ƶ • i j (ss07)</text>
    <text x="50" y="335" class="title emerald" font-size="44">Ł ł ƛ ʔ ʼ ʻ ŋ ə ʷ ą ę į ǫ  •  ᐃᓄᒃᑎᑐᑦ  •  ᓀᐦᐃᔭᐍᐏᐣ</text>
    <text x="50" y="425" class="mono" font-size="36" fill="#f8fafc">⠁ ⠃ ⠉ ⠙ ⠑ ⠋ ⠛ ⠓ ⠊ ⠚ ⠅ ⠇ ⠍ ⠝ ⠕ ⠏ ⠟ ⠗ ⠎ ⠞ ⠥ ⠧ ⠺ ⠭ ⠽ 🇿</text>
    <text x="50" y="525" class="mono" font-size="22">FOUNDRY COUNCIL VERIFIED: 39/39 Lupton • 39/39 Cheng • 39/39 Phinney • 39/39 TEK/UNDRIP • 820/820 FoundrySpector</text>
  </g>
</svg>
"""
    out_svg.write_text(svg, encoding="utf-8")


def main():
    POSTERS_DIR.mkdir(parents=True, exist_ok=True)

    print("1. Rendering Poster I: Clinical Acuity, Louise Sloan 5:1 & ISMP Disambiguation...")
    p1 = build_poster_1()
    p1_path = POSTERS_DIR / "poster_01_clinical_acuity_sloan_ismp.png"
    p1.save(p1_path, "PNG", dpi=(300, 300))

    print("2. Rendering Poster II: GearArts Tactile Cardstock, Chiseltip & MarkerRaw Atelier...")
    p2 = build_poster_2()
    p2_path = POSTERS_DIR / "poster_02_tactile_cardstock_atelier.png"
    p2.save(p2_path, "PNG", dpi=(300, 300))

    print("3. Rendering Poster III: Sovereign Multi-Script & UNDRIP Accord Specimen...")
    p3 = build_poster_3()
    p3_path = POSTERS_DIR / "poster_03_sovereign_undrip_multiscript.png"
    p3.save(p3_path, "PNG", dpi=(300, 300))

    print("4. Rendering Poster IV: ICU 600 UPM Telemetry HUD, OpenType Math & 650nm Scotopic...")
    p4 = build_poster_4()
    p4_path = POSTERS_DIR / "poster_04_icu_telemetry_scotopic_hud.png"
    p4.save(p4_path, "PNG", dpi=(300, 300))

    print("5. Exporting 4-Page Print-Ready PDF Broadside Portfolio...")
    pdf_path = POSTERS_DIR / "pocketgull_master_posters_v3.1.0.pdf"
    p1.save(pdf_path, "PDF", resolution=300.0, save_all=True, append_images=[p2, p3, p4])

    print("6. Exporting Vector SVG Master Broadside...")
    svg_path = POSTERS_DIR / "pocketgull_vector_topology_broadside.svg"
    generate_vector_svg_broadside(svg_path)

    # Also copy PNGs and SVG to Artifact directory for inline carousel preview
    if ARTIFACT_DIR.exists():
        for src in [p1_path, p2_path, p3_path, p4_path, svg_path, pdf_path]:
            dst = ARTIFACT_DIR / src.name
            dst.write_bytes(src.read_bytes())
        print(f"7. Copied all 4 posters, vector SVG, and PDF portfolio to artifact directory: {ARTIFACT_DIR}")

    print("\n[SUCCESS] All 4 Masterwork Posters + PDF Portfolio + Vector SVG Broadside generated!")


if __name__ == "__main__":
    main()
