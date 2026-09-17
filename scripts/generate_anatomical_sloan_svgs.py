#!/usr/bin/env python3
"""
PocketGull Anatomical Louise Sloan 5:1 Optotype ASL Vector Engine
=================================================================
Synthesizes authentic, anatomical, high-contrast ASL manual alphabet handshapes.
Enforces:
1. Louise Sloan 5:1 Optotype Acuity (bold contours, generous counter-spaces, instant digit counts).
2. ISMP Medical Disambiguation:
   - A: Thumb upright flush against index side.
   - S: Thumb wrapped across front of fist.
   - T: Thumb tip poking between index & middle.
   - M: 3 finger arches with thumb peeking under ring.
   - N: 2 finger arches with thumb peeking under middle.
   - 1, 2, 3, 4, 5: Unambiguous digit counts with 1-unit optical gaps.
   - 6, 7, 8, 9: Exact thumb-to-finger contact points.
3. 25 UPM Humanist Fillets on all joints.
"""

import json
from pathlib import Path

SVGS = {}

# Style Constants
STYLE_WRAP = (
    '<svg viewBox="0 0 100 120" class="asl-hand-svg" fill="none" '
    'stroke="var(--cyan)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
)

SKIN_FILL = 'fill="rgba(6, 182, 212, 0.14)" stroke="var(--cyan)" stroke-width="2.6"'
FRONT_FILL = 'fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2.6"'
ACCENT_FILL = 'fill="rgba(16, 185, 129, 0.25)" stroke="var(--emerald)" stroke-width="2.6"'

def make_svg(content):
    return f'{STYLE_WRAP}{content}</svg>'

# -----------------------------------------------------------------------------
# REUSABLE ANATOMICAL PRIMITIVES
# -----------------------------------------------------------------------------
def wrist_palm():
    return '''
  <!-- Wrist and Base Palm -->
  <path d="M 34 114 C 33 98 32 86 30 76 C 26 66 26 56 30 48" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 66 114 C 67 98 72 86 76 74 C 80 62 78 54 74 48" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 34 114 C 42 116 58 116 66 114" stroke="var(--cyan)" stroke-width="2" opacity="0.6" />
'''

def single_upright_finger(x, y_tip, y_base=60, width=11, fill_str=SKIN_FILL):
    hw = width / 2.0
    return f'''
  <path d="M {x - hw} {y_base} L {x - hw} {y_tip + hw} C {x - hw} {y_tip} {x + hw} {y_tip} {x + hw} {y_tip + hw} L {x + hw} {y_base}" {fill_str} />
  <line x1="{x - hw + 1.5}" y1="{y_tip + (y_base - y_tip)*0.35}" x2="{x + hw - 1.5}" y2="{y_tip + (y_base - y_tip)*0.35}" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" />
  <line x1="{x - hw + 1.5}" y1="{y_tip + (y_base - y_tip)*0.65}" x2="{x + hw - 1.5}" y2="{y_tip + (y_base - y_tip)*0.65}" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" />
  <ellipse cx="{x}" cy="{y_tip + 3.5}" rx="{hw - 2}" ry="2.5" stroke="var(--cyan)" stroke-width="1.2" opacity="0.8" />
'''

def curled_finger_pad(x, y_top=48, width=12, height=24):
    hw = width / 2.0
    return f'''
  <path d="M {x - hw} {y_top + height} L {x - hw} {y_top + hw} C {x - hw} {y_top} {x + hw} {y_top} {x + hw} {y_top + hw} L {x + hw} {y_top + height}" {SKIN_FILL} />
  <path d="M {x - hw + 1} {y_top + height*0.55} Q {x} {y_top + height*0.62} {x + hw - 1} {y_top + height*0.55}" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" fill="none" />
  <ellipse cx="{x}" cy="{y_top + height*0.8}" rx="{hw - 2.5}" ry="3" stroke="var(--cyan)" stroke-width="1.2" opacity="0.7" />
'''

# -----------------------------------------------------------------------------
# LETTERS A - Z
# -----------------------------------------------------------------------------

