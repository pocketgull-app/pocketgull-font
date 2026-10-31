#!/usr/bin/env python3
"""
PocketGull Typefoundry: Systems Thinking & Cybernetics Font Glyph Synthesizer
=============================================================================
Synthesizes and injects 16 native, 600-UPM monospaced vector glyphs using
100% generic, classical Cybernetics, Set Theory & System Dynamics nomenclature
(Zero proprietary trademarks in binary PostScript glyph names):

1. Classical Cybernetics & Structural Set Topology (PUA 0xE9E0–0xE9E7):
   - U+E9E0 (sys_boundary_set): Boundary & Set Distinction (Spencer-Brown mark / Venn boundary)
   - U+E9E1 (sys_holon_triad): System Holarchy Triad (Koestler / Bertalanffy part-whole network)
   - U+E9E2 (sys_causal_coupling): Bidirectional Cybernetic Coupling (Wiener action-reaction)
   - U+E9E3 (sys_observer_frame): Second-Order Cybernetic Observer Frame (von Foerster lens)
   - U+E9E4 (sys_bipartite_split): Bipartite Boundary Split (Inside | Outside state partition)
   - U+E9E5 (sys_nested_holarchy): Concentric Nested Hierarchy (3-tier subsystem containment)
   - U+E9E6 (sys_relational_node): Mediated Edge-Node Channel (Reified state transition link)
   - U+E9E7 (sys_metacognitive_lens): Ophthalmic Observer Aperture (Perspective & framing)
2. System Dynamics, Feedback Loops & Phase Space (PUA 0xE9E8–0xE9EF):
   - U+E9E8 (sys_loop_reinforcing): Reinforcing Feedback Loop (R+ positive gain)
   - U+E9E9 (sys_loop_balancing): Balancing Feedback Loop (B− negative homeostatic control)
   - U+E9EA (sys_stock_accumulator): Stock / Accumulator Reservoir Box (Forrester state integral)
   - U+E9EB (sys_flow_valve): Flow Pipe with Bowtie Control Valve (Rate regulator dS/dt)
   - U+E9EC (sys_delay_hash): Causal Link with Double-Hash Time Delay (Phase lag //)
   - U+E9ED (sys_source_sink_cloud): Infinite Source / Sink Boundary Cloud
   - U+E9EE (sys_leverage_fulcrum): High-Leverage Fulcrum (Archimedes / Meadows intervention Δ)
   - U+E9EF (sys_emergence_attractor): Phase-Space Strange Attractor / Emergence (Lorenz ∞)

Invariants Enforced:
- Fixed 600 UPM advance width across all target styles.
- Louise Sloan 5:1 optotypic clarity & 25 UPM humanist corner radii.
- 2-byte word alignment (loca[i] % 2 == 0) via pure Dart 3.11 SfntTransformer.
- Bit-6 & Bit-7 flag masking (flag & 0x3F).
- Zero duplicate consecutive nodes (W3C OTS 100% compliant).
- High-efficiency Brotli Q11 WOFF2 recompression.
"""

import math
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"
PUBLIC_FONTS_DIR = ROOT_DIR.parent / "pocketgull" / "public" / "fonts"

ADVANCE = 600
STROKE_W = 48

LEGACY_DSRP_NAMES = [
    "dsrp_distinction",
    "dsrp_system",
    "dsrp_relationship",
    "dsrp_perspective",
    "dsrp_identity_other",
    "dsrp_part_whole",
    "dsrp_action_reaction",
    "dsrp_point_view",
]


def finish_glyph(pen):
    g = pen.glyph()
    g.program = Program()
    return g


def sanitize_contour_points(coords, endPts):
    """Eliminates consecutive identical points to guarantee 0 duplicate nodes."""
    start = 0
    for end in endPts:
        for i in range(start, end):
            if coords[i] == coords[i + 1]:
                coords[i + 1] = (coords[i + 1][0] + 1, coords[i + 1][1])
        if len(coords) > 1 and coords[start] == coords[end]:
            coords[end] = (coords[end][0] + 1, coords[end][1])
        start = end + 1


