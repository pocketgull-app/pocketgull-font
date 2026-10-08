import 'models.dart';

/// 256-Glyph Universal Unicode Braille Transcriber (ISO/TR 11548).
///
/// Synthesizes the complete U+2800–28FF Unicode 8-dot computer Braille block.
/// Each codepoint represents an 8-bit bitfield mapped to tactile dot coordinates:
/// - Left column: Dots 1, 2, 3, 7 (bits 0, 1, 2, 6)
/// - Right column: Dots 4, 5, 6, 8 (bits 3, 4, 5, 7)
class BrailleGenerator {
  static const int cellWidth = 750;
  static const int dotRadius = 60;
  static const int calibratedDotRadius = 78;

  // 1. Raw ISO/TR 11548 tactile coordinate matrix (UPM 1000)
  static const dotCoordinates = [
    (200, 700), // Dot 1 (bit 0)
    (200, 450), // Dot 2 (bit 1)
    (200, 200), // Dot 3 (bit 2)
    (520, 700), // Dot 4 (bit 3)
    (520, 450), // Dot 5 (bit 4)
    (520, 200), // Dot 6 (bit 5)
    (200, -50), // Dot 7 (bit 6)
    (520, -50), // Dot 8 (bit 7)
  ];

  // 2. PocketGull Optically-Calibrated Readability Matrix
  // Grounded between English baseline (y=0) and Cap Height (y=720):
  // - Dot 3 bottom sits tangent to baseline (y=0): cy = 78 (bottom = 78 - 78 = 0 UPM)
  // - Dot 2 sits at optical midline: cy = 360 UPM
  // - Dot 1 top sits tangent to Cap Height (y=720): cy = 642 (top = 642 + 78 = 720 UPM)
  // - Dots 7 & 8 sit in dedicated descender zone: cy = -180 UPM
  static const calibratedDotCoordinates = [
    (210, 642), // Dot 1 (top of primary cell, tangent to Cap Height y=720)
    (210, 360), // Dot 2 (optical median)
    (210, 78),  // Dot 3 (grounded on baseline, tangent to y=0)
    (510, 642), // Dot 4 (top right)
    (510, 360), // Dot 5 (mid right)
    (510, 78),  // Dot 6 (grounded right)
    (210, -180), // Dot 7 (descender zone)
    (510, -180), // Dot 8 (descender zone)
  ];

  /// Generates a single circular dot contour (clockwise for TrueType).
  static GlyphContour _buildDotContour(int cx, int cy, int r) {
    return GlyphContour()
      ..add(cx, cy + r)
      ..add(cx + r, cy + r, onCurve: false)
      ..add(cx + r, cy)
      ..add(cx + r, cy - r, onCurve: false)
      ..add(cx, cy - r)
      ..add(cx - r, cy - r, onCurve: false)
      ..add(cx - r, cy)
      ..add(cx - r, cy + r, onCurve: false);
  }

  /// Generates a cushioned Philocardia heart dot contour (clockwise for TrueType).
  static GlyphContour _buildHeartDotContour(int cx, int cy, int r) {
    final double hr = r * 1.15;
    final int top = cy + r;
    final int bot = cy - r;
    final int cleft = cy + (r * 0.25).round();
    final int apexR = (r * 0.15).round();

    return GlyphContour()
      ..add(cx, bot)
      ..add(cx + apexR, bot, onCurve: false)
      ..add(cx + hr.round(), cy)
      ..add(cx + hr.round(), top, onCurve: false)
      ..add(cx + (hr * 0.5).round(), top)
      ..add(cx + (hr * 0.15).round(), top, onCurve: false)
      ..add(cx, cleft)
      ..add(cx - (hr * 0.15).round(), top, onCurve: false)
      ..add(cx - (hr * 0.5).round(), top)
      ..add(cx - hr.round(), top, onCurve: false)
      ..add(cx - hr.round(), cy)
      ..add(cx - apexR, bot, onCurve: false);
  }

  /// Synthesizes a Braille glyph from its 8-bit pattern (0 to 255).
  static GlyphRecord generateBrailleGlyph(
    int gid,
    int bytePattern, {
    bool opticalReadability = true,
    bool philocardiaHearts = false,
  }) {
    final codePoint = 0x2800 + bytePattern;
    final contours = <GlyphContour>[];
    final coords = opticalReadability ? calibratedDotCoordinates : dotCoordinates;
    final radius = opticalReadability ? calibratedDotRadius : dotRadius;

    for (var dot = 0; dot < 8; dot++) {
      if ((bytePattern & (1 << dot)) != 0) {
        final pos = coords[dot];
        if (philocardiaHearts) {
          contours.add(_buildHeartDotContour(pos.$1, pos.$2, radius));
        } else {
          contours.add(_buildDotContour(pos.$1, pos.$2, radius));
        }
      }
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: codePoint,
      name: 'uni${codePoint.toRadixString(16).toUpperCase().padLeft(4, "0")}',
      advanceWidth: cellWidth,
      lsb: contours.isEmpty ? 0 : 210 - radius,
      contours: contours,
    );
  }

  /// Synthesizes the full 256-glyph block into a list of GlyphRecords.
  static List<GlyphRecord> generateAll(
    int startingGid, {
    bool opticalReadability = true,
    bool philocardiaHearts = false,
  }) {
    final list = <GlyphRecord>[];
    for (var b = 0; b < 256; b++) {
      list.add(generateBrailleGlyph(
        startingGid + b,
        b,
        opticalReadability: opticalReadability,
        philocardiaHearts: philocardiaHearts,
      ));
    }
    return list;
  }
}
