#!/usr/bin/env python3
"""
Generate High-Fidelity Anatomical ASL Vector SVGs for PocketGull Sign Studio
=============================================================================
Creates realistic, beautiful line-art vector hand illustrations with:
- Natural wrist and palm contours
- Anatomically accurate finger knuckles, folds, and creases
- Clear thumb opposition, tucks, and overlaps
- Theme-adaptive currentColor vector paths
"""

import json
from pathlib import Path

SVGS = {}

# Common SVG wrapper: viewBox="0 0 100 120"
# Style: stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"
# Base wrist & palm fill: fill="rgba(6, 182, 212, 0.08)"

def wrap_svg(inner_paths):
    return (
        f'<svg viewBox="0 0 100 120" class="asl-hand-svg" fill="none" '
        f'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M 36 112 C 35 98 33 88 30 78 C 26 68 25 58 28 50 C 31 42 38 42 42 48 C 45 42 52 40 56 44 C 60 40 68 40 71 46 C 75 42 81 44 82 52 C 84 66 80 82 72 96 C 68 104 65 108 64 112 Z" '
        f'fill="rgba(6, 182, 212, 0.06)" stroke="none"/>'
        f'{inner_paths}'
        f'</svg>'
    )

# 'A': Fist with thumb upright alongside index
SVGS['A'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Fist Knuckle Arches (Index, Middle, Ring, Pinky) -->
  <path d="M 38 52 C 38 44 46 44 48 48 C 48 42 56 42 58 46 C 58 40 66 40 68 46 C 68 42 76 44 76 52 C 76 68 74 78 72 86 C 70 94 66 104 64 112" />
  <!-- Curled fingers horizontal crease lines -->
  <path d="M 38 66 C 48 64 66 64 74 68" stroke-width="1.8" opacity="0.7" />
  <path d="M 38 78 C 48 76 64 76 72 80" stroke-width="1.8" opacity="0.7" />
  <!-- Vertical finger dividers -->
  <path d="M 48 48 L 48 74" stroke-width="1.6" opacity="0.6" />
  <path d="M 58 46 L 58 74" stroke-width="1.6" opacity="0.6" />
  <path d="M 68 46 L 68 74" stroke-width="1.6" opacity="0.6" />
  <!-- Thumb upright on the left -->
  <path d="M 30 76 C 24 70 22 56 24 46 C 26 38 34 38 36 44 C 38 50 38 64 38 74" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 26 44 C 28 42 32 42 34 44" stroke-width="1.5" opacity="0.8" /><!-- thumb nail -->
''')

# 'B': Open flat hand, 4 fingers straight up, thumb across palm
SVGS['B'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 28 74" />
  <path d="M 64 112 C 66 98 72 86 74 72" />
  <!-- 4 upright fingers touching -->
  <!-- Index -->
  <path d="M 32 60 L 32 20 C 32 14 40 14 40 20 L 40 56" />
  <!-- Middle -->
  <path d="M 40 22 L 40 14 C 40 8 48 8 48 14 L 48 56" />
  <!-- Ring -->
  <path d="M 48 20 L 48 16 C 48 10 56 10 56 16 L 56 58" />
  <!-- Pinky -->
  <path d="M 56 24 L 56 22 C 56 16 64 16 64 22 L 64 64" />
  <path d="M 64 64 C 70 70 74 74 74 84" />
  <!-- Finger joint horizontal creases -->
  <path d="M 33 34 L 63 34" stroke-width="1.6" opacity="0.6" />
  <path d="M 33 46 L 63 46" stroke-width="1.6" opacity="0.6" />
  <!-- Thumb folded across lower palm -->
  <path d="M 28 74 C 32 68 40 66 52 68 C 56 69 56 76 50 78 C 42 80 34 82 30 86" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 46 70 C 48 71 50 73 48 75" stroke-width="1.4" opacity="0.8" /><!-- thumb nail -->
''')

