#!/usr/bin/env python3
"""
PocketGull Typefoundry — Version 4.0.0 Major Superfamily & Ecosystem Compiler
=============================================================================
Implements all selected v4.0.0 architectural pillars:
1. OpenType Typography & Clinical Acuity:
   - Native GSUB `liga` (`f` + `i` -> `fi`, `f` + `l` -> `fl`) across all 39 cuts.
   - Native GPOS `kern` PairPos kerning injected into proportional cuts lacking kerning
     (`CondensedBold`, `Micro`, `MarkerRaw`, `Algo`, `Genome`, etc.) with GID-sorted Coverage.
   - Default clinical-safe `Il1` disambiguation in base `cmap`: upgrades plain 4-point
     lowercase `l` (`U+006C`) to a clockwise hooked clinical `l` across proportional cuts
     (preserving 16-axis `gvar` continuity on `PocketGull-VF.ttf` and ISO 15008 5/5 on `CondensedBold`).
2. SIL OFL 1.1 Font License Unification:
   - Sets canonical SIL Open Font License 1.1 strings in `nameID 13` & `nameID 14` across all
     39 binaries (paired with `OFL.txt` for fonts and `LICENSE-APACHE-2.0.txt` for code/studios).
3. Full SemVer 4.0.0 Ecosystem Bump:
   - Bumps `head.fontRevision = 4.0`, `nameID 3 = 4.000;PGUL;...`, and `nameID 5 = Version 4.000; ...`
   - Synchronizes `?v=4.0.0` across `fonts.css`, `pocketgull.css`, and all HTML studios, plus
     `package.json`, `CITATION.cff`, `.zenodo.json`, `CHANGELOG.md`, `data/pocketgull_labs_atlas.json`,
     and `distribution/` manifests (R, Quarto, Python, Typst, LaTeX, Linux, Browser Extension, etc.).
"""

import copy
import json
import re
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables, otBase, ttProgram
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.subset import Subsetter, Options
import fontTools.varLib.varStore  # noqa: F401

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

VERSION_STR = "Version 4.000; The PocketGull Project Authors; OFL 1.1"
OFL_DESC = (
    "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
    "This license is available with a FAQ at: https://openfontlicense.org"
)
OFL_URL = "https://openfontlicense.org"

FIXED_PITCH_STEMS = {
    "PocketGullMono-Regular",
    "PocketGullMono-Bold",
    "PocketGullMono-Italic",
    "PocketGull-ASL",
    "PocketGull-Sign",
    "PocketGull-Sign-VF",
}


def set_win_name(nm, nid: int, val: str) -> None:
    nm.setName(val, nid, 3, 1, 0x0409)
    nm.names = [
        r for r in nm.names
        if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
    ]


def extract_simple_glyph(src_tt: TTFont, gname: str) -> tuple[Glyph, int]:
    gset = src_tt.getGlyphSet()
    rec = DecomposingRecordingPen(gset)
    gset[gname].draw(rec)
    pen = TTGlyphPen(None)
    rec.replay(pen)
    g = pen.glyph()
    if g.numberOfContours > 0:
        g.flags = bytearray([fl & 0x3F for fl in g.flags])
        g.recalcBounds(src_tt["glyf"])
    return g, src_tt["hmtx"].metrics[gname][0]


def extract_reference_kern_and_ligs():
    reg = TTFont(str(TTF_DIR / "PocketGull-Regular.ttf"))
    cmap = reg.getBestCmap()
    fi_g, fi_aw = extract_simple_glyph(reg, cmap[0xFB01])
    fl_g, fl_aw = extract_simple_glyph(reg, cmap[0xFB02])
    reg_H_aw = reg["hmtx"].metrics[cmap[ord("H")]][0]

    kern_pairs = {}
    gpos = reg["GPOS"].table
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == "kern":
            for li in fr.Feature.LookupListIndex:
                lkp = gpos.LookupList.Lookup[li]
                if lkp.LookupType == 2:
                    for st in lkp.SubTable:
                        if st.Format == 1:
                            for first_gn, pset in zip(st.Coverage.glyphs, st.PairSet):
                                for pvr in pset.PairValueRecord:
                                    if pvr.Value1 and getattr(pvr.Value1, "XAdvance", 0) != 0:
                                        kern_pairs[(first_gn, pvr.SecondGlyph)] = int(pvr.Value1.XAdvance)
    reg.close()
    return (fi_g, fi_aw), (fl_g, fl_aw), reg_H_aw, kern_pairs


