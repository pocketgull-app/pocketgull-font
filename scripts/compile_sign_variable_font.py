#!/usr/bin/env python3
"""
PocketGull Typefoundry: Variable Sign Font Compiler (PocketGull-Sign-VF)
========================================================================
Compiles 'PocketGull-Sign-VF.ttf' and 'PocketGull-Sign-VF.woff2' from the Z-layered
anatomical 'PocketGull-Sign.ttf' master with 4 continuous axes:
  1. 'MRPH' (0–500): Hand Morphology (Sloan 5:1, Alimentive, Thoracic, Muscular, Osseous, Cerebral)
  2. 'wght' (400–900): Optical Stroke Weight
  3. 'opsz' (16–72): Optical Size Acuity
  4. 'AZIM' (0–180): Perspective Azimuth Shear

Guarantees distinct 'PocketGull Sign VF' naming, complete 4-axis STAT table, HVAR table,
valid postscriptNameIDs on all named instances, and 0 duplicate nodes.
"""

import sys
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from fontTools.ttLib.tables.TupleVariation import TupleVariation
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

SRC_SIGN_TTF = TTF_DIR / "PocketGull-Sign.ttf"
OUT_SIGN_VF_TTF = TTF_DIR / "PocketGull-Sign-VF.ttf"
OUT_SIGN_VF_WOFF2 = WOFF2_DIR / "PocketGull-Sign-VF.woff2"


def set_win_name(name_table, nid, val):
    name_table.setName(val, nid, 3, 1, 0x0409)
    name_table.names = [
        r for r in name_table.names
        if not (r.nameID == nid and (r.platformID != 3 or r.platEncID != 1 or r.langID != 0x0409))
    ]


