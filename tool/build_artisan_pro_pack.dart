/// Pure Dart SFNT Color-Font Synthesizer for PocketGull Artisan Studio Packs:
/// 1. PocketGull-Kinpaku.ttf (金箔 — 24k Gold Leaf): Layers solid PocketGull-Black (Layer 0: Kinpaku Gold Seam)
///    beneath hollow PocketGull-Kintsugi (Layer 1: Ceramic Body) via OpenType COLR v0 + CPAL!
///    Every hollow trabecular channel shines with authentic 24k Kinpaku gold leaf on urushi lacquer.
/// 2. PocketGull-BotanicaColor.ttf: Dual-palette botanical emerald & vermilion rubrication.
/// 3. Exports standalone SVG Herbarium Vector Pack (U+2766..U+2698) for Figma/Illustrator.

import 'dart:io';
import 'dart:typed_data';
import 'foundry/models.dart';
import 'foundry/cpal_colr_engine.dart';
import 'foundry/phinney_auditor.dart';

class RawSfntFont {
  final Uint8List bytes;
  final Map<String, ({int offset, int length})> tables = {};

  RawSfntFont(this.bytes) {
    final bd = ByteData.sublistView(bytes);
    final numTables = bd.getUint16(4, Endian.big);
    for (var i = 0; i < numTables; i++) {
      final off = 12 + i * 16;
      final tag = String.fromCharCodes(bytes.sublist(off, off + 4));
      final tOff = bd.getUint32(off + 8, Endian.big);
      final tLen = bd.getUint32(off + 12, Endian.big);
      tables[tag] = (offset: tOff, length: tLen);
    }
  }

  Uint8List tableBytes(String tag) {
    final t = tables[tag]!;
    return Uint8List.sublistView(bytes, t.offset, t.offset + t.length);
  }

  int get numGlyphs {
    final maxp = tableBytes('maxp');
    return ByteData.sublistView(maxp).getUint16(4, Endian.big);
  }

  int get indexToLocFormat {
    final head = tableBytes('head');
    return ByteData.sublistView(head).getInt16(50, Endian.big);
  }

  List<int> readLocaOffsets() {
    final loca = tableBytes('loca');
    final bd = ByteData.sublistView(loca);
    final count = numGlyphs + 1;
    if (indexToLocFormat == 0) {
      return List<int>.generate(count, (i) => bd.getUint16(i * 2, Endian.big) * 2);
    } else {
      return List<int>.generate(count, (i) => bd.getUint32(i * 4, Endian.big));
    }
  }

  Map<int, int> readCmapFormat4Or12() {
    final cmap = tableBytes('cmap');
    final bd = ByteData.sublistView(cmap);
    final numSubtables = bd.getUint16(2, Endian.big);
    int? fmt12Off;
    int? fmt4Off;
    for (var i = 0; i < numSubtables; i++) {
      final plat = bd.getUint16(4 + i * 8, Endian.big);
      final subOff = bd.getUint32(4 + i * 8 + 4, Endian.big);
      final fmt = bd.getUint16(subOff, Endian.big);
      if ((plat == 3 || plat == 0) && fmt == 12) fmt12Off = subOff;
      if ((plat == 3 || plat == 0) && fmt == 4) fmt4Off = subOff;
    }

    final result = <int, int>{};
    if (fmt12Off != null) {
      final nGroups = bd.getUint32(fmt12Off + 12, Endian.big);
      for (var g = 0; g < nGroups; g++) {
        final go = fmt12Off + 16 + g * 12;
        final startCp = bd.getUint32(go, Endian.big);
        final endCp = bd.getUint32(go + 4, Endian.big);
        final startGid = bd.getUint32(go + 8, Endian.big);
        for (var cp = startCp; cp <= endCp; cp++) {
          result[cp] = startGid + (cp - startCp);
        }
      }
      return result;
    }
    if (fmt4Off != null) {
      final segCount = bd.getUint16(fmt4Off + 6, Endian.big) ~/ 2;
      final endCodeOff = fmt4Off + 14;
      final startCodeOff = endCodeOff + segCount * 2 + 2;
      final idDeltaOff = startCodeOff + segCount * 2;
      final idRangeOff = idDeltaOff + segCount * 2;
      for (var s = 0; s < segCount; s++) {
        final endC = bd.getUint16(endCodeOff + s * 2, Endian.big);
        final startC = bd.getUint16(startCodeOff + s * 2, Endian.big);
        final delta = bd.getInt16(idDeltaOff + s * 2, Endian.big);
        final rangeOff = bd.getUint16(idRangeOff + s * 2, Endian.big);
        if (startC == 0xFFFF) break;
        for (var cp = startC; cp <= endC; cp++) {
          int gid;
          if (rangeOff == 0) {
            gid = (cp + delta) & 0xFFFF;
          } else {
            final glyphIdxOff = idRangeOff + s * 2 + rangeOff + (cp - startC) * 2;
            final raw = bd.getUint16(glyphIdxOff, Endian.big);
            gid = raw == 0 ? 0 : (raw + delta) & 0xFFFF;
          }
          if (gid != 0) result[cp] = gid;
        }
      }
    }
    return result;
  }

