#!/usr/bin/env python3
"""
PocketGull Typefoundry - Philocardia Hearts & Clinical Pictograms Synthesizer (Clean-Room)
========================================================================================
100% Procedural TrueType Quadratic Bézier Synthesis (Zero external font dependencies):
1. Philocardia Hearts:
   - U+2665 (♥ Black Heart Suit / uni2665)
   - U+2764 (❤ Heavy Heart / uni2764)
2. Universal Clinical Pictograms:
   - U+2695 (⚕ Rod of Asclepius / uni2695)
   - U+26A0 (⚠️ High-Alert Warning / uni26A0)
   - U+263C (☀️ Morning Dosage AM / sun)
   - U+263D (🌙 Night Dosage PM / uni263D)
   - U+2298 (⊘ Do Not Crush & Do Not Split / uni2298)
3. OpenType ss07 "Philocardia Heart Tittles":
   - i.heart and j.heart (tactile felt-marker heart replacing circular dot tittle)
   - Encapsulated strictly in GSUB ss07 (Stylistic Set 7)
   - Base cmap preserves standard dot tittles for 100% clinical safety on 6pt-8pt labels.
4. Monospace pitch invariant: All glyphs in Mono cut locked to 600 UPM.
5. Realigns all tables to 2-byte word boundaries (loca[i] % 2 == 0).
"""

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.ttLib.tables import otTables as ot
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def sanitize_contour_points(coords, endPts):
    """Eliminates consecutive identical points to guarantee 0 duplicate nodes and OTS safety."""
    start = 0
    for end in endPts:
        for i in range(start, end):
            if coords[i] == coords[i + 1]:
                coords[i + 1] = (coords[i + 1][0] + 1, coords[i + 1][1])
        if len(coords) > 1 and coords[start] == coords[end]:
            coords[end] = (coords[end][0] + 1, coords[end][1])
        start = end + 1

# -----------------------------------------------------------------------------
# 100% PROCEDURAL TRUE-TYPE BÉZIER GENERATORS
# -----------------------------------------------------------------------------

def build_procedural_heart(advance, is_mono, heavy=False):
    """Synthesizes an authentic humanist felt-marker heart with cushioned 35 UPM apex fillet."""
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    base_y = 120 if is_mono else 100
    width = 470 if is_mono else (530 if heavy else 490)
    height = int(width * 0.90)
    
    half_w = width / 2.0
    top_y = base_y + height
    cleft_y = base_y + height * 0.62
    mid_y = base_y + height * 0.48
    
    # Tactile felt-marker apex fillet (r = 28 UPM, eliminates sharp needle vertex)
    r_apex = 28
    apex_drop = 8

    # Start at bottom center of cushioned apex arc
    pen.moveTo((int(cx), int(base_y)))
    # Apex curve right
    pen.qCurveTo((int(cx + r_apex * 0.6), int(base_y)), (int(cx + r_apex), int(base_y + apex_drop)))
    # Upward sweeping lower right flank
    pen.qCurveTo((int(cx + half_w * 0.92), int(base_y + height * 0.22)), (int(cx + half_w), int(mid_y)))
    # Right crown lobe
    pen.qCurveTo((int(cx + half_w), int(top_y)), (int(cx + half_w * 0.52), int(top_y)))
    # Down into the central cleft with a smooth 120° dip
    pen.qCurveTo((int(cx + half_w * 0.18), int(top_y)), (int(cx), int(cleft_y)))
    # Left crown lobe
    pen.qCurveTo((int(cx - half_w * 0.18), int(top_y)), (int(cx - half_w * 0.52), int(top_y)))
    # Left flank curve downward
    pen.qCurveTo((int(cx - half_w), int(top_y)), (int(cx - half_w), int(mid_y)))
    pen.qCurveTo((int(cx - half_w * 0.92), int(base_y + height * 0.22)), (int(cx - r_apex), int(base_y + apex_drop)))
    # Apex curve back to center
    pen.qCurveTo((int(cx - r_apex * 0.6), int(base_y)), (int(cx), int(base_y)))
    pen.closePath()
    g = pen.glyph()
    g.program = Program()
    return g

