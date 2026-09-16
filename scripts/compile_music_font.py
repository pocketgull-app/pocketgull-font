#!/usr/bin/env python3
"""
PocketGull Typefoundry: Master Music & Audiology Font Compiler
==============================================================
Compiles 'PocketGull-Music.ttf' and 'PocketGull-Music.woff2'
World's First Humanist Clinical Music Therapy, Audiology Telemetry
& W3C SMuFL (Standard Music Font Layout) Typeface
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

SRC_REGULAR = os.path.join(TTF_DIR, "PocketGull-Regular.ttf")
SRC_BOLD = os.path.join(TTF_DIR, "PocketGull-Bold.ttf")

OUT_TTF = os.path.join(TTF_DIR, "PocketGull-Music.ttf")
OUT_WOFF2 = os.path.join(WOFF2_DIR, "PocketGull-Music.woff2")
ROOT_TTF = os.path.join(ROOT_DIR, "PocketGull-Music.ttf")
ROOT_WOFF2 = os.path.join(ROOT_DIR, "PocketGull-Music.woff2")

DEFAULT_ADV = 600
STROKE_W = 68
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

def draw_rotated_ellipse(pen, cx, cy, rx, ry, angle_deg, clockwise=True):
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    pts = []
    num_pts = 8
    sign = -1 if clockwise else 1
    for i in range(num_pts):
        th = sign * 2 * math.pi * i / num_pts
        x_local = rx * math.cos(th)
        y_local = ry * math.sin(th)
        x_rot = cx + int(x_local * cos_a - y_local * sin_a)
        y_rot = cy + int(x_local * sin_a + y_local * cos_a)
        pts.append((x_rot, y_rot))
    pen.moveTo(pts[0])
    for pt in pts[1:]:
        pen.lineTo(pt)
    pen.closePath()

def build_music_font():
    print("=" * 76)
    print("  POCKETGULL TYPEFOUNDRY: CLINICAL MUSIC & SMuFL COMPILER")
    print("=" * 76)

    if not os.path.isfile(SRC_REGULAR):
        print(f"[ERROR] Master font missing: {SRC_REGULAR}")
        sys.exit(1)

    print("\n1. Loading master regular font source...")
    font = TTFont(SRC_REGULAR)

    glyf = font["glyf"]
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    glyph_order = list(font.getGlyphOrder())

    def register_glyph(gname, codepoints, pen, adv=DEFAULT_ADV, lsb=None):
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        if lsb is None:
            lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (adv, lsb)
        if gname not in glyph_order:
            glyph_order.append(gname)
        for cp in codepoints:
            cmap[cp] = gname

    print("\n2. Synthesizing W3C SMuFL Standard Clefs & Staves...")

    # Glyph 1: 5-Line Staff Raster Segment U+E014
    pen = TTGlyphPen(None)
    # 5 horizontal lines from y = 100 to y = 580 (spacing 120 UPM)
    staff_w = 40  # Staff line thickness
    for line_idx in range(5):
        y_pos = 100 + line_idx * 120
        draw_rect(pen, 0, y_pos - staff_w // 2, 600, y_pos + staff_w // 2)
    register_glyph("staff_5lines", [0xE014], pen, 600, 0)

    # Glyph 2: Single Barline U+E030 & U+1D100
    pen = TTGlyphPen(None)
    draw_rect(pen, 280 - hw, 100, 280 + hw, 580)
    register_glyph("barline_single", [0xE030, 0x1D100], pen, 560, 246)

    # Glyph 2b: Double Barline U+E031 & U+1D101
    pen = TTGlyphPen(None)
    draw_rect(pen, 200, 100, 200 + STROKE_W, 580)
    draw_rect(pen, 320, 100, 320 + STROKE_W, 580)
    register_glyph("barline_double", [0xE031, 0x1D101], pen, 560, 200)

    # Glyph 2c: Final Barline U+E032 & U+1D102
    pen = TTGlyphPen(None)
    draw_rect(pen, 200, 100, 200 + STROKE_W, 580)
    draw_rect(pen, 340, 100, 480, 580)  # Thick bar
    register_glyph("barline_final", [0xE032, 0x1D102], pen, 560, 200)

    # Glyph 2d: Repeat Left (Start Repeat) U+E040 & U+1D106
    pen = TTGlyphPen(None)
    draw_rect(pen, 140, 100, 240, 580)  # Thick outer bar
    draw_rect(pen, 290, 100, 290 + STROKE_W, 580)  # Thin inner bar
    draw_circle(pen, 390, 280, 36, clockwise=True)  # Repeat dot in space 2
    draw_circle(pen, 390, 400, 36, clockwise=True)  # Repeat dot in space 3
    register_glyph("barline_repeat_left", [0xE040, 0x1D106], pen, 560, 140)

    # Glyph 2e: Repeat Right (End Repeat) U+E041 & U+1D107
    pen = TTGlyphPen(None)
    draw_circle(pen, 170, 280, 36, clockwise=True)  # Repeat dot in space 2
    draw_circle(pen, 170, 400, 36, clockwise=True)  # Repeat dot in space 3
    draw_rect(pen, 270, 100, 270 + STROKE_W, 580)  # Thin inner bar
    draw_rect(pen, 340, 100, 440, 580)  # Thick outer bar
    register_glyph("barline_repeat_right", [0xE041, 0x1D107], pen, 560, 170)

    # Glyph 2f: Note Stem U+E210
    pen = TTGlyphPen(None)
    draw_rect(pen, 280 - hw, 100, 280 + hw, 680)
    register_glyph("stem", [0xE210], pen, 560, 250)

    # Glyph 2g: Beam Segment (Crossbar) U+E8E0
    pen = TTGlyphPen(None)
    draw_rect(pen, 0, 300, 600, 390)
    register_glyph("beam_segment", [0xE8E0], pen, 600, 0)

    # Glyph 2h: Common Time Signature U+E08A & U+1D134
    pen = TTGlyphPen(None)
    pen.moveTo((420, 470))
    pen.qCurveTo((300, 500), (220, 430))
    pen.qCurveTo((150, 340), (220, 250))
    pen.qCurveTo((300, 180), (420, 210))
    pen.lineTo((410, 260))
    pen.qCurveTo((320, 240), (270, 290))
    pen.qCurveTo((220, 340), (270, 390))
    pen.qCurveTo((320, 440), (410, 420))
    pen.closePath()
    register_glyph("time_sig_common", [0xE08A, 0x1D134], pen, 560, 150)

    # Glyph 2i: Cut Time (Alla Breve) Signature U+E08B & U+1D135
    pen = TTGlyphPen(None)
    pen.moveTo((420, 470))
    pen.qCurveTo((300, 500), (220, 430))
    pen.qCurveTo((150, 340), (220, 250))
    pen.qCurveTo((300, 180), (420, 210))
    pen.lineTo((410, 260))
    pen.qCurveTo((320, 240), (270, 290))
    pen.qCurveTo((220, 340), (270, 390))
    pen.qCurveTo((320, 440), (410, 420))
    pen.closePath()
    draw_rect(pen, 280 - hw, 140, 280 + hw, 540)  # Vertical cut bar
    register_glyph("time_sig_cut", [0xE08B, 0x1D135], pen, 560, 150)

    # Glyph 2j-s: SMuFL Time Signature Digits 0-9 (U+E080 - U+E089)
    digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for d_idx, d_name in enumerate(digit_names):
        pen = TTGlyphPen(glyphSet=glyf)
        scale_f = 0.34
        orig_w = hmtx.metrics[d_name][0] if d_name in hmtx.metrics else 560
        target_w = int(orig_w * scale_f)
        pen.addComponent(d_name, (scale_f, 0, 0, scale_f, 40, 100))
        register_glyph(f"time_sig_{d_idx}", [0xE080 + d_idx], pen, max(360, target_w + 80), 40)

    # Glyph 2t-z: Pre-Composed Two-Story Stacked Time Signatures (PUA U+E940 - U+E947)
    # Strictly conforms to Gould's Rule: NO FRACTION BAR / SLASH.
    # Numerator occupies staff spaces 3-4 (y=340 to 580); Denominator occupies spaces 1-2 (y=100 to 340).
    stacked_meters = [
        ("time_sig_2_4", [0xE940], "two", "four"),
        ("time_sig_3_4", [0xE941], "three", "four"),
        ("time_sig_4_4", [0xE942], "four", "four"),
        ("time_sig_6_8", [0xE943], "six", "eight"),
        ("time_sig_7_8", [0xE944], "seven", "eight"),
        ("time_sig_9_8", [0xE945], "nine", "eight"),
        ("time_sig_5_4", [0xE946], "five", "four"),
    ]

    for g_name, codepoints, num_d, den_d in stacked_meters:
        pen = TTGlyphPen(glyphSet=glyf)
        s = 0.34
        w_num = (glyf[num_d].xMax - glyf[num_d].xMin) * s
        w_den = (glyf[den_d].xMax - glyf[den_d].xMin) * s
        max_w = max(w_num, w_den)
        adv = int(max(400, max_w + 160))
        mid = adv / 2
        dx_num = int(mid - w_num / 2 - glyf[num_d].xMin * s)
        dx_den = int(mid - w_den / 2 - glyf[den_d].xMin * s)
        pen.addComponent(num_d, (s, 0, 0, s, dx_num, 340))
        pen.addComponent(den_d, (s, 0, 0, s, dx_den, 100))
        register_glyph(g_name, codepoints, pen, adv, int(mid - max_w / 2))

    # Compound 12/8 Meter
    pen = TTGlyphPen(glyphSet=glyf)
    s = 0.34
    w1 = (glyf["one"].xMax - glyf["one"].xMin) * s
    w2 = (glyf["two"].xMax - glyf["two"].xMin) * s
    w_num = w1 + w2 + 20
    w_den = (glyf["eight"].xMax - glyf["eight"].xMin) * s
    adv = int(max(500, w_num + 140))
    mid = adv / 2
    x_start_num = mid - w_num / 2
    pen.addComponent("one", (s, 0, 0, s, int(x_start_num - glyf["one"].xMin * s), 340))
    pen.addComponent("two", (s, 0, 0, s, int(x_start_num + w1 + 20 - glyf["two"].xMin * s), 340))
    pen.addComponent("eight", (s, 0, 0, s, int(mid - w_den / 2 - glyf["eight"].xMin * s), 100))
    register_glyph("time_sig_12_8", [0xE947], pen, adv, int(x_start_num))


    # Glyph 3: Treble G-Clef U+E050 & U+1D11E & U+26D1
    pen = TTGlyphPen(None)
    # Master G-clef geometry centered at x = 320
    # Central stem
    draw_rect(pen, 310 - hw, -80, 310 + hw, 740)
    # Bottom curled terminal dot: center (240, -40)
    draw_circle(pen, 240, -40, 60, clockwise=True)
    # Center spiral around G4 (y = 220):
    draw_circle(pen, 310, 220, 140, clockwise=True)
    draw_circle(pen, 310, 220, 140 - STROKE_W, clockwise=False)
    # Upper loop around y = 520
    draw_circle(pen, 310, 520, 110, clockwise=True)
    draw_circle(pen, 310, 520, 110 - STROKE_W, clockwise=False)
    register_glyph("clef_treble_g", [0xE050, 0x1D11E], pen, 640, 150)

    # Glyph 4: Bass F-Clef U+E062 & U+1D122
    pen = TTGlyphPen(None)
    # Master curved arch at top: center (280, 460)
    draw_circle(pen, 280, 460, 140, clockwise=True)
    draw_circle(pen, 280, 460, 140 - STROKE_W, clockwise=False)
    # Descending tail
    pen.moveTo((420, 460))
    pen.qCurveTo((420, 260), (320, 160))
    pen.lineTo((320 - STROKE_W, 160))
    pen.qCurveTo((420 - STROKE_W, 260), (420 - STROKE_W, 460))
    pen.closePath()
    # Central anchor dot at F4 (y = 460)
    draw_circle(pen, 280, 460, 55, clockwise=True)
    # Two dots straddling 4th line (y = 460): upper (470, 520), lower (470, 400)
    draw_circle(pen, 470, 520, 42, clockwise=True)
    draw_circle(pen, 470, 400, 42, clockwise=True)
    register_glyph("clef_bass_f", [0xE062, 0x1D122], pen, 600, 140)

    # Glyph 5: Alto/Tenor C-Clef U+E05C & U+1D121
    pen = TTGlyphPen(None)
    # Two vertical bounding bars at x = 160 and x = 200
    draw_rect(pen, 160, 100, 190, 580)
    draw_rect(pen, 215, 100, 235, 580)
    # Upper lobe centered at y = 460
    draw_circle(pen, 340, 460, 110, clockwise=True)
    draw_circle(pen, 340, 460, 110 - STROKE_W, clockwise=False)
    # Lower lobe centered at y = 220
    draw_circle(pen, 340, 220, 110, clockwise=True)
    draw_circle(pen, 340, 220, 110 - STROKE_W, clockwise=False)
    # Center cusp pointing at middle C (y = 340)
    pen.moveTo((235, 340))
    pen.lineTo((310, 380))
    pen.lineTo((310, 300))
    pen.closePath()
    register_glyph("clef_c", [0xE05C, 0x1D121], pen, 600, 160)

    # Glyph 6: Neutral Percussion Clef U+E069 & U+1D125
    pen = TTGlyphPen(None)
    draw_rect(pen, 220, 220, 260, 460)
    draw_rect(pen, 340, 220, 380, 460)
    register_glyph("clef_percussion", [0xE069, 0x1D125], pen, 600, 220)

    print("\n3. Synthesizing SMuFL Noteheads, Stems & Accidentals...")

    # Glyph 7: Black/Quarter Notehead U+E0A4 & U+1D158
    pen = TTGlyphPen(None)
    draw_rotated_ellipse(pen, 300, 340, 160, 105, 22, clockwise=True)
    register_glyph("notehead_black", [0xE0A4, 0x1D158], pen, 560, 140)

    # Glyph 8: Half Notehead (Minim) U+E0A3 & U+1D157
    pen = TTGlyphPen(None)
    draw_rotated_ellipse(pen, 300, 340, 160, 105, 22, clockwise=True)
    draw_rotated_ellipse(pen, 300, 340, 160 - STROKE_W, 105 - STROKE_W // 2, 22, clockwise=False)
    register_glyph("notehead_half", [0xE0A3, 0x1D157], pen, 560, 140)

    # Glyph 9: Whole Notehead (Semibreve) U+E0A2 & U+1D15D
    pen = TTGlyphPen(None)
    draw_rotated_ellipse(pen, 300, 340, 190, 110, 0, clockwise=True)
    draw_rotated_ellipse(pen, 300, 340, 190 - STROKE_W * 2, 110 - STROKE_W // 2, 45, clockwise=False)
    register_glyph("notehead_whole", [0xE0A2, 0x1D15D], pen, 600, 110)

    # Glyph 10: Diamond Acoustic Harmonic Notehead U+E0DB
    pen = TTGlyphPen(None)
    pen.moveTo((300, 460))
    pen.lineTo((460, 340))
    pen.lineTo((300, 220))
    pen.lineTo((140, 340))
    pen.closePath()
    pen.moveTo((300, 460 - STROKE_W))
    pen.lineTo((140 + STROKE_W, 340))
    pen.lineTo((300, 220 + STROKE_W))
    pen.lineTo((460 - STROKE_W, 340))
    pen.closePath()
    register_glyph("notehead_diamond", [0xE0DB], pen, 600, 140)

    # Glyph 11: X-Notehead (Percussion/Spoken) U+E0A9
    pen = TTGlyphPen(None)
    pen.moveTo((180, 220))
    pen.lineTo((420, 460))
    pen.lineTo((420 - STROKE_W, 460))
    pen.lineTo((180 - STROKE_W, 220))
    pen.closePath()
    pen.moveTo((180, 460))
    pen.lineTo((420, 220))
    pen.lineTo((420 - STROKE_W, 220))
    pen.lineTo((180 - STROKE_W, 460))
    pen.closePath()
    register_glyph("notehead_x", [0xE0A9], pen, 600, 150)

    # Glyph 12: Natural Sign U+E261 & U+266E
    pen = TTGlyphPen(None)
    draw_rect(pen, 200, 180, 200 + STROKE_W, 560)  # Left stem
    draw_rect(pen, 380 - STROKE_W, 100, 380, 480)  # Right stem
    # Ascending crossbars
    draw_rect(pen, 200, 280, 380, 280 + STROKE_W)
    draw_rect(pen, 200, 400, 380, 400 + STROKE_W)
    register_glyph("accidental_natural", [0xE261, 0x266E], pen, 520, 200)

    # Glyph 13: Sharp Sign U+E262 & U+266F
    pen = TTGlyphPen(None)
    draw_rect(pen, 220, 80, 220 + STROKE_W, 580)
    draw_rect(pen, 360, 80, 360 + STROKE_W, 580)
    # Slanted crossbars angled +10 degrees
    pen.moveTo((120, 240))
    pen.lineTo((460, 300))
    pen.lineTo((460, 300 + STROKE_W))
    pen.lineTo((120, 240 + STROKE_W))
    pen.closePath()
    pen.moveTo((120, 380))
    pen.lineTo((460, 440))
    pen.lineTo((460, 440 + STROKE_W))
    pen.lineTo((120, 380 + STROKE_W))
    pen.closePath()
    register_glyph("accidental_sharp", [0xE262, 0x266F], pen, 540, 120)

    # Glyph 14: Flat Sign U+E260 & U+266D
    pen = TTGlyphPen(None)
    draw_rect(pen, 180, 100, 180 + STROKE_W, 620)  # Tall ascender stem
    # Teardrop loop at bottom
    pen.moveTo((180, 180))
    pen.qCurveTo((400, 220), (400, 340))
    pen.qCurveTo((400, 420), (180, 300))
    pen.closePath()
    pen.moveTo((180 + STROKE_W, 230))
    pen.qCurveTo((320, 260), (320, 340))
    pen.qCurveTo((320, 380), (180 + STROKE_W, 300))
    pen.closePath()
    register_glyph("accidental_flat", [0xE260, 0x266D], pen, 520, 180)

    # Glyph 15: Double Sharp U+E263 & U+1D12A
    pen = TTGlyphPen(None)
    # Bold cross with square terminal serifs
    draw_rect(pen, 200, 280, 400, 360)
    draw_rect(pen, 260, 220, 340, 420)
    draw_rect(pen, 180, 260, 220, 380)
    draw_rect(pen, 380, 260, 420, 380)
    draw_rect(pen, 240, 200, 360, 240)
    draw_rect(pen, 240, 400, 360, 440)
    register_glyph("accidental_double_sharp", [0xE263, 0x1D12A], pen, 560, 180)

    # Glyph 16: Quarter Rest U+E4E5 & U+1D13D
    pen = TTGlyphPen(None)
    # Classic lightning zig-zag rest
    pen.moveTo((340, 560))
    pen.lineTo((240, 420))
    pen.lineTo((360, 320))
    pen.lineTo((220, 200))
    pen.lineTo((240, 120))
    pen.lineTo((280, 120))
    pen.lineTo((300, 180))
    pen.lineTo((400, 280))
    pen.lineTo((280, 380))
    pen.lineTo((380, 520))
    pen.closePath()
    register_glyph("rest_quarter", [0xE4E5, 0x1D13D], pen, 560, 220)

    print("\n4. Synthesizing Clinical Audiology & Music Therapy Telemetry...")

    # Glyph 17: Right Ear Air Conduction Unmasked (Red O) PUA U+E930
    pen = TTGlyphPen(None)
    draw_circle(pen, 300, 350, 180, clockwise=True)
    draw_circle(pen, 300, 350, 180 - STROKE_W, clockwise=False)
    register_glyph("audiology_right_ear_air", [0xE930], pen, 600, 120)

    # Glyph 18: Left Ear Air Conduction Unmasked (Blue X) PUA U+E931
    pen = TTGlyphPen(None)
    pen.moveTo((160, 210))
    pen.lineTo((440, 490))
    pen.lineTo((440 - STROKE_W, 490))
    pen.lineTo((160 - STROKE_W, 210))
    pen.closePath()
    pen.moveTo((160, 490))
    pen.lineTo((440, 210))
    pen.lineTo((440 - STROKE_W, 210))
    pen.lineTo((160 - STROKE_W, 490))
    pen.closePath()
    register_glyph("audiology_left_ear_air", [0xE931], pen, 600, 130)

    # Glyph 19: Bone Conduction Right Bracket [ PUA U+E932
    pen = TTGlyphPen(None)
    draw_rect(pen, 200, 180, 200 + STROKE_W, 520)
    draw_rect(pen, 200, 520 - STROKE_W, 340, 520)
    draw_rect(pen, 200, 180, 340, 180 + STROKE_W)
    register_glyph("audiology_bone_right", [0xE932], pen, 540, 200)

    # Glyph 20: Bone Conduction Left Bracket ] PUA U+E933
    pen = TTGlyphPen(None)
    draw_rect(pen, 340 - STROKE_W, 180, 340, 520)
    draw_rect(pen, 200, 520 - STROKE_W, 340, 520)
    draw_rect(pen, 200, 180, 340, 180 + STROKE_W)
    register_glyph("audiology_bone_left", [0xE933], pen, 540, 200)

    # Glyph 21: Cardiac Entrainment Metronome Anchor (60 BPM) PUA U+E935
    pen = TTGlyphPen(None)
    # Metronome triangular body
    pen.moveTo((300, 600))
    pen.lineTo((440, 120))
    pen.lineTo((160, 120))
    pen.closePath()
    pen.moveTo((300, 540))
    pen.lineTo((190, 160))
    pen.lineTo((410, 160))
    pen.closePath()
    # Pendulum arm angled +15 degrees
    pen.moveTo((300, 160))
    pen.lineTo((380, 520))
    pen.lineTo((380 - hw, 520))
    pen.lineTo((300 - hw, 160))
    pen.closePath()
    # Pendulum weight weight slider at y = 380
    draw_rect(pen, 320, 360, 380, 420)
    register_glyph("metronome_cardiac_pacing", [0xE935], pen, 600, 160)

    # Glyph 22: Forward Arrow U+2192 & U+27F6
    pen = TTGlyphPen(None)
    draw_rect(pen, 80, 260 - hw, 480, 260 + hw)
    pen.moveTo((500, 260))
    pen.lineTo((360, 260 + 120))
    pen.lineTo((360, 260 + 120 - STROKE_W))
    pen.lineTo((440, 260))
    pen.lineTo((360, 260 - 120 + STROKE_W))
    pen.lineTo((360, 260 - 120))
    pen.closePath()
    register_glyph("arrow_right", [0x2192, 0x27F6], pen, 560, 80)

    # Glyph 22: Dynamics Forte U+E522 & Dynamic Piano U+E520
    # Create italicized forte and piano glyphs
    pen = TTGlyphPen(glyphSet=glyf)
    pen.addComponent("f", (1, 0, 0, 1, 60, 0))
    register_glyph("dynamic_forte", [0xE522, 0x1D191], pen, 560, 80)

    pen = TTGlyphPen(glyphSet=glyf)
    pen.addComponent("p", (1, 0, 0, 1, 60, 0))
    register_glyph("dynamic_piano", [0xE520, 0x1D18F], pen, 560, 80)

    # 5. Metadata and Versioning
    print("\n5. Updating metadata, SemVer 3.100, and OFL 1.1 licensing...")
    font.setGlyphOrder(glyph_order)
    font["head"].fontRevision = 3.1
    family_name = "PocketGull Music"
    ps_name = "PocketGull-Music"
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

    # 6. Serialization and Compression
    print("\n6. Serializing TrueType binary and compressing Brotli Q11 WOFF2...")
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
    print("  [SUCCESS] PocketGull Music SMuFL Superfamily compiled!")
    print("=" * 76)

if __name__ == "__main__":
    build_music_font()
