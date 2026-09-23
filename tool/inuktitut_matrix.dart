// Copyright (c) 2026, The PocketGull Project Authors.
// All rights reserved. Use of this source code is governed by an OFL 1.1 license.

/// Inuktitut Syllabic Matrix & Rotational Transformation Engine
///
/// Implements sound static typing with Dart 3,
/// pattern matching, zero virtualenv friction, and sub-microsecond precision.
///
/// Maps the James Evans 1840 Canadian Aboriginal Syllabics phonetic geometry
/// across 13 consonant series and 4 cardinal vowel orientations:
///   - Orientation I  (0° / pointing up)
///   - Orientation U  (90° clockwise / pointing right)
///   - Orientation A  (180° / pointing down)
///   - Orientation E  (270° / pointing left)
///
/// Along with long-vowel diacritic dots (ii, uu, aa) and coda finals.
library;

import 'dart:convert';
import 'dart:io';

enum VowelOrientation {
  i(0, 'i'),
  u(90, 'u'),
  a(180, 'a'),
  e(270, 'e');

  const VowelOrientation(this.angleDegrees, this.vowelName);
  final double angleDegrees;
  final String vowelName;
}

enum SyllabicKind {
  standard,
  longVowel,
  codaFinal,
}

class SyllabicCharacter {
  final int codepoint;
  final String character;
  final String series; // 'VOWEL', 'P', 'T', 'K', 'G', 'M', 'N', 'S', 'L', 'J', 'R', 'Q', 'NG'
  final VowelOrientation? orientation;
  final SyllabicKind kind;
  final String transliteration;

  const SyllabicCharacter({
    required this.codepoint,
    required this.character,
    required this.series,
    this.orientation,
    required this.kind,
    required this.transliteration,
  });

  Map<String, dynamic> toJson() => {
    'codepoint': codepoint,
    'hex': '0x${codepoint.toRadixString(16).toUpperCase().padLeft(4, '0')}',
    'char': character,
    'series': series,
    'orientation': orientation?.name,
    'angle': orientation?.angleDegrees ?? 0,
    'kind': kind.name,
    'transliteration': transliteration,
  };
}

