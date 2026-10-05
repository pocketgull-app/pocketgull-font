import 'dart:io';
import '../tool/foundry/sfnt_transformer.dart';
import '../tool/foundry/phinney_auditor.dart';

void main() {
  final dir = Directory('fonts/ttf');
  final ttfs = dir.listSync().whereType<File>().where((f) => f.path.endsWith('.ttf')).toList();
  ttfs.sort((a, b) => a.path.compareTo(b.path));
  
  print('======================================================================');
  print('  POCKETGULL FOUNDRY: SFNT 2-BYTE WORD ALIGNMENT & BIT-7 MASKING');
  print('======================================================================\n');
  print('Processing ${ttfs.length} TTF files in fonts/ttf/...\n');
  
  int totalPassed = 0;
  for (final ttf in ttfs) {
    final name = ttf.uri.pathSegments.last;
    stdout.write('  • Realigning $name ... ');
    try {
      SfntTransformer.transformFont(inputFile: ttf);
      final res = ThomasPhinneyAuditor.audit(ttf);
      if (res.passed) {
        print('[PASS: 0 odd loca, 0 bad flags]');
        totalPassed++;
      } else {
        print('[FAIL: ${res.oddLocaOffsets} odd loca, ${res.badBit7Flags} bad flags]');
      }
    } catch (e) {
      print('[ERROR: $e]');
    }
  }
  
  print('\nSummary: $totalPassed / ${ttfs.length} fonts 100% W3C OTS valid.');
}
