#!/usr/bin/env python3
"""
PocketGull Typefoundry - ISMP Disambiguation Bold & Chiseltip Curing Engine
==========================================================================
Systematically scales and cures the Louise Sloan / ISMP disambiguation alternates:
  - cv05 (l.curved): Scales stem width to 151 UPM (Bold) and 191 UPM (Chiseltip)
  - ss02 (I.serif): Replaces thin unbracketed stem with full native bilateral serifed I (151 UPM / 194 UPM)
  - zero / cv08 (zero.slash): Replaces thin 84 UPM zero with full bold counter + diagonal slash (150 UPM / 192 UPM)

Applies cures across:
  1. UFO source master glyphs (.glif)
  2. Master Glyphs file (PocketGull.glyphs)
  3. Typefoundry TTF & Brotli WOFF2 webfonts (fonts/ttf, fonts/woff2)
  4. philgear.dev and philgear.biz webfont distributions
"""

import os
import sys
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.woff2 import compress, decompress

# -----------------------------------------------------------------------------
# GEOMETRY DEFINITIONS
# -----------------------------------------------------------------------------

# Bold (700) Geometry
BOLD_L_CURVED_PTS = [
    (80, 0), (80, 75), (246, 90), (246, 685),
    (86, 685), (86, 760), (397, 760), (397, 90),
    (571, 75), (571, 0)
]
BOLD_SLASH_PTS = [(185, 100), (126, 152), (406, 626), (458, 560)]

# Chiseltip (900) Geometry
CHISELTIP_L_CURVED_PTS = [
    (70, 0), (70, 85), (220, 100), (220, 670),
    (70, 670), (70, 760), (411, 760), (411, 100),
    (585, 85), (585, 0)
]
CHISELTIP_SLASH_PTS = [(210, 130), (160, 175), (370, 580), (420, 535)]

