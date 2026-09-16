#!/usr/bin/env python3
"""
PocketGull Typefoundry: K-12 Literacy, Dyslexia & Schoolbook Font Compiler
==========================================================================
Compiles 'PocketGull-Learn.ttf' and 'PocketGull-Learn.woff2'
World's First Humanist Clinical Education, Dyslexia Grounded & TouchMath Typeface
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

SRC_REGULAR = os.path.join(TTF_DIR, "PocketGull-Regular.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Learn.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Learn.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Learn.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Learn.woff2")

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

def build_learn_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: K-12 LITERACY & DYSLEXIA COMPILER")
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

    def register_glyph(gname, codepoints, pen, adv=550, lsb=None):
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
    # 2. Elementary Single-Story 'a' & 'g'
    # -------------------------------------------------------------
    print("\n2. Synthesizing Elementary Single-Story Letterforms...")

    # Single-Story 'a' (uniE961 and mapped to primary 'a' 0x0061 in Learn)
    pen = TTGlyphPen(None)
    # Bowl: outer oval from x=80..460, y=0..520
    pen.moveTo((460, 260))
    pen.qCurveTo((460, 520), (270, 520))
    pen.qCurveTo((80, 520), (80, 260))
    pen.qCurveTo((80, 0), (270, 0))
    pen.qCurveTo((460, 0), (460, 260))
    pen.closePath()
    # Bowl inner
    pen.moveTo((396, 260))
    pen.qCurveTo((396, 68), (270, 68))
    pen.qCurveTo((148, 68), (148, 260))
    pen.qCurveTo((148, 452), (270, 452))
    pen.qCurveTo((396, 452), (396, 260))
    pen.closePath()
    # Right vertical stem: x=396..464, y=0..520
    draw_rect(pen, 396, 0, 464, 520)
    register_glyph("a_single_story", [0xE961, 0x0061], pen, 530)

    # Single-Story 'g' (uniE962 and mapped to primary 'g' 0x0067 in Learn)
    pen = TTGlyphPen(None)
    # Upper bowl
    pen.moveTo((460, 280))
    pen.qCurveTo((460, 520), (270, 520))
    pen.qCurveTo((80, 520), (80, 280))
    pen.qCurveTo((80, 80), (270, 80))
    pen.qCurveTo((460, 80), (460, 280))
    pen.closePath()
    # Inner bowl
    pen.moveTo((396, 280))
    pen.qCurveTo((396, 144), (270, 144))
    pen.qCurveTo((148, 144), (148, 280))
    pen.qCurveTo((148, 456), (270, 456))
    pen.qCurveTo((396, 456), (396, 280))
    pen.closePath()
    # Descender stem & open bottom hook curving left
    draw_rect(pen, 396, -60, 464, 520)
    pen.moveTo((464, -60))
    pen.qCurveTo((464, -180), (260, -180))
    pen.qCurveTo((140, -180), (100, -120))
    pen.lineTo((130, -75))
    pen.qCurveTo((160, -118), (260, -118))
    pen.qCurveTo((396, -118), (396, -60))
    pen.closePath()
    register_glyph("g_single_story", [0xE962, 0x0067], pen, 530)

    # -------------------------------------------------------------
    # 3. Dyslexia-Grounded Letterforms (Weighted Bases & Distinct Terminals)
    # -------------------------------------------------------------
    print("\n3. Synthesizing Dyslexia-Grounded Geometric Letterforms...")

    # b_dyslexic uniE963: Heavier bottom curve, pronounced left bottom spur
    pen = TTGlyphPen(None)
    draw_rect(pen, 90, 0, 160, 750)       # Left tall ascender stem
    draw_rect(pen, 50, 0, 160, 45)         # Pronounced bottom-left anchor foot
    # Bottom-heavy bowl
    pen.moveTo((480, 230))
    pen.qCurveTo((480, 520), (300, 520))
    pen.qCurveTo((160, 520), (160, 230))
    pen.qCurveTo((160, 0), (300, 0))
    pen.qCurveTo((480, 0), (480, 230))
    pen.closePath()
    # Inner cutout (offset down for low center of gravity)
    pen.moveTo((405, 230))
    pen.qCurveTo((405, 80), (300, 80))
    pen.qCurveTo((160, 80), (160, 230))
    pen.qCurveTo((160, 455), (300, 455))
    pen.qCurveTo((405, 455), (405, 230))
    pen.closePath()
    register_glyph("b_dyslexic", [0xE963], pen, 550)

    # d_dyslexic uniE964: Right stem with distinct upward terminal foot, higher optical waist
    pen = TTGlyphPen(None)
    draw_rect(pen, 400, 40, 470, 750)      # Right ascender stem
    # Distinctive bottom right outward curl
    pen.moveTo((400, 40))
    pen.qCurveTo((400, 0), (440, 0))
    pen.qCurveTo((495, 0), (520, 55))
    pen.lineTo((500, 100))
    pen.qCurveTo((470, 60), (450, 60))
    pen.qCurveTo((440, 60), (440, 120))
    pen.lineTo((400, 120))
    pen.closePath()
    # Non-mirrored bowl with higher center of gravity
    pen.moveTo((400, 280))
    pen.qCurveTo((400, 520), (240, 520))
    pen.qCurveTo((80, 520), (80, 280))
    pen.qCurveTo((80, 60), (240, 60))
    pen.qCurveTo((400, 60), (400, 280))
    pen.closePath()
    pen.moveTo((335, 280))
    pen.qCurveTo((335, 125), (240, 125))
    pen.qCurveTo((148, 125), (148, 280))
    pen.qCurveTo((148, 455), (240, 455))
    pen.qCurveTo((335, 455), (335, 280))
    pen.closePath()
    register_glyph("d_dyslexic", [0xE964], pen, 560)

    # p_dyslexic uniE965: Descender has downward-angled chisel tip, low center of gravity
    pen = TTGlyphPen(None)
    draw_rect(pen, 90, -180, 160, 520)     # Left descender stem
    # Angled terminal at bottom
    pen.moveTo((90, -180))
    pen.lineTo((160, -140))
    pen.lineTo((160, -180))
    pen.closePath()
    # Bowl
    pen.moveTo((480, 240))
    pen.qCurveTo((480, 520), (300, 520))
    pen.qCurveTo((160, 520), (160, 240))
    pen.qCurveTo((160, 20), (300, 20))
    pen.qCurveTo((480, 20), (480, 240))
    pen.closePath()
    pen.moveTo((405, 240))
    pen.qCurveTo((405, 95), (300, 95))
    pen.qCurveTo((160, 95), (160, 240))
    pen.qCurveTo((160, 455), (300, 455))
    pen.qCurveTo((405, 455), (405, 240))
    pen.closePath()
    register_glyph("p_dyslexic", [0xE965], pen, 550)

    # q_dyslexic uniE966: Right descender with prominent upward return hook
    pen = TTGlyphPen(None)
    draw_rect(pen, 400, -180, 470, 520)    # Right descender stem
    # Distinctive upward return hook from y=-180 to -70
    pen.moveTo((470, -180))
    pen.qCurveTo((525, -180), (545, -120))
    pen.lineTo((545, -60))
    pen.lineTo((495, -60))
    pen.lineTo((495, -115))
    pen.qCurveTo((485, -135), (470, -135))
    pen.closePath()
    # Bowl
    pen.moveTo((400, 270))
    pen.qCurveTo((400, 520), (240, 520))
    pen.qCurveTo((75, 520), (75, 270))
    pen.qCurveTo((75, 50), (240, 50))
    pen.qCurveTo((400, 50), (400, 270))
    pen.closePath()
    pen.moveTo((335, 270))
    pen.qCurveTo((335, 115), (240, 115))
    pen.qCurveTo((145, 115), (145, 270))
    pen.qCurveTo((145, 455), (240, 455))
    pen.qCurveTo((335, 455), (335, 270))
    pen.closePath()
    register_glyph("q_dyslexic", [0xE966], pen, 570)

    # -------------------------------------------------------------
    # 4. Handwriting Practice Ruling Guidelines (D'Nealian Grid)
    # -------------------------------------------------------------
    print("\n4. Synthesizing Handwriting Practice Ruling Guidelines...")

    # Blank Ruling Guideline Segment uniE967 (Width 600 UPM)
    # Ascender line: y=750 (stroke 16)
    # Midline (dashed): y=270 (dashes: 0..100, 150..250, 300..400, 450..550)
    # Baseline: y=0 (solid stroke 22)
    # Descender line: y=-180 (stroke 16)
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 742, 600, 758)      # Topline
    draw_rect(pen, 0, -8, 600, 14)         # Solid Baseline
    draw_rect(pen, 0, -188, 600, -172)    # Descender line
    # Dashes for midline
    for dx in [0, 150, 300, 450]:
        draw_rect(pen, dx, 263, dx + 100, 277)
    register_glyph("rule_guide_segment", [0xE967], pen, 600)

    # Full Width Rule Spacer uniE968
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 742, 400, 758)
    draw_rect(pen, 0, -8, 400, 14)
    draw_rect(pen, 0, -188, 400, -172)
    draw_rect(pen, 0, 263, 80, 277)
    draw_rect(pen, 130, 263, 210, 277)
    draw_rect(pen, 260, 263, 340, 277)
    register_glyph("rule_space", [0xE968], pen, 400)

    # -------------------------------------------------------------
    # 5. TouchMath Subitizing Numerals (uniE971 - uniE979)
    # -------------------------------------------------------------
    print("\n5. Synthesizing TouchMath Subitizing Numerals...")

    # TouchMath dot radius
    DOT_R = 36
    RING_RO = 58
    RING_RI = 42

    def add_touch_dot(pen, cx, cy):
        draw_circle(pen, cx, cy, DOT_R, clockwise=True)

    def add_double_touch(pen, cx, cy):
        draw_circle(pen, cx, cy, DOT_R, clockwise=True)
        draw_ring(pen, cx, cy, RING_RO, RING_RI)

    # Helper to clone numeral from regular and overlay dots
    def build_touch_numeral(digit_char, gname, cp, dot_coords, double_coords=[]):
        adv, lsb = hmtx.metrics.get(digit_char, (550, 50))
        pen = TTGlyphPen(glyphSet=font.getGlyphSet())
        # Add base digit component
        pen.addComponent(digit_char, (1, 0, 0, 1, 0, 0))
        # Add single touch dots
        for cx, cy in dot_coords:
            add_touch_dot(pen, cx, cy)
        # Add double touch dots
        for cx, cy in double_coords:
            add_double_touch(pen, cx, cy)
        register_glyph(gname, [cp], pen, adv, lsb)

    # Numerals 1 through 9 TouchMath Touchpoint Layouts:
    # 1: 1 dot at top
    build_touch_numeral("one", "touch_1", 0xE971, [(275, 680)])
    # 2: 2 dots (start of curve, corner of base)
    build_touch_numeral("two", "touch_2", 0xE972, [(160, 570), (450, 45)])
    # 3: 3 dots (start, middle cusp, bottom terminal)
    build_touch_numeral("three", "touch_3", 0xE973, [(150, 570), (300, 360), (140, 110)])
    # 4: 4 dots (top left, junction corner, top right stem, bottom stem)
    build_touch_numeral("four", "touch_4", 0xE974, [(130, 700), (90, 230), (420, 700), (420, 50)])
    # 5: 5 dots (top right, top left, middle corner, belly curve, bottom terminal)
    build_touch_numeral("five", "touch_5", 0xE975, [(450, 680), (160, 680), (150, 420), (480, 240), (140, 90)])
    # 6: 3 double touchpoints = 6 (top, middle-left, bottom-right)
    build_touch_numeral("six", "touch_6", 0xE976, [], [(380, 680), (120, 270), (480, 210)])
    # 7: 1 single dot + 3 double touchpoints = 7
    build_touch_numeral("seven", "touch_7", 0xE977, [(120, 680)], [(480, 680), (370, 450), (270, 100)])
    # 8: 4 double touchpoints = 8 (top loop left/right, bottom loop left/right)
    build_touch_numeral("eight", "touch_8", 0xE978, [], [(160, 550), (420, 550), (140, 180), (440, 180)])
    # 9: 1 single dot + 4 double touchpoints = 9
    build_touch_numeral("nine", "touch_9", 0xE979, [(210, 40)], [(440, 550), (130, 500), (310, 680), (440, 270)])

    # -------------------------------------------------------------
    # 6. Metadata & SemVer 3.100 OFL 1.1 Licensing
    # -------------------------------------------------------------
    print("\n6. Updating OpenType metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Learn"
    ps_name = "PocketGull-Learn"
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
    print("  [SUCCESS] PocketGull Learn OpenType Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_learn_font()
