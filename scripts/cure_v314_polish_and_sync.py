#!/usr/bin/env python3
"""
PocketGull Typefoundry — v3.1.4 ISO 15008, OpenType Polish, Web Cache-Bust & ASL SVG Sync
=========================================================================================
1. Track 4 (Fontspector ISO 15008 + Top Universal WARN Polish):
   - Tunes PocketGull-CondensedBold.ttf H proportion & lowercase vertical-stem raycast spacing
     for 5/5 PASS (0 FAIL, 0 WARN) on `fontspector --profile iso15008`.
   - Adds spec-compliant `avar` axis-variation tables to all 4 variable fonts
     (PocketGull-VF, PocketGull-Serif-VF, PocketGull-Sign-VF, PocketGullSerif[wght]).
   - Adds OpenType `FeatureParamsStylisticSet` (ssXX) & `FeatureParamsCharacterVariants` (cvXX)
     UI labels in GSUB across all 39 fonts (eliminating `stylisticset_description` WARNs).
   - Populates visible rectangular `.notdef` tofu outlines where empty, recalculates exact
     `OS/2.xAvgCharWidth`, bumps `nameID 5` / `head.fontRevision` to `3.104`, and purges Mac names.
2. Track 3 (1:1 Z-Layered ASL Web Studio SVG Sync):
   - Regenerates `js/asl_svg_data.js` (preserving clinical multi-hand signs HELP/STOP/PAIN/DOCTOR/WATER)
     and `js/asl_morph_svg_data.js` (all 6 morphological archetypes from PocketGull-Sign-VF MRPH=0..500)
     directly from the Z-layered TrueType glyph contours.
3. Track 2 (Web Cache-Busting `?v=3.1.4`, Core Subset Sync, & Docs):
   - Rebuilds all 4 `fonts/woff2/PocketGull-*-Core.woff2` subsets with unified 'PocketGull' + tnum + cv09.
   - Updates `?v=3.1.0` -> `?v=3.1.4` across `fonts.css` and root `.html` studios, plus `package.json` & `README.md`.
"""

import json
import re
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables, ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.subset import Subsetter, Options

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

VERSION_STR = "Version 3.104; The PocketGull Project Authors; OFL 1.1"

SS_LABELS = {
    "ss01": "Alternate Clinical Forms",
    "ss02": "Clinical Barred I & Hooked l",
    "ss03": "High-Legibility Numerals",
    "ss07": "Sovereign High-Acuity Forms",
}

CV_LABELS = {
    "cv05": "Hooked Lowercase l",
    "cv08": "Open-Tail Digit 6 & 9",
    "cv09": "Philocardia Heart Tittle i & j",
    "cv11": "High-Acuity Telemetry Figures",
    "cv12": "Slashed Clinical Zero",
}


def set_win_name(nm, nid: int, val: str) -> None:
    nm.setName(val, nid, 3, 1, 0x0409)
    nm.names = [
        r for r in nm.names
        if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
    ]


def build_notdef_glyph(glyf_table, width: int = 500) -> tuple[Glyph, tuple[int, int]]:
    margin = max(60, int(round(width * 0.14)))
    stroke = 46
    x0, x1 = margin, width - margin
    y0, y1 = 0, 700
    ix0, ix1 = x0 + stroke, x1 - stroke
    iy0, iy1 = y0 + stroke, y1 - stroke

    # Outer CW, inner CCW
    pts = [
        (x0, y0), (x0, y1), (x1, y1), (x1, y0),
        (ix0, iy0), (ix1, iy0), (ix1, iy1), (ix0, iy1),
    ]
    g = Glyph()
    g.numberOfContours = 2
    g.coordinates = GlyphCoordinates(pts)
    g.endPtsOfContours = [3, 7]
    g.flags = bytearray([1] * 8)
    prog = ttProgram.Program()
    prog.fromBytecode(b"")
    g.program = prog
    g.recalcBounds(glyf_table)
    return g, (width, g.xMin)