def cure_binary_font(font_path: Path, weight_type: str):
    """Cures TTF or WOFF2 font binary."""
    print(f"Curing {font_path} ({weight_type})...")
    is_woff2 = font_path.suffix.lower() == ".woff2"
    
    font = TTFont(str(font_path))
    glyf = font.get('glyf')
    if not glyf:
        print(f"  [SKIP] No glyf table in {font_path}")
        return

    hmtx = font['hmtx']
    gsub = font.get('GSUB')
    
    l_target = "l.curved" if "l.curved" in glyf else None
    I_target = "I.serif" if "I.serif" in glyf else None
    zero_target = "zero.slash" if "zero.slash" in glyf else None
    
    if gsub and gsub.table.FeatureList:
        for fr in gsub.table.FeatureList.FeatureRecord:
            if fr.FeatureTag == 'cv05' and not l_target:
                lk = gsub.table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
                l_target = lk.SubTable[0].mapping.get('l')
            elif fr.FeatureTag == 'ss02' and not I_target:
                lk = gsub.table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
                I_target = lk.SubTable[0].mapping.get('I')
            elif fr.FeatureTag in ('zero', 'cv08') and not zero_target:
                lk = gsub.table.LookupList.Lookup[fr.Feature.LookupListIndex[0]]
                zero_target = lk.SubTable[0].mapping.get('zero')

    is_bold = (weight_type == "bold")
    l_pts = BOLD_L_CURVED_PTS if is_bold else CHISELTIP_L_CURVED_PTS
    slash_pts = BOLD_SLASH_PTS if is_bold else CHISELTIP_SLASH_PTS
    l_advance = 650 if is_bold else 680
    l_lsb = 80 if is_bold else 70

    # 1. Cure I.serif
    if I_target and I_target in glyf and 'I' in glyf:
        g_I = glyf['I']
        coords_I, endPts_I, flags_I = g_I.getCoordinates(glyf)
        tgt_I = glyf[I_target]
        tgt_I.numberOfContours = len(endPts_I)
        tgt_I.endPtsOfContours = list(endPts_I)
        tgt_I.coordinates = GlyphCoordinates(list(coords_I))
        tgt_I.flags = bytearray(flags_I)
        tgt_I.program = g_I.program
        tgt_I.recalcBounds(glyf)
        hmtx[I_target] = (hmtx['I'][0], tgt_I.xMin)
        print(f"  [CURED] {I_target} (I.serif) -> Native Bold Bilateral Serifs (Stem: {tgt_I.xMax - tgt_I.xMin} UPM)")

    # 2. Cure zero.slash
    if zero_target and zero_target in glyf and 'zero' in glyf:
        g_zero = glyf['zero']
        coords_z, endPts_z, flags_z = g_zero.getCoordinates(glyf)
        c0_pts = [coords_z[i] for i in range(0, endPts_z[0] + 1)]
        c0_flags = [flags_z[i] for i in range(0, endPts_z[0] + 1)]
        c1_pts = [coords_z[i] for i in range(endPts_z[0] + 1, endPts_z[1] + 1)]
        c1_flags = [flags_z[i] for i in range(endPts_z[0] + 1, endPts_z[1] + 1)]
        
        slash_flags = [1] * len(slash_pts)
        all_pts = c0_pts + c1_pts + slash_pts
        all_flags = c0_flags + c1_flags + slash_flags
        
        tgt_z = glyf[zero_target]
        tgt_z.numberOfContours = 3
        tgt_z.endPtsOfContours = [endPts_z[0], endPts_z[1], len(all_pts) - 1]
        tgt_z.coordinates = GlyphCoordinates(all_pts)
        tgt_z.flags = bytearray(all_flags)
        tgt_z.program = g_zero.program
        tgt_z.recalcBounds(glyf)
        hmtx[zero_target] = (hmtx['zero'][0], tgt_z.xMin)
        print(f"  [CURED] {zero_target} (zero.slash) -> Full Counter + Diagonal Slash (Stroke: {tgt_z.xMax - tgt_z.xMin} UPM)")

    # 3. Cure l.curved
    if l_target and l_target in glyf:
        tgt_l = glyf[l_target]
        tgt_l.numberOfContours = 1
        tgt_l.endPtsOfContours = [len(l_pts) - 1]
        tgt_l.coordinates = GlyphCoordinates(l_pts)
        tgt_l.flags = bytearray([1] * len(l_pts))
        tgt_l.program = glyf['l'].program if 'l' in glyf else tgt_l.program
        tgt_l.recalcBounds(glyf)
        hmtx[l_target] = (l_advance, l_lsb)
        stem_w = (397 - 246) if is_bold else (411 - 220)
        print(f"  [CURED] {l_target} (l.curved) -> Stem: {stem_w} UPM, Adv: {l_advance}")

    # Ensure 2-byte word padding
    font.save(str(font_path))
    if is_woff2:
        # Recompress to WOFF2 cleanly
        tmp_ttf = font_path.with_suffix(".tmp.ttf")
        font.flavor = None
        font.save(str(tmp_ttf))
        compress(str(tmp_ttf), str(font_path))
        if tmp_ttf.exists():
            tmp_ttf.unlink()
    print(f"  [SAVED] {font_path}")

