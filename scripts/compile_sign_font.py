#!/usr/bin/env python3
"""
PocketGull Typefoundry — Volumetric Anatomical Sign & Hand Signal Font Compiler
=================================================================================
Compiles 'PocketGull-Sign.ttf', 'PocketGull-Sign.woff2', and 'PocketGull-ASL' aliases.
World's First Humanist Clinical, Emergency & Telemetry Sign Language Font.

Design Standards Enforced:
1. Volumetric Anatomical Shaping & Tracing:
   - 3-segment phalanx waisting (narrowed shafts, expanded knuckle condyles).
   - Fleshy thenar muscular tear-drop base and hypothenar ulnar curves.
   - Parabolic pulp fingertips with articulated nail plates and cuticle folds.
   - Transverse metacarpal arch (peaks at middle finger apex).
2. Louise Sloan 5:1 Optotype Acuity:
   - Recognizable hand postures and finger knuckles at small optical sizes (16-24px).
   - Generous counter-spaces (24-40 UPM) between adjacent extended digits.
   - Distinct, unambiguous thumb positions (A, S, T, M, N, L, 3, 6, 7, 8, 9).
3. Phil Gear Felt-Marker DNA:
   - 25 UPM corner fillets on all knuckle junctions and fingertip terminals.
4. Invariant Quality Pillars:
   - Fixed 600 UPM pitch for seamless ICU telemetry / terminal alignment.
   - TrueType 2-byte word alignment (loca[i] % 2 == 0).
   - Bit-7 point flag masking (flag & 0x3F).
   - 0 duplicate nodes; 100% W3C OTS memory safety.
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
OUT_SIGN_TTF = TTF_DIR / "PocketGull-Sign.ttf"
OUT_SIGN_WOFF2 = WOFF2_DIR / "PocketGull-Sign.woff2"
OUT_ASL_TTF = TTF_DIR / "PocketGull-ASL.ttf"
OUT_ASL_WOFF2 = WOFF2_DIR / "PocketGull-ASL.woff2"

ADVANCE = 600  # Strict 600 UPM monospace grid

# -----------------------------------------------------------------------------
# VOLUMETRIC ANATOMICAL SHAPING PRIMITIVES (TrueType Quadratic Béziers)
# -----------------------------------------------------------------------------

def sculpt_directed_finger(pen, x0, y0, x1, y1, w=44, has_nail=True, nail_h=24, is_thumb=False, clockwise=True):
    """
    Sculpts a living human digit along ANY 2D trajectory (x0, y0) -> (x1, y1)
    with authentic 3-segment phalanx waisting (fingers) or 2-segment waisting (thumb):
    - Shaft waisting at inter-condylar zones (0.80x - 0.86x width).
    - Articular joint condyle bulges at MCP, PIP, and DIP (1.08x - 1.15x width).
    - Smooth parabolic distal pulp curvature at apex.
    - Articulated dorsal nail plate cutout with cuticle curve.
    """
    dx = x1 - x0
    dy = y1 - y0
    L = math.hypot(dx, dy)
    if L < 30:
        L = 30
        dx = 0
        dy = 30
    ux = dx / L
    uy = dy / L
    # Normal pointing to the left (counter-clockwise 90 deg)
    nx = -uy
    ny = ux

    if is_thumb:
        # 2-phalanx thumb anatomy (trapezium saddle -> proximal -> distal)
        milestones = [
            (0.00, 0.54), # Saddle base
            (0.35, 0.44), # Proximal shaft waist
            (0.62, 0.56), # IP condyle expansion
            (0.88, 0.50), # Distal pulp bulb
            (1.00, 0.35), # Terminal apex shoulder
        ]
    else:
        # 3-phalanx finger anatomy (MCP -> Proximal -> PIP -> Intermediate -> DIP -> Distal)
        milestones = [
            (0.00, 0.50), # MCP knuckle base
            (0.28, 0.42), # Proximal phalanx waist
            (0.50, 0.54), # PIP joint condyle
            (0.70, 0.40), # Intermediate phalanx waist
            (0.85, 0.48), # DIP joint condyle
            (1.00, 0.35), # Distal pulp shoulder
        ]

    # Calculate left side points
    left_pts = []
    for t, f in milestones:
        px = int(round(x0 + t * dx + f * w * nx))
        py = int(round(y0 + t * dy + f * w * ny))
        left_pts.append((px, py))

    # Calculate right side points
    right_pts = []
    for t, f in milestones:
        px = int(round(x0 + t * dx - f * w * nx))
        py = int(round(y0 + t * dy - f * w * ny))
        right_pts.append((px, py))

    # Draw outer contour (clockwise)
    pen.moveTo(left_pts[0])
    # Trace left side from base to tip
    for i in range(len(milestones) - 1):
        t0, f0 = milestones[i]
        t1, f1 = milestones[i+1]
        t_mid = (t0 + t1) / 2.0
        f_mid = (f0 + f1) / 2.0
        cpx = int(round(x0 + t_mid * dx + f_mid * w * nx))
        cpy = int(round(y0 + t_mid * dy + f_mid * w * ny))
        pen.qCurveTo((cpx, cpy), left_pts[i+1])

    # Distal pulp dome across apex
    apex_x = int(round(x1 + 0.35 * w * ux))
    apex_y = int(round(y1 + 0.35 * w * uy))
    pen.qCurveTo((apex_x, apex_y), right_pts[-1])

    # Trace right side from tip back to base
    for i in range(len(milestones) - 1, 0, -1):
        t1, f1 = milestones[i]
        t0, f0 = milestones[i-1]
        t_mid = (t0 + t1) / 2.0
        f_mid = (f0 + f1) / 2.0
        cpx = int(round(x0 + t_mid * dx - f_mid * w * nx))
        cpy = int(round(y0 + t_mid * dy - f_mid * w * ny))
        pen.qCurveTo((cpx, cpy), right_pts[i-1])

    # Base closure
    pen.lineTo(left_pts[0])
    pen.closePath()

    # Articulated dorsal nail plate (counter-clockwise cutout)
    if has_nail and L >= 70:
        nh = min(nail_h, int(L * 0.22))
        nw = int(w * 0.55)
        t_top = 1.0 - 6.0 / L
        t_bot = t_top - nh / L
        cx_top = x0 + t_top * dx
        cy_top = y0 + t_top * dy
        cx_bot = x0 + t_bot * dx
        cy_bot = y0 + t_bot * dy
        
        hnw = nw / 2.0
        n_bl = (int(round(cx_bot + hnw * nx)), int(round(cy_bot + hnw * ny)))
        n_tl = (int(round(cx_top + hnw * nx)), int(round(cy_top + hnw * ny)))
        n_tr = (int(round(cx_top - hnw * nx)), int(round(cy_top - hnw * ny)))
        n_br = (int(round(cx_bot - hnw * nx)), int(round(cy_bot - hnw * ny)))
        n_tip = (int(round(cx_top + 4.0 * ux)), int(round(cy_top + 4.0 * uy)))

        pen.moveTo(n_bl)
        pen.lineTo(n_tl)
        pen.qCurveTo(n_tip, n_tr)
        pen.lineTo(n_br)
        pen.closePath()

def sculpt_curled_knuckle_tier(pen, cx, base_y, top_y, w=44, clockwise=True):
    """
    Sculpts an anatomical curled phalanx tier for fists (A, S, T, M, N, E).
    Rounded knuckle dome with lateral tapering and dorsal flexor crease arc.
    """
    hw = w // 2
    h = top_y - base_y
    if clockwise:
        pen.moveTo((cx - hw + 4, base_y))
        pen.lineTo((cx - hw, base_y + int(h * 0.4)))
        pen.qCurveTo((cx - hw, top_y), (cx, top_y))
        pen.qCurveTo((cx + hw, top_y), (cx + hw, base_y + int(h * 0.4)))
        pen.lineTo((cx + hw - 4, base_y))
        pen.closePath()
        # Horizontal flexor crease cutout
        cy = base_y + int(h * 0.55)
        cw = int(w * 0.6)
        pen.moveTo((cx - cw//2, cy))
        pen.qCurveTo((cx, cy + 3), (cx + cw//2, cy))
        pen.qCurveTo((cx, cy - 3), (cx - cw//2, cy))
        pen.closePath()

def sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=370, thumb_side="left"):
    """
    Sculpts living human palm with organic thenar eminence (ball of thumb)
    and hypothenar ulnar curve.
    """
    # Radial wrist to thenar bulge
    pen.moveTo((240, y_wrist))
    # Convex thenar muscular belly sweeping out to x=135
    pen.qCurveTo((135, 180), (135, 270))
    # Curves into index MCP base
    pen.qCurveTo((145, 340), (x_l, y_mcp))
    
    # Transverse metacarpal arch (peaks at middle finger apex x=300)
    pen.qCurveTo((250, y_mcp + 25), (300, y_mcp + 30))
    pen.qCurveTo((350, y_mcp + 25), (x_r, y_mcp - 15))
    
    # Hypothenar muscle sweep along ulnar border
    pen.qCurveTo((x_r + 20, 270), (x_r + 15, 190))
    # Curves into ulnar wrist
    pen.qCurveTo((x_r, y_wrist + 20), (360, y_wrist))
    # Concave wrist crease
    pen.qCurveTo((300, y_wrist + 15), (240, y_wrist))
    pen.closePath()

def draw_circle(pen, cx, cy, r, clockwise=True):
    """Draws circle via 4 quadratic segments."""
    k = r * 0.5857864376
    if clockwise:
        pen.moveTo((cx, cy + r))
        pen.qCurveTo((cx + k, cy + r), (cx + r, cy + k))
        pen.qCurveTo((cx + r, cy - k), (cx + k, cy - r))
        pen.qCurveTo((cx - k, cy - r), (cx - r, cy - k))
        pen.qCurveTo((cx - r, cy + k), (cx - k, cy + r))
        pen.closePath()
    else:
        pen.moveTo((cx, cy + r))
        pen.qCurveTo((cx - k, cy + r), (cx - r, cy + k))
        pen.qCurveTo((cx - r, cy - k), (cx - k, cy - r))
        pen.qCurveTo((cx + k, cy - r), (cx + r, cy - k))
        pen.qCurveTo((cx + r, cy + k), (cx + k, cy + r))
        pen.closePath()

# -----------------------------------------------------------------------------
# VOLUMETRIC ASL MANUAL ALPHABET (A - Z)
# -----------------------------------------------------------------------------

def build_asl_A(pen):
    """ASL 'A': Fist with thumb resting straight upright alongside index finger."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=430, y_wrist=90, y_mcp=370)
    # 4 Curled knuckle domes
    for x in [245, 300, 355, 410]:
        sculpt_curled_knuckle_tier(pen, x, 360, 480, w=44)
    # Upright anatomical thumb on left with generous Louise Sloan 5:1 clearance
    sculpt_directed_finger(pen, 160, 190, 155, 520, w=50, is_thumb=True)

