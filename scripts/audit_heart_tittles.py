#!/usr/bin/env python3
"""
PocketGull Typefoundry — Forensic Philocardia Varieties, Punctuation & Math Audit
=================================================================================
Verifies all 38 non-Sign TTFs, 38 WOFF2s, 4 Core subsets, root/ofl/apache/distribution
mirrors, all 8 OpenType GSUB tags (cv09, cv10, cv19, ss07..ss11) strictly < min_liga,
all 30 synthesized variety+dotless glyphs per cut, all 6 standalone symbols,
PocketGull-Math.ttf U+1D6A4/U+1D6A5 + MATH table + AxisHeight=260 alignment,
VF multi-axis gvar/HVAR extremes, and live HarfBuzz shaping.
"""

from __future__ import annotations

import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.varLib.iup import iup_delta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
SKIP_FONTS = {"PocketGull-ASL.ttf", "PocketGull-Sign.ttf", "PocketGull-Sign-VF.ttf"}

EXPECTED_CHARS = [
    (0x0069, "i", "top", "letter"),
    (0x006A, "j", "top", "letter"),
    (0x0021, "exclam", "bottom", "punct"),
    (0x003F, "question", "bottom", "punct"),
    (0x00A1, "exclamdown", "top", "punct"),
    (0x00BF, "questiondown", "top", "punct"),
]

TARGET_TAGS = ("cv09", "cv10", "cv19", "ss07", "ss08", "ss09", "ss10", "ss11")

VARIETY_FEATURE_MAP = [
    ("heart", None, (1.05, 1.38)),
    ("blossom", "ss08", (0.90, 1.18)),
    ("nuqta", "ss09", (0.90, 1.18)),
    ("star", "ss10", (0.90, 1.18)),
    ("droplet", "ss11", (0.74, 0.98)),
]

STANDALONE_CPS = (0x2665, 0x2724, 0x25C6, 0x2726, 0x25CF, 0x1F4A7)


def shoelace_area(pts: list[tuple[float, float]]) -> float:
    n = len(pts)
    return sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2.0


def extract_contours(glyf, gn: str) -> list[dict]:
    g = glyf[gn]
    if g.isComposite() or g.numberOfContours <= 0:
        return []
    c, e, f = g.getCoordinates(glyf)
    res = []
    s = 0
    for ci, end in enumerate(e):
        pts = [(int(c[k][0]), int(c[k][1])) for k in range(s, end + 1)]
        fls = [int(f[k]) for k in range(s, end + 1)]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        dups = sum(1 for k in range(len(pts)) if pts[k] == pts[(k + 1) % len(pts)])
        bit7 = sum(1 for fl in fls if fl & 0xC0)
        res.append({
            "ci": ci,
            "pts": pts,
            "fls": fls,
            "xmin": min(xs),
            "xmax": max(xs),
            "ymin": min(ys),
            "ymax": max(ys),
            "w": max(xs) - min(xs),
            "h": max(ys) - min(ys),
            "area": shoelace_area(pts),
            "dups": dups,
            "bit7": bit7,
        })
        s = end + 1
    return res


def get_feature_info(tt: TTFont) -> tuple[bool, dict, dict, dict, dict]:
    gsub = tt["GSUB"].table
    tags = [fr.FeatureTag for fr in gsub.FeatureList.FeatureRecord]
    sorted_ok = tags == sorted(tags)
    feat_maps: dict[str, dict[str, str]] = {}
    feat_lidxs: dict[str, list[int]] = {}
    feat_params: dict[str, tuple[str | None, list[int]]] = {}
    tag_indices: dict[str, list[int]] = {}

    watched = set(TARGET_TAGS) | {"liga"}
    for idx, fr in enumerate(gsub.FeatureList.FeatureRecord):
        tag = fr.FeatureTag
        tag_indices.setdefault(tag, []).append(idx)
        if tag in watched:
            mp: dict[str, str] = {}
            for li in fr.Feature.LookupListIndex:
                lk = gsub.LookupList.Lookup[li]
                for st in lk.SubTable:
                    if hasattr(st, "mapping"):
                        mp.update(st.mapping)
            feat_maps[tag] = mp
            feat_lidxs[tag] = list(fr.Feature.LookupListIndex)
            fp = fr.Feature.FeatureParams
            lbl = None
            chars: list[int] = []
            if fp is not None:
                nid = getattr(fp, "FeatUILabelNameID", None) or getattr(fp, "UINameID", None)
                if nid:
                    lbl = tt["name"].getDebugName(nid)
                chars = list(getattr(fp, "Character", []) or [])
            feat_params[tag] = (lbl, chars)

    script_reg: dict[str, bool] = {}
    if gsub.ScriptList is not None:
        for tag in TARGET_TAGS:
            idxs = set(tag_indices.get(tag, []))
            ok = bool(idxs)
            for sr in gsub.ScriptList.ScriptRecord:
                if sr.Script.DefaultLangSys is not None:
                    if not (idxs & set(sr.Script.DefaultLangSys.FeatureIndex)):
                        ok = False
                for ls in getattr(sr.Script, "LangSysRecord", []) or []:
                    if not (idxs & set(ls.LangSys.FeatureIndex)):
                        ok = False
            script_reg[tag] = ok

    return sorted_ok, feat_maps, feat_lidxs, feat_params, script_reg