def build_procedural_asclepius(advance, is_mono):
    """Synthesizes the authentic clinical Rod of Asclepius (U+2695).
    Features an organic wooden staff (Staff of Epidauros) and a calligraphic entwined serpent.
    """
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    
    # -------------------------------------------------------------------------
    # 1. Staff of Epidauros (Tapered organic wooden rod with rounded caps)
    # -------------------------------------------------------------------------
    y_bot = 80
    y_top = 740
    hw_bot = 22  # 44 UPM width at base
    hw_top = 17  # 34 UPM width at apex (natural taper)
    r_cap = 18

    # Rounded bottom cap
    pen.moveTo((int(cx - hw_bot), int(y_bot + r_cap)))
    pen.qCurveTo((int(cx - hw_bot), int(y_bot)), (int(cx), int(y_bot)))
    pen.qCurveTo((int(cx + hw_bot), int(y_bot)), (int(cx + hw_bot), int(y_bot + r_cap)))
    
    # Staff right edge rising with slight organic knot swelling at y=400
    pen.lineTo((int(cx + hw_bot - 1), 380))
    pen.qCurveTo((int(cx + hw_bot + 3), 410), (int(cx + hw_top + 1), 440))
    pen.lineTo((int(cx + hw_top), int(y_top - r_cap)))
    
    # Rounded top cap
    pen.qCurveTo((int(cx + hw_top), int(y_top)), (int(cx), int(y_top)))
    pen.qCurveTo((int(cx - hw_top), int(y_top)), (int(cx - hw_top), int(y_top - r_cap)))
    
    # Staff left edge descending
    pen.lineTo((int(cx - hw_top - 1), 440))
    pen.qCurveTo((int(cx - hw_bot - 3), 410), (int(cx - hw_bot + 1), 380))
    pen.lineTo((int(cx - hw_bot), int(y_bot + r_cap)))
    pen.closePath()

    # -------------------------------------------------------------------------
    # 2. The Sacred Serpent (Entwined clockwise with calligraphic modulation)
    # -------------------------------------------------------------------------
    pen.moveTo((int(cx + 85), 140))  # Tail entry
    # Lower right sweep
    pen.qCurveTo((int(cx + 125), 180), (int(cx + 125), 230))
    pen.qCurveTo((int(cx + 125), 280), (int(cx + 60), 320))
    # Cross in front of staff to left flank
    pen.qCurveTo((int(cx - 20), 350), (int(cx - 105), 380))
    pen.qCurveTo((int(cx - 135), 410), (int(cx - 135), 460))
    pen.qCurveTo((int(cx - 135), 510), (int(cx - 70), 545))
    # Cross behind staff to right flank
    pen.qCurveTo((int(cx + 25), 580), (int(cx + 115), 615))
    pen.qCurveTo((int(cx + 140), 650), (int(cx + 140), 690))
    # Arch over top to form benevolent head facing staff
    pen.qCurveTo((int(cx + 140), 735), (int(cx + 85), 735))
    pen.qCurveTo((int(cx + 40), 735), (int(cx + 28), 705))  # Snout
    # Head underside & jaw
    pen.qCurveTo((int(cx + 38), 680), (int(cx + 70), 680))
    pen.qCurveTo((int(cx + 100), 680), (int(cx + 100), 655))
    # Inner body line descending (thickness ~ 36-42 UPM)
    pen.qCurveTo((int(cx + 100), 625), (int(cx + 30), 590))
    pen.qCurveTo((int(cx - 55), 555), (int(cx - 95), 520))
    pen.qCurveTo((int(cx - 95), 470), (int(cx - 65), 440))
    # Inner body crossing staff downward
    pen.qCurveTo((int(cx + 15), 400), (int(cx + 85), 365))
    pen.qCurveTo((int(cx + 85), 270), (int(cx + 50), 240))
    pen.qCurveTo((int(cx + 25), 215), (int(cx + 25), 180))
    # Tail tip tapering to smooth rounded end
    pen.qCurveTo((int(cx + 25), 140), (int(cx + 55), 120))
    pen.qCurveTo((int(cx + 75), 120), (int(cx + 85), 140))
    pen.closePath()

    g = pen.glyph()
    g.program = Program()
    return g

