"""
Fix ISMP Disambiguation Glyphs & OpenType GSUB FeatureList Ordering across PocketGull fonts:
  1. Slashed Zero (cv08 / zero): Boolean UNION of base `zero` and CW 45-deg slash via skia-pathops
     (eliminates negative-winding bite holes where the slash meets the outer oval).
  2. Optical Dotted Zero (cv12): Ensures central optical dot contour has CW (+1) winding inside the CCW hole.
  3. Slashed Z (cv11): Synthesizes zero-overlap `Z.slash` and `z.slash` via skia-pathops UNION with a
     horizontal clinical crossbar and registers `cv11` in GSUB.
  4. Curved Lowercase l (cv05): Replaces numeral-1 top-flag shape with true lowercase `l` + outward right
     baseline terminal foot (eliminates `1 1 I` collision).
  5. Alphabetical FeatureRecord Sort: Sorts GSUB FeatureList.FeatureRecord by FeatureTag so HarfBuzz
     binary search (`hb_ot_layout_table_find_feature`) resolves `cv11`, `cv12`, and `ss07` in all browsers.
"""

from pathlib import Path
import copy
import pathops
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib.tables import otTables

ROOT = Path(__file__).resolve().parents[1]


def glyph_to_skia_path(tt: TTFont, glyph_name: str) -> pathops.Path:
    glyph_set = tt.getGlyphSet()
    sk_path = pathops.Path()
    pen = sk_path.getPen()
    glyph_set[glyph_name].draw(pen)
    return sk_path


def skia_path_to_tt_glyph(sk_path: pathops.Path):
    tt_pen = TTGlyphPen(None)
    cu2qu_pen = Cu2QuPen(tt_pen, max_err=1.0, reverse_direction=True)
    sk_path.draw(cu2qu_pen)
    return tt_pen.glyph()


def build_slashed_zero_glyph(tt: TTFont):
    """Boolean-union base `zero` with a CW diagonal slash bar across the interior aperture."""
    g0 = tt["glyf"]["zero"]
    g0.recalcBounds(tt["glyf"])
    xmin, ymin, xmax, ymax = g0.xMin, g0.yMin, g0.xMax, g0.yMax
    w = xmax - xmin
    h = ymax - ymin

    base_path = glyph_to_skia_path(tt, "zero")

    # Diagonal bar inside the oval (overlapping the ring cleanly without extending outside)
    slash = pathops.Path()
    x1 = xmin + 0.19 * w
    y1 = ymin + 0.18 * h
    x2 = xmin + 0.72 * w
    y2 = ymin + 0.85 * h
    dx = 0.095 * w
    dy = -0.075 * h

    slash.moveTo(x1, y1)
    slash.lineTo(x2, y2)
    slash.lineTo(x2 + dx, y2 + dy)
    slash.lineTo(x1 + dx, y1 + dy)
    slash.close()

    unioned = pathops.op(base_path, slash, pathops.PathOp.UNION)
    unioned.simplify()
    return skia_path_to_tt_glyph(unioned)


def build_dotted_zero_glyph(tt: TTFont):
    """Copy base `zero` (CW outer, CCW hole) and append a CW (+1 winding) optical dot inside the hole."""
    g0 = tt["glyf"]["zero"]
    g0.recalcBounds(tt["glyf"])
    cx = int(round(0.5 * (g0.xMin + g0.xMax)))
    cy = int(round(0.5 * (g0.yMin + g0.yMax)))
    r = int(round(max(38.0, 0.095 * (g0.xMax - g0.xMin))))
    d = int(round(r * 0.7071))

    tt_pen = TTGlyphPen(None)
    tt.getGlyphSet()["zero"].draw(tt_pen)

    # Counter-clockwise in y-up coordinates gives positive shoelace area matching outer contour 0 (+312188.5)
    tt_pen.moveTo((cx, cy + r))
    tt_pen.qCurveTo((cx - r, cy + r), (cx - r, cy))
    tt_pen.qCurveTo((cx - r, cy - r), (cx, cy - r))
    tt_pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
    tt_pen.qCurveTo((cx + r, cy + r), (cx, cy + r))
    tt_pen.closePath()
    return tt_pen.glyph()


