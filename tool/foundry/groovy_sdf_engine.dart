import 'dart:io';
import 'dart:math' as math;
import 'dart:typed_data';
import 'models.dart';
import 'sfnt_builder.dart';
import 'phinney_auditor.dart';

/// High-Weirdness Psych-Mechanic SDF + Marching Squares + C1 Quadratic B-Spline Engine
/// for Gearhead Groovy (GearArts 2k26 Collection).
///
/// Synthesizes:
/// 1. 1970s Keep-On-Truckin' / Ed "Big Daddy" Roth non-linear Bell-Bottom & Rubber-Hose Warp
/// 2. External Sprocket Gear Crowns (letters sprouting real gear teeth on their outer backs!)
/// 3. Open-End Spanner / Wrench-Jaw Terminals
/// 4. Tilted Asymmetrical Star-Cog Counters
/// 5. Extreme Multi-Tendril Viscous Paint Meltdowns + Upward Splash Droplets

typedef SdfFunc = double Function(double x, double y);

class SdfPrimitives {
  /// Smooth minimum (polynomial smooth union) for liquid ink-pooling fillets
  static double smin(double a, double b, [double k = 32.0]) {
    if (k <= 0) return math.min(a, b);
    final h = math.max(k - (a - b).abs(), 0.0) / k;
    return math.min(a, b) - h * h * k * 0.25;
  }

  /// Smooth subtraction (cuts `hole` out of `base` with subtle fillet `k`)
  static double ssub(double base, double hole, [double k = 8.0]) {
    return -smin(-base, hole, k);
  }

  /// Non-linear 1970s "Rubber-Hose & Bell-Bottom Lava-Lamp" coordinate warp!
  /// - Bends straight stems into groovy S-curves
  /// - Pinches the high waist (y ~ 450) and swells the bottom (y ~ 120) like bell-bottom overalls!
  static (double wx, double wy, double swell) warpGroovy(
    double x,
    double y, {
    double centerX = 370.0,
    double swayAmp = 26.0,
    double bellBottomStrength = 0.28,
    double phase = 0.0,
  }) {
    final normY = ((y - 80.0) / 580.0).clamp(-0.4, 1.3);
    // Rubber-hose S-bend sway
    final sway = swayAmp * math.sin(normY * math.pi * 1.65 + phase);
    // Bell-bottom gravity scale: wider at bottom (normY ~ 0.1), pinched at waist (normY ~ 0.65), flared at top (normY ~ 1.0)
    final bottomBulge = math.exp(-math.pow((normY - 0.12) / 0.32, 2));
    final waistPinch = math.exp(-math.pow((normY - 0.62) / 0.25, 2));
    final horizScale = 1.0 + bellBottomStrength * bottomBulge - 0.18 * waistPinch;

    final wx = centerX + (x - centerX - sway) / horizScale;
    final swell = 1.0 + 0.26 * bottomBulge - 0.14 * waistPinch;
    return (wx, y, swell);
  }

  /// Circle SDF centered at (cx, cy) with radius r
  static double circle(double x, double y, double cx, double cy, double r) {
    final dx = x - cx;
    final dy = y - cy;
    return math.sqrt(dx * dx + dy * dy) - r;
  }

  /// Variable-radius pillowed capsule with extreme dog-bone / bell-bottom lobe swell
  static double capsule(
    double x,
    double y,
    double x1,
    double y1,
    double x2,
    double y2,
    double r1,
    double r2, {
    double waistFactor = 0.72,
    double sway = 22.0,
  }) {
    final pax = x - x1;
    final pay = y - y1;
    final bax = x2 - x1;
    final bay = y2 - y1;
    final baLen2 = bax * bax + bay * bay;
    final t = baLen2 > 0 ? ((pax * bax + pay * bay) / baLen2).clamp(0.0, 1.0) : 0.0;

    // Orthogonal normal for rubber-hose bow along the capsule
    final len = math.sqrt(baLen2);
    final nx = len > 0 ? -bay / len : 0.0;
    final ny = len > 0 ? bax / len : 0.0;
    final bow = sway * math.sin(t * math.pi);

    final dx = pax - bax * t - nx * bow;
    final dy = pay - bay * t - ny * bow;
    final dist = math.sqrt(dx * dx + dy * dy);

    // Exaggerated hourglass waist pinch in the middle of the stroke for rubber-hose feel
    final rLinear = r1 + (r2 - r1) * t;
    final pinch = 1.0 - (1.0 - waistFactor) * 4.0 * t * (1.0 - t);
    final tube = dist - rLinear * pinch;

    // Swollen 1970s mushroom / bell-bottom terminal bulbs at both ends
    final lobe1 = circle(x, y, x1, y1, r1 * 1.08);
    final lobe2 = circle(x, y, x2, y2, r2 * 1.08);
    return smin(tube, math.min(lobe1, lobe2), 28.0);
  }

