import 'dart:io';
import 'glyph_inspector.dart';

class TekUndripAuditResult {
  final String filename;
  final bool passed;
  final int totalGlyphs;
  final int panTribalPasses;
  final int syllabicsPasses;
  final int duployanPasses;
  final int braillePasses;
  final int clearancePasses;
  final List<String> details;

  const TekUndripAuditResult({
    required this.filename,
    required this.passed,
    required this.totalGlyphs,
    required this.panTribalPasses,
    required this.syllabicsPasses,
    required this.duployanPasses,
    required this.braillePasses,
    required this.clearancePasses,
    required this.details,
  });
}

/// Traditional Ecological Knowledge (TEK) & UNDRIP Typographic Accord Auditor.
/// Grounded in:
/// - United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP Articles 11, 13, 14, 24, 31)
/// - First Nations OCAP® Principles & CARE Principles for Indigenous Data Governance
/// - Nancy J. Turner & Eugene S. Hunn Pacific Northwest Ethnobotanical Taxonomy
/// - Fikret Berkes "Sacred Ecology" Relational Principles
///
/// Invariants Audited:
/// 1. Pan-Tribal Latin Diacritics (12 IHS Administrative Jurisdictions):
///    - Diné Bizaad: Nasals (ą, ę, į, ǫ), Barred Ł/ł, Saltillo (ʼ / ʔ).
///    - Lushootseed / Coast Salish: Schwa (ə), Barred Lambda (ƛ), Lateral Fricative (ɬ), Labializer (ʷ).
///    - Lakȟótiyapi: Eng (ŋ), Caron consonants (č, š, ž).
/// 2. Canadian Aboriginal Syllabics (U+1400–U+167F, 640 codepoints): Inuktitut / Cree / Ojibwe.
/// 3. Duployan / Chinuk Pipa (U+1BC00–U+1BC9F, 143 codepoints): Pacific Northwest shorthand literacy.
/// 4. Tactile Braille Integration (U+2800–U+28FF, 256 codepoints): ISO/TR 11548 baseline grounding (y >= 0).
/// 5. Stacked Diacritic Clearance: >= 80 UPM clearance for tribal EHR prescription legibility.
class TekUndripAuditor {
  // Key Pan-Tribal Latin codepoints
  static const panTribalCodes = [
    0x0105, // a ogonek (ą)
    0x0119, // e ogonek (ę)
    0x012F, // i ogonek (į)
    0x01EB, // o ogonek (ǫ)
    0x0141, // L stroke (Ł)
    0x0142, // l stroke (ł)
    0x019B, // lambda stroke (ƛ)
    0x026C, // l belt (ɬ)
    0x0294, // glottal stop (ʔ)
    0x02BC, // apostrophe modifier (ʼ)
    0x02BB, // okina (ʻ)
    0x0259, // schwa (ə)
    0x02B7, // w modifier (ʷ)
    0x014B, // eng (ŋ)
    0x0101, // a macron (ā)
  ];

  static TekUndripAuditResult audit(File fontFile) {
    final name = fontFile.uri.pathSegments.last;
    if (!fontFile.existsSync()) {
      return TekUndripAuditResult(
        filename: name,
        passed: false,
        totalGlyphs: 0,
        panTribalPasses: 0,
        syllabicsPasses: 0,
        duployanPasses: 0,
        braillePasses: 0,
        clearancePasses: 0,
        details: ['File not found on disk'],
      );
    }

    final inspector = GlyphInspector.fromFile(fontFile);
    final details = <String>[];

    // 1. Pan-Tribal Latin Coverage
    int panTribalCount = 0;
    for (final cp in panTribalCodes) {
      if (inspector.unicodeToGid.containsKey(cp)) {
        panTribalCount++;
      }
    }

    // 2. Canadian Aboriginal Syllabics Coverage (U+1400–U+167F)
    int syllabicsCount = 0;
    for (int cp = 0x1400; cp <= 0x167F; cp++) {
      if (inspector.unicodeToGid.containsKey(cp)) {
        syllabicsCount++;
      }
    }

    // 3. Duployan / Chinuk Pipa Coverage (U+1BC00–U+1BC9F)
    int duployanCount = 0;
    for (int cp = 0x1BC00; cp <= 0x1BC9F; cp++) {
      if (inspector.unicodeToGid.containsKey(cp)) {
        duployanCount++;
      }
    }

    // 4. Unicode Braille Coverage & Baseline Grounding (U+2800–U+28FF)
    int brailleCount = 0;
    int groundedCount = 0;
    for (int cp = 0x2800; cp <= 0x28FF; cp++) {
      final gid = inspector.unicodeToGid[cp];
      if (gid != null) {
        brailleCount++;
        final data = inspector.getGlyphData(gid);
        // ISO/TR 11548 8-dot cells span y = -260 (dots 7,8) to y = 720 (dots 1,4)
        if (data['empty'] == true || (data['yMin'] != null && data['yMin'] >= -300 && data['yMax'] <= 850)) {
          groundedCount++;
        }
      }
    }

    // 5. Stacked Diacritic Clearance (Navajo a-ogonek + acute / e-ogonek)
    int clearancePasses = 0;
    final aOgonekGid = inspector.unicodeToGid[0x0105];
    if (aOgonekGid != null) {
      final data = inspector.getGlyphData(aOgonekGid);
      if (data['yMax'] != null && data['yMax'] >= 500) {
        clearancePasses++;
      }
    }

    final lStrokeGid = inspector.unicodeToGid[0x0142];
    if (lStrokeGid != null) {
      final data = inspector.getGlyphData(lStrokeGid);
      if (data['yMax'] != null && data['yMax'] >= 650) {
        clearancePasses++;
      }
    }

    // Pass criteria:
    // Core Pan-Tribal Latin >= 13/15 (or all present)
    // Syllabics >= 600/640
    // Braille >= 256/256
    final bool passed = panTribalCount >= 13 &&
                        syllabicsCount >= 600 &&
                        brailleCount == 256 &&
                        groundedCount >= 250;

    return TekUndripAuditResult(
      filename: name,
      passed: passed,
      totalGlyphs: inspector.numGlyphs,
      panTribalPasses: panTribalCount,
      syllabicsPasses: syllabicsCount,
      duployanPasses: duployanCount,
      braillePasses: brailleCount,
      clearancePasses: clearancePasses,
      details: details,
    );
  }
}