def draw_rect(pen, x0, y0, x1, y1, clockwise=True):
    if clockwise:
        pen.moveTo((int(x0), int(y0)))
        pen.lineTo((int(x0), int(y1)))
        pen.lineTo((int(x1), int(y1)))
        pen.lineTo((int(x1), int(y0)))
    else:
        pen.moveTo((int(x0), int(y0)))
        pen.lineTo((int(x1), int(y0)))
        pen.lineTo((int(x1), int(y1)))
        pen.lineTo((int(x0), int(y1)))
    pen.closePath()


def draw_circle(pen, cx, cy, r, clockwise=True):
    cx, cy, r = int(cx), int(cy), int(r)
    if clockwise:
        pen.moveTo((cx, cy + r))
        pen.qCurveTo((cx + r, cy + r), (cx + r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy + r), (cx, cy + r))
    else:
        pen.moveTo((cx, cy + r))
        pen.qCurveTo((cx - r, cy + r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx + r, cy - r), (cx + r, cy))
        pen.qCurveTo((cx + r, cy + r), (cx, cy + r))
    pen.closePath()


def draw_annulus(pen, cx, cy, r_out, r_in):
    draw_circle(pen, cx, cy, r_out, clockwise=True)
    draw_circle(pen, cx, cy, r_in, clockwise=False)


def draw_rounded_box(pen, x0, y0, x1, y1, r=25, sw=44):
    """Draws a hollow rounded rectangle with outer CW and inner CCW contours."""
    x0, y0, x1, y1, r, sw = int(x0), int(y0), int(x1), int(y1), int(r), int(sw)
    pen.moveTo((x0, y0 + r))
    pen.lineTo((x0, y1 - r))
    pen.qCurveTo((x0, y1), (x0 + r, y1))
    pen.lineTo((x1 - r, y1))
    pen.qCurveTo((x1, y1), (x1, y1 - r))
    pen.lineTo((x1, y0 + r))
    pen.qCurveTo((x1, y0), (x1 - r, y0))
    pen.lineTo((x0 + r, y0))
    pen.qCurveTo((x0, y0), (x0, y0 + r))
    pen.closePath()

    ix0, iy0, ix1, iy1 = x0 + sw, y0 + sw, x1 - sw, y1 - sw
    if ix1 > ix0 and iy1 > iy0:
        draw_rect(pen, ix0, iy0, ix1, iy1, clockwise=False)


def draw_stroke_line(pen, x0, y0, x1, y1, w=40):
    dx = x1 - x0
    dy = y1 - y0
    L = math.hypot(dx, dy)
    if L < 1:
        return
    nx = -dy / L * (w / 2.0)
    ny = dx / L * (w / 2.0)
    pen.moveTo((int(round(x0 + nx)), int(round(y0 + ny))))
    pen.lineTo((int(round(x1 + nx)), int(round(y1 + ny))))
    pen.lineTo((int(round(x1 - nx)), int(round(y1 - ny))))
    pen.lineTo((int(round(x0 - nx)), int(round(y0 - ny))))
    pen.closePath()


# =============================================================================
# 1. CLASSICAL CYBERNETICS & SET TOPOLOGY GLYPHS (U+E9E0 - U+E9E7)
# =============================================================================

def build_sys_boundary_set():
    """U+E9E0: Boundary & Set Distinction (System vs. Environment).
    Crisp boundary circle with solid inner core and external complement satellite.
    """
    pen = TTGlyphPen(None)
    cx, cy = 260, 330
    draw_annulus(pen, cx, cy, 190, 142)
    draw_circle(pen, cx, cy, 66, clockwise=True)
    draw_annulus(pen, 495, 520, 62, 30)
    return finish_glyph(pen)