def audit_font_binary(path: Path, is_subset: bool = False) -> list[str]:
    errs: list[str] = []
    name = path.name
    tt = TTFont(str(path))
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    cmap = tt.getBestCmap() or {}
    gorder = tt.getGlyphOrder()
    gid_map = {gn: idx for idx, gn in enumerate(gorder)}
    italic_angle = float(tt["post"].italicAngle) if "post" in tt else 0.0
    is_ttf = path.suffix.lower() == ".ttf"
    loca = list(tt["loca"].locations) if is_ttf and "loca" in tt else None

    sorted_ok, feat_maps, feat_lidxs, feat_params, script_reg = get_feature_info(tt)
    if not sorted_ok:
        errs.append(f"{name}: GSUB FeatureList is not alphabetically sorted")
    for tag in TARGET_TAGS:
        if tag not in feat_maps:
            errs.append(f"{name}: missing GSUB feature '{tag}'")
        if not script_reg.get(tag, False):
            errs.append(f"{name}: '{tag}' not registered across all GSUB ScriptRecords")

    # FeatureParams verification
    if "cv09" in feat_params:
        lbl, chars = feat_params["cv09"]
        if not lbl or "Heart" not in lbl:
            errs.append(f"{name}: cv09 UI label invalid ({lbl!r})")
        if chars != [0x0069, 0x006A]:
            errs.append(f"{name}: cv09 Character array {chars} != [0x0069, 0x006A]")
    if "cv10" in feat_params:
        lbl, chars = feat_params["cv10"]
        if not lbl or "Heart" not in lbl:
            errs.append(f"{name}: cv10 UI label invalid ({lbl!r})")
        if chars != [0x0021, 0x003F, 0x00A1, 0x00BF]:
            errs.append(f"{name}: cv10 Character array {chars} != [0x0021, 0x003F, 0x00A1, 0x00BF]")
    if "cv19" in feat_params:
        lbl, chars = feat_params["cv19"]
        if not lbl or "Dotless" not in lbl:
            errs.append(f"{name}: cv19 UI label invalid ({lbl!r})")
        if chars != [0x0021, 0x003F, 0x0069, 0x006A, 0x00A1, 0x00BF, 0x0131, 0x0237]:
            errs.append(f"{name}: cv19 Character array {chars} invalid")
    for tag, kw in (("ss07", "Heart"), ("ss08", "Blossom"), ("ss09", "Nuqta"), ("ss10", "Star"), ("ss11", "Droplet")):
        if tag in feat_params:
            lbl, _ = feat_params[tag]
            if not lbl or kw not in lbl:
                errs.append(f"{name}: {tag} UI label invalid ({lbl!r})")

    # Split-brain check on ss07
    expected_ss07 = {}
    expected_ss07.update(feat_maps.get("cv09", {}))
    expected_ss07.update(feat_maps.get("cv10", {}))
    if feat_maps.get("ss07", {}) != expected_ss07:
        errs.append(f"{name}: ss07 != (cv09 U cv10)")

    # ALL 8 feature lookups must sit strictly before min_liga
    if "liga" in feat_lidxs and feat_lidxs["liga"]:
        min_liga = min(feat_lidxs["liga"])
        for tag in TARGET_TAGS:
            if tag in feat_lidxs and feat_lidxs[tag]:
                if max(feat_lidxs[tag]) >= min_liga:
                    errs.append(f"{name}: {tag} lookup {feat_lidxs[tag]} not strictly before liga ({min_liga})")

    gdef_cls = tt["GDEF"].table.GlyphClassDef.classDefs if ("GDEF" in tt and tt["GDEF"].table.GlyphClassDef) else {}

    f_gn = cmap.get(0x0066)
    f_aw, f_upper_xmax = None, None
    if f_gn and f_gn in glyf:
        f_aw = hmtx[f_gn][0]
        fcs = extract_contours(glyf, f_gn)
        f_hi = [p[0] for c in fcs for p in c["pts"] if 540 <= p[1] <= 740]
        f_upper_xmax = max(f_hi) if f_hi else glyf[f_gn].xMax

    is_outline = "Outline" in name
    is_inline = "Inline" in name
    is_halftone = "Halftone" in name
    is_kintsugi = "Kintsugi" in name
    is_mono = "Mono" in name or any(k in name for k in ("Algo", "Emoji", "Genome"))
    is_math = name.startswith("PocketGull-Math.")

    # Standalone monochrome symbol coverage & Mono 600 UPM / Math AxisHeight=260 checks
    for cp in STANDALONE_CPS:
        sgn = cmap.get(cp)
        if not sgn or sgn not in glyf:
            errs.append(f"{name}: missing standalone symbol U+{cp:04X} in cmap")
            continue
        saw, _ = hmtx[sgn]
        if is_mono and saw != 600:
            errs.append(f"{name}: standalone U+{cp:04X} ({sgn}) aw={saw} != 600 in Mono")
        sg = glyf[sgn]
        if is_math and cp in (0x2724, 0x25C6, 0x2726, 0x25CF, 0x1F4A7):
            y_ctr = (sg.yMin + sg.yMax) / 2.0
            if abs(y_ctr - 260.0) > 6.0:
                errs.append(f"{name}: Math U+{cp:04X} ({sgn}) y_ctr={y_ctr:.1f} not centered on AxisHeight=260")

    # PocketGull-Math special checks: U+1D6A4 & U+1D6A5 + sorted MATH coverage
    if is_math and not is_subset:
        for cp, expected_gn in ((0x1D6A4, "u1D6A4"), (0x1D6A5, "u1D6A5")):
            mgn = cmap.get(cp)
            if mgn != expected_gn or mgn not in glyf:
                errs.append(f"{name}: missing Math italic dotless U+{cp:05X} -> {expected_gn}")
        if "MATH" in tt and tt["MATH"].table.MathGlyphInfo:
            gi = tt["MATH"].table.MathGlyphInfo
            if gi.MathItalicsCorrectionInfo and gi.MathItalicsCorrectionInfo.Coverage:
                ic_glyphs = list(gi.MathItalicsCorrectionInfo.Coverage.glyphs)
                ic_gids = [gid_map[g] for g in ic_glyphs]
                if ic_gids != sorted(ic_gids):
                    errs.append(f"{name}: MATH ItalicsCorrection Coverage not sorted by GlyphID")
                for req_g in ("u1D6A4", "u1D6A5"):
                    if req_g not in ic_glyphs:
                        errs.append(f"{name}: MATH ItalicsCorrection missing {req_g}")
            if gi.MathTopAccentAttachment and gi.MathTopAccentAttachment.TopAccentCoverage:
                ta_glyphs = list(gi.MathTopAccentAttachment.TopAccentCoverage.glyphs)
                ta_gids = [gid_map[g] for g in ta_glyphs]
                if ta_gids != sorted(ta_gids):
                    errs.append(f"{name}: MATH TopAccentAttachment Coverage not sorted by GlyphID")
                for req_g in ("u1D6A4", "u1D6A5"):
                    if req_g not in ta_glyphs:
                        errs.append(f"{name}: MATH TopAccentAttachment missing {req_g}")

    for cp, canon, dot_pos, kind in EXPECTED_CHARS:
        bgn = cmap.get(cp)
        if not bgn:
            errs.append(f"{name}: missing base cmap for U+{cp:04X}")
            continue
        baw, _ = hmtx[bgn]
        bcs = extract_contours(glyf, bgn)

        # Verify cv19 dotless stem glyph
        dl_gn = feat_maps.get("cv19", {}).get(bgn)
        if not dl_gn or dl_gn not in glyf:
            errs.append(f"{name}: cv19 missing mapping for {bgn}")
        else:
            if gdef_cls.get(dl_gn) != 1:
                errs.append(f"{name}: {dl_gn} missing GDEF class 1")
            dl_aw, dl_lsb = hmtx[dl_gn]
            dl_g = glyf[dl_gn]
            if dl_aw != baw:
                errs.append(f"{name}: {dl_gn} advance width {dl_aw} != base {baw}")
            if dl_lsb != dl_g.xMin:
                errs.append(f"{name}: {dl_gn} lsb {dl_lsb} != xMin {dl_g.xMin}")
            if hasattr(dl_g, "program") and len(dl_g.program.getBytecode()) != 0:
                errs.append(f"{name}: {dl_gn} has non-empty bytecode")
            if loca is not None:
                gid = gid_map[dl_gn]
                if loca[gid] % 2 != 0 or loca[gid + 1] % 2 != 0:
                    errs.append(f"{name}: {dl_gn} has odd loca offset")
            dl_cs = extract_contours(glyf, dl_gn)
            if not dl_cs:
                errs.append(f"{name}: {dl_gn} has no contours")
            elif not is_outline and not is_inline and not is_halftone and not (is_kintsugi and canon in ("i", "j")):
                if len(dl_cs) != 1:
                    errs.append(f"{name}: {dl_gn} expected 1 stem contour, got {len(dl_cs)}")
            if canon == "i" and 0x0131 in cmap and feat_maps.get("cv19", {}).get(cmap[0x0131]) != dl_gn:
                errs.append(f"{name}: cv19 does not map dotlessi -> {dl_gn}")
            if canon == "j" and 0x0237 in cmap and feat_maps.get("cv19", {}).get(cmap[0x0237]) != dl_gn:
                errs.append(f"{name}: cv19 does not map dotlessj -> {dl_gn}")

        # Verify all 5 variety shapes (heart, blossom, nuqta, star, droplet)
        for vkey, vfeat, (min_r, max_r) in VARIETY_FEATURE_MAP:
            feat_key = ("cv09" if kind == "letter" else "cv10") if vkey == "heart" else vfeat
            tgn = feat_maps.get(feat_key, {}).get(bgn)
            if not tgn or tgn not in glyf:
                errs.append(f"{name}: {feat_key} missing mapping for {bgn}")
                continue

            if gdef_cls.get(tgn) != 1:
                errs.append(f"{name}: {tgn} missing GDEF class 1 (got {gdef_cls.get(tgn)})")

            taw, tlsb = hmtx[tgn]
            tg = glyf[tgn]
            if baw != taw:
                errs.append(f"{name}: {tgn} advance width {taw} != base {baw}")
            if tlsb != tg.xMin:
                errs.append(f"{name}: {tgn} lsb {tlsb} != xMin {tg.xMin}")
            if hasattr(tg, "program") and len(tg.program.getBytecode()) != 0:
                errs.append(f"{name}: {tgn} has non-empty glyph bytecode")

            if loca is not None:
                gid = gid_map[tgn]
                if loca[gid] % 2 != 0 or loca[gid + 1] % 2 != 0:
                    errs.append(f"{name}: {tgn} gid={gid} has odd loca offset")

            tcs = extract_contours(glyf, tgn)
            if not tcs:
                errs.append(f"{name}: {tgn} has no contours")
                continue

            for c in tcs:
                if c["dups"] > 0:
                    errs.append(f"{name}: {tgn} contour {c['ci']} has {c['dups']} duplicate nodes")
                if c["bit7"] > 0:
                    errs.append(f"{name}: {tgn} contour {c['ci']} has {c['bit7']} bit-7 flags")

            if is_outline:
                if len(tcs) < 3 or len(tcs) > 4:
                    errs.append(f"{name}: Outline {tgn} unexpected contour count {len(tcs)}")
                    continue
                stem_cs = tcs[:2]
                hrt_cs = tcs[2:]
                hrt_outer = max(hrt_cs, key=lambda c: c["w"])
                if hrt_outer["area"] >= 0:
                    errs.append(f"{name}: {tgn} Outline outer tittle winding invalid")
                if len(hrt_cs) == 2:
                    hrt_inner = min(hrt_cs, key=lambda c: c["w"])
                    if hrt_inner["area"] <= 0:
                        errs.append(f"{name}: {tgn} Outline inner tittle winding invalid")
                if canon in ("i", "j"):
                    if bcs[1]["pts"] != stem_cs[1]["pts"]:
                        errs.append(f"{name}: Outline {tgn} inner stem c1 mismatch")
                    if stem_cs[0]["ymax"] > 570:
                        errs.append(f"{name}: Outline {tgn} stem still fused (ymax={stem_cs[0]['ymax']})")
                else:
                    if bcs[0]["pts"] != stem_cs[0]["pts"] or bcs[1]["pts"] != stem_cs[1]["pts"]:
                        errs.append(f"{name}: Outline {tgn} stem mismatch")
                dot_c = bcs[2]
                dot_cx = (dot_c["xmin"] + dot_c["xmax"]) / 2.0
            elif is_inline:
                if len(tcs) < 4:
                    errs.append(f"{name}: Inline {tgn} unexpected contour count {len(tcs)}")
                    continue
                stem_cs = tcs[:3]
                hrt_cs = tcs[3:]
                for k in range(3):
                    if bcs[k]["pts"] != stem_cs[k]["pts"]:
                        errs.append(f"{name}: Inline {tgn} stem contour {k} mismatch")
                hrt_outer = max(hrt_cs, key=lambda c: c["w"])
                if hrt_outer["area"] >= 0:
                    errs.append(f"{name}: Inline {tgn} outer tittle winding CCW")
                dot_cx = (min(c["xmin"] for c in bcs[3:]) + max(c["xmax"] for c in bcs[3:])) / 2.0
            elif is_kintsugi and canon in ("i", "j"):
                b_stem = [c for c in bcs if c["ymax"] <= 560]
                b_dot = [c for c in bcs if c["ymin"] >= 585]
                stem_cs = tcs[: len(b_stem)]
                hrt_cs = tcs[len(b_stem) :]
                if len(hrt_cs) < 1:
                    errs.append(f"{name}: Kintsugi {tgn} missing tittle contours")
                    continue
                for bs, ts in zip(b_stem, stem_cs):
                    if bs["pts"] != ts["pts"]:
                        errs.append(f"{name}: Kintsugi {tgn} stem mismatch")
                hrt_outer = max(hrt_cs, key=lambda c: c["w"])
                if hrt_outer["area"] >= 0:
                    errs.append(f"{name}: Kintsugi {tgn} outer tittle winding CCW")
                dot_cx = (min(c["xmin"] for c in b_dot) + max(c["xmax"] for c in b_dot)) / 2.0
            elif is_halftone:
                if canon in ("i", "j"):
                    b_stem = [c for c in bcs if c["ymax"] <= 555]
                    b_dot = [c for c in bcs if c["ymin"] >= 580]
                elif canon in ("exclam", "question"):
                    b_dot = [c for c in bcs if c["ymax"] <= 165]
                    b_stem = [c for c in bcs if c["ymin"] >= 210]
                else:
                    b_stem = [c for c in bcs if c["ymax"] <= 320]
                    b_dot = [c for c in bcs if c["ymin"] >= 370]
                stem_cs = tcs[:-1]
                hrt_outer = tcs[-1]
                if len(stem_cs) != len(b_stem) or any(bs["pts"] != ts["pts"] for bs, ts in zip(b_stem, stem_cs)):
                    errs.append(f"{name}: Halftone {tgn} stem dots mismatch ({len(stem_cs)} vs {len(b_stem)})")
                if hrt_outer["area"] >= 0:
                    errs.append(f"{name}: Halftone {tgn} tittle winding CCW")
                dot_cx = (min(c["xmin"] for c in b_dot) + max(c["xmax"] for c in b_dot)) / 2.0
            else:
                if len(bcs) != 2 or len(tcs) != 2:
                    errs.append(f"{name}: {tgn} expected 2 contours (base={len(bcs)}, tgt={len(tcs)})")
                    continue
                if dot_pos == "top":
                    b_stem, b_dot = min(bcs, key=lambda c: c["ymin"]), max(bcs, key=lambda c: c["ymax"])
                    t_stem, hrt_outer = min(tcs, key=lambda c: c["ymin"]), max(tcs, key=lambda c: c["ymax"])
                else:
                    b_dot, b_stem = min(bcs, key=lambda c: c["ymin"]), max(bcs, key=lambda c: c["ymax"])
                    hrt_outer, t_stem = min(tcs, key=lambda c: c["ymin"]), max(tcs, key=lambda c: c["ymax"])
                stem_cs = [t_stem]
                if b_stem["pts"] != t_stem["pts"]:
                    errs.append(f"{name}: {tgn} stem not bit-identical to {bgn}")
                if hrt_outer["area"] >= 0:
                    errs.append(f"{name}: {tgn} tittle winding is CCW (area={hrt_outer['area']:.0f})")
                dot_cx = (b_dot["xmin"] + b_dot["xmax"]) / 2.0

            stem_ymin = min(c["ymin"] for c in stem_cs)
            stem_ymax = max(c["ymax"] for c in stem_cs)
            gap = (hrt_outer["ymin"] - stem_ymax) if dot_pos == "top" else (stem_ymin - hrt_outer["ymax"])
            min_req_gap = 24 if is_outline else (48 if dot_pos == "top" else 44)
            if gap < min_req_gap:
                errs.append(f"{name}: {tgn} gap {gap} < {min_req_gap}")

            hrt_cx = (hrt_outer["xmin"] + hrt_outer["xmax"]) / 2.0
            if abs(hrt_cx - dot_cx) > 3.5:
                errs.append(f"{name}: {tgn} horizontal center drift {hrt_cx:.1f} vs dot {dot_cx:.1f}")

            ratio = hrt_outer["w"] / max(1, hrt_outer["h"])
            if not is_outline and not (min_r <= ratio <= max_r):
                errs.append(f"{name}: {tgn} aspect ratio {ratio:.2f} out of [{min_r}, {max_r}]")

            if canon == "i" and f_aw is not None and f_upper_xmax is not None and not is_mono and not is_subset:
                fi_gap = (f_aw + hrt_outer["xmin"]) - f_upper_xmax
                req_fi = -14 if is_outline else (1 if abs(italic_angle) > 0.1 else 6)
                if fi_gap < req_fi:
                    errs.append(f"{name}: {tgn} fi clearance {fi_gap} < {req_fi}")

    tt.close()
    return errs