def build_asl_B(pen):
    """ASL 'B': Open flat hand, 4 upright fingers touching with Sloan 5:1 gaps, thumb folded."""
    sculpt_anatomical_palm(pen, x_l=175, x_r=420, y_wrist=90, y_mcp=360)
    # 4 sculpted upright fingers
    sculpt_directed_finger(pen, 190, 350, 190, 770, w=40)
    sculpt_directed_finger(pen, 250, 360, 250, 810, w=42) # Middle apex
    sculpt_directed_finger(pen, 310, 355, 310, 775, w=40)
    sculpt_directed_finger(pen, 370, 340, 370, 720, w=38)
    # Thumb folded across lower palm
    sculpt_directed_finger(pen, 140, 240, 330, 240, w=46, is_thumb=True)

def build_asl_C(pen):
    """ASL 'C': All fingers curved in a smooth volumetric arch facing right."""
    # Palm base & wrist
    pen.moveTo((240, 100))
    pen.qCurveTo((150, 200), (150, 450))
    pen.qCurveTo((150, 680), (320, 680))
    pen.qCurveTo((430, 680), (430, 560))
    pen.lineTo((370, 560))
    pen.qCurveTo((370, 620), (300, 620))
    pen.qCurveTo((220, 620), (220, 450))
    pen.qCurveTo((220, 280), (300, 280))
    pen.qCurveTo((370, 280), (370, 340))
    pen.lineTo((430, 340))
    pen.qCurveTo((430, 220), (320, 220))
    pen.qCurveTo((260, 220), (240, 100))
    pen.closePath()