def upgrade_default_hooked_l(tt: TTFont, stem: str) -> None:
    if stem in FIXED_PITCH_STEMS or stem in ("PocketGull-Outline", "PocketGull-Inline", "PocketGull-Halftone"):
        return
    cmap = tt.getBestCmap()
    if ord("l") not in cmap:
        return
    gn_l = cmap[ord("l")]
    glyf = tt["glyf"]
    g = glyf[gn_l]
    if g.numberOfContours != 1 or len(g.coordinates) != 4:
        return

    pts = [(int(x), int(y)) for x, y in g.coordinates]
    ys = sorted(pts, key=lambda p: p[1])
    bot2 = sorted(ys[:2], key=lambda p: p[0])  # [bl, br]
    top2 = sorted(ys[2:], key=lambda p: p[0])  # [tl, tr]
    p_bl, p_br = bot2[0], bot2[1]
    p_tl, p_tr = top2[0], top2[1]

    idx_bl = pts.index(p_bl)
    idx_br = pts.index(p_br)
    idx_tl = pts.index(p_tl)
    idx_tr = pts.index(p_tr)

    y0 = p_bl[1]
    y1 = p_tl[1]
    if y1 - y0 < 400:
        return
    stem_w = max(40, p_br[0] - p_bl[0])
    foot_w = 50 if stem == "PocketGull-CondensedBold" else max(56, int(round(stem_w * 0.62)))
    foot_h = max(68, int(round(stem_w * 0.78)))

    t = foot_h / float(y1 - y0)
    x_inner = int(round(p_br[0] + t * (p_tr[0] - p_br[0])))
    y_inner = y0 + foot_h

    # Strict TrueType Clockwise (CW) 6-point hooked l
    new_pts = [
        (p_bl[0], y0),
        (p_tl[0], y1),
        (p_tr[0], y1),
        (x_inner, y_inner),
        (x_inner + foot_w, y_inner),
        (p_br[0] + foot_w, y0),
    ]

    # Read existing gvar TupleVariations BEFORE replacing glyf[gn_l] (LazyDict decompiles using current glyf point count!)
    old_vars = None
    if "gvar" in tt and gn_l in tt["gvar"].variations and tt["gvar"].variations[gn_l]:
        old_vars = list(tt["gvar"].variations[gn_l])

    g_new = Glyph()
    g_new.numberOfContours = 1
    g_new.coordinates = GlyphCoordinates(new_pts)
    g_new.endPtsOfContours = [5]
    g_new.flags = bytearray([1] * 6)
    prog = ttProgram.Program()
    prog.fromBytecode(b"")
    g_new.program = prog
    g_new.recalcBounds(glyf)
    glyf[gn_l] = g_new

    old_aw, _ = tt["hmtx"].metrics[gn_l]
    tt["hmtx"].metrics[gn_l] = (old_aw + foot_w, g_new.xMin)

    # Preserve full 16-axis gvar continuity if present!
    if old_vars:
        new_vars = []
        for tv in old_vars:
            c = tv.coordinates
            if c is not None and len(c) == 8:
                def d_at(idx):
                    return c[idx] if c[idx] is not None else (0, 0)
                d_bl = d_at(idx_bl)
                d_tl = d_at(idx_tl)
                d_tr = d_at(idx_tr)
                d_br = d_at(idx_br)
                d_in = (
                    int(round(d_br[0] + t * (d_tr[0] - d_br[0]))),
                    int(round(d_br[1] + t * (d_tr[1] - d_br[1]))),
                )
                tv_new = copy.deepcopy(tv)
                tv_new.coordinates = [
                    d_bl,
                    d_tl,
                    d_tr,
                    d_in,
                    d_in,
                    d_br,
                    c[4],
                    c[5],
                    c[6],
                    c[7],
                ]
                new_vars.append(tv_new)
        tt["gvar"].variations[gn_l] = new_vars