  /// Quadratic Bézier skeleton stroke with variable radius and terminal swell
  static double quadStroke(
    double x,
    double y,
    double x0,
    double y0,
    double x1,
    double y1,
    double x2,
    double y2,
    double rStart,
    double rMid,
    double rEnd, {
    int steps = 16,
  }) {
    double minD = 999999.0;
    double prevX = x0;
    double prevY = y0;
    double prevR = rStart;

    for (int i = 1; i <= steps; i++) {
      final t = i / steps;
      final omt = 1.0 - t;
      final curX = omt * omt * x0 + 2 * omt * t * x1 + t * t * x2;
      final curY = omt * omt * y0 + 2 * omt * t * y1 + t * t * y2;
      final curR = t < 0.5
          ? rStart + (rMid - rStart) * (t * 2.0)
          : rMid + (rEnd - rMid) * ((t - 0.5) * 2.0);

      final pax = x - prevX;
      final pay = y - prevY;
      final bax = curX - prevX;
      final bay = curY - prevY;
      final ba2 = bax * bax + bay * bay;
      final h = ba2 > 0 ? ((pax * bax + pay * bay) / ba2).clamp(0.0, 1.0) : 0.0;
      final dx = pax - bax * h;
      final dy = pay - bay * h;
      final r = prevR + (curR - prevR) * h;
      final d = math.sqrt(dx * dx + dy * dy) - r;
      if (d < minD) minD = d;

      prevX = curX;
      prevY = curY;
      prevR = curR;
    }
    final startLobe = circle(x, y, x0, y0, rStart * 1.10);
    final endLobe = circle(x, y, x2, y2, rEnd * 1.12);
    return smin(minD, math.min(startLobe, endLobe), 26.0);
  }

  /// Internal AGMA Star-Cog Gear Counter SDF
  static double gearCounter(
    double x,
    double y,
    double cx,
    double cy,
    double pitchRadius, {
    int teeth = 8,
    double toothDepth = 32.0,
    double rotationRad = 0.22,
  }) {
    final dx = x - cx;
    final dy = y - cy;
    final r = math.sqrt(dx * dx + dy * dy);
    final theta = math.atan2(dy, dx) + rotationRad;
    final wave = (math.cos(teeth * theta) * 1.65).clamp(-1.0, 1.0);
    final targetR = pitchRadius + toothDepth * 0.5 * wave;
    return r - targetR;
  }

  /// External Sprocket Gear Crown! Sprouts chunky mechanical gear teeth along an angular arc
  /// [angleMinRad, angleMaxRad] of an outer letterform curve centered at (cx, cy)!
  static double addExternalGearTeeth(
    double baseD,
    double x,
    double y,
    double cx,
    double cy,
    double baseRadius, {
    int teeth = 10,
    double toothHeight = 42.0,
    double angleMinRad = -3.14,
    double angleMaxRad = 3.14,
  }) {
    final dx = x - cx;
    final dy = y - cy;
    final r = math.sqrt(dx * dx + dy * dy);
    final theta = math.atan2(dy, dx);

    // Smooth angular window so teeth only sprout along the desired sector
    double inSector = 0.0;
    if (theta >= angleMinRad && theta <= angleMaxRad) {
      final edgeDist = math.min(theta - angleMinRad, angleMaxRad - theta);
      inSector = (edgeDist / 0.25).clamp(0.0, 1.0);
    }
    if (inSector <= 0.0) return baseD;

    final wave = (math.cos(teeth * theta) * 1.7).clamp(0.0, 1.0);
    final cogR = baseRadius + toothHeight * wave * inSector;
    final cogD = r - cogR;
    // Also bound inner radius so it doesn't fill the letter's inner hole
    final ringD = math.max(cogD, (baseRadius - 55.0) - r);
    return smin(baseD, ringD, 14.0);
  }