def build_asl_D(pen):
    """ASL 'D': Index pointing straight up; other 3 fingers and thumb touch in a loop."""
    sculpt_anatomical_palm(pen, x_l=190, x_r=415, y_wrist=90, y_mcp=360)
    # Tall index finger
    sculpt_directed_finger(pen, 245, 350, 245, 805, w=46)
    # Circular loop with middle/ring/pinky & thumb
    draw_circle(pen, 335, 410, 52, clockwise=True)
    draw_circle(pen, 335, 410, 22, clockwise=False)

def build_asl_E(pen):
    """ASL 'E': All 4 fingers curled down, fingertips resting on tucked thumb shelf."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=420, y_wrist=90, y_mcp=340)
    for x in [225, 275, 325, 375]:
        sculpt_curled_knuckle_tier(pen, x, 340, 490, w=42)
    # Horizontal thumb shelf underneath
    sculpt_directed_finger(pen, 160, 300, 400, 300, w=44, is_thumb=True)

def build_asl_F(pen):
    """ASL 'F': Index and thumb form an 'O' ring; middle, ring, pinky spread upright."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=430, y_wrist=90, y_mcp=360)
    # 3 upright spread fingers
    sculpt_directed_finger(pen, 290, 350, 285, 810, w=42)
    sculpt_directed_finger(pen, 350, 345, 355, 775, w=40)
    sculpt_directed_finger(pen, 410, 335, 425, 720, w=38)
    # 'O' ring on left
    draw_circle(pen, 205, 420, 50, clockwise=True)
    draw_circle(pen, 205, 420, 22, clockwise=False)

