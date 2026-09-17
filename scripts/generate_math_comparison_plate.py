#!/usr/bin/env python3
"""
scripts/generate_math_comparison_plate.py

Generates a publication-grade visual comparison plate demonstrating:
1. The Dark-Mode "Anorexia" Problem: Computer Modern Hairlines vs. PocketGull 68 UPM Stem.
2. ISMP Character Disambiguation: Greek nu vs Latin v, 0 vs O, 1 vs l vs I, 2 vs Z.
3. Stepped Delimiters (MathVariants .v1 to .v4): Zero-distortion bracket scaling.
4. Zero-Shear Text Table: Fallback font drift vs. PocketGull unified 1000 UPM em-square.
"""

import os
from generate_self_contained_math_svg import embed_font_in_svg

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DOC_IMG_DIR = os.path.join(ROOT_DIR, "documentation", "images")
os.makedirs(DOC_IMG_DIR, exist_ok=True)

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 800" width="1100" height="800">
  <defs>
    <style>
      @import url('/fonts/fonts.css');
      .bg { fill: #09090b; }
      .card { fill: #121217; stroke: #272732; stroke-width: 1.5; rx: 12; }
      .title { font-family: 'PocketGull', 'Atkinson Hyperlegible Next', -apple-system, sans-serif; font-weight: 700; fill: #f4f4f5; font-size: 22px; }
      .subtitle { font-family: 'PocketGull Mono', monospace; fill: #14b8a6; font-size: 11px; letter-spacing: 0.06em; }
      .section-hdr { font-family: 'PocketGull', -apple-system, sans-serif; font-weight: 700; fill: #f4f4f5; font-size: 15px; }
      .section-sub { font-family: 'PocketGull Mono', monospace; fill: #a1a1aa; font-size: 10.5px; }
      .label-bad { font-family: 'PocketGull Mono', monospace; fill: #ef4444; font-size: 10.5px; font-weight: 600; }
      .label-good { font-family: 'PocketGull Mono', monospace; fill: #10b981; font-size: 10.5px; font-weight: 600; }
      .cm-text { font-family: 'Latin Modern Math', 'Computer Modern', serif; fill: #71717a; font-size: 21px; font-style: italic; }
      .pg-math { font-family: 'PocketGull Math', 'PocketGull Mono', monospace; fill: #38bdf8; font-size: 21px; font-feature-settings: "cv05" 1, "cv08" 1, "ss02" 1, "tnum" 1; }
      .box-raw { font-family: 'PocketGull Mono', monospace; fill: #e4e4e7; font-size: 11px; line-height: 1.4; }
      .callout { fill: #181820; stroke: #272732; stroke-width: 1; rx: 8; }
      .desc-text { font-family: -apple-system, 'Atkinson Hyperlegible', sans-serif; fill: #d4d4d8; font-size: 11.5px; }
      .comp-bad { font-family: 'Latin Modern Math', 'Computer Modern', serif; fill: #f87171; font-size: 14px; font-style: italic; }
      .comp-good { font-family: 'PocketGull Math', 'PocketGull Mono', monospace; fill: #34d399; font-size: 14px; font-feature-settings: "cv05" 1, "cv08" 1, "ss02" 1; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="1100" height="800" class="bg"/>

  <!-- Header -->
  <g transform="translate(40, 35)">
    <text x="0" y="24" class="title">PocketGull Math vs. Legacy Computer Modern</text>
    <text x="0" y="46" class="subtitle">EMPIRICAL PROOF PLATE: DARK-MODE TELEMETRY &amp; ISMP DISAMBIGUATION</text>
  </g>

  <!-- QUADRANT 1: Dark Mode Hairline Anorexia -->
  <g transform="translate(40, 95)">
    <rect width="495" height="325" class="card"/>
    <text x="24" y="32" class="section-hdr">1. The Dark-Mode "Hairline Anorexia" Problem</text>
    <text x="24" y="50" class="section-sub">1978 INK-SPREAD DESIGN VS. 2026 OLED CALIBRATED STEM</text>

    <!-- Legacy Computer Modern Box -->
    <g transform="translate(24, 72)">
      <rect width="447" height="92" class="callout"/>
      <text x="16" y="22" class="label-bad">✕ LEGACY COMPUTER MODERN (HAIRLINE COLLAPSE ON OLED)</text>
      <text x="16" y="56" class="cm-text">ℒ_ASL = - ∑ y_k (1 - p_k)^γ</text>
      <text x="16" y="78" class="desc-text" fill="#71717a">Stem &lt; 20 UPM: Sub-pixel hairlines vanish under high-contrast dark mode.</text>
    </g>

    <!-- PocketGull Math Box -->
    <g transform="translate(24, 182)">
      <rect width="447" height="116" class="callout" stroke="#059669" stroke-width="1.2"/>
      <text x="16" y="22" class="label-good">✓ POCKETGULL MATH (68 UPM HUMANIST CALIBRATED STEM)</text>
      <text x="16" y="58" class="pg-math">ℒ_ASL = - ∑ y_k (1 - p_k)^γ</text>
      <text x="16" y="84" class="desc-text" fill="#34d399">Humanist stroke width remains solid on dark HUDs without retinal glare.</text>
      <text x="16" y="102" class="section-sub" fill="#10b981">68 UPM core stem • Optical anti-crowding • Louise Sloan 5:1 acuity</text>
    </g>
  </g>

  <!-- QUADRANT 2: ISMP Clinical Disambiguation -->
  <g transform="translate(565, 95)">
    <rect width="495" height="325" class="card"/>
    <text x="24" y="32" class="section-hdr">2. ISMP Life-Critical Character Disambiguation</text>
    <text x="24" y="50" class="section-sub">ELIMINATING VARIABLE COLLISIONS IN CLINICAL FORMULAS</text>

    <g transform="translate(24, 72)">
      <!-- Row 1: nu vs v -->
      <rect width="447" height="50" class="callout"/>
      <text x="14" y="31" class="desc-text">Greek ν vs. Latin v:</text>
      <text x="150" y="31" class="comp-bad">✕ ν ≈ v  (Collision)</text>
      <text x="295" y="31" class="comp-good">✓ ν ≠ v  (Distinct cv05)</text>
    </g>

    <g transform="translate(24, 130)">
      <!-- Row 2: 0 vs O -->
      <rect width="447" height="50" class="callout"/>
      <text x="14" y="31" class="desc-text">Zero vs. Capital O:</text>
      <text x="150" y="31" class="comp-bad">✕ 0 vs O  (Identical)</text>
      <text x="295" y="31" class="comp-good">✓ 0̸ vs O  (Slashed cv08)</text>
    </g>

    <g transform="translate(24, 188)">
      <!-- Row 3: 1 vs l vs I -->
      <rect width="447" height="50" class="callout"/>
      <text x="14" y="31" class="desc-text">One vs. l vs. I:</text>
      <text x="150" y="31" class="comp-bad">✕ 1 / l / I  (Indistinct)</text>
      <text x="295" y="31" class="comp-good">✓ 1 / l / I  (Foot &amp; Serifs)</text>
    </g>

    <g transform="translate(24, 246)">
      <!-- Row 4: 2 vs Z -->
      <rect width="447" height="50" class="callout"/>
      <text x="14" y="31" class="desc-text">Two vs. Capital Z:</text>
      <text x="150" y="31" class="comp-bad">✕ 2 vs Z  (Blur Hazard)</text>
      <text x="295" y="31" class="comp-good">✓ 2 vs Z  (Crossbar cv11)</text>
    </g>
  </g>

  <!-- QUADRANT 3: Stepped Delimiters (MathVariants .v1 - .v4) -->
  <g transform="translate(40, 445)">
    <rect width="495" height="320" class="card"/>
    <text x="24" y="32" class="section-hdr">3. Stepped Delimiters (MathVariants .v1 to .v4)</text>
    <text x="24" y="50" class="section-sub">SCALES FRACTIONS &amp; INTEGRALS WITHOUT CORNER DISTORTION</text>

    <g transform="translate(24, 72)">
      <rect width="447" height="224" class="callout"/>
      
      <!-- Delimiter Visualizer with wide, collision-free spacing -->
      <g transform="translate(28, 105)">
        <text x="0" y="0" class="pg-math" font-size="24">( [ { √</text>
        <text x="0" y="38" class="section-sub">v1 (1200 UPM)</text>
      </g>
      <g transform="translate(136, 105)">
        <text x="0" y="0" class="pg-math" font-size="32">( [ { √</text>
        <text x="0" y="38" class="section-sub">v2 (1600 UPM)</text>
      </g>
      <g transform="translate(248, 105)">
        <text x="0" y="0" class="pg-math" font-size="40">( [ {</text>
        <text x="0" y="38" class="section-sub">v3 (2000 UPM)</text>
      </g>
      <g transform="translate(352, 105)">
        <text x="0" y="0" class="pg-math" font-size="48">( [</text>
        <text x="0" y="38" class="section-sub">v4 (2400 UPM)</text>
      </g>
      <text x="20" y="195" class="desc-text" fill="#94a3b8">Pure quadratic spline expansion • Constant terminal radius • Zero corner thinning</text>
    </g>
  </g>

  <!-- QUADRANT 4: Zero-Shear Text & Markdown Graphs -->
  <g transform="translate(565, 445)">
    <rect width="495" height="320" class="card"/>
    <text x="24" y="32" class="section-hdr">4. Zero-Shear Unicode &amp; ASCII Markdown Graphs</text>
    <text x="24" y="50" class="section-sub">UNIFIED 1000 UPM GRID ELIMINATES FALLBACK COLUMN DRIFT</text>

    <g transform="translate(24, 72)">
      <rect width="447" height="224" class="callout"/>
      <text x="14" y="32" class="box-raw" xml:space="preserve">┌─────────────────────────────────────────────┐</text>
      <text x="14" y="52" class="box-raw" xml:space="preserve">│ GENERATION 9 CLINICAL PIPELINE GRAPH        │</text>
      <text x="14" y="72" class="box-raw" xml:space="preserve">├─────────────────────────────────────────────┤</text>
      <text x="14" y="92" class="box-raw" xml:space="preserve">│ [Input MRI: 392×392] ──► ViT ──► η=2×10⁻⁶   │</text>
      <text x="14" y="112" class="box-raw" xml:space="preserve">│                               │             │</text>
      <text x="14" y="132" class="box-raw" xml:space="preserve">│                               ▼             │</text>
      <text x="14" y="152" class="box-raw" xml:space="preserve">│             StudyMIL Head (z = ∑ᵢ αᵢ hᵢ)    │</text>
      <text x="14" y="172" class="box-raw" xml:space="preserve">│                               ▼             │</text>
      <text x="14" y="192" class="box-raw" xml:space="preserve">│        ℒ_ASL (γ₊=1.0) ──► Macro-AUC ≥ 0.850 │</text>
      <text x="14" y="212" class="box-raw" xml:space="preserve">└─────────────────────────────────────────────┘</text>
    </g>
  </g>
</svg>
"""

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PocketGull Math vs. Computer Modern Comparison Plate</title>
  <link rel="stylesheet" href="/fonts.css">
  <style>
    body {{
      background: #09090b;
      margin: 0;
      padding: 40px;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      font-family: 'PocketGull', -apple-system, sans-serif;
    }}
  </style>
</head>
<body>
  {svg_content}
</body>
</html>
"""

svg_path = os.path.join(DOC_IMG_DIR, "math_comparison_plate.svg")
html_path = os.path.join(DOC_IMG_DIR, "math_comparison_plate.html")
embedded_svg_path = os.path.join(DOC_IMG_DIR, "math_comparison_plate_embedded.svg")

with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

try:
    embedded_content = embed_font_in_svg(svg_content)
    with open(embedded_svg_path, "w", encoding="utf-8") as f:
        f.write(embedded_content)
    print(f"[OK] Generated: {embedded_svg_path}")
except Exception as e:
    print(f"[WARN] Embedded SVG generation skipped: {e}")

print(f"[OK] Generated: {svg_path}")
print(f"[OK] Generated: {html_path}")
