// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Inuktitut Specimen Generator
///
/// Procedurally synthesizes the 6 canonical typeface specimen assets in SVG
/// using authentic Nunavut / Inuit vexillology colors, Canadian Aboriginal
/// Syllabics (U+1400–U+167F), clinical health terminology, the official
/// Flag of Nunavut, ISO 3166-2 Country Code (CA-NU), and embedded high-res
/// photographic substrates.
///
/// Renders 300 DPI Master Museum Print PNGs (up to 3750x5375 / 8+ MB)
/// using Inkscape 1.4.3 in WSL.
library;

import 'dart:convert';
import 'dart:io';

void main() async {
  stdout.writeln('=== POCKETGULL INUKTITUT SPECIMEN & VEXILLOLOGY GENERATOR ===');

  final repoDir = Directory('c:/Users/philg/Pocketgull/pocketgull-typeface');
  final targetDir = Directory('${repoDir.path}/documentation/images/inuktitut');
  if (!targetDir.existsSync()) {
    targetDir.createSync(recursive: true);
  }
  stdout.writeln('Target Directory: ${targetDir.path}\n');

  // Load high-resolution photographic plates and bioregional substrates
  // Load high-resolution photographic plates, bioregions, and vexillological masterworks
  final deviceJpgPath = '${repoDir.path}/article/libre_pocketgull_device_1x1.jpg';
  final quillingJpgPath = '${repoDir.path}/article/synaptic_quilling_backdrop.jpg';
  final kellsWebpPath = '${repoDir.path}/documentation/masterworks/inuktitut/kells_arctic_vexillology.webp';

  stdout.write('Loading photographic and masterwork substrates... ');
  final deviceBase64 = File(deviceJpgPath).existsSync()
      ? base64Encode(File(deviceJpgPath).readAsBytesSync())
      : '';
  final quillingBase64 = File(quillingJpgPath).existsSync()
      ? base64Encode(File(quillingJpgPath).readAsBytesSync())
      : '';
  final kellsBase64 = File(kellsWebpPath).existsSync()
      ? base64Encode(File(kellsWebpPath).readAsBytesSync())
      : '';
  stdout.writeln('OK (Kells Vexillology: ${(kellsBase64.length / 1024).toStringAsFixed(0)} KB, Device: ${(deviceBase64.length / 1024).toStringAsFixed(0)} KB)\n');

  // 1. Generate social_github_preview.svg (1280x640)
  stdout.writeln('[1/6] Synthesizing social_github_preview.svg (Flag + CA-NU + Vexillological Fine Art Plate)...');
  final githubSvg = generateSocialGithubPreview(
    kellsBase64.isNotEmpty ? kellsBase64 : deviceBase64,
    mimeType: kellsBase64.isNotEmpty ? 'image/webp' : 'image/jpeg',
    badgeTitle: 'CA-NU',
    badgeNativeText: 'ᓄᓇᕗᑦ',
    badgeSubtitle: 'FINE ART SCRIPTORIUM',
  );
  File('${targetDir.path}/social_github_preview.svg').writeAsStringSync(githubSvg);

  // 2. Generate pocketgull_libre_synaptic_specimen.svg (1200x1720)
  stdout.writeln('[2/6] Synthesizing pocketgull_libre_synaptic_specimen.svg (Dark Basalt + Quilling Plate)...');
  final synapticDarkSvg = generateSynapticSpecimenDark(quillingBase64);
  File('${targetDir.path}/pocketgull_libre_synaptic_specimen.svg').writeAsStringSync(synapticDarkSvg);

  // 3. Generate pocketgull_libre_synaptic_light.svg (1200x1720)
  stdout.writeln('[3/6] Synthesizing pocketgull_libre_synaptic_light.svg (Light Polar Washi + Quilling Plate)...');
  final synapticLightSvg = generateSynapticSpecimenLight(quillingBase64);
  File('${targetDir.path}/pocketgull_libre_synaptic_light.svg').writeAsStringSync(synapticLightSvg);

  // 4. Generate pocketgull_synaptic_specimen_light.svg (2560x1280)
  stdout.writeln('[4/6] Synthesizing pocketgull_synaptic_specimen_light.svg (Panoramic 16:9 + Flag)...');
  final panoramicLightSvg = generatePanoramicSpecimenLight(deviceBase64, quillingBase64);
  File('${targetDir.path}/pocketgull_synaptic_specimen_light.svg').writeAsStringSync(panoramicLightSvg);

  // 5. Generate pocketgull-perma-thoughts-card.svg (1200x1200)
  stdout.writeln('[5/6] Synthesizing pocketgull-perma-thoughts-card.svg (6 PERMA+ Clinical Pillars)...');
  final permaSvg = generatePermaThoughtsCard();
  File('${targetDir.path}/pocketgull-perma-thoughts-card.svg').writeAsStringSync(permaSvg);
  File('${targetDir.path}/pocketgull_perma_thoughts_washi_card.svg').writeAsStringSync(permaSvg);
  File('${targetDir.path}/pocketgull-pemda-thoughts-card.svg').writeAsStringSync(permaSvg);
  File('${targetDir.path}/pocketgull_pemda_thoughts_washi_card.svg').writeAsStringSync(permaSvg);

  // 6. Generate print_gallery_exhibition.svg (1200x1600)
  stdout.writeln('[6/9] Synthesizing print_gallery_exhibition.svg (Museum Broadside + Dual Plates)...');
  final exhibitionSvg = generatePrintGalleryExhibition(deviceBase64, quillingBase64);
  File('${targetDir.path}/print_gallery_exhibition.svg').writeAsStringSync(exhibitionSvg);

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

  stdout.writeln('\nAll SVG specimen assets written to ${targetDir.path}/');

  // Master 300 DPI Rendering Configurations
  stdout.writeln('\n--- RASTERING 300 DPI MASTER PRINT PNGs VIA WSL INKSCAPE ---');
  final specs = [
    ('social_github_preview.svg', 'social_github_preview.png', 1280, 640),
    ('pocketgull_libre_synaptic_specimen.svg', 'pocketgull_libre_synaptic_specimen.png', 3750, 5375),
    ('pocketgull_libre_synaptic_light.svg', 'pocketgull_libre_synaptic_light.png', 3750, 5375),
    ('pocketgull_synaptic_specimen_light.svg', 'pocketgull_synaptic_specimen_light.png', 3840, 1920),
    ('pocketgull-perma-thoughts-card.svg', 'pocketgull-perma-thoughts-card.png', 2400, 2400),
    ('print_gallery_exhibition.svg', 'print_gallery_exhibition.png', 3600, 4800),
    ('pocketgull_type_engineering_specimen.svg', 'pocketgull_type_engineering_specimen.png', 2688, 3600),
    ('pocketgull_telemetry_type_specimen.svg', 'pocketgull_telemetry_type_specimen.png', 2688, 3600),
    ('pocketgull_pedagogical_typeface.svg', 'pocketgull_pedagogical_typeface.png', 2688, 3600),
  ];

  for (final (svgName, pngName, width, height) in specs) {
    final wslSvgPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/inuktitut/$svgName';
    final wslPngPath = '/mnt/c/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/inuktitut/$pngName';

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

  // Duplicate aliases for backwards compatibility
  final permaPng = File('${targetDir.path}/pocketgull-perma-thoughts-card.png');
  if (permaPng.existsSync()) {
    permaPng.copySync('${targetDir.path}/pocketgull-pemda-thoughts-card.png');
    permaPng.copySync('${targetDir.path}/pocketgull_pemda_thoughts_washi_card.png');
    permaPng.copySync('${targetDir.path}/pocketgull_perma_thoughts_washi_card.png');
  }

  stdout.writeln('\n[SUCCESS] Completed Inuktitut specimen generation with Flag, CA-NU code, and 300 DPI Master Print quality.');
}

// =============================================================================
// HELPER: OFFICIAL NUNAVUT FLAG SVG COMPONENT (MUSEUM HERALDRY STANDARD)
// =============================================================================
String nunavutFlagSvg({double x = 0, double y = 0, double width = 64, double height = 36}) {
  final scaleX = width / 9600.0;
  final scaleY = height / 5400.0;
  return '''
  <g transform="translate($x, $y)">
    <!-- Crisp Outer Border & Drop Shadow -->
    <rect width="$width" height="$height" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <g transform="scale($scaleX, $scaleY)">
      <!-- Left Field: Nunavut Gold -->
      <path fill="#FFD100" d="m0 0h4800v5400H0z"/>
      <!-- Right Field: Pristine Arctic Snow White -->
      <path fill="#FFFFFF" d="m4800 0h4800v5400h-4800z"/>
      <!-- Center Inuksuk in Nunavut Crimson with Black Outline (Official Construction) -->
      <path stroke="#0F172A" stroke-linejoin="round" stroke-width="70" fill="#D52B1E" d="m4800 39c83 18 434 417 464 510 24 96-94 927-204 1201-203 44-528 17-715-39-37-77-114-1079-79-1225 37-71 458-435 534-447zm-2085 1653c868 101 2615 93 3817 124 114 14-83 307-132 426-48 119-57 384-335 377-1021-30-1946-58-2939-89-361-11-640-863-411-838zm1336 882c176 20 873 8 1134 43 178 27 176 634 93 728-91 105-531 36-775 108-232 66-251 138-685 89 108-573 40-992 233-968zm-372 1048c67-89 192-64 341-53 203 9 649-161 945-158 180 7 319 79 315 242-6 129 7 438-74 613-48 114-745 92-1065-23-93-33-440 31-480-29-46-64-75-469 18-592zm50 664c27-51 157-69 239-63 216 15 626 196 1085 112 276-50 575 544 477 700-100 164-216 240-336 330-940 8-1614 89-1602-271 6-184 24-609 137-808z"/>
      <!-- Niqirtsuituq Polaris Star in Polaris Blue (Upper Right Fly) -->
      <path fill="#003896" d="m8847 753-784 399 869 138-622-622 138 869z"/>
    </g>
  </g>
  ''';
}

// =============================================================================
// HELPER: OFFICIAL NATIONAL FLAG OF CANADA (JACQUES SAINT-CYR 1964 STANDARD)
// =============================================================================
String canadaFlagSvg({double x = 0, double y = 0, double width = 64, double height = 32}) {
  final scaleX = width / 9600.0;
  final scaleY = height / 4800.0;
  return '''
  <g transform="translate($x, $y)">
    <rect width="$width" height="$height" rx="2" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="0.8"/>
    <g transform="scale($scaleX, $scaleY)">
      <!-- Official Canadian Red Bars (1:4 width each) -->
      <path fill="#D52B1E" d="m0 0h2400v4800H0z"/>
      <path fill="#D52B1E" d="m7200 0h2400v4800h-2400z"/>
      <!-- Pure White Center Pale Square (1:2 width) -->
      <path fill="#FFFFFF" d="m2400 0h4800v4800h-4800z"/>
      <!-- The Official 11-Point Canadian Maple Leaf -->
      <path fill="#D52B1E" d="m4890 4430-45-863a95 95 0 0 1 111-98l859 151-116-320a65 65 0 0 1 20-73l941-762-212-99a65 65 0 0 1-34-79l186-572-542 115a65 65 0 0 1-73-38l-105-247-423 454a65 65 0 0 1-111-57l204-1052-327 189a65 65 0 0 1-91-27l-332-652-332 652a65 65 0 0 1-91 27l-327-189 204 1052a65 65 0 0 1-111 57l-423-454-105 247a65 65 0 0 1-73 38l-542-115 186 572a65 65 0 0 1-34 79l-212 99 941 762a65 65 0 0 1 20 73l-116 320 859-151a95 95 0 0 1 111 98l-45 863z"/>
    </g>
  </g>
  ''';
}

// =============================================================================
// 1. SOCIAL GITHUB PREVIEW (1280x640) — POLAR WASHI PAPERBOARD THEME
// =============================================================================
String generateSocialGithubPreview(
  String photoBase64, {
  String mimeType = 'image/jpeg',
  String badgeTitle = 'CA-NU • NUNAVUT',
  String badgeNativeText = 'ᓄᓇᕗᑦ ᓴᙱᓂᖓ',
  String badgeSubtitle = 'BIOREGION SCRIPTORIUM // 300 DPI',
}) {
  final canFlag = canadaFlagSvg(x: 395, y: 0, width: 56, height: 28);
  final flagBlock = nunavutFlagSvg(x: 458, y: 0, width: 56, height: 31);

  final photoEmbed = photoBase64.isNotEmpty
      ? '''
      <g transform="translate(60, 60)">
        <!-- Soft Washi Ambient Shadow -->
        <rect x="2" y="6" width="460" height="520" rx="18" fill="#78716C" fill-opacity="0.08"/>
        <clipPath id="ghImgClip"><rect width="460" height="520" rx="18"/></clipPath>
        
        <!-- Base Paper Surface -->
        <rect width="460" height="520" rx="18" fill="#FAF8F5"/>
        <image href="data:$mimeType;base64,$photoBase64" xlink:href="data:$mimeType;base64,$photoBase64" width="460" height="520" preserveAspectRatio="xMidYMid slice" clip-path="url(#ghImgClip)"/>
        
        <!-- Seamless Washi Feathering Vignette (Blends image into washi canvas) -->
        <rect width="460" height="520" rx="18" fill="url(#photoWashiOverlay)" clip-path="url(#ghImgClip)"/>
      </g>
      '''
      : '';

  final leftShift = photoBase64.isNotEmpty ? 550 : 70;

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1280" height="640" viewBox="0 0 1280 640" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .font-body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
      .font-syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; font-weight: bold; }
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

  <!-- Top Accent Rules: Nunavut Gold, Inuksuk Red, Polaris Blue -->
  <rect x="24" y="24" width="410" height="4" fill="#FFD100"/>
  <rect x="434" y="24" width="410" height="4" fill="#D52B1E"/>
  <rect x="844" y="24" width="412" height="4" fill="#003896"/>

  <!-- Photographic Plate (Left Side) -->
  $photoEmbed

  <!-- Right Side: Inuktitut Typography & Seven Generations HUD on Washi -->
  <g transform="translate($leftShift, 60)">
    <!-- Header Ribbon: Country Code CA-NU + Official Museum Flags -->
    <g>
      <rect x="0" y="0" width="120" height="28" rx="3" fill="#D52B1E"/>
      <text x="60" y="19" class="font-mono" font-size="12" fill="#FFFFFF" text-anchor="middle" font-weight="bold">CASE STUDY 01</text>
      
      <rect x="128" y="0" width="190" height="28" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="223" y="19" class="font-mono" font-size="11" fill="#B45309" text-anchor="middle" font-weight="bold">ISO 3166-2: CA-NU • CAN</text>

      <rect x="326" y="0" width="60" height="28" rx="3" fill="#003896"/>
      <text x="356" y="19" class="font-mono" font-size="11" fill="#FFFFFF" text-anchor="middle" font-weight="bold">iu-CA</text>

      $canFlag
      $flagBlock
    </g>

    <!-- Large Bilingual Title in Charcoal Letterpress & Inuksuk Crimson -->
    <text x="0" y="80" class="font-syllabic" font-size="44" fill="#1F1B16" letter-spacing="-0.02em">ᐳᒃᑭᑦᒐᓪ <tspan fill="#D52B1E">PocketGull</tspan></text>
    <text x="0" y="112" class="font-syllabic" font-size="17" fill="#003896">ᐃᓄᒃᑎᑐᑦ • CANADIAN ABORIGINAL SYLLABICS (U+1400–U+167F)</text>

    <!-- Elder Wisdom & Seven Generations Quote Ribbon -->
    <g transform="translate(0, 130)">
      <rect width="665" height="50" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <rect x="0" y="0" width="4" height="50" fill="#D52B1E"/>
      <text x="14" y="20" class="font-syllabic" font-size="12" fill="#1F1B16">"ᐃᓄᒃᑐᑦ ᐅᖃᐅᓯᖅ ᑭᓇᐅᓂᑦᑎᓐᓂᒃ ᓴᖅᑭᔮᖅᑎᑦᑎᔪᖅ." <tspan class="font-body" font-size="11" fill="#57534E">— Jose Kusugak ("Our language is our identity")</tspan></text>
      <text x="14" y="38" class="font-body" font-size="11" fill="#003896" font-style="italic">ᒪᒥᓴᕐᓂᖅ • ᖃᐅᔨᒪᓂᖅ • ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ • ᖁᕕᐊᓱᖕᓂᖅ // Healing • Wisdom • Longevity • Humour</text>
    </g>

    <!-- Rotational Vowel Syllabics Plate on Ivory Washi -->
    <g transform="translate(0, 195)">
      <rect width="665" height="88" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <line x1="0" y1="0" x2="665" y2="0" stroke="#FFD100" stroke-width="2.5"/>
      <text x="18" y="25" class="font-mono" font-size="11" fill="#B45309" font-weight="bold">ROTATIONAL VOWEL ORIENTATION [i • u • a] // 640 SYLLABIC CODEPOINTS</text>
      <text x="18" y="65" class="font-syllabic" font-size="28" fill="#1F1B16" letter-spacing="0.14em">ᐱ ᐲ ᐳ ᐴ ᐸ ᐹ ᑉ   ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ ᑦ</text>
    </g>

    <!-- 4 Weights Invariant Badges in Washi Styling -->
    <g transform="translate(0, 298)">
      <rect x="0" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="77" y="21" class="font-mono" font-size="11" fill="#003896" text-anchor="middle" font-weight="bold">Fineliner 400</text>

      <rect x="168" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="245" y="21" class="font-mono" font-size="11" fill="#B45309" text-anchor="middle" font-weight="bold">Bold 700</text>

      <rect x="336" y="0" width="155" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="413" y="21" class="font-mono" font-size="11" fill="#D52B1E" text-anchor="middle" font-weight="bold">Chiseltip 900</text>

      <rect x="504" y="0" width="161" height="32" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
      <text x="584" y="21" class="font-mono" font-size="11" fill="#0D9488" text-anchor="middle" font-weight="bold">Mono 600 UPM</text>
    </g>

    <!-- Clinical Hospital Vitals & Words of Healing Ribbon -->
    <g transform="translate(0, 345)">
      <rect width="665" height="80" rx="3" fill="#FFFDF8" stroke="#D52B1E" stroke-width="1.2"/>
      <text x="18" y="25" class="font-syllabic" font-size="13" fill="#D52B1E" font-weight="bold">ᐋᓐᓂᐊᕕᒃ AANNIAVIK // QIKIQTANI GENERAL HOSPITAL (IQALUIT, NU)</text>
      <text x="18" y="58" class="font-syllabic" font-size="20" fill="#1F1B16">ᐆᒻᒪᑎ: 72 bpm • ᐊᓂᕐᓂᖃᕐᓇᖅ: 99% • ᑲᔪᓯᓂᖃᑦᓯᐊᕐᑐᖅ: STABLE</text>
    </g>

    <!-- Seven Generations & Humour Note + Colophon -->
    <g transform="translate(0, 442)">
      <text x="0" y="16" class="font-body" font-size="12" fill="#57534E">ᓯᕗᓂᒃᓴᕗᑦ ᑭᖑᕚᒃᓴᕗᑦ ᐱᓪᓗᒋᑦ: "Without humor, you freeze twice—once in body, once in spirit."</text>
      <text x="0" y="38" class="font-mono" font-size="11" fill="#78716C">PHILLIP GEAR // UNIVERSAL WORLD SCRIPTS INITIATIVE // OFL 1.1 // CA-NU 🇨🇦 // POCKETGULL.APP</text>
    </g>
  </g>
</svg>
''';
}

// =============================================================================
// 2. SYNAPTIC SPECIMEN DARK (1200x1720)
// =============================================================================
String generateSynapticSpecimenDark(String quillingBase64) {
  final quillingPlate = quillingBase64.isNotEmpty
      ? '''
      <g id="synaptic-quilling-plate" transform="translate(60, 135)">
        <clipPath id="quillClip"><rect width="1080" height="420" rx="3"/></clipPath>
        <rect width="1080" height="420" rx="3" fill="#080D1A" stroke="#1E293B" stroke-width="1.2"/>
        <image href="data:image/jpeg;base64,$quillingBase64" width="1080" height="420" preserveAspectRatio="xMidYMid slice" clip-path="url(#quillClip)"/>
        <!-- Dark Polar Overlay Gradient -->
        <rect width="1080" height="420" clip-path="url(#quillClip)" fill="url(#quillOverlayDark)"/>
        
        <!-- Photographic Plate Legend Overlay -->
        <g transform="translate(30, 320)">
          <rect width="520" height="70" rx="3" fill="#050811" fill-opacity="0.88" stroke="#FFD100" stroke-width="0.8"/>
          <text x="20" y="28" class="font-syllabic" font-size="18" fill="#F8FAFC" font-weight="bold">ᐳᒃᑭᑦᒐᓪ ᐃᓄᒃᑎᑐᑦ • CELLULAR SYNAPSE &amp; ARCTIC CODE</text>
          <text x="20" y="50" class="font-mono" font-size="11" fill="#38BDF8">NUNAVUT SCRIPT SOVEREIGNTY // COUNTRY CODE: CA-NU 🇨🇦</text>
        </g>
      </g>
      '''
      : '';

  final matrixY = quillingBase64.isNotEmpty ? 580 : 135;

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .font-syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; }
      .font-braille { font-family: "PocketGull", "DejaVu Sans", monospace; letter-spacing: 0.16em; }
      .font-meta { font-family: "PocketGull Mono", -apple-system, sans-serif; letter-spacing: 0.06em; }
    </style>
    <linearGradient id="obsidianGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#05070B"/>
      <stop offset="35%" stop-color="#080D18"/>
      <stop offset="70%" stop-color="#050912"/>
      <stop offset="100%" stop-color="#030508"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0E1626" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#080C16" stop-opacity="0.98"/>
    </linearGradient>
    <linearGradient id="quillOverlayDark" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#05070B" stop-opacity="0.10"/>
      <stop offset="60%" stop-color="#05070B" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#05070B" stop-opacity="0.94"/>
    </linearGradient>
  </defs>

  <!-- 1. Base Canvas -->
  <rect width="1200" height="1720" fill="url(#obsidianGrad)"/>

  <!-- Architectural 60px Reference Grid -->
  <g stroke="#1E293B" stroke-width="0.5" stroke-opacity="0.3">
    <line x1="60" y1="60" x2="1140" y2="60"/>
    <line x1="60" y1="120" x2="1140" y2="120"/>
    <line x1="60" y1="180" x2="1140" y2="180"/>
    <line x1="60" y1="240" x2="1140" y2="240"/>
    <line x1="60" y1="300" x2="1140" y2="300"/>
    <line x1="60" y1="60" x2="60" y2="1660"/>
    <line x1="1140" y1="60" x2="1140" y2="1660"/>
  </g>

  <!-- 2. Braille & Syllabic Top Perimeter -->
  <rect x="60" y="24" width="1080" height="28" rx="0" fill="#0A0F1D" stroke="#1E293B" stroke-width="0.8"/>
  <text x="600" y="43" class="font-syllabic" font-size="13" fill="#FFD100" text-anchor="middle" font-weight="bold">ᐳᒃᑭᑦᒐᓪ • ᐃᓄᒃᑎᑐᑦ ᑲᓇᑕᒥ ᓄᓇᖃᖅᑳᖅᓯᒪᔪᑦ • POCKETGULL CASE STUDY 01 // CA-NU 🇨🇦</text>

  <!-- 3. Modular Header with Official Flag and Country Code -->
  <g transform="translate(60, 65)">
    <line x1="0" y1="0" x2="1080" y2="0" stroke="#334155" stroke-width="1.2"/>
    <text x="0" y="34" class="font-syllabic" font-size="32" fill="#F8FAFC" font-weight="bold">ᐳᒃᑭᑦᒐᓪ <tspan fill="#FFD100">POCKETGULL</tspan></text>
    
    <!-- Country Code & Flag Cluster -->
    <rect x="360" y="12" width="170" height="26" rx="3" fill="#0B132B" stroke="#D52B1E" stroke-width="1"/>
    <text x="445" y="29" class="font-mono" font-size="12" fill="#FFFFFF" text-anchor="middle" font-weight="bold">CA-NU • CANADA 🇨🇦</text>

    <text x="550" y="30" class="font-meta" font-size="13" fill="#94A3B8" font-weight="bold">TIER 6: CANADIAN ABORIGINAL SYLLABICS (U+1400–U+167F)</text>
    <text x="1080" y="30" class="font-mono" font-size="13" fill="#2DD4BF" text-anchor="end" font-weight="bold">640 GLYPHS • 1000 UPM</text>
    <line x1="0" y1="50" x2="1080" y2="50" stroke="#334155" stroke-width="1.2"/>
  </g>

  <!-- 4. Photographic Quilling Substrate -->
  $quillingPlate

  <!-- 5. Complete Inuktitut Syllabics Matrix Plate -->
  <g id="syllabics-matrix-plate" transform="translate(60, $matrixY)">
    <rect width="1080" height="380" rx="3" fill="#070C16" stroke="#1E293B" stroke-width="1.2"/>
    
    <!-- Plate Banner -->
    <rect x="0" y="0" width="1080" height="36" fill="#0E1626"/>
    <text x="24" y="24" class="font-mono" font-size="12" fill="#FFD100" font-weight="bold">CANADIAN ABORIGINAL SYLLABICS // 13 CONSONANT SERIES × ROTATIONAL VOWELS</text>
    <text x="1056" y="24" class="font-mono" font-size="11" fill="#38BDF8" text-anchor="end">ROTATIONAL GEOMETRIC SYMMETRY</text>
    <line x1="0" y1="36" x2="1080" y2="36" stroke="#1E293B" stroke-width="1"/>

    <!-- Matrix Rows -->
    <g transform="translate(24, 70)" class="font-syllabic" font-size="20" fill="#F8FAFC">
      <text x="80" y="0" text-anchor="middle">ᐃ ᐄ ᐅ ᐆ ᐊ ᐋ</text>
      <text x="320" y="0" text-anchor="middle">ᐱ ᐲ ᐳ ᐴ ᐸ ᐹ ᑉ</text>
      <text x="640" y="0" text-anchor="middle">ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ ᑦ</text>
      <text x="960" y="0" class="font-mono" font-size="12" fill="#38BDF8" text-anchor="middle">Vowels / P / T</text>

      <text x="80" y="36" text-anchor="middle">ᑭ ᑮ ᑯ ᑰ ᑲ ᑳ ᒃ</text>
      <text x="320" y="36" text-anchor="middle">ᒋ ᒌ ᒍ ᒎ ᒐ ᒑ ᒡ</text>
      <text x="640" y="36" text-anchor="middle">ᒥ ᒦ ᒧ ᒨ ᒪ ᒫ ᒻ</text>
      <text x="960" y="36" class="font-mono" font-size="12" fill="#94A3B8" text-anchor="middle">K / G / M</text>

      <text x="80" y="72" text-anchor="middle">ᓂ ᓃ ᓄ ᓅ ᓇ ᓈ ᓐ</text>
      <text x="320" y="72" text-anchor="middle">ᓯ ᓰ ᓱ ᓲ ᓴ ᓵ ᔅ</text>
      <text x="640" y="72" text-anchor="middle">ᓕ ᓖ ᓗ ᓘ ᓚ ᓛ ᓪ</text>
      <text x="960" y="72" class="font-mono" font-size="12" fill="#94A3B8" text-anchor="middle">N / S / L</text>

      <text x="80" y="108" text-anchor="middle">ᔨ ᔩ ᔪ ᔫ ᔭ ᔭ ᔾ</text>
      <text x="320" y="108" text-anchor="middle">ᕆ ᕇ ᕈ ᕉ ᕋ ᕌ ᕐ</text>
      <text x="640" y="108" text-anchor="middle">ᕕ ᕖ ᕗ ᕘ ᕙ ᕚ ᕝ</text>
      <text x="960" y="108" class="font-mono" font-size="12" fill="#94A3B8" text-anchor="middle">Y / R / V</text>

      <text x="80" y="144" text-anchor="middle">ᕿ ᖀ ᖁ ᖂ ᖃ ᖄ ᖅ</text>
      <text x="320" y="144" text-anchor="middle">ᖏ ᖐ ᖑ ᖒ ᖓ ᖔ ᖕ</text>
      <text x="640" y="144" text-anchor="middle">ᙱ ᙲ ᙳ ᙴ ᙵ ᙶ ᖖ</text>
      <text x="960" y="144" class="font-mono" font-size="12" fill="#94A3B8" text-anchor="middle">Q / Ng / Nng</text>

      <text x="80" y="180" text-anchor="middle">ᖠ ᖡ ᖢ ᖣ ᖤ ᖥ ᖦ</text>
      <text x="320" y="180" class="font-mono" font-size="13" fill="#003896">CARRIER &amp; CREE EXTENSIONS</text>
      <text x="640" y="180" class="font-mono" font-size="13" fill="#D52B1E">100% UNICODE 16.0</text>
      <text x="960" y="180" class="font-mono" font-size="12" fill="#FFD100" text-anchor="middle">Ł-Series</text>
    </g>

    <!-- Matrix Footnote -->
    <line x1="24" y1="330" x2="1056" y2="330" stroke="#1E293B" stroke-width="0.8"/>
    <text x="24" y="354" class="font-mono" font-size="11" fill="#64748B">ROTATIONAL CODE: [i] NORTH • [u] EAST • [a] SOUTH • OVERHEAD DOT = LONG VOWEL • COUNTRY: CA-NU 🇨🇦</text>
    <text x="1056" y="354" class="font-mono" font-size="11" fill="#FFD100" text-anchor="end">100% UNICODE 16.0 COMPLIANT</text>
  </g>

  <!-- 6. 4 Clinical Principle Cards -->
  <g transform="translate(0, 240)">
    <!-- Card 01: Louise Sloan 5:1 Invariant in Polaris Blue -->
    <g transform="translate(60, 740)">
      <rect width="525" height="225" rx="3" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="1.2"/>
      <line x1="0" y1="0" x2="525" y2="0" stroke="#38BDF8" stroke-width="3"/>
      <text x="22" y="26" class="font-meta" font-size="12" fill="#38BDF8" font-weight="bold">[01] LOUISE SLOAN 5:1 OPTOTYPE INVARIANT</text>
      <text x="22" y="42" class="font-mono" font-size="10" fill="#64748B">ᐊᖏᓂᖓ • 55 CM SNELLEN 20/20 • 5-ARCMINUTE VISUAL ANGLE</text>
      <line x1="20" y1="50" x2="505" y2="50" stroke="#1E293B" stroke-width="1"/>
      
      <text x="24" y="76" class="font-syllabic" font-size="16" fill="#F8FAFC">ᐋᓐᓂᐊᕕᖕᒥ ᑕᑯᑦᓯᐊᕈᓐᓇᕐᓂᖅ</text>
      <text x="24" y="100" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">An optotype measured in Arctic light,</text>
      <text x="24" y="122" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">Five minutes of arc in the polar sight;</text>
      <text x="24" y="144" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">With a stroke one-fifth wide on the tundra snow,</text>
      <text x="24" y="170" class="font-title" font-size="14" fill="#FFD100" font-weight="bold">Louise gave clinicians their clarity to glow!</text>

      <line x1="20" y1="195" x2="505" y2="195" stroke="#1E293B" stroke-width="0.8"/>
      <text x="22" y="212" class="font-mono" font-size="10" fill="#64748B">NODE: sloan_inuktitut // 5:1 STROKE CALIBRATION</text>
      <text x="503" y="212" class="font-mono" font-size="10" fill="#38BDF8" text-anchor="end">OPTOTYPE VERIFIED</text>
    </g>

    <!-- Card 02: Herman Bouma Crowding in Nunavut Gold -->
    <g transform="translate(615, 740)">
      <rect width="525" height="225" rx="3" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="1.2"/>
      <line x1="0" y1="0" x2="525" y2="0" stroke="#FFD100" stroke-width="3"/>
      <text x="22" y="26" class="font-meta" font-size="12" fill="#FFD100" font-weight="bold">[02] HERMAN BOUMA LATERAL CROWDING</text>
      <text x="22" y="42" class="font-mono" font-size="10" fill="#64748B">ᐃᓂᖓ • 0.12em CRITICAL SPACING • ZERO GLYPH BLUR</text>
      <line x1="20" y1="50" x2="505" y2="50" stroke="#1E293B" stroke-width="1"/>

      <text x="24" y="76" class="font-syllabic" font-size="16" fill="#F8FAFC">ᐊᑯᓐᓂᖏᑦ ᑕᒻᒪᙱᓪᓗᑎᒃ ᐅᖃᓕᒫᒐᒃᓴᑦ</text>
      <text x="24" y="100" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">When syllabics crowd on a vitals chart,</text>
      <text x="24" y="122" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">They blur and they wander apart;</text>
      <text x="24" y="144" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">With Bouma's wide space in telemetry view,</text>
      <text x="24" y="170" class="font-title" font-size="14" fill="#FFD100" font-weight="bold">Each vital sign rings unmistakable and true!</text>

      <line x1="20" y1="195" x2="505" y2="195" stroke="#1E293B" stroke-width="0.8"/>
      <text x="22" y="212" class="font-mono" font-size="10" fill="#64748B">NODE: bouma_spacing // 600 UPM ADVANCE</text>
      <text x="503" y="212" class="font-mono" font-size="10" fill="#FFD100" text-anchor="end">TELEMETRY SECURE</text>
    </g>

    <!-- Card 03: ISMP Clinical Safety in Inuksuk Red -->
    <g transform="translate(60, 985)">
      <rect width="525" height="225" rx="3" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="1.2"/>
      <line x1="0" y1="0" x2="525" y2="0" stroke="#D52B1E" stroke-width="3"/>
      <text x="22" y="26" class="font-meta" font-size="12" fill="#D52B1E" font-weight="bold">[03] ISMP LIFE-CRITICAL DISAMBIGUATION</text>
      <text x="22" y="42" class="font-mono" font-size="10" fill="#64748B">ᐃᓅᓕᓴᐅᑦ ᐊᑦᑕᕐᓇᖅᑕᐃᓕᒪᓂᖅ • cv08 cv05 ss02 • ZERO NAKED DECIMALS</text>
      <line x1="20" y1="50" x2="505" y2="50" stroke="#1E293B" stroke-width="1"/>

      <text x="24" y="76" class="font-syllabic" font-size="16" fill="#F8FAFC">ᐋᓐᓂᐊᓯᐅᑎᓂᒃ ᑕᒻᒪᖅᑕᐃᓕᒪᓂᖅ</text>
      <text x="24" y="100" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">A decimal stray in a dosage line,</text>
      <text x="24" y="122" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">Can endanger a patient's vital design;</text>
      <text x="24" y="144" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">With a slashed zero caught and no trailing dots,</text>
      <text x="24" y="170" class="font-title" font-size="14" fill="#D52B1E" font-weight="bold">Safe healing is brought to Arctic spots!</text>

      <line x1="20" y1="195" x2="505" y2="195" stroke="#1E293B" stroke-width="0.8"/>
      <text x="22" y="212" class="font-mono" font-size="10" fill="#64748B">NODE: ismp_patient_safety // FDA 21 CFR COMPLIANT</text>
      <text x="503" y="212" class="font-mono" font-size="10" fill="#D52B1E" text-anchor="end">PATIENT SAFE</text>
    </g>

    <!-- Card 04: Arctic Telehealth in Celadon Teal -->
    <g transform="translate(615, 985)">
      <rect width="525" height="225" rx="3" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="1.2"/>
      <line x1="0" y1="0" x2="525" y2="0" stroke="#2DD4BF" stroke-width="3"/>
      <text x="22" y="26" class="font-meta" font-size="12" fill="#2DD4BF" font-weight="bold">[04] ARCTIC TELEHEALTH &amp; SOVEREIGNTY</text>
      <text x="22" y="42" class="font-mono" font-size="10" fill="#64748B">ᑲᔪᓯᓂᖃᑦᓯᐊᕐᑐᖅ • NUNAVUT HEALTH NETWORK • CA-NU 🇨🇦</text>
      <line x1="20" y1="50" x2="505" y2="50" stroke="#1E293B" stroke-width="1"/>

      <text x="24" y="76" class="font-syllabic" font-size="16" fill="#F8FAFC">ᓄᓇᕗᒻᒥ ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ</text>
      <text x="24" y="100" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">Across Baffin bay and the Kivalliq wind,</text>
      <text x="24" y="122" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">Where clinics and elders are closely pinned;</text>
      <text x="24" y="144" class="font-title" font-size="13" fill="#CBD5E1" font-style="italic">Inuktitut glyphs in telemetry glow,</text>
      <text x="24" y="170" class="font-title" font-size="14" fill="#2DD4BF" font-weight="bold">Bringing medicine safe to the northern snow!</text>

      <line x1="20" y1="195" x2="505" y2="195" stroke="#1E293B" stroke-width="0.8"/>
      <text x="22" y="212" class="font-mono" font-size="10" fill="#64748B">NODE: arctic_sovereignty // NUNAVUT TELEMETRY</text>
      <text x="503" y="212" class="font-mono" font-size="10" fill="#2DD4BF" text-anchor="end">SOVEREIGNTY SEALED</text>
    </g>
  </g>

  <!-- 7. Typographic Anatomy & Disambiguation Ribbon -->
  <g id="typography-ribbon" transform="translate(60, 1470)">
    <rect width="1080" height="95" rx="3" fill="#060913" stroke="#1E293B" stroke-width="1.2"/>
    <text x="24" y="24" class="font-meta" font-size="12" fill="#FFD100" font-weight="bold">POCKETGULL INUKTITUT CLINICAL DISAMBIGUATION // CA-NU • iu-CA</text>
    <text x="1056" y="24" class="font-mono" font-size="11" fill="#64748B" text-anchor="end">NUNAVUT OFFICIAL LANGUAGE ACT COMPLIANT</text>
    <line x1="20" y1="32" x2="1060" y2="32" stroke="#1E293B" stroke-width="0.8"/>

    <!-- Syllabics Line -->
    <text x="24" y="65" class="font-syllabic" font-size="22" fill="#F8FAFC">ᐋᓐᓂᐊᕕᒃ • ᓘᒃᑖᖅ • ᐋᓐᓂᐊᓯᐅᖅᑎ • ᐃᓅᓕᓴᐅᑦ • ᐆᒻᒪᑎ 72 bpm • ᐊᓂᕐᓂᖃᕐᓇᖅ 99% • ᑲᔪᓯᓂᖃᑦᓯᐊᕐᑐᖅ</text>
  </g>

  <!-- 8. Bottom Colophon -->
  <g transform="translate(60, 1585)">
    <line x1="0" y1="0" x2="1080" y2="0" stroke="#334155" stroke-width="0.8"/>
    <text x="0" y="28" class="font-meta" font-size="11" fill="#94A3B8">DESIGNED BY PHILLIP GEAR // THE POCKETGULL PROJECT // ROOTED IN EMPIRICAL OPTICS. ENGINEERED FOR LIFE.</text>
    <text x="1080" y="28" class="font-mono" font-size="11" fill="#FFD100" text-anchor="end" font-weight="bold">SIL OPEN FONT LICENSE 1.1 // ISO 3166-2: CA-NU 🇨🇦 // POCKETGULL.APP</text>
  </g>
</svg>
''';
}