  /// Cuts an Open-End Spanner / Wrench Jaw notch into a terminal at (wx, wy) pointing at angleRad
  static double cutWrenchJaw(
    double baseD,
    double x,
    double y,
    double wx,
    double wy, {
    double angleRad = 0.0,
    double jawWidth = 38.0,
    double jawDepth = 65.0,
  }) {
    final dx = x - wx;
    final dy = y - wy;
    final cosA = math.cos(-angleRad);
    final sinA = math.sin(-angleRad);
    final lx = dx * cosA - dy * sinA;
    final ly = dx * sinA + dy * cosA;

    // Hex-nut / wrench slot centered at origin extending +lx
    final slot = capsule(lx, ly, -10, 0, jawDepth, 0, jawWidth, jawWidth * 1.15, waistFactor: 1.0, sway: 0.0);
    return ssub(baseD, slot, 6.0);
  }

  /// Attaches a weird, stretchy, multi-bulbous lava-lamp paint drip with meniscus neck
  static double addDrip(
    double baseD,
    double x,
    double y,
    double topX,
    double topY,
    double botY, {
    double neckRadius = 17.0,
    double bulbRadius = 31.0,
    bool withDetachedDrop = false,
    double dropRadius = 21.0,
    double sway = 10.0,
  }) {
    final stem = capsule(
      x,
      y,
      topX,
      topY + 30,
      topX + sway * 0.4,
      botY + bulbRadius * 0.35,
      neckRadius * 1.5,
      neckRadius * 0.72,
      waistFactor: 0.68,
      sway: sway,
    );
    final bulb = circle(x, y, topX + sway * 0.4, botY, bulbRadius);
    final connectedDrip = smin(stem, bulb, 26.0);
    double res = smin(baseD, connectedDrip, 38.0);
    if (withDetachedDrop) {
      final dropCenterY = botY - bulbRadius - dropRadius - 18.0;
      final dropX = topX + sway * 0.55;
      final drop = circle(x, y, dropX, dropCenterY, dropRadius);
      final dropCone = capsule(x, y, dropX, dropCenterY + dropRadius * 1.1, dropX, dropCenterY, 7.0, dropRadius, sway: 0);
      res = math.min(res, smin(drop, dropCone, 10.0));
    }
    return res;
  }

  /// Adds an upward-flying paint splatter droplet above the letter (from the tipped bucket!)
  static double addSplashDrop(
    double baseD,
    double x,
    double y,
    double cx,
    double cy, {
    double r = 20.0,
    double tailAngleRad = -1.2,
  }) {
    final drop = circle(x, y, cx, cy, r);
    final tx = cx + math.cos(tailAngleRad) * r * 1.5;
    final ty = cy + math.sin(tailAngleRad) * r * 1.5;
    final tail = capsule(x, y, cx, cy, tx, ty, r * 0.9, 6.0, sway: 0);
    return math.min(baseD, smin(drop, tail, 8.0));
  }
}

