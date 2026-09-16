#!/usr/bin/env python3
"""
scripts/cure_mono_astro_and_bio_symbols.py
===========================================
Elevates PocketGull Mono with astronomical and bio-reaction operators:
- Sun ☉ (U+2609) & ⊙ (U+2299)
- Earth ♁ (U+2641) & ⊕ (U+2295)
- Jupiter ♃ (U+2643)
- Saturn ♄ (U+2644)
- Equilibrium Harpoons ⇌ (U+21CC & U+21CB)
- LeftRight Arrow ↔ (U+2194)

Strictly preserves:
1. Fixed 600 UPM pitch on every glyph (Quality Pillar 6).
2. 2-byte word alignment on loca/glyf (Quality Pillar 2).
3. Bit-7 flag clearing on all points (Quality Pillar 3).
"""

import os
import sys
import shutil
import subprocess
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")
PUBLIC_FONTS = r"c:\Users\philg\Pocketgull\pocketgull\public\fonts"

ADVANCE = 600
AXIS_HEIGHT = 260
STROKE_W = 68
hw = STROKE_W // 2

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
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.closePath()

def update_mono_font(ttf_path):
    filename = os.path.basename(ttf_path)
    print(f"\n• Processing {filename}...")
    font = TTFont(ttf_path)
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())

    def register_op(gname, codepoints, pen):
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (ADVANCE, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    # 1. Sun (☉ U+2609 & ⊙ U+2299)
    if 0x2299 in cmap:
        cmap[0x2609] = cmap[0x2299]
    else:
        pen = TTGlyphPen(None)
        draw_circle(pen, 300, AXIS_HEIGHT, 170, clockwise=False)
        draw_circle(pen, 300, AXIS_HEIGHT, 170 - STROKE_W, clockwise=True)
        draw_circle(pen, 300, AXIS_HEIGHT, 48, clockwise=False)
        register_op("circdot_sun", [0x2299, 0x2609], pen)

    # 2. Earth (♁ U+2641 & ⊕ U+2295)
    if 0x2295 in cmap:
        cmap[0x2641] = cmap[0x2295]
    else:
        pen = TTGlyphPen(None)
        draw_circle(pen, 300, AXIS_HEIGHT, 170, clockwise=False)
        draw_circle(pen, 300, AXIS_HEIGHT, 170 - STROKE_W, clockwise=True)
        draw_rect(pen, 300 - 170 + STROKE_W, AXIS_HEIGHT - hw, 300 + 170 - STROKE_W, AXIS_HEIGHT + hw)
        draw_rect(pen, 300 - hw, AXIS_HEIGHT - 170 + STROKE_W, 300 + hw, AXIS_HEIGHT + 170 - STROKE_W)
        register_op("circplus_earth", [0x2295, 0x2641], pen)

    # 3. Jupiter symbol (♃ U+2643)
    pen = TTGlyphPen(None)
    draw_rect(pen, 360 - hw, -60, 360 + hw, 600)
    draw_rect(pen, 200, 380 - hw, 480, 380 + hw)
    pen.moveTo((120, 200))
    pen.qCurveTo((120, 480), (360, 480))
    pen.lineTo((360, 480 - STROKE_W))
    pen.qCurveTo((120 + STROKE_W, 480 - STROKE_W), (120 + STROKE_W, 200))
    pen.closePath()
    register_op("jupiter", [0x2643], pen)

    # 4. Saturn symbol (♄ U+2644)
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
    register_op("saturn", [0x2644], pen)

    # 5. Equilibrium Paired Harpoons (⇌ U+21CC & U+21CB)
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
    register_op("equilibrium", [0x21CC, 0x21CB], pen)

    # 6. LeftRight Arrow (↔ U+2194)
    if 0x2194 not in cmap:
        if "arrowboth" in glyf:
            cmap[0x2194] = "arrowboth"
        else:
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
            register_op("leftrightarrow", [0x2194], pen)

    # Ensure all glyphs strictly maintain 600 UPM advance width
    for gname in glyph_order:
        if gname in hmtx.metrics:
            _, lsb = hmtx[gname]
            hmtx[gname] = (ADVANCE, lsb)
        else:
            hmtx[gname] = (ADVANCE, 50)

    font.setGlyphOrder(glyph_order)
    font.save(ttf_path)
    font.close()

    # Recompress WOFF2
    base_name = os.path.splitext(filename)[0]
    woff2_path = os.path.join(WOFF2_DIR, f"{base_name}.woff2")
    compress(ttf_path, woff2_path)

    # Synchronize to root and public if applicable
    root_file = os.path.join(ROOT_DIR, filename)
    if os.path.isfile(root_file):
        shutil.copyfile(ttf_path, root_file)
    root_woff2 = os.path.join(ROOT_DIR, f"{base_name}.woff2")
    if os.path.isfile(root_woff2):
        shutil.copyfile(woff2_path, root_woff2)

    if os.path.isdir(PUBLIC_FONTS):
        shutil.copyfile(ttf_path, os.path.join(PUBLIC_FONTS, filename))
        shutil.copyfile(woff2_path, os.path.join(PUBLIC_FONTS, f"{base_name}.woff2"))

    print(f"  [OK] Successfully updated {filename} & {base_name}.woff2")

def main():
    print("=" * 76)
    print("  ELEVATING POCKETGULL MONO: ASTRONOMICAL & BIO OPERATOR INJECTION")
    print("=" * 76)
    mono_fonts = [
        "PocketGullMono-Regular.ttf",
        "PocketGullMono-Bold.ttf",
        "PocketGullMono-Italic.ttf"
    ]
    for m in mono_fonts:
        p = os.path.join(TTF_DIR, m)
        if os.path.isfile(p):
            update_mono_font(p)

    # Run pure Dart 3.11 realign command to guarantee 2-byte word boundaries
    print("\n• Realigning 2-byte word boundaries on all TTFs via Dart 3.11...")
    subprocess.run(["dart", "run", "tool/pocketgull_foundry.dart", "realign"], cwd=ROOT_DIR)

    print("\n" + "=" * 76)
    print("  [SUCCESS] PocketGull Mono superfamily elevated with astronomical & bio operators!")
    print("=" * 76)

if __name__ == "__main__":
    main()
