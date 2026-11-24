import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

/// Pure Dart 3.11 Compiler-Emitted OpenType Capability Manifest Generator.
/// Reads compiled SFNT binaries directly (`head`, `maxp`, `loca`, `cmap`, `name`,
/// `fvar`, `STAT`, `gvar`, `HVAR`, `GSUB`, `GPOS`) and emits a deterministic
/// Single-Source-of-Truth JSON manifest (`fonts/opentype-manifest.json`).
class OpenTypeManifestEmitter {
  static Future<File> emit({required Directory projectRoot}) async {
    final pkgFile = File('${projectRoot.path}${Platform.pathSeparator}package.json');
    var semver = '4.0.0';
    if (pkgFile.existsSync()) {
      final pkg = jsonDecode(pkgFile.readAsStringSync()) as Map<String, dynamic>;
      semver = (pkg['version'] as String?) ?? semver;
    }

    final vfFile = File(
      '${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf${Platform.pathSeparator}PocketGull-VF.ttf',
    );
    if (!vfFile.existsSync()) {
      throw StateError('Missing primary variable font binary: ${vfFile.path}');
    }

    final vfManifest = inspectFontBinary(vfFile);

    // Inspect representative static & specialty cuts for superfamily feature parity
    const superfamilyTargets = [
      'PocketGull-Regular.ttf',
      'PocketGull-Bold.ttf',
      'PocketGull-Fineliner.ttf',
      'PocketGull-Chiseltip.ttf',
      'PocketGullMono-Regular.ttf',
      'PocketGull-Slab-Bold.ttf',
      'PocketGull-Math.ttf',
      'PocketGull-ASL.ttf',
    ];

    final familyMembers = <Map<String, dynamic>>[];
    for (final fileName in superfamilyTargets) {
      final f = File(
        '${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}ttf${Platform.pathSeparator}$fileName',
      );
      if (f.existsSync()) {
        final info = inspectFontBinary(f, includeDetailedInstances: false);
        familyMembers.add({
          'file': 'fonts/ttf/$fileName',
          'woff2': 'fonts/woff2/${fileName.replaceAll('.ttf', '.woff2')}',
          'familyName': info['familyName'],
          'subfamilyName': info['subfamilyName'],
          'versionString': info['versionString'],
          'unitsPerEm': info['unitsPerEm'],
          'numGlyphs': info['numGlyphs'],
          'mappedCodepoints': info['mappedCodepoints'],
          'wordAligned2Byte': info['wordAligned2Byte'],
          'gsubFeatures': info['gsubFeatures'],
          'gposFeatures': info['gposFeatures'],
        });
      }
    }

    final manifest = <String, dynamic>{
      'schemaVersion': '1.0.0',
      'semver': semver,
      'foundry': 'PocketGull Typefoundry',
      'license': {
        'fonts': 'OFL-1.1',
        'toolingAndCss': 'Apache-2.0',
      },
      'primaryVariableFont': {
        'file': 'fonts/ttf/PocketGull-VF.ttf',
        'woff2': 'fonts/woff2/PocketGull-VF.woff2',
        ...vfManifest,
      },
      'cssPolarityCompensation': {
        'description':
            'Zero-reflow dark/ICU and 670nm scotopic halation compensation mapped to HVAR-invariant contour inset axes.',
        'customProperties': {
          '--pg-grad': {
            'syntax': '<number>',
            'lightDefault': 0,
            'darkIcuDefault': -25,
            'scotopicPbmDefault': -45,
          },
          '--pg-thrm': {
            'syntax': '<number>',
            'axisTag': 'THRM',
            'lightDefault': 0.0,
            'darkIcuDefault': 0.35,
            'scotopicPbmDefault': 0.60,
            'zeroHorizontalReflow': true,
          },
        },
      },
      'superfamilyCutSummary': familyMembers,
    };

    final outFile = File(
      '${projectRoot.path}${Platform.pathSeparator}fonts${Platform.pathSeparator}opentype-manifest.json',
    );
    const encoder = JsonEncoder.withIndent('  ');
    outFile.writeAsStringSync('${encoder.convert(manifest)}\n');
    return outFile;
  }

