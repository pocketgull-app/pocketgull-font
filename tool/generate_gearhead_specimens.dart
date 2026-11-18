import 'dart:io';
import 'dart:convert';
import 'dart:math' as math;

/// Mathematically generates true AGMA 2001-D04 / ISO 53 Involute Gear SVG paths
/// and writes the complete, museum-grade HTML specimens for Gearhead Groovy.

String involuteGearPath({
  required double cx,
  required double cy,
  required double module,
  required int teeth,
  double pressureAngleDeg = 20.0,
  double rotationDeg = 0.0,
}) {
  final rp = 0.5 * module * teeth;
  final ra = rp + 1.0 * module;
  final rf = rp - 1.25 * module;
  final rb = rp * math.cos(pressureAngleDeg * math.pi / 180.0);
  final rBase = math.max(rf, rb);

  final alphaRad = pressureAngleDeg * math.pi / 180.0;
  final invAlpha = math.tan(alphaRad) - alphaRad;
  // Half tooth thickness angle at base circle
  final halfToothBase = (math.pi / (2.0 * teeth)) + invAlpha;
  final tMax = math.sqrt(math.max(0.0, (ra * ra) / (rb * rb) - 1.0));
  final rotRad = rotationDeg * math.pi / 180.0;

  final sb = StringBuffer();
  final pitchAngle = 2.0 * math.pi / teeth;

  for (int i = 0; i < teeth; i++) {
    final centerAngle = rotRad + i * pitchAngle;

    // Root start
    final aRootLeft = centerAngle - halfToothBase;
    final xRL = cx + rf * math.cos(aRootLeft);
    final yRL = cy + rf * math.sin(aRootLeft);

    if (i == 0) {
      sb.write('M ${xRL.toStringAsFixed(2)} ${yRL.toStringAsFixed(2)} ');
    } else {
      sb.write('L ${xRL.toStringAsFixed(2)} ${yRL.toStringAsFixed(2)} ');
    }

    // Left involute flank (5 samples from base to addendum)
    for (int s = 0; s <= 4; s++) {
      final t = tMax * (s / 4.0);
      final r = math.max(rf, rb * math.sqrt(1.0 + t * t));
      final inv = t - math.atan(t);
      final a = centerAngle - halfToothBase + inv;
      final px = cx + r * math.cos(a);
      final py = cy + r * math.sin(a);
      sb.write('L ${px.toStringAsFixed(2)} ${py.toStringAsFixed(2)} ');
    }

    // Right involute flank (5 samples from addendum down to base)
    for (int s = 4; s >= 0; s--) {
      final t = tMax * (s / 4.0);
      final r = math.max(rf, rb * math.sqrt(1.0 + t * t));
      final inv = t - math.atan(t);
      final a = centerAngle + halfToothBase - inv;
      final px = cx + r * math.cos(a);
      final py = cy + r * math.sin(a);
      sb.write('L ${px.toStringAsFixed(2)} ${py.toStringAsFixed(2)} ');
    }

    // Root end
    final aRootRight = centerAngle + halfToothBase;
    final xRR = cx + rf * math.cos(aRootRight);
    final yRR = cy + rf * math.sin(aRootRight);
    sb.write('L ${xRR.toStringAsFixed(2)} ${yRR.toStringAsFixed(2)} ');
  }
  sb.write('Z');
  return sb.toString();
}

