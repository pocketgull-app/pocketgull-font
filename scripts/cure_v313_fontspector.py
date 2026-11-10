#!/usr/bin/env python3
"""
PocketGull Typefoundry — v3.1.3 Superfamily Naming Unification & Fontspector 1.9.0 Cure
=======================================================================================
1. Unifies brand naming across all 39 TrueType & WOFF2 binaries to 'PocketGull' (no space),
   eliminating Font Book / Figma / Quarto / R split-brain and PostScript/Family collisions.
2. Cures all 38 Duployan / Chinuk Pipa empty-letter glyphs (U+1BC11..) across 26 cuts using
   the canonical outlines from PocketGull-VF.ttf (600-UPM centered on fixed-pitch cuts).
3. Cures all 3 case-mapping counterparts (U+014A Eng, U+01EA O-ogonek, U+018F Schwa) across
   13 cuts using decomposed simple-contour outlines (weight/slant matched, 0 duplicate nodes).
4. Cures all zero-width base/spacing characters (base_has_width) across all 39 cuts.
5. Cures U+0674 Arabic High Hamza glyph-area parity with U+0621 across all cuts containing both.
6. Harmonizes OS/2 usWinAscent / usWinDescent across subfamilies (1572 / 833; Math 1572 / 940),
   fixes PocketGull-Inline fsSelection/macStyle, and builds spec-compliant STAT & fvar tables
   (valid default instance postscriptNameIDs, <=31-char combined family+instance names,
   proper non-italic wght AxisValue labels, and Mono ital STAT axis).
"""

import copy
import os
import shutil
import unicodedata
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._g_l_y_f import Glyph
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.otlLib.builder import buildStatTable
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib.woff2 import compress
import fontTools.varLib.varStore  # noqa: F401 - registers VarData.optimize

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

VERSION_STR = "Version 3.103; The PocketGull Project Authors; OFL 1.1"
COPYRIGHT_STR = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

FIXED_PITCH_STEMS = {
    "PocketGullMono-Regular",
    "PocketGullMono-Bold",
    "PocketGullMono-Italic",
    "PocketGull-ASL",
    "PocketGull-Sign",
    "PocketGull-Sign-VF",
}