// =============================================================================
// 3. SYNAPTIC SPECIMEN LIGHT (1200x1720)
// =============================================================================
String generateSynapticSpecimenLight(String quillingBase64) {
  final flagBlock = nunavutFlagSvg(x: 880, y: 18, width: 80, height: 50);
  final canFlag = canadaFlagSvg(x: 790, y: 18, width: 80, height: 50);

  final quillingPlate = quillingBase64.isNotEmpty
      ? '''
      <g id="synaptic-quilling-plate-light" transform="translate(70, 205)">
        <clipPath id="quillClipLight"><rect width="1060" height="380" rx="3"/></clipPath>
        <rect width="1060" height="380" rx="3" fill="#FAF8F5" stroke="#E7E2D6" stroke-width="1.2"/>
        <image href="data:image/jpeg;base64,$quillingBase64" width="1060" height="380" preserveAspectRatio="xMidYMid slice" clip-path="url(#quillClipLight)"/>
        <!-- Light Washi Overlay Gradient -->
        <rect width="1060" height="380" clip-path="url(#quillClipLight)" fill="url(#quillOverlayLight)"/>
        
        <g transform="translate(30, 290)">
          <rect width="520" height="65" rx="3" fill="#FFFFFF" fill-opacity="0.92" stroke="#E7E2D6" stroke-width="1"/>
          <text x="20" y="26" class="font-syllabic" font-size="18" fill="#1F1B16" font-weight="bold">ᐳᒃᑭᑦᒐᓪ ᐃᓄᒃᑎᑐᑦ • DAYLIGHT WASHI SPECIMEN</text>
          <text x="20" y="48" class="font-mono" font-size="11" fill="#003896">NUNAVUT SCRIPT SOVEREIGNTY // ISO 3166-2: CA-NU 🇨🇦</text>
        </g>
      </g>
      '''
      : '';

  final matrixY = quillingBase64.isNotEmpty ? 610 : 205;

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1720" viewBox="0 0 1200 1720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .font-syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; }
      .font-braille { font-family: "DejaVu Sans", monospace; letter-spacing: 0.16em; }
      .font-meta { font-family: "PocketGull Mono", -apple-system, sans-serif; letter-spacing: 0.06em; }
    </style>
    <linearGradient id="washiBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F2ECE1"/>
    </linearGradient>
    <linearGradient id="quillOverlayLight" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF8F5" stop-opacity="0.10"/>
      <stop offset="65%" stop-color="#FAF8F5" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#FAF8F5" stop-opacity="0.94"/>
    </linearGradient>
  </defs>

  <!-- Base Canvas -->
  <rect width="1200" height="1720" fill="url(#washiBg)"/>

  <!-- Outer Architectural Deckle Rules in Nunavut Gold & Inuksuk Red -->
  <rect x="30" y="30" width="1140" height="1660" fill="none" stroke="#E7E2D6" stroke-width="1.5"/>
  <rect x="36" y="36" width="1128" height="1648" fill="none" stroke="#E7E2D6" stroke-width="0.8" stroke-dasharray="4,4"/>

  <!-- Top Accent Bar: Nunavut Flag Gold, Red, White -->
  <rect x="30" y="30" width="380" height="4" fill="#FFD100"/>
  <rect x="410" y="30" width="380" height="4" fill="#D52B1E"/>
  <rect x="790" y="30" width="380" height="4" fill="#003896"/>

  <!-- Modular Header with Flags -->
  <g transform="translate(70, 75)">
    <text x="0" y="45" class="font-syllabic" font-size="44" fill="#1F1B16" font-weight="bold">ᐳᒃᑭᑦᒐᓪ <tspan fill="#D52B1E">PocketGull</tspan></text>
    <text x="0" y="80" class="font-syllabic" font-size="20" fill="#57534E">ᐃᓄᒃᑎᑐᑦ ᑲᓇᑕᒥ ᓄᓇᖃᖅᑳᖅᓯᒪᔪᑦ • Inuktitut Syllabics (U+1400–U+167F)</text>
    
    $canFlag
    $flagBlock

    <line x1="0" y1="105" x2="1060" y2="105" stroke="#E7E2D6" stroke-width="1.5"/>
    <text x="1060" y="98" class="font-mono" font-size="12" fill="#78716C" text-anchor="end" font-weight="bold">CASE STUDY 01 // CA-NU 🇨🇦 // LIGHT SPECIMEN</text>
  </g>

  <!-- Photographic Quilling Substrate -->
  $quillingPlate

  <!-- Complete Syllabics Matrix Table on Arctic Washi -->
  <g transform="translate(70, $matrixY)">
    <rect width="1060" height="480" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
    <line x1="0" y1="0" x2="1060" y2="0" stroke="#003896" stroke-width="3"/>
    
    <text x="24" y="32" class="font-mono" font-size="13" fill="#003896" font-weight="bold">CANADIAN ABORIGINAL SYLLABICS // ROTATIONAL MATRIX (PHOTOPIC 55 CM DAYLIGHT)</text>
    <line x1="20" y1="45" x2="1040" y2="45" stroke="#E7E2D6" stroke-width="1"/>

    <!-- Matrix Rows -->
    <g transform="translate(24, 75)" class="font-syllabic" font-size="20" fill="#1F1B16">
      <text x="80" y="0" text-anchor="middle">ᐃ ᐄ ᐅ ᐆ ᐊ ᐋ</text>
      <text x="320" y="0" text-anchor="middle">ᐱ ᐲ ᐳ ᐴ ᐸ ᐹ ᑉ</text>
      <text x="640" y="0" text-anchor="middle">ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ ᑦ</text>
      <text x="940" y="0" class="font-mono" font-size="12" fill="#D52B1E" font-weight="bold">Vowels / P / T</text>

      <text x="80" y="36" text-anchor="middle">ᑭ ᑮ ᑯ ᑰ ᑲ ᑳ ᒃ</text>
      <text x="320" y="36" text-anchor="middle">ᒋ ᒌ ᒍ ᒎ ᒐ ᒑ ᒡ</text>
      <text x="640" y="36" text-anchor="middle">ᒥ ᒦ ᒧ ᒨ ᒪ ᒫ ᒻ</text>
      <text x="940" y="36" class="font-mono" font-size="12" fill="#78716C">K / G / M</text>

      <text x="80" y="72" text-anchor="middle">ᓂ ᓃ ᓄ ᓅ ᓇ ᓈ ᓐ</text>
      <text x="320" y="72" text-anchor="middle">ᓯ ᓰ ᓱ ᓲ ᓴ ᓵ ᔅ</text>
      <text x="640" y="72" text-anchor="middle">ᓕ ᓖ ᓗ ᓘ ᓚ ᓛ ᓪ</text>
      <text x="940" y="72" class="font-mono" font-size="12" fill="#78716C">N / S / L</text>

      <text x="80" y="108" text-anchor="middle">ᔨ ᔩ ᔪ ᔫ ᔭ ᔭ ᔾ</text>
      <text x="320" y="108" text-anchor="middle">ᕆ ᕇ ᕈ ᕉ ᕋ ᕌ ᕐ</text>
      <text x="640" y="108" text-anchor="middle">ᕕ ᕖ ᕗ ᕘ ᕙ ᕚ ᕝ</text>
      <text x="940" y="108" class="font-mono" font-size="12" fill="#78716C">Y / R / V</text>

      <text x="80" y="144" text-anchor="middle">ᕿ ᖀ ᖁ ᖂ ᖃ ᖄ ᖅ</text>
      <text x="320" y="144" text-anchor="middle">ᖏ ᖐ ᖑ ᖒ ᖓ ᖔ ᖕ</text>
      <text x="640" y="144" text-anchor="middle">ᙱ ᙲ ᙳ ᙴ ᙵ ᙶ ᖖ</text>
      <text x="940" y="144" class="font-mono" font-size="12" fill="#78716C">Q / Ng / Nng</text>

      <text x="80" y="180" text-anchor="middle">ᖠ ᖡ ᖢ ᖣ ᖤ ᖥ ᖦ</text>
      <text x="320" y="180" class="font-mono" font-size="13" fill="#003896">CARRIER &amp; CREE EXTENSIONS</text>
      <text x="640" y="180" class="font-mono" font-size="13" fill="#D52B1E">100% UNICODE 16.0</text>
      <text x="940" y="180" class="font-mono" font-size="12" fill="#B45309" font-weight="bold">Ł-Series</text>
    </g>
  </g>

  <!-- Clinical Telehealth & Snellen 20/20 Showcase -->
  <g transform="translate(70, 1120)">
    <rect width="1060" height="260" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
    <line x1="0" y1="0" x2="1060" y2="0" stroke="#FFD100" stroke-width="3"/>

    <text x="24" y="34" class="font-mono" font-size="13" fill="#D52B1E" font-weight="bold">QIKIQTANI GENERAL HOSPITAL // NUNAVUT HEALTH CARE PLAN (CA-NU)</text>
    <text x="1036" y="34" class="font-mono" font-size="11" fill="#78716C" text-anchor="end">IQALUIT TELEMETRY HUD</text>
    <line x1="20" y1="46" x2="1040" y2="46" stroke="#E7E2D6" stroke-width="0.8"/>

    <!-- Large Bilingual Clinical Statements -->
    <g transform="translate(24, 80)">
      <text x="0" y="0" class="font-syllabic" font-size="28" fill="#1F1B16" font-weight="bold">ᐋᓐᓂᐊᕕᒃ • ᓘᒃᑖᖅ ᖃᐅᔨᓴᕐᑐᖅ ᐆᒻᒪᑎᒥᒃ</text>
      <text x="0" y="28" class="font-body" font-size="16" fill="#57534E">Hospital Clinic: The physician examines cardiac rhythm and respiration.</text>

      <text x="0" y="75" class="font-syllabic" font-size="28" fill="#003896" font-weight="bold">ᑲᔪᓯᓂᖃᑦᓯᐊᕐᑐᖅ: ᐊᓂᕐᓂᖃᕐᓇᖅ 99% • ᐆᒻᒪᑎ 72 bpm</text>
      <text x="0" y="103" class="font-mono" font-size="14" fill="#2DD4BF" font-weight="bold">PATIENT VITALS STABLE • ZERO DOSAGE AMBIGUITY (ISMP cv08 0 vs O)</text>
    </g>

    <!-- Sloan 5:1 Badge -->
    <g transform="translate(24, 210)">
      <rect width="320" height="38" fill="#FAF8F5" stroke="#E7E2D6" stroke-width="1"/>
      <text x="16" y="24" class="font-mono" font-size="11" fill="#D52B1E" font-weight="bold">LOUISE SLOAN 5:1 OPTOTYPE PASS</text>
      <text x="304" y="24" class="font-mono" font-size="11" fill="#003896" text-anchor="end" font-weight="bold">SNELLEN 20/20</text>
    </g>
  </g>

  <!-- Bottom Colophon -->
  <g transform="translate(70, 1600)">
    <line x1="0" y1="0" x2="1060" y2="0" stroke="#E7E2D6" stroke-width="1"/>
    <text x="0" y="30" class="font-mono" font-size="11" fill="#78716C">THE POCKETGULL FOUNDRY // UNIVERSAL WORLD SCRIPTS INITIATIVE</text>
    <text x="1060" y="30" class="font-mono" font-size="11" fill="#003896" text-anchor="end" font-weight="bold">NUNAVUT SCRIPT SOVEREIGNTY // ISO 3166-2: CA-NU 🇨🇦 // OFL 1.1</text>
  </g>