def polish_single_font(ttf_path: Path) -> None:
    stem = ttf_path.stem
    tt = TTFont(str(ttf_path))
    has_gvar = "gvar" in tt
    if has_gvar:
        _ = tt["gvar"].variations

    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    cmap = tt.getBestCmap()
    nm = tt["name"]

    # 1. ISO 15008 5/5 tuning on PocketGull-CondensedBold
    if stem == "PocketGull-CondensedBold":
        gn_H = cmap[ord("H")]
        gH = glyf[gn_H]
        # Idempotent check: only widen if H ratio < 0.65
        if (gH.xMax - gH.xMin) / 714.0 < 0.65:
            gH.coordinates = GlyphCoordinates([(int(round(70 + (x - 70) * 1.06)), y) for x, y in gH.coordinates])
            gH.recalcBounds(glyf)
            hmtx[gn_H] = (gH.xMax + 70, gH.xMin)
            for ch in "ilmnuhr":
                gn = cmap[ord(ch)]
                g = glyf[gn]
                if g.numberOfContours > 0:
                    g.coordinates = GlyphCoordinates([(x + 8, y) for x, y in g.coordinates])
                    g.recalcBounds(glyf)
                    aw, _ = hmtx[gn]
                    hmtx[gn] = (aw + 16, g.xMin)

    # 2. Ensure visible .notdef glyph outline
    if ".notdef" in glyf.glyphs and glyf[".notdef"].numberOfContours == 0:
        is_fixed = tt["post"].isFixedPitch == 1
        nd_w = 600 if is_fixed else 500
        g_nd, mtx_nd = build_notdef_glyph(glyf, nd_w)
        glyf[".notdef"] = g_nd
        hmtx[".notdef"] = mtx_nd
        if has_gvar:
            tt["gvar"].variations[".notdef"] = []

    # 3. Add avar table to variable fonts
    if "fvar" in tt:
        avar = newTable("avar")
        for ax in tt["fvar"].axes:
            if ax.axisTag == "wght" and ax.minValue < ax.defaultValue < ax.maxValue:
                avar.segments[ax.axisTag] = {-1.0: -1.0, 0.0: 0.0, 0.5: 0.52, 1.0: 1.0}
            else:
                avar.segments[ax.axisTag] = {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}
        tt["avar"] = avar

    # 4. Add FeatureParams UI descriptions for ss01..ss20 and cv01..cv99 in GSUB
    if "GSUB" in tt and tt["GSUB"].table.FeatureList:
        next_ui_nid = 720
        assigned_tags = {}
        for frec in tt["GSUB"].table.FeatureList.FeatureRecord:
            tag = frec.FeatureTag
            feat = frec.Feature
            if re.match(r"^ss(0[1-9]|1[0-9]|20)$", tag):
                if tag not in assigned_tags:
                    lbl = SS_LABELS.get(tag, f"Stylistic Set {int(tag[2:])}")
                    set_win_name(nm, next_ui_nid, lbl)
                    assigned_tags[tag] = next_ui_nid
                    next_ui_nid += 1
                fp = otTables.FeatureParamsStylisticSet()
                fp.Version = 0
                fp.UINameID = assigned_tags[tag]
                feat.FeatureParams = fp
            elif re.match(r"^cv(0[1-9]|[1-9][0-9])$", tag):
                if tag not in assigned_tags:
                    lbl = CV_LABELS.get(tag, f"Character Variant {int(tag[2:])}")
                    set_win_name(nm, next_ui_nid, lbl)
                    assigned_tags[tag] = next_ui_nid
                    next_ui_nid += 1
                fp = otTables.FeatureParamsCharacterVariants()
                fp.Format = 0
                fp.FeatUILabelNameID = assigned_tags[tag]
                fp.FeatUITooltipTextNameID = 0
                fp.SampleTextNameID = 0
                fp.NumNamedParameters = 0
                fp.FirstParamUILabelNameID = 0
                fp.CharCount = 0
                fp.Character = []
                feat.FeatureParams = fp

    # 5. Bump version to 3.104 & recalculate xAvgCharWidth & purge non-Win name entries
    ps = nm.getDebugName(6) or stem
    set_win_name(nm, 3, f"3.104;PGUL;{ps}")
    set_win_name(nm, 5, VERSION_STR)
    tt["head"].fontRevision = 3.104
    tt["OS/2"].recalcAvgCharWidth(tt)
    nm.names = [r for r in nm.names if r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0409]

    # Mask simple glyph flags (& 0x3F)
    for gname in tt.getGlyphOrder():
        g = glyf[gname]
        if g.numberOfContours > 0:
            g.flags = bytearray([fl & 0x3F for fl in g.flags])

    tt.save(str(ttf_path))
    tt.close()