  static Map<String, dynamic> inspectFontBinary(
    File file, {
    bool includeDetailedInstances = true,
  }) {
    final bytes = file.readAsBytesSync();
    final data = ByteData.sublistView(bytes);
    final numTables = data.getUint16(4);
    final tables = <String, (int offset, int length)>{};

    for (var i = 0; i < numTables; i++) {
      final rec = 12 + i * 16;
      if (rec + 16 > bytes.length) break;
      final tag = String.fromCharCodes(bytes.sublist(rec, rec + 4));
      tables[tag] = (data.getUint32(rec + 8), data.getUint32(rec + 12));
    }

    final sortedTags = tables.keys.toList()..sort();
    final names = _parseNameTable(bytes, data, tables['name']);

    // head & maxp
    var unitsPerEm = 1000;
    var fontRevision = 0.0;
    var isLongLoca = false;
    if (tables.containsKey('head')) {
      final hOff = tables['head']!.$1;
      fontRevision =
          double.parse((data.getInt32(hOff + 4) / 65536.0).toStringAsFixed(3));
      unitsPerEm = data.getUint16(hOff + 18);
      isLongLoca = data.getInt16(hOff + 50) == 1;
    }

    final numGlyphs =
        tables.containsKey('maxp') ? data.getUint16(tables['maxp']!.$1 + 4) : 0;

    // 2-byte word alignment check on loca
    var oddLocaOffsets = 0;
    if (tables.containsKey('loca')) {
      final (lOff, lLen) = tables['loca']!;
      if (isLongLoca) {
        final count = lLen ~/ 4;
        for (var i = 0; i < count; i++) {
          if (data.getUint32(lOff + i * 4).isOdd) oddLocaOffsets++;
        }
      } else {
        final count = lLen ~/ 2;
        for (var i = 0; i < count; i++) {
          if ((data.getUint16(lOff + i * 2) * 2).isOdd) oddLocaOffsets++;
        }
      }
    }

    final mappedCodepoints = _countCmapCodepoints(bytes, data, tables['cmap']);
    final gsubTags = _extractLayoutFeatures(bytes, data, tables['GSUB']);
    final gposTags = _extractLayoutFeatures(bytes, data, tables['GPOS']);

    final hvarActiveAxes = _extractHvarActiveAxisIndices(data, tables['HVAR']);

    final axes = <Map<String, dynamic>>[];
    final instances = <Map<String, dynamic>>[];
    if (tables.containsKey('fvar')) {
      final fvOff = tables['fvar']!.$1;
      final axesArrayOff = fvOff + data.getUint16(fvOff + 4);
      final axisCount = data.getUint16(fvOff + 8);
      final axisSize = data.getUint16(fvOff + 10);
      final instanceCount = data.getUint16(fvOff + 12);
      final instanceSize = data.getUint16(fvOff + 14);

      for (var a = 0; a < axisCount; a++) {
        final p = axesArrayOff + a * axisSize;
        final tag = String.fromCharCodes(bytes.sublist(p, p + 4));
        final minVal = _fixedToDouble(data.getInt32(p + 4));
        final defVal = _fixedToDouble(data.getInt32(p + 8));
        final maxVal = _fixedToDouble(data.getInt32(p + 12));
        final flags = data.getUint16(p + 16);
        final nameId = data.getUint16(p + 18);
        final propSuffix = tag.toLowerCase();
        final affectsHvar = hvarActiveAxes.contains(a);

        axes.add({
          'index': a,
          'tag': tag,
          'nameId': nameId,
          'name': names[nameId] ?? tag,
          'min': minVal,
          'default': defVal,
          'max': maxVal,
          'hidden': (flags & 0x0001) != 0,
          'hvarAffectsAdvanceWidth': affectsHvar,
          'zeroReflowContourOnly': !affectsHvar,
          'cssCustomProperty': '--pg-$propSuffix',
          'cssSnippet': "'$tag' var(--pg-$propSuffix, $defVal)",
        });
      }

      if (includeDetailedInstances) {
        final instStart = axesArrayOff + axisCount * axisSize;
        final hasPsName = instanceSize >= (4 + axisCount * 4 + 2);
        for (var i = 0; i < instanceCount; i++) {
          final ip = instStart + i * instanceSize;
          if (ip + 4 + axisCount * 4 > bytes.length) break;
          final subNameId = data.getUint16(ip);
          final coords = <String, double>{};
          for (var a = 0; a < axisCount; a++) {
            final tag = axes[a]['tag'] as String;
            coords[tag] = _fixedToDouble(data.getInt32(ip + 4 + a * 4));
          }
          int? psNameId;
          if (hasPsName) {
            psNameId = data.getUint16(ip + 4 + axisCount * 4);
          }
          instances.add({
            'subfamilyNameId': subNameId,
            'name': names[subNameId] ?? 'Instance $i',
            if (psNameId != null && psNameId != 0xFFFF && names.containsKey(psNameId))
              'postScriptName': names[psNameId],
            'coordinates': coords,
          });
        }
      }
    }

    final statInfo = _parseStatTable(bytes, data, tables['STAT'], names);

    Map<String, dynamic>? gvarSummary;
    if (tables.containsKey('gvar')) {
      final gvOff = tables['gvar']!.$1;
      gvarSummary = {
        'majorVersion': data.getUint16(gvOff),
        'minorVersion': data.getUint16(gvOff + 2),
        'axisCount': data.getUint16(gvOff + 4),
        'sharedTupleCount': data.getUint16(gvOff + 6),
        'glyphCount': data.getUint16(gvOff + 12),
        'offsetSizeBytes': (data.getUint16(gvOff + 14) & 1) != 0 ? 4 : 2,
      };
    }

    return {
      'familyName': names[16] ?? names[1] ?? file.uri.pathSegments.last,
      'subfamilyName': names[17] ?? names[2] ?? 'Regular',
      'versionString': names[5] ?? '',
      'fontRevision': fontRevision,
      'unitsPerEm': unitsPerEm,
      'numGlyphs': numGlyphs,
      'mappedCodepoints': mappedCodepoints,
      'sfntTables': sortedTags,
      'wordAligned2Byte': oddLocaOffsets == 0 && bytes.length.isEven,
      'oddLocaOffsets': oddLocaOffsets,
      if (axes.isNotEmpty) 'axes': axes,
      if (instances.isNotEmpty) 'namedInstances': instances,
      if (statInfo != null) 'stat': statInfo,
      if (gvarSummary != null) 'gvar': gvarSummary,
      'gsubFeatures': gsubTags
          .map((t) => {
                'tag': t,
                'description': _featureDescription(t),
                'cssSnippet': 'font-feature-settings: "$t" 1;',
              })
          .toList(),
      'gposFeatures': gposTags
          .map((t) => {
                'tag': t,
                'description': _featureDescription(t),
                'cssSnippet': 'font-feature-settings: "$t" 1;',
              })
          .toList(),
    };
  }