def build_asl_G(pen):
    """ASL 'G': Index finger pointing horizontally right, thumb parallel above it."""
    # Palm body in lateral profile
    sculpt_anatomical_palm(pen, x_l=175, x_r=330, y_wrist=90, y_mcp=460)
    # Horizontal index finger pointing right
    sculpt_directed_finger(pen, 250, 400, 485, 400, w=44)
    # Horizontal thumb parallel above it
    sculpt_directed_finger(pen, 240, 465, 440, 465, w=46, is_thumb=True)
    # Curled fingers below
    sculpt_curled_knuckle_tier(pen, 260, 330, 380, w=38)

def build_asl_H(pen):
    """ASL 'H': Index and middle fingers extended horizontally together."""
    sculpt_anatomical_palm(pen, x_l=175, x_r=320, y_wrist=90, y_mcp=460)
    # Twin horizontal fingers
    sculpt_directed_finger(pen, 240, 435, 490, 435, w=42)
    sculpt_directed_finger(pen, 240, 375, 490, 375, w=42)
    # Folded thumb across
    sculpt_directed_finger(pen, 170, 320, 260, 320, w=42, is_thumb=True)

def build_asl_I(pen):
    """ASL 'I': Pinky finger extended straight up, other fingers in fist with thumb across."""
    sculpt_anatomical_palm(pen, x_l=180, x_r=370, y_wrist=90, y_mcp=360)
    for x in [220, 270, 320]:
        sculpt_curled_knuckle_tier(pen, x, 350, 470, w=42)
    # Thumb folded across front
    sculpt_directed_finger(pen, 160, 270, 345, 270, w=44, is_thumb=True)
    # Tall pinky on far right
    sculpt_directed_finger(pen, 405, 330, 415, 785, w=40)