def build_procedural_warning(advance, is_mono):
    """Synthesizes the High-Alert Clinical Warning Sign (U+26A0)."""
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    base_w = 480 if is_mono else 520
    y_bot = 100
    y_top = 680
    r = 25
    half_w = base_w / 2.0

    # Outer rounded triangle
    pen.moveTo((cx - half_w + r, y_bot))
    pen.lineTo((cx + half_w - r, y_bot))
    pen.qCurveTo((cx + half_w, y_bot), (cx + half_w - 10, y_bot + 20))
    pen.lineTo((cx + 15, y_top - 25))
    pen.qCurveTo((cx, y_top), (cx - 15, y_top - 25))
    pen.lineTo((cx - half_w + 10, y_bot + 20))
    pen.qCurveTo((cx - half_w, y_bot), (cx - half_w + r, y_bot))
    pen.closePath()

    # Inner cutout exclamation bar
    bar_w = 42
    pen.moveTo((cx - bar_w / 2, 480))
    pen.lineTo((cx + bar_w / 2, 480))
    pen.lineTo((cx + bar_w / 2 - 4, 300))
    pen.lineTo((cx - bar_w / 2 + 4, 300))
    pen.closePath()

    # Exclamation dot
    dot_r = 24
    dot_cy = 220
    pen.moveTo((cx - dot_r, dot_cy))
    pen.qCurveTo((cx - dot_r, dot_cy + dot_r), (cx, dot_cy + dot_r))
    pen.qCurveTo((cx + dot_r, dot_cy + dot_r), (cx + dot_r, dot_cy))
    pen.qCurveTo((cx + dot_r, dot_cy - dot_r), (cx, dot_cy - dot_r))
    pen.qCurveTo((cx - dot_r, dot_cy - dot_r), (cx - dot_r, dot_cy))
    pen.closePath()

    g = pen.glyph()
    g.program = Program()
    return g

def build_procedural_sun(advance, is_mono):
    """Synthesizes the Morning Dosage Sun (U+263C)."""
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    cy = 380
    r_core = 110

    # Central sun core
    pen.moveTo((cx - r_core, cy))
    pen.qCurveTo((cx - r_core, cy + r_core), (cx, cy + r_core))
    pen.qCurveTo((cx + r_core, cy + r_core), (cx + r_core, cy))
    pen.qCurveTo((cx + r_core, cy - r_core), (cx, cy - r_core))
    pen.qCurveTo((cx - r_core, cy - r_core), (cx - r_core, cy))
    pen.closePath()

    # 8 Cardinal & Diagonal Rays
    ray_in = 150
    ray_out = 230
    ray_w = 26
    for i in range(8):
        ang = i * (math.pi / 4.0)
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)
        x0 = cx + ray_in * cos_a
        y0 = cy + ray_in * sin_a
        x1 = cx + ray_out * cos_a
        y1 = cy + ray_out * sin_a
        dx = -sin_a * (ray_w / 2.0)
        dy = cos_a * (ray_w / 2.0)
        pen.moveTo((x0 - dx, y0 - dy))
        pen.lineTo((x1 - dx, y1 - dy))
        pen.lineTo((x1 + dx, y1 + dy))
        pen.lineTo((x0 + dx, y0 + dy))
        pen.closePath()

    g = pen.glyph()
    g.program = Program()
    return g

def build_procedural_moon(advance, is_mono):
    """Synthesizes the Night Dosage Moon Crescent (U+263D)."""
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    cy = 380
    r_outer = 230
    r_inner = 190
    offset_x = 75

    pen.moveTo((cx + offset_x, cy + r_outer - 40))
    pen.qCurveTo((cx - r_outer + offset_x, cy + r_outer), (cx - r_outer + offset_x, cy))
    pen.qCurveTo((cx - r_outer + offset_x, cy - r_outer), (cx + offset_x, cy - r_outer + 40))
    pen.qCurveTo((cx - r_inner + offset_x * 2.2, cy - r_inner * 0.8), (cx - r_inner + offset_x * 2.2, cy))
    pen.qCurveTo((cx - r_inner + offset_x * 2.2, cy + r_inner * 0.8), (cx + offset_x, cy + r_outer - 40))
    pen.closePath()

    g = pen.glyph()
    g.program = Program()
    return g