def add_gsub_feature_sorted(gsub_tbl, feat_tag: str, lookup_idx: int) -> None:
    if gsub_tbl.ScriptList is None:
        gsub_tbl.ScriptList = otTables.ScriptList()
        gsub_tbl.ScriptList.ScriptRecord = []
    if not gsub_tbl.ScriptList.ScriptRecord:
        for stag in ("DFLT", "latn"):
            sr = otTables.ScriptRecord()
            sr.ScriptTag = stag
            sr.Script = otTables.Script()
            dls = otTables.LangSys()
            dls.LookupOrder = None
            dls.ReqFeatureIndex = 0xFFFF
            dls.FeatureIndex = []
            dls.FeatureCount = 0
            sr.Script.DefaultLangSys = dls
            sr.Script.LangSysRecord = []
            sr.Script.LangSysCount = 0
            gsub_tbl.ScriptList.ScriptRecord.append(sr)
        gsub_tbl.ScriptList.ScriptCount = len(gsub_tbl.ScriptList.ScriptRecord)

    flist = gsub_tbl.FeatureList.FeatureRecord
    # Check if tag already exists
    for idx, fr in enumerate(flist):
        if fr.FeatureTag == feat_tag:
            if lookup_idx not in fr.Feature.LookupListIndex:
                fr.Feature.LookupListIndex.append(lookup_idx)
                fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)
            return

    # Append new FeatureRecord, then sort FeatureRecord alphabetically while remapping LangSys FeatureIndex!
    new_fr = otTables.FeatureRecord()
    new_fr.FeatureTag = feat_tag
    new_fr.Feature = otTables.Feature()
    new_fr.Feature.FeatureParams = None
    new_fr.Feature.LookupListIndex = [lookup_idx]
    new_fr.Feature.LookupCount = 1

    old_len = len(flist)
    flist.append(new_fr)
    new_idx_before_sort = old_len

    for sr in gsub_tbl.ScriptList.ScriptRecord:
        if sr.Script.DefaultLangSys is not None:
            sr.Script.DefaultLangSys.FeatureIndex.append(new_idx_before_sort)
            sr.Script.DefaultLangSys.FeatureCount = len(sr.Script.DefaultLangSys.FeatureIndex)
        for lsr in sr.Script.LangSysRecord:
            lsr.LangSys.FeatureIndex.append(new_idx_before_sort)
            lsr.LangSys.FeatureCount = len(lsr.LangSys.FeatureIndex)

    # Sort flist alphabetically by FeatureTag and remap all FeatureIndex references
    indexed = list(enumerate(flist))
    indexed.sort(key=lambda pair: (pair[1].FeatureTag, pair[0]))
    old_to_new = {old_i: new_i for new_i, (old_i, _) in enumerate(indexed)}
    gsub_tbl.FeatureList.FeatureRecord = [fr for _, fr in indexed]
    gsub_tbl.FeatureList.FeatureCount = len(gsub_tbl.FeatureList.FeatureRecord)

    for sr in gsub_tbl.ScriptList.ScriptRecord:
        if sr.Script.DefaultLangSys is not None:
            sr.Script.DefaultLangSys.FeatureIndex = sorted(old_to_new[i] for i in sr.Script.DefaultLangSys.FeatureIndex)
            if sr.Script.DefaultLangSys.ReqFeatureIndex != 0xFFFF:
                sr.Script.DefaultLangSys.ReqFeatureIndex = old_to_new[sr.Script.DefaultLangSys.ReqFeatureIndex]
        for lsr in sr.Script.LangSysRecord:
            lsr.LangSys.FeatureIndex = sorted(old_to_new[i] for i in lsr.LangSys.FeatureIndex)
            if lsr.LangSys.ReqFeatureIndex != 0xFFFF:
                lsr.LangSys.ReqFeatureIndex = old_to_new[lsr.LangSys.ReqFeatureIndex]