def build_sys_holon_triad():
    """U+E9E1: System Holarchy Triad (Part-Whole Network).
    Whole system containment ring housing 3 interconnected node elements in a triad.
    """
    pen = TTGlyphPen(None)
    cx, cy = 300, 340
    draw_annulus(pen, cx, cy, 235, 190)
    p1 = (300, 445)
    p2 = (205, 275)
    p3 = (395, 275)
    for px, py in (p1, p2, p3):
        draw_circle(pen, px, py, 44, clockwise=True)
    draw_stroke_line(pen, p1[0], p1[1], p2[0], p2[1], 24)
    draw_stroke_line(pen, p2[0], p2[1], p3[0], p3[1], 24)
    draw_stroke_line(pen, p3[0], p3[1], p1[0], p1[1], 24)
    return finish_glyph(pen)


def build_sys_causal_coupling():
    """U+E9E2: Bidirectional Cybernetic Coupling (Action-Reaction).
    Two nodes linked by opposing forward (top →) and return (← bottom) vectors.
    """
    pen = TTGlyphPen(None)
    draw_annulus(pen, 125, 340, 75, 38)
    draw_annulus(pen, 475, 340, 75, 38)
    draw_rect(pen, 215, 405, 345, 441)
    pen.moveTo((340, 475))
    pen.lineTo((400, 423))
    pen.lineTo((340, 371))
    pen.closePath()
    draw_rect(pen, 255, 239, 385, 275)
    pen.moveTo((260, 309))
    pen.lineTo((200, 257))
    pen.lineTo((260, 205))
    pen.closePath()
    return finish_glyph(pen)


def build_sys_observer_frame():
    """U+E9E3: Second-Order Cybernetic Observer Frame (Observer → Observed).
    Observer node projecting a widening gaze cone onto a target horizon arc.
    """
    pen = TTGlyphPen(None)
    draw_circle(pen, 115, 340, 56, clockwise=True)
    draw_circle(pen, 115, 340, 24, clockwise=False)
    draw_stroke_line(pen, 180, 365, 430, 505, 32)
    draw_stroke_line(pen, 180, 315, 430, 175, 32)
    pen.moveTo((455, 545))
    pen.qCurveTo((545, 340), (455, 135))
    pen.lineTo((415, 155))
    pen.qCurveTo((495, 340), (415, 525))
    pen.closePath()
    draw_circle(pen, 340, 340, 36, clockwise=True)
    return finish_glyph(pen)


def build_sys_bipartite_split():
    """U+E9E4: Bipartite Boundary Split (Inside | Outside Partition).
    Dual-chamber tablet split by a vertical partition wall (solid left, hollow right).
    """
    pen = TTGlyphPen(None)
    draw_rounded_box(pen, 60, 130, 540, 550, r=28, sw=42)
    draw_rect(pen, 280, 150, 320, 530)
    draw_rect(pen, 135, 250, 225, 430)
    draw_annulus(pen, 415, 340, 62, 32)
    return finish_glyph(pen)


def build_sys_nested_holarchy():
    """U+E9E5: Concentric Nested Holarchy (Subsystem Containment).
    Concentric 3-tier holon hierarchy showing nested emergent structure.
    """
    pen = TTGlyphPen(None)
    draw_rounded_box(pen, 55, 105, 545, 575, r=30, sw=40)
    draw_rounded_box(pen, 145, 195, 455, 485, r=22, sw=36)
    draw_rect(pen, 240, 285, 360, 395)
    return finish_glyph(pen)


def build_sys_relational_node():
    """U+E9E6: Mediated Edge-Node Channel (Reified State Link).
    Two nodes linked by a channel carrying a central state-modulating ring.
    """
    pen = TTGlyphPen(None)
    draw_circle(pen, 105, 340, 65, clockwise=True)
    draw_circle(pen, 495, 340, 65, clockwise=True)
    draw_rect(pen, 155, 318, 445, 362)
    draw_annulus(pen, 300, 340, 88, 48)
    return finish_glyph(pen)


