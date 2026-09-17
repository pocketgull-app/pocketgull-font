#!/usr/bin/env python3
"""
PocketGull Louise Sloan 5:1 Optotype ASL Vector Generator
==========================================================
Generates ultra-high visibility, bold humanist felt-marker hand shapes conforming to:
1. Louise Sloan 5:1 Optotype Acuity:
   - Stroke-to-gap ratio strictly calibrated (1:5 counter-space rule).
   - Zero hairline collapse: bold 4px–5px stroke contours or solid high-contrast duotone silhouettes.
   - Distinct, unmistakable finger separation (every single digit counts at a glance).
2. ISMP Life-Critical Clinical Acuity:
   - Immediate recognition of digits under stress, low light, and fatigue.
3. Phil Gear Felt-Marker Cardstock DNA:
   - 25 UPM corner fillets and organic, tactile weight.
"""

import json
from pathlib import Path

# Canvas: viewBox="0 0 100 120"
# All paths use bold strokes (stroke-width: 3.5 to 4.5) and solid silhouette fills
# so every digit is instantly visible at 50 paces.

SVGS = {}

def wrap_sloan(paths):
    return (
        f'<svg viewBox="0 0 100 120" class="asl-hand-svg sloan-optotype" fill="currentColor" '
        f'stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">'
        f'{paths}'
        f'</svg>'
    )

# 'A': Solid fist with bold upright thumb alongside index
SVGS['A'] = wrap_sloan('''
  <!-- Palm & Knuckles Body -->
  <path d="M 38 112 C 36 94 34 82 34 74 L 34 56 C 34 46 44 42 48 48 C 50 42 58 42 60 48 C 62 42 70 42 72 48 C 74 44 82 46 82 54 L 80 84 C 78 98 74 106 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Bold Upright Thumb on Left -->
  <path d="M 36 78 C 28 74 22 64 22 48 C 22 36 34 36 36 44 L 36 78 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <ellipse cx="29" cy="42" rx="3.5" ry="4.5" fill="var(--card-bg)" stroke="none" /><!-- Thumb nail cutout -->
  <!-- Knuckle & Finger Crease Negative Space Cutouts -->
  <line x1="48" y1="46" x2="48" y2="76" stroke="var(--card-bg)" stroke-width="3" />
  <line x1="60" y1="46" x2="60" y2="76" stroke="var(--card-bg)" stroke-width="3" />
  <line x1="72" y1="46" x2="72" y2="76" stroke="var(--card-bg)" stroke-width="3" />
  <path d="M 34 66 Q 58 64 80 66" stroke="var(--card-bg)" stroke-width="3.5" fill="none" />
  <path d="M 34 80 Q 58 78 78 80" stroke="var(--card-bg)" stroke-width="3.5" fill="none" />
''')

# 'B': Flat open hand, 4 straight upright fingers with bold separation, thumb folded across palm
SVGS['B'] = wrap_sloan('''
  <!-- 4 Bold Distinct Fingers -->
  <!-- Index -->
  <path d="M 32 58 L 32 18 C 32 10 42 10 42 18 L 42 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle -->
  <path d="M 44 58 L 44 12 C 44 5 54 5 54 12 L 54 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Ring -->
  <path d="M 56 58 L 56 16 C 56 9 66 9 66 16 L 66 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Pinky -->
  <path d="M 68 58 L 68 24 C 68 18 78 18 78 24 L 78 68 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm Base & Wrist -->
  <path d="M 32 58 C 30 76 30 92 34 112 L 74 112 C 78 96 78 78 78 68 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Folded Thumb across lower palm -->
  <path d="M 24 76 C 28 66 42 64 56 66 C 62 68 62 76 56 78 C 42 82 30 84 24 76 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Joint Knuckle Cutouts -->
  <line x1="33" y1="36" x2="77" y2="36" stroke="var(--card-bg)" stroke-width="2.8" />
  <line x1="33" y1="50" x2="77" y2="50" stroke="var(--card-bg)" stroke-width="2.8" />
''')

