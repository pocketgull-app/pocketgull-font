#!/usr/bin/env python3
"""
PocketGull Typefoundry: PocketGull Slab Generator v2.0
=====================================================
Engineers the fourth pillar of the superfamily: PocketGull Slab
(PocketGull-Slab-Regular and PocketGull-Slab-Bold) for high-impact
clinical reading, display titling, and telemetry legibility.

Features:
- Sturdy bracketed humanist slab serifs derived from clinical I.serif
- Quadratic fillets preventing ink clotting on EHR displays and thermal printers
- ISMP character safeguards:
    * Capital 'I': Bilateral serifs top and bottom (ss02)
    * Lowercase 'l': Top entry spur + curved outward foot sweep (cv05)
    * Numeral '1': Angled beak flag + broad flat baseline slab
    * Slashed zero '0' (cv08)
    * Calibrated heart tittle grounding at y = 687.5 UPM (cv09 / .philocardia-heart)
- Corrected topological serifier:
    * D, B, b: Unilateral leftward stem serifs; 0 spurs cutting into or through bowls
    * d: Top entry spur at y = 760 ascender; rightward baseline foot; clean round bowl
    * P, R: Top-left entry spur; bilateral baseline foot; clean bowls
    * h, k, l: Top entry spur at y = 760 ascender; clean arches; baseline feet
    * m, n, p, r, u: Top entry spurs at y = 536; clean arches & bowls
- 1000 UPM standard em-square, 2-byte word alignment (loca[i] % 2 == 0), bit-7 flag clearing
- Google Fonts Option 5 naming compliance
"""

import os
import sys
import copy
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(r"c:\Users\philg\Pocketgull\pocketgull-typeface")
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

def clean_glyph_geometry(glyph):
    if glyph.numberOfContours <= 0:
        return
    coords = list(glyph.coordinates)
    flags = list(glyph.flags)
    endPts = list(glyph.endPtsOfContours)
    new_coords, new_flags, new_endPts = [], [], []
    start = 0
    for end in endPts:
        pts = coords[start:end+1]
        flgs = flags[start:end+1]
        filtered_pts, filtered_flgs = [], []
        for i in range(len(pts)):
            if not filtered_pts or pts[i] != filtered_pts[-1]:
                filtered_pts.append(pts[i])
                filtered_flgs.append(flgs[i] & 0x3F)
        if len(filtered_pts) > 1 and filtered_pts[0] == filtered_pts[-1]:
            filtered_pts = filtered_pts[:-1]
            filtered_flgs = filtered_flgs[:-1]
        if len(filtered_pts) >= 3:
            new_coords.extend(filtered_pts)
            new_flags.extend(filtered_flgs)
            new_endPts.append(len(new_coords) - 1)
        start = end + 1
    glyph.coordinates = GlyphCoordinates(new_coords)
    glyph.flags = bytearray(new_flags)
    glyph.endPtsOfContours = new_endPts

def make_serif_nodes(xl, xr, y, O, H_slab, H_rise, mode, pos, going_rtl):
    H_tot = H_slab + H_rise
    if pos == 'base':
        if mode == 'bilateral':
            nodes = [
                (xl, y + H_tot),
                (xl - O, y + H_slab),
                (xl - O, y),
                (xr + O, y),
                (xr + O, y + H_slab),
                (xr, y + H_tot)
            ]
        elif mode == 'left_only':
            nodes = [
                (xl, y + H_tot),
                (xl - O, y + H_slab),
                (xl - O, y),
                (xr, y)
            ]
        elif mode == 'right_only':
            nodes = [
                (xl, y),
                (xr + O, y),
                (xr + O, y + H_slab),
                (xr, y + H_tot)
            ]
    elif pos == 'top':
        if mode == 'bilateral':
            nodes = [
                (xl, y - H_tot),
                (xl - O, y - H_slab),
                (xl - O, y),
                (xr + O, y),
                (xr + O, y - H_slab),
                (xr, y - H_tot)
            ]
        elif mode == 'left_only':
            nodes = [
                (xl, y - H_tot),
                (xl - O, y - H_slab),
                (xl - O, y),
                (xr, y)
            ]
        elif mode == 'right_only':
            nodes = [
                (xl, y),
                (xr + O, y),
                (xr + O, y - H_slab),
                (xr, y - H_tot)
            ]
    elif pos == 'descender':
        nodes = [
            (xl, y + H_tot),
            (xl - O, y + H_slab),
            (xl - O, y),
            (xr + O, y),
            (xr + O, y + H_slab),
            (xr, y + H_tot)
        ]

    if going_rtl:
        nodes.reverse()
    return nodes