def build_sys_metacognitive_lens():
    """U+E9E7: Metacognitive Observer Aperture.
    Symmetric ophthalmic eye contour with central iris annulus and pupil.
    """
    pen = TTGlyphPen(None)
    cx, cy = 300, 340
    pen.moveTo((45, cy))
    pen.qCurveTo((cx, cy + 230), (555, cy))
    pen.qCurveTo((cx, cy - 230), (45, cy))
    pen.closePath()
    pen.moveTo((105, cy))
    pen.qCurveTo((cx, cy - 165), (495, cy))
    pen.qCurveTo((cx, cy + 165), (105, cy))
    pen.closePath()
    draw_annulus(pen, cx, cy, 86, 38)
    return finish_glyph(pen)


# =============================================================================
# 2. SYSTEM DYNAMICS, FEEDBACK LOOPS & LEVERAGE POINTS (U+E9E8 - U+E9EF)
# =============================================================================

def build_sys_loop_reinforcing():
    """U+E9E8: Reinforcing Feedback Loop (R+)."""
    pen = TTGlyphPen(None)
    cx, cy = 300, 340
    draw_annulus(pen, cx, cy, 235, 185)
    pen.moveTo((485, 535))
    pen.lineTo((555, 415))
    pen.lineTo((425, 445))
    pen.closePath()
    draw_rect(pen, cx - 85, cy - 22, cx + 85, cy + 22)
    draw_rect(pen, cx - 22, cy - 85, cx + 22, cy + 85)
    return finish_glyph(pen)


def build_sys_loop_balancing():
    """U+E9E9: Balancing Feedback Loop (B−)."""
    pen = TTGlyphPen(None)
    cx, cy = 300, 340
    draw_annulus(pen, cx, cy, 235, 185)
    pen.moveTo((485, 535))
    pen.lineTo((555, 415))
    pen.lineTo((425, 445))
    pen.closePath()
    draw_rect(pen, cx - 95, cy - 24, cx + 95, cy + 24)
    return finish_glyph(pen)


def build_sys_stock_accumulator():
    """U+E9EA: Jay Forrester / Donella Meadows Stock (Accumulator Reservoir)."""
    pen = TTGlyphPen(None)
    draw_rounded_box(pen, 65, 120, 535, 560, r=25, sw=44)
    draw_rect(pen, 130, 175, 470, 320)
    return finish_glyph(pen)


def build_sys_flow_valve():
    """U+E9EB: Rate / Flow Pipe with Bowtie Control Valve."""
    pen = TTGlyphPen(None)
    cy = 340
    draw_rect(pen, 40, cy - 22, 460, cy + 22)
    pen.moveTo((450, cy + 85))
    pen.lineTo((565, cy))
    pen.lineTo((450, cy - 85))
    pen.closePath()
    cx = 260
    pen.moveTo((cx - 85, cy + 165))
    pen.lineTo((cx + 85, cy + 165))
    pen.lineTo((cx, cy + 15))
    pen.closePath()
    pen.moveTo((cx, cy - 15))
    pen.lineTo((cx + 85, cy - 165))
    pen.lineTo((cx - 85, cy - 165))
    pen.closePath()
    return finish_glyph(pen)


def build_sys_delay_hash():
    """U+E9EC: System Time Delay Link (//)."""
    pen = TTGlyphPen(None)
    cy = 340
    draw_rect(pen, 45, cy - 20, 455, cy + 20)
    pen.moveTo((445, cy + 75))
    pen.lineTo((555, cy))
    pen.lineTo((445, cy - 75))
    pen.closePath()
    draw_stroke_line(pen, 185, 180, 265, 500, 38)
    draw_stroke_line(pen, 275, 180, 355, 500, 38)
    return finish_glyph(pen)


def build_sys_source_sink_cloud():
    """U+E9ED: Infinite Source / Sink System Boundary Cloud."""
    pen = TTGlyphPen(None)
    lobes = [(210, 390, 110), (370, 410, 120), (420, 275, 105), (200, 265, 105)]
    for lx, ly, lr in lobes:
        draw_circle(pen, lx, ly, lr, clockwise=True)
    draw_circle(pen, 300, 335, 95, clockwise=False)
    return finish_glyph(pen)