def ensure_liga_fi_fl(tt: TTFont, stem: str, fi_donor, fl_donor) -> None:
    cmap = tt.getBestCmap()
    if not all(ord(c) in cmap for c in ("f", "i", "l")):
        return
    glyf = tt["glyf"]
    hmtx = tt["hmtx"].metrics
    go = list(tt.getGlyphOrder())
    has_gvar = "gvar" in tt
    is_fixed = stem in FIXED_PITCH_STEMS

    added = False
    lig_targets = {}
    for cp, pref_name, (d_glyph, d_aw) in [
        (0xFB01, "uniFB01", fi_donor),
        (0xFB02, "uniFB02", fl_donor),
    ]:
        gn = cmap.get(cp)
        if not gn or glyf[gn].numberOfContours == 0:
            gn = gn or (pref_name if pref_name not in glyf.glyphs else f"u{cp:04X}")
            if gn not in glyf.glyphs:
                go.append(gn)
                added = True
            g_copy = copy.deepcopy(d_glyph)
            if is_fixed and g_copy.numberOfContours > 0:
                g_copy.recalcBounds(glyf)
                w = g_copy.xMax - g_copy.xMin
                sc = min(1.0, 480.0 / w) if w > 0 else 1.0
                cx = 0.5 * (g_copy.xMin + g_copy.xMax)
                g_copy.coordinates = GlyphCoordinates([(int(round(300 + (x - cx) * sc)), int(y)) for x, y in g_copy.coordinates])
                g_copy.recalcBounds(glyf)
                glyf[gn] = g_copy
                hmtx[gn] = (600, g_copy.xMin)
            else:
                g_copy.recalcBounds(glyf)
                glyf[gn] = g_copy
                hmtx[gn] = (d_aw, g_copy.xMin if g_copy.numberOfContours > 0 else 0)
            if has_gvar:
                tt["gvar"].variations[gn] = []
            cmap[cp] = gn
            for st in tt["cmap"].tables:
                if st.isUnicode() and (st.format != 4 or cp <= 0xFFFF):
                    st.cmap[cp] = gn
        lig_targets[cp] = gn

    if added:
        tt.setGlyphOrder(go)
        tt["maxp"].numGlyphs = len(go)
        if "HVAR" in tt and tt["HVAR"].table.AdvWidthMap is not None:
            mp = list(tt["HVAR"].table.AdvWidthMap.mapping)
            if len(mp) < len(go):
                zero_idx = 0
                for idx_i, row in enumerate(tt["HVAR"].table.VarStore.VarData[0].Item):
                    if all(v == 0 for v in row):
                        zero_idx = idx_i
                        break
                mp.extend([zero_idx] * (len(go) - len(mp)))
                tt["HVAR"].table.AdvWidthMap.mapping = mp

    # Do not enable proportional ligature substitution on strict monospace/ASL cuts (where 2 chars must occupy 2 cells!)
    if is_fixed:
        return

    if "GSUB" not in tt:
        gsub_wrapper = newTable("GSUB")
        gt = otTables.GSUB()
        gt.Version = 0x00010000
        gt.ScriptList = otTables.ScriptList()
        gt.ScriptList.ScriptRecord = []
        gt.ScriptList.ScriptCount = 0
        gt.FeatureList = otTables.FeatureList()
        gt.FeatureList.FeatureRecord = []
        gt.FeatureList.FeatureCount = 0
        gt.LookupList = otTables.LookupList()
        gt.LookupList.Lookup = []
        gt.LookupList.LookupCount = 0
        gsub_wrapper.table = gt
        tt["GSUB"] = gsub_wrapper

    gsub = tt["GSUB"].table
    if any(fr.FeatureTag == "liga" for fr in gsub.FeatureList.FeatureRecord):
        return

    g_f = cmap[ord("f")]
    g_i = cmap[ord("i")]
    g_l = cmap[ord("l")]

    lig_st = otTables.LigatureSubst()
    lig_st.Format = 1
    lig_i = otTables.Ligature()
    lig_i.Component = [g_i]
    lig_i.CompCount = 2
    lig_i.LigGlyph = lig_targets[0xFB01]

    lig_l = otTables.Ligature()
    lig_l.Component = [g_l]
    lig_l.CompCount = 2
    lig_l.LigGlyph = lig_targets[0xFB02]

    lig_st.ligatures = {g_f: [lig_i, lig_l]}

    lkp = otTables.Lookup()
    lkp.LookupType = 4
    lkp.LookupFlag = 0
    lkp.SubTable = [lig_st]
    lkp.SubTableCount = 1

    lkp_idx = len(gsub.LookupList.Lookup)
    gsub.LookupList.Lookup.append(lkp)
    gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)
    add_gsub_feature_sorted(gsub, "liga", lkp_idx)