/// Internal ring gear path (teeth pointing inward)
String internalRingGearPath({
  required double cx,
  required double cy,
  required double module,
  required int teeth,
  required double outerRimRadius,
  double pressureAngleDeg = 20.0,
}) {
  final rp = 0.5 * module * teeth;
  final ra = rp - 0.85 * module; // inward tip
  final rf = rp + 1.15 * module; // outward root
  final pitchAngle = 2.0 * math.pi / teeth;

  final sb = StringBuffer();
  // Outer circle CW
  sb.write('M ${(cx + outerRimRadius).toStringAsFixed(2)} ${cy.toStringAsFixed(2)} ');
  for (int i = 1; i <= 64; i++) {
    final a = i * 2.0 * math.pi / 64.0;
    sb.write('L ${(cx + outerRimRadius * math.cos(a)).toStringAsFixed(2)} ${(cy + outerRimRadius * math.sin(a)).toStringAsFixed(2)} ');
  }
  sb.write('Z ');

  // Inner toothed bore CCW
  for (int i = 0; i < teeth; i++) {
    final cAngle = i * pitchAngle;
    final a1 = cAngle - pitchAngle * 0.30;
    final a2 = cAngle - pitchAngle * 0.14;
    final a3 = cAngle + pitchAngle * 0.14;
    final a4 = cAngle + pitchAngle * 0.30;

    final p1x = cx + rf * math.cos(a1);
    final p1y = cy + rf * math.sin(a1);
    final p2x = cx + ra * math.cos(a2);
    final p2y = cy + ra * math.sin(a2);
    final p3x = cx + ra * math.cos(a3);
    final p3y = cy + ra * math.sin(a3);
    final p4x = cx + rf * math.cos(a4);
    final p4y = cy + rf * math.sin(a4);

    if (i == 0) {
      sb.write('M ${p1x.toStringAsFixed(2)} ${p1y.toStringAsFixed(2)} ');
    } else {
      sb.write('L ${p1x.toStringAsFixed(2)} ${p1y.toStringAsFixed(2)} ');
    }
    sb.write('L ${p2x.toStringAsFixed(2)} ${p2y.toStringAsFixed(2)} ');
    sb.write('L ${p3x.toStringAsFixed(2)} ${p3y.toStringAsFixed(2)} ');
    sb.write('L ${p4x.toStringAsFixed(2)} ${p4y.toStringAsFixed(2)} ');
  }
  sb.write('Z');
  return sb.toString();
}

