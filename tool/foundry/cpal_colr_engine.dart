import 'dart:typed_data';
import 'models.dart';

/// A 32-bit RGBA color representation for OpenType CPAL tables.
class CpalColor {
  final int r;
  final int g;
  final int b;
  final int a;

  const CpalColor(this.r, this.g, this.b, [this.a = 255]);

  /// Hex helper (e.g., 0xFF2A2A)
  factory CpalColor.fromHex(int rgbHex, [int alpha = 255]) {
    final r = (rgbHex >> 16) & 0xFF;
    final g = (rgbHex >> 8) & 0xFF;
    final b = rgbHex & 0xFF;
    return CpalColor(r, g, b, alpha);
  }

  /// Encodes to OpenType CPAL BGRA 4-byte format.
  Uint8List toBgraBytes() {
    final bytes = Uint8List(4);
    bytes[0] = b;
    bytes[1] = g;
    bytes[2] = r;
    bytes[3] = a;
    return bytes;
  }

  String toCssRgba() => 'rgba($r, $g, $b, ${a / 255})';
  String toHex() => '#${r.toRadixString(16).padLeft(2, '0')}${g.toRadixString(16).padLeft(2, '0')}${b.toRadixString(16).padLeft(2, '0')}';
}

/// A named color palette in the OpenType CPAL table.
class CpalPalette {
  final String name;
  final List<CpalColor> colors;

  const CpalPalette(this.name, this.colors);
}

/// OpenType CPAL (Color Palette Table) version 0 binary compiler.
/// Conforms strictly to ISO/IEC 14496-22 OpenType specification:
/// - uint16 version = 0
/// - uint16 numPaletteEntries
/// - uint16 numPalettes
/// - uint16 numColorRecords
/// - uint32 colorRecordsArrayOffset
/// - uint16 colorRecordIndices[numPalettes]
/// - BGRA colorRecords[numColorRecords]
class CpalTableBuilder {
  final List<CpalPalette> palettes;

  CpalTableBuilder(this.palettes);

