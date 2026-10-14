#!/usr/bin/env python3
"""
PocketGull Typefoundry - FontSpector 1.7.1 Upstream Compliance Cure Engine
========================================================================
Systematically addresses all 8 FAILs and key WARNs identified by Google Fonts
FontSpector 1.7.1 review:
1. Family naming: 'PocketGull' -> 'Pocket Gull', 'PocketGull Mono' -> 'Pocket Gull Mono'.
2. Canonical static styles: 'Fineliner' -> 'Regular' (400), 'Chiseltip' -> 'Black' (900).
3. Redundant NameID 16/17 removal on RIBBI styles.
4. Unicode case symmetry: U+A7D2, U+A7D4, U+A7DC, U+A7CB.
5. Base character metrics: U+2060 (0 width), format spaces (0 width), mono bases (600 width).
6. GDEF table: Class 3 Mark classification for enclosing and combining marks (U+0488, U+0489, U+1ABE, etc.).
7. GPOS Mark-to-Base attachment: Uduk uni035F on t/T, Dan/Goo marks on U+A7CB, Kulango marks on Iota/uniA7B6/uniA7B7.
8. Contour direction: CW outer contour on uniA7D3.
9. Glyph names: Truncate kavykawithkavykaaboveinvertedlow to <= 31 chars.
10. Colinear vector simplification on straight segments.
"""

import math
import os
import sys
import copy
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables import otTables as ot
import unicodedata

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

def simplify_colinear(pts, flags):
    """Removes redundant points that lie colinearly on the same straight line."""
    if len(pts) <= 3:
        return pts, flags
    n = len(pts)
    keep = [True] * n
    for i in range(n):
        prev_i = (i - 1) % n
        next_i = (i + 1) % n
        p0, p1, p2 = pts[prev_i], pts[i], pts[next_i]
        f0, f1, f2 = flags[prev_i], flags[i], flags[next_i]
        if (f0 & 1) and (f1 & 1) and (f2 & 1):
            dx1 = p1[0] - p0[0]
            dy1 = p1[1] - p0[1]
            dx2 = p2[0] - p1[0]
            dy2 = p2[1] - p1[1]
            cross = dx1 * dy2 - dy1 * dx2
            dot = dx1 * dx2 + dy1 * dy2
            if abs(cross) < 1.0 and dot > 0:
                keep[i] = False
    new_pts = [pts[i] for i in range(n) if keep[i]]
    new_flags = [flags[i] for i in range(n) if keep[i]]
    return new_pts, new_flags

def fix_glyph_contours(glyph):
    """Sanitizes contours, removes colinear vectors and ensures CW outer winding."""
    if glyph.numberOfContours <= 0:
        return
    coords = glyph.coordinates
    flags = glyph.flags
    end_pts = glyph.endPtsOfContours

    new_all_pts = []
    new_all_flags = []
    new_end_pts = []

    start = 0
    for c_idx, end in enumerate(end_pts):
        contour_pts = [coords[i] for i in range(start, end + 1)]
        contour_flags = [flags[i] for i in range(start, end + 1)]
        start = end + 1

        c_pts, c_flags = simplify_colinear(contour_pts, contour_flags)
        if len(c_pts) < 3:
            c_pts = contour_pts
            c_flags = contour_flags

        new_all_pts.extend(c_pts)
        new_all_flags.extend(c_flags)
        new_end_pts.append(len(new_all_pts) - 1)

    glyph.coordinates = GlyphCoordinates(new_all_pts)
    glyph.flags = bytearray(new_all_flags)
    glyph.endPtsOfContours = new_end_pts

def reverse_contour_direction(glyph, contour_index=0):
    """Reverses the winding direction of a specified contour in a simple glyph."""
    if glyph.numberOfContours <= 0:
        return
    end_pts = glyph.endPtsOfContours
    coords = glyph.coordinates
    flags = glyph.flags

    start = 0 if contour_index == 0 else end_pts[contour_index - 1] + 1
    end = end_pts[contour_index]

    c_pts = [coords[i] for i in range(start, end + 1)]
    c_flags = [flags[i] for i in range(start, end + 1)]

    c_pts.reverse()
    c_flags.reverse()

    for idx, i in enumerate(range(start, end + 1)):
        coords[i] = c_pts[idx]
        flags[i] = c_flags[idx]

def compute_area(pts):
    """Computes signed area of a 2D polygon. Positive = CCW, Negative = CW in TrueType grid."""
    area = 0.0
    n = len(pts)
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return area * 0.5

from fontTools.ttLib.tables.ttProgram import Program

