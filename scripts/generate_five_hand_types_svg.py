#!/usr/bin/env python3
"""
Advanced Five Human Hand Types Studio Generator.
Based on Elsie Lincoln Benedict & Ralph Paine Benedict (1921)
Illustrated by Raymond H. Lufkin (The Roycrofters)
Enforces Louise Sloan 5:1 Optotype Acuity & Dieter Rams Design Invariants.

Anatomical Invariants:
- Left Hand Dorsal View matching 1921 archival plates.
- Digit III (Middle Finger) is the apex/longest digit.
- Thumb projects UPWARD and OUTWARD at 35°-40° (tip at y ~ 240-260).
- True thenar eminence & first interdigital web space.
- 100% self-contained diagnostic comparisons and layered telemetry.
"""

import os
import json

def get_nail_svg(cx, cy, w, h, nail_type='oval', angle=0, fill_color="#38bdf8"):
    transform = f'transform="rotate({angle}, {cx}, {cy})"' if angle != 0 else ''
    
    if nail_type == 'round': # Alimentive
        return f'''<g {transform} class="nail-plate">
          <path d="M {cx - w/2} {cy + h/2}
                   C {cx - w/2} {cy + h/2 - 2}, {cx - w/2} {cy}, {cx - w/2 + 2} {cy - h/4}
                   C {cx - w/3} {cy - h/2}, {cx + w/3} {cy - h/2}, {cx + w/2 - 2} {cy - h/4}
                   C {cx + w/2} {cy}, {cx + w/2} {cy + h/2 - 2}, {cx + w/2} {cy + h/2}
                   C {cx + w/3} {cy + h/2 + 2}, {cx - w/3} {cy + h/2 + 2}, {cx - w/2} {cy + h/2} Z"
                fill="{fill_color}" fill-opacity="0.32" stroke="{fill_color}" stroke-width="1.8"/>
          <path d="M {cx - w/2 - 1} {cy + h/2} Q {cx} {cy + h/2 + 3} {cx + w/2 + 1} {cy + h/2}"
                fill="none" stroke="{fill_color}" stroke-width="1.4" opacity="0.8"/>
          <path d="M {cx - w/3} {cy + h/2} Q {cx} {cy + h/4} {cx + w/3} {cy + h/2}"
                fill="{fill_color}" fill-opacity="0.45"/>
        </g>'''
        
    elif nail_type == 'conical': # Thoracic
        return f'''<g {transform} class="nail-plate">
          <path d="M {cx - w/2} {cy + h/2}
                   C {cx - w/2} {cy + h/4}, {cx - w/2.5} {cy - h/4}, {cx} {cy - h/2}
                   C {cx + w/2.5} {cy - h/4}, {cx + w/2} {cy + h/4}, {cx + w/2} {cy + h/2}
                   Q {cx} {cy + h/2 + 2} {cx - w/2} {cy + h/2} Z"
                fill="{fill_color}" fill-opacity="0.32" stroke="{fill_color}" stroke-width="1.8"/>
          <path d="M {cx - w/2 - 1} {cy + h/2} Q {cx} {cy + h/2 + 2.5} {cx + w/2 + 1} {cy + h/2}"
                fill="none" stroke="{fill_color}" stroke-width="1.4" opacity="0.85"/>
          <path d="M {cx - w/3} {cy + h/2} Q {cx} {cy + h/3} {cx + w/3} {cy + h/2}"
                fill="{fill_color}" fill-opacity="0.45"/>
        </g>'''

    elif nail_type == 'square': # Muscular
        return f'''<g {transform} class="nail-plate">
          <path d="M {cx - w/2} {cy - h/2}
                   L {cx + w/2} {cy - h/2}
                   L {cx + w/2} {cy + h/2 - 2}
                   C {cx + w/2} {cy + h/2}, {cx + w/3} {cy + h/2 + 1}, {cx} {cy + h/2 + 1}
                   C {cx - w/3} {cy + h/2 + 1}, {cx - w/2} {cy + h/2}, {cx - w/2} {cy + h/2 - 2} Z"
                fill="{fill_color}" fill-opacity="0.35" stroke="{fill_color}" stroke-width="2"/>
          <path d="M {cx - w/2 - 1} {cy + h/2 - 1} Q {cx} {cy + h/2 + 2} {cx + w/2 + 1} {cy + h/2 - 1}"
                fill="none" stroke="{fill_color}" stroke-width="1.5" opacity="0.85"/>
          <path d="M {cx - w/3} {cy + h/2} Q {cx} {cy + h/4} {cx + w/3} {cy + h/2}"
                fill="{fill_color}" fill-opacity="0.5"/>
        </g>'''

    elif nail_type == 'oblong': # Osseous
        return f'''<g {transform} class="nail-plate">
          <rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="2"
                fill="{fill_color}" fill-opacity="0.32" stroke="{fill_color}" stroke-width="1.9"/>
          <line x1="{cx - w/2 - 1}" y1="{cy + h/2}" x2="{cx + w/2 + 1}" y2="{cy + h/2}"
                stroke="{fill_color}" stroke-width="1.5" opacity="0.85"/>
          <path d="M {cx - w/3} {cy + h/2} Q {cx} {cy + h/3} {cx + w/3} {cy + h/2}"
                fill="{fill_color}" fill-opacity="0.45"/>
        </g>'''

    else: # Cerebral (Filbert / Slender Oval)
        return f'''<g {transform} class="nail-plate">
          <ellipse cx="{cx}" cy="{cy}" rx="{w/2}" ry="{h/2}"
                   fill="{fill_color}" fill-opacity="0.3" stroke="{fill_color}" stroke-width="1.8"/>
          <path d="M {cx - w/2 + 1} {cy + h/3} Q {cx} {cy + h/2 + 1} {cx + w/2 - 1} {cy + h/3}"
                fill="none" stroke="{fill_color}" stroke-width="1.3" opacity="0.8"/>
          <path d="M {cx - w/3} {cy + h/2 - 1} Q {cx} {cy + h/4} {cx + w/3} {cy + h/2 - 1}"
                fill="{fill_color}" fill-opacity="0.4"/>
        </g>'''

