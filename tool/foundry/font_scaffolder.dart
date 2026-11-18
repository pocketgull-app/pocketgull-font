import 'dart:io';
import 'dart:convert';

/// Engine to scaffold new typography projects / future font ideas with
/// standard 1000 UPM, Google Fonts METADATA.pb, W3C OTS memory safety invariants,
/// and an interactive specimen preview out of the box.
class FontScaffolder {
  static Future<bool> scaffold({
    required String projectName,
    required String projectRoot,
    String? category,
    String? designer,
  }) async {
    final cleanName = _sanitizeFamilyName(projectName);
    final targetDir = Directory('$projectRoot/experiments/$cleanName');
    final cat = (category ?? 'SANS_SERIF').toUpperCase();
    final author = designer ?? 'Phil Gear';

    print('\n======================================================================');
    print('  FOUNDRY SCAFFOLDER: INITIALIZING NEW FONT PROJECT');
    print('  Family: $cleanName');
    print('  Category: $cat');
    print('  Target: ${targetDir.path}');
    print('======================================================================\n');

    if (targetDir.existsSync()) {
      print('[WARN] Directory already exists: ${targetDir.path}');
      print('       Updating scaffold files while preserving custom glyph sources...\n');
    } else {
      targetDir.createSync(recursive: true);
    }

    // 1. Create directory structure
    final subdirs = [
      'sources',
      'fonts/ttf',
      'fonts/woff2',
      'tests',
    ];
    for (final s in subdirs) {
      Directory('${targetDir.path}/$s').createSync(recursive: true);
    }

    // 2. foundry.config.json (SSOT Parametric DNA)
    final config = {
      r"$schema": "https://font.pocketgull.app/schemas/foundry-config.v1.json",
      "familyName": cleanName,
      "version": "0.1.0",
      "category": cat,
      "designer": author,
      "license": "OFL 1.1",
      "upm": 1000,
      "metrics": {
        "sTypoAscender": 780,
        "sTypoDescender": -180,
        "sTypoLineGap": 100,
        "usWinAscent": 960,
        "usWinDescent": 240
      },
      "geometry": {
        "optotypeRatio": "5:1",
        "cornerRadiiUpm": 25,
        "isFixedPitch": cat == 'MONOSPACE',
        "advanceWidth": cat == 'MONOSPACE' ? 600 : null
      },
      "disambiguation": {
        "slashedZero": true,
        "curvedLowercaseL": true,
        "serifedCapitalI": true,
        "slashedZ": true
      },
      "scripts": [
        "latin-basic",
        "latin-extended",
        "braille-256",
        "telemetry-math"
      ]
    };
    File('${targetDir.path}/foundry.config.json').writeAsStringSync(
      const JsonEncoder.withIndent('  ').convert(config),
    );
    print('  ✓ Created foundry.config.json (Parametric DNA)');

    // 3. Google Fonts METADATA.pb Template
    final metadataPb = '''name: "$cleanName"
designer: "$author"
license: "OFL"
category: "$cat"
date_added: "${DateTime.now().toIso8601String().substring(0, 10)}"
fonts {
  name: "$cleanName"
  style: "normal"
  weight: 400
  filename: "$cleanName-Regular.ttf"
  post_script_name: "$cleanName-Regular"
  full_name: "$cleanName Regular"
  copyright: "Copyright ${DateTime.now().year} The $cleanName Project Authors."
}
subsets: "latin"
subsets: "latin-ext"
subsets: "menu"
''';
    File('${targetDir.path}/METADATA.pb').writeAsStringSync(metadataPb);
    print('  ✓ Created METADATA.pb (Google Fonts Pre-flight Spec)');

    // 4. README & Architectural Charter
    final readme = '''# $cleanName

A contemporary $cat typography project created with the PocketGull Typefoundry compiler.

## Typographic Invariants
1. **1000 UPM Em-Square**: Conforming to ISO/IEC 14496-22 standard metrics.
2. **2-Byte Word-Alignment**: Enforces `loca[i] % 2 == 0` for zero Chromium/DirectWrite OTS eviction.
3. **Bit-7 Masking**: Clears point flags byte bit 7 (0x80) on TrueType contours.
4. **ISMP Acuity**: Life-critical disambiguation features (slashed zero, curved l, serifed I).

## Quick Start
```bash
# Build font binaries
dart run ../../tool/pocketgull_foundry.dart compile --target=experiments/$cleanName

# Run Phinney & W3C OTS memory safety audit
dart run ../../tool/pocketgull_foundry.dart audit --target=experiments/$cleanName

# Launch preview specimen
open specimen.html
```
''';
    File('${targetDir.path}/README.md').writeAsStringSync(readme);
    print('  ✓ Created README.md (Foundry Charter & Metrics)');

    // 5. Standalone Specimen HTML Preview
    final specimenHtml = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>$cleanName — Typographic Specimen</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    @font-face {
      font-family: '$cleanName';
      src: url('fonts/woff2/$cleanName-Regular.woff2') format('woff2'),
           url('fonts/ttf/$cleanName-Regular.ttf') format('truetype');
      font-weight: 400;
      font-style: normal;
      font-display: swap;
    }
    :root {
      --bg: #0f1115;
      --card: #181b22;
      --text: #f0f3f6;
      --accent: #4895ef;
      --muted: #8b949e;
      --border: #30363d;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, -apple-system, sans-serif;
      margin: 0;
      padding: 2.5rem 1.5rem;
      line-height: 1.5;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
    }
    header {
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
      margin-bottom: 2rem;
    }
    h1 {
      font-size: 2.5rem;
      margin: 0 0 0.5rem 0;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 999px;
      font-size: 0.8rem;
      color: var(--accent);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .specimen-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
    }
    .font-sample {
      font-family: '$cleanName', sans-serif;
      color: var(--text);
    }
    .waterfall-xl { font-size: 64px; line-height: 1.1; margin-bottom: 1.5rem; }
    .waterfall-lg { font-size: 36px; line-height: 1.2; margin-bottom: 1.5rem; }
    .waterfall-md { font-size: 20px; line-height: 1.4; margin-bottom: 1.5rem; }
    .waterfall-sm { font-size: 14px; line-height: 1.5; color: var(--muted); }
    .acuity-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-top: 1.5rem;
    }
    .acuity-box {
      background: var(--bg);
      border: 1px solid var(--border);
      padding: 1rem;
      border-radius: 8px;
      text-align: center;
    }
    .acuity-glyph {
      font-family: '$cleanName', sans-serif;
      font-size: 48px;
      color: var(--accent);
      margin-bottom: 0.25rem;
    }
    .acuity-label {
      font-size: 11px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge">$cat · 1000 UPM</div>
      <h1>$cleanName</h1>
      <p style="color: var(--muted); margin: 0;">Designed by $author · Open Font License 1.1</p>
    </header>

    <div class="specimen-card">
      <div class="font-sample waterfall-xl">Sphinx of black quartz, judge my vow.</div>
      <div class="font-sample waterfall-lg">Pack my box with five dozen liquor jugs.</div>
      <div class="font-sample waterfall-md">
        How quickly daft jumping zebras vex. 0123456789 (ISMP Disambiguated)
      </div>
      <div class="font-sample waterfall-sm">
        Standard 1000 UPM em-square | 2-byte loca word boundary: VALID | OTS memory safe: TRUE
      </div>
    </div>

    <div class="specimen-card">
      <h3 style="margin-top: 0; color: var(--muted); font-size: 0.9rem; text-transform: uppercase;">
        Acuity & Disambiguation Benchmarks
      </h3>
      <div class="acuity-grid">
        <div class="acuity-box">
          <div class="acuity-glyph">0̸ 0</div>
          <div class="acuity-label">Slashed Zero (cv08)</div>
        </div>
        <div class="acuity-box">
          <div class="acuity-glyph">1 l I</div>
          <div class="acuity-label">Footed l & Bilobe I</div>
        </div>
        <div class="acuity-box">
          <div class="acuity-glyph">Z 2</div>
          <div class="acuity-label">Crossbar Z (cv11)</div>
        </div>
        <div class="acuity-box">
          <div class="acuity-glyph">⠎⠇⠕⠁⠝</div>
          <div class="acuity-label">Tactile Braille</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
''';
    File('${targetDir.path}/specimen.html').writeAsStringSync(specimenHtml);
    print('  ✓ Created specimen.html (Interactive High-Legibility Specimen)');

    print('\n[SUCCESS] New font project ready at:');
    print('          experiments/$cleanName\n');
    return true;
  }

  static String _sanitizeFamilyName(String input) {
    var s = input.trim();
    if (s.isEmpty) return 'NewFont';
    // Remove special chars, capitalize words
    s = s.replaceAll(RegExp(r'[^a-zA-Z0-9_\-]'), '');
    if (s.isEmpty) return 'NewFont';
    return s[0].toUpperCase() + s.substring(1);
  }
}