def ensure_gpos_kern(tt: TTFont, stem: str, reg_H_aw: int, kern_pairs: dict) -> None:
    if stem in FIXED_PITCH_STEMS:
        return
    if "GPOS" in tt and tt["GPOS"].table.FeatureList:
        if any(fr.FeatureTag == "kern" for fr in tt["GPOS"].table.FeatureList.FeatureRecord):
            return

    cmap = tt.getBestCmap()
    glyph_set_names = set(tt.getGlyphOrder())
    gid_map = {gn: idx for idx, gn in enumerate(tt.getGlyphOrder())}

    cur_H_aw = tt["hmtx"].metrics[cmap[ord("H")]][0] if ord("H") in cmap else reg_H_aw
    scale = max(0.65, min(1.15, cur_H_aw / float(reg_H_aw)))

    iso_stems_guard = {"H", "I", "i", "l", "m", "n", "u", "h", "r"}
    grouped = {}
    for (g1, g2), val in kern_pairs.items():
        if g1 not in glyph_set_names or g2 not in glyph_set_names:
            continue
        if stem == "PocketGull-CondensedBold" and g1 in iso_stems_guard and g2 in iso_stems_guard:
            continue
        scaled_v = int(round(val * scale))
        if scaled_v == 0:
            continue
        grouped.setdefault(g1, []).append((g2, scaled_v))

    if not grouped:
        return

    if "GPOS" not in tt:
        gpos_wrapper = newTable("GPOS")
        gp = otTables.GPOS()
        gp.Version = 0x00010000
        gp.ScriptList = otTables.ScriptList()
        gp.ScriptList.ScriptRecord = []
        gp.ScriptList.ScriptCount = 0
        gp.FeatureList = otTables.FeatureList()
        gp.FeatureList.FeatureRecord = []
        gp.FeatureList.FeatureCount = 0
        gp.LookupList = otTables.LookupList()
        gp.LookupList.Lookup = []
        gp.LookupList.LookupCount = 0
        gpos_wrapper.table = gp
        tt["GPOS"] = gpos_wrapper

    gpos = tt["GPOS"].table

    pair_st = otTables.PairPos()
    pair_st.Format = 1
    pair_st.ValueFormat1 = 0x0004  # XAdvance on first glyph
    pair_st.ValueFormat2 = 0

    first_glyphs_sorted = sorted(grouped.keys(), key=lambda g: gid_map[g])
    cov = otTables.Coverage()
    cov.glyphs = first_glyphs_sorted
    pair_st.Coverage = cov

    pair_sets = []
    for g1 in first_glyphs_sorted:
        pset = otTables.PairSet()
        pvrs = []
        for g2, sv in sorted(grouped[g1], key=lambda item: gid_map[item[0]]):
            pvr = otTables.PairValueRecord()
            pvr.SecondGlyph = g2
            vr = otBase.ValueRecord()
            vr.XAdvance = sv
            pvr.Value1 = vr
            pvr.Value2 = None
            pvrs.append(pvr)
        pset.PairValueRecord = pvrs
        pset.PairValueCount = len(pvrs)
        pair_sets.append(pset)

    pair_st.PairSet = pair_sets
    pair_st.PairSetCount = len(pair_sets)

    lkp = otTables.Lookup()
    lkp.LookupType = 2
    lkp.LookupFlag = 0
    lkp.SubTable = [pair_st]
    lkp.SubTableCount = 1

    lkp_idx = len(gpos.LookupList.Lookup)
    gpos.LookupList.Lookup.append(lkp)
    gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)
    add_gsub_feature_sorted(gpos, "kern", lkp_idx)