  /// Default PocketGull Clinical & Telemetry 4-Palette Suite.
  factory CpalTableBuilder.pocketgullStandard() {
    return CpalTableBuilder([
      // Palette 0: Daylight EHR (High-Acuity Clinical Charting)
      CpalPalette('Daylight EHR', [
        CpalColor.fromHex(0x0A0E14), // 0: Obsidian Body Text
        CpalColor.fromHex(0x0D74CE), // 1: Clinical Blue Pill Fill
        CpalColor.fromHex(0xFFFFFF), // 2: Pure White Glyph Mark
        CpalColor.fromHex(0xD91F26), // 3: ISMP Alert Crimson
        CpalColor.fromHex(0x0284C7), // 4: Telemetry Cyan
        CpalColor.fromHex(0x059669), // 5: Safe Green Badge
        CpalColor.fromHex(0xD97706), // 6: Warning Amber
        CpalColor.fromHex(0xE2E8F0), // 7: Pill Border Stroke
      ]),

      // Palette 1: Scotopic 650nm (Circadian Night Vision / Zero Rhodopsin Bleaching)
      CpalPalette('Scotopic 650nm', [
        CpalColor.fromHex(0xFF2A2A), // 0: Pure 650nm Red Text
        CpalColor.fromHex(0x3B0A0A), // 1: Deep Red Pill Fill
        CpalColor.fromHex(0xFF6B6B), // 2: Luminous Red Glyph Mark
        CpalColor.fromHex(0xFF0000), // 3: High-Intensity Alert Red
        CpalColor.fromHex(0x800D0D), // 4: Muted Ember Accent
        CpalColor.fromHex(0xB91C1C), // 5: Crimson Status Pill
        CpalColor.fromHex(0xDC2626), // 6: Warning Glow Red
        CpalColor.fromHex(0x571010), // 7: Deep Ember Border
      ]),

      // Palette 2: Telemetry Phosphor (CRT Cathode Ray Monospace & Sub-cell ECG)
      CpalPalette('Telemetry Phosphor', [
        CpalColor.fromHex(0x00FF66), // 0: P1 Phosphor Vector Green
        CpalColor.fromHex(0x021F0D), // 1: CRT Glass Dark Green Pill
        CpalColor.fromHex(0x80FFB3), // 2: Phosphor Highlight Mark
        CpalColor.fromHex(0xFFAA00), // 3: Vector Amber Alert
        CpalColor.fromHex(0x00E5FF), // 4: Telemetry Cyan Waveform
        CpalColor.fromHex(0x10B981), // 5: Baseline Rhythm Green
        CpalColor.fromHex(0xF59E0B), // 6: Caution Amber Pill
        CpalColor.fromHex(0x064E24), // 7: Vector Grid Line Green
      ]),

      // Palette 3: ISMP Clinical Safety Alert (Dosage Disambiguation & Overdose Alarms)
      CpalPalette('ISMP Safety Alert', [
        CpalColor.fromHex(0x1E293B), // 0: Slate Contrast Text
        CpalColor.fromHex(0xFEE2E2), // 1: Soft Alert Tint Pill Fill
        CpalColor.fromHex(0x991B1B), // 2: Critical Dark Crimson Mark
        CpalColor.fromHex(0xDC2626), // 3: Trailing-Zero Strikethrough Flame
        CpalColor.fromHex(0xFEF3C7), // 4: Soft Warning Amber Fill
        CpalColor.fromHex(0xB45309), // 5: Amber Dosage Warning Mark
        CpalColor.fromHex(0xE11D48), // 6: Fatal Conflict Rose
        CpalColor.fromHex(0xFCA5A5), // 7: High-Risk Alert Border
      ]),

      // Palette 4: Washi Paper (Mulberry Cellulose & Sumi Ink / Low-Glare Matte Reflection)
      CpalPalette('Washi Paper', [
        CpalColor.fromHex(0x1E1B18), // 0: Sumi Ink Body Text
        CpalColor.fromHex(0xEBE3D3), // 1: Pressed Mulberry Paper Pill Fill
        CpalColor.fromHex(0x1E3A8A), // 2: Aizome Indigo Glyph Mark
        CpalColor.fromHex(0x991B1B), // 3: Vermilion Hanko Seal Red
        CpalColor.fromHex(0x0D9488), // 4: Antique Teal Accent
        CpalColor.fromHex(0x059669), // 5: Bamboo Green Badge
        CpalColor.fromHex(0xB45309), // 6: Persimmon Kaki Amber
        CpalColor.fromHex(0xD4C8B2), // 7: Kozo Fiber Border
      ]),

      // Palette 5: Amber Hearth (1800K Candlelight / Zero-Blue Melatonin Preservation)
      CpalPalette('Amber Hearth', [
        CpalColor.fromHex(0xFBBF24), // 0: Warm Amber 1800K Text
        CpalColor.fromHex(0x26160A), // 1: Dark Mahogany Hearth Fill
        CpalColor.fromHex(0xFDE68A), // 2: Golden Flame Mark
        CpalColor.fromHex(0xEA580C), // 3: Terracotta Fire Glow
        CpalColor.fromHex(0xD97706), // 4: Cinnamon Amber Accent
        CpalColor.fromHex(0x78350F), // 5: Smoked Oak Badge
        CpalColor.fromHex(0xB45309), // 6: Molten Bronze Warning
        CpalColor.fromHex(0x451A03), // 7: Charred Walnut Border
      ]),

      // Palette 6: Sage Scriptorium (Biophilic Celadon & Pine / Ciliary Muscle Relaxation)
      CpalPalette('Sage Scriptorium', [
        CpalColor.fromHex(0x132E20), // 0: Forest Pine Text
        CpalColor.fromHex(0xD1E7DD), // 1: Celadon Clay Pill Fill
        CpalColor.fromHex(0x065F46), // 2: Deep Emerald Optotype
        CpalColor.fromHex(0x9F1239), // 3: Winterberry Alert
        CpalColor.fromHex(0x0284C7), // 4: Mountain Stream Cyan
        CpalColor.fromHex(0x10B981), // 5: Sprout Green Badge
        CpalColor.fromHex(0xCA8A04), // 6: Moss Lichen Amber
        CpalColor.fromHex(0xA7D0BA), // 7: Botanical Stem Border
      ]),

      // Palette 7: Obsidian Anti-Halation (Soft Slate on Pure Black / Zero Glare)
      CpalPalette('Obsidian Dark', [
        CpalColor.fromHex(0xCBD5E1), // 0: Soft Slate Neutral 300 Text (No Halation)
        CpalColor.fromHex(0x0F172A), // 1: Midnight Slate 900 Fill
        CpalColor.fromHex(0x38BDF8), // 2: Luminous Sky Blue Mark
        CpalColor.fromHex(0xF43F5E), // 3: Subdued Rose Alert
        CpalColor.fromHex(0x818CF8), // 4: Periwinkle Accent
        CpalColor.fromHex(0x34D399), // 5: Mint Safe Badge
        CpalColor.fromHex(0xFBBF24), // 6: Warm Ochre Warning
        CpalColor.fromHex(0x334155), // 7: Slate 700 Border
      ]),

      // Palette 8: Sunshine Meadow (Joyful Warmth, Playfulness & Hope)
      CpalPalette('Sunshine Meadow', [
        CpalColor.fromHex(0x78350F), // 0: Warm Honey Amber Text
        CpalColor.fromHex(0xFEF3C7), // 1: Buttercup Cream Fill
        CpalColor.fromHex(0xF59E0B), // 2: Golden Marigold Sunburst
        CpalColor.fromHex(0xF43F5E), // 3: Wildflower Coral Heart
        CpalColor.fromHex(0x38BDF8), // 4: Morning Sky Blue
        CpalColor.fromHex(0x10B981), // 5: Fresh Clover Sprout
        CpalColor.fromHex(0xFBBF24), // 6: Radiant Sunshine Yellow
        CpalColor.fromHex(0xFDE68A), // 7: Honeycomb Golden Border
      ]),
    ]);
  }