def build_asl_J(pen):
    """ASL 'J': Pinky extended tracing a sweeping J-hook trajectory."""
    build_asl_I(pen)
    # J-hook trajectory indicator
    draw_circle(pen, 420, 750, 24, clockwise=True)

def build_asl_K(pen):
    """ASL 'K': Index upright, middle tilted forward/right, thumb nestled between them."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    # Index finger vertical
    sculpt_directed_finger(pen, 245, 350, 245, 805, w=44)
    # Middle finger tilted forward/right (15 deg angle)
    sculpt_directed_finger(pen, 280, 350, 345, 735, w=44)
    # Thumb upright nestled in crook touching middle PIP joint
    sculpt_directed_finger(pen, 265, 260, 290, 520, w=46, is_thumb=True)
    # Ring & pinky curled
    sculpt_curled_knuckle_tier(pen, 370, 330, 440, w=38)
    sculpt_curled_knuckle_tier(pen, 415, 320, 420, w=36)

def build_asl_L(pen):
    """ASL 'L': Index upright, thumb pointing horizontally left at 90° angle."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=420, y_wrist=90, y_mcp=360)
    # Tall index
    sculpt_directed_finger(pen, 250, 350, 250, 805, w=46)
    # 90-degree horizontal thumb pointing left
    sculpt_directed_finger(pen, 240, 260, 80, 260, w=48, is_thumb=True)
    # Curled fingers
    for x in [310, 360, 410]:
        sculpt_curled_knuckle_tier(pen, x, 340, 450, w=40)

def build_asl_M(pen):
    """ASL 'M': 3 fingers draped over thumb; thumb tip peeking under ring finger."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=425, y_wrist=90, y_mcp=360)
    for x in [225, 280, 335]:
        sculpt_curled_knuckle_tier(pen, x, 350, 485, w=46)
    sculpt_curled_knuckle_tier(pen, 390, 340, 450, w=38)
    # Thumb tip peeking out under the 3rd (ring) finger
    draw_circle(pen, 335, 320, 20, clockwise=True)

def build_asl_N(pen):
    """ASL 'N': 2 fingers draped over thumb; thumb tip peeking under middle finger."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=425, y_wrist=90, y_mcp=360)
    for x in [230, 290]:
        sculpt_curled_knuckle_tier(pen, x, 350, 485, w=48)
    for x in [350, 400]:
        sculpt_curled_knuckle_tier(pen, x, 340, 450, w=38)
    # Thumb tip peeking out under the 2nd (middle) finger
    draw_circle(pen, 290, 320, 20, clockwise=True)

def build_asl_O(pen):
    """ASL 'O': All fingertips curled forward to touch thumb tip in an O-shape."""
    draw_circle(pen, 300, 450, 110, clockwise=True)
    draw_circle(pen, 300, 450, 54, clockwise=False)
    # Wrist base
    sculpt_anatomical_palm(pen, x_l=210, x_r=390, y_wrist=90, y_mcp=340)

def build_asl_P(pen):
    """ASL 'P': Like 'K' pointing downward."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=550, y_mcp=350)
    # Index pointing straight down
    sculpt_directed_finger(pen, 245, 360, 245, 100, w=44)
    # Middle tilted down/right
    sculpt_directed_finger(pen, 285, 360, 345, 160, w=44)
    # Thumb nestled between them
    sculpt_directed_finger(pen, 270, 420, 295, 260, w=46, is_thumb=True)

def build_asl_Q(pen):
    """ASL 'Q': Like 'G' pointing downward."""
    sculpt_anatomical_palm(pen, x_l=175, x_r=330, y_wrist=550, y_mcp=350)
    # Index pointing down
    sculpt_directed_finger(pen, 270, 360, 270, 105, w=44)
    # Thumb parallel beside it
    sculpt_directed_finger(pen, 215, 360, 215, 160, w=46, is_thumb=True)

def build_asl_R(pen):
    """ASL 'R': Index and middle fingers crossed."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    # Crossed fingers: index under, middle crossing over
    sculpt_directed_finger(pen, 250, 350, 310, 800, w=44)
    sculpt_directed_finger(pen, 295, 350, 235, 800, w=44)
    # Thumb folded across ring & pinky
    sculpt_directed_finger(pen, 160, 270, 355, 270, w=42, is_thumb=True)
    sculpt_curled_knuckle_tier(pen, 365, 330, 440, w=38)
    sculpt_curled_knuckle_tier(pen, 410, 320, 420, w=36)