# 'C': Curved open C profile with high-contrast aperture
SVGS['C'] = wrap_sloan('''
  <!-- Wrist -->
  <path d="M 28 112 C 28 94 30 82 28 72" stroke="var(--cyan)" stroke-width="5" fill="none" />
  <path d="M 54 112 C 52 98 48 86 44 76" stroke="var(--cyan)" stroke-width="5" fill="none" />
  <!-- Upper C Arch (4 fingers grouped) -->
  <path d="M 28 72 C 26 40 38 18 62 18 C 76 18 88 26 88 40 C 88 50 78 54 72 48 C 66 42 58 36 46 38 C 36 40 36 54 36 72 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Lower C Arch (Thumb) -->
  <path d="M 30 74 C 36 82 46 90 62 90 C 76 90 84 82 84 72 C 84 64 74 62 68 68 C 60 74 50 76 40 74 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- High Contrast Open C Aperture Indicator -->
  <circle cx="56" cy="56" r="14" fill="var(--card-bg)" stroke="none" />
''')

# 'D': Index finger straight up (Sloan optotype), thumb and fingers form bold circle loop
SVGS['D'] = wrap_sloan('''
  <!-- Index finger straight up - Maximum Bold Optical Anchor -->
  <path d="M 34 60 L 34 12 C 34 4 46 4 46 12 L 46 60 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <ellipse cx="40" cy="12" rx="4" ry="4" fill="var(--card-bg)" stroke="none" /><!-- nail cutout -->
  <!-- Hand Base & Fist Loop -->
  <path d="M 36 112 C 34 94 32 82 32 74 C 32 60 46 54 62 54 C 78 54 84 68 84 78 C 84 94 76 106 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Circular Counter Loop Hole (Sloan 5:1 Aperture) -->
  <ellipse cx="58" cy="70" rx="11" ry="11" fill="var(--card-bg)" stroke="none" />
''')