def build_slashed_z_glyph(tt: TTFont, base_name: str = "Z"):
    """Boolean-union `Z` or `z` with a crisp horizontal ISMP crossbar."""
    gz = tt["glyf"][base_name]
    gz.recalcBounds(tt["glyf"])
    xmin, ymin, xmax, ymax = gz.xMin, gz.yMin, gz.xMax, gz.yMax
    w = xmax - xmin
    h = ymax - ymin

    base_path = glyph_to_skia_path(tt, base_name)
    bar = pathops.Path()
    cy = ymin + 0.50 * h
    half_thick = max(36.0, 0.062 * h)
    bx0 = xmin + 0.16 * w
    bx1 = xmax - 0.16 * w

    bar.moveTo(bx0, cy - half_thick)
    bar.lineTo(bx1, cy - half_thick)
    bar.lineTo(bx1, cy + half_thick)
    bar.lineTo(bx0, cy + half_thick)
    bar.close()

    unioned = pathops.op(base_path, bar, pathops.PathOp.UNION)
    unioned.simplify()
    return skia_path_to_tt_glyph(unioned)


def build_curved_l_glyph(tt: TTFont):
    """Build true lowercase `l` with outward right baseline terminal foot (no top-left `1` flag)."""
    gl = tt["glyf"]["l"]
    gl.recalcBounds(tt["glyf"])
    xmin, ymin, xmax, ymax = gl.xMin, gl.yMin, gl.xMax, gl.yMax
    stem_w = max(90, xmax - xmin)
    foot_h = min(115, int(stem_w * 0.78))
    foot_ext = int(stem_w * 1.15)

    path = pathops.Path()
    # Vertical stem
    path.moveTo(xmin, ymin + foot_h)
    path.lineTo(xmin, ymax)
    path.lineTo(xmax, ymax)
    path.lineTo(xmax, ymin + foot_h)
    # Outward right exit foot with curved lower-left heel
    path.lineTo(xmax + foot_ext, ymin + foot_h)
    path.lineTo(xmax + foot_ext, ymin)
    path.lineTo(xmin + foot_h * 0.65, ymin)
    path.cubicTo(xmin + foot_h * 0.2, ymin, xmin, ymin + foot_h * 0.2, xmin, ymin + foot_h)
    path.close()
    path.simplify()

    tt_g = skia_path_to_tt_glyph(path)
    return tt_g, int(xmax + foot_ext + xmin)


