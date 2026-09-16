#!/usr/bin/env python3
"""
PocketGull Typefoundry: Computer Science & Algorithm Font Compiler
==================================================================
Compiles 'PocketGull-Algo.ttf' and 'PocketGull-Algo.woff2'
World's First Humanist Clinical & CS Monospace Typeface
"""

import os
import sys
import math
import shutil
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

SRC_MONO = os.path.join(TTF_DIR, "PocketGullMono-Regular.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Algo.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Algo.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Algo.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Algo.woff2")

ADVANCE = 600      # Strict 600 UPM fixed pitch monospace
STROKE_W = 68      # Standard stroke weight
hw = STROKE_W // 2

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

def build_algo_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: COMPUTER SCIENCE & ALGO COMPILER")
    print("=" * 76)

    if not os.path.isfile(SRC_MONO):
        print(f"[ERROR] Master monospace font missing: {SRC_MONO}")
        sys.exit(1)

    print("\n1. Loading master monospace font source...")
    font = TTFont(SRC_MONO)

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())

    def register_glyph(gname, codepoints, pen, adv=ADVANCE, lsb=None):
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        if lsb is None:
            lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (adv, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    print("\n2. Synthesizing Asymptotic Complexity (Big-O) Glyphs...")

    def draw_big_o(pen, cx=200, cy=360, rx=130, ry=240, sw=64):
        # Outer
        pen.moveTo((cx + rx, cy))
        pen.qCurveTo((cx + rx, cy + ry), (cx, cy + ry))
        pen.qCurveTo((cx - rx, cy + ry), (cx - rx, cy))
        pen.qCurveTo((cx - rx, cy - ry), (cx, cy - ry))
        pen.qCurveTo((cx + rx, cy - ry), (cx + rx, cy))
        pen.closePath()
        # Inner
        irx = rx - sw
        iry = ry - sw
        pen.moveTo((cx + irx, cy))
        pen.qCurveTo((cx + irx, cy - iry), (cx, cy - iry))
        pen.qCurveTo((cx - irx, cy - iry), (cx - irx, cy))
        pen.qCurveTo((cx - irx, cy + iry), (cx, cy + iry))
        pen.qCurveTo((cx + irx, cy + iry), (cx + irx, cy))
        pen.closePath()

    # Glyph 1: O(1) uniE950
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=200, cy=360, rx=130, ry=230, sw=52)
    draw_rect(pen, 380, 180, 420, 520)
    register_glyph("asymp_O_1", [0xE950], pen, ADVANCE)

    # Glyph 2: O(log n) uniE951
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=170, cy=360, rx=115, ry=220, sw=46)
    draw_rect(pen, 340, 180, 380, 480)
    draw_rect(pen, 340, 180, 520, 220)
    register_glyph("asymp_O_logn", [0xE951], pen, ADVANCE)

    # Glyph 3: O(n) uniE952
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=180, cy=360, rx=120, ry=220, sw=48)
    draw_rect(pen, 350, 180, 390, 420)
    draw_rect(pen, 460, 180, 500, 420)
    draw_rect(pen, 370, 380, 480, 420)
    register_glyph("asymp_O_n", [0xE952], pen, ADVANCE)

    # Glyph 4: O(n log n) uniE953
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=150, cy=360, rx=100, ry=200, sw=40)
    draw_rect(pen, 290, 180, 325, 420)
    draw_rect(pen, 375, 180, 410, 420)
    draw_rect(pen, 305, 385, 395, 420)
    draw_rect(pen, 460, 180, 495, 480)
    register_glyph("asymp_O_nlogn", [0xE953], pen, ADVANCE)

    # Glyph 5: O(n^2) uniE954
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=170, cy=360, rx=110, ry=210, sw=44)
    draw_rect(pen, 330, 180, 365, 390)
    draw_rect(pen, 415, 180, 450, 390)
    draw_rect(pen, 340, 355, 435, 390)
    draw_rect(pen, 480, 460, 540, 495)
    draw_rect(pen, 505, 400, 540, 460)
    draw_rect(pen, 475, 370, 540, 405)
    register_glyph("asymp_O_n2", [0xE954], pen, ADVANCE)

    # Glyph 6: O(2^n) uniE955
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=170, cy=360, rx=110, ry=210, sw=44)
    draw_rect(pen, 330, 180, 400, 215)
    draw_rect(pen, 330, 215, 365, 290)
    draw_rect(pen, 330, 290, 400, 325)
    draw_rect(pen, 365, 325, 400, 395)
    draw_rect(pen, 330, 365, 400, 400)
    draw_rect(pen, 450, 420, 475, 530)
    draw_rect(pen, 505, 420, 530, 530)
    draw_rect(pen, 460, 500, 520, 530)
    register_glyph("asymp_O_2n", [0xE955], pen, ADVANCE)

    # Glyph 7: Omega(1) uniE956
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 160, 190, 205)
    draw_rect(pen, 410, 160, 520, 205)
    draw_circle(pen, 300, 390, 180, clockwise=True)
    draw_circle(pen, 300, 390, 125, clockwise=False)
    draw_rect(pen, 280, 240, 320, 500)  # Inner 1
    register_glyph("asymp_Omega_1", [0xE956], pen, ADVANCE)

    # Glyph 8: Theta(n) uniE957
    pen = TTGlyphPen(None)
    draw_big_o(pen, cx=300, cy=360, rx=180, ry=230, sw=52)
    draw_rect(pen, 160, 335, 440, 385)
    register_glyph("asymp_Theta_n", [0xE957], pen, ADVANCE)

    print("\n3. Synthesizing AST Tree & Graph Connectors...")

    # Glyph 9: Tree Branch Junction ├── uniE958
    pen = TTGlyphPen(None)
    draw_rect(pen, 160, -200, 200, 800)
    draw_rect(pen, 160, 330, 600, 370)
    register_glyph("ast_branch_junction", [0xE958], pen, ADVANCE)

    # Glyph 10: Tree Leaf Junction └── uniE959
    pen = TTGlyphPen(None)
    draw_rect(pen, 160, 330, 200, 800)
    draw_rect(pen, 160, 330, 600, 370)
    register_glyph("ast_leaf_junction", [0xE959], pen, ADVANCE)

    # Glyph 11: Tree Trunk Pipe │ uniE95A
    pen = TTGlyphPen(None)
    draw_rect(pen, 160, -200, 200, 800)
    register_glyph("ast_trunk_pipe", [0xE95A], pen, ADVANCE)

    # Glyph 12: DAG Flow Triangle Arrow uniE95B
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 330, 400, 370)
    pen.moveTo((390, 230))
    pen.lineTo((520, 350))
    pen.lineTo((390, 470))
    pen.closePath()
    register_glyph("dag_flow_arrow", [0xE95B], pen, ADVANCE)

    print("\n4. Synthesizing Formal Semantics & Lambda Calculus...")

    # Glyph 13: Beta-Reduction Arrow →_β uniE95C
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 330, 420, 370)
    pen.moveTo((400, 250))
    pen.lineTo((500, 350))
    pen.lineTo((400, 450))
    pen.closePath()
    draw_rect(pen, 320, 100, 350, 260)
    draw_circle(pen, 380, 210, 50, clockwise=True)
    draw_circle(pen, 380, 210, 25, clockwise=False)
    draw_circle(pen, 380, 135, 45, clockwise=True)
    draw_circle(pen, 380, 135, 20, clockwise=False)
    register_glyph("semantics_beta_reduce", [0xE95C], pen, ADVANCE)

    # Glyph 14: Alpha-Equivalence ≡_α uniE95D
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 240, 340, 275)
    draw_rect(pen, 80, 320, 340, 355)
    draw_rect(pen, 80, 400, 340, 435)
    draw_circle(pen, 440, 220, 55, clockwise=True)
    draw_circle(pen, 440, 220, 30, clockwise=False)
    register_glyph("semantics_alpha_equiv", [0xE95D], pen, ADVANCE)

    # Glyph 15: Turnstile ⊢ U+22A2
    pen = TTGlyphPen(None)
    draw_rect(pen, 160, 140, 200, 600)
    draw_rect(pen, 190, 350, 480, 390)
    register_glyph("logic_turnstile", [0x22A2], pen, ADVANCE)

    # Glyph 16: Double Turnstile ⊨ U+22A8
    pen = TTGlyphPen(None)
    draw_rect(pen, 160, 140, 200, 600)
    draw_rect(pen, 190, 420, 480, 455)
    draw_rect(pen, 190, 320, 480, 355)
    register_glyph("logic_double_turnstile", [0x22A8], pen, ADVANCE)

    # Glyph 17: Semantic Brackets ⟦ U+27E6 & ⟧ U+27E7
    pen = TTGlyphPen(None)
    draw_rect(pen, 180, 100, 215, 620)
    draw_rect(pen, 245, 100, 280, 620)
    draw_rect(pen, 180, 585, 360, 620)
    draw_rect(pen, 180, 100, 360, 135)
    register_glyph("semantic_bracket_l", [0x27E6], pen, ADVANCE)

    pen = TTGlyphPen(None)
    draw_rect(pen, 385, 100, 420, 620)
    draw_rect(pen, 320, 100, 355, 620)
    draw_rect(pen, 240, 585, 420, 620)
    draw_rect(pen, 240, 100, 420, 135)
    register_glyph("semantic_bracket_r", [0x27E7], pen, ADVANCE)

    print("\n5. Synthesizing Memory & Endianness Indicators...")

    # Glyph 18: Little-Endian Flow →_LE uniE95F
    pen = TTGlyphPen(None)
    draw_rect(pen, 60, 340, 300, 375)
    pen.moveTo((290, 280))
    pen.lineTo((370, 357))
    pen.lineTo((290, 435))
    pen.closePath()
    draw_rect(pen, 400, 220, 430, 480)
    draw_rect(pen, 400, 220, 480, 255)
    draw_rect(pen, 500, 220, 530, 480)
    draw_rect(pen, 500, 445, 560, 480)
    draw_rect(pen, 500, 335, 550, 365)
    draw_rect(pen, 500, 220, 560, 255)
    register_glyph("mem_endian_le", [0xE95F], pen, ADVANCE)

    # Glyph 19: Big-Endian Flow ←_BE uniE960
    pen = TTGlyphPen(None)
    draw_rect(pen, 300, 340, 540, 375)
    pen.moveTo((310, 280))
    pen.lineTo((230, 357))
    pen.lineTo((310, 435))
    pen.closePath()
    draw_rect(pen, 60, 220, 90, 480)
    draw_rect(pen, 60, 445, 140, 480)
    draw_rect(pen, 60, 335, 135, 365)
    draw_rect(pen, 60, 220, 140, 255)
    draw_rect(pen, 130, 350, 150, 470)
    draw_rect(pen, 130, 230, 150, 350)
    register_glyph("mem_endian_be", [0xE960], pen, ADVANCE)

    print("\n6. Updating OpenType Tables & Metadata...")
    font.setGlyphOrder(glyph_order)

    # Update names
    name_table = font["name"]
    name_table.names = [n for n in name_table.names if n.nameID not in (1, 3, 4, 6)]
    
    def add_name(name_id, val):
        name_table.addName(val, platforms=((3, 1, 0x409), (1, 0, 0)), minNameID=name_id)

    add_name(1, "PocketGull Algo")
    add_name(3, "3.100;PGUL;PocketGullAlgo-Regular")
    add_name(4, "PocketGull Algo Regular")
    add_name(6, "PocketGullAlgo-Regular")

    # Post Table
    font["post"].isFixedPitch = 1
    font["OS/2"].panose.bProportion = 9

    # OTS loca byte alignment
    loca = font["loca"]
    glyf_table = font["glyf"]
    for gname in glyph_order:
        g = glyf_table[gname]
        data = g.compile(glyf_table)
        if len(data) % 2 != 0:
            if g.numberOfContours > 0:
                g.flags[-1] &= 0x3F

    print(f"\n7. Saving compiled TrueType binary: {OUT_TTF}")
    font.save(OUT_TTF)
    font.save(ROOT_TTF)

    print(f"8. Compressing WOFF2 binary via Brotli quality 11: {OUT_WOFF2}")
    compress(OUT_TTF, OUT_WOFF2)
    shutil.copy2(OUT_WOFF2, ROOT_WOFF2)

    print("\n[SUCCESS] PocketGull Algo compiled and compressed with zero errors!")

if __name__ == "__main__":
    build_algo_font()