def audit_vf_extremes() -> list[str]:
    errs: list[str] = []
    vf_configs = [
        ("PocketGull-VF.ttf", [
            {"wght": -1.0}, {"wght": 1.0}, {"wdth": -1.0}, {"slnt": -1.0},
            {"opsz": -1.0}, {"HLNG": 1.0}, {"CHIS": 1.0}, {"BOUM": 1.0}, {"SOFT": 1.0},
        ]),
        ("PocketGull-Serif-VF.ttf", [{"wght": 1.0}]),
        ("PocketGullSerif[wght].ttf", [{"wght": 1.0}]),
    ]
    for vfn, locs in vf_configs:
        tt = TTFont(str(TTF_DIR / vfn))
        glyf = tt["glyf"]
        hmtx = tt["hmtx"]
        cmap = tt.getBestCmap() or {}
        _, feat_maps, _, _, _ = get_feature_info(tt)
        adv_map = tt["HVAR"].table.AdvWidthMap.mapping if ("HVAR" in tt and tt["HVAR"].table.AdvWidthMap) else {}

        for cp, canon, dot_pos, kind in EXPECTED_CHARS:
            bgn = cmap[cp]
            b_tvs = tt["gvar"].variations.get(bgn, [])
            bg = glyf[bgn]
            bc, be, _ = bg.getCoordinates(glyf)
            b_all = list(bc) + glyf._getPhantomPoints(bgn, hmtx, None)

            # Check dotless stem VF variation
            dl_gn = feat_maps["cv19"][bgn]
            dl_tvs = tt["gvar"].variations.get(dl_gn, [])
            if len(dl_tvs) != len(b_tvs) or len(dl_tvs) == 0:
                errs.append(f"{vfn}: {dl_gn} gvar count {len(dl_tvs)} != base {len(b_tvs)}")
            if adv_map and adv_map.get(dl_gn) != adv_map.get(bgn):
                errs.append(f"{vfn}: {dl_gn} HVAR mismatch")

            # Check all 5 varieties
            for vkey, vfeat, _ in VARIETY_FEATURE_MAP:
                tgn = feat_maps[("cv09" if kind == "letter" else "cv10") if vkey == "heart" else vfeat][bgn]
                t_tvs = tt["gvar"].variations.get(tgn, [])
                if len(t_tvs) != len(b_tvs) or len(t_tvs) == 0:
                    errs.append(f"{vfn}: {tgn} gvar count {len(t_tvs)} != base {len(b_tvs)}")
                    continue
                if adv_map and adv_map.get(tgn) != adv_map.get(bgn):
                    errs.append(f"{vfn}: {tgn} HVAR AdvWidthMap {adv_map.get(tgn)} != base {adv_map.get(bgn)}")

                tg = glyf[tgn]
                tc, te, _ = tg.getCoordinates(glyf)
                t_all = list(tc) + glyf._getPhantomPoints(tgn, hmtx, None)

                for loc in locs:
                    b_pos = list(b_all)
                    t_pos = list(t_all)
                    for btv, ttv in zip(b_tvs, t_tvs):
                        scalar = 1.0
                        matched = True
                        for ax, (mn, pk, mx) in btv.axes.items():
                            v = loc.get(ax, 0.0)
                            if v == 0.0 or v * pk <= 0:
                                matched = False
                                break
                            scalar *= min(1.0, abs(v))
                        if not matched:
                            continue
                        bd = iup_delta(btv.coordinates, b_all, list(be))
                        td = iup_delta(ttv.coordinates, t_all, list(te))
                        b_pos = [(p[0] + d[0] * scalar, p[1] + d[1] * scalar) for p, d in zip(b_pos, bd)]
                        t_pos = [(p[0] + d[0] * scalar, p[1] + d[1] * scalar) for p, d in zip(t_pos, td)]

                    b_aw = round(b_pos[-3][0] - b_pos[-4][0])
                    t_aw = round(t_pos[-3][0] - t_pos[-4][0])
                    if b_aw != t_aw:
                        errs.append(f"{vfn} @ {loc} {tgn}: aw {t_aw} != base {b_aw}")

                    t_c0 = t_pos[: te[0] + 1]
                    t_c1 = t_pos[te[0] + 1 : te[1] + 1]
                    if shoelace_area(t_c1) >= 0:
                        errs.append(f"{vfn} @ {loc} {tgn}: contour CCW")
                    gap = (min(p[1] for p in t_c1) - max(p[1] for p in t_c0)) if dot_pos == "top" else (min(p[1] for p in t_c0) - max(p[1] for p in t_c1))
                    if gap < 40.0:
                        errs.append(f"{vfn} @ {loc} {tgn}: gap {gap:.1f} < 40.0")
        tt.close()
    return errs