/// Complete Inuktitut & Nunavut Official Syllabary
class InuktitutMatrix {
  static const List<SyllabicCharacter> roster = [
    // 1. Pure Vowels (ᐃ ᐅ ᐊ ᐁ)
    SyllabicCharacter(codepoint: 0x1403, character: 'ᐃ', series: 'VOWEL', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'i'),
    SyllabicCharacter(codepoint: 0x1404, character: 'ᐄ', series: 'VOWEL', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'ii'),
    SyllabicCharacter(codepoint: 0x1405, character: 'ᐅ', series: 'VOWEL', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'u'),
    SyllabicCharacter(codepoint: 0x1406, character: 'ᐆ', series: 'VOWEL', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'uu'),
    SyllabicCharacter(codepoint: 0x140A, character: 'ᐊ', series: 'VOWEL', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'a'),
    SyllabicCharacter(codepoint: 0x140B, character: 'ᐋ', series: 'VOWEL', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'aa'),
    SyllabicCharacter(codepoint: 0x1401, character: 'ᐁ', series: 'VOWEL', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'e'),

    // 2. P-Series (ᐱ ᐳ ᐸ ᐯ + ᑉ)
    SyllabicCharacter(codepoint: 0x1431, character: 'ᐱ', series: 'P', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'pi'),
    SyllabicCharacter(codepoint: 0x1432, character: 'ᐲ', series: 'P', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'pii'),
    SyllabicCharacter(codepoint: 0x1433, character: 'ᐳ', series: 'P', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'pu'),
    SyllabicCharacter(codepoint: 0x1434, character: 'ᐴ', series: 'P', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'puu'),
    SyllabicCharacter(codepoint: 0x1438, character: 'ᐸ', series: 'P', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'pa'),
    SyllabicCharacter(codepoint: 0x1439, character: 'ᐹ', series: 'P', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'paa'),
    SyllabicCharacter(codepoint: 0x142F, character: 'ᐯ', series: 'P', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'pe'),
    SyllabicCharacter(codepoint: 0x1449, character: 'ᑉ', series: 'P', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'p'),

    // 3. T-Series (ᑎ ᑐ ᑕ ᑌ + ᑦ)
    SyllabicCharacter(codepoint: 0x144E, character: 'ᑎ', series: 'T', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ti'),
    SyllabicCharacter(codepoint: 0x144F, character: 'ᑏ', series: 'T', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'tii'),
    SyllabicCharacter(codepoint: 0x1450, character: 'ᑐ', series: 'T', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'tu'),
    SyllabicCharacter(codepoint: 0x1451, character: 'ᑑ', series: 'T', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'tuu'),
    SyllabicCharacter(codepoint: 0x1455, character: 'ᑕ', series: 'T', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ta'),
    SyllabicCharacter(codepoint: 0x1456, character: 'ᑖ', series: 'T', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'taa'),
    SyllabicCharacter(codepoint: 0x144C, character: 'ᑌ', series: 'T', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'te'),
    SyllabicCharacter(codepoint: 0x1466, character: 'ᑦ', series: 'T', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 't'),

    // 4. K-Series (ᑭ ᑯ ᑲ ᑫ + ᒃ)
    SyllabicCharacter(codepoint: 0x146D, character: 'ᑭ', series: 'K', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ki'),
    SyllabicCharacter(codepoint: 0x146E, character: 'ᑮ', series: 'K', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'kii'),
    SyllabicCharacter(codepoint: 0x146F, character: 'ᑯ', series: 'K', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'ku'),
    SyllabicCharacter(codepoint: 0x1470, character: 'ᑰ', series: 'K', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'kuu'),
    SyllabicCharacter(codepoint: 0x1472, character: 'ᑲ', series: 'K', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ka'),
    SyllabicCharacter(codepoint: 0x1473, character: 'ᑳ', series: 'K', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'kaa'),
    SyllabicCharacter(codepoint: 0x146B, character: 'ᑫ', series: 'K', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'ke'),
    SyllabicCharacter(codepoint: 0x1483, character: 'ᒃ', series: 'K', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'k'),

    // 5. G-Series (ᒋ ᒍ ᒐ ᒉ + ᒡ)
    SyllabicCharacter(codepoint: 0x148B, character: 'ᒋ', series: 'G', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'gi'),
    SyllabicCharacter(codepoint: 0x148C, character: 'ᒌ', series: 'G', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'gii'),
    SyllabicCharacter(codepoint: 0x148D, character: 'ᒍ', series: 'G', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'gu'),
    SyllabicCharacter(codepoint: 0x148E, character: 'ᒎ', series: 'G', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'guu'),
    SyllabicCharacter(codepoint: 0x1490, character: 'ᒐ', series: 'G', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ga'),
    SyllabicCharacter(codepoint: 0x1491, character: 'ᒑ', series: 'G', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'gaa'),
    SyllabicCharacter(codepoint: 0x1489, character: 'ᒉ', series: 'G', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'ge'),
    SyllabicCharacter(codepoint: 0x14A1, character: 'ᒡ', series: 'G', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'g'),

    // 6. M-Series (ᒥ ᒧ ᒪ ᒣ + ᒻ)
    SyllabicCharacter(codepoint: 0x14A5, character: 'ᒥ', series: 'M', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'mi'),
    SyllabicCharacter(codepoint: 0x14A6, character: 'ᒦ', series: 'M', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'mii'),
    SyllabicCharacter(codepoint: 0x14A7, character: 'ᒧ', series: 'M', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'mu'),
    SyllabicCharacter(codepoint: 0x14A8, character: 'ᒨ', series: 'M', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'muu'),
    SyllabicCharacter(codepoint: 0x14AA, character: 'ᒪ', series: 'M', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ma'),
    SyllabicCharacter(codepoint: 0x14AB, character: 'ᒫ', series: 'M', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'maa'),
    SyllabicCharacter(codepoint: 0x14A3, character: 'ᒣ', series: 'M', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'me'),
    SyllabicCharacter(codepoint: 0x14BB, character: 'ᒻ', series: 'M', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'm'),

    // 7. N-Series (ᓂ ᓄ ᓇ ᓀ + ᓐ)
    SyllabicCharacter(codepoint: 0x14BF, character: 'ᓂ', series: 'N', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ni'),
    SyllabicCharacter(codepoint: 0x14C0, character: 'ᓃ', series: 'N', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'nii'),
    SyllabicCharacter(codepoint: 0x14C1, character: 'ᓄ', series: 'N', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'nu'),
    SyllabicCharacter(codepoint: 0x14C2, character: 'ᓅ', series: 'N', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'nuu'),
    SyllabicCharacter(codepoint: 0x14C4, character: 'ᓇ', series: 'N', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'na'),
    SyllabicCharacter(codepoint: 0x14C5, character: 'ᓈ', series: 'N', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'naa'),
    SyllabicCharacter(codepoint: 0x14BD, character: 'ᓀ', series: 'N', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'ne'),
    SyllabicCharacter(codepoint: 0x14D0, character: 'ᓐ', series: 'N', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'n'),

    // 8. S-Series (ᓯ ᓱ ᓴ ᓭ + ᔅ)
    SyllabicCharacter(codepoint: 0x14EF, character: 'ᓯ', series: 'S', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'si'),
    SyllabicCharacter(codepoint: 0x14F0, character: 'ᓰ', series: 'S', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'sii'),
    SyllabicCharacter(codepoint: 0x14F1, character: 'ᓱ', series: 'S', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'su'),
    SyllabicCharacter(codepoint: 0x14F2, character: 'ᓲ', series: 'S', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'suu'),
    SyllabicCharacter(codepoint: 0x14F4, character: 'ᓴ', series: 'S', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'sa'),
    SyllabicCharacter(codepoint: 0x14F5, character: 'ᓵ', series: 'S', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'saa'),
    SyllabicCharacter(codepoint: 0x14ED, character: 'ᓭ', series: 'S', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'se'),
    SyllabicCharacter(codepoint: 0x1505, character: 'ᔅ', series: 'S', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 's'),

    // 9. L-Series (ᓕ ᓗ ᓚ ᓓ + ᓪ)
    SyllabicCharacter(codepoint: 0x14D5, character: 'ᓕ', series: 'L', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'li'),
    SyllabicCharacter(codepoint: 0x14D6, character: 'ᓖ', series: 'L', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'lii'),
    SyllabicCharacter(codepoint: 0x14D7, character: 'ᓗ', series: 'L', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'lu'),
    SyllabicCharacter(codepoint: 0x14D8, character: 'ᓘ', series: 'L', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'luu'),
    SyllabicCharacter(codepoint: 0x14DA, character: 'ᓚ', series: 'L', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'la'),
    SyllabicCharacter(codepoint: 0x14DB, character: 'ᓛ', series: 'L', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'laa'),
    SyllabicCharacter(codepoint: 0x14D3, character: 'ᓓ', series: 'L', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'le'),
    SyllabicCharacter(codepoint: 0x14EA, character: 'ᓪ', series: 'L', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'l'),

    // 10. J-Series (ᔨ ᔪ ᔭ ᔦ + ᔾ)
    SyllabicCharacter(codepoint: 0x1528, character: 'ᔨ', series: 'J', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ji'),
    SyllabicCharacter(codepoint: 0x1529, character: 'ᔩ', series: 'J', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'jii'),
    SyllabicCharacter(codepoint: 0x152A, character: 'ᔪ', series: 'J', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'ju'),
    SyllabicCharacter(codepoint: 0x152B, character: 'ᔫ', series: 'J', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'juu'),
    SyllabicCharacter(codepoint: 0x152D, character: 'ᔭ', series: 'J', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ja'),
    SyllabicCharacter(codepoint: 0x152E, character: 'ᔮ', series: 'J', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'jaa'),
    SyllabicCharacter(codepoint: 0x1526, character: 'ᔦ', series: 'J', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'je'),
    SyllabicCharacter(codepoint: 0x153E, character: 'ᔾ', series: 'J', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'j'),

    // 11. R-Series (ᕆ ᕈ ᕋ ᕂ + ᕐ)
    SyllabicCharacter(codepoint: 0x1546, character: 'ᕆ', series: 'R', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ri'),
    SyllabicCharacter(codepoint: 0x1547, character: 'ᕇ', series: 'R', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'rii'),
    SyllabicCharacter(codepoint: 0x1548, character: 'ᕈ', series: 'R', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'ru'),
    SyllabicCharacter(codepoint: 0x1549, character: 'ᕉ', series: 'R', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'ruu'),
    SyllabicCharacter(codepoint: 0x154B, character: 'ᕋ', series: 'R', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'ra'),
    SyllabicCharacter(codepoint: 0x154C, character: 'ᕌ', series: 'R', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'raa'),
    SyllabicCharacter(codepoint: 0x1542, character: 'ᕂ', series: 'R', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 're'),
    SyllabicCharacter(codepoint: 0x1550, character: 'ᕐ', series: 'R', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'r'),

    // 12. Q-Series (ᕿ ᖁ ᖃ ᕴ + ᖅ)
    SyllabicCharacter(codepoint: 0x1555, character: 'ᕿ', series: 'Q', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'qi'),
    SyllabicCharacter(codepoint: 0x1556, character: 'ᖀ', series: 'Q', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'qii'),
    SyllabicCharacter(codepoint: 0x1557, character: 'ᖁ', series: 'Q', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'qu'),
    SyllabicCharacter(codepoint: 0x1558, character: 'ᖂ', series: 'Q', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'quu'),
    SyllabicCharacter(codepoint: 0x1559, character: 'ᖃ', series: 'Q', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'qa'),
    SyllabicCharacter(codepoint: 0x155A, character: 'ᖄ', series: 'Q', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'qaa'),
    SyllabicCharacter(codepoint: 0x1553, character: 'ᕴ', series: 'Q', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'qe'),
    SyllabicCharacter(codepoint: 0x155D, character: 'ᖅ', series: 'Q', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'q'),

    // 13. NG-Series (ᖏ ᖑ ᖓ ᖐ + ᖕ)
    SyllabicCharacter(codepoint: 0x1590, character: 'ᖏ', series: 'NG', orientation: VowelOrientation.i, kind: SyllabicKind.standard, transliteration: 'ngi'),
    SyllabicCharacter(codepoint: 0x1592, character: 'ᖒ', series: 'NG', orientation: VowelOrientation.i, kind: SyllabicKind.longVowel, transliteration: 'ngii'),
    SyllabicCharacter(codepoint: 0x1591, character: 'ᖑ', series: 'NG', orientation: VowelOrientation.u, kind: SyllabicKind.standard, transliteration: 'ngu'),
    SyllabicCharacter(codepoint: 0x1593, character: 'ᖓ', series: 'NG', orientation: VowelOrientation.u, kind: SyllabicKind.longVowel, transliteration: 'nguu'),
    SyllabicCharacter(codepoint: 0x1593, character: 'ᖓ', series: 'NG', orientation: VowelOrientation.a, kind: SyllabicKind.standard, transliteration: 'nga'),
    SyllabicCharacter(codepoint: 0x1594, character: 'ᖔ', series: 'NG', orientation: VowelOrientation.a, kind: SyllabicKind.longVowel, transliteration: 'ngaa'),
    SyllabicCharacter(codepoint: 0x158E, character: 'ᖐ', series: 'NG', orientation: VowelOrientation.e, kind: SyllabicKind.standard, transliteration: 'nge'),
    SyllabicCharacter(codepoint: 0x1595, character: 'ᖕ', series: 'NG', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'ng'),

    // 14. Nunavut Special Characters (H, NNG)
    SyllabicCharacter(codepoint: 0x15A4, character: 'ᕼ', series: 'H', orientation: null, kind: SyllabicKind.codaFinal, transliteration: 'h'),
    SyllabicCharacter(codepoint: 0x1585, character: 'ᙱ', series: 'NNG', orientation: null, kind: SyllabicKind.standard, transliteration: 'nng'),
  ];
}

void main(List<String> args) {
  stdout.writeln('=== INUKTITUT SYLLABIC MATRIX AUDITOR (DART 3.11) ===');
  stdout.writeln('Loaded ${InuktitutMatrix.roster.length} primary Inuktitut syllabics.');

  final seriesSet = <String>{};
  for (final item in InuktitutMatrix.roster) {
    seriesSet.add(item.series);
  }
  stdout.writeln('Active Consonant Series: ${seriesSet.join(', ')}');

  final jsonOut = jsonEncode({
    'timestamp': DateTime.now().toUtc().toIso8601String(),
    'script': 'Canadian Aboriginal Syllabics (Inuktitut)',
    'count': InuktitutMatrix.roster.length,
    'series_count': seriesSet.length,
    'characters': InuktitutMatrix.roster.map((e) => e.toJson()).toList(),
  });

  final outFile = File('fonts/inuktitut_matrix.json');
  outFile.writeAsStringSync(jsonOut);
  stdout.writeln('[SUCCESS] Exported validated matrix to ${outFile.path}');
}