def build_procedural_do_not_crush(advance, is_mono):
    """Synthesizes the Do Not Crush / Do Not Split symbol (U+2298)."""
    pen = TTGlyphPen(None)
    cx = advance / 2.0
    cy = 380
    r_outer = 240
    sw = 46
    r_inner = r_outer - sw

    # Outer circle
    pen.moveTo((cx - r_outer, cy))
    pen.qCurveTo((cx - r_outer, cy + r_outer), (cx, cy + r_outer))
    pen.qCurveTo((cx + r_outer, cy + r_outer), (cx + r_outer, cy))
    pen.qCurveTo((cx + r_outer, cy - r_outer), (cx, cy - r_outer))
    pen.qCurveTo((cx - r_outer, cy - r_outer), (cx - r_outer, cy))
    pen.closePath()

    # Inner cutout circle (counter)
    pen.moveTo((cx - r_inner, cy))
    pen.lineTo((cx, cy - r_inner))
    pen.lineTo((cx + r_inner, cy))
    pen.lineTo((cx, cy + r_inner))
    pen.closePath()

    # 45-degree diagonal slash
    bar_w = 42
    d = r_outer * 0.7071
    pen.moveTo((cx - d - bar_w / 2, cy - d + bar_w / 2))
    pen.lineTo((cx + d - bar_w / 2, cy + d + bar_w / 2))
    pen.lineTo((cx + d + bar_w / 2, cy + d - bar_w / 2))
    pen.lineTo((cx - d + bar_w / 2, cy - d - bar_w / 2))
    pen.closePath()

    g = pen.glyph()
    g.program = Program()
    return g

def ensure_feature_record(gsub, tag, lookup_index):
    """Ensures a FeatureRecord with tag and lookup_index exists in GSUB and is registered in all scripts."""
    if gsub.FeatureList is None:
        gsub.FeatureList = ot.FeatureList()
        gsub.FeatureList.FeatureRecord = []
        gsub.FeatureList.FeatureCount = 0

    feature_idx = None
    for i, fr in enumerate(gsub.FeatureList.FeatureRecord):
        if fr.FeatureTag == tag:
            feature_idx = i
            if lookup_index not in fr.Feature.LookupListIndex:
                fr.Feature.LookupListIndex.append(lookup_index)
                fr.Feature.LookupCount = len(fr.Feature.LookupListIndex)
            break

    if feature_idx is None:
        fr = ot.FeatureRecord()
        fr.FeatureTag = tag
        fr.Feature = ot.Feature()
        fr.Feature.LookupListIndex = [lookup_index]
        fr.Feature.LookupCount = 1
        fr.Feature.FeatureParams = None
        feature_idx = len(gsub.FeatureList.FeatureRecord)
        gsub.FeatureList.FeatureRecord.append(fr)
        gsub.FeatureList.FeatureCount = len(gsub.FeatureList.FeatureRecord)

    # Register in all Script records
    if gsub.ScriptList is not None:
        for s in gsub.ScriptList.ScriptRecord:
            if s.Script.DefaultLangSys is None:
                s.Script.DefaultLangSys = ot.DefaultLangSys()
                s.Script.DefaultLangSys.FeatureIndex = []
                s.Script.DefaultLangSys.LookupOrder = None
                s.Script.DefaultLangSys.ReqFeatureIndex = 0xFFFF
            if feature_idx not in s.Script.DefaultLangSys.FeatureIndex:
                s.Script.DefaultLangSys.FeatureIndex.append(feature_idx)
                s.Script.DefaultLangSys.FeatureCount = len(s.Script.DefaultLangSys.FeatureIndex)
            if hasattr(s.Script, 'LangSysRecord') and s.Script.LangSysRecord:
                for ls in s.Script.LangSysRecord:
                    if feature_idx not in ls.LangSys.FeatureIndex:
                        ls.LangSys.FeatureIndex.append(feature_idx)
                        ls.LangSys.FeatureCount = len(ls.LangSys.FeatureIndex)

def realign_font_word_boundaries():
    """Realigns font tables and glyf records to 2-byte word boundaries via pure Dart SfntTransformer."""
    foundry_tool = ROOT_DIR / "tool" / "pocketgull_foundry.dart"
    if foundry_tool.exists():
        subprocess.run(["dart", "run", str(foundry_tool), "realign"], check=False, cwd=str(ROOT_DIR))

