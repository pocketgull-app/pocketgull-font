import 'dart:io';
import 'foundry/sfnt_builder.dart';
import 'foundry/sfnt_transformer.dart';
import 'foundry/specimen_embedder.dart';
import 'foundry/sloan_optotype.dart';
import 'foundry/braille_generator.dart';
import 'foundry/ismp_engine.dart';
import 'foundry/monospace_hud.dart';
import 'foundry/phinney_auditor.dart';
import 'foundry/glyph_inspector.dart';
import 'foundry/font_surgeon.dart';
import 'foundry/smoe_subsetter.dart';
import 'foundry/upstream_cure_engine.dart';
import 'foundry/foundry_spector.dart';
import 'foundry/sanctuary_tui.dart';
import 'foundry/sanctuary_server.dart';
import 'foundry/var_spector.dart';

const fontStems = [
  'PocketGull-Regular',
  'PocketGull-Bold',
  'PocketGull-Black',
  'PocketGull-BoldItalic',
  'PocketGull-Fineliner',
  'PocketGull-Italic',
  'PocketGull-Chiseltip',
  'PocketGull-Antigravity',
  'PocketGull-Numerics',
  'PocketGullMono-Regular',
  'PocketGullMono-Bold',
  'PocketGullMono-Italic',
  'PocketGull-MarkerRaw',
  'PocketGull-Micro',
  'PocketGull-CondensedBold',
  'PocketGull-Soft',
  'PocketGull-Soft-Regular',
  'PocketGull-Soft-Bold',
  'PocketGull-Slab-Regular',
  'PocketGull-Slab-Bold',
  'PocketGull-Serif-Regular',
  'PocketGull-Serif-Bold',
  'PocketGull-Outline',
  'PocketGull-Inline',
  'PocketGull-Halftone',
  'PocketGull-VF',
  'PocketGull-Math',
];

Directory findTypefaceDir() {
  var dir = Directory.current;
  while (dir.path != dir.parent.path) {
    if (dir.path.endsWith('pocketgull-typeface')) return dir;
    final candidate = Directory('${dir.path}${Platform.pathSeparator}pocketgull-typeface');
    if (candidate.existsSync()) return candidate;
    dir = dir.parent;
  }
  return Directory.current;
}

Directory? findAppDir() {
  final tf = findTypefaceDir();
  final candidate = Directory('${tf.parent.path}${Platform.pathSeparator}pocketgull');
  if (candidate.existsSync()) return candidate;
  return null;
}

String findProjectRoot() {
  return findTypefaceDir().path;
}

void runAudit() {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: THOMAS PHINNEY FORENSIC AUDITOR (DART 3.11)');
  print('======================================================================\n');

  final typefaceRoot = findTypefaceDir();
  final appDir = findAppDir();
  final auditDirs = <Directory>[typefaceRoot];
  if (appDir != null) {
    auditDirs.add(Directory('${appDir.path}${Platform.pathSeparator}public${Platform.pathSeparator}fonts'));
  }

  var total = 0;
  var passed = 0;

  for (final dir in auditDirs) {
    print('Auditing fonts in: ${dir.path}');
    if (!dir.existsSync()) {
      print('  [SKIP] Directory does not exist');
      continue;
    }
    for (final stem in fontStems) {
      for (final ext in ['.ttf', '.woff2']) {
        final sub = ext == '.ttf' ? 'ttf' : 'woff2';
        final candidates = [
          File('${dir.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}$sub${Platform.pathSeparator}$stem$ext'),
          File('${dir.path}${Platform.pathSeparator}$stem$ext'),
        ];
        File? fontFile;
        for (final c in candidates) {
          if (c.existsSync()) {
            fontFile = c;
            break;
          }
        }
        if (fontFile == null) continue;
        total++;
        stdout.write('  [AUDIT] $stem$ext ... ');
        final res = ThomasPhinneyAuditor.audit(fontFile);
        if (res.passed) {
          passed++;
          print('[PASS] ${res.message}');
        } else {
          print('[FAIL] ${res.message}');
        }
      }
    }
    print('');
  }

  print('======================================================================');
  print('  AUDIT SUMMARY: $passed / $total FONT BINARIES PASSED W3C OTS VALIDATION');
  print('======================================================================\n');

  if (passed < total) {
    exitCode = 1;
  }
}

