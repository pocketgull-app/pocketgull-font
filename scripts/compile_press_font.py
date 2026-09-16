#!/usr/bin/env python3
"""
PocketGull Typefoundry: Press, Packaging, GD&T & 3D Printing Font Compiler
==========================================================================
Compiles 'PocketGull-Press.ttf' and 'PocketGull-Press.woff2'
World's First Humanist Print Production, Structural Packaging, CAD Tolerancing,
and Additive Manufacturing (3D Printing) Specification Typeface
"""

import os
import sys
import shutil
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

SRC_REGULAR = os.path.join(TTF_DIR, "PocketGull-Regular.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Press.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Press.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Press.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Press.woff2")

def draw_rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0))
    pen.lineTo((x1, y0))
    pen.lineTo((x1, y1))
    pen.lineTo((x0, y1))
    pen.closePath()

def draw_circle(pen, cx, cy, r, clockwise=True):
    if clockwise:
        pen.moveTo((cx + r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy + r), (cx, cy + r))
        pen.qCurveTo((cx + r, cy + r), (cx + r, cy))
        pen.closePath()
    else:
        pen.moveTo((cx + r, cy))
        pen.qCurveTo((cx + r, cy + r), (cx, cy + r))
        pen.qCurveTo((cx - r, cy + r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.closePath()

def draw_ring(pen, cx, cy, ro, ri):
    draw_circle(pen, cx, cy, ro, clockwise=True)
    draw_circle(pen, cx, cy, ri, clockwise=False)

def draw_rounded_badge(pen, x0, y0, x1, y1, r=36, sw=28):
    pen.moveTo((x0 + r, y0))
    pen.lineTo((x1 - r, y0))
    pen.qCurveTo((x1, y0), (x1, y0 + r))
    pen.lineTo((x1, y1 - r))
    pen.qCurveTo((x1, y1), (x1 - r, y1))
    pen.lineTo((x0 + r, y1))
    pen.qCurveTo((x0, y1), (x0, y1 - r))
    pen.lineTo((x0, y0 + r))
    pen.qCurveTo((x0, y0), (x0 + r, y0))
    pen.closePath()
    # Inner cutout
    ix0, iy0, ix1, iy1 = x0 + sw, y0 + sw, x1 - sw, y1 - sw
    ir = max(6, r - sw)
    pen.moveTo((ix0 + ir, iy0))
    pen.qCurveTo((ix0, iy0), (ix0, iy0 + ir))
    pen.lineTo((ix0, iy1 - ir))
    pen.qCurveTo((ix0, iy1), (ix0 + ir, iy1))
    pen.lineTo((ix1 - ir, iy1))
    pen.qCurveTo((ix1, iy1), (ix1, iy1 - ir))
    pen.lineTo((ix1, iy0 + ir))
    pen.qCurveTo((ix1, iy0), (ix1 - ir, iy0))
    pen.closePath()

def build_press_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: PRESS, PACKAGING, CAD & 3D PRINTING COMPILER")
    print("=" * 76)

    if not os.path.isfile(SRC_REGULAR):
        print(f"[ERROR] Master regular font missing: {SRC_REGULAR}")
        sys.exit(1)

    print("\n1. Loading master regular font source...")
    font = TTFont(SRC_REGULAR)

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())
    glyph_set = font.getGlyphSet()

    def register_glyph(gname, codepoints, pen, adv=600, lsb=None):
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        if lsb is None:
            lsb = g.xMin if g.numberOfContours > 0 else 40
        hmtx[gname] = (adv, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    # -------------------------------------------------------------
    # 2. Press Marks, Registration Targets & Crop/Bleeds
    # -------------------------------------------------------------
    print("\n2. Synthesizing Registration Targets & Print Marks...")

    # Registration Crosshair uniE990 (⊕)
    pen = TTGlyphPen(None)
    draw_ring(pen, 300, 350, 240, 210)
    draw_rect(pen, 285, 80, 315, 620)      # Vertical line
    draw_rect(pen, 30, 335, 570, 365)      # Horizontal line
    register_glyph("press_reg_crosshair", [0xE990], pen, 600)

    # Bullseye Registration Target uniE991 (⊗)
    pen = TTGlyphPen(None)
    draw_ring(pen, 300, 350, 240, 215)
    draw_ring(pen, 300, 350, 150, 125)
    draw_circle(pen, 300, 350, 50, clockwise=True)
    draw_rect(pen, 288, 80, 312, 620)
    draw_rect(pen, 30, 338, 570, 362)
    register_glyph("press_reg_bullseye", [0xE991], pen, 600)

    # Four-Color Alignment Wedge uniE992
    pen = TTGlyphPen(None)
    # Quadrant 1 (top right)
    pen.moveTo((305, 355))
    pen.lineTo((540, 355))
    pen.qCurveTo((540, 590), (305, 590))
    pen.closePath()
    # Quadrant 3 (bottom left)
    pen.moveTo((295, 345))
    pen.lineTo((60, 345))
    pen.qCurveTo((60, 110), (295, 110))
    pen.closePath()
    draw_ring(pen, 300, 350, 260, 240)
    register_glyph("press_reg_cmyk_target", [0xE992], pen, 600)

    # 3mm Crop Marks (Corner Ticks)
    # Top-Left Crop Mark uniE993
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, 450, 116, 700)     # Vertical tick
    draw_rect(pen, 50, 450, 300, 466)      # Horizontal tick
    register_glyph("press_crop_tl", [0xE993], pen, 400)

    # Top-Right Crop Mark uniE994
    pen = TTGlyphPen(None)
    draw_rect(pen, 284, 450, 300, 700)
    draw_rect(pen, 100, 450, 350, 466)
    register_glyph("press_crop_tr", [0xE994], pen, 400)

    # Bottom-Left Crop Mark uniE995
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, 0, 116, 250)
    draw_rect(pen, 50, 234, 300, 250)
    register_glyph("press_crop_bl", [0xE995], pen, 400)

    # Bottom-Right Crop Mark uniE996
    pen = TTGlyphPen(None)
    draw_rect(pen, 284, 0, 300, 250)
    draw_rect(pen, 100, 234, 350, 250)
    register_glyph("press_crop_br", [0xE996], pen, 400)

    # Paper Grain Long uniE997 (⇈ GL)
    pen = TTGlyphPen(glyphSet=glyph_set)
    # Double vertical arrow
    draw_rect(pen, 120, 140, 150, 560)
    pen.moveTo((80, 500))
    pen.lineTo((135, 620))
    pen.lineTo((190, 500))
    pen.closePath()
    draw_rect(pen, 240, 140, 270, 560)
    pen.moveTo((200, 500))
    pen.lineTo((255, 620))
    pen.lineTo((310, 500))
    pen.closePath()
    # Letters GL
    pen.addComponent("G", (0.55, 0, 0, 0.55, 360, 160))
    pen.addComponent("L", (0.55, 0, 0, 0.55, 540, 160))
    register_glyph("paper_grain_long", [0xE997], pen, 760)

    # Paper Grain Short uniE998 (⇉ GS)
    pen = TTGlyphPen(glyphSet=glyph_set)
    # Double horizontal arrow
    draw_rect(pen, 60, 400, 300, 430)
    pen.moveTo((260, 360))
    pen.lineTo((340, 415))
    pen.lineTo((260, 470))
    pen.closePath()
    draw_rect(pen, 60, 270, 300, 300)
    pen.moveTo((260, 230))
    pen.lineTo((340, 285))
    pen.lineTo((260, 340))
    pen.closePath()
    pen.addComponent("G", (0.55, 0, 0, 0.55, 380, 160))
    pen.addComponent("S", (0.55, 0, 0, 0.55, 560, 160))
    register_glyph("paper_grain_short", [0xE998], pen, 760)

    # Densitometer Step Wedges (10% to 100%) uniE999 - uniE99C
    pen = TTGlyphPen(None)
    for i in range(10):
        h = int(50 + i * 55)
        draw_rect(pen, 50 + i * 50, 100, 85 + i * 50, 100 + h)
    register_glyph("densitometer_wedge", [0xE999], pen, 580)

    # Spine Creep Gauge uniE9A3
    pen = TTGlyphPen(None)
    draw_rect(pen, 40, 240, 560, 260)
    for tick_x in [60, 120, 180, 240, 300, 360, 420, 480, 540]:
        draw_rect(pen, tick_x - 4, 180, tick_x + 4, 320)
    draw_rect(pen, 296, 120, 304, 380)     # Spine center tick
    register_glyph("spine_creep_gauge", [0xE9A3], pen, 600)

    # -------------------------------------------------------------
    # 3. Packaging Die-lines (Cut, Crease, Perf, Flute)
    # -------------------------------------------------------------
    print("\n3. Synthesizing Structural Packaging Die-lines...")

    # Die Cut Rule uniE9B0 (Solid line: 100% through cut, 600 UPM advance)
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 250, 600, 290)
    register_glyph("dieline_cut_rule", [0xE9B0], pen, 600)

    # Die Crease / Score Rule uniE9B1 (Dashed line: 50% score/fold line)
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 255, 120, 285)
    draw_rect(pen, 160, 255, 280, 285)
    draw_rect(pen, 320, 255, 440, 285)
    draw_rect(pen, 480, 255, 600, 285)
    register_glyph("dieline_crease_rule", [0xE9B1], pen, 600)

    # Die Perforation Rule uniE9B2 (Tear line: dash-dot-dash)
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 258, 140, 282)
    draw_circle(pen, 200, 270, 14, clockwise=True)
    draw_rect(pen, 260, 258, 400, 282)
    draw_circle(pen, 460, 270, 14, clockwise=True)
    draw_rect(pen, 520, 258, 600, 282)
    register_glyph("dieline_perf_rule", [0xE9B2], pen, 600)

    # Glue Flap 45° Hatch uniE9B3
    pen = TTGlyphPen(None)
    for hx in range(0, 600, 80):
        pen.moveTo((hx, 150))
        pen.lineTo((hx + 100, 390))
        pen.lineTo((hx + 120, 390))
        pen.lineTo((hx + 20, 150))
        pen.closePath()
    register_glyph("dieline_glue_flap", [0xE9B3], pen, 600)

    # Flute Direction Arrow uniE9B4 (Vertical wave with arrow)
    pen = TTGlyphPen(None)
    draw_rect(pen, 285, 100, 315, 600)
    pen.moveTo((240, 520))
    pen.lineTo((300, 640))
    pen.lineTo((360, 520))
    pen.closePath()
    pen.moveTo((240, 180))
    pen.lineTo((300, 60))
    pen.lineTo((360, 180))
    pen.closePath()
    # Wave ribs
    for wy in [240, 330, 420]:
        pen.moveTo((220, wy))
        pen.qCurveTo((300, wy + 40), (380, wy))
        pen.qCurveTo((300, wy + 20), (220, wy))
        pen.closePath()
    register_glyph("dieline_flute_dir", [0xE9B4], pen, 600)

    # Board Caliper Offset uniE9B5
    pen = TTGlyphPen(glyphSet=glyph_set)
    draw_rounded_badge(pen, 30, 100, 570, 600, r=40, sw=26)
    pen.addComponent("c", (0.6, 0, 0, 0.6, 100, 180))
    pen.addComponent("a", (0.6, 0, 0, 0.6, 260, 180))
    pen.addComponent("l", (0.6, 0, 0, 0.6, 420, 180))
    register_glyph("dieline_caliper_gauge", [0xE9B5], pen, 600)

    # -------------------------------------------------------------
    # 4. CAD & GD&T Dimensions
    # -------------------------------------------------------------
    print("\n4. Synthesizing CAD Dimensioning & GD&T Invariants...")

    # Dimension Lead-In Arrow Left |← uniE9B6
    pen = TTGlyphPen(None)
    draw_rect(pen, 40, 40, 68, 660)        # Witness line
    draw_rect(pen, 68, 335, 360, 365)      # Dimension line
    pen.moveTo((160, 280))
    pen.lineTo((70, 350))
    pen.lineTo((160, 420))
    pen.closePath()
    register_glyph("dim_lead_left", [0xE9B6], pen, 360)

    # Dimension Lead-Out Arrow Right →| uniE9B7
    pen = TTGlyphPen(None)
    draw_rect(pen, 300, 40, 328, 660)      # Witness line
    draw_rect(pen, 0, 335, 298, 365)       # Dimension line
    pen.moveTo((210, 280))
    pen.lineTo((300, 350))
    pen.lineTo((210, 420))
    pen.closePath()
    register_glyph("dim_lead_right", [0xE9B7], pen, 360)

    # In-line Dimension Bar uniE9B8
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 338, 400, 362)
    register_glyph("dim_bar", [0xE9B8], pen, 400)

    # CAD Diameter ⌀ U+2300 & uniE9B9
    pen = TTGlyphPen(None)
    draw_ring(pen, 300, 350, 220, 180)
    # 45-degree slash through circle
    sw = 38
    pen.moveTo((110, 160))
    pen.lineTo((110 + sw, 160))
    pen.lineTo((490, 540))
    pen.lineTo((490 - sw, 540))
    pen.closePath()
    register_glyph("cad_diameter", [0x2300, 0xE9B9], pen, 600)

    # CAD Counterbore ⌴ U+2334
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 200, 116, 500)
    draw_rect(pen, 80, 200, 520, 236)
    draw_rect(pen, 484, 200, 520, 500)
    register_glyph("cad_counterbore", [0x2334], pen, 600)

    # CAD Countersink ⌵ U+2335
    pen = TTGlyphPen(None)
    pen.moveTo((80, 500))
    pen.lineTo((300, 200))
    pen.lineTo((520, 500))
    pen.lineTo((470, 500))
    pen.lineTo((300, 260))
    pen.lineTo((130, 500))
    pen.closePath()
    register_glyph("cad_countersink", [0x2335], pen, 600)

    # CAD Depth ↧ U+21A7
    pen = TTGlyphPen(None)
    draw_rect(pen, 284, 180, 316, 580)
    draw_rect(pen, 120, 550, 480, 580)
    pen.moveTo((220, 280))
    pen.lineTo((300, 150))
    pen.lineTo((380, 280))
    pen.closePath()
    register_glyph("cad_depth", [0x21A7], pen, 600)

    # GD&T Flatness ⏥ U+23E5
    pen = TTGlyphPen(None)
    sw = 32
    pen.moveTo((160, 240))
    pen.lineTo((520, 240))
    pen.lineTo((440, 440))
    pen.lineTo((80, 440))
    pen.closePath()
    # Inner cutout
    pen.moveTo((160 + sw, 240 + sw))
    pen.lineTo((80 + sw, 440 - sw))
    pen.lineTo((440 - sw, 440 - sw))
    pen.lineTo((520 - sw, 240 + sw))
    pen.closePath()
    register_glyph("gdt_flatness", [0x23E5], pen, 600)

    # GD&T Cylindricity ⌭ U+232D
    pen = TTGlyphPen(None)
    draw_ring(pen, 300, 350, 180, 150)
    # Two parallel diagonal lines
    draw_rect(pen, 110, 120, 138, 580)
    draw_rect(pen, 462, 120, 490, 580)
    register_glyph("gdt_cylindricity", [0x232D], pen, 600)

    # -------------------------------------------------------------
    # 5. Additive Manufacturing (3D Printing) Specifications
    # -------------------------------------------------------------
    print("\n5. Synthesizing 3D Printing Specifications & Badges...")

    # Nozzle Badges (⌀0.2, ⌀0.4, ⌀0.6, ⌀0.8)
    def build_nozzle_badge(gname, cp, num_str):
        pen = TTGlyphPen(glyphSet=glyph_set)
        total_w = 980
        draw_rounded_badge(pen, 30, 80, total_w - 30, 620, r=50, sw=30)
        # ⌀
        pen.addComponent("cad_diameter", (0.55, 0, 0, 0.55, 50, 140))
        # Zero
        pen.addComponent("zero", (0.55, 0, 0, 0.55, 340, 140))
        # Period
        pen.addComponent("period", (0.55, 0, 0, 0.55, 540, 140))
        # Num digit
        pen.addComponent(num_str, (0.55, 0, 0, 0.55, 680, 140))
        register_glyph(gname, [cp], pen, total_w)

    build_nozzle_badge("print_nozzle_04", 0xE9C0, "four")
    build_nozzle_badge("print_nozzle_02", 0xE9C1, "two")
    build_nozzle_badge("print_nozzle_06", 0xE9C2, "six")
    build_nozzle_badge("print_nozzle_08", 0xE9C3, "eight")

    # Layer Orientation Z-Axis (↑ Z) uniE9C4
    pen = TTGlyphPen(glyphSet=glyph_set)
    draw_rect(pen, 180, 120, 216, 520)
    pen.moveTo((130, 460))
    pen.lineTo((198, 590))
    pen.lineTo((266, 460))
    pen.closePath()
    pen.addComponent("Z", (0.65, 0, 0, 0.65, 300, 130))
    register_glyph("print_axis_z", [0xE9C4], pen, 640)

    # Layer Orientation XY Planar (↔ XY) uniE9C5
    pen = TTGlyphPen(glyphSet=glyph_set)
    draw_rect(pen, 80, 420, 360, 452)
    pen.moveTo((140, 380))
    pen.lineTo((60, 436))
    pen.lineTo((140, 492))
    pen.closePath()
    pen.moveTo((300, 380))
    pen.lineTo((380, 436))
    pen.lineTo((300, 492))
    pen.closePath()
    pen.addComponent("X", (0.55, 0, 0, 0.55, 420, 130))
    pen.addComponent("Y", (0.55, 0, 0, 0.55, 620, 130))
    register_glyph("print_axis_xy", [0xE9C5], pen, 840)

    # 45° Self-Supporting Overhang Chamfer ∠45° uniE9C6
    pen = TTGlyphPen(None)
    # Right-angle triangle indicating 45-degree slope
    pen.moveTo((100, 140))
    pen.lineTo((460, 140))
    pen.lineTo((460, 500))
    pen.closePath()
    pen.moveTo((150, 180))
    pen.lineTo((420, 450))
    pen.lineTo((420, 180))
    pen.closePath()
    register_glyph("print_overhang_45", [0xE9C6], pen, 560)

    # Bridging Horizontal Span Marker uniE9C7
    pen = TTGlyphPen(None)
    draw_rect(pen, 60, 120, 110, 480)      # Left pillar
    draw_rect(pen, 490, 120, 540, 480)     # Right pillar
    draw_rect(pen, 60, 440, 540, 480)      # Unsupported bridge deck
    # Sag indicator dotted
    draw_circle(pen, 300, 410, 18, clockwise=True)
    register_glyph("print_bridge_span", [0xE9C7], pen, 600)

    # Infill Pattern Symbols: Gyroid, Honeycomb, Grid (uniE9C8 - uniE9CA)
    # Gyroid Infill Symbol uniE9C8
    pen = TTGlyphPen(None)
    for gy in [220, 340, 460]:
        pen.moveTo((80, gy))
        pen.qCurveTo((180, gy + 70), (280, gy))
        pen.qCurveTo((380, gy - 70), (480, gy))
        pen.lineTo((480, gy + 30))
        pen.qCurveTo((380, gy - 40), (280, gy + 30))
        pen.qCurveTo((180, gy + 100), (80, gy + 30))
        pen.closePath()
    register_glyph("print_infill_gyroid", [0xE9C8], pen, 560)

    # Honeycomb Hexagonal Infill uniE9C9
    pen = TTGlyphPen(None)
    def draw_hex(pen, cx, cy, r):
        pen.moveTo((cx, cy + r))
        pen.lineTo((cx + int(r * 0.866), cy + int(r * 0.5)))
        pen.lineTo((cx + int(r * 0.866), cy - int(r * 0.5)))
        pen.lineTo((cx, cy - r))
        pen.lineTo((cx - int(r * 0.866), cy - int(r * 0.5)))
        pen.lineTo((cx - int(r * 0.866), cy + int(r * 0.5)))
        pen.closePath()
    draw_hex(pen, 300, 350, 180)
    draw_hex(pen, 300, 350, 140)
    register_glyph("print_infill_honeycomb", [0xE9C9], pen, 600)

    # Grid Infill uniE9CA
    pen = TTGlyphPen(None)
    draw_rect(pen, 180, 120, 215, 580)
    draw_rect(pen, 385, 120, 420, 580)
    draw_rect(pen, 80, 240, 520, 275)
    draw_rect(pen, 80, 425, 520, 460)
    register_glyph("print_infill_grid", [0xE9CA], pen, 600)

    # Clearance Fit Badges (FIT 0.15, FIT 0.25, FIT 0.40)
    def build_fit_badge(gname, cp, num_str):
        pen = TTGlyphPen(glyphSet=glyph_set)
        total_w = 1180
        draw_rounded_badge(pen, 30, 80, total_w - 30, 620, r=50, sw=30)
        # F-I-T
        pen.addComponent("F", (0.55, 0, 0, 0.55, 70, 140))
        pen.addComponent("I", (0.55, 0, 0, 0.55, 230, 140))
        pen.addComponent("T", (0.55, 0, 0, 0.55, 330, 140))
        # 0.xx
        pen.addComponent("zero", (0.55, 0, 0, 0.55, 530, 140))
        pen.addComponent("period", (0.55, 0, 0, 0.55, 730, 140))
        # 15 / 25 / 40
        if num_str == "15":
            pen.addComponent("one", (0.55, 0, 0, 0.55, 840, 140))
            pen.addComponent("five", (0.55, 0, 0, 0.55, 990, 140))
        elif num_str == "25":
            pen.addComponent("two", (0.55, 0, 0, 0.55, 840, 140))
            pen.addComponent("five", (0.55, 0, 0, 0.55, 990, 140))
        else:
            pen.addComponent("four", (0.55, 0, 0, 0.55, 840, 140))
            pen.addComponent("zero", (0.55, 0, 0, 0.55, 990, 140))
        register_glyph(gname, [cp], pen, total_w)

    build_fit_badge("print_fit_tight", 0xE9CB, "15")
    build_fit_badge("print_fit_slide", 0xE9CC, "25")
    build_fit_badge("print_fit_loose", 0xE9CD, "40")

    # Material Badges ([PLA], [PETG], [ABS], [TPU], [RESIN])
    def build_mat_badge(gname, cp, letters, total_w):
        pen = TTGlyphPen(glyphSet=glyph_set)
        draw_rounded_badge(pen, 30, 80, total_w - 30, 620, r=50, sw=30)
        cur_x = 75
        for l_char in letters:
            adv = hmtx.metrics.get(l_char, (550, 40))[0]
            s = 0.58
            pen.addComponent(l_char, (s, 0, 0, s, cur_x, 140))
            cur_x += int(adv * s) + 12
        register_glyph(gname, [cp], pen, total_w)

    build_mat_badge("print_mat_pla", 0xE9CE, ["P", "L", "A"], 760)
    build_mat_badge("print_mat_petg", 0xE9CF, ["P", "E", "T", "G"], 940)
    build_mat_badge("print_mat_abs", 0xE9D0, ["A", "B", "S"], 760)
    build_mat_badge("print_mat_tpu", 0xE9D1, ["T", "P", "U"], 760)
    build_mat_badge("print_mat_resin", 0xE9D2, ["R", "E", "S", "I", "N"], 1080)

    # First-Layer Elephant's Foot Compensation uniE9D3
    pen = TTGlyphPen(None)
    # Build plate surface
    draw_rect(pen, 40, 60, 560, 95)
    # Flared foot squish
    pen.moveTo((120, 95))
    pen.lineTo((100, 160))
    pen.lineTo((180, 160))
    pen.lineTo((180, 480))
    pen.lineTo((420, 480))
    pen.lineTo((420, 160))
    pen.lineTo((500, 160))
    pen.lineTo((480, 95))
    pen.closePath()
    register_glyph("print_elephants_foot", [0xE9D3], pen, 600)

    # -------------------------------------------------------------
    # 6. Metadata & SemVer 3.100 OFL 1.1 Licensing
    # -------------------------------------------------------------
    print("\n6. Updating OpenType metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Press"
    ps_name = "PocketGull-Press"
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = font["name"]
    name_table.names = [n for n in name_table.names if n.nameID not in [0, 1, 2, 3, 4, 5, 6, 16, 17, 25]]
    def add_n(nid, val):
        name_table.addMultilingualName({"en": val}, font, nameID=nid)

    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, "Regular")
    add_n(3, f"3.100;POCK;{ps_name}")
    add_n(4, family_name)
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(16, family_name)
    add_n(17, "Regular")
    add_n(25, "PocketGull")

    if "OS/2" in font:
        font["OS/2"].achVendID = "POCK"

    # OTS 2-byte word boundary and bit-7 flag clearing
    glyf_table = font["glyf"]
    for gname in glyph_order:
        g = glyf_table[gname]
        data = g.compile(glyf_table)
        if len(data) % 2 != 0:
            if g.numberOfContours > 0:
                g.flags[-1] &= 0x3F

    # -------------------------------------------------------------
    # 7. Save TTF and Compress WOFF2
    # -------------------------------------------------------------
    print(f"\n7. Saving TrueType binary: {OUT_TTF}")
    font.save(OUT_TTF)
    shutil.copyfile(OUT_TTF, ROOT_TTF)

    print(f"8. Compressing WOFF2 binary via Brotli quality 11: {OUT_WOFF2}")
    compress(OUT_TTF, OUT_WOFF2)
    shutil.copyfile(OUT_WOFF2, ROOT_WOFF2)

    ttf_sz = os.path.getsize(OUT_TTF)
    woff2_sz = os.path.getsize(OUT_WOFF2)
    print(f"   • Output TTF:   {OUT_TTF} ({ttf_sz:,} bytes)")
    print(f"   • Output WOFF2: {OUT_WOFF2} ({woff2_sz:,} bytes)")
    print("=" * 76)
    print("  [SUCCESS] PocketGull Press OpenType Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_press_font()
