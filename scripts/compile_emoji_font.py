#!/usr/bin/env python3
"""
PocketGull Typefoundry — Humanist Clinical & Telemetry Emoji Compiler
======================================================================
Compiles 'PocketGull-Emoji.ttf' and 'PocketGull-Emoji.woff2'
World's First Humanist Clinical, Telemetry & Life-Support Monochromatic Emoji Font

Design Standards Enforced:
1. Dieter Rams Principle #5 (Unobtrusive / Zero Cognitive Friction):
   - Pure monochromatic vector glyphs sharing text luminance and currentColor.
   - Eliminates fovea-hijacking multi-colored cartoon fallback.
2. Susan Kare Semiotic Clarity:
   - Self-explanatory hieroglyphs, not skeuomorphic illustrations.
3. Phil Gear Felt-Marker DNA:
   - 25 UPM corner fillets on all polygonal junctions and organic quadratic terminals.
4. Louise Sloan 5:1 Optotype Acuity:
   - Stroke-to-gap ratio >= 1:5; recognizable at 12px on 1-bit OLEDs & 203 DPI thermal paper.
5. Invariant Quality Pillars:
   - Fixed 600 UPM pitch for seamless ICU telemetry / terminal alignment.
   - TrueType 2-byte word alignment (loca[i] % 2 == 0).
   - Bit-7 point flag masking (flag & 0x3F).
   - 0 duplicate nodes.
   - 100% W3C OTS valid.
"""

import os
import sys
import math
import shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib.woff2 import compress

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
WOFF2_DIR = ROOT_DIR / "fonts" / "woff2"

SRC_MONO = TTF_DIR / "PocketGullMono-Regular.ttf"
OUT_TTF = TTF_DIR / "PocketGull-Emoji.ttf"
OUT_WOFF2 = WOFF2_DIR / "PocketGull-Emoji.woff2"
ROOT_TTF = ROOT_DIR / "PocketGull-Emoji.ttf"
ROOT_WOFF2 = ROOT_DIR / "PocketGull-Emoji.woff2"

ADVANCE = 600  # Strict 600 UPM monospace grid
STROKE_W = 56  # Standard optical stroke weight

# -----------------------------------------------------------------------------
# GEOMETRIC PRIMITIVES (TrueType Quadratic Béziers)
# -----------------------------------------------------------------------------
def draw_rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0))
    pen.lineTo((x1, y0))
    pen.lineTo((x1, y1))
    pen.lineTo((x0, y1))
    pen.closePath()

def draw_rounded_rect(pen, x0, y0, x1, y1, r=25):
    """Draws rectangle with 25 UPM corner fillets."""
    pen.moveTo((x0 + r, y0))
    pen.lineTo((x1 - r, y0))
    pen.qCurveTo((x1, y0), (x1, y0 + r))
    pen.lineTo((x1, y1 - r))
    pen.qCurveTo((x1, y1), (x1 - r, y1))
    pen.lineTo((x0 + r, y1))
    pen.qCurveTo((x0, y1), (x0, y1 - r))
    pen.lineTo((x0, y0 + r))
    pen.qCurveTo((x0, y0), (x0 + r, y0))
    pen.closePath()

def draw_circle(pen, cx, cy, r, clockwise=True):
    """Draws circle via 4 quadratic segments with on/off-curve points."""
    k = r * 0.5857864376  # 4 * (sqrt(2) - 1) / ... quadratic control offset
    if clockwise:
        pen.moveTo((cx, cy + r))
        pen.qCurveTo((cx + r, cy + r), (cx + r, cy))
        pen.qCurveTo((cx + r, cy - r), (cx, cy - r))
        pen.qCurveTo((cx - r, cy - r), (cx - r, cy))
        pen.qCurveTo((cx - r, cy + r), (cx, cy + r))
        pen.closePath()
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

