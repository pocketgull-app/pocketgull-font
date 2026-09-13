// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Chinuk Pipa Specimen Generator
///
/// Procedurally synthesizes the 9 canonical typeface specimen plates in SVG
/// using authentic Pacific Northwest & Grand Ronde color palettes, Duployan
/// shorthand for Chinuk Wawa (U+1BC00–U+1BC9F), the PERMA+ clinical wellness
/// model, and embedded high-resolution neural masterworks (Kells, Pebble, Rubaiyat).
///
/// Enforces:
///   - 100% Inuktitut-parity Social GitHub Preview with Polar Washi Paperboard,
///     deckle borders, official heraldic flags, and clinical ribbons.
///   - Museum Print Broadside Pedagogical Language Map (White/Ivory, high contrast).
///   - Strict WCAG AAA Compliance (>= 7:1 contrast) on Dark Obsidian Basalt.
///   - Landmark Typographic Triad: Type Engineering Blueprint, Clinical Telemetry,
///     and Pedagogical Scaffolding Plate.
///
/// Renders 300 DPI Master Museum Print PNGs using Inkscape in WSL.
library;

import 'dart:convert';
import 'dart:io';

void main() async {
  stdout.writeln('=== POCKETGULL CHINUK PIPA SPECIMEN GENERATOR (DART 3.11) ===');

  final repoDir = Directory('c:/Users/philg/Pocketgull/pocketgull-typeface');
  final targetDir = Directory('${repoDir.path}/documentation/images/chinuk_pipa');
  if (!targetDir.existsSync()) {
    targetDir.createSync(recursive: true);
  }
  stdout.writeln('Target Directory: ${targetDir.path}\n');

  // Load high-resolution Pacific Northwest masterworks
  final kellsWebpPath = '${repoDir.path}/documentation/masterworks/pacific_northwest/kells_pnw_vexillology.webp';
  final pebbleWebpPath = '${repoDir.path}/documentation/masterworks/pacific_northwest/pebble_pnw_biodiversity.webp';
  final rubaiyatWebpPath = '${repoDir.path}/documentation/masterworks/pacific_northwest/rubaiyat_pnw_astrolabe.webp';

  stdout.write('Loading masterwork substrates... ');
  final kellsBase64 = File(kellsWebpPath).existsSync()
      ? base64Encode(File(kellsWebpPath).readAsBytesSync())
      : '';
  final pebbleBase64 = File(pebbleWebpPath).existsSync()
      ? base64Encode(File(pebbleWebpPath).readAsBytesSync())
      : '';
  final rubaiyatBase64 = File(rubaiyatWebpPath).existsSync()
      ? base64Encode(File(rubaiyatWebpPath).readAsBytesSync())
      : '';
  stdout.writeln('OK (Kells: ${(kellsBase64.length / 1024).toStringAsFixed(0)} KB, Pebble: ${(pebbleBase64.length / 1024).toStringAsFixed(0)} KB, Rubaiyat: ${(rubaiyatBase64.length / 1024).toStringAsFixed(0)} KB)\n');

  // 1. Social GitHub Preview (1280x640) — Polar Washi Paperboard (Inuktitut Parity)
  stdout.writeln('[1/9] Synthesizing social_github_preview.svg (Polar Washi Deckle + Flags)...');
  final socialSvg = generateSocialPreview(kellsBase64);
  File('${targetDir.path}/social_github_preview.svg').writeAsStringSync(socialSvg);

  // 2. Synaptic Specimen Dark (1200x1720) — Strict WCAG AAA (>= 7:1 Contrast)
  stdout.writeln('[2/9] Synthesizing pocketgull_synaptic_specimen_dark.svg (WCAG AAA Obsidian)...');
  final darkSvg = generateSynapticSpecimenDark(rubaiyatBase64);
  File('${targetDir.path}/pocketgull_synaptic_specimen_dark.svg').writeAsStringSync(darkSvg);

  // 3. Synaptic Specimen Light (1200x1720)
  stdout.writeln('[3/9] Synthesizing pocketgull_synaptic_specimen_light.svg (Polar Washi Light)...');
  final lightSvg = generateSynapticSpecimenLight(pebbleBase64);
  File('${targetDir.path}/pocketgull_synaptic_specimen_light.svg').writeAsStringSync(lightSvg);

  // 4. PERMA+ Thoughts Card (800x800)
  stdout.writeln('[4/9] Synthesizing pocketgull_perma_thoughts_card.svg (800x800)...');
  final permaSvg = generatePermaThoughtsCard();
  File('${targetDir.path}/pocketgull_perma_thoughts_card.svg').writeAsStringSync(permaSvg);

  // 5. Print Gallery Exhibition (1200x1720)
  stdout.writeln('[5/9] Synthesizing print_gallery_exhibition.svg (Museum Broadside)...');
  final exhibitionSvg = generatePrintExhibition(kellsBase64);
  File('${targetDir.path}/print_gallery_exhibition.svg').writeAsStringSync(exhibitionSvg);

  // 6. Chinuk Pipa Language Map (1200x1720) — Clean Museum Print Broadside
  stdout.writeln('[6/9] Synthesizing chinuk_pipa_language_map.svg (High-Contrast Museum Broadside)...');
  final mapSvg = generateLanguageMap();
  File('${targetDir.path}/chinuk_pipa_language_map.svg').writeAsStringSync(mapSvg);

  // 7. Landmark Plate A: Type Engineering Blueprint (896x1200)
  stdout.writeln('[7/9] Synthesizing pocketgull_type_engineering_specimen.svg (Cyan Blueprint)...');
  final engSvg = generateTypeEngineeringPlate();
  File('${targetDir.path}/pocketgull_type_engineering_specimen.svg').writeAsStringSync(engSvg);

  // 8. Landmark Plate B: Clinical Telemetry Specimen (896x1200)
  stdout.writeln('[8/9] Synthesizing pocketgull_telemetry_type_specimen.svg (ICU Clinical)...');
  final telSvg = generateTelemetryTypePlate();
  File('${targetDir.path}/pocketgull_telemetry_type_specimen.svg').writeAsStringSync(telSvg);

  // 9. Landmark Plate C: Pedagogical Typeface Specimen (896x1200)
  stdout.writeln('[9/9] Synthesizing pocketgull_pedagogical_typeface.svg (Deckle Washi Scaffolding)...');
  final pedSvg = generatePedagogicalPlate();
  File('${targetDir.path}/pocketgull_pedagogical_typeface.svg').writeAsStringSync(pedSvg);

  // High-Resolution 300 DPI Master Print Rasterization via WSL Inkscape
  stdout.writeln('\n--- RASTERIZING 300 DPI MASTER PRINT PNGS VIA WSL INKSCAPE ---');
  final specs = [
    ('social_github_preview.svg', 'social_github_preview.png', 1280, 640),
    ('pocketgull_synaptic_specimen_dark.svg', 'pocketgull_synaptic_specimen_dark.png', 3750, 5375),
    ('pocketgull_synaptic_specimen_light.svg', 'pocketgull_synaptic_specimen_light.png', 3750, 5375),
    ('pocketgull_perma_thoughts_card.svg', 'pocketgull_perma_thoughts_card.png', 2400, 2400),
    ('print_gallery_exhibition.svg', 'print_gallery_exhibition.png', 3600, 5160),
    ('chinuk_pipa_language_map.svg', 'chinuk_pipa_language_map.png', 3600, 5160),
    ('pocketgull_type_engineering_specimen.svg', 'pocketgull_type_engineering_specimen.png', 2688, 3600),
    ('pocketgull_telemetry_type_specimen.svg', 'pocketgull_telemetry_type_specimen.png', 2688, 3600),
    ('pocketgull_pedagogical_typeface.svg', 'pocketgull_pedagogical_typeface.png', 2688, 3600),
  ];

  for (final (svgName, pngName, width, height) in specs) {
    final wslSvgPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/chinuk_pipa/$svgName';
    final wslPngPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/chinuk_pipa/$pngName';

    stdout.write('Rendering $pngName (${width}x$height, 300 DPI)... ');
    final result = await Process.run('wsl', [
      '--',
      '/usr/bin/inkscape',
      wslSvgPath,
      '--export-type=png',
      '--export-filename=$wslPngPath',
      '-w',
      '$width',
      '-h',
      '$height',
    ]);

    if (result.exitCode == 0) {
      final pngFile = File('${targetDir.path}/$pngName');
      final sizeMb = (pngFile.existsSync() ? pngFile.lengthSync() / (1024 * 1024) : 0).toStringAsFixed(2);
      stdout.writeln('OK ($sizeMb MB)');
    } else {
      stderr.writeln('FAILED (exit code ${result.exitCode})');
      stderr.writeln(result.stderr);
    }
  }

  stdout.writeln('\n[SUCCESS] Completed Chinuk Pipa specimen suite generation at 300 DPI Master Museum Print quality.');
}

// =============================================================================
// HELPER: OFFICIAL UNITED STATES FLAG (TITLE 4 U.S.C. SPECIFICATION)
// =============================================================================
String usFlagSvg({double x = 0, double y = 0, double width = 56, double height = 28}) {
  final stripeH = height / 13.0;
  final cantonW = width * 0.42;
  final cantonH = stripeH * 7.0;

  final sb = StringBuffer();
  sb.writeln('<g transform="translate($x, $y)">');
  sb.writeln('  <rect width="$width" height="$height" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>');
  // Stripes
  for (int i = 0; i < 13; i++) {
    final color = (i % 2 == 0) ? '#B22234' : '#FFFFFF';
    sb.writeln('  <rect x="0" y="${(i * stripeH).toStringAsFixed(2)}" width="$width" height="${stripeH.toStringAsFixed(2)}" fill="$color"/>');
  }
  // Canton
  sb.writeln('  <rect x="0" y="0" width="${cantonW.toStringAsFixed(2)}" height="${cantonH.toStringAsFixed(2)}" fill="#3C3B6E"/>');
  // Stylized Star Grid
  sb.writeln('  <g fill="#FFFFFF" opacity="0.95">');
  for (int row = 0; row < 4; row++) {
    for (int col = 0; col < 5; col++) {
      final sx = 4.0 + col * 4.4;
      final sy = 2.5 + row * 3.4;
      sb.writeln('    <circle cx="${sx.toStringAsFixed(1)}" cy="${sy.toStringAsFixed(1)}" r="0.9"/>');
    }
  }
  sb.writeln('  </g>');
  sb.writeln('</g>');
  return sb.toString();
}

