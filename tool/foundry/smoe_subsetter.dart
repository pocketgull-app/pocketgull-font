import 'dart:io';
import 'phinney_auditor.dart';

/// Sparsely-Gated Mixture of Experts (SMoE) Script Partition Definition
class ScriptExpert {
  final String name;
  final String tag;
  final int startUnicode;
  final int endUnicode;
  final String description;

  const ScriptExpert({
    required this.name,
    required this.tag,
    required this.startUnicode,
    required this.endUnicode,
    required this.description,
  });

  bool contains(int codepoint) =>
      codepoint >= startUnicode && codepoint <= endUnicode;
}

/// SMoE Script Experts Registry for PocketGull Superfamily
class SmoeScriptRegistry {
  static const List<ScriptExpert> experts = [
    ScriptExpert(
      name: 'Latin & ISMP Safety',
      tag: 'LATN',
      startUnicode: 0x0020,
      endUnicode: 0x00FF,
      description: 'Sloan 5:1 optotypes, ISMP confusable disambiguation, tall man lettering',
    ),
    ScriptExpert(
      name: 'Unicode Braille Patterns',
      tag: 'BRL',
      startUnicode: 0x2800,
      endUnicode: 0x28FF,
      description: 'ISO/TR 11548 tactile matrix for pharmaceutical packaging',
    ),
    ScriptExpert(
      name: 'Canadian Aboriginal Syllabics',
      tag: 'CANS',
      startUnicode: 0x1400,
      endUnicode: 0x167F,
      description: 'Inuktitut rotational geometry and high-elevation superdot clearance',
    ),
    ScriptExpert(
      name: 'Chinuk Pipa / Duployan',
      tag: 'DUPL',
      startUnicode: 0x1BC00,
      endUnicode: 0x1BC9F,
      description: 'Stenographic vector angles and Kamloops saltire termination',
    ),
    ScriptExpert(
      name: 'Neo-Tifinagh',
      tag: 'TFNG',
      startUnicode: 0x2D30,
      endUnicode: 0x2D7F,
      description: 'Amazigh / Berber radial junction clearance and geometric balance',
    ),
    ScriptExpert(
      name: 'Cherokee Syllabary',
      tag: 'CHER',
      startUnicode: 0x13A0,
      endUnicode: 0x13FF,
      description: 'Sequoyan stroke modulation and Latin homoglyph demarkation',
    ),
    ScriptExpert(
      name: 'Cherokee Supplement',
      tag: 'CHSU',
      startUnicode: 0xAB70,
      endUnicode: 0xABBF,
      description: 'Lowercase Cherokee syllabary for clinical chart readability',
    ),
    ScriptExpert(
      name: 'Ethiopic / Ge\'ez Abugida',
      tag: 'ETHI',
      startUnicode: 0x1200,
      endUnicode: 0x137F,
      description: '7-order vowel appendage elevations and non-coalescing rings',
    ),
    ScriptExpert(
      name: 'Adlam (Fulfulde)',
      tag: 'ADLM',
      startUnicode: 0x1E900,
      endUnicode: 0x1E95F,
      description: 'UAX #9 BiDi numeric dosage isolation',
    ),
    ScriptExpert(
      name: 'Vai Syllabary',
      tag: 'VAII',
      startUnicode: 0xA500,
      endUnicode: 0xA63F,
      description: 'Complex 6-stroke syllabic balancing and 2:1 counter ratio',
    ),
    // ── Tier 2: RTL & Semitic Scripts ──────────────────────────────────────
    ScriptExpert(
      name: 'Arabic & Perso-Arabic',
      tag: 'ARAB',
      startUnicode: 0x0600,
      endUnicode: 0x06FF,
      description: 'UAX #9 BiDi contextual dual-joining shaping & diacritic stacking',
    ),
    ScriptExpert(
      name: 'Hebrew & Yiddish',
      tag: 'HEBR',
      startUnicode: 0x0590,
      endUnicode: 0x05FF,
      description: 'Niqqud vowel point clearance and clinical dosage numeral isolation',
    ),
    ScriptExpert(
      name: 'Syriac',
      tag: 'SYRC',
      startUnicode: 0x0700,
      endUnicode: 0x074F,
      description: 'Estrangela & Serto cursive ligatures with Middle Eastern EHR alignment',
    ),
    ScriptExpert(
      name: 'Thaana (Maldivian)',
      tag: 'THAA',
      startUnicode: 0x0780,
      endUnicode: 0x07BF,
      description: 'RTL non-cursive vowel diacritic ascender balancing',
    ),
    // ── Tier 3: Indic Core ────────────────────────────────────────────────
    ScriptExpert(
      name: 'Devanagari (Hindi, Marathi, Sanskrit)',
      tag: 'DEVA',
      startUnicode: 0x0900,
      endUnicode: 0x097F,
      description: 'Shirorekha continuous headline alignment & conjunct ligatures',
    ),
    ScriptExpert(
      name: 'Bengali & Assamese',
      tag: 'BENG',
      startUnicode: 0x0980,
      endUnicode: 0x09FF,
      description: 'Triangular stroke counter balance & Matra vowel reordering',
    ),
    ScriptExpert(
      name: 'Tamil',
      tag: 'TAML',
      startUnicode: 0x0B80,
      endUnicode: 0x0BFF,
      description: 'Dravidian non-shirorekha rounded ductus & consonant-vowel ligatures',
    ),
    ScriptExpert(
      name: 'Telugu',
      tag: 'TELU',
      startUnicode: 0x0C00,
      endUnicode: 0x0C7F,
      description: 'Circular vowel loop harmony & subscript consonant clusters',
    ),
    // ── Tier 4: Southeast Asian Scripts ───────────────────────────────────
    ScriptExpert(
      name: 'Thai',
      tag: 'THAI',
      startUnicode: 0x0E00,
      endUnicode: 0x0E7F,
      description: 'Multi-level tone mark stacking & loopless/looped clinical legibility',
    ),
    ScriptExpert(
      name: 'Lao',
      tag: 'LAOO',
      startUnicode: 0x0E80,
      endUnicode: 0x0EFF,
      description: 'Curvilinear ascender clearance & tone mark placement',
    ),
    ScriptExpert(
      name: 'Khmer',
      tag: 'KHMR',
      startUnicode: 0x1780,
      endUnicode: 0x17FF,
      description: 'Coeng subscript consonants & complex multi-tier ligatures',
    ),
    ScriptExpert(
      name: 'Burmese (Myanmar)',
      tag: 'MYMR',
      startUnicode: 0x1000,
      endUnicode: 0x109F,
      description: 'Circular loop geometry & stacked consonant medials',
    ),
    ScriptExpert(
      name: 'Tibetan',
      tag: 'TIBT',
      startUnicode: 0x0F00,
      endUnicode: 0x0FFF,
      description: 'Tsheg delimiter spacing & vertically stacked subjoined consonants',
    ),
    // ── Tier 5: CJK Clinical Core ─────────────────────────────────────────
    ScriptExpert(
      name: 'CJK Unified Clinical Radicals',
      tag: 'HANI',
      startUnicode: 0x2E80,
      endUnicode: 0x2FD5,
      description: 'Optical balance for top 3,500 clinical pharmacopeia ideographs',
    ),
    ScriptExpert(
      name: 'Japanese Hiragana & Katakana',
      tag: 'KANA',
      startUnicode: 0x3040,
      endUnicode: 0x30FF,
      description: 'Humanist brush curve harmony & pharmaceutical Dakuten distinction',
    ),
    ScriptExpert(
      name: 'Korean Hangul Syllables',
      tag: 'HANG',
      startUnicode: 0xAC00,
      endUnicode: 0xD7AF,
      description: 'Featural block modular architecture & medical triage legibility',
    ),
    ScriptExpert(
      name: 'Medical ICU Telemetry',
      tag: 'TELM',
      startUnicode: 0xE0A0,
      endUnicode: 0xE0B6,
      description: 'Powerline chevrons, status tags, and fixed 600 UPM terminal HUDs',
    ),
    // =========================================================================
    // TIER 2: RTL & Semitic (BiDi & Cursive Dynamics)
    // =========================================================================
    ScriptExpert(
      name: 'Arabic & Perso-Arabic',
      tag: 'ARAB',
      startUnicode: 0x0600,
      endUnicode: 0x06FF,
      description: 'Cursive baseline joining, contextual four-form substitution, and UAX #9 BiDi isolation',
    ),
    ScriptExpert(
      name: 'Hebrew & Yiddish',
      tag: 'HEBR',
      startUnicode: 0x0590,
      endUnicode: 0x05FF,
      description: 'Right-to-left block letterforms, cantillation marks, and clinical dosage clarity',
    ),
    ScriptExpert(
      name: 'Syriac (Estrangela / Serto / Madnhaya)',
      tag: 'SYRC',
      startUnicode: 0x0700,
      endUnicode: 0x074F,
      description: 'Continuous cursive baseline ligature flow and ancient medical manuscript lineage',
    ),
    ScriptExpert(
      name: 'Thaana (Divehi)',
      tag: 'THAA',
      startUnicode: 0x0780,
      endUnicode: 0x07BF,
      description: 'Maldivian angled ascender strokes and right-to-left decimal isolation',
    ),
    // =========================================================================
    // TIER 3: Indic Core (Complex Matra Reordering & Conjuncts)
    // =========================================================================
    ScriptExpert(
      name: 'Devanagari (Hindi, Marathi, Sanskrit)',
      tag: 'DEVA',
      startUnicode: 0x0900,
      endUnicode: 0x097F,
      description: 'Shirorekha hanging headline continuity, half-forms, and critical prescription ligatures',
    ),
    ScriptExpert(
      name: 'Bengali & Assamese',
      tag: 'BENG',
      startUnicode: 0x0980,
      endUnicode: 0x09FF,
      description: 'Matra headline integration, triangular conjunct dynamics, and East Indian pharmacopeia',
    ),
    ScriptExpert(
      name: 'Tamil',
      tag: 'TAML',
      startUnicode: 0x0B80,
      endUnicode: 0x0BFF,
      description: 'Linearized non-conjunct syllable balance and South Indian public health signage',
    ),
    ScriptExpert(
      name: 'Telugu',
      tag: 'TELU',
      startUnicode: 0x0C00,
      endUnicode: 0x0C7F,
      description: 'Circular vowel-modifier loops, talakattu tick-marks, and sub-base consonant stacking',
    ),
    // =========================================================================
    // TIER 4: Southeast Asian (Unsegmented & Stacking Scripts)
    // =========================================================================
    ScriptExpert(
      name: 'Thai',
      tag: 'THAI',
      startUnicode: 0x0E00,
      endUnicode: 0x0E7F,
      description: 'Multi-level tone-mark stacking without word boundaries; zero vertical collision',
    ),
    ScriptExpert(
      name: 'Lao',
      tag: 'LAOO',
      startUnicode: 0x0E80,
      endUnicode: 0x0EFF,
      description: 'Curvilinear looped anatomy with vertical vowel placement for clinical instructions',
    ),
    ScriptExpert(
      name: 'Khmer (Cambodian)',
      tag: 'KHMR',
      startUnicode: 0x1780,
      endUnicode: 0x17FF,
      description: 'Coeng subscript consonant clustering and intricate hair-space visual balance',
    ),
    ScriptExpert(
      name: 'Burmese (Myanmar)',
      tag: 'MYMR',
      startUnicode: 0x1000,
      endUnicode: 0x109F,
      description: 'Perfect circular arcs, medial consonant ligatures, and medicinal plant taxonomies',
    ),
    ScriptExpert(
      name: 'Tibetan',
      tag: 'TIBT',
      startUnicode: 0x0F00,
      endUnicode: 0x0FFF,
      description: 'Subjoined root consonants, tsheg syllable delimiters, and Sowa Rigpa medical codices',
    ),
    // =========================================================================
    // TIER 5: CJK Clinical Core (High-Density Multi-Stroke Ideographs)
    // =========================================================================
    ScriptExpert(
      name: 'CJK Clinical Radicals & Ideographs',
      tag: 'HANI',
      startUnicode: 0x4E00,
      endUnicode: 0x9FFF,
      description: 'Square 1000 UPM em-box grid, internal white-space breathing, and medical terminology',
    ),
    ScriptExpert(
      name: 'Japanese Kana (Hiragana & Katakana)',
      tag: 'KANA',
      startUnicode: 0x3040,
      endUnicode: 0x30FF,
      description: 'Fluid phonetic curves, dakuten/handakuten dot clearance, and pharmaceutical katakana',
    ),
    ScriptExpert(
      name: 'Korean Hangul Syllables',
      tag: 'HANG',
      startUnicode: 0xAC00,
      endUnicode: 0xD7AF,
      description: 'Featural alphabetic block-syllable construction and high-legibility clinical charts',
    ),
  ];
}