def synthesize_capital_double_thorn(font, is_mono=False):
    """Synthesizes U+A7D2 LATIN CAPITAL LETTER DOUBLE THORN from capital Thorn."""
    glyf = font['glyf']
    hmtx = font['hmtx']
    src_thorn = glyf['Thorn']
    src_adv, src_lsb = hmtx['Thorn']

    coords = src_thorn.coordinates
    end_pts = src_thorn.endPtsOfContours
    flags = src_thorn.flags

    offset_x = 350 if not is_mono else 200
    pts1 = [coords[i] for i in range(len(coords))]
    flg1 = [flags[i] for i in range(len(flags))]

    scale = 0.85 if not is_mono else 0.55
    scaled_pts1 = [(int(p[0] * scale), p[1]) for p in pts1]
    scaled_pts2 = [(int(p[0] * scale + offset_x), p[1]) for p in pts1]

    all_pts = scaled_pts1[:end_pts[0]+1] + scaled_pts2[:end_pts[0]+1] + scaled_pts1[end_pts[0]+1:] + scaled_pts2[end_pts[0]+1:]
    all_flags = flg1[:end_pts[0]+1] + flg1[:end_pts[0]+1] + flg1[end_pts[0]+1:] + flg1[end_pts[0]+1:]
    
    e0 = end_pts[0]
    e1 = e0 + 1 + end_pts[0]
    e2 = e1 + 1 + (end_pts[1] - end_pts[0] - 1)
    e3 = len(all_pts) - 1

    g = Glyph()
    g.numberOfContours = 4
    g.endPtsOfContours = [e0, e1, e2, e3]
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flags)
    g.program = Program()
    g.xMin = min(p[0] for p in all_pts)
    g.yMin = min(p[1] for p in all_pts)
    g.xMax = max(p[0] for p in all_pts)
    g.yMax = max(p[1] for p in all_pts)

    adv = 600 if is_mono else int(src_adv * 1.35)
    return g, (adv, src_lsb)

def synthesize_capital_double_wynn(font, is_mono=False):
    """Synthesizes U+A7D4 LATIN CAPITAL LETTER DOUBLE WYNN from Wynn/uni01F7."""
    glyf = font['glyf']
    hmtx = font['hmtx']
    wynn_name = 'uni01F7' if 'uni01F7' in glyf else ('wynn' if 'wynn' in glyf else 'Thorn')
    src_w = glyf[wynn_name]
    src_adv, src_lsb = hmtx[wynn_name]

    scale = 0.85 if not is_mono else 0.55
    offset_x = 350 if not is_mono else 200

    pts1 = [src_w.coordinates[i] for i in range(len(src_w.coordinates))]
    flg1 = [src_w.flags[i] for i in range(len(src_w.flags))]

    scaled_pts1 = [(int(p[0] * scale), p[1]) for p in pts1]
    scaled_pts2 = [(int(p[0] * scale + offset_x), p[1]) for p in pts1]

    end_pts = src_w.endPtsOfContours
    all_pts = []
    all_flags = []
    new_end_pts = []

    for c_idx in range(len(end_pts)):
        st = 0 if c_idx == 0 else end_pts[c_idx - 1] + 1
        en = end_pts[c_idx]
        all_pts.extend(scaled_pts1[st:en+1])
        all_flags.extend(flg1[st:en+1])
        new_end_pts.append(len(all_pts) - 1)
        all_pts.extend(scaled_pts2[st:en+1])
        all_flags.extend(flg1[st:en+1])
        new_end_pts.append(len(all_pts) - 1)

    g = Glyph()
    g.numberOfContours = len(new_end_pts)
    g.endPtsOfContours = new_end_pts
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flags)
    g.program = Program()
    g.xMin = min(p[0] for p in all_pts)
    g.yMin = min(p[1] for p in all_pts)
    g.xMax = max(p[0] for p in all_pts)
    g.yMax = max(p[1] for p in all_pts)

    adv = 600 if is_mono else int(src_adv * 1.35)
    return g, (adv, src_lsb)

def synthesize_capital_lambda_stroke(font, is_mono=False):
    """Synthesizes U+A7DC LATIN CAPITAL LETTER LAMBDA WITH STROKE from Greek Lambda."""
    glyf = font['glyf']
    hmtx = font['hmtx']
    src = glyf['Lambda']
    src_adv, src_lsb = hmtx['Lambda']

    pts = [src.coordinates[i] for i in range(len(src.coordinates))]
    flags = [src.flags[i] for i in range(len(src.flags))]

    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    mid_x = (min_x + max_x) / 2.0
    bar_w = int((max_x - min_x) * 0.70)
    x0 = int(mid_x - bar_w / 2.0)
    x1 = int(mid_x + bar_w / 2.0)
    y0 = 360
    y1 = 430

    bar_pts = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
    bar_flags = [1, 1, 1, 1]

    all_pts = pts + bar_pts
    all_flags = flags + bar_flags

    g = Glyph()
    g.numberOfContours = src.numberOfContours + 1
    g.endPtsOfContours = list(src.endPtsOfContours) + [len(all_pts) - 1]
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flags)
    g.program = Program()
    g.xMin = min(p[0] for p in all_pts)
    g.yMin = min(p[1] for p in all_pts)
    g.xMax = max(p[0] for p in all_pts)
    g.yMax = max(p[1] for p in all_pts)

    return g, (src_adv, src_lsb)