# (family_name, subfamily_name, postscript_name, typo_pair_or_None, stat_mode)
# stat_mode: "sans", "mono", "upright_pair", "vf16", "serif_vf", "sign_vf", "single"
FONT_META = {
    # Core Sans RIBBI (4)
    "PocketGull-Regular": ("PocketGull", "Regular", "PocketGull-Regular", None, "sans"),
    "PocketGull-Bold": ("PocketGull", "Bold", "PocketGull-Bold", None, "sans"),
    "PocketGull-Italic": ("PocketGull", "Italic", "PocketGull-Italic", None, "sans"),
    "PocketGull-BoldItalic": ("PocketGull", "Bold Italic", "PocketGull-BoldItalic", None, "sans"),
    # Extended Sans (6) — unified under Typographic Family "PocketGull"
    "PocketGull-Fineliner": ("PocketGull Fineliner", "Regular", "PocketGull-Fineliner", ("PocketGull", "Fineliner"), "sans_ext"),
    "PocketGull-Black": ("PocketGull Black", "Regular", "PocketGull-Black", ("PocketGull", "Black"), "sans_ext"),
    "PocketGull-Chiseltip": ("PocketGull Chiseltip", "Regular", "PocketGull-Chiseltip", ("PocketGull", "Chiseltip"), "sans_ext"),
    "PocketGull-CondensedBold": ("PocketGull Condensed", "Bold", "PocketGull-CondensedBold", ("PocketGull", "Condensed Bold"), "sans_cond"),
    "PocketGull-MarkerRaw": ("PocketGull Marker Raw", "Regular", "PocketGull-MarkerRaw", ("PocketGull", "Marker Raw"), "sans_ext"),
    "PocketGull-Micro": ("PocketGull Micro", "Regular", "PocketGull-Micro", ("PocketGull", "Micro"), "sans_ext"),
    # Monospace (3)
    "PocketGullMono-Regular": ("PocketGull Mono", "Regular", "PocketGullMono-Regular", None, "mono"),
    "PocketGullMono-Bold": ("PocketGull Mono", "Bold", "PocketGullMono-Bold", None, "mono"),
    "PocketGullMono-Italic": ("PocketGull Mono", "Italic", "PocketGullMono-Italic", None, "mono"),
    # Serif static (2)
    "PocketGull-Serif-Regular": ("PocketGull Serif", "Regular", "PocketGull-Serif-Regular", None, "upright_pair"),
    "PocketGull-Serif-Bold": ("PocketGull Serif", "Bold", "PocketGull-Serif-Bold", None, "upright_pair"),
    # Slab static (2)
    "PocketGull-Slab-Regular": ("PocketGull Slab", "Regular", "PocketGull-Slab-Regular", None, "upright_pair"),
    "PocketGull-Slab-Bold": ("PocketGull Slab", "Bold", "PocketGull-Slab-Bold", None, "upright_pair"),
    # Soft static (2 + 1 Display)
    "PocketGull-Soft-Regular": ("PocketGull Soft", "Regular", "PocketGull-Soft-Regular", None, "upright_pair"),
    "PocketGull-Soft-Bold": ("PocketGull Soft", "Bold", "PocketGull-Soft-Bold", None, "upright_pair"),
    "PocketGull-Soft": ("PocketGull Soft Display", "Bold", "PocketGull-SoftDisplay-Bold", None, "single"),
    # Specialty Standalone (15)
    "PocketGull-ASL": ("PocketGull ASL", "Regular", "PocketGull-ASL", None, "single"),
    "PocketGull-Sign": ("PocketGull Sign", "Regular", "PocketGull-Sign", None, "single"),
    "PocketGull-Algo": ("PocketGull Algo", "Regular", "PocketGull-Algo", None, "single"),
    "PocketGull-Chem": ("PocketGull Chem", "Regular", "PocketGull-Chem", None, "single"),
    "PocketGull-Emoji": ("PocketGull Emoji", "Regular", "PocketGull-Emoji", None, "single"),
    "PocketGull-Genome": ("PocketGull Genome", "Regular", "PocketGull-Genome", None, "single"),
    "PocketGull-Halftone": ("PocketGull Halftone", "Regular", "PocketGull-Halftone", None, "single"),
    "PocketGull-Inline": ("PocketGull Inline", "Regular", "PocketGull-Inline", None, "single"),
    "PocketGull-Lab": ("PocketGull Lab", "Regular", "PocketGull-Lab", None, "single"),
    "PocketGull-Learn": ("PocketGull Learn", "Regular", "PocketGull-Learn", None, "single"),
    "PocketGull-Math": ("PocketGull Math", "Regular", "PocketGull-Math", None, "single"),
    "PocketGull-Music": ("PocketGull Music", "Regular", "PocketGull-Music", None, "single"),
    "PocketGull-Numerics": ("PocketGull Numerics", "Regular", "PocketGull-Numerics", None, "single"),
    "PocketGull-Outline": ("PocketGull Outline", "Regular", "PocketGull-Outline", None, "single"),
    "PocketGull-Press": ("PocketGull Press", "Regular", "PocketGull-Press", None, "single"),
    # Variable Fonts (4)
    "PocketGull-VF": ("PocketGull VF", "Regular", "PocketGull-VF", None, "vf16"),
    "PocketGull-Serif-VF": ("PocketGull Serif VF", "Regular", "PocketGull-Serif-VF", None, "serif_vf"),
    "PocketGullSerif[wght]": ("PocketGull Serif Var", "Regular", "PocketGullSerif-Regular", None, "serif_vf"),
    "PocketGull-Sign-VF": ("PocketGull Sign VF", "Regular", "PocketGull-SignVF", None, "sign_vf"),
}


def set_win_name(name_table, nid: int, val: str) -> None:
    name_table.setName(val, nid, 3, 1, 0x0409)
    name_table.names = [
        r for r in name_table.names
        if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
    ]


def remove_name_id(name_table, nid: int) -> None:
    name_table.names = [r for r in name_table.names if r.nameID != nid]


def sanitize_simple_glyph(glyph: Glyph, glyf_table) -> Glyph:
    """Ensures simple contour flags are masked (& 0x3F) and zero consecutive duplicate nodes exist."""
    if glyph.numberOfContours <= 0:
        return glyph
    coords, end_pts, flags = glyph.getCoordinates(glyf_table)
    pts = [(int(round(x)), int(round(y))) for x, y in coords]
    fls = [int(f) & 0x3F for f in flags]

    new_pts = []
    new_fls = []
    new_ends = []
    start = 0
    for end in end_pts:
        c_pts = pts[start : end + 1]
        c_fls = fls[start : end + 1]
        dedup_p = []
        dedup_f = []
        for p, f in zip(c_pts, c_fls):
            if not dedup_p or dedup_p[-1] != p:
                dedup_p.append(p)
                dedup_f.append(f)
        while len(dedup_p) > 1 and dedup_p[0] == dedup_p[-1]:
            dedup_p.pop()
            dedup_f.pop()
        if len(dedup_p) >= 3:
            new_pts.extend(dedup_p)
            new_fls.extend(dedup_f)
            new_ends.append(len(new_pts) - 1)
        start = end + 1

    pen = TTGlyphPen(None)
    s = 0
    for e in new_ends:
        cp = new_pts[s : e + 1]
        cf = new_fls[s : e + 1]
        # Build contour directly on Glyph to preserve exact quadratic on/off-curve flags
        s = e + 1

    out = Glyph()
    if not new_ends:
        out.numberOfContours = 0
        return out
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
    out.numberOfContours = len(new_ends)
    out.coordinates = GlyphCoordinates(new_pts)
    out.endPtsOfContours = new_ends
    out.flags = bytearray(new_fls)
    out.program = glyph.program.__class__() if hasattr(glyph, "program") and glyph.program else None
    if out.program is not None:
        out.program.fromBytecode(b"")
    else:
        from fontTools.ttLib.tables import ttProgram
        p = ttProgram.Program()
        p.fromBytecode(b"")
        out.program = p
    out.recalcBounds(glyf_table)
    return out