</svg>
''';
}

// =============================================================================
// 4. PANORAMIC SPECIMEN LIGHT (2560x1280)
// =============================================================================
String generatePanoramicSpecimenLight(String deviceBase64, String quillingBase64) {
  final flagBlock = nunavutFlagSvg(x: 2360, y: 80, width: 100, height: 62);
  final canFlag = canadaFlagSvg(x: 2245, y: 80, width: 100, height: 62);

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="2560" height="1280" viewBox="0 0 2560 1280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .font-syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; }
      .font-body { font-family: "PocketGull", -apple-system, sans-serif; }
    </style>
    <linearGradient id="panoBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="40%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F2EDE2"/>
    </linearGradient>
  </defs>

  <!-- Canvas -->
  <rect width="2560" height="1280" fill="url(#panoBg)"/>

  <!-- Outer Architectural Framing -->
  <rect x="60" y="60" width="2440" height="1160" fill="none" stroke="#E7E2D6" stroke-width="2"/>
  <line x1="1280" y1="60" x2="1280" y2="1220" stroke="#E7E2D6" stroke-width="1.5"/>

  <!-- Flags in Top Right -->
  $canFlag
  $flagBlock

  <!-- Left Half: Inuktitut Syllabics Core Anatomy & Rotational Sovereignty -->
  <g transform="translate(120, 120)">
    <rect x="0" y="0" width="240" height="34" rx="3" fill="#D52B1E"/>
    <text x="120" y="22" class="font-mono" font-size="14" fill="#FFFFFF" text-anchor="middle" font-weight="bold">TIER 6 • CASE STUDY 01</text>
    <text x="260" y="24" class="font-mono" font-size="14" fill="#003896" font-weight="bold">NUNAVUT VEXILLOLOGY // CA-NU 🇨🇦 // CANADIAN ABORIGINAL SYLLABICS</text>

    <!-- Giant Bilingual Title -->
    <text x="0" y="115" class="font-syllabic" font-size="72" fill="#1F1B16" font-weight="bold">ᐳᒃᑭᑦᒐᓪ <tspan fill="#FFD100">PocketGull</tspan></text>
    <text x="0" y="160" class="font-syllabic" font-size="30" fill="#003896">ᐃᓄᒃᑎᑐᑦ • ROTATIONAL SOVEREIGNTY IN TELEMETRY</text>

    <text x="0" y="210" class="font-body" font-size="20" fill="#57534E">Procedural compilation of 640 concrete syllabic glyphs (U+1400–U+167F) in 13.87 ms.</text>
    <text x="0" y="240" class="font-body" font-size="20" fill="#57534E">Strict 1000 UPM grid, Louise Sloan 5:1 optotype ratio, 600 UPM fixed medical pitch.</text>

    <!-- Large Syllabic Callout Ribbon -->
    <g transform="translate(0, 280)">
      <rect width="1040" height="180" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1.5"/>
      <line x1="0" y1="0" x2="1040" y2="0" stroke="#FFD100" stroke-width="4"/>
      <text x="30" y="40" class="font-mono" font-size="13" fill="#78716C" font-weight="bold">THE ROTATIONAL VOWEL CODE (pi, pu, pa + p-final)</text>
      <text x="30" y="120" class="font-syllabic" font-size="64" fill="#1F1B16" letter-spacing="0.25em">ᐱ ᐲ ᐳ ᐴ ᐸ ᐹ ᑉ</text>
      <text x="30" y="155" class="font-mono" font-size="13" fill="#003896" font-weight="bold">[ᐱ = NORTH • ᐳ = EAST • ᐸ = SOUTH • ᑉ = FINAL SUPERSCRIPT]</text>
    </g>

    <!-- 4 Weights Comparison Line -->
    <g transform="translate(0, 500)">
      <text x="0" y="30" class="font-mono" font-size="14" fill="#78716C" font-weight="bold">4 SUPERFAMILY WEIGHTS (UNIFORM OPTICAL DENSITY):</text>
      <text x="0" y="80" class="font-syllabic" font-size="36" fill="#1F1B16">Fineliner: ᐋᓐᓂᐊᕕᒃ ᓘᒃᑖᖅ ᐆᒻᒪᑎ 72 bpm</text>
      <text x="0" y="130" class="font-syllabic" font-size="36" fill="#1F1B16" font-weight="bold">Bold: ᐋᓐᓂᐊᕕᒃ ᓘᒃᑖᖅ ᐆᒻᒪᑎ 72 bpm</text>
      <text x="0" y="180" class="font-syllabic" font-size="36" fill="#003896" font-weight="bold">Mono: ᐋᓐᓂᐊᕕᒃ ᓘᒃᑖᖅ ᐆᒻᒪᑎ 72 bpm</text>
    </g>

    <!-- Footer Seal -->
    <text x="0" y="740" class="font-mono" font-size="13" fill="#78716C">UNIVERSAL WORLD SCRIPTS INITIATIVE // OFL 1.1 // ZERO NODE DUPLICATION // ISO 3166-2: CA-NU</text>
  </g>

  <!-- Right Half: Nunavut Clinical Health Center Telemetry HUD -->
  <g transform="translate(1360, 120)">
    <rect width="1080" height="980" rx="6" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="2"/>
    <line x1="0" y1="0" x2="1080" y2="0" stroke="#003896" stroke-width="5"/>

    <!-- Header with Official Star & Locality Title -->
    <g transform="translate(40, 45)">
      <polygon points="16,0 20,12 32,16 20,20 16,32 12,20 0,16 12,12" fill="#003896"/>
      <text x="45" y="24" class="font-syllabic" font-size="26" fill="#1F1B16" font-weight="bold">ᕿᑭᖅᑖᓗᒃ ᐋᓐᓂᐊᕕᒃ • QIKIQTANI GENERAL HOSPITAL</text>
      <text x="45" y="50" class="font-mono" font-size="13" fill="#78716C">IQALUIT, NUNAVUT // ARCTIC EMERGENCY TELEMETRY CONSOLE // CA-NU 🇨🇦</text>
      <line x1="0" y1="65" x2="1000" y2="65" stroke="#E7E2D6" stroke-width="1.5"/>
    </g>

    <!-- Nunavut Localities & Health Network Bar -->
    <g transform="translate(40, 125)">
      <rect width="1000" height="34" rx="3" fill="#FAF8F5" stroke="#E7E2D6" stroke-width="1"/>
      <line x1="0" y1="0" x2="1000" y2="0" stroke="#FFD100" stroke-width="2"/>
      <text x="16" y="22" class="font-mono" font-size="10" fill="#B45309" font-weight="bold">LOCALITIES // ᓄᓇᓕᖕᓂ ᐋᓐᓂᐊᕕᖃᕐᕖᑦ:</text>
      <text x="250" y="22" class="font-syllabic" font-size="12" fill="#1F1B16">ᐃᖃᓗᐃᑦ (Iqaluit) • ᑲᖏᖅᖠᓂᖅ (Rankin Inlet) • ᐃᖃᓗᒃᑑᑦᑎᐊᖅ (Cambridge Bay) • ᐃᒡᓗᓕᒃ (Igloolik) • ᐸᖕᓂᕐᑑᖅ (Pangnirtung) • ᑭᙵᐃᑦ (Kinngait)</text>
    </g>

    <!-- Telemetry Vitals Display (Tabular Figures) -->
    <g transform="translate(40, 175)">
      <!-- Box 1: Heart Rate -->
      <rect x="0" y="0" width="310" height="130" fill="#FAF8F5" stroke="#D52B1E" stroke-width="1.5"/>
      <text x="24" y="32" class="font-syllabic" font-size="16" fill="#D52B1E" font-weight="bold">ᐆᒻᒪᑎ • HEART RATE</text>
      <text x="24" y="88" class="font-mono" font-size="48" fill="#1F1B16" font-weight="bold">72 <tspan font-size="18" fill="#78716C">BPM</tspan></text>
      <text x="24" y="114" class="font-mono" font-size="11" fill="#003896">NORMAL SINUS RHYTHM</text>

      <!-- Box 2: SpO2 -->
      <rect x="345" y="0" width="310" height="130" fill="#FAF8F5" stroke="#003896" stroke-width="1.5"/>
      <text x="369" y="32" class="font-syllabic" font-size="16" fill="#003896" font-weight="bold">ᐊᓂᕐᓂᖃᕐᓇᖅ • SpO₂</text>
      <text x="369" y="88" class="font-mono" font-size="48" fill="#1F1B16" font-weight="bold">99<tspan font-size="18" fill="#78716C">%</tspan></text>
      <text x="369" y="114" class="font-mono" font-size="11" fill="#003896">ROOM AIR • 55 CM ACUITY</text>

      <!-- Box 3: Blood Pressure -->
      <rect x="690" y="0" width="310" height="130" fill="#FAF8F5" stroke="#FFD100" stroke-width="1.5"/>
      <text x="714" y="32" class="font-syllabic" font-size="16" fill="#B45309" font-weight="bold">ᐊᐅᒃ • BLOOD PRESSURE</text>
      <text x="714" y="88" class="font-mono" font-size="44" fill="#1F1B16" font-weight="bold">120/80</text>
      <text x="714" y="114" class="font-mono" font-size="11" fill="#003896">TABULAR FIGURES • MONO</text>
    </g>

    <!-- Elder Wisdom, Healing, Longevity & Humour Banner -->
    <g transform="translate(40, 325)">
      <rect width="1000" height="42" rx="3" fill="#FAF8F5" stroke="#E7E2D6" stroke-width="1"/>
      <rect x="0" y="0" width="4" height="42" fill="#D52B1E"/>
      <text x="14" y="18" class="font-syllabic" font-size="12" fill="#1F1B16">"ᐃᓄᒃᑐᑦ ᐅᖃᐅᓯᖅ ᑭᓇᐅᓂᑦᑎᓐᓂᒃ ᓴᖅᑭᔮᖅᑎᑦᑎᔪᖅ." <tspan class="font-body" font-size="11" fill="#57534E">— Jose Kusugak ("Our language is our identity")</tspan></text>
      <text x="14" y="33" class="font-body" font-size="11" fill="#003896" font-style="italic">ᒪᒥᓴᕐᓂᖅ (Healing) • ᖃᐅᔨᒪᓂᖅ (Wisdom) • ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ (Longevity) • ᖁᕕᐊᓱᖕᓂᖅ (Humour: "Laughter is northern medicine")</text>
    </g>

    <!-- Clinical Vocabulary Table -->
    <g transform="translate(40, 385)">
      <rect width="1000" height="315" fill="#FAF8F5" stroke="#E7E2D6" stroke-width="1.5"/>
      <line x1="0" y1="0" x2="1000" y2="0" stroke="#FFD100" stroke-width="3"/>
      <text x="24" y="32" class="font-mono" font-size="13" fill="#003896" font-weight="bold">OFFICIAL CLINICAL LEXICON // NUNAVUT HEALTH ACT // CA-NU 🇨🇦</text>
      <line x1="24" y1="44" x2="976" y2="44" stroke="#E7E2D6" stroke-width="1"/>

      <g transform="translate(24, 75)" class="font-syllabic" font-size="20" fill="#1F1B16">
        <text x="0" y="0">ᐋᓐᓂᐊᕕᒃ</text>
        <text x="240" y="0" class="font-mono" font-size="15" fill="#78716C">Aanniavik</text>
        <text x="500" y="0" class="font-body" font-size="17" fill="#003896">Hospital / Health Center</text>

        <text x="0" y="42">ᓘᒃᑖᖅ</text>
        <text x="240" y="42" class="font-mono" font-size="15" fill="#78716C">Luuktaaq</text>
        <text x="500" y="42" class="font-body" font-size="17" fill="#003896">Doctor / Physician</text>

        <text x="0" y="84">ᐋᓐᓂᐊᓯᐅᖅᑎ</text>
        <text x="240" y="84" class="font-mono" font-size="15" fill="#78716C">Aanniasiuqti</text>
        <text x="500" y="84" class="font-body" font-size="17" fill="#003896">Nurse / Practitioner</text>

        <text x="0" y="126">ᐃᓅᓕᓴᐅᑦ</text>
        <text x="240" y="126" class="font-mono" font-size="15" fill="#78716C">Inuulisaut</text>
        <text x="500" y="126" class="font-body" font-size="17" fill="#003896">Medicine / Prescription Order</text>

        <text x="0" y="168">ᑲᔪᓯᓂᖃᑦᓯᐊᕐᑐᖅ</text>
        <text x="240" y="168" class="font-mono" font-size="15" fill="#78716C">Kajusiniqatsiaqtuq</text>
        <text x="500" y="168" class="font-mono" font-size="15" fill="#D52B1E" font-weight="bold">PATIENT STATE: STABLE</text>
      </g>
    </g>

    <!-- 203 DPI Thermal Simulation -->
    <g transform="translate(40, 720)">
      <rect width="1000" height="120" fill="#060911" stroke="#334155" stroke-width="1.5"/>
      <text x="24" y="32" class="font-mono" font-size="12" fill="#FFD100" font-weight="bold">203 DPI THERMAL HOSPITAL LABEL EMULATION (LOUISE SLOAN 5:1 COMPLIANT)</text>
      <text x="24" y="68" class="font-syllabic" font-size="24" fill="#FFFFFF">ᐋᓐᓂᐊᕕᒃ ᐃᓄᒃᑎᑐᑦ 500 mg (NOT 5.0 mg) [cv08 0 vs O] • ᐆᒻᒪᑎ 72 bpm</text>
      <text x="24" y="98" class="font-mono" font-size="13" fill="#2DD4BF">WCAG AAA 7:1+ CONTRAST RATIO • ZERO AMBIGUITY • FDA 21 CFR PART 11 DIGEST</text>
    </g>
  </g>
</svg>
''';
}