  static Map<int, String> _parseNameTable(
    Uint8List bytes,
    ByteData data,
    (int, int)? nameEntry,
  ) {
    final result = <int, String>{};
    if (nameEntry == null) return result;
    final nOff = nameEntry.$1;
    final count = data.getUint16(nOff + 2);
    final storageOff = nOff + data.getUint16(nOff + 4);

    for (var i = 0; i < count; i++) {
      final rec = nOff + 6 + i * 12;
      if (rec + 12 > bytes.length) break;
      final platformId = data.getUint16(rec);
      final langId = data.getUint16(rec + 4);
      final nameId = data.getUint16(rec + 6);
      final length = data.getUint16(rec + 8);
      final strOff = storageOff + data.getUint16(rec + 10);
      if (strOff + length > bytes.length) continue;

      if (platformId == 3 && (langId == 0x0409 || !result.containsKey(nameId))) {
        final codeUnits = <int>[];
        for (var k = 0; k + 1 < length; k += 2) {
          codeUnits.add(data.getUint16(strOff + k));
        }
        result[nameId] = String.fromCharCodes(codeUnits);
      } else if (platformId == 1 && !result.containsKey(nameId)) {
        result[nameId] = latin1.decode(bytes.sublist(strOff, strOff + length));
      }
    }
    return result;
  }