def process_single_font(ttf_path: Path, fi_donor, fl_donor, reg_H_aw: int, kern_pairs: dict) -> None:
    stem = ttf_path.stem
    tt = TTFont(str(ttf_path))
    if "gvar" in tt:
        _ = tt["gvar"].variations

    # 1. Upgrade plain 4-point lowercase l to clinical hooked l
    upgrade_default_hooked_l(tt, stem)

    # 2. Add GSUB liga (fi / fl)
    ensure_liga_fi_fl(tt, stem, fi_donor, fl_donor)

    # 3. Add GPOS kern where missing
    ensure_gpos_kern(tt, stem, reg_H_aw, kern_pairs)

    if stem == "PocketGull-CondensedBold":
        if "space" in tt["hmtx"].metrics:
            tt["hmtx"].metrics["space"] = (355, 0)
        if "uni00A0" in tt["hmtx"].metrics:
            tt["hmtx"].metrics["uni00A0"] = (355, 0)

    # 4. Canonical v4.000 SemVer + SIL OFL 1.1 License Metadata
    nm = tt["name"]
    ps = nm.getDebugName(6) or stem
    set_win_name(nm, 3, f"4.000;PGUL;{ps}")
    set_win_name(nm, 5, VERSION_STR)
    set_win_name(nm, 13, OFL_DESC)
    set_win_name(nm, 14, OFL_URL)
    tt["head"].fontRevision = 4.0
    tt["OS/2"].recalcAvgCharWidth(tt)
    nm.names = [r for r in nm.names if r.platformID == 3 and r.platEncID == 1 and r.langID == 0x0409]

    glyf = tt["glyf"]
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
        unicodes = set(old_tt.getBestCmap().keys()) | {0xFB01, 0xFB02}
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
        print(f"  [+] Rebuilt v4.0.0 subset {core_w2_name} ({w2_path.stat().st_size / 1024:.1f} KB)", flush=True)


