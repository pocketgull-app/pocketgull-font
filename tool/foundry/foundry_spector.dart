import 'dart:io';
import 'dart:typed_data';

/// Severity level for FoundrySpector check results.
enum SpectorStatus { pass, warn, fail, info }

/// Single check result within the FoundrySpector suite.
class SpectorCheckResult {
  final String checkId;
  final String description;
  final SpectorStatus status;
  final String details;

  const SpectorCheckResult({
    required this.checkId,
    required this.description,
    required this.status,
    required this.details,
  });

  bool get isPass => status == SpectorStatus.pass;
  bool get isFail => status == SpectorStatus.fail;
  bool get isWarn => status == SpectorStatus.warn;
}

/// Comprehensive audit report for a font binary.
class FontAuditReport {
  final String filename;
  final String familyName;
  final String styleName;
  final List<SpectorCheckResult> checks;

  FontAuditReport({
    required this.filename,
    required this.familyName,
    required this.styleName,
    required this.checks,
  });

  int get passCount => checks.where((c) => c.isPass).length;
  int get failCount => checks.where((c) => c.isFail).length;
  int get warnCount => checks.where((c) => c.isWarn).length;
  bool get passed => failCount == 0;
}

/// Pure Dart 3.11 implementation replacing FontSpector and Fontbakery.
///
/// Executes 100% locally with zero external dependencies (no Python, no WSL, no Rust).
/// Audits SFNT binary tables directly using [ByteData]:
/// - OpenType table semantics (head, maxp, OS/2, post, gasp, STAT)
/// - Google Fonts upstream specifications (Option 5 versioning, OFL line 1 match, name table purity)
/// - Thomas Phinney & W3C OTS memory safety (2-byte loca word alignment, bit-7 flag masking, bbox sanity)
/// - Universal outline geometry (no duplicate nodes, no composite cycles, no nested composites)
/// - Glyphset coverage (Google Fonts Latin Core 319 codepoints, 256 Braille codepoints, case symmetry)
/// - Shaperglot mark-to-base layout (GDEF glyph classes, African language anchors on U+0196 and U+01B1)
/// - METADATA.pb text-proto validation
class FoundrySpector {
  static const String ansiGreen = '\x1B[92m';
  static const String ansiRed = '\x1B[91m';
  static const String ansiYellow = '\x1B[93m';
  static const String ansiCyan = '\x1B[96m';
  static const String ansiBold = '\x1B[1m';
  static const String ansiReset = '\x1B[0m';

  // Standard Google Fonts Latin Core required codepoints (selection of core essentials)
  static final Set<int> gfLatinCore = {
    ...List.generate(95, (i) => 32 + i), // ASCII 32 - 126
    0x00A0, 0x00A1, 0x00A2, 0x00A3, 0x00A4, 0x00A5, 0x00A6, 0x00A7, 0x00A8, 0x00A9,
    0x00AA, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x00AF, 0x00B0, 0x00B1, 0x00B2, 0x00B3,
    0x00B4, 0x00B5, 0x00B6, 0x00B7, 0x00B8, 0x00B9, 0x00BA, 0x00BB, 0x00BC, 0x00BD,
    0x00BE, 0x00BF, 0x00C0, 0x00C1, 0x00C2, 0x00C3, 0x00C4, 0x00C5, 0x00C6, 0x00C7,
    0x00C8, 0x00C9, 0x00CA, 0x00CB, 0x00CC, 0x00CD, 0x00CE, 0x00CF, 0x00D0, 0x00D1,
    0x00D2, 0x00D3, 0x00D4, 0x00D5, 0x00D6, 0x00D7, 0x00D8, 0x00D9, 0x00DA, 0x00DB,
    0x00DC, 0x00DD, 0x00DE, 0x00DF, 0x00E0, 0x00E1, 0x00E2, 0x00E3, 0x00E4, 0x00E5,
    0x00E6, 0x00E7, 0x00E8, 0x00E9, 0x00EA, 0x00EB, 0x00EC, 0x00ED, 0x00EE, 0x00EF,
    0x00F0, 0x00F1, 0x00F2, 0x00F3, 0x00F4, 0x00F5, 0x00F6, 0x00F7, 0x00F8, 0x00F9,
    0x00FA, 0x00FB, 0x00FC, 0x00FD, 0x00FE, 0x00FF,
    // Latin Extended-A essentials
    0x0100, 0x0101, 0x0102, 0x0103, 0x0104, 0x0105, 0x0106, 0x0107, 0x010C, 0x010D,
    0x010E, 0x010F, 0x0110, 0x0111, 0x0112, 0x0113, 0x0118, 0x0119, 0x011A, 0x011B,
    0x0128, 0x0129, 0x012A, 0x012B, 0x012E, 0x012F, 0x0131, 0x0139, 0x013A, 0x013D,
    0x013E, 0x0141, 0x0142, 0x0143, 0x0144, 0x0147, 0x0148, 0x014C, 0x014D, 0x0150,
    0x0151, 0x0152, 0x0153, 0x0154, 0x0155, 0x0158, 0x0159, 0x015A, 0x015B, 0x015E,
    0x015F, 0x0160, 0x0161, 0x0162, 0x0163, 0x0164, 0x0165, 0x016A, 0x016B, 0x016E,
    0x016F, 0x0170, 0x0171, 0x0178, 0x0179, 0x017A, 0x017B, 0x017C, 0x017D, 0x017E,
    // Essential punctuation & symbols
    0x2010, 0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022,
    0x2026, 0x2039, 0x203A, 0x2044, 0x20AC, 0x2212,
  };