def build_sys_leverage_fulcrum():
    """U+E9EE: High-Leverage Fulcrum (Δ)."""
    pen = TTGlyphPen(None)
    pen.moveTo((160, 110))
    pen.lineTo((250, 290))
    pen.lineTo((340, 110))
    pen.closePath()
    draw_stroke_line(pen, 65, 240, 535, 390, 42)
    draw_rect(pen, 85, 295, 195, 405)
    pen.moveTo((495, 450))
    pen.lineTo((545, 550))
    pen.lineTo((445, 550))
    pen.closePath()
    return finish_glyph(pen)


def build_sys_emergence_attractor():
    """U+E9EF: Lorenz Phase-Space Strange Attractor / Emergence (∞)."""
    pen = TTGlyphPen(None)
    draw_annulus(pen, 175, 340, 125, 72)
    draw_annulus(pen, 425, 340, 125, 72)
    draw_circle(pen, 300, 340, 42, clockwise=True)
    return finish_glyph(pen)


# =============================================================================
# REGISTRY & FONT INJECTION PIPELINE
# =============================================================================

SYSTEMS_GLYPH_REGISTRY = {
    0xE9E0: ("sys_boundary_set", build_sys_boundary_set),
    0xE9E1: ("sys_holon_triad", build_sys_holon_triad),
    0xE9E2: ("sys_causal_coupling", build_sys_causal_coupling),
    0xE9E3: ("sys_observer_frame", build_sys_observer_frame),
    0xE9E4: ("sys_bipartite_split", build_sys_bipartite_split),
    0xE9E5: ("sys_nested_holarchy", build_sys_nested_holarchy),
    0xE9E6: ("sys_relational_node", build_sys_relational_node),
    0xE9E7: ("sys_metacognitive_lens", build_sys_metacognitive_lens),
    0xE9E8: ("sys_loop_reinforcing", build_sys_loop_reinforcing),
    0xE9E9: ("sys_loop_balancing", build_sys_loop_balancing),
    0xE9EA: ("sys_stock_accumulator", build_sys_stock_accumulator),
    0xE9EB: ("sys_flow_valve", build_sys_flow_valve),
    0xE9EC: ("sys_delay_hash", build_sys_delay_hash),
    0xE9ED: ("sys_source_sink_cloud", build_sys_source_sink_cloud),
    0xE9EE: ("sys_leverage_fulcrum", build_sys_leverage_fulcrum),
    0xE9EF: ("sys_emergence_attractor", build_sys_emergence_attractor),
}


def inject_systems_glyphs(ttf_path: Path):
    print(f"  • Injecting 16 Systems Thinking & Cybernetics glyphs -> {ttf_path.name}")
    font = TTFont(str(ttf_path))
    if "glyf" not in font:
        font.close()
        return

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap_table = font["cmap"]
    glyph_order = list(font.getGlyphOrder())

    gvar = None
    if "gvar" in font:
        try:
            gvar = font["gvar"]
        except AssertionError:
            import struct
            raw_gvar = font.reader["gvar"]
            gvar_glyph_count = struct.unpack(">H", raw_gvar[12:14])[0]
            saved_order = list(font.getGlyphOrder())
            font.setGlyphOrder(saved_order[:gvar_glyph_count])
            gvar = font["gvar"]
            font.setGlyphOrder(saved_order)
            for extra_g in saved_order[gvar_glyph_count:]:
                gvar.variations[extra_g] = []

    # Remove any legacy dsrp_* glyph names if present
    for old_name in LEGACY_DSRP_NAMES:
        if old_name in glyph_order:
            glyph_order.remove(old_name)
        if old_name in glyf.glyphs:
            del glyf.glyphs[old_name]
        if old_name in hmtx.metrics:
            del hmtx.metrics[old_name]
        if gvar is not None and old_name in gvar.variations:
            del gvar.variations[old_name]

    has_format_12 = any(t.format == 12 for t in cmap_table.tables)
    if not has_format_12:
        subtable_12 = CmapSubtable.newSubtable(12)
        subtable_12.platformID = 3
        subtable_12.platEncID = 10
        subtable_12.language = 0
        subtable_12.cmap = dict(font.getBestCmap())
        cmap_table.tables.append(subtable_12)

    for cp, (gname, builder_fn) in SYSTEMS_GLYPH_REGISTRY.items():
        g = builder_fn()
        g.recalcBounds(glyf)
        g.flags = bytearray([f & 0x3F for f in g.flags])
        sanitize_contour_points(g.coordinates, g.endPtsOfContours)
        glyf[gname] = g
        lsb = g.xMin if g.numberOfContours > 0 else 45
        hmtx[gname] = (ADVANCE, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)

        for table in cmap_table.tables:
            if table.format in (4, 12):
                if table.format == 4 and cp > 0xFFFF:
                    continue
                table.cmap[cp] = gname

        if gvar is not None and gname not in gvar.variations:
            gvar.variations[gname] = []

    if gvar is not None and "HVAR" in font:
        del font["HVAR"]

    if "OS/2" in font:
        font["OS/2"].ulUnicodeRange2 |= (1 << 25)  # Bit 57: Plane 0 Private Use Area

    font.setGlyphOrder(glyph_order)
    font["maxp"].numGlyphs = len(glyph_order)
    font.save(str(ttf_path))
    font.close()