def serify_stem(pts, flags, gname, O=52, H_slab=48, H_rise=18):
    n = len(pts)
    new_pts = []
    new_flgs = []
    i = 0
    while i < n:
        p0 = pts[i]
        p1 = pts[(i+1)%n]
        dx = abs(p0[0] - p1[0])
        dy = abs(p0[1] - p1[1])
        y_avg = (p0[1] + p1[1]) / 2.0
        xl = min(p0[0], p1[0])
        xr = max(p0[0], p1[0])
        going_rtl = p0[0] > p1[0]

        # Caps D, B: special handling (stem at left edge x=97)
        if gname in ['D', 'B']:
            # Top-left corner at (stem_x, 714)
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                new_pts.append(p0)
                new_flgs.append(flags[i])
                H_tot = H_slab + H_rise
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            # Baseline corner at (stem_x, 0)
            elif abs(p1[1] - 0) <= 6 and p0[0] > p1[0] and abs(p0[1] - 0) <= 6 and p1[0] < 200:
                H_tot = H_slab + H_rise
                foot = [
                    (p1[0], 0),
                    (p1[0] - O, 0),
                    (p1[0] - O, H_slab),
                    (p1[0], H_tot)
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in foot:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue

        # Caps P, R:
        elif gname in ['P', 'R']:
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                new_pts.append(p0)
                new_flgs.append(flags[i])
                H_tot = H_slab + H_rise
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 220 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase b:
        elif gname == 'b':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 200 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'left_only', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase d:
        elif gname == 'd':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl >= 400 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'right_only', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Standard uppercase stems (H, K, M, N, T, U):
        elif gname in ['H', 'K', 'M', 'N', 'T', 'U']:
            if gname != 'T' and dy <= 4 and abs(y_avg - 714) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 714, O, H_slab, H_rise, 'bilateral', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase ascenders (h, k):
        elif gname in ['h', 'k']:
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase x-height stems (m, n, r):
        elif gname in ['m', 'n', 'r']:
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'bilateral', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase p:
        elif gname == 'p':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - (-240)) <= 8 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, -240, O, H_slab, H_rise, 'bilateral', 'descender', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        # Lowercase u:
        elif gname == 'u':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_rise, 'left_only', 'top', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and xl >= 380 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_rise, 'right_only', 'base', going_rtl)
                for pt in nodes:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 2
                continue

        new_pts.append(p0)
        new_flgs.append(flags[i])
        i += 1

    return new_pts, new_flgs