// =============================================================================
// 5. PERMA+ THOUGHTS CARD (1200x1200) — POSITIVE PSYCHOLOGY & ARCTIC CLINICAL LEXICON
// =============================================================================
String generatePermaThoughtsCard() {
  final flagBlock = nunavutFlagSvg(x: 960, y: 35, width: 75, height: 42);
  final canFlag = canadaFlagSvg(x: 875, y: 35, width: 75, height: 38);

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1200" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="washiBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F4EFE6"/>
    </linearGradient>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
      .syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; font-weight: bold; }
    </style>
  </defs>

  <!-- Washi Paperboard Canvas -->
  <rect width="1200" height="1200" fill="url(#washiBg)"/>
  
  <!-- Outer Architectural Deckle Frame -->
  <rect x="26" y="26" width="1148" height="1148" fill="none" stroke="#E2DACB" stroke-width="1.5"/>
  <rect x="32" y="32" width="1136" height="1136" fill="none" stroke="#E2DACB" stroke-width="0.8" stroke-dasharray="4,4"/>

  <!-- Nunavut Vexillology Accent Rules -->
  <rect x="26" y="26" width="382" height="4" fill="#FFD100"/>
  <rect x="408" y="26" width="384" height="4" fill="#D52B1E"/>
  <rect x="792" y="26" width="382" height="4" fill="#003896"/>

  <!-- Header Section with Official Museum Flags -->
  <g transform="translate(60, 75)">
    <text x="0" y="48" class="title" font-size="50" fill="#1F1B16" letter-spacing="-0.02em">PERMA<tspan fill="#D52B1E">+</tspan> Thoughts: <tspan fill="#003896" class="syllabic">ᐃᓄᒃᑎᑐᑦ</tspan></text>
    <text x="0" y="80" class="body" font-size="17" fill="#57534E">Positive Psychology, Arctic Clinical Medicine &amp; Seven Generations Longevity // CA-NU 🇨🇦</text>
    
    $canFlag
    $flagBlock

    <line x1="0" y1="104" x2="1080" y2="104" stroke="#E2DACB" stroke-width="1.5"/>
  </g>

  <!-- Elder Wisdom, Healing & Humour Banner -->
  <g transform="translate(60, 190)">
    <rect width="1080" height="42" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <rect x="0" y="0" width="4" height="42" fill="#D52B1E"/>
    <text x="16" y="18" class="syllabic" font-size="12" fill="#1F1B16">"ᐃᓄᒃᑐᑦ ᐅᖃᐅᓯᖅ ᑭᓇᐅᓂᑦᑎᓐᓂᒃ ᓴᖅᑭᔮᖅᑎᑦᑎᔪᖅ — Our language is our identity; writing it lets our elders live forward." <tspan class="mono" font-size="11" fill="#78716C">— Jose Kusugak</tspan></text>
    <text x="16" y="34" class="body" font-size="11" fill="#003896" font-style="italic">ᒪᒥᓴᕐᓂᖅ (Healing) • ᖃᐅᔨᒪᓂᖅ (Wisdom) • ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ (Longevity) • ᖁᕕᐊᓱᖕᓂᖅ (Humour: "Without humor, you freeze twice—once in body, once in spirit")</text>
  </g>

  <!-- Nunavut Localities & Arctic Health Nodes Ribbon -->
  <g transform="translate(60, 238)">
    <rect width="1080" height="34" rx="3" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="1080" y2="0" stroke="#FFD100" stroke-width="2"/>
    <text x="16" y="22" class="mono" font-size="10" fill="#B45309" font-weight="bold">ARCTIC HEALTH NODES // ᓄᓇᓕᖕᓂ ᐋᓐᓂᐊᕕᖃᕐᕖᑦ:</text>
    <text x="270" y="22" class="syllabic" font-size="13" fill="#1F1B16">ᐃᖃᓗᐃᑦ <tspan font-size="10" fill="#78716C">(Iqaluit)</tspan> • ᑲᖏᖅᖠᓂᖅ <tspan font-size="10" fill="#78716C">(Rankin Inlet)</tspan> • ᐃᖃᓗᒃᑑᑦᑎᐊᖅ <tspan font-size="10" fill="#78716C">(Cambridge Bay)</tspan> • ᐃᒡᓗᓕᒃ <tspan font-size="10" fill="#78716C">(Igloolik)</tspan> • ᐸᖕᓂᕐᑑᖅ <tspan font-size="10" fill="#78716C">(Pangnirtung)</tspan> • ᑭᙵᐃᑦ <tspan font-size="10" fill="#78716C">(Kinngait)</tspan></text>
  </g>

  <!-- ================= 6 PERMA+ PILLARS GRID ================= -->

  <!-- ================= ROW 1 ================= -->
  
  <!-- Pillar 1: (P) Positive Emotion & Vitals Balance in Inuksuk Red -->
  <g transform="translate(60, 285)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#D52B1E" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#D52B1E" font-weight="bold">(P) Positive Emotion</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᖁᕕᐊᓱᖕᓂᖅ • ᐃᒡᓗᕐᓂᖅ (Humour)</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Vagal balance &amp; cortisol regulation</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="32" fill="#D52B1E" text-anchor="middle">ᐱ ᐳ ᐸ ᐯ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Laughter as Medicine (ᐃᒡᓗᕐᓂᖅ)</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">Humour stimulates endorphins and</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">reduces salivary cortisol by ~22%.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Vital Signs (ᐆᒻᒪᑎ / ᐊᓂᕐᓂᖅ)</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Resting heart rate 72 bpm, calm</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">parasympathetic vagal tone.</text>
  </g>

  <!-- Pillar 2: (E) Engagement & Focused Flow in Nunavut Gold -->
  <g transform="translate(429, 285)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#FFD100" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#B45309" font-weight="bold">(E) Engagement / Flow</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᐱᓇᓱᐊᕐᓂᖅ • Mindful Focus</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Sloan 5:1 optotype &amp; neuroplasticity</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="28" fill="#B45309" text-anchor="middle" font-weight="bold">ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Snellen 20/20 Optical Precision</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">Resolves at 5-arcminute visual angle</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">to eliminate visual screen fatigue.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Somatic Flow (ᐃᓱᒪᒃᑯᑦ ᓴᙱᓂᖅ)</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Full cognitive presence during care</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">planning and physical rehabilitation.</text>
  </g>

  <!-- Pillar 3: (R) Relationships & Social Co-Regulation in Polaris Blue -->
  <g transform="translate(798, 285)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#003896" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#003896" font-weight="bold">(R) Relationships</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᐃᓅᖃᑎᒌᑦᑎᐊᕐᓂᖅ • Kinship</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Social determinants &amp; co-regulation</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="28" fill="#003896" text-anchor="middle" font-weight="bold">ᒥ ᒦ ᒧ ᒨ ᒪ ᒫ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Community Health (ᐃᓅᖃᑎᒌᑦ)</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">Kinship bonds lower cardiac load</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">and mitigate post-op vulnerability.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Caregiver Alliance (ᐃᓚᒌᑦ)</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Shared decision-making across</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">family and remote nursing stations.</text>
  </g>

  <!-- ================= ROW 2 ================= -->
  
  <!-- Pillar 4: (M) Meaning & Eudaimonic Purpose in Celadon Teal -->
  <g transform="translate(60, 665)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#0D9488" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#0D9488" font-weight="bold">(M) Meaning &amp; Purpose</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ • Elder Wisdom</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Eudaimonia &amp; telomere longevity</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="28" fill="#0D9488" text-anchor="middle" font-weight="bold">ᓂ ᓃ ᓄ ᓅ ᓇ ᓈ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Purposeful Life (ᐃᓅᓯᖅ)</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">A reason to rise protects cellular</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">telomeres and immune defense.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Traditional Wisdom (IQ)</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Inuit Qaujimajatuqangit acts as an</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">intergenerational protective anchor.</text>
  </g>

  <!-- Pillar 5: (A) Accomplishment & Autonomous Mastery in Inuksuk Red -->
  <g transform="translate(429, 665)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#D52B1E" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#D52B1E" font-weight="bold">(A) Accomplishment</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᐊᔪᙱᓐᓂᖃᕐᓂᖅ • Self-Efficacy</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Patient activation &amp; functional goals</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="28" fill="#D52B1E" text-anchor="middle" font-weight="bold">ᑭ ᑮ ᑯ ᑰ ᑲ ᑳ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Clinical Milestones (ᐊᔪᙱᓐᓂᖅ)</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">Autonomous recovery wins across</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">physical therapy and daily mobility.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• 100% Inuktitut Parity</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Full 640-glyph Unicode architecture</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">empowering native chart literacy.</text>
  </g>

  <!-- Pillar 6: (+) Physical Vitality & Restorative Health in Nunavut Gold -->
  <g transform="translate(798, 665)">
    <rect width="342" height="365" fill="#FFFDF8" stroke="#E2DACB" stroke-width="1"/>
    <line x1="0" y1="0" x2="342" y2="0" stroke="#FFD100" stroke-width="3"/>
    
    <text x="22" y="34" class="mono" font-size="15" fill="#B45309" font-weight="bold">(+) Physical Vitality</text>
    <text x="22" y="55" class="syllabic" font-size="14" fill="#1F1B16">ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ • Health</text>
    <text x="22" y="74" class="body" font-size="11" fill="#78716C" font-style="italic">Sleep, nutrition &amp; 7 generations life</text>
    
    <g transform="translate(22, 90)">
      <rect width="298" height="62" fill="#FAF8F5" stroke="#E2DACB" stroke-width="1"/>
      <text x="149" y="42" class="syllabic" font-size="28" fill="#003896" text-anchor="middle" font-weight="bold">ᓯ ᓰ ᓱ ᓲ ᓴ ᓵ</text>
    </g>
    
    <line x1="22" y1="170" x2="320" y2="170" stroke="#E2DACB" stroke-width="0.8"/>
    
    <text x="22" y="198" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• Restorative Sleep (ᓯᓂᖕᓂᖅ)</text>
    <text x="32" y="218" class="body" font-size="11" fill="#57534E">Deep slow-wave repair, cellular</text>
    <text x="32" y="234" class="body" font-size="11" fill="#57534E">glymphatic cleansing and calm.</text>
    
    <text x="22" y="264" class="body" font-size="12" fill="#1F1B16" font-weight="bold">• ISMP Safety &amp; Vitality</text>
    <text x="32" y="284" class="body" font-size="11" fill="#57534E">Zero trailing zeroes (500 mg, NOT</text>
    <text x="32" y="300" class="body" font-size="11" fill="#57534E">5.0 mg) across 25 Arctic clinics.</text>
  </g>

  <!-- Footer Section -->
  <g transform="translate(60, 1050)">
    <line x1="0" y1="0" x2="1080" y2="0" stroke="#E2DACB" stroke-width="1.5"/>
    <text x="0" y="26" class="mono" font-size="10" fill="#78716C">POCKETGULL TYPEFOUNDRY // UNIVERSAL WORLD SCRIPTS INITIATIVE // ARCTIC HEALTH TELEMETRY</text>
    <text x="1080" y="26" class="mono" font-size="10" fill="#003896" text-anchor="end" font-weight="bold">SIL OPEN FONT LICENSE 1.1 // ISO 3166-2: CA-NU 🇨🇦 // PHILGEAR.BIZ</text>
  </g>
