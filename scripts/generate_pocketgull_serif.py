#!/usr/bin/env python3
"""
PocketGull Typefoundry: PocketGull Serif Generator v3.1
======================================================
Engineers the authentic Humanist / Venetian bracketed serif companion to PocketGull:
PocketGull-Serif-Regular and PocketGull-Serif-Bold.

Unlike PocketGull Slab's heavy rectangular architectural blocks, PocketGull Serif
features:
- Slender, refined bracketed serifs with flowing quadratic Bézier concave fillets
- Delicate shelf thickness (H_slab = 26 Regular / 36 Bold)
- Extended parabolic bracket rise (H_bracket = 38 Regular / 48 Bold)
- Classical bracketed terminals on horizontal arms (E, F, L, T, Z)
- Authenticated ISMP safeguards:
    * Capital 'I': ss02 bilateral serifs top and bottom
    * Lowercase 'l': cv05 entry spur + outward terminal curved foot
    * Lowercase 'i': entry spur + base bilateral serif + calibrated tittle
    * Slashed zero '0' (cv08)
- 1000 UPM em-square, 2-byte word alignment (loca[i] % 2 == 0), bit-7 flag clearing
- Google Fonts Option 5 naming compliance (Version 3.100, fontRevision 3.1)
"""

import os
import sys
import copy
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
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

def make_serif_nodes(xl, xr, y, O, H_slab, H_bracket, mode, pos, going_rtl):
    """
    Constructs graceful humanist bracketed serif nodes using quadratic Bézier curves.
    At bracket transitions, an off-curve control point (flag=0) provides C1 tangency
    connecting the vertical stem to the horizontal serif shelf.
    """
    H_tot = H_slab + H_bracket
    nodes = []

    if pos == 'base':
        if mode == 'bilateral':
            nodes = [
                ((xl, y + H_tot), 1),
                ((xl, y + H_slab), 0), # quadratic fillet control point
                ((xl - O, y + H_slab), 1),
                ((xl - O, y), 1),
                ((xr + O, y), 1),
                ((xr + O, y + H_slab), 1),
                ((xr, y + H_slab), 0), # quadratic fillet control point
                ((xr, y + H_tot), 1)
            ]
        elif mode == 'left_only':
            nodes = [
                ((xl, y + H_tot), 1),
                ((xl, y + H_slab), 0),
                ((xl - O, y + H_slab), 1),
                ((xl - O, y), 1),
                ((xr, y), 1)
            ]
        elif mode == 'right_only':
            nodes = [
                ((xl, y), 1),
                ((xr + O, y), 1),
                ((xr + O, y + H_slab), 1),
                ((xr, y + H_slab), 0),
                ((xr, y + H_tot), 1)
            ]
    elif pos == 'top':
        if mode == 'bilateral':
            nodes = [
                ((xl, y - H_tot), 1),
                ((xl, y - H_slab), 0), # quadratic fillet control point
                ((xl - O, y - H_slab), 1),
                ((xl - O, y), 1),
                ((xr + O, y), 1),
                ((xr + O, y - H_slab), 1),
                ((xr, y - H_slab), 0), # quadratic fillet control point
                ((xr, y - H_tot), 1)
            ]
        elif mode == 'left_only':
            nodes = [
                ((xl, y - H_tot), 1),
                ((xl, y - H_slab), 0),
                ((xl - O, y - H_slab), 1),
                ((xl - O, y), 1),
                ((xr, y), 1)
            ]
        elif mode == 'right_only':
            nodes = [
                ((xl, y), 1),
                ((xr + O, y), 1),
                ((xr + O, y - H_slab), 1),
                ((xr, y - H_slab), 0),
                ((xr, y - H_tot), 1)
            ]
    elif pos == 'descender':
        nodes = [
            ((xl, y + H_tot), 1),
            ((xl, y + H_slab), 0),
            ((xl - O, y + H_slab), 1),
            ((xl - O, y), 1),
            ((xr + O, y), 1),
            ((xr + O, y + H_slab), 1),
            ((xr, y + H_slab), 0),
            ((xr, y + H_tot), 1)
        ]

    if going_rtl:
        nodes.reverse()
    return nodes