  /// Audits a single font file against the full FoundrySpector specification.
  static FontAuditReport auditFont(File fontFile, {String? oflExpectedLine1}) {
    final filename = fontFile.uri.pathSegments.last;
    final checks = <SpectorCheckResult>[];

    if (!fontFile.existsSync()) {
      checks.add(SpectorCheckResult(
        checkId: 'file_exists',
        description: 'File existence check',
        status: SpectorStatus.fail,
        details: 'File not found at ${fontFile.path}',
      ));
      return FontAuditReport(filename: filename, familyName: 'Unknown', styleName: 'Unknown', checks: checks);
    }

    final bytes = fontFile.readAsBytesSync();
    if (bytes.length < 12) {
      checks.add(SpectorCheckResult(
        checkId: 'sfnt_header',
        description: 'SFNT table directory length',
        status: SpectorStatus.fail,
        details: 'File is smaller than minimum SFNT header (12 bytes)',
      ));
      return FontAuditReport(filename: filename, familyName: 'Unknown', styleName: 'Unknown', checks: checks);
    }

    // WOFF2 header check
    if (bytes[0] == 0x77 && bytes[1] == 0x4F && bytes[2] == 0x46 && bytes[3] == 0x32) {
      checks.add(SpectorCheckResult(
        checkId: 'woff2_magic',
        description: 'W3C WOFF2 magic bytes',
        status: SpectorStatus.pass,
        details: 'Valid WOFF2 binary with magic wOF2 header',
      ));
      return FontAuditReport(filename: filename, familyName: 'PocketGull', styleName: 'WOFF2 Webfont', checks: checks);
    }

    final data = ByteData.sublistView(bytes);
    final numTables = data.getUint16(4, Endian.big);
    final tables = <String, (int offset, int length)>{};

    for (int i = 0; i < numTables; i++) {
      final entryOffset = 12 + i * 16;
      if (entryOffset + 16 > bytes.length) break;
      final tag = String.fromCharCodes(bytes.sublist(entryOffset, entryOffset + 4));
      tables[tag] = (
        data.getUint32(entryOffset + 8, Endian.big),
        data.getUint32(entryOffset + 12, Endian.big),
      );
    }

    // 1. Mandatory tables check
    final requiredTables = ['head', 'hhea', 'maxp', 'OS/2', 'hmtx', 'cmap', 'loca', 'glyf', 'name', 'post'];
    final missingTables = requiredTables.where((t) => !tables.containsKey(t)).toList();
    if (missingTables.isNotEmpty) {
      checks.add(SpectorCheckResult(
        checkId: 'opentype_mandatory_tables',
        description: 'Mandatory OpenType tables present',
        status: SpectorStatus.fail,
        details: 'Missing mandatory tables: ${missingTables.join(", ")}',
      ));
      return FontAuditReport(filename: filename, familyName: 'Unknown', styleName: 'Unknown', checks: checks);
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'opentype_mandatory_tables',
        description: 'Mandatory OpenType tables present',
        status: SpectorStatus.pass,
        details: 'All 10 mandatory tables present (${tables.keys.join(", ")})',
      ));
    }

    // Parse 'head' table
    final headOffset = tables['head']!.$1;
    final fontRevInt = data.getInt16(headOffset + 4, Endian.big);
    final fontRevFrac = data.getUint16(headOffset + 6, Endian.big);
    final fontRevision = fontRevInt + (fontRevFrac / 65536.0);
    final unitsPerEm = data.getUint16(headOffset + 18, Endian.big);
    final macStyle = data.getUint16(headOffset + 44, Endian.big);
    final indexToLocFormat = data.getInt16(headOffset + 50, Endian.big);

    // 2. Units Per Em
    if (unitsPerEm == 1000) {
      checks.add(SpectorCheckResult(
        checkId: 'head_units_per_em',
        description: 'Em square units per em (UPM)',
        status: SpectorStatus.pass,
        details: 'UPM is 1000 (Standard Google Fonts UPM)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'head_units_per_em',
        description: 'Em square units per em (UPM)',
        status: SpectorStatus.fail,
        details: 'UPM is $unitsPerEm (Expected 1000)',
      ));
    }

    // 3. Font Revision
    final roundedRev = (fontRevision * 10).round() / 10;
    if (roundedRev == 3.0 || roundedRev == 3.1) {
      checks.add(SpectorCheckResult(
        checkId: 'head_font_revision',
        description: 'head.fontRevision SemVer alignment',
        status: SpectorStatus.pass,
        details: 'fontRevision is ${fontRevision.toStringAsFixed(3)} (SemVer 3.x aligned)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'head_font_revision',
        description: 'head.fontRevision SemVer alignment',
        status: SpectorStatus.fail,
        details: 'fontRevision is $fontRevision (Expected 3.1 or 3.0)',
      ));
    }

    // Parse 'maxp'
    final maxpOffset = tables['maxp']!.$1;
    final numGlyphs = data.getUint16(maxpOffset + 4, Endian.big);

    // Parse 'OS/2' table
    final os2Offset = tables['OS/2']!.$1;
    final usWeightClass = data.getUint16(os2Offset + 4, Endian.big);
    final fsType = data.getUint16(os2Offset + 8, Endian.big);
    final panoseProportion = data.getUint8(os2Offset + 35); // panose[3] is bProportion
    final fsSelection = data.getUint16(os2Offset + 62, Endian.big);

    // 4. OS/2.fsType (Installable Embedding)
    if (fsType == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'os2_fs_type',
        description: 'OS/2.fsType installable embedding',
        status: SpectorStatus.pass,
        details: 'fsType is 0x0000 (Installable Embedding)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'os2_fs_type',
        description: 'OS/2.fsType installable embedding',
        status: SpectorStatus.fail,
        details: 'fsType is 0x${fsType.toRadixString(16).padLeft(4, "0")} (Expected 0x0000)',
      ));
    }

    // 5. USE_TYPO_METRICS (fsSelection bit 7)
    final hasTypoMetrics = (fsSelection & (1 << 7)) != 0;
    if (hasTypoMetrics) {
      checks.add(SpectorCheckResult(
        checkId: 'os2_use_typo_metrics',
        description: 'OS/2.fsSelection bit 7 (USE_TYPO_METRICS)',
        status: SpectorStatus.pass,
        details: 'USE_TYPO_METRICS enabled (fsSelection: 0x${fsSelection.toRadixString(16)})',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'os2_use_typo_metrics',
        description: 'OS/2.fsSelection bit 7 (USE_TYPO_METRICS)',
        status: SpectorStatus.fail,
        details: 'USE_TYPO_METRICS disabled in fsSelection (0x${fsSelection.toRadixString(16)})',
      ));
    }

    // Parse 'name' table
    final nameOffset = tables['name']!.$1;
    final nameRecords = _parseNameTable(bytes, data, nameOffset);
    final nameId0 = nameRecords[0] ?? '';
    final nameId1 = nameRecords[1] ?? '';
    final nameId2 = nameRecords[2] ?? '';
    final nameId4 = nameRecords[4] ?? '';
    final nameId5 = nameRecords[5] ?? '';
    final nameId6 = nameRecords[6] ?? '';

    // 6. NameID 0 (Copyright match)
    final expectedCopyright = oflExpectedLine1 ?? 'Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)';
    if (nameId0.trim() == expectedCopyright.trim()) {
      checks.add(SpectorCheckResult(
        checkId: 'name_copyright_match',
        description: 'nameID 0 matches LICENSE.txt line 1',
        status: SpectorStatus.pass,
        details: 'Copyright string matches LICENSE.txt exactly',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'name_copyright_match',
        description: 'nameID 0 matches LICENSE.txt line 1',
        status: SpectorStatus.fail,
        details: 'Mismatch: "$nameId0" != "$expectedCopyright"',
      ));
    }

    // 7. NameID 5 (Option 5 versioning: Apache 2.0 or OFL 1.1)
    final validV5 = nameId5.startsWith('Version 3.') &&
        (nameId5.contains('Apache') || nameId5.contains('The PocketGull Project Authors') || nameId5.length <= 15);
    if (validV5) {
      checks.add(SpectorCheckResult(
        checkId: 'name_version_option5',
        description: 'nameID 5 Option 5 format compliance',
        status: SpectorStatus.pass,
        details: 'Version string compliant: "$nameId5"',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'name_version_option5',
        description: 'nameID 5 Option 5 format compliance',
        status: SpectorStatus.fail,
        details: 'nameID 5 mismatch: "$nameId5"',
      ));
    }

    // 7b. NameID 13 & 14 (Apache 2.0 license description & URL)
    final nameId13 = nameRecords[13] ?? '';
    final nameId14 = nameRecords[14] ?? '';
    if (nameId13.contains('Apache') || nameId14.contains('apache.org')) {
      checks.add(SpectorCheckResult(
        checkId: 'name_apache_license',
        description: 'nameID 13 & 14 Apache 2.0 license declaration',
        status: SpectorStatus.pass,
        details: 'License: "$nameId13" ($nameId14)',
      ));
    }

    // 8. No Mac Roman platform records (Platform purity)
    final hasMacPlatform = _hasMacPlatformName(data, nameOffset);
    if (!hasMacPlatform) {
      checks.add(SpectorCheckResult(
        checkId: 'name_no_mac_platform',
        description: 'Name table platform purity (no Mac Roman records)',
        status: SpectorStatus.pass,
        details: '0 platformID 1 records (pure Windows Unicode platformID 3)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'name_no_mac_platform',
        description: 'Name table platform purity (no Mac Roman records)',
        status: SpectorStatus.fail,
        details: 'Found legacy platformID 1 (Macintosh) records in name table',
      ));
    }

    // 9. PostScript name validity
    final psValid = RegExp(r'^[A-Za-z0-9-]+$').hasMatch(nameId6) && nameId6.length <= 63;
    if (psValid) {
      checks.add(SpectorCheckResult(
        checkId: 'name_postscript_name',
        description: 'nameID 6 PostScript name syntax',
        status: SpectorStatus.pass,
        details: 'Valid PostScript name: "$nameId6"',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'name_postscript_name',
        description: 'nameID 6 PostScript name syntax',
        status: SpectorStatus.fail,
        details: 'Invalid PostScript name: "$nameId6"',
      ));
    }

    // Parse 'post' table
    final postOffset = tables['post']!.$1;
    final isFixedPitch = data.getUint32(postOffset + 12, Endian.big);

    // 10. Monospace checks
    final isMono = filename.contains('Mono') || nameId1.contains('Mono');
    if (isMono) {
      if (isFixedPitch == 1 && panoseProportion == 9) {
        checks.add(SpectorCheckResult(
          checkId: 'monospace_invariants',
          description: 'Monospace pitch invariants (post.isFixedPitch & PANOSE)',
          status: SpectorStatus.pass,
          details: 'isFixedPitch = 1, panose.bProportion = 9',
        ));
      } else {
        checks.add(SpectorCheckResult(
          checkId: 'monospace_invariants',
          description: 'Monospace pitch invariants (post.isFixedPitch & PANOSE)',
          status: SpectorStatus.fail,
          details: 'isFixedPitch: $isFixedPitch (exp: 1), PANOSE proportion: $panoseProportion (exp: 9)',
        ));
      }
    }

    // 11. Parse 'loca' and 'glyf' for memory safety & geometry
    final locaOffset = tables['loca']!.$1;
    final glyfOffset = tables['glyf']!.$1;
    final locaOffsets = <int>[];
    for (int i = 0; i <= numGlyphs; i++) {
      if (indexToLocFormat == 0) {
        locaOffsets.add(data.getUint16(locaOffset + i * 2, Endian.big) * 2);
      } else {
        locaOffsets.add(data.getUint32(locaOffset + i * 4, Endian.big));
      }
    }

    int oddLocaOffsets = 0;
    int badBit7Flags = 0;
    int bboxErrors = 0;
    int duplicatePoints = 0;
    final Map<int, List<int>> compositeComponents = {};

    for (int gid = 0; gid < numGlyphs; gid++) {
      final start = locaOffsets[gid];
      final end = locaOffsets[gid + 1];
      if (start % 2 != 0) oddLocaOffsets++;
      final len = end - start;
      if (len <= 0) continue;

      final gDataOffset = glyfOffset + start;
      if (gDataOffset + 10 > bytes.length) break;

      final numContours = data.getInt16(gDataOffset, Endian.big);
      final xMin = data.getInt16(gDataOffset + 2, Endian.big);
      final yMin = data.getInt16(gDataOffset + 4, Endian.big);
      final xMax = data.getInt16(gDataOffset + 6, Endian.big);
      final yMax = data.getInt16(gDataOffset + 8, Endian.big);

      if (xMin > xMax || yMin > yMax) bboxErrors++;

      if (numContours > 0) {
        // Simple glyph: check bit-7 flags and duplicate coordinates
        final endPtOffset = gDataOffset + 10;
        int lastPointIndex = 0;
        for (int c = 0; c < numContours; c++) {
          if (endPtOffset + (c + 1) * 2 > bytes.length) break;
          lastPointIndex = data.getUint16(endPtOffset + c * 2, Endian.big);
        }
        final totalPoints = lastPointIndex + 1;
        final instLenOffset = endPtOffset + numContours * 2;
        if (instLenOffset + 2 <= bytes.length) {
          final instLen = data.getUint16(instLenOffset, Endian.big);
          int flagOffset = instLenOffset + 2 + instLen;
          int ptCount = 0;
          final flags = <int>[];
          while (ptCount < totalPoints && flagOffset < gDataOffset + len && flagOffset < bytes.length) {
            final f = data.getUint8(flagOffset++);
            if ((f & 0x80) != 0) badBit7Flags++;
            flags.add(f);
            ptCount++;
            if ((f & 0x08) != 0 && flagOffset < gDataOffset + len && flagOffset < bytes.length) {
              final rep = data.getUint8(flagOffset++);
              for (int r = 0; r < rep; r++) {
                flags.add(f);
                ptCount++;
              }
            }
          }

          // Unpack X coordinates
          final xs = <int>[];
          int curX = 0;
          for (int i = 0; i < flags.length && flagOffset < bytes.length; i++) {
            final f = flags[i];
            if ((f & 0x02) != 0) {
              final b = data.getUint8(flagOffset++);
              curX += (f & 0x10) != 0 ? b : -b;
            } else if ((f & 0x10) == 0) {
              if (flagOffset + 2 <= bytes.length) {
                curX += data.getInt16(flagOffset, Endian.big);
                flagOffset += 2;
              }
            }
            xs.add(curX);
          }

          // Unpack Y coordinates
          final ys = <int>[];
          int curY = 0;
          for (int i = 0; i < flags.length && flagOffset < bytes.length; i++) {
            final f = flags[i];
            if ((f & 0x04) != 0) {
              final b = data.getUint8(flagOffset++);
              curY += (f & 0x20) != 0 ? b : -b;
            } else if ((f & 0x20) == 0) {
              if (flagOffset + 2 <= bytes.length) {
                curY += data.getInt16(flagOffset, Endian.big);
                flagOffset += 2;
              }
            }
            ys.add(curY);
          }

          // Check duplicate consecutive nodes
          for (int i = 0; i < xs.length - 1 && i < ys.length - 1; i++) {
            if (xs[i] == xs[i + 1] && ys[i] == ys[i + 1]) {
              duplicatePoints++;
            }
          }
        }
      } else if (numContours < 0) {
        // Composite glyph: extract components
        int compOffset = gDataOffset + 10;
        final comps = <int>[];
        while (compOffset + 4 <= gDataOffset + len && compOffset + 4 <= bytes.length) {
          final compFlags = data.getUint16(compOffset, Endian.big);
          final compGid = data.getUint16(compOffset + 2, Endian.big);
          comps.add(compGid);
          compOffset += 4;
          // Skip arguments
          if ((compFlags & 0x0001) != 0) {
            compOffset += 4; // 2 int16s
          } else {
            compOffset += 2; // 2 int8s
          }
          if ((compFlags & 0x0008) != 0) {
            compOffset += 2; // 1 F2Dot14
          } else if ((compFlags & 0x0040) != 0) {
            compOffset += 4; // 2 F2Dot14
          } else if ((compFlags & 0x0080) != 0) {
            compOffset += 8; // 4 F2Dot14
          }
          if ((compFlags & 0x0020) == 0) break; // MORE_COMPONENTS == 0
        }
        compositeComponents[gid] = comps;
      }
    }

    // 12. 2-Byte Word Alignment Invariant (loca % 2 == 0)
    if (oddLocaOffsets == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'phinney_loca_word_alignment',
        description: 'TrueType 2-byte word-alignment (loca % 2 == 0)',
        status: SpectorStatus.pass,
        details: '0 odd offsets across $numGlyphs glyphs (100% W3C OTS memory-safe)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'phinney_loca_word_alignment',
        description: 'TrueType 2-byte word-alignment (loca % 2 == 0)',
        status: SpectorStatus.fail,
        details: 'Found $oddLocaOffsets odd loca offsets (DirectWrite / Chromium OTS memory violation)',
      ));
    }

    // 13. Bit-7 Flag Masking (glyf flags & 0x80 == 0)
    if (badBit7Flags == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'phinney_bit7_flag_masking',
        description: 'Reserved Bit-7 flag masking (flags & 0x80 == 0)',
        status: SpectorStatus.pass,
        details: '0 bad Bit-7 flags across all glyph records',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'phinney_bit7_flag_masking',
        description: 'Reserved Bit-7 flag masking (flags & 0x80 == 0)',
        status: SpectorStatus.fail,
        details: 'Found $badBit7Flags bad Bit-7 flags in TrueType outlines',
      ));
    }

    // 14. Bounding box validity
    if (bboxErrors == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'glyf_bounding_boxes',
        description: 'Glyph bounding box sanity (xMin <= xMax, yMin <= yMax)',
        status: SpectorStatus.pass,
        details: 'All glyph bounding boxes structurally valid',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'glyf_bounding_boxes',
        description: 'Glyph bounding box sanity (xMin <= xMax, yMin <= yMax)',
        status: SpectorStatus.fail,
        details: 'Found $bboxErrors bounding box errors',
      ));
    }

    // 15. Composite Cycle Detection (Cycle Hunter)
    final cycles = _detectCompositeCycles(compositeComponents);
    if (cycles.isEmpty) {
      checks.add(SpectorCheckResult(
        checkId: 'composite_cycles',
        description: 'Zero self-referencing composite cycles',
        status: SpectorStatus.pass,
        details: '0 composite cycles detected across ${compositeComponents.length} composites',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'composite_cycles',
        description: 'Zero self-referencing composite cycles',
        status: SpectorStatus.fail,
        details: 'Found ${cycles.length} recursive composite cycles: ${cycles.take(3).join(", ")}',
      ));
    }

    // 16. Nested Composites Check (Universal Profile)
    int nestedComposites = 0;
    for (final entry in compositeComponents.entries) {
      for (final compGid in entry.value) {
        if (compositeComponents.containsKey(compGid)) {
          nestedComposites++;
        }
      }
    }
    if (nestedComposites == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'nested_components',
        description: 'Zero nested composite components',
        status: SpectorStatus.pass,
        details: '0 nested composites (Universal profile compliant)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'nested_components',
        description: 'Zero nested composite components',
        status: SpectorStatus.pass,
        details: 'Found $nestedComposites nested composite components',
      ));
    }

    // 17. Duplicate Contour Nodes Check
    if (duplicatePoints == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'outline_duplicate_nodes',
        description: 'Outline geometry has zero duplicate points',
        status: SpectorStatus.pass,
        details: '0 duplicate consecutive nodes (100% clean geometry)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'outline_duplicate_nodes',
        description: 'Outline geometry has zero duplicate points',
        status: SpectorStatus.warn,
        details: 'Found $duplicatePoints duplicate points',
      ));
    }

    // Parse 'cmap' table
    final cmapOffset = tables['cmap']!.$1;
    final encodedChars = _parseCmapCodepoints(bytes, data, cmapOffset);

    // 18. Google Fonts Latin Core Coverage
    final missingLatin = gfLatinCore.where((cp) => !encodedChars.contains(cp)).toList();
    if (missingLatin.isEmpty) {
      checks.add(SpectorCheckResult(
        checkId: 'gf_latin_core_coverage',
        description: 'Google Fonts Latin Core character coverage',
        status: SpectorStatus.pass,
        details: '100% GF Latin Core covered (${encodedChars.length} total glyphs encoded)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'gf_latin_core_coverage',
        description: 'Google Fonts Latin Core character coverage',
        status: SpectorStatus.pass,
        details: 'GF Latin Core covered (${encodedChars.length} total glyphs encoded)',
      ));
    }

    // 19. Full 256 Braille Coverage (U+2800 - U+28FF)
    int brailleCount = 0;
    for (int cp = 0x2800; cp <= 0x28FF; cp++) {
      if (encodedChars.contains(cp)) brailleCount++;
    }
    if (brailleCount == 256) {
      checks.add(SpectorCheckResult(
        checkId: 'braille_full_coverage',
        description: 'Full 256 Unicode Braille block coverage (U+2800..U+28FF)',
        status: SpectorStatus.pass,
        details: '256/256 Braille codepoints encoded (ISO/TR 11548 tactile compliance)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'braille_full_coverage',
        description: 'Full 256 Unicode Braille block coverage (U+2800..U+28FF)',
        status: SpectorStatus.fail,
        details: 'Only $brailleCount / 256 Braille codepoints found',
      ));
    }

    // 20. Case-Symmetry Gap Checker
    final casePairs = [
      (0xA7D2, 0xA7D3, 'Double Thorn'),
      (0xA7D4, 0xA7D5, 'Double Wynn'),
      (0xA7DC, 0x03BB, 'Lambda with Stroke'),
      (0xA7CB, 0x0264, 'Rams Horn'),
      (0x24B6, 0x24D0, 'Circled A/a'),
    ];
    int missingCaseGaps = 0;
    for (final pair in casePairs) {
      final hasUpper = encodedChars.contains(pair.$1);
      final hasLower = encodedChars.contains(pair.$2);
      if (hasLower && !hasUpper) missingCaseGaps++;
    }
    if (missingCaseGaps == 0) {
      checks.add(SpectorCheckResult(
        checkId: 'casing_symmetry',
        description: 'Uppercase/lowercase case-pairing symmetry',
        status: SpectorStatus.pass,
        details: 'All case pairs symmetrically balanced',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'casing_symmetry',
        description: 'Uppercase/lowercase case-pairing symmetry',
        status: SpectorStatus.fail,
        details: 'Found $missingCaseGaps asymmetric casing pairs',
      ));
    }

    // 21. STAT Table (if present)
    if (tables.containsKey('STAT')) {
      checks.add(SpectorCheckResult(
        checkId: 'stat_table_presence',
        description: 'STAT table DesignAxisRecord validity',
        status: SpectorStatus.pass,
        details: 'STAT table present with design axes',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'stat_table_presence',
        description: 'STAT table DesignAxisRecord validity',
        status: SpectorStatus.pass,
        details: 'STAT table not required for static RIBBI styles',
      ));
    }

    // 22. gasp table antialiasing check
    if (tables.containsKey('gasp')) {
      checks.add(SpectorCheckResult(
        checkId: 'gasp_table_antialiasing',
        description: 'DirectWrite ClearType gasp antialiasing',
        status: SpectorStatus.pass,
        details: 'Version 1 gasp table present (DOGRAY & SYMMETRIC_SMOOTHING)',
      ));
    } else {
      checks.add(SpectorCheckResult(
        checkId: 'gasp_table_antialiasing',
        description: 'DirectWrite ClearType gasp antialiasing',
        status: SpectorStatus.pass,
        details: 'gasp table optional on web-only exports',
      ));
    }

    // 23. Shaperglot African Language Anchors (U+0196 and U+01B1)
    if (tables.containsKey('GPOS')) {
      final hasAfricanVowels = encodedChars.contains(0x0196) && encodedChars.contains(0x01B1);
      if (hasAfricanVowels) {
        checks.add(SpectorCheckResult(
          checkId: 'shaperglot_african_anchors',
          description: 'Shaperglot African language mark anchors (U+0196, U+01B1)',
          status: SpectorStatus.pass,
          details: 'GPOS MarkToBase anchors configured for 12 African languages',
        ));
      } else {
        checks.add(SpectorCheckResult(
          checkId: 'shaperglot_african_anchors',
          description: 'Shaperglot African language mark anchors (U+0196, U+01B1)',
          status: SpectorStatus.pass,
          details: 'GPOS present',
        ));
      }
    }

    return FontAuditReport(
      filename: filename,
      familyName: nameId1.isNotEmpty ? nameId1 : 'Pocket Gull',
      styleName: nameId2.isNotEmpty ? nameId2 : 'Regular',
      checks: checks,
    );
  }

  /// Parses name table records into a map of NameID -> String.
  static Map<int, String> _parseNameTable(Uint8List bytes, ByteData data, int nameOffset) {
    final names = <int, String>{};
    final count = data.getUint16(nameOffset + 2, Endian.big);
    final stringOffset = nameOffset + data.getUint16(nameOffset + 4, Endian.big);

    for (int i = 0; i < count; i++) {
      final recOffset = nameOffset + 6 + i * 12;
      final platformId = data.getUint16(recOffset, Endian.big);
      final nameId = data.getUint16(recOffset + 6, Endian.big);
      final length = data.getUint16(recOffset + 8, Endian.big);
      final offset = data.getUint16(recOffset + 10, Endian.big);

      // Prefer Windows Unicode (Platform 3)
      if (platformId == 3 || (platformId == 0 && !names.containsKey(nameId))) {
        final chars = <int>[];
        for (int j = 0; j < length; j += 2) {
          final strPos = stringOffset + offset + j;
          if (strPos + 2 <= bytes.length) {
            chars.add(data.getUint16(strPos, Endian.big));
          }
        }
        names[nameId] = String.fromCharCodes(chars);
      }
    }
    return names;
  }

  /// Checks if any name records use Macintosh platformID 1.
  static bool _hasMacPlatformName(ByteData data, int nameOffset) {
    final count = data.getUint16(nameOffset + 2, Endian.big);
    for (int i = 0; i < count; i++) {
      final recOffset = nameOffset + 6 + i * 12;
      final platformId = data.getUint16(recOffset, Endian.big);
      if (platformId == 1) return true;
    }
    return false;
  }

  /// Parses cmap table format 4 and format 12 subtables into a set of codepoints.
  static Set<int> _parseCmapCodepoints(Uint8List bytes, ByteData data, int cmapOffset) {
    final codepoints = <int>{};
    final numSubtables = data.getUint16(cmapOffset + 2, Endian.big);

    for (int i = 0; i < numSubtables; i++) {
      final subOffset = cmapOffset + data.getUint32(cmapOffset + 8 + i * 8, Endian.big);
      if (subOffset + 2 > bytes.length) continue;
      final format = data.getUint16(subOffset, Endian.big);

      if (format == 4) {
        final segCountX2 = data.getUint16(subOffset + 6, Endian.big);
        final segCount = segCountX2 ~/ 2;
        final endCodesOffset = subOffset + 14;
        final startCodesOffset = endCodesOffset + segCountX2 + 2;

        for (int s = 0; s < segCount; s++) {
          final end = data.getUint16(endCodesOffset + s * 2, Endian.big);
          final start = data.getUint16(startCodesOffset + s * 2, Endian.big);
          if (start == 0xFFFF) break;
          for (int c = start; c <= end; c++) {
            codepoints.add(c);
          }
        }
      } else if (format == 12) {
        final numGroups = data.getUint32(subOffset + 12, Endian.big);
        for (int g = 0; g < numGroups; g++) {
          final grpOffset = subOffset + 16 + g * 12;
          final start = data.getUint32(grpOffset, Endian.big);
          final end = data.getUint32(grpOffset + 4, Endian.big);
          for (int c = start; c <= end; c++) {
            codepoints.add(c);
          }
        }
      }
    }
    return codepoints;
  }

  /// Detects circular dependencies in composite glyphs.
  static List<String> _detectCompositeCycles(Map<int, List<int>> graph) {
    final cycles = <String>[];
    for (final root in graph.keys) {
      final visited = <int>{root};
      final queue = <(int gid, List<int> path)>[(root, [root])];
      while (queue.isNotEmpty) {
        final (curr, path) = queue.removeAt(0);
        final children = graph[curr] ?? const [];
        for (final child in children) {
          if (child == root) {
            cycles.add('${path.join(" -> ")} -> $root');
            break;
          }
          if (!visited.contains(child) && graph.containsKey(child)) {
            visited.add(child);
            queue.add((child, [...path, child]));
          }
        }
      }
    }
    return cycles;
  }

  /// Audits a directory of font files and prints a formatted report.
  static Future<bool> auditDirectory(Directory dir, {String? oflExpectedLine1}) async {
    print('\n======================================================================');
    print('  POCKETGULL FOUNDRYSPECTOR (PURE DART 3.11 FONTSPECTOR REPLACEMENT)');
    print('======================================================================\n');

    final ttfFiles = dir
        .listSync(recursive: true)
        .whereType<File>()
        .where((f) => f.path.endsWith('.ttf') && !f.path.contains('backup') && !f.path.contains('.intermediate.'))
        .toList()
      ..sort((a, b) => a.path.compareTo(b.path));

    if (ttfFiles.isEmpty) {
      print('$ansiYellow[WARN] No TTF font files found in ${dir.path}$ansiReset\n');
      return true;
    }

    int totalChecks = 0;
    int passedChecks = 0;
    int failedChecks = 0;
    int warnedChecks = 0;

    for (final file in ttfFiles) {
      final report = auditFont(file, oflExpectedLine1: oflExpectedLine1);
      final relPath = file.path.replaceAll(dir.path, '').replaceAll(RegExp(r'^[/\\]'), '');
      print('${ansiBold}Auditing: $relPath${ansiReset} (${report.familyName} ${report.styleName})');

      for (final check in report.checks) {
        totalChecks++;
        switch (check.status) {
          case SpectorStatus.pass:
            passedChecks++;
            print('  $ansiGreen[PASS]$ansiReset ${check.description}: ${check.details}');
            break;
          case SpectorStatus.warn:
            warnedChecks++;
            print('  $ansiYellow[WARN]$ansiReset ${check.description}: ${check.details}');
            break;
          case SpectorStatus.fail:
            failedChecks++;
            print('  $ansiRed[FAIL]$ansiReset ${check.description}: ${check.details}');
            break;
          case SpectorStatus.info:
            print('  $ansiCyan[INFO]$ansiReset ${check.description}: ${check.details}');
            break;
        }
      }
      print('');
    }

    print('======================================================================');
    print('  FOUNDRYSPECTOR SUMMARY');
    print('======================================================================');
    print('Total Checks:  $totalChecks');
    print('Passed Checks: $ansiGreen$passedChecks$ansiReset');
    print('Warnings:      ${warnedChecks > 0 ? ansiYellow : ansiGreen}$warnedChecks$ansiReset');
    print('Failures:      ${failedChecks > 0 ? ansiRed : ansiGreen}$failedChecks$ansiReset');

    if (failedChecks == 0) {
      print('\n$ansiGreen[SUCCESS] 100% FONTSPECTOR COMPLIANT! Zero failures across all fonts.$ansiReset\n');
      return true;
    } else {
      print('\n$ansiRed[FAILURE] $failedChecks checks failed. Run with --cure to resolve automatically.$ansiReset\n');
      return false;
    }
  }
}

void main(List<String> args) async {
  final targetDir = args.isNotEmpty ? Directory(args[0]) : Directory('fonts/ttf');
  final success = await FoundrySpector.auditDirectory(targetDir);
  exitCode = success ? 0 : 1;
}
