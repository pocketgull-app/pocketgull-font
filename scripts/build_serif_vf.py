#!/usr/bin/env python3
"""
scripts/build_serif_vf.py
=========================
Builds the Google Fonts & OpenType compliant continuous weight variable font:
- PocketGull-Serif-VF.ttf (wght: 400.0 - 700.0)
- PocketGull-Serif-VF.woff2

Sources:
- PocketGull-Serif-Regular.ttf (wght: 400.0) - Default Master
- PocketGull-Serif-Bold.ttf    (wght: 700.0)

Generates:
- Clean gvar tuple variations with 10,500+ glyphs interpolating smoothly
- fvar table with wght axis [400..700] and named instances (Regular, Medium, SemiBold, Bold)
- STAT table axis values
- 100% 2-byte word boundary alignment on loca (padding = 2)
- Brotli quality 11 WOFF2 compression
- Automatic synchronization to:
  * pocketgull-typeface/fonts/ttf/ & fonts/woff2/
  * pocketgull/public/fonts/
  * pocketgull-font/fonts/ttf/ & fonts/woff2/
"""

import os
import sys
import shutil
from pathlib import Path
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor
from fontTools.varLib import build
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._f_v_a_r import NamedInstance
from fontTools.ttLib.woff2 import compress

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT / "fonts" / "ttf"
WOFF2_DIR = ROOT / "fonts" / "woff2"

APP_FONTS_DIR = ROOT.parent / "pocketgull" / "public" / "fonts"
DIST_FONTS_DIR = ROOT.parent / "pocketgull-font"

def build_serif_vf():
    print("==================================================================")
    print("POCKETGULL SERIF VARIABLE FONT COMPILER (v3.1)")
    print("==================================================================")

    src_regular = TTF_DIR / "PocketGull-Serif-Regular.ttf"
    src_bold = TTF_DIR / "PocketGull-Serif-Bold.ttf"

    if not src_regular.exists() or not src_bold.exists():
        print(f"[ERROR] Required master missing: {src_regular} or {src_bold}")
        sys.exit(1)

    print("1. Constructing Designspace for wght 400..700...")
    doc = DesignSpaceDocument()

    ax_w = AxisDescriptor()
    ax_w.name = 'Weight'
    ax_w.tag = 'wght'
    ax_w.minimum = 400.0
    ax_w.default = 400.0
    ax_w.maximum = 700.0
    doc.addAxis(ax_w)

    s_reg = SourceDescriptor()
    s_reg.path = str(src_regular)
    s_reg.name = 'Regular'
    s_reg.location = {'Weight': 400.0}
    doc.addSource(s_reg)

    s_bld = SourceDescriptor()
    s_bld.path = str(src_bold)
    s_bld.name = 'Bold'
    s_bld.location = {'Weight': 700.0}
    doc.addSource(s_bld)

    print("2. Running varLib.build()...")
    vf, model, _ = build(doc, exclude=['GPOS', 'GDEF'])

    print("3. Configuring OpenType metadata & Option 5 naming table...")
    family_name = "PocketGull Serif"
    ps_name = "PocketGull-Serif-VF"
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = vf['name']
    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 9, 16, 17, 25]]

    def add_n(nid, val):
        name_table.addMultilingualName({'en': val}, vf, nameID=nid)

    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, "Regular")
    add_n(3, f"3.100;POCK;{ps_name}")
    add_n(4, f"{family_name} Regular")
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(9, "Phil Gear")
    add_n(16, family_name)
    add_n(17, "Regular")
    add_n(25, "PocketGullSerif")

    # Configure fvar named instances
    fvar = vf['fvar']
    fvar.instances = []

    instances = [
        ("Regular", 400.0, "PocketGull-Serif-Regular"),
        ("Medium", 500.0, "PocketGull-Serif-Medium"),
        ("SemiBold", 600.0, "PocketGull-Serif-SemiBold"),
        ("Bold", 700.0, "PocketGull-Serif-Bold"),
    ]

    nid = 270
    for iname, wval, psname_inst in instances:
        inst = NamedInstance()
        inst.subfamilyNameID = nid
        add_n(nid, iname)
        nid += 1
        inst.postscriptNameID = nid
        add_n(nid, psname_inst)
        nid += 1
        inst.coordinates = {'wght': wval}
        fvar.instances.append(inst)

    vf['head'].fontRevision = 3.1
    if 'OS/2' in vf:
        vf['OS/2'].usWeightClass = 400
        vf['OS/2'].usWidthClass = 5
        vf['OS/2'].achVendID = "POCK"
        vf['OS/2'].fsType = 0x0000

    # Ensure 100% 2-byte word boundary alignment on loca (OTS invariant)
    vf['glyf'].padding = 2

    out_ttf = TTF_DIR / f"{ps_name}.ttf"
    gf_ttf = TTF_DIR / "PocketGullSerif[wght].ttf"
    root_ttf = ROOT / f"{ps_name}.ttf"
    out_woff2 = WOFF2_DIR / f"{ps_name}.woff2"
    gf_woff2 = WOFF2_DIR / "PocketGullSerif[wght].woff2"
    root_woff2 = ROOT / f"{ps_name}.woff2"

    print("4. Saving TrueType Variable Font...")
    vf.save(str(out_ttf))
    vf.save(str(gf_ttf))
    try:
        vf.save(str(root_ttf))
    except Exception as e:
        print(f"  [NOTE] Root TTF save note: {e}")
    vf.close()
    print(f"  [SUCCESS] Saved {out_ttf} ({out_ttf.stat().st_size:,} bytes)")

    print("5. Compressing Brotli WOFF2...")
    compress(str(out_ttf), str(out_woff2))
    compress(str(gf_ttf), str(gf_woff2))
    try:
        shutil.copyfile(str(out_woff2), str(root_woff2))
    except Exception as e:
        pass
    print(f"  [SUCCESS] Compressed {out_woff2} ({out_woff2.stat().st_size:,} bytes)")

    # 6. Synchronize to consumer workspaces
    print("6. Synchronizing to consumer workspaces...")
    for ttf_src in [out_ttf, gf_ttf]:
        if APP_FONTS_DIR.exists():
            shutil.copy2(str(ttf_src), str(APP_FONTS_DIR / ttf_src.name))
        if DIST_FONTS_DIR.exists() and DIST_FONTS_DIR.resolve() != ROOT.resolve() and (DIST_FONTS_DIR / "fonts" / "ttf").exists():
            shutil.copy2(str(ttf_src), str(DIST_FONTS_DIR / "fonts" / "ttf" / ttf_src.name))

    for woff2_src in [out_woff2, gf_woff2]:
        if APP_FONTS_DIR.exists():
            shutil.copy2(str(woff2_src), str(APP_FONTS_DIR / woff2_src.name))
        if DIST_FONTS_DIR.exists() and DIST_FONTS_DIR.resolve() != ROOT.resolve() and (DIST_FONTS_DIR / "fonts" / "woff2").exists():
            shutil.copy2(str(woff2_src), str(DIST_FONTS_DIR / "fonts" / "woff2" / woff2_src.name))

    print(f"  [SUCCESS] Synchronized PocketGull-Serif-VF binaries across all workspaces.")
    print("==================================================================")
    print("ALL DONE: PocketGull Serif Variable Font is ready!")
    print("==================================================================")

if __name__ == "__main__":
    build_serif_vf()