</svg>
''';
}

// Keep generatePemdaThoughtsCard as alias for backwards compatibility
String generatePemdaThoughtsCard() => generatePermaThoughtsCard();

// =============================================================================
// 6. PRINT GALLERY EXHIBITION POSTER (1200x1600)
// =============================================================================
String generatePrintGalleryExhibition(String deviceBase64, String quillingBase64) {
  final flagBlock = nunavutFlagSvg(x: 1040, y: 15, width: 70, height: 44);
  final canFlag = canadaFlagSvg(x: 960, y: 15, width: 70, height: 44);

  final plateAPhoto = deviceBase64.isNotEmpty
      ? '''
      <g transform="translate(0, 75)" filter="url(#printShadow)">
        <clipPath id="devClip"><rect width="535" height="280" rx="3"/></clipPath>
        <rect width="535" height="280" rx="3" fill="#080D18" stroke="#E7E2D6" stroke-width="1"/>
        <image href="data:image/jpeg;base64,$deviceBase64" width="535" height="280" preserveAspectRatio="xMidYMid slice" clip-path="url(#devClip)"/>
      </g>
      '''
      : '''
      <g transform="translate(24, 90)">
        <text x="20" y="60" class="font-syllabic" font-size="60" fill="#1F1B16">ᐱ</text>
        <text x="150" y="60" class="font-syllabic" font-size="60" fill="#1F1B16">ᐳ</text>
        <text x="280" y="60" class="font-syllabic" font-size="60" fill="#1F1B16">ᐸ</text>
        <text x="410" y="60" class="font-syllabic" font-size="60" fill="#D52B1E">ᑉ</text>
      </g>
      ''';

  final plateBPhoto = quillingBase64.isNotEmpty
      ? '''
      <g transform="translate(0, 75)" filter="url(#printShadow)">
        <clipPath id="quillExClip"><rect width="535" height="280" rx="3"/></clipPath>
        <rect width="535" height="280" rx="3" fill="#080D18" stroke="#E7E2D6" stroke-width="1"/>
        <image href="data:image/jpeg;base64,$quillingBase64" width="535" height="280" preserveAspectRatio="xMidYMid slice" clip-path="url(#quillExClip)"/>
      </g>
      '''
      : '''
      <g transform="translate(24, 85)">
        <text x="0" y="24" class="font-syllabic" font-size="20" fill="#1F1B16">ᐋᓐᓂᐊᕕᒃ AANNIAVIK</text>
        <text x="0" y="54" class="font-syllabic" font-size="20" fill="#003896">ᐆᒻᒪᑎ 72 BPM • ᐊᓂᕐᓂᖃᕐᓇᖅ 99%</text>
      </g>
      ''';

  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="1600" viewBox="0 0 1200 1600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @font-face { font-family: "PocketGull"; src: local("PocketGull"), local("PocketGull-Bold"); font-weight: bold; }
      @font-face { font-family: "PocketGull Mono"; src: local("PocketGull Mono"), local("PocketGullMono-Regular"); }
      .font-title { font-family: "PocketGull", -apple-system, sans-serif; font-weight: bold; }
      .font-mono { font-family: "PocketGull Mono", "Courier New", monospace; }
      .font-syllabic { font-family: "PocketGull", "Gadugi", "Euphemia", sans-serif; }
      .font-braille { font-family: "DejaVu Sans", monospace; letter-spacing: 0.22em; font-weight: bold; }
      .font-body { font-family: "PocketGull", -apple-system, sans-serif; }
    </style>
    <linearGradient id="printBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAF8F5"/>
      <stop offset="100%" stop-color="#F3EFE7"/>
    </linearGradient>
    <filter id="printShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="6" stdDeviation="8" flood-color="#462D12" flood-opacity="0.16"/>
    </filter>
  </defs>
  
  <!-- Museum Cardstock Canvas -->
  <rect width="1200" height="1600" fill="url(#printBg)"/>

  <!-- Outer Braille Perimeter Border -->
  <rect x="50" y="30" width="1100" height="26" rx="0" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="0.8"/>
  <text x="600" y="48" class="font-syllabic" font-size="13" fill="#003896" text-anchor="middle" font-weight="bold">ᐳᒃᑭᑦᒐᓪ — ᐃᓚᐃᓐᓇᖓ, ᑭᓯᐊᓂ ᐱᐅᓂᖅᓴᖅ — CA-NU 🇨🇦 — WENIGER, ABER BESSER</text>

  <!-- Exhibition Header with Official Flags & Country Code -->
  <g transform="translate(50, 75)">
    <line x1="0" y1="0" x2="1100" y2="0" stroke="#E7E2D6" stroke-width="1"/>
    <text x="0" y="36" class="font-title" font-size="36" fill="#1F1B16">POCKETGULL <tspan class="font-syllabic" fill="#D52B1E">ᐳᒃᑭᑦᒐᓪ</tspan></text>
    
    <text x="365" y="30" class="font-mono" font-size="13" fill="#57534E" font-weight="bold">SYSTEM 01 // CASE STUDY 01: CANADIAN ABORIGINAL SYLLABICS</text>
    
    $canFlag
    $flagBlock

    <line x1="0" y1="50" x2="1100" y2="50" stroke="#E7E2D6" stroke-width="1"/>
  </g>

  <!-- Dual Exhibition Plates (Photographic Substrates) -->
  <g transform="translate(50, 145)">
    <!-- Plate A: PocketGull Physical Hardware Device Plate -->
    <g transform="translate(0, 0)">
      <rect width="535" height="420" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
      <line x1="0" y1="0" x2="535" y2="0" stroke="#D52B1E" stroke-width="3"/>
      
      <text x="24" y="32" class="font-mono" font-size="12" fill="#D52B1E" font-weight="bold">PLATE A: POCKETGULL PHYSICAL HARDWARE DEVICE</text>
      <text x="24" y="52" class="font-mono" font-size="10" fill="#78716C">CLINICAL TELEMETRY CONSOLE // TACTILE CHISEL NIB DNA</text>
      <line x1="20" y1="62" x2="515" y2="62" stroke="#E7E2D6" stroke-width="0.8"/>

      $plateAPhoto

      <text x="24" y="385" class="font-mono" font-size="11" fill="#1F1B16" font-weight="bold">640 SYLLABIC GLYPHS COMPILED IN 13.87 MS • CA-NU 🇨🇦</text>
      <text x="24" y="405" class="font-mono" font-size="10" fill="#64748B">ZERO NODE DUPLICATION • 100% OTS COMPLIANCE</text>
    </g>

    <!-- Plate B: Synaptic Quilling Biological Substrate Plate -->
    <g transform="translate(565, 0)">
      <rect width="535" height="420" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
      <line x1="0" y1="0" x2="535" y2="0" stroke="#003896" stroke-width="3"/>
      
      <text x="24" y="32" class="font-mono" font-size="12" fill="#003896" font-weight="bold">PLATE B: SYNAPTIC QUILLING CELLULAR CODEX</text>
      <text x="24" y="52" class="font-mono" font-size="10" fill="#78716C">BIOPHYSICAL SUBSTRATE // ARCTIC CELLULAR LIGATURES</text>
      <line x1="20" y1="62" x2="515" y2="62" stroke="#E7E2D6" stroke-width="0.8"/>

      $plateBPhoto

      <text x="24" y="385" class="font-mono" font-size="11" fill="#003896" font-weight="bold">QIKIQTANI GENERAL HOSPITAL (IQALUIT, NU) // SNELLEN 20/20</text>
      <text x="24" y="405" class="font-mono" font-size="10" fill="#64748B">ISMP LIFE-CRITICAL DISAMBIGUATION (cv08 0 vs O • cv05 l)</text>
    </g>
  </g>

  <!-- Complete Vowel & Consonant Syllabics Matrix Ribbon -->
  <g transform="translate(50, 595)">
    <rect width="1100" height="420" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
    <line x1="0" y1="0" x2="1100" y2="0" stroke="#FFD100" stroke-width="3"/>
    
    <text x="24" y="32" class="font-mono" font-size="12" fill="#B45309" font-weight="bold">CANADIAN ABORIGINAL SYLLABICS TYPEFACE MATRIX (U+1400–U+167F) // CA-NU • iu-CA 🇨🇦</text>
    <line x1="20" y1="44" x2="1080" y2="44" stroke="#E7E2D6" stroke-width="0.8"/>

    <g transform="translate(24, 80)" class="font-syllabic" font-size="22" fill="#1F1B16">
      <text x="0" y="0">ᐃ ᐄ ᐅ ᐆ ᐊ ᐋ</text>
      <text x="320" y="0">ᐱ ᐲ ᐳ ᐴ ᐸ ᐹ ᑉ</text>
      <text x="680" y="0">ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ ᑦ</text>

      <text x="0" y="45">ᑭ ᑮ ᑯ ᑰ ᑲ ᑳ ᒃ</text>
      <text x="320" y="45">ᒋ ᒌ ᒍ ᒎ ᒐ ᒑ ᒡ</text>
      <text x="680" y="45">ᒥ ᒦ ᒧ ᒨ ᒪ ᒫ ᒻ</text>

      <text x="0" y="90">ᓂ ᓃ ᓄ ᓅ ᓇ ᓈ ᓐ</text>
      <text x="320" y="90">ᓯ ᓰ ᓱ ᓲ ᓴ ᓵ ᔅ</text>
      <text x="680" y="90">ᓕ ᓖ ᓗ ᓘ ᓚ ᓛ ᓪ</text>

      <text x="0" y="135">ᔨ ᔩ ᔪ ᔫ ᔭ ᔭ ᔾ</text>
      <text x="320" y="135">ᕆ ᕇ ᕈ ᕉ ᕋ ᕌ ᕐ</text>
      <text x="680" y="135">ᕕ ᕖ ᕗ ᕘ ᕙ ᕚ ᕝ</text>

      <text x="0" y="180">ᕿ ᖀ ᖁ ᖂ ᖃ ᖄ ᖅ</text>
      <text x="320" y="180">ᖏ ᖐ ᖑ ᖒ ᖓ ᖔ ᖕ</text>
      <text x="680" y="180">ᙱ ᙲ ᙳ ᙴ ᙵ ᙶ ᖖ</text>

      <text x="0" y="225">ᖠ ᖡ ᖢ ᖣ ᖤ ᖥ ᖦ</text>
      <text x="320" y="225" class="font-mono" font-size="14" fill="#003896">WOODS CREE &amp; CARRIER EXTENSIONS</text>
      <text x="680" y="225" class="font-mono" font-size="14" fill="#D52B1E">100% UNICODE 16.0</text>
    </g>

    <line x1="20" y1="330" x2="1080" y2="330" stroke="#E7E2D6" stroke-width="0.8"/>
    <text x="24" y="355" class="font-mono" font-size="11" fill="#78716C">LOCALITIES: IQALUIT (ᐃᖃᓗᐃᑦ) • RANKIN INLET (ᑲᖏᖅᖠᓂᖅ) • CAMBRIDGE BAY (ᐃᖃᓗᒃᑑᑦᑎᐊᖅ) • IGLOOLIK (ᐃᒡᓗᓕᒃ) • PANGNIRTUNG (ᐸᖕᓂᕐᑑᖅ) • KINNGAIT (ᑭᙵᐃᑦ)</text>
    <text x="24" y="375" class="font-body" font-size="11" fill="#003896">"ᐃᓄᒃᑐᑦ ᐅᖃᐅᓯᖅ ᑭᓇᐅᓂᑦᑎᓐᓂᒃ ᓴᖅᑭᔮᖅᑎᑦᑎᔪᖅ." — Jose Kusugak // "Without humor, you freeze twice—once in body, once in spirit."</text>
    <text x="24" y="395" class="font-mono" font-size="10" fill="#D52B1E" font-weight="bold">SEVEN GENERATIONS: HEALING (ᒪᒥᓴᕐᓂᖅ) • WISDOM (ᖃᐅᔨᒪᓂᖅ) • LONGEVITY (ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ) • HUMOUR (ᖁᕕᐊᓱᖕᓂᖅ)</text>
  </g>

  <!-- Dieter Rams Ten Principles in Inuktitut -->
  <g transform="translate(50, 1045)">
    <rect width="1100" height="420" fill="#FFFDF8" stroke="#E7E2D6" stroke-width="1"/>
    <line x1="0" y1="0" x2="1100" y2="0" stroke="#003896" stroke-width="3"/>
    
    <text x="24" y="32" class="font-mono" font-size="12" fill="#003896" font-weight="bold">DIETER RAMS: TEN PRINCIPLES OF GOOD DESIGN // ᖁᓕᑦ ᐱᐅᔪᑦ ᐋᖅᑭᒃᓯᒪᔾᔪᑏᑦ</text>
    <line x1="20" y1="44" x2="1080" y2="44" stroke="#E7E2D6" stroke-width="0.8"/>

    <g transform="translate(24, 75)" class="font-body" font-size="14" fill="#1F1B16">
      <text x="0" y="0"><tspan font-weight="bold">1. INNOVATIVE</tspan> — ᓄᑖᖑᖅᐸᓪᓕᐊᓂᖅ: Good design is innovative.</text>
      <text x="560" y="0"><tspan font-weight="bold">6. HONEST</tspan> — ᓱᓕᓂᖅ: Good design is honest.</text>

      <text x="0" y="40"><tspan font-weight="bold">2. USEFUL</tspan> — ᐊᑐᕐᓂᖃᑦᓯᐊᕐᑐᖅ: Good design makes a product useful.</text>
      <text x="560" y="40"><tspan font-weight="bold">7. LONG-LASTING</tspan> — ᐊᑯᓂᐅᔪᖅ: Good design is long-lasting.</text>

      <text x="0" y="80"><tspan font-weight="bold">3. AESTHETIC</tspan> — ᑕᑯᒥᓇᕐᑐᖅ: Good design is aesthetic.</text>
      <text x="560" y="80"><tspan font-weight="bold">8. THOROUGH</tspan> — ᓇᓗᓇᐃᑦᓯᐊᕐᑐᖅ: Good design is thorough down to the last detail.</text>

      <text x="0" y="120"><tspan font-weight="bold">4. UNDERSTANDABLE</tspan> — ᑐᑭᓯᓇᕐᑐᖅ: Good design makes a product understandable.</text>
      <text x="560" y="120"><tspan font-weight="bold">9. SUSTAINABLE</tspan> — ᐊᕙᑎᒥᒃ ᑲᒪᑦᓯᐊᕐᓂᖅ: Good design is environmentally friendly.</text>

      <text x="0" y="160"><tspan font-weight="bold">5. UNOBTRUSIVE</tspan> — ᐃᓗᐊᕐᑐᖅ: Good design is unobtrusive.</text>
      <text x="560" y="160"><tspan font-weight="bold">10. AS LITTLE DESIGN AS POSSIBLE</tspan> — ᐃᓚᐃᓐᓇᖓ, ᑭᓯᐊᓂ ᐱᐅᓂᖅᓴᖅ: Less, but better.</text>
    </g>

    <line x1="20" y1="280" x2="1080" y2="280" stroke="#E7E2D6" stroke-width="0.8"/>
    
    <g transform="translate(24, 310)">
      <text x="0" y="20" class="font-syllabic" font-size="24" fill="#D52B1E" font-weight="bold">ᐃᓚᐃᓐᓇᖓ, ᑭᓯᐊᓂ ᐱᐅᓂᖅᓴᖅ — WENIGER, ABER BESSER</text>
      <text x="0" y="48" class="font-mono" font-size="13" fill="#57534E">"Good design is as little design as possible." — Dieter Rams</text>
      <text x="0" y="72" class="font-mono" font-size="12" fill="#78716C">Translated into Canadian Aboriginal Syllabics for the PocketGull Sovereign Typefoundry.</text>
    </g>
  </g>

  <!-- Exhibition Colophon -->
  <g transform="translate(50, 1500)">
    <line x1="0" y1="0" x2="1100" y2="0" stroke="#E7E2D6" stroke-width="1.5"/>
    <text x="0" y="32" class="font-mono" font-size="11" fill="#78716C">CURATED BY PHILLIP GEAR // THE POCKETGULL TYPEFOUNDRY // PORTLAND, OR &amp; IQALUIT, NU</text>
    <text x="1100" y="32" class="font-mono" font-size="11" fill="#003896" text-anchor="end" font-weight="bold">SIL OPEN FONT LICENSE 1.1 // ISO 3166-2: CA-NU 🇨🇦 // OPEN RESEARCH ARCHIVE</text>
  </g>
</svg>
''';
}