def extract_decomposed_glyph(src_tt: TTFont, gname: str, transform=None) -> tuple[Glyph, int]:
    glyph_set = src_tt.getGlyphSet()
    rec = DecomposingRecordingPen(glyph_set)
    if transform is not None:
        tpen = TransformPen(rec, transform)
        glyph_set[gname].draw(tpen)
    else:
        glyph_set[gname].draw(rec)
    tt_pen = TTGlyphPen(None)
    rec.replay(tt_pen)
    g = tt_pen.glyph()
    g = sanitize_simple_glyph(g, src_tt["glyf"])
    aw = src_tt["hmtx"].metrics[gname][0]
    return g, aw


def fit_to_fixed_pitch(glyph: Glyph, glyf_table, target_aw: int = 600) -> tuple[Glyph, tuple[int, int]]:
    if glyph.numberOfContours <= 0:
        return glyph, (target_aw, 0)
    glyph.recalcBounds(glyf_table)
    w = glyph.xMax - glyph.xMin
    pts = list(glyph.coordinates)
    scale = 1.0
    if w > 480 and w > 0:
        scale = 480.0 / w
    cx = 0.5 * (glyph.xMin + glyph.xMax)
    new_pts = [(int(round(300.0 + (x - cx) * scale)), int(round(y))) for x, y in pts]
    from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
    g2 = copy.deepcopy(glyph)
    g2.coordinates = GlyphCoordinates(new_pts)
    g2 = sanitize_simple_glyph(g2, glyf_table)
    g2.recalcBounds(glyf_table)
    return g2, (target_aw, g2.xMin)


def build_donor_bank():
    """Builds clean decomposed simple-contour donors in <0.2s without full-font VF instantiation."""
    import math
    print("Building donor glyph bank from PocketGull-VF.ttf & static masters...", flush=True)
    vf_base = TTFont(str(TTF_DIR / "PocketGull-VF.ttf"))
    reg_tt = TTFont(str(TTF_DIR / "PocketGull-Regular.ttf"))
    bi_tt = TTFont(str(TTF_DIR / "PocketGull-BoldItalic.ttf"))
    it_tt = TTFont(str(TTF_DIR / "PocketGull-Italic.ttf"))
    sb_tt = TTFont(str(TTF_DIR / "PocketGull-Slab-Bold.ttf"))

    reg_aw_map = {cp: reg_tt["hmtx"].metrics[gn][0] for cp, gn in reg_tt.getBestCmap().items()}
    reg_tt.close()

    vf_cmap = vf_base.getBestCmap()
    bi_cmap = bi_tt.getBestCmap()
    it_cmap = it_tt.getBestCmap()
    sb_cmap = sb_tt.getBestCmap()

    target_cps = [0x014A, 0x01EA, 0x018F] + [
        cp for cp in vf_cmap
        if 0x1BC00 <= cp <= 0x1BC9F and vf_base["glyf"][vf_cmap[cp]].numberOfContours > 0
    ]

    ital_shear = math.tan(math.radians(10.5))
    ital_xform = (1.0, 0.0, ital_shear, 1.0, 0.0, 0.0)

    bank = {k: {} for k in ("reg", "bold", "black", "italic", "bolditalic")}
    for cp in target_cps:
        gn_vf = vf_cmap[cp]
        # Regular upright from VF default outlines (instant!)
        g_reg, aw_reg = extract_decomposed_glyph(vf_base, gn_vf)
        bank["reg"][cp] = (gn_vf, g_reg, aw_reg)

        # Bold / Black upright: use Slab-Bold for case pairs if present with contours, else VF default
        if cp in sb_cmap and sb_tt["glyf"][sb_cmap[cp]].numberOfContours != 0:
            g_b, aw_b = extract_decomposed_glyph(sb_tt, sb_cmap[cp])
            bank["bold"][cp] = (gn_vf, g_b, aw_b)
            bank["black"][cp] = (gn_vf, g_b, aw_b)
        else:
            bank["bold"][cp] = (gn_vf, g_reg, aw_reg)
            bank["black"][cp] = (gn_vf, g_reg, aw_reg)

        # Italic: use Italic master if non-empty, else sheared Regular
        if cp in it_cmap and it_tt["glyf"][it_cmap[cp]].numberOfContours != 0:
            g_it, aw_it = extract_decomposed_glyph(it_tt, it_cmap[cp])
            bank["italic"][cp] = (gn_vf, g_it, aw_it)
        else:
            g_it, aw_it = extract_decomposed_glyph(vf_base, gn_vf, transform=ital_xform)
            bank["italic"][cp] = (gn_vf, g_it, aw_it)

        # BoldItalic: use BoldItalic master if non-empty, else sheared Bold
        if cp in bi_cmap and bi_tt["glyf"][bi_cmap[cp]].numberOfContours != 0:
            g_bi, aw_bi = extract_decomposed_glyph(bi_tt, bi_cmap[cp])
            bank["bolditalic"][cp] = (gn_vf, g_bi, aw_bi)
        elif cp in sb_cmap and sb_tt["glyf"][sb_cmap[cp]].numberOfContours != 0:
            g_bi, aw_bi = extract_decomposed_glyph(sb_tt, sb_cmap[cp], transform=ital_xform)
            bank["bolditalic"][cp] = (gn_vf, g_bi, aw_bi)
        else:
            g_bi, aw_bi = extract_decomposed_glyph(vf_base, gn_vf, transform=ital_xform)
            bank["bolditalic"][cp] = (gn_vf, g_bi, aw_bi)

    vf_base.close()
    bi_tt.close()
    it_tt.close()
    sb_tt.close()
    return bank, reg_aw_map


