#!/usr/bin/env python3
"""
PocketGull Typefoundry: Clinical Laboratory & Pathology Font Compiler
=====================================================================
Compiles 'PocketGull-Lab.ttf' and 'PocketGull-Lab.woff2'
World's First Humanist Clinical Pathology, Diagnostics & Wet Lab SOP Typeface
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

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Lab.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Lab.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Lab.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Lab.woff2")

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

def draw_rounded_badge(pen, x0, y0, x1, y1, r=40, sw=32):
    # Outer rounded rect
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
    ir = max(8, r - sw)
    pen.moveTo((ix0 + ir, iy0))
    pen.qCurveTo((ix0, iy0), (ix0, iy0 + ir))
    pen.lineTo((ix0, iy1 - ir))
    pen.qCurveTo((ix0, iy1), (ix0 + ir, iy1))
    pen.lineTo((ix1 - ir, iy1))
    pen.qCurveTo((ix1, iy1), (ix1, iy1 - ir))
    pen.lineTo((ix1, iy0 + ir))
    pen.qCurveTo((ix1, iy0), (ix1 - ir, iy0))
    pen.closePath()

def build_lab_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: CLINICAL LABORATORY & PATHOLOGY COMPILER")
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

    print("\n2. Synthesizing Relative Centrifugal Force (×g)...")

    # Glyph 1: Centrifugation ×g uniE980
    pen = TTGlyphPen(None)
    # Multiplier ×
    sw = 24
    cx, cy = 180, 260
    # Arm 1
    pen.moveTo((cx - 80, cy - 80 + sw))
    pen.lineTo((cx + 80 - sw, cy + 80))
    pen.lineTo((cx + 80, cy + 80 - sw))
    pen.lineTo((cx - 80 + sw, cy - 80))
    pen.closePath()
    # Arm 2
    pen.moveTo((cx - 80 + sw, cy + 80))
    pen.lineTo((cx + 80, cy - 80 + sw))
    pen.lineTo((cx + 80 - sw, cy - 80))
    pen.lineTo((cx - 80, cy + 80 - sw))
    pen.closePath()
    # Letter 'g' (single-story loop)
    gx0 = 340
    # Bowl
    pen.moveTo((gx0 + 260, 260))
    pen.qCurveTo((gx0 + 260, 480), (gx0 + 130, 480))
    pen.qCurveTo((gx0, 480), (gx0, 260))
    pen.qCurveTo((gx0, 50), (gx0 + 130, 50))
    pen.qCurveTo((gx0 + 260, 50), (gx0 + 260, 260))
    pen.closePath()
    pen.moveTo((gx0 + 215, 260))
    pen.qCurveTo((gx0 + 215, 95), (gx0 + 130, 95))
    pen.qCurveTo((gx0 + 45, 95), (gx0 + 45, 260))
    pen.qCurveTo((gx0 + 45, 435), (gx0 + 130, 435))
    pen.qCurveTo((gx0 + 215, 435), (gx0 + 215, 260))
    pen.closePath()
    # Descender & hook
    draw_rect(pen, gx0 + 215, -40, gx0 + 260, 480)
    pen.moveTo((gx0 + 260, -40))
    pen.qCurveTo((gx0 + 260, -160), (gx0 + 120, -160))
    pen.qCurveTo((gx0 + 30, -160), (gx0, -100))
    pen.lineTo((gx0 + 25, -65))
    pen.qCurveTo((gx0 + 50, -115), (gx0 + 120, -115))
    pen.qCurveTo((gx0 + 215, -115), (gx0 + 215, -40))
    pen.closePath()
    register_glyph("rcf_xg", [0xE980], pen, 680)

    print("\n3. Synthesizing Calibrated Micropipette Badges (P10 - P1000)...")

    def build_pipette_badge(gname, cp, label_glyphs, total_w):
        pen = TTGlyphPen(glyphSet=glyph_set)
        draw_rounded_badge(pen, 30, 60, total_w - 30, 640, r=60, sw=34)
        cur_x = 75
        for g_id in label_glyphs:
            g_adv = hmtx.metrics.get(g_id, (550, 40))[0]
            s = 0.65
            pen.addComponent(g_id, (s, 0, 0, s, cur_x, 150))
            cur_x += int(g_adv * s) + 15
        register_glyph(gname, [cp], pen, total_w)

    build_pipette_badge("pipette_p10", 0xE981, ["P", "one", "zero"], 780)
    build_pipette_badge("pipette_p20", 0xE982, ["P", "two", "zero"], 780)
    build_pipette_badge("pipette_p200", 0xE983, ["P", "two", "zero", "zero"], 960)
    build_pipette_badge("pipette_p1000", 0xE984, ["P", "one", "zero", "zero", "zero"], 1150)

    print("\n4. Synthesizing Serial Dilution Tiers (1:10^3, 1:10^6, 1:10^9)...")

    def build_dilution(gname, cp, exp_g):
        pen = TTGlyphPen(glyphSet=glyph_set)
        # 1:10
        pen.addComponent("one", (0.7, 0, 0, 0.7, 40, 100))
        pen.addComponent("colon", (0.8, 0, 0, 0.8, 260, 100))
        pen.addComponent("one", (0.7, 0, 0, 0.7, 400, 100))
        pen.addComponent("zero", (0.7, 0, 0, 0.7, 620, 100))
        # Exponent
        pen.addComponent(exp_g, (0.45, 0, 0, 0.45, 880, 360))
        register_glyph(gname, [cp], pen, 1080)

    build_dilution("dilution_10_3", 0xE985, "three")
    build_dilution("dilution_10_6", 0xE986, "six")
    build_dilution("dilution_10_9", 0xE987, "nine")

    print("\n5. Synthesizing Spectrophotometric Absorbance (OD600 & A260/A280)...")

    # OD600 uniE988
    pen = TTGlyphPen(glyphSet=glyph_set)
    pen.addComponent("O", (0.7, 0, 0, 0.7, 40, 100))
    pen.addComponent("D", (0.7, 0, 0, 0.7, 360, 100))
    pen.addComponent("six", (0.45, 0, 0, 0.45, 720, 60))
    pen.addComponent("zero", (0.45, 0, 0, 0.45, 900, 60))
    pen.addComponent("zero", (0.45, 0, 0, 0.45, 1080, 60))
    register_glyph("absorbance_od600", [0xE988], pen, 1300)

    # A260/A280 uniE989
    pen = TTGlyphPen(glyphSet=glyph_set)
    pen.addComponent("A", (0.6, 0, 0, 0.6, 40, 120))
    pen.addComponent("two", (0.38, 0, 0, 0.38, 320, 80))
    pen.addComponent("six", (0.38, 0, 0, 0.38, 460, 80))
    pen.addComponent("zero", (0.38, 0, 0, 0.38, 600, 80))
    pen.addComponent("slash", (0.6, 0, 0, 0.6, 750, 120))
    pen.addComponent("A", (0.6, 0, 0, 0.6, 920, 120))
    pen.addComponent("two", (0.38, 0, 0, 0.38, 1200, 80))
    pen.addComponent("eight", (0.38, 0, 0, 0.38, 1340, 80))
    pen.addComponent("zero", (0.38, 0, 0, 0.38, 1480, 80))
    register_glyph("ratio_a260_a280", [0xE989], pen, 1680)

    print("\n6. Synthesizing Biosafety Level (BSL) Badges...")

    def build_bsl_badge(gname, cp, num_g):
        pen = TTGlyphPen(glyphSet=glyph_set)
        draw_rounded_badge(pen, 30, 60, 920, 640, r=60, sw=34)
        pen.addComponent("B", (0.6, 0, 0, 0.6, 80, 150))
        pen.addComponent("S", (0.6, 0, 0, 0.6, 260, 150))
        pen.addComponent("L", (0.6, 0, 0, 0.6, 440, 150))
        pen.addComponent("hyphen", (0.6, 0, 0, 0.6, 600, 150))
        pen.addComponent(num_g, (0.6, 0, 0, 0.6, 720, 150))
        register_glyph(gname, [cp], pen, 960)

    build_bsl_badge("bsl_1", 0xE98A, "one")
    build_bsl_badge("bsl_2", 0xE98B, "two")
    build_bsl_badge("bsl_3", 0xE98C, "three")
    build_bsl_badge("bsl_4", 0xE98D, "four")

    # pH unit ligature uniE98E
    pen = TTGlyphPen(glyphSet=glyph_set)
    pen.addComponent("p", (0.8, 0, 0, 0.8, 40, 100))
    pen.addComponent("H", (0.8, 0, 0, 0.8, 380, 100))
    register_glyph("ph_unit", [0xE98E], pen, 760)

    # Molar concentration badge [M] uniE98F
    pen = TTGlyphPen(glyphSet=glyph_set)
    draw_rounded_badge(pen, 30, 60, 570, 640, r=50, sw=32)
    pen.addComponent("M", (0.65, 0, 0, 0.65, 100, 150))
    register_glyph("molar_badge", [0xE98F], pen, 600)

    # -------------------------------------------------------------
    # 7. Metadata & SemVer 3.100 OFL 1.1 Licensing
    # -------------------------------------------------------------
    print("\n7. Updating OpenType metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Lab"
    ps_name = "PocketGull-Lab"
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

    # Tabular numbers flag in OS/2
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
    # 8. Save TTF and Compress WOFF2
    # -------------------------------------------------------------
    print(f"\n8. Saving TrueType binary: {OUT_TTF}")
    font.save(OUT_TTF)
    shutil.copyfile(OUT_TTF, ROOT_TTF)

    print(f"9. Compressing WOFF2 binary via Brotli quality 11: {OUT_WOFF2}")
    compress(OUT_TTF, OUT_WOFF2)
    shutil.copyfile(OUT_WOFF2, ROOT_WOFF2)

    ttf_sz = os.path.getsize(OUT_TTF)
    woff2_sz = os.path.getsize(OUT_WOFF2)
    print(f"   • Output TTF:   {OUT_TTF} ({ttf_sz:,} bytes)")
    print(f"   • Output WOFF2: {OUT_WOFF2} ({woff2_sz:,} bytes)")
    print("=" * 76)
    print("  [SUCCESS] PocketGull Lab OpenType Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_lab_font()