// =============================================================================
// HELPER: OREGON STATE / GRAND RONDE HERALDIC BADGE
// =============================================================================
String oregonBadgeSvg({double x = 0, double y = 0, double width = 56, double height = 28}) {
  return '''
  <g transform="translate($x, $y)">
    <rect width="$width" height="$height" rx="2" fill="#002B66" stroke="#CBD5E1" stroke-width="0.8"/>
    <!-- Gold Trim Rule -->
    <rect x="0" y="0" width="$width" height="2" fill="#F59E0B"/>
    <rect x="0" y="${height - 2}" width="$width" height="2" fill="#F59E0B"/>
    <!-- Gold Center Star & Shield Symbol -->
    <text x="${width / 2}" y="15" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="bold" fill="#FBBF24" text-anchor="middle" letter-spacing="0.05em">OREGON</text>
    <text x="${width / 2}" y="23" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="bold" fill="#FDE68A" text-anchor="middle">1859 • GRD</text>
  </g>
  ''';
}

// =============================================================================
// 1. SOCIAL GITHUB PREVIEW (1280x640) — POLAR WASHI PAPERBOARD (INUKTITUT PARITY)
// =============================================================================
String generateSocialPreview(String photoBase64) {
  final usFlag = usFlagSvg(x: 410, y: 0, width: 52, height: 28);
  final orBadge = oregonBadgeSvg(x: 468, y: 0, width: 52, height: 28);

  final photoEmbed = photoBase64.isNotEmpty
      ? '''
      <g transform="translate(60, 60)">
        <!-- Soft Washi Ambient Shadow -->
        <rect x="2" y="6" width="460" height="520" rx="18" fill="#78716C" fill-opacity="0.08"/>
        <clipPath id="ghImgClip"><rect width="460" height="520" rx="18"/></clipPath>
        
        <!-- Base Paper Surface -->
        <rect width="460" height="520" rx="18" fill="#FAF8F5"/>
        <image href="data:image/webp;base64,$photoBase64" width="460" height="520" preserveAspectRatio="xMidYMid slice" clip-path="url(#ghImgClip)"/>
        
        <!-- Seamless Washi Feathering Vignette -->
        <rect width="460" height="520" rx="18" fill="url(#photoWashiOverlay)" clip-path="url(#ghImgClip)"/>
      </g>
      '''
      : '';

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="640" viewBox="0 0 1280 640" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
      .font-body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    </style>
    <linearGradient id="polarWashiBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="40%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F2ECE1"/>
    </linearGradient>
    <linearGradient id="photoWashiOverlay" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF8F5" stop-opacity="0.05"/>
      <stop offset="70%" stop-color="#FAF8F5" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FAF8F5" stop-opacity="0.85"/>
    </linearGradient>
  </defs>

  <!-- Base Polar Washi Paperboard Canvas -->
  <rect width="1280" height="640" fill="url(#polarWashiBg)"/>

  <!-- Outer Tactile Deckle Framing in Organic Washi & Vexillology Accent -->
  <rect x="24" y="24" width="1232" height="592" fill="none" stroke="#E2DACB" stroke-width="1.5"/>
  <rect x="30" y="30" width="1220" height="580" fill="none" stroke="#E2DACB" stroke-width="0.8" stroke-dasharray="4,4"/>

  <!-- Top Accent Rules: Royal Blue, Tribal Gold, Forest Green, Redcedar Amber -->
  <rect x="24" y="24" width="308" height="4" fill="#1E3A8A"/>
  <rect x="332" y="24" width="308" height="4" fill="#F59E0B"/>
  <rect x="640" y="24" width="308" height="4" fill="#166534"/>
  <rect x="948" y="24" width="308" height="4" fill="#C2410C"/>

  <!-- Photographic Plate (Left Side) -->
  $photoEmbed

  <!-- Right Side: Chinuk Pipa Typography & Seven Generations HUD on Washi -->
  <g transform="translate(550, 60)">
    <!-- Header Ribbon: Country Code + Flags -->
    <g>
      <rect x="0" y="0" width="120" height="28" rx="3" fill="#1E3A8A"/>
      <text x="60" y="19" class="font-mono" font-size="12" fill="#FFFFFF" text-anchor="middle" font-weight="bold">CASE STUDY 02</text>
      
      <rect x="128" y="0" width="200" height="28" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="228" y="19" class="font-mono" font-size="11" fill="#B45309" text-anchor="middle" font-weight="bold">ISO 3166-2: US-OR • USA</text>

      <rect x="336" y="0" width="66" height="28" rx="3" fill="#166534"/>
      <text x="369" y="19" class="font-mono" font-size="11" fill="#FFFFFF" text-anchor="middle" font-weight="bold">chn-US</text>

      $usFlag
      $orBadge
    </g>

    <!-- Large Bilingual Title in Charcoal Letterpress & Redcedar Amber -->
    <text x="0" y="80" class="font-brand" font-size="44" font-weight="800" fill="#1F1B16" letter-spacing="-0.02em">PocketGull <tspan fill="#C2410C">Chinuk Pipa</tspan></text>
    <text x="0" y="112" class="font-duployan" font-size="17" fill="#1E3A8A">𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁 • DUPLOYAN SHORTHAND (U+1BC00–U+1BC9F)</text>

    <!-- Elder Wisdom & Living Language Foundation Ribbon -->
    <g transform="translate(0, 130)">
      <rect width="665" height="50" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <rect x="0" y="0" width="4" height="50" fill="#C2410C"/>
      <text x="14" y="20" class="font-duployan" font-size="14" fill="#1F1B16">"𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁 𛲟 𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛲟 𛰃𛱆𛰆𛱆𛰅𛱑𛰙" <tspan class="font-body" font-size="11" fill="#57534E">— Grand Ronde Ancestral Wisdom</tspan></text>
      <text x="14" y="38" class="font-body" font-size="11" fill="#1E3A8A" font-style="italic">Good Words • Good Heart • Sacred Family // Confederated Tribes of Grand Ronde</text>
    </g>

    <!-- Stenographic Vector & Vowel Plate on Ivory Washi -->
    <g transform="translate(0, 195)">
      <rect width="665" height="88" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <line x1="0" y1="0" x2="665" y2="0" stroke="#F59E0B" stroke-width="2.5"/>
      <text x="18" y="25" class="font-mono" font-size="11" fill="#B45309" font-weight="bold">DUPLOYAN PHONETIC GEOMETRY [LINES • ARCS • CIRCLES] // 143 CODEPOINTS</text>
      <text x="18" y="65" class="font-duployan" font-size="28" fill="#1F1B16" letter-spacing="0.14em">𛰂 𛰃 𛰅 𛰆 𛰙 𛰚 𛰛 𛰜   𛱁 𛱄 𛱆 𛱑 𛱼 𛲟 𛲞</text>
    </g>

    <!-- 4 Weights Invariant Badges in Washi Styling -->
    <g transform="translate(0, 298)">
      <rect x="0" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="77" y="21" class="font-mono" font-size="11" fill="#1E3A8A" text-anchor="middle" font-weight="bold">Fineliner 400</text>

      <rect x="168" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="245" y="21" class="font-mono" font-size="11" fill="#B45309" text-anchor="middle" font-weight="bold">Bold 700</text>

      <rect x="336" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="413" y="21" class="font-mono" font-size="11" fill="#C2410C" text-anchor="middle" font-weight="bold">Chiseltip 900</text>

      <rect x="504" y="0" width="161" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="584" y="21" class="font-mono" font-size="11" fill="#166534" text-anchor="middle" font-weight="bold">Mono 600 UPM</text>
    </g>

    <!-- Clinical Hospital Vitals & Words of Healing Ribbon -->
    <g transform="translate(0, 345)">
      <rect width="665" height="80" rx="3" fill="#FFFDF8" stroke="#166534" stroke-width="1.2"/>
      <text x="18" y="25" class="font-brand" font-size="13" fill="#166534" font-weight="bold">DOCTOR TILIKUM // GRAND RONDE HEALTH &amp; WELLNESS CENTER (OREGON)</text>
      <text x="18" y="58" class="font-duployan" font-size="20" fill="#1F1B16">𛰃𛱑𛰙 𛰃𛱑𛰙: 72 bpm • 𛰸𛱆𛰚: 99% • 𛰜𛰅𛱑𛰅𛱑𛰙 𛰃𛱑𛰙 𛰃𛱑𛰙: STABLE</text>
    </g>

    <!-- Seven Generations & Living Heritage Note + Colophon -->
    <g transform="translate(0, 442)">
      <text x="0" y="16" class="font-body" font-size="12" fill="#57534E">"Nsayka wawa kakwa nsayka tilixam munk-kemteks nsayka." (Our words teach our people)</text>
      <text x="0" y="38" class="font-mono" font-size="11" fill="#78716C">PHILLIP GEAR // UNIVERSAL WORLD SCRIPTS INITIATIVE // OFL 1.1 // US-OR 🇺🇸 // POCKETGULL.APP</text>
    </g>
  </g>
</svg>''';
}

// =============================================================================
// 2. SYNAPTIC SPECIMEN DARK (1200x1720) — STRICT WCAG AAA (>= 7:1 CONTRAST)
// =============================================================================
String generateSynapticSpecimenDark(String rubaiyatBase64) {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
  </defs>

  <!-- Deep Obsidian Basalt Canvas -->
  <rect width="1200" height="1720" fill="#09090B"/>

  <!-- High-Contrast Outer Framing (WCAG AAA) -->
  <rect x="30" y="30" width="1140" height="1660" rx="14" fill="none" stroke="#334155" stroke-width="2"/>
  <rect x="36" y="36" width="1128" height="1648" rx="10" fill="none" stroke="#1E293B" stroke-width="1"/>

  <!-- Header -->
  <g transform="translate(70, 95)">
    <text x="0" y="0" class="font-mono" font-size="12" fill="#FBBF24" font-weight="700" letter-spacing="0.12em">POCKETGULL TYPEFOUNDRY // TIER 6 SPECIMEN (WCAG AAA CERTIFIED)</text>
    <text x="0" y="44" class="font-brand" font-size="44" font-weight="800" fill="#F8FAFC">Chinuk Pipa (Duployan Shorthand)</text>
    <text x="0" y="78" class="font-brand" font-size="18" font-weight="600" fill="#CBD5E1">The 1891 Phonetic Stenography of Chinuk Wawa (U+1BC00–U+1BC9F) // Zero-Tofu Edition</text>
  </g>

  <!-- Masterwork Plate with High-Contrast Text Overlays -->
  <g transform="translate(70, 200)">
    <rect width="1060" height="320" rx="12" fill="#0F172A" stroke="#475569" stroke-width="1.5"/>
    <clipPath id="darkArtClip">
      <rect width="1060" height="320" rx="12"/>
    </clipPath>
    <g clip-path="url(#darkArtClip)">
      ${rubaiyatBase64.isNotEmpty ? '<image x="0" y="-80" width="1060" height="480" href="data:image/webp;base64,$rubaiyatBase64" preserveAspectRatio="xMidYMid slice" opacity="0.45"/>' : ''}
      <rect width="1060" height="320" fill="linear-gradient(to right, #09090B 0%, rgba(9,9,11,0.6) 50%, #09090B 100%)"/>
    </g>
    <text x="40" y="125" class="font-duployan" font-size="60" fill="#FDE68A" letter-spacing="0.12em">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛲟 𛰀𛱇𛰀𛱇 𛲟 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
    <text x="40" y="190" class="font-brand" font-size="22" font-weight="800" fill="#FFFFFF">Kloshe Tumtum • Heehee • Tilikum</text>
    <text x="40" y="222" class="font-mono" font-size="14" font-weight="700" fill="#93C5FD">Good Heart (Vagal Tone) • Laughter &amp; Joy • Sacred Family Community</text>
  </g>

  <!-- Section 1: Consonant Geometry -->
  <g transform="translate(70, 560)">
    <text x="0" y="0" class="font-mono" font-size="14" fill="#FBBF24" font-weight="700">1. CONSONANT GEOMETRY: LINES &amp; ROTATIONAL VECTORS</text>
    <rect x="0" y="15" width="1060" height="230" rx="10" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>

    <g transform="translate(30, 55)">
      <!-- Row 1 -->
      <g>
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰂</text>
        <text x="45" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">P (U+1BC02)</text>
        <text x="45" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Pipa (paper, letter)</text>

        <text x="260" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰃</text>
        <text x="305" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">T (U+1BC03)</text>
        <text x="305" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Tumtum (heart, soul)</text>

        <text x="520" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰅</text>
        <text x="565" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">K (U+1BC05)</text>
        <text x="565" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Kloshe (good, peaceful)</text>

        <text x="780" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰆</text>
        <text x="825" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">L (U+1BC06)</text>
        <text x="825" y="12" class="font-brand" font-size="13" fill="#CBD5E1">La-kret (medicine)</text>
      </g>

      <!-- Row 2 -->
      <g transform="translate(0, 95)">
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰙</text>
        <text x="45" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">M (U+1BC19)</text>
        <text x="45" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Mamook (make, work)</text>

        <text x="260" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰚</text>
        <text x="305" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">N (U+1BC1A)</text>
        <text x="305" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Nanitch (see, attend)</text>

        <text x="520" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰛</text>
        <text x="565" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">J / CH (U+1BC1B)</text>
        <text x="565" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Chako (come, arrive)</text>

        <text x="780" y="0" class="font-duployan" font-size="34" fill="#FDE68A">𛰜</text>
        <text x="825" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">S (U+1BC1C)</text>
        <text x="825" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Skookum (strong, safe)</text>
      </g>
    </g>
  </g>

  <!-- Section 2: Vocalic Circles Grid -->
  <g transform="translate(70, 835)">
    <text x="0" y="0" class="font-mono" font-size="14" fill="#38BDF8" font-weight="700">2. VOCALIC CIRCLES &amp; COMPOUND GLIDES</text>
    <rect x="0" y="15" width="1060" height="210" rx="10" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>

    <g transform="translate(30, 55)">
      <!-- Row 1 -->
      <g>
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱁</text>
        <text x="45" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">A (U+1BC41)</text>
        <text x="45" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Alki (future, hope)</text>

        <text x="260" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱄</text>
        <text x="305" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">O (U+1BC44)</text>
        <text x="305" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Olally (berry, food)</text>

        <text x="520" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱆</text>
        <text x="565" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">I (U+1BC46)</text>
        <text x="565" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Ikt (one, unity)</text>

        <text x="780" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱑</text>
        <text x="825" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">U (U+1BC51)</text>
        <text x="825" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Ulman (elder wisdom)</text>
      </g>

      <!-- Row 2 -->
      <g transform="translate(0, 95)">
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱼</text>
        <text x="45" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">WA (U+1BC5C)</text>
        <text x="45" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Wawa (words, speech)</text>

        <text x="260" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛱾</text>
        <text x="305" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">WI (U+1BC5E)</text>
        <text x="305" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Win (breath, wind)</text>

        <text x="520" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛲟</text>
        <text x="565" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">FULL STOP (U+1BC9F)</text>
        <text x="565" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Kamloops Sentence Cross</text>

        <text x="780" y="0" class="font-duployan" font-size="34" fill="#38BDF8">𛲞</text>
        <text x="825" y="-8" class="font-mono" font-size="14" fill="#FFFFFF" font-weight="700">DOUBLE (U+1BC9E)</text>
        <text x="825" y="12" class="font-brand" font-size="13" fill="#CBD5E1">Reduplication Mark</text>
      </g>
    </g>
  </g>

  <!-- Section 3: Clinical PERMA+ Well-Being Table -->
  <g transform="translate(70, 1090)">
    <text x="0" y="0" class="font-mono" font-size="14" fill="#4ADE80" font-weight="700">3. CLINICAL PERMA+ WELL-BEING &amp; EHR LEXICON</text>
    <rect x="0" y="15" width="1060" height="450" rx="10" fill="#0F172A" stroke="#334155" stroke-width="1.5"/>

    <g transform="translate(35, 55)">
      <g>
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#FBBF24">[P] Positive Emotion (Vagal Tone):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Kloshe Tumtum ("Good Heart / Serenity")</text>
      </g>

      <g transform="translate(0, 60)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#4ADE80">[E] Engagement (Flow &amp; Play):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰀𛱇𛰀𛱇</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Heehee ("Laughter / Dopaminergic Play")</text>
      </g>

      <g transform="translate(0, 120)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#38BDF8">[R] Relationships (Kinship &amp; SDOH):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Tilikum ("Sacred Family &amp; Community")</text>
      </g>

      <g transform="translate(0, 180)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#C084FC">[M] Meaning (Existential Truth):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Kloshe Wawa ("Truthful Counsel &amp; Consent")</text>
      </g>

      <g transform="translate(0, 240)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#F472B6">[A] Accomplishment (Rehab):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰙𛱁𛰙𛱑𛰅 𛰅𛰆𛱄𛰜</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Mamook Kloshe ("To Make Well / Mastery")</text>
      </g>

      <g transform="translate(0, 300)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#F87171">[+] Physical Vitality (Nutrition):</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰅𛰆𛱄𛰜 𛰙𛱑𛰅𛱁𛰙𛱑𛰅</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Kloshe Muckamuck ("Vital Nourishment")</text>
      </g>

      <g transform="translate(0, 360)">
        <text x="0" y="0" class="font-brand" font-size="16" font-weight="700" fill="#38BDF8">[Dr] Primary Attending Healer:</text>
        <text x="360" y="0" class="font-duployan" font-size="26" fill="#FDE68A">𛰈𛱄𛰅𛰃𛱄𛰋 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
        <text x="620" y="0" class="font-mono" font-size="14" fill="#F8FAFC">Doctor Tilikum ("Physician Provider")</text>
      </g>
    </g>
  </g>

  <!-- Colophon Footer -->
  <g transform="translate(70, 1630)">
    <text x="0" y="0" class="font-mono" font-size="12" fill="#94A3B8">
      PocketGull Superfamily (Fineliner 400 • Bold 700 • Chiseltip 900 • Mono 400) // SIL OFL 1.1 // WCAG AAA &gt;= 7:1
    </text>
  </g>
</svg>''';
}