# 'C': Curved open arch in profile
SVGS['C'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 26 108 C 28 92 28 82 26 72" />
  <path d="M 52 112 C 50 98 46 88 44 80" />
  <!-- Upper C arc (fingers grouped together arching over) -->
  <path d="M 26 72 C 26 44 34 26 52 24 C 66 22 78 28 82 40 C 84 46 78 52 72 50 C 66 48 64 42 56 38 C 46 36 38 46 38 60" />
  <!-- Finger tip separators on C end -->
  <path d="M 76 34 L 80 44" stroke-width="1.6" opacity="0.6" />
  <path d="M 72 38 L 76 48" stroke-width="1.6" opacity="0.6" />
  <!-- Lower C arc (thumb arching forward and up) -->
  <path d="M 30 76 C 34 82 42 86 54 86 C 66 86 76 80 78 72 C 79 66 74 62 68 64 C 60 66 54 72 46 74 C 40 76 36 74 32 72" />
''')

# 'D': Index finger pointing straight up; middle, ring, pinky touch thumb in a loop
SVGS['D'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 30 74" />
  <path d="M 64 112 C 66 98 70 88 72 76" />
  <!-- Index finger straight up -->
  <path d="M 34 60 L 34 18 C 34 10 44 10 44 18 L 44 56" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 35 30 L 43 30" stroke-width="1.6" opacity="0.6" />
  <path d="M 35 44 L 43 44" stroke-width="1.6" opacity="0.6" />
  <!-- Curled loop: middle, ring, pinky touching thumb tip -->
  <path d="M 44 56 C 54 52 66 52 70 60 C 74 68 72 78 66 82 C 58 86 48 84 42 80" />
  <!-- Thumb arching up to meet curled fingers -->
  <path d="M 30 74 C 32 64 42 60 54 62 C 60 64 62 70 56 74 C 48 76 40 76 36 78" />
  <!-- Loop center hole -->
  <circle cx="52" cy="68" r="7" stroke-width="1.8" opacity="0.8" />
''')

# 'E': All fingers curled tight down resting on thumb
SVGS['E'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 30 74" />
  <path d="M 64 112 C 66 98 70 88 74 76" />
  <!-- Knuckle crest across top -->
  <path d="M 32 58 C 32 46 40 44 44 48 C 46 44 52 42 56 46 C 58 42 64 42 68 46 C 70 42 78 44 78 54 C 78 68 76 78 72 86 C 68 96 66 104 64 112" />
  <!-- 4 curled finger pads facing forward -->
  <path d="M 34 56 C 36 64 42 66 44 58" />
  <path d="M 44 56 C 46 64 52 66 54 58" />
  <path d="M 54 56 C 56 64 62 66 64 58" />
  <path d="M 64 56 C 66 64 74 66 76 58" />
  <!-- Thumb horizontal support under fingertips -->
  <path d="M 28 76 C 34 68 46 66 68 68 C 74 69 74 76 68 78 C 54 80 38 82 32 84" fill="rgba(6, 182, 212, 0.15)" />
''')

# 'F': Index and thumb touch in loop; middle, ring, pinky spread upright
SVGS['F'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 33 86 32 76" />
  <path d="M 64 112 C 66 98 72 88 76 76" />
  <!-- 3 upright spread fingers (Middle, Ring, Pinky) -->
  <!-- Middle -->
  <path d="M 46 54 L 46 16 C 46 10 54 10 54 16 L 54 52" />
  <!-- Ring -->
  <path d="M 54 30 L 58 18 C 60 12 68 14 66 20 L 64 54" />
  <!-- Pinky -->
  <path d="M 65 36 L 72 26 C 74 20 82 24 80 30 L 74 64" />
  <!-- Index & Thumb circular loop on left -->
  <path d="M 32 76 C 26 70 24 60 26 50 C 28 42 38 42 42 48 C 46 54 44 64 38 68 C 34 70 32 74 32 76" />
  <circle cx="34" cy="54" r="6" stroke-width="1.8" />
''')

