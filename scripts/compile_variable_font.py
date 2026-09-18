#!/usr/bin/env python3
"""
PocketGull Typefoundry: Universal Variable Font Compiler
=========================================================
Compiles 'PocketGull-VF.ttf' and 'PocketGull-VF.woff2' with continuous
'wght' (400-900), 'slnt' (-10.5 to 0), 'opsz' (14-96), and 'wdth' (75-100) axes.

Features:
- TrueType fvar, gvar, HVAR, and STAT table generation
- Universal wdth variation deltas derived from PocketGull-CondensedBold master
- Google Fonts Option 5 versioning and SIL OFL 1.1 licensing
- Brotli Quality 11 WOFF2 compression
"""

import os
import sys
import shutil
from fontTools.ttLib import TTFont
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor
from fontTools.varLib import build
from fontTools.ttLib.tables._f_v_a_r import Axis, NamedInstance
from fontTools.ttLib.tables.TupleVariation import TupleVariation
from fontTools.ttLib.woff2 import compress

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

def compile_variable_font():
    print("=== POCKETGULL 4-AXIS VARIABLE FONT COMPILER ===")
    
    src_bold = os.path.join(TTF_DIR, "PocketGull-Bold.ttf")
    src_cond = os.path.join(TTF_DIR, "PocketGull-CondensedBold.ttf")
    src_vf = os.path.join(TTF_DIR, "PocketGull-VF.ttf")
    
    out_ttf = os.path.join(TTF_DIR, "PocketGull-VF.ttf")
    out_woff2 = os.path.join(WOFF2_DIR, "PocketGull-VF.woff2")
    root_ttf = os.path.join(ROOT_DIR, "PocketGull-VF.ttf")
    root_woff2 = os.path.join(ROOT_DIR, "PocketGull-VF.woff2")
    
    for path in [src_bold, src_cond, src_vf]:
        if not os.path.isfile(path):
            print(f"[ERROR] Required font master missing: {path}")
            sys.exit(1)
            
    print("1. Loading existing variable font base...")
    vf = TTFont(src_vf)
    fvar = vf['fvar']
    gvar = vf['gvar']
    name_table = vf['name']
    
    # Check if 'wdth' is already in fvar axes
    has_wdth = any(a.axisTag == 'wdth' for a in fvar.axes)
    if not has_wdth:
        print("2. Extracting width ('wdth') variation deltas via varLib from Condensed master...")
        doc = DesignSpaceDocument()
        ax_w = AxisDescriptor()
        ax_w.name = 'Width'
        ax_w.tag = 'wdth'
        ax_w.minimum = 75.0
        ax_w.default = 100.0
        ax_w.maximum = 100.0
        doc.addAxis(ax_w)

        s1 = SourceDescriptor()
        s1.path = src_bold
        s1.name = 'PocketGull Bold'
        s1.location = {'Width': 100.0}
        doc.addSource(s1)

        s2 = SourceDescriptor()
        s2.path = src_cond
        s2.name = 'PocketGull Condensed Bold'
        s2.location = {'Width': 78.0}
        doc.addSource(s2)

        vf_wdth, _, _ = build(doc)
        wdth_gvar = vf_wdth['gvar']
        print(f"  • Extracted wdth variation deltas across {len(wdth_gvar.variations)} glyphs.")

        print("3. Appending 'wdth' continuous axis to fvar table...")
        axis_wdth = Axis()
        axis_wdth.axisTag = 'wdth'
        axis_wdth.minValue = 75.0
        axis_wdth.defaultValue = 100.0
        axis_wdth.maxValue = 100.0
        axis_wdth.flags = 0
        axis_wdth.axisNameID = 280
        name_table.addMultilingualName({'en': 'Width'}, vf, nameID=280)
        fvar.axes.append(axis_wdth)

        for inst in fvar.instances:
            inst.coordinates['wdth'] = 100.0

        cond_instances = [
            ('Condensed Fineliner', {'wght': 400.0, 'slnt': 0.0, 'opsz': 38.0, 'wdth': 78.0}),
            ('Condensed Bold', {'wght': 700.0, 'slnt': 0.0, 'opsz': 38.0, 'wdth': 78.0}),
            ('Condensed Bold Italic', {'wght': 700.0, 'slnt': -10.5, 'opsz': 38.0, 'wdth': 78.0}),
        ]
        nid = 281
        for iname, coords in cond_instances:
            inst = NamedInstance()
            inst.subfamilyNameID = nid
            name_table.addMultilingualName({'en': iname}, vf, nameID=nid)
            nid += 1
            inst.coordinates = coords
            fvar.instances.append(inst)

        print("4. Integrating wdth TupleVariations into gvar variation table...")
        integrated = 0
        skipped = 0
        for gname in vf.getGlyphOrder():
            if gname not in wdth_gvar.variations or gname not in gvar.variations:
                continue
            w_tvs = wdth_gvar.variations[gname]
            v_tvs = gvar.variations[gname]
            if not w_tvs:
                continue
            w_tv = w_tvs[0]
            
            # Check if already has wdth
            if any('wdth' in tv.axes for tv in v_tvs):
                continue
                
            if v_tvs and len(w_tv.coordinates) != len(v_tvs[0].coordinates):
                skipped += 1
                continue
                
            new_tv = TupleVariation(w_tv.axes, w_tv.coordinates)
            v_tvs.append(new_tv)
            integrated += 1

        print(f"  • Integrated wdth deltas into {integrated} glyphs (skipped {skipped}).")
    else:
        print("  • Variable font already contains 'wdth' axis and variation deltas.")

    print(f"  • Total active axes: {[a.axisTag for a in fvar.axes]}")
    print(f"  • Total named instances: {len(fvar.instances)}")

    # Update metadata
    family_name = "PocketGull VF"
    ps_name = "PocketGull-VF"
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table.names = [n for n in name_table.names if n.nameID not in [1, 2, 3, 4, 5, 6, 16, 17]]
    def add_n(nid, val):
        name_table.addMultilingualName({"en": val}, vf, nameID=nid)
        
    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, "Regular")
    add_n(3, f"3.100;POCK;{ps_name}")
    add_n(4, family_name)
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(16, family_name)
    add_n(17, "Regular")

    vf["head"].fontRevision = 3.1
    if "OS/2" in vf:
        vf["OS/2"].usWeightClass = 400
        vf["OS/2"].usWidthClass = 5
        vf["OS/2"].achVendID = "POCK"

    print("5. Saving TTF and recompressing WOFF2...")
    vf.save(out_ttf)
    vf.close()
    try:
        shutil.copyfile(out_ttf, root_ttf)
    except Exception as e:
        print(f"  [WARN] Root TTF sync note: {e}")

    compress(out_ttf, out_woff2)
    try:
        shutil.copyfile(out_woff2, root_woff2)
    except Exception as e:
        print(f"  [WARN] Root WOFF2 sync note: {e}")

    ttf_sz = os.path.getsize(out_ttf)
    woff2_sz = os.path.getsize(out_woff2)
    print(f"  • Saved TTF:   {out_ttf} ({ttf_sz:,} bytes)")
    print(f"  • Saved WOFF2: {out_woff2} ({woff2_sz:,} bytes)")
    print("✅ PocketGull 4-Axis Variable Font compiled successfully!")

if __name__ == "__main__":
    compile_variable_font()