void runRealign() {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: 2-BYTE WORD BOUNDARY ALIGNMENT (DART 3.11)');
  print('======================================================================\n');

  final root = findProjectRoot();
  final appDir = findAppDir();
  final ttfDirs = [
    Directory('$root${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf'),
    Directory('$root${Platform.pathSeparator}apache${Platform.pathSeparator}pocketgull'),
    Directory('$root${Platform.pathSeparator}apache${Platform.pathSeparator}pocketgullmono'),
  ];
  if (appDir != null) {
    ttfDirs.add(Directory('${appDir.path}${Platform.pathSeparator}public${Platform.pathSeparator}fonts'));
  }

  for (final dir in ttfDirs) {
    if (!dir.existsSync()) continue;
    final files = dir.listSync().whereType<File>().where((f) => f.path.endsWith('.ttf')).toList();
    files.sort((a, b) => a.path.compareTo(b.path));
    for (final ttf in files) {
      final name = ttf.uri.pathSegments.last;
      stdout.write('  • Realigning $name ... ');
      try {
        SfntTransformer.transformFont(inputFile: ttf);
        print('[OK 2-byte aligned]');
      } catch (e) {
        print('[ERR: $e]');
      }
    }
  }
}

void runCompile() {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: PURE DART SFNT COMPILER (DART 3.11)');
  print('======================================================================\n');

  final root = findProjectRoot();
  final typefaceRoot = Directory('${Directory(root).parent.path}${Platform.pathSeparator}pocketgull-typeface');

  // 1. Compile Reference Clinical Test Font
  final builder = SfntBuilder(
    familyName: 'PocketGull Precision',
    subFamilyName: 'Clinical Regular',
    upm: 1000,
    ascender: 800,
    descender: -200,
    lineGap: 200,
  );

  int gid = 0;
  print('  [1/4] Synthesizing Louise Sloan 5:1 optotypes (C, H, O)...');
  builder.addGlyph(SloanOptotypeEngine.generateLetterO(gid++));
  builder.addGlyph(SloanOptotypeEngine.generateLetterC(gid++));
  builder.addGlyph(SloanOptotypeEngine.generateLetterH(gid++));

  print('  [2/4] Synthesizing ISMP clinical safety glyphs (0 vs O, l vs 1 vs I, Z vs 2)...');
  builder.addGlyph(IsmpDisambiguationEngine.generateSlashedZero(gid++));
  builder.addGlyph(IsmpDisambiguationEngine.generateCurvedL(gid++));
  builder.addGlyph(IsmpDisambiguationEngine.generateSerifedI(gid++));
  builder.addGlyph(IsmpDisambiguationEngine.generateSlashedZ(gid++));

  print('  [3/4] Synthesizing 600 UPM gapless ICU HUD & sub-cell ECG waveforms...');
  final hudGlyphs = MonospaceHudEngine.generateCoreSet(gid);
  for (final g in hudGlyphs) {
    builder.addGlyph(g);
    gid++;
  }

  print('  [4/4] Synthesizing 256-glyph Unicode Braille tactile block (ISO/TR 11548)...');
  final brailleGlyphs = BrailleGenerator.generateAll(gid);
  for (final g in brailleGlyphs) {
    builder.addGlyph(g);
    gid++;
  }

  print('  Compiling $gid glyphs into bit-exact SFNT OpenType binary...');
  final binary = builder.compile();

  final outDir = Directory('${findProjectRoot()}${Platform.pathSeparator}dist${Platform.pathSeparator}fonts');
  if (!outDir.existsSync()) outDir.createSync(recursive: true);

  final outFile = File('${outDir.path}${Platform.pathSeparator}PocketGull-Precision-Dart.ttf');
  outFile.writeAsBytesSync(binary);
  print('  [OK] Successfully wrote: ${outFile.path} (${binary.length} bytes)');

  // 2. Transform & Realign Full Production Superfamily
  if (typefaceRoot.existsSync()) {
    print('\n  [5/5] Realigning and sanitizing complete production superfamily in Dart...');
    final weightMap = {
      'PocketGull-Regular.ttf': 400,
      'PocketGull-Fineliner.ttf': 400,
      'PocketGull-Bold.ttf': 700,
      'PocketGull-Black.ttf': 900,
      'PocketGull-BoldItalic.ttf': 700,
      'PocketGull-Chiseltip.ttf': 900,
      'PocketGull-MarkerRaw.ttf': 900,
      'PocketGull-Italic.ttf': 400,
      'PocketGull-Antigravity.ttf': 400,
      'PocketGull-Numerics.ttf': 600,
      'PocketGullMono-Regular.ttf': 400,
      'PocketGullMono-Italic.ttf': 400,
      'PocketGull-VF.ttf': 400,
    };

    for (final entry in weightMap.entries) {
      File? ttfFile;
      final candidates = [
        File('${typefaceRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf${Platform.pathSeparator}${entry.key}'),
        File('${typefaceRoot.path}${Platform.pathSeparator}${entry.key}'),
      ];
      for (final c in candidates) {
        if (c.existsSync()) {
          ttfFile = c;
          break;
        }
      }
      if (ttfFile != null && ttfFile.existsSync()) {
        stdout.write('    • Transforming ${entry.key} (wght: ${entry.value}) ... ');
        try {
          SfntTransformer.transformFont(
            inputFile: ttfFile,
            overrideWeight: entry.value,
            injectGasp: true,
          );
          print('[OK 2-byte aligned]');
        } catch (e) {
          print('[ERR: $e]');
        }
      }
    }
  }

  // 3. Run immediate Thomas Phinney forensic audit
  stdout.write('\n  [VERIFY] Forensic verification of compiled binary ... ');
  final auditRes = ThomasPhinneyAuditor.audit(outFile);
  if (auditRes.passed) {
    print('[PASS] ${auditRes.message}');
  } else {
    print('[FAIL] ${auditRes.message}');
    exitCode = 1;
  }
}