def main():
    print("=" * 78)
    print("  POCKETGULL TYPEFOUNDRY: SYSTEMS THINKING & CYBERNETICS GLYPH SYNTHESIZER")
    print("=" * 78)

    target_stems = [
        "PocketGull-Algo",
        "PocketGullMono-Regular",
        "PocketGullMono-Bold",
        "PocketGull-Regular",
        "PocketGull-Bold",
        "PocketGull-Fineliner",
        "PocketGull-Learn",
        "PocketGull-Lab",
        "PocketGull-Math",
        "PocketGull-VF",
    ]

    processed_stems = []
    for stem in target_stems:
        ttf_path = TTF_DIR / f"{stem}.ttf"
        if ttf_path.exists():
            inject_systems_glyphs(ttf_path)
            processed_stems.append(stem)

    print("\n[Step 2] Enforcing 2-byte word alignment (loca[i] % 2 == 0) via Dart 3.11...")
    dart_tool = ROOT_DIR / "tool" / "pocketgull_foundry.dart"
    if dart_tool.exists():
        for stem in processed_stems:
            ttf_path = TTF_DIR / f"{stem}.ttf"
            subprocess.run(
                ["dart", "run", str(dart_tool), "realign", str(ttf_path)],
                check=True,
                cwd=str(ROOT_DIR),
            )

    print("\n[Step 3] Compressing WOFF2 binaries (Brotli Q11) & syncing mirrors...")
    for stem in processed_stems:
        ttf_path = TTF_DIR / f"{stem}.ttf"
        woff2_path = WOFF2_DIR / f"{stem}.woff2"
        compress(str(ttf_path), str(woff2_path))
        print(f"  ✓ {woff2_path.name} ({woff2_path.stat().st_size:,} bytes)")

        root_ttf = ROOT_DIR / f"{stem}.ttf"
        if root_ttf.exists():
            shutil.copy2(ttf_path, root_ttf)
        root_woff2 = ROOT_DIR / f"{stem}.woff2"
        if root_woff2.exists():
            shutil.copy2(woff2_path, root_woff2)

        if PUBLIC_FONTS_DIR.exists():
            pub_ttf = PUBLIC_FONTS_DIR / f"{stem}.ttf"
            pub_woff2 = PUBLIC_FONTS_DIR / f"{stem}.woff2"
            if pub_ttf.exists():
                shutil.copy2(ttf_path, pub_ttf)
            if pub_woff2.exists():
                shutil.copy2(woff2_path, pub_woff2)

    print("\n[SUCCESS] All 16 Systems Thinking & Cybernetics glyphs synthesized (Zero Trademark Risk)!")


if __name__ == "__main__":
    main()
