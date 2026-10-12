import 'dart:io';
import 'foundry/cpal_colr_engine.dart';

void main() {
  stdout.writeln('=== POCKETGULL CPAL & COLRv0 FOUNDRY TEST ===');

  // 1. Build CPAL Table
  final cpalBuilder = CpalTableBuilder.pocketgullStandard();
  final cpalTable = cpalBuilder.build();

  stdout.writeln('✔ CPAL Table compiled: ${cpalTable.data.length} bytes (Checksum: 0x${cpalTable.checksum.toRadixString(16).padLeft(8, '0')})');
  assert(cpalTable.data.length % 2 == 0, 'CPAL table must be 2-byte word aligned');
  assert(cpalTable.tag == 'CPAL');

  // 2. Build COLRv0 Table
  final rules = PocketGullChromaticLibrary.getStandardRules();
  final colrGlyphs = rules.map((r) => ColrBaseGlyph(r.baseGlyphId, r.layers)).toList();
  final colrBuilder = ColrTableBuilder(colrGlyphs);
  final colrTable = colrBuilder.build();

  stdout.writeln('✔ COLR Table compiled: ${colrTable.data.length} bytes (Checksum: 0x${colrTable.checksum.toRadixString(16).padLeft(8, '0')})');
  assert(colrTable.data.length % 2 == 0, 'COLR table must be 2-byte word aligned');
  assert(colrTable.tag == 'COLR');

  final totalTableBytes = cpalTable.data.length + colrTable.data.length;
  stdout.writeln('📊 Total Chromatic Table Overhead: $totalTableBytes bytes (~${(totalTableBytes / 1024).toStringAsFixed(2)} KB)');
  stdout.writeln('🎉 All CPAL/COLR assertions passed successfully!');
}