def rebuild_core_woff2_subsets() -> None:
    core_map = {
        "PocketGull-Bold-Core.woff2": "PocketGull-Bold.ttf",
        "PocketGull-Fineliner-Core.woff2": "PocketGull-Fineliner.ttf",
        "PocketGull-Micro-Core.woff2": "PocketGull-Micro.ttf",
        "PocketGull-Regular-Core.woff2": "PocketGull-Regular.ttf",
    }
    for core_w2_name, src_ttf_name in core_map.items():
        w2_path = WOFF2_DIR / core_w2_name
        if not w2_path.is_file():
            continue
        old_tt = TTFont(str(w2_path))
        unicodes = set(old_tt.getBestCmap().keys())
        old_tt.close()

        src_tt = TTFont(str(TTF_DIR / src_ttf_name))
        opts = Options()
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.name_legacy = False
        opts.name_languages = [0x0409]
        opts.notdef_outline = True
        opts.recalc_bounds = True
        opts.recalc_average_width = True
        subsetter = Subsetter(options=opts)
        subsetter.populate(unicodes=unicodes)
        subsetter.subset(src_tt)
        src_tt.flavor = "woff2"
        src_tt.save(str(w2_path))
        src_tt.close()
        print(f"  [+] Rebuilt subset {core_w2_name} ({w2_path.stat().st_size / 1024:.1f} KB)", flush=True)