  /// Compiles table to binary byte buffer.
  SfntTable build() {
    if (palettes.isEmpty) {
      throw ArgumentError('CPAL table requires at least 1 palette');
    }

    final numPalettes = palettes.length;
    final numPaletteEntries = palettes.first.colors.length;

    // Verify all palettes have matching number of entries
    for (final p in palettes) {
      if (p.colors.length != numPaletteEntries) {
        throw ArgumentError('All CPAL palettes must have exactly $numPaletteEntries entries');
      }
    }

    final numColorRecords = numPalettes * numPaletteEntries;
    final headerSize = 12; // version(2) + numEntries(2) + numPalettes(2) + numColorRecords(2) + offset(4)
    final indicesSize = numPalettes * 2;
    final colorRecordsArrayOffset = headerSize + indicesSize;
    final totalSize = colorRecordsArrayOffset + numColorRecords * 4;

    // Align to 2-byte word boundary
    final paddedSize = (totalSize % 2 != 0) ? totalSize + 1 : totalSize;
    final bytes = Uint8List(paddedSize);
    final bd = ByteData.sublistView(bytes);

    // Header
    bd.setUint16(0, 0, Endian.big); // version = 0
    bd.setUint16(2, numPaletteEntries, Endian.big);
    bd.setUint16(4, numPalettes, Endian.big);
    bd.setUint16(6, numColorRecords, Endian.big);
    bd.setUint32(8, colorRecordsArrayOffset, Endian.big);

    // Color Record Indices
    for (var i = 0; i < numPalettes; i++) {
      bd.setUint16(12 + i * 2, i * numPaletteEntries, Endian.big);
    }

    // Color Records (BGRA)
    var offset = colorRecordsArrayOffset;
    for (final palette in palettes) {
      for (final color in palette.colors) {
        final bgra = color.toBgraBytes();
        bytes.setRange(offset, offset + 4, bgra);
        offset += 4;
      }
    }

    return SfntTable('CPAL', bytes);
  }
}

/// A layer definition in a COLR glyph.
class ColrLayer {
  final int glyphId;
  final int paletteIndex; // 0xFFFF = use current text color

  const ColrLayer(this.glyphId, this.paletteIndex);
}

/// A base glyph mapping in the OpenType COLR table.
class ColrBaseGlyph {
  final int glyphId;
  final List<ColrLayer> layers;

  const ColrBaseGlyph(this.glyphId, this.layers);
}

/// OpenType COLR (Color Table) version 0 binary compiler.
/// Conforms strictly to ISO/IEC 14496-22:
/// - uint16 version = 0
/// - uint16 numBaseGlyphRecords
/// - uint32 baseGlyphRecordsOffset
/// - uint32 layerRecordsOffset
/// - uint16 numLayerRecords
/// - BaseGlyphRecord[numBaseGlyphRecords] (MUST be sorted by glyphId)
/// - LayerRecord[numLayerRecords]
class ColrTableBuilder {
  final List<ColrBaseGlyph> baseGlyphs;