  ({int advanceWidth, int lsb}) readHmtxMetric(int gid) {
    final hhea = tableBytes('hhea');
    final numOfLongHorMetrics = ByteData.sublistView(hhea).getUint16(34, Endian.big);
    final hmtx = tableBytes('hmtx');
    final bd = ByteData.sublistView(hmtx);
    if (gid < numOfLongHorMetrics) {
      return (
        advanceWidth: bd.getUint16(gid * 4, Endian.big),
        lsb: bd.getInt16(gid * 4 + 2, Endian.big),
      );
    } else {
      final aw = bd.getUint16((numOfLongHorMetrics - 1) * 4, Endian.big);
      final lsbOff = numOfLongHorMetrics * 4 + (gid - numOfLongHorMetrics) * 2;
      return (advanceWidth: aw, lsb: bd.getInt16(lsbOff, Endian.big));
    }
  }
}

Uint8List buildNameTable({
  required String familyName,
  required String subFamilyName,
  required String postScriptName,
}) {
  final fullName = subFamilyName == 'Regular' ? familyName : '$familyName $subFamilyName';
  final records = <(int, String)>[
    (0, 'Copyright 2026 PocketGull LLC & Phil Gear (https://pocketgull.com). Commercial Studio Edition.'),
    (1, familyName),
    (2, subFamilyName),
    (3, '4.000;PGUL;$postScriptName'),
    (4, fullName),
    (5, 'Version 4.000; PocketGull Artisan Foundry'),
    (6, postScriptName),
    (9, 'Phil Gear'),
    (11, 'https://pocketgull.com/foundry'),
    (13, 'PocketGull Commercial Studio & Patron License (https://pocketgull.com/foundry)'),
    (14, 'https://pocketgull.com/foundry'),
    (16, familyName),
    (17, subFamilyName),
  ];

  final count = records.length;
  final stringOffset = 6 + count * 12;
  final header = ByteData(stringOffset);
  header.setUint16(0, 0, Endian.big);
  header.setUint16(2, count, Endian.big);
  header.setUint16(4, stringOffset, Endian.big);

  final pool = BytesBuilder();
  for (var i = 0; i < count; i++) {
    final (nameId, val) = records[i];
    final utf16 = Uint8List(val.length * 2);
    final v = ByteData.sublistView(utf16);
    for (var c = 0; c < val.length; c++) {
      v.setUint16(c * 2, val.codeUnitAt(c), Endian.big);
    }
    final recOff = 6 + i * 12;
    header.setUint16(recOff + 0, 3, Endian.big);
    header.setUint16(recOff + 2, 1, Endian.big);
    header.setUint16(recOff + 4, 0x0409, Endian.big);
    header.setUint16(recOff + 6, nameId, Endian.big);
    header.setUint16(recOff + 8, utf16.length, Endian.big);
    header.setUint16(recOff + 10, pool.length, Endian.big);
    pool.add(utf16);
  }

  final out = BytesBuilder();
  out.add(header.buffer.asUint8List());
  out.add(pool.takeBytes());
  final raw = out.takeBytes();
  if (raw.length % 2 != 0) {
    final padded = Uint8List(raw.length + 1)..setAll(0, raw);
    return padded;
  }
  return raw;
}