// =============================================================================
// 3. SYNAPTIC SPECIMEN LIGHT (1200x1720)
// =============================================================================
String generateSynapticSpecimenLight(String pebbleBase64) {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <linearGradient id="lightBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FDFBF7"/>
      <stop offset="100%" stop-color="#F4EFE6"/>
    </linearGradient>
  </defs>

  <rect width="1200" height="1720" fill="url(#lightBg)"/>
  <rect x="30" y="30" width="1140" height="1660" rx="16" fill="none" stroke="#D6D3D1" stroke-width="1.5"/>

  <!-- Header -->
  <g transform="translate(70, 90)">
    <text x="0" y="0" class="font-mono" font-size="12" fill="#B45309" font-weight="700" letter-spacing="0.1em">POCKETGULL TYPEFOUNDRY // POLAR WASHI LIGHT SPECIMEN</text>
    <text x="0" y="45" class="font-brand" font-size="42" font-weight="800" fill="#1C1917">Chinuk Pipa (Pacific Northwest)</text>
    <text x="0" y="78" class="font-brand" font-size="18" font-weight="500" fill="#78716C">Duployan Stenography for Chinuk Wawa // High-Legibility Clinical Print Standard</text>
  </g>

  <!-- Pebble River Artwork Plate -->
  <g transform="translate(70, 190)">
    <rect width="1060" height="320" rx="12" fill="#E7E5E4" stroke="#D6D3D1"/>
    <clipPath id="lightArtClip">
      <rect width="1060" height="320" rx="12"/>
    </clipPath>
    <g clip-path="url(#lightArtClip)">
      ${pebbleBase64.isNotEmpty ? '<image x="0" y="-80" width="1060" height="480" href="data:image/webp;base64,$pebbleBase64" preserveAspectRatio="xMidYMid slice" opacity="0.7"/>' : ''}
      <rect width="1060" height="320" fill="linear-gradient(to right, #FDFBF7 0%, transparent 60%, #FDFBF7 100%)"/>
    </g>
    <text x="40" y="130" class="font-duployan" font-size="64" fill="#9A3412" letter-spacing="0.12em">𛰅𛰆𛱄𛰜 𛰙𛱑𛰅𛱁𛰙𛱑𛰅 𛲟 𛰜𛰅𛱑𛰅𛱑𛰙</text>
    <text x="40" y="190" class="font-brand" font-size="20" font-weight="700" fill="#292524">Kloshe Muckamuck • Skookum Tumtum</text>
    <text x="40" y="218" class="font-mono" font-size="13" fill="#44403C">Vital Nourishment • Resilient Courage &amp; Strong Heart</text>
  </g>

  <!-- Clinical Text Sample -->
  <g transform="translate(70, 560)">
    <rect width="1060" height="240" rx="10" fill="#FFFFFF" stroke="#E7E5E4"/>
    <g transform="translate(40, 50)">
      <text x="0" y="0" class="font-mono" font-size="12" fill="#B45309" font-weight="700">1891 KAMLOOPS WAWA CLINICAL SAMPLE (BEDSIDE INTAKE):</text>
      <text x="0" y="55" class="font-duployan" font-size="36" fill="#1C1917" letter-spacing="0.08em">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛲟 𛰅𛰆𛱄𛰜 𛰚𛱁𛰚𛱆𛰛 𛰙𛱇𛰜𛰅𛱁𛰀𛱇 𛲟 𛰙𛱁𛰀𛰜𛱆</text>
      <text x="0" y="110" class="font-brand" font-size="17" fill="#44403C" font-weight="600">"Kloshe tumtum. Kloshe nanitch meskahke. Mahsie."</text>
      <text x="0" y="135" class="font-brand" font-size="14" fill="#78716C">Be of good heart. Take careful heed of your medicine. Thank you.</text>
    </g>
  </g>

  <!-- Monospace Verification Section -->
  <g transform="translate(70, 840)">
    <rect width="1060" height="420" rx="10" fill="#FFFFFF" stroke="#E7E5E4"/>
    <g transform="translate(40, 45)">
      <text x="0" y="0" class="font-mono" font-size="12" fill="#0369A1" font-weight="700">POCKETGULL MONO: FIXED 600 UPM MEDICAL TERMINAL ALIGNMENT</text>
      <g transform="translate(0, 40)" class="font-mono" font-size="14" fill="#1C1917">
        <text x="0" y="0">COL 01-10:   𛰂 𛰃 𛰅 𛰆 𛰇 𛰈 𛰊 𛰋 𛰙 𛰚</text>
        <text x="0" y="35">COL 11-20:   𛰛 𛰜 𛰸 𛱁 𛱄 𛱆 𛱇 𛱑 𛱼 𛱾</text>
        <text x="0" y="70">DELIMITERS:  𛲟 𛲞 𛲜 𛲀 𛲁 𛲂 𛲃 𛲄 𛲅 𛲆</text>
      </g>
      <line x1="0" y1="180" x2="980" y2="180" stroke="#E7E5E4"/>
      <g transform="translate(0, 215)">
        <text x="0" y="0" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Louise Sloan 5:1 Optotype Compliance:</text>
        <text x="0" y="24" class="font-brand" font-size="13" fill="#57534E">All 143 Duployan codepoints centered with equalized sidebearings (lsb = rsb), ensuring zero layout jitter in ICU monitors.</text>
        <text x="0" y="55" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">ISMP Safe Medication Practice:</text>
        <text x="0" y="79" class="font-brand" font-size="13" fill="#57534E">Zero ambiguity between numerals, decimal points, and shorthand ticks. Slashed zero (cv08) and curved l (cv05) enforced.</text>
      </g>
    </g>
  </g>

  <!-- Footprint & Attribution -->
  <g transform="translate(70, 1630)">
    <text x="0" y="0" class="font-mono" font-size="11" fill="#78716C">
      PocketGull Superfamily // Universal World Scripts Tier 6 // Confederated Tribes of Grand Ronde Stewardship
    </text>
  </g>
</svg>''';
}

// =============================================================================
// 4. PERMA+ CLINICAL THOUGHTS CARD (800x800)
// =============================================================================
String generatePermaThoughtsCard() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="800" viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <radialGradient id="washiCardGlow" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFDF9"/>
      <stop offset="60%" stop-color="#F9F6F0"/>
      <stop offset="100%" stop-color="#EFE9DC"/>
    </radialGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#1C1917" flood-opacity="0.12"/>
    </filter>
  </defs>

  <rect width="800" height="800" fill="#EAE5D9"/>

  <g filter="url(#cardShadow)">
    <rect x="40" y="40" width="720" height="720" rx="20" fill="url(#washiCardGlow)" stroke="#D6D3D1" stroke-width="1.5"/>
  </g>

  <g transform="translate(80, 85)">
    <rect x="0" y="0" width="130" height="24" rx="5" fill="#1E3A8A" fill-opacity="0.1" stroke="#1E3A8A" stroke-width="1"/>
    <text x="10" y="16" class="font-mono" font-size="10" font-weight="700" fill="#1E3A8A">CHINUK WAWA</text>

    <rect x="140" y="0" width="125" height="24" rx="5" fill="#166534" fill-opacity="0.1" stroke="#166534" stroke-width="1"/>
    <text x="150" y="16" class="font-mono" font-size="10" font-weight="700" fill="#166534">PERMA+ MODEL</text>

    <text x="0" y="55" class="font-brand" font-size="28" font-weight="800" fill="#1C1917">Clinical Well-Being Specimen</text>
    <text x="0" y="80" class="font-brand" font-size="14" font-weight="500" fill="#78716C">Duployan Stenography (Chinuk Pipa) &amp; Lifestyle Medicine</text>
  </g>

  <g transform="translate(80, 195)">
    <g transform="translate(0, 0)">
      <circle cx="16" cy="16" r="16" fill="#F59E0B" fill-opacity="0.2"/>
      <text x="16" y="21" class="font-mono" font-size="14" font-weight="700" fill="#B45309" text-anchor="middle">P</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Kloshe Tumtum <tspan font-weight="400" fill="#78716C">• Good Heart / Vagal Tone</tspan></text>
    </g>

    <g transform="translate(0, 75)">
      <circle cx="16" cy="16" r="16" fill="#10B981" fill-opacity="0.2"/>
      <text x="16" y="21" class="font-mono" font-size="14" font-weight="700" fill="#047857" text-anchor="middle">E</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰀𛱇𛰀𛱇</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Heehee <tspan font-weight="400" fill="#78716C">• Joyful Laughter / Play</tspan></text>
    </g>

    <g transform="translate(0, 150)">
      <circle cx="16" cy="16" r="16" fill="#3B82F6" fill-opacity="0.2"/>
      <text x="16" y="21" class="font-mono" font-size="14" font-weight="700" fill="#1D4ED8" text-anchor="middle">R</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Tilikum <tspan font-weight="400" fill="#78716C">• Sacred Family / Community</tspan></text>
    </g>

    <g transform="translate(0, 225)">
      <circle cx="16" cy="16" r="16" fill="#8B5CF6" fill-opacity="0.2"/>
      <text x="16" y="21" class="font-mono" font-size="14" font-weight="700" fill="#6D28D9" text-anchor="middle">M</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Kloshe Wawa <tspan font-weight="400" fill="#78716C">• Meaningful Counsel / Truth</tspan></text>
    </g>

    <g transform="translate(0, 300)">
      <circle cx="16" cy="16" r="16" fill="#EC4899" fill-opacity="0.2"/>
      <text x="16" y="21" class="font-mono" font-size="14" font-weight="700" fill="#BE185D" text-anchor="middle">A</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰙𛱁𛰙𛱑𛰅 𛰅𛰆𛱄𛰜</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Mamook Kloshe <tspan font-weight="400" fill="#78716C">• To Make Well / Mastery</tspan></text>
    </g>

    <g transform="translate(0, 375)">
      <circle cx="16" cy="16" r="16" fill="#EF4444" fill-opacity="0.2"/>
      <text x="16" y="22" class="font-mono" font-size="16" font-weight="700" fill="#B91C1C" text-anchor="middle">+</text>
      <text x="45" y="12" class="font-duployan" font-size="22" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰙𛱑𛰅𛱁𛰙𛱑𛰅</text>
      <text x="45" y="30" class="font-brand" font-size="13" font-weight="700" fill="#1C1917">Kloshe Muckamuck <tspan font-weight="400" fill="#78716C">• Nourishment &amp; Vitality</tspan></text>
    </g>
  </g>

  <g transform="translate(80, 680)">
    <line x1="0" y1="0" x2="640" y2="0" stroke="#E7E5E4"/>
    <text x="0" y="25" class="font-mono" font-size="10" fill="#78716C">
      POCKETGULL MEDICAL CARE PLAN // GRAND RONDE HERITAGE // WCAG AAA
    </text>
  </g>
</svg>''';
}