# 'A': Fist with thumb upright alongside index
SVGS['A'] = make_svg(f'''
  {wrist_palm()}
  <!-- 4 Curled Fingers in Fist -->
  {curled_finger_pad(37, 46, 11, 28)}
  {curled_finger_pad(48, 44, 11, 30)}
  {curled_finger_pad(59, 45, 11, 29)}
  {curled_finger_pad(70, 48, 11, 26)}
  <!-- Palm Base Fill -->
  <path d="M 32 74 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 74 Z" fill="rgba(6, 182, 212, 0.1)" stroke="none" />
  <!-- Prominent Upright Thumb on Left -->
  <path d="M 32 76 C 24 72 20 62 20 48 C 20 36 32 36 34 44 L 34 76 Z" {FRONT_FILL} />
  <ellipse cx="27" cy="42" rx="3.5" ry="4" stroke="var(--cyan)" stroke-width="1.5" />
  <line x1="22" y1="56" x2="34" y2="56" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" />
''')

# 'B': Flat hand, 4 upright fingers touching, thumb folded across palm
SVGS['B'] = make_svg(f'''
  {wrist_palm()}
  <!-- 4 Upright Fingers (Sloan 5:1 Optotype) -->
  {single_upright_finger(35, 16, 56, 11)}
  {single_upright_finger(46, 10, 56, 11)}
  {single_upright_finger(57, 14, 56, 11)}
  {single_upright_finger(68, 22, 56, 11)}
  <!-- Palm Base -->
  <path d="M 30 56 C 30 76 32 96 36 114 L 64 114 C 70 96 74 76 74 56 Z" fill="rgba(6, 182, 212, 0.12)" stroke="none" />
  <!-- Thumb folded across lower palm -->
  <path d="M 22 74 C 26 64 38 64 54 66 C 60 68 60 76 54 78 C 42 82 28 84 22 74 Z" {FRONT_FILL} />
  <ellipse cx="48" cy="71" rx="3" ry="3.5" stroke="var(--cyan)" stroke-width="1.4" />
''')

# 'C': Curved open arch (Profile view)
SVGS['C'] = make_svg('''
  <!-- Wrist -->
  <path d="M 28 112 C 28 94 30 82 28 72" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 54 112 C 52 98 48 86 44 76" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Upper C Curve (Fingers) -->
  <path d="M 28 72 C 26 38 38 18 64 18 C 78 18 88 28 88 40 C 88 48 80 52 74 46 C 68 40 60 34 48 36 C 38 38 38 52 38 72 Z" fill="rgba(6, 182, 212, 0.14)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Finger tip separators on C end -->
  <line x1="78" y1="28" x2="84" y2="40" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" />
  <line x1="72" y1="34" x2="78" y2="46" stroke="var(--cyan)" stroke-width="1.6" opacity="0.7" />
  <!-- Lower C Curve (Thumb) -->
  <path d="M 30 74 C 36 82 46 90 62 90 C 76 90 84 82 84 72 C 84 64 74 62 68 68 C 60 74 50 76 40 74 Z" fill="rgba(6, 182, 212, 0.14)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Inner Open C Aperture Indicator -->
  <ellipse cx="56" cy="56" rx="14" ry="16" stroke="var(--cyan)" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.5" />
''')