  ColrTableBuilder(List<ColrBaseGlyph> glyphs) : baseGlyphs = List.from(glyphs) {
    // OpenType specification requires baseGlyphRecords to be sorted by glyphId for binary search
    baseGlyphs.sort((a, b) => a.glyphId.compareTo(b.glyphId));
  }

  SfntTable build() {
    final numBaseGlyphs = baseGlyphs.length;
    final totalLayers = baseGlyphs.fold<int>(0, (sum, bg) => sum + bg.layers.length);

    final headerSize = 14; // version(2) + numBase(2) + baseOffset(4) + layerOffset(4) + numLayers(2)
    final baseRecordsOffset = headerSize;
    final baseRecordsSize = numBaseGlyphs * 6; // glyphId(2) + firstLayerIndex(2) + numLayers(2)
    final layerRecordsOffset = baseRecordsOffset + baseRecordsSize;
    final layerRecordsSize = totalLayers * 4; // glyphId(2) + paletteIndex(2)
    final totalSize = layerRecordsOffset + layerRecordsSize;

    // Pad to 2-byte word boundary
    final paddedSize = (totalSize % 2 != 0) ? totalSize + 1 : totalSize;
    final bytes = Uint8List(paddedSize);
    final bd = ByteData.sublistView(bytes);

    // Header
    bd.setUint16(0, 0, Endian.big); // version = 0
    bd.setUint16(2, numBaseGlyphs, Endian.big);
    bd.setUint32(4, baseRecordsOffset, Endian.big);
    bd.setUint32(8, layerRecordsOffset, Endian.big);
    bd.setUint16(12, totalLayers, Endian.big);

    // Write BaseGlyphRecords and LayerRecords
    int layerCounter = 0;
    for (var i = 0; i < numBaseGlyphs; i++) {
      final bg = baseGlyphs[i];
      final baseOff = baseRecordsOffset + i * 6;
      bd.setUint16(baseOff, bg.glyphId, Endian.big);
      bd.setUint16(baseOff + 2, layerCounter, Endian.big);
      bd.setUint16(baseOff + 4, bg.layers.length, Endian.big);

      for (final layer in bg.layers) {
        final layerOff = layerRecordsOffset + layerCounter * 4;
        bd.setUint16(layerOff, layer.glyphId, Endian.big);
        bd.setUint16(layerOff + 2, layer.paletteIndex, Endian.big);
        layerCounter++;
      }
    }

    return SfntTable('COLR', bytes);
  }
}

/// A pattern definition that triggers an in-font contextual multi-color token.
class ChromaticPatternRule {
  final String patternString;
  final String tokenName;
  final String description;
  final int baseGlyphId;
  final List<ColrLayer> layers;

  const ChromaticPatternRule({
    required this.patternString,
    required this.tokenName,
    required this.description,
    required this.baseGlyphId,
    required this.layers,
  });
}