/// Marching Squares + C1 Quadratic B-Spline Contour Extractor
class MarchingSquaresCompiler {
  static List<GlyphContour> extractContours({
    required SdfFunc sdf,
    required double xMin,
    required double yMin,
    required double xMax,
    required double yMax,
    double step = 5.0,
  }) {
    final cols = ((xMax - xMin) / step).ceil() + 1;
    final rows = ((yMax - yMin) / step).ceil() + 1;

    final grid = List.generate(rows, (r) {
      final y = yMin + r * step;
      return List.generate(cols, (c) {
        final x = xMin + c * step;
        return sdf(x, y);
      });
    });

    final segments = <(math.Point<double>, math.Point<double>)>[];

    math.Point<double> interp(double x1, double y1, double v1, double x2, double y2, double v2) {
      final denom = v1 - v2;
      final t = denom.abs() > 1e-9 ? (v1 / denom).clamp(0.05, 0.95) : 0.5;
      return math.Point<double>(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t);
    }

    for (int r = 0; r < rows - 1; r++) {
      final y0 = yMin + r * step;
      final y1 = y0 + step;
      for (int c = 0; c < cols - 1; c++) {
        final x0 = xMin + c * step;
        final x1 = x0 + step;

        final v00 = grid[r][c];
        final v10 = grid[r][c + 1];
        final v11 = grid[r + 1][c + 1];
        final v01 = grid[r + 1][c];

        int mask = 0;
        if (v00 < 0) mask |= 1;
        if (v10 < 0) mask |= 2;
        if (v11 < 0) mask |= 4;
        if (v01 < 0) mask |= 8;

        if (mask == 0 || mask == 15) continue;

        final pBottom = interp(x0, y0, v00, x1, y0, v10);
        final pRight = interp(x1, y0, v10, x1, y1, v11);
        final pTop = interp(x0, y1, v01, x1, y1, v11);
        final pLeft = interp(x0, y0, v00, x0, y1, v01);

        switch (mask) {
          case 1:
            segments.add((pBottom, pLeft));
            break;
          case 2:
            segments.add((pRight, pBottom));
            break;
          case 3:
            segments.add((pRight, pLeft));
            break;
          case 4:
            segments.add((pTop, pRight));
            break;
          case 5:
            segments.add((pBottom, pRight));
            segments.add((pTop, pLeft));
            break;
          case 6:
            segments.add((pTop, pBottom));
            break;
          case 7:
            segments.add((pTop, pLeft));
            break;
          case 8:
            segments.add((pLeft, pTop));
            break;
          case 9:
            segments.add((pBottom, pTop));
            break;
          case 10:
            segments.add((pLeft, pBottom));
            segments.add((pRight, pTop));
            break;
          case 11:
            segments.add((pRight, pTop));
            break;
          case 12:
            segments.add((pLeft, pRight));
            break;
          case 13:
            segments.add((pBottom, pRight));
            break;
          case 14:
            segments.add((pLeft, pBottom));
            break;
        }
      }
    }

    final used = List<bool>.filled(segments.length, false);
    final rawLoops = <List<math.Point<double>>>[];

    for (int i = 0; i < segments.length; i++) {
      if (used[i]) continue;
      used[i] = true;
      final loop = <math.Point<double>>[segments[i].$1, segments[i].$2];

      while (true) {
        final tail = loop.last;
        int bestIdx = -1;
        double bestDist2 = 4.0;

        for (int j = 0; j < segments.length; j++) {
          if (used[j]) continue;
          final head = segments[j].$1;
          final dx = head.x - tail.x;
          final dy = head.y - tail.y;
          final d2 = dx * dx + dy * dy;
          if (d2 < bestDist2) {
            bestDist2 = d2;
            bestIdx = j;
            if (d2 < 1e-4) break;
          }
        }

        if (bestIdx != -1) {
          used[bestIdx] = true;
          loop.add(segments[bestIdx].$2);
        } else {
          break;
        }
      }

      if (loop.length >= 8) {
        final dx = loop.last.x - loop.first.x;
        final dy = loop.last.y - loop.first.y;
        if (dx * dx + dy * dy < 4.0) {
          loop.removeLast();
        }
        rawLoops.add(loop);
      }
    }

    final contours = <GlyphContour>[];
    for (final raw in rawLoops) {
      var pts = raw;
      for (int pass = 0; pass < 1; pass++) {
        final nextPts = <math.Point<double>>[];
        final n = pts.length;
        for (int i = 0; i < n; i++) {
          final pPrev = pts[(i - 1 + n) % n];
          final pCur = pts[i];
          final pNext = pts[(i + 1) % n];
          nextPts.add(math.Point<double>(
            pCur.x * 0.64 + (pPrev.x + pNext.x) * 0.18,
            pCur.y * 0.64 + (pPrev.y + pNext.y) * 0.18,
          ));
        }
        pts = nextPts;
      }

      final controlPoly = <math.Point<double>>[];
      double accumDist = 0.0;
      controlPoly.add(pts.first);
      for (int i = 1; i < pts.length; i++) {
        final prev = controlPoly.last;
        final cur = pts[i];
        final dist = math.sqrt((cur.x - prev.x) * (cur.x - prev.x) + (cur.y - prev.y) * (cur.y - prev.y));
        accumDist += dist;
        if (accumDist >= 11.0) {
          controlPoly.add(cur);
          accumDist = 0.0;
        }
      }

      if (controlPoly.length < 4) continue;

      final contour = GlyphContour();
      final m = controlPoly.length;
      for (int i = 0; i < m; i++) {
        final p0 = controlPoly[i];
        final p1 = controlPoly[(i + 1) % m];
        final midX = ((p0.x + p1.x) * 0.5).round();
        final midY = ((p0.y + p1.y) * 0.5).round();
        final offX = p1.x.round();
        final offY = p1.y.round();

        contour.add(midX, midY, onCurve: true);
        contour.add(offX, offY, onCurve: false);
      }

      contours.add(contour);
    }

    return contours;
  }
}