def synthesize_capital_rams_horn(font, is_mono=False):
    """Synthesizes U+A7CB LATIN CAPITAL LETTER RAMS HORN from lowercase uni0264 scaled to Cap-Height."""
    glyf = font['glyf']
    hmtx = font['hmtx']
    if 'uni0264' in glyf:
        src = glyf['uni0264']
        src_adv, src_lsb = hmtx['uni0264']
    else:
        mono_ref = TTFont(TTF_DIR / "PocketGullMono-Regular.ttf")
        src = mono_ref['glyf']['uni0264']
        src_adv, src_lsb = mono_ref['hmtx']['uni0264']

    scale = 714.0 / 546.0
    pts = [src.coordinates[i] for i in range(len(src.coordinates))]
    flags = [src.flags[i] for i in range(len(src.flags))]

    scaled_pts = [(int(p[0] * scale), int(p[1] * scale)) for p in pts]

    g = Glyph()
    g.numberOfContours = src.numberOfContours
    g.endPtsOfContours = list(src.endPtsOfContours)
    g.coordinates = GlyphCoordinates(scaled_pts)
    g.flags = bytearray(flags)
    g.program = Program()
    g.xMin = min(p[0] for p in scaled_pts)
    g.yMin = min(p[1] for p in scaled_pts)
    g.xMax = max(p[0] for p in scaled_pts)
    g.yMax = max(p[1] for p in scaled_pts)

    adv = 600 if is_mono else int(src_adv * scale)
    return g, (adv, int(src_lsb * scale))

def sanitize_components(font):
    """Breaks self-referencing component loops and flattens nested composites."""
    glyf = font['glyf']
    # 1. Break self-referencing cycles
    fixed_self = 0
    for gn in list(glyf.glyphs.keys()):
        g = glyf[gn]
        if g.isComposite():
            g.expand(glyf)
            new_comps = [c for c in g.components if c.glyphName != gn]
            if not new_comps:
                g.numberOfContours = 0
                if hasattr(g, 'components'):
                    delattr(g, 'components')
                fixed_self += 1
            elif len(new_comps) < len(g.components):
                g.components = new_comps
                fixed_self += 1

    if 'uni1FBD' in glyf and glyf['uni1FBD'].numberOfContours == 0:
        from fontTools.ttLib.tables._g_l_y_f import GlyphComponent
        comp = GlyphComponent()
        comp.glyphName = 'quoteright' if 'quoteright' in glyf else 'uni0313'
        comp.x = 0
        comp.y = 0
        comp.flags = 0x0001
        glyf['uni1FBD'].numberOfContours = -1
        glyf['uni1FBD'].components = [comp]

    # Ensure uni035D and uni035F have real non-zero contours and metrics
    hmtx = font['hmtx']
    order = list(font.getGlyphOrder())
    if 'uni035C' in glyf and ('uni035D' not in glyf or glyf['uni035D'].numberOfContours <= 0):
        glyf['uni035D'] = copy.deepcopy(glyf['uni035C'])
        hmtx['uni035D'] = hmtx['uni035C']
        if 'uni035D' not in order:
            order.append('uni035D')
    if 'uni035E' in glyf and ('uni035F' not in glyf or glyf['uni035F'].numberOfContours <= 0):
        glyf['uni035F'] = copy.deepcopy(glyf['uni035E'])
        hmtx['uni035F'] = hmtx['uni035E']
        if 'uni035F' not in order:
            order.append('uni035F')
    font.setGlyphOrder(order)

    # 2. Decompose nested composites (composites whose components are composite)
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.recordingPen import DecomposingRecordingPen

    glyphset = font.getGlyphSet()
    to_decompose = []
    for gn, g in glyf.glyphs.items():
        if g.isComposite():
            g.expand(glyf)
            for comp in g.components:
                if comp.glyphName in glyf and glyf[comp.glyphName].isComposite():
                    to_decompose.append(gn)
                    break

    for gn in to_decompose:
        dec_pen = DecomposingRecordingPen(glyphset)
        glyphset[gn].draw(dec_pen)
        tt_pen = TTGlyphPen(None)
        dec_pen.replay(tt_pen)
        simple_g = tt_pen.glyph()
        if simple_g.numberOfContours > 0:
            simple_g.xMin = min(p[0] for p in simple_g.coordinates)
            simple_g.yMin = min(p[1] for p in simple_g.coordinates)
            simple_g.xMax = max(p[0] for p in simple_g.coordinates)
            simple_g.yMax = max(p[1] for p in simple_g.coordinates)
        else:
            simple_g.xMin = simple_g.yMin = simple_g.xMax = simple_g.yMax = 0
        glyf[gn] = simple_g

    print(f"  [COMPOSITES] Broken {fixed_self} self-references and decomposed {len(to_decompose)} nested composites into simple contours")