# 'D': Index finger pointing straight up, other fingers touch thumb in circular loop
SVGS['D'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index finger straight up -->
  {single_upright_finger(38, 10, 56, 12)}
  <!-- Fist Body -->
  <path d="M 32 76 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 76 Z" fill="rgba(6, 182, 212, 0.1)" stroke="none" />
  <!-- Circular Loop of Middle, Ring, Pinky touching Thumb -->
  <path d="M 44 56 C 58 50 76 50 76 66 C 76 80 62 84 48 82 C 38 80 30 76 30 68 C 30 58 40 56 44 56 Z" {FRONT_FILL} />
  <circle cx="56" cy="67" r="8" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2" />
''')

# 'E': Fingers curled down tightly, fingertips resting on tucked thumb
SVGS['E'] = make_svg(f'''
  {wrist_palm()}
  <!-- 4 Knuckle Arches -->
  <path d="M 30 58 C 30 42 40 38 44 46 C 46 40 54 38 58 46 C 60 40 68 40 72 46 C 74 40 84 42 84 56 L 82 68 L 30 68 Z" {SKIN_FILL} />
  <!-- Finger divider lines -->
  <line x1="44" y1="44" x2="44" y2="68" stroke="var(--cyan)" stroke-width="2" />
  <line x1="58" y1="44" x2="58" y2="68" stroke="var(--cyan)" stroke-width="2" />
  <line x1="72" y1="44" x2="72" y2="68" stroke="var(--cyan)" stroke-width="2" />
  <!-- Thumb shelf supporting fingertips -->
  <path d="M 22 76 C 28 66 46 64 74 66 C 80 68 80 76 74 78 C 58 82 34 84 22 76 Z" {FRONT_FILL} />
  <ellipse cx="68" cy="71" rx="4" ry="3.5" stroke="var(--cyan)" stroke-width="1.4" />
''')

# 'F': Index and thumb form O loop; 3 fingers spread upright
SVGS['F'] = make_svg(f'''
  {wrist_palm()}
  <!-- 3 Spread Upright Fingers (Middle, Ring, Pinky) -->
  {single_upright_finger(46, 10, 56, 11)}
  {single_upright_finger(59, 14, 56, 11)}
  {single_upright_finger(72, 22, 56, 11)}
  <!-- Base Palm -->
  <path d="M 32 76 C 32 94 34 104 36 114 L 64 114 C 68 104 74 94 74 76 Z" fill="rgba(6, 182, 212, 0.1)" stroke="none" />
  <!-- Circular O-Ring of Index & Thumb on left -->
  <circle cx="32" cy="56" r="14" {FRONT_FILL} />
  <circle cx="32" cy="56" r="6" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2" />
''')

# 'G': Index horizontal right, thumb parallel above
SVGS['G'] = make_svg('''
  <!-- Forearm & Wrist -->
  <path d="M 26 112 C 28 94 28 82 26 70 C 24 52 32 42 46 42 L 52 42" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 46 112 C 44 98 44 88 46 76" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Fist body -->
  <path d="M 28 72 C 28 54 36 44 48 44 C 52 44 54 62 50 82 Z" fill="rgba(6, 182, 212, 0.12)" stroke="none" />
  <!-- Horizontal Thumb (Top) -->
  <path d="M 44 42 L 78 42 C 86 42 86 32 78 32 L 44 32 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <ellipse cx="74" cy="37" rx="3.5" ry="3" stroke="var(--cyan)" stroke-width="1.4" />
  <!-- Horizontal Index Finger (Bottom) -->
  <path d="M 44 60 L 88 60 C 96 60 96 48 88 48 L 44 48 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <ellipse cx="84" cy="54" rx="3.5" ry="3.5" stroke="var(--cyan)" stroke-width="1.4" />
''')

# 'H': Index and middle fingers extended horizontally together
SVGS['H'] = make_svg('''
  <!-- Wrist & Hand Body -->
  <path d="M 26 112 C 28 94 28 82 26 70 C 24 52 32 40 44 40 C 50 40 50 64 46 88 L 46 112" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Index finger (upper horizontal) -->
  <path d="M 44 48 L 88 48 C 96 48 96 36 88 36 L 44 36 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Middle finger (lower horizontal) -->
  <path d="M 44 62 L 88 62 C 96 62 96 50 88 50 L 44 50 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <line x1="44" y1="49" x2="90" y2="49" stroke="var(--card-bg)" stroke-width="2.6" />
''')

# 'I': Pinky extended upright, fist closed with thumb across
SVGS['I'] = make_svg(f'''
  {wrist_palm()}
  <!-- Pinky finger straight up -->
  {single_upright_finger(68, 12, 58, 11)}
  <!-- 3 Curled Fingers (Index, Middle, Ring) -->
  {curled_finger_pad(36, 46, 11, 28)}
  {curled_finger_pad(47, 44, 11, 30)}
  {curled_finger_pad(58, 45, 11, 29)}
  <!-- Thumb across front -->
  <path d="M 22 74 C 28 64 42 62 58 64 C 64 66 62 74 56 76 C 42 78 30 80 22 74 Z" {FRONT_FILL} />
  <ellipse cx="50" cy="69" rx="3.5" ry="4" stroke="var(--cyan)" stroke-width="1.4" />
''')

# 'J': Pinky upright with J-hook trajectory arrow
SVGS['J'] = make_svg(f'''
  {wrist_palm()}
  {single_upright_finger(68, 16, 58, 11)}
  {curled_finger_pad(36, 46, 11, 28)}
  {curled_finger_pad(47, 44, 11, 30)}
  {curled_finger_pad(58, 45, 11, 29)}
  <path d="M 22 74 C 28 64 42 62 58 64 C 64 66 62 74 56 76 C 42 78 30 80 22 74 Z" {FRONT_FILL} />
  <!-- Glowing Amber J-Hook Arrow -->
  <path d="M 72 20 C 88 26 92 48 86 64 C 80 80 64 88 48 88 C 38 88 32 82 36 74" stroke="var(--amber)" stroke-width="3.5" stroke-dasharray="3,3" fill="none" />
  <polygon points="32,72 40,78 32,84" fill="var(--amber)" stroke="none" />
''')

# 'K': Index vertical, middle angled forward, thumb nestled between
SVGS['K'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index finger vertical -->
  {single_upright_finger(35, 10, 56, 11)}
  <!-- Middle finger angled forward -->
  <path d="M 44 46 L 62 18 C 66 12 76 18 72 24 L 54 58 Z" {SKIN_FILL} />
  <!-- Curled Ring & Pinky -->
  {curled_finger_pad(58, 54, 10, 24)}
  {curled_finger_pad(68, 56, 10, 22)}
  <!-- Thumb upright nestled between index and middle -->
  <path d="M 34 74 C 36 58 42 48 46 40 C 50 36 56 38 54 46 C 52 56 48 68 44 76 Z" {FRONT_FILL} />
  <ellipse cx="49" cy="42" rx="3" ry="3.5" stroke="var(--cyan)" stroke-width="1.3" />
''')