def get_sloan_grid_svg(view_w=680, view_h=520, unit_size=65):
    """5x5 Louise Sloan Optotype Grid with 1-unit stroke clearance markers."""
    lines = []
    start_x = 240 - (2.5 * unit_size)
    start_y = 260 - (2.5 * unit_size)
    for i in range(6):
        x = start_x + (i * unit_size)
        y = start_y + (i * unit_size)
        lines.append(f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{start_y + 5*unit_size}" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.35"/>')
        lines.append(f'<line x1="{start_x}" y1="{y}" x2="{start_x + 5*unit_size}" y2="{y}" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.35"/>')
    lines.append(f'<rect x="{start_x}" y="{start_y - 22}" width="165" height="18" rx="4" fill="#090d16" stroke="#38bdf8" stroke-width="1" opacity="0.8"/>')
    lines.append(f'<text x="{start_x + 6}" y="{start_y - 9}" fill="#38bdf8" font-family="monospace" font-size="10" font-weight="bold">SLOAN 5×5 OPTOTYPE GRID (1U=65px)</text>')
    return '<g class="layer-sloan" style="display: none;">\n' + '\n'.join(lines) + '\n</g>'

def get_callout_badge(x1, y1, x2, y2, text_title, text_sub, color, anchor="start"):
    """Renders a leader line with a high-contrast pill badge to guarantee zero text clipping."""
    bw = max(len(text_title), len(text_sub)) * 7 + 16
    by = y2 - 12
    if anchor == "end":
        bx = max(x2, -90 + bw)
        rect_x = bx - bw
        tx = bx - 8
    else:
        bx = min(x2, 560 - bw)
        rect_x = bx
        tx = rect_x + 8
    
    return f'''<g class="layer-callouts callout-badge">
      <polyline points="{x1},{y1} {bx},{y1} {bx},{y2}" fill="none" stroke="{color}" stroke-width="1.4" opacity="0.8"/>
      <circle cx="{x1}" cy="{y1}" r="3" fill="{color}"/>
      <rect x="{rect_x}" y="{by}" width="{bw}" height="28" rx="5" fill="#0b1120" stroke="{color}" stroke-width="1.2" filter="url(#badgeShadow)"/>
      <text x="{tx}" y="{by + 12}" text-anchor="{anchor}" fill="{color}" font-family="system-ui, sans-serif" font-size="10.5" font-weight="bold">{text_title}</text>
      <text x="{tx}" y="{by + 23}" text-anchor="{anchor}" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="9">{text_sub}</text>
    </g>'''

def get_ratio_caliper_svg(x_left, y_top, y_bottom, label, ratio_text, color, offset_x=-35):
    """Renders vertical caliper dimension lines with arrowheads and ratio badges."""
    cx = x_left + offset_x
    return f'''<g class="layer-ratios caliper-guide" style="display: none;">
      <line x1="{x_left}" y1="{y_top}" x2="{cx - 10}" y2="{y_top}" stroke="{color}" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>
      <line x1="{x_left}" y1="{y_bottom}" x2="{cx - 10}" y2="{y_bottom}" stroke="{color}" stroke-width="1" stroke-dasharray="2 2" opacity="0.7"/>
      <line x1="{cx}" y1="{y_top + 4}" x2="{cx}" y2="{y_bottom - 4}" stroke="{color}" stroke-width="1.5"/>
      <polygon points="{cx},{y_top} {cx-3},{y_top+6} {cx+3},{y_top+6}" fill="{color}"/>
      <polygon points="{cx},{y_bottom} {cx-3},{y_bottom-6} {cx+3},{y_bottom-6}" fill="{color}"/>
      <rect x="{cx - 45}" y="{(y_top + y_bottom)/2 - 14}" width="90" height="26" rx="4" fill="#090d16" stroke="{color}" stroke-width="1.2"/>
      <text x="{cx}" y="{(y_top + y_bottom)/2 - 1}" text-anchor="middle" fill="{color}" font-family="system-ui" font-size="9.5" font-weight="bold">{label}</text>
      <text x="{cx}" y="{(y_top + y_bottom)/2 + 10}" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">{ratio_text}</text>
    </g>'''

# ==========================================
# 1. THE ALIMENTIVE HAND (Full Multi-Layer)
# ==========================================
def get_alimentive_full_svg():
    c = "#f59e0b"
    return f'''<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="alimGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadowAlim" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- LAYER 1: MASS SILHOUETTE -->
  <g class="layer-mass">
    <circle cx="240" cy="265" r="180" fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.4"/>
    <text x="240" y="38" text-anchor="middle" fill="{c}" font-family="monospace" font-size="11" letter-spacing="1">GEOMETRIC ARCHETYPE: CIRCLE</text>
    <circle cx="235" cy="285" r="130" fill="url(#alimGlow)"/>
  </g>

  <!-- LAYER 2: UNDERLYING PRIMITIVES (Stacked Spheres Along Natural Ray) -->
  <g class="layer-primitives" style="display: none;" stroke="{c}" stroke-width="1.2" fill="{c}" fill-opacity="0.08" stroke-dasharray="3 3">
    <circle cx="240" cy="330" r="80"/>
    <circle cx="345" cy="370" r="45"/>
    <!-- Little Stacked Spheres (Digit V) -->
    <circle cx="160" cy="245" r="15"/>
    <circle cx="158" cy="210" r="14"/>
    <circle cx="156" cy="175" r="12"/>
    <!-- Ring Stacked Spheres (Digit IV) -->
    <circle cx="222" cy="240" r="18"/>
    <circle cx="221" cy="190" r="16"/>
    <circle cx="220" cy="145" r="14"/>
    <!-- Middle Stacked Spheres (Digit III - Longest) -->
    <circle cx="283" cy="235" r="19"/>
    <circle cx="284" cy="175" r="17"/>
    <circle cx="285" cy="120" r="15"/>
    <!-- Index Stacked Spheres (Digit II) -->
    <circle cx="345" cy="245" r="18"/>
    <circle cx="348" cy="195" r="16"/>
    <circle cx="350" cy="150" r="14"/>
    <!-- Thumb Stacked Spheres (Projects Up & Out at 35°) -->
    <circle cx="365" cy="360" r="20"/>
    <circle cx="392" cy="310" r="17"/>
    <circle cx="418" cy="255" r="14"/>
  </g>

  <!-- LAYER 3: RATIO & DIMENSION CALIPERS -->
  {get_ratio_caliper_svg(150, 95, 245, "Finger Len", "L = 150px", c, -50)}
  {get_ratio_caliper_svg(150, 245, 450, "Palm Height", "H = 205px", c, -50)}
  <g class="layer-ratios caliper-guide" style="display: none;">
    <line x1="160" y1="450" x2="310" y2="450" stroke="{c}" stroke-width="1.5"/>
    <rect x="205" y="458" width="80" height="20" rx="3" fill="#090d16" stroke="{c}" stroke-width="1"/>
    <text x="245" y="472" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9">Wrist: 150px (0.92:1)</text>
    <rect x="420" y="190" width="125" height="32" rx="4" fill="#090d16" stroke="{c}" stroke-width="1.2"/>
    <text x="482" y="204" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">PALM : FINGER RATIO</text>
    <text x="482" y="216" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">1.00 : 0.78 (Short Digits)</text>
  </g>

  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  {get_sloan_grid_svg()}

  <!-- LAYER 5: MAIN HAND CONTOUR (Anatomical Left Hand Dorsal with Upward Thumb) -->
  <g class="layer-contour">
    <path d="M 160 450
             C 158 395, 140 345, 145 275
             C 140 250, 134 210, 144 175
             C 148 152, 172 152, 176 175
             C 182 200, 180 230, 186 255
             C 188 225, 192 158, 204 128
             C 212 112, 234 112, 242 128
             C 250 158, 246 225, 250 248
             C 254 215, 260 135, 270 95
             C 278 80, 298 80, 306 95
             C 316 135, 312 215, 316 250
             C 320 225, 326 155, 338 135
             C 346 122, 368 122, 374 138
             C 380 170, 370 235, 362 272
             C 358 288, 368 298, 382 290
             C 392 280, 404 262, 414 246
             C 422 232, 436 240, 432 255
             C 428 275, 430 310, 420 340
             C 410 375, 380 420, 310 450
             Z"
          fill="#1e293b" stroke="{c}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" filter="url(#shadowAlim)"/>
  </g>

  <!-- LAYER 6: DETAILS (Articulated Nails, Dimples, Creases) -->
  <g class="layer-details">
    <!-- Articulated Upward-Sloped Chubby Thumb (35° tilt) -->
    <path d="M 370 340 C 390 315, 405 285, 414 252" fill="none" stroke="{c}" stroke-width="2" opacity="0.6"/>
    {get_nail_svg(424, 248, 16, 14, 'round', 35, c)}

    <!-- Finger Nails (Left to Right: Pinky, Ring, Middle, Index) -->
    {get_nail_svg(160, 162, 12, 11, 'round', 0, c)}
    {get_nail_svg(223, 120, 15, 14, 'round', 0, c)}
    {get_nail_svg(288, 88, 16, 15, 'round', 0, c)}
    {get_nail_svg(356, 130, 14, 13, 'round', 0, c)}

    <!-- Knuckle Dimples -->
    <g stroke="{c}" stroke-width="2.5" stroke-linecap="round" fill="none">
      <path d="M 160 260 Q 165 264 170 260"/>
      <circle cx="165" cy="259" r="2" fill="{c}"/>
      <path d="M 216 252 Q 221 256 226 252"/>
      <circle cx="221" cy="251" r="2" fill="{c}"/>
      <path d="M 280 250 Q 285 254 290 250"/>
      <circle cx="285" cy="249" r="2" fill="{c}"/>
      <path d="M 344 265 Q 349 269 354 265"/>
      <circle cx="349" cy="264" r="2" fill="{c}"/>
      <circle cx="418" cy="335" r="2.5" fill="{c}"/>
    </g>

    <!-- Fleshy Infant Wrist Creases -->
    <path d="M 185 415 Q 235 430 285 415" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" opacity="0.7"/>
    <path d="M 195 435 Q 235 446 275 435" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
  </g>

  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    <rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>
    <text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>
    <text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">Phalanx vs. Joint Profile</text>
    <rect x="52" y="32" width="10" height="75" rx="3" fill="#64748b" opacity="0.6"/>
    <path d="M 46 32 C 34 50, 34 65, 46 72 C 34 85, 36 95, 50 107 L 64 107 C 78 95, 80 85, 68 72 C 80 65, 80 50, 68 32 Z"
          fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>
    <line x1="28" y1="72" x2="44" y2="72" stroke="{c}" stroke-width="1.2"/>
    <text x="25" y="75" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Narrow</text>
    <text x="25" y="83" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Joint</text>
    <line x1="86" y1="52" x2="70" y2="52" stroke="{c}" stroke-width="1.2"/>
    <text x="89" y="55" text-anchor="start" fill="{c}" font-family="monospace" font-size="8">Fat Puff</text>
  </g>

  <!-- LAYER 8: UNCLIPPED HIGH-CONTRAST CALLOUT BADGES -->
  {get_callout_badge(165, 259, -15, 240, "Knuckle Dimples", "Fat cushions replace bone", c, "end")}
  {get_callout_badge(370, 205, 480, 175, "Narrow Joints", "Flesh puffs out between", c, "start")}
  {get_callout_badge(424, 248, 485, 240, "Plump Upward Thumb", "Articulated at 35° angle", c, "start")}
  {get_callout_badge(235, 435, -15, 420, "Fleshy Wrist", "Double infant skin folds", c, "end")}
</svg>'''

# ==========================================
# 2. THE THORACIC HAND (Full Multi-Layer)
# ==========================================
def get_thoracic_full_svg():
    c = "#ec4899"
    return f'''<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="thorGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadowThor" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- LAYER 1: MASS SILHOUETTE -->
  <g class="layer-mass">
    <path d="M 235 50 L 375 255 L 235 450 L 95 255 Z" fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.4"/>
    <text x="235" y="38" text-anchor="middle" fill="{c}" font-family="monospace" font-size="11" letter-spacing="1">GEOMETRIC ARCHETYPE: WEDGE / CONICAL TAPER</text>
    <circle cx="235" cy="265" r="130" fill="url(#thorGlow)"/>
  </g>

  <!-- LAYER 2: UNDERLYING PRIMITIVES (Converging Conical Wedges) -->
  <g class="layer-primitives" style="display: none;" stroke="{c}" stroke-width="1.2" fill="{c}" fill-opacity="0.08" stroke-dasharray="3 3">
    <polygon points="175,255 295,255 285,440 185,440"/>
    <polygon points="156,245 180,245 170,145"/>
    <polygon points="196,240 242,240 226,105"/>
    <polygon points="256,238 310,238 284,55"/>
    <polygon points="318,245 362,245 344,115"/>
    <!-- Upward Thumb Wedge -->
    <polygon points="350,350 422,235 385,385"/>
  </g>

  <!-- LAYER 3: RATIO & DIMENSION CALIPERS -->
  {get_ratio_caliper_svg(160, 55, 240, "Digit III", "L = 185px", c, -50)}
  {get_ratio_caliper_svg(160, 240, 445, "Palm Height", "H = 155px", c, -50)}
  <g class="layer-ratios caliper-guide" style="display: none;">
    <line x1="180" y1="445" x2="295" y2="445" stroke="{c}" stroke-width="1.5"/>
    <rect x="200" y="455" width="80" height="20" rx="3" fill="#090d16" stroke="{c}" stroke-width="1"/>
    <text x="240" y="469" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9">Wrist: 115px (0.72:1)</text>
    <rect x="420" y="190" width="135" height="32" rx="4" fill="#090d16" stroke="{c}" stroke-width="1.2"/>
    <text x="487" y="204" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">PALM : FINGER RATIO</text>
    <text x="487" y="216" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">1.00 : 1.18 (Long Middle)</text>
  </g>

  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  {get_sloan_grid_svg()}

  <!-- LAYER 5: MAIN HAND CONTOUR (Anatomical Left Hand Dorsal with Upward Thumb) -->
  <g class="layer-contour">
    <path d="M 180 445
             C 174 385, 156 330, 162 270
             C 156 240, 150 190, 158 152
             C 164 134, 178 134, 184 152
             C 190 190, 186 225, 192 245
             C 196 205, 204 145, 215 110
             C 222 92, 238 92, 245 110
             C 255 145, 252 205, 256 242
             C 260 200, 266 100, 275 60
             C 282 45, 296 45, 304 60
             C 314 100, 310 200, 314 245
             C 320 205, 328 140, 338 120
             C 345 105, 360 108, 365 125
             C 370 160, 362 225, 355 268
             C 350 285, 362 295, 376 285
             C 388 275, 402 255, 414 238
             C 422 225, 435 232, 432 248
             C 426 270, 424 310, 412 345
             C 398 385, 365 425, 295 445
             Z"
          fill="#1e293b" stroke="{c}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round" filter="url(#shadowThor)"/>
  </g>

  <!-- LAYER 6: DETAILS (Conical Nails, Dorsal Veins, Upward Graceful Thumb) -->
  <g class="layer-details">
    <path d="M 365 330 C 385 305, 402 278, 416 248" fill="none" stroke="{c}" stroke-width="1.8" opacity="0.6"/>
    {get_nail_svg(422, 240, 15, 18, 'conical', 38, c)}

    <!-- Conical Nails (Pinky, Ring, Middle, Index) -->
    {get_nail_svg(171, 142, 11, 15, 'conical', -6, c)}
    {get_nail_svg(230, 102, 14, 18, 'conical', -2, c)}
    {get_nail_svg(290, 52, 16, 22, 'conical', 0, c)}
    {get_nail_svg(352, 115, 13, 17, 'conical', 5, c)}

    <!-- High Thoracic Vascularity (Dorsal Veins) -->
    <path d="M 235 425 C 238 375, 250 330, 245 290 C 240 258, 215 242, 205 232"
          fill="none" stroke="#f43f5e" stroke-width="1.6" opacity="0.75"/>
    <path d="M 245 290 C 260 262, 280 246, 285 234"
          fill="none" stroke="#f43f5e" stroke-width="1.4" opacity="0.65"/>
  </g>

  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    <rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>
    <text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>
    <text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">Conical Taper Profile</text>
    <path d="M 44 32 L 54 105 L 66 105 L 76 32 Z" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>
    <path d="M 52 32 Q 60 22 68 32 Z" fill="{c}" fill-opacity="0.5" stroke="{c}" stroke-width="1.2"/>
    <line x1="30" y1="65" x2="50" y2="65" stroke="{c}" stroke-width="1.2"/>
    <text x="26" y="68" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Smooth</text>
    <text x="26" y="76" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Taper</text>
  </g>

  <!-- LAYER 8: UNCLIPPED CALLOUT BADGES -->
  {get_callout_badge(290, 50, -15, 60, "Long 2nd Digit", "Dominates hand length", c, "end")}
  {get_callout_badge(171, 142, -15, 140, "Conical Nails", "Tapered distal plates", c, "end")}
  {get_callout_badge(422, 240, 485, 235, "Slender Upward Thumb", "Projects at 38° elevation", c, "start")}
  {get_callout_badge(245, 290, 485, 310, "Thin-Skinned", "High thoracic vascularity", c, "start")}
</svg>'''

# ==========================================
# 3. THE MUSCULAR HAND (Full Multi-Layer)
# ==========================================
def get_muscular_full_svg():
    c = "#06b6d4"
    return f'''<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="muscGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadowMusc" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- LAYER 1: MASS SILHOUETTE -->
  <g class="layer-mass">
    <rect x="115" y="75" width="265" height="325" rx="4" fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.4"/>
    <text x="247" y="38" text-anchor="middle" fill="{c}" font-family="monospace" font-size="11" letter-spacing="1">GEOMETRIC ARCHETYPE: SQUARE / RIGHT ANGLES</text>
    <circle cx="245" cy="275" r="140" fill="url(#muscGlow)"/>
  </g>

  <!-- LAYER 2: UNDERLYING PRIMITIVES (1:1 Square Blocks & Spatulate Cylinders) -->
  <g class="layer-primitives" style="display: none;" stroke="{c}" stroke-width="1.2" fill="{c}" fill-opacity="0.08" stroke-dasharray="3 3">
    <rect x="155" y="235" width="170" height="170" rx="4"/>
    <rect x="155" y="405" width="170" height="45"/>
    <polygon points="134,135 174,135 170,240 138,240"/>
    <polygon points="190,98 240,98 236,235 194,235"/>
    <polygon points="256,75 306,75 302,238 260,238"/>
    <polygon points="322,110 368,110 364,245 324,245"/>
    <!-- Upward Heavy Thenar Cube -->
    <rect x="340" y="295" width="80" height="75" rx="6" transform="rotate(-35, 380, 330)"/>
  </g>

  <!-- LAYER 3: RATIO & DIMENSION CALIPERS -->
  {get_ratio_caliper_svg(140, 75, 235, "Digit III", "L = 160px", c, -50)}
  {get_ratio_caliper_svg(140, 235, 450, "Palm Height", "H = 215px", c, -50)}
  <g class="layer-ratios caliper-guide" style="display: none;">
    <line x1="155" y1="450" x2="325" y2="450" stroke="{c}" stroke-width="1.5"/>
    <rect x="200" y="458" width="80" height="20" rx="3" fill="#090d16" stroke="{c}" stroke-width="1"/>
    <text x="240" y="472" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9">Wrist: 170px (1.02:1)</text>
    <rect x="420" y="190" width="135" height="32" rx="4" fill="#090d16" stroke="{c}" stroke-width="1.2"/>
    <text x="487" y="204" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">PALM : FINGER RATIO</text>
    <text x="487" y="216" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">1.00 : 1.00 (Square Balance)</text>
  </g>

  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  {get_sloan_grid_svg()}

  <!-- LAYER 5: MAIN HAND CONTOUR (Anatomical Left Hand Dorsal with Upward Spatulate Thumb) -->
  <g class="layer-contour">
    <path d="M 155 450
             L 155 390
             L 142 390
             C 138 335, 142 275, 148 245
             L 138 152
             L 134 135
             L 174 135
             L 170 152
             L 174 240
             L 182 240
             L 194 116
             L 190 98
             L 240 98
             L 236 116
             L 242 235
             L 250 235
             L 260 92
             L 256 75
             L 306 75
             L 302 92
             L 308 238
             L 316 238
             L 326 128
             L 322 110
             L 368 110
             L 364 128
             L 368 268
             C 362 285, 372 295, 386 285
             C 398 275, 412 256, 422 242
             C 432 230, 446 238, 442 254
             C 436 280, 435 325, 420 358
             C 402 395, 368 430, 325 450
             Z"
          fill="#1e293b" stroke="{c}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round" filter="url(#shadowMusc)"/>
  </g>

  <!-- LAYER 6: DETAILS (Spatulate Nails, Knuckles, Upward Thumb) -->
  <g class="layer-details">
    <path d="M 380 340 C 400 310, 416 280, 428 252" fill="none" stroke="{c}" stroke-width="2.2" opacity="0.6"/>
    {get_nail_svg(430, 246, 20, 18, 'square', 35, c)}

    <!-- Spatulate Nails (Pinky, Ring, Middle, Index) -->
    {get_nail_svg(154, 142, 18, 14, 'square', 0, c)}
    {get_nail_svg(215, 105, 23, 17, 'square', 0, c)}
    {get_nail_svg(281, 82, 25, 18, 'square', 0, c)}
    {get_nail_svg(345, 118, 22, 16, 'square', 0, c)}

    <!-- Square Knuckles -->
    <g fill="{c}" opacity="0.75">
      <rect x="145" y="235" width="22" height="7" rx="3.5"/>
      <rect x="202" y="228" width="26" height="7" rx="3.5"/>
      <rect x="268" y="222" width="28" height="7" rx="3.5"/>
      <rect x="330" y="232" width="26" height="7" rx="3.5"/>
    </g>
  </g>

  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    <rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>
    <text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>
    <text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">Square Block Profile</text>
    <rect x="50" y="32" width="14" height="75" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>
    <rect x="46" y="28" width="22" height="12" rx="2" fill="{c}" fill-opacity="0.5"/>
    <line x1="28" y1="68" x2="48" y2="68" stroke="{c}" stroke-width="1.2"/>
    <text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Right</text>
    <text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Angles</text>
  </g>

  <!-- LAYER 8: UNCLIPPED CALLOUT BADGES -->
  {get_callout_badge(154, 142, -15, 140, "Square Nails", "Broad durable beds", c, "end")}
  {get_callout_badge(281, 82, -15, 60, "Right-Angled Apex", "Built upon the square", c, "end")}
  {get_callout_badge(430, 246, 485, 240, "Square Upward Thumb", "Powerful 35° opposition", c, "start")}
  {get_callout_badge(155, 420, -15, 420, "Right-Angled Wrist", "Runs straight down", c, "end")}
</svg>'''

# ==========================================
# 4. THE OSSEOUS HAND (Full Multi-Layer)
# ==========================================
def get_osseous_full_svg():
    c = "#10b981"
    return f'''<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="ossGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadowOss" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- LAYER 1: MASS SILHOUETTE -->
  <g class="layer-mass">
    <rect x="130" y="65" width="245" height="340" rx="4" fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.4"/>
    <text x="245" y="38" text-anchor="middle" fill="{c}" font-family="monospace" font-size="11" letter-spacing="1">GEOMETRIC ARCHETYPE: OBLONG / RECTANGLE</text>
    <circle cx="245" cy="275" r="140" fill="url(#ossGlow)"/>
  </g>

  <!-- LAYER 2: UNDERLYING PRIMITIVES (Oblong Cylinders & Knotted Hinges) -->
  <g class="layer-primitives" style="display: none;" stroke="{c}" stroke-width="1.2" fill="{c}" fill-opacity="0.08" stroke-dasharray="3 3">
    <rect x="160" y="240" width="150" height="170"/>
    <circle cx="160" cy="180" r="12"/>
    <circle cx="160" cy="130" r="10"/>
    <circle cx="215" cy="160" r="14"/>
    <circle cx="215" cy="110" r="12"/>
    <circle cx="275" cy="140" r="15"/>
    <circle cx="275" cy="90" r="13"/>
    <circle cx="335" cy="160" r="14"/>
    <circle cx="335" cy="115" r="12"/>
    <!-- Thumb Knuckle Knot & Cylinders -->
    <circle cx="430" cy="315" r="16"/>
    <circle cx="415" cy="245" r="13"/>
  </g>

  <!-- LAYER 3: RATIO & DIMENSION CALIPERS -->
  {get_ratio_caliper_svg(140, 65, 235, "Digit III", "L = 170px", c, -50)}
  {get_ratio_caliper_svg(140, 235, 450, "Palm Height", "H = 215px", c, -50)}
  <g class="layer-ratios caliper-guide" style="display: none;">
    <line x1="160" y1="450" x2="298" y2="450" stroke="{c}" stroke-width="1.5"/>
    <rect x="200" y="458" width="80" height="20" rx="3" fill="#090d16" stroke="{c}" stroke-width="1"/>
    <text x="240" y="472" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9">Wrist: 138px (0.85:1)</text>
    <rect x="420" y="190" width="135" height="32" rx="4" fill="#090d16" stroke="{c}" stroke-width="1.2"/>
    <text x="487" y="204" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">PALM : FINGER RATIO</text>
    <text x="487" y="216" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">1.00 : 1.08 (Elongated)</text>
  </g>

  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  {get_sloan_grid_svg()}

  <!-- LAYER 5: MAIN HAND CONTOUR (Anatomical Left Hand Dorsal with Upward Knotty Thumb) -->
  <g class="layer-contour">
    <path d="M 160 450
             C 145 442, 138 435, 146 418
             C 150 385, 142 335, 148 275
             C 138 250, 134 215, 142 188
             C 136 172, 136 155, 146 132
             C 156 118, 172 118, 180 132
             C 188 155, 184 172, 178 188
             C 186 215, 180 250, 186 270
             C 192 245, 186 195, 196 162
             C 188 144, 185 120, 198 96
             C 208 80, 228 80, 238 96
             C 250 120, 246 144, 238 162
             C 248 195, 242 245, 246 268
             C 252 235, 246 185, 258 145
             C 250 128, 248 98, 262 72
             C 272 58, 294 58, 304 72
             C 316 98, 314 128, 306 145
             C 316 185, 310 235, 314 268
             C 320 240, 316 200, 326 170
             C 320 152, 318 132, 330 110
             C 340 96, 358 98, 366 112
             C 374 132, 370 152, 362 170
             C 370 200, 364 240, 358 272
             C 352 288, 364 298, 378 288
             C 390 276, 404 256, 416 240
             C 426 226, 440 234, 436 250
             C 430 275, 442 308, 432 328
             C 420 348, 402 370, 375 395
             C 352 418, 330 435, 298 450
             Z"
          fill="#1e293b" stroke="{c}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round" filter="url(#shadowOss)"/>
  </g>

  <!-- LAYER 6: DETAILS (Knotty Joints, Oblong Nails, Upward Thumb Knot) -->
  <g class="layer-details">
    <path d="M 370 335 C 390 305, 405 275, 418 248" fill="none" stroke="{c}" stroke-width="2" opacity="0.6"/>
    <circle cx="430" cy="315" r="7" fill="{c}" opacity="0.5"/>
    {get_nail_svg(424, 242, 16, 20, 'oblong', 35, c)}

    <!-- Oblong Nails (Pinky, Ring, Middle, Index) -->
    {get_nail_svg(162, 126, 13, 16, 'oblong', 0, c)}
    {get_nail_svg(218, 90, 16, 19, 'oblong', 0, c)}
    {get_nail_svg(283, 66, 17, 21, 'oblong', 0, c)}
    {get_nail_svg(348, 104, 15, 18, 'oblong', 0, c)}

    <!-- Bulging Interphalangeal Knots -->
    <g fill="{c}">
      <ellipse cx="160" cy="142" rx="10" ry="5.5" opacity="0.5"/>
      <ellipse cx="216" cy="108" rx="12" ry="6" opacity="0.5"/>
      <ellipse cx="282" cy="82" rx="13" ry="6.5" opacity="0.5"/>
      <ellipse cx="346" cy="120" rx="11" ry="5.5" opacity="0.5"/>
      <ellipse cx="160" cy="195" rx="12" ry="7" opacity="0.6"/>
      <ellipse cx="216" cy="170" rx="13" ry="7.5" opacity="0.6"/>
      <ellipse cx="282" cy="150" rx="14" ry="8" opacity="0.6"/>
      <ellipse cx="346" cy="178" rx="13" ry="7.5" opacity="0.6"/>
    </g>
  </g>

  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    <rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>
    <text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>
    <text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">Knotty Joint Profile</text>
    <rect x="52" y="32" width="10" height="75" rx="2" fill="#64748b" opacity="0.6"/>
    <path d="M 44 32 C 32 45, 30 55, 40 68 C 30 80, 32 90, 44 105 L 70 105 C 82 90, 84 80, 74 68 C 84 55, 82 45, 70 32 Z"
          fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>
    <ellipse cx="57" cy="68" rx="18" ry="7" fill="{c}" opacity="0.4"/>
    <line x1="26" y1="68" x2="40" y2="68" stroke="{c}" stroke-width="1.2"/>
    <text x="23" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Bulging</text>
    <text x="23" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Knots</text>
  </g>

  <!-- LAYER 8: UNCLIPPED CALLOUT BADGES -->
  {get_callout_badge(282, 82, -15, 60, "Knotty Knuckles", "Joints = widest points", c, "end")}
  {get_callout_badge(162, 126, -15, 120, "Oblong Nails", "Flat gnarled beds", c, "end")}
  {get_callout_badge(424, 242, 485, 235, "Knotty Upward Thumb", "Bulging MCP joint knot", c, "start")}
  {get_callout_badge(146, 418, -15, 410, "Styloid Process", "Prominent head of ulna", c, "end")}
</svg>'''

# ==========================================
# 5. THE CEREBRAL HAND (Full Multi-Layer)
# ==========================================
def get_cerebral_full_svg():
    c = "#8b5cf6"
    return f'''<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="cerGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{c}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{c}" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadowCer" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <filter id="badgeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>

  <!-- LAYER 1: MASS SILHOUETTE -->
  <g class="layer-mass">
    <polygon points="120,70 360,70 235,445" fill="none" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 6" opacity="0.4"/>
    <text x="240" y="38" text-anchor="middle" fill="{c}" font-family="monospace" font-size="11" letter-spacing="1">GEOMETRIC ARCHETYPE: INVERTED TRIANGLE</text>
    <circle cx="235" cy="275" r="130" fill="url(#cerGlow)"/>
  </g>

  <!-- LAYER 2: UNDERLYING PRIMITIVES (Inverted Triangular Wedge & Uniform Cylinders) -->
  <g class="layer-primitives" style="display: none;" stroke="{c}" stroke-width="1.2" fill="{c}" fill-opacity="0.08" stroke-dasharray="3 3">
    <polygon points="174,255 296,255 275,445 195,445"/>
    <rect x="166" y="140" width="16" height="115" rx="3"/>
    <rect x="198" y="100" width="18" height="155" rx="3"/>
    <rect x="232" y="75" width="18" height="180" rx="3"/>
    <rect x="266" y="110" width="16" height="145" rx="3"/>
    <!-- Upward Slender Thumb Cylinder -->
    <rect x="330" y="280" width="14" height="85" rx="3" transform="rotate(-32, 340, 310)"/>
  </g>

  <!-- LAYER 3: RATIO & DIMENSION CALIPERS -->
  {get_ratio_caliper_svg(150, 75, 255, "Digit III", "L = 180px", c, -50)}
  {get_ratio_caliper_svg(150, 255, 445, "Palm Height", "H = 190px", c, -50)}
  <g class="layer-ratios caliper-guide" style="display: none;">
    <line x1="195" y1="445" x2="275" y2="445" stroke="{c}" stroke-width="1.5"/>
    <rect x="200" y="455" width="80" height="20" rx="3" fill="#090d16" stroke="{c}" stroke-width="1"/>
    <text x="235" y="469" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9">Wrist: 80px (0.60:1)</text>
    <rect x="420" y="190" width="135" height="32" rx="4" fill="#090d16" stroke="{c}" stroke-width="1.2"/>
    <text x="487" y="204" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">PALM : FINGER RATIO</text>
    <text x="487" y="216" text-anchor="middle" fill="#cbd5e1" font-family="monospace" font-size="9">1.00 : 1.25 (Longest Reach)</text>
  </g>

  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  {get_sloan_grid_svg()}

  <!-- LAYER 5: MAIN HAND CONTOUR (Anatomical Left Hand Dorsal with Upward Slender Thumb) -->
  <g class="layer-contour">
    <path d="M 195 445
             C 192 385, 178 335, 174 278
             C 170 240, 160 195, 164 142
             C 166 122, 182 122, 184 142
             L 184 255
             L 196 255
             L 196 102
             C 198 82, 216 82, 218 102
             L 218 255
             L 230 255
             L 230 78
             C 232 58, 250 58, 252 78
             L 252 255
             L 264 255
             L 264 112
             C 266 92, 282 92, 284 112
             L 284 255
             L 296 255
             L 296 148
             C 298 130, 312 130, 314 148
             C 316 200, 308 258, 304 278
             C 300 295, 312 305, 326 295
             C 338 285, 354 265, 368 248
             C 376 236, 390 242, 386 256
             C 380 278, 378 318, 366 348
             C 348 382, 315 418, 275 445
             Z"
          fill="#1e293b" stroke="{c}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round" filter="url(#shadowCer)"/>
  </g>

  <!-- LAYER 6: DETAILS (Filbert Nails, Parallel Line Guides, Slender Upward Thumb) -->
  <g class="layer-details">
    <path d="M 330 330 C 348 300, 362 272, 374 248" fill="none" stroke="{c}" stroke-width="1.4" opacity="0.6"/>
    {get_nail_svg(376, 248, 12, 18, 'cerebral', 32, c)}

    <!-- Slender Filbert Nails (Pinky, Ring, Middle, Index) -->
    {get_nail_svg(174, 132, 10, 16, 'cerebral', 0, c)}
    {get_nail_svg(207, 92, 12, 18, 'cerebral', 0, c)}
    {get_nail_svg(241, 68, 12, 20, 'cerebral', 0, c)}
    {get_nail_svg(274, 102, 11, 17, 'cerebral', 0, c)}

    <!-- Parallel Straight Line Guides -->
    <line x1="164" y1="140" x2="164" y2="255" stroke="{c}" stroke-width="1.2" stroke-dasharray="2 2" opacity="0.75"/>
    <line x1="184" y1="140" x2="184" y2="255" stroke="{c}" stroke-width="1.2" stroke-dasharray="2 2" opacity="0.75"/>
  </g>

  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    <rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>
    <text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>
    <text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"Smooth Finger" Profile</text>
    <rect x="50" y="32" width="14" height="75" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>
    <ellipse cx="57" cy="30" rx="5" ry="4" fill="{c}" fill-opacity="0.5"/>
    <line x1="28" y1="68" x2="48" y2="68" stroke="{c}" stroke-width="1.2"/>
    <text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Straight</text>
    <text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Edges</text>
  </g>

  <!-- LAYER 8: UNCLIPPED CALLOUT BADGES -->
  {get_callout_badge(174, 132, -15, 130, "Smooth Fingers", "Straight parallel outlines", c, "end")}
  {get_callout_badge(241, 68, -15, 60, "Frail & Slender", "Zero knots, zero fat puff", c, "end")}
  {get_callout_badge(376, 248, 485, 240, "Slender Upward Thumb", "Delicate 32° reach", c, "start")}
  {get_callout_badge(275, 435, 485, 430, "Narrow Base", "Delicate frail wrist", c, "start")}
</svg>'''

# ==========================================
# MULTI-PERSPECTIVE GENERATORS (Palmar, Lateral, 3/4) via Procedural 3D Kinematic Engine
# ==========================================
def get_perspective_svg(hand_key, perspective):
    """Generates Palmar, Lateral, or 3/4 Perspective SVGs with full 8-layer telemetry using HandSVGDirector."""
    from hand_3d_engine import HandSVGDirector
    director = HandSVGDirector(hand_key)
    return director.generate_svg(perspective)


# ==========================================
# DIAGNOSTIC COMPARISONS (Self-Contained)
# ==========================================
def get_joint_diagnostic_comparison():
    return '''<svg viewBox="0 0 900 360" class="diagnostic-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="diagGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#334155" stroke-width="0.5" opacity="0.3"/>
    </pattern>
  </defs>
  <rect width="900" height="360" fill="#0f172a"/>
  <rect width="900" height="360" fill="url(#diagGrid)"/>

  <line x1="40" y1="120" x2="860" y2="120" stroke="#475569" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="865" y="124" fill="#94a3b8" font-family="monospace" font-size="10">DIP Joint</text>
  <line x1="40" y1="200" x2="860" y2="200" stroke="#475569" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="865" y="204" fill="#94a3b8" font-family="monospace" font-size="10">PIP Joint</text>
  <line x1="40" y1="280" x2="860" y2="280" stroke="#475569" stroke-width="1" stroke-dasharray="4 4"/>
  <text x="865" y="284" fill="#94a3b8" font-family="monospace" font-size="10">MCP Joint</text>

  <!-- 1. Alimentive -->
  <g transform="translate(100, 0)">
    <text x="0" y="35" text-anchor="middle" fill="#f59e0b" font-family="system-ui" font-size="14" font-weight="bold">1. ALIMENTIVE</text>
    <text x="0" y="52" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="11">Puffy / Narrow Joints</text>
    <path d="M -18 300 C -24 280, -32 240, -18 200 C -30 160, -26 130, -14 120 C -20 100, -12 70, 0 65 C 12 70, 20 100, 14 120 C 26 130, 30 160, 18 200 C 32 240, 24 280, 18 300 Z"
          fill="#1e293b" stroke="#f59e0b" stroke-width="3"/>
    <text x="0" y="325" text-anchor="middle" fill="#f59e0b" font-size="11" font-weight="bold">Joints = Narrowest</text>
    <text x="0" y="340" text-anchor="middle" fill="#94a3b8" font-size="10">Flesh puffs outward</text>
  </g>

  <!-- 2. Thoracic -->
  <g transform="translate(270, 0)">
    <text x="0" y="35" text-anchor="middle" fill="#ec4899" font-family="system-ui" font-size="14" font-weight="bold">2. THORACIC</text>
    <text x="0" y="52" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="11">Pointed Wedge Cone</text>
    <path d="M -18 300 L -15 200 L -12 120 L 0 45 L 12 120 L 15 200 L 18 300 Z"
          fill="#1e293b" stroke="#ec4899" stroke-width="3"/>
    <ellipse cx="0" cy="65" rx="5" ry="10" fill="#ec4899" opacity="0.4"/>
    <text x="0" y="325" text-anchor="middle" fill="#ec4899" font-size="11" font-weight="bold">Tapering Arrow</text>
    <text x="0" y="340" text-anchor="middle" fill="#94a3b8" font-size="10">Longest middle digit</text>
  </g>

  <!-- 3. Muscular -->
  <g transform="translate(450, 0)">
    <text x="0" y="35" text-anchor="middle" fill="#06b6d4" font-family="system-ui" font-size="14" font-weight="bold">3. MUSCULAR</text>
    <text x="0" y="52" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="11">Spatulate Paddle Flare</text>
    <path d="M -16 300 L -16 200 L -17 120 C -20 100, -25 75, -20 60 L 20 60 C 25 75, 20 100, 17 120 L 16 200 L 16 300 Z"
          fill="#1e293b" stroke="#06b6d4" stroke-width="3"/>
    <rect x="-14" y="68" width="28" height="18" rx="2" fill="#06b6d4" opacity="0.4" stroke="#06b6d4" stroke-width="1.5"/>
    <text x="0" y="325" text-anchor="middle" fill="#06b6d4" font-size="11" font-weight="bold">Spatulate Flare</text>
    <text x="0" y="340" text-anchor="middle" fill="#94a3b8" font-size="10">Broad paddle tips</text>
  </g>

  <!-- 4. Osseous -->
  <g transform="translate(630, 0)">
    <text x="0" y="35" text-anchor="middle" fill="#10b981" font-family="system-ui" font-size="14" font-weight="bold">4. OSSEOUS</text>
    <text x="0" y="52" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="11">Knotty Nodes / Sunken</text>
    <path d="M -16 300 C -25 280, -24 275, -12 240 C -26 200, -24 195, -10 160 C -22 120, -20 115, -12 75 L 12 75 C 20 115, 22 120, 10 160 C 24 195, 26 200, 12 240 C 24 275, 25 280, 16 300 Z"
          fill="#1e293b" stroke="#10b981" stroke-width="3"/>
    <ellipse cx="0" cy="120" rx="18" ry="6" fill="#10b981" opacity="0.4"/>
    <ellipse cx="0" cy="200" rx="20" ry="7" fill="#10b981" opacity="0.5"/>
    <ellipse cx="0" cy="280" rx="22" ry="8" fill="#10b981" opacity="0.6"/>
    <text x="0" y="325" text-anchor="middle" fill="#10b981" font-size="11" font-weight="bold">Joints = Widest</text>
    <text x="0" y="340" text-anchor="middle" fill="#94a3b8" font-size="10">Sunken inter-joint gaps</text>
  </g>

  <!-- 5. Cerebral -->
  <g transform="translate(800, 0)">
    <text x="0" y="35" text-anchor="middle" fill="#8b5cf6" font-family="system-ui" font-size="14" font-weight="bold">5. CEREBRAL</text>
    <text x="0" y="52" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="11">"Smooth Fingers"</text>
    <path d="M -12 300 L -12 200 L -12 120 C -12 75, -10 65, 0 60 C 10 65, 12 75, 12 120 L 12 200 L 12 300 Z"
          fill="#1e293b" stroke="#8b5cf6" stroke-width="2.8"/>
    <line x1="-15" y1="70" x2="-15" y2="300" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
    <line x1="15" y1="70" x2="15" y2="300" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="3 3" opacity="0.6"/>
    <text x="0" y="325" text-anchor="middle" fill="#8b5cf6" font-size="11" font-weight="bold">Smooth Parallel Lines</text>
    <text x="0" y="340" text-anchor="middle" fill="#94a3b8" font-size="10">No bulges, pads, or knots</text>
  </g>
</svg>'''

def get_sloan_acuity_comparison():
    return '''<svg viewBox="0 0 900 320" class="sloan-vector-svg" xmlns="http://www.w3.org/2000/svg">
  <rect width="900" height="320" fill="#090d16"/>
  <defs>
    <pattern id="sloanGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    </pattern>
  </defs>
  <rect width="900" height="320" fill="url(#sloanGrid)"/>

  <text x="450" y="30" text-anchor="middle" fill="#38bdf8" font-family="system-ui" font-size="13" font-weight="bold" letter-spacing="1">
    LOUISE SLOAN 5:1 OPTOTYPE ASL TEST: MANUAL LETTER 'A' (FIST + THUMB UPRIGHT)
  </text>
  <text x="450" y="48" text-anchor="middle" fill="#64748b" font-family="system-ui" font-size="11">
    How morphological variation alters optical counter-spaces and stroke disambiguation in clinical environments
  </text>

  <!-- Alimentive 'A' -->
  <g transform="translate(90, 60)">
    <rect x="-60" y="0" width="120" height="200" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>
    <path d="M -30 180 C -45 130, -45 90, -25 70 C -15 60, 25 60, 35 75 C 45 90, 45 140, 30 180 Z" fill="#1e293b" stroke="#f59e0b" stroke-width="3"/>
    <path d="M -30 150 C -45 140, -48 100, -35 80 C -25 65, -15 75, -20 110 Z" fill="#0f172a" stroke="#f59e0b" stroke-width="2.8"/>
    <circle cx="-5" cy="100" r="2.5" fill="#f59e0b"/>
    <circle cx="10" cy="98" r="2.5" fill="#f59e0b"/>
    <circle cx="25" cy="102" r="2.5" fill="#f59e0b"/>
    <text x="0" y="225" text-anchor="middle" fill="#f59e0b" font-weight="bold" font-size="12">Alimentive 'A'</text>
    <text x="0" y="240" text-anchor="middle" fill="#94a3b8" font-size="10">High occlusion risk;</text>
    <text x="0" y="252" text-anchor="middle" fill="#94a3b8" font-size="10">Needs 1-unit air gap</text>
  </g>

  <!-- Thoracic 'A' -->
  <g transform="translate(270, 60)">
    <rect x="-60" y="0" width="120" height="200" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>
    <path d="M -25 180 C -35 130, -35 80, -15 65 C -5 55, 15 55, 25 70 C 35 85, 35 130, 25 180 Z" fill="#1e293b" stroke="#ec4899" stroke-width="3"/>
    <path d="M -25 150 C -38 135, -40 85, -28 60 C -20 48, -10 55, -15 100 Z" fill="#0f172a" stroke="#ec4899" stroke-width="2.8"/>
    <ellipse cx="0" cy="90" rx="4" ry="2" fill="#ec4899" opacity="0.7"/>
    <text x="0" y="225" text-anchor="middle" fill="#ec4899" font-weight="bold" font-size="12">Thoracic 'A'</text>
    <text x="0" y="240" text-anchor="middle" fill="#94a3b8" font-size="10">High vertical reach;</text>
    <text x="0" y="252" text-anchor="middle" fill="#94a3b8" font-size="10">Sharp silhouette apex</text>
  </g>

  <!-- Muscular 'A' -->
  <g transform="translate(450, 60)">
    <rect x="-60" y="0" width="120" height="200" rx="8" fill="#1e293b" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>
    <path d="M -30 180 L -30 85 C -30 75, -20 70, 0 70 C 20 70, 30 75, 30 85 L 30 180 Z" fill="#1e293b" stroke="#06b6d4" stroke-width="3.5"/>
    <path d="M -30 160 C -45 150, -48 100, -36 75 C -28 60, -14 65, -18 115 Z" fill="#0f172a" stroke="#06b6d4" stroke-width="3"/>
    <rect x="-18" y="90" width="36" height="5" rx="2" fill="#06b6d4" opacity="0.7"/>
    <text x="0" y="225" text-anchor="middle" fill="#06b6d4" font-weight="bold" font-size="12">Muscular 'A'</text>
    <text x="0" y="240" text-anchor="middle" fill="#94a3b8" font-size="10">High mass volume;</text>
    <text x="0" y="252" text-anchor="middle" fill="#94a3b8" font-size="10">Clear square angles</text>
  </g>

  <!-- Osseous 'A' -->
  <g transform="translate(630, 60)">
    <rect x="-60" y="0" width="120" height="200" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>
    <path d="M -26 180 C -34 135, -34 85, -20 70 C -12 60, 18 60, 26 72 C 34 85, 32 135, 26 180 Z" fill="#1e293b" stroke="#10b981" stroke-width="3.2"/>
    <path d="M -26 150 C -42 138, -44 95, -32 72 C -22 55, -12 65, -16 110 Z" fill="#0f172a" stroke="#10b981" stroke-width="2.8"/>
    <circle cx="-32" cy="72" r="3" fill="#10b981"/>
    <ellipse cx="-4" cy="95" rx="6" ry="3" fill="#10b981" opacity="0.7"/>
    <ellipse cx="12" cy="95" rx="6" ry="3" fill="#10b981" opacity="0.7"/>
    <text x="0" y="225" text-anchor="middle" fill="#10b981" font-weight="bold" font-size="12">Osseous 'A'</text>
    <text x="0" y="240" text-anchor="middle" fill="#94a3b8" font-size="10">High joint definition;</text>
    <text x="0" y="252" text-anchor="middle" fill="#94a3b8" font-size="10">Natural knotty air gaps</text>
  </g>

  <!-- Cerebral 'A' -->
  <g transform="translate(810, 60)">
    <rect x="-60" y="0" width="120" height="200" rx="8" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>
    <path d="M -22 180 C -28 135, -28 85, -16 70 C -8 60, 14 60, 20 72 C 28 85, 26 135, 20 180 Z" fill="#1e293b" stroke="#8b5cf6" stroke-width="2.8"/>
    <path d="M -22 150 C -34 138, -36 95, -26 72 C -18 55, -10 65, -14 110 Z" fill="#0f172a" stroke="#8b5cf6" stroke-width="2.5"/>
    <line x1="-15" y1="75" x2="-15" y2="180" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="2 2" opacity="0.6"/>
    <text x="0" y="225" text-anchor="middle" fill="#8b5cf6" font-weight="bold" font-size="12">Cerebral 'A'</text>
    <text x="0" y="240" text-anchor="middle" fill="#94a3b8" font-size="10">Delicate, long lever;</text>
    <text x="0" y="252" text-anchor="middle" fill="#94a3b8" font-size="10">High resolution need</text>
  </g>
</svg>'''

# ==========================================
# MAIN EXPORT ENGINE
# ==========================================
def main():
    root_dir = r'C:\Users\philg\Pocketgull\pocketgull-typeface'
    js_dir = os.path.join(root_dir, 'js')
    assets_dir = os.path.join(root_dir, 'assets', 'hand_types')
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    hand_types_data = {
        "alimentive": {
            "name": "The Alimentive Type",
            "subtitle": "The Circular / Plump Hand",
            "historicalChart": "Chart 2 (Page 40)",
            "dominantSystem": "Digestive & Alimentary System",
            "geometricArchetype": "Circle",
            "color": "#f59e0b",
            "ratios": {
                "fingerToPalm": "1 : 0.78 (Short Fingers)",
                "wristToKnuckle": "0.92 : 1.00 (Fleshy Wrist)",
                "archetypePrimitive": "Stacked Spheres & Rounded Masses"
            },
            "keyDiagnoses": [
                "Modeled upon the circle: round hands, round fingers, round wrists.",
                "Dimples where knuckles are supposed to be; fat cushions replace bone projections.",
                "Fingers puff out between joints — the joints mark the narrowest spots.",
                "Short, baby-like, fleshy fingers with small rounded nail plates and multiple wrist creases."
            ],
            "bookQuote": "Because his bones are small the pure Alimentive has small feet and small hands... The entire physical makeup of this type is modeled upon the circle—round hands with dimples where the knuckles are supposed to be; round fingers... puff out between the joints. (Chart 2)",
            "hciImplication": "High contour occlusion. In optical hand tracking (MediaPipe) and Louise Sloan 5:1 optotype rendering, the fatty tissues can obscure finger gaps. Requires exaggerated 1-stroke-width counter-spaces to keep finger counts distinguishable.",
            "dorsalSvg": get_alimentive_full_svg(),
            "palmarSvg": get_perspective_svg('alimentive', 'palmar'),
            "lateralSvg": get_perspective_svg('alimentive', 'lateral'),
            "threeQuarterSvg": get_perspective_svg('alimentive', 'threeQuarter')
        },
        "thoracic": {
            "name": "The Thoracic Type",
            "subtitle": "The Pointed / Oval Hand",
            "historicalChart": "Chart 4 (Page 88)",
            "dominantSystem": "Circulatory & Respiratory Systems",
            "geometricArchetype": "Wedge / Conical Taper",
            "color": "#ec4899",
            "ratios": {
                "fingerToPalm": "1 : 1.18 (Conspicuously Long Middle)",
                "wristToKnuckle": "0.72 : 1.00 (Steep Wedge Taper)",
                "archetypePrimitive": "Converging Conical Wedges"
            },
            "keyDiagnoses": [
                "Pointed effect when fingers are laid together; wedge/arrowhead contour.",
                "Extreme length of the second (middle) finger conspicuously dominates.",
                "Thin-skinned with high vascularity; naturally more pink than average.",
                "Conical / almond-shaped nail plates on slender, graceful, tapering digits."
            ],
            "bookQuote": "The pointed hand is the hand of the pure Thoracic. (See Chart 4) Note the extreme length of the second finger and the pointed effect of this hand when all the fingers are laid together... The fingers of the Thoracic are also inclined to be more thin-skinned... naturally more pink than the average.",
            "hciImplication": "Strong directional pointing trajectories. The prominent middle finger alters vertical center-of-mass; telemetry bounding boxes must adjust vertical margins so numerals (e.g. 3, 6, W) don't collide with upper bounds.",
            "dorsalSvg": get_thoracic_full_svg(),
            "palmarSvg": get_perspective_svg('thoracic', 'palmar'),
            "lateralSvg": get_perspective_svg('thoracic', 'lateral'),
            "threeQuarterSvg": get_perspective_svg('thoracic', 'threeQuarter')
        },
        "muscular": {
            "name": "The Muscular Type",
            "subtitle": "The Square / Spatulate Hand",
            "historicalChart": "Chart 6 (Page 142)",
            "dominantSystem": "Muscular & Motor System",
            "geometricArchetype": "Square / Right Angles",
            "color": "#06b6d4",
            "ratios": {
                "fingerToPalm": "1 : 1.00 (Perfect Square Balance)",
                "wristToKnuckle": "1.02 : 1.00 (Right-Angled Block)",
                "archetypePrimitive": "1:1 Square Blocks & Spatulate Cylinders"
            },
            "keyDiagnoses": [
                "Built in a series of squares; runs out from the wrist at right angles.",
                "Spatulate finger ends: tips broaden outward into paddle shapes with muscular pads.",
                "Broad square nail beds with flat horizontal free edges; powerful grip.",
                "The classic 'Hand of the Creative Craftsman, Builder, Pianist & Sculptor'."
            ],
            "bookQuote": "The hand of the Muscular, like all the rest of his body, is built in a series of squares. It runs out from the wrist and down in a straighter line and tends to right angles. (See Chart 6)... Every hand artist will be found to have spatulate-fingered hands—in short, muscular hands.",
            "hciImplication": "Maximum silhouette mass and robust optical presence. The spatulate paddle tips provide wide contact zones for tactile interfaces and high-contrast broadside legibility in emergency sign telemetry.",
            "dorsalSvg": get_muscular_full_svg(),
            "palmarSvg": get_perspective_svg('muscular', 'palmar'),
            "lateralSvg": get_perspective_svg('muscular', 'lateral'),
            "threeQuarterSvg": get_perspective_svg('muscular', 'threeQuarter')
        },
        "osseous": {
            "name": "The Osseous Type",
            "subtitle": "The Oblong / Knotty Hand",
            "historicalChart": "Chart 8 (Page 184)",
            "dominantSystem": "Skeletal & Framework System",
            "geometricArchetype": "Oblong / Rectangle",
            "color": "#10b981",
            "ratios": {
                "fingerToPalm": "1 : 1.08 (Elongated Oblong)",
                "wristToKnuckle": "0.85 : 1.00 (Straight Sides & Styloid Head)",
                "archetypePrimitive": "Oblong Cylinders & Articulated Hinges"
            },
            "keyDiagnoses": [
                "Outlines approximate the oblong; sides run straight down instead of tapering.",
                "Knotty fingers: joints mark the widest spots, and spaces between joints are sunken.",
                "Bony, angular, large-jointed, with knobby thumb joint and flat oblong nails.",
                "Stiff, inflexible grip; built for stoical pioneering and physical endurance."
            ],
            "bookQuote": "'The gnarled hand' well describes that of the Osseous. The hand outlines of this type also approximate the oblong. (See Chart 8)... In the Osseous fingers the joints mark the widest spots and the spaces between are sunken.",
            "hciImplication": "High joint visibility. The prominent knuckle knots create natural negative air gaps between fingers even when loosely closed, enabling computer vision models to accurately separate digit counts without false-positive contact errors.",
            "dorsalSvg": get_osseous_full_svg(),
            "palmarSvg": get_perspective_svg('osseous', 'palmar'),
            "lateralSvg": get_perspective_svg('osseous', 'lateral'),
            "threeQuarterSvg": get_perspective_svg('osseous', 'threeQuarter')
        },
        "cerebral": {
            "name": "The Cerebral Type",
            "subtitle": "The Triangular / Smooth Hand",
            "historicalChart": "Chart 10 (Page 228)",
            "dominantSystem": "Nervous & Cerebral System",
            "geometricArchetype": "Inverted Triangle",
            "color": "#8b5cf6",
            "ratios": {
                "fingerToPalm": "1 : 1.25 (Longest Slender Reach)",
                "wristToKnuckle": "0.60 : 1.00 (Whisper-Thin Taper)",
                "archetypePrimitive": "Inverted Triangular Wedge & Uniform Cylinders"
            },
            "keyDiagnoses": [
                "Frail, delicate, aesthetic appearance; narrow palm tapering from slender wrist.",
                "'Smooth fingers': finger outlines run straight up and down in unbroken parallel lines.",
                "Elongated oval/filbert nails with slender long thumb; zero knots or bulges.",
                "Highly sensitive nervous organization; the hand of meditation and abstract reflection."
            ],
            "bookQuote": "A thin, delicate hand denotes a larger-than-average Cerebral element. (See Chart 10)... Smooth fingers are characteristic of the extreme Cerebral type. They are called this because their outlines run straight up and down... presenting a more frail, aesthetic appearance.",
            "hciImplication": "Razor-sharp angular contours with long lever arms. Highly legible for crossed or intricate fingerspelling (R, X, K), but slender lines require high-contrast rendering under dim or noisy illumination to prevent threshold dropout.",
            "dorsalSvg": get_cerebral_full_svg(),
            "palmarSvg": get_perspective_svg('cerebral', 'palmar'),
            "lateralSvg": get_perspective_svg('cerebral', 'lateral'),
            "threeQuarterSvg": get_perspective_svg('cerebral', 'threeQuarter')
        }
    }

    js_content = "/**\n * Five Human Hand Types Studio Dataset (V3 - Advanced Multi-Perspective & Layered Telemetry)\n * Based on Elsie Lincoln Benedict & Ralph Paine Benedict (1921)\n * Illustrated by Raymond H. Lufkin (The Roycrofters)\n */\n\n"
    js_content += f"window.FIVE_HAND_TYPES = {json.dumps(hand_types_data, indent=2)};\n\n"
    js_content += f"window.BENEDICT_JOINT_DIAGNOSTIC_SVG = `{get_joint_diagnostic_comparison()}`;\n\n"
    js_content += f"window.SLOAN_5_1_ACUITY_SVG = `{get_sloan_acuity_comparison()}`;\n"

    js_file = os.path.join(js_dir, 'five_hand_types_data.js')
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Written: {js_file}")

    for key, data in hand_types_data.items():
        svg_file = os.path.join(assets_dir, f"{key}_dorsal.svg")
        with open(svg_file, 'w', encoding='utf-8') as f:
            f.write(data['dorsalSvg'])
        print(f"Written: {svg_file}")

    print("[SUCCESS] All 5 Hand Types generated with authentic upward-sloped thumbs (35°-40°)!")

if __name__ == '__main__':
    main()