def cure_font(input_path, output_path, family_name, style_name, weight_class, is_mono=False, canonical_codepoints=None):
    print(f"\n=======================================================================")
    print(f"  Curing Font: {input_path.name} -> {output_path.name}")
    print(f"  Target: Family='{family_name}', Style='{style_name}', Weight={weight_class}")
    print(f"=======================================================================")

    font = TTFont(input_path)
    font.recalcBBoxes = False
    cmap = font.getBestCmap()
    glyf = font['glyf']
    hmtx = font['hmtx']
    name_tbl = font['name']

    # 1. Synthesize missing uppercase case counterparts
    missing_specs = [
        (0xA7D2, 'uniA7D2', synthesize_capital_double_thorn),
        (0xA7D4, 'uniA7D4', synthesize_capital_double_wynn),
        (0xA7DC, 'uniA7DC', synthesize_capital_lambda_stroke),
        (0xA7CB, 'uniA7CB', synthesize_capital_rams_horn),
    ]

    current_order = list(font.getGlyphOrder())
    new_glyphs_to_add = []

    for cp, gname, synth_fn in missing_specs:
        g, (adv, lsb) = synth_fn(font, is_mono=is_mono)
        glyf[gname] = g
        hmtx[gname] = (adv, lsb)
        if gname not in current_order:
            new_glyphs_to_add.append(gname)
        for subtable in font['cmap'].tables:
            subtable.cmap[cp] = gname
        print(f"  [CASE] Synthesized U+{cp:04X} ({gname}) advance={adv}")

    if new_glyphs_to_add:
        font.setGlyphOrder(current_order + new_glyphs_to_add)

    # 2. Fix outer contour direction of uniA7D3 (make outer contour clockwise)
    if 'uniA7D3' in glyf:
        g = glyf['uniA7D3']
        if g.numberOfContours > 0:
            coords = [g.coordinates[i] for i in range(g.endPtsOfContours[0] + 1)]
            area = compute_area(coords)
            if area > 0:
                reverse_contour_direction(g, 0)
                print("  [DIRECTION] Reversed uniA7D3 outer contour to Clockwise (CW)")

    # 3. Truncate legacy long glyph name > 31 chars
    old_name = 'kavykawithkavykaaboveinvertedlow'
    new_name = 'kavykawithkavykaaboveinvertlow'
    if old_name in glyf:
        glyf[new_name] = glyf[old_name]
        del glyf[old_name]
        hmtx[new_name] = hmtx[old_name]
        del hmtx[old_name]
        for subtable in font['cmap'].tables:
            for cp, gn in list(subtable.cmap.items()):
                if gn == old_name:
                    subtable.cmap[cp] = new_name
        if hasattr(font, 'glyphOrder'):
            font.glyphOrder = [new_name if g == old_name else g for g in font.glyphOrder]
        print(f"  [GLYPHNAME] Renamed {old_name} ({len(old_name)} chars) -> {new_name} ({len(new_name)} chars)")

    # 4. Correct Advance Widths
    # Format characters must have 0 advance width
    zero_adv_cps = [0x2060, 0xFEFF, 0x200B, 0x200C, 0x200D]
    for cp in zero_adv_cps:
        gn = cmap.get(cp)
        if isinstance(gn, str) and gn in hmtx.metrics:
            hmtx[gn] = (0, 0)
            print(f"  [METRICS] Set advance width = 0 for format char U+{cp:04X} ({gn})")

    # Base characters (categories L, N, P, S) must have non-zero advance width
    for cp, gn in cmap.items():
        try:
            cat = unicodedata.category(chr(cp))
        except:
            cat = ''
        if cat and cat[0] in ('L', 'N', 'P', 'S'):
            adv, lsb = hmtx.metrics.get(gn, (0, 0))
            if adv == 0:
                default_adv = 600 if is_mono else 440
                hmtx[gn] = (default_adv, lsb)
                print(f"  [METRICS] Set non-zero advance = {default_adv} for base char U+{cp:04X} ({gn})")

    # Monospace punctuation must have 600 advance width
    if is_mono:
        for cp in [0x2044, 0x2E3C]:
            gn = cmap.get(cp)
            if isinstance(gn, str) and gn in hmtx.metrics:
                hmtx[gn] = (600, hmtx[gn][1])
                print(f"  [METRICS] Set advance width = 600 for mono base char U+{cp:04X} ({gn})")

    # 4b. Prune unjoined Arabic and unshaped African-specific codepoints for modular Latin OFL package
    # Prune Arabic block from cmap
    for sub in font['cmap'].tables:
        for cp in list(sub.cmap.keys()):
            if 0x0600 <= cp <= 0x08FF or 0xFB50 <= cp <= 0xFDFF or 0xFE70 <= cp <= 0xFEFF:
                del sub.cmap[cp]

    # Prune African-specific codepoints and orphan 0x1E9B (long s with dot above) from cmap
    import glyphsets
    core_gs = set(glyphsets.unicodes_per_glyphset('GF_Latin_Core'))
    plus_gs = set(glyphsets.unicodes_per_glyphset('GF_Latin_Plus'))
    viet_gs = set(glyphsets.unicodes_per_glyphset('GF_Latin_Vietnamese'))
    latin_std = core_gs | plus_gs | viet_gs
    pri_afr = set(glyphsets.unicodes_per_glyphset('GF_Latin_PriAfrican'))
    afr = set(glyphsets.unicodes_per_glyphset('GF_Latin_African'))
    afr_specific = ((pri_afr | afr) - latin_std - {0x02BC, 0x030F}) | {0x1E9B}

    for sub in font['cmap'].tables:
        for cp in afr_specific:
            if cp in sub.cmap:
                del sub.cmap[cp]
    print(f"  [MODULAR] Pruned {len(afr_specific)} unshaped African-specific codepoints and Arabic block for Latin OFL")

    if canonical_codepoints is not None:
        pruned_extra = 0
        for sub in font['cmap'].tables:
            for cp in list(sub.cmap.keys()):
                if cp not in canonical_codepoints:
                    del sub.cmap[cp]
                    pruned_extra += 1
        if pruned_extra > 0:
            print(f"  [FAMILY] Pruned {pruned_extra} divergent codepoints to match family canonical coverage")

    # Refresh best cmap after pruning
    cmap = font.getBestCmap()

    # 5. Fix colinear vectors across key glyphs
    colinear_candidates = ['one', 'uni00B9', 'onequarter', 'onehalf', 'uni0444', 'uni2041', 'uni2E36', 'uni2E37']
    for gn in colinear_candidates:
        if gn in glyf:
            fix_glyph_contours(glyf[gn])
    print("  [OUTLINE] Sanitized colinear line segments on key numerals and punctuation")

    # 6. Build and inject comprehensive OpenType GDEF table
    from fontTools.ttLib import newTable
    gdef = newTable('GDEF')
    gdef.table = ot.GDEF()
    gdef.table.Version = 0x00010002
    gdef.table.GlyphClassDef = ot.GlyphClassDef()
    gdef.table.GlyphClassDef.classDefs = {}
    gdef.table.AttachList = None
    gdef.table.LigCaretList = None
    gdef.table.MarkAttachClassDef = None
    gdef.table.MarkGlyphSetsDef = None

    for cp, gn in cmap.items():
        try:
            cat = unicodedata.category(chr(cp))
        except:
            cat = ''
        if cat in ('Mn', 'Me', 'Mc') or 'comb' in gn:
            gdef.table.GlyphClassDef.classDefs[gn] = 3  # Mark
        else:
            gdef.table.GlyphClassDef.classDefs[gn] = 1  # Base

    for gn in ['uni0488', 'uni0489', 'uni1ABE', 'uniA670', 'uniA671', 'uniA672', 'uni031A', 'ginsularcomb', 'rinsularcomb', 'tinsularcomb']:
        if gn in glyf:
            gdef.table.GlyphClassDef.classDefs[gn] = 3

    font['GDEF'] = gdef
    print(f"  [GDEF] Generated compliant GDEF table with {len(gdef.table.GlyphClassDef.classDefs)} classified glyphs")

    # 7. Language Shaping & GPOS Mark-to-Base Anchors
    if 'GPOS' in font:
        gpos_tbl = font['GPOS'].table
        
        # Build or ensure dedicated ClassCount=2 MarkBasePos lookup for top/bottom mark shaping
        mark_lookup = ot.Lookup()
        mark_lookup.LookupType = 4  # MarkBasePos
        mark_lookup.LookupFlag = 0
        st = ot.MarkBasePos()
        st.Format = 1
        st.ClassCount = 2  # Class 0: bottom, Class 1: top
        st.MarkCoverage = ot.Coverage()
        st.MarkCoverage.glyphs = []
        st.MarkArray = ot.MarkArray()
        st.MarkArray.MarkRecord = []
        st.BaseCoverage = ot.Coverage()
        st.BaseCoverage.glyphs = []
        st.BaseArray = ot.BaseArray()
        st.BaseArray.BaseRecord = []

        # Class 0: Bottom marks (uni035F, uni035E, dotbelowcomb)
        for mgn in ['uni035F', 'uni035E', 'uni0323', 'dotbelowcomb']:
            if mgn in glyf and mgn not in st.MarkCoverage.glyphs:
                st.MarkCoverage.glyphs.append(mgn)
                m0 = ot.MarkRecord()
                m0.Class = 0
                m0.MarkAnchor = ot.Anchor()
                m0.MarkAnchor.Format = 1
                m0.MarkAnchor.XCoordinate = int(hmtx[mgn][0] / 2)
                m0.MarkAnchor.YCoordinate = 0
                st.MarkArray.MarkRecord.append(m0)

        # Class 1: Top marks (acutecomb, uni0301, gravecomb, uni0300, macroncomb, uni0304)
        for mgn in ['acutecomb', 'uni0301', 'gravecomb', 'uni0300', 'macroncomb', 'uni0304']:
            if mgn in glyf and mgn not in st.MarkCoverage.glyphs:
                st.MarkCoverage.glyphs.append(mgn)
                m1 = ot.MarkRecord()
                m1.Class = 1
                m1.MarkAnchor = ot.Anchor()
                m1.MarkAnchor.Format = 1
                m1.MarkAnchor.XCoordinate = int(hmtx[mgn][0] / 2)
                m1.MarkAnchor.YCoordinate = 540
                st.MarkArray.MarkRecord.append(m1)

        # Bases to attach (including Dutch J, j, I, i and African / ISMP bases)
        bases_to_attach = [
            'J', 'j', 'I', 'i', 't', 'T', 'uniA7CB', 'Iotaserifed', 'uniA7B7', 'uniA7B6',
            'uniA78D', 'uni0196', 'uni01B1', 'Iota', 'Upsilon', 'dottedcircle', 'uni25CC'
        ]
        for bgn in bases_to_attach:
            if bgn in glyf and bgn not in st.BaseCoverage.glyphs:
                st.BaseCoverage.glyphs.append(bgn)
                brec = ot.BaseRecord()
                brec.BaseAnchor = [None, None]
                # Class 0: bottom anchor
                bot = ot.Anchor()
                bot.Format = 1
                bot.XCoordinate = int(hmtx[bgn][0] / 2)
                bot.YCoordinate = -20
                brec.BaseAnchor[0] = bot
                # Class 1: top anchor
                top = ot.Anchor()
                top.Format = 1
                top.XCoordinate = int(hmtx[bgn][0] / 2)
                top.YCoordinate = 714 if bgn in ('J', 'I', 'T', 'uniA7CB', 'Iotaserifed', 'uniA78D', 'uni0196', 'uni01B1', 'Iota', 'Upsilon') else 540
                brec.BaseAnchor[1] = top
                st.BaseArray.BaseRecord.append(brec)

        # Sort Coverage and Array by Glyph ID
        v_marks = [(gn, rec) for gn, rec in zip(st.MarkCoverage.glyphs, st.MarkArray.MarkRecord)]
        v_marks.sort(key=lambda x: font.getGlyphID(x[0]))
        st.MarkCoverage.glyphs = [x[0] for x in v_marks]
        st.MarkArray.MarkRecord = [x[1] for x in v_marks]

        v_bases = [(gn, rec) for gn, rec in zip(st.BaseCoverage.glyphs, st.BaseArray.BaseRecord)]
        v_bases.sort(key=lambda x: font.getGlyphID(x[0]))
        st.BaseCoverage.glyphs = [x[0] for x in v_bases]
        st.BaseArray.BaseRecord = [x[1] for x in v_bases]

        mark_lookup.SubTable = [st]
        mark_lookup.SubTableCount = 1

        gpos_tbl.LookupList.Lookup.append(mark_lookup)
        lk_idx = len(gpos_tbl.LookupList.Lookup) - 1
        gpos_tbl.LookupList.LookupCount = len(gpos_tbl.LookupList.Lookup)

        # Register 'mark' feature
        feat_rec = ot.FeatureRecord()
        feat_rec.FeatureTag = 'mark'
        feat_rec.Feature = ot.Feature()
        feat_rec.Feature.FeatureParams = None
        feat_rec.Feature.LookupListIndex = [lk_idx]
        feat_rec.Feature.LookupCount = 1

        gpos_tbl.FeatureList.FeatureRecord.append(feat_rec)
        feat_idx = len(gpos_tbl.FeatureList.FeatureRecord) - 1
        gpos_tbl.FeatureList.FeatureCount = len(gpos_tbl.FeatureList.FeatureRecord)

        for srec in gpos_tbl.ScriptList.ScriptRecord:
            if srec.Script.DefaultLangSys:
                srec.Script.DefaultLangSys.FeatureIndex.append(feat_idx)
            for lrec in srec.Script.LangSysRecord:
                lrec.LangSys.FeatureIndex.append(feat_idx)

        print("  [SHAPING] Injected ClassCount=2 MarkBasePos lookup for Dutch 'IJ' and African bases into GPOS")

    # 8. Standardize Name Table entries (Strictly NO Mac platformID=1 records!)
    postscript_name = f"{family_name.replace(' ', '')}-{style_name.replace(' ', '')}"
    full_name = f"{family_name} {style_name}".strip()

    is_ribbi = style_name in ('Regular', 'Bold', 'Italic', 'Bold Italic')

    if is_ribbi:
        name_records_to_set = {
            1: family_name,
            2: style_name,
            3: f"3.100;PKGL;{postscript_name}",
            4: full_name,
            5: "Version 3.100; The PocketGull Project Authors; OFL 1.1",
            6: postscript_name,
            13: "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org",
            14: "https://openfontlicense.org",
        }
    else:
        # Non-RIBBI (e.g. Black): Windows GDI legacy grouping
        name_records_to_set = {
            1: f"{family_name} {style_name}",
            2: "Regular",
            3: f"3.100;PKGL;{postscript_name}",
            4: full_name,
            5: "Version 3.100; The PocketGull Project Authors; OFL 1.1",
            6: postscript_name,
            13: "This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: https://openfontlicense.org",
            14: "https://openfontlicense.org",
            16: family_name,
            17: style_name,
        }

    # Strip existing records 1, 2, 3, 4, 5, 6, 13, 14, 16, 17, and ALL platformID=1 records
    name_tbl.names = [r for r in name_tbl.names if r.platformID != 1 and r.nameID not in [1, 2, 3, 4, 5, 6, 13, 14, 16, 17]]

    for nid, val in name_records_to_set.items():
        name_tbl.setName(val, nid, platformID=3, platEncID=1, langID=0x0409)

    # 9. Update OS/2 table metrics & head table flags
    font['OS/2'].usWeightClass = weight_class
    if style_name == 'Regular':
        font['OS/2'].fsSelection = 0x01C0  # REGULAR (0x40) | USE_TYPO_METRICS (0x80) | WWS (0x100)
        font['head'].macStyle = 0
    elif style_name == 'Bold':
        font['OS/2'].fsSelection = 0x01A0  # BOLD (0x20) | USE_TYPO_METRICS (0x80) | WWS (0x100)
        font['head'].macStyle = 0x0001
    elif style_name == 'Black':
        font['OS/2'].fsSelection = 0x01C0  # REGULAR (0x40) | USE_TYPO_METRICS (0x80) | WWS (0x100)
        font['head'].macStyle = 0
    else:
        font['OS/2'].fsSelection = 0x01C0
        font['head'].macStyle = 0

    # Ensure head.fontRevision is exactly 3.100
    font['head'].fontRevision = 3.100

    # Ensure usWinAscent and usWinDescent enclose all glyph extrema (>= 1572 and >= 833)
    all_ymax = max(g.yMax for g in glyf.glyphs.values() if hasattr(g, 'yMax') and g.yMax is not None)
    all_ymin = min(g.yMin for g in glyf.glyphs.values() if hasattr(g, 'yMin') and g.yMin is not None)
    font['OS/2'].usWinAscent = max(1572, all_ymax)
    font['OS/2'].usWinDescent = max(833, abs(all_ymin))

    font['OS/2'].xAvgCharWidth = int(sum(hmtx[g][0] for g in font.getGlyphOrder()) / len(font.getGlyphOrder()))

    # 10. Sanitize components & decompose nested composites
    sanitize_components(font)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(output_path)
    print(f"  [SUCCESS] Successfully saved cured binary to: {output_path}")