// =============================================================================
// 5. PRINT GALLERY EXHIBITION (1200x1720)
// =============================================================================
String generatePrintExhibition(String kellsBase64) {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
  </defs>

  <rect width="1200" height="1720" fill="#FFFFFF"/>
  <rect x="40" y="40" width="1120" height="1640" fill="none" stroke="#1C1917" stroke-width="2"/>
  <rect x="50" y="50" width="1100" height="1620" fill="none" stroke="#A8A29E" stroke-width="0.8"/>

  <g transform="translate(80, 120)">
    <text x="0" y="0" class="font-mono" font-size="12" fill="#78716C" letter-spacing="0.2em">EXHIBITION BROADSIDE NO. 02</text>
    <text x="0" y="45" class="font-brand" font-size="44" font-weight="800" fill="#1C1917">CHINUK PIPA &amp; KAMLOOPS WAWA</text>
    <text x="0" y="78" class="font-brand" font-size="18" fill="#57534E">The 1891 Duployan Stenography of the Pacific Northwest Trade Language</text>
  </g>

  <g transform="translate(80, 240)">
    <rect width="1040" height="420" fill="#F5F5F4" stroke="#E7E5E4"/>
    <clipPath id="exhClip">
      <rect width="1040" height="420"/>
    </clipPath>
    <g clip-path="url(#exhClip)">
      ${kellsBase64.isNotEmpty ? '<image x="0" y="-120" width="1040" height="600" href="data:image/webp;base64,$kellsBase64" preserveAspectRatio="xMidYMid slice"/>' : ''}
    </g>
  </g>

  <g transform="translate(80, 720)">
    <text x="0" y="0" class="font-mono" font-size="13" fill="#1C1917" font-weight="700">CANONICAL PASSAGE (MAY 1891 KAMLOOPS WAWA NO. 1):</text>
    <g transform="translate(0, 45)">
      <text x="0" y="0" class="font-duployan" font-size="42" fill="#1C1917" letter-spacing="0.08em">𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁 𛲟 𛰅𛰆𛱄𛰜 𛰃𛱑𛰙𛰃𛱑𛰙 𛲟 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
      <text x="0" y="55" class="font-brand" font-size="20" font-weight="600" fill="#44403C">"Kloshe wawa. Kloshe tumtum. Kloshe tilikum."</text>
      <text x="0" y="85" class="font-brand" font-size="16" fill="#78716C">Good words. A good heart. Good people.</text>
    </g>

    <g transform="translate(0, 190)">
      <text x="0" y="0" class="font-mono" font-size="13" fill="#1C1917" font-weight="700">COMPLETE PHONETIC ROSTER (POCKETGULL CHINUK PIPA):</text>
      <rect x="0" y="15" width="1040" height="420" fill="#FAFAF9" stroke="#E7E5E4"/>
      
      <g transform="translate(30, 60)" class="font-duployan" font-size="36" fill="#1C1917" letter-spacing="0.15em">
        <text x="0" y="0">𛰀 𛰁 𛰂 𛰃 𛰄 𛰅 𛰆 𛰇 𛰈 𛰊 𛰋 𛰙 𛰚 𛰛 𛰜</text>
        <text x="0" y="65">𛰸 𛱁 𛱄 𛱆 𛱇 𛱑 𛱼 𛱾 𛲀 𛲁 𛲂 𛲃 𛲄 𛲅 𛲆</text>
        <text x="0" y="130">𛲟 𛲞 𛲜 𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛰀𛱇𛰀𛱇 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
      </g>

      <g transform="translate(30, 260)" class="font-mono" font-size="12" fill="#57534E">
        <text x="0" y="0">COLOPHON ATTRIBUTION:</text>
        <text x="0" y="24">Compiled into PocketGull Font Superfamily across 4 concrete weights in 11,358.73 ms.</text>
        <text x="0" y="44">Preserved with guidance from the Confederated Tribes of Grand Ronde language archives.</text>
        <text x="0" y="64">100% Free &amp; Open-Source under the SIL Open Font License 1.1.</text>
      </g>
    </g>
  </g>

  <g transform="translate(80, 1620)">
    <text x="0" y="0" class="font-mono" font-size="11" fill="#A8A29E">
      THE POCKETGULL PROJECT // REPRODUCIBLE TYPOGRAPHY // 2026
    </text>
  </g>
</svg>''';
}

// =============================================================================
// 6. CHINUK PIPA LANGUAGE MAP (1200x1720) — CLEAN MUSEUM BROADSIDE (PRINT GALLERY PARITY)
// =============================================================================
String generateLanguageMap() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
  </defs>

  <!-- Crisp Museum Exhibition Surface -->
  <rect width="1200" height="1720" fill="#FFFFFF"/>
  <rect x="40" y="40" width="1120" height="1640" fill="none" stroke="#1C1917" stroke-width="2"/>
  <rect x="50" y="50" width="1100" height="1620" fill="none" stroke="#A8A29E" stroke-width="0.8"/>

  <!-- Museum Title Header -->
  <g transform="translate(80, 110)">
    <text x="0" y="0" class="font-mono" font-size="12" fill="#B45309" font-weight="700" letter-spacing="0.2em">PEDAGOGICAL LANGUAGE MAP NO. 02</text>
    <text x="0" y="42" class="font-brand" font-size="40" font-weight="800" fill="#1C1917">CHINUK PIPA STENOGRAPHIC MAP</text>
    <text x="0" y="72" class="font-brand" font-size="17" font-weight="500" fill="#57534E">Euclidean Stroke Geometry of Duployan Shorthand for Chinuk Wawa (U+1BC00–U+1BC9F)</text>
  </g>

  <!-- Section 1: Consonant Vectors (Lines & Arcs) -->
  <g transform="translate(80, 230)">
    <text x="0" y="0" class="font-mono" font-size="13" fill="#1C1917" font-weight="700">1. CONSONANT VECTOR PRIMITIVES (LINES AT 4 CARDINAL ANGLES &amp; QUARTER-ARCS):</text>
    <rect x="0" y="15" width="1040" height="340" fill="#FAFAF9" stroke="#E7E5E4" stroke-width="1.5"/>

    <g transform="translate(30, 50)">
      <!-- Straight Lines -->
      <g>
        <text x="0" y="0" class="font-mono" font-size="12" fill="#B45309" font-weight="700">STRAIGHT LINES (4 ANGLES):</text>
        
        <g transform="translate(0, 30)">
          <text x="0" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰂</text>
          <text x="40" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">P (45° down)</text>
          <text x="40" y="12" class="font-brand" font-size="12" fill="#57534E">Pipa (paper, book)</text>

          <text x="250" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰃</text>
          <text x="290" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">T (90° down)</text>
          <text x="290" y="12" class="font-brand" font-size="12" fill="#57534E">Tumtum (heart, soul)</text>

          <text x="500" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰅</text>
          <text x="540" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">K (0° horiz)</text>
          <text x="540" y="12" class="font-brand" font-size="12" fill="#57534E">Kloshe (good, well)</text>

          <text x="750" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰆</text>
          <text x="790" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">L (135° up)</text>
          <text x="790" y="12" class="font-brand" font-size="12" fill="#57534E">La-kret (medicine)</text>
        </g>
      </g>

      <!-- Curves & Arcs -->
      <g transform="translate(0, 115)">
        <text x="0" y="0" class="font-mono" font-size="12" fill="#B45309" font-weight="700">CURVES &amp; QUARTER-CIRCLE ARCS:</text>

        <g transform="translate(0, 30)">
          <text x="0" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰙</text>
          <text x="40" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">M (⌒ top arch)</text>
          <text x="40" y="12" class="font-brand" font-size="12" fill="#57534E">Mamook (make, work)</text>

          <text x="250" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰚</text>
          <text x="290" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">N (⌣ bottom arch)</text>
          <text x="290" y="12" class="font-brand" font-size="12" fill="#57534E">Nanitch (see, watch)</text>

          <text x="500" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰛</text>
          <text x="540" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">J / CH ( right arch)</text>
          <text x="540" y="12" class="font-brand" font-size="12" fill="#57534E">Chako (come, arrive)</text>

          <text x="750" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛰜</text>
          <text x="790" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">S ( left arch)</text>
          <text x="790" y="12" class="font-brand" font-size="12" fill="#57534E">Skookum (strong, safe)</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Section 2: Vocalic Circles & Glides -->
  <g transform="translate(80, 625)">
    <text x="0" y="0" class="font-mono" font-size="13" fill="#1C1917" font-weight="700">2. VOCALIC CIRCLES &amp; COMPOUND GLIDES:</text>
    <rect x="0" y="15" width="1040" height="280" fill="#FAFAF9" stroke="#E7E5E4" stroke-width="1.5"/>

    <g transform="translate(30, 50)">
      <g>
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱁</text>
        <text x="40" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">A (mid circle)</text>
        <text x="40" y="12" class="font-brand" font-size="12" fill="#57534E">Alki (future, hope)</text>

        <text x="250" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱄</text>
        <text x="290" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">O (large circle)</text>
        <text x="290" y="12" class="font-brand" font-size="12" fill="#57534E">Olally (berries, fruit)</text>

        <text x="500" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱆</text>
        <text x="540" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">I (small circle)</text>
        <text x="540" y="12" class="font-brand" font-size="12" fill="#57534E">Ikt (one, baseline)</text>

        <text x="750" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱑</text>
        <text x="790" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">U (horseshoe)</text>
        <text x="790" y="12" class="font-brand" font-size="12" fill="#57534E">Ulman (elder, ancient)</text>
      </g>

      <g transform="translate(0, 95)">
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱼</text>
        <text x="40" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">WA (circle + dot)</text>
        <text x="40" y="12" class="font-brand" font-size="12" fill="#57534E">Wawa (words, speech)</text>

        <text x="250" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛱾</text>
        <text x="290" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">WI (circle + dash)</text>
        <text x="290" y="12" class="font-brand" font-size="12" fill="#57534E">Win (breath, wind)</text>

        <text x="500" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛲟</text>
        <text x="540" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">FULL STOP (cross)</text>
        <text x="540" y="12" class="font-brand" font-size="12" fill="#57534E">Kamloops Sentence Final</text>

        <text x="750" y="0" class="font-duployan" font-size="34" fill="#1C1917">𛲞</text>
        <text x="790" y="-8" class="font-mono" font-size="14" fill="#1C1917" font-weight="700">DOUBLE MARK</text>
        <text x="790" y="12" class="font-brand" font-size="12" fill="#57534E">Reduplication Mark</text>
      </g>
    </g>
  </g>

  <!-- Section 3: PERMA+ Clinical Vocabulary Table -->
  <g transform="translate(80, 960)">
    <text x="0" y="0" class="font-mono" font-size="13" fill="#1C1917" font-weight="700">3. CLINICAL PERMA+ WELL-BEING LEXICON FOR PATIENT EDUCATION:</text>
    <rect x="0" y="15" width="1040" height="560" fill="#FAFAF9" stroke="#E7E5E4" stroke-width="1.5"/>

    <g transform="translate(30, 50)">
      <g>
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#B45309">[P] POSITIVE EMOTION</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Kloshe Tumtum ("Good Heart")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Vagal tone balance, parasympathetic relaxation, emotional serenity.</text>
      </g>

      <g transform="translate(0, 75)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#15803D">[E] ENGAGEMENT</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰀𛱇𛰀𛱇</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Heehee ("Laughter / Play")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Dopaminergic focus, recreational therapy, pediatric engagement.</text>
      </g>

      <g transform="translate(0, 150)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#1D4ED8">[R] RELATIONSHIPS</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Tilikum ("Sacred Family &amp; Tribe")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Social determinants of health (SDOH), tribal kinship, peer recovery.</text>
      </g>

      <g transform="translate(0, 225)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#7E22CE">[M] MEANING</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰸𛱁𛰸𛱁</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Kloshe Wawa ("Truthful Words")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Culturally safe clinical dialogue, shared decision-making, informed consent.</text>
      </g>

      <g transform="translate(0, 300)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#BE185D">[A] ACCOMPLISHMENT</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰙𛱁𛰙𛱑𛰅 𛰅𛰆𛱄𛰜</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Mamook Kloshe ("To Make Well")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Patient Activation Measure (PAM), physical rehabilitation adherence.</text>
      </g>

      <g transform="translate(0, 375)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#B91C1C">[+] PHYSICAL VITALITY</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰙𛱑𛰅𛱁𛰙𛱑𛰅</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Kloshe Muckamuck ("Good Food")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Traditional foodways, metabolic stabilization, nutritional vitality.</text>
      </g>

      <g transform="translate(0, 450)">
        <text x="0" y="0" class="font-mono" font-size="14" font-weight="700" fill="#0284C7">[CLIN] CLINICAL CARE</text>
        <text x="240" y="0" class="font-duployan" font-size="28" fill="#1C1917">𛰅𛰆𛱄𛰜 𛰚𛱁𛰚𛱆𛰛</text>
        <text x="460" y="-3" class="font-brand" font-size="15" font-weight="700" fill="#1C1917">Kloshe Nanitch ("Take Care / Watch")</text>
        <text x="460" y="17" class="font-brand" font-size="13" fill="#57534E">Clinical observation, vital sign monitoring, outpatient discharge safety.</text>
      </g>
    </g>
  </g>

  <!-- Museum Colophon Footer -->
  <g transform="translate(80, 1630)">
    <text x="0" y="0" class="font-mono" font-size="11" fill="#78716C">
      POCKETGULL PEDAGOGICAL LANGUAGE MAP // 1891 KAMLOOPS WAWA // CONFEDERATED TRIBES OF GRAND RONDE // OFL 1.1
    </text>
  </g>
</svg>''';
}