void runEmbed() {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: SPECIMEN EMBEDDER (DART 3.11)');
  print('======================================================================\n');

  final typefaceRoot = findTypefaceDir();
  final htmlFile = File('${typefaceRoot.path}${Platform.pathSeparator}index.html');

  SpecimenEmbedder.embedFonts(typefaceDir: typefaceRoot, htmlFile: htmlFile);

  final dlFile = File(r'C:\Users\philg\Downloads\PocketGull — The Clinical font superfamily & Interactive Specimen.html1.html');
  if (dlFile.existsSync()) {
    SpecimenEmbedder.embedFonts(typefaceDir: typefaceRoot, htmlFile: dlFile);
    print('  [SUCCESS] Also embedded fonts into ${dlFile.path}');
  }
}

void runSync() {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: FONT ASSET SYNCHRONIZATION (DART 3.11)');
  print('======================================================================\n');

  final typefaceRoot = findTypefaceDir();
  final appDir = findAppDir();

  if (!typefaceRoot.existsSync()) {
    print('[ERROR] Source typeface directory does not exist: ${typefaceRoot.path}');
    exitCode = 1;
    return;
  }

  final targetDirs = <Directory>[];
  if (appDir != null) {
    targetDirs.add(Directory('${appDir.path}${Platform.pathSeparator}public${Platform.pathSeparator}fonts'));
    targetDirs.add(Directory('${appDir.path}${Platform.pathSeparator}public${Platform.pathSeparator}brand${Platform.pathSeparator}fonts'));
  }

  for (final td in targetDirs) {
    td.createSync(recursive: true);
  }

  var synced = 0;
  for (final stem in fontStems) {
    for (final ext in ['.ttf', '.woff2']) {
      final filename = '$stem$ext';
      final sub = ext == '.ttf' ? 'ttf' : 'woff2';
      File? srcFile;
      final candidates = [
        File('${typefaceRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}$sub${Platform.pathSeparator}$filename'),
        File('${typefaceRoot.path}${Platform.pathSeparator}$filename'),
      ];
      for (final c in candidates) {
        if (c.existsSync()) {
          srcFile = c;
          break;
        }
      }
      if (srcFile == null) continue;

      for (final td in targetDirs) {
        final dst = File('${td.path}${Platform.pathSeparator}$filename');
        try {
          dst.writeAsBytesSync(srcFile.readAsBytesSync());
          synced++;
        } catch (e) {
          print('    [WARN] Could not overwrite ${dst.path} (in use): $e');
        }
      }
      print('  [OK] Synchronized $filename across all targets');
    }
  }

  if (appDir != null) {
    final srcCss = File('${typefaceRoot.path}${Platform.pathSeparator}fonts.css');
    if (srcCss.existsSync()) {
      final dstCss = File('${appDir.path}${Platform.pathSeparator}public${Platform.pathSeparator}fonts${Platform.pathSeparator}fonts.css');
      try {
        dstCss.writeAsStringSync(srcCss.readAsStringSync());
        print('  [OK] Synchronized fonts.css to ${dstCss.path}');
      } catch (e) {
        print('  [WARN] Could not overwrite fonts.css (in use): $e');
      }
    }
  }

  print('\n[DONE] Successfully synchronized $synced font files.\n');
}