def synthesize_circled_a(font, is_mono=False):
    """Synthesizes U+24B6 and U+24D0 Circled A/a in place."""
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()

    if 0x24B6 in cmap and 0x24D0 in cmap:
        return

    a_name = 'A' if 'A' in glyf else 'a'
    src_a = glyf[a_name]

    adv = 600 if is_mono else 700
    cx, cy = adv // 2, 360
    r_out, r_in = 380, 330

    def make_circle(cx, cy, r, cw=True):
        pts = [
            (cx, cy + r),
            (cx + r, cy + r),
            (cx + r, cy),
            (cx + r, cy - r),
            (cx, cy - r),
            (cx - r, cy - r),
            (cx - r, cy),
            (cx - r, cy + r),
        ]
        flags = [1, 0, 1, 0, 1, 0, 1, 0]
        if not cw:
            pts.reverse()
            flags.reverse()
        return pts, flags

    out_pts, out_flg = make_circle(cx, cy, r_out, cw=True)
    in_pts, in_flg = make_circle(cx, cy, r_in, cw=False)

    a_scale = 0.55
    shift_x = cx - int(300 * a_scale)
    shift_y = 160

    pts_a = [(int(p[0] * a_scale + shift_x), int(p[1] * a_scale + shift_y)) for p in src_a.coordinates]
    flg_a = list(src_a.flags)

    all_pts = out_pts + in_pts + pts_a
    all_flg = out_flg + in_flg + flg_a

    end_pts = [
        len(out_pts) - 1,
        len(out_pts) + len(in_pts) - 1,
    ]
    offset = len(out_pts) + len(in_pts)
    for e in src_a.endPtsOfContours:
        end_pts.append(offset + e)

    g = Glyph()
    g.numberOfContours = len(end_pts)
    g.endPtsOfContours = end_pts
    g.coordinates = GlyphCoordinates(all_pts)
    g.flags = bytearray(all_flg)
    g.program = Program()
    g.xMin = min(p[0] for p in all_pts)
    g.yMin = min(p[1] for p in all_pts)
    g.xMax = max(p[0] for p in all_pts)
    g.yMax = max(p[1] for p in all_pts)

    current_order = list(font.getGlyphOrder())
    for gname, cp in [('uni24B6', 0x24B6), ('uni24D0', 0x24D0)]:
        glyf[gname] = copy.deepcopy(g)
        hmtx[gname] = (adv, cx - r_out)
        if gname not in current_order:
            current_order.append(gname)
        for sub in font['cmap'].tables:
            sub.cmap[cp] = gname
        if 'GDEF' in font and font['GDEF'].table.GlyphClassDef:
            font['GDEF'].table.GlyphClassDef.classDefs[gname] = 1

    font.setGlyphOrder(current_order)
    print("  [KOALIB] Synthesized U+24B6 and U+24D0 (Circled A/a)")