# 'G': Hand in profile, index finger pointing right, thumb parallel above
SVGS['G'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 28 108 C 30 94 30 84 28 74" />
  <path d="M 52 112 C 52 98 48 88 46 80" />
  <!-- Fist body -->
  <path d="M 28 74 C 26 56 32 46 44 46 L 54 46" />
  <path d="M 46 80 C 50 82 56 80 58 72 L 58 58" />
  <!-- Extended horizontal thumb above -->
  <path d="M 44 46 C 44 38 52 36 68 36 C 76 36 78 44 70 46 L 54 48" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 68 37 C 72 38 74 41 72 43" stroke-width="1.4" opacity="0.8" /><!-- nail -->
  <!-- Extended horizontal index finger below -->
  <path d="M 54 50 L 78 50 C 86 50 86 60 78 60 L 56 60" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 78 52 C 82 53 84 56 82 58" stroke-width="1.4" opacity="0.8" /><!-- nail -->
  <!-- Knuckle crease line -->
  <path d="M 46 62 C 48 70 52 70 54 62" stroke-width="1.6" opacity="0.6" />
''')

# 'H': Index and middle fingers extended horizontally together
SVGS['H'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 28 108 C 30 94 30 84 28 74" />
  <path d="M 52 112 C 52 98 48 88 46 80" />
  <!-- Fist body -->
  <path d="M 28 74 C 26 56 32 44 44 44" />
  <!-- Tucked thumb resting across -->
  <path d="M 42 44 C 44 38 52 38 54 44 L 54 56" />
  <!-- Index finger (upper horizontal) -->
  <path d="M 48 44 L 78 44 C 86 44 86 54 78 54 L 52 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle finger (lower horizontal touching index) -->
  <path d="M 52 54 L 78 54 C 86 54 86 64 78 64 L 48 64" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Curled ring and pinky under -->
  <path d="M 48 64 C 48 74 54 76 56 68" stroke-width="1.8" opacity="0.7" />
  <path d="M 42 74 C 44 80 48 80 50 74" stroke-width="1.8" opacity="0.7" />
''')

# 'I': Fist with pinky extended straight up
SVGS['I'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Curled fingers (Index, Middle, Ring) -->
  <path d="M 34 58 C 34 48 42 48 44 52 C 46 48 54 48 56 52 C 58 48 66 48 66 56 L 66 78" />
  <!-- Folded horizontal thumb across -->
  <path d="M 26 72 C 30 62 42 60 56 62 C 60 64 60 70 54 74 C 44 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <!-- Pinky finger straight up -->
  <path d="M 66 60 L 66 18 C 66 12 76 12 76 18 L 76 72" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 67 32 L 75 32" stroke-width="1.5" opacity="0.6" />
  <path d="M 67 46 L 75 46" stroke-width="1.5" opacity="0.6" />
''')

# 'J': Pinky upright with dynamic sweeping J-hook arrow
SVGS['J'] = wrap_svg('''
  <!-- Wrist & Fist (like I) -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <path d="M 34 58 C 34 48 42 48 44 52 C 46 48 54 48 56 52 C 58 48 66 48 66 56 L 66 78" />
  <path d="M 26 72 C 30 62 42 60 56 62 C 60 64 60 70 54 74 C 44 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <!-- Pinky finger -->
  <path d="M 66 60 L 66 22 C 66 16 76 16 76 22 L 76 72" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Dynamic J-hook trajectory arrow -->
  <path d="M 72 20 C 82 26 84 44 80 58 C 76 72 64 80 50 82 C 42 82 36 78 38 72" stroke="var(--cyan)" stroke-width="2.2" stroke-dasharray="3,3" />
  <polygon points="36,70 42,75 36,80" fill="var(--cyan)" />
''')

# 'K': Index vertical, middle angled forward, thumb nestled between
SVGS['K'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index vertical -->
  <path d="M 34 58 L 34 16 C 34 10 44 10 44 16 L 44 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle finger angled forward/right -->
  <path d="M 44 48 L 56 22 C 58 16 68 20 64 26 L 52 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Thumb upright nestled between index and middle -->
  <path d="M 30 74 C 32 62 40 54 44 46 C 46 42 50 42 50 48 C 48 56 46 68 44 76" fill="rgba(6, 182, 212, 0.18)" />
  <!-- Curled ring and pinky -->
  <path d="M 52 56 C 58 54 66 56 68 64 C 70 72 68 80 62 82" />
''')