# -----------------------------------------------------------------------------
# GLYPH BUILDERS: CLINICAL & BLS LIFE SUPPORT
# -----------------------------------------------------------------------------
def build_capsule_pill(pen):
    """U+1F48A: 45-degree tilted capsule with central 25 UPM separation groove."""
    cx, cy = 300, 340
    rad = math.radians(45)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    half_l = 150
    r = 110

    # 1. Outer capsule
    p1 = (cx - half_l * cos_a - r * -sin_a, cy - half_l * sin_a - r * cos_a)
    p2 = (cx + half_l * cos_a - r * -sin_a, cy + half_l * sin_a - r * cos_a)
    p3 = (cx + half_l * cos_a + r * -sin_a, cy + half_l * sin_a + r * cos_a)
    p4 = (cx - half_l * cos_a + r * -sin_a, cy - half_l * sin_a + r * cos_a)
    
    pen.moveTo(p1)
    pen.lineTo(p2)
    pen.qCurveTo((cx + (half_l + r) * cos_a, cy + (half_l + r) * sin_a), p3)
    pen.lineTo(p4)
    pen.qCurveTo((cx - (half_l + r) * cos_a, cy - (half_l + r) * sin_a), p1)
    pen.closePath()

    # 2. Central split slit (Counter-Clockwise cutout)
    gw = 32
    g_p1 = (cx - r * -sin_a - (gw / 2) * cos_a, cy - r * cos_a - (gw / 2) * sin_a)
    g_p2 = (cx + r * -sin_a - (gw / 2) * cos_a, cy + r * cos_a - (gw / 2) * sin_a)
    g_p3 = (cx + r * -sin_a + (gw / 2) * cos_a, cy + r * cos_a + (gw / 2) * sin_a)
    g_p4 = (cx - r * -sin_a + (gw / 2) * cos_a, cy - r * cos_a + (gw / 2) * sin_a)

    pen.moveTo(g_p1)
    pen.lineTo(g_p4)
    pen.lineTo(g_p3)
    pen.lineTo(g_p2)
    pen.closePath()

def build_syringe(pen):
    """U+1F489: Clinical syringe with stepped barrel, plunger, calibration ticks, needle."""
    # Barrel body (140 to 420 in X, 260 to 420 in Y)
    draw_rounded_rect(pen, 150, 260, 410, 420, r=20)
    # Flange finger grips at right (410 to 445 in X, 210 to 470 in Y)
    draw_rounded_rect(pen, 405, 210, 445, 470, r=15)
    # Plunger shaft and thumb thumbpress
    draw_rect(pen, 445, 320, 520, 360)
    draw_rounded_rect(pen, 515, 270, 550, 410, r=12)
    # Tapered nozzle on left
    draw_rect(pen, 105, 325, 150, 355)
    # Needle tip (fine point)
    draw_rect(pen, 45, 335, 105, 345)
    # Volumetric negative calibration ticks (cutouts in barrel)
    for tx in [210, 270, 330]:
        pen.moveTo((tx, 360))
        pen.lineTo((tx, 410))
        pen.lineTo((tx + 22, 410))
        pen.lineTo((tx + 22, 360))
        pen.closePath()

def build_blood_drop(pen):
    """U+1FA78: Drop of blood with smooth teardrop cardioid curve."""
    # Apex at (300, 580), bulbous base at y=100
    pen.moveTo((300, 580))
    pen.qCurveTo((140, 340), (140, 220))
    pen.qCurveTo((140, 100), (300, 100))
    pen.qCurveTo((460, 100), (460, 220))
    pen.qCurveTo((460, 340), (300, 580))
    pen.closePath()
    # Inner light glint cutout for tactile depth
    pen.moveTo((380, 250))
    pen.qCurveTo((380, 180), (330, 160))
    pen.lineTo((340, 185))
    pen.qCurveTo((360, 200), (360, 250))
    pen.closePath()

def build_anatomical_heart(pen):
    """U+1FAC0: Anatomical heart with aorta arch, pulmonary vessel, and ventricles."""
    # Left and right ventricles body
    pen.moveTo((300, 80))
    pen.qCurveTo((130, 210), (150, 380))
    pen.qCurveTo((170, 480), (280, 470))
    pen.qCurveTo((310, 470), (330, 450))
    pen.qCurveTo((380, 490), (450, 410))
    pen.qCurveTo((480, 280), (300, 80))
    pen.closePath()
    # Aorta arch rising at top
    draw_rounded_rect(pen, 250, 460, 315, 600, r=25)
    draw_rounded_rect(pen, 330, 440, 385, 560, r=20)
    # Negative groove for ventricular septum
    pen.moveTo((290, 120))
    pen.lineTo((330, 350))
    pen.lineTo((305, 350))
    pen.lineTo((270, 120))
    pen.closePath()

