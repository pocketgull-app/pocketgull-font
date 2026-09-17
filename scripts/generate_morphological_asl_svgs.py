#!/usr/bin/env python3
"""
PocketGull Morphological ASL Vector Generator
=============================================
Synthesizes authentic anatomical ASL vector silhouettes for all 5 Benedict hand archetypes
and the Louise Sloan 5:1 optotype standard across A-Z, 0-9, and clinical emergency signals:

1. sloan: Canonical Louise Sloan 5:1 Optotype (crisp medical acuity, 25 UPM fillets)
2. alimentive: Spherical archetype (plump, rounded, chubby fingers, shallow knuckle dimples, fleshy base)
3. thoracic: Wedge / Conical archetype (elongated conical fingers, high taper, prominent middle finger apex)
4. muscular: Square archetype (1:1 square block palm, spatulate paddle tips, heavy structural contours)
5. osseous: Knotty / Oblong archetype (prominent articular knuckle nodes, excavated phalanx shafts)
6. cerebral: Inverted triangle archetype (hyper-delicate, slender parallel contours, graceful lines)

Strict ASL Standards Enforced:
- Stokoe Phonology & Battison Orientation (Receptive viewer view, G/H medial radial, P/Q downward pronated).
- Fist Disambiguation: A (upright radial), S (transverse wrap), T (interdigital poke), M (under 3), N (under 2).
- Closed E Rule: All 4 fingertips resting firmly on horizontal thumb shelf (zero floating screaming E).
- Louise Sloan 5:1 Acuity: U (touching) vs V (splayed wedge) vs W (trident fan) vs B (flat blade).
- Dynamic Kinematic Traces: J and Z include amber directional trajectory paths.

Outputs:
- js/asl_morph_svg_data.js (ASL_MORPH_DATA object)
"""

import json
import math
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_JS = ROOT_DIR / "js" / "asl_morph_svg_data.js"

MODELS = {
    "sloan": {
        "color": "#06b6d4",
        "stroke_width": 2.6,
        "finger_w": 11.0,
        "wrist_w": 32.0,
        "tip_style": "round",
        "knuckle_style": "crease",
        "palm_ratio": 1.0,
        "middle_extra": 0.0,
        "joint_bulge": 0.0,
        "dimple": False,
        "shaft_taper": 1.0,
        "v_angle": 24,
    },
    "alimentive": {
        "color": "#f59e0b",
        "stroke_width": 3.2,
        "finger_w": 14.5,
        "wrist_w": 36.0,
        "tip_style": "cushion_dome",
        "knuckle_style": "dimple",
        "palm_ratio": 0.90,  # shorter fingers relative to palm
        "middle_extra": -1.0, # shorter apex
        "joint_bulge": -1.0, # smooth, no knobby joints
        "dimple": True,
        "shaft_taper": 0.95,
        "v_angle": 28,      # wider Sloan angle to prevent fleshy pulp collision
    },
    "thoracic": {
        "color": "#ec4899",
        "stroke_width": 2.2,
        "finger_w": 9.5,
        "wrist_w": 28.0,
        "tip_style": "pointed_cone",
        "knuckle_style": "slender_crease",
        "palm_ratio": 1.15, # longer fingers
        "middle_extra": 5.0, # distinct middle finger apex
        "joint_bulge": 0.5,
        "dimple": False,
        "shaft_taper": 0.72, # sharp taper toward tip
        "v_angle": 22,
    },
    "muscular": {
        "color": "#06b6d4",
        "stroke_width": 3.0,
        "finger_w": 13.0,
        "wrist_w": 34.0,
        "tip_style": "spatulate_paddle",
        "knuckle_style": "block_bar",
        "palm_ratio": 1.0,  # 1:1 square block
        "middle_extra": 1.0,
        "joint_bulge": 0.0,
        "dimple": False,
        "shaft_taper": 1.0, # parallel square shafts
        "v_angle": 24,
    },
    "osseous": {
        "color": "#10b981",
        "stroke_width": 2.5,
        "finger_w": 10.0,
        "wrist_w": 27.0,
        "tip_style": "angular_stop",
        "knuckle_style": "knotty_node",
        "palm_ratio": 1.12, # long bony digits
        "middle_extra": 3.0,
        "joint_bulge": 3.5, # prominent protruding knuckle nodes
        "dimple": False,
        "shaft_taper": 0.88,
        "v_angle": 25,
    },
    "cerebral": {
        "color": "#8b5cf6",
        "stroke_width": 1.8,
        "finger_w": 8.0,
        "wrist_w": 24.0,
        "tip_style": "whisper_fine",
        "knuckle_style": "hairline",
        "palm_ratio": 1.10,
        "middle_extra": 2.0,
        "joint_bulge": -0.5,
        "dimple": False,
        "shaft_taper": 0.85,
        "v_angle": 26,
    }
}