# 'L': Index finger vertical, thumb horizontal (classic 90 degree L)
SVGS['L'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 38 112 C 37 98 36 88 34 78" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index vertical -->
  <path d="M 38 58 L 38 16 C 38 10 48 10 48 16 L 48 56" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 39 30 L 47 30" stroke-width="1.6" opacity="0.6" />
  <path d="M 39 44 L 47 44" stroke-width="1.6" opacity="0.6" />
  <!-- Thumb horizontal to the left (90 degree) -->
  <path d="M 34 78 C 30 78 20 74 12 74 C 6 74 6 64 12 64 C 22 64 32 60 38 58" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 12 65 C 10 67 10 71 12 73" stroke-width="1.4" opacity="0.8" /><!-- thumb nail -->
  <!-- Curled 3 fingers in fist -->
  <path d="M 48 56 C 54 52 64 52 68 60 C 72 68 70 78 64 82" />
''')

# 'M': Fist with thumb tucked under 3 fingers (index, middle, ring)
SVGS['M'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- 3 prominent knuckle bumps draping over thumb -->
  <path d="M 32 54 C 32 44 42 42 44 48 C 46 42 54 42 56 48 C 58 42 66 44 68 50 C 70 46 76 48 76 56 L 74 84" />
  <!-- Thumb tip peeking out under the 3rd (ring) knuckle -->
  <path d="M 58 66 C 60 62 66 62 68 68 C 68 72 64 76 60 74 Z" fill="rgba(6, 182, 212, 0.22)" stroke-width="1.8" />
  <!-- Horizontal finger drape crease -->
  <path d="M 34 66 C 44 64 56 64 68 66" stroke-width="1.8" opacity="0.7" />
  <path d="M 44 48 L 44 66" stroke-width="1.6" opacity="0.6" />
  <path d="M 56 48 L 56 66" stroke-width="1.6" opacity="0.6" />
''')

# 'N': Fist with thumb tucked under 2 fingers (index, middle)
SVGS['N'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- 2 prominent knuckle bumps draping over thumb -->
  <path d="M 32 54 C 32 44 44 42 46 48 C 48 42 58 42 60 48 C 62 46 72 48 74 56 L 74 84" />
  <!-- Thumb tip peeking out under the 2nd (middle) knuckle -->
  <path d="M 48 66 C 50 62 56 62 58 68 C 58 72 54 76 50 74 Z" fill="rgba(6, 182, 212, 0.22)" stroke-width="1.8" />
  <!-- Horizontal finger drape crease -->
  <path d="M 34 66 C 44 64 56 64 68 66" stroke-width="1.8" opacity="0.7" />
  <path d="M 46 48 L 46 66" stroke-width="1.6" opacity="0.6" />
''')

# 'O': Hand in profile, all fingers curved forward meeting thumb in an O circle
SVGS['O'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 28 108 C 30 94 30 84 28 74" />
  <path d="M 52 112 C 52 98 48 88 46 80" />
  <!-- Curved upper fingers meeting thumb in circular O profile -->
  <path d="M 28 74 C 26 50 34 32 52 30 C 66 28 78 36 78 48 C 78 58 72 64 62 66 C 52 68 46 72 40 76" />
  <!-- Curved thumb meeting finger tips -->
  <path d="M 30 78 C 34 84 44 86 54 84 C 64 82 72 74 72 64 C 72 56 66 54 60 56" />
  <!-- Center open aperture of the O -->
  <ellipse cx="54" cy="56" rx="10" ry="12" stroke-width="2" />
''')

# 'P': Like K pointing downward (index forward/down, middle pointing down)
SVGS['P'] = wrap_svg('''
  <!-- Wrist & Forearm entering from upper left -->
  <path d="M 24 36 C 36 44 44 50 50 58" />
  <path d="M 40 24 C 50 34 56 42 62 50" />
  <!-- Index pointing forward/downward -->
  <path d="M 62 50 L 84 62 C 88 64 84 72 78 70 L 58 64" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle pointing straight downward -->
  <path d="M 58 64 L 56 94 C 56 100 48 100 48 94 L 48 72" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Thumb angled between them -->
  <path d="M 46 54 C 52 56 56 60 54 66 C 52 70 46 70 44 64" fill="rgba(6, 182, 212, 0.18)" />
''')

# 'Q': Like G pointing downward (index and thumb pointing down)
SVGS['Q'] = wrap_svg('''
  <!-- Forearm from upper left -->
  <path d="M 24 36 C 36 44 44 50 50 58" />
  <path d="M 40 24 C 50 34 56 42 62 50" />
  <!-- Index finger pointing straight down -->
  <path d="M 54 54 L 54 94 C 54 100 46 100 46 94 L 46 64" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Thumb pointing down alongside index -->
  <path d="M 62 50 L 66 84 C 67 90 60 92 58 86 L 56 64" fill="rgba(6, 182, 212, 0.12)" />
''')