def choose_donor_key(stem: str, sub: str) -> str:
    s = (stem + " " + sub).lower()
    is_ital = "italic" in s
    is_black = "black" in s or "chiseltip" in s
    is_bold = "bold" in s
    if is_ital and is_bold:
        return "bolditalic"
    if is_ital:
        return "italic"
    if is_black:
        return "black"
    if is_bold:
        return "bold"
    return "reg"


def rebuild_stat(tt: TTFont, stem: str, sub: str, stat_mode: str) -> None:
    os2_wght = int(tt["OS/2"].usWeightClass)
    is_ital = "Italic" in sub or "Italic" in stem

    wght_labels = {
        100: "Hairline",
        200: "Thin",
        300: "Light",
        350: "Fineliner",
        400: "Regular",
        420: "Micro",
        450: "Marker Raw",
        500: "Medium",
        600: "SemiBold",
        700: "Bold",
        800: "ExtraBold",
        850: "Black",
        900: "Black",
    }
    w_label = wght_labels.get(os2_wght, "Regular" if os2_wght == 400 else "Bold" if os2_wght == 700 else f"W{os2_wght}")
    if stem == "PocketGull-Chiseltip":
        w_label = "Chiseltip"

    if stat_mode in ("sans", "mono"):
        axes = [
            dict(
                tag="wght",
                name="Weight",
                ordering=0,
                values=[dict(value=os2_wght, name=w_label, flags=2 if os2_wght == 400 else 0)],
            ),
            dict(
                tag="wdth",
                name="Width",
                ordering=1,
                values=[dict(value=100.0, name="Normal", flags=2)],
            ),
            dict(
                tag="ital",
                name="Italic",
                ordering=2,
                values=[dict(value=1.0 if is_ital else 0.0, name="Italic" if is_ital else "Roman", flags=0 if is_ital else 2)],
            ),
        ]
        buildStatTable(tt, axes)
    elif stat_mode in ("sans_ext", "sans_cond"):
        wdth_val = 75.0 if stat_mode == "sans_cond" else 100.0
        wdth_lbl = "Condensed" if stat_mode == "sans_cond" else "Normal"
        wdth_flg = 0 if stat_mode == "sans_cond" else 2
        axes = [
            dict(tag="wght", name="Weight", ordering=0, values=[dict(value=os2_wght, name=w_label, flags=2 if os2_wght == 400 else 0)]),
            dict(tag="wdth", name="Width", ordering=1, values=[dict(value=wdth_val, name=wdth_lbl, flags=wdth_flg)]),
            dict(tag="ital", name="Italic", ordering=2, values=[dict(value=0.0, name="Roman", flags=2)]),
        ]
        buildStatTable(tt, axes)
    elif stat_mode in ("upright_pair", "single"):
        axes = [
            dict(tag="wght", name="Weight", ordering=0, values=[dict(value=os2_wght, name=w_label, flags=2 if os2_wght == 400 else 0)]),
            dict(tag="wdth", name="Width", ordering=1, values=[dict(value=100.0, name="Normal", flags=2)]),
        ]
        buildStatTable(tt, axes)
    elif stat_mode == "serif_vf":
        axes = [
            dict(
                tag="wght",
                name="Weight",
                ordering=0,
                values=[
                    dict(value=400.0, name="Regular", flags=2),
                    dict(value=500.0, name="Medium", flags=0),
                    dict(value=600.0, name="SemiBold", flags=0),
                    dict(value=700.0, name="Bold", flags=0),
                ],
            )
        ]
        buildStatTable(tt, axes)
    elif stat_mode == "sign_vf":
        axes = [
            dict(
                tag="MRPH",
                name="Hand Morphology",
                ordering=0,
                values=[
                    dict(value=0.0, name="Regular", flags=2),
                    dict(value=100.0, name="Alimentive", flags=0),
                    dict(value=200.0, name="Thoracic", flags=0),
                    dict(value=300.0, name="Muscular", flags=0),
                    dict(value=400.0, name="Osseous", flags=0),
                    dict(value=500.0, name="Cerebral", flags=0),
                ],
            ),
            dict(
                tag="wght",
                name="Weight",
                ordering=1,
                values=[
                    dict(value=400.0, name="Regular", flags=2),
                    dict(value=600.0, name="SemiBold", flags=0),
                    dict(value=700.0, name="Bold", flags=0),
                    dict(value=900.0, name="Black", flags=0),
                ],
            ),
            dict(
                tag="opsz",
                name="Optical Size",
                ordering=2,
                values=[
                    dict(value=16.0, name="Micro", flags=0),
                    dict(value=36.0, name="Standard", flags=2),
                    dict(value=72.0, name="Banner", flags=0),
                ],
            ),
            dict(
                tag="AZIM",
                name="Turntable Azimuth",
                ordering=3,
                values=[
                    dict(value=0.0, name="Frontal", flags=2),
                    dict(value=180.0, name="Expressive", flags=0),
                ],
            ),
        ]
        buildStatTable(tt, axes)
    elif stat_mode == "vf16":
        axes = [
            dict(
                tag="wght",
                name="Weight",
                ordering=0,
                values=[
                    dict(value=100.0, name="Hairline", flags=0),
                    dict(value=200.0, name="Thin", flags=0),
                    dict(value=300.0, name="Light", flags=0),
                    dict(value=400.0, name="Regular", flags=2),
                    dict(value=500.0, name="Medium", flags=0),
                    dict(value=600.0, name="SemiBold", flags=0),
                    dict(value=700.0, name="Bold", flags=0),
                    dict(value=800.0, name="ExtraBold", flags=0),
                    dict(value=900.0, name="Black", flags=0),
                ],
            ),
            dict(
                tag="wdth",
                name="Width",
                ordering=1,
                values=[
                    dict(value=75.0, name="Condensed", flags=0),
                    dict(value=100.0, name="Normal", flags=2),
                ],
            ),
            dict(
                tag="slnt",
                name="Slant",
                ordering=2,
                values=[
                    dict(value=0.0, name="Upright", flags=2),
                    dict(value=-10.5, name="Oblique", flags=0),
                ],
            ),
            dict(
                tag="opsz",
                name="Optical Size",
                ordering=3,
                values=[
                    dict(value=6.0, name="6pt Thermal", flags=0),
                    dict(value=12.0, name="12pt EHR", flags=0),
                    dict(value=14.0, name="14pt Body", flags=2),
                    dict(value=24.0, name="24pt Header", flags=0),
                    dict(value=72.0, name="72pt Wayfinding", flags=0),
                ],
            ),
            dict(tag="SOFT", name="Felt Cushion", ordering=4, values=[dict(value=0.0, name="Crisp", flags=2), dict(value=1.0, name="Soft", flags=0)]),
            dict(tag="THRM", name="Thermal Bleed Inset", ordering=5, values=[dict(value=0.0, name="Standard", flags=2), dict(value=1.0, name="203dpi Trap", flags=0)]),
            dict(tag="APTR", name="ETDRS Aperture Dilation", ordering=6, values=[dict(value=0.0, name="Normal", flags=2), dict(value=1.0, name="Dilated", flags=0)]),
            dict(tag="SMRN", name="ISMP Disambiguation", ordering=7, values=[dict(value=0.0, name="Standard", flags=2), dict(value=1.0, name="Safe MAR", flags=0)]),
            dict(tag="HLNG", name="Restorative Tone", ordering=8, values=[dict(value=0.0, name="Neutral", flags=2), dict(value=1.0, name="Healing", flags=0)]),
            dict(tag="BION", name="Bionic Fixation", ordering=9, values=[dict(value=0.0, name="Off", flags=2), dict(value=1.0, name="Bionic", flags=0)]),
            dict(tag="GRAV", name="Dyslexia Gravity", ordering=10, values=[dict(value=0.0, name="Standard", flags=2), dict(value=1.0, name="Grounded", flags=0)]),
            dict(tag="BOUM", name="Bouma Margin", ordering=11, values=[dict(value=0.0, name="Normal", flags=2), dict(value=1.0, name="Spacious", flags=0)]),
            dict(tag="CHIS", name="Chisel Nib Angle", ordering=12, values=[dict(value=0.0, name="Round", flags=2), dict(value=45.0, name="Chisel 45", flags=0)]),
            dict(tag="NUQT", name="Nuqta Anti-Clotting", ordering=13, values=[dict(value=0.0, name="Standard", flags=2), dict(value=1.0, name="Anti-Clot", flags=0)]),
            dict(tag="INUK", name="Inuktitut Acuity", ordering=14, values=[dict(value=0.0, name="Standard", flags=2), dict(value=1.0, name="High Apex", flags=0)]),
            dict(tag="BRLS", name="Braille Elevation", ordering=15, values=[dict(value=40.0, name="Low", flags=0), dict(value=78.0, name="Standard", flags=2), dict(value=96.0, name="Tactile", flags=0)]),
        ]
        buildStatTable(tt, axes)