  static int _countCmapCodepoints(
    Uint8List bytes,
    ByteData data,
    (int, int)? cmapEntry,
  ) {
    if (cmapEntry == null) return 0;
    final cOff = cmapEntry.$1;
    final numSub = data.getUint16(cOff + 2);
    final codepoints = <int>{};

    for (var i = 0; i < numSub; i++) {
      final subOff = cOff + data.getUint32(cOff + 8 + i * 8);
      if (subOff + 4 > bytes.length) continue;
      final format = data.getUint16(subOff);
      if (format == 12) {
        final numGroups = data.getUint32(subOff + 12);
        for (var g = 0; g < numGroups; g++) {
          final gp = subOff + 16 + g * 12;
          if (gp + 12 > bytes.length) break;
          final start = data.getUint32(gp);
          final end = data.getUint32(gp + 4);
          final startGid = data.getUint32(gp + 8);
          for (var cp = start; cp <= end; cp++) {
            if (startGid + (cp - start) != 0) codepoints.add(cp);
          }
        }
      } else if (format == 4 && codepoints.isEmpty) {
        final segCountX2 = data.getUint16(subOff + 6);
        final segCount = segCountX2 ~/ 2;
        final endOff = subOff + 14;
        final startOff = endOff + segCountX2 + 2;
        final deltaOff = startOff + segCountX2;
        final rangeOff = deltaOff + segCountX2;
        for (var s = 0; s < segCount; s++) {
          final end = data.getUint16(endOff + s * 2);
          final start = data.getUint16(startOff + s * 2);
          if (start == 0xFFFF) break;
          final delta = data.getInt16(deltaOff + s * 2);
          final ro = data.getUint16(rangeOff + s * 2);
          for (var cp = start; cp <= end; cp++) {
            var gid = 0;
            if (ro == 0) {
              gid = (cp + delta) & 0xFFFF;
            } else {
              final gAddr = rangeOff + s * 2 + ro + (cp - start) * 2;
              if (gAddr + 2 <= bytes.length) {
                final raw = data.getUint16(gAddr);
                if (raw != 0) gid = (raw + delta) & 0xFFFF;
              }
            }
            if (gid != 0) codepoints.add(cp);
          }
        }
      }
    }
    return codepoints.length;
  }

  static List<String> _extractLayoutFeatures(
    Uint8List bytes,
    ByteData data,
    (int, int)? entry,
  ) {
    if (entry == null) return const [];
    final off = entry.$1;
    if (off + 10 > bytes.length) return const [];
    final featListOff = off + data.getUint16(off + 6);
    if (featListOff + 2 > bytes.length) return const [];
    final featCount = data.getUint16(featListOff);
    final tags = <String>{};
    for (var i = 0; i < featCount; i++) {
      final p = featListOff + 2 + i * 6;
      if (p + 6 > bytes.length) break;
      tags.add(String.fromCharCodes(bytes.sublist(p, p + 4)));
    }
    final list = tags.toList()..sort();
    return list;
  }

  static Set<int> _extractHvarActiveAxisIndices(
    ByteData data,
    (int, int)? hvarEntry,
  ) {
    final active = <int>{};
    if (hvarEntry == null) return active;
    final hvOff = hvarEntry.$1;
    final ivsOff = hvOff + data.getUint32(hvOff + 4);
    final regListOff = ivsOff + data.getUint32(ivsOff + 2);
    final axisCount = data.getUint16(regListOff);
    final regionCount = data.getUint16(regListOff + 2);
    for (var r = 0; r < regionCount; r++) {
      for (var a = 0; a < axisCount; a++) {
        final p = regListOff + 4 + (r * axisCount + a) * 6;
        final peak = data.getInt16(p + 2);
        if (peak != 0) active.add(a);
      }
    }
    return active;
  }

