
/// Pure Dart 3.11 Clinical Arabic Positional Specification.
/// Maps base Arabic/Persian characters to authentic positional variants (.init, .medi, .fina, .isol)
/// according to classical Arabic joining types (Dual-joining vs Right-joining).
class ArabicGlyphSpec {
  final int codepoint;
  final String baseName;
  final String joiningType; // 'D' (Dual), 'R' (Right), 'U' (Non-joining)
  final String? initName;
  final String? mediName;
  final String? finaName;
  final String? isolName;

  const ArabicGlyphSpec({
    required this.codepoint,
    required this.baseName,
    required this.joiningType,
    this.initName,
    this.mediName,
    this.finaName,
    this.isolName,
  });
}

const clinicalArabicSpecs = <ArabicGlyphSpec>[
  // Right-joining letters (only isolated and final forms)
  ArabicGlyphSpec(codepoint: 0x0627, baseName: 'uni0627', joiningType: 'R', finaName: 'uni0627.fina', isolName: 'uni0627'),
  ArabicGlyphSpec(codepoint: 0x062F, baseName: 'uni062F', joiningType: 'R', finaName: 'uni062F.fina', isolName: 'uni062F'),
  ArabicGlyphSpec(codepoint: 0x0630, baseName: 'uni0630', joiningType: 'R', finaName: 'uni0630.fina', isolName: 'uni0630'),
  ArabicGlyphSpec(codepoint: 0x0631, baseName: 'uni0631', joiningType: 'R', finaName: 'uni0631.fina', isolName: 'uni0631'),
  ArabicGlyphSpec(codepoint: 0x0632, baseName: 'uni0632', joiningType: 'R', finaName: 'uni0632.fina', isolName: 'uni0632'),
  ArabicGlyphSpec(codepoint: 0x0698, baseName: 'uni0698', joiningType: 'R', finaName: 'uni0698.fina', isolName: 'uni0698'), // Zhe (Persian)
  ArabicGlyphSpec(codepoint: 0x0648, baseName: 'uni0648', joiningType: 'R', finaName: 'uni0648.fina', isolName: 'uni0648'),
  ArabicGlyphSpec(codepoint: 0x0629, baseName: 'uni0629', joiningType: 'R', finaName: 'uni0629.fina', isolName: 'uni0629'), // Teh Marbuta

  // Dual-joining letters (all 4 forms: init, medi, fina, isol)
  ArabicGlyphSpec(codepoint: 0x0628, baseName: 'uni0628', joiningType: 'D', initName: 'uni0628.init', mediName: 'uni0628.medi', finaName: 'uni0628.fina', isolName: 'uni0628'),
  ArabicGlyphSpec(codepoint: 0x067E, baseName: 'uni067E', joiningType: 'D', initName: 'uni067E.init', mediName: 'uni067E.medi', finaName: 'uni067E.fina', isolName: 'uni067E'), // Peh (Persian)
  ArabicGlyphSpec(codepoint: 0x062A, baseName: 'uni062A', joiningType: 'D', initName: 'uni062A.init', mediName: 'uni062A.medi', finaName: 'uni062A.fina', isolName: 'uni062A'),
  ArabicGlyphSpec(codepoint: 0x062C, baseName: 'uni062C', joiningType: 'D', initName: 'uni062C.init', mediName: 'uni062C.medi', finaName: 'uni062C.fina', isolName: 'uni062C'),
  ArabicGlyphSpec(codepoint: 0x062D, baseName: 'uni062D', joiningType: 'D', initName: 'uni062D.init', mediName: 'uni062D.medi', finaName: 'uni062D.fina', isolName: 'uni062D'),
  ArabicGlyphSpec(codepoint: 0x062E, baseName: 'uni062E', joiningType: 'D', initName: 'uni062E.init', mediName: 'uni062E.medi', finaName: 'uni062E.fina', isolName: 'uni062E'),
  ArabicGlyphSpec(codepoint: 0x0633, baseName: 'uni0633', joiningType: 'D', initName: 'uni0633.init', mediName: 'uni0633.medi', finaName: 'uni0633.fina', isolName: 'uni0633'),
  ArabicGlyphSpec(codepoint: 0x0634, baseName: 'uni0634', joiningType: 'D', initName: 'uni0634.init', mediName: 'uni0634.medi', finaName: 'uni0634.fina', isolName: 'uni0634'),
  ArabicGlyphSpec(codepoint: 0x0635, baseName: 'uni0635', joiningType: 'D', initName: 'uni0635.init', mediName: 'uni0635.medi', finaName: 'uni0635.fina', isolName: 'uni0635'),
  ArabicGlyphSpec(codepoint: 0x0637, baseName: 'uni0637', joiningType: 'D', initName: 'uni0637.init', mediName: 'uni0637.medi', finaName: 'uni0637.fina', isolName: 'uni0637'),
  ArabicGlyphSpec(codepoint: 0x0639, baseName: 'uni0639', joiningType: 'D', initName: 'uni0639.init', mediName: 'uni0639.medi', finaName: 'uni0639.fina', isolName: 'uni0639'),
  ArabicGlyphSpec(codepoint: 0x063A, baseName: 'uni063A', joiningType: 'D', initName: 'uni063A.init', mediName: 'uni063A.medi', finaName: 'uni063A.fina', isolName: 'uni063A'),
  ArabicGlyphSpec(codepoint: 0x0641, baseName: 'uni0641', joiningType: 'D', initName: 'uni0641.init', mediName: 'uni0641.medi', finaName: 'uni0641.fina', isolName: 'uni0641'),
  ArabicGlyphSpec(codepoint: 0x0643, baseName: 'uni0643', joiningType: 'D', initName: 'uni0643.init', mediName: 'uni0643.medi', finaName: 'uni0643.fina', isolName: 'uni0643'),
  ArabicGlyphSpec(codepoint: 0x06AF, baseName: 'uni06AF', joiningType: 'D', initName: 'uni06AF.init', mediName: 'uni06AF.medi', finaName: 'uni06AF.fina', isolName: 'uni06AF'), // Gaf (Persian)
  ArabicGlyphSpec(codepoint: 0x0644, baseName: 'uni0644', joiningType: 'D', initName: 'uni0644.init', mediName: 'uni0644.medi', finaName: 'uni0644.fina', isolName: 'uni0644'),
  ArabicGlyphSpec(codepoint: 0x0645, baseName: 'uni0645', joiningType: 'D', initName: 'uni0645.init', mediName: 'uni0645.medi', finaName: 'uni0645.fina', isolName: 'uni0645'),
  ArabicGlyphSpec(codepoint: 0x0646, baseName: 'uni0646', joiningType: 'D', initName: 'uni0646.init', mediName: 'uni0646.medi', finaName: 'uni0646.fina', isolName: 'uni0646'),
  ArabicGlyphSpec(codepoint: 0x0647, baseName: 'uni0647', joiningType: 'D', initName: 'uni0647.init', mediName: 'uni0647.medi', finaName: 'uni0647.fina', isolName: 'uni0647'),
  ArabicGlyphSpec(codepoint: 0x064A, baseName: 'uni064A', joiningType: 'D', initName: 'uni064A.init', mediName: 'uni064A.medi', finaName: 'uni064A.fina', isolName: 'uni064A'),
  ArabicGlyphSpec(codepoint: 0x06CC, baseName: 'uni06CC', joiningType: 'D', initName: 'uni06CC.init', mediName: 'uni06CC.medi', finaName: 'uni06CC.fina', isolName: 'uni06CC'), // Farsi Yeh
  ArabicGlyphSpec(codepoint: 0x0626, baseName: 'uni0626', joiningType: 'D', initName: 'uni0626.init', mediName: 'uni0626.medi', finaName: 'uni0626.fina', isolName: 'uni0626'),
];

void main() {
  print('Clinical Arabic Positional Mapping Matrix: \ letters defined.');
  var totalVariants = 0;
  for (final s in clinicalArabicSpecs) {
    var v = 1; // isol/base
    if (s.initName != null) v++;
    if (s.mediName != null) v++;
    if (s.finaName != null) v++;
    totalVariants += v;
  }
  print('Total positional glyphs to generate and wire: ' + totalVariants.toString());
}