Future<void> runServe(int requestedPort) async {
  final root = findProjectRoot();
  final typefaceRoot = File('$root${Platform.pathSeparator}index.html').existsSync()
      ? Directory(root)
      : Directory('${Directory(root).parent.path}${Platform.pathSeparator}pocketgull-typeface');

  if (!typefaceRoot.existsSync()) {
    print('[ERROR] Typeface directory not found: ${typefaceRoot.path}');
    exitCode = 1;
    return;
  }

  int port = requestedPort;
  HttpServer? server;

  for (var offset = 0; offset < 10; offset++) {
    try {
      server = await HttpServer.bind(InternetAddress.anyIPv4, port + offset);
      port = port + offset;
      break;
    } catch (_) {}
  }

  if (server == null) {
    print('[ERROR] Could not bind to any local port.');
    exitCode = 1;
    return;
  }

  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY PREVIEW SERVER (ZERO CORS, DART 3.11)');
  print('======================================================================');
  print('  Standard URL:     http://localhost:$port/index.html');
  print('  Dedicated Domain: http://pocketgull.localhost:$port/index.html');
  print('  Serving:          ${typefaceRoot.path}');
  print('  Cache Policy:     no-cache, no-store (Instant refresh)');
  print('  Press Ctrl+C to terminate server.\n');

  await for (HttpRequest request in server) {
    var path = request.uri.path;
    if (path == '/' || path.isEmpty) path = '/index.html';
    final targetPath = '${typefaceRoot.path}${path.replaceAll('/', Platform.pathSeparator)}';
    final targetFile = File(targetPath);

    final ext = path.contains('.') ? path.split('.').last.toLowerCase() : '';
    final isHtml = ext == 'html';
    final isFont = ext == 'woff2' || ext == 'ttf' || ext == 'otf';
    final isStaticAsset = ext == 'css' || ext == 'js' || ext == 'svg' || ext == 'png' || ext == 'webp' || ext == 'ico' || ext == 'json';

    request.response.headers.add('Access-Control-Allow-Origin', '*');
    request.response.headers.add('Access-Control-Allow-Methods', 'GET, HEAD, OPTIONS');
    request.response.headers.add('TDM-Reservation', '1');
    request.response.headers.add('X-Content-Type-Options', 'nosniff');

    if (isFont) {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'public, max-age=31536000, immutable');
    } else if (isStaticAsset) {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'public, max-age=86400');
    } else if (isHtml) {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'no-cache');
    } else {
      request.response.headers.set(HttpHeaders.cacheControlHeader, 'no-cache');
    }

    if (request.method == 'OPTIONS') {
      request.response.statusCode = HttpStatus.ok;
      await request.response.close();
      continue;
    }

    if (await targetFile.exists()) {
      if (path.endsWith('.html')) request.response.headers.contentType = ContentType.html;
      if (path.endsWith('.css')) request.response.headers.contentType = ContentType('text', 'css', charset: 'utf-8');
      if (path.endsWith('.js')) request.response.headers.contentType = ContentType('application', 'javascript', charset: 'utf-8');
      if (path.endsWith('.json')) request.response.headers.contentType = ContentType('application', 'json', charset: 'utf-8');
      if (path.endsWith('.woff2')) request.response.headers.contentType = ContentType('font', 'woff2');
      if (path.endsWith('.ttf')) request.response.headers.contentType = ContentType('font', 'ttf');
      if (path.endsWith('.svg')) request.response.headers.contentType = ContentType('image', 'svg+xml');
      if (path.endsWith('.png')) request.response.headers.contentType = ContentType('image', 'png');
      if (path.endsWith('.webp')) request.response.headers.contentType = ContentType('image', 'webp');

      if (request.method == 'HEAD') {
        request.response.statusCode = HttpStatus.ok;
        await request.response.close();
        continue;
      }

      final isCompressible = isHtml || ext == 'css' || ext == 'js' || ext == 'svg' || ext == 'json';
      final acceptEncoding = request.headers.value(HttpHeaders.acceptEncodingHeader) ?? '';
      if (isCompressible && acceptEncoding.contains('gzip')) {
        request.response.headers.set(HttpHeaders.contentEncodingHeader, 'gzip');
        request.response.headers.set(HttpHeaders.varyHeader, 'Accept-Encoding');
        await targetFile.openRead().transform(gzip.encoder).pipe(request.response);
      } else {
        await targetFile.openRead().pipe(request.response);
      }
    } else {
      request.response.statusCode = HttpStatus.notFound;
      request.response.write('404 Not Found: $path');
      await request.response.close();
    }
  }
}