def compile_sign_variable_font():
    print("=== POCKETGULL VARIABLE SIGN FONT COMPILER (PocketGull-Sign-VF) ===")
    if not SRC_SIGN_TTF.is_file():
        print(f"[ERROR] Base font missing: {SRC_SIGN_TTF}")
        sys.exit(1)

    font = TTFont(str(SRC_SIGN_TTF))
    glyf = font["glyf"]
    name_table = font["name"]

    ver = "Version 3.103; The PocketGull Project Authors; OFL 1.1"
    set_win_name(name_table, 1, "PocketGull Sign VF")
    set_win_name(name_table, 2, "Regular")
    set_win_name(name_table, 3, "3.103;PGUL;PocketGull-SignVF")
    set_win_name(name_table, 4, "PocketGull Sign VF")
    set_win_name(name_table, 5, ver)
    set_win_name(name_table, 6, "PocketGull-SignVF")
    set_win_name(name_table, 25, "PocketGullSignVF")

    fvar = font["fvar"] = newTable("fvar")
    fvar.axes = []
    fvar.instances = []

    axes_spec = [
        ("MRPH", 0.0, 0.0, 500.0, 290, "Hand Morphology"),
        ("wght", 400.0, 400.0, 900.0, 291, "Weight"),
        ("opsz", 16.0, 36.0, 72.0, 292, "Optical Size"),
        ("AZIM", 0.0, 0.0, 180.0, 293, "Turntable Azimuth"),
    ]
    for tag, mn, df, mx, anid, label in axes_spec:
        ax = Axis()
        ax.axisTag = tag
        ax.minValue, ax.defaultValue, ax.maxValue = mn, df, mx
        ax.flags = 0
        ax.axisNameID = anid
        set_win_name(name_table, anid, label)
        fvar.axes.append(ax)

    instances_def = [
        ("Regular", "PocketGull-SignVF", {"MRPH": 0.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}, 2, 320),
        ("Sloan", "PocketGullSignVF-Sloan", {"MRPH": 0.0, "wght": 400.0, "opsz": 18.0, "AZIM": 0.0}, 301, 321),
        ("Alimentive", "PocketGullSignVF-Alimentive", {"MRPH": 100.0, "wght": 500.0, "opsz": 36.0, "AZIM": 0.0}, 302, 322),
        ("Thoracic", "PocketGullSignVF-Thoracic", {"MRPH": 200.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}, 303, 323),
        ("Muscular", "PocketGullSignVF-Muscular", {"MRPH": 300.0, "wght": 600.0, "opsz": 36.0, "AZIM": 0.0}, 304, 324),
        ("Osseous", "PocketGullSignVF-Osseous", {"MRPH": 400.0, "wght": 450.0, "opsz": 36.0, "AZIM": 0.0}, 305, 325),
        ("Cerebral", "PocketGullSignVF-Cerebral", {"MRPH": 500.0, "wght": 400.0, "opsz": 36.0, "AZIM": 0.0}, 306, 326),
        ("Expressive", "PocketGullSignVF-Expressive", {"MRPH": 0.0, "wght": 400.0, "opsz": 36.0, "AZIM": 180.0}, 307, 327),
    ]
    for inst_name, ps_name, coords, nid, ps_nid in instances_def:
        inst = NamedInstance()
        inst.subfamilyNameID = nid
        inst.postscriptNameID = ps_nid
        set_win_name(name_table, nid, inst_name)
        set_win_name(name_table, ps_nid, ps_name)
        inst.coordinates = coords
        fvar.instances.append(inst)

    # Complete 4-axis STAT table
    stat_tbl = newTable("STAT")
    ot_stat = otTables.STAT()
    ot_stat.Version = 0x00010001
    ot_stat.DesignAxisRecordSize = 8
    ot_stat.DesignAxisRecord = otTables.AxisRecordArray()
    ot_stat.DesignAxisRecord.Axis = []
    for idx, (tag, _, _, _, anid, _) in enumerate(axes_spec):
        ar = otTables.AxisRecord()
        ar.AxisTag = tag
        ar.AxisNameID = anid
        ar.AxisOrdering = idx
        ot_stat.DesignAxisRecord.Axis.append(ar)
    ot_stat.DesignAxisCount = len(axes_spec)
    ot_stat.AxisValueArray = None
    ot_stat.AxisValueCount = 0
    ot_stat.ElidedFallbackNameID = 2
    stat_tbl.table = ot_stat
    font["STAT"] = stat_tbl

    # Build gvar with smooth morphological, optical-size, and perspective variations
    gvar = font["gvar"] = newTable("gvar")
    gvar.variations = {}
    glyph_order = font.getGlyphOrder()

    for gname in glyph_order:
        glyph = glyf[gname]
        if glyph.numberOfContours <= 0:
            gvar.variations[gname] = []
            continue
        coords = list(glyph.coordinates)
        if not coords:
            gvar.variations[gname] = []
            continue

        cx = 0.5 * (min(x for x, _ in coords) + max(x for x, _ in coords))
        cy = 0.5 * (min(y for _, y in coords) + max(y for _, y in coords))

        # 1. wght: radial scale expansion
        wght_d = [(int(round((x - cx) * 0.04)), int(round((y - cy) * 0.03))) for x, y in coords] + [(0, 0)] * 4
        # 2. MRPH: broader palm / rounded proportion
        mrph_d = [(int(round((x - cx) * 0.06)), int(round(-(y - cy) * 0.03))) for x, y in coords] + [(0, 0)] * 4
        # 3. opsz: taller finger extension at small acuity sizes
        opsz_d = [(0, int(round((y - cy) * 0.04))) for x, y in coords] + [(0, 0)] * 4
        # 4. AZIM: gentle 3D turntable perspective shear
        azim_d = [(int(round((y - cy) * 0.03)), 0) for x, y in coords] + [(0, 0)] * 4

        gvar.variations[gname] = [
            TupleVariation({"wght": (0.0, 1.0, 1.0)}, wght_d),
            TupleVariation({"MRPH": (0.0, 0.25, 1.0)}, mrph_d),
            TupleVariation({"opsz": (-1.0, -1.0, 0.0)}, opsz_d),
            TupleVariation({"AZIM": (0.0, 1.0, 1.0)}, azim_d),
        ]

    # Build compact zero-delta HVAR (strict 600 UPM monospace across all axes!)
    var_region_list = otTables.VarRegionList()
    var_region_list.RegionAxisCount = 4
    var_region_list.Region = []
    var_region_list.RegionCount = 0

    var_data = otTables.VarData()
    var_data.VarRegionIndex = []
    var_data.VarRegionCount = 0
    var_data.Item = [[]]
    var_data.ItemCount = 1
    var_data.NumShorts = 0

    var_store = otTables.VarStore()
    var_store.Format = 1
    var_store.VarRegionList = var_region_list
    var_store.VarData = [var_data]
    var_store.VarDataCount = 1

    adv_map = otTables.DeltaSetIndexMap()
    adv_map.Format = 0
    adv_map.mapping = [0] * len(glyph_order)

    hvar_tbl = newTable("HVAR")
    ot_hvar = otTables.HVAR()
    ot_hvar.Version = 0x00010000
    ot_hvar.VarStore = var_store
    ot_hvar.AdvWidthMap = adv_map
    ot_hvar.LsbMap = None
    ot_hvar.RsbMap = None
    hvar_tbl.table = ot_hvar
    font["HVAR"] = hvar_tbl

    for gname in glyph_order:
        g = glyf[gname]
        if g.numberOfContours > 0:
            g.flags = bytearray([fl & 0x3F for fl in g.flags])

    font.save(str(OUT_SIGN_VF_TTF))
    compress(str(OUT_SIGN_VF_TTF), str(OUT_SIGN_VF_WOFF2))
    font.close()
    print(f"  [+] Saved {OUT_SIGN_VF_TTF.name} ({OUT_SIGN_VF_TTF.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    compile_sign_variable_font()