def process_slab_font(src_name, family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=400, is_bold=False):
    style_suffix = "Bold" if is_bold else "Regular"
    ps_name = f"{ps_family}-{style_suffix}"
    out_ttf = TTF_DIR / f"{ps_name}.ttf"
    out_woff2 = WOFF2_DIR / f"{ps_name}.woff2"
    public_ttf = PUBLIC_DIR / f"{ps_name}.ttf"
    public_woff2 = PUBLIC_DIR / f"{ps_name}.woff2"

    print(f"\n==================================================================")
    print(f"Generating {family_name} {style_suffix} (from {src_name})")
    print(f"==================================================================")

    font = TTFont(TTF_DIR / src_name)
    glyf = font['glyf']
    hmtx = font['hmtx']

    # Slab parameters calibrated to weight
    if is_bold:
        O = 65
        H_slab = 68
        H_rise = 26
    else:
        O = 52
        H_slab = 48
        H_rise = 18

    target_glyphs = ['H', 'M', 'N', 'K', 'B', 'D', 'P', 'R', 'T', 'U', 'b', 'd', 'h', 'k', 'm', 'n', 'p', 'r', 'u']
    transformed = 0

    for gname in target_glyphs:
        if gname not in glyf:
            continue
        g = glyf[gname]
        if g.numberOfContours <= 0:
            continue

        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)

        new_coords = []
        new_flags = []
        new_endPts = []
        start = 0

        for end in endPts:
            c_pts = coords[start:end+1]
            c_flgs = flags[start:end+1]
            s_pts, s_flgs = serify_stem(c_pts, c_flgs, gname, O=O, H_slab=H_slab, H_rise=H_rise)
            new_coords.extend(s_pts)
            new_flags.extend(s_flgs)
            new_endPts.append(len(new_coords) - 1)
            start = end + 1

        g.coordinates = GlyphCoordinates(new_coords)
        g.flags = bytearray(new_flags)
        g.endPtsOfContours = new_endPts
        clean_glyph_geometry(g)
        g.recalcBounds(glyf)

        orig_adv, orig_lsb = hmtx[gname]
        new_adv = max(orig_adv, int(g.xMax + 45))
        hmtx[gname] = (new_adv, g.xMin)
        transformed += 1

    # ISMP Special Glyphs:
    # 1. Capital 'I': Copy from I.serif (authenticated ISMP bilateral serifs)
    if 'I.serif' in glyf:
        glyf['I'] = copy.deepcopy(glyf['I.serif'])
        clean_glyph_geometry(glyf['I'])
        glyf['I'].recalcBounds(glyf)
        hmtx['I'] = (max(hmtx['I.serif'][0], glyf['I'].xMax + 45), glyf['I'].xMin)
        print("  • Injected authenticated ISMP Capital 'I' (ss02 bilateral serifs)")

    # 2. Lowercase 'l': Keep curved foot (cv05) and add top entry spur
    if 'l' in glyf:
        g = glyf['l']
        coords = list(g.coordinates)
        flags = list(g.flags)
        s_pts, s_flgs = serify_stem(coords, flags, 'h', O=O, H_slab=H_slab, H_rise=H_rise)
        g.coordinates = GlyphCoordinates(s_pts)
        g.flags = bytearray(s_flgs)
        g.endPtsOfContours = [len(s_pts) - 1]
        clean_glyph_geometry(g)
        g.recalcBounds(glyf)
        hmtx['l'] = (max(hmtx['l'][0], g.xMax + 45), g.xMin)
        print("  • Injected ISMP Lowercase 'l' (top entry spur + outward terminal curved foot)")

    # 3. Lowercase 'i': Base serif + top spur, preserves heart tittle
    if 'i' in glyf:
        g = glyf['i']
        coords = list(g.coordinates)
        flags = list(g.flags)
        endPts = list(g.endPtsOfContours)
        if len(endPts) == 2:
            stem_pts = coords[:endPts[0]+1]
            stem_flgs = flags[:endPts[0]+1]
            dot_pts = coords[endPts[0]+1:]
            dot_flgs = flags[endPts[0]+1:]
            
            s_pts, s_flgs = serify_stem(stem_pts, stem_flgs, 'n', O=O, H_slab=H_slab, H_rise=H_rise)
            g.coordinates = GlyphCoordinates(s_pts + dot_pts)
            g.flags = bytearray(s_flgs + dot_flgs)
            g.endPtsOfContours = [len(s_pts) - 1, len(s_pts) + len(dot_pts) - 1]
            clean_glyph_geometry(g)
            g.recalcBounds(glyf)
            hmtx['i'] = (max(hmtx['i'][0], g.xMax + 45), g.xMin)
            print("  • Injected ISMP Lowercase 'i' (calibrated tittle + base slab & entry spur)")

    print(f"  -> Transformed {transformed} letterforms with robust slab serifs.")

    # 4. OpenType Option 5 Metadata
    print("Updating OpenType metadata & Option 5 naming table...")
    version_str = "Version 3.000; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = font['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]

    def add_name(name_id, text):
        name_table.addMultilingualName({'en': text}, font, nameID=name_id)

    add_name(0, copyright_str)
    add_name(1, family_name)
    add_name(2, style_suffix)
    add_name(3, f"3.000;POCK;{ps_name}")
    add_name(4, f"{family_name} {style_suffix}")
    add_name(5, version_str)
    add_name(6, ps_name)
    add_name(16, family_name)
    add_name(17, style_suffix)

    font['head'].fontRevision = 3.0
    font['head'].macStyle = 0x0001 if is_bold else 0x0000

    if 'OS/2' in font:
        font['OS/2'].usWeightClass = weight_class
        if is_bold:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x20 | 0x80
        else:
            font['OS/2'].fsSelection = (font['OS/2'].fsSelection & ~0x01 & ~0x20) | 0x40 | 0x80
        font['OS/2'].achVendID = 'POCK'
        font['OS/2'].fsType = 0x0000

    font.save(str(out_ttf))
    font.close()

    # Realign loca/glyf to 2-byte word boundaries
    font = TTFont(str(out_ttf))
    glyf = font['glyf']
    for gn in font.getGlyphOrder():
        glyph = glyf[gn]
        if hasattr(glyph, 'data') and glyph.data and len(glyph.data) % 2 != 0:
            glyph.data = glyph.data + b'\x00'
    font.save(str(out_ttf))
    font.close()

    # WOFF2 compression
    compress(str(out_ttf), str(out_woff2))

    # Sync to public mirror
    if PUBLIC_DIR.exists():
        shutil.copy2(str(out_ttf), str(public_ttf))
        shutil.copy2(str(out_woff2), str(public_woff2))

    print(f"[SUCCESS] Compiled {out_ttf}")
    print(f"[SUCCESS] Compressed {out_woff2} ({out_woff2.stat().st_size:,} bytes)")

def build_slab_superfamily():
    print("==================================================================")
    print("POCKETGULL TYPEFOUNDRY: SLAB MASTERFAMILY COMPILER")
    print("==================================================================")
    # Build Canonical PocketGull Slab
    process_slab_font("PocketGull-Regular.ttf", family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=400, is_bold=False)
    process_slab_font("PocketGull-Bold.ttf", family_name="PocketGull Slab", ps_family="PocketGull-Slab", weight_class=700, is_bold=True)
    
    # Also update PocketGull Serif files with identical clean contours for compatibility
    process_slab_font("PocketGull-Regular.ttf", family_name="PocketGull Serif", ps_family="PocketGull-Serif", weight_class=400, is_bold=False)
    process_slab_font("PocketGull-Bold.ttf", family_name="PocketGull Serif", ps_family="PocketGull-Serif", weight_class=700, is_bold=True)
    
    print("\n[ALL DONE] PocketGull Slab & Serif Regular and Bold successfully compiled!")

if __name__ == '__main__':
    build_slab_superfamily()