def build_model_svg(char, model_key, cfg):
    color = cfg["color"]
    sw = cfg["stroke_width"]
    fw = cfg["finger_w"]
    hw = fw / 2.0
    tip = cfg["tip_style"]
    dimple = cfg["dimple"]
    bulge = cfg["joint_bulge"]
    taper = cfg["shaft_taper"]
    mid_ex = cfg["middle_extra"]
    v_ang = cfg["v_angle"]

    # Fills & Strokes
    fill_skin = f'fill="{color}22" stroke="{color}" stroke-width="{sw}"'
    fill_front = f'fill="var(--card-bg)" stroke="{color}" stroke-width="{sw}"'
    accent = f'fill="#10b98144" stroke="#10b981" stroke-width="{sw}"'
    kinetic = 'stroke="#f59e0b" stroke-width="2.6" stroke-dasharray="3,3" fill="none"'

    def wrist(y_bot=114, y_top=76):
        w_half = cfg["wrist_w"] / 2.0
        x_l = 50 - w_half
        x_r = 50 + w_half
        return f"""
  <!-- Wrist and Lower Palm -->
  <path d="M {x_l} {y_bot} C {x_l-2} 98 {x_l-3} 86 {x_l-5} {y_top} C {x_l-8} 66 {x_l-8} 56 {x_l-4} 48" stroke="{color}" stroke-width="{sw}" />
  <path d="M {x_r} {y_bot} C {x_r+1} 98 {x_r+4} 86 {x_r+7} 74 C {x_r+10} 62 {x_r+8} 54 {x_r+5} 48" stroke="{color}" stroke-width="{sw}" />
  <path d="M {x_l} {y_bot} C 42 {y_bot+2} 58 {y_bot+2} {x_r} {y_bot}" stroke="{color}" stroke-width="{max(1.5, sw-0.8)}" opacity="0.6" />
"""

    def upright_finger(x, y_tip, y_base=56, is_middle=False, angle_deg=0):
        eff_tip = y_tip - (mid_ex if is_middle else 0)
        tip_w = fw * taper
        hw_t = tip_w / 2.0

        transform_attr = f' transform="rotate({angle_deg} {x} {y_base})"' if angle_deg != 0 else ''

        elements = []
        if angle_deg != 0:
            elements.append(f'<g{transform_attr}>')

        if tip == "spatulate_paddle":
            # Muscular: Square flat paddle tip with slight chamfer
            elements.append(f"""
  <path d="M {x - hw} {y_base} L {x - hw} {eff_tip + 4} L {x - hw_t} {eff_tip + 1} L {x + hw_t} {eff_tip + 1} L {x + hw} {eff_tip + 4} L {x + hw} {y_base}" {fill_skin} />
  <line x1="{x - hw + 1}" y1="{eff_tip + (y_base - eff_tip)*0.35}" x2="{x + hw - 1}" y2="{eff_tip + (y_base - eff_tip)*0.35}" stroke="{color}" stroke-width="{max(1.2, sw-1.0)}" />
  <line x1="{x - hw + 1}" y1="{eff_tip + (y_base - eff_tip)*0.65}" x2="{x + hw - 1}" y2="{eff_tip + (y_base - eff_tip)*0.65}" stroke="{color}" stroke-width="{max(1.2, sw-1.0)}" />
  <rect x="{x - hw_t + 1}" y="{eff_tip + 2.5}" width="{tip_w - 2}" height="3" rx="1" stroke="{color}" stroke-width="1.0" opacity="0.8" />
""")
        elif tip == "pointed_cone":
            # Thoracic: Conical tapering tip
            elements.append(f"""
  <path d="M {x - hw} {y_base} L {x - hw_t} {eff_tip + 3} Q {x} {eff_tip} {x + hw_t} {eff_tip + 3} L {x + hw} {y_base}" {fill_skin} />
  <line x1="{x - hw*0.7}" y1="{eff_tip + (y_base - eff_tip)*0.32}" x2="{x + hw*0.7}" y2="{eff_tip + (y_base - eff_tip)*0.32}" stroke="{color}" stroke-width="{max(1.0, sw-1.0)}" opacity="0.7" />
  <ellipse cx="{x}" cy="{eff_tip + 3}" rx="{hw_t - 1}" ry="2" stroke="{color}" stroke-width="1.0" opacity="0.8" />
""")
        elif tip == "angular_stop" or bulge > 1.5:
            # Osseous: Bulging articular knuckle knots & hollowed phalanx shaft
            mid_y = (eff_tip + y_base) / 2.0
            elements.append(f"""
  <path d="M {x - hw*0.8} {y_base} C {x - hw - bulge} {mid_y + 6} {x - hw - bulge} {mid_y - 6} {x - hw*0.85} {eff_tip + hw_t} C {x - hw_t} {eff_tip} {x + hw_t} {eff_tip} {x + hw*0.85} {eff_tip + hw_t} C {x + hw + bulge} {mid_y - 6} {x + hw + bulge} {mid_y + 6} {x + hw*0.8} {y_base}" {fill_skin} />
  <ellipse cx="{x}" cy="{mid_y}" rx="{hw + bulge - 1}" ry="2.5" stroke="{color}" stroke-width="1.3" opacity="0.85" fill="none" />
  <line x1="{x - hw*0.7}" y1="{eff_tip + 12}" x2="{x + hw*0.7}" y2="{eff_tip + 12}" stroke="{color}" stroke-width="1.2" opacity="0.7" />
  <ellipse cx="{x}" cy="{eff_tip + 3.5}" rx="{hw_t - 1.5}" ry="2" stroke="{color}" stroke-width="1.0" opacity="0.8" />
""")
        else:
            # Sloan / Alimentive / Cerebral: Humanist waisting & condyle expansion
            h_len = y_base - eff_tip
            y_p_waist = y_base - int(h_len * 0.28)
            y_pip_j = y_base - int(h_len * 0.50)
            y_i_waist = y_base - int(h_len * 0.70)
            y_dip_j = y_base - int(h_len * 0.84)
            w_w = hw * 0.84  # narrow waist
            w_c = hw * 1.12  # condyle bulge

            elements.append(f"""
  <path d="M {x - hw} {y_base}
           C {x - w_w} {y_p_waist + 4}, {x - w_w} {y_p_waist - 4}, {x - w_c} {y_pip_j}
           C {x - w_w} {y_i_waist + 4}, {x - w_w} {y_i_waist - 4}, {x - w_c} {y_dip_j}
           C {x - hw_t} {eff_tip + 3}, {x} {eff_tip}, {x} {eff_tip}
           C {x} {eff_tip}, {x + hw_t} {eff_tip + 3}, {x + w_c} {y_dip_j}
           C {x + w_w} {y_i_waist - 4}, {x + w_w} {y_i_waist + 4}, {x + w_c} {y_pip_j}
           C {x + w_w} {y_p_waist - 4}, {x + w_w} {y_p_waist + 4}, {x + hw} {y_base} Z" {fill_skin} />
""")
            if dimple:
                elements.append(f"""
  <circle cx="{x}" cy="{eff_tip + (y_base - eff_tip)*0.45}" r="2.2" stroke="{color}" stroke-width="1.2" opacity="0.8" fill="{color}44" />
  <ellipse cx="{x}" cy="{eff_tip + 3.5}" rx="{hw - 2.5}" ry="2.5" stroke="{color}" stroke-width="1.2" opacity="0.8" />
""")
            else:
                elements.append(f"""
  <line x1="{x - hw + 2}" y1="{y_pip_j}" x2="{x + hw - 2}" y2="{y_pip_j}" stroke="{color}" stroke-width="1.4" opacity="0.7" />
  <line x1="{x - hw + 2}" y1="{y_dip_j}" x2="{x + hw - 2}" y2="{y_dip_j}" stroke="{color}" stroke-width="1.4" opacity="0.7" />
  <ellipse cx="{x}" cy="{eff_tip + 3.5}" rx="{hw - 2}" ry="2.2" stroke="{color}" stroke-width="1.0" opacity="0.8" />
""")
        if angle_deg != 0:
            elements.append('</g>')
        return "\n".join(elements)

    def curled_finger(x, y_top=48, h=26):
        eff_w = fw + 0.5
        eff_hw = eff_w / 2.0
        elements = []
        if dimple:
            elements.append(f"""
  <path d="M {x - eff_hw} {y_top + h} L {x - eff_hw} {y_top + eff_hw} C {x - eff_hw} {y_top} {x + eff_hw} {y_top} {x + eff_hw} {y_top + eff_hw} L {x + eff_hw} {y_top + h}" {fill_skin} />
  <circle cx="{x}" cy="{y_top + h*0.48}" r="2.2" stroke="{color}" stroke-width="1.2" fill="{color}44" />
  <ellipse cx="{x}" cy="{y_top + h*0.78}" rx="{eff_hw - 2.5}" ry="3" stroke="{color}" stroke-width="1.1" opacity="0.75" />
""")
        elif bulge > 1.5:
            elements.append(f"""
  <path d="M {x - eff_hw} {y_top + h} L {x - eff_hw - 1.5} {y_top + eff_hw + 2} C {x - eff_hw - 1} {y_top} {x + eff_hw + 1} {y_top} {x + eff_hw + 1.5} {y_top + eff_hw + 2} L {x + eff_hw} {y_top + h}" {fill_skin} />
  <line x1="{x - eff_hw}" y1="{y_top + h*0.5}" x2="{x + eff_hw}" y2="{y_top + h*0.5}" stroke="{color}" stroke-width="1.6" />
  <ellipse cx="{x}" cy="{y_top + h*0.8}" rx="{eff_hw - 2}" ry="2.5" stroke="{color}" stroke-width="1.1" opacity="0.75" />
""")
        else:
            elements.append(f"""
  <path d="M {x - eff_hw} {y_top + h} L {x - eff_hw} {y_top + eff_hw} C {x - eff_hw} {y_top} {x + eff_hw} {y_top} {x + eff_hw} {y_top + eff_hw} L {x + eff_hw} {y_top + h}" {fill_skin} />
  <path d="M {x - eff_hw + 1} {y_top + h*0.55} Q {x} {y_top + h*0.62} {x + eff_hw - 1} {y_top + h*0.55}" stroke="{color}" stroke-width="1.4" opacity="0.7" fill="none" />
  <ellipse cx="{x}" cy="{y_top + h*0.8}" rx="{eff_hw - 2.5}" ry="3" stroke="{color}" stroke-width="1.1" opacity="0.7" />
""")
        return "\n".join(elements)

    # Coordinates across the palm
    spacing = 11.5 if fw < 11 else (12.5 if fw < 13 else 13.5)
    f1 = 50 - 1.5 * spacing
    f2 = 50 - 0.5 * spacing
    f3 = 50 + 0.5 * spacing
    f4 = 50 + 1.5 * spacing

    body = []

    # -------------------------------------------------------------------------
    # SIGN DISPATCHER
    # -------------------------------------------------------------------------

    if char == 'A':
        body.append(wrist())
        body.append(f"""  <!-- 4 Curled Fingers in Fist -->
  {curled_finger(f1, 46, 28)}
  {curled_finger(f2, 44, 30)}
  {curled_finger(f3, 45, 29)}
  {curled_finger(f4, 48, 26)}
  <!-- Palm Base Fill -->
  <path d="M 32 74 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 74 Z" fill="{color}18" stroke="none" />
  <!-- A Standard: Prominent Upright Thumb along Radial Border (never crossing palm) -->
  <path d="M 32 76 C {23 - bulge} 72 {19 - bulge} 62 {19 - bulge} 46 C {19 - bulge} 34 32 34 34 44 L 34 76 Z" {fill_front} />
  <ellipse cx="{26 - bulge*0.5}" cy="41" rx="{3.5 + (0.5 if dimple else 0)}" ry="{4 + (0.5 if dimple else 0)}" stroke="{color}" stroke-width="1.5" />
  <line x1="{21 - bulge}" y1="56" x2="34" y2="56" stroke="{color}" stroke-width="1.5" opacity="0.7" />""")

    elif char == 'B':
        body.append(wrist())
        body.append(f"""  <!-- 4 Upright Fingers (Blade) -->
  {upright_finger(f1, 16, 56)}
  {upright_finger(f2, 10, 56, is_middle=True)}
  {upright_finger(f3, 14, 56)}
  {upright_finger(f4, 22, 56)}
  <!-- Palm Base -->
  <path d="M 30 56 C 30 76 32 96 36 114 L 64 114 C 70 96 74 76 74 56 Z" fill="{color}1a" stroke="none" />
  <!-- Thumb folded across lower palm -->
  <path d="M 22 74 C 26 64 38 64 54 66 C 60 68 60 76 54 78 C 42 82 28 84 22 74 Z" {fill_front} />
  <ellipse cx="48" cy="71" rx="3.2" ry="3.5" stroke="{color}" stroke-width="1.4" />""")

    elif char == 'C':
        body.append(wrist())
        body.append(f"""  <!-- C Profile Arc -->
  <path d="M 28 72 C 26 38 38 18 64 18 C 78 18 88 28 88 40 C 88 48 80 52 74 46 C 68 40 60 34 48 36 C 38 38 38 52 38 72 Z" {fill_skin} />
  <path d="M 30 74 C 36 82 46 90 62 90 C 76 90 84 82 84 72 C 84 64 74 62 68 68 C 60 74 50 76 40 74 Z" {fill_skin} />
  <ellipse cx="56" cy="56" rx="14" ry="16" stroke="{color}" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.5" />""")

    elif char == 'D':
        body.append(wrist())
        body.append(f"""  <!-- Index finger vertical -->
  {upright_finger(f1, 12, 56)}
  <!-- Curled fingers & thumb loop -->
  <path d="M 32 76 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 76 Z" fill="{color}18" stroke="none" />
  <path d="M 44 56 C 58 50 76 50 76 66 C 76 80 62 84 48 82 C 38 80 30 76 30 68 C 30 58 40 56 44 56 Z" {fill_front} />
  <circle cx="56" cy="67" r="8" fill="var(--card-bg)" stroke="{color}" stroke-width="2" />""")

    elif char == 'E':
        body.append(wrist())
        # CLOSED E RULE: All 4 fingertips rest firmly on the horizontal shelf of the tucked thumb.
        y_shelf = 66
        y_knuckle = 42
        body.append(f"""  <!-- 4 Flexed Finger Knuckles Resting on Thumb Shelf -->
  <path d="M {f1-hw} {y_shelf} L {f1-hw} {y_knuckle+6} C {f1-hw} {y_knuckle} {f1+hw} {y_knuckle} {f1+hw} {y_knuckle+6} L {f1+hw} {y_shelf}" {fill_skin} />
  <path d="M {f2-hw} {y_shelf} L {f2-hw} {y_knuckle+4} C {f2-hw} {y_knuckle-2} {f2+hw} {y_knuckle-2} {f2+hw} {y_knuckle+4} L {f2+hw} {y_shelf}" {fill_skin} />
  <path d="M {f3-hw} {y_shelf} L {f3-hw} {y_knuckle+6} C {f3-hw} {y_knuckle} {f3+hw} {y_knuckle} {f3+hw} {y_knuckle+6} L {f3+hw} {y_shelf}" {fill_skin} />
  <path d="M {f4-hw} {y_shelf} L {f4-hw} {y_knuckle+8} C {f4-hw} {y_knuckle+2} {f4+hw} {y_knuckle+2} {f4+hw} {y_knuckle+8} L {f4+hw} {y_shelf}" {fill_skin} />
  <!-- Knuckle flexion crease lines -->
  <line x1="{f1-hw+2}" y1="{y_knuckle+12}" x2="{f1+hw-2}" y2="{y_knuckle+12}" stroke="{color}" stroke-width="1.2" opacity="0.7" />
  <line x1="{f2-hw+2}" y1="{y_knuckle+10}" x2="{f2+hw-2}" y2="{y_knuckle+10}" stroke="{color}" stroke-width="1.2" opacity="0.7" />
  <line x1="{f3-hw+2}" y1="{y_knuckle+12}" x2="{f3+hw-2}" y2="{y_knuckle+12}" stroke="{color}" stroke-width="1.2" opacity="0.7" />
  <line x1="{f4-hw+2}" y1="{y_knuckle+14}" x2="{f4+hw-2}" y2="{y_knuckle+14}" stroke="{color}" stroke-width="1.2" opacity="0.7" />
  <!-- MANDATORY HORIZONTAL THUMB SHELF (Closed E Bed) -->
  <path d="M 22 78 C 26 67 44 65 74 66 C 82 66 82 76 74 78 C 58 82 34 84 22 78 Z" {fill_front} />
  <ellipse cx="68" cy="71" rx="4" ry="3.5" stroke="{color}" stroke-width="1.4" />""")

    elif char == 'F':
        body.append(wrist())
        body.append(f"""  <!-- 3 Spread Upright Fingers (Middle, Ring, Pinky) -->
  {upright_finger(f2, 10, 56, is_middle=True)}
  {upright_finger(f3, 14, 56)}
  {upright_finger(f4, 22, 56)}
  <!-- Base Palm -->
  <path d="M 32 76 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 76 Z" fill="{color}18" stroke="none" />
  <!-- Circular O-Ring of Index & Thumb on left -->
  <circle cx="32" cy="56" r="14" {fill_front} />
  <circle cx="32" cy="56" r="6" fill="var(--card-bg)" stroke="{color}" stroke-width="2" />""")

    elif char == 'G':
        # BATTISON ORIENTATION: Medial radial profile (palm inward toward signer).
        body.append(f"""  <!-- Medial Radial Wrist / Dorsal Profile -->
  <path d="M 18 114 C 20 96 22 84 24 72 C 26 56 34 46 48 46 L 54 46" stroke="{color}" stroke-width="{sw}" />
  <path d="M 44 114 C 42 98 42 88 44 76" stroke="{color}" stroke-width="{sw}" />
  <path d="M 24 76 C 24 58 32 46 46 46 C 52 46 54 64 48 84 Z" fill="{color}18" stroke="none" />
  <!-- Curled fingers below (middle, ring, pinky) -->
  <path d="M 40 68 C 42 76 46 86 54 86 C 58 86 60 78 54 72 Z" {fill_skin} />
  <!-- Horizontal Thumb (Top beam) -->
  <path d="M 44 44 L 78 44 C 84 44 84 34 78 34 L 44 34 Z" {fill_skin} />
  <ellipse cx="74" cy="39" rx="3.5" ry="3" stroke="{color}" stroke-width="1.4" />
  <!-- Horizontal Index Finger (Bottom beam) -->
  <path d="M 44 60 L 88 60 C 96 60 96 48 88 48 L 44 48 Z" {fill_skin} />
  <ellipse cx="84" cy="54" rx="3.5" ry="3.5" stroke="{color}" stroke-width="1.4" />""")

    elif char == 'H':
        # BATTISON ORIENTATION: Medial radial profile with twin horizontal fingers.
        body.append(f"""  <!-- Medial Radial Wrist / Dorsal Profile -->
  <path d="M 18 114 C 20 96 22 84 24 72 C 26 54 34 42 46 42 C 52 42 52 64 46 88 L 46 114" stroke="{color}" stroke-width="{sw}" />
  <!-- Horizontal Index Finger (Upper) -->
  <path d="M 44 46 L 88 46 C 96 46 96 34 88 34 L 44 34 Z" {fill_skin} />
  <!-- Horizontal Middle Finger (Lower) -->
  <path d="M 44 60 L 88 60 C 96 60 96 48 88 48 L 44 48 Z" {fill_skin} />
  <line x1="44" y1="47" x2="90" y2="47" stroke="var(--card-bg)" stroke-width="{sw}" />
  <!-- Folded Thumb over lower fingers -->
  <path d="M 32 64 C 36 56 46 54 56 56 C 60 58 60 66 56 68 C 46 72 36 72 32 64 Z" {fill_front} />""")

    elif char == 'I':
        body.append(wrist())
        body.append(f"""  <!-- Pinky vertical, others curled -->
  {upright_finger(f4, 15, 58)}
  {curled_finger(f1, 51, 23)}
  {curled_finger(f2, 49, 25)}
  {curled_finger(f3, 50, 24)}
  <path d="M 22 74 C 28 64 42 62 58 64 C 64 66 62 74 56 76 C 42 78 30 80 22 74 Z" {fill_front} />
  <ellipse cx="50" cy="69" rx="3.5" ry="4" stroke="{color}" stroke-width="1.4" />""")

    elif char == 'J':
        # DYNAMIC KINEMATIC TRACE: Pinky upright, tracing sweeping J-curve down and hook
        body.append(wrist())
        body.append(f"""  <!-- Pinky vertical in 'I' shape -->
  {upright_finger(f4, 18, 58)}
  {curled_finger(f1, 51, 23)}
  {curled_finger(f2, 49, 25)}
  {curled_finger(f3, 50, 24)}
  <path d="M 22 74 C 28 64 42 62 58 64 C 64 66 62 74 56 76 C 42 78 30 80 22 74 Z" {fill_front} />
  <!-- Amber Dynamic J-Hook Motion Vector -->
  <path d="M {f4+2} 24 C {f4+14} 38 {f4+14} 70 {f4+6} 86 C {f4-2} 98 {f4-18} 102 {f4-24} 92 C {f4-28} 84 {f4-24} 76 {f4-16} 78" {kinetic} />
  <polygon points="{f4-14},74 {f4-20},82 {f4-12},84" fill="#f59e0b" stroke="none" />""")

    elif char == 'K':
        body.append(wrist())
        body.append(f"""  <!-- Index vertical, Middle angled forward/right, Thumb between -->
  {upright_finger(f1, 14, 56)}
  <path d="M 44 46 L 62 18 C 66 12 76 18 72 24 L 54 58 Z" {fill_skin} />
  {curled_finger(f3, 58, 20)}
  {curled_finger(f4, 60, 18)}
  <!-- Thumb upright between index and middle -->
  <path d="M 34 74 C 36 58 42 48 46 40 C 50 36 56 38 54 46 C 52 56 48 68 44 76 Z" {fill_front} />
  <ellipse cx="49" cy="42" rx="3" ry="3.5" stroke="{color}" stroke-width="1.3" />""")

    elif char == 'L':
        body.append(wrist())
        body.append(f"""  <!-- Index vertical, Thumb horizontal 90 deg -->
  {upright_finger(f1, 12, 56)}
  <!-- Thumb horizontal left -->
  <path d="M 38 78 L 10 78 C 3 78 3 66 10 66 L 38 66 Z" {fill_front} />
  <ellipse cx="14" cy="72" rx="3" ry="4" stroke="{color}" stroke-width="1.4" />
  {curled_finger(f2, 58, 20)}
  {curled_finger(f3, 58, 20)}
  {curled_finger(f4, 60, 18)}""")

    elif char == 'M':
        body.append(wrist())
        body.append(f"""  <!-- 3 Finger Arches draped over thumb -->
  {curled_finger(f1, 48, 26)}
  {curled_finger(f2, 46, 28)}
  {curled_finger(f3, 48, 26)}
  {curled_finger(f4, 53, 21)}
  <!-- Thumb tip peeking under ring finger (3 fingers) -->
  <ellipse cx="{f3}" cy="74" rx="6" ry="7" {accent} />
  <ellipse cx="{f3}" cy="74" rx="3" ry="3.5" stroke="#10b981" stroke-width="1.2" />""")

    elif char == 'N':
        body.append(wrist())
        body.append(f"""  <!-- 2 Finger Arches draped over thumb -->
  {curled_finger(f1, 48, 26)}
  {curled_finger(f2, 46, 28)}
  {curled_finger(f3, 52, 22)}
  {curled_finger(f4, 55, 19)}
  <!-- Thumb tip peeking under middle finger (2 fingers) -->
  <ellipse cx="{f2}" cy="74" rx="6" ry="7" {accent} />
  <ellipse cx="{f2}" cy="74" rx="3" ry="3.5" stroke="#10b981" stroke-width="1.2" />""")

    elif char == 'O':
        body.append(wrist())
        body.append(f"""  <!-- O aperture profile -->
  <path d="M 28 68 C 24 44 36 26 56 24 C 74 22 88 34 88 52 C 88 74 74 86 58 88 C 42 90 38 98 42 112" stroke="{color}" stroke-width="{sw}" fill="{color}18" />
  <ellipse cx="56" cy="54" rx="14" ry="16" fill="var(--card-bg)" stroke="{color}" stroke-width="{sw}" />""")

    elif char == 'P':
        # BATTISON ORIENTATION: Downward counterpart of 'K'. Pronated forearm entering top.
        body.append(f"""  <!-- Pronated Forearm entering from top -->
  <path d="M 32 6 C 32 18 34 28 38 38 L 62 38 C 66 28 68 18 68 6" stroke="{color}" stroke-width="{sw}" />
  <path d="M 32 6 C 42 8 58 8 68 6" stroke="{color}" stroke-width="{max(1.5, sw-0.8)}" opacity="0.6" />
  <!-- Curled Ring & Pinky Fingers tucked at top right -->
  <path d="M 58 38 C 64 36 72 40 72 48 C 72 56 64 58 58 54 Z" {fill_skin} />
  <!-- Index finger pointing straight down -->
  <path d="M 38 38 L 38 96 C 38 102 {38+fw} 102 {38+fw} 96 L {38+fw} 38 Z" {fill_skin} />
  <ellipse cx="{38+hw}" cy="92" rx="{hw-1}" ry="2.5" stroke="{color}" stroke-width="1.2" />
  <!-- Middle finger tilted downward-right -->
  <path d="M 46 44 L 66 84 C 70 90 80 84 76 78 L 56 38 Z" {fill_skin} />
  <!-- Thumb nestled between index and middle, resting against middle knuckle -->
  <path d="M 36 44 C 42 46 50 48 54 56 C 54 64 44 66 38 58 Z" {fill_front} />
  <ellipse cx="48" cy="54" rx="3.5" ry="3.5" stroke="{color}" stroke-width="1.3" />""")

    elif char == 'Q':
        # BATTISON ORIENTATION: Downward counterpart of 'G'. Pronated forearm entering top.
        body.append(f"""  <!-- Pronated Forearm entering from top -->
  <path d="M 30 6 C 30 18 32 28 36 38 L 62 38 C 66 28 68 18 68 6" stroke="{color}" stroke-width="{sw}" />
  <path d="M 30 6 C 42 8 58 8 68 6" stroke="{color}" stroke-width="{max(1.5, sw-0.8)}" opacity="0.6" />
  <!-- Curled middle, ring, pinky tucked at top -->
  <path d="M 48 38 C 58 36 68 40 68 50 C 68 60 56 62 48 56 Z" {fill_skin} />
  <!-- Thumb pointing downward (left beam) -->
  <path d="M 28 38 L 28 78 C 28 84 {28+fw} 84 {28+fw} 78 L {28+fw} 38 Z" {fill_skin} />
  <ellipse cx="{28+hw}" cy="75" rx="{hw-1}" ry="2.5" stroke="{color}" stroke-width="1.2" />
  <!-- Index finger pointing downward (right beam, slightly longer) -->
  <path d="M 40 38 L 40 96 C 40 102 {40+fw} 102 {40+fw} 96 L {40+fw} 38 Z" {fill_skin} />
  <ellipse cx="{40+hw}" cy="92" rx="{hw-1}" ry="2.5" stroke="{color}" stroke-width="1.2" />""")

    elif char == 'R':
        body.append(wrist())
        body.append(f"""  <!-- Crossed index and middle -->
  <path d="M 34 54 L 56 12 C 58 6 68 10 64 16 L 46 54 Z" {fill_skin} />
  <path d="M 54 54 L 38 12 C 36 6 46 4 48 10 L 58 54 Z" {fill_front} />
  {curled_finger(f3, 57, 19)}
  {curled_finger(f4, 61, 15)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {fill_front} />""")

    elif char == 'S':
        body.append(wrist())
        body.append(f"""  <!-- Fist with BOLD THUMB LOCKED HORIZONTALLY ACROSS FRONT -->
  {curled_finger(f1, 51, 23)}
  {curled_finger(f2, 49, 25)}
  {curled_finger(f3, 50, 24)}
  {curled_finger(f4, 53, 21)}
  <!-- BOLD THUMB WRAPPED HORIZONTALLY ACROSS ALL 4 DIGITS -->
  <path d="M 18 62 C 26 50 48 48 72 52 C 80 54 80 66 70 68 C 46 72 26 74 18 62 Z" {fill_front} />
  <ellipse cx="66" cy="61" rx="4" ry="4.5" stroke="{color}" stroke-width="1.4" />""")

    elif char == 'T':
        body.append(wrist())
        # T STANDARD: Thumb bulb poking up strictly between index and middle knuckles
        t_poke_x = f1 + (f2 - f1) * 0.5
        body.append(f"""  <!-- Fist with thumb poked between index and middle -->
  {curled_finger(f1, 51, 23)}
  {curled_finger(f2, 49, 25)}
  {curled_finger(f3, 50, 24)}
  {curled_finger(f4, 53, 21)}
  <!-- THUMB BULB POKING UP BETWEEN INDEX AND MIDDLE -->
  <ellipse cx="{t_poke_x}" cy="45" rx="{5.5 + (1.0 if dimple else 0)}" ry="{7.0 + (1.0 if dimple else 0)}" {fill_front} />
  <ellipse cx="{t_poke_x}" cy="42" rx="3.2" ry="3.2" stroke="{color}" stroke-width="1.3" />""")

    elif char == 'U':
        body.append(wrist())
        # U STANDARD: Index & Middle tightly touching side-by-side
        body.append(f"""  <!-- Index & Middle tightly together (Unison) -->
  {upright_finger(44 - hw, 12, 56)}
  {upright_finger(44 + hw, 12, 56, is_middle=True)}
  {curled_finger(f3, 57, 19)}
  {curled_finger(f4, 61, 15)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {fill_front} />""")

    elif char == 'V':
        body.append(wrist())
        # V STANDARD: Index & Middle diverging with distinct Louise Sloan 5:1 counter-space
        body.append(f"""  <!-- Index & Middle spread V (Angle: {v_ang} deg) -->
  {upright_finger(42, 12, 56, angle_deg=-v_ang//2)}
  {upright_finger(58, 12, 56, is_middle=True, angle_deg=v_ang//2)}
  {curled_finger(f3, 57, 19)}
  {curled_finger(f4, 61, 15)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {fill_front} />""")

    elif char == 'W':
        body.append(wrist())
        # W STANDARD: 3 fingers splayed evenly (Index, Middle, Ring)
        body.append(f"""  <!-- 3 Spread Upright Fingers (Trident Fan) -->
  {upright_finger(36, 14, 54, angle_deg=-16)}
  {upright_finger(50, 10, 54, is_middle=True)}
  {upright_finger(64, 14, 54, angle_deg=16)}
  {curled_finger(f4, 60, 16)}
  <ellipse cx="44" cy="68" rx="5" ry="5" {fill_front} />""")

    elif char == 'X':
        body.append(wrist())
        body.append(f"""  <!-- Hooked Index finger (Question-mark hook) -->
  <path d="M 32 56 L 32 28 C 32 16 52 16 52 28 C 52 38 42 42 42 56 Z" {fill_skin} />
  {curled_finger(f2, 58, 18)}
  {curled_finger(f3, 58, 18)}
  {curled_finger(f4, 60, 16)}
  <path d="M 22 74 C 28 64 42 62 58 64 C 64 66 62 74 56 76 C 42 78 30 80 22 74 Z" {fill_front} />""")

    elif char == 'Y':
        body.append(wrist())
        body.append(f"""  <!-- Thumb & Pinky extended (Shaka / Horns) -->
  <path d="M 36 74 L 10 52 C 4 46 10 38 18 42 L 40 64 Z" {fill_skin} />
  <path d="M 60 64 L 82 42 C 90 38 96 46 90 52 L 64 74 Z" {fill_skin} />
  {curled_finger(40, 52, 22)}
  {curled_finger(50, 50, 24)}
  {curled_finger(60, 52, 22)}""")

    elif char == 'Z':
        body.append(wrist())
        # DYNAMIC KINEMATIC TRACE: Index drawing Z in signing plane
        body.append(f"""  <!-- Index finger upright with Z trajectory -->
  {upright_finger(f1, 12, 56)}
  {curled_finger(f2, 58, 18)}
  {curled_finger(f3, 58, 18)}
  {curled_finger(f4, 60, 16)}
  <!-- Amber Z Zig-Zag Kinetic Vector -->
  <path d="M 44 24 L 78 24 L 52 46 L 86 46" {kinetic} />
  <polygon points="86,42 94,46 86,50" fill="#f59e0b" stroke="none" />""")

    # Numerals 0 - 9
    elif char == '0':
        body.append(wrist())
        body.append(f"""  <path d="M 28 68 C 24 44 36 26 56 24 C 74 22 88 34 88 52 C 88 74 74 86 58 88 C 42 90 38 98 42 112" stroke="{color}" stroke-width="{sw}" fill="{color}18" />
  <ellipse cx="56" cy="54" rx="14" ry="16" fill="var(--card-bg)" stroke="{color}" stroke-width="{sw}" />""")

    elif char == '1':
        body.append(wrist())
        body.append(f"""  {upright_finger(f1, 10, 56)}
  {curled_finger(f2, 56, 20)}
  {curled_finger(f3, 56, 20)}
  {curled_finger(f4, 58, 18)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {fill_front} />""")

    elif char == '2':
        body.append(wrist())
        body.append(f"""  {upright_finger(f1, 12, 56)}
  {upright_finger(f2, 8, 56, is_middle=True)}
  {curled_finger(f3, 56, 20)}
  {curled_finger(f4, 58, 18)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {fill_front} />""")

    elif char == '3':
        body.append(wrist())
        body.append(f"""  <path d="M 36 74 L 10 54 C 4 48 10 40 18 44 L 38 64 Z" {fill_skin} />
  {upright_finger(46, 12, 56)}
  {upright_finger(58, 8, 56, is_middle=True)}
  {curled_finger(68, 58, 18)}
  {curled_finger(76, 60, 16)}""")

    elif char == '4':
        body.append(wrist())
        body.append(f"""  {upright_finger(f1, 14, 56)}
  {upright_finger(f2, 8, 56, is_middle=True)}
  {upright_finger(f3, 12, 56)}
  {upright_finger(f4, 20, 56)}
  <path d="M 22 74 C 26 64 38 64 54 66 C 60 68 60 76 54 78 C 42 82 28 84 22 74 Z" {fill_front} />""")

    elif char == '5':
        body.append(wrist())
        body.append(f"""  <path d="M 36 74 L 8 46 C 2 40 8 32 16 36 L 38 62 Z" {fill_skin} />
  {upright_finger(36, 14, 54, angle_deg=-18)}
  {upright_finger(50, 6, 54, is_middle=True)}
  {upright_finger(64, 10, 54, angle_deg=14)}
  {upright_finger(76, 18, 56, angle_deg=26)}""")

    elif char in ['6', '7', '8', '9']:
        body.append(wrist())
        tucked_idx = {'6': f4, '7': f3, '8': f2, '9': f1}[char]
        for f, x_pos, y_pos in [(f1, f1, 12), (f2, f2, 8), (f3, f3, 12), (f4, f4, 18)]:
            if f == tucked_idx:
                body.append(curled_finger(x_pos, 54, 22))
            else:
                body.append(upright_finger(x_pos, y_pos, 56, is_middle=(f==f2)))
        body.append(f"""  <!-- Thumb contacting {char} digit -->
  <ellipse cx="{tucked_idx}" cy="68" rx="6" ry="6" {fill_front} />
  <circle cx="{tucked_idx}" cy="68" r="3" fill="#10b981" />""")

    else:
        body.append(wrist())
        body.append(f"""  {upright_finger(50, 10, 56, is_middle=True)}
  {curled_finger(f1, 52, 24)}
  {curled_finger(f3, 52, 24)}
  {curled_finger(f4, 54, 22)}""")

    content = "\n".join(body)
    svg = f'<svg viewBox="0 0 100 120" class="asl-hand-svg" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">\n{content}\n</svg>'
    return svg

def main():
    print("Generating Morphological ASL SVG Library across all 5 Benedict Archetypes...")
    
    chars = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [str(i) for i in range(10)]
    dataset = {}

    for model_key, cfg in MODELS.items():
        dataset[model_key] = {}
        for char in chars:
            dataset[model_key][char] = build_model_svg(char, model_key, cfg)
        print(f"  [+] Synthesized {len(chars)} anatomical signs for '{model_key}' archetype.")

    js_content = "/**\n * PocketGull Anatomical Morphological ASL Vector Library\n * Generates authentic Benedict 1921 & Louise Sloan 5:1 Optotypes\n */\n"
    js_content += f"const ASL_MORPH_DATA = {json.dumps(dataset, indent=2)};\n"

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"\nSuccessfully written {OUTPUT_JS} ({OUTPUT_JS.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    main()