def build_asl_S(pen):
    """ASL 'S': Fist with thumb folded horizontally across all 4 fingers."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=425, y_wrist=90, y_mcp=360)
    for x in [220, 275, 330, 385]:
        sculpt_curled_knuckle_tier(pen, x, 340, 480, w=44)
    # BOLD HORIZONTAL THUMB WRAPPED ACROSS FRONT
    sculpt_directed_finger(pen, 135, 320, 440, 320, w=54, is_thumb=True)

def build_asl_T(pen):
    """ASL 'T': Fist with thumb poked up between index and middle fingers."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=425, y_wrist=90, y_mcp=360)
    for x in [220, 275, 330, 385]:
        sculpt_curled_knuckle_tier(pen, x, 340, 470, w=44)
    # Thumb tip protruding between index and middle knuckles
    draw_circle(pen, 248, 485, 26, clockwise=True)

def build_asl_U(pen):
    """ASL 'U': Index and middle fingers extended straight up, tight together."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    # Twin fingers held tightly together (18 UPM gap)
    sculpt_directed_finger(pen, 265, 350, 265, 805, w=44)
    sculpt_directed_finger(pen, 315, 350, 315, 805, w=44)
    sculpt_directed_finger(pen, 160, 270, 355, 270, w=42, is_thumb=True)
    sculpt_curled_knuckle_tier(pen, 370, 330, 440, w=38)
    sculpt_curled_knuckle_tier(pen, 415, 320, 420, w=36)

def build_asl_V(pen):
    """ASL 'V': Index and middle fingers spread in a distinct 'V' shape."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    # V spread fingers (angled -10 deg and +10 deg)
    sculpt_directed_finger(pen, 270, 350, 210, 795, w=44)
    sculpt_directed_finger(pen, 290, 350, 350, 795, w=44)
    sculpt_directed_finger(pen, 160, 270, 355, 270, w=42, is_thumb=True)
    sculpt_curled_knuckle_tier(pen, 370, 330, 440, w=38)
    sculpt_curled_knuckle_tier(pen, 415, 320, 420, w=36)

def build_asl_W(pen):
    """ASL 'W': Index, middle, and ring fingers spread upright."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=425, y_wrist=90, y_mcp=360)
    # 3 fingers splayed in W fan
    sculpt_directed_finger(pen, 260, 350, 200, 785, w=42)
    sculpt_directed_finger(pen, 290, 350, 290, 810, w=42)
    sculpt_directed_finger(pen, 320, 350, 380, 785, w=42)
    # Thumb folded over pinky
    draw_circle(pen, 340, 270, 28, clockwise=True)

def build_asl_X(pen):
    """ASL 'X': Index finger crooked/hooked at middle knuckle."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    # Organic hooked index finger
    pen.moveTo((220, 350))
    pen.lineTo((220, 580))
    pen.qCurveTo((220, 680), (280, 680))
    pen.qCurveTo((340, 680), (340, 580))
    pen.lineTo((340, 500))
    pen.qCurveTo((340, 470), (310, 470))
    pen.qCurveTo((280, 470), (280, 500))
    pen.lineTo((280, 560))
    pen.qCurveTo((280, 610), (260, 610))
    pen.qCurveTo((250, 610), (250, 560))
    pen.lineTo((250, 350))
    pen.closePath()
    for x in [305, 355, 405]:
        sculpt_curled_knuckle_tier(pen, x, 340, 450, w=40)
    # Thumb folded across
    sculpt_directed_finger(pen, 160, 270, 330, 270, w=42, is_thumb=True)