int computeTableChecksum(Uint8List data) {
  final paddedLen = (data.length + 3) & ~3;
  final buf = Uint8List(paddedLen)..setAll(0, data);
  final bd = ByteData.sublistView(buf);
  var sum = 0;
  for (var i = 0; i < paddedLen; i += 4) {
    sum = (sum + bd.getUint32(i, Endian.big)) & 0xFFFFFFFF;
  }
  return sum;
}

Uint8List assembleSfnt(Map<String, Uint8List> tableMap) {
  final sortedTags = tableMap.keys.toList()..sort();
  final numTables = sortedTags.length;

  var searchRange = 1;
  var entrySelector = 0;
  while (searchRange * 2 <= numTables) {
    searchRange *= 2;
    entrySelector++;
  }
  searchRange *= 16;
  final rangeShift = numTables * 16 - searchRange;

  final dirSize = 12 + numTables * 16;
  var currentOffset = dirSize;
  final offsets = <String, int>{};
  final lengths = <String, int>{};
  final checksums = <String, int>{};

  // Ensure head checkSumAdjustment is zeroed before checksumming
  if (tableMap.containsKey('head')) {
    final headCopy = Uint8List.fromList(tableMap['head']!);
    ByteData.sublistView(headCopy).setUint32(8, 0, Endian.big);
    tableMap['head'] = headCopy;
  }

  final body = BytesBuilder();
  for (final tag in sortedTags) {
    final data = tableMap[tag]!;
    offsets[tag] = currentOffset;
    lengths[tag] = data.length;
    checksums[tag] = computeTableChecksum(data);

    body.add(data);
    final pad = (4 - (data.length % 4)) % 4;
    if (pad > 0) body.add(Uint8List(pad));
    currentOffset += data.length + pad;
  }

  final header = Uint8List(dirSize);
  final hbd = ByteData.sublistView(header);
  hbd.setUint32(0, 0x00010000, Endian.big);
  hbd.setUint16(4, numTables, Endian.big);
  hbd.setUint16(6, searchRange, Endian.big);
  hbd.setUint16(8, entrySelector, Endian.big);
  hbd.setUint16(10, rangeShift, Endian.big);

  for (var i = 0; i < numTables; i++) {
    final tag = sortedTags[i];
    final off = 12 + i * 16;
    for (var c = 0; c < 4; c++) {
      header[off + c] = tag.codeUnitAt(c);
    }
    hbd.setUint32(off + 4, checksums[tag]!, Endian.big);
    hbd.setUint32(off + 8, offsets[tag]!, Endian.big);
    hbd.setUint32(off + 12, lengths[tag]!, Endian.big);
  }

  final full = BytesBuilder()
    ..add(header)
    ..add(body.takeBytes());
  final fullBytes = full.takeBytes();

  // Write head.checkSumAdjustment = 0xB1B0AFBA - totalChecksum
  final totalSum = computeTableChecksum(fullBytes);
  final adj = (0xB1B0AFBA - totalSum) & 0xFFFFFFFF;
  final headOffset = offsets['head']!;
  ByteData.sublistView(fullBytes).setUint32(headOffset + 8, adj, Endian.big);

  return fullBytes;
}