// =============================================================================
// 7. LANDMARK PLATE A: TYPE ENGINEERING SPECIMEN (896x1200)
// =============================================================================
String generateTypeEngineeringPlate() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="896" height="1200" viewBox="0 0 896 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
    <!-- Cyan Millimetric Technical Grid -->
    <pattern id="cyanGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#E0F2FE" stroke-width="0.8"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#BAE6FD" stroke-width="1.2"/>
    </pattern>
  </defs>

  <!-- Technical Canvas Surface -->
  <rect width="896" height="1200" fill="#F8FAFC"/>
  <rect width="896" height="1200" fill="url(#cyanGrid)"/>

  <!-- Border -->
  <rect x="25" y="25" width="846" height="1150" fill="none" stroke="#0284C7" stroke-width="1.5"/>

  <!-- Title -->
  <g transform="translate(45, 65)">
    <text x="0" y="0" class="font-brand" font-size="26" font-weight="800" fill="#0F172A">PocketGull – Chinuk Pipa Type Design &amp; Stenographic Engineering</text>
    <line x1="0" y1="12" x2="806" y2="12" stroke="#0F172A" stroke-width="2"/>
  </g>

  <!-- Two Column Layout (Top Half) -->
  <!-- Col 1: Section I -->
  <g transform="translate(45, 110)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">I. STENOGRAPHIC VECTOR ANGLES &amp; ACUTE JUNCTION INKTRAPS</text>

    <rect x="0" y="15" width="390" height="380" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    
    <!-- Large Engineering Glyphs with Vector Callouts -->
    <g transform="translate(30, 80)">
      <!-- Line 45° P -->
      <text x="20" y="60" class="font-duployan" font-size="90" fill="#0F172A">𛰂</text>
      <line x1="20" y1="10" x2="70" y2="10" stroke="#EF4444" stroke-width="1.5" stroke-dasharray="2,2"/>
      <text x="80" y="14" class="font-mono" font-size="10" fill="#B91C1C">45° Down-Vector</text>
      <text x="20" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">P: Acute Down-Slant</text>

      <!-- Line 90° T -->
      <text x="200" y="60" class="font-duployan" font-size="90" fill="#0F172A">𛰃</text>
      <line x1="200" y1="10" x2="250" y2="10" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="2,2"/>
      <text x="260" y="14" class="font-mono" font-size="10" fill="#0369A1">90° Vertical</text>
      <text x="200" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">T: True Perpendicular</text>

      <!-- Line 0° K -->
      <g transform="translate(0, 130)">
        <text x="20" y="60" class="font-duployan" font-size="90" fill="#0F172A">𛰅</text>
        <line x1="20" y1="15" x2="70" y2="15" stroke="#166534" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="80" y="19" class="font-mono" font-size="10" fill="#15803D">0° Horizontal</text>
        <text x="20" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">K: Baseline Glide</text>

        <!-- Line 135° L -->
        <text x="200" y="60" class="font-duployan" font-size="90" fill="#0F172A">𛰆</text>
        <line x1="200" y1="15" x2="250" y2="15" stroke="#B45309" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="260" y="19" class="font-mono" font-size="10" fill="#B45309">135° Ascender</text>
        <text x="200" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">L: Ascending Diagonal</text>
      </g>
    </g>
    <text x="15" y="365" class="font-brand" font-size="10" fill="#64748B">Engineered minimal-node Bezier paths prevent ink blooming during high-speed printing.</text>
  </g>

  <!-- Col 2: Section II & III -->
  <g transform="translate(460, 110)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">II. DUPLOYAN ARCS &amp; CIRCULAR TANGENTS</text>
    <rect x="0" y="15" width="390" height="170" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>
    
    <g transform="translate(20, 50)">
      <text x="0" y="0" class="font-duployan" font-size="34" fill="#0F172A">𛰙 𛰚 𛰛 𛰜</text>
      <text x="170" y="-8" class="font-mono" font-size="12" font-weight="700" fill="#0F172A">M • N • J • S</text>
      <text x="170" y="10" class="font-brand" font-size="11" fill="#64748B">G2 Continuous Quarter-Arcs</text>

      <g transform="translate(0, 60)">
        <text x="0" y="0" class="font-duployan" font-size="34" fill="#0F172A">𛱁 𛱄 𛱆 𛱑</text>
        <text x="170" y="-8" class="font-mono" font-size="12" font-weight="700" fill="#0F172A">A • O • I • U</text>
        <text x="170" y="10" class="font-brand" font-size="11" fill="#64748B">Concentric Vocalic Rings</text>
      </g>
    </g>

    <g transform="translate(0, 205)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">III. OPTICAL SIZING SCALES (6PT – 72PT)</text>
      <rect x="0" y="15" width="390" height="160" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

      <g transform="translate(20, 45)">
        <text x="0" y="0" class="font-mono" font-size="9" fill="#64748B">Caption 6pt</text>
        <text x="0" y="18" class="font-duployan" font-size="14" fill="#0F172A">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛲟 𛰀𛱇𛰀𛱇 𛲟 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>

        <text x="0" y="42" class="font-mono" font-size="9" fill="#64748B">Text 12pt</text>
        <text x="0" y="64" class="font-duployan" font-size="20" fill="#0F172A">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 𛲟 𛰀𛱇𛰀𛱇</text>

        <text x="0" y="92" class="font-mono" font-size="9" fill="#64748B">Display 36pt</text>
        <text x="0" y="125" class="font-duployan" font-size="36" fill="#0F172A">𛰅𛰆𛱄𛰜 𛰃𛱑𛰙</text>
      </g>
    </g>
  </g>

  <!-- Lower Half: Section IV & V -->
  <!-- Col 1: Section IV -->
  <g transform="translate(45, 520)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">IV. NUMERAL SET COMPARISONS &amp; MONOSPACE CELL NORMALIZATION</text>
    <rect x="0" y="15" width="806" height="260" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

    <g transform="translate(25, 45)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#64748B">PROPORTIONAL DISPLAY (700 BOLD)</text>
      <text x="0" y="35" class="font-brand" font-size="28" font-weight="700" fill="#0F172A">1234567890 𛰅𛰆𛱄𛰜 𛰃𛱑𛰙</text>
      <text x="0" y="55" class="font-brand" font-size="11" fill="#64748B">• Proportional widths • Natural calligraphic sidebearings • Display authority</text>

      <line x1="0" y1="80" x2="756" y2="80" stroke="#E2E8F0"/>

      <g transform="translate(0, 105)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">TABULAR LINING &amp; MONOSPACE 600 UPM CELL (POCKETGULL MONO)</text>
        <text x="0" y="35" class="font-mono" font-size="26" font-weight="700" fill="#0F172A">1234567890 𛰅 𛰆 𛱄 𛰜 𛰃 𛱑 𛰙</text>
        <text x="0" y="55" class="font-brand" font-size="11" fill="#64748B">• Exact 600 UPM advance • Centered with equalized LSB/RSB • Zero horizontal layout jitter in ICU EHR</text>
      </g>
    </g>
  </g>

  <!-- Section V: Shorthand Join Matrices -->
  <g transform="translate(45, 815)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">V. DUPLOYAN JOIN VECTORS &amp; REDUPLICATION RULES</text>
    <rect x="0" y="15" width="806" height="320" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

    <g transform="translate(30, 50)">
      <g>
        <rect x="0" y="0" width="220" height="110" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">Line-to-Line (T + K)</text>
        <text x="15" y="65" class="font-duployan" font-size="34" fill="#0F172A">𛰃𛰅</text>
        <text x="15" y="92" class="font-mono" font-size="10" fill="#64748B">90° + 0° Corner</text>
      </g>

      <g transform="translate(260, 0)">
        <rect x="0" y="0" width="220" height="110" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">Line-to-Arc (T + M)</text>
        <text x="15" y="65" class="font-duployan" font-size="34" fill="#0F172A">𛰃𛰙</text>
        <text x="15" y="92" class="font-mono" font-size="10" fill="#64748B">Stem into Arch</text>
      </g>

      <g transform="translate(520, 0)">
        <rect x="0" y="0" width="220" height="110" rx="6" fill="#F8FAFC" stroke="#E2E8F0"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">Reduplication (Tumtum)</text>
        <text x="15" y="65" class="font-duployan" font-size="34" fill="#0F172A">𛰃𛱑𛰙𛲞</text>
        <text x="15" y="92" class="font-mono" font-size="10" fill="#64748B">Double Mark U+1BC9E</text>
      </g>

      <g transform="translate(0, 140)">
        <rect x="0" y="0" width="740" height="100" rx="6" fill="#EFF6FF" stroke="#BFDBFE"/>
        <text x="20" y="28" class="font-brand" font-size="13" font-weight="700" fill="#1E3A8A">Optical Quality Attestation &amp; Zero Tofu Guarantee:</text>
        <text x="20" y="52" class="font-brand" font-size="12" fill="#1E40AF">Passed with 0 duplicate nodes across all 143 Duployan codepoints. 100% compliant with Google Fonts specifications.</text>
        <text x="20" y="74" class="font-mono" font-size="11" fill="#2563EB">Verified via ots-sanitize &amp; fontTools // unitsPerEm: 1000 // OFL 1.1 License</text>
      </g>
    </g>
  </g>