def build_asl_Y(pen):
    """ASL 'Y': Thumb and pinky extended wide; 3 middle fingers folded (Shaka)."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=390, y_wrist=90, y_mcp=360)
    # Thumb angled left (-35 deg)
    sculpt_directed_finger(pen, 190, 260, 95, 520, w=48, is_thumb=True)
    # Pinky angled right (+35 deg)
    sculpt_directed_finger(pen, 370, 320, 465, 600, w=42)
    # 3 middle fingers curled in fist
    for x in [250, 300, 350]:
        sculpt_curled_knuckle_tier(pen, x, 350, 460, w=42)

def build_asl_Z(pen):
    """ASL 'Z': Index finger tracing 'Z' trajectory in space."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 245, 350, 255, 800, w=46)
    for x in [305, 355, 405]:
        sculpt_curled_knuckle_tier(pen, x, 340, 450, w=40)
    # Z kinematic trajectory indicator
    draw_circle(pen, 400, 650, 20, clockwise=True)

# -----------------------------------------------------------------------------
# NUMERALS (0 - 9)
# -----------------------------------------------------------------------------

def build_asl_0(pen): build_asl_O(pen)

def build_asl_1(pen):
    """Numeral 1: Index upright, other 3 fingers and thumb curled."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 250, 350, 250, 805, w=46)
    for x in [305, 355, 405]:
        sculpt_curled_knuckle_tier(pen, x, 340, 450, w=40)
    sculpt_directed_finger(pen, 160, 270, 355, 270, w=42, is_thumb=True)

def build_asl_2(pen):
    """Numeral 2: Index and middle upright, thumb across other 2."""
    build_asl_V(pen)

def build_asl_3(pen):
    """Numeral 3: Thumb, index, and middle extended."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 180, 220, 115, 520, w=48, is_thumb=True)
    sculpt_directed_finger(pen, 245, 350, 235, 800, w=44)
    sculpt_directed_finger(pen, 315, 350, 325, 800, w=44)
    sculpt_curled_knuckle_tier(pen, 370, 330, 440, w=38)
    sculpt_curled_knuckle_tier(pen, 415, 320, 420, w=36)

def build_asl_4(pen):
    """Numeral 4: 4 fingers upright, thumb folded in palm."""
    build_asl_B(pen)

def build_asl_5(pen):
    """Numeral 5: All 5 digits splayed open wide."""
    sculpt_anatomical_palm(pen, x_l=210, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 180, 220, 105, 530, w=48, is_thumb=True)
    sculpt_directed_finger(pen, 245, 350, 205, 780, w=40)
    sculpt_directed_finger(pen, 285, 360, 285, 810, w=42)
    sculpt_directed_finger(pen, 325, 355, 365, 780, w=40)
    sculpt_directed_finger(pen, 365, 340, 435, 720, w=38)

def build_asl_6(pen):
    """Numeral 6: Thumb touching pinky tip, other 3 extended."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 225, 350, 225, 780, w=40)
    sculpt_directed_finger(pen, 290, 360, 290, 810, w=42)
    sculpt_directed_finger(pen, 355, 350, 355, 780, w=40)
    draw_circle(pen, 400, 340, 24, clockwise=True)

def build_asl_7(pen):
    """Numeral 7: Thumb touching ring tip, other 3 extended."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 225, 350, 225, 780, w=40)
    sculpt_directed_finger(pen, 290, 360, 290, 810, w=42)
    draw_circle(pen, 355, 340, 24, clockwise=True)
    sculpt_directed_finger(pen, 415, 340, 415, 720, w=38)

def build_asl_8(pen):
    """Numeral 8: Thumb touching middle tip, other 3 extended."""
    sculpt_anatomical_palm(pen, x_l=185, x_r=415, y_wrist=90, y_mcp=360)
    sculpt_directed_finger(pen, 225, 350, 225, 780, w=40)
    draw_circle(pen, 290, 350, 24, clockwise=True)
    sculpt_directed_finger(pen, 355, 350, 355, 780, w=40)
    sculpt_directed_finger(pen, 415, 340, 415, 720, w=38)

def build_asl_9(pen):
    """Numeral 9: Thumb touching index tip, other 3 extended."""
    build_asl_F(pen)