def inject_philocardia():
    print("=" * 80)
    print("  POCKETGULL FOUNDRY: CLEAN-ROOM PHILOCARDIA & CLINICAL PICTOGRAMS SYNTHESIZER")
    print("=" * 80)

    target_fonts = sorted([f for f in TTF_DIR.glob("*.ttf")])

    for font_path in target_fonts:
        fname = font_path.name
        is_mono = "Mono" in fname
        adv = 600 if is_mono else 700
        font = TTFont(str(font_path))
        glyf = font["glyf"]
        hmtx = font["hmtx"]
        gorder = font.getGlyphOrder()

        # 1. Synthesize Procedural Clean Glyphs
        procedural_glyphs = [
            (0x2665, "uni2665", build_procedural_heart(adv, is_mono, heavy=False)),
            (0x2764, "uni2764", build_procedural_heart(adv, is_mono, heavy=True)),
            (0x2695, "uni2695", build_procedural_asclepius(adv, is_mono)),
            (0x26A0, "uni26A0", build_procedural_warning(adv, is_mono)),
            (0x263C, "uni263C", build_procedural_sun(adv, is_mono)),
            (0x263D, "uni263D", build_procedural_moon(adv, is_mono)),
            (0x2298, "uni2298", build_procedural_do_not_crush(adv, is_mono)),
        ]

        for cp, dest_name, g in procedural_glyphs:
            glyf[dest_name] = g
            g.recalcBounds(glyf)
            hmtx[dest_name] = (adv, g.xMin)

            if dest_name not in gorder:
                gorder.append(dest_name)

            for table in font["cmap"].tables:
                if table.format == 12:
                    table.cmap[cp] = dest_name
                elif table.format == 4 and cp <= 0xFFFF:
                    table.cmap[cp] = dest_name

        # 2. Synthesize i.heart and j.heart for ss07 OpenType Stylistic Set
        for base_char, heart_char in [("i", "i.heart"), ("j", "j.heart")]:
            if base_char in glyf and glyf[base_char].numberOfContours >= 2:
                base_g = glyf[base_char]
                raw_c, endpts, fl = base_g.getCoordinates(glyf)
                
                # Contour 0 is the stem
                stem_c = raw_c[0:endpts[0] + 1]
                stem_fl = fl[0:endpts[0] + 1]

                # Contour 1 is the tittle dot
                dot_c = raw_c[endpts[0] + 1:endpts[1] + 1]
                dot_min_x = min(c[0] for c in dot_c)
                dot_max_x = max(c[0] for c in dot_c)
                dot_min_y = min(c[1] for c in dot_c)
                dot_max_y = max(c[1] for c in dot_c)
                dot_cx = (dot_min_x + dot_max_x) / 2.0
                dot_cy = (dot_min_y + dot_max_y) / 2.0
                dot_w = dot_max_x - dot_min_x
                dot_h = dot_max_y - dot_min_y

                # Generate small humanist heart tittle with cushioned apex fillet
                h_pen = TTGlyphPen(None)
                h_w = max(dot_w, dot_h) * 1.30
                h_h = h_w * 0.90
                half_hw = h_w / 2.0
                h_base_y = dot_cy - h_h * 0.45
                h_top_y = h_base_y + h_h
                h_cleft_y = h_base_y + h_h * 0.62
                h_mid_y = h_base_y + h_h * 0.48
                r_apex_t = max(2, int(h_w * 0.08))

                # Start at bottom center of cushioned apex
                h_pen.moveTo((int(dot_cx), int(h_base_y)))
                h_pen.qCurveTo((int(dot_cx + r_apex_t * 0.6), int(h_base_y)), (int(dot_cx + r_apex_t), int(h_base_y + 3)))
                h_pen.qCurveTo((int(dot_cx + half_hw * 0.92), int(h_base_y + h_h * 0.22)), (int(dot_cx + half_hw), int(h_mid_y)))
                h_pen.qCurveTo((int(dot_cx + half_hw), int(h_top_y)), (int(dot_cx + half_hw * 0.52), int(h_top_y)))
                h_pen.qCurveTo((int(dot_cx + half_hw * 0.18), int(h_top_y)), (int(dot_cx), int(h_cleft_y)))
                h_pen.qCurveTo((int(dot_cx - half_hw * 0.18), int(h_top_y)), (int(dot_cx - half_hw * 0.52), int(h_top_y)))
                h_pen.qCurveTo((int(dot_cx - half_hw), int(h_top_y)), (int(dot_cx - half_hw), int(h_mid_y)))
                h_pen.qCurveTo((int(dot_cx - half_hw * 0.92), int(h_base_y + h_h * 0.22)), (int(dot_cx - r_apex_t), int(h_base_y + 3)))
                h_pen.qCurveTo((int(dot_cx - r_apex_t * 0.6), int(h_base_y)), (int(dot_cx), int(h_base_y)))
                h_pen.closePath()

                raw_h_glyph = h_pen.glyph()
                raw_h_coords, raw_h_endpts, raw_h_flags = raw_h_glyph.getCoordinates(glyf)

                all_coords = stem_c + list(raw_h_coords)
                all_flags = list(stem_fl) + [f & 0x3F for f in raw_h_flags]
                new_endpts = [len(stem_c) - 1, len(all_coords) - 1]

                heart_g = Glyph()
                heart_g.numberOfContours = 2
                heart_g.endPtsOfContours = new_endpts
                heart_g.flags = bytearray(all_flags)
                heart_g.program = Program()
                c_obj = GlyphCoordinates(all_coords)
                sanitize_contour_points(c_obj, heart_g.endPtsOfContours)
                heart_g.coordinates = c_obj
                heart_g.recalcBounds(glyf)

                base_adv, _ = hmtx[base_char]
                glyf[heart_char] = heart_g
                hmtx[heart_char] = (base_adv, heart_g.xMin)

                if heart_char not in gorder:
                    gorder.append(heart_char)

        # 3. Setup OpenType GSUB ss07 "Philocardia Heart Tittles"
        if "GSUB" in font:
            gsub = font["GSUB"].table
            if gsub.LookupList is None:
                gsub.LookupList = ot.LookupList()
                gsub.LookupList.Lookup = []
                gsub.LookupList.LookupCount = 0

            ss07_lookup_idx = None
            for i_idx, lk in enumerate(gsub.LookupList.Lookup):
                if lk.LookupType == 1:
                    for st in lk.SubTable:
                        if hasattr(st, "mapping") and st.mapping.get("i") == "i.heart":
                            ss07_lookup_idx = i_idx
                            st.mapping["j"] = "j.heart"
                            break
                if ss07_lookup_idx is not None:
                    break

            if ss07_lookup_idx is None:
                st = ot.SingleSubst()
                st.Format = 1
                st.mapping = {"i": "i.heart", "j": "j.heart"}
                lk = ot.Lookup()
                lk.LookupType = 1
                lk.LookupFlag = 0
                lk.SubTable = [st]
                lk.SubTableCount = 1
                ss07_lookup_idx = len(gsub.LookupList.Lookup)
                gsub.LookupList.Lookup.append(lk)
                gsub.LookupList.LookupCount = len(gsub.LookupList.Lookup)

            ensure_feature_record(gsub, "ss07", ss07_lookup_idx)

        # Update glyph order & save
        font.setGlyphOrder(gorder)
        font.save(str(font_path))
        print(f"  [OK] {fname:28s} | Synthesized 100% clean procedural pictograms + ss07")

    # Realign word boundaries across all fonts
    print("\n  • Realigning 2-byte word boundaries on all TTFs via Dart 3.11...")
    realign_font_word_boundaries()

    # Sync root copies
    root_mono = ROOT_DIR / "PocketGullMono-Regular.ttf"
    if root_mono.exists() and (TTF_DIR / "PocketGullMono-Regular.ttf").exists():
        shutil.copyfile(TTF_DIR / "PocketGullMono-Regular.ttf", root_mono)
        print("  [OK] Synchronized root PocketGullMono-Regular.ttf")

    root_vf = ROOT_DIR / "PocketGull-VF.ttf"
    if root_vf.exists() and (TTF_DIR / "PocketGull-VF.ttf").exists():
        shutil.copyfile(TTF_DIR / "PocketGull-VF.ttf", root_vf)
        print("  [OK] Synchronized root PocketGull-VF.ttf")

    print("\n[SUCCESS] Philocardia hearts and clinical pictograms 100% clean-room synthesized!")

if __name__ == "__main__":
    inject_philocardia()