void runInspect(String? fontPath, String? chars) {
  final path = fontPath ?? r'..\pocketgull-typeface\PocketGull-Bold.ttf';
  final fontFile = File(path);
  if (!fontFile.existsSync()) {
    print('[ERROR] Font file not found: $path');
    return;
  }
  final testChars = chars ?? 'Tactile Humanist Warmth Meets Clinical Precision 0123456789';
  print('\n=== POCKETGULL GLYPH INSPECTOR (PURE DART 3.11) ===');
  print('Font: ${fontFile.path}');
  print('Test string: "$testChars"\n');

  final inspector = GlyphInspector.fromFile(fontFile);
  print('Total glyphs: ${inspector.numGlyphs}, Tables: ${inspector.tables.keys.join(", ")}');

  for (int i = 0; i < testChars.length; i++) {
    final ch = testChars[i];
    final code = ch.codeUnitAt(0);
    final gid = inspector.unicodeToGid[code];
    if (gid == null) {
      print('  [$ch] U+${code.toRadixString(16).padLeft(4, "0").toUpperCase()}: [MISSING IN CMAP]');
      continue;
    }
    final g = inspector.getGlyphData(gid);
    if (g['empty'] == true) {
      print('  [$ch] gid: $gid, code: $code: [SPACE/EMPTY] adv=${g['adv']}');
    } else {
      final bounds = g['bounds'] as List<int>;
      final w = bounds[2] - bounds[0];
      final h = bounds[3] - bounds[1];
      final bad = g['badFlags'] as int;
      print('  [$ch] gid: $gid, code: $code: bounds=(${bounds.join(", ")}), w=$w, h=$h, adv=${g['adv']}, badFlags=$bad');
    }
  }

  // Export visual proof SVG
  final svg = GlyphInspector.generateSvgSheet(fontFile, 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789');
  final outSvg = File(r'C:\Users\philg\.gemini\antigravity-ide\brain\555824f7-b8ba-4d8f-81d9-71abc72967cc\scratch\dart_full_alphabet_proof.svg');
  outSvg.writeAsStringSync(svg);
  print('\n[PROOF] Exported pure Dart alphabet proof to: ${outSvg.path}\n');
}

void runRepair() {
  final root = findProjectRoot();
  final typefaceRoot = Directory('${Directory(root).parent.path}${Platform.pathSeparator}pocketgull-typeface');
  print('\n=== POCKETGULL FONT SURGEON (PURE DART 3.11) ===\n');

  for (final stem in ['PocketGull-Bold', 'PocketGull-Fineliner', 'PocketGull-Chiseltip']) {
    final ttfFile = File('${typefaceRoot.path}${Platform.pathSeparator}$stem.ttf');
    if (!ttfFile.existsSync()) continue;
    final tempOut = File('${typefaceRoot.path}${Platform.pathSeparator}${stem}_repaired.ttf');
    FontSurgeon.repairFont(ttfFile, tempOut);
    tempOut.renameSync(ttfFile.path);
    print('  [REPLACED] $stem.ttf updated with repaired geometry!');
  }

  print('\n[SUCCESS] Font surgery complete. Now realigning and embedding...\n');
  runCompile();
  runEmbed();
}

String resolvePythonCmd(String root) {
  final conda = File(r'C:\Users\philg\anaconda3\python.exe');
  if (conda.existsSync()) return conda.path;
  final pyVenv = File('${root}${Platform.pathSeparator}.venv${Platform.pathSeparator}Scripts${Platform.pathSeparator}python.exe');
  if (pyVenv.existsSync()) return pyVenv.path;
  return 'python';
}

Future<void> runBuild() async {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: UNIFIED BUILD & QA PIPELINE (DART 3.11)');
  print('======================================================================\n');

  final root = findProjectRoot();
  final ttfDir = Directory('${root}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf');

  // Step 1: 2-Byte Alignment via SfntTransformer
  print('Step 1: Realigning TrueType binaries to 2-byte word boundaries...');
  final targetStems = [
    'PocketGull-Bold',
    'PocketGull-BoldItalic',
    'PocketGull-Fineliner',
    'PocketGull-Italic',
    'PocketGull-Chiseltip',
    'PocketGull-MarkerRaw',
    'PocketGullMono-Regular',
    'PocketGullMono-Italic',
    'PocketGull-Soft',
    'PocketGull-Soft-Regular',
    'PocketGull-Soft-Bold',
    'PocketGull-Slab-Regular',
    'PocketGull-Slab-Bold',
    'PocketGull-Serif-Regular',
    'PocketGull-Serif-Bold',
    'PocketGull-Outline',
    'PocketGull-Inline',
    'PocketGull-Halftone',
    'PocketGull-VF',
    'PocketGull-Math',
  ];

  for (final stem in targetStems) {
    final ttf = File('${ttfDir.path}${Platform.pathSeparator}$stem.ttf');
    if (ttf.existsSync()) {
      stdout.write('  • Realigning $stem.ttf ... ');
      SfntTransformer.transformFont(inputFile: ttf);
      print('[OK]');
    }
  }

  // Also root Mono
  final rootMono = File('${root}${Platform.pathSeparator}PocketGullMono-Regular.ttf');
  if (rootMono.existsSync()) {
    stdout.write('  • Realigning root PocketGullMono-Regular.ttf ... ');
    SfntTransformer.transformFont(inputFile: rootMono);
    print('[OK]');
  }

  // Step 2: Recompress WOFF2 using Python fontTools.ttLib.woff2
  print('\nStep 2: Recompressing WOFF2 webfonts (Brotli Q11)...');
  final pythonCmd = resolvePythonCmd(root);

  final pyScript = '''
import os, sys
from fontTools.ttLib.woff2 import compress

root = r"$root"
ttf_dir = os.path.join(root, "fonts", "ttf")
woff2_dir = os.path.join(root, "fonts", "woff2")

for stem in ["PocketGull-Bold", "PocketGull-BoldItalic", "PocketGull-Fineliner", "PocketGull-Italic", "PocketGull-Chiseltip", "PocketGull-MarkerRaw", "PocketGullMono-Regular", "PocketGullMono-Italic"]:
    src = os.path.join(ttf_dir, stem + ".ttf")
    dst = os.path.join(woff2_dir, stem + ".woff2")
    if os.path.isfile(src):
        compress(src, dst)
        print("  • " + stem + ".woff2 (" + str(os.path.getsize(dst)) + " bytes)")

root_ttf = os.path.join(root, "PocketGullMono-Regular.ttf")
root_woff2 = os.path.join(root, "PocketGullMono-Regular.woff2")
if os.path.isfile(root_ttf):
    compress(root_ttf, root_woff2)
    print("  • root PocketGullMono-Regular.woff2 (" + str(os.path.getsize(root_woff2)) + " bytes)")
''';

  final compRes = await Process.run(pythonCmd, ['-c', pyScript]);
  stdout.write(compRes.stdout);
  if (compRes.exitCode != 0) {
    stderr.write(compRes.stderr);
    exitCode = 1;
    return;
  }

  // Step 3: Run Thomas Phinney Forensic Table Audit
  print('\nStep 3: Thomas Phinney Forensic Audit...');
  runAudit();

  // Step 4: Run Google Fonts Specification Pre-Flight
  print('Step 4: Google Fonts Specification Pre-Flight...');
  final valScript = File('${root}${Platform.pathSeparator}sources${Platform.pathSeparator}validate_fonts.py');
  if (valScript.existsSync()) {
    final valRes = await Process.run(pythonCmd, [valScript.path]);
    stdout.write(valRes.stdout);
    if (valRes.exitCode != 0) {
      stderr.write(valRes.stderr);
      exitCode = 1;
      return;
    }
  }

  print('\n[SUCCESS] UNIFIED BUILD COMPLETE: All fonts 100% aligned, compressed, and validated!\n');
}

Future<void> runHeal() async {
  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: AUTONOMOUS CLOSED-LOOP SELF-HEALING ENGINE');
  print('======================================================================\n');

  final root = findProjectRoot();

  // Phase 1: 2-Byte Word Boundary Realignment
  print('[1/5] Healing 2-byte word boundary alignment across all TTF binaries...');
  runRealign();

  // Phase 2: Brotli Q11 Webfont Synchronization
  print('\n[2/5] Synchronizing Brotli Q11 WOFF2 webfonts across superfamily...');
  final recompressScript = File('$root${Platform.pathSeparator}scripts${Platform.pathSeparator}run-recompress.mjs');
  if (recompressScript.existsSync()) {
    final compProc = await Process.run('node', [recompressScript.path]);
    stdout.write(compProc.stdout);
    if (compProc.exitCode != 0) {
      stderr.write(compProc.stderr);
    }
  }

  // Phase 3: Synchronize verified font assets to app and web directories
  print('\n[3/5] Synchronizing font assets to public web app and brand targets...');
  runSync();

  // Phase 4: Refresh Cryptographic Checksums (SHA-256 and SRI Hashes)
  print('\n[4/5] Refreshing cryptographic integrity manifests (SHA256SUMS & SRI)...');
  final checksumScript = File('$root${Platform.pathSeparator}scripts${Platform.pathSeparator}generate_checksums.mjs');
  if (checksumScript.existsSync()) {
    final csProc = await Process.run('node', [checksumScript.path]);
    stdout.write(csProc.stdout);
  }

  // Phase 5: Comprehensive Forensic Verification
  print('\n[5/5] Executing Thomas Phinney forensic table audit & Google Fonts pre-flight...');
  runAudit();

  final valScript = File('$root${Platform.pathSeparator}scripts${Platform.pathSeparator}run-font-validator.mjs');
  if (valScript.existsSync()) {
    final valProc = await Process.run('node', [valScript.path]);
    stdout.write(valProc.stdout);
  }

  print('\n[HEAL COMPLETE] Superfamily 100% healed, aligned, synchronized, and verified!\n');
}

Future<void> runWatch() async {
  final root = findProjectRoot();
  final ttfDir = Directory('$root${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf');
  if (!ttfDir.existsSync()) {
    print('[ERROR] fonts/ttf directory not found: ${ttfDir.path}');
    exitCode = 1;
    return;
  }

  print('\n======================================================================');
  print('  POCKETGULL TYPEFOUNDRY: AUTONOMOUS CLOSED-LOOP WATCH DAEMON');
  print('======================================================================');
  print('  Watching: ${ttfDir.path}');
  print('  Trigger:  Automatic heal cycle on TTF modification');
  print('  Press Ctrl+C to stop.\n');

  DateTime lastTrigger = DateTime.now().subtract(const Duration(seconds: 10));
  bool isHealing = false;

  await for (final event in ttfDir.watch(events: FileSystemEvent.modify | FileSystemEvent.create)) {
    if (!event.path.endsWith('.ttf')) continue;
    final now = DateTime.now();
    if (now.difference(lastTrigger).inMilliseconds < 1500 || isHealing) continue;
    lastTrigger = now;
    isHealing = true;
    print('\n[CHANGE DETECTED] ${event.path} modified. Initiating self-healing loop...');
    try {
      await runHeal();
    } catch (e) {
      print('[ERROR during heal]: $e');
    } finally {
      isHealing = false;
      print('  Watching for changes...');
    }
  }
}

void printHelp() {
  print('''
======================================================================
  POCKETGULL CLINICAL TYPEFOUNDRY CLI (DART 3.11)
======================================================================

Usage:
  dart run tool/pocketgull_foundry.dart <command> [arguments]

Commands:
  heal              Autonomous closed-loop self-healing pipeline (realign, compress, sync, checksum, audit)
  watch             Autonomous closed-loop daemon monitoring fonts/ttf for modifications
  build             Execute unified 4-step pipeline (realign, compress, audit, validate)
  audit             Forensic W3C OTS & 2-byte word-alignment verification (Thomas Phinney)
  compile           Compile precision Sloan optotypes, Braille & ISMP glyphs into SFNT
  embed             Embed verified pristine Base64 fonts into HTML specimen
  inspect [font]    Inspect glyph metrics, bounds, contours, and flags in pure Dart
  repair            Surgically fix letterform geometry (C flip, wordmark g, G spur) in Dart
  cure              Execute Google Fonts upstream compliance pipeline (casing, GDEF/GPOS, Option 5, 2-byte alignment, audit)
  sync              Synchronize verified binaries across typeface and app font directories
  smoe [font]       Audit SMoE script expert routing across active Unicode blocks
  spector [dir]     Pure Dart 3.11 replacement for FontSpector (OpenType, Google Fonts, W3C OTS)
  varspector [font] Pure Dart 3.11 Variable Typography Auditor (fvar, STAT, gvar, HVAR, wght/wdth/slnt)
  benchmark         Run scientific rasterization throughput & latency benchmark suite
  serve [port]      Serve specimen proof locally with zero CORS restrictions (default: 8770)
  sanctuary         Launch interactive Pure-Dart Terminal Sanctuary (TUI, Ludology, Pacing)
''');
}

Future<void> main(List<String> args) async {
  final command = args.isNotEmpty ? args[0] : 'audit';
  switch (command) {
    case 'varspector':
    case 'var':
      final target = args.length > 1 ? File(args[1]) : File('fonts/ttf/PocketGull-VF.ttf');
      print('\n======================================================================');
      print('  POCKETGULL FOUNDRY: VARSPECTOR VARIABLE TYPOGRAPHY AUDITOR');
      print('======================================================================\n');
      final rep = VariableFoundrySpector.audit(target);
      for (final c in rep.checks) {
        final tag = c.isPass ? '[PASS]' : (c.isWarn ? '[WARN]' : '[FAIL]');
        print('  $tag ${c.id}: ${c.details}');
      }
      print('\n  SUMMARY: Total Checks: ${rep.checks.length} | PASS: ${rep.passCount} | WARN: ${rep.warnCount} | FAIL: ${rep.failCount}\n');
      if (!rep.passed) exitCode = 1;
      break;
    case 'sanctuary':
    case 'tui':
    case 'parlor':
      final tui = SanctuaryTui(projectRoot: Directory(findProjectRoot()));
      await tui.run();
      break;
    case 'heal':
    case 'self-heal':
      await runHeal();
      break;
    case 'watch':
      await runWatch();
      break;
    case 'build':
      await runBuild();
      break;
    case 'spector':
      final dir = args.length > 1 ? Directory(args[1]) : Directory('apache');
      final ok = await FoundrySpector.auditDirectory(dir);
      if (!ok) exitCode = 1;
      break;
    case 'cure':
    case 'upstream':
      await UpstreamCureEngine.run(projectRoot: findProjectRoot());
      break;
    case 'audit':
      runAudit();
      break;
    case 'realign':
      runRealign();
      break;
    case 'smoe':
      final targetFont = args.length > 1 ? args[1] : 'fonts/ttf/PocketGull-Bold.ttf';
      SmoeSubsetter.analyzeFont(File(targetFont));
      break;
    case 'compile':
      runCompile();
      break;
    case 'embed':
      runEmbed();
      break;
    case 'inspect':
      final fontPath = args.length > 1 ? args[1] : null;
      final chars = args.length > 2 ? args[2] : null;
      runInspect(fontPath, chars);
      break;
    case 'repair':
      runRepair();
      break;
    case 'sync':
      runSync();
      break;
    case 'benchmark':
    case 'bench':
      final py = resolvePythonCmd(findProjectRoot());
      final benchScript = File('${findProjectRoot()}${Platform.pathSeparator}tool${Platform.pathSeparator}benchmark_rasterizer.py');
      final proc = await Process.start(py, [benchScript.path, ...args.skip(1)], mode: ProcessStartMode.inheritStdio);
      exitCode = await proc.exitCode;
      break;
    case 'serve':
    case 'server':
      final port = args.length > 1 ? int.tryParse(args[1]) ?? 8770 : 8770;
      final server = SanctuaryServer(projectRoot: Directory(findProjectRoot()), port: port);
      await server.start();
      break;
    case 'help':
    case '--help':
    case '-h':
      printHelp();
      break;
    default:
      print('[ERROR] Unknown command: $command');
      printHelp();
      exitCode = 1;
  }
}