/// Builds PocketGull-Kinpaku.ttf (or legacy alias):
/// Appends solid underlay glyphs from PocketGull-Black for ASCII & Latin-1 display characters,
/// then wires OpenType COLR v0 + 4-Palette CPAL so Layer 0 = 24k Kinpaku Gold Seam and Layer 1 = Ceramic Body!
Uint8List buildKinpakuColorFont(
  RawSfntFont kintsugi,
  RawSfntFont solidBlack, {
  String familyName = 'PocketGull Kinpaku',
  String postScriptName = 'PocketGullKinpaku-Regular',
}) {
  final kinCmap = kintsugi.readCmapFormat4Or12();
  final blkCmap = solidBlack.readCmapFormat4Or12();

  final kinLoca = kintsugi.readLocaOffsets();
  final blkLoca = solidBlack.readLocaOffsets();
  final kinGlyf = kintsugi.tableBytes('glyf');
  final blkGlyf = solidBlack.tableBytes('glyf');

  final origNumGlyphs = kintsugi.numGlyphs;
  final hhea = Uint8List.fromList(kintsugi.tableBytes('hhea'));
  final origNumHMetrics = ByteData.sublistView(hhea).getUint16(34, Endian.big);

  // Rebuild full hmtx with longHorMetric for all glyphs so appended glyphs have clean metrics
  final hmtxBuilder = BytesBuilder();
  for (var g = 0; g < origNumGlyphs; g++) {
    final m = kintsugi.readHmtxMetric(g);
    final b = ByteData(4)
      ..setUint16(0, m.advanceWidth, Endian.big)
      ..setInt16(2, m.lsb, Endian.big);
    hmtxBuilder.add(b.buffer.asUint8List());
  }

  final glyfBuilder = BytesBuilder()..add(kinGlyf);
  if (kinGlyf.length % 2 != 0) glyfBuilder.addByte(0);

  final newLoca = List<int>.from(kinLoca);
  newLoca[newLoca.length - 1] = glyfBuilder.length;

  final colrGlyphs = <ColrBaseGlyph>[];
  var nextGid = origNumGlyphs;

  // Target printable display range: U+0021..U+024F + punctuation
  final targetCps = kinCmap.keys.where((cp) =>
    (cp >= 0x0021 && cp <= 0x007E) ||
    (cp >= 0x00A1 && cp <= 0x024F) ||
    (cp >= 0x2010 && cp <= 0x203A)
  ).toList()..sort();

  for (final cp in targetCps) {
    final kinGid = kinCmap[cp]!;
    final blkGid = blkCmap[cp];
    if (blkGid == null || kinGid == 0 || blkGid == 0) continue;

    final bStart = blkLoca[blkGid];
    final bEnd = blkLoca[blkGid + 1];
    if (bEnd <= bStart) continue; // empty space glyph

    var slice = Uint8List.sublistView(blkGlyf, bStart, bEnd);
    if (slice.length % 2 != 0) {
      final padded = Uint8List(slice.length + 1)..setAll(0, slice);
      slice = padded;
    }

    final underlayGid = nextGid++;
    glyfBuilder.add(slice);
    newLoca.add(glyfBuilder.length);

    final km = kintsugi.readHmtxMetric(kinGid);
    final mb = ByteData(4)
      ..setUint16(0, km.advanceWidth, Endian.big)
      ..setInt16(2, km.lsb, Endian.big);
    hmtxBuilder.add(mb.buffer.asUint8List());

    // COLR v0: Layer 0 = Solid Gold Lacquer Underlay (palette index 1), Layer 1 = Kintsugi Ceramic Wall (palette index 0)
    colrGlyphs.add(ColrBaseGlyph(kinGid, [
      ColrLayer(underlayGid, 1), // 24k Urushi Gold Seam filling the hollow medullary channels!
      ColrLayer(kinGid, 0),      // Ceramic / Obsidian cortical outer wall
    ]));
  }

  // Update head.indexToLocFormat = 1 (long offsets)
  final head = Uint8List.fromList(kintsugi.tableBytes('head'));
  ByteData.sublistView(head).setInt16(50, 1, Endian.big);

  // Build 4-byte loca table
  final locaBytes = Uint8List(newLoca.length * 4);
  final lbd = ByteData.sublistView(locaBytes);
  for (var i = 0; i < newLoca.length; i++) {
    lbd.setUint32(i * 4, newLoca[i], Endian.big);
  }

  // Update maxp.numGlyphs & hhea.numberOfHMetrics
  final maxp = Uint8List.fromList(kintsugi.tableBytes('maxp'));
  ByteData.sublistView(maxp).setUint16(4, nextGid, Endian.big);
  ByteData.sublistView(hhea).setUint16(34, nextGid, Endian.big);

  // Update post table to version 3.0 (clean for appended synthetic underlay glyphs)
  final post = Uint8List.fromList(kintsugi.tableBytes('post').sublist(0, 32));
  ByteData.sublistView(post).setUint32(0, 0x00030000, Endian.big);

  // Build 4 Artisan Kintsugi Palettes in CPAL
  final cpal = CpalTableBuilder([
    // Palette 0: Kuro-Urushi & 24k Gold (Dark Obsidian Ceramic + Luminous Gold Seam)
    CpalPalette('Kuro-Urushi 24k Gold', [
      CpalColor.fromHex(0xF8FAFC), // 0: Porcelain Ivory Wall (high contrast on dark web hero)
      CpalColor.fromHex(0xF59E0B), // 1: 24k Molten Urushi Gold Seam
    ]),
    // Palette 1: Kyoto Celadon & Gold (Daylight Washi Paper Mode)
    CpalPalette('Kyoto Celadon & Gold', [
      CpalColor.fromHex(0x1C1917), // 0: Sumi Stoneware Charcoal Wall
      CpalColor.fromHex(0xD97706), // 1: Burnished Kinpaku Gold Leaf Seam
    ]),
    // Palette 2: Aizome Indigo & Platinum Silver (Gin-tsugi Silver Joinery)
    CpalPalette('Aizome Silver Gin-tsugi', [
      CpalColor.fromHex(0x1E3A8A), // 0: Deep Aizome Indigo Porcelain
      CpalColor.fromHex(0x38BDF8), // 1: Luminous Silver-Cyan Seam
    ]),
    // Palette 3: Shu-Urushi Vermilion & Gold
    CpalPalette('Vermilion Lacquer & Gold', [
      CpalColor.fromHex(0x7F1D1D), // 0: Deep Vermilion Lacquer Wall
      CpalColor.fromHex(0xFBBF24), // 1: Imperial Gold Vein
    ]),
  ]).build();

  final colr = ColrTableBuilder(colrGlyphs).build();

  final outTables = <String, Uint8List>{};
  for (final tag in kintsugi.tables.keys) {
    if (tag == 'DSIG') continue;
    outTables[tag] = kintsugi.tableBytes(tag);
  }
  outTables['head'] = head;
  outTables['maxp'] = maxp;
  outTables['hhea'] = hhea;
  outTables['hmtx'] = hmtxBuilder.takeBytes();
  outTables['loca'] = locaBytes;
  outTables['glyf'] = glyfBuilder.takeBytes();
  outTables['post'] = post;
  outTables['name'] = buildNameTable(
    familyName: familyName,
    subFamilyName: 'Regular',
    postScriptName: postScriptName,
  );
  outTables['CPAL'] = cpal.data;
  outTables['COLR'] = colr.data;

  print('  [COLR] Synthesized ${colrGlyphs.length} 24k Kinpaku Gold-Seam glyphs [$familyName] ($origNumGlyphs -> $nextGid total glyphs, origHMetrics=$origNumHMetrics)');
  return assembleSfnt(outTables);
}