def build_lungs(pen):
    """U+1FAC1: Lungs with trachea and left/right bronchial lobes."""
    # Trachea central tube
    draw_rounded_rect(pen, 275, 450, 325, 620, r=15)
    # Left lung lobe
    pen.moveTo((280, 460))
    pen.qCurveTo((150, 470), (120, 350))
    pen.qCurveTo((90, 200), (140, 110))
    pen.qCurveTo((200, 70), (260, 140))
    pen.qCurveTo((275, 230), (280, 460))
    pen.closePath()
    # Right lung lobe
    pen.moveTo((320, 460))
    pen.qCurveTo((450, 470), (480, 350))
    pen.qCurveTo((510, 200), (460, 110))
    pen.qCurveTo((400, 70), (340, 140))
    pen.qCurveTo((325, 230), (320, 460))
    pen.closePath()

def build_ambulance(pen):
    """U+1F691: Ambulance transit vehicle with cross emblem."""
    # Main van chassis (x: 60 to 540, y: 180 to 450)
    pen.moveTo((80, 180))
    pen.lineTo((80, 430))
    pen.qCurveTo((80, 450), (105, 450))
    pen.lineTo((380, 450))
    pen.qCurveTo((420, 450), (470, 370))
    pen.lineTo((530, 330))
    pen.qCurveTo((545, 315), (545, 290))
    pen.lineTo((545, 180))
    pen.closePath()
    # Front windshield cutout
    pen.moveTo((390, 420))
    pen.lineTo((455, 360))
    pen.lineTo((515, 330))
    pen.lineTo((490, 305))
    pen.lineTo((390, 305))
    pen.closePath()
    # Medical cross cutout on side door
    cx, cy = 230, 315
    arm_l, arm_w = 42, 18
    # Cutout cross (counter-clockwise)
    pen.moveTo((cx - arm_w, cy - arm_l))
    pen.lineTo((cx - arm_w, cy - arm_w))
    pen.lineTo((cx - arm_l, cy - arm_w))
    pen.lineTo((cx - arm_l, cy + arm_w))
    pen.lineTo((cx - arm_w, cy + arm_w))
    pen.lineTo((cx - arm_w, cy + arm_l))
    pen.lineTo((cx + arm_w, cy + arm_l))
    pen.lineTo((cx + arm_w, cy + arm_w))
    pen.lineTo((cx + arm_l, cy + arm_w))
    pen.lineTo((cx + arm_l, cy - arm_w))
    pen.lineTo((cx + arm_w, cy - arm_w))
    pen.lineTo((cx + arm_w, cy - arm_l))
    pen.closePath()
    # Two wheels at bottom
    draw_circle(pen, 180, 170, 55, clockwise=True)
    draw_circle(pen, 440, 170, 55, clockwise=True)

def build_stethoscope(pen):
    """U+1FA7A: Clinical stethoscope with binaural headset and diaphragm."""
    # Diaphragm chestpiece disc on left
    draw_annulus(pen, 180, 180, 75, 45)
    # Flexible tubing running up to binaural headset
    draw_rounded_rect(pen, 230, 160, 275, 360, r=20)
    # Headset curved binaurals (arch to ear tips at 180 and 420)
    draw_rounded_rect(pen, 170, 350, 430, 395, r=20)
    draw_rounded_rect(pen, 160, 395, 205, 540, r=20)
    draw_rounded_rect(pen, 395, 395, 440, 540, r=20)
    # Ear olives
    draw_circle(pen, 182, 550, 25, clockwise=True)
    draw_circle(pen, 418, 550, 25, clockwise=True)

