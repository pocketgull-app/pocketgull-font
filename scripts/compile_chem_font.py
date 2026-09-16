#!/usr/bin/env python3
"""
PocketGull Typefoundry: Master Chemistry & Pharmacology Font Compiler
====================================================================
Compiles 'PocketGull-Chem.ttf' and 'PocketGull-Chem.woff2'
World's First Humanist Clinical Chemistry, Pharmacological & Molecular Typeface
"""

import os
import sys
import math
import shutil
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

SRC_REGULAR = os.path.join(TTF_DIR, "PocketGull-Regular.ttf")
SRC_ITALIC = os.path.join(TTF_DIR, "PocketGull-Italic.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Chem.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Chem.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Chem.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Chem.woff2")

AXIS_HEIGHT = 260  # Chemical and reaction centerline (half of x-height 520)
STROKE_W = 68      # Standard bond and arrow stroke weight
DEFAULT_ADV = 600  # Standard operator advance width

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
        pen.qCurveTo((cx - r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.closePath()

def create_glyph_from_pen(pen):
    return pen.glyph()

def build_chem_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: CLINICAL CHEMISTRY & MOLECULAR COMPILER")
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

    ital_glyf = italic_font["glyf"]
    ital_hmtx = italic_font["hmtx"]
    ital_cmap = italic_font.getBestCmap()

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

    # 2. Procedural Stereochemical Bond Synthesis
    print("\n2. Synthesizing Stereochemical Bonds & Spatial Geometry...")

    # Bond 1: Solid Wedged Bond (protruding out of plane) U+25C0 (Left Black Triangle / Wedge) & PUA 0xE900
    pen = TTGlyphPen(None)
    pen.moveTo((80, AXIS_HEIGHT))
    pen.lineTo((460, AXIS_HEIGHT + 110))
    pen.lineTo((460, AXIS_HEIGHT - 110))
    pen.closePath()
    register_op("bond_wedge_solid", [0x25C0, 0xE900], pen, 520, 80)

    # Bond 2: Solid Wedged Bond Right U+25B6 & PUA 0xE901
    pen = TTGlyphPen(None)
    pen.moveTo((460, AXIS_HEIGHT))
    pen.lineTo((80, AXIS_HEIGHT + 110))
    pen.lineTo((80, AXIS_HEIGHT - 110))
    pen.closePath()
    register_op("bond_wedge_solid_right", [0x25B6, 0xE901], pen, 520, 80)

    # Bond 3: Hashed Wedged Bond (receding into plane) PUA 0xE902
    pen = TTGlyphPen(None)
    # Series of 7 parallel vertical hashes of increasing height
    num_hashes = 7
    x_start = 100
    x_end = 460
    dx = (x_end - x_start) / (num_hashes - 1)
    for i in range(num_hashes):
        x = int(x_start + i * dx)
        h = int(24 + i * 28)
        draw_rect(pen, x - 12, AXIS_HEIGHT - h, x + 12, AXIS_HEIGHT + h)
    register_op("bond_wedge_hashed", [0xE902], pen, 520, 88)

    # Bond 4: Coordination / Dative Covalent Bond (Lewis Arrow) U+27F6 & PUA 0xE903
    pen = TTGlyphPen(None)
    draw_rect(pen, 60, AXIS_HEIGHT - hw, 480, AXIS_HEIGHT + hw)
    pen.moveTo((500, AXIS_HEIGHT))
    pen.lineTo((340, AXIS_HEIGHT + 120))
    pen.lineTo((340, AXIS_HEIGHT + 120 - STROKE_W))
    pen.lineTo((440, AXIS_HEIGHT))
    pen.lineTo((340, AXIS_HEIGHT - 120 + STROKE_W))
    pen.lineTo((340, AXIS_HEIGHT - 120))
    pen.closePath()
    register_op("bond_dative", [0x2192, 0x27F6, 0xE903], pen, 560, 60)

    # Bond 5: Hydrogen Bond (Three centered dots) U+22EF & PUA 0xE904
    pen = TTGlyphPen(None)
    r_dot = 32
    draw_circle(pen, 160, AXIS_HEIGHT, r_dot)
    draw_circle(pen, 280, AXIS_HEIGHT, r_dot)
    draw_circle(pen, 400, AXIS_HEIGHT, r_dot)
    register_op("bond_hydrogen", [0x22EF, 0xE904], pen, 560, 128)

    # Bond 6: Single Covalent Bond U+2014 & U+2212
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, AXIS_HEIGHT - hw, 480, AXIS_HEIGHT + hw)
    register_op("bond_single", [0x2212], pen, 560, 80)

    # Bond 7: Double Covalent Bond U+003D
    pen = TTGlyphPen(None)
    gap = 60
    draw_rect(pen, 80, AXIS_HEIGHT + gap - hw, 480, AXIS_HEIGHT + gap + hw)
    draw_rect(pen, 80, AXIS_HEIGHT - gap - hw, 480, AXIS_HEIGHT - gap + hw)
    register_op("bond_double", [0x003D], pen, 560, 80)

    # Bond 8: Triple Covalent Bond U+2261
    pen = TTGlyphPen(None)
    gap3 = 70
    draw_rect(pen, 80, AXIS_HEIGHT + gap3 - hw, 480, AXIS_HEIGHT + gap3 + hw)
    draw_rect(pen, 80, AXIS_HEIGHT - hw, 480, AXIS_HEIGHT + hw)
    draw_rect(pen, 80, AXIS_HEIGHT - gap3 - hw, 480, AXIS_HEIGHT - gap3 + hw)
    register_op("bond_triple", [0x2261], pen, 560, 80)

    # Bond 9: Aromatic Benzene Ring with Delocalized Circle U+2B21 & PUA 0xE905
    pen = TTGlyphPen(None)
    # Outer hexagon: vertices at angles 30, 90, 150, 210, 270, 330
    cx, cy, R = 300, 350, 260
    hex_pts_outer = []
    hex_pts_inner = []
    r_in = R - STROKE_W
    for k in range(6):
        ang = math.radians(60 * k + 30)
        hex_pts_outer.append((cx + int(R * math.cos(ang)), cy + int(R * math.sin(ang))))
        hex_pts_inner.append((cx + int(r_in * math.cos(ang)), cy + int(r_in * math.sin(ang))))

    pen.moveTo(hex_pts_outer[0])
    for pt in hex_pts_outer[1:]:
        pen.lineTo(pt)
    pen.closePath()

    # Inner hexagon traversed in reverse for non-zero winding rule cutout
    pen.moveTo(hex_pts_inner[-1])
    for pt in reversed(hex_pts_inner[:-1]):
        pen.lineTo(pt)
    pen.closePath()

    # Inner aromatic delocalization circular ring
    draw_circle(pen, cx, cy, 130, clockwise=True)
    draw_circle(pen, cx, cy, 130 - STROKE_W, clockwise=False)
    register_op("ring_aromatic", [0x2B21, 0xE905], pen, 600, 80)

    # Bond 10: Transition State Activation Dagger U+2021
    pen = TTGlyphPen(None)
    draw_rect(pen, 280 - hw, -100, 280 + hw, 680)
    draw_rect(pen, 120, 480 - hw, 440, 480 + hw)
    draw_rect(pen, 120, 240 - hw, 440, 240 + hw)
    register_op("dagger_double", [0x2021], pen, 560, 120)

    # Bond 11: Standard State Degree Sign U+00B0
    pen = TTGlyphPen(None)
    draw_circle(pen, 260, 560, 90, clockwise=True)
    draw_circle(pen, 260, 560, 90 - STROKE_W, clockwise=False)
    register_op("degree_standard_state", [0x00B0], pen, 440, 170)

    # 3. Chemical Reaction & Equilibrium Arrows
    print("\n3. Synthesizing Chemical Reaction & Thermodynamic Equilibrium Arrows...")

    # Arrow 1: Dynamic Equilibrium Paired Harpoons U+21CC
    pen = TTGlyphPen(None)
    # Upper right harpoon: y = AXIS_HEIGHT + 45
    y_up = AXIS_HEIGHT + 50
    draw_rect(pen, 80, y_up - hw, 480, y_up + hw)
    pen.moveTo((500, y_up))
    pen.lineTo((360, y_up + 120))
    pen.lineTo((360, y_up + 120 - STROKE_W))
    pen.lineTo((440, y_up))
    pen.closePath()

    # Lower left harpoon: y = AXIS_HEIGHT - 45
    y_dn = AXIS_HEIGHT - 50
    draw_rect(pen, 100, y_dn - hw, 500, y_dn + hw)
    pen.moveTo((80, y_dn))
    pen.lineTo((220, y_dn - 120))
    pen.lineTo((220, y_dn - 120 + STROKE_W))
    pen.lineTo((140, y_dn))
    pen.closePath()
    register_op("equilibrium", [0x21CC], pen, 580, 80)

    # Arrow 2: Product-Favored Equilibrium Harpoons PUA 0xE906
    pen = TTGlyphPen(None)
    # Upper right long harpoon: length 500
    draw_rect(pen, 60, y_up - hw, 500, y_up + hw)
    pen.moveTo((520, y_up))
    pen.lineTo((380, y_up + 120))
    pen.lineTo((380, y_up + 120 - STROKE_W))
    pen.lineTo((460, y_up))
    pen.closePath()
    # Lower left short harpoon: length 240
    draw_rect(pen, 60, y_dn - hw, 300, y_dn + hw)
    pen.moveTo((60, y_dn))
    pen.lineTo((180, y_dn - 120))
    pen.lineTo((180, y_dn - 120 + STROKE_W))
    pen.lineTo((120, y_dn))
    pen.closePath()
    register_op("equilibrium_product_favored", [0xE906], pen, 580, 60)

    # Arrow 3: Reactant-Favored Equilibrium Harpoons PUA 0xE907
    pen = TTGlyphPen(None)
    # Upper right short harpoon: length 240
    draw_rect(pen, 280, y_up - hw, 520, y_up + hw)
    pen.moveTo((520, y_up))
    pen.lineTo((400, y_up + 120))
    pen.lineTo((400, y_up + 120 - STROKE_W))
    pen.lineTo((460, y_up))
    pen.closePath()
    # Lower left long harpoon: length 500
    draw_rect(pen, 80, y_dn - hw, 520, y_dn + hw)
    pen.moveTo((60, y_dn))
    pen.lineTo((200, y_dn - 120))
    pen.lineTo((200, y_dn - 120 + STROKE_W))
    pen.lineTo((120, y_dn))
    pen.closePath()
    register_op("equilibrium_reactant_favored", [0xE907], pen, 580, 60)

    # Arrow 4: Resonance Canonical Double-Headed Arrow U+27F7 & U+2194
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, AXIS_HEIGHT - hw, 460, AXIS_HEIGHT + hw)
    # Right head
    pen.moveTo((520, AXIS_HEIGHT))
    pen.lineTo((380, AXIS_HEIGHT + 130))
    pen.lineTo((380, AXIS_HEIGHT + 130 - STROKE_W))
    pen.lineTo((450, AXIS_HEIGHT))
    pen.lineTo((380, AXIS_HEIGHT - 130 + STROKE_W))
    pen.lineTo((380, AXIS_HEIGHT - 130))
    pen.closePath()
    # Left head
    pen.moveTo((60, AXIS_HEIGHT))
    pen.lineTo((200, AXIS_HEIGHT + 130))
    pen.lineTo((200, AXIS_HEIGHT + 130 - STROKE_W))
    pen.lineTo((130, AXIS_HEIGHT))
    pen.lineTo((200, AXIS_HEIGHT - 130 + STROKE_W))
    pen.lineTo((200, AXIS_HEIGHT - 130))
    pen.closePath()
    register_op("resonance_arrow", [0x27F7, 0x2194], pen, 580, 60)

    # Arrow 5: Retrosynthetic Organic Disconnection Arrow U+27F9 & U+21D2
    pen = TTGlyphPen(None)
    d_gap = 50
    draw_rect(pen, 80, AXIS_HEIGHT + d_gap - hw, 440, AXIS_HEIGHT + d_gap + hw)
    draw_rect(pen, 80, AXIS_HEIGHT - d_gap - hw, 440, AXIS_HEIGHT - d_gap + hw)
    pen.moveTo((540, AXIS_HEIGHT))
    pen.lineTo((360, AXIS_HEIGHT + 160))
    pen.lineTo((360, AXIS_HEIGHT + 160 - STROKE_W))
    pen.lineTo((480, AXIS_HEIGHT))
    pen.lineTo((360, AXIS_HEIGHT - 160 + STROKE_W))
    pen.lineTo((360, AXIS_HEIGHT - 160))
    pen.closePath()
    register_op("retrosynthetic_arrow", [0x27F9, 0x21D2], pen, 600, 80)

    # Arrow 6: Precipitation Arrow (Downward) U+2193
    pen = TTGlyphPen(None)
    draw_rect(pen, 260 - hw, 140, 260 + hw, 640)
    pen.moveTo((260, 80))
    pen.lineTo((140, 220))
    pen.lineTo((140 + STROKE_W, 220))
    pen.lineTo((260, 140))
    pen.lineTo((380 - STROKE_W, 220))
    pen.lineTo((380, 220))
    pen.closePath()
    register_op("precipitate_down", [0x2193], pen, 520, 140)

    # Arrow 7: Gas Evolution Arrow (Upward) U+2191
    pen = TTGlyphPen(None)
    draw_rect(pen, 260 - hw, 80, 260 + hw, 580)
    pen.moveTo((260, 640))
    pen.lineTo((140, 500))
    pen.lineTo((140 + STROKE_W, 500))
    pen.lineTo((260, 580))
    pen.lineTo((380 - STROKE_W, 500))
    pen.lineTo((380, 500))
    pen.closePath()
    register_op("gas_evolution_up", [0x2191], pen, 520, 140)

    # Arrow 8: Curved Electron-Pair Push Arrow U+2935 & PUA 0xE908
    pen = TTGlyphPen(None)
    pen.moveTo((120, 200))
    pen.qCurveTo((120, 560), (320, 560))
    pen.qCurveTo((440, 560), (440, 360))
    pen.lineTo((440 - STROKE_W, 360))
    pen.qCurveTo((440 - STROKE_W, 560 - STROKE_W), (320, 560 - STROKE_W))
    pen.qCurveTo((120 + STROKE_W, 560 - STROKE_W), (120 + STROKE_W, 200))
    pen.closePath()
    # Arrow head pointing down-right
    pen.moveTo((440, 300))
    pen.lineTo((380, 420))
    pen.lineTo((380 + STROKE_W, 420))
    pen.lineTo((440, 360))
    pen.lineTo((500 - STROKE_W, 420))
    pen.lineTo((500, 420))
    pen.closePath()
    register_op("curved_electron_push", [0x2935, 0xE908], pen, 560, 120)

    # 4. Stereochemical Enantiomer Indicators: (R), (S), (E), (Z)
    print("\n4. Synthesizing Stereochemical Enantiomer Indicators...")
    pen_ring = TTGlyphPen(None)
    draw_circle(pen_ring, 300, 350, 270, clockwise=True)
    draw_circle(pen_ring, 300, 350, 270 - STROKE_W, clockwise=False)
    register_op("badge_ring", [], pen_ring, 600, 30)

    def draw_chiral_badge(letter_char, gname, cp):
        pen = TTGlyphPen(glyphSet=glyf)
        pen.addComponent("badge_ring", (1, 0, 0, 1, 0, 0))
        adv, lsb = hmtx.metrics.get(letter_char, (600, 50))
        dx = int(300 - (adv * 0.55) / 2)
        dy = int(350 - (700 * 0.55) / 2)
        pen.addComponent(letter_char, (0.55, 0, 0, 0.55, dx, dy))
        register_op(gname, [cp], pen, 600, 30)

    draw_chiral_badge("R", "chiral_R", 0xE909)
    draw_chiral_badge("S", "chiral_S", 0xE90A)
    draw_chiral_badge("E", "chiral_E", 0xE90B)
    draw_chiral_badge("Z", "chiral_Z", 0xE90C)

    # 5. Metadata and Versioning
    print("\n5. Updating metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Chem"
    ps_name = "PocketGull-Chem"
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
    print("\n6. Serializing TrueType binary and compressing Brotli Q11 WOFF2...")
    tmp_ttf = OUT_TTF + ".tmp"
    font.save(tmp_ttf)
    font.close()
    os.replace(tmp_ttf, OUT_TTF)
    shutil.copyfile(OUT_TTF, ROOT_TTF)

    compress(OUT_TTF, OUT_WOFF2)
    shutil.copyfile(OUT_WOFF2, ROOT_WOFF2)

    ttf_sz = os.path.getsize(OUT_TTF)
    woff2_sz = os.path.getsize(OUT_WOFF2)
    print(f"   • Output TTF:   {OUT_TTF} ({ttf_sz:,} bytes)")
    print(f"   • Output WOFF2: {OUT_WOFF2} ({woff2_sz:,} bytes)")
    print("=" * 76)
    print("  [SUCCESS] PocketGull Chem OpenType Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_chem_font()