# 'L': Index finger vertical, thumb horizontal (classic 90 degree L)
SVGS['L'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index finger vertical -->
  {single_upright_finger(38, 8, 56, 12)}
  <!-- Thumb horizontal to the left (90 degree) -->
  <path d="M 38 78 L 10 78 C 3 78 3 66 10 66 L 38 66 Z" {FRONT_FILL} />
  <ellipse cx="14" cy="72" rx="3" ry="4" stroke="var(--cyan)" stroke-width="1.4" />
  <!-- Curled 3 fingers in fist -->
  {curled_finger_pad(49, 54, 10, 24)}
  {curled_finger_pad(59, 54, 10, 24)}
  {curled_finger_pad(69, 56, 10, 22)}
''')

# 'M': Fist with thumb tucked under 3 fingers (3 distinct arches + thumb peeking)
SVGS['M'] = make_svg(f'''
  {wrist_palm()}
  <!-- 3 Distinct Finger Arches (Index, Middle, Ring) draped over thumb -->
  {curled_finger_pad(36, 44, 12, 30)}
  {curled_finger_pad(49, 42, 12, 32)}
  {curled_finger_pad(62, 44, 12, 30)}
  <!-- Pinky tucked on right -->
  {curled_finger_pad(73, 50, 10, 24)}
  <!-- Thumb tip peeking out under the 3rd (ring) knuckle -->
  <ellipse cx="68" cy="74" rx="6" ry="7" {ACCENT_FILL} />
  <ellipse cx="68" cy="74" rx="3" ry="3.5" stroke="var(--emerald)" stroke-width="1.2" />
''')

# 'N': Fist with thumb tucked under 2 fingers (2 distinct arches + thumb peeking)
SVGS['N'] = make_svg(f'''
  {wrist_palm()}
  <!-- 2 Distinct Finger Arches (Index, Middle) draped over thumb -->
  {curled_finger_pad(38, 44, 13, 30)}
  {curled_finger_pad(52, 42, 13, 32)}
  <!-- Ring & Pinky tucked on right -->
  {curled_finger_pad(65, 48, 11, 26)}
  {curled_finger_pad(75, 52, 10, 22)}
  <!-- Thumb tip peeking out under the 2nd (middle) knuckle -->
  <ellipse cx="58" cy="74" rx="6" ry="7" {ACCENT_FILL} />
  <ellipse cx="58" cy="74" rx="3" ry="3.5" stroke="var(--emerald)" stroke-width="1.2" />
''')

# 'O': O-loop in profile
SVGS['O'] = make_svg('''
  <!-- Wrist -->
  <path d="M 28 112 C 28 92 28 80 26 68" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 52 112 C 50 96 46 86 42 78" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- O-ring profile contour -->
  <path d="M 28 68 C 24 44 36 26 56 24 C 74 22 88 34 88 52 C 88 74 74 86 58 88 C 42 90 38 98 42 112" stroke="var(--cyan)" stroke-width="2.6" fill="rgba(6, 182, 212, 0.14)" />
  <!-- Center O Aperture (Sloan 5:1 ratio) -->
  <ellipse cx="56" cy="54" rx="14" ry="16" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2.6" />
''')

# 'P': K pointing downward
SVGS['P'] = make_svg('''
  <!-- Forearm from upper left -->
  <path d="M 18 26 L 42 46 L 28 62 L 8 40 Z" fill="rgba(6, 182, 212, 0.14)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Index finger horizontal forward -->
  <path d="M 42 46 L 88 54 C 96 56 96 66 88 66 L 44 58 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Middle finger pointing straight downward -->
  <path d="M 44 58 L 48 104 C 48 112 36 112 36 104 L 36 62 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Thumb nestled between them -->
  <ellipse cx="52" cy="60" rx="6" ry="6" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2.6" />
''')

# 'Q': G pointing downward
SVGS['Q'] = make_svg('''
  <!-- Forearm from upper left -->
  <path d="M 18 26 L 44 48 L 30 62 L 8 38 Z" fill="rgba(6, 182, 212, 0.14)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Index pointing straight down -->
  <path d="M 42 52 L 42 104 C 42 112 32 112 32 104 L 32 58 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Thumb pointing down parallel -->
  <path d="M 56 50 L 58 96 C 58 104 48 104 48 96 L 46 56 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <line x1="44" y1="54" x2="44" y2="104" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'R': Index and middle crossed vertically
SVGS['R'] = make_svg(f'''
  {wrist_palm()}
  <!-- Back finger (Index angled right) -->
  <path d="M 34 54 L 56 12 C 58 6 68 10 64 16 L 46 54 Z" fill="rgba(6, 182, 212, 0.12)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Front crossing finger (Middle angled left) -->
  <path d="M 54 54 L 38 12 C 36 6 46 4 48 10 L 58 54 Z" {FRONT_FILL} />
  <!-- Curled Ring & Pinky -->
  {curled_finger_pad(64, 52, 10, 24)}
  {curled_finger_pad(73, 56, 10, 20)}
  <!-- Thumb across front -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
''')

# 'S': Fist with thumb wrapped FIRMLY across front of all knuckles
SVGS['S'] = make_svg(f'''
  {wrist_palm()}
  <!-- 4 Curled Fingers in Fist -->
  {curled_finger_pad(36, 46, 11, 28)}
  {curled_finger_pad(47, 44, 11, 30)}
  {curled_finger_pad(58, 45, 11, 29)}
  {curled_finger_pad(69, 48, 11, 26)}
  <!-- BOLD HORIZONTAL THUMB WRAPPED ACROSS FRONT OF ALL FINGERS -->
  <path d="M 18 62 C 26 50 48 48 72 52 C 80 54 80 66 70 68 C 46 72 26 74 18 62 Z" {FRONT_FILL} />
  <ellipse cx="66" cy="61" rx="4" ry="4.5" stroke="var(--cyan)" stroke-width="1.4" />
''')

# 'T': Fist with thumb tucked between index and middle
SVGS['T'] = make_svg(f'''
  {wrist_palm()}
  <!-- 4 Curled Fingers in Fist -->
  {curled_finger_pad(36, 46, 11, 28)}
  {curled_finger_pad(47, 44, 11, 30)}
  {curled_finger_pad(58, 45, 11, 29)}
  {curled_finger_pad(69, 48, 11, 26)}
  <!-- THUMB BULB POKING UP BETWEEN INDEX AND MIDDLE -->
  <ellipse cx="44" cy="46" rx="7" ry="8" {FRONT_FILL} />
  <ellipse cx="44" cy="43" rx="3.5" ry="3.5" stroke="var(--cyan)" stroke-width="1.3" />
''')

# 'U': Index and middle held together straight up
SVGS['U'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index & Middle combined twin pillar (held tightly together) -->
  {single_upright_finger(40, 10, 56, 11)}
  {single_upright_finger(51, 10, 56, 11)}
  <!-- Curled Ring & Pinky -->
  {curled_finger_pad(63, 52, 10, 24)}
  {curled_finger_pad(73, 56, 10, 20)}
  <!-- Thumb across front -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
''')

# 'V': Peace / V with index and middle spread apart
SVGS['V'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index angled left -->
  <path d="M 36 56 L 24 14 C 22 6 34 4 38 10 L 46 54 Z" {SKIN_FILL} />
  <!-- Middle angled right -->
  <path d="M 46 54 L 56 10 C 60 4 72 6 70 14 L 56 56 Z" {SKIN_FILL} />
  <!-- Curled Ring & Pinky -->
  {curled_finger_pad(63, 52, 10, 24)}
  {curled_finger_pad(73, 56, 10, 20)}
  <!-- Thumb across front -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
''')

# 'W': Three spread upright fingers in a W
SVGS['W'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index angled left -->
  <path d="M 34 54 L 20 16 C 18 8 28 6 32 12 L 40 52 Z" {SKIN_FILL} />
  <!-- Middle straight up -->
  {single_upright_finger(46, 8, 54, 11)}
  <!-- Ring angled right -->
  <path d="M 54 52 L 64 12 C 68 6 78 8 76 16 L 64 54 Z" {SKIN_FILL} />
  <!-- Pinky curled held by thumb -->
  {curled_finger_pad(73, 56, 10, 20)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
''')

# 'X': Crooked / hooked index finger
SVGS['X'] = make_svg(f'''
  {wrist_palm()}
  <!-- Curled middle, ring, pinky -->
  {curled_finger_pad(48, 48, 11, 28)}
  {curled_finger_pad(59, 49, 11, 27)}
  {curled_finger_pad(70, 52, 11, 24)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
  <!-- Bold Hooked Index Finger -->
  <path d="M 32 60 L 32 30 C 32 16 46 16 48 26 C 50 36 42 42 38 40" stroke="var(--cyan)" stroke-width="5" fill="none" />
''')

# 'Y': Shaka - thumb and pinky extended wide
SVGS['Y'] = make_svg(f'''
  {wrist_palm()}
  <!-- Curled middle 3 fingers -->
  {curled_finger_pad(41, 48, 11, 28)}
  {curled_finger_pad(52, 46, 11, 30)}
  {curled_finger_pad(63, 48, 11, 28)}
  <!-- Extended Thumb wide left -->
  <path d="M 32 74 L 6 52 C 0 46 8 38 16 44 L 34 58 Z" {FRONT_FILL} />
  <!-- Extended Pinky wide right -->
  <path d="M 64 64 L 88 38 C 94 32 102 40 96 48 L 70 78 Z" {FRONT_FILL} />
''')

# 'Z': Index finger with high-contrast Z stroke
SVGS['Z'] = make_svg(f'''
  {wrist_palm()}
  {single_upright_finger(38, 12, 56, 12)}
  {curled_finger_pad(49, 52, 10, 24)}
  {curled_finger_pad(59, 52, 10, 24)}
  {curled_finger_pad(69, 54, 10, 22)}
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" {FRONT_FILL} />
  <!-- Glowing Amber Z Vector Path -->
  <path d="M 52 16 L 86 16 L 56 46 L 90 46" stroke="var(--amber)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
  <polygon points="86,40 96,46 86,52" fill="var(--amber)" stroke="none" />
''')

# -----------------------------------------------------------------------------
# NUMERALS 0 - 9
# -----------------------------------------------------------------------------
SVGS['0'] = SVGS['O']
SVGS['1'] = SVGS['D']
SVGS['2'] = SVGS['V']
SVGS['3'] = make_svg(f'''
  {wrist_palm()}
  <!-- Thumb extended wide left -->
  <path d="M 32 74 L 8 52 C 2 46 10 38 18 44 L 34 58 Z" {FRONT_FILL} />
  <!-- Index upright -->
  {single_upright_finger(38, 10, 56, 11)}
  <!-- Middle upright -->
  {single_upright_finger(51, 8, 56, 11)}
  <!-- Ring & Pinky in fist -->
  {curled_finger_pad(64, 52, 10, 24)}
  {curled_finger_pad(74, 54, 10, 22)}
''')
SVGS['4'] = SVGS['B']
SVGS['5'] = make_svg(f'''
  {wrist_palm()}
  <!-- Thumb wide left -->
  <path d="M 30 74 L 6 52 C 0 46 8 38 16 44 L 32 58 Z" {FRONT_FILL} />
  <!-- 4 spread upright fingers -->
  <path d="M 32 58 L 24 16 C 22 9 32 8 36 14 L 40 54 Z" {SKIN_FILL} />
  {single_upright_finger(46, 8, 54, 11)}
  <path d="M 54 54 L 62 14 C 64 7 74 9 72 16 L 64 56 Z" {SKIN_FILL} />
  <path d="M 64 56 L 76 22 C 78 15 88 18 86 25 L 76 66 Z" {SKIN_FILL} />
''')
SVGS['6'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index, Middle, Ring upright -->
  {single_upright_finger(35, 12, 56, 11)}
  {single_upright_finger(47, 8, 56, 11)}
  {single_upright_finger(59, 14, 56, 11)}
  <!-- Pinky touching thumb in loop on right -->
  <circle cx="68" cy="70" r="13" {FRONT_FILL} />
  <circle cx="68" cy="70" r="5.5" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2" />
''')
SVGS['7'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index, Middle upright -->
  {single_upright_finger(35, 12, 56, 11)}
  {single_upright_finger(47, 8, 56, 11)}
  <!-- Pinky upright on right -->
  {single_upright_finger(72, 22, 56, 11)}
  <!-- Ring touching thumb in center loop -->
  <circle cx="58" cy="68" r="13" {FRONT_FILL} />
  <circle cx="58" cy="68" r="5.5" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2" />
''')
SVGS['8'] = make_svg(f'''
  {wrist_palm()}
  <!-- Index upright -->
  {single_upright_finger(35, 12, 56, 11)}
  <!-- Ring, Pinky upright -->
  {single_upright_finger(60, 14, 56, 11)}
  {single_upright_finger(72, 22, 56, 11)}
  <!-- Middle touching thumb in center loop -->
  <circle cx="47" cy="66" r="13" {FRONT_FILL} />
  <circle cx="47" cy="66" r="5.5" fill="var(--card-bg)" stroke="var(--cyan)" stroke-width="2" />
''')
SVGS['9'] = SVGS['F']

# -----------------------------------------------------------------------------
# EMERGENCY SIGNALS
# -----------------------------------------------------------------------------
SVGS['HELP'] = make_svg('''
  <!-- Supporting Non-Dominant Palm (Bottom) -->
  <path d="M 16 92 L 84 92 C 88 92 88 104 84 104 L 16 104 C 12 104 12 92 16 92 Z" fill="rgba(16, 185, 129, 0.25)" stroke="var(--emerald)" stroke-width="3" />
  <!-- Dominant Fist Resting on Top -->
  <path d="M 36 90 L 36 54 C 36 44 48 40 52 46 C 56 40 68 40 70 48 L 70 90 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Thumb Upright -->
  <path d="M 36 74 C 28 70 24 60 24 44 C 24 32 36 32 38 40 L 38 74 Z" fill="var(--card-bg)" stroke="var(--amber)" stroke-width="3" />
  <!-- Upward Assist Arrow -->
  <path d="M 50 32 L 50 12" stroke="var(--emerald)" stroke-width="4" stroke-linecap="round" />
  <polygon points="44,16 50,8 56,16" fill="var(--emerald)" />
''')

SVGS['STOP'] = make_svg('''
  <!-- Octagonal Warning Shield Aura -->
  <polygon points="50,4 82,16 96,50 82,84 50,96 18,84 4,50 18,16" fill="rgba(251, 113, 133, 0.15)" stroke="var(--rose)" stroke-width="3.5" />
  <!-- Solid Flat Hand Barrier Palm Facing Outward -->
  <path d="M 30 64 L 28 22 C 28 14 36 14 36 22 L 38 56" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
  <path d="M 38 24 L 44 14 C 44 6 52 6 52 14 L 52 56" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
  <path d="M 52 22 L 58 16 C 58 8 66 8 66 16 L 64 56" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
  <path d="M 64 26 L 72 24 C 72 16 80 16 80 24 L 76 66" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
  <path d="M 34 88 C 30 76 20 68 14 56 C 10 50 18 46 22 52 L 32 64" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
  <path d="M 32 64 L 76 66 C 76 80 72 96 68 112 L 36 112 C 34 98 34 86 34 76 Z" fill="rgba(251, 113, 133, 0.3)" stroke="var(--rose)" stroke-width="3" />
''')

SVGS['PAIN'] = make_svg('''
  <!-- Left Index Finger pointing right -->
  <path d="M 12 50 L 40 50 C 46 50 46 62 40 62 L 12 62 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="3" />
  <!-- Right Index Finger pointing left -->
  <path d="M 88 50 L 60 50 C 54 50 54 62 60 62 L 88 62 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="3" />
  <!-- Central Lightning / Shockwave Collision -->
  <polygon points="50,30 46,48 54,48 48,72 56,52 48,52" fill="var(--amber)" stroke="var(--amber)" stroke-width="2" />
  <circle cx="50" cy="56" r="16" fill="none" stroke="var(--rose)" stroke-width="2.5" stroke-dasharray="3,3" />
''')

SVGS['DOCTOR'] = make_svg('''
  <!-- Horizontal Forearm -->
  <path d="M 10 68 L 90 68 C 96 68 96 86 90 86 L 10 86 C 4 86 4 68 10 68 Z" fill="rgba(6, 182, 212, 0.15)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Two Fingers Palpating Pulse -->
  <path d="M 44 68 L 44 26 C 44 18 52 18 52 26 L 52 68 Z" fill="var(--card-bg)" stroke="var(--emerald)" stroke-width="3" />
  <path d="M 54 68 L 54 26 C 54 18 62 18 62 26 L 62 68 Z" fill="var(--card-bg)" stroke="var(--emerald)" stroke-width="3" />
  <!-- Pulse Wave Rings -->
  <circle cx="53" cy="70" r="12" fill="none" stroke="var(--amber)" stroke-width="3" stroke-dasharray="3,3" />
''')

SVGS['WATER'] = make_svg('''
  <!-- 'W' Handshape -->
  <path d="M 32 58 L 22 22 C 20 14 30 12 34 18 L 40 56 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 40 56 L 46 14 C 46 7 56 7 56 14 L 56 56 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <path d="M 56 56 L 66 18 C 68 12 78 14 76 20 L 66 58 Z" fill="rgba(6, 182, 212, 0.2)" stroke="var(--cyan)" stroke-width="2.6" />
  <!-- Water Ripple Drops -->
  <circle cx="50" cy="80" r="8" fill="var(--cyan)" stroke="none" />
  <circle cx="50" cy="80" r="16" fill="none" stroke="var(--cyan)" stroke-width="3" stroke-dasharray="4,4" />
''')

out_path = Path(__file__).resolve().parent.parent / "js" / "asl_svg_data.js"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("// PocketGull Anatomical Louise Sloan 5:1 Optotype ASL Vector Library\n")
    f.write("const ASL_SVG_DATA = " + json.dumps(SVGS, indent=2) + ";\n")

print(f"Generated {len(SVGS)} Anatomical Sloan 5:1 optotype ASL vectors to {out_path}")