def audit_harfbuzz_shaping() -> list[str]:
    errs: list[str] = []
    sample = "clinical! ¿listo? ¡sí! fi ii ij"
    test_fonts = [
        "PocketGull-Regular.ttf",
        "PocketGull-Bold.ttf",
        "PocketGull-Italic.ttf",
        "PocketGull-BoldItalic.ttf",
        "PocketGull-CondensedBold.ttf",
        "PocketGullMono-Regular.ttf",
        "PocketGullMono-Italic.ttf",
        "PocketGull-Math.ttf",
        "PocketGull-Genome.ttf",
        "PocketGull-VF.ttf",
        "PocketGull-Serif-VF.ttf",
        "PocketGull-Halftone.ttf",
        "PocketGull-Inline.ttf",
        "PocketGull-Outline.ttf",
        "PocketGull-Kintsugi.ttf",
    ]
    for fn in test_fonts:
        p = TTF_DIR / fn
        tt = TTFont(str(p))
        cmap = tt.getBestCmap() or {}
        gorder = tt.getGlyphOrder()
        _, feat_maps, _, _, _ = get_feature_info(tt)
        tt.close()

        blob = hb.Blob.from_file_path(str(p))
        face = hb.Face(blob)
        hb_font = hb.Font(face)

        def shape_names(feats: dict[str, int], text: str = sample) -> list[str]:
            buf = hb.Buffer()
            buf.add_str(text)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf, feats)
            return [gorder[info.codepoint] for info in buf.glyph_infos]

        base_names = shape_names({})
        cv09_names = shape_names({"cv09": 1})
        cv10_names = shape_names({"cv10": 1})
        cv19_names = shape_names({"cv19": 1}, "ıȷi j ! ? ¡ ¿")
        ss07_names = shape_names({"ss07": 1})
        both_names = shape_names({"cv09": 1, "ss07": 1})

        i_heart = feat_maps["cv09"][cmap[0x0069]]
        j_heart = feat_maps["cv09"][cmap[0x006A]]
        ex_heart = feat_maps["cv10"][cmap[0x0021]]
        q_heart = feat_maps["cv10"][cmap[0x003F]]
        exd_heart = feat_maps["cv10"][cmap[0x00A1]]
        qd_heart = feat_maps["cv10"][cmap[0x00BF]]

        if cv09_names.count(i_heart) < 6 or cv09_names.count(j_heart) < 1:
            errs.append(f"HB {fn} cv09 missing letter substitutions")
        if ex_heart in cv09_names or q_heart in cv09_names:
            errs.append(f"HB {fn} cv09 unexpectedly touched punctuation")

        for expected_p in (ex_heart, q_heart, exd_heart, qd_heart):
            if expected_p not in cv10_names:
                errs.append(f"HB {fn} cv10 missing {expected_p}")
        if i_heart in cv10_names or j_heart in cv10_names:
            errs.append(f"HB {fn} cv10 unexpectedly touched letters")

        for expected_all in (i_heart, j_heart, ex_heart, q_heart, exd_heart, qd_heart):
            if expected_all not in ss07_names:
                errs.append(f"HB {fn} ss07 missing {expected_all}")
        if ss07_names != both_names:
            errs.append(f"HB {fn} ss07 != (cv09+ss07)")
        if "uniFB01" in ss07_names or "uniFB01" in cv09_names:
            errs.append(f"HB {fn} liga uniFB01 shadowed heart tittle in 'fi'")
        if base_names.count(i_heart) > 0 or base_names.count(ex_heart) > 0:
            errs.append(f"HB {fn} default shaping leaked heart glyphs")

        # Verify cv19 dotless stems on ı, ȷ, i, j, !, ?, ¡, ¿
        for expected_dl in ("i.dotless", "j.dotless", "exclam.dotless", "question.dotless", "exclamdown.dotless", "questiondown.dotless"):
            if expected_dl not in cv19_names:
                errs.append(f"HB {fn} cv19 missing {expected_dl}: {cv19_names}")
        if cv19_names.count("i.dotless") < 2 or cv19_names.count("j.dotless") < 2:
            errs.append(f"HB {fn} cv19 did not map both dotlessi/i and dotlessj/j: {cv19_names}")

        # Verify ss08 (blossom), ss09 (nuqta), ss10 (star), ss11 (droplet) all bypass fi liga and substitute all 6 chars
        for tag in ("ss08", "ss09", "ss10", "ss11"):
            shaped = shape_names({tag: 1})
            if "uniFB01" in shaped:
                errs.append(f"HB {fn} {tag} shadowed by liga uniFB01 in 'fi'")
            for cp, _, _, _ in EXPECTED_CHARS:
                tgt = feat_maps[tag][cmap[cp]]
                if tgt not in shaped:
                    errs.append(f"HB {fn} {tag} missing {tgt}")

    return errs