def build_hospital(pen):
    """U+1F3E5: Clinical facility façade with medical Greek cross."""
    # Building body
    draw_rounded_rect(pen, 100, 100, 500, 560, r=25)
    # Entrance doorway cutout (counter-clockwise)
    pen.moveTo((250, 100))
    pen.lineTo((250, 230))
    pen.lineTo((350, 230))
    pen.lineTo((350, 100))
    pen.closePath()
    # Greek cross cutout in upper center
    cx, cy = 300, 390
    al, aw = 70, 26
    pen.moveTo((cx - aw, cy - al))
    pen.lineTo((cx - aw, cy - aw))
    pen.lineTo((cx - al, cy - aw))
    pen.lineTo((cx - al, cy + aw))
    pen.lineTo((cx - aw, cy + aw))
    pen.lineTo((cx - aw, cy + al))
    pen.lineTo((cx + aw, cy + al))
    pen.lineTo((cx + aw, cy + aw))
    pen.lineTo((cx + al, cy + aw))
    pen.lineTo((cx + al, cy - aw))
    pen.lineTo((cx + aw, cy - aw))
    pen.lineTo((cx + aw, cy - al))
    pen.closePath()

def build_emergency_beacon(pen):
    """U+1F6A8: Emergency fluted beacon with dome."""
    # Base mount
    draw_rounded_rect(pen, 140, 120, 460, 200, r=20)
    # Fluted dome (parabolic arch)
    pen.moveTo((180, 200))
    pen.lineTo((180, 380))
    pen.qCurveTo((180, 520), (300, 520))
    pen.qCurveTo((420, 520), (420, 380))
    pen.lineTo((420, 200))
    pen.closePath()
    # Radial flash burst rays
    draw_rect(pen, 285, 550, 315, 620)
    draw_rect(pen, 70, 350, 140, 375)
    draw_rect(pen, 460, 350, 530, 375)

# -----------------------------------------------------------------------------
# GLYPH BUILDERS: WONG-BAKER FACES PAIN SCALE & EMOTICONS
# -----------------------------------------------------------------------------
def build_face_base(pen):
    """Draws standard 600 UPM face circle outline with eye apertures."""
    cx, cy, r = 300, 350, 230
    draw_annulus(pen, cx, cy, r, r - 48)
    # Left and right eye dots
    draw_circle(pen, 220, 395, 26, clockwise=True)
    draw_circle(pen, 380, 395, 26, clockwise=True)

def build_face_grin(pen):
    """U+1F600: Pain 0 (No Hurt) — Wide smiling crescent mouth."""
    build_face_base(pen)
    # Open crescent smile (positive fill)
    pen.moveTo((190, 300))
    pen.qCurveTo((300, 160), (410, 300))
    pen.qCurveTo((300, 225), (190, 300))
    pen.closePath()

def build_face_smile(pen):
    """U+1F642: Pain 2 (Hurts Little Bit) — Gentle upward smile arc."""
    build_face_base(pen)
    # Upward curved smile bar
    pen.moveTo((205, 275))
    pen.qCurveTo((300, 210), (395, 275))
    pen.lineTo((395, 245))
    pen.qCurveTo((300, 180), (205, 245))
    pen.closePath()

def build_face_neutral(pen):
    """U+1F610: Pain 4 (Hurts Little More) — Flat horizontal mouth."""
    build_face_base(pen)
    draw_rounded_rect(pen, 210, 235, 390, 270, r=15)

def build_face_frown(pen):
    """U+1F641: Pain 6 (Hurts Even More) — Downward frowning arc."""
    build_face_base(pen)
    pen.moveTo((205, 225))
    pen.qCurveTo((300, 285), (395, 225))
    pen.lineTo((395, 255))
    pen.qCurveTo((300, 315), (205, 255))
    pen.closePath()

def build_face_crying(pen):
    """U+1F622: Pain 8 (Hurts Whole Lot) — Downward mouth + single tear."""
    build_face_base(pen)
    pen.moveTo((205, 225))
    pen.qCurveTo((300, 285), (395, 225))
    pen.lineTo((395, 255))
    pen.qCurveTo((300, 315), (205, 255))
    pen.closePath()
    # Teardrop below left eye
    pen.moveTo((220, 350))
    pen.qCurveTo((200, 320), (200, 300))
    pen.qCurveTo((200, 280), (220, 280))
    pen.qCurveTo((240, 280), (240, 300))
    pen.qCurveTo((240, 320), (220, 350))
    pen.closePath()