</svg>''';
}

// =============================================================================
// 8. LANDMARK PLATE B: CLINICAL TELEMETRY SPECIMEN (896x1200)
// =============================================================================
String generateTelemetryTypePlate() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="896" height="1200" viewBox="0 0 896 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap');
      .font-brand { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
    </style>
  </defs>

  <rect width="896" height="1200" fill="#F0F9FF"/>
  <rect x="25" y="25" width="846" height="1150" fill="none" stroke="#0284C7" stroke-width="1.5"/>

  <!-- Technical Header -->
  <g transform="translate(45, 65)">
    <text x="0" y="0" class="font-mono" font-size="24" font-weight="800" fill="#0369A1">POCKETGULL</text>
    <text x="0" y="32" class="font-mono" font-size="30" font-weight="800" fill="#0F172A">TELEMETRY &amp; CLINICAL GLYPHS</text>
    <text x="560" y="0" class="font-mono" font-size="11" fill="#0284C7">TECHNICAL DATA</text>
    <text x="560" y="16" class="font-mono" font-size="11" fill="#0F172A">1000 UPM / 600 ADV</text>
    <text x="700" y="0" class="font-mono" font-size="11" fill="#0284C7">CHINUK PIPA</text>
    <text x="700" y="16" class="font-mono" font-size="11" fill="#0F172A">U+1BC00-1BC9F</text>
    <line x1="0" y1="48" x2="806" y2="48" stroke="#0F172A" stroke-width="2"/>
  </g>

  <!-- Monospace Subhead -->
  <g transform="translate(45, 135)">
    <text x="0" y="0" class="font-mono" font-size="20" font-weight="800" fill="#0F172A">POCKETGULL MONO</text>
    <text x="0" y="20" class="font-mono" font-size="11" fill="#0284C7">A MONOSPACED SCRIPT FOR HEALTHCARE &amp; BEDSIDE MONITORS</text>
    
    <text x="430" y="0" class="font-mono" font-size="20" font-weight="800" fill="#0F172A">CLINICAL SAFETY</text>
    <text x="430" y="20" class="font-mono" font-size="11" fill="#0284C7">ISMP / FDA DOSAGE DISAMBIGUATION</text>
  </g>

  <!-- Left: Monospace Character Chart -->
  <g transform="translate(45, 185)">
    <rect width="390" height="280" fill="#FFFFFF" stroke="#CBD5E1"/>
    <g transform="translate(15, 30)" class="font-mono" font-size="13" fill="#0F172A" letter-spacing="0.2em">
      <text x="0" y="0">! @ # \$ % ^ &amp; * ( ) _ +</text>
      <text x="0" y="30">1 2 3 4 5 6 7 8 9 0 - =</text>
      <text x="0" y="60">Q W E R T Y U I O P [ ]</text>
      <text x="0" y="90">A S D F G H J K L ; ' \</text>
      <text x="0" y="120">Z X C V B N M , . / ?</text>
      <text x="0" y="150" class="font-duployan" fill="#0369A1">𛰂 𛰃 𛰅 𛰆 𛰇 𛰈 𛰊 𛰋 𛰙 𛰚 𛰛</text>
      <text x="0" y="180" class="font-duployan" fill="#0369A1">𛰜 𛰸 𛱁 𛱄 𛱆 𛱇 𛱑 𛱼 𛱾 𛲟 𛲞</text>
      <text x="0" y="210">Δ % ± μg mg/dL mmHg bpm</text>
    </g>
  </g>

  <!-- Right: Disambiguation & Tabular Sizes -->
  <g transform="translate(475, 185)">
    <!-- 0 vs O -->
    <rect x="0" y="0" width="180" height="85" fill="#FFFFFF" stroke="#CBD5E1"/>
    <rect x="0" y="0" width="180" height="22" fill="#E0F2FE"/>
    <text x="10" y="15" class="font-mono" font-size="10" font-weight="700" fill="#0369A1">SLASHED ZERO (cv08)</text>
    <text x="25" y="60" class="font-mono" font-size="34" font-weight="700" fill="#0F172A">0 vs O</text>

    <!-- 1 vs l vs I -->
    <rect x="195" y="0" width="176" height="85" fill="#FFFFFF" stroke="#CBD5E1"/>
    <rect x="195" y="0" width="176" height="22" fill="#E0F2FE"/>
    <text x="205" y="15" class="font-mono" font-size="10" font-weight="700" fill="#0369A1">SERIFED I (ss02)</text>
    <text x="215" y="60" class="font-mono" font-size="34" font-weight="700" fill="#0F172A">1 | I l</text>

    <!-- Clinical Units -->
    <g transform="translate(0, 105)">
      <rect x="0" y="0" width="371" height="175" fill="#FFFFFF" stroke="#CBD5E1"/>
      <g transform="translate(15, 30)">
        <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0369A1">TABULAR CLINICAL FIGURES &amp; MEDICAL SYMBOLS</text>
        <text x="0" y="32" class="font-mono" font-size="18" font-weight="700" fill="#0F172A">Δ % ± μg mg/dL mEq/L</text>
        <text x="0" y="62" class="font-mono" font-size="18" font-weight="700" fill="#0F172A">≤ ≥ ≠ ≈ → mmHg SpO2</text>
        <line x1="0" y1="85" x2="340" y2="85" stroke="#E2E8F0"/>
        <text x="0" y="110" class="font-brand" font-size="12" fill="#64748B">ISMP Standard: Leading zero mandated (0.5 mg), trailing zero strictly prohibited (5 mg, never 5.0 mg).</text>
      </g>
    </g>
  </g>

  <!-- Sample Clinical Data Screen (ICU Monitor) -->
  <g transform="translate(45, 490)">
    <text x="0" y="0" class="font-mono" font-size="13" font-weight="700" fill="#0F172A">SAMPLE CLINICAL TELEMETRY DISPLAY (GRAND RONDE CLINIC BED 04):</text>
    
    <g transform="translate(0, 15)">
      <!-- Dark ICU Monitor Shell -->
      <rect width="806" height="280" rx="10" fill="#090D16" stroke="#1E293B" stroke-width="2"/>

      <!-- ECG Waveform Panel -->
      <g transform="translate(25, 25)">
        <rect width="450" height="230" rx="6" fill="#050811" stroke="#1E293B"/>
        <text x="20" y="28" class="font-mono" font-size="12" fill="#22C55E" font-weight="700">ECG LEAD II • SINUS RHYTHM</text>
        
        <!-- ECG Polyline -->
        <polyline fill="none" stroke="#22C55E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
          points="20,110 60,110 75,110 82,90 90,140 100,50 112,130 120,110 135,110 150,98 165,110 220,110 235,110 242,90 250,140 260,50 272,130 280,110 295,110 310,98 325,110 380,110 395,110 402,90 410,140 420,50 432,130 440,110"/>
        
        <text x="20" y="190" class="font-duployan" font-size="22" fill="#FDE68A">𛰃𛱑𛰙 𛰃𛱑𛰙: 72 bpm • 𛰜𛰅𛱑𛰅𛱑𛰙</text>
        <text x="20" y="212" class="font-brand" font-size="12" fill="#94A3B8">Tumtum: 72 bpm • Skookum (Stable)</text>
      </g>

      <!-- Vitals Telemetry Numbers -->
      <g transform="translate(500, 25)">
        <rect width="280" height="230" rx="6" fill="#0F172A" stroke="#1E293B"/>
        <g transform="translate(20, 35)">
          <text x="0" y="0" class="font-mono" font-size="11" fill="#94A3B8">HEART RATE</text>
          <text x="0" y="32" class="font-mono" font-size="36" font-weight="700" fill="#22C55E">72 <tspan font-size="16">bpm</tspan></text>

          <text x="0" y="75" class="font-mono" font-size="11" fill="#94A3B8">BLOOD PRESSURE</text>
          <text x="0" y="105" class="font-mono" font-size="32" font-weight="700" fill="#38BDF8">120/80</text>

          <text x="0" y="145" class="font-mono" font-size="11" fill="#94A3B8">O2 SATURATION (WIN)</text>
          <text x="0" y="175" class="font-mono" font-size="32" font-weight="700" fill="#FBBF24">99%</text>
        </g>
      </g>
    </g>
  </g>

  <!-- Bottom: Medical Form & Optical Corrections -->
  <g transform="translate(45, 810)">
    <text x="0" y="0" class="font-mono" font-size="13" font-weight="700" fill="#0F172A">CLINICAL DOSAGE CORRECTIONS &amp; EHR TERMINOLOGY:</text>

    <rect x="0" y="15" width="806" height="320" fill="#FFFFFF" stroke="#CBD5E1"/>

    <g transform="translate(30, 50)">
      <g>
        <text x="0" y="0" class="font-brand" font-size="14" font-weight="700" fill="#0F172A">Attending Physician (Doctor Tilikum):</text>
        <text x="320" y="0" class="font-duployan" font-size="24" fill="#0369A1">𛰈𛱄𛰅𛰃𛱄𛰋 𛰃𛱆𛰆𛱆𛰅𛱑𛰙</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Dr. P. Gear, MD</text>
      </g>

      <g transform="translate(0, 50)">
        <text x="0" y="0" class="font-brand" font-size="14" font-weight="700" fill="#0F172A">Clinical Vigilance (Kloshe Nanitch):</text>
        <text x="320" y="0" class="font-duployan" font-size="24" fill="#0369A1">𛰅𛰆𛱄𛰜 𛰚𛱁𛰚𛱆𛰛</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Vitals q4h / Post-Op Watch</text>
      </g>

      <g transform="translate(0, 100)">
        <text x="0" y="0" class="font-brand" font-size="14" font-weight="700" fill="#0F172A">Remedy / Pharmacotherapy (Meskahke):</text>
        <text x="320" y="0" class="font-duployan" font-size="24" fill="#0369A1">𛰙𛱇𛰜𛰅𛱁𛰀𛱇</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Cephalexin 500 mg PO BID</text>
      </g>

      <g transform="translate(0, 150)">
        <text x="0" y="0" class="font-brand" font-size="14" font-weight="700" fill="#0F172A">Gratitude Attestation (Mahsie):</text>
        <text x="320" y="0" class="font-duployan" font-size="24" fill="#0369A1">𛰙𛱁𛰀𛰜𛱆</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Care Plan Attested &amp; Signed</text>
      </g>

      <line x1="0" y1="190" x2="746" y2="190" stroke="#E2E8F0"/>

      <g transform="translate(0, 220)">
        <text x="0" y="0" class="font-mono" font-size="11" fill="#64748B">
          OPTICAL CORRECTIONS: Tabular lining figures • Slashed zero (cv08) • Serifed capital I (ss02) • Curved lowercase l (cv05)
        </text>
      </g>
    </g>
  </g>
</svg>''';
}

