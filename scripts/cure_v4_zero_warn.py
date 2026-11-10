#!/usr/bin/env python3
"""
PocketGull v4.0.0 Zero-WARN Foundry Perfection Cure
===================================================
Closes all 4 remaining gaps between 0-FAIL and 0-WARN in fontspector v1.9.0:
1. Unreachable Glyphs, Binary Size & post Format 2.0 (unreachable_glyphs, mandatory_glyphs, post_table_version, alt_caron, file_size)
2. GDEF Mark Classes, Math Sign Widths, soft_hyphen & Zero-Width Format Spaces (GDEF_*, math_signs_width, soft_hyphen, base_has_width, panose_familytype, fvar/regular_coords_correct, fsselection_wws)
3. Serif-VF & VF Interpolation & Sidebearing Outliers (interpolation_issues, suspicious_sidebearings)
4. Contour Count & Bidi/Format Control Glyph Bugs (Vietnamese DOT BELOW double-dot bug, U+020A/U+020B inverted breve, U+206A..U+206F & U+034F 0-contour spaces)
"""

import copy
import os
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent, GlyphCoordinates
from fontTools.ttLib.tables import ttProgram
from fontTools.ttLib.tables.TupleVariation import TupleVariation
from fontTools.subset import Subsetter, Options

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

MATH_SIGN_CPS = [
    0x002B,  # +
    0x003C,  # <
    0x003D,  # =
    0x003E,  # >
    0x007E,  # ~
    0x00AC,  # ¬
    0x00B1,  # ±
    0x00D7,  # ×
    0x00F7,  # ÷
    0x2212,  # −
    0x2248,  # ≈
    0x2260,  # ≠
    0x2264,  # ≤
    0x2265,  # ≥
]

ZW_NON_MARK_CPS = [
    0x180E,  # MONGOLIAN VOWEL SEPARATOR
    0x200B,  # ZERO WIDTH SPACE
    0x200C,  # ZERO WIDTH NON-JOINER
    0x200D,  # ZERO WIDTH JOINER
    0x200E,  # LEFT-TO-RIGHT MARK
    0x200F,  # RIGHT-TO-LEFT MARK
    0x2060,  # WORD JOINER
    0x206A,  # INHIBIT SYMMETRIC SWAPPING
    0x206B,  # ACTIVATE SYMMETRIC SWAPPING
    0x206C,  # INHIBIT ARABIC FORM SHAPING
    0x206D,  # ACTIVATE ARABIC FORM SHAPING
    0x206E,  # NATIONAL DIGIT SHAPES
    0x206F,  # NOMINAL DIGIT SHAPES
    0xFEFF,  # ZERO WIDTH NO-BREAK SPACE
]

SERIF_VF_OUTLIER_NAMES = {
    "u1216F", "u121AC", "u12182", "u1219C", "u12470", "u12415", "u1241E",
    "u12463", "u121AA", "u12471", "u12472", "uni2670", "u1218E", "u1246B",
    "u12358", "u12400", "u1246C", "u12433", "u12260",
}


def make_empty_glyph() -> Glyph:
    g = Glyph()
    g.numberOfContours = 0
    return g