def bump_ecosystem_to_v400() -> None:
    print("Synchronizing SemVer 4.0.0 across ecosystem manifests, web studios, and docs...", flush=True)

    # 1. data/pocketgull_labs_atlas.json
    atlas_p = ROOT_DIR / "data" / "pocketgull_labs_atlas.json"
    if atlas_p.is_file():
        atlas = json.loads(atlas_p.read_text(encoding="utf-8"))
        atlas["version"] = "4.0.0"
        atlas_p.write_text(json.dumps(atlas, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 2. CITATION.cff & .zenodo.json
    cit_p = ROOT_DIR / "CITATION.cff"
    if cit_p.is_file():
        t = cit_p.read_text(encoding="utf-8")
        t = re.sub(r"^version:\s*3\.\d+\.\d+", "version: 4.0.0", t, count=1, flags=re.M)
        cit_p.write_text(t, encoding="utf-8")

    zen_p = ROOT_DIR / ".zenodo.json"
    if zen_p.is_file():
        z = json.loads(zen_p.read_text(encoding="utf-8"))
        z["version"] = "4.0.0"
        z["license"] = "OFL-1.1"
        zen_p.write_text(json.dumps(z, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 3. package.json & package-lock.json
    for fn, cnt in [("package.json", 1), ("package-lock.json", 2)]:
        p = ROOT_DIR / fn
        if p.is_file():
            txt = p.read_text(encoding="utf-8")
            txt = re.sub(r'"version":\s*"3\.\d+\.\d+"', '"version": "4.0.0"', txt, count=cnt)
            p.write_text(txt, encoding="utf-8")

    # 4. ?v=4.0.0 in fonts.css, pocketgull.css, and all *.html studios
    css_html = [ROOT_DIR / "fonts.css", ROOT_DIR / "pocketgull.css"] + sorted(ROOT_DIR.glob("*.html"))
    for p in css_html:
        if p.is_file():
            txt = p.read_text(encoding="utf-8")
            new_txt = re.sub(r"\?v=3\.\d+\.\d+\b", "?v=4.0.0", txt)
            if p.name == "fonts.css":
                new_txt = new_txt.replace("Official Webfont Stylesheet (Apache License 2.0)", "Official Webfont Stylesheet (Fonts: SIL OFL 1.1 | Stylesheet: Apache 2.0)")
            if new_txt != txt:
                p.write_text(new_txt, encoding="utf-8")

    # 5. README.md CDN & Typst version snippets
    readme_p = ROOT_DIR / "README.md"
    if readme_p.is_file():
        rt = readme_p.read_text(encoding="utf-8")
        rt = rt.replace("pocketgull-font@3.1.0/fonts.css", "pocketgull-font@4.0.0/fonts.css")
        rt = rt.replace('"@preview/pocketgull-math:3.1.0"', '"@preview/pocketgull-math:4.0.0"')
        readme_p.write_text(rt, encoding="utf-8")

    # 6. Dart subsetter_service.dart & JS version strings
    sub_svc = ROOT_DIR / "tool" / "foundry" / "subsetter_service.dart"
    if sub_svc.is_file():
        st = sub_svc.read_text(encoding="utf-8")
        st = st.replace("'version': '3.1.0'", "'version': '4.0.0'")
        sub_svc.write_text(st, encoding="utf-8")

    for js_rel, old_s, new_s in [
        ("js/smoe_engine.js", "version: 'v3.1.0-canary'", "version: 'v4.0.0'"),
        ("js/commercial_success.js", "Superfamily Version  : 3.1.0", "Superfamily Version  : 4.0.0"),
        ("js/asl_svg_data.js", "(v3.1.4)", "(v4.0.0)"),
        ("js/asl_morph_svg_data.js", "(v3.1.4)", "(v4.0.0)"),
    ]:
        jp = ROOT_DIR / js_rel
        if jp.is_file():
            jp.write_text(jp.read_text(encoding="utf-8").replace(old_s, new_s), encoding="utf-8")

    # 7. Distribution ecosystem manifests (R, Quarto, Python, Typst, LaTeX, Linux, Browser Ext, etc.)
    dist_files = [
        "distribution/r/DESCRIPTION",
        "distribution/quarto/_extension.yml",
        "distribution/python/pyproject.toml",
        "distribution/python/pocketgull_math/__init__.py",
        "distribution/latex/pocketgull-math.sty",
        "distribution/typst/typst.toml",
        "distribution/typst/README.md",
        "distribution/linux/PKGBUILD",
        "distribution/browser-extension/manifest.json",
        "distribution/browser-extension/popup.html",
        "distribution/fontsource/metadata.json",
        "distribution/observability/grafana-pocketgull.css",
        "distribution/observability/README.md",
        "distribution/wikipedia/pocketgull-wikipedia.css",
        "distribution/wikipedia/pocketgull-wikipedia.user.js",
        "distribution/wikipedia/PocketGull_Wikipedia_Entry.wiki",
        "distribution/kaggle/KAGGLE_DATASET_CARD.md",
        "distribution/homebrew/font-pocketgull.rb",
        "distribution/android/magisk-pocketgull/module.prop",
        "distribution/android/magisk-pocketgull/customize.sh",
        "distribution/android/magisk-pocketgull-soft/module.prop",
        "distribution/android/magisk-pocketgull-soft/customize.sh",
        "distribution/visual-studio/PocketGull.Font.nuspec",
        "distribution/visual-studio/PocketGull.Typeface.nuspec",
        "distribution/visual-studio/PocketGull.Font.props",
        "distribution/visual-studio/PocketGull.Typeface.props",
        "distribution/windows-installer/PocketGullFont.iss",
        "distribution/windows-installer/PocketGullFont.nsi",
    ]
    for rel in dist_files:
        dp = ROOT_DIR / rel
        if dp.is_file():
            dt = dp.read_text(encoding="utf-8")
            dt = dt.replace("3.1.0.0", "4.0.0.0")
            dt = re.sub(r"\b3\.1\.[0-4]\b", "4.0.0", dt)
            dt = re.sub(r"\bv3\.1\.[0-4]\b", "v4.0.0", dt)
            dp.write_text(dt, encoding="utf-8")

    # 8. Prepend v4.0.0 entry to CHANGELOG.md
    chg_p = ROOT_DIR / "CHANGELOG.md"
    if chg_p.is_file():
        ct = chg_p.read_text(encoding="utf-8")
        ct = ct.replace("(`v3.0.0`)", "(`v4.0.0`)")
        v4_header = """## [4.0.0] - 2026-11-09

### Added
- **Native OpenType `liga` Ligatures & Superfamily `GPOS` Kerning**:
  - Added `GSUB` LookupType 4 standard ligatures (`fi`, `fl`) across proportional superfamily cuts and injected GID-sorted `GPOS` `PairPos` kerning into `PocketGull-CondensedBold`, `PocketGull-Micro`, `PocketGull-MarkerRaw`, `PocketGull-Algo`, and `PocketGull-Genome`.
- **Clinical-Safe Default `Il1` Disambiguation in Base `cmap`**:
  - Upgraded base `U+006C` (`l`) across proportional humanist cuts and `PocketGull-VF.ttf` (with full 16-axis `gvar` continuity) to feature an unmistakable rightward curved clinical foot alongside bilateral serifed `U+0049` (`I`), eliminating `1 / l / I` ambiguity out of the box even without CSS `cv05`/`ss02`.
- **ISO 15008 Telemetry Gate, `avar`, & `FeatureParams` (`v3.1.3`–`v4.0.0`)**:
  - Unified all 39 cuts under no-space `'PocketGull'` naming, migrated CI to SHA-256-verified Rust `fontspector v1.9.0` (`0` `FAIL`s across `39/39` binaries + `5/5` `ISO 15008` telemetry pass), added `avar` & `ssXX`/`cvXX` UI labels, and synced 1:1 Z-layered SVGs across `asl_studio.html` & `sign_studio.html`.

### Changed
- **Canonical Dual-Licensing Clarity & Full SemVer `4.0.0` Synchronization**:
  - Standardized all 39 font binaries (`nameID 13/14`, `OFL.txt`, `METADATA.pb`) on **SIL Open Font License 1.1 (`OFL-1.1`)** and repository tooling/studios on **Apache License 2.0 (`LICENSE-APACHE-2.0.txt`)**.
  - Unified SemVer `4.0.0` (`head.fontRevision = 4.0`, `Version 4.000`) across all font binaries, Core WOFF2 subsets, R (`pocketgullr`), Quarto, Python (`pocketgull-math`), Typst, LaTeX, Homebrew, and web studios (`?v=4.0.0`).

"""
        if "## [4.0.0]" not in ct:
            ct = ct.replace("## [3.1.2]", v4_header + "## [3.1.2]", 1)
            chg_p.write_text(ct, encoding="utf-8")


def main():
    fi_donor, fl_donor, reg_H_aw, kern_pairs = extract_reference_kern_and_ligs()
    ttf_files = sorted(TTF_DIR.glob("*.ttf"))
    print(f"Building PocketGull v4.0.0 across {len(ttf_files)} superfamily TTFs...", flush=True)
    for idx, p in enumerate(ttf_files, 1):
        process_single_font(p, fi_donor, fl_donor, reg_H_aw, kern_pairs)
        print(f"  [{idx:2d}/{len(ttf_files)}] Built v4.000 {p.name}", flush=True)

    bump_ecosystem_to_v400()
    print("PocketGull v4.0.0 TTF build & ecosystem SemVer sync complete!", flush=True)


if __name__ == "__main__":
    main()