# 'R': Index and middle fingers crossed vertically
SVGS['R'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Folded thumb across front of ring & pinky -->
  <path d="M 26 72 C 30 62 42 60 56 62 C 60 64 60 70 54 74 C 44 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <!-- Middle finger crossing over in front of index -->
  <path d="M 48 56 L 38 18 C 36 12 46 10 48 16 L 54 52" fill="rgba(6, 182, 212, 0.18)" />
  <!-- Index finger extending behind and to the right -->
  <path d="M 34 56 L 48 16 C 50 10 60 12 56 18 L 46 54" fill="rgba(6, 182, 212, 0.1)" />
  <!-- Curled ring and pinky in fist -->
  <path d="M 56 56 C 64 54 72 58 72 68 C 72 76 68 82 62 84" />
''')

# 'S': Tight fist with thumb folded across FRONT of all knuckles
SVGS['S'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Knuckle crest across top -->
  <path d="M 30 58 C 30 46 40 44 44 48 C 46 44 52 42 56 46 C 58 42 64 42 68 46 C 70 42 78 44 78 54 C 78 68 76 78 72 86 C 68 96 66 104 64 112" />
  <!-- THUMB WRAPPED FIRMLY HORIZONTALLY ACROSS FRONT (Distinct from A) -->
  <path d="M 24 64 C 32 56 48 56 66 58 C 72 59 72 68 64 70 C 48 72 32 74 26 78 Z" fill="rgba(6, 182, 212, 0.25)" stroke-width="2.6" />
  <path d="M 60 60 C 64 62 65 65 63 67" stroke-width="1.5" opacity="0.8" /><!-- thumb nail -->
  <!-- Curled finger creases beneath thumb -->
  <path d="M 34 78 C 44 76 56 76 68 78" stroke-width="1.8" opacity="0.7" />
''')

# 'T': Fist with thumb tucked between index and middle
SVGS['T'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <path d="M 30 58 C 30 46 40 44 44 48 C 46 42 52 42 56 46 C 58 42 64 42 68 46 C 70 42 78 44 78 54 L 74 84" />
  <!-- THUMB POKING UP BETWEEN INDEX AND MIDDLE -->
  <path d="M 38 56 C 38 46 46 46 46 56 C 46 62 42 66 38 64 Z" fill="rgba(6, 182, 212, 0.28)" stroke-width="2.2" />
  <path d="M 40 48 C 42 47 44 47 45 49" stroke-width="1.4" opacity="0.8" /><!-- nail -->
  <!-- Horizontal finger crease -->
  <path d="M 34 66 C 46 64 58 64 70 66" stroke-width="1.8" opacity="0.7" />
''')

# 'U': Index and middle fingers held together straight up
SVGS['U'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index and Middle held together straight up -->
  <path d="M 36 56 L 36 16 C 36 10 46 10 46 16 L 46 54" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 46 16 C 46 10 56 10 56 16 L 56 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Dividing line between index and middle -->
  <line x1="46" y1="12" x2="46" y2="54" stroke-width="1.8" />
  <!-- Joint creases -->
  <path d="M 37 30 L 55 30" stroke-width="1.6" opacity="0.6" />
  <path d="M 37 42 L 55 42" stroke-width="1.6" opacity="0.6" />
  <!-- Thumb folded across curled ring and pinky -->
  <path d="M 28 72 C 32 64 44 62 58 64 C 62 66 60 72 54 74 C 44 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 56 56 C 64 54 72 58 72 68 L 72 82" />
''')

# 'V': Peace sign / V with index and middle spread apart
SVGS['V'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index angled left -->
  <path d="M 36 56 L 28 18 C 26 12 36 8 38 14 L 46 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle angled right -->
  <path d="M 46 54 L 58 14 C 60 8 70 12 68 18 L 56 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Thumb folded across curled ring & pinky -->
  <path d="M 26 72 C 30 64 42 62 56 64 C 60 66 58 72 52 74 C 42 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 56 56 C 64 54 72 58 72 68 L 72 82" />
''')

# 'W': Three fingers (index, middle, ring) spread apart in a W
SVGS['W'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index angled left -->
  <path d="M 34 56 L 24 20 C 22 14 30 12 34 18 L 42 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle straight up -->
  <path d="M 42 54 L 44 14 C 44 8 52 8 52 14 L 54 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Ring angled right -->
  <path d="M 54 54 L 64 18 C 66 12 74 14 72 20 L 64 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Thumb holding curled pinky -->
  <path d="M 28 72 C 32 64 44 64 54 66 C 58 68 56 74 50 76 C 40 78 32 80 28 82" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 64 58 C 70 60 74 66 72 74 L 72 82" />
''')