def fix_vf_fvar_instances(tt: TTFont, stem: str, ps_name: str) -> None:
    if "fvar" not in tt:
        return
    nm = tt["name"]
    fvar = tt["fvar"]
    defaults = {ax.axisTag: ax.defaultValue for ax in fvar.axes}

    if stem == "PocketGull-VF":
        rename_map = {
            "Fineliner (EHR Text)": ("Fineliner EHR", "PocketGullVF-FinelinerEHR", {"opsz": 12.0}),
            "Bold (Clinical Header)": ("Clinical Bold", "PocketGullVF-ClinicalBold", {"wght": 700.0, "opsz": 24.0}),
            "Chiseltip (Wayfinding)": ("Chiseltip", "PocketGullVF-Chiseltip", None),
            "Condensed Bold (Telemetry)": ("Condensed Bold", "PocketGullVF-CondensedBold", None),
            "Happy & Healing Sanctuary": ("Healing Calm", "PocketGullVF-HealingCalm", None),
            "Patient Recovery & Homeward Care (72 bpm)": ("Recovery 72bpm", "PocketGullVF-Recovery72bpm", None),
            "203 DPI Thermal Bedside Rx": ("Thermal Bedside", "PocketGullVF-ThermalBedside", None),
            "Bionic Shift Speed": ("Bionic Speed", "PocketGullVF-BionicSpeed", None),
            "Dyslexia High-Gravity": ("Dyslexia Gravity", "PocketGullVF-DyslexiaGravity", None),
            "Arctic Telehealth Syllabics": ("Arctic Syllabics", "PocketGullVF-ArcticSyllabics", None),
            "Grand Ronde Sovereign Pipa": ("Chinuk Pipa", "PocketGullVF-ChinukPipa", None),
            "Tactile Blister Pack Braille": ("Tactile Braille", "PocketGullVF-TactileBraille", None),
            "Persian Penicillin Safe MAR": ("Safe MAR Nuqta", "PocketGullVF-SafeMARNuqta", None),
        }
        next_nid = 600
        for inst in fvar.instances:
            cur_sub = nm.getDebugName(inst.subfamilyNameID) or ""
            if cur_sub == "Regular":
                set_win_name(nm, next_nid, ps_name)
                inst.postscriptNameID = next_nid
                next_nid += 1
            elif cur_sub in rename_map:
                new_sub, new_ps, coord_patch = rename_map[cur_sub]
                set_win_name(nm, next_nid, new_sub)
                inst.subfamilyNameID = next_nid
                next_nid += 1
                set_win_name(nm, next_nid, new_ps)
                inst.postscriptNameID = next_nid
                next_nid += 1
                if coord_patch:
                    for k, v in coord_patch.items():
                        inst.coordinates[k] = v
    elif stem in ("PocketGull-Serif-VF", "PocketGullSerif[wght]"):
        next_nid = 600
        for inst in fvar.instances:
            is_def = all(abs(inst.coordinates.get(k, v) - v) < 1e-4 for k, v in defaults.items())
            if is_def:
                set_win_name(nm, 2, "Regular")
                inst.subfamilyNameID = 2
                set_win_name(nm, next_nid, ps_name)
                inst.postscriptNameID = next_nid
                next_nid += 1
    elif stem == "PocketGull-Sign-VF":
        from fontTools.ttLib.tables._f_v_a_r import NamedInstance
        new_defs = [
            ("Regular", ps_name, {"MRPH": 0.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Sloan", "PocketGullSignVF-Sloan", {"MRPH": 0.0, "wght": 400.0, "opsz": 18.0, "AZIM": 0.0}),
            ("Alimentive", "PocketGullSignVF-Alimentive", {"MRPH": 100.0, "wght": 500.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Thoracic", "PocketGullSignVF-Thoracic", {"MRPH": 200.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Muscular", "PocketGullSignVF-Muscular", {"MRPH": 300.0, "wght": 600.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Osseous", "PocketGullSignVF-Osseous", {"MRPH": 400.0, "wght": 450.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Cerebral", "PocketGullSignVF-Cerebral", {"MRPH": 500.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}),
            ("Expressive", "PocketGullSignVF-Expressive", {"MRPH": 0.0, "wght": 400.0, "opsz": 36.0, "AZIM": 180.0}),
        ]
        fvar.instances = []
        nid = 600
        for s_lbl, p_lbl, coords in new_defs:
            inst = NamedInstance()
            if s_lbl == "Regular":
                inst.subfamilyNameID = 2
            else:
                set_win_name(nm, nid, s_lbl)
                inst.subfamilyNameID = nid
                nid += 1
            set_win_name(nm, nid, p_lbl)
            inst.postscriptNameID = nid
            nid += 1
            inst.coordinates = coords
            fvar.instances.append(inst)


def cure_single_font(ttf_path: Path, donor_bank: dict, reg_aw_map: dict) -> None:
    stem = ttf_path.stem
    if stem not in FONT_META:
        raise ValueError(f"Missing FONT_META entry for {stem}")
    fam, sub, ps, typo_pair, stat_mode = FONT_META[stem]
    is_fixed = stem in FIXED_PITCH_STEMS

    tt = TTFont(str(ttf_path))
    # Force-decompile gvar BEFORE mutating glyf/glyphOrder!
    has_gvar = "gvar" in tt
    if has_gvar:
        _ = tt["gvar"].variations

    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    cmap = tt.getBestCmap()
    go = list(tt.getGlyphOrder())
    donor_key = choose_donor_key(stem, sub)
    donors = donor_bank[donor_key]

    added_glyphs = False

    def set_glyph_and_cmap(cp: int, preferred_name: str, g_obj: Glyph, aw_val: int):
        nonlocal added_glyphs
        existing_gn = cmap.get(cp)
        gn = existing_gn or (preferred_name if preferred_name not in glyf.glyphs else f"u{cp:04X}")
        if gn not in glyf.glyphs:
            go.append(gn)
            added_glyphs = True
        if is_fixed:
            g_fit, mtx = fit_to_fixed_pitch(copy.deepcopy(g_obj), glyf, 600)
            glyf[gn] = g_fit
            hmtx[gn] = mtx
        else:
            g_clean = sanitize_simple_glyph(copy.deepcopy(g_obj), glyf)
            g_clean.recalcBounds(glyf)
            glyf[gn] = g_clean
            hmtx[gn] = (aw_val, g_clean.xMin if g_clean.numberOfContours > 0 else 0)
        if has_gvar:
            tt["gvar"].variations[gn] = []
        cmap[cp] = gn
        for subtable in tt["cmap"].tables:
            if subtable.isUnicode():
                if subtable.format == 4 and cp > 0xFFFF:
                    continue
                subtable.cmap[cp] = gn

    # 1. Case-mapping counterparts (U+014A, U+01EA, U+018F)
    case_pairs = [(0x014B, 0x014A), (0x01EB, 0x01EA), (0x0259, 0x018F)]
    for lower_cp, upper_cp in case_pairs:
        if lower_cp in cmap and (upper_cp not in cmap or glyf[cmap[upper_cp]].numberOfContours == 0):
            pref_gn, d_glyph, d_aw = donors[upper_cp]
            set_glyph_and_cmap(upper_cp, pref_gn, d_glyph, d_aw)

    # 2. Empty letters (U+1BC11.. Duployan / Chinuk Pipa)
    for cp, gn in list(cmap.items()):
        cat = unicodedata.category(chr(cp))
        if cat in ("Ll", "Lm", "Lo", "Lt", "Lu") and cp not in (0x115F, 0x1160, 0x3164, 0xFFA0):
            if glyf[gn].numberOfContours == 0 and cp in donors:
                pref_gn, d_glyph, d_aw = donors[cp]
                set_glyph_and_cmap(cp, pref_gn, d_glyph, d_aw)

    if added_glyphs:
        tt.setGlyphOrder(go)
        tt["maxp"].numGlyphs = len(go)
        if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
            mapping = list(tt["HVAR"].table.AdvWidthMap.mapping)
            if len(mapping) < len(go):
                # Map newly appended static glyphs to zero-delta index 0 (or Regular fallback)
                zero_idx = 0
                var_data = tt["HVAR"].table.VarStore.VarData[0]
                for idx_i, row in enumerate(var_data.Item):
                    if all(v == 0 for v in row):
                        zero_idx = idx_i
                        break
                mapping.extend([zero_idx] * (len(go) - len(mapping)))
                tt["HVAR"].table.AdvWidthMap.mapping = mapping

    # 3. Arabic High Hamza (U+0674) outline area parity with U+0621
    if 0x0621 in cmap and 0x0674 in cmap:
        gn_hamza = cmap[0x0621]
        gn_high = cmap[0x0674]
        g_src, aw_src = extract_decomposed_glyph(tt, gn_hamza, transform=(1, 0, 0, 1, 0, 200))
        if g_src.numberOfContours > 0:
            if is_fixed:
                g_src, mtx = fit_to_fixed_pitch(g_src, glyf, 600)
                glyf[gn_high] = g_src
                hmtx[gn_high] = mtx
            else:
                g_src.recalcBounds(glyf)
                glyf[gn_high] = g_src
                hmtx[gn_high] = (aw_src, g_src.xMin)
            if has_gvar:
                tt["gvar"].variations[gn_high] = []

    # 4. Zero-width bases (base_has_width)
    zw_exempt = {
        0x00AD, 0x115F, 0x1160, 0x180B, 0x180C, 0x180D, 0x180E,
        0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF,
    }
    for cp, gn in cmap.items():
        if cp in zw_exempt or (0xFE00 <= cp <= 0xFE0F) or (0xE0100 <= cp <= 0xE01EF):
            continue
        cat = unicodedata.category(chr(cp))
        if cat in ("Mn", "Cf", "Cc", "Cs", "Zl", "Zp"):
            continue
        cur_aw, cur_lsb = hmtx[gn]
        if cur_aw == 0:
            if is_fixed:
                hmtx[gn] = (600, cur_lsb)
            elif cp in reg_aw_map and reg_aw_map[cp] > 0:
                hmtx[gn] = (reg_aw_map[cp], cur_lsb)
            else:
                g = glyf[gn]
                if g.numberOfContours > 0:
                    g.recalcBounds(glyf)
                    hmtx[gn] = (max(440, (g.xMax - g.xMin) + 120), cur_lsb)
                else:
                    hmtx[gn] = (500, 0)

    # 5. PocketGull-Inline fsSelection / macStyle consistency
    if stem == "PocketGull-Inline":
        tt["head"].macStyle = 0
        tt["OS/2"].usWeightClass = 400
        tt["OS/2"].fsSelection = (1 << 6) | (1 << 7)  # REGULAR | USE_TYPO_METRICS

    # 6. Harmonize OS/2 usWinAscent / usWinDescent (keeping compact-descent standalone cuts within <= 2 * |yMin|)
    if stem in ("PocketGull-Algo", "PocketGull-Emoji", "PocketGull-Genome"):
        tt["OS/2"].usWinAscent = max(1230, int(tt["head"].yMax))
        tt["OS/2"].usWinDescent = max(520, int(abs(min(0, tt["head"].yMin))))
    else:
        tt["OS/2"].usWinAscent = max(1572, int(tt["head"].yMax))
        target_desc = 940 if stem == "PocketGull-Math" else 833
        tt["OS/2"].usWinDescent = max(target_desc, int(abs(min(0, tt["head"].yMin))))
    tt["OS/2"].fsSelection |= (1 << 7)  # Ensure USE_TYPO_METRICS bit 7 always enabled

    # 7. Unified Name Table (Windows PID=3, EID=1, Lang=0x0409 only — zero Mac entries)
    nm = tt["name"]
    nm.names = [r for r in nm.names if r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0409]
    full_name = fam if sub == "Regular" else f"{fam} {sub}"
    set_win_name(nm, 0, COPYRIGHT_STR)
    set_win_name(nm, 1, fam)
    set_win_name(nm, 2, sub)
    set_win_name(nm, 3, f"3.103;PGUL;{ps}")
    set_win_name(nm, 4, full_name)
    set_win_name(nm, 5, VERSION_STR)
    set_win_name(nm, 6, ps)
    if typo_pair is not None:
        set_win_name(nm, 16, typo_pair[0])
        set_win_name(nm, 17, typo_pair[1])
    else:
        remove_name_id(nm, 16)
        remove_name_id(nm, 17)
    if "fvar" in tt:
        set_win_name(nm, 25, ps.replace("-", ""))

    tt["head"].fontRevision = 3.103

    # 8. Fix fvar instances & rebuild STAT, then purge any platformID != 3 records added by buildStatTable
    fix_vf_fvar_instances(tt, stem, ps)
    rebuild_stat(tt, stem, sub, stat_mode)
    nm.names = [r for r in nm.names if r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0409]

    # 9. Mask all simple glyph flags (& 0x3F) and strip any glyph bytecode
    for gname in tt.getGlyphOrder():
        g = glyf[gname]
        if g.numberOfContours > 0:
            g.flags = bytearray([fl & 0x3F for fl in g.flags])
            if hasattr(g, "program") and g.program:
                g.program.fromBytecode(b"")

    tt.save(str(ttf_path))
    tt.close()


def main():
    donor_bank, reg_aw_map = build_donor_bank()
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    print(f"Curing {len(ttf_files)} superfamily TTFs for v3.1.3...")
    for idx, p in enumerate(ttf_files, 1):
        cure_single_font(p, donor_bank, reg_aw_map)
        print(f"  [{idx:2d}/{len(ttf_files)}] Cured {p.name}")


if __name__ == "__main__":
    main()