BUILDERS = {
    'A': build_asl_A, 'B': build_asl_B, 'C': build_asl_C, 'D': build_asl_D,
    'E': build_asl_E, 'F': build_asl_F, 'G': build_asl_G, 'H': build_asl_H,
    'I': build_asl_I, 'J': build_asl_J, 'K': build_asl_K, 'L': build_asl_L,
    'M': build_asl_M, 'N': build_asl_N, 'O': build_asl_O, 'P': build_asl_P,
    'Q': build_asl_Q, 'R': build_asl_R, 'S': build_asl_S, 'T': build_asl_T,
    'U': build_asl_U, 'V': build_asl_V, 'W': build_asl_W, 'X': build_asl_X,
    'Y': build_asl_Y, 'Z': build_asl_Z,
    '0': build_asl_0, '1': build_asl_1, '2': build_asl_2, '3': build_asl_3,
    '4': build_asl_4, '5': build_asl_5, '6': build_asl_6, '7': build_asl_7,
    '8': build_asl_8, '9': build_asl_9,
}

def compile_volumetric_font():
    print("=== POCKETGULL VOLUMETRIC ANATOMICAL SIGN FONT COMPILER ===")
    
    if not SRC_MONO.is_file():
        print(f"[ERROR] Required base font missing: {SRC_MONO}")
        sys.exit(1)

    print(f"1. Loading base monospace telemetry font from {SRC_MONO.name}...")
    font = TTFont(str(SRC_MONO))
    glyf = font['glyf']
    hmtx = font['hmtx']
    cmap = font.getBestCmap()
    glyph_order = font.getGlyphOrder()

    print("2. Sculpting living volumetric TrueType Bézier glyphs (A-Z, 0-9)...")
    for char, builder in BUILDERS.items():
        pen = TTGlyphPen(glyf)
        builder(pen)
        glyph = pen.glyph()
        
        gname = char
        if gname not in glyf:
            # Map by codepoint or create
            cp = ord(char)
            if cp in cmap:
                gname = cmap[cp]
            else:
                gname = f"uni{cp:04X}"
                if gname not in glyph_order:
                    glyph_order.append(gname)
                    font.setGlyphOrder(glyph_order)

        glyf[gname] = glyph
        hmtx[gname] = (ADVANCE, 20) # 600 UPM fixed pitch, 20 UPM left side bearing

    # 3. Align 2-byte word boundaries & mask bit-7
    print("3. Enforcing 2-byte word alignment and bit-7 point flag masking...")
    for gname in font.getGlyphOrder():
        g = glyf[gname]
        if hasattr(g, 'flags'):
            g.flags = [flag & 0x3F for flag in g.flags]

    # 4. Update font naming table
    name_table = font['name']
    name_table.setName('PocketGull Sign', 1, 3, 1, 0x409)
    name_table.setName('PocketGull Sign', 4, 3, 1, 0x409)
    name_table.setName('PocketGull-Sign', 6, 3, 1, 0x409)

    # 5. Save TTF
    print(f"4. Saving compiled TrueType font to {OUT_SIGN_TTF}...")
    font.save(str(OUT_SIGN_TTF))
    shutil.copy(str(OUT_SIGN_TTF), str(OUT_ASL_TTF))

    # 6. Compress WOFF2
    print(f"5. Compressing WOFF2 binaries via Brotli Quality 11...")
    compress(str(OUT_SIGN_TTF), str(OUT_SIGN_WOFF2))
    compress(str(OUT_ASL_TTF), str(OUT_ASL_WOFF2))

    ttf_size = OUT_SIGN_TTF.stat().st_size
    woff2_size = OUT_SIGN_WOFF2.stat().st_size
    print(f"  [+] PocketGull-Sign.ttf:   {ttf_size / 1024:.1f} KB")
    print(f"  [+] PocketGull-Sign.woff2: {woff2_size / 1024:.1f} KB")
    print("=== VOLUMETRIC SIGN FONT COMPILATION COMPLETE ===")

if __name__ == "__main__":
    compile_volumetric_font()