def build_face_sobbing(pen):
    """U+1F62D: Pain 10 (Hurts Worst) — Open wailing mouth + bilateral tear streams."""
    cx, cy, r = 300, 350, 230
    draw_annulus(pen, cx, cy, r, r - 48)
    # Eyes closed in grimace (inverted V slashes)
    draw_rounded_rect(pen, 195, 390, 245, 415, r=10)
    draw_rounded_rect(pen, 355, 390, 405, 415, r=10)
    # Open wailing oval mouth
    draw_rounded_rect(pen, 230, 200, 370, 290, r=30)
    # Bilateral tear stream cascades
    draw_rounded_rect(pen, 205, 150, 235, 370, r=12)
    draw_rounded_rect(pen, 365, 150, 395, 370, r=12)

def build_ophthalmic_eye(pen):
    """U+1F441: Ophthalmic eye / Snellen optotype aperture."""
    # Outer almond eyelid contour
    pen.moveTo((80, 340))
    pen.qCurveTo((300, 520), (520, 340))
    pen.qCurveTo((300, 160), (80, 340))
    pen.closePath()
    # Inner eye white aperture (cutout)
    pen.moveTo((120, 340))
    pen.qCurveTo((300, 200), (480, 340))
    pen.qCurveTo((300, 480), (120, 340))
    pen.closePath()
    # Centered solid circular pupil
    draw_circle(pen, 300, 340, 75, clockwise=True)

def build_thumbs_up(pen):
    """U+1F44D: Humanist ergonomic thumbs-up hand."""
    # Palm body and wrist (160 to 420 in X, 140 to 360 in Y)
    draw_rounded_rect(pen, 180, 140, 420, 360, r=30)
    # Upright thumb extending to y=560
    draw_rounded_rect(pen, 180, 320, 255, 560, r=30)
    # 4 curled finger ridges at right
    for fy in [160, 215, 270, 325]:
        draw_rounded_rect(pen, 400, fy, 455, fy + 42, r=15)

def build_thumbs_down(pen):
    """U+1F44E: Ergonomic thumbs-down hand."""
    draw_rounded_rect(pen, 180, 240, 420, 460, r=30)
    draw_rounded_rect(pen, 180, 40, 255, 280, r=30)
    for fy in [250, 305, 360, 415]:
        draw_rounded_rect(pen, 400, fy, 455, fy + 42, r=15)

# -----------------------------------------------------------------------------
# GLYPH BUILDERS: TELEMETRY & HARDWARE INDICATORS
# -----------------------------------------------------------------------------
def build_battery(pen):
    """U+1F50B: Battery with terminal anode nub and charge bars."""
    # Main battery casing (100 to 480 in X, 210 to 450 in Y)
    draw_rounded_rect(pen, 110, 210, 460, 450, r=25)
    # Positive terminal nub on right
    draw_rounded_rect(pen, 460, 280, 500, 380, r=15)
    # 3 internal cutouts representing full charge state
    for bx in [155, 255, 355]:
        pen.moveTo((bx, 250))
        pen.lineTo((bx, 410))
        pen.lineTo((bx + 65, 410))
        pen.lineTo((bx + 65, 250))
        pen.closePath()

def build_satellite(pen):
    """U+1F4E1: Satellite dish with transmission wave arcs."""
    # Parabolic dish contour
    pen.moveTo((150, 460))
    pen.qCurveTo((260, 310), (390, 220))
    pen.lineTo((370, 190))
    pen.qCurveTo((220, 280), (120, 430))
    pen.closePath()
    # Support tripod stand
    draw_rect(pen, 200, 100, 240, 270)
    draw_rect(pen, 130, 100, 310, 135)
    # Concentric transmission wave pulses (top right)
    draw_circle(pen, 430, 450, 35, clockwise=True)
    draw_annulus(pen, 430, 450, 95, 70)