void main() {
  // Precompute precision CAD SVG gear paths
  // 1. Spur Gear Meshing Pair: Pinion (12T, m=4.2) at (72, 110) + Wheel (18T, m=4.2) at (135, 110)
  // Center distance = 0.5 * 4.2 * (12 + 18) = 63.0 -> 72 + 63 = 135!
  final spurPinion = involuteGearPath(cx: 68, cy: 105, module: 4.0, teeth: 12, rotationDeg: 15.0);
  final spurWheel = involuteGearPath(cx: 128, cy: 105, module: 4.0, teeth: 18, rotationDeg: 0.0);

  // 6. Planetary Epicyclic Set: Sun (14T, m=3.0, rp=21), 3 Planets (11T, m=3.0, rp=16.5), Ring (36T, m=3.0, rp=54)
  // Orbit radius = rp_sun + rp_planet = 21 + 16.5 = 37.5
  final planetRing = internalRingGearPath(cx: 110, cy: 105, module: 3.1, teeth: 36, outerRimRadius: 76);
  final planetSun = involuteGearPath(cx: 110, cy: 105, module: 3.1, teeth: 14, rotationDeg: 12.0);
  final planet1 = involuteGearPath(
    cx: 110 + 38.75 * math.cos(-math.pi / 2),
    cy: 105 + 38.75 * math.sin(-math.pi / 2),
    module: 3.1,
    teeth: 11,
    rotationDeg: 8.0,
  );
  final planet2 = involuteGearPath(
    cx: 110 + 38.75 * math.cos(math.pi / 6),
    cy: 105 + 38.75 * math.sin(math.pi / 6),
    module: 3.1,
    teeth: 11,
    rotationDeg: 20.0,
  );
  final planet3 = involuteGearPath(
    cx: 110 + 38.75 * math.cos(5 * math.pi / 6),
    cy: 105 + 38.75 * math.sin(5 * math.pi / 6),
    module: 3.1,
    teeth: 11,
    rotationDeg: -4.0,
  );

  // Read compiled WOFF2 for zero-CORS Base64 data URI + external file fallback
  final woff2Bytes = File('experiments/geararts-2k26/GearheadGroovy/fonts/woff2/GearheadGroovy-Regular.woff2').readAsBytesSync();
  final woff2B64 = base64Encode(woff2Bytes);

  // Write Master Specimen (`specimen.html`)
  final specimenHtml = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Gearhead Groovy — Master Cardstock Broadside & AGMA Kinematic Specimen (GearArts 2k26)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    @font-face {
      font-family: 'GearheadGroovy';
      src: url('data:font/woff2;base64,$woff2B64') format('woff2'),
           url('fonts/woff2/GearheadGroovy-Regular.woff2') format('woff2'),
           url('fonts/ttf/GearheadGroovy-Regular.ttf') format('truetype');
      font-weight: 400 900;
      font-style: normal;
      font-display: block;
    }

    :root {
      --rag-paper: #f3ecd8;
      --rag-paper-deep: #e7dec3;
      --card-ivory: #faf6eb;
      --plum-ink: #2d0e24;
      --plum-muted: #5e3152;
      --enamel-pink: #f28cb1;
      --enamel-yellow: #ffe07d;
      --enamel-mint: #9ed6a3;
      --enamel-lavender: #c59be0;
      --denim-blue: #6a93b5;
      --boot-russet: #8c4d3e;
      --blueprint-bg: #0c1421;
      --blueprint-grid: rgba(0, 216, 255, 0.08);
      --blueprint-cyan: #00e5ff;
      --brass-gold: #f5b700;
    }

    * { box-sizing: border-box; }

    body {
      background-color: #161116;
      background-image:
        radial-gradient(circle at 50% 0%, rgba(242, 140, 177, 0.08) 0%, transparent 60%),
        repeating-linear-gradient(45deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 2px, transparent 2px, transparent 8px);
      color: var(--plum-ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      margin: 0;
      padding: 2.5rem 1.25rem;
      line-height: 1.5;
    }

    .master-frame {
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 2.5rem;
    }

    /* 1. VINTAGE PHYSICAL CARDSTOCK BROADSIDE */
    .cardstock-sheet {
      background:
        radial-gradient(ellipse at center, var(--card-ivory) 0%, var(--rag-paper) 75%, var(--rag-paper-deep) 100%);
      border-radius: 20px;
      padding: 2.75rem 2.5rem;
      box-shadow:
        0 24px 60px rgba(0, 0, 0, 0.65),
        inset 0 0 0 3px var(--plum-ink),
        inset 0 0 0 9px var(--rag-paper),
        inset 0 0 0 11px rgba(45, 14, 36, 0.35);
      position: relative;
      overflow: hidden;
    }

    .broadside-top-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid rgba(45, 14, 36, 0.2);
      padding-bottom: 0.75rem;
      margin-bottom: 1.5rem;
      font-size: 0.8rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--plum-muted);
    }

    .rainbow-drip-ribbon {
      display: flex;
      height: 8px;
      border-radius: 999px;
      overflow: hidden;
      border: 1.5px solid var(--plum-ink);
      width: 220px;
    }
    .rainbow-drip-ribbon span { flex: 1; }

    /* Live Compiled Font Hero Titling */
    .groovy-hero-banner {
      font-family: 'GearheadGroovy', sans-serif;
      font-size: clamp(3.4rem, 7.8vw, 6.8rem);
      color: var(--plum-ink);
      text-align: center;
      line-height: 1.08;
      letter-spacing: 0.01em;
      margin: 0.5rem 0 1.75rem 0;
      text-shadow: 2px 3px 0px rgba(242, 140, 177, 0.35);
      user-select: all;
    }

    /* 3-Column Cardstock Specimen Layout Flanking the Mascot */
    .broadside-triptych {
      display: grid;
      grid-template-columns: 1fr 370px 1fr;
      gap: 2rem;
      align-items: center;
      margin-top: 1rem;
    }
    @media (max-width: 1060px) {
      .broadside-triptych { grid-template-columns: 1fr; }
    }

    .specimen-wing {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
    }
    .specimen-wing.left {
      text-align: right;
    }
    .specimen-wing.right {
      text-align: left;
    }
    @media (max-width: 1060px) {
      .specimen-wing.left, .specimen-wing.right { text-align: center; }
    }

    .wing-row {
      font-family: 'GearheadGroovy', sans-serif;
      font-size: clamp(2.4rem, 4.2vw, 3.8rem);
      line-height: 1.18;
      color: var(--plum-ink);
      letter-spacing: 0.02em;
    }

    .wing-caption {
      font-size: 0.75rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--plum-muted);
      margin-top: 0.25rem;
    }

    .mascot-medallion {
      background: #efe6cc;
      border: 3px solid var(--plum-ink);
      border-radius: 18px;
      padding: 1rem;
      box-shadow: 6px 8px 0px var(--plum-ink);
      text-align: center;
      position: relative;
    }
    .mascot-medallion img {
      width: 100%;
      height: auto;
      border-radius: 10px;
      display: block;
      border: 1.5px solid rgba(45, 14, 36, 0.25);
    }
    .mascot-tag {
      display: inline-block;
      margin-top: 0.75rem;
      padding: 0.25rem 0.75rem;
      background: var(--plum-ink);
      color: var(--card-ivory);
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 800;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    /* Interactive Live Type Tester Strip inside the Broadside */
    .type-tester-drawer {
      margin-top: 2.5rem;
      padding-top: 1.75rem;
      border-top: 2px dashed rgba(45, 14, 36, 0.25);
    }
    .tester-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 1rem;
    }
    .tester-controls {
      display: flex;
      gap: 1.25rem;
      align-items: center;
      flex-wrap: wrap;
    }
    .control-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(45, 14, 36, 0.08);
      padding: 0.4rem 0.85rem;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--plum-ink);
    }
    .control-pill input[type="range"] {
      accent-color: var(--plum-ink);
      width: 100px;
    }
    .ink-swatches {
      display: flex;
      gap: 0.45rem;
      align-items: center;
    }
    .swatch-btn {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      border: 2px solid var(--plum-ink);
      cursor: pointer;
      transition: transform 0.15s ease;
    }
    .swatch-btn:hover { transform: scale(1.15); }

    .live-tester-input {
      width: 100%;
      background: rgba(255, 255, 255, 0.65);
      border: 2.5px solid var(--plum-ink);
      border-radius: 14px;
      padding: 1.25rem 1.5rem;
      font-family: 'GearheadGroovy', sans-serif;
      font-size: 64px;
      line-height: 1.2;
      color: var(--plum-ink);
      text-align: center;
      outline: none;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.06);
      transition: all 0.15s ease;
    }
    .live-tester-input:focus {
      background: #ffffff;
      box-shadow: 4px 5px 0px var(--plum-ink);
    }

    /* 2. AGMA KINEMATIC GEAR ENGINEERING BLUEPRINT ATLAS */
    .blueprint-section {
      background-color: var(--blueprint-bg);
      background-image:
        linear-gradient(var(--blueprint-grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--blueprint-grid) 1px, transparent 1px);
      background-size: 24px 24px;
      border: 2px solid #243b55;
      border-radius: 20px;
      padding: 2.5rem;
      color: #e2e8f0;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }

    .blueprint-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 1rem;
      border-bottom: 1px solid #243b55;
      padding-bottom: 1.25rem;
      margin-bottom: 2rem;
    }
    .blueprint-header h2 {
      margin: 0;
      font-size: 2rem;
      font-weight: 900;
      letter-spacing: -0.02em;
      color: #fff;
    }
    .agma-spec-badge {
      font-family: ui-monospace, SFMono-Regular, monospace;
      font-size: 0.8rem;
      color: var(--blueprint-cyan);
      background: rgba(0, 229, 255, 0.1);
      border: 1px solid var(--blueprint-cyan);
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
    }

    .gear-atlas-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
      gap: 1.5rem;
    }

    .cad-card {
      background: rgba(15, 25, 42, 0.88);
      border: 1px solid #2a4365;
      border-radius: 14px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .cad-card-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .cad-card-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--brass-gold);
      margin: 0;
    }
    .cad-feature-tag {
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: var(--blueprint-cyan);
      background: rgba(0, 229, 255, 0.12);
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      border: 1px solid rgba(0, 229, 255, 0.3);
    }

    .cad-viewport {
      background: #080d16;
      border: 1px solid #1e334d;
      border-radius: 10px;
      height: 210px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1rem;
      position: relative;
      overflow: hidden;
    }
    .cad-viewport svg {
      width: 220px;
      height: 200px;
      overflow: visible;
    }

    .cad-meta-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
      font-family: ui-monospace, monospace;
    }
    .cad-meta-table td {
      padding: 0.35rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .cad-meta-table td:first-child { color: #94a3b8; }
    .cad-meta-table td:last-child { color: #f8fafc; text-align: right; }

    @keyframes spinCW {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
    }
    @keyframes spinCCW {
      from { transform: rotate(0deg); }
      to { transform: rotate(-360deg); }
    }
    .spin-cw {
      transform-box: fill-box;
      transform-origin: center;
      animation: spinCW 18s linear infinite;
    }
    .spin-ccw {
      transform-box: fill-box;
      transform-origin: center;
      animation: spinCCW 27s linear infinite;
    }
  </style>
</head>
<body>
  <div class="master-frame">
    <!-- 1. AUTHENTIC PHYSICAL CARDSTOCK BROADSIDE -->
    <section class="cardstock-sheet">
      <div class="broadside-top-meta">
        <span>GearArts 2k26 Foundry Collection · Plate No. 01</span>
        <div class="rainbow-drip-ribbon" title="Tipped Enamel Paint Bucket Palette">
          <span style="background: var(--enamel-pink)"></span>
          <span style="background: var(--enamel-yellow)"></span>
          <span style="background: var(--enamel-mint)"></span>
          <span style="background: var(--enamel-lavender)"></span>
          <span style="background: var(--denim-blue)"></span>
        </div>
        <span>1000 UPM · W3C OTS Certified · OFL 1.1</span>
      </div>

      <!-- Hero Title Rendered Live by the Compiled Font Binary -->
      <h1 class="groovy-hero-banner" id="hero-banner">GEARHEAD GROOVY</h1>

      <!-- 3-Column Triptych Matching Original Cardstock Layout -->
      <div class="broadside-triptych">
        <!-- Left Wing -->
        <div class="specimen-wing left">
          <div class="wing-row">ABCDEF</div>
          <div class="wing-row">GHIJKLM</div>
          <div class="wing-row">NOPQRS</div>
          <div class="wing-caption">
            Left Specimen Wing · Rounded Epsilon 'E' &amp; 8-Tooth Star-Cog 'A, O, P, Q, R'
          </div>
        </div>

        <!-- Center Mascot Medallion -->
        <div class="mascot-medallion">
          <img src="sources/mascot_specimen_card.jpg" alt="Original Gearhead Groovy Physical Cardstock Artwork by Phil Gear">
          <div class="mascot-tag">Original Cardstock Master · Phil Gear</div>
        </div>

        <!-- Right Wing (Exact rows from right side of photo!) -->
        <div class="specimen-wing right">
          <div class="wing-row">NOPQR</div>
          <div class="wing-row">TVWXY</div>
          <div class="wing-row">012345</div>
          <div class="wing-row">789!&amp;</div>
          <div class="wing-caption">
            Right Specimen Wing · Viscous Meniscus Drips on 'T, V, Y, !' &amp; Cog '9'
          </div>
        </div>
      </div>

      <!-- Interactive Live Type Tester -->
      <div class="type-tester-drawer">
        <div class="tester-toolbar">
          <div style="font-weight: 900; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em;">
            💧 Live Compiled Binary Type Tester (Type Any Text Below):
          </div>
          <div class="tester-controls">
            <div class="control-pill">
              <span>Size</span>
              <input type="range" min="32" max="110" value="64" oninput="setTesterSize(this.value)">
              <span id="lbl-size">64px</span>
            </div>
            <div class="control-pill">
              <span>Torque Rake</span>
              <input type="range" min="-15" max="15" value="0" oninput="setTesterSkew(this.value)">
              <span id="lbl-skew">0°</span>
            </div>
            <div class="ink-swatches">
              <button class="swatch-btn" style="background:#2d0e24" title="Cardstock Plum Ink" onclick="setTesterInk('#2d0e24')"></button>
              <button class="swatch-btn" style="background:#b81d5c" title="Hot-Rod Candy Berry" onclick="setTesterInk('#b81d5c')"></button>
              <button class="swatch-btn" style="background:#1c4e80" title="Denim Overalls Indigo" onclick="setTesterInk('#1c4e80')"></button>
              <button class="swatch-btn" style="background:#1f5c3a" title="Garage Enamel Green" onclick="setTesterInk('#1f5c3a')"></button>
            </div>
          </div>
        </div>
        <input
          type="text"
          class="live-tester-input"
          id="tester-input"
          value="GEARHEAD GROOVY 789!&"
          aria-label="Interactive Gearhead Groovy Font Tester"
        >
      </div>
    </section>

    <!-- 2. PRECISION AGMA KINEMATIC GEAR ENGINEERING ATLAS -->
    <section class="blueprint-section">
      <div class="blueprint-header">
        <div>
          <div style="font-size: 0.78rem; font-weight: 800; color: var(--blueprint-cyan); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem;">
            Society of Gear Manufacturers &amp; Automotive Coating Specialists
          </div>
          <h2>AGMA 2001-D04 KINEMATIC GEAR &amp; RHEOLOGY ATLAS</h2>
        </div>
        <div class="agma-spec-badge">
          INVOLUTE r(t) = r_b · √(1 + t²) · α = 20.0°
        </div>
      </div>

      <div class="gear-atlas-grid">
        <!-- Card 1: Meshing Involute Spur Gear Pair -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">1. Involute Spur Mesh (12T : 18T)</h3>
              <span class="cad-feature-tag">cv01 · Spur Counter</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 210 210">
                <!-- Pitch circles -->
                <circle cx="68" cy="105" r="24" stroke="#00e5ff" stroke-width="1" stroke-dasharray="3 3" fill="none" opacity="0.6"/>
                <circle cx="128" cy="105" r="36" stroke="#00e5ff" stroke-width="1" stroke-dasharray="3 3" fill="none" opacity="0.6"/>
                <!-- 12T Pinion -->
                <g class="spin-cw">
                  <path d="$spurPinion" fill="#1e3a5f" stroke="#00e5ff" stroke-width="1.5"/>
                  <circle cx="68" cy="105" r="9" fill="#080d16" stroke="#00e5ff" stroke-width="1.5"/>
                </g>
                <!-- 18T Wheel -->
                <g class="spin-ccw">
                  <path d="$spurWheel" fill="#2d1a3a" stroke="#f5b700" stroke-width="1.5"/>
                  <circle cx="128" cy="105" r="13" fill="#080d16" stroke="#f5b700" stroke-width="1.5"/>
                </g>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Pressure Angle (α)</td><td>20.0° Standard Involute</td></tr>
            <tr><td>Reduction Ratio</td><td>1.50 : 1 (Coplanar Parallel)</td></tr>
            <tr><td>Glyph Mapping</td><td>A, O, P, Q, R, 0, 8, 9</td></tr>
          </table>
        </div>

        <!-- Card 2: Coaxial Epicyclic Planetary Set -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">2. Epicyclic Planetary Transmission</h3>
              <span class="cad-feature-tag">cv06 · Concentric Ring</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 220 210">
                <!-- Internal Ring Annulus (36T) -->
                <path d="$planetRing" fill="#172a45" stroke="#00e5ff" stroke-width="1.4" fill-rule="evenodd"/>
                <!-- Carrier Web -->
                <polygon points="110,66.25 143.56,124.38 76.44,124.38" fill="none" stroke="rgba(245,183,0,0.45)" stroke-width="2" stroke-dasharray="4 2"/>
                <!-- Sun Gear (14T) -->
                <path d="$planetSun" fill="#4a154b" stroke="#f28cb1" stroke-width="1.4"/>
                <circle cx="110" cy="105" r="8" fill="#080d16" stroke="#f28cb1" stroke-width="1.2"/>
                <!-- 3 Orbiting Planet Gears (11T) -->
                <path d="$planet1" fill="#3d2b10" stroke="#f5b700" stroke-width="1.3"/>
                <circle cx="110" cy="66.25" r="5.5" fill="#080d16" stroke="#f5b700" stroke-width="1.2"/>
                <path d="$planet2" fill="#3d2b10" stroke="#f5b700" stroke-width="1.3"/>
                <circle cx="143.56" cy="124.38" r="5.5" fill="#080d16" stroke="#f5b700" stroke-width="1.2"/>
                <path d="$planet3" fill="#3d2b10" stroke="#f5b700" stroke-width="1.3"/>
                <circle cx="76.44" cy="124.38" r="5.5" fill="#080d16" stroke="#f5b700" stroke-width="1.2"/>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Tooth Constraint</td><td>Z_r (36) = Z_s (14) + 2·Z_p (11)</td></tr>
            <tr><td>Torque Split</td><td>3× Balanced Planet Carrier</td></tr>
            <tr><td>Glyph Mapping</td><td>O, Q, 0, @ Concentric Bowls</td></tr>
          </table>
        </div>

        <!-- Card 3: André Citroën Double-Helical Herringbone -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">3. Double-Helical Herringbone</h3>
              <span class="cad-feature-tag">cv03 · Zero Axial Thrust</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 220 210">
                <!-- Cylinder body -->
                <rect x="45" y="25" width="130" height="160" rx="10" fill="#15263d" stroke="#00e5ff" stroke-width="1.8"/>
                <line x1="110" y1="20" x2="110" y2="190" stroke="#00e5ff" stroke-width="1" stroke-dasharray="4 3"/>
                <!-- Opposed V-Chevron Helical Teeth -->
                <g stroke="#f5b700" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none">
                  <path d="M 55 42 L 110 68 L 165 42"/>
                  <path d="M 55 72 L 110 98 L 165 72"/>
                  <path d="M 55 102 L 110 128 L 165 102"/>
                  <path d="M 55 132 L 110 158 L 165 132"/>
                  <path d="M 55 162 L 110 184 L 165 162"/>
                </g>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Helix Angle (β)</td><td>±30.0° Opposed V-Chevrons</td></tr>
            <tr><td>Net Axial Thrust</td><td>0.0 N (Self-Cancelling)</td></tr>
            <tr><td>Glyph Mapping</td><td>V, W, M &amp; Chevron Terminals</td></tr>
          </table>
        </div>

        <!-- Card 4: Self-Locking Worm & Phosphor-Bronze Wheel -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">4. Irreversible Worm &amp; Wheel</h3>
              <span class="cad-feature-tag">cv05 · 60:1 Self-Lock</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 220 210">
                <!-- Worm shaft -->
                <rect x="25" y="30" width="170" height="32" rx="6" fill="#1e293b" stroke="#00e5ff" stroke-width="1.5"/>
                <!-- Acme / Involute Helicoid Threads -->
                <g stroke="#00e5ff" stroke-width="6" stroke-linecap="round">
                  <line x1="45" y1="28" x2="62" y2="64"/>
                  <line x1="72" y1="28" x2="89" y2="64"/>
                  <line x1="99" y1="28" x2="116" y2="64"/>
                  <line x1="126" y1="28" x2="143" y2="64"/>
                  <line x1="153" y1="28" x2="170" y2="64"/>
                </g>
                <!-- Meshing Bronze Wheel below -->
                <g transform="translate(42, 42)">
                  <path d="$spurWheel" fill="#3d2914" stroke="#f5b700" stroke-width="1.5"/>
                  <circle cx="68" cy="105" r="14" fill="#080d16" stroke="#f5b700" stroke-width="1.5"/>
                </g>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Lead Angle (λ)</td><td>4.2° (&lt; Friction Angle φ)</td></tr>
            <tr><td>Backdrive Lock</td><td>100% Irreversible Hold</td></tr>
            <tr><td>Glyph Mapping</td><td>Threaded Stems &amp; Serifs</td></tr>
          </table>
        </div>

        <!-- Card 5: 90° Hypoid Spiral Bevel Differential -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">5. Hypoid Spiral Bevel (90°)</h3>
              <span class="cad-feature-tag">cv04 · Offset Pinion</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 220 210">
                <!-- Conical Ring Gear -->
                <ellipse cx="110" cy="135" rx="78" ry="42" fill="#231528" stroke="#f28cb1" stroke-width="2"/>
                <ellipse cx="110" cy="135" rx="42" ry="22" fill="#080d16" stroke="#f28cb1" stroke-width="1.5"/>
                <!-- Spiral Bevel Flutes -->
                <g stroke="#f28cb1" stroke-width="3.5" fill="none">
                  <path d="M 45 135 Q 70 110 95 120"/>
                  <path d="M 65 162 Q 85 135 102 142"/>
                  <path d="M 110 177 Q 118 155 115 152"/>
                  <path d="M 155 162 Q 140 138 128 140"/>
                  <path d="M 175 135 Q 150 112 125 120"/>
                </g>
                <!-- Offset Hypoid Drive Pinion -->
                <polygon points="125,35 165,35 178,92 112,92" fill="#172a45" stroke="#00e5ff" stroke-width="1.8"/>
                <path d="M 122 50 Q 145 65 170 55" stroke="#00e5ff" stroke-width="3.5" fill="none"/>
                <path d="M 116 75 Q 145 90 174 78" stroke="#00e5ff" stroke-width="3.5" fill="none"/>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Hypoid Offset (E)</td><td>38.1 mm Below Axle Centerline</td></tr>
            <tr><td>Application</td><td>Ford 9-Inch / Dana 60 Hot-Rod</td></tr>
            <tr><td>Glyph Mapping</td><td>R, K, X Diagonal Junctions</td></tr>
          </table>
        </div>

        <!-- Card 6: Rayleigh-Plateau Enamel Paint Rheology -->
        <div class="cad-card">
          <div>
            <div class="cad-card-head">
              <h3 class="cad-card-title">6. Enamel Coating Rheology</h3>
              <span class="cad-feature-tag">ss01 · Meniscus Drip</span>
            </div>
            <div class="cad-viewport">
              <svg viewBox="0 0 220 210">
                <!-- Baseline Stroke Bar -->
                <rect x="25" y="25" width="170" height="36" rx="18" fill="#2d0e24" stroke="#f28cb1" stroke-width="2"/>
                <!-- Stage 1: Capillary Swell -->
                <path d="M 50 60 C 55 60, 58 88, 65 88 C 72 88, 75 60, 80 60 Z" fill="#f28cb1"/>
                <!-- Stage 2: Meniscus Necking & Pendant Drop -->
                <path d="M 98 60 C 106 60, 108 95, 104 115 C 100 132, 106 146, 114 146 C 122 146, 128 132, 124 115 C 120 95, 122 60, 130 60 Z" fill="#ffe07d"/>
                <!-- Stage 3: Pinch-off & Airborne Satellite Droplet -->
                <path d="M 152 60 C 158 60, 160 85, 157 102 C 154 116, 159 126, 165 126 C 171 126, 176 116, 173 102 C 170 85, 172 60, 178 60 Z" fill="#9ed6a3"/>
                <circle cx="165" cy="152" r="11" fill="#9ed6a3"/>
                <circle cx="165" cy="180" r="6" fill="#9ed6a3"/>
              </svg>
            </div>
          </div>
          <table class="cad-meta-table">
            <tr><td>Capillary Number</td><td>Bo = ρ·g·R² / γ (Pendant Pinch)</td></tr>
            <tr><td>Efflux Viscosity</td><td>Zahn Cup #2 · 28 sec @ 25°C</td></tr>
            <tr><td>Glyph Mapping</td><td>G, H, O, R, T, V, Y, !</td></tr>
          </table>
        </div>
      </div>
    </section>
  </div>

  <script>
    const tester = document.getElementById('tester-input');
    const lblSize = document.getElementById('lbl-size');
    const lblSkew = document.getElementById('lbl-skew');

    function setTesterSize(px) {
      tester.style.fontSize = px + 'px';
      lblSize.textContent = px + 'px';
    }

    function setTesterSkew(deg) {
      tester.style.transform = 'skewX(' + (-deg) + 'deg)';
      lblSkew.textContent = deg + '°';
    }

    function setTesterInk(hex) {
      tester.style.color = hex;
      document.getElementById('hero-banner').style.color = hex;
    }
  </script>
</body>
</html>
''';

  File('experiments/geararts-2k26/GearheadGroovy/specimen.html').writeAsStringSync(specimenHtml);
  print('  ✓ Generated Master Broadside & Kinematic Atlas: experiments/geararts-2k26/GearheadGroovy/specimen.html');
}