def main() -> int:
    all_errs: list[str] = []

    ttfs = [p for p in sorted(TTF_DIR.glob("*.ttf")) if p.name not in SKIP_FONTS]
    print(f"1. Auditing {len(ttfs)} canonical TTFs...")
    for p in ttfs:
        all_errs.extend(audit_font_binary(p, is_subset=False))

    w2s = [WOFF2_DIR / f"{p.stem}.woff2" for p in ttfs]
    print(f"2. Auditing {len(w2s)} canonical WOFF2s...")
    for p in w2s:
        if not p.exists():
            all_errs.append(f"Missing WOFF2: {p}")
        else:
            all_errs.extend(audit_font_binary(p, is_subset=False))

    cores = sorted(WOFF2_DIR.glob("*-Core.woff2"))
    print(f"3. Auditing {len(cores)} Core WOFF2 subsets...")
    for p in cores:
        all_errs.extend(audit_font_binary(p, is_subset=True))

    mirrors = (
        sorted(ROOT_DIR.glob("PocketGull*.ttf"))
        + sorted(ROOT_DIR.glob("PocketGull*.woff2"))
        + sorted((ROOT_DIR / "ofl").rglob("*.ttf"))
        + sorted((ROOT_DIR / "apache").rglob("*.ttf"))
        + sorted((ROOT_DIR / "distribution" / "python" / "pocketgull_math" / "fonts").glob("*.ttf"))
        + sorted((ROOT_DIR / "distribution" / "r" / "inst" / "fonts").glob("*.ttf"))
        + sorted((ROOT_DIR / "distribution" / "upcycled").glob("*.ttf"))
        + sorted((ROOT_DIR / "distribution" / "upcycled").glob("*.woff2"))
    )
    print(f"4. Auditing {len(mirrors)} root/ofl/apache/distribution mirror binaries...")
    for m in mirrors:
        if m.name in SKIP_FONTS or m.stem + ".ttf" in SKIP_FONTS:
            continue
        canon = (TTF_DIR if m.suffix == ".ttf" else WOFF2_DIR) / m.name
        if not canon.exists():
            all_errs.append(f"Mirror {m.relative_to(ROOT_DIR)} has no canonical counterpart")
        elif m.read_bytes() != canon.read_bytes():
            all_errs.append(f"Stale mirror bytes: {m.relative_to(ROOT_DIR)} != {canon.relative_to(ROOT_DIR)}")

    print("5. Auditing Variable Font multi-axis gvar & HVAR extremes (all 5 varieties + cv19)...")
    all_errs.extend(audit_vf_extremes())

    print("6. Auditing live HarfBuzz shaping across 15 representative cuts (cv09/10/19 + ss07..ss11)...")
    all_errs.extend(audit_harfbuzz_shaping())

    if all_errs:
        print(f"\n[FAIL] {len(all_errs)} audit error(s):")
        for e in all_errs[:60]:
            print(f"  - {e}")
        return 1

    print("\n[PASS] All 38 TTFs, 38 WOFF2s, 4 Core subsets, mirrors, Math MATH table, VF extremes & HarfBuzz shaping passed 100%!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