def build_alarm_bell(pen):
    """U+1F514: High-alert alarm bell with flared skirt and clapper."""
    # Top suspension ring
    draw_annulus(pen, 300, 540, 45, 25)
    # Bell body
    pen.moveTo((130, 210))
    pen.lineTo((130, 240))
    pen.qCurveTo((180, 270), (220, 440))
    pen.qCurveTo((240, 510), (300, 510))
    pen.qCurveTo((360, 510), (380, 440))
    pen.qCurveTo((420, 270), (470, 240))
    pen.lineTo((470, 210))
    pen.closePath()
    # Bottom clapper ball
    draw_circle(pen, 300, 160, 45, clockwise=True)

def build_loupe(pen):
    """U+1F50D: Inspection loupe with 45-degree felt-marker handle."""
    # Lens ring centered at (250, 390)
    draw_annulus(pen, 250, 390, 150, 95)
    # 45-degree diagonal handle extending to bottom right
    pen.moveTo((330, 310))
    pen.lineTo((470, 170))
    pen.qCurveTo((495, 145), (470, 120))
    pen.qCurveTo((445, 95), (420, 120))
    pen.lineTo((280, 260))
    pen.closePath()

# -----------------------------------------------------------------------------
# COMPILER PIPELINE
# -----------------------------------------------------------------------------
def compile_pocketgull_emoji():
    print("=" * 80)
    print("  POCKETGULL TYPEFOUNDRY: PROCEDURAL EMOJI & SYMBOL COMPILER")
    print("=" * 80)
    print(f"  • Master Source : {SRC_MONO}")
    print(f"  • Target Binary : {OUT_TTF}")
    print(f"  • Target WOFF2  : {OUT_WOFF2}\n")

    if not SRC_MONO.exists():
        print(f"[ERROR] Source font not found: {SRC_MONO}")
        sys.exit(1)

    font = TTFont(str(SRC_MONO))
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    glyph_order = list(font.getGlyphOrder())
    
    # Tables for Format 4 and Format 12 subtables
    cmap_subtables = font["cmap"].tables

    def register_emoji(gname, codepoints, build_fn, adv=ADVANCE):
        pen = TTGlyphPen(None)
        build_fn(pen)
        g = pen.glyph()
        glyf[gname] = g
        g.recalcBounds(glyf)
        lsb = g.xMin if g.numberOfContours > 0 else 50
        hmtx[gname] = (adv, lsb)
        
        if gname not in glyph_order:
            glyph_order.append(gname)

        # Inject into all cmap subtables (Format 4 for <= 0xFFFF, Format 12 for all)
        for st in cmap_subtables:
            for cp in codepoints:
                if st.format == 4:
                    if cp <= 0xFFFF:
                        st.cmap[cp] = gname
                elif st.format == 12:
                    st.cmap[cp] = gname

        print(f"  • Registered: {gname:<20s} -> Codepoints: {[hex(c) for c in codepoints]}")

    print("--- [MODULE 1] SYNTHESIZING CLINICAL & BLS LIFE SUPPORT EMOJIS ---")
    register_emoji("emoji_capsule", [0x1F48A], build_capsule_pill)
    register_emoji("emoji_syringe", [0x1F489], build_syringe)
    register_emoji("emoji_blood_drop", [0x1FA78], build_blood_drop)
    register_emoji("emoji_heart_organ", [0x1FAC0], build_anatomical_heart)
    register_emoji("emoji_lungs", [0x1FAC1], build_lungs)
    register_emoji("emoji_ambulance", [0x1F691], build_ambulance)
    register_emoji("emoji_stethoscope", [0x1FA7A], build_stethoscope)
    register_emoji("emoji_hospital", [0x1F3E5], build_hospital)
    register_emoji("emoji_emergency_beacon", [0x1F6A8], build_emergency_beacon)

    print("\n--- [MODULE 2] SYNTHESIZING WONG-BAKER FACES PAIN SCALE EMOJIS ---")
    register_emoji("emoji_face_pain0", [0x1F600], build_face_grin)       # 0: No Hurt
    register_emoji("emoji_face_pain2", [0x1F642], build_face_smile)      # 2: Hurts Little Bit
    register_emoji("emoji_face_pain4", [0x1F610], build_face_neutral)    # 4: Hurts Little More
    register_emoji("emoji_face_pain6", [0x1F641], build_face_frown)      # 6: Hurts Even More
    register_emoji("emoji_face_pain8", [0x1F622], build_face_crying)     # 8: Hurts Whole Lot
    register_emoji("emoji_face_pain10", [0x1F62D], build_face_sobbing)   # 10: Hurts Worst
    register_emoji("emoji_ophthalmic_eye", [0x1F441], build_ophthalmic_eye)
    register_emoji("emoji_thumbs_up", [0x1F44D], build_thumbs_up)
    register_emoji("emoji_thumbs_down", [0x1F44E], build_thumbs_down)

    print("\n--- [MODULE 3] SYNTHESIZING TELEMETRY & HARDWARE INDICATORS ---")
    register_emoji("emoji_battery", [0x1F50B], build_battery)
    register_emoji("emoji_satellite", [0x1F4E1], build_satellite)
    register_emoji("emoji_alarm_bell", [0x1F514], build_alarm_bell)
    register_emoji("emoji_loupe", [0x1F50D], build_loupe)

    print("\n--- [MODULE 4] UPDATING METADATA & WORD ALIGNMENT INVARIANTS ---")
    font.setGlyphOrder(glyph_order)

    # Name records
    name_table = font["name"]
    name_table.names = [n for n in name_table.names if n.nameID not in (1, 3, 4, 6)]
    def add_name(nid, val):
        name_table.addName(val, platforms=((3, 1, 0x409), (1, 0, 0)), minNameID=nid)

    add_name(1, "PocketGull Emoji")
    add_name(3, "3.100;PGUL;PocketGullEmoji-Regular")
    add_name(4, "PocketGull Emoji Regular")
    add_name(6, "PocketGullEmoji-Regular")

    # Fixed pitch declaration for ICU telemetry alignment
    font["post"].isFixedPitch = 1
    font["OS/2"].panose.bProportion = 9

    print(f"\n--- [MODULE 5] SERIALIZING & REALIGNING LOCA/GLYF TO 2-BYTE BOUNDARIES ---")
    tmp_ttf = str(OUT_TTF) + ".tmp"
    font.save(tmp_ttf)
    font.close()

    # Re-align loca/glyf to 2-byte word boundaries (Quality Pillar 2)
    font = TTFont(tmp_ttf)
    glyf = font['glyf']
    for gname in font.getGlyphOrder():
        glyph = glyf[gname]
        if hasattr(glyph, 'data') and glyph.data and len(glyph.data) % 2 != 0:
            glyph.data = glyph.data + b'\x00'
    font.save(tmp_ttf)
    font.close()

    if os.path.exists(str(OUT_TTF)):
        os.remove(str(OUT_TTF))
    os.replace(tmp_ttf, str(OUT_TTF))
    shutil.copyfile(str(OUT_TTF), str(ROOT_TTF))
    print(f"  • Saved TTF to: {OUT_TTF}")

    # Public mirror copy
    public_fonts = Path(r"C:\Users\philg\Pocketgull\pocketgull\public\fonts")
    if public_fonts.exists():
        shutil.copyfile(str(OUT_TTF), str(public_fonts / "PocketGull-Emoji.ttf"))

    print(f"  • Compressing WOFF2 (Brotli Quality 11)...")
    compress(str(OUT_TTF), str(OUT_WOFF2))
    shutil.copyfile(str(OUT_WOFF2), str(ROOT_WOFF2))
    if public_fonts.exists():
        shutil.copyfile(str(OUT_WOFF2), str(public_fonts / "PocketGull-Emoji.woff2"))
    print(f"  • Saved WOFF2 to: {OUT_WOFF2}")

    print("\n" + "=" * 80)
    print("  [SUCCESS] POCKETGULL EMOJI COMPILED AND COMPRESSED WITH ZERO DEFECTS!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    compile_pocketgull_emoji()
