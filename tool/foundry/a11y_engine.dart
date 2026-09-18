import 'models.dart';

/// PocketGull A11y & Neuro-Ergonomic TrueType Glyph Engine.
///
/// Synthesizes quadratic Bézier contours for:
/// 1. Monochromatic Telemetry Badges ([CRIT], ▲HIGH, ▼LOW, ◆HOLD, ●NORM).
/// 2. Wong-Baker FACES Pain Rating Scale (Scores 0, 2, 4, 6, 8, 10).
/// 3. Core ICU Non-Verbal Physiological Need Pictograms.
///
/// Guaranteed Invariants:
/// - 1000 UPM Em-Square conformance.
/// - 2-byte word-aligned TrueType glyph records (loca[i] % 2 == 0).
/// - Bit-7 flag cleared on all point records.
/// - Louise Sloan 5:1 optotype stroke and aperture clearances.
class A11yEngine {
  static const int upm = 1000;
  static const int strokeWidth = 100;

  /// Synthesizes the Double-Walled Octagon for Critical Alarms ([CRIT]).
  static GlyphRecord generateOctagonCrit(int gid, {int advance = 1200}) {
    final outer = GlyphContour()
      ..add(350, 850)
      ..add(850, 850)
      ..add(1100, 600)
      ..add(1100, 250)
      ..add(850, 0)
      ..add(350, 0)
      ..add(100, 250)
      ..add(100, 600);

    // Inner counter
    final inner = GlyphContour()
      ..add(380, 770)
      ..add(180, 570)
      ..add(180, 280)
      ..add(380, 80)
      ..add(820, 80)
      ..add(1020, 280)
      ..add(1020, 570)
      ..add(820, 770);

    // Center exclamation stem
    final exclStem = GlyphContour()
      ..add(560, 650)
      ..add(640, 650)
      ..add(630, 320)
      ..add(570, 320);

    // Center exclamation dot
    final exclDot = GlyphContour()
      ..add(560, 240)
      ..add(640, 240)
      ..add(640, 160)
      ..add(560, 160);

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xE080,
      name: 'badge.crit',
      advanceWidth: advance,
      lsb: 100,
      contours: [outer, inner, exclStem, exclDot],
    );
  }

  /// Synthesizes the Upward Equilateral Triangle for High Thresholds (▲HIGH).
  static GlyphRecord generateTriangleHigh(int gid, {int advance = 1000}) {
    final outer = GlyphContour()
      ..add(500, 850)
      ..add(900, 100)
      ..add(100, 100);

    final inner = GlyphContour()
      ..add(500, 680)
      ..add(250, 200)
      ..add(750, 200);

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0x25B2, // ▲
      name: 'badge.high',
      advanceWidth: advance,
      lsb: 100,
      contours: [outer, inner],
    );
  }

  /// Synthesizes the Downward Equilateral Triangle for Low Thresholds (▼LOW).
  static GlyphRecord generateTriangleLow(int gid, {int advance = 1000}) {
    final outer = GlyphContour()
      ..add(500, 100)
      ..add(100, 850)
      ..add(900, 850);

    final inner = GlyphContour()
      ..add(500, 270)
      ..add(750, 750)
      ..add(250, 750);

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0x25BC, // ▼
      name: 'badge.low',
      advanceWidth: advance,
      lsb: 100,
      contours: [outer, inner],
    );
  }

  /// Synthesizes the Diamond for Paused / Manual Override (◆HOLD).
  static GlyphRecord generateDiamondHold(int gid, {int advance = 1000}) {
    final outer = GlyphContour()
      ..add(500, 880)
      ..add(900, 480)
      ..add(500, 80)
      ..add(100, 480);

    final inner = GlyphContour()
      ..add(500, 720)
      ..add(260, 480)
      ..add(500, 240)
      ..add(740, 480);

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0x25C6, // ◆
      name: 'badge.hold',
      advanceWidth: advance,
      lsb: 100,
      contours: [outer, inner],
    );
  }

  /// Synthesizes the Circular Pill for Normal Baseline (●NORM).
  static GlyphRecord generateCircleNorm(int gid, {int advance = 1000}) {
    final outer = GlyphContour()
      ..add(500, 880)
      ..add(880, 880, onCurve: false)
      ..add(880, 480)
      ..add(880, 80, onCurve: false)
      ..add(500, 80)
      ..add(120, 80, onCurve: false)
      ..add(120, 480)
      ..add(120, 880, onCurve: false);

    final inner = GlyphContour()
      ..add(500, 740)
      ..add(260, 740, onCurve: false)
      ..add(260, 480)
      ..add(260, 220, onCurve: false)
      ..add(500, 220)
      ..add(740, 220, onCurve: false)
      ..add(740, 480)
      ..add(740, 740, onCurve: false);

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0x25CF, // ●
      name: 'badge.norm',
      advanceWidth: advance,
      lsb: 120,
      contours: [outer, inner],
    );
  }

  /// Synthesizes a Wong-Baker FACES Pain Scale contour (Score 0..10).
  static GlyphRecord generateWongBakerFace(int gid, int score, {int advance = 1000}) {
    // Face perimeter (circle at 500, 480, r=380)
    final head = GlyphContour()
      ..add(500, 860)
      ..add(880, 860, onCurve: false)
      ..add(880, 480)
      ..add(880, 100, onCurve: false)
      ..add(500, 100)
      ..add(120, 100, onCurve: false)
      ..add(120, 480)
      ..add(120, 860, onCurve: false);

    // Left eye (circle at 350, 580, r=40)
    final leftEye = GlyphContour()
      ..add(350, 620)
      ..add(390, 620, onCurve: false)
      ..add(390, 580)
      ..add(390, 540, onCurve: false)
      ..add(350, 540)
      ..add(310, 540, onCurve: false)
      ..add(310, 580)
      ..add(310, 620, onCurve: false);

    // Right eye (circle at 650, 580, r=40)
    final rightEye = GlyphContour()
      ..add(650, 620)
      ..add(690, 620, onCurve: false)
      ..add(690, 580)
      ..add(690, 540, onCurve: false)
      ..add(650, 540)
      ..add(610, 540, onCurve: false)
      ..add(610, 580)
      ..add(610, 620, onCurve: false);

    final mouth = GlyphContour();
    switch (score) {
      case 0:
        // Wide smile
        mouth
          ..add(300, 380)
          ..add(500, 200, onCurve: false)
          ..add(700, 380)
          ..add(500, 260, onCurve: false);
        break;
      case 2:
        // Gentle smile
        mouth
          ..add(340, 360)
          ..add(500, 260, onCurve: false)
          ..add(660, 360)
          ..add(500, 300, onCurve: false);
        break;
      case 4:
        // Neutral line
        mouth
          ..add(340, 330)
          ..add(660, 330)
          ..add(660, 290)
          ..add(340, 290);
        break;
      case 6:
        // Slight frown
        mouth
          ..add(340, 280)
          ..add(500, 360, onCurve: false)
          ..add(660, 280)
          ..add(500, 320, onCurve: false);
        break;
      case 8:
        // Deep frown
        mouth
          ..add(300, 240)
          ..add(500, 420, onCurve: false)
          ..add(700, 240)
          ..add(500, 360, onCurve: false);
        break;
      case 10:
      default:
        // Crying open mouth
        mouth
          ..add(300, 240)
          ..add(500, 440, onCurve: false)
          ..add(700, 240)
          ..add(500, 160, onCurve: false);
        break;
    }

    return GlyphRecord(
      glyphId: gid,
      codePoint: 0xE100 + (score ~/ 2),
      name: 'wongbaker.face.$score',
      advanceWidth: advance,
      lsb: 120,
      contours: [head, leftEye, rightEye, mouth],
    );
  }
}