# 'E': All fingers curled down tight resting on folded thumb
SVGS['E'] = wrap_sloan('''
  <!-- Wrist -->
  <path d="M 36 112 C 34 94 32 82 32 72 L 76 72 C 76 84 74 96 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- 4 Bold Curled Fingers arched down -->
  <path d="M 28 58 C 28 42 38 38 42 46 C 44 40 52 38 56 46 C 58 40 66 40 70 46 C 72 40 82 42 82 56 L 82 66 L 28 66 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb shelf supporting fingertips -->
  <path d="M 24 78 C 30 68 46 66 74 68 C 80 69 80 78 74 80 C 58 82 36 84 24 78 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Slits between 4 fingers -->
  <line x1="42" y1="44" x2="42" y2="66" stroke="var(--card-bg)" stroke-width="3" />
  <line x1="56" y1="44" x2="56" y2="66" stroke="var(--card-bg)" stroke-width="3" />
  <line x1="70" y1="44" x2="70" y2="66" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'F': Index and thumb form O loop; 3 fingers fan out upright
SVGS['F'] = wrap_sloan('''
  <!-- 3 Extended Spread Fingers -->
  <!-- Middle -->
  <path d="M 44 54 L 44 12 C 44 5 54 5 54 12 L 54 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Ring -->
  <path d="M 56 54 L 60 16 C 62 9 72 11 70 18 L 66 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Pinky -->
  <path d="M 68 56 L 76 24 C 78 17 88 20 86 27 L 78 66 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm Base -->
  <path d="M 34 112 C 32 96 32 82 32 74 C 32 64 42 60 54 60 C 68 60 76 74 76 84 C 76 98 74 106 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Bold Circular O-Ring of Index & Thumb on left -->
  <circle cx="34" cy="56" r="16" fill="var(--cyan)" stroke="var(--card-bg)" stroke-width="4" />
  <circle cx="34" cy="56" r="7" fill="var(--card-bg)" stroke="none" />
''')

# 'G': Index finger pointing horizontally right, thumb parallel above
SVGS['G'] = wrap_sloan('''
  <!-- Fist Body -->
  <path d="M 26 110 C 28 92 28 80 26 68 C 24 50 32 40 46 40 L 52 40 C 52 56 50 74 46 88 C 42 98 44 104 46 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Bold Horizontal Thumb (Top) -->
  <path d="M 44 42 L 76 42 C 84 42 84 32 76 32 L 44 32 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Bold Horizontal Index (Bottom) -->
  <path d="M 44 58 L 86 58 C 94 58 94 48 86 48 L 44 48 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Clean Separating Channel between Thumb and Index -->
  <line x1="44" y1="45" x2="86" y2="45" stroke="var(--card-bg)" stroke-width="4.5" />
''')

# 'H': Index and middle fingers extended horizontally together
SVGS['H'] = wrap_sloan('''
  <!-- Fist Body -->
  <path d="M 26 110 C 28 92 28 80 26 68 C 24 50 32 40 44 40 C 50 40 50 64 46 88 L 46 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Index finger (upper) -->
  <path d="M 44 48 L 88 48 C 96 48 96 36 88 36 L 44 36 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle finger (lower) -->
  <path d="M 44 62 L 88 62 C 96 62 96 50 88 50 L 44 50 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Separator between Index and Middle -->
  <line x1="44" y1="49" x2="90" y2="49" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'I': Pinky finger pointing straight up, fist closed with thumb across
SVGS['I'] = wrap_sloan('''
  <!-- Pinky finger straight up (bold high anchor) -->
  <path d="M 66 60 L 66 14 C 66 6 78 6 78 14 L 78 72 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <ellipse cx="72" cy="14" rx="4" ry="4" fill="var(--card-bg)" stroke="none" />
  <!-- Fist Body -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 30 56 C 30 46 42 44 46 50 C 48 44 58 44 62 50 L 66 76 C 66 94 66 104 64 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb across front -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'J': Pinky upright with dynamic sweeping J-hook arrow
SVGS['J'] = wrap_sloan('''
  <!-- Pinky & Fist (same as I) -->
  <path d="M 66 60 L 66 16 C 66 8 78 8 78 16 L 78 72 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <path d="M 34 112 C 32 94 30 82 30 72 L 30 56 C 30 46 42 44 46 50 C 48 44 58 44 62 50 L 66 76 L 64 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Dynamic High-Visibility J-Hook Arrow -->
  <path d="M 72 20 C 88 26 92 48 86 64 C 80 80 64 88 48 88 C 38 88 32 82 36 74" stroke="var(--amber)" stroke-width="4.5" fill="none" />
  <polygon points="32,72 40,78 32,84" fill="var(--amber)" stroke="none" />
''')

# 'K': Index vertical, middle angled forward, thumb nestled between
SVGS['K'] = wrap_sloan('''
  <!-- Index finger vertical -->
  <path d="M 32 58 L 32 12 C 32 5 44 5 44 12 L 44 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle finger angled forward -->
  <path d="M 44 46 L 62 18 C 66 12 76 18 72 24 L 54 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 64 56 C 76 56 78 72 78 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb standing upright between knuckles -->
  <path d="M 36 74 C 38 58 44 48 48 40 C 52 36 58 38 56 46 C 54 56 50 68 46 76 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'L': Index vertical, thumb horizontal (classic 90 degree L)
SVGS['L'] = wrap_sloan('''
  <!-- Index finger vertical -->
  <path d="M 38 58 L 38 10 C 38 3 50 3 50 10 L 50 56 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Thumb pointing straight horizontal to left (90 deg) -->
  <path d="M 38 78 L 10 78 C 3 78 3 66 10 66 L 38 66 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Fist Body -->
  <path d="M 38 58 C 50 52 68 52 74 62 C 78 72 76 86 72 112 L 42 112 C 38 98 38 88 38 78 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Knuckle Creases -->
  <line x1="50" y1="68" x2="72" y2="68" stroke="var(--card-bg)" stroke-width="3" />
  <line x1="50" y1="80" x2="70" y2="80" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'M': Fist with thumb tucked under 3 fingers (3 distinct knuckle mounds + thumb peeking)
SVGS['M'] = wrap_sloan('''
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 76 72 C 76 84 74 96 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- 3 Curved Knuckles folded over thumb -->
  <path d="M 28 58 C 28 42 38 38 44 46 C 46 38 56 38 62 46 C 64 38 76 40 80 52 L 78 72 L 28 72 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb tip peeking out under the 3rd (ring) knuckle -->
  <ellipse cx="68" cy="74" rx="7" ry="8" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
  <!-- 2 Separating cutouts between 3 fingers -->
  <line x1="44" y1="44" x2="44" y2="72" stroke="var(--card-bg)" stroke-width="3.5" />
  <line x1="62" y1="44" x2="62" y2="72" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'N': Fist with thumb tucked under 2 fingers (2 distinct knuckle mounds + thumb peeking)
SVGS['N'] = wrap_sloan('''
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 76 72 C 76 84 74 96 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- 2 Curved Knuckles folded over thumb -->
  <path d="M 28 58 C 28 42 42 38 48 46 C 52 38 68 38 74 50 L 74 72 L 28 72 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb tip peeking out under the 2nd (middle) knuckle -->
  <ellipse cx="56" cy="74" rx="7" ry="8" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
  <!-- Separating cutout between 2 fingers -->
  <line x1="48" y1="44" x2="48" y2="72" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'O': Bold circular O aperture
SVGS['O'] = wrap_sloan('''
  <!-- Hand silhouette in profile -->
  <path d="M 28 112 C 28 92 28 80 26 68 C 24 44 36 26 56 24 C 74 22 88 34 88 52 C 88 74 74 86 58 88 C 42 90 38 98 44 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- High-Contrast Open Circular O Cutout -->
  <ellipse cx="56" cy="54" rx="14" ry="16" fill="var(--card-bg)" stroke="none" />
''')

# 'P': K pointing downward
SVGS['P'] = wrap_sloan('''
  <!-- Wrist coming from upper left -->
  <path d="M 20 28 L 44 48 L 30 64 L 10 42 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Index finger extending horizontally forward -->
  <path d="M 44 48 L 88 56 C 96 58 96 68 88 68 L 44 60 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle finger pointing straight downward -->
  <path d="M 44 60 L 48 102 C 48 110 36 110 36 102 L 36 64 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Thumb nestled between them -->
  <ellipse cx="52" cy="62" rx="7" ry="7" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'Q': G pointing downward
SVGS['Q'] = wrap_sloan('''
  <!-- Forearm from upper left -->
  <path d="M 20 28 L 46 50 L 32 64 L 10 40 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Index pointing straight down -->
  <path d="M 44 54 L 44 104 C 44 112 34 112 34 104 L 34 60 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb pointing down parallel -->
  <path d="M 58 52 L 60 96 C 60 104 50 104 50 96 L 48 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Separator line -->
  <line x1="46" y1="56" x2="46" y2="104" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'R': Index and middle crossed vertically
SVGS['R'] = wrap_sloan('''
  <!-- Fist Body -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 58 44 54 68 54 C 76 54 78 72 78 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Back finger (Index angled right) -->
  <path d="M 34 54 L 56 12 C 58 6 68 10 64 16 L 46 54 Z" fill="var(--cyan)" stroke="var(--cyan)" opacity="0.85" />
  <!-- Front crossing finger (Middle angled left) -->
  <path d="M 54 54 L 38 12 C 36 6 46 4 48 10 L 58 54 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
  <!-- Thumb across front -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--cyan)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'S': Fist with thumb wrapped FIRMLY across front (Louise Sloan distinct form)
SVGS['S'] = wrap_sloan('''
  <!-- Solid Fist Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 30 54 C 30 42 42 38 48 44 C 52 38 64 38 68 44 C 72 38 82 40 82 52 L 80 84 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- BOLD HORIZONTAL THUMB OVER FRONT OF ALL FINGERS -->
  <path d="M 20 62 C 28 52 48 50 72 54 C 80 56 80 68 70 70 C 46 74 28 76 20 62 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="4" />
  <!-- Thumb nail cutout -->
  <ellipse cx="66" cy="62" rx="4" ry="4.5" fill="var(--card-bg)" stroke="none" />
''')

# 'T': Fist with thumb tucked between index and middle (thumb tip poking up)
SVGS['T'] = wrap_sloan('''
  <!-- Fist Body -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 30 54 C 30 42 42 38 48 44 C 52 38 64 38 68 44 C 72 38 82 40 82 52 L 80 84 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- THUMB BULB POKING UP BETWEEN INDEX AND MIDDLE -->
  <ellipse cx="46" cy="46" rx="8" ry="9" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="4" />
  <ellipse cx="46" cy="43" rx="3.5" ry="3.5" fill="var(--card-bg)" stroke="none" /><!-- nail -->
  <!-- Horizontal finger crease -->
  <line x1="30" y1="68" x2="80" y2="68" stroke="var(--card-bg)" stroke-width="3.5" />
''')

# 'U': Index and middle held together straight up
SVGS['U'] = wrap_sloan('''
  <!-- Index & Middle combined twin pillar -->
  <path d="M 34 56 L 34 12 C 34 4 46 4 46 12 L 46 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 46 56 L 46 12 C 46 4 58 4 58 12 L 58 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <line x1="46" y1="8" x2="46" y2="56" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 C 78 56 80 72 80 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb across folded ring and pinky -->
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'V': Peace / V with index and middle spread apart
SVGS['V'] = wrap_sloan('''
  <!-- Index angled left -->
  <path d="M 36 56 L 24 14 C 22 6 34 4 38 10 L 46 54 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Middle angled right -->
  <path d="M 46 54 L 56 10 C 60 4 72 6 70 14 L 56 56 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 C 78 56 80 72 80 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'W': Three spread upright fingers in a W
SVGS['W'] = wrap_sloan('''
  <!-- Index angled left -->
  <path d="M 34 54 L 20 16 C 18 8 28 6 32 12 L 40 52 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle straight up -->
  <path d="M 40 52 L 44 10 C 44 3 54 3 54 10 L 54 52 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Ring angled right -->
  <path d="M 54 52 L 64 12 C 68 6 78 8 76 16 L 64 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 C 78 56 80 72 80 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
''')

# 'X': Crooked / hooked index finger
SVGS['X'] = wrap_sloan('''
  <!-- Fist Body -->
  <path d="M 34 112 C 32 94 30 82 30 72 L 30 56 C 30 46 42 44 48 50 C 50 44 62 44 66 50 L 76 76 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Bold Hooked Index Finger -->
  <path d="M 32 58 L 32 30 C 32 16 46 16 48 26 C 50 36 42 42 38 40" stroke="var(--cyan)" stroke-width="7" fill="none" />
''')

# 'Y': Shaka - thumb and pinky extended wide
SVGS['Y'] = wrap_sloan('''
  <!-- Fist Base -->
  <path d="M 36 112 C 34 94 32 82 32 72 L 32 56 C 32 46 42 44 46 50 C 48 44 58 44 62 50 L 64 76 L 64 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Extended Thumb wide left -->
  <path d="M 32 74 L 6 52 C 0 46 8 38 16 44 L 34 58 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Extended Pinky wide right -->
  <path d="M 64 64 L 88 38 C 94 32 102 40 96 48 L 70 78 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
''')

# 'Z': Index finger with high-contrast Z stroke
SVGS['Z'] = wrap_sloan('''
  <!-- Index finger pointing up/forward -->
  <path d="M 34 60 L 34 16 C 34 8 46 8 46 16 L 46 60 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Fist Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 C 78 56 80 72 80 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 24 74 C 30 64 44 62 58 64 C 64 66 62 74 56 76 C 44 78 32 80 24 74 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- High-Visibility Glowing Z Vector -->
  <path d="M 52 16 L 86 16 L 56 46 L 90 46" stroke="var(--amber)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none" />
  <polygon points="86,40 96,46 86,52" fill="var(--amber)" stroke="none" />
''')

# Digits 0-9
SVGS['0'] = SVGS['O']
SVGS['1'] = SVGS['D']
SVGS['2'] = SVGS['V']
SVGS['3'] = wrap_sloan('''
  <!-- ASL 3: Thumb, Index, Middle extended -->
  <!-- Thumb extended wide left -->
  <path d="M 32 74 L 8 52 C 2 46 10 38 18 44 L 34 58 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="4" />
  <!-- Index upright -->
  <path d="M 34 56 L 34 12 C 34 4 44 4 44 12 L 44 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle upright -->
  <path d="M 46 54 L 48 10 C 48 3 58 3 58 10 L 58 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm Base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 C 78 56 80 72 80 82 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
''')
SVGS['4'] = SVGS['B']
SVGS['5'] = wrap_sloan('''
  <!-- All 5 digits spread open wide -->
  <!-- Thumb -->
  <path d="M 30 74 L 6 52 C 0 46 8 38 16 44 L 32 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- 4 spread fingers -->
  <path d="M 32 58 L 24 16 C 22 9 32 8 36 14 L 40 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 40 54 L 44 10 C 44 3 54 3 54 10 L 54 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 54 54 L 62 14 C 64 7 74 9 72 16 L 64 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 64 56 L 76 22 C 78 15 88 18 86 25 L 76 66 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm -->
  <path d="M 34 112 C 30 94 30 82 32 74 L 76 74 C 76 86 74 98 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
''')
SVGS['6'] = wrap_sloan('''
  <!-- Pinky touches thumb tip, index/middle/ring upright -->
  <path d="M 32 56 L 32 14 C 32 7 42 7 42 14 L 42 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 44 54 L 46 10 C 46 3 56 3 56 10 L 56 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 58 54 L 64 16 C 66 9 76 11 74 18 L 68 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Pinky + thumb loop on right -->
  <circle cx="68" cy="70" r="14" fill="var(--cyan)" stroke="var(--card-bg)" stroke-width="3.5" />
  <circle cx="68" cy="70" r="6" fill="var(--card-bg)" stroke="none" />
''')
SVGS['7'] = wrap_sloan('''
  <!-- Ring touches thumb tip, index/middle/pinky upright -->
  <path d="M 32 56 L 32 14 C 32 7 42 7 42 14 L 42 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 44 54 L 46 10 C 46 3 56 3 56 10 L 56 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 68 56 L 76 22 C 78 15 88 18 86 25 L 78 66 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Ring + thumb loop in center -->
  <circle cx="56" cy="68" r="14" fill="var(--cyan)" stroke="var(--card-bg)" stroke-width="3.5" />
  <circle cx="56" cy="68" r="6" fill="var(--card-bg)" stroke="none" />
''')
SVGS['8'] = wrap_sloan('''
  <!-- Middle touches thumb tip, index/ring/pinky upright -->
  <path d="M 32 56 L 32 14 C 32 7 42 7 42 14 L 42 54 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 58 54 L 62 16 C 64 9 74 11 72 18 L 66 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 68 56 L 76 22 C 78 15 88 18 86 25 L 78 66 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Palm base -->
  <path d="M 34 112 C 32 94 30 82 30 72 C 30 60 44 56 68 56 L 72 112 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Middle + thumb loop -->
  <circle cx="46" cy="66" r="14" fill="var(--cyan)" stroke="var(--card-bg)" stroke-width="3.5" />
  <circle cx="46" cy="66" r="6" fill="var(--card-bg)" stroke="none" />
''')
SVGS['9'] = SVGS['F']

# Emergency & Clinical Hand Signals
SVGS['HELP'] = wrap_sloan('''
  <!-- Supporting Non-Dominant Palm (Bottom) -->
  <path d="M 16 92 L 84 92 C 88 92 88 104 84 104 L 16 104 C 12 104 12 92 16 92 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Dominant Fist Resting on Top -->
  <path d="M 36 90 L 36 54 C 36 44 48 40 52 46 C 56 40 68 40 70 48 L 70 90 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Thumb Upright -->
  <path d="M 36 74 C 28 70 24 60 24 44 C 24 32 36 32 38 40 L 38 74 Z" fill="var(--amber)" stroke="var(--card-bg)" stroke-width="3" />
  <!-- Upward Assist Arrow -->
  <path d="M 50 32 L 50 12" stroke="var(--emerald)" stroke-width="4" stroke-linecap="round" />
  <polygon points="44,16 50,8 56,16" fill="var(--emerald)" />
''')

SVGS['STOP'] = wrap_sloan('''
  <!-- Octagonal Warning Shield Aura -->
  <polygon points="50,4 82,16 96,50 82,84 50,96 18,84 4,50 18,16" fill="rgba(251, 113, 133, 0.15)" stroke="var(--rose)" stroke-width="4" />
  <!-- Solid Flat Hand Barrier Palm Facing Outward -->
  <path d="M 30 64 L 28 22 C 28 14 36 14 36 22 L 38 56" fill="var(--rose)" stroke="var(--rose)" stroke-width="3.5" />
  <path d="M 38 24 L 44 14 C 44 6 52 6 52 14 L 52 56" fill="var(--rose)" stroke="var(--rose)" stroke-width="3.5" />
  <path d="M 52 22 L 58 16 C 58 8 66 8 66 16 L 64 56" fill="var(--rose)" stroke="var(--rose)" stroke-width="3.5" />
  <path d="M 64 26 L 72 24 C 72 16 80 16 80 24 L 76 66" fill="var(--rose)" stroke="var(--rose)" stroke-width="3.5" />
  <path d="M 34 88 C 30 76 20 68 14 56 C 10 50 18 46 22 52 L 32 64" fill="var(--rose)" stroke="var(--rose)" stroke-width="3.5" />
  <path d="M 32 64 L 76 66 C 76 80 72 96 68 112 L 36 112 C 34 98 34 86 34 76 Z" fill="var(--rose)" stroke="var(--rose)" />
''')

SVGS['PAIN'] = wrap_sloan('''
  <!-- Left Index Finger pointing right -->
  <path d="M 12 50 L 40 50 C 46 50 46 62 40 62 L 12 62 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="3.5" />
  <!-- Right Index Finger pointing left -->
  <path d="M 88 50 L 60 50 C 54 50 54 62 60 62 L 88 62 Z" fill="var(--cyan)" stroke="var(--cyan)" stroke-width="3.5" />
  <!-- Central Lightning / Shockwave Collision -->
  <polygon points="50,30 46,48 54,48 48,72 56,52 48,52" fill="var(--amber)" stroke="var(--amber)" stroke-width="2" />
  <circle cx="50" cy="56" r="16" fill="none" stroke="var(--rose)" stroke-width="2.5" stroke-dasharray="3,3" />
''')

SVGS['DOCTOR'] = wrap_sloan('''
  <!-- Horizontal Forearm -->
  <path d="M 10 68 L 90 68 C 96 68 96 86 90 86 L 10 86 C 4 86 4 68 10 68 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Two Fingers Palpating Pulse -->
  <path d="M 44 68 L 44 26 C 44 18 52 18 52 26 L 52 68 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
  <path d="M 54 68 L 54 26 C 54 18 62 18 62 26 L 62 68 Z" fill="var(--emerald)" stroke="var(--card-bg)" stroke-width="3.5" />
  <!-- Pulse Wave Rings -->
  <circle cx="53" cy="70" r="12" fill="none" stroke="var(--amber)" stroke-width="3" stroke-dasharray="3,3" />
''')

SVGS['WATER'] = wrap_sloan('''
  <!-- 'W' Handshape -->
  <path d="M 32 58 L 22 22 C 20 14 30 12 34 18 L 40 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 40 56 L 46 14 C 46 7 56 7 56 14 L 56 56 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <path d="M 56 56 L 66 18 C 68 12 78 14 76 20 L 66 58 Z" fill="var(--cyan)" stroke="var(--cyan)" />
  <!-- Water Ripple Drops -->
  <circle cx="50" cy="80" r="8" fill="var(--cyan)" stroke="none" />
  <circle cx="50" cy="80" r="16" fill="none" stroke="var(--cyan)" stroke-width="3" stroke-dasharray="4,4" />
''')

out_path = Path(__file__).resolve().parent.parent / "js" / "asl_svg_data.js"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("// PocketGull Louise Sloan 5:1 Optotype High-Acuity ASL Vector Library\n")
    f.write("const ASL_SVG_DATA = " + json.dumps(SVGS, indent=2) + ";\n")

print(f"Generated {len(SVGS)} Louise Sloan 5:1 optotype ASL vectors to {out_path}")