  static Map<String, dynamic>? _parseStatTable(
    Uint8List bytes,
    ByteData data,
    (int, int)? statEntry,
    Map<int, String> names,
  ) {
    if (statEntry == null) return null;
    final sOff = statEntry.$1;
    final major = data.getUint16(sOff);
    final minor = data.getUint16(sOff + 2);
    final designAxisSize = data.getUint16(sOff + 4);
    final designAxisCount = data.getUint16(sOff + 6);
    final designAxesOff = sOff + data.getUint32(sOff + 8);
    final axisValueCount = data.getUint16(sOff + 12);
    final axisValueOffsetsBase = sOff + data.getUint32(sOff + 14);

    final designAxes = <Map<String, dynamic>>[];
    for (var i = 0; i < designAxisCount; i++) {
      final p = designAxesOff + i * designAxisSize;
      if (p + 8 > bytes.length) break;
      final tag = String.fromCharCodes(bytes.sublist(p, p + 4));
      final nameId = data.getUint16(p + 4);
      final ordering = data.getUint16(p + 6);
      designAxes.add({
        'tag': tag,
        'nameId': nameId,
        'name': names[nameId] ?? tag,
        'ordering': ordering,
      });
    }

    final axisValues = <Map<String, dynamic>>[];
    for (var i = 0; i < axisValueCount; i++) {
      final relOff = data.getUint16(axisValueOffsetsBase + i * 2);
      final vp = axisValueOffsetsBase + relOff;
      if (vp + 6 > bytes.length) break;
      final format = data.getUint16(vp);
      if (format == 1 || format == 2 || format == 3) {
        final axisIndex = data.getUint16(vp + 2);
        final flags = data.getUint16(vp + 4);
        final valNameId = data.getUint16(vp + 6);
        final value = _fixedToDouble(data.getInt32(vp + 8));
        final axisTag =
            axisIndex < designAxes.length ? designAxes[axisIndex]['tag'] : '$axisIndex';
        axisValues.add({
          'format': format,
          'axisTag': axisTag,
          'name': names[valNameId] ?? 'Value $i',
          'value': value,
          'elidable': (flags & 0x0002) != 0,
        });
      }
    }

    return {
      'version': '$major.$minor',
      'designAxes': designAxes,
      'axisValues': axisValues,
    };
  }

  static double _fixedToDouble(int fixed) {
    return double.parse((fixed / 65536.0).toStringAsFixed(4));
  }

  static String _featureDescription(String tag) {
    return switch (tag) {
      'zero' => 'ISMP Slashed Zero for dosage safety (500 mg)',
      'tnum' => 'Tabular Fixed-Pitch Numerals (0px telemetry jitter)',
      'liga' => 'Standard Humanist Ligature Composition',
      'kern' => 'Optical Pairwise Kerning',
      'mark' => 'Pan-Tribal & Salishan Combining Mark-to-Base Positioning',
      'mkmk' => 'Stacked Diacritic Mark-to-Mark Elevation (>= 110 UPM)',
      'ss02' => 'ISMP Bilobe Serifed Capital I (IL-6, IgA disambiguation)',
      'ss07' => 'Philocardia Cardiac Heart Tittle Set (i, j, !, ?)',
      'ss08' => 'Philocardia Blossom Tittle Set',
      'ss09' => 'Philocardia Calligraphic Nuqta Tittle Set',
      'ss10' => 'Philocardia Radiant Star Tittle Set',
      'ss11' => 'Philocardia Hydration Droplet Tittle Set',
      'cv05' => 'ISMP Curved Terminal Foot Lowercase l',
      'cv08' => 'ISMP Anti-Clotting Slashed Zero Character Variant',
      'cv09' => 'Philocardia Lowercase i Heart Tittle Alternate',
      'cv10' => 'Philocardia Lowercase j Heart Tittle Alternate',
      'cv11' => 'ISMP Crossbar Capital Z (2/Z disambiguation)',
      'cv12' => 'Open-Counter Clinical Numeral Four',
      'cv19' => 'High-Acuity Clinical Punctuation Variant',
      _ => 'OpenType Typographic Feature ($tag)',
    };
  }
}