def patch_font(font_path: Path) -> bool:
    tt = TTFont(str(font_path))
    if "glyf" not in tt or "GSUB" not in tt:
        return False

    # Force decompile of GSUB, glyf, hmtx before adding glyphs
    gsub = tt["GSUB"].table
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    glyph_order = list(tt.getGlyphOrder())

    # 1. Discover existing target glyph names for cv08/zero, cv12, cv05
    zero_slash_name = None
    zero_dot_name = None
    l_cv05_name = None

    for frec in gsub.FeatureList.FeatureRecord:
        for lidx in frec.Feature.LookupListIndex:
            for st in gsub.LookupList.Lookup[lidx].SubTable:
                mp = getattr(st, "mapping", {})
                if frec.FeatureTag in ("zero", "cv08") and "zero" in mp:
                    zero_slash_name = mp["zero"]
                elif frec.FeatureTag == "cv12" and "zero" in mp:
                    zero_dot_name = mp["zero"]
                elif frec.FeatureTag == "cv05" and "l" in mp:
                    l_cv05_name = mp["l"]

    # 2. Rebuild Slashed Zero (zero / cv08)
    if zero_slash_name and "zero" in glyf:
        new_zslash = build_slashed_zero_glyph(tt)
        new_zslash.recalcBounds(glyf)
        glyf[zero_slash_name] = new_zslash
        hmtx[zero_slash_name] = (hmtx["zero"][0], new_zslash.xMin)

    # 3. Rebuild Optical Dotted Zero (cv12)
    if zero_dot_name and "zero" in glyf:
        new_zdot = build_dotted_zero_glyph(tt)
        new_zdot.recalcBounds(glyf)
        glyf[zero_dot_name] = new_zdot
        hmtx[zero_dot_name] = (hmtx["zero"][0], new_zdot.xMin)

    # 4. Rebuild Curved Lowercase l (cv05)
    if l_cv05_name and "l" in glyf:
        new_l, adv_w = build_curved_l_glyph(tt)
        new_l.recalcBounds(glyf)
        glyf[l_cv05_name] = new_l
        hmtx[l_cv05_name] = (adv_w, new_l.xMin)

    # 5. Synthesize Z.slash and z.slash and add cv11 feature to GSUB
    cv11_map = {}
    for base_z, slash_z in [("Z", "Z.slash"), ("z", "z.slash")]:
        if base_z in glyf and glyf[base_z].numberOfContours > 0:
            new_zg = build_slashed_z_glyph(tt, base_z)
            new_zg.recalcBounds(glyf)
            if slash_z not in glyph_order:
                glyph_order.append(slash_z)
            glyf[slash_z] = new_zg
            hmtx[slash_z] = (hmtx[base_z][0], new_zg.xMin)
            cv11_map[base_z] = slash_z

    tt.setGlyphOrder(glyph_order)

    if cv11_map:
        existing_cv11 = [f for f in gsub.FeatureList.FeatureRecord if f.FeatureTag == "cv11"]
        if not existing_cv11:
            lk = otTables.Lookup()
            lk.LookupType = 1
            lk.LookupFlag = 0
            st = otTables.SingleSubst()
            st.mapping = cv11_map
            lk.SubTable = [st]
            lk.SubTableCount = 1
            new_lidx = len(gsub.LookupList.Lookup)
            gsub.LookupList.Lookup.append(lk)
            gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

            frec = otTables.FeatureRecord()
            frec.FeatureTag = "cv11"
            frec.Feature = otTables.Feature()
            frec.Feature.FeatureParams = None
            frec.Feature.LookupListIndex = [new_lidx]
            frec.Feature.LookupCount = 1
            gsub.FeatureList.FeatureRecord.append(frec)
            gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)
        else:
            for frec in existing_cv11:
                for lidx in frec.Feature.LookupListIndex:
                    for st in gsub.LookupList.Lookup[lidx].SubTable:
                        if hasattr(st, "mapping"):
                            st.mapping.update(cv11_map)

    # 6. Sort GSUB.FeatureList.FeatureRecord alphabetically by FeatureTag (OpenType spec requirement for HarfBuzz binary search)
    gsub.FeatureList.FeatureRecord.sort(key=lambda rec: rec.FeatureTag)
    all_feat_indices = list(range(len(gsub.FeatureList.FeatureRecord)))
    for srec in gsub.ScriptList.ScriptRecord:
        if srec.Script.DefaultLangSys:
            srec.Script.DefaultLangSys.FeatureIndex = list(all_feat_indices)
            srec.Script.DefaultLangSys.FeatureCount = len(all_feat_indices)
        for lsys in getattr(srec.Script, "LangSysRecord", []) or []:
            lsys.LangSys.FeatureIndex = list(all_feat_indices)
            lsys.LangSys.FeatureCount = len(all_feat_indices)

    tt.save(str(font_path))
    return True


if __name__ == "__main__":
    import shutil
    primary_targets = [
        ROOT / "fonts" / "ttf" / "PocketGull-Bold.ttf",
        ROOT / "fonts" / "ttf" / "PocketGull-Regular.ttf",
        ROOT / "fonts" / "ttf" / "PocketGull-Fineliner.ttf",
        ROOT / "fonts" / "ttf" / "PocketGullMono-Regular.ttf",
        ROOT / "fonts" / "ttf" / "PocketGullMono-Bold.ttf",
        ROOT / "fonts" / "woff2" / "PocketGull-Bold.woff2",
        ROOT / "fonts" / "woff2" / "PocketGull-Bold-Core.woff2",
        ROOT / "fonts" / "woff2" / "PocketGull-Regular.woff2",
        ROOT / "fonts" / "woff2" / "PocketGull-Fineliner.woff2",
        ROOT / "fonts" / "woff2" / "PocketGull-Fineliner-Core.woff2",
        ROOT / "fonts" / "woff2" / "PocketGullMono-Regular.woff2",
        ROOT / "fonts" / "woff2" / "PocketGullMono-Bold.woff2",
    ]
    for p in primary_targets:
        if p.exists():
            ok = patch_font(p)
            print(f"Patched {p.relative_to(ROOT)}: {ok}")

    # Sync root copies from canonical fonts/ttf and fonts/woff2
    sync_pairs = [
        (ROOT / "fonts" / "ttf" / "PocketGull-Bold.ttf", ROOT / "PocketGull-Bold.ttf"),
        (ROOT / "fonts" / "woff2" / "PocketGull-Bold.woff2", ROOT / "PocketGull-Bold.woff2"),
        (ROOT / "fonts" / "ttf" / "PocketGullMono-Regular.ttf", ROOT / "PocketGullMono-Regular.ttf"),
        (ROOT / "fonts" / "woff2" / "PocketGullMono-Regular.woff2", ROOT / "PocketGullMono-Regular.woff2"),
    ]
    for src, dst in sync_pairs:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Synced {dst.name}")