# 'X': Fist with index finger crooked/hooked upright
SVGS['X'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Curled fingers in fist -->
  <path d="M 44 56 C 46 48 56 48 58 52 C 60 48 68 48 70 56 L 72 82" />
  <path d="M 26 72 C 30 62 42 60 56 62 C 60 64 60 70 54 74 C 44 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <!-- Crooked index finger hook -->
  <path d="M 32 60 L 32 36 C 32 26 42 26 44 34 C 46 42 40 44 38 42" fill="rgba(6, 182, 212, 0.18)" stroke-width="2.6" />
''')

# 'Y': Shaka - thumb and pinky extended wide, middle 3 curled
SVGS['Y'] = wrap_svg('''
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 34 86 32 76" />
  <path d="M 64 112 C 65 100 68 88 70 76" />
  <!-- 3 middle fingers curled in fist -->
  <path d="M 36 58 C 36 48 44 48 46 52 C 48 48 54 48 56 52 C 58 48 64 48 64 56 L 64 78" />
  <!-- Extended thumb pointing wide left -->
  <path d="M 32 76 C 26 74 16 66 10 52 C 8 46 16 42 20 48 C 26 56 30 60 36 58" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 12 48 C 14 46 18 47 18 51" stroke-width="1.4" opacity="0.8" /><!-- nail -->
  <!-- Extended pinky pointing wide right -->
  <path d="M 64 62 C 70 58 78 50 84 38 C 88 32 94 36 92 42 C 88 56 78 68 70 76" fill="rgba(6, 182, 212, 0.15)" />
  <path d="M 88 38 C 90 39 92 42 90 44" stroke-width="1.4" opacity="0.8" /><!-- nail -->
''')

# 'Z': Index finger drawing Z in space
SVGS['Z'] = wrap_svg('''
  <!-- Wrist & Hand (like 1/D) -->
  <path d="M 36 112 C 35 98 32 86 30 76" />
  <path d="M 64 112 C 65 100 70 88 74 76" />
  <!-- Index finger pointing forward -->
  <path d="M 34 58 L 34 22 C 34 16 44 16 44 22 L 44 56" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 44 56 C 52 52 64 52 68 60 L 68 82" />
  <path d="M 28 72 C 32 64 44 62 56 64 C 60 66 58 72 52 74 C 42 76 34 78 30 82" fill="rgba(6, 182, 212, 0.15)" />
  <!-- 'Z' trajectory path indicator -->
  <path d="M 52 18 L 78 18 L 56 42 L 82 42" stroke="var(--cyan)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" />
  <polygon points="80,38 86,42 80,46" fill="var(--cyan)" />
''')

# Digits 0-9
SVGS['0'] = SVGS['O']
SVGS['1'] = SVGS['D']
SVGS['2'] = SVGS['V']
SVGS['3'] = wrap_svg('''
  <!-- ASL 3: Thumb, Index, Middle extended -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 98 34 86 32 76" />
  <path d="M 64 112 C 65 100 68 88 70 76" />
  <!-- Thumb extended left -->
  <path d="M 32 76 C 26 74 16 66 10 52 C 8 46 16 42 20 48 C 26 56 30 60 36 58" fill="rgba(6, 182, 212, 0.15)" />
  <!-- Index vertical -->
  <path d="M 36 56 L 36 16 C 36 10 46 10 46 16 L 46 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle vertical -->
  <path d="M 46 54 L 50 14 C 50 8 60 8 60 14 L 60 56" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Curled ring and pinky in fist -->
  <path d="M 60 56 C 66 54 74 58 74 68 L 72 82" />
''')
SVGS['4'] = wrap_svg('''
  <!-- ASL 4: 4 fingers upright, thumb folded in -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 28 74" />
  <path d="M 64 112 C 66 98 72 86 74 72" />
  <!-- 4 spread upright fingers -->
  <path d="M 30 58 L 28 20 C 28 14 36 14 36 20 L 38 56" />
  <path d="M 38 22 L 42 14 C 42 8 50 8 50 14 L 50 56" />
  <path d="M 50 20 L 54 16 C 54 10 62 10 62 16 L 62 58" />
  <path d="M 62 24 L 66 22 C 66 16 74 16 74 22 L 74 64" />
  <!-- Thumb folded across lower palm -->
  <path d="M 28 74 C 32 68 40 66 52 68 C 56 69 56 76 50 78 C 42 80 34 82 30 86" fill="rgba(6, 182, 212, 0.15)" />
''')
SVGS['5'] = wrap_svg('''
  <!-- ASL 5: All 5 fingers spread open wide -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 34 84 32 74" />
  <path d="M 64 112 C 66 98 68 86 70 72" />
  <!-- Thumb spread wide left -->
  <path d="M 32 74 C 26 72 16 64 10 52 C 8 46 16 42 20 48 C 26 56 30 60 34 56" fill="rgba(6, 182, 212, 0.15)" />
  <!-- 4 spread upright fingers -->
  <path d="M 34 56 L 30 20 C 30 14 38 14 38 20 L 42 54" />
  <path d="M 42 54 L 46 14 C 46 8 54 8 54 14 L 54 54" />
  <path d="M 54 54 L 60 16 C 60 10 68 10 68 16 L 66 56" />
  <path d="M 66 56 L 74 22 C 76 16 84 18 82 24 L 74 64" />
''')
SVGS['6'] = wrap_svg('''
  <!-- ASL 6: Pinky touches thumb tip, index/middle/ring upright -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 30 74" />
  <path d="M 64 112 C 66 98 70 88 74 76" />
  <!-- 3 upright fingers (Index, Middle, Ring) -->
  <path d="M 34 56 L 34 16 C 34 10 44 10 44 16 L 44 54" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 44 54 L 50 14 C 50 8 60 8 60 14 L 60 54" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 60 54 L 66 18 C 66 12 76 12 74 18 L 72 58" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Pinky touching thumb in loop on right -->
  <path d="M 30 74 C 34 66 46 64 56 68 C 62 70 64 78 58 80 C 48 82 38 82 30 82" />
  <circle cx="62" cy="72" r="6" stroke-width="1.8" />
''')
SVGS['7'] = wrap_svg('''
  <!-- ASL 7: Ring touches thumb tip, index/middle/pinky upright -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 30 74" />
  <path d="M 64 112 C 66 98 70 88 74 76" />
  <!-- Index and Middle upright -->
  <path d="M 34 56 L 34 16 C 34 10 44 10 44 16 L 44 54" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 44 54 L 50 14 C 50 8 60 8 60 14 L 60 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Pinky upright on right -->
  <path d="M 68 54 L 74 22 C 76 16 84 18 82 24 L 74 64" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Ring touching thumb in center loop -->
  <circle cx="56" cy="68" r="6" stroke-width="1.8" />
''')
SVGS['8'] = wrap_svg('''
  <!-- ASL 8: Middle touches thumb tip, index/ring/pinky upright -->
  <!-- Wrist -->
  <path d="M 36 112 C 35 96 32 84 30 74" />
  <path d="M 64 112 C 66 98 70 88 74 76" />
  <!-- Index upright -->
  <path d="M 34 56 L 34 16 C 34 10 44 10 44 16 L 44 54" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Ring and Pinky upright -->
  <path d="M 58 54 L 62 18 C 62 12 70 12 70 18 L 68 58" fill="rgba(6, 182, 212, 0.12)" />
  <path d="M 68 54 L 74 22 C 76 16 84 18 82 24 L 74 64" fill="rgba(6, 182, 212, 0.12)" />
  <!-- Middle finger touching thumb tip in loop -->
  <circle cx="48" cy="66" r="6" stroke-width="1.8" />
''')
SVGS['9'] = SVGS['F']

# Output JSON file for easy embedding or reading
out_path = Path(__file__).resolve().parent.parent / "js" / "asl_svg_data.js"
out_path.parent.mkdir(parents=True, exist_ok=True)

with open(out_path, "w", encoding="utf-8") as f:
    f.write("// PocketGull High-Fidelity Anatomical ASL Vector SVG Library\n")
    f.write("const ASL_SVG_DATA = " + json.dumps(SVGS, indent=2) + ";\n")

print(f"Generated {len(SVGS)} high-fidelity ASL SVG vectors to {out_path}")