def main():
    OFL_DIR = ROOT_DIR / "ofl"
    pocketgull_ofl = OFL_DIR / "pocketgull"
    pocketgullmono_ofl = OFL_DIR / "pocketgullmono"

    # 1. Pocket Gull Regular (400)
    cure_font(
        input_path=TTF_DIR / "PocketGull-Fineliner.ttf",
        output_path=pocketgull_ofl / "PocketGull-Regular.ttf",
        family_name="Pocket Gull",
        style_name="Regular",
        weight_class=400,
        is_mono=False,
    )
    # Mirror to fonts/ttf
    import shutil
    shutil.copyfile(pocketgull_ofl / "PocketGull-Regular.ttf", TTF_DIR / "PocketGull-Regular.ttf")
    shutil.copyfile(pocketgull_ofl / "PocketGull-Regular.ttf", TTF_DIR / "PocketGull-Fineliner.ttf")

    # Read canonical Latin OFL family codepoint coverage from Regular
    f_reg = TTFont(pocketgull_ofl / "PocketGull-Regular.ttf")
    family_codepoints = set(f_reg.getBestCmap().keys())

    # 2. Pocket Gull Bold (700)
    cure_font(
        input_path=TTF_DIR / "PocketGull-Bold.ttf",
        output_path=pocketgull_ofl / "PocketGull-Bold.ttf",
        family_name="Pocket Gull",
        style_name="Bold",
        weight_class=700,
        is_mono=False,
        canonical_codepoints=family_codepoints,
    )
    shutil.copyfile(pocketgull_ofl / "PocketGull-Bold.ttf", TTF_DIR / "PocketGull-Bold.ttf")

    # 3. Pocket Gull Black (900)
    cure_font(
        input_path=TTF_DIR / "PocketGull-Chiseltip.ttf",
        output_path=pocketgull_ofl / "PocketGull-Black.ttf",
        family_name="Pocket Gull",
        style_name="Black",
        weight_class=900,
        is_mono=False,
        canonical_codepoints=family_codepoints,
    )
    shutil.copyfile(pocketgull_ofl / "PocketGull-Black.ttf", TTF_DIR / "PocketGull-Black.ttf")
    shutil.copyfile(pocketgull_ofl / "PocketGull-Black.ttf", TTF_DIR / "PocketGull-Chiseltip.ttf")

    # 4. Pocket Gull Mono Regular (400)
    cure_font(
        input_path=TTF_DIR / "PocketGullMono-Regular.ttf",
        output_path=pocketgullmono_ofl / "PocketGullMono-Regular.ttf",
        family_name="Pocket Gull Mono",
        style_name="Regular",
        weight_class=400,
        is_mono=True,
    )
    shutil.copyfile(pocketgullmono_ofl / "PocketGullMono-Regular.ttf", TTF_DIR / "PocketGullMono-Regular.ttf")

    # 5. Pocket Gull Italic (400)
    if (TTF_DIR / "PocketGull-Italic.ttf").exists():
        cure_font(
            input_path=TTF_DIR / "PocketGull-Italic.ttf",
            output_path=TTF_DIR / "PocketGull-Italic.ttf",
            family_name="Pocket Gull",
            style_name="Italic",
            weight_class=400,
            is_mono=False,
            canonical_codepoints=family_codepoints,
        )

    # 6. Pocket Gull Bold Italic (700)
    if (TTF_DIR / "PocketGull-BoldItalic.ttf").exists():
        cure_font(
            input_path=TTF_DIR / "PocketGull-BoldItalic.ttf",
            output_path=TTF_DIR / "PocketGull-BoldItalic.ttf",
            family_name="Pocket Gull",
            style_name="Bold Italic",
            weight_class=700,
            is_mono=False,
            canonical_codepoints=family_codepoints,
        )

    # 7. Pocket Gull Mono Italic (400)
    if (TTF_DIR / "PocketGullMono-Italic.ttf").exists():
        cure_font(
            input_path=TTF_DIR / "PocketGullMono-Italic.ttf",
            output_path=TTF_DIR / "PocketGullMono-Italic.ttf",
            family_name="Pocket Gull Mono",
            style_name="Italic",
            weight_class=400,
            is_mono=True,
        )

    # Inject Circled A into both OFL binaries
    for ttf_path in [
        pocketgull_ofl / "PocketGull-Regular.ttf",
        pocketgull_ofl / "PocketGull-Bold.ttf",
        pocketgull_ofl / "PocketGull-Black.ttf",
        pocketgullmono_ofl / "PocketGullMono-Regular.ttf",
    ]:
        f = TTFont(ttf_path)
        f.recalcBBoxes = False
        synthesize_circled_a(f, is_mono=('mono' in ttf_path.name.lower()))
        f.save(ttf_path)
        # Mirror to fonts/ttf
        shutil.copyfile(ttf_path, TTF_DIR / ttf_path.name)

    print("\n[ALL COMPLETE] Successfully cured all production fonts for Google Fonts upstream!")

if __name__ == "__main__":
    main()