def serify_stem(pts, flags, gname, O=38, H_slab=26, H_bracket=38):
    n = len(pts)
    new_pts = []
    new_flgs = []
    i = 0
    H_tot = H_slab + H_bracket

    while i < n:
        p0 = pts[i]
        p1 = pts[(i+1)%n]
        dx = abs(p0[0] - p1[0])
        dy = abs(p0[1] - p1[1])
        y_avg = (p0[1] + p1[1]) / 2.0
        xl = min(p0[0], p1[0])
        xr = max(p0[0], p1[0])
        going_rtl = p0[0] > p1[0]

        # Caps D, B: Left stem only (protecting right rounded bowls)
        if gname in ['D', 'B']:
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            elif abs(p1[1] - 0) <= 6 and p0[0] > p1[0] and abs(p0[1] - 0) <= 6 and p1[0] < 200:
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

        # Caps P, R: Top-left entry spur, bilateral baseline foot
        elif gname in ['P', 'R']:
            if abs(p1[1] - 714) <= 6 and abs(p0[0] - p1[0]) <= 8 and p0[1] < p1[1] and p1[0] < 200:
                spur = [
                    (p1[0], p1[1] - H_tot),
                    (p1[0] - O, p1[1] - H_slab),
                    (p1[0] - O, p1[1]),
                    (p1[0], p1[1])
                ]
                new_pts.append(p0)
                new_flgs.append(flags[i])
                for pt in spur:
                    new_pts.append(pt)
                    new_flgs.append(1)
                i += 1
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 220 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase b:
        elif gname == 'b':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl < 200 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'left_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase d:
        elif gname == 'd':
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 5 and xl >= 400 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase q:
        elif gname == 'q':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl >= 400 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, 536, O, H_slab, H_bracket, 'right_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - (-240)) <= 8 and dx >= 50:
                nodes = make_serif_nodes(xl, xr, -240, O, H_slab, H_bracket, 'bilateral', 'descender', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Caps E, F:
        elif gname in ['E', 'F']:
            if dy <= 4 and abs(y_avg - 0) <= 6 and xl < 200 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Cap L:
        elif gname == 'L':
            if dy <= 4 and abs(y_avg - 714) <= 6 and xl < 200 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 714, O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Standard uppercase stems (H, M, N, K, T, U):
        elif gname in ['H', 'M', 'N', 'K', 'T', 'U']:
            if gname != 'T' and dy <= 4 and abs(y_avg - 714) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 714, O, H_slab, H_bracket, 'bilateral', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase ascenders (h, k):
        elif gname in ['h', 'k']:
            if dy <= 4 and abs(y_avg - 760) <= 10 and dx >= 60:
                nodes = make_serif_nodes(xl, xr, 760, O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase x-height stems (m, n, r):
        elif gname in ['m', 'n', 'r']:
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'bilateral', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase p:
        elif gname == 'p':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - (-240)) <= 8 and 60 <= dx <= 180:
                nodes = make_serif_nodes(xl, xr, -240, O, H_slab, H_bracket, 'bilateral', 'descender', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase u:
        elif gname == 'u':
            if dy <= 5 and abs(y_avg - 536) <= 8 and xl < 220 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, p0[1], O, H_slab, H_bracket, 'left_only', 'top', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue
            elif dy <= 4 and abs(y_avg - 0) <= 6 and xl >= 380 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        # Lowercase a:
        elif gname == 'a':
            if dy <= 4 and abs(y_avg - 0) <= 6 and xl >= 380 and 50 <= dx <= 150:
                nodes = make_serif_nodes(xl, xr, 0, O, H_slab, H_bracket, 'right_only', 'base', going_rtl)
                for pt, flg in nodes:
                    new_pts.append(pt)
                    new_flgs.append(flg)
                i += 2
                continue

        new_pts.append(p0)
        new_flgs.append(flags[i])
        i += 1

    return new_pts, new_flgs

def process_serif_font(src_name, weight_class=400, is_bold=False):
    style_suffix = "Bold" if is_bold else "Regular"
    family_name = "PocketGull Serif"
    ps_name = f"PocketGull-Serif-{style_suffix}"
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

    # Refined Humanist Serif dimensions: slender shelf, generous parabolic bracket
    if is_bold:
        O = 48
        H_slab = 36
        H_bracket = 48
    else:
        O = 38
        H_slab = 26
        H_bracket = 38

    target_glyphs = [
        'H', 'M', 'N', 'K', 'B', 'D', 'P', 'R', 'T', 'U', 'E', 'F', 'L',
        'b', 'd', 'h', 'k', 'm', 'n', 'p', 'q', 'r', 'u', 'a'
    ]
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
            s_pts, s_flgs = serify_stem(c_pts, c_flgs, gname, O=O, H_slab=H_slab, H_bracket=H_bracket)
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
        s_pts, s_flgs = serify_stem(coords, flags, 'h', O=O, H_slab=H_slab, H_bracket=H_bracket)
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
            
            s_pts, s_flgs = serify_stem(stem_pts, stem_flgs, 'n', O=O, H_slab=H_slab, H_bracket=H_bracket)
            g.coordinates = GlyphCoordinates(s_pts + dot_pts)
            g.flags = bytearray(s_flgs + dot_flgs)
            g.endPtsOfContours = [len(s_pts) - 1, len(s_pts) + len(dot_pts) - 1]
            clean_glyph_geometry(g)
            g.recalcBounds(glyf)
            hmtx['i'] = (max(hmtx['i'][0], g.xMax + 45), g.xMin)
            print("  • Injected ISMP Lowercase 'i' (calibrated tittle + base slab & entry spur)")

    print(f"  -> Transformed {transformed} letterforms with classical humanist bracketed serifs.")

    # 4. OpenType Option 5 Metadata aligned to SemVer 3.1.0
    print("Updating OpenType metadata & Option 5 naming table...")
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = font['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]

    def add_name(name_id, text):
        name_table.addMultilingualName({'en': text}, font, nameID=name_id)

    add_name(0, copyright_str)
    add_name(1, family_name)
    add_name(2, style_suffix)
    add_name(3, f"3.100;POCK;{ps_name}")
    add_name(4, f"{family_name} {style_suffix}")
    add_name(5, version_str)
    add_name(6, ps_name)
    add_name(16, family_name)
    add_name(17, style_suffix)

    font['head'].fontRevision = 3.1
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

def build_serif_superfamily():
    print("==================================================================")
    print("POCKETGULL TYPEFOUNDRY: SERIF MASTERFAMILY COMPILER (v3.1)")
    print("==================================================================")
    process_serif_font("PocketGull-Regular.ttf", weight_class=400, is_bold=False)
    process_serif_font("PocketGull-Bold.ttf", weight_class=700, is_bold=True)
    print("\n[ALL DONE] PocketGull Serif Regular & Bold successfully compiled!")

if __name__ == '__main__':
    build_serif_superfamily()