/// Standard PocketGull Pattern Rules for In-Font Token Matching.
class PocketGullChromaticLibrary {
  static List<ChromaticPatternRule> getStandardRules() {
    return [
      ChromaticPatternRule(
        patternString: '*.dart',
        tokenName: 'token.glob_dart',
        description: 'Developer Glob Match: Dart Source File Wildcard',
        baseGlyphId: 9001,
        layers: [
          ColrLayer(8801, 1), // Layer 0: Baseline accent bar (Clinical Blue / Deep Red)
          ColrLayer(8802, 2), // Layer 1: High-contrast white glyph text "DART"
          ColrLayer(8803, 4), // Layer 2: Cyan accent dot indicator
        ],
      ),
      ChromaticPatternRule(
        patternString: '**/*',
        tokenName: 'token.globstar_tree',
        description: 'Developer Glob Match: Recursive Directory Globstar Tree',
        baseGlyphId: 9002,
        layers: [
          ColrLayer(8801, 7), // Layer 0: Subtle baseline anchor
          ColrLayer(8804, 0), // Layer 1: Monospace folder tree chevron
          ColrLayer(8805, 5), // Layer 2: Green recursive branch dot
        ],
      ),
      ChromaticPatternRule(
        patternString: '[OK]',
        tokenName: 'badge.status_ok',
        description: 'Terminal & Telemetry Status: System Normal (Telemetry Green)',
        baseGlyphId: 9003,
        layers: [
          ColrLayer(8801, 5), // Layer 0: Green Status Fill
          ColrLayer(8806, 2), // Layer 1: Sloan optotype checkmark & "OK"
        ],
      ),
      ChromaticPatternRule(
        patternString: '[WARN]',
        tokenName: 'badge.status_warn',
        description: 'Terminal & Telemetry Status: Warning Alert (Hazard Amber)',
        baseGlyphId: 9004,
        layers: [
          ColrLayer(8801, 6), // Layer 0: Amber Warning Fill
          ColrLayer(8807, 0), // Layer 1: Obsidian Warning Triangle & "WARN"
        ],
      ),
      ChromaticPatternRule(
        patternString: '[FATAL]',
        tokenName: 'badge.status_fatal',
        description: 'Terminal & Telemetry Status: Critical Failure (Alert Crimson)',
        baseGlyphId: 9005,
        layers: [
          ColrLayer(8801, 3), // Layer 0: High-Intensity Crimson Fill
          ColrLayer(8808, 2), // Layer 1: Pure White Alert Diamond & "FATAL"
        ],
      ),
      ChromaticPatternRule(
        patternString: '5.0 mg',
        tokenName: 'alert.trailing_zero',
        description: 'ISMP Life-Critical Safeguard: Trailing-Zero Overdose Warning',
        baseGlyphId: 9006,
        layers: [
          ColrLayer(8809, 0), // Layer 0: "5." base numeral
          ColrLayer(8810, 3), // Layer 1: Crimson warning slash across dangerous "0"
          ColrLayer(8811, 0), // Layer 2: "mg" dosage unit
        ],
      ),
      ChromaticPatternRule(
        patternString: 'Fe2+',
        tokenName: 'chem.ferrous_ion',
        description: 'Clinical Biochemistry: Stoichiometric Hemoglobin Oxygen Carrier',
        baseGlyphId: 9007,
        layers: [
          ColrLayer(8812, 0), // Layer 0: "Fe" elemental stem
          ColrLayer(8813, 3), // Layer 1: Alert Crimson "2+" valence charge superscript
        ],
      ),
      ChromaticPatternRule(
        patternString: ':)',
        tokenName: 'joy.humanist_smile',
        description: 'Humanist Felt-Marker Smile: Organic Warmth & Cheerful Greeting',
        baseGlyphId: 9008,
        layers: [
          ColrLayer(8801, 6), // Layer 0: Golden sunshine accent bar
          ColrLayer(8814, 0), // Layer 1: Humanist curved felt-pen smile
          ColrLayer(8815, 2), // Layer 2: Joyful sparkle dot
        ],
      ),
      ChromaticPatternRule(
        patternString: '<3',
        tokenName: 'joy.philocardia_heart',
        description: 'Philocardia Heart Tittle: Cardiac Pacing & Affective Compassion',
        baseGlyphId: 9009,
        layers: [
          ColrLayer(8801, 1), // Layer 0: Warm rose baseline ground
          ColrLayer(8816, 3), // Layer 1: Anatomical Philocardia heart mark
          ColrLayer(8817, 2), // Layer 2: Gentle systolic glow accent
        ],
      ),
      ChromaticPatternRule(
        patternString: '[JOY]',
        tokenName: 'joy.radiant_sunburst',
        description: 'Celebratory Sunburst: Radiant Morning Light & Vitality',
        baseGlyphId: 9010,
        layers: [
          ColrLayer(8801, 6), // Layer 0: Marigold golden anchor
          ColrLayer(8818, 0), // Layer 1: Bold Sloan "JOY" lettering
          ColrLayer(8819, 2), // Layer 2: 8-ray sunburst halo
        ],
      ),
      ChromaticPatternRule(
        patternString: '[HEAL]',
        tokenName: 'joy.clover_sprout',
        description: 'Botanical Vitality: Fresh Spring Sprout & Salutogenic Recovery',
        baseGlyphId: 9011,
        layers: [
          ColrLayer(8801, 5), // Layer 0: Fresh clover green anchor
          ColrLayer(8820, 0), // Layer 1: Clean Sloan "HEAL" lettering
          ColrLayer(8821, 5), // Layer 2: Two-leaf regenerative seedling
        ],
      ),
    ];
  }
}