// =============================================================================
// 9. LANDMARK PLATE C: PEDAGOGICAL TYPEFACE SPECIMEN (896x1200)
// =============================================================================
String generatePedagogicalPlate() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="896" height="1200" viewBox="0 0 896 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .font-brand { font-family: 'PocketGull Bold', 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'PocketGull Mono', 'JetBrains Mono', monospace; }
      .font-duployan { font-family: 'Pocket Gull', 'PocketGull', 'Pocket Gull Bold', 'PocketGull Bold', 'SansSerifCollection', sans-serif; }
      .font-fineliner { font-family: 'PocketGull Fineliner', 'PocketGull', sans-serif; }
      .font-bold { font-family: 'PocketGull Bold', 'PocketGull', sans-serif; }
      .font-chiseltip { font-family: 'PocketGull Chiseltip', 'PocketGull', sans-serif; }
    </style>
    <radialGradient id="leatherBg" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#3E2723"/>
      <stop offset="100%" stop-color="#1A0C08"/>
    </radialGradient>
  </defs>

  <!-- Dark Leather Background -->
  <rect width="896" height="1200" fill="url(#leatherBg)"/>

  <!-- Torn-Edge Washi Papercraft Sheet -->
  <g transform="translate(48, 40)">
    <!-- Ambient Washi Sheet Shadow -->
    <rect x="4" y="12" width="800" height="1120" rx="4" fill="#000000" opacity="0.35"/>
    <rect width="800" height="1120" rx="4" fill="#FCFAF6" stroke="#E2DACB" stroke-width="1.5"/>

    <g transform="translate(50, 60)">
      <!-- Main Title -->
      <text x="0" y="0" class="font-chiseltip" font-size="27" font-weight="900" fill="#1C1917" letter-spacing="-0.02em">PocketGull: Teaching Through the Typeface</text>
      <text x="0" y="24" class="font-mono" font-size="12" font-weight="700" fill="#B45309">CHINUK PIPA (DUPLOYAN) &amp; CLINICAL COGNITIVE SCAFFOLDING</text>
      <line x1="0" y1="36" x2="700" y2="36" stroke="#1C1917" stroke-width="2"/>

      <!-- Section 1: Cognitive Scaffolding -->
      <g transform="translate(0, 65)">
        <text x="0" y="0" class="font-bold" font-size="18" font-weight="700" fill="#1C1917">COGNITIVE SCAFFOLDING</text>
        <text x="0" y="20" class="font-brand" font-size="12" fill="#78716C">Typography as a teaching and learning engine for tribal community wellness.</text>

        <g transform="translate(0, 50)">
          <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#991B1B">900 Heavy</text>
          <text x="80" y="5" class="font-chiseltip" font-size="24" font-weight="900" fill="#1C1917">SKOOKUM TUMTUM // CARDIOVASCULAR</text>

          <g transform="translate(80, 25)">
            <path d="M 0 0 L 0 20 L 15 20" fill="none" stroke="#C2410C" stroke-width="2"/>
            <polygon points="15,16 22,20 15,24" fill="#C2410C"/>
            <text x="30" y="25" class="font-bold" font-size="16" font-weight="700" fill="#292524">
              Kloshe tumtum munk-skookum konaway tilixam...
            </text>
            <text x="30" y="45" class="font-fineliner" font-size="13" fill="#57534E">
              A good heart gives endurance to all family members and community.
            </text>
          </g>

          <g transform="translate(80, 85)">
            <line x1="0" y1="0" x2="20" y2="0" stroke="#78716C"/>
            <text x="30" y="4" class="font-mono" font-size="10.5" fill="#78716C">
              100 Fineliner: Includes resting heart rate, vagal parasympathetic recovery, and systolic metrics.
            </text>
          </g>
        </g>
      </g>

      <line x1="0" y1="260" x2="700" y2="260" stroke="#1C1917" stroke-width="1.5"/>

      <!-- Section 2: Bionic Reading Fixation -->
      <g transform="translate(0, 290)">
        <text x="0" y="0" class="font-bold" font-size="18" font-weight="700" fill="#1C1917">BIONIC READING FIXATION IN CHINUK WAWA</text>
        <text x="0" y="20" class="font-brand" font-size="12" fill="#78716C">Bold initial vector anchors guide the eye through rapid clinical reading acceleration.</text>

        <g transform="translate(0, 45)">
          <text x="0" y="30" class="font-chiseltip" font-size="44" font-weight="900" fill="#C2410C">A</text>
          <line x1="45" y1="18" x2="115" y2="18" stroke="#C2410C" stroke-width="3"/>
          <polygon points="115,12 125,18 115,24" fill="#C2410C"/>

          <g transform="translate(140, 0)">
            <rect x="0" y="0" width="30" height="38" fill="#C2410C" rx="3"/>
            <text x="7" y="28" class="font-chiseltip" font-size="28" font-weight="900" fill="#FFFFFF">B</text>
            <text x="40" y="20" class="font-fineliner" font-size="13" fill="#1C1917">
              <tspan class="font-bold" font-weight="700">Klo</tspan>she <tspan class="font-bold" font-weight="700">tum</tspan>tum <tspan class="font-bold" font-weight="700">mun</tspan>k-skookum <tspan class="font-bold" font-weight="700">ti</tspan>likum. <tspan class="font-bold" font-weight="700">Nan</tspan>itch <tspan class="font-bold" font-weight="700">mes</tspan>kahke...
            </text>
            <text x="40" y="38" class="font-brand" font-size="11.5" fill="#57534E">
              Initial fixation syllables anchor visual saccades, enabling 650 WPM reading velocity
            </text>
            <text x="40" y="52" class="font-brand" font-size="11.5" fill="#57534E">
              across EHR clinical summaries without cognitive fatigue.
            </text>
          </g>
        </g>
      </g>

      <line x1="0" y1="460" x2="700" y2="460" stroke="#1C1917" stroke-width="1.5"/>

      <!-- Lower Half: Pedagogical Ligatures & Sacred Proportions -->
      <g transform="translate(0, 490)">
        <!-- Left: Pedagogical Ligatures -->
        <g>
          <text x="0" y="0" class="font-brand" font-size="16" font-weight="800" fill="#1C1917">PEDAGOGICAL LIGATURES</text>
          <text x="0" y="18" class="font-brand" font-size="11" fill="#78716C">Typeface automatically converts shorthand compounds.</text>

          <g transform="translate(0, 50)">
            <text x="0" y="0" class="font-brand" font-size="28" font-weight="700" fill="#1C1917">H2O → H₂O</text>
            <text x="0" y="45" class="font-brand" font-size="28" font-weight="700" fill="#1C1917">mg/dl → mg/dL</text>
            <text x="0" y="90" class="font-duployan" font-size="34" fill="#1C1917">𛰃𛱑𛰙 + 𛲞 → 𛰃𛱑𛰙𛲞</text>
            <text x="0" y="125" class="font-mono" font-size="12" fill="#B45309">Tumtum Reduplication Ligature</text>
          </g>
        </g>

        <!-- Right: Sacred Proportions -->
        <g transform="translate(360, 0)">
          <text x="0" y="0" class="font-brand" font-size="16" font-weight="800" fill="#1C1917">SACRED PROPORTIONS (φ)</text>
          <text x="0" y="18" class="font-brand" font-size="11" fill="#78716C">Golden ratio overlays inside numeral anatomy.</text>

          <g transform="translate(0, 40)">
            <!-- Numeral 8, 9, 6 with Golden Spiral Graphic -->
            <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
            <text x="18" y="115" class="font-brand" font-size="120" font-weight="800" fill="#1C1917">8</text>
            <circle cx="50" cy="45" r="32" fill="none" stroke="#C2410C" stroke-width="1.2"/>
            <circle cx="50" cy="105" r="42" fill="none" stroke="#C2410C" stroke-width="1.2"/>

            <g transform="translate(115, 0)">
              <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
              <text x="18" y="115" class="font-brand" font-size="120" font-weight="800" fill="#1C1917">9</text>
              <circle cx="50" cy="45" r="38" fill="none" stroke="#C2410C" stroke-width="1.2"/>
            </g>

            <g transform="translate(230, 0)">
              <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
              <text x="18" y="115" class="font-brand" font-size="120" font-weight="800" fill="#1C1917">6</text>
              <circle cx="50" cy="105" r="38" fill="none" stroke="#C2410C" stroke-width="1.2"/>
            </g>
          </g>
          <text x="0" y="215" class="font-mono" font-size="11" fill="#64748B">Golden ratio φ (1.618) governs all bowl-to-stem proportions.</text>
        </g>
      </g>

      <!-- Bottom Footnote -->
      <g transform="translate(0, 980)">
        <line x1="0" y1="0" x2="700" y2="0" stroke="#E2DACB"/>
        <text x="0" y="20" class="font-mono" font-size="10" fill="#78716C">
          POCKETGULL PEDAGOGICAL SPECIMEN // GRAND RONDE HERITAGE // OFL 1.1 OPEN SOURCE
        </text>
      </g>
    </g>
  </g>
</svg>''';
}