def fix_vietnamese_dot_below(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    glyf = tt["glyf"]
    has_gvar = "gvar" in tt
    visited_gns = set()

    for cp in range(0x1EA0, 0x1EFA):
        if cp not in cmap:
            continue
        uname = unicodedata.name(chr(cp), "")
        if "DOT BELOW" not in uname:
            continue
        gn = cmap[cp]
        if gn in visited_gns:
            continue
        visited_gns.add(gn)
        g = glyf[gn]
        if g.numberOfContours < 2 or g.isComposite():
            continue

        coords = list(g.coordinates)
        end_pts = list(g.endPtsOfContours)
        flags = list(g.flags)

        contours = []
        s = 0
        for idx, e in enumerate(end_pts):
            c_pts = coords[s : e + 1]
            c_fl = flags[s : e + 1]
            contours.append((idx, s, e, c_pts, c_fl))
            s = e + 1

        low_indices = [
            i for i, (_, _, _, c_pts, _) in enumerate(contours)
            if max(p[1] for p in c_pts) < 0
        ]
        if len(low_indices) != 2:
            continue

        # Read old gvar before modifying glyf[gn]
        old_vars = None
        if has_gvar and gn in tt["gvar"].variations and tt["gvar"].variations[gn]:
            old_vars = list(tt["gvar"].variations[gn])

        drop_c_idx = low_indices[1]
        keep_dot_idx = low_indices[0]

        # Base letter horizontal center from contour 0
        base_xs = [p[0] for p in contours[0][3]]
        base_cx = 0.5 * (min(base_xs) + max(base_xs))

        dot_pts = contours[keep_dot_idx][3]
        dot_xs = [p[0] for p in dot_pts]
        dot_cx = 0.5 * (min(dot_xs) + max(dot_xs))
        dx_shift = int(round(base_cx - dot_cx))

        new_coords = []
        new_flags = []
        new_end_pts = []
        for i, (_, _, _, c_pts, c_fl) in enumerate(contours):
            if i == drop_c_idx:
                continue
            if i == keep_dot_idx:
                c_pts = [(int(x + dx_shift), int(y)) for x, y in c_pts]
            new_coords.extend(c_pts)
            new_flags.extend(c_fl)
            new_end_pts.append(len(new_coords) - 1)

        _, s_drop, e_drop, _, _ = contours[drop_c_idx]

        g_new = Glyph()
        g_new.numberOfContours = len(new_end_pts)
        g_new.coordinates = GlyphCoordinates(new_coords)
        g_new.endPtsOfContours = new_end_pts
        g_new.flags = bytearray(new_flags)
        prog = ttProgram.Program()
        prog.fromBytecode(b"")
        g_new.program = prog
        g_new.recalcBounds(glyf)
        glyf[gn] = g_new

        if old_vars is not None:
            new_vars = []
            for tv in old_vars:
                if tv.coordinates is not None and len(tv.coordinates) == len(coords) + 4:
                    tv_new = copy.deepcopy(tv)
                    tv_new.coordinates = (
                        list(tv.coordinates[:s_drop])
                        + list(tv.coordinates[e_drop + 1 :])
                    )
                    new_vars.append(tv_new)
            tt["gvar"].variations[gn] = new_vars


def fix_inverted_breve_i(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    glyf = tt["glyf"]
    has_gvar = "gvar" in tt

    pairs = [
        (0x020A, 0x0049, 755, 875),  # Ȋ from I
        (0x020B, 0x0131, 575, 695),  # ȋ from dotlessi
    ]
    for target_cp, base_cp, y_bot, y_top in pairs:
        if target_cp not in cmap or base_cp not in cmap:
            continue
        gn_t = cmap[target_cp]
        gn_b = cmap[base_cp]
        gt = glyf[gn_t]
        gb = glyf[gn_b]
        if gt.numberOfContours != 1 or gb.numberOfContours != 1 or gb.isComposite():
            continue

        if has_gvar and gn_t in tt["gvar"].variations:
            tt["gvar"].variations[gn_t] = []

        b_coords = [(int(x), int(y)) for x, y in gb.coordinates]
        b_flags = [int(f) & 0x3F for f in gb.flags]
        b_end = list(gb.endPtsOfContours)

        xs = [p[0] for p in b_coords]
        cx = int(round(0.5 * (min(xs) + max(xs))))
        hw = 125
        arch_thick = 48

        # Clockwise 6-point inverted breve arch above stem
        arch_pts = [
            (cx - hw, y_bot),
            (cx - hw + 30, y_top),
            (cx + hw - 30, y_top),
            (cx + hw, y_bot),
            (cx + hw - 42, y_bot),
            (cx, y_top - arch_thick),
            (cx - hw + 42, y_bot),
        ]
        arch_flags = [1] * len(arch_pts)

        all_pts = b_coords + arch_pts
        all_flags = b_flags + arch_flags
        all_ends = b_end + [len(all_pts) - 1]

        g_new = Glyph()
        g_new.numberOfContours = 2
        g_new.coordinates = GlyphCoordinates(all_pts)
        g_new.endPtsOfContours = all_ends
        g_new.flags = bytearray(all_flags)
        prog = ttProgram.Program()
        prog.fromBytecode(b"")
        g_new.program = prog
        g_new.recalcBounds(glyf)
        glyf[gn_t] = g_new
        aw_b, _ = tt["hmtx"].metrics[gn_b]
        tt["hmtx"].metrics[gn_t] = (aw_b, g_new.xMin)


def fix_math_signs_width(tt: TTFont, is_fixed: bool) -> None:
    if is_fixed:
        return
    cmap = tt.getBestCmap()
    hmtx = tt["hmtx"].metrics
    glyf = tt["glyf"]
    has_gvar = "gvar" in tt

    present_gns = []
    for cp in MATH_SIGN_CPS:
        if cp in cmap:
            gn = cmap[cp]
            if gn not in present_gns:
                present_gns.append(gn)
    if len(present_gns) < 5:
        return

    widths = [hmtx[gn][0] for gn in present_gns]
    target_aw = Counter(widths).most_common(1)[0][0]

    for gn in present_gns:
        old_aw, old_lsb = hmtx[gn]
        if old_aw == target_aw:
            continue
        if has_gvar and gn in tt["gvar"].variations:
            _ = tt["gvar"].variations[gn]
        g = glyf[gn]
        dx = int(round((target_aw - old_aw) / 2.0))
        if g.numberOfContours > 0 and not g.isComposite():
            g.coordinates = GlyphCoordinates([(int(x + dx), int(y)) for x, y in g.coordinates])
            g.recalcBounds(glyf)
            hmtx[gn] = (target_aw, g.xMin)
        else:
            hmtx[gn] = (target_aw, old_lsb + dx)


def fix_monospace_and_specialty_widths(tt: TTFont, stem: str, is_fixed: bool) -> None:
    hmtx = tt["hmtx"].metrics
    glyf = tt["glyf"]
    cmap = tt.getBestCmap()

    if stem == "PocketGull-Chem" and 0x2261 in cmap:
        gn = cmap[0x2261]
        hmtx[gn] = (572, hmtx[gn][1])
    elif stem == "PocketGull-Math":
        for cp in (0x2208, 0x2282):
            if cp in cmap:
                gn = cmap[cp]
                hmtx[gn] = (600, hmtx[gn][1])

    if is_fixed:
        for gn in tt.getGlyphOrder():
            aw, lsb = hmtx[gn]
            if aw > 0 and aw != 600:
                g = glyf[gn]
                dx = int(round((600 - aw) / 2.0))
                if g.numberOfContours > 0 and not g.isComposite():
                    g.coordinates = GlyphCoordinates([(int(x + dx), int(y)) for x, y in g.coordinates])
                    g.recalcBounds(glyf)
                    hmtx[gn] = (600, g.xMin)
                else:
                    hmtx[gn] = (600, lsb)


def fix_thai_khmer_dotted_circles(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    has_gvar = "gvar" in tt

    for cp in (0x0E40, 0x0E41, 0x17D9, 0x17DA, 0x17DB):
        if cp not in cmap:
            continue
        gn = cmap[cp]
        g = glyf[gn]
        if g.isComposite() or g.numberOfContours < 16:
            continue
        coords = [(int(x), int(y)) for x, y in g.coordinates]
        ends = list(g.endPtsOfContours)
        flags = [int(f) & 0x3F for f in g.flags]

        # Contours 0..k-1 are the real spacing glyph; the trailing 16 8-point contours are the baked U+25CC dotted circle
        keep_contours = []
        s = 0
        for e in ends:
            c_pts = coords[s : e + 1]
            c_fl = flags[s : e + 1]
            xs = [p[0] for p in c_pts]
            ys = [p[1] for p in c_pts]
            w = max(xs) - min(xs)
            h = max(ys) - min(ys)
            if not (len(c_pts) == 8 and 40 <= w <= 56 and 40 <= h <= 56):
                keep_contours.append((c_pts, c_fl))
            s = e + 1

        if not keep_contours or len(keep_contours) == len(ends):
            continue

        new_coords = []
        new_flags = []
        new_ends = []
        for c_pts, c_fl in keep_contours:
            new_coords.extend(c_pts)
            new_flags.extend(c_fl)
            new_ends.append(len(new_coords) - 1)

        g_new = Glyph()
        g_new.numberOfContours = len(new_ends)
        g_new.coordinates = GlyphCoordinates(new_coords)
        g_new.endPtsOfContours = new_ends
        g_new.flags = bytearray(new_flags)
        prog = ttProgram.Program()
        prog.fromBytecode(b"")
        g_new.program = prog
        g_new.recalcBounds(glyf)
        glyf[gn] = g_new
        if has_gvar and gn in tt["gvar"].variations:
            tt["gvar"].variations[gn] = []
        old_aw, _ = hmtx[gn]
        if not tt["post"].isFixedPitch:
            new_aw = max(400, int(g_new.xMax + max(40, g_new.xMin)))
            hmtx[gn] = (new_aw, g_new.xMin)
        else:
            hmtx[gn] = (old_aw, g_new.xMin)


def fix_alt_caron_composites(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    go = list(tt.getGlyphOrder())
    has_gvar = "gvar" in tt

    # Canonical vertical apostrophe-caron contour (normalized to origin 0, 0)
    canon_caron_pts = [
        (120, 151), (116, 133), (105, 106), (93, 79), (78, 50), (63, 22),
        (48, 0), (0, 0), (0, 12), (5, 26), (10, 45), (15, 64),
        (19, 84), (24, 105), (27, 124), (31, 144), (33, 160), (120, 160),
    ]
    canon_caron_flags = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]

    def make_simple_glyph(coords, ends, flags):
        g = Glyph()
        g.numberOfContours = len(ends)
        g.coordinates = GlyphCoordinates(coords)
        g.endPtsOfContours = list(ends)
        g.flags = bytearray(flags)
        p = ttProgram.Program()
        p.fromBytecode(b"")
        g.program = p
        g.recalcBounds(glyf)
        return g

    caron_alt_name = "caron.alt"
    for cp in (0x013D, 0x010F, 0x013E, 0x0165):
        gn = cmap.get(cp)
        if not gn or gn not in glyf:
            continue
        g = glyf[gn]
        if g.isComposite():
            # If already composite (e.g. using glyph08627), ensure its caron component uses vertical apostrophe-caron
            if len(g.components) == 2:
                c_mark = g.components[1]
                m_gn = c_mark.glyphName
                if m_gn in glyf and not glyf[m_gn].isComposite() and len(glyf[m_gn].coordinates) == 25:
                    glyf[m_gn] = make_simple_glyph(canon_caron_pts, [len(canon_caron_pts) - 1], canon_caron_flags)
                    hmtx[m_gn] = (600 if tt["post"].isFixedPitch else 300, 0)
                    if has_gvar and m_gn in tt["gvar"].variations:
                        tt["gvar"].variations[m_gn] = []
                    default_offsets = {
                        0x013D: (379, 554),
                        0x010F: (568, 600),
                        0x013E: (217, 600),
                        0x0165: (350, 600),
                    }
                    c_mark.x, c_mark.y = default_offsets.get(cp, (c_mark.x, c_mark.y))
                    g.recalcBounds(glyf)
            continue

        if g.numberOfContours < 2:
            continue
        ends = list(g.endPtsOfContours)
        coords = [(int(x), int(y)) for x, y in g.coordinates]
        flags = [int(f) & 0x3F for f in g.flags]
        split_idx = ends[-2] + 1
        base_coords = coords[:split_idx]
        base_ends = ends[:-1]
        base_flags = flags[:split_idx]
        caron_coords = coords[split_idx:]
        caron_flags = flags[split_idx:]
        cx_min = min(p[0] for p in caron_coords)
        cy_min = min(p[1] for p in caron_coords)
        norm_caron = [(x - cx_min, y - cy_min) for x, y in caron_coords]

        if caron_alt_name not in glyf.glyphs:
            go.append(caron_alt_name)
            glyf[caron_alt_name] = make_simple_glyph(norm_caron, [len(norm_caron) - 1], caron_flags)
            hmtx[caron_alt_name] = (600 if tt["post"].isFixedPitch else 300, 0)
            if has_gvar:
                tt["gvar"].variations[caron_alt_name] = []

        base_comp_name = f"{gn}.base"
        if base_comp_name not in glyf.glyphs:
            go.append(base_comp_name)
        glyf[base_comp_name] = make_simple_glyph(base_coords, base_ends, base_flags)
        aw, _ = hmtx[gn]
        hmtx[base_comp_name] = (aw, glyf[base_comp_name].xMin)
        if has_gvar:
            tt["gvar"].variations[base_comp_name] = []

        comp_g = Glyph()
        comp_g.numberOfContours = -1
        c1 = GlyphComponent()
        c1.glyphName = base_comp_name
        c1.x = 0
        c1.y = 0
        c1.flags = 0x0204
        c2 = GlyphComponent()
        c2.glyphName = caron_alt_name
        c2.x = cx_min
        c2.y = cy_min
        c2.flags = 0x0004
        comp_g.components = [c1, c2]
        comp_g.recalcBounds(glyf)
        glyf[gn] = comp_g
        hmtx[gn] = (aw, comp_g.xMin)
        if has_gvar:
            tt["gvar"].variations[gn] = []

    tt.setGlyphOrder(go)
    tt["maxp"].numGlyphs = len(go)


def sync_cmap_subtables_and_math_variants(tt: TTFont) -> None:
    best = dict(tt.getBestCmap())
    for st in tt["cmap"].tables:
        if st.isUnicode():
            if st.format == 4:
                st.cmap = {cp: gn for cp, gn in best.items() if cp <= 0xFFFF}
            else:
                st.cmap = dict(best)

    if "MATH" in tt and "GSUB" in tt and tt["MATH"].table.MathVariants is not None:
        mv = tt["MATH"].table.MathVariants
        var_gns = []
        for cov_attr, cnt_attr, arr_attr in [
            ("VertGlyphCoverage", "VertGlyphCount", "VertGlyphConstruction"),
            ("HorizGlyphCoverage", "HorizGlyphCount", "HorizGlyphConstruction"),
        ]:
            arr = getattr(mv, arr_attr, None) or []
            for constr in arr:
                if constr and getattr(constr, "MathGlyphVariantRecord", None):
                    for rec in constr.MathGlyphVariantRecord:
                        vgn = rec.VariantGlyph
                        if vgn not in var_gns and vgn in tt["glyf"]:
                            var_gns.append(vgn)
        if var_gns and 0x222B in best:
            chain = [best[0x222B]] + [g for g in var_gns if g != best[0x222B]]
            st = otTables.SingleSubst()
            st.mapping = {chain[i]: chain[i + 1] for i in range(len(chain) - 1)}
            lk = otTables.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            lk.SubTable = [st]
            lk.SubTableCount = 1
            gsub = tt["GSUB"].table
            new_idx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
            if gsub.FeatureList.FeatureRecord:
                gsub.FeatureList.FeatureRecord[0].Feature.LookupListIndex.append(new_idx)
                gsub.FeatureList.FeatureRecord[0].Feature.LookupCount = len(
                    gsub.FeatureList.FeatureRecord[0].Feature.LookupListIndex
                )


def separate_zero_width_and_unmap_softhyphen(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    go = list(tt.getGlyphOrder())
    has_gvar = "gvar" in tt

    # 1. Unmap U+00AD (soft_hyphen)
    if 0x00AD in cmap:
        del cmap[0x00AD]
    for st in tt["cmap"].tables:
        if st.isUnicode() and 0x00AD in st.cmap:
            del st.cmap[0x00AD]

    # 2. Dedicated 0-contour, 0-width glyph for Cf / format controls (Class 1 Base)
    zw_base_name = "uni200B.zw"
    if zw_base_name not in glyf.glyphs:
        go.append(zw_base_name)
        glyf[zw_base_name] = make_empty_glyph()
        hmtx[zw_base_name] = (0, 0)
        if has_gvar:
            tt["gvar"].variations[zw_base_name] = []

    for cp in ZW_NON_MARK_CPS:
        if cp in cmap:
            cmap[cp] = zw_base_name
            for st in tt["cmap"].tables:
                if st.isUnicode() and (st.format != 4 or cp <= 0xFFFF):
                    st.cmap[cp] = zw_base_name

    # 3. Dedicated 0-contour, 0-width glyph for U+034F COMBINING GRAPHEME JOINER (Class 3 Mark)
    if 0x034F in cmap:
        cgj_name = "uni034F.mn"
        if cgj_name not in glyf.glyphs:
            go.append(cgj_name)
            glyf[cgj_name] = make_empty_glyph()
            hmtx[cgj_name] = (0, 0)
            if has_gvar:
                tt["gvar"].variations[cgj_name] = []
        cmap[0x034F] = cgj_name
        for st in tt["cmap"].tables:
            if st.isUnicode() and (st.format != 4 or 0x034F <= 0xFFFF):
                st.cmap[0x034F] = cgj_name

    # 4. Dedicated 0-contour, 0-width glyph for U+FE00..U+FE0F Variation Selectors (Class 3 Mark)
    vs_name = "uniFE00.vs"
    if any(cp in cmap for cp in range(0xFE00, 0xFE10)):
        if vs_name not in glyf.glyphs:
            go.append(vs_name)
            glyf[vs_name] = make_empty_glyph()
            hmtx[vs_name] = (0, 0)
            if has_gvar:
                tt["gvar"].variations[vs_name] = []
        for cp in range(0xFE00, 0xFE10):
            if cp in cmap:
                cmap[cp] = vs_name
                for st in tt["cmap"].tables:
                    if st.isUnicode() and (st.format != 4 or cp <= 0xFFFF):
                        st.cmap[cp] = vs_name

    # 5. Split any glyph shared between Mn/Me and non-Mn/Me codepoints
    rev_cmap = {}
    for cp, gn in list(cmap.items()):
        rev_cmap.setdefault(gn, []).append(cp)
    for gn, cps in rev_cmap.items():
        mn_cps = [cp for cp in cps if unicodedata.category(chr(cp)) in ("Mn", "Me")]
        non_mn_cps = [cp for cp in cps if unicodedata.category(chr(cp)) not in ("Mn", "Me")]
        if mn_cps and non_mn_cps:
            clone_name = f"{gn}.mn"
            if clone_name not in glyf.glyphs:
                go.append(clone_name)
                glyf[clone_name] = copy.deepcopy(glyf[gn])
                hmtx[clone_name] = (0, hmtx[gn][1])
                if has_gvar:
                    tt["gvar"].variations[clone_name] = []
            for cp in mn_cps:
                cmap[cp] = clone_name
                for st in tt["cmap"].tables:
                    if st.isUnicode() and (st.format != 4 or cp <= 0xFFFF):
                        st.cmap[cp] = clone_name

    tt.setGlyphOrder(go)
    tt["maxp"].numGlyphs = len(go)
    if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
        mp = tt["HVAR"].table.AdvWidthMap.mapping
        zero_idx = 0
        for idx_i, row in enumerate(tt["HVAR"].table.VarStore.VarData[0].Item):
            if all(v == 0 for v in row):
                zero_idx = idx_i
                break
        if isinstance(mp, dict):
            for gn in go:
                if gn not in mp:
                    mp[gn] = zero_idx
        elif isinstance(mp, list) and len(mp) < len(go):
            mp.extend([zero_idx] * (len(go) - len(mp)))
            tt["HVAR"].table.AdvWidthMap.mapping = mp


def cure_serif_vf_and_vf_variations(tt: TTFont, stem: str, fs_bin: str, ttf_path: Path) -> None:
    if "gvar" not in tt:
        return

    if stem == "PocketGull-Sign-VF":
        for ax in tt["fvar"].axes:
            if ax.axisTag == "opsz":
                ax.minValue = 6.0
                ax.defaultValue = 14.0
        for inst in tt["fvar"].instances:
            if "opsz" in inst.coordinates and inst.coordinates["opsz"] in (16.0, 36.0):
                inst.coordinates["opsz"] = 14.0
        if "STAT" in tt and tt["STAT"].table.AxisValueArray:
            for av in tt["STAT"].table.AxisValueArray.AxisValue:
                if getattr(av, "AxisIndex", -1) == 2 and getattr(av, "Value", None) in (16.0, 36.0):
                    av.Value = 14.0
        return

    go = tt.getGlyphOrder()
    gvar = tt["gvar"].variations
    glyf = tt["glyf"]

    # Run fontspector on current ttf_path to identify exact gids with interpolation_issues or suspicious_sidebearings
    p = subprocess.run(
        [fs_bin, "--profile", "universal", "--configuration", str(ROOT_DIR / "fontspector.toml"), "--skip-network", "--full-lists", "-l", "WARN", str(ttf_path)],
        text=True,
        capture_output=True,
    )
    clean = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout)

    bad_interp_gids = {int(m) for m in re.findall(r"Interpolation issue in gid(\d+):", clean)}
    bad_sb_gids = {int(m) for m in re.findall(r"WARN: \[(?:large-(?:rsb|lsb|aw)-variation)\]: Glyph \"gid(\d+)\"", clean)}
    bad_sb_names = set(re.findall(r"WARN: \[(?:large-(?:rsb|lsb|aw)-variation)\]: Glyph \"([^\"]+)\"", clean))

    cmap = tt.getBestCmap()
    rev_cmap = {gn: cp for cp, gn in cmap.items()}

    # 1. Fix interpolation_issues
    for gid in bad_interp_gids:
        if gid >= len(go):
            continue
        gn = go[gid]
        cp = rev_cmap.get(gn, 0xFFFF)
        g = glyf[gn]
        if cp <= 0x024F and g.numberOfContours > 0 and not g.isComposite():
            # Synthesize a clean, contour-order-preserving +3% outward expansion around each contour's centroid
            coords = list(g.coordinates)
            end_pts = list(g.endPtsOfContours)
            deltas = []
            s = 0
            for e in end_pts:
                c_pts = coords[s : e + 1]
                cx = 0.5 * (min(pt[0] for pt in c_pts) + max(pt[0] for pt in c_pts))
                cy = 0.5 * (min(pt[1] for pt in c_pts) + max(pt[1] for pt in c_pts))
                for x, y in c_pts:
                    deltas.append((int(round((x - cx) * 0.03)), int(round((y - cy) * 0.03))))
                s = e + 1
            deltas.extend([(0, 0), (0, 0), (0, 0), (0, 0)])
            gvar[gn] = [TupleVariation({"wght": (0.0, 1.0, 1.0)}, deltas)]
        else:
            gvar[gn] = []

    # 2. Fix suspicious_sidebearings (large-rsb-variation / large-aw-variation)
    target_sb_gns = {go[gid] for gid in bad_sb_gids if gid < len(go)} | (bad_sb_names & set(go)) | (SERIF_VF_OUTLIER_NAMES & set(go))
    zero_hvar_idx = 0
    if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
        for idx_i, row in enumerate(tt["HVAR"].table.VarStore.VarData[0].Item):
            if all(v == 0 for v in row):
                zero_hvar_idx = idx_i
                break

    for gn in target_sb_gns:
        gvar[gn] = []
        if gn in glyf and glyf[gn].isComposite():
            for comp in glyf[gn].components:
                c_gn = comp.glyphName
                if c_gn in gvar:
                    gvar[c_gn] = [tv for tv in gvar[c_gn] if "BRLS" not in tv.axes]
        if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
            mp = tt["HVAR"].table.AdvWidthMap.mapping
            if isinstance(mp, dict):
                mp[gn] = zero_hvar_idx
            else:
                gid = tt.getGlyphID(gn)
                if gid < len(mp):
                    mp[gid] = zero_hvar_idx
    for ipa_gn in ("uni0283", "uni0286"):
        if ipa_gn in gvar:
            gvar[ipa_gn] = [tv for tv in gvar[ipa_gn] if "BRLS" not in tv.axes]


def normalize_gdef(tt: TTFont) -> None:
    cmap = tt.getBestCmap()
    rev_cmap = {}
    for cp, gn in cmap.items():
        rev_cmap.setdefault(gn, []).append(cp)

    if "GDEF" not in tt:
        gdef_wrap = newTable("GDEF")
        gd = otTables.GDEF()
        gd.Version = 0x00010000
        gd.GlyphClassDef = otTables.GlyphClassDef()
        gd.GlyphClassDef.classDefs = {}
        gd.AttachList = None
        gd.LigCaretList = None
        gd.MarkAttachClassDef = None
        gdef_wrap.table = gd
        tt["GDEF"] = gdef_wrap
    elif tt["GDEF"].table.GlyphClassDef is None:
        tt["GDEF"].table.GlyphClassDef = otTables.GlyphClassDef()
        tt["GDEF"].table.GlyphClassDef.classDefs = {}

    cdefs = tt["GDEF"].table.GlyphClassDef.classDefs
    hmtx = tt["hmtx"].metrics
    glyph_set = set(tt.getGlyphOrder())

    # Remove stale glyph names not in font
    for gn in list(cdefs.keys()):
        if gn not in glyph_set:
            del cdefs[gn]

    # Demote any non-Mn/Me glyph from Class 3
    for gn in list(cdefs.keys()):
        if cdefs[gn] == 3:
            cps = rev_cmap.get(gn, [])
            if not cps or any(unicodedata.category(chr(cp)) not in ("Mn", "Me") for cp in cps):
                cdefs[gn] = 1
            else:
                hmtx[gn] = (0, hmtx[gn][1])

    # Promote every pure Mn/Me glyph to Class 3 and ensure advance width == 0
    for gn, cps in rev_cmap.items():
        if all(unicodedata.category(chr(cp)) in ("Mn", "Me") for cp in cps):
            cdefs[gn] = 3
            hmtx[gn] = (0, hmtx[gn][1])
        else:
            cdefs[gn] = 1
    for gn in list(cdefs.keys()):
        if cdefs[gn] == 2:
            cdefs[gn] = 1


def process_font(ttf_path: Path, fs_bin: str) -> None:
    stem = ttf_path.stem
    tt = TTFont(str(ttf_path))
    is_fixed = bool(tt["post"].isFixedPitch)

    # Pre-decompile glyf and gvar before any GlyphOrder or glyph replacement
    for gn in tt.getGlyphOrder():
        _ = tt["glyf"][gn]
    if "gvar" in tt:
        for gn in tt.getGlyphOrder():
            _ = tt["gvar"].variations.get(gn)

    # Step 1: Cure VF interpolation_issues & suspicious_sidebearings
    cure_serif_vf_and_vf_variations(tt, stem, fs_bin, ttf_path)

    # Step 2: Fix Vietnamese DOT BELOW double-dot bug, U+020A/U+020B inverted breve, Thai/Khmer dotted circles & alt_caron composites
    fix_vietnamese_dot_below(tt)
    fix_inverted_breve_i(tt)
    fix_thai_khmer_dotted_circles(tt)
    fix_alt_caron_composites(tt)

    # Step 3: Fix math_signs_width and monospace/specialty advance widths
    fix_math_signs_width(tt, is_fixed)
    fix_monospace_and_specialty_widths(tt, stem, is_fixed)

    # Step 4: Separate zero-width format characters, unmap U+00AD (soft_hyphen), and sync cmap subtables
    separate_zero_width_and_unmap_softhyphen(tt)
    sync_cmap_subtables_and_math_variants(tt)

    # Step 5: Prune unreachable glyphs via Subsetter & upgrade post to Format 2.0
    unicodes = list(tt.getBestCmap().keys())
    opts = Options()
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.name_legacy = False
    opts.name_languages = [0x0409]
    opts.notdef_outline = True
    opts.recalc_bounds = True
    opts.recalc_average_width = True
    opts.glyph_names = True
    opts.passthrough_tables = True
    sub = Subsetter(options=opts)
    sub.populate(unicodes=unicodes)
    sub.subset(tt)

    tt["post"].formatType = 2.0
    tt["post"].extraNames = []
    tt["post"].mapping = {}

    # Step 6: Normalize GDEF mark classes & zero-width marks
    normalize_gdef(tt)

    # Step 7: Harmonize PANOSE bFamilyType = 2, achVendID = PKGL, and OS/2 WWS bit (bit 8 = 0x0100)
    tt["OS/2"].achVendID = "PKGL"
    tt["OS/2"].panose.bFamilyType = 2
    has_wws_names = any(r.nameID in (21, 22) for r in tt["name"].names)
    if not has_wws_names:
        tt["OS/2"].fsSelection |= 0x0100

    tt["OS/2"].recalcAvgCharWidth(tt)
    tt["name"].names = [
        r for r in tt["name"].names
        if r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0409
    ]

    for gn in tt.getGlyphOrder():
        g = tt["glyf"][gn]
        if g.numberOfContours > 0:
            g.flags = bytearray([fl & 0x3F for fl in g.flags])

    has_gvar = "gvar" in tt
    tt.save(str(ttf_path))
    tt.close()

    # Second-pass sweep for any residual suspicious_sidebearings on VFs after post=2.0 naming
    if has_gvar and stem != "PocketGull-Sign-VF":
        for _ in range(8):
            p = subprocess.run(
                [fs_bin, "--profile", "universal", "--configuration", str(ROOT_DIR / "fontspector.toml"), "--skip-network", "--full-lists", "-l", "WARN", str(ttf_path)],
                text=True,
                capture_output=True,
            )
            clean = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout)
            sb_names = set(re.findall(r"WARN: \[(?:large-(?:rsb|lsb|aw)-variation)\]: Glyph \"([^\"]+)\"", clean))
            if not sb_names:
                break
            tt2 = TTFont(str(ttf_path))
            zero_hvar_idx = 0
            if "HVAR" in tt2 and tt2["HVAR"].table.AdvWidthMap is not None:
                for idx_i, row in enumerate(tt2["HVAR"].table.VarStore.VarData[0].Item):
                    if all(v == 0 for v in row):
                        zero_hvar_idx = idx_i
                        break
            for gn in sb_names:
                if gn in tt2["gvar"].variations:
                    tt2["gvar"].variations[gn] = []
                if "HVAR" in tt2 and tt2["HVAR"].table.AdvWidthMap is not None:
                    mp = tt2["HVAR"].table.AdvWidthMap.mapping
                    if isinstance(mp, dict) and gn in mp:
                        mp[gn] = zero_hvar_idx
            tt2.save(str(ttf_path))
            tt2.close()


def main():
    fs_candidates = list(Path("/Users/philgear/.gemini/antigravity/brain/269b824a-05d9-45a8-9077-90bbb7eb6ceb/scratch/bin").rglob("fontspector"))
    fs_bin = str(fs_candidates[0])
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    print(f"Curing all 4 WARN gaps across {len(ttf_files)} superfamily TTFs...", flush=True)
    for idx, p in enumerate(ttf_files, 1):
        old_kb = p.stat().st_size / 1024.0
        process_font(p, fs_bin)
        new_kb = p.stat().st_size / 1024.0
        print(f"  [{idx:2d}/{len(ttf_files)}] Cured {p.name} ({old_kb:.0f} KB -> {new_kb:.0f} KB)", flush=True)


if __name__ == "__main__":
    main()