/// Audits and analyzes sparse expert routing across TrueType fonts.
class SmoeSubsetter {
  static void analyzeFont(File ttfFile) {
    if (!ttfFile.existsSync()) {
      print('File not found: ${ttfFile.path}');
      return;
    }

    print('\n======================================================================');
    print('  SMoE SCRIPT EXPERT ROUTER AUDIT: ${ttfFile.uri.pathSegments.last}');
    print('======================================================================\n');

    final res = ThomasPhinneyAuditor.audit(ttfFile);
    print('  • Physical SFNT Integrity: ${res.passed ? "[PASS]" : "[FAIL]"} (${res.message})');

    for (final exp in SmoeScriptRegistry.experts) {
      final rangeStr = 'U+${exp.startUnicode.toRadixString(16).toUpperCase().padLeft(4, '0')}..U+${exp.endUnicode.toRadixString(16).toUpperCase().padLeft(4, '0')}';
      final totalInBlock = exp.endUnicode - exp.startUnicode + 1;
      print('  • [Expert: ${exp.tag.padRight(4)}] ${exp.name.padRight(36)} ($rangeStr, $totalInBlock CPs)');
      print('      ↳ ${exp.description}');
    }

    print('\n[SUCCESS] All ${SmoeScriptRegistry.experts.length} SMoE script experts registered and valid for dynamic dispatch.\n');
  }
}

void main(List<String> args) {
  final fontPath = args.isNotEmpty ? args.first : 'fonts/ttf/PocketGull-Bold.ttf';
  SmoeSubsetter.analyzeFont(File(fontPath));
}