def glyph_to_svg(tt: TTFont, ch: str, stroke_color: str, use_css_var: bool = False) -> str:
    cmap = tt.getBestCmap()
    gn = cmap[ord(ch)]
    gset = tt.getGlyphSet()
    # Map x in [0..600] -> [8..92], y in [0..860] -> [112..10]
    sx = 84.0 / 600.0
    sy = -102.0 / 860.0
    dx = 8.0
    dy = 112.0
    svg_pen = SVGPathPen(gset, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    tpen = TransformPen(svg_pen, (sx, 0.0, 0.0, sy, dx, dy))
    gset[gn].draw(tpen)
    d_path = svg_pen.getCommands()

    fill_col = "var(--cyan)" if use_css_var else stroke_color
    amber_col = "var(--amber)" if use_css_var else "#f59e0b"

    motion_overlay = ""
    if ch == "J":
        motion_overlay = (
            f'\n  <path d="M 74 20 C 88 28 90 50 84 66 C 78 82 62 90 46 90 C 36 90 30 84 34 76" '
            f'stroke="{amber_col}" stroke-width="3" stroke-dasharray="3,3" fill="none" />'
            f'\n  <polygon points="30,74 38,80 30,86" fill="{amber_col}" stroke="none" />'
        )
    elif ch == "Z":
        motion_overlay = (
            f'\n  <path d="M 56 14 L 88 14 L 58 42 L 90 42" '
            f'stroke="{amber_col}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" fill="none" />'
            f'\n  <polygon points="86,37 95,42 86,47" fill="{amber_col}" stroke="none" />'
        )

    return (
        f'<svg viewBox="0 0 100 120" class="asl-hand-svg" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round">\n'
        f'  <path d="{d_path}" fill="{fill_col}" fill-rule="nonzero" stroke="none" />'
        f'{motion_overlay}\n</svg>'
    )


def regenerate_asl_web_svgs() -> None:
    print("Regenerating js/asl_svg_data.js & js/asl_morph_svg_data.js from Z-layered ASL outlines...", flush=True)
    asl_svg_path = ROOT_DIR / "js" / "asl_svg_data.js"
    old_txt = asl_svg_path.read_text(encoding="utf-8")

    # Extract clinical phrase keys ("HELP", "STOP", "PAIN", "DOCTOR", "WATER") from existing asl_svg_data.js
    preserved = {}
    for phrase in ("HELP", "STOP", "PAIN", "DOCTOR", "WATER"):
        m = re.search(rf'  "{phrase}": ("<svg.*?</svg>")', old_txt)
        if m:
            preserved[phrase] = json.loads(m.group(1))

    chars = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    asl_tt = TTFont(str(TTF_DIR / "PocketGull-ASL.ttf"))
    asl_entries = []
    for ch in chars:
        svg_str = glyph_to_svg(asl_tt, ch, "#06b6d4", use_css_var=True)
        asl_entries.append(f"  {json.dumps(ch)}: {json.dumps(svg_str)}")
    for phrase, svg_str in preserved.items():
        asl_entries.append(f"  {json.dumps(phrase)}: {json.dumps(svg_str)}")
    asl_tt.close()

    asl_js_out = (
        "// PocketGull Z-Layered Anatomical Louise Sloan 5:1 Optotype ASL Vector Library (v3.1.4)\n"
        "const ASL_SVG_DATA = {\n" + ",\n".join(asl_entries) + "\n};\n"
    )
    asl_svg_path.write_text(asl_js_out, encoding="utf-8")

    # Regenerate all 6 morphological hand archetypes in js/asl_morph_svg_data.js from PocketGull-Sign-VF.ttf
    sign_vf = TTFont(str(TTF_DIR / "PocketGull-Sign-VF.ttf"))
    morph_specs = [
        ("sloan", 0.0, "#06b6d4"),
        ("alimentive", 100.0, "#f59e0b"),
        ("thoracic", 200.0, "#ec4899"),
        ("muscular", 300.0, "#06b6d4"),
        ("osseous", 400.0, "#10b981"),
        ("cerebral", 500.0, "#8b5cf6"),
    ]
    morph_blocks = []
    for key, mrph_val, hex_col in morph_specs:
        inst = instantiateVariableFont(sign_vf, {"MRPH": mrph_val, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}, inplace=False)
        ch_lines = []
        for ch in chars:
            svg_str = glyph_to_svg(inst, ch, hex_col, use_css_var=False)
            ch_lines.append(f"    {json.dumps(ch)}: {json.dumps(svg_str)}")
        inst.close()
        morph_blocks.append(f'  "{key}": {{\n' + ",\n".join(ch_lines) + "\n  }")
    sign_vf.close()

    morph_path = ROOT_DIR / "js" / "asl_morph_svg_data.js"
    morph_js_out = (
        "/**\n"
        " * PocketGull Z-Layered Anatomical Morphological ASL Vector Library (v3.1.4)\n"
        " * Synchronized 1:1 with PocketGull-ASL.ttf & PocketGull-Sign-VF.ttf (MRPH 0..500)\n"
        " */\n"
        "const ASL_MORPH_DATA = {\n" + ",\n".join(morph_blocks) + "\n};\n"
    )
    morph_path.write_text(morph_js_out, encoding="utf-8")
    print("  [+] Updated js/asl_svg_data.js & js/asl_morph_svg_data.js", flush=True)


def update_web_cache_and_docs() -> None:
    print("Updating ?v=3.1.4 webfont cache-busters, package.json, and README.md...", flush=True)
    # 1. fonts.css and all root *.html files
    targets = [ROOT_DIR / "fonts.css"] + sorted(ROOT_DIR.glob("*.html"))
    for p in targets:
        if not p.is_file():
            continue
        txt = p.read_text(encoding="utf-8")
        new_txt = re.sub(r"\?v=3\.1\.[0-3]\b", "?v=3.1.4", txt)
        if new_txt != txt:
            p.write_text(new_txt, encoding="utf-8")
            print(f"  [+] Cache-busted ?v=3.1.4 in {p.name}", flush=True)

    # 2. package.json & package-lock.json top-level version
    pkg_path = ROOT_DIR / "package.json"
    if pkg_path.is_file():
        pkg_txt = pkg_path.read_text(encoding="utf-8")
        pkg_txt = re.sub(r'"version":\s*"3\.1\.[0-3]"', '"version": "3.1.4"', pkg_txt, count=1)
        pkg_path.write_text(pkg_txt, encoding="utf-8")

    lock_path = ROOT_DIR / "package-lock.json"
    if lock_path.is_file():
        lock_txt = lock_path.read_text(encoding="utf-8")
        lock_txt = re.sub(r'"version":\s*"3\.1\.[0-3]"', '"version": "3.1.4"', lock_txt, count=2)
        lock_path.write_text(lock_txt, encoding="utf-8")

    # 3. README.md release download URL
    readme_path = ROOT_DIR / "README.md"
    if readme_path.is_file():
        r_txt = readme_path.read_text(encoding="utf-8")
        r_txt = r_txt.replace(
            "releases/download/v3.1.2/pocketgull-typeface-v3.1.2.zip",
            "releases/download/v3.1.4/pocketgull-typeface-v3.1.4.zip",
        ).replace(
            "releases/download/v3.1.3/pocketgull-typeface-v3.1.3.zip",
            "releases/download/v3.1.4/pocketgull-typeface-v3.1.4.zip",
        )
        readme_path.write_text(r_txt, encoding="utf-8")


def main():
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    print(f"Polishing {len(ttf_files)} superfamily TTFs for v3.1.4...", flush=True)
    for idx, p in enumerate(ttf_files, 1):
        polish_single_font(p)
        print(f"  [{idx:2d}/{len(ttf_files)}] Polished {p.name}", flush=True)

    regenerate_asl_web_svgs()
    update_web_cache_and_docs()
    print("v3.1.4 TTF polish, ASL SVG sync, and web cache-busting complete!", flush=True)


if __name__ == "__main__":
    main()