/// Extracts TrueType quadratic contours from Botanica's 6 Herbarium Fleurons (U+2766..U+2698)
/// and writes crisp standalone SVG vector plates for print/Figma/Adobe Illustrator buyers.
void exportHerbariumSvgKit(RawSfntFont botanica, Directory svgOutDir) {
  svgOutDir.createSync(recursive: true);
  final cmap = botanica.readCmapFormat4Or12();
  final loca = botanica.readLocaOffsets();
  final glyf = botanica.tableBytes('glyf');

  const specimens = <(int, String, String)>[
    (0x2766, '01-aldine-ivy-leaf', 'Aldine Ivy Leaf (U+2766)'),
    (0x2767, '02-hedera-vine-sprig', 'Hedera Vine Sprig (U+2767)'),
    (0x2619, '03-laurel-branch', 'Laurel Branch (U+2619)'),
    (0x273F, '04-wild-briar-rose', 'Wild Briar Rose (U+273F)'),
    (0x2740, '05-waterlily-crown', 'Waterlily Crown (U+2740)'),
    (0x2698, '06-stemmed-tulip', 'Stemmed Tulip (U+2698)'),
  ];

  for (final (cp, slug, title) in specimens) {
    final gid = cmap[cp];
    if (gid == null) continue;
    final gStart = loca[gid];
    final gEnd = loca[gid + 1];
    if (gEnd <= gStart) continue;

    final slice = Uint8List.sublistView(glyf, gStart, gEnd);
    final bd = ByteData.sublistView(slice);
    final numContours = bd.getInt16(0, Endian.big);
    if (numContours <= 0) continue;

    final xMin = bd.getInt16(2, Endian.big);
    final yMin = bd.getInt16(4, Endian.big);
    final xMax = bd.getInt16(6, Endian.big);
    final yMax = bd.getInt16(8, Endian.big);

    final endPts = <int>[];
    for (var c = 0; c < numContours; c++) {
      endPts.add(bd.getUint16(10 + c * 2, Endian.big));
    }
    final numPoints = endPts.last + 1;
    final instrLen = bd.getUint16(10 + numContours * 2, Endian.big);
    var ptr = 10 + numContours * 2 + 2 + instrLen;

    final flags = <int>[];
    while (flags.length < numPoints) {
      final f = slice[ptr++];
      flags.add(f);
      if ((f & 0x08) != 0) {
        final repeat = slice[ptr++];
        for (var r = 0; r < repeat; r++) {
          flags.add(f);
        }
      }
    }

    final xs = List<int>.filled(numPoints, 0);
    var curX = 0;
    for (var i = 0; i < numPoints; i++) {
      final f = flags[i];
      if ((f & 0x02) != 0) {
        final dx = slice[ptr++];
        curX += ((f & 0x10) != 0) ? dx : -dx;
      } else if ((f & 0x10) == 0) {
        curX += bd.getInt16(ptr, Endian.big);
        ptr += 2;
      }
      xs[i] = curX;
    }

    final ys = List<int>.filled(numPoints, 0);
    var curY = 0;
    for (var i = 0; i < numPoints; i++) {
      final f = flags[i];
      if ((f & 0x04) != 0) {
        final dy = slice[ptr++];
        curY += ((f & 0x20) != 0) ? dy : -dy;
      } else if ((f & 0x20) == 0) {
        curY += bd.getInt16(ptr, Endian.big);
        ptr += 2;
      }
      ys[i] = curY;
    }

    // Convert TrueType contours (y-up) to SVG path data (y-down inside 1000x1000 viewBox)
    final pathBuf = StringBuffer();
    var cStart = 0;
    for (var c = 0; c < numContours; c++) {
      final cEnd = endPts[c];
      final count = cEnd - cStart + 1;
      if (count >= 2) {
        List<({double x, double y, bool on})> pts = [];
        for (var idx = cStart; idx <= cEnd; idx++) {
          pts.add((x: xs[idx].toDouble(), y: (900 - ys[idx]).toDouble(), on: (flags[idx] & 0x01) != 0));
        }

        // Expand implied on-curve midpoints between consecutive off-curve points
        final expanded = <({double x, double y, bool on})>[];
        for (var i = 0; i < pts.length; i++) {
          final curr = pts[i];
          final next = pts[(i + 1) % pts.length];
          expanded.add(curr);
          if (!curr.on && !next.on) {
            expanded.add((x: 0.5 * (curr.x + next.x), y: 0.5 * (curr.y + next.y), on: true));
          }
        }

        // Rotate so first point is on-curve
        final firstOn = expanded.indexWhere((p) => p.on);
        if (firstOn >= 0) {
          final ordered = [...expanded.sublist(firstOn), ...expanded.sublist(0, firstOn)];
          pathBuf.write('M ${ordered[0].x.toStringAsFixed(1)} ${ordered[0].y.toStringAsFixed(1)} ');
          var i = 1;
          while (i < ordered.length) {
            final p = ordered[i];
            if (p.on) {
              pathBuf.write('L ${p.x.toStringAsFixed(1)} ${p.y.toStringAsFixed(1)} ');
              i++;
            } else {
              final next = ordered[(i + 1) % ordered.length];
              pathBuf.write('Q ${p.x.toStringAsFixed(1)} ${p.y.toStringAsFixed(1)} ${next.x.toStringAsFixed(1)} ${next.y.toStringAsFixed(1)} ');
              i += 2;
            }
          }
          pathBuf.write('Z ');
        }
      }
      cStart = cEnd + 1;
    }

    final pad = 60;
    final vbX = xMin - pad;
    final vbY = (900 - yMax) - pad;
    final vbW = (xMax - xMin) + pad * 2;
    final vbH = (yMax - yMin) + pad * 2;

    final svg = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- PocketGull Botanica v3 Herbarium Vector Plate: $title -->
<!-- Copyright (c) 2026 PocketGull LLC & Phil Gear (https://pocketgull.com/foundry) -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="$vbX $vbY $vbW $vbH" width="1000" height="1000" role="img" aria-label="$title">
  <title>$title — PocketGull Botanica Herbarium</title>
  <path fill="#166534" fill-rule="nonzero" d="${pathBuf.toString().trim()}"/>
</svg>
''';
    File('${svgOutDir.path}/$slug.svg').writeAsStringSync(svg);
  }
  print('  [SVG] Exported 6 standalone Botanica Herbarium SVG plates to ${svgOutDir.path}');
}

void main() {
  final kinBytes = File('distribution/upcycled/PocketGull-Kintsugi.ttf').readAsBytesSync();
  final botBytes = File('distribution/upcycled/PocketGull-Botanica.ttf').readAsBytesSync();
  final blkBytes = File('fonts/ttf/PocketGull-Black.ttf').readAsBytesSync();

  final kintsugi = RawSfntFont(kinBytes);
  final botanica = RawSfntFont(botBytes);
  final solidBlack = RawSfntFont(blkBytes);

  final proDir = Directory('../pocketgull-com/public/fonts/foundry');
  proDir.createSync(recursive: true);
  final localFoundryDir = Directory('fonts/foundry');
  localFoundryDir.createSync(recursive: true);

  // 1. Build Primary PocketGull-Kinpaku.ttf (金箔 24k Gold COLR) + Legacy Alias PocketGull-KintsugiGold.ttf
  final kinpakuBytes = buildKinpakuColorFont(
    kintsugi,
    solidBlack,
    familyName: 'PocketGull Kinpaku',
    postScriptName: 'PocketGullKinpaku-Regular',
  );
  final kintsugiGoldAliasBytes = buildKinpakuColorFont(
    kintsugi,
    solidBlack,
    familyName: 'PocketGull Kintsugi Gold',
    postScriptName: 'PocketGullKintsugiGold-Regular',
  );

  final outKinpakuPath = '${proDir.path}/PocketGull-Kinpaku.ttf';
  final outGoldAliasPath = '${proDir.path}/PocketGull-KintsugiGold.ttf';
  File(outKinpakuPath).writeAsBytesSync(kinpakuBytes);
  File(outGoldAliasPath).writeAsBytesSync(kintsugiGoldAliasBytes);
  File('${localFoundryDir.path}/PocketGull-Kinpaku.ttf').writeAsBytesSync(kinpakuBytes);
  File('${localFoundryDir.path}/PocketGull-KintsugiGold.ttf').writeAsBytesSync(kintsugiGoldAliasBytes);

  // Copy Botanica & Kintsugi WOFF2 + TTF for instant live type-tester & Pro ZIP packaging
  File('distribution/upcycled/PocketGull-Botanica.woff2')
      .copySync('${proDir.path}/PocketGull-Botanica.woff2');
  File('distribution/upcycled/PocketGull-Kintsugi.woff2')
      .copySync('${proDir.path}/PocketGull-Kintsugi.woff2');
  File('distribution/upcycled/PocketGull-Botanica.ttf')
      .copySync('${proDir.path}/PocketGull-Botanica.ttf');
  File('distribution/upcycled/PocketGull-Kintsugi.ttf')
      .copySync('${proDir.path}/PocketGull-Kintsugi.ttf');

  // 2. Audit newly compiled Kinpaku & KintsugiGold binaries with ThomasPhinneyAuditor!
  for (final p in [outKinpakuPath, outGoldAliasPath]) {
    final auditReport = ThomasPhinneyAuditor.audit(File(p));
    if (!auditReport.passed) {
      stderr.writeln('FATAL: Phinney audit failed on $p: ${auditReport.message}');
      exit(1);
    }
    print('  [OTS] ${p.split('/').last} passed 100% Phinney W3C OTS Audit (${auditReport.message}, ${(File(p).lengthSync() / 1024).toStringAsFixed(1)} KB)');
  }

  // 3. Export standalone SVG Herbarium Vector Kit
  exportHerbariumSvgKit(botanica, Directory('${proDir.path}/herbarium-svg'));
}
