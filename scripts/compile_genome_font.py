#!/usr/bin/env python3
"""
PocketGull Typefoundry: Master Genome & Bioinformatics Font Compiler
===================================================================
Compiles 'PocketGull-Genome.ttf' and 'PocketGull-Genome.woff2'
World's First Humanist Clinical Genomics, Bioinformatics & CRISPR/Cas9 Monospace Typeface
"""

import os
import sys
import math
import shutil
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TTF_DIR = os.path.join(ROOT_DIR, "fonts", "ttf")
WOFF2_DIR = os.path.join(ROOT_DIR, "fonts", "woff2")

SRC_MONO = os.path.join(TTF_DIR, "PocketGullMono-Regular.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Genome.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Genome.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Genome.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Genome.woff2")

ADVANCE = 600      # Strict 600 UPM fixed pitch monospace
AXIS_HEIGHT = 260  # Reading centerline
STROKE_W = 68      # Standard stroke weight
hw = STROKE_W // 2

def draw_rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0))
    pen.lineTo((x1, y0))
    pen.lineTo((x1, y1))
    pen.lineTo((x0, y1))
    pen.closePath()

def draw_circle(pen, cx, cy, r, clockwise=True):
    if clockwise:
        pen.moveTo((cx + r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy + r), (cx, cy + r))
        pen.qCurveTo((cx + r, cy + r), (cx + r, cy))
        pen.closePath()
    else:
        pen.moveTo((cx + r, cy))
        pen.qCurveTo((cx + r, cy + r), (cx, cy + r))
        pen.qCurveTo((cx - r, cy + r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.closePath()

def build_genome_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: CLINICAL GENOMICS & BIOINFORMATICS COMPILER")
    print("=" * 76)

    if not os.path.isfile(SRC_MONO):
        print(f"[ERROR] Master monospace font missing: {SRC_MONO}")
        sys.exit(1)

    print("\n1. Loading master monospace font source...")
    font = TTFont(SRC_MONO)

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())

    def register_glyph(gname, codepoints, pen):
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (ADVANCE, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    print("\n2. Synthesizing CRISPR-Cas9 & Genetic Engineering Glyphs...")

    # Glyph 1: CRISPR Double-Strand Break (DSB) Cleavage Scissors U+2702 & PUA U+E920
    pen = TTGlyphPen(None)
    # Pivot screw at center (300, 350)
    draw_circle(pen, 300, 350, 42, clockwise=True)
    draw_circle(pen, 300, 350, 42 - hw, clockwise=False)
    # Left blade angled up-right
    pen.moveTo((290, 350))
    pen.lineTo((490, 620))
    pen.lineTo((470, 635))
    pen.lineTo((275, 365))
    pen.closePath()
    # Right blade angled down-right
    pen.moveTo((290, 350))
    pen.lineTo((490, 80))
    pen.lineTo((470, 65))
    pen.lineTo((275, 335))
    pen.closePath()
    # Finger loop upper-left: center (180, 520)
    draw_circle(pen, 180, 520, 80, clockwise=True)
    draw_circle(pen, 180, 520, 80 - STROKE_W, clockwise=False)
    pen.moveTo((235, 465))
    pen.lineTo((295, 365))
    pen.lineTo((280, 350))
    pen.lineTo((220, 450))
    pen.closePath()
    # Finger loop lower-left: center (180, 180)
    draw_circle(pen, 180, 180, 80, clockwise=True)
    draw_circle(pen, 180, 180, 80 - STROKE_W, clockwise=False)
    pen.moveTo((235, 235))
    pen.lineTo((295, 335))
    pen.lineTo((280, 350))
    pen.lineTo((220, 250))
    pen.closePath()
    register_glyph("crispr_dsb_scissors", [0x2702, 0xE920], pen)

    # Glyph 2: PAM Motif Bracket Badge [NGG] PUA U+E921
    pen = TTGlyphPen(None)
    # Left bracket [
    draw_rect(pen, 80, 100, 80 + STROKE_W, 600)
    draw_rect(pen, 80, 600 - STROKE_W, 160, 600)
    draw_rect(pen, 80, 100, 160, 100 + STROKE_W)
    # Right bracket ]
    draw_rect(pen, 520 - STROKE_W, 100, 520, 600)
    draw_rect(pen, 440, 600 - STROKE_W, 520, 600)
    draw_rect(pen, 440, 100, 520, 100 + STROKE_W)
    # Center PAM symbol: Bold P-A-M dots or recognition chevron
    pen.moveTo((220, 200))
    pen.lineTo((300, 350))
    pen.lineTo((380, 200))
    pen.lineTo((380 - STROKE_W, 200))
    pen.lineTo((300, 350 - STROKE_W))
    pen.lineTo((220 + STROKE_W, 200))
    pen.closePath()
    draw_rect(pen, 200, 420, 400, 420 + STROKE_W)
    draw_rect(pen, 250, 500, 350, 500 + STROKE_W)
    register_glyph("pam_motif_badge", [0xE921], pen)

    # Glyph 3: sgRNA Hairpin Stem-Loop PUA U+E922
    pen = TTGlyphPen(None)
    # Two vertical stem strands at x = 240 and x = 360
    draw_rect(pen, 240 - hw, 50, 240 + hw, 450)
    draw_rect(pen, 360 - hw, 50, 360 + hw, 450)
    # Transverse base-pair rungs connecting stems
    draw_rect(pen, 240, 120 - hw, 360, 120 + hw)
    draw_rect(pen, 240, 220 - hw, 360, 220 + hw)
    draw_rect(pen, 240, 320 - hw, 360, 320 + hw)
    draw_rect(pen, 240, 420 - hw, 360, 420 + hw)
    # Hairpin loop at top: center (300, 480), outer radius 120, inner radius 120 - STROKE_W
    draw_circle(pen, 300, 480, 120, clockwise=True)
    draw_circle(pen, 300, 480, 120 - STROKE_W, clockwise=False)
    register_glyph("sgrna_hairpin_loop", [0xE922], pen)

    # Glyph 4: Hydrogen Bond Pairing Badges: Double H-Bond (A=T) PUA U+E923
    pen = TTGlyphPen(None)
    # Left pillar at x = 120, right pillar at x = 480
    draw_rect(pen, 120 - hw, 150, 120 + hw, 550)
    draw_rect(pen, 480 - hw, 150, 480 + hw, 550)
    # Two dashed/solid horizontal H-bonds
    hgap = 60
    draw_rect(pen, 120, 350 + hgap - hw, 480, 350 + hgap + hw)
    draw_rect(pen, 120, 350 - hgap - hw, 480, 350 - hgap + hw)
    register_glyph("hbond_double_at", [0xE923], pen)

    # Glyph 5: Hydrogen Bond Pairing Badges: Triple H-Bond (G≡C) PUA U+E924
    pen = TTGlyphPen(None)
    draw_rect(pen, 120 - hw, 150, 120 + hw, 550)
    draw_rect(pen, 480 - hw, 150, 480 + hw, 550)
    # Three horizontal H-bonds
    hgap3 = 70
    draw_rect(pen, 120, 350 + hgap3 - hw, 480, 350 + hgap3 + hw)
    draw_rect(pen, 120, 350 - hw, 480, 350 + hw)
    draw_rect(pen, 120, 350 - hgap3 - hw, 480, 350 - hgap3 + hw)
    register_glyph("hbond_triple_gc", [0xE924], pen)

    # Glyph 6: Wobble Base Pair (G·U) PUA U+E925
    pen = TTGlyphPen(None)
    draw_rect(pen, 120 - hw, 150, 120 + hw, 550)
    draw_rect(pen, 480 - hw, 150, 480 + hw, 550)
    draw_circle(pen, 300, 350, 40, clockwise=True)
    register_glyph("wobble_pair_gu", [0xE925], pen)

    # Glyph 7: Centromere Constriction Symbol PUA U+E926
    pen = TTGlyphPen(None)
    # Hourglass chromosome constriction
    pen.moveTo((160, 600))
    pen.lineTo((440, 600))
    pen.lineTo((330, 350))
    pen.lineTo((440, 100))
    pen.lineTo((160, 100))
    pen.lineTo((270, 350))
    pen.closePath()
    # Hollow center constriction cutout
    pen.moveTo((200, 560))
    pen.lineTo((280, 365))
    pen.lineTo((200, 140))
    pen.lineTo((400, 140))
    pen.lineTo((320, 365))
    pen.lineTo((400, 560))
    pen.closePath()
    register_glyph("chromosome_centromere", [0xE926], pen)

    # Glyph 8: Telomere Cap Symbol PUA U+E927
    pen = TTGlyphPen(None)
    # Rounded domed chromosome end cap
    draw_rect(pen, 160, 100, 440, 350)
    draw_circle(pen, 300, 350, 140, clockwise=True)
    draw_circle(pen, 300, 350, 140 - STROKE_W, clockwise=False)
    draw_rect(pen, 160 + STROKE_W, 100 + STROKE_W, 440 - STROKE_W, 350)
    register_glyph("chromosome_telomere", [0xE927], pen)

    # Glyph 9: 5' to 3' Directional Indicator PUA U+E92A
    pen = TTGlyphPen(None)
    draw_rect(pen, 100, AXIS_HEIGHT - hw, 480, AXIS_HEIGHT + hw)
    # Arrowhead pointing right
    pen.moveTo((500, AXIS_HEIGHT))
    pen.lineTo((380, AXIS_HEIGHT + 120))
    pen.lineTo((380, AXIS_HEIGHT + 120 - STROKE_W))
    pen.lineTo((440, AXIS_HEIGHT))
    pen.lineTo((380, AXIS_HEIGHT - 120 + STROKE_W))
    pen.lineTo((380, AXIS_HEIGHT - 120))
    pen.closePath()
    # 5-prime notch at left (x = 100)
    draw_rect(pen, 100, AXIS_HEIGHT - 80, 100 + STROKE_W, AXIS_HEIGHT + 80)
    register_glyph("strand_5to3_arrow", [0xE92A], pen)

    # Glyph 10: 3' to 5' Directional Indicator PUA U+E92B
    pen = TTGlyphPen(None)
    draw_rect(pen, 120, AXIS_HEIGHT - hw, 500, AXIS_HEIGHT + hw)
    # Arrowhead pointing left
    pen.moveTo((100, AXIS_HEIGHT))
    pen.lineTo((220, AXIS_HEIGHT + 120))
    pen.lineTo((220, AXIS_HEIGHT + 120 - STROKE_W))
    pen.lineTo((160, AXIS_HEIGHT))
    pen.lineTo((220, AXIS_HEIGHT - 120 + STROKE_W))
    pen.lineTo((220, AXIS_HEIGHT - 120))
    pen.closePath()
    # 3-prime notch at right (x = 500)
    draw_rect(pen, 500 - STROKE_W, AXIS_HEIGHT - 80, 500, AXIS_HEIGHT + 80)
    register_glyph("strand_3to5_arrow", [0xE92B], pen)

    # Glyph 11: Epigenetic 5-Methylcytosine (m5C) Badge PUA U+E928
    pen = TTGlyphPen(glyphSet=glyf)
    # Base letter 'C' component scaled 0.75
    pen.addComponent("C", (0.75, 0, 0, 0.75, 120, 50))
    # m5 prefix
    pen.addComponent("m", (0.45, 0, 0, 0.45, 80, 360))
    register_glyph("epigenetic_m5c", [0xE928], pen)

    # Glyph 12: Epigenetic N6-Methyladenosine (m6A) Badge PUA U+E929
    pen = TTGlyphPen(glyphSet=glyf)
    pen.addComponent("A", (0.75, 0, 0, 0.75, 120, 50))
    pen.addComponent("m", (0.45, 0, 0, 0.45, 80, 360))
    register_glyph("epigenetic_m6a", [0xE929], pen)

    # Glyph 13: Chromosomal Translocation Reciprocal Symbol PUA U+E92C
    pen = TTGlyphPen(None)
    # Two intersecting curved interchange arrows
    pen.moveTo((120, 520))
    pen.qCurveTo((300, 350), (480, 520))
    pen.lineTo((480, 520 - STROKE_W))
    pen.qCurveTo((300, 350 - STROKE_W), (120, 520 - STROKE_W))
    pen.closePath()
    pen.moveTo((120, 180))
    pen.qCurveTo((300, 350), (480, 180))
    pen.lineTo((480, 180 + STROKE_W))
    pen.qCurveTo((300, 350 + STROKE_W), (120, 180 + STROKE_W))
    pen.closePath()
    # Arrowhead at top right
    pen.moveTo((480, 520))
    pen.lineTo((400, 560))
    pen.lineTo((410, 480))
    pen.closePath()
    # Arrowhead at bottom right
    pen.moveTo((480, 180))
    pen.lineTo((400, 140))
    pen.lineTo((410, 220))
    pen.closePath()
    register_glyph("translocation_symbol", [0xE92C], pen)

    # 3. Monospace pitch verification across all glyphs
    print("\n3. Enforcing 600 UPM fixed pitch monospace invariant...")
    font["post"].isFixedPitch = 1
    font["OS/2"].panose.bProportion = 9
    for gname in glyf.glyphs.keys():
        adv, lsb = hmtx.metrics.get(gname, (ADVANCE, 50))
        hmtx[gname] = (ADVANCE, lsb)

    # 4. Metadata and SemVer 3.100 Versioning
    print("\n4. Setting metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Genome"
    ps_name = "PocketGull-Genome"
    version_str = "Version 3.100; The PocketGull Project Authors; OFL 1.1"
    copyright_str = "Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)"

    name_table = font["name"]
    name_table.names = [n for n in name_table.names if n.nameID not in [0, 1, 2, 3, 4, 5, 6, 16, 17, 25]]

    def add_n(nid, val):
        name_table.setName(val, nid, platformID=3, platEncID=1, langID=0x409)
        name_table.setName(val, nid, platformID=1, platEncID=0, langID=0x0)

    add_n(0, copyright_str)
    add_n(1, family_name)
    add_n(2, "Regular")
    add_n(3, f"3.100;PGUL;{ps_name}")
    add_n(4, family_name)
    add_n(5, version_str)
    add_n(6, ps_name)
    add_n(16, family_name)
    add_n(17, "Regular")

    # 5. Serialization and Compression
    print("\n5. Serializing TrueType binary and compressing Brotli Q11 WOFF2...")
    os.makedirs(TTF_DIR, exist_ok=True)
    os.makedirs(WOFF2_DIR, exist_ok=True)

    font.save(OUT_TTF)
    shutil.copyfile(OUT_TTF, ROOT_TTF)
    compress(OUT_TTF, OUT_WOFF2)
    shutil.copyfile(OUT_WOFF2, ROOT_WOFF2)

    ttf_sz = os.path.getsize(OUT_TTF)
    woff2_sz = os.path.getsize(OUT_WOFF2)
    print(f"   • Output TTF:   {OUT_TTF} ({ttf_sz:,} bytes)")
    print(f"   • Output WOFF2: {OUT_WOFF2} ({woff2_sz:,} bytes)")
    print("=" * 76)
    print("  [SUCCESS] PocketGull Genome Monospace Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_genome_font()
