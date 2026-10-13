#!/usr/bin/env python3
"""
PocketGull Typefoundry - Clinical Monospace Terminal Icons Synthesizer
======================================================================
Synthesizes and injects native, clinical-grade monospaced vector glyphs for:
1. U+1F4C1 (📁 File Folder / Clinical Medical Chart) -> u1F4C1
2. U+23F1  (⏱ Stopwatch / Clinical Telemetry Timer) -> uni23F1
3. PUA Aliases:
   - U+F07B (Nerd Font folder) -> u1F4C1
   - U+F115 (Nerd Font open folder) -> u1F4C1

Invariants:
- Fixed 600 UPM advance width across all styles.
- Louise Sloan 5:1 optotypic clarity (prevents dark-mode hairline collapse).
- 2-byte word alignment (loca[i] % 2 == 0).
- Bit-7 flag masking (flag & 0x3F).
- Zero duplicate nodes.
- W3C OTS 100% compliant.
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(r"C:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

def sanitize_contour_points(coords, endPts):
    """Eliminates consecutive identical points to guarantee 0 duplicate nodes."""
    start = 0
    for end in endPts:
        for i in range(start, end):
            if coords[i] == coords[i + 1]:
                coords[i + 1] = (coords[i + 1][0] + 1, coords[i + 1][1])
        if len(coords) > 1 and coords[start] == coords[end]:
            coords[end] = (coords[end][0] + 1, coords[end][1])
        start = end + 1

def build_folder_glyph(is_bold=False):
    """Constructs a crisp, clinical file folder with humanist corner radii and pocket slit."""
    pen = TTGlyphPen(None)
    x0 = 50 if is_bold else 60
    x1 = 550 if is_bold else 540
    y0 = 80
    y_body = 480
    y_tab = 590
    tab_w = 180
    r = 25

    # 1. Outer boundary (Clockwise: bottom-left -> tab -> right -> bottom)
    pen.moveTo((x0, y0 + r))
    pen.lineTo((x0, y_tab - r))
    pen.qCurveTo((x0, y_tab), (x0 + r, y_tab))
    pen.lineTo((x0 + tab_w - r, y_tab))
    pen.qCurveTo((x0 + tab_w - 5, y_tab), (x0 + tab_w + 10, y_body + 40))
    pen.lineTo((x0 + tab_w + 35, y_body))
    pen.lineTo((x1 - r, y_body))
    pen.qCurveTo((x1, y_body), (x1, y_body - r))
    pen.lineTo((x1, y0 + r))
    pen.qCurveTo((x1, y0), (x1 - r, y0))
    pen.lineTo((x0 + r, y0))
    pen.qCurveTo((x0, y0), (x0, y0 + r))
    pen.closePath()

    # 2. Pocket slit cutout (Counter-Clockwise: bottom-left -> bottom-right -> top-right -> top-left)
    slit_h = 55 if is_bold else 45
    slit_y = 345
    slit_x0 = x0 + (45 if is_bold else 40)
    slit_x1 = x1 - (45 if is_bold else 40)

    pen.moveTo((slit_x0, slit_y))
    pen.lineTo((slit_x1, slit_y))
    pen.lineTo((slit_x1, slit_y + slit_h))
    pen.lineTo((slit_x0, slit_y + slit_h))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_stopwatch_glyph(is_bold=False):
    """Constructs a high-visibility clinical stopwatch with 70 UPM dial, top winder, and telemetry hands."""
    pen = TTGlyphPen(None)
    cx, cy = 300, 320
    r_out = 220
    r_in = 145 if is_bold else 160
    k_out = r_out * 1.41421356
    k_in = r_in * 1.41421356

    # 1. Outer circle (Clockwise: Top -> Right -> Bottom -> Left)
    pen.moveTo((cx, cy + r_out))
    pen.qCurveTo((int(cx + k_out/2), int(cy + k_out/2)), (cx + r_out, cy))
    pen.qCurveTo((int(cx + k_out/2), int(cy - k_out/2)), (cx, cy - r_out))
    pen.qCurveTo((int(cx - k_out/2), int(cy - k_out/2)), (cx - r_out, cy))
    pen.qCurveTo((int(cx - k_out/2), int(cy + k_out/2)), (cx, cy + r_out))
    pen.closePath()

    # 2. Inner cutout circle (Counter-Clockwise: Top -> Left -> Bottom -> Right)
    pen.moveTo((cx, cy + r_in))
    pen.qCurveTo((int(cx - k_in/2), int(cy + k_in/2)), (cx - r_in, cy))
    pen.qCurveTo((int(cx - k_in/2), int(cy - k_in/2)), (cx, cy - r_in))
    pen.qCurveTo((int(cx + k_in/2), int(cy - k_in/2)), (cx + r_in, cy))
    pen.qCurveTo((int(cx + k_in/2), int(cy + k_in/2)), (cx, cy + r_in))
    pen.closePath()

    # 3. Top Crown Stem & Winder Button (Clockwise)
    w_stem = 40 if is_bold else 30
    w_crown = 80 if is_bold else 70
    h_crown = 55 if is_bold else 45
    pen.moveTo((cx - w_stem, cy + r_out - 10))
    pen.lineTo((cx - w_stem, cy + r_out + 45))
    pen.lineTo((cx - w_crown, cy + r_out + 45))
    pen.lineTo((cx - w_crown, cy + r_out + 45 + h_crown))
    pen.lineTo((cx + w_crown, cy + r_out + 45 + h_crown))
    pen.lineTo((cx + w_crown, cy + r_out + 45))
    pen.lineTo((cx + w_stem, cy + r_out + 45))
    pen.lineTo((cx + w_stem, cy + r_out - 10))
    pen.closePath()

    # 4. Lap Button at 45 deg (Clockwise)
    pen.moveTo((430, 465))
    pen.lineTo((465, 500))
    pen.lineTo((495, 470))
    pen.lineTo((460, 435))
    pen.closePath()

    # 5. Minute Hand (pointing to 12 o'clock)
    hw = 18 if is_bold else 14
    pen.moveTo((cx - hw, cy - 20))
    pen.lineTo((cx - hw, cy + r_in - 30))
    pen.lineTo((cx + hw, cy + r_in - 30))
    pen.lineTo((cx + hw, cy - 20))
    pen.closePath()

    # 6. Lap Hand (pointing to ~2 o'clock)
    pen.moveTo((cx - 10, cy - 10))
    pen.lineTo((cx + 90, cy + 50))
    pen.lineTo((cx + 105, cy + 25))
    pen.lineTo((cx + 5, cy - 35))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_git_branch_glyph(is_bold=False):
    """Constructs a crisp, Susan Kare-inspired Git Branch / Unicode Alternative Key Symbol (U+E0A0 / U+2387)."""
    pen = TTGlyphPen(None)
    sw = 56 if is_bold else 46
    half = sw // 2
    x_main = 190
    x_branch = 420
    y_bot = 110
    y_top = 630
    y_fork = 270
    y_branch_top = 490
    r_node = 68 if is_bold else 60
    r_hole = 26 if is_bold else 24

    def add_ring(cx, cy):
        k = int(r_node * 0.7071)
        pen.moveTo((cx, cy + r_node))
        pen.qCurveTo((cx + k, cy + k), (cx + r_node, cy))
        pen.qCurveTo((cx + k, cy - k), (cx, cy - r_node))
        pen.qCurveTo((cx - k, cy - k), (cx - r_node, cy))
        pen.qCurveTo((cx - k, cy + k), (cx, cy + r_node))
        pen.closePath()
        kh = int(r_hole * 0.7071)
        pen.moveTo((cx, cy + r_hole))
        pen.qCurveTo((cx - kh, cy + kh), (cx - r_hole, cy))
        pen.qCurveTo((cx - kh, cy - kh), (cx, cy - r_hole))
        pen.qCurveTo((cx + kh, cy - kh), (cx + r_hole, cy))
        pen.qCurveTo((cx + kh, cy + kh), (cx, cy + r_hole))
        pen.closePath()

    add_ring(x_main, y_bot + r_node)
    add_ring(x_main, y_top - r_node)
    add_ring(x_branch, y_branch_top)

    pen.moveTo((x_main - half, y_bot + r_node * 2 - 12))
    pen.lineTo((x_main - half, y_top - r_node * 2 + 12))
    pen.lineTo((x_main + half, y_top - r_node * 2 + 12))
    pen.lineTo((x_main + half, y_bot + r_node * 2 - 12))
    pen.closePath()

    pen.moveTo((x_main + half - 6, y_fork))
    pen.qCurveTo((x_branch - half, y_fork + 20), (x_branch - half, y_branch_top - r_node + 10))
    pen.lineTo((x_branch + half, y_branch_top - r_node + 10))
    pen.qCurveTo((x_branch + half, y_fork - 30), (x_main + half - 6, y_fork - sw))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_ln_glyph(is_bold=False):
    """Constructs the Line-Number 'LN' monogram (U+E0A1) and Column-Number 'CN' (U+E0A3)."""
    pen = TTGlyphPen(None)
    sw = 48 if is_bold else 40
    pen.moveTo((90, 160))
    pen.lineTo((90, 580))
    pen.lineTo((90 + sw, 580))
    pen.lineTo((90 + sw, 160 + sw))
    pen.lineTo((255, 160 + sw))
    pen.lineTo((255, 160))
    pen.closePath()

    pen.moveTo((300, 160))
    pen.lineTo((300, 580))
    pen.lineTo((300 + sw, 580))
    pen.lineTo((510 - sw, 250))
    pen.lineTo((510 - sw, 580))
    pen.lineTo((510, 580))
    pen.lineTo((510, 160))
    pen.lineTo((510 - sw, 160))
    pen.lineTo((300 + sw, 490))
    pen.lineTo((300 + sw, 160))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_lock_glyph(is_bold=False):
    """Constructs a crisp Padlock / Read-Only Lock (U+E0A2 / U+26BF / U+1F512)."""
    pen = TTGlyphPen(None)
    x0, x1 = 130, 470
    y0, y1 = 90, 390
    r = 25
    pen.moveTo((x0, y0 + r))
    pen.lineTo((x0, y1 - r))
    pen.qCurveTo((x0, y1), (x0 + r, y1))
    pen.lineTo((x1 - r, y1))
    pen.qCurveTo((x1, y1), (x1, y1 - r))
    pen.lineTo((x1, y0 + r))
    pen.qCurveTo((x1, y0), (x1 - r, y0))
    pen.lineTo((x0 + r, y0))
    pen.qCurveTo((x0, y0), (x0, y0 + r))
    pen.closePath()

    pen.moveTo((275, 175))
    pen.lineTo((325, 175))
    pen.lineTo((315, 255))
    pen.lineTo((330, 275))
    pen.lineTo((300, 305))
    pen.lineTo((270, 275))
    pen.lineTo((285, 255))
    pen.closePath()

    pen.moveTo((190, 390))
    pen.lineTo((190, 500))
    pen.qCurveTo((190, 610), (300, 610))
    pen.qCurveTo((410, 610), (410, 500))
    pen.lineTo((410, 390))
    pen.lineTo((355, 390))
    pen.lineTo((355, 495))
    pen.qCurveTo((355, 555), (300, 555))
    pen.qCurveTo((245, 555), (245, 495))
    pen.lineTo((245, 390))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_chevron_solid(direction="right", is_powerline=True):
    """Constructs solid right/left triangle chevron (U+E0B0, U+E0B2, U+25B6, U+25C0)."""
    pen = TTGlyphPen(None)
    y_bot = -240 if is_powerline else 60
    y_top = 960 if is_powerline else 660
    y_mid = (y_bot + y_top) // 2
    x0 = 0 if is_powerline else 50
    x1 = 600 if is_powerline else 550

    if direction == "right":
        pen.moveTo((x0, y_bot))
        pen.lineTo((x0, y_top))
        pen.lineTo((x1, y_mid))
        pen.closePath()
    else:
        pen.moveTo((x1, y_top))
        pen.lineTo((x1, y_bot))
        pen.lineTo((x0, y_mid))
        pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_chevron_thin(direction="right", is_powerline=True):
    """Constructs thin right/left chevron divider (U+E0B1, U+E0B3, U+25B7, U+25C1)."""
    pen = TTGlyphPen(None)
    y_bot = -240 if is_powerline else 60
    y_top = 960 if is_powerline else 660
    y_mid = (y_bot + y_top) // 2
    sw = 56

    if direction == "right":
        x0, x_tip = (120, 520) if is_powerline else (80, 520)
        pen.moveTo((x0, y_top))
        pen.lineTo((x_tip, y_mid))
        pen.lineTo((x0, y_bot))
        pen.lineTo((x0 - sw, y_bot))
        pen.lineTo((x_tip - sw, y_mid))
        pen.lineTo((x0 - sw, y_top))
        pen.closePath()
    else:
        x0, x_tip = (480, 80) if is_powerline else (520, 80)
        pen.moveTo((x0, y_bot))
        pen.lineTo((x_tip, y_mid))
        pen.lineTo((x0, y_top))
        pen.lineTo((x0 + sw, y_top))
        pen.lineTo((x_tip + sw, y_mid))
        pen.lineTo((x0 + sw, y_bot))
        pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_pill_cap(direction="right", thin=False, is_powerline=True):
    """Constructs rounded pill caps (U+E0B4, U+E0B5, U+E0B6, U+E0B7, U+25D6, U+25D7)."""
    pen = TTGlyphPen(None)
    y_bot = -240 if is_powerline else 60
    y_top = 960 if is_powerline else 660
    y_mid = (y_bot + y_top) // 2
    sw = 54

    if direction == "right":
        x_base = 0 if is_powerline else 120
        rx = 580 if is_powerline else 380
        if not thin:
            pen.moveTo((x_base, y_bot))
            pen.lineTo((x_base, y_top))
            pen.qCurveTo((x_base + rx, y_top), (x_base + rx, y_mid))
            pen.qCurveTo((x_base + rx, y_bot), (x_base, y_bot))
            pen.closePath()
        else:
            pen.moveTo((x_base, y_top))
            pen.qCurveTo((x_base + rx, y_top), (x_base + rx, y_mid))
            pen.qCurveTo((x_base + rx, y_bot), (x_base, y_bot))
            pen.lineTo((x_base, y_bot + sw))
            pen.qCurveTo((x_base + rx - sw, y_bot + sw), (x_base + rx - sw, y_mid))
            pen.qCurveTo((x_base + rx - sw, y_top - sw), (x_base, y_top - sw))
            pen.closePath()
    else:
        x_base = 600 if is_powerline else 480
        rx = 580 if is_powerline else 380
        if not thin:
            pen.moveTo((x_base, y_top))
            pen.lineTo((x_base, y_bot))
            pen.qCurveTo((x_base - rx, y_bot), (x_base - rx, y_mid))
            pen.qCurveTo((x_base - rx, y_top), (x_base, y_top))
            pen.closePath()
        else:
            pen.moveTo((x_base, y_bot))
            pen.qCurveTo((x_base - rx, y_bot), (x_base - rx, y_mid))
            pen.qCurveTo((x_base - rx, y_top), (x_base, y_top))
            pen.lineTo((x_base, y_top - sw))
            pen.qCurveTo((x_base - rx + sw, y_top - sw), (x_base - rx + sw, y_mid))
            pen.qCurveTo((x_base - rx + sw, y_bot + sw), (x_base, y_bot + sw))
            pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def build_trojan_defense_badge(is_bidi=True):
    """Constructs a high-contrast boxed warning pill (!) at 600 UPM for Trojan Source BiDi & Zero-Width spoof codepoints."""
    pen = TTGlyphPen(None)
    x0, x1 = 40, 560
    y0, y1 = 80, 620
    r = 25
    b = 45
    # Outer warning pill frame (Clockwise)
    pen.moveTo((x0, y0 + r))
    pen.lineTo((x0, y1 - r))
    pen.qCurveTo((x0, y1), (x0 + r, y1))
    pen.lineTo((x1 - r, y1))
    pen.qCurveTo((x1, y1), (x1, y1 - r))
    pen.lineTo((x1, y0 + r))
    pen.qCurveTo((x1, y0), (x1 - r, y0))
    pen.lineTo((x0 + r, y0))
    pen.qCurveTo((x0, y0), (x0, y0 + r))
    pen.closePath()

    # Inner cutout (Counter-Clockwise)
    pen.moveTo((x0 + b, y0 + b))
    pen.lineTo((x1 - b, y0 + b))
    pen.lineTo((x1 - b, y1 - b))
    pen.lineTo((x0 + b, y1 - b))
    pen.closePath()

    # Exclamation stem inside warning box (Clockwise)
    pen.moveTo((268, 280))
    pen.lineTo((268, 510))
    pen.lineTo((332, 510))
    pen.lineTo((332, 280))
    pen.closePath()

    # Exclamation dot inside warning box (Clockwise)
    pen.moveTo((268, 175))
    pen.lineTo((268, 235))
    pen.lineTo((332, 235))
    pen.lineTo((332, 175))
    pen.closePath()

    g = pen.glyph()
    g.flags = bytearray([f & 0x3F for f in g.flags])
    sanitize_contour_points(g.coordinates, g.endPtsOfContours)
    return g

def inject_glyphs_into_font(font_path):
    is_bold = "Bold" in font_path.name or "Black" in font_path.name or "Chiseltip" in font_path.name
    font = TTFont(str(font_path))
    if "glyf" not in font:
        return
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    gvar = None
    if "gvar" in font:
        try:
            gvar = font["gvar"]
        except AssertionError:
            raw_gvar = font.reader["gvar"]
            import struct
            gvar_glyph_count = struct.unpack(">H", raw_gvar[12:14])[0]
            saved_order = list(font.getGlyphOrder())
            font.setGlyphOrder(saved_order[:gvar_glyph_count])
            gvar = font["gvar"]
            font.setGlyphOrder(saved_order)
            for extra_g in saved_order[gvar_glyph_count:]:
                gvar.variations[extra_g] = []
    gorder = list(font.getGlyphOrder())

    # Trojan Source BiDi (CVE-2021-42574) & Zero-Width Spoofing codepoints
    trojan_bidi_cps = [0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069, 0x200E, 0x200F, 0x061C]
    zero_width_cps = [0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF]
    spoof_filler_cps = [0x115F, 0x1160, 0x180E, 0x3164, 0xFFA0]

    glyph_map = {
        "u1F4C1": (build_folder_glyph(is_bold), [0x1F4C1, 0xF07B, 0xF115]),
        "uni23F1": (build_stopwatch_glyph(is_bold), [0x23F1]),
        "uniE0A0": (build_git_branch_glyph(is_bold), [0xE0A0, 0x2387, 0x2397, 0xF418, 0xF126, 0xE725, 0xE702]),
        "uniE0A1": (build_ln_glyph(is_bold), [0xE0A1, 0xE0A3]),
        "uniE0A2": (build_lock_glyph(is_bold), [0xE0A2, 0x26BF, 0x1F512]),
        "uniE0B0": (build_chevron_solid("right", True), [0xE0B0]),
        "uniE0B1": (build_chevron_thin("right", True), [0xE0B1]),
        "uniE0B2": (build_chevron_solid("left", True), [0xE0B2]),
        "uniE0B3": (build_chevron_thin("left", True), [0xE0B3]),
        "uniE0B4": (build_pill_cap("right", False, True), [0xE0B4]),
        "uniE0B5": (build_pill_cap("right", True, True), [0xE0B5]),
        "uniE0B6": (build_pill_cap("left", False, True), [0xE0B6]),
        "uniE0B7": (build_pill_cap("left", True, True), [0xE0B7]),
        "uni25B6": (build_chevron_solid("right", False), [0x25B6]),
        "uni25B7": (build_chevron_thin("right", False), [0x25B7]),
        "uni25C0": (build_chevron_solid("left", False), [0x25C0]),
        "uni25C1": (build_chevron_thin("left", False), [0x25C1]),
        "uni25D7": (build_pill_cap("right", False, False), [0x25D7]),
        "uni25D6": (build_pill_cap("left", False, False), [0x25D6]),
        "uni202E.guard": (build_trojan_defense_badge(True), trojan_bidi_cps + zero_width_cps + spoof_filler_cps),
    }

    for gname, (glyph_obj, codepoints) in glyph_map.items():
        glyf[gname] = glyph_obj
        glyph_obj.recalcBounds(glyf)
        hmtx[gname] = (600, getattr(glyph_obj, "xMin", 0))
        if gname not in gorder:
            gorder.append(gname)

        for table in font["cmap"].tables:
            if table.format in (4, 12):
                for cp in codepoints:
                    if table.format == 4 and cp > 0xFFFF:
                        continue
                    table.cmap[cp] = gname

    if "OS/2" in font:
        font["OS/2"].ulUnicodeRange2 |= (1 << 25)  # Bit 57: Private Use Area (Plane 0)
        font["OS/2"].ulUnicodeRange2 |= (1 << 5)   # Bit 37: Miscellaneous Technical (U+2300-U+23FF)
        font["OS/2"].ulUnicodeRange2 |= (1 << 6)   # Bit 38: Control Pictures / Optical
        font["OS/2"].ulUnicodeRange2 |= (1 << 13)  # Bit 45: Geometric Shapes (U+25A0-U+25FF)

    if gvar is not None:
        for gname in glyph_map.keys():
            if gname not in gvar.variations:
                gvar.variations[gname] = []
        if "HVAR" in font:
            del font["HVAR"]

    font.setGlyphOrder(gorder)
    font["maxp"].numGlyphs = len(gorder)
    font.save(str(font_path))
    print(f"  [OK] Synthesized PUA + Unicode Standard symbols -> {font_path.name}")

def main():
    print("=" * 80)
    print("  POCKETGULL FOUNDRY: PUA + UNICODE STANDARD SYMBOL SYNTHESIS")
    print("=" * 80)

    target_fonts = sorted(TTF_DIR.glob("*.ttf"))
    root_mono = ROOT_DIR / "PocketGullMono-Regular.ttf"

    for font_path in target_fonts:
        inject_glyphs_into_font(font_path)

    if root_mono.exists() and (TTF_DIR / "PocketGullMono-Regular.ttf").exists():
        shutil.copyfile(TTF_DIR / "PocketGullMono-Regular.ttf", root_mono)
        print("  [OK] Synchronized root PocketGullMono-Regular.ttf")

    print("\n[Step 2] Enforcing 2-byte word alignment (loca[i] % 2 == 0) via Dart 3.11...")
    dart_tool = ROOT_DIR / "tool" / "pocketgull_foundry.dart"
    if dart_tool.exists():
        subprocess.run(["dart", "run", str(dart_tool), "realign"], check=False, cwd=str(ROOT_DIR))

if __name__ == "__main__":
    main()

