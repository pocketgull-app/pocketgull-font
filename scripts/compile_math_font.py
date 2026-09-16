#!/usr/bin/env python3
"""
PocketGull Typefoundry: Master OpenType Math Font Compiler
============================================================
Compiles 'PocketGull-Math.ttf' and 'PocketGull-Math.woff2'
World's First Humanist Clinical Sans-Serif OpenType Math Font
"""

import os
import sys
import math
import shutil
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

SRC_REGULAR = os.path.join(TTF_DIR, "PocketGull-Regular.ttf")
SRC_ITALIC = os.path.join(TTF_DIR, "PocketGull-Italic.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Math.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Math.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Math.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Math.woff2")

AXIS_HEIGHT = 260  # Mathematical centerline (half of x-height 520)
STROKE_W = 68      # Standard operator stroke weight
DEFAULT_ADV = 600  # Standard operator advance width

def draw_rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0))
    pen.lineTo((x1, y0))
    pen.lineTo((x1, y1))
    pen.lineTo((x0, y1))
    pen.closePath()

def draw_circle(pen, cx, cy, r, clockwise=False):
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
        pen.qCurveTo((cx - r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.closePath()

def create_glyph_from_pen(pen):
    return pen.glyph()

def build_math_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: OPENTYPE MATH SUPERFAMILY COMPILER")
    print("=" * 76)

    if not os.path.isfile(SRC_REGULAR) or not os.path.isfile(SRC_ITALIC):
        print(f"[ERROR] Master fonts missing: {SRC_REGULAR} or {SRC_ITALIC}")
        sys.exit(1)

    print("\n1. Loading master regular and italic sources...")
    font = TTFont(SRC_REGULAR)
    italic_font = TTFont(SRC_ITALIC)

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())

    # Map Italic Letters to Mathematical Alphanumerics (U+1D400-U+1D7FF)
    print("\n2. Synthesizing Mathematical Italic Latin & Greek alphanumerics...")
    ital_glyf = italic_font["glyf"]
    ital_hmtx = italic_font["hmtx"]
    ital_cmap = italic_font.getBestCmap()

    added_math_alphanumerics = 0

    # Math Italic Capital A-Z: U+1D434 - U+1D44D
    for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        codepoint = 0x1D434 + i
        src_cp = ord(ch)
        if src_cp in ital_cmap:
            src_gname = ital_cmap[src_cp]
            new_gname = f"math_ital_{ch}"
            if new_gname not in glyf:
                glyf[new_gname] = ital_glyf[src_gname]
                hmtx[new_gname] = ital_hmtx[src_gname]
                glyph_order.append(new_gname)
            cmap[codepoint] = new_gname
            added_math_alphanumerics += 1

    # Math Italic Small a-z: U+1D44E - U+1D467 (except h which is Planck U+210E)
    for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
        codepoint = 0x1D44E + i
        if ch == "h":
            codepoint = 0x210E
        src_cp = ord(ch)
        if src_cp in ital_cmap:
            src_gname = ital_cmap[src_cp]
            new_gname = f"math_ital_{ch}"
            if new_gname not in glyf:
                glyf[new_gname] = ital_glyf[src_gname]
                hmtx[new_gname] = ital_hmtx[src_gname]
                glyph_order.append(new_gname)
            cmap[codepoint] = new_gname
            added_math_alphanumerics += 1

    # Math Italic Greek Small alpha-omega: U+1D6FC - U+1D714
    greek_small = [
        ("alpha", 0x03B1, 0x1D6FC),
        ("beta", 0x03B2, 0x1D6FD),
        ("gamma", 0x03B3, 0x1D6FE),
        ("delta", 0x03B4, 0x1D6FF),
        ("epsilon", 0x03B5, 0x1D700),
        ("zeta", 0x03B6, 0x1D701),
        ("eta", 0x03B7, 0x1D702),
        ("theta", 0x03B8, 0x1D703),
        ("iota", 0x03B9, 0x1D704),
        ("kappa", 0x03BA, 0x1D705),
        ("lambda", 0x03BB, 0x1D706),
        ("mu", 0x03BC, 0x1D707),
        ("nu", 0x03BD, 0x1D708),
        ("xi", 0x03BE, 0x1D709),
        ("pi", 0x03C0, 0x1D70B),
        ("rho", 0x03C1, 0x1D70C),
        ("sigma", 0x03C3, 0x1D70E),
        ("tau", 0x03C4, 0x1D70F),
        ("upsilon", 0x03C5, 0x1D710),
        ("phi", 0x03C6, 0x1D711),
        ("chi", 0x03C7, 0x1D712),
        ("psi", 0x03C8, 0x1D713),
        ("omega", 0x03C9, 0x1D714),
    ]
    for g_name, src_cp, target_cp in greek_small:
        if src_cp in ital_cmap:
            src_gname = ital_cmap[src_cp]
            new_gname = f"math_ital_{g_name}"
            if new_gname not in glyf:
                glyf[new_gname] = ital_glyf[src_gname]
                hmtx[new_gname] = ital_hmtx[src_gname]
                glyph_order.append(new_gname)
            cmap[target_cp] = new_gname
            added_math_alphanumerics += 1

    # Math Italic Greek Capitals: U+1D6E4 - U+1D6F9
    greek_caps = [
        ("Gamma", 0x0393, 0x1D6E4),
        ("Delta", 0x0394, 0x1D6E5),
        ("Theta", 0x0398, 0x1D6E9),
        ("Lambda", 0x039B, 0x1D6EC),
        ("Xi", 0x039E, 0x1D6EF),
        ("Pi", 0x03A0, 0x1D6F1),
        ("Sigma", 0x03A3, 0x1D6F4),
        ("Upsilon", 0x03A5, 0x1D6F6),
        ("Phi", 0x03A6, 0x1D6F7),
        ("Psi", 0x03A8, 0x1D6F8),
        ("Omega", 0x03A9, 0x1D6F9),
    ]
    for g_name, src_cp, target_cp in greek_caps:
        if src_cp in ital_cmap:
            src_gname = ital_cmap[src_cp]
            new_gname = f"math_ital_{g_name}"
            if new_gname not in glyf:
                glyf[new_gname] = ital_glyf[src_gname]
                hmtx[new_gname] = ital_hmtx[src_gname]
                glyph_order.append(new_gname)
            cmap[target_cp] = new_gname
            added_math_alphanumerics += 1

    print(f"   • Synthesized {added_math_alphanumerics} Mathematical Italic letterforms (Latin + Greek).")

    # 3. Procedural Mathematical Operator Synthesis
    print("\n3. Procedurally synthesizing 64+ Mathematical Operators & Relations...")

    def register_op(gname, codepoints, pen, adv=DEFAULT_ADV, lsb=None):
        g = create_glyph_from_pen(pen)
        glyf[gname] = g
        g.recalcBounds(glyf)
        if lsb is None:
            lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (adv, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    hw = STROKE_W // 2

    # Operator 1: plus (+) U+002B
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    draw_rect(pen, 300 - hw, AXIS_HEIGHT - 200, 300 + hw, AXIS_HEIGHT + 200)
    register_op("plus", [0x002B], pen, 600)

    # Operator 2: minus (−) U+2212
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    register_op("minus", [0x2212], pen, 600)

    # Operator 3: equal (=) U+003D
    pen = TTGlyphPen(None)
    gap = 70
    draw_rect(pen, 100, AXIS_HEIGHT + gap - hw, 500, AXIS_HEIGHT + gap + hw)
    draw_rect(pen, 100, AXIS_HEIGHT - gap - hw, 500, AXIS_HEIGHT - gap + hw)
    register_op("equal", [0x003D], pen, 600)

    # Operator 4: not equal (≠) U+2260
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT + gap - hw, 500, AXIS_HEIGHT + gap + hw)
    draw_rect(pen, 100, AXIS_HEIGHT - gap - hw, 500, AXIS_HEIGHT - gap + hw)
    pen.moveTo((380 - hw, AXIS_HEIGHT + 220))
    pen.lineTo((380 + hw, AXIS_HEIGHT + 220))
    pen.lineTo((220 + hw, AXIS_HEIGHT - 220))
    pen.lineTo((220 - hw, AXIS_HEIGHT - 220))
    pen.closePath()
    register_op("notequal", [0x2260], pen, 600)

    # Operator 5: multiply (×) U+00D7
    pen = TTGlyphPen(None)
    rad = 170
    cos45 = 0.7071
    cx, cy = 300, AXIS_HEIGHT
    d = int(rad * cos45)
    sw = int(hw * cos45)
    pen.moveTo((cx - d - sw, cy + d - sw))
    pen.lineTo((cx - d + sw, cy + d + sw))
    pen.lineTo((cx + d + sw, cy - d + sw))
    pen.lineTo((cx + d - sw, cy - d - sw))
    pen.closePath()
    pen.moveTo((cx - d + sw, cy - d - sw))
    pen.lineTo((cx - d - sw, cy - d + sw))
    pen.lineTo((cx + d - sw, cy + d + sw))
    pen.lineTo((cx + d + sw, cy + d - sw))
    pen.closePath()
    register_op("multiply", [0x00D7], pen, 600)

    # Operator 6: divide (÷) U+00F7
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    draw_circle(pen, 300, AXIS_HEIGHT + 130, 42)
    draw_circle(pen, 300, AXIS_HEIGHT - 130, 42)
    register_op("divide", [0x00F7], pen, 600)

    # Operator 7: plus-minus (±) U+00B1
    pen = TTGlyphPen(None)
    c_y = AXIS_HEIGHT + 60
    draw_rect(pen, 120, c_y - hw, 480, c_y + hw)
    draw_rect(pen, 300 - hw, c_y - 150, 300 + hw, c_y + 150)
    draw_rect(pen, 120, AXIS_HEIGHT - 170 - hw, 480, AXIS_HEIGHT - 170 + hw)
    register_op("plusminus", [0x00B1], pen, 600)

    # Operator 8: minus-plus (∓) U+2213
    pen = TTGlyphPen(None)
    c_y = AXIS_HEIGHT - 60
    draw_rect(pen, 120, AXIS_HEIGHT + 170 - hw, 480, AXIS_HEIGHT + 170 + hw)
    draw_rect(pen, 120, c_y - hw, 480, c_y + hw)
    draw_rect(pen, 300 - hw, c_y - 150, 300 + hw, c_y + 150)
    register_op("minusplus", [0x2213], pen, 600)

    # Operator 9: approx equal (≈) U+2248
    pen = TTGlyphPen(None)
    def draw_tilde(y_off):
        pen.moveTo((100, y_off))
        pen.qCurveTo((180, y_off + 70), (280, y_off))
        pen.qCurveTo((380, y_off - 70), (480, y_off))
        pen.lineTo((480, y_off + STROKE_W))
        pen.qCurveTo((380, y_off - 70 + STROKE_W), (280, y_off + STROKE_W))
        pen.qCurveTo((180, y_off + 70 + STROKE_W), (100, y_off + STROKE_W))
        pen.closePath()
    draw_tilde(AXIS_HEIGHT + 45)
    draw_tilde(AXIS_HEIGHT - 75)
    register_op("approxequal", [0x2248], pen, 600)

    # Operator 10: less than (<) U+003C & greater than (>) U+003E
    pen = TTGlyphPen(None)
    pen.moveTo((460, AXIS_HEIGHT + 180))
    pen.lineTo((140, AXIS_HEIGHT))
    pen.lineTo((460, AXIS_HEIGHT - 180))
    pen.lineTo((460, AXIS_HEIGHT - 180 + STROKE_W + 15))
    pen.lineTo((190, AXIS_HEIGHT))
    pen.lineTo((460, AXIS_HEIGHT + 180 - STROKE_W - 15))
    pen.closePath()
    register_op("less", [0x003C], pen, 600)

    pen = TTGlyphPen(None)
    pen.moveTo((140, AXIS_HEIGHT + 180))
    pen.lineTo((460, AXIS_HEIGHT))
    pen.lineTo((140, AXIS_HEIGHT - 180))
    pen.lineTo((140, AXIS_HEIGHT - 180 + STROKE_W + 15))
    pen.lineTo((410, AXIS_HEIGHT))
    pen.lineTo((140, AXIS_HEIGHT + 180 - STROKE_W - 15))
    pen.closePath()
    register_op("greater", [0x003E], pen, 600)

    # Operator 11: less-than-or-equal (≤) U+2264 & greater-than-or-equal (≥) U+2265
    pen = TTGlyphPen(None)
    pen.moveTo((460, AXIS_HEIGHT + 200))
    pen.lineTo((140, AXIS_HEIGHT + 40))
    pen.lineTo((460, AXIS_HEIGHT - 120))
    pen.lineTo((460, AXIS_HEIGHT - 120 + STROKE_W + 15))
    pen.lineTo((190, AXIS_HEIGHT + 40))
    pen.lineTo((460, AXIS_HEIGHT + 200 - STROKE_W - 15))
    pen.closePath()
    draw_rect(pen, 140, AXIS_HEIGHT - 190 - hw, 460, AXIS_HEIGHT - 190 + hw)
    register_op("lessequal", [0x2264], pen, 600)

    pen = TTGlyphPen(None)
    pen.moveTo((140, AXIS_HEIGHT + 200))
    pen.lineTo((460, AXIS_HEIGHT + 40))
    pen.lineTo((140, AXIS_HEIGHT - 120))
    pen.lineTo((140, AXIS_HEIGHT - 120 + STROKE_W + 15))
    pen.lineTo((410, AXIS_HEIGHT + 40))
    pen.lineTo((140, AXIS_HEIGHT + 200 - STROKE_W - 15))
    pen.closePath()
    draw_rect(pen, 140, AXIS_HEIGHT - 190 - hw, 460, AXIS_HEIGHT - 190 + hw)
    register_op("greaterequal", [0x2265], pen, 600)

    # Operator 12: integral (∫) U+222B
    pen = TTGlyphPen(None)
    pen.moveTo((420, 680))
    pen.qCurveTo((420, 760), (320, 760))
    pen.qCurveTo((220, 760), (220, 640))
    pen.lineTo((220, -40))
    pen.qCurveTo((220, -160), (120, -160))
    pen.qCurveTo((20, -160), (20, -80))
    pen.lineTo((20 + STROKE_W, -80))
    pen.qCurveTo((20 + STROKE_W, -120), (100, -120))
    pen.qCurveTo((160, -120), (160, 0))
    pen.lineTo((160, 600))
    pen.qCurveTo((160, 720), (280, 720))
    pen.qCurveTo((360, 720), (360, 680))
    pen.closePath()
    register_op("integral", [0x222B], pen, 450)

    # Operator 13: double integral (∬) U+222C
    pen = TTGlyphPen(None)
    for shift in [0, 200]:
        pen.moveTo((260 + shift, 680))
        pen.qCurveTo((260 + shift, 760), (200 + shift, 760))
        pen.qCurveTo((140 + shift, 760), (140 + shift, 640))
        pen.lineTo((140 + shift, -40))
        pen.qCurveTo((140 + shift, -160), (80 + shift, -160))
        pen.qCurveTo((20 + shift, -160), (20 + shift, -80))
        pen.lineTo((20 + shift + STROKE_W, -80))
        pen.qCurveTo((20 + shift + STROKE_W, -120), (70 + shift, -120))
        pen.qCurveTo((100 + shift, -120), (100 + shift, 0))
        pen.lineTo((100 + shift, 600))
        pen.qCurveTo((100 + shift, 720), (180 + shift, 720))
        pen.qCurveTo((220 + shift, 720), (220 + shift, 680))
        pen.closePath()
    register_op("iint", [0x222C], pen, 650)

    # Operator 14: summation (∑) U+2211
    pen = TTGlyphPen(None)
    pen.moveTo((480, 700))
    pen.lineTo((120, 700))
    pen.lineTo((290, AXIS_HEIGHT))
    pen.lineTo((120, -80))
    pen.lineTo((480, -80))
    pen.lineTo((480, -80 + STROKE_W))
    pen.lineTo((200, -80 + STROKE_W))
    pen.lineTo((340, AXIS_HEIGHT))
    pen.lineTo((200, 700 - STROKE_W))
    pen.lineTo((480, 700 - STROKE_W))
    pen.closePath()
    register_op("summation", [0x2211], pen, 600)

    # Operator 15: product (∏) U+220F
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, 632, 500, 700)
    draw_rect(pen, 160, -80, 160 + STROKE_W, 640)
    draw_rect(pen, 440 - STROKE_W, -80, 440, 640)
    register_op("product", [0x220F], pen, 600)

    # Operator 16: partial differential (∂) U+2202
    pen = TTGlyphPen(None)
    pen.moveTo((420, 680))
    pen.qCurveTo((300, 680), (240, 560))
    pen.lineTo((240, 360))
    pen.qCurveTo((160, 360), (100, 260))
    pen.qCurveTo((60, 180), (60, 100))
    pen.qCurveTo((60, 0), (150, 0))
    pen.qCurveTo((260, 0), (320, 100))
    pen.lineTo((320, 480))
    pen.qCurveTo((340, 620), (420, 620))
    pen.closePath()
    pen.moveTo((240, 100))
    pen.lineTo((240, 260))
    pen.qCurveTo((160, 260), (140, 180))
    pen.qCurveTo((140, 100), (240, 100))
    pen.closePath()
    register_op("partialdiff", [0x2202], pen, 550)

    # Operator 17: nabla (∇) U+2207
    pen = TTGlyphPen(None)
    pen.moveTo((100, 680))
    pen.lineTo((500, 680))
    pen.lineTo((300, 60))
    pen.closePath()
    pen.moveTo((300, 180))
    pen.lineTo((420, 612))
    pen.lineTo((180, 612))
    pen.closePath()
    register_op("nabla", [0x2207], pen, 600)

    # Operator 18: square root (√) U+221A
    pen = TTGlyphPen(None)
    pen.moveTo((80, AXIS_HEIGHT))
    pen.lineTo((140, AXIS_HEIGHT))
    pen.lineTo((220, 20))
    pen.lineTo((360, 720))
    pen.lineTo((580, 720))
    pen.lineTo((580, 720 - STROKE_W))
    pen.lineTo((390, 720 - STROKE_W))
    pen.lineTo((240, -40))
    pen.lineTo((190, -40))
    pen.lineTo((110, AXIS_HEIGHT - 60))
    pen.lineTo((80, AXIS_HEIGHT - 60))
    pen.closePath()
    register_op("radical", [0x221A], pen, 620)

    # Operator 19: infinity (∞) U+221E
    pen = TTGlyphPen(None)
    draw_circle(pen, 200, AXIS_HEIGHT, 150)
    draw_circle(pen, 500, AXIS_HEIGHT, 150)
    draw_circle(pen, 200, AXIS_HEIGHT, 90)
    draw_circle(pen, 500, AXIS_HEIGHT, 90)
    register_op("infinity", [0x221E], pen, 700)

    # Operator 20: element of (∈) U+2208
    pen = TTGlyphPen(None)
    pen.moveTo((450, AXIS_HEIGHT + 180))
    pen.lineTo((450, AXIS_HEIGHT + 180 - STROKE_W))
    pen.qCurveTo((200, AXIS_HEIGHT + 180 - STROKE_W), (200, AXIS_HEIGHT))
    pen.qCurveTo((200, AXIS_HEIGHT - 180 + STROKE_W), (450, AXIS_HEIGHT - 180 + STROKE_W))
    pen.lineTo((450, AXIS_HEIGHT - 180))
    pen.qCurveTo((120, AXIS_HEIGHT - 180), (120, AXIS_HEIGHT))
    pen.qCurveTo((120, AXIS_HEIGHT + 180), (450, AXIS_HEIGHT + 180))
    pen.closePath()
    draw_rect(pen, 170, AXIS_HEIGHT - hw, 450, AXIS_HEIGHT + hw)
    register_op("element", [0x2208], pen, 550)

    # Operator 21: subset (⊂) U+2282
    pen = TTGlyphPen(None)
    pen.moveTo((450, AXIS_HEIGHT + 180))
    pen.lineTo((450, AXIS_HEIGHT + 180 - STROKE_W))
    pen.qCurveTo((200, AXIS_HEIGHT + 180 - STROKE_W), (200, AXIS_HEIGHT))
    pen.qCurveTo((200, AXIS_HEIGHT - 180 + STROKE_W), (450, AXIS_HEIGHT - 180 + STROKE_W))
    pen.lineTo((450, AXIS_HEIGHT - 180))
    pen.qCurveTo((120, AXIS_HEIGHT - 180), (120, AXIS_HEIGHT))
    pen.qCurveTo((120, AXIS_HEIGHT + 180), (450, AXIS_HEIGHT + 180))
    pen.closePath()
    register_op("subset", [0x2282], pen, 550)

    # Operator 22: union (∪) U+222A & intersection (∩) U+2229
    pen = TTGlyphPen(None)
    pen.moveTo((120, AXIS_HEIGHT + 180))
    pen.lineTo((120 + STROKE_W, AXIS_HEIGHT + 180))
    pen.lineTo((120 + STROKE_W, AXIS_HEIGHT - 60))
    pen.qCurveTo((120 + STROKE_W, AXIS_HEIGHT - 180 + STROKE_W), (300, AXIS_HEIGHT - 180 + STROKE_W))
    pen.qCurveTo((480 - STROKE_W, AXIS_HEIGHT - 180 + STROKE_W), (480 - STROKE_W, AXIS_HEIGHT - 60))
    pen.lineTo((480 - STROKE_W, AXIS_HEIGHT + 180))
    pen.lineTo((480, AXIS_HEIGHT + 180))
    pen.lineTo((480, AXIS_HEIGHT - 60))
    pen.qCurveTo((480, AXIS_HEIGHT - 180), (300, AXIS_HEIGHT - 180))
    pen.qCurveTo((120, AXIS_HEIGHT - 180), (120, AXIS_HEIGHT - 60))
    pen.closePath()
    register_op("union", [0x222A], pen, 600)

    pen = TTGlyphPen(None)
    pen.moveTo((120, AXIS_HEIGHT - 180))
    pen.lineTo((120 + STROKE_W, AXIS_HEIGHT - 180))
    pen.lineTo((120 + STROKE_W, AXIS_HEIGHT + 60))
    pen.qCurveTo((120 + STROKE_W, AXIS_HEIGHT + 180 - STROKE_W), (300, AXIS_HEIGHT + 180 - STROKE_W))
    pen.qCurveTo((480 - STROKE_W, AXIS_HEIGHT + 180 - STROKE_W), (480 - STROKE_W, AXIS_HEIGHT + 60))
    pen.lineTo((480 - STROKE_W, AXIS_HEIGHT - 180))
    pen.lineTo((480, AXIS_HEIGHT - 180))
    pen.lineTo((480, AXIS_HEIGHT + 60))
    pen.qCurveTo((480, AXIS_HEIGHT + 180), (300, AXIS_HEIGHT + 180))
    pen.qCurveTo((120, AXIS_HEIGHT + 180), (120, AXIS_HEIGHT + 60))
    pen.closePath()
    register_op("intersection", [0x2229], pen, 600)

    # Operator 23: for all (∀) U+2200 & there exists (∃) U+2203
    pen = TTGlyphPen(None)
    pen.moveTo((100, 680))
    pen.lineTo((100 + STROKE_W + 15, 680))
    pen.lineTo((300, 140))
    pen.lineTo((500 - STROKE_W - 15, 680))
    pen.lineTo((500, 680))
    pen.lineTo((300 + hw, 60))
    pen.lineTo((300 - hw, 60))
    pen.closePath()
    draw_rect(pen, 190, 400 - hw, 410, 400 + hw)
    register_op("forall", [0x2200], pen, 600)

    pen = TTGlyphPen(None)
    draw_rect(pen, 420 - STROKE_W, 60, 420, 680)
    draw_rect(pen, 160, 680 - STROKE_W, 420, 680)
    draw_rect(pen, 200, 370 - hw, 420, 370 + hw)
    draw_rect(pen, 160, 60, 420, 60 + STROKE_W)
    register_op("exists", [0x2203], pen, 550)

    # Operator 24: right arrow (→) U+2192 & left arrow (←) U+2190
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    pen.moveTo((520, AXIS_HEIGHT))
    pen.lineTo((340, AXIS_HEIGHT + 140))
    pen.lineTo((340, AXIS_HEIGHT + 140 - STROKE_W))
    pen.lineTo((460, AXIS_HEIGHT))
    pen.lineTo((340, AXIS_HEIGHT - 140 + STROKE_W))
    pen.lineTo((340, AXIS_HEIGHT - 140))
    pen.closePath()
    register_op("rightarrow", [0x2192], pen, 600)

    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 520, AXIS_HEIGHT + hw)
    pen.moveTo((80, AXIS_HEIGHT))
    pen.lineTo((260, AXIS_HEIGHT + 140))
    pen.lineTo((260, AXIS_HEIGHT + 140 - STROKE_W))
    pen.lineTo((140, AXIS_HEIGHT))
    pen.lineTo((260, AXIS_HEIGHT - 140 + STROKE_W))
    pen.lineTo((260, AXIS_HEIGHT - 140))
    pen.closePath()
    register_op("leftarrow", [0x2190], pen, 600)

    # Operator 25: double right arrow (⇒) U+21D2
    pen = TTGlyphPen(None)
    d_gap = 50
    draw_rect(pen, 80, AXIS_HEIGHT + d_gap - hw, 460, AXIS_HEIGHT + d_gap + hw)
    draw_rect(pen, 80, AXIS_HEIGHT - d_gap - hw, 460, AXIS_HEIGHT - d_gap + hw)
    pen.moveTo((540, AXIS_HEIGHT))
    pen.lineTo((360, AXIS_HEIGHT + 160))
    pen.lineTo((360, AXIS_HEIGHT + 160 - STROKE_W))
    pen.lineTo((480, AXIS_HEIGHT))
    pen.lineTo((360, AXIS_HEIGHT - 160 + STROKE_W))
    pen.lineTo((360, AXIS_HEIGHT - 160))
    pen.closePath()
    register_op("Rightarrow", [0x21D2], pen, 600)

    # Operator 25B: left-right arrow (↔) U+2194
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    pen.moveTo((540, AXIS_HEIGHT))
    pen.lineTo((400, AXIS_HEIGHT + 140))
    pen.lineTo((400, AXIS_HEIGHT + 140 - STROKE_W))
    pen.lineTo((480, AXIS_HEIGHT))
    pen.lineTo((400, AXIS_HEIGHT - 140 + STROKE_W))
    pen.lineTo((400, AXIS_HEIGHT - 140))
    pen.closePath()
    pen.moveTo((60, AXIS_HEIGHT))
    pen.lineTo((200, AXIS_HEIGHT + 140))
    pen.lineTo((200, AXIS_HEIGHT + 140 - STROKE_W))
    pen.lineTo((120, AXIS_HEIGHT))
    pen.lineTo((200, AXIS_HEIGHT - 140 + STROKE_W))
    pen.lineTo((200, AXIS_HEIGHT - 140))
    pen.closePath()
    register_op("leftrightarrow", [0x2194], pen, 600)

    # Operator 25C: chemical equilibrium paired harpoons (⇌) U+21CC & U+21CB
    pen = TTGlyphPen(None)
    y_up = AXIS_HEIGHT + 50
    draw_rect(pen, 80, y_up - hw, 480, y_up + hw)
    pen.moveTo((500, y_up))
    pen.lineTo((360, y_up + 120))
    pen.lineTo((360, y_up + 120 - STROKE_W))
    pen.lineTo((440, y_up))
    pen.closePath()
    y_dn = AXIS_HEIGHT - 50
    draw_rect(pen, 100, y_dn - hw, 500, y_dn + hw)
    pen.moveTo((80, y_dn))
    pen.lineTo((220, y_dn - 120))
    pen.lineTo((220, y_dn - 120 + STROKE_W))
    pen.lineTo((140, y_dn))
    pen.closePath()
    register_op("equilibrium", [0x21CC, 0x21CB], pen, 580)

    # Operator 25D: circled dot / Sun (⊙ / ☉) U+2299 & U+2609
    pen = TTGlyphPen(None)
    draw_circle(pen, 300, AXIS_HEIGHT, 170, clockwise=False)
    draw_circle(pen, 300, AXIS_HEIGHT, 170 - STROKE_W, clockwise=True)
    draw_circle(pen, 300, AXIS_HEIGHT, 48, clockwise=False)
    register_op("circdot_sun", [0x2299, 0x2609], pen, 600)

    # Operator 25E: circled plus / Earth (⊕ / ♁) U+2295 & U+2641
    pen = TTGlyphPen(None)
    draw_circle(pen, 300, AXIS_HEIGHT, 170, clockwise=False)
    draw_circle(pen, 300, AXIS_HEIGHT, 170 - STROKE_W, clockwise=True)
    draw_rect(pen, 300 - 170 + STROKE_W, AXIS_HEIGHT - hw, 300 + 170 - STROKE_W, AXIS_HEIGHT + hw)
    draw_rect(pen, 300 - hw, AXIS_HEIGHT - 170 + STROKE_W, 300 + hw, AXIS_HEIGHT + 170 - STROKE_W)
    register_op("circplus_earth", [0x2295, 0x2641], pen, 600)

    # Operator 25F: Jupiter symbol (♃) U+2643
    pen = TTGlyphPen(None)
    draw_rect(pen, 360 - hw, -60, 360 + hw, 600)
    draw_rect(pen, 200, 380 - hw, 480, 380 + hw)
    pen.moveTo((120, 200))
    pen.qCurveTo((120, 480), (360, 480))
    pen.lineTo((360, 480 - STROKE_W))
    pen.qCurveTo((120 + STROKE_W, 480 - STROKE_W), (120 + STROKE_W, 200))
    pen.closePath()
    register_op("jupiter", [0x2643], pen, 560)

    # Operator 25G: Saturn symbol (♄) U+2644
    pen = TTGlyphPen(None)
    draw_rect(pen, 200 - hw, 260, 200 + hw, 660)
    draw_rect(pen, 100, 520 - hw, 300, 520 + hw)
    pen.moveTo((200, 260))
    pen.qCurveTo((200, -60), (360, -60))
    pen.qCurveTo((480, -60), (480, 120))
    pen.lineTo((480 - STROKE_W, 120))
    pen.qCurveTo((480 - STROKE_W, -60 + STROKE_W), (360, -60 + STROKE_W))
    pen.qCurveTo((200 + STROKE_W, -60 + STROKE_W), (200 + STROKE_W, 260))
    pen.closePath()
    register_op("saturn", [0x2644], pen, 560)

    # Operator 26: Blackboard Bold (R, N, Z, C, Q)
    # R (Reals) U+211D
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 120, 700 - STROKE_W, 380, 700)
    pen.moveTo((380, 700))
    pen.qCurveTo((500, 700), (500, 520))
    pen.qCurveTo((500, 360), (360, 360))
    pen.lineTo((120, 360))
    pen.lineTo((120, 360 + STROKE_W))
    pen.lineTo((360, 360 + STROKE_W))
    pen.qCurveTo((430, 360 + STROKE_W), (430, 520))
    pen.qCurveTo((430, 700 - STROKE_W), (360, 700 - STROKE_W))
    pen.closePath()
    pen.moveTo((320, 360))
    pen.lineTo((480, 0))
    pen.lineTo((480 - STROKE_W - 20, 0))
    pen.lineTo((260, 360))
    pen.closePath()
    register_op("reals", [0x211D], pen, 620)

    # N (Naturals) U+2115 & U+1D545
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 460 - STROKE_W, 0, 460, 700)
    pen.moveTo((120 + STROKE_W * 2 + 35, 700))
    pen.lineTo((460 - STROKE_W, 0))
    pen.lineTo((460 - STROKE_W - STROKE_W, 0))
    pen.lineTo((120 + STROKE_W * 2 + 35 - STROKE_W, 700))
    pen.closePath()
    register_op("naturals", [0x2115, 0x1D545], pen, 580)

    # Z (Integers) U+2124 & U+1D551
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 700 - STROKE_W, 460, 700)
    draw_rect(pen, 120, 0, 460, STROKE_W)
    pen.moveTo((460, 700 - STROKE_W))
    pen.lineTo((460 - STROKE_W, 700 - STROKE_W))
    pen.lineTo((190, STROKE_W))
    pen.lineTo((190 + STROKE_W, STROKE_W))
    pen.closePath()
    pen.moveTo((390, 700 - STROKE_W))
    pen.lineTo((390 - STROKE_W, 700 - STROKE_W))
    pen.lineTo((120, STROKE_W))
    pen.lineTo((120 + STROKE_W, STROKE_W))
    pen.closePath()
    register_op("integers", [0x2124, 0x1D551], pen, 580)

    # C (Complex numbers) U+2102
    pen = TTGlyphPen(None)
    pen.moveTo((460, 580))
    pen.qCurveTo((380, 700), (280, 700))
    pen.qCurveTo((120, 700), (120, 350))
    pen.qCurveTo((120, 0), (280, 0))
    pen.qCurveTo((380, 0), (460, 120))
    pen.lineTo((460 - STROKE_W, 160))
    pen.qCurveTo((360, STROKE_W), (280, STROKE_W))
    pen.qCurveTo((120 + STROKE_W, STROKE_W), (120 + STROKE_W, 350))
    pen.qCurveTo((120 + STROKE_W, 700 - STROKE_W), (280, 700 - STROKE_W))
    pen.qCurveTo((360, 700 - STROKE_W), (420, 560))
    pen.closePath()
    draw_rect(pen, 200, 120, 200 + STROKE_W, 580)
    register_op("complex", [0x2102], pen, 580)

    # Q (Rationals) U+211A & U+1D548
    pen = TTGlyphPen(None)
    pen.moveTo((480, 560))
    pen.qCurveTo((400, 700), (290, 700))
    pen.qCurveTo((120, 700), (120, 350))
    pen.qCurveTo((120, 0), (290, 0))
    pen.qCurveTo((400, 0), (480, 140))
    pen.lineTo((480 - STROKE_W, 180))
    pen.qCurveTo((380, STROKE_W), (290, STROKE_W))
    pen.qCurveTo((120 + STROKE_W, STROKE_W), (120 + STROKE_W, 350))
    pen.qCurveTo((120 + STROKE_W, 700 - STROKE_W), (290, 700 - STROKE_W))
    pen.qCurveTo((380, 700 - STROKE_W), (440, 540))
    pen.closePath()
    draw_rect(pen, 200, 120, 200 + STROKE_W, 580)
    pen.moveTo((310, 150))
    pen.lineTo((490, -80))
    pen.lineTo((430, -80))
    pen.lineTo((260, 100))
    pen.closePath()
    register_op("rationals", [0x211A, 0x1D548], pen, 600)

    # P (Probability / Primes) U+2119 & U+1D547
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 120, 700 - STROKE_W, 360, 700)
    pen.moveTo((360, 700))
    pen.qCurveTo((490, 700), (490, 530))
    pen.qCurveTo((490, 360), (360, 360))
    pen.lineTo((120, 360))
    pen.lineTo((120, 360 + STROKE_W))
    pen.lineTo((360, 360 + STROKE_W))
    pen.qCurveTo((420, 360 + STROKE_W), (420, 530))
    pen.qCurveTo((420, 700 - STROKE_W), (360, 700 - STROKE_W))
    pen.closePath()
    register_op("probability", [0x2119, 0x1D547], pen, 580)

    # E (Expectation) U+2147 & U+1D53C
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 120, 700 - STROKE_W, 460, 700)
    draw_rect(pen, 120, 350 - hw, 380, 350 + hw)
    draw_rect(pen, 120, 0, 460, STROKE_W)
    register_op("expectation", [0x2147, 0x1D53C], pen, 580)

    # H (Quaternions / Upper Half-Plane) U+210D & U+1D53F
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 460 - STROKE_W * 2 - 35, 0, 460 - STROKE_W - 35, 700)
    draw_rect(pen, 460 - STROKE_W, 0, 460, 700)
    draw_rect(pen, 120, 350 - hw, 460, 350 + hw)
    register_op("quaternions", [0x210D, 0x1D53F], pen, 600)

    # F (Field) U+1D53D
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, 0, 120 + STROKE_W, 700)
    draw_rect(pen, 120 + STROKE_W + 35, 0, 120 + STROKE_W * 2 + 35, 700)
    draw_rect(pen, 120, 700 - STROKE_W, 440, 700)
    draw_rect(pen, 120, 350 - hw, 360, 350 + hw)
    register_op("field", [0x1D53D], pen, 560)

    # 1 (Blackboard Indicator Function) U+1D7D9
    pen = TTGlyphPen(None)
    draw_rect(pen, 240, 0, 240 + STROKE_W, 700)
    draw_rect(pen, 240 + STROKE_W + 30, 0, 240 + STROKE_W * 2 + 30, 700)
    draw_rect(pen, 140, 0, 440, STROKE_W)
    draw_rect(pen, 150, 590, 240, 590 + STROKE_W)
    register_op("indicator1", [0x1D7D9], pen, 520)

    # Multi-Size Vertical Delimiters for MathVariants (.v1 to .v4)
    print("\n4. Synthesizing multi-size vertical delimiters (.v1 - .v4)...")
    height_steps = [1200, 1600, 2000, 2400]
    for idx, H in enumerate(height_steps, start=1):
        y_half = H // 2
        y_min = AXIS_HEIGHT - y_half
        y_max = AXIS_HEIGHT + y_half

        # parenleft.v{i}
        pen = TTGlyphPen(None)
        pen.moveTo((260, y_max))
        pen.qCurveTo((60, y_max - int((y_max - AXIS_HEIGHT) * 0.4)), (60, AXIS_HEIGHT))
        pen.qCurveTo((60, y_min + int((AXIS_HEIGHT - y_min) * 0.4)), (260, y_min))
        pen.lineTo((260 - STROKE_W, y_min))
        pen.qCurveTo((60 + STROKE_W, y_min + int((AXIS_HEIGHT - y_min) * 0.4)), (60 + STROKE_W, AXIS_HEIGHT))
        pen.qCurveTo((60 + STROKE_W, y_max - int((y_max - AXIS_HEIGHT) * 0.4)), (260 - STROKE_W, y_max))
        pen.closePath()
        register_op(f"parenleft.v{idx}", [], pen, 310, 60)

        # parenright.v{i}
        pen = TTGlyphPen(None)
        pen.moveTo((50, y_max))
        pen.qCurveTo((250, y_max - int((y_max - AXIS_HEIGHT) * 0.4)), (250, AXIS_HEIGHT))
        pen.qCurveTo((250, y_min + int((AXIS_HEIGHT - y_min) * 0.4)), (50, y_min))
        pen.lineTo((50 + STROKE_W, y_min))
        pen.qCurveTo((250 - STROKE_W, y_min + int((AXIS_HEIGHT - y_min) * 0.4)), (250 - STROKE_W, AXIS_HEIGHT))
        pen.qCurveTo((250 - STROKE_W, y_max - int((y_max - AXIS_HEIGHT) * 0.4)), (50 + STROKE_W, y_max))
        pen.closePath()
        register_op(f"parenright.v{idx}", [], pen, 300, 50)

        # bracketleft.v{i}
        pen = TTGlyphPen(None)
        draw_rect(pen, 80, y_min, 80 + STROKE_W, y_max)
        draw_rect(pen, 80, y_max - STROKE_W, 250, y_max)
        draw_rect(pen, 80, y_min, 250, y_min + STROKE_W)
        register_op(f"bracketleft.v{idx}", [], pen, 340, 80)

        # bracketright.v{i}
        pen = TTGlyphPen(None)
        draw_rect(pen, 250 - STROKE_W, y_min, 250, y_max)
        draw_rect(pen, 80, y_max - STROKE_W, 250, y_max)
        draw_rect(pen, 80, y_min, 250, y_min + STROKE_W)
        register_op(f"bracketright.v{idx}", [], pen, 330, 80)

        # braceleft.v{i}
        pen = TTGlyphPen(None)
        pen.moveTo((260, y_max))
        pen.qCurveTo((140, y_max), (140, y_max - 120))
        pen.lineTo((140, AXIS_HEIGHT + 90))
        pen.qCurveTo((140, AXIS_HEIGHT + 30), (60, AXIS_HEIGHT))
        pen.qCurveTo((140, AXIS_HEIGHT - 30), (140, AXIS_HEIGHT - 90))
        pen.lineTo((140, y_min + 120))
        pen.qCurveTo((140, y_min), (260, y_min))
        pen.lineTo((260, y_min + STROKE_W))
        pen.qCurveTo((140 + STROKE_W, y_min + STROKE_W), (140 + STROKE_W, y_min + 120))
        pen.lineTo((140 + STROKE_W, AXIS_HEIGHT - 90))
        pen.qCurveTo((140 + STROKE_W, AXIS_HEIGHT - 10), (60 + STROKE_W + 20, AXIS_HEIGHT))
        pen.qCurveTo((140 + STROKE_W, AXIS_HEIGHT + 10), (140 + STROKE_W, AXIS_HEIGHT + 90))
        pen.lineTo((140 + STROKE_W, y_max - 120))
        pen.qCurveTo((140 + STROKE_W, y_max - STROKE_W), (260, y_max - STROKE_W))
        pen.closePath()
        register_op(f"braceleft.v{idx}", [], pen, 380, 60)

        # braceright.v{i}
        pen = TTGlyphPen(None)
        pen.moveTo((80, y_max))
        pen.qCurveTo((200, y_max), (200, y_max - 120))
        pen.lineTo((200, AXIS_HEIGHT + 90))
        pen.qCurveTo((200, AXIS_HEIGHT + 30), (280, AXIS_HEIGHT))
        pen.qCurveTo((200, AXIS_HEIGHT - 30), (200, AXIS_HEIGHT - 90))
        pen.lineTo((200, y_min + 120))
        pen.qCurveTo((200, y_min), (80, y_min))
        pen.lineTo((80, y_min + STROKE_W))
        pen.qCurveTo((200 - STROKE_W, y_min + STROKE_W), (200 - STROKE_W, y_min + 120))
        pen.lineTo((200 - STROKE_W, AXIS_HEIGHT - 90))
        pen.qCurveTo((200 - STROKE_W, AXIS_HEIGHT - 10), (280 - STROKE_W - 20, AXIS_HEIGHT))
        pen.qCurveTo((200 - STROKE_W, AXIS_HEIGHT + 10), (200 - STROKE_W, AXIS_HEIGHT + 90))
        pen.lineTo((200 - STROKE_W, y_max - 120))
        pen.qCurveTo((200 - STROKE_W, y_max - STROKE_W), (80, y_max - STROKE_W))
        pen.closePath()
        register_op(f"braceright.v{idx}", [], pen, 380, 80)

        # radical.v{i}
        pen = TTGlyphPen(None)
        pen.moveTo((80, AXIS_HEIGHT))
        pen.lineTo((140, AXIS_HEIGHT))
        pen.lineTo((220, y_min + 100))
        pen.lineTo((360, y_max))
        pen.lineTo((600, y_max))
        pen.lineTo((600, y_max - STROKE_W))
        pen.lineTo((390, y_max - STROKE_W))
        pen.lineTo((240, y_min + 40))
        pen.lineTo((190, y_min + 40))
        pen.lineTo((110, AXIS_HEIGHT - 60))
        pen.lineTo((80, AXIS_HEIGHT - 60))
        pen.closePath()
        register_op(f"radical.v{idx}", [], pen, 640, 80)

    font.setGlyphOrder(glyph_order)
    print("   • Synthesized 32 core mathematical operators, blackboard letters, and stepped delimiters.")

    # 5. Construct OpenType MATH Table
    print("\n5. Constructing ISO/IEC 14496-22 OpenType MATH Table...")
    math_table = otTables.MATH()
    math_table.Version = 0x00010000

    mc = otTables.MathConstants()
    mc.ScriptPercentScaleDown = 70
    mc.ScriptScriptPercentScaleDown = 52
    mc.DelimitedSubFormulaMinHeight = 1500
    mc.DisplayOperatorMinHeight = 1400

    math_value_records = {
        'MathLeading': 150,
        'AxisHeight': AXIS_HEIGHT,
        'AccentBaseHeight': 520,
        'FlattenedAccentBaseHeight': 520,
        'SubscriptShiftDown': 200,
        'SubscriptTopMax': 400,
        'SubscriptBaselineDropMin': 180,
        'SuperscriptShiftUp': 350,
        'SuperscriptShiftUpCramped': 300,
        'SuperscriptBottomMin': 120,
        'SuperscriptBaselineDropMax': 220,
        'SubSuperscriptGapMin': 100,
        'SuperscriptBottomMaxWithSubscript': 350,
        'SpaceAfterScript': 50,
        'UpperLimitGapMin': 150,
        'UpperLimitBaselineRiseMin': 200,
        'LowerLimitGapMin': 150,
        'LowerLimitBaselineDropMin': 200,
        'StackTopShiftUp': 400,
        'StackTopDisplayStyleShiftUp': 500,
        'StackBottomShiftDown': 200,
        'StackBottomDisplayStyleShiftDown': 350,
        'StackGapMin': 150,
        'StackDisplayStyleGapMin': 250,
        'StretchStackTopShiftUp': 400,
        'StretchStackBottomShiftDown': 200,
        'StretchStackGapAboveMin': 150,
        'StretchStackGapBelowMin': 150,
        'FractionNumeratorShiftUp': 400,
        'FractionNumeratorDisplayStyleShiftUp': 550,
        'FractionDenominatorShiftDown': 250,
        'FractionDenominatorDisplayStyleShiftDown': 400,
        'FractionNumeratorGapMin': 100,
        'FractionNumDisplayStyleGapMin': 180,
        'FractionRuleThickness': STROKE_W,
        'FractionDenominatorGapMin': 100,
        'FractionDenomDisplayStyleGapMin': 180,
        'SkewedFractionHorizontalGap': 250,
        'SkewedFractionVerticalGap': 100,
        'OverbarVerticalGap': 120,
        'OverbarRuleThickness': STROKE_W,
        'OverbarExtraAscender': 50,
        'UnderbarVerticalGap': 120,
        'UnderbarRuleThickness': STROKE_W,
        'UnderbarExtraDescender': 50,
        'RadicalVerticalGap': 120,
        'RadicalDisplayStyleVerticalGap': 180,
        'RadicalRuleThickness': STROKE_W,
        'RadicalExtraAscender': 50,
        'RadicalKernBeforeDegree': 100,
        'RadicalKernAfterDegree': -250,
    }

    for name, val in math_value_records.items():
        rec = otTables.MathValueRecord()
        rec.Value = val
        setattr(mc, name, rec)
    mc.RadicalDegreeBottomRaisePercent = 60
    math_table.MathConstants = mc

    # 5B. MathGlyphInfo: Italic Correction & Top Accent Attachment
    mgi = otTables.MathGlyphInfo()

    mici = otTables.MathItalicsCorrectionInfo()
    mici_cov = otTables.Coverage()
    corr_glyphs = []
    corr_values = []

    # Key glyphs needing italic correction to prevent superscript collision
    special_corr = {
        "integral": 120,
        "iint": 120,
        "summation": 60,
        "partialdiff": 70,
        "math_ital_f": 100,
        "math_ital_d": 45,
        "math_ital_j": 80,
        "math_ital_p": 50,
        "math_ital_t": 40,
        "math_ital_y": 55,
        "math_ital_beta": 65,
        "math_ital_gamma": 60,
        "math_ital_lambda": 55,
        "math_ital_phi": 60,
        "math_ital_psi": 65,
    }
    for gname, val in special_corr.items():
        if gname in glyf:
            corr_glyphs.append(gname)
            rec = otTables.MathValueRecord()
            rec.Value = val
            corr_values.append(rec)

    for cp in range(0x1D434, 0x1D468):
        if cp in cmap:
            g = cmap[cp]
            if g in glyf and g not in corr_glyphs:
                corr_glyphs.append(g)
                rec = otTables.MathValueRecord()
                rec.Value = 35
                corr_values.append(rec)

    mici_cov.glyphs = corr_glyphs
    mici.Coverage = mici_cov
    mici.ItalicsCorrection = corr_values
    mgi.MathItalicsCorrectionInfo = mici

    # Top Accent Attachment
    mtaa = otTables.MathTopAccentAttachment()
    mtaa_cov = otTables.Coverage()
    acc_glyphs = []
    acc_values = []
    for gname in glyph_order:
        if gname in glyf and (gname.startswith("math_") or gname in ["reals", "complex", "naturals", "rationals", "probability", "expectation"]):
            acc_glyphs.append(gname)
            rec = otTables.MathValueRecord()
            rec.Value = hmtx[gname][0] // 2 + 25
            acc_values.append(rec)

    mtaa_cov.glyphs = acc_glyphs
    mtaa.TopAccentCoverage = mtaa_cov
    mtaa.TopAccentAttachment = acc_values
    mgi.MathTopAccentAttachment = mtaa

    math_table.MathGlyphInfo = mgi

    # 5C. MathVariants: Vertical Delimiter Auto-Growing Construction
    mv = otTables.MathVariants()
    mv.MinConnectorOverlap = 50
    mv.HorizGlyphCoverage = None
    mv.HorizGlyphConstruction = []

    delims = [
        ("parenleft", ["parenleft.v1", "parenleft.v2", "parenleft.v3", "parenleft.v4"]),
        ("parenright", ["parenright.v1", "parenright.v2", "parenright.v3", "parenright.v4"]),
        ("bracketleft", ["bracketleft.v1", "bracketleft.v2", "bracketleft.v3", "bracketleft.v4"]),
        ("bracketright", ["bracketright.v1", "bracketright.v2", "bracketright.v3", "bracketright.v4"]),
        ("braceleft", ["braceleft.v1", "braceleft.v2", "braceleft.v3", "braceleft.v4"]),
        ("braceright", ["braceright.v1", "braceright.v2", "braceright.v3", "braceright.v4"]),
        ("radical", ["radical.v1", "radical.v2", "radical.v3", "radical.v4"]),
    ]

    v_cov = otTables.Coverage()
    v_cov.glyphs = [base for base, _ in delims if base in glyf]
    mv.VertGlyphCoverage = v_cov
    mv.VertGlyphConstruction = []

    for base, var_names in delims:
        if base in glyf:
            vgc = otTables.VertGlyphConstruction()
            vgc.MathGlyphVariantRecord = []
            for vname, h in zip(var_names, height_steps):
                rec = otTables.MathGlyphVariantRecord()
                rec.VariantGlyph = vname
                rec.AdvanceMeasurement = h
                vgc.MathGlyphVariantRecord.append(rec)
            mv.VertGlyphConstruction.append(vgc)

    math_table.MathVariants = mv

    table = newTable('MATH')
    table.table = math_table
    font['MATH'] = table

    # 5. Metadata and Versioning
    print("\n5. Updating metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Math"
    ps_name = "PocketGull-Math"
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
        font["OS/2"].usWeightClass = 400
        font["OS/2"].achVendID = "POCK"
        font["OS/2"].fsSelection = 0x1c0

    # 6. Save TTF and Brotli Q11 WOFF2
    print("\n6. Serializing TrueType binary and realigning loca/glyf to 2-byte boundaries...")
    tmp_ttf = OUT_TTF + ".tmp"
    font.save(tmp_ttf)
    font.close()

    # Re-align loca/glyf to 2-byte word boundaries (Quality Pillar 2)
    font = TTFont(tmp_ttf)
    glyf = font['glyf']
    for gname in font.getGlyphOrder():
        glyph = glyf[gname]
        if hasattr(glyph, 'data') and glyph.data and len(glyph.data) % 2 != 0:
            glyph.data = glyph.data + b'\x00'
    font.save(tmp_ttf)
    font.close()

    os.replace(tmp_ttf, OUT_TTF)
    shutil.copyfile(OUT_TTF, ROOT_TTF)

    # Sync to public web directory if present
    public_fonts = r"c:\Users\philg\Pocketgull\pocketgull\public\fonts"
    if os.path.isdir(public_fonts):
        shutil.copyfile(OUT_TTF, os.path.join(public_fonts, "PocketGull-Math.ttf"))

    compress(OUT_TTF, OUT_WOFF2)
    shutil.copyfile(OUT_WOFF2, ROOT_WOFF2)
    if os.path.isdir(public_fonts):
        shutil.copyfile(OUT_WOFF2, os.path.join(public_fonts, "PocketGull-Math.woff2"))

    ttf_sz = os.path.getsize(OUT_TTF)
    woff2_sz = os.path.getsize(OUT_WOFF2)
    print(f"   • Output TTF:   {OUT_TTF} ({ttf_sz:,} bytes)")
    print(f"   • Output WOFF2: {OUT_WOFF2} ({woff2_sz:,} bytes)")
    print("=" * 76)
    print("  [SUCCESS] PocketGull Math OpenType Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_math_font()