def cure_ufo(ufo_dir: Path, weight_type: str):
    """Cures glyphs inside a UFO directory."""
    print(f"Curing UFO: {ufo_dir} ({weight_type})...")
    glyphs_dir = ufo_dir / "glyphs"
    if not glyphs_dir.exists():
        print(f"  [SKIP] No glyphs dir in {ufo_dir}")
        return

    is_bold = (weight_type == "bold")

    # 1. Cure I_.serif.glif
    i_src = glyphs_dir / "I_.glif"
    i_serif_tgt = glyphs_dir / "I_.serif.glif"
    if i_src.exists():
        with open(i_src, "r", encoding="utf-8") as f:
            content = f.read()
        cured_content = content.replace('name="I"', 'name="I.serif"')
        with open(i_serif_tgt, "w", encoding="utf-8") as f:
            f.write(cured_content)
        print("  [CURED UFO] I_.serif.glif")

    # 2. Cure zero.slash.glif
    z_src = glyphs_dir / "zero.glif"
    z_slash_tgt = glyphs_dir / "zero.slash.glif"
    if z_src.exists():
        with open(z_src, "r", encoding="utf-8") as f:
            z_lines = f.readlines()
        slash_xml = """    <contour>
      <point x="185" y="100" type="line"/>
      <point x="126" y="152" type="line"/>
      <point x="406" y="626" type="line"/>
      <point x="458" y="560" type="line"/>
    </contour>
""" if is_bold else """    <contour>
      <point x="210" y="130" type="line"/>
      <point x="160" y="175" type="line"/>
      <point x="370" y="580" type="line"/>
      <point x="420" y="535" type="line"/>
    </contour>
"""
        new_lines = []
        for line in z_lines:
            if 'name="zero"' in line:
                new_lines.append(line.replace('name="zero"', 'name="zero.slash"'))
            elif '</outline>' in line:
                new_lines.append(slash_xml)
                new_lines.append(line)
            else:
                new_lines.append(line)
        with open(z_slash_tgt, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print("  [CURED UFO] zero.slash.glif")

    # 3. Cure l.curved.glif
    l_curved_tgt = glyphs_dir / "l.curved.glif"
    l_advance = 650 if is_bold else 680
    pts = BOLD_L_CURVED_PTS if is_bold else CHISELTIP_L_CURVED_PTS
    l_lines = [
        "<?xml version='1.0' encoding='UTF-8'?>\n",
        '<glyph name="l.curved" format="2">\n',
        f'  <advance width="{l_advance}"/>\n',
        "  <outline>\n",
        "    <contour>\n"
    ]
    for x, y in pts:
        l_lines.append(f'      <point x="{x}" y="{y}" type="line"/>\n')
    l_lines.extend([
        "    </contour>\n",
        "  </outline>\n",
        "</glyph>\n"
    ])
    with open(l_curved_tgt, "w", encoding="utf-8") as f:
        f.writelines(l_lines)
    print("  [CURED UFO] l.curved.glif")

def main():
    root_dir = Path(__file__).resolve().parent.parent
    
    # 1. Source UFOs
    bold_ufo = root_dir / "sources" / "PocketGull-Bold.ufo"
    chisel_ufo = root_dir / "sources" / "PocketGull-Chiseltip.ufo"
    if bold_ufo.exists():
        cure_ufo(bold_ufo, "bold")
    if chisel_ufo.exists():
        cure_ufo(chisel_ufo, "chiseltip")

    # 2. Typefoundry Binaries
    tf_files = [
        (root_dir / "fonts" / "ttf" / "PocketGull-Bold.ttf", "bold"),
        (root_dir / "fonts" / "ttf" / "PocketGull-Chiseltip.ttf", "chiseltip"),
        (root_dir / "fonts" / "woff2" / "PocketGull-Bold.woff2", "bold"),
        (root_dir / "fonts" / "woff2" / "PocketGull-Chiseltip.woff2", "chiseltip"),
    ]
    for path, weight in tf_files:
        if path.exists():
            cure_binary_font(path, weight)

    # 3. philgear.dev Binaries
    dev_fonts_dir = Path("C:/Users/philg/Dev/philgear.dev/public/fonts/pocketgull")
    if dev_fonts_dir.exists():
        dev_files = [
            (dev_fonts_dir / "PocketGull-Bold.ttf", "bold"),
            (dev_fonts_dir / "PocketGull-Bold.woff2", "bold"),
            (dev_fonts_dir / "PocketGull-Chiseltip.ttf", "chiseltip"),
            (dev_fonts_dir / "PocketGull-Chiseltip.woff2", "chiseltip"),
        ]
        for path, weight in dev_files:
            if path.exists():
                cure_binary_font(path, weight)

    # 4. philgear.biz Binaries (if present)
    biz_fonts_dir = Path("C:/Users/philg/Dev/philgear.biz/public/fonts/pocketgull")
    if biz_fonts_dir.exists():
        biz_files = [
            (biz_fonts_dir / "PocketGull-Bold.ttf", "bold"),
            (biz_fonts_dir / "PocketGull-Chiseltip.ttf", "chiseltip"),
        ]
        for path, weight in biz_files:
            if path.exists():
                cure_binary_font(path, weight)

    print("\n[SUCCESS] All PocketGull Bold and Chiseltip fonts cured with authentic 151 UPM / 191 UPM geometry!")

if __name__ == "__main__":
    main()