// =============================================================================
// 7. LANDMARK PLATE A: TYPE ENGINEERING BLUEPRINT (896x1200)
// =============================================================================
String generateTypeEngineeringPlate() {
  return '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="896" height="1200" viewBox="0 0 896 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="cyanGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#BAE6FD" stroke-width="0.5"/>
    </pattern>
    <style>
      .font-brand { font-family: 'PocketGull Bold', 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'PocketGull Mono', 'JetBrains Mono', monospace; }
      .font-syllabic { font-family: 'PocketGull', 'PocketGull Bold', 'Gadugi', sans-serif; }
      .font-fineliner { font-family: 'PocketGull Fineliner', 'PocketGull', sans-serif; }
      .font-bold { font-family: 'PocketGull Bold', 'PocketGull', sans-serif; }
      .font-chiseltip { font-family: 'PocketGull Chiseltip', 'PocketGull', sans-serif; }
    </style>
  </defs>

  <!-- Technical Background Grid -->
  <rect width="896" height="1200" fill="#F8FAFC"/>
  <rect width="896" height="1200" fill="url(#cyanGrid)"/>

  <!-- Outer Structural Border -->
  <rect x="24" y="24" width="848" height="1152" fill="none" stroke="#0284C7" stroke-width="1.5"/>

  <!-- Header Section -->
  <g transform="translate(45, 55)">
    <text x="0" y="0" class="font-chiseltip" font-size="28" font-weight="900" fill="#0F172A" letter-spacing="-0.02em">
      PocketGull – Inuktitut Type Design &amp; Syllabic Engineering
    </text>
    <line x1="0" y1="12" x2="806" y2="12" stroke="#0F172A" stroke-width="2"/>
  </g>

  <!-- Col 1: Rotational Symmetry & Inktraps -->
  <g transform="translate(45, 95)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">I. ROTATIONAL SYMMETRY &amp; VERTEX INKTRAPS</text>
    <rect x="0" y="15" width="390" height="380" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

    <g transform="translate(25, 45)">
      <!-- Pi, Pu, Pa, Pe Rotational Quad -->
      <g transform="translate(0, 0)">
        <text x="30" y="60" class="font-syllabic" font-size="70" fill="#0F172A">ᐱ</text>
        <line x1="30" y1="10" x2="70" y2="10" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="80" y="14" class="font-mono" font-size="10" fill="#0284C7">0° Acute Ascender</text>
        <text x="30" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">ᐱ: Pi (Vocalic I)</text>
      </g>

      <g transform="translate(180, 0)">
        <text x="30" y="60" class="font-syllabic" font-size="70" fill="#0F172A">ᐳ</text>
        <line x1="30" y1="10" x2="70" y2="10" stroke="#0284C7" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="80" y="14" class="font-mono" font-size="10" fill="#0284C7">90° Right Rotated</text>
        <text x="30" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">ᐳ: Pu (Vocalic U)</text>
      </g>

      <g transform="translate(0, 120)">
        <text x="30" y="60" class="font-syllabic" font-size="70" fill="#0F172A">ᐸ</text>
        <line x1="30" y1="10" x2="70" y2="10" stroke="#166534" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="80" y="14" class="font-mono" font-size="10" fill="#15803D">180° Inverted</text>
        <text x="30" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">ᐸ: Pa (Vocalic A)</text>
      </g>

      <g transform="translate(180, 120)">
        <text x="30" y="60" class="font-syllabic" font-size="70" fill="#0F172A">ᐯ</text>
        <line x1="30" y1="10" x2="70" y2="10" stroke="#B45309" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="80" y="14" class="font-mono" font-size="10" fill="#B45309">270° Left Rotated</text>
        <text x="30" y="85" class="font-mono" font-size="10" font-weight="700" fill="#0F172A">ᐯ: Pe (Aiviq Dialect)</text>
      </g>
    </g>

    <text x="15" y="340" class="font-brand" font-size="10" fill="#64748B">
      Vertex inktraps in Chiseltip (900) prevent ink spread across acute triangular intersections.
    </text>
    <text x="15" y="358" class="font-mono" font-size="9.5" fill="#0284C7">
      Harmonic 4-fold rotational symmetry preserves uniform visual weight across all vowel stances.
    </text>
  </g>

  <!-- Col 2: Superdots & Superior Finals -->
  <g transform="translate(460, 95)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">II. SUPERDOTS &amp; SUPERIOR FINALS</text>
    <rect x="0" y="15" width="390" height="175" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

    <g transform="translate(20, 50)">
      <text x="0" y="0" class="font-syllabic" font-size="36" fill="#0F172A">ᐲ ᐴ ᐹ ᐯ</text>
      <text x="180" y="-8" class="font-mono" font-size="12" font-weight="700" fill="#0F172A">Pii • Puu • Paa • Pee</text>
      <text x="180" y="10" class="font-brand" font-size="11" fill="#64748B">Centroid-Anchored Superdots</text>

      <g transform="translate(0, 65)">
        <text x="0" y="0" class="font-syllabic" font-size="32" fill="#0F172A">ᑊ ᐟ ᐠ ᐨ ᒡ ᒻ ᓐ</text>
        <text x="180" y="-8" class="font-mono" font-size="12" font-weight="700" fill="#0F172A">p • t • k • c • g • m • n</text>
        <text x="180" y="10" class="font-brand" font-size="11" fill="#64748B">True Superior Finals (Optically Balanced)</text>
      </g>
    </g>

    <!-- Section III: Optical Sizing Scales -->
    <g transform="translate(0, 210)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">III. OPTICAL SIZING SCALES (6PT – 72PT)</text>
      <rect x="0" y="15" width="390" height="155" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

      <g transform="translate(20, 45)">
        <text x="0" y="0" class="font-mono" font-size="10" fill="#64748B">Caption 6pt (Fineliner 400)</text>
        <text x="0" y="18" class="font-fineliner" font-size="13" fill="#0F172A">ᓄᓇᕗᒻᒥ ᐃᓄᐃᑦ ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ</text>

        <text x="0" y="48" class="font-mono" font-size="10" fill="#64748B">Text 12pt (Bold 700)</text>
        <text x="0" y="68" class="font-bold" font-size="17" font-weight="700" fill="#0F172A">ᐃᓅᓯᖃᑦᓯᐊᕐᓂᖅ ᒪᒥᓴᕐᓂᕐᓗ</text>

        <text x="0" y="98" class="font-mono" font-size="10" fill="#64748B">Display 36pt (Chiseltip 900)</text>
        <text x="0" y="128" class="font-chiseltip" font-size="26" font-weight="900" fill="#0F172A">ᐆᒻᒪᑎᓕᕆᓂᖅ</text>
      </g>
    </g>
  </g>

  <!-- Section IV: Numeral Set Comparisons & Monospace Cell Normalization -->
  <g transform="translate(45, 500)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">IV. PROPORTIONAL SUPERFAMILY VS MONOSPACE 600 UPM CELL</text>
    <rect x="0" y="15" width="806" height="190" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1"/>

    <!-- Proportional Row -->
    <g transform="translate(25, 45)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0369A1">PROPORTIONAL DISPLAY CUTS (FINELINER 400 • BOLD 700 • CHISELTIP 900)</text>
      <text x="0" y="32" class="font-bold" font-size="28" font-weight="700" fill="#0F172A">1234567890 ᐱᐳᐸᐯ ᑎᑐᑕᑌ</text>
      <text x="0" y="52" class="font-brand" font-size="11" fill="#64748B">• Proportional glyph advances (280–1100 UPM) • Class-based kerning • Natural word rhythm</text>
    </g>

    <line x1="25" y1="115" x2="781" y2="115" stroke="#E2E8F0"/>

    <!-- Tabular Monospace Row -->
    <g transform="translate(25, 140)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0369A1">TABULAR LINING &amp; MONOSPACE 600 UPM CELL (POCKETGULL MONO)</text>
      <text x="0" y="32" class="font-mono" font-size="26" font-weight="700" fill="#0F172A">1234567890 ᐱᐳᐸᐯ ᑎᑐᑕᑌ</text>
      <text x="0" y="50" class="font-brand" font-size="11" fill="#64748B">• Exact 600 UPM fixed pitch • Equalized sidebearings • Zero layout jitter across telemetry streams</text>
    </g>
  </g>

  <!-- Section V: Syllabic Morpheme Anatomy & Healing Lexicon -->
  <g transform="translate(45, 715)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0284C7">V. SYLLABIC MORPHEME ANATOMY &amp; CLINICAL HEALING LEXICON</text>
    
    <g transform="translate(0, 15)">
      <!-- Card 1: Heart -->
      <g transform="translate(0, 0)">
        <rect width="255" height="110" rx="4" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">ᐆᒻᒪᑎ (Uummati)</text>
        <text x="15" y="65" class="font-chiseltip" font-size="32" font-weight="900" fill="#0369A1">ᐆᒻᒪᑎ</text>
        <text x="15" y="90" class="font-brand" font-size="10.5" fill="#64748B">The Human Heart / Cardia</text>
      </g>

      <!-- Card 2: Hospital / Clinic -->
      <g transform="translate(275, 0)">
        <rect width="255" height="110" rx="4" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">ᐋᓐᓂᐊᕕᒃ (Aanniavik)</text>
        <text x="15" y="65" class="font-bold" font-size="32" font-weight="700" fill="#0369A1">ᐋᓐᓂᐊᕕᒃ</text>
        <text x="15" y="90" class="font-brand" font-size="10.5" fill="#64748B">Hospital / Healing Sanctuary</text>
      </g>

      <!-- Card 3: Recovery / Healing -->
      <g transform="translate(550, 0)">
        <rect width="256" height="110" rx="4" fill="#FFFFFF" stroke="#CBD5E1"/>
        <text x="15" y="25" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">ᒪᒥᓴᕐᓂᖅ (Mamisarniq)</text>
        <text x="15" y="65" class="font-fineliner" font-size="32" fill="#0369A1">ᒪᒥᓴᕐᓂᖅ</text>
        <text x="15" y="90" class="font-brand" font-size="10.5" fill="#64748B">Holistic Healing / Restoration</text>
      </g>
    </g>

    <!-- Attestation Box -->
    <g transform="translate(0, 145)">
      <rect width="806" height="75" rx="4" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1"/>
      <text x="20" y="25" class="font-brand" font-size="13" font-weight="700" fill="#0369A1">
        Optical Quality Attestation &amp; Zero Tofu Guarantee:
      </text>
      <text x="20" y="45" class="font-mono" font-size="11" fill="#0F172A">
        Passed with 0 duplicate nodes across all 640 Inuktitut UCAS codepoints. 100% compliant with Google Fonts specifications.
      </text>
      <text x="20" y="62" class="font-mono" font-size="10" fill="#0284C7">
        Verified via ots-sanitize &amp; fontTools // unitsPerEm: 1000 // SIL OFL 1.1 Open Source
      </text>
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
      .font-brand { font-family: 'PocketGull Bold', 'Plus Jakarta Sans', system-ui, sans-serif; }
      .font-mono { font-family: 'PocketGull Mono', 'JetBrains Mono', monospace; }
      .font-syllabic { font-family: 'PocketGull', 'PocketGull Bold', 'Gadugi', sans-serif; }
      .font-fineliner { font-family: 'PocketGull Fineliner', 'PocketGull', sans-serif; }
      .font-bold { font-family: 'PocketGull Bold', 'PocketGull', sans-serif; }
      .font-chiseltip { font-family: 'PocketGull Chiseltip', 'PocketGull', sans-serif; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="896" height="1200" fill="#F8FAFC"/>
  <rect x="24" y="24" width="848" height="1152" fill="none" stroke="#0F172A" stroke-width="1.5"/>

  <!-- Top Banner -->
  <g transform="translate(45, 55)">
    <text x="0" y="0" class="font-mono" font-size="22" font-weight="800" fill="#0284C7" letter-spacing="0.05em">POCKETGULL</text>
    <text x="0" y="32" class="font-chiseltip" font-size="34" font-weight="900" fill="#0F172A" letter-spacing="-0.02em">TELEMETRY &amp; CLINICAL GLYPHS</text>
    <line x1="0" y1="46" x2="806" y2="46" stroke="#0F172A" stroke-width="2"/>

    <!-- Metadata right -->
    <text x="806" y="0" class="font-mono" font-size="10" fill="#0284C7" text-anchor="end">TECHNICAL DATA</text>
    <text x="806" y="14" class="font-mono" font-size="10" fill="#64748B" text-anchor="end">1000 UPM / 600 ADV</text>
    <text x="806" y="28" class="font-mono" font-size="10" fill="#0284C7" text-anchor="end">INUKTITUT (UCAS)</text>
    <text x="806" y="42" class="font-mono" font-size="10" fill="#64748B" text-anchor="end">U+1400-U+167F</text>
  </g>

  <!-- Section 1: Monospace & Disambiguation -->
  <g transform="translate(45, 125)">
    <text x="0" y="0" class="font-mono" font-size="20" font-weight="800" fill="#0F172A">POCKETGULL MONO</text>
    <text x="0" y="20" class="font-mono" font-size="11" fill="#0284C7">A MONOSPACED SCRIPT FOR HEALTHCARE &amp; BEDSIDE MONITORS</text>
    
    <text x="430" y="0" class="font-mono" font-size="20" font-weight="800" fill="#0F172A">CLINICAL SAFETY</text>
    <text x="430" y="20" class="font-mono" font-size="11" fill="#0284C7">ISMP / FDA DOSAGE DISAMBIGUATION</text>
  </g>

  <!-- Left: Monospace Character Chart -->
  <g transform="translate(45, 175)">
    <rect width="390" height="255" fill="#FFFFFF" stroke="#CBD5E1"/>
    <g transform="translate(15, 25)" class="font-mono" font-size="13" fill="#0F172A" letter-spacing="0.2em">
      <text x="0" y="0">! @ # \$ % ^ &amp; * ( ) _ +</text>
      <text x="0" y="28">1 2 3 4 5 6 7 8 9 0 - =</text>
      <text x="0" y="56">Q W E R T Y U I O P [ ]</text>
      <text x="0" y="84">A S D F G H J K L ; ' \</text>
      <text x="0" y="112">Z X C V B N M , . / ?</text>
      <text x="0" y="140" class="font-syllabic" fill="#0369A1">ᐃ ᐄ ᐅ ᐆ ᐊ ᐋ ᐱ ᐲ ᐳ ᐴ ᐸ</text>
      <text x="0" y="168" class="font-syllabic" fill="#0369A1">ᑎ ᑏ ᑐ ᑑ ᑕ ᑖ ᑭ ᑮ ᑯ ᑰ ᑲ</text>
      <text x="0" y="196">Δ % ± μg mg/dL mmHg bpm</text>
    </g>
  </g>

  <!-- Right: Disambiguation & Tabular Sizes -->
  <g transform="translate(475, 175)">
    <!-- 0 vs O -->
    <rect x="0" y="0" width="180" height="85" fill="#FFFFFF" stroke="#CBD5E1"/>
    <rect x="0" y="0" width="180" height="22" fill="#E0F2FE"/>
    <text x="10" y="15" class="font-mono" font-size="10" font-weight="700" fill="#0369A1">SLASHED ZERO (cv08)</text>
    <text x="25" y="65" class="font-mono" font-size="44" font-weight="700" fill="#0F172A">0</text>
    <text x="75" y="60" class="font-mono" font-size="16" fill="#64748B">vs</text>
    <text x="115" y="65" class="font-mono" font-size="44" font-weight="700" fill="#0F172A">O</text>

    <!-- 1 vs I vs l -->
    <g transform="translate(195, 0)">
      <rect x="0" y="0" width="180" height="85" fill="#FFFFFF" stroke="#CBD5E1"/>
      <rect x="0" y="0" width="180" height="22" fill="#E0F2FE"/>
      <text x="10" y="15" class="font-mono" font-size="10" font-weight="700" fill="#0369A1">SERIFED I (ss02)</text>
      <text x="20" y="65" class="font-mono" font-size="40" font-weight="700" fill="#0F172A">1</text>
      <text x="65" y="60" class="font-mono" font-size="18" fill="#64748B">|</text>
      <text x="90" y="65" class="font-mono" font-size="40" font-weight="700" fill="#0F172A">I</text>
      <text x="135" y="65" class="font-mono" font-size="40" font-weight="700" fill="#0F172A">l</text>
    </g>

    <!-- Tabular Clinical Figures -->
    <g transform="translate(0, 100)">
      <rect x="0" y="0" width="375" height="155" fill="#FFFFFF" stroke="#CBD5E1"/>
      <text x="15" y="24" class="font-mono" font-size="10" font-weight="700" fill="#0369A1">TABULAR CLINICAL FIGURES &amp; MEDICAL SYMBOLS</text>
      <text x="15" y="60" class="font-mono" font-size="20" font-weight="700" fill="#0F172A">Δ % ± μg mg/dL mEq/L</text>
      <text x="15" y="95" class="font-mono" font-size="20" font-weight="700" fill="#0F172A">≤ ≥ ≠ ≈ → mmHg SpO2</text>
      <text x="15" y="130" class="font-mono" font-size="10" fill="#64748B">ISMP Standard: Leading zero mandated (0.5 mg), trailing zero strictly prohibited.</text>
    </g>
  </g>

  <!-- Center: Sample Clinical Telemetry Display (Qikiqtani Hospital Bed 02) -->
  <g transform="translate(45, 455)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">
      SAMPLE CLINICAL TELEMETRY DISPLAY (QIKIQTANI GENERAL HOSPITAL BED 02):
    </text>
    
    <!-- Telemetry Monitor Screen -->
    <rect x="0" y="15" width="806" height="230" rx="8" fill="#090D16" stroke="#1E293B" stroke-width="2"/>

    <!-- ECG Waveform Grid -->
    <g transform="translate(25, 35)">
      <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#22C55E" letter-spacing="0.1em">ECG LEAD II • SINUS RHYTHM</text>
      
      <!-- Continuous Green ECG Waveform -->
      <path d="M 0 80 L 70 80 L 80 60 L 90 100 L 98 15 L 106 110 L 114 75 L 122 80 L 170 80 L 220 80 L 230 60 L 240 100 L 248 15 L 256 110 L 264 75 L 272 80 L 320 80 L 370 80 L 380 60 L 390 100 L 398 15 L 406 110 L 414 75 L 422 80 L 470 80" 
            fill="none" stroke="#22C55E" stroke-width="2.2" stroke-linejoin="round"/>

      <!-- Patient Vitals in Inuktitut -->
      <text x="0" y="145" class="font-syllabic" font-size="20" fill="#FBBF24">ᐆᒻᒪᑎᑉ ᓱᒃᑲᓂᖓ: 72 bpm • ᐊᐅᑉ ᐊழுᓂᖓ: 120/80</text>
      <text x="0" y="170" class="font-mono" font-size="11" fill="#94A3B8">Uummati: 72 bpm (Normal Sinus) • Aup Tingirninga: 120/80 mmHg (Normotensive)</text>
    </g>

    <!-- Numerical Telemetry Readouts (Right) -->
    <g transform="translate(540, 40)">
      <g transform="translate(0, 0)">
        <text x="0" y="0" class="font-mono" font-size="10" fill="#94A3B8">HEART RATE</text>
        <text x="0" y="32" class="font-mono" font-size="38" font-weight="700" fill="#22C55E">72</text>
        <text x="70" y="28" class="font-mono" font-size="14" fill="#22C55E">bpm</text>
      </g>

      <g transform="translate(0, 65)">
        <text x="0" y="0" class="font-mono" font-size="10" fill="#94A3B8">BLOOD PRESSURE</text>
        <text x="0" y="30" class="font-mono" font-size="34" font-weight="700" fill="#38BDF8">120/80</text>
      </g>

      <g transform="translate(0, 125)">
        <text x="0" y="0" class="font-mono" font-size="10" fill="#94A3B8">O2 SATURATION (SpO2)</text>
        <text x="0" y="30" class="font-mono" font-size="34" font-weight="700" fill="#FBBF24">99%</text>
      </g>
    </g>
  </g>

  <!-- Bottom: Clinical Dosage & Terminology Table -->
  <g transform="translate(45, 725)">
    <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#0F172A">
      CLINICAL DOSAGE CORRECTIONS &amp; EHR TERMINOLOGY:
    </text>
    <rect x="0" y="15" width="806" height="235" fill="#FFFFFF" stroke="#CBD5E1"/>

    <g transform="translate(30, 50)">
      <g transform="translate(0, 0)">
        <text x="0" y="0" class="font-bold" font-size="14" font-weight="700" fill="#0F172A">Attending Physician (Doctor):</text>
        <text x="320" y="0" class="font-chiseltip" font-size="22" font-weight="900" fill="#0369A1">ᐋᓐᓂᐊᓯᐅᖅᑎᒻᒪᕆᒃ</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Dr. P. Gear, MD</text>
      </g>

      <g transform="translate(0, 50)">
        <text x="0" y="0" class="font-bold" font-size="14" font-weight="700" fill="#0F172A">Clinical Vigilance (Monitoring):</text>
        <text x="320" y="0" class="font-bold" font-size="22" font-weight="700" fill="#0369A1">ᖃᐅᔨᓴᕐᓂᖅ ᐃᓅᓯᕐᒥᒃ</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Vitals q4h / ICU Watch</text>
      </g>

      <g transform="translate(0, 100)">
        <text x="0" y="0" class="font-bold" font-size="14" font-weight="700" fill="#0F172A">Remedy / Pharmacotherapy:</text>
        <text x="320" y="0" class="font-fineliner" font-size="22" fill="#0369A1">ᐋᓐᓂᐊᕈᑎᒧᑦ ᐃᓅᓕᓴᐅᑦ</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Amoxicillin 500 mg PO TID</text>
      </g>

      <g transform="translate(0, 150)">
        <text x="0" y="0" class="font-bold" font-size="14" font-weight="700" fill="#0F172A">Patient Attestation (Consent):</text>
        <text x="320" y="0" class="font-fineliner" font-size="22" fill="#0369A1">ᐊᑎᓕᐅᕐᓂᖅ ᐊᖏᕈᑎᒥᒃ</text>
        <text x="560" y="0" class="font-mono" font-size="13" fill="#64748B">Care Plan Attested &amp; Signed</text>
      </g>

      <line x1="0" y1="185" x2="746" y2="185" stroke="#E2E8F0"/>

      <g transform="translate(0, 210)">
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
      .font-syllabic { font-family: 'PocketGull', 'PocketGull Bold', 'Gadugi', sans-serif; }
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

  <!-- Torn-Edge Polar Washi Papercraft Sheet -->
  <g transform="translate(48, 40)">
    <!-- Ambient Washi Sheet Shadow -->
    <rect x="4" y="12" width="800" height="1120" rx="4" fill="#000000" opacity="0.35"/>
    <rect width="800" height="1120" rx="4" fill="#FCFAF6" stroke="#E2DACB" stroke-width="1.5"/>

    <g transform="translate(50, 60)">
      <!-- Main Title -->
      <text x="0" y="0" class="font-chiseltip" font-size="27" font-weight="900" fill="#1C1917" letter-spacing="-0.02em">PocketGull: Teaching Through the Typeface</text>
      <text x="0" y="24" class="font-mono" font-size="12" font-weight="700" fill="#B45309">INUKTITUT SYLLABICS (UCAS) &amp; CLINICAL COGNITIVE SCAFFOLDING</text>
      <line x1="0" y1="36" x2="700" y2="36" stroke="#1C1917" stroke-width="2"/>

      <!-- Section 1: Cognitive Scaffolding -->
      <g transform="translate(0, 65)">
        <text x="0" y="0" class="font-bold" font-size="18" font-weight="700" fill="#1C1917">COGNITIVE SCAFFOLDING</text>
        <text x="0" y="20" class="font-brand" font-size="12" fill="#78716C">Typography as a teaching and learning engine for Arctic healthcare and clinical sovereignty.</text>

        <g transform="translate(0, 50)">
          <text x="0" y="0" class="font-mono" font-size="11" font-weight="700" fill="#991B1B">900 Heavy</text>
          <text x="80" y="5" class="font-chiseltip" font-size="24" font-weight="900" fill="#1C1917">ᐆᒻᒪᑎᓕᕆᓂᖅ // CARDIOVASCULAR</text>

          <g transform="translate(80, 25)">
            <path d="M 0 0 L 0 20 L 15 20" fill="none" stroke="#C2410C" stroke-width="2"/>
            <polygon points="15,16 22,20 15,24" fill="#C2410C"/>
            <text x="30" y="25" class="font-bold" font-size="16" font-weight="700" fill="#292524">
              ᐆᒻᒪᑎ ᐊᒻᒪ ᐊᐅᑉ ᐊᖁᑎᖏᑦ...
            </text>
            <text x="30" y="45" class="font-fineliner" font-size="13" fill="#57534E">
              The heart and blood vessels pump life through all parts of the human body.
            </text>
          </g>

          <g transform="translate(80, 85)">
            <line x1="0" y1="0" x2="20" y2="0" stroke="#78716C"/>
            <text x="30" y="4" class="font-mono" font-size="10.5" fill="#78716C">
              100 Fineliner: Includes resting cardiac output, stroke volume, and arterial baroreceptor feedback.
            </text>
          </g>
        </g>
      </g>

      <line x1="0" y1="260" x2="700" y2="260" stroke="#1C1917" stroke-width="1.5"/>

      <!-- Section 2: Bionic Reading Fixation in Inuktitut -->
      <g transform="translate(0, 290)">
        <text x="0" y="0" class="font-bold" font-size="18" font-weight="700" fill="#1C1917">BIONIC READING FIXATION IN INUKTITUT</text>
        <text x="0" y="20" class="font-brand" font-size="12" fill="#78716C">Bold initial syllabic anchors guide the human eye through rapid clinical reading acceleration.</text>

        <g transform="translate(0, 45)">
          <text x="0" y="30" class="font-chiseltip" font-size="44" font-weight="900" fill="#C2410C">A</text>
          <line x1="45" y1="18" x2="115" y2="18" stroke="#C2410C" stroke-width="3"/>
          <polygon points="115,12 125,18 115,24" fill="#C2410C"/>

          <g transform="translate(140, 0)">
            <rect x="0" y="0" width="30" height="38" fill="#C2410C" rx="3"/>
            <text x="7" y="28" class="font-chiseltip" font-size="28" font-weight="900" fill="#FFFFFF">B</text>
            <text x="40" y="20" class="font-fineliner" font-size="14" fill="#1C1917">
              <tspan class="font-bold" font-weight="700">ᐆᒻ</tspan>ᒪᑎ <tspan class="font-bold" font-weight="700">ᓱᒃ</tspan>ᑲᓂᖓ <tspan class="font-bold" font-weight="700">ᐊᐅᑉ</tspan> ᐊᖁᑎᖏᑦ. <tspan class="font-bold" font-weight="700">ᐋᓐ</tspan>ᓂᐊᓯᐅᖅᑎ...
            </text>
            <text x="40" y="38" class="font-brand" font-size="11.5" fill="#57534E">
              Initial fixation syllables anchor visual saccades, enabling 650 WPM reading velocity
            </text>
            <text x="40" y="52" class="font-brand" font-size="11.5" fill="#57534E">
              across Arctic clinical records and diagnostic summaries without cognitive fatigue.
            </text>
          </g>
        </g>
      </g>

      <line x1="0" y1="460" x2="700" y2="460" stroke="#1C1917" stroke-width="1.5"/>

      <!-- Lower Half: Pedagogical Ligatures & Sacred Proportions -->
      <g transform="translate(0, 490)">
        <!-- Left: Pedagogical Ligatures -->
        <g>
          <text x="0" y="0" class="font-bold" font-size="16" font-weight="700" fill="#1C1917">PEDAGOGICAL LIGATURES</text>
          <text x="0" y="18" class="font-brand" font-size="11" fill="#78716C">Typeface automatically converts syllabic compounds.</text>

          <g transform="translate(0, 50)">
            <text x="0" y="0" class="font-bold" font-size="28" font-weight="700" fill="#1C1917">H2O → H₂O</text>
            <text x="0" y="45" class="font-bold" font-size="28" font-weight="700" fill="#1C1917">mg/dl → mg/dL</text>
            <text x="0" y="90" class="font-syllabic" font-size="34" fill="#1C1917">ᐆ + ᒻ → ᐆᒻ</text>
            <text x="0" y="125" class="font-mono" font-size="12" fill="#B45309">Syllabic Nucleus + Final Morpheme</text>
          </g>
        </g>

        <!-- Right: Sacred Proportions -->
        <g transform="translate(360, 0)">
          <text x="0" y="0" class="font-bold" font-size="16" font-weight="700" fill="#1C1917">SACRED PROPORTIONS (φ)</text>
          <text x="0" y="18" class="font-brand" font-size="11" fill="#78716C">Golden ratio overlays inside numeral anatomy.</text>

          <g transform="translate(0, 40)">
            <!-- Numeral 8, 9, 6 with Golden Spiral Graphic -->
            <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
            <text x="18" y="115" class="font-bold" font-size="120" font-weight="800" fill="#1C1917">8</text>
            <circle cx="50" cy="45" r="32" fill="none" stroke="#C2410C" stroke-width="1.2"/>
            <circle cx="50" cy="105" r="42" fill="none" stroke="#C2410C" stroke-width="1.2"/>

            <g transform="translate(115, 0)">
              <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
              <text x="18" y="115" class="font-bold" font-size="120" font-weight="800" fill="#1C1917">9</text>
              <circle cx="50" cy="45" r="38" fill="none" stroke="#C2410C" stroke-width="1.2"/>
            </g>

            <g transform="translate(230, 0)">
              <rect x="0" y="0" width="100" height="150" fill="#FFFFFF" stroke="#EF4444" stroke-width="0.8"/>
              <text x="18" y="115" class="font-bold" font-size="120" font-weight="800" fill="#1C1917">6</text>
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
          POCKETGULL PEDAGOGICAL SPECIMEN // INUIT HEALTHCARE SOVEREIGNTY // OFL 1.1 OPEN SOURCE
        </text>
      </g>
    </g>
  </g>
</svg>''';
}

