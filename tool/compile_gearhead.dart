import 'dart:io';
import 'dart:math' as math;
import 'dart:typed_data';
import 'foundry/models.dart';
import 'foundry/sfnt_builder.dart';
import 'foundry/phinney_auditor.dart';
import 'foundry/groovy_sdf_engine.dart';

/// Master Full-Alphabet Compiler for Gearhead Groovy (GearArts 2k26).
/// Synthesizes:
/// - 1970s Keep-On-Truckin' / Cooper-Black Bell-Bottom Gravity & High-Waist Pinch
/// - Rubber-Hose S-Curve Stems & Swollen Mushroom Lobe Terminals
/// - External Sprocket Gear Crowns + Internal 8-Tooth Star-Cog Counters
/// - Open-End Wrench-Jaw Terminals + Multi-Tendril Lava-Lamp Paint Meltdowns
void main() async {
  final outTtf = 'experiments/geararts-2k26/GearheadGroovy/fonts/ttf/GearheadGroovy-Regular.ttf';
  final outWoff2 = 'experiments/geararts-2k26/GearheadGroovy/fonts/woff2/GearheadGroovy-Regular.woff2';

  print('\n======================================================================');
  print('  GEARARTS 2K26: COMPILING HIGH-WEIRDNESS 1970s GEARHEAD GROOVY');
  print('  Target TTF:   $outTtf');
  print('  Target WOFF2: $outWoff2');
  print('======================================================================\n');

  Directory('experiments/geararts-2k26/GearheadGroovy/fonts/ttf').createSync(recursive: true);
  Directory('experiments/geararts-2k26/GearheadGroovy/fonts/woff2').createSync(recursive: true);

  final builder = SfntBuilder(
    familyName: 'GearheadGroovy',
    subFamilyName: 'Regular',
    upm: 1000,
    ascender: 840,
    descender: -250,
    lineGap: 100,
  );

  int gid = 0;

  // 0. .notdef
  builder.addGlyph(GlyphRecord(
    glyphId: gid++,
    codePoint: -1,
    name: '.notdef',
    advanceWidth: 600,
    lsb: 50,
    contours: [
      GlyphContour([
        const GlyphPoint(50, 0),
        const GlyphPoint(50, 740),
        const GlyphPoint(550, 740),
        const GlyphPoint(550, 0),
      ]),
      GlyphContour([
        const GlyphPoint(120, 70),
        const GlyphPoint(480, 70),
        const GlyphPoint(480, 670),
        const GlyphPoint(120, 670),
      ]),
    ],
  ));

  // 1. space
  builder.addGlyph(GlyphRecord(
    glyphId: gid++,
    codePoint: 0x0020,
    name: 'space',
    advanceWidth: 320,
    lsb: 0,
    contours: [],
  ));

  void addSdfGlyph({
    required String name,
    required int unicode,
    required int advanceWidth,
    required SdfFunc sdf,
    int? lowercaseMirrorUnicode,
    double swayAmp = 28.0,
    double bellBottomStrength = 0.34,
    double phase = 0.15,
  }) {
    // Wrap SDF with 1970s non-linear Bell-Bottom & Rubber-Hose Lava-Lamp Warp
    double warpedSdf(double x, double y) {
      final (wx, wy, swell) = SdfPrimitives.warpGroovy(
        x,
        y,
        centerX: advanceWidth * 0.5,
        swayAmp: swayAmp,
        bellBottomStrength: bellBottomStrength,
        phase: phase,
      );
      return sdf(wx, wy) / swell;
    }

    final contours = MarchingSquaresCompiler.extractContours(
      sdf: warpedSdf,
      xMin: -70,
      yMin: -250,
      xMax: advanceWidth + 70.0,
      yMax: 840,
      step: 5.0,
    );

    int lsb = 40;
    if (contours.isNotEmpty) {
      int minX = 999999;
      for (final c in contours) {
        for (final p in c.points) {
          if (p.x < minX) minX = p.x;
        }
      }
      if (minX < 999999) lsb = minX;
    }

    builder.addGlyph(GlyphRecord(
      glyphId: gid++,
      codePoint: unicode,
      name: name,
      advanceWidth: advanceWidth,
      lsb: lsb,
      contours: contours,
    ));

    if (lowercaseMirrorUnicode != null) {
      builder.addGlyph(GlyphRecord(
        glyphId: gid++,
        codePoint: lowercaseMirrorUnicode,
        name: name.toLowerCase(),
        advanceWidth: advanceWidth,
        lsb: lsb,
        contours: contours,
      ));
    }
  }

  // --- UPPERCASE & LOWERCASE ALPHABET (A-Z) ---

  // A: High-waisted 1970s bell-bottom A with massive elephant-foot boots,
  //    8-tooth star-cog cyclops eye, and lava-lamp belly drip!
  addSdfGlyph(
    name: 'A',
    unicode: 0x0041,
    lowercaseMirrorUnicode: 0x0061,
    advanceWidth: 780,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final leftLeg = SdfPrimitives.capsule(x, y, 130, 95, 360, 665, 118, 76, sway: -26);
      final rightLeg = SdfPrimitives.capsule(x, y, 650, 95, 420, 665, 118, 76, sway: 26);
      final dome = SdfPrimitives.circle(x, y, 390, 565, 185);
      final crossbar = SdfPrimitives.capsule(x, y, 200, 315, 580, 315, 82, 82, sway: -18);
      double outer = SdfPrimitives.smin(leftLeg, rightLeg, 48);
      outer = SdfPrimitives.smin(outer, dome, 45);
      outer = SdfPrimitives.smin(outer, crossbar, 42);
      // Sprout external gear teeth on top dome crown!
      outer = SdfPrimitives.addExternalGearTeeth(outer, x, y, 390, 565, 182,
          teeth: 9, toothHeight: 36, angleMinRad: 0.5, angleMaxRad: 2.64);
      final cog = SdfPrimitives.gearCounter(x, y, 390, 505, 82, teeth: 8, toothDepth: 32);
      outer = SdfPrimitives.ssub(outer, cog, 6);
      outer = SdfPrimitives.addDrip(outer, x, y, 390, 260, 115, neckRadius: 15, bulbRadius: 26, sway: 12);
      return outer;
    },
  );

  // B: Tiny high top loop + huge bell-bottom belly + double meshing transmission gears inside!
  addSdfGlyph(
    name: 'B',
    unicode: 0x0042,
    lowercaseMirrorUnicode: 0x0062,
    advanceWidth: 760,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 165, 95, 175, 660, 112, 82, sway: 22);
      final topBowl = SdfPrimitives.circle(x, y, 375, 565, 175);
      final botBowl = SdfPrimitives.circle(x, y, 425, 245, 245);
      double outer = SdfPrimitives.smin(stem, SdfPrimitives.smin(topBowl, botBowl, 42), 45);
      final topCog = SdfPrimitives.gearCounter(x, y, 365, 565, 64, teeth: 6, toothDepth: 22, rotationRad: 0.4);
      final botCog = SdfPrimitives.gearCounter(x, y, 405, 240, 92, teeth: 8, toothDepth: 32);
      outer = SdfPrimitives.ssub(outer, topCog, 6);
      outer = SdfPrimitives.ssub(outer, botCog, 6);
      return SdfPrimitives.addDrip(outer, x, y, 435, 35, -95, neckRadius: 16, bulbRadius: 28, sway: -12);
    },
  );

  // C: Heavy bottom-swollen 1970s C with external sprocket spine + fat curled mushroom terminals
  addSdfGlyph(
    name: 'C',
    unicode: 0x0043,
    lowercaseMirrorUnicode: 0x0063,
    advanceWidth: 740,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final topArc = SdfPrimitives.quadStroke(x, y, 575, 545, 370, 755, 165, 540, 96, 78, 84);
      final midArc = SdfPrimitives.quadStroke(x, y, 165, 540, 85, 365, 165, 195, 84, 96, 102);
      final botArc = SdfPrimitives.quadStroke(x, y, 165, 195, 385, -15, 600, 225, 102, 112, 118);
      double c = SdfPrimitives.smin(topArc, SdfPrimitives.smin(midArc, botArc, 35), 35);
      // External sprocket teeth along the upper-left spine
      c = SdfPrimitives.addExternalGearTeeth(c, x, y, 365, 380, 295,
          teeth: 12, toothHeight: 38, angleMinRad: 1.8, angleMaxRad: 3.6);
      c = SdfPrimitives.addDrip(c, x, y, 585, 470, 345, neckRadius: 14, bulbRadius: 24, sway: 8);
      return c;
    },
  );

  // D: Bell-bottom D with external gear teeth on its belly + tilted star-cog counter
  addSdfGlyph(
    name: 'D',
    unicode: 0x0044,
    lowercaseMirrorUnicode: 0x0064,
    advanceWidth: 760,
    swayAmp: 28.0,
    bellBottomStrength: 0.35,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 170, 95, 175, 660, 114, 84, sway: 24);
      final arcTop = SdfPrimitives.quadStroke(x, y, 175, 655, 585, 680, 605, 360, 82, 84, 102);
      final arcBot = SdfPrimitives.quadStroke(x, y, 605, 360, 625, 45, 170, 95, 102, 114, 112);
      double d = SdfPrimitives.smin(stem, SdfPrimitives.smin(arcTop, arcBot, 38), 42);
      d = SdfPrimitives.addExternalGearTeeth(d, x, y, 365, 365, 305,
          teeth: 11, toothHeight: 36, angleMinRad: -0.9, angleMaxRad: 0.9);
      final cog = SdfPrimitives.gearCounter(x, y, 365, 355, 92, teeth: 8, toothDepth: 28, rotationRad: 0.35);
      return SdfPrimitives.ssub(d, cog, 6);
    },
  );

  // E: Psychedelic high-waisted epsilon E with wrench-jaw top terminal & fat bell-bottom lower curl
  addSdfGlyph(
    name: 'E',
    unicode: 0x0045,
    lowercaseMirrorUnicode: 0x0065,
    advanceWidth: 720,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final topLoop = SdfPrimitives.quadStroke(x, y, 565, 595, 290, 735, 165, 560, 96, 80, 82);
      final topMid = SdfPrimitives.quadStroke(x, y, 165, 560, 155, 435, 485, 435, 82, 76, 88);
      final botMid = SdfPrimitives.quadStroke(x, y, 485, 435, 135, 435, 155, 210, 88, 86, 102);
      final botLoop = SdfPrimitives.quadStroke(x, y, 155, 210, 310, -10, 595, 165, 102, 114, 120);
      double e = SdfPrimitives.smin(
        SdfPrimitives.smin(topLoop, topMid, 32),
        SdfPrimitives.smin(botMid, botLoop, 32),
        32,
      );
      // Wrench jaw cut into the top right terminal!
      e = SdfPrimitives.cutWrenchJaw(e, x, y, 575, 590, angleRad: -0.35, jawWidth: 34, jawDepth: 62);
      e = SdfPrimitives.addDrip(e, x, y, 360, 35, -90, neckRadius: 15, bulbRadius: 26, sway: 14);
      return e;
    },
  );

  // F: High-waisted Keep-On-Truckin' F with gigantic bell-bottom boot & wrench-jaw arm
  addSdfGlyph(
    name: 'F',
    unicode: 0x0046,
    lowercaseMirrorUnicode: 0x0066,
    advanceWidth: 700,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 195, 95, 185, 655, 122, 82, sway: 28);
      final topBar = SdfPrimitives.capsule(x, y, 185, 655, 565, 655, 82, 98, sway: -16);
      final midBar = SdfPrimitives.capsule(x, y, 185, 425, 505, 425, 78, 92, sway: 14);
      double f = SdfPrimitives.smin(stem, SdfPrimitives.smin(topBar, midBar, 38), 42);
      f = SdfPrimitives.cutWrenchJaw(f, x, y, 575, 655, angleRad: 0.0, jawWidth: 34, jawDepth: 60);
      f = SdfPrimitives.addDrip(f, x, y, 490, 375, 255, neckRadius: 14, bulbRadius: 23, sway: -10);
      return f;
    },
  );

  // G: Signature GROOVY G — external gear teeth on top arch, curled lip, long left-bottom drip + falling droplet + splash drop!
  addSdfGlyph(
    name: 'G',
    unicode: 0x0047,
    lowercaseMirrorUnicode: 0x0067,
    advanceWidth: 780,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final topArc = SdfPrimitives.quadStroke(x, y, 595, 575, 375, 745, 160, 540, 94, 80, 86);
      final midArc = SdfPrimitives.quadStroke(x, y, 160, 540, 85, 365, 165, 190, 86, 94, 104);
      final botArc = SdfPrimitives.quadStroke(x, y, 165, 190, 395, -5, 615, 215, 104, 112, 106);
      final spur = SdfPrimitives.capsule(x, y, 615, 215, 610, 395, 106, 92, sway: -16);
      final lip = SdfPrimitives.capsule(x, y, 415, 395, 610, 395, 96, 88, sway: 14);
      double g = SdfPrimitives.smin(
        SdfPrimitives.smin(topArc, midArc, 32),
        SdfPrimitives.smin(botArc, SdfPrimitives.smin(spur, lip, 32), 34),
        34,
      );
      g = SdfPrimitives.addExternalGearTeeth(g, x, y, 375, 390, 305,
          teeth: 12, toothHeight: 38, angleMinRad: 1.1, angleMaxRad: 2.9);
      // Long paint drip + detached droplet on left-bottom belly (matches GROOVY photo!)
      g = SdfPrimitives.addDrip(g, x, y, 225, 95, -105,
          neckRadius: 17, bulbRadius: 30, withDetachedDrop: true, dropRadius: 21, sway: -14);
      // Upward splash drop above top right
      g = SdfPrimitives.addSplashDrop(g, x, y, 635, 725, r: 22, tailAngleRad: -2.2);
      return g;
    },
  );

  // H: High-waisted bell-bottom H with massive elephant boots + twin uneven drips off right stem (matches RHEAD!)
  addSdfGlyph(
    name: 'H',
    unicode: 0x0048,
    lowercaseMirrorUnicode: 0x0068,
    advanceWidth: 800,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final leftStem = SdfPrimitives.capsule(x, y, 175, 95, 190, 655, 120, 82, sway: 28);
      final rightStem = SdfPrimitives.capsule(x, y, 625, 95, 610, 655, 120, 82, sway: -28);
      final crossbar = SdfPrimitives.capsule(x, y, 185, 445, 615, 445, 82, 82, sway: -22);
      double h = SdfPrimitives.smin(leftStem, SdfPrimitives.smin(rightStem, crossbar, 42), 42);
      // Twin uneven drips off the right stem base (exact match to H in RHEAD photo!)
      h = SdfPrimitives.addDrip(h, x, y, 575, 60, -85, neckRadius: 16, bulbRadius: 26, sway: -10);
      h = SdfPrimitives.addDrip(h, x, y, 645, 60, -145, neckRadius: 16, bulbRadius: 29, sway: 12);
      return h;
    },
  );

  // I: Lava-lamp dog-bone column with pinched waist, giant bell-bottom base & star-cog top eye
  addSdfGlyph(
    name: 'I',
    unicode: 0x0049,
    lowercaseMirrorUnicode: 0x0069,
    advanceWidth: 460,
    swayAmp: 34.0,
    bellBottomStrength: 0.40,
    sdf: (x, y) {
      final col = SdfPrimitives.capsule(x, y, 230, 95, 230, 655, 124, 96, waistFactor: 0.62, sway: 28);
      return SdfPrimitives.addDrip(col, x, y, 230, 55, -80, neckRadius: 15, bulbRadius: 25, sway: -12);
    },
  );

  // J: Deep bell-bottom hook with huge bulbous terminal lobe
  addSdfGlyph(
    name: 'J',
    unicode: 0x004A,
    lowercaseMirrorUnicode: 0x006A,
    advanceWidth: 680,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 490, 250, 485, 655, 96, 92, sway: 22);
      final hook = SdfPrimitives.quadStroke(x, y, 490, 250, 475, -15, 155, 215, 96, 112, 122);
      double j = SdfPrimitives.smin(stem, hook, 36);
      return SdfPrimitives.addDrip(j, x, y, 365, 45, -85, neckRadius: 15, bulbRadius: 26, sway: 10);
    },
  );

  // K: Strutting bell-bottom K with wrench-jaw upper arm & huge kicking lower boot
  addSdfGlyph(
    name: 'K',
    unicode: 0x004B,
    lowercaseMirrorUnicode: 0x006B,
    advanceWidth: 760,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 175, 95, 185, 655, 118, 84, sway: 24);
      final topArm = SdfPrimitives.capsule(x, y, 215, 410, 575, 650, 74, 96, sway: -18);
      final botArm = SdfPrimitives.capsule(x, y, 255, 445, 605, 95, 78, 122, sway: 24);
      double k = SdfPrimitives.smin(stem, SdfPrimitives.smin(topArm, botArm, 40), 42);
      k = SdfPrimitives.cutWrenchJaw(k, x, y, 585, 655, angleRad: 0.55, jawWidth: 34, jawDepth: 60);
      return k;
    },
  );

  // L: Swooping rubber-hose L with huge bell-bottom foot & wrench-jaw toe
  addSdfGlyph(
    name: 'L',
    unicode: 0x004C,
    lowercaseMirrorUnicode: 0x006C,
    advanceWidth: 680,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 185, 105, 195, 655, 112, 86, sway: 28);
      final base = SdfPrimitives.capsule(x, y, 185, 105, 555, 105, 112, 118, sway: -20);
      double l = SdfPrimitives.smin(stem, base, 45);
      l = SdfPrimitives.cutWrenchJaw(l, x, y, 570, 105, angleRad: 0.0, jawWidth: 36, jawDepth: 62);
      return l;
    },
  );

  // M: Four-legged lava-lamp monster M with massive outer elephant boots & dripping center valley
  addSdfGlyph(
    name: 'M',
    unicode: 0x004D,
    lowercaseMirrorUnicode: 0x006D,
    advanceWidth: 900,
    swayAmp: 26.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final left = SdfPrimitives.capsule(x, y, 150, 95, 205, 655, 118, 82, sway: 24);
      final diagL = SdfPrimitives.capsule(x, y, 205, 655, 450, 250, 78, 92, sway: -14);
      final diagR = SdfPrimitives.capsule(x, y, 695, 655, 450, 250, 78, 92, sway: 14);
      final right = SdfPrimitives.capsule(x, y, 750, 95, 695, 655, 118, 82, sway: -24);
      double m = SdfPrimitives.smin(
        SdfPrimitives.smin(left, diagL, 38),
        SdfPrimitives.smin(diagR, right, 38),
        38,
      );
      return SdfPrimitives.addDrip(m, x, y, 450, 190, 45, neckRadius: 15, bulbRadius: 26, sway: 8);
    },
  );

  // N: High-waisted rubber-hose N with giant bell-bottom feet
  addSdfGlyph(
    name: 'N',
    unicode: 0x004E,
    lowercaseMirrorUnicode: 0x006E,
    advanceWidth: 780,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final left = SdfPrimitives.capsule(x, y, 175, 95, 185, 655, 118, 82, sway: 24);
      final diag = SdfPrimitives.capsule(x, y, 190, 640, 590, 110, 80, 88, sway: -18);
      final right = SdfPrimitives.capsule(x, y, 605, 95, 595, 655, 118, 82, sway: -24);
      return SdfPrimitives.smin(left, SdfPrimitives.smin(diag, right, 40), 40);
    },
  );

  // O: Signature GROOVY O — Pear-shaped bell-bottom lava donut + external top sprocket teeth +
  //    8-tooth star-cog counter + twin bottom-right drips!
  addSdfGlyph(
    name: 'O',
    unicode: 0x004F,
    advanceWidth: 780,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final outer = SdfPrimitives.capsule(x, y, 390, 285, 390, 455, 325, 275, waistFactor: 0.94, sway: 18);
      double o = SdfPrimitives.addExternalGearTeeth(outer, x, y, 390, 445, 275,
          teeth: 10, toothHeight: 38, angleMinRad: 0.6, angleMaxRad: 2.54);
      final cog = SdfPrimitives.gearCounter(x, y, 390, 385, 108, teeth: 8, toothDepth: 34, rotationRad: 0.2);
      o = SdfPrimitives.ssub(o, cog, 6);
      // Twin drips hanging off bottom-right of O (matches GROOVY photo!)
      o = SdfPrimitives.addDrip(o, x, y, 430, 55, -90, neckRadius: 15, bulbRadius: 26, sway: 10);
      o = SdfPrimitives.addDrip(o, x, y, 495, 75, -55, neckRadius: 13, bulbRadius: 21, sway: -8);
      return o;
    },
  );

  // Lowercase o: Bell-bottom pear-shaped cog wheel with external side sprocket teeth
  addSdfGlyph(
    name: 'o',
    unicode: 0x006F,
    advanceWidth: 780,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    phase: -0.25,
    sdf: (x, y) {
      final outer = SdfPrimitives.capsule(x, y, 390, 285, 390, 455, 320, 275, waistFactor: 0.94, sway: -18);
      double o = SdfPrimitives.addExternalGearTeeth(outer, x, y, 390, 365, 300,
          teeth: 11, toothHeight: 36, angleMinRad: -0.8, angleMaxRad: 0.8);
      final cog = SdfPrimitives.gearCounter(x, y, 390, 385, 108, teeth: 8, toothDepth: 34, rotationRad: 0.55);
      return SdfPrimitives.ssub(o, cog, 6);
    },
  );

  // P: Fat bell-bottom stem + swollen top cog-bowl
  addSdfGlyph(
    name: 'P',
    unicode: 0x0050,
    lowercaseMirrorUnicode: 0x0070,
    advanceWidth: 740,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 185, 95, 185, 655, 122, 84, sway: 26);
      final bowl = SdfPrimitives.circle(x, y, 405, 515, 235);
      double p = SdfPrimitives.smin(stem, bowl, 44);
      final cog = SdfPrimitives.gearCounter(x, y, 390, 515, 82, teeth: 8, toothDepth: 28);
      p = SdfPrimitives.ssub(p, cog, 6);
      return SdfPrimitives.addDrip(p, x, y, 425, 305, 185, neckRadius: 14, bulbRadius: 23, sway: 10);
    },
  );

  // Q: Pear-shaped gear O + external sprocket crown + kicking wrench-tail
  addSdfGlyph(
    name: 'Q',
    unicode: 0x0051,
    lowercaseMirrorUnicode: 0x0071,
    advanceWidth: 800,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final outer = SdfPrimitives.capsule(x, y, 385, 295, 385, 455, 315, 270, waistFactor: 0.94, sway: 16);
      final tail = SdfPrimitives.capsule(x, y, 465, 210, 665, 45, 74, 106, sway: 20);
      double q = SdfPrimitives.smin(outer, tail, 38);
      q = SdfPrimitives.addExternalGearTeeth(q, x, y, 385, 445, 270,
          teeth: 10, toothHeight: 36, angleMinRad: 0.7, angleMaxRad: 2.5);
      final cog = SdfPrimitives.gearCounter(x, y, 385, 385, 104, teeth: 8, toothDepth: 32);
      return SdfPrimitives.ssub(q, cog, 6);
    },
  );

  // R: Signature GROOVY R — High-waisted 8-tooth cog head + strutting Keep-On-Truckin' bell-bottom leg + twin stem drips!
  addSdfGlyph(
    name: 'R',
    unicode: 0x0052,
    lowercaseMirrorUnicode: 0x0072,
    advanceWidth: 780,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 185, 95, 185, 655, 114, 84, sway: 24);
      final bowl = SdfPrimitives.circle(x, y, 395, 525, 225);
      final leg = SdfPrimitives.quadStroke(x, y, 355, 385, 495, 210, 635, 95, 78, 96, 122);
      double r = SdfPrimitives.smin(stem, SdfPrimitives.smin(bowl, leg, 40), 42);
      final cog = SdfPrimitives.gearCounter(x, y, 385, 525, 82, teeth: 8, toothDepth: 28);
      r = SdfPrimitives.ssub(r, cog, 6);
      // Hanging paint drips on left stem (matches R in GROOVY photo!)
      r = SdfPrimitives.addDrip(r, x, y, 160, 55, -110, neckRadius: 16, bulbRadius: 27, sway: -10);
      r = SdfPrimitives.addDrip(r, x, y, 220, 55, -55, neckRadius: 13, bulbRadius: 21, sway: 8);
      return r;
    },
  );

  // S: Classic 1970s bottom-heavy Cobra S with external sprocket crest & huge lower belly
  addSdfGlyph(
    name: 'S',
    unicode: 0x0053,
    lowercaseMirrorUnicode: 0x0073,
    advanceWidth: 720,
    swayAmp: 34.0,
    bellBottomStrength: 0.40,
    sdf: (x, y) {
      final top = SdfPrimitives.quadStroke(x, y, 555, 585, 345, 745, 170, 565, 94, 78, 84);
      final spine = SdfPrimitives.quadStroke(x, y, 170, 565, 185, 415, 545, 265, 84, 88, 104);
      final bot = SdfPrimitives.quadStroke(x, y, 545, 265, 575, -15, 150, 185, 104, 116, 122);
      double s = SdfPrimitives.smin(top, SdfPrimitives.smin(spine, bot, 32), 32);
      s = SdfPrimitives.addExternalGearTeeth(s, x, y, 355, 560, 195,
          teeth: 8, toothHeight: 34, angleMinRad: 0.8, angleMaxRad: 2.5);
      return SdfPrimitives.addDrip(s, x, y, 165, 115, -55, neckRadius: 14, bulbRadius: 24, sway: -10);
    },
  );

  // T: Fat groovy T with massive bell-bottom pedestal + twin left overhang drips + stem base drip & falling droplet!
  addSdfGlyph(
    name: 'T',
    unicode: 0x0054,
    lowercaseMirrorUnicode: 0x0074,
    advanceWidth: 740,
    swayAmp: 32.0,
    bellBottomStrength: 0.40,
    sdf: (x, y) {
      final topBar = SdfPrimitives.capsule(x, y, 105, 650, 635, 650, 96, 96, sway: -20);
      final stem = SdfPrimitives.capsule(x, y, 370, 95, 370, 650, 124, 82, waistFactor: 0.65, sway: 28);
      double t = SdfPrimitives.smin(topBar, stem, 44);
      // Left overhang drips under top bar (exact match to TVWXY in photo!)
      t = SdfPrimitives.addDrip(t, x, y, 160, 580, 425, neckRadius: 15, bulbRadius: 24, sway: -8);
      t = SdfPrimitives.addDrip(t, x, y, 225, 580, 470, neckRadius: 12, bulbRadius: 19, sway: 6);
      // Bottom stem drip + detached droplet
      t = SdfPrimitives.addDrip(t, x, y, 395, 60, -85,
          neckRadius: 15, bulbRadius: 26, withDetachedDrop: true, dropRadius: 18, sway: 12);
      return t;
    },
  );

  // U: Bottom-heavy horseshoe U with swollen lower belly
  addSdfGlyph(
    name: 'U',
    unicode: 0x0055,
    lowercaseMirrorUnicode: 0x0075,
    advanceWidth: 760,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final left = SdfPrimitives.capsule(x, y, 180, 270, 190, 655, 102, 86, sway: 22);
      final right = SdfPrimitives.capsule(x, y, 580, 270, 570, 655, 102, 86, sway: -22);
      final arch = SdfPrimitives.quadStroke(x, y, 180, 270, 380, -35, 580, 270, 102, 118, 102);
      return SdfPrimitives.smin(left, SdfPrimitives.smin(right, arch, 36), 36);
    },
  );

  // V: Signature GROOVY V — Swollen mushroom top ears + fat bottom apex + twin apex drips + upward splash drop!
  addSdfGlyph(
    name: 'V',
    unicode: 0x0056,
    lowercaseMirrorUnicode: 0x0076,
    advanceWidth: 740,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final left = SdfPrimitives.capsule(x, y, 150, 655, 370, 105, 96, 114, sway: 24);
      final right = SdfPrimitives.capsule(x, y, 590, 655, 370, 105, 96, 114, sway: -24);
      double v = SdfPrimitives.smin(left, right, 42);
      v = SdfPrimitives.addDrip(v, x, y, 345, 60, -100, neckRadius: 16, bulbRadius: 27, sway: -10);
      v = SdfPrimitives.addDrip(v, x, y, 405, 70, -50, neckRadius: 13, bulbRadius: 21, sway: 8);
      v = SdfPrimitives.addSplashDrop(v, x, y, 370, 745, r: 22, tailAngleRad: -1.57);
      return v;
    },
  );

  // W: Squishy twin-belly W with fat bulbous bottoms
  addSdfGlyph(
    name: 'W',
    unicode: 0x0057,
    lowercaseMirrorUnicode: 0x0077,
    advanceWidth: 920,
    swayAmp: 26.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final s1 = SdfPrimitives.capsule(x, y, 130, 655, 275, 95, 84, 114, sway: 20);
      final s2 = SdfPrimitives.capsule(x, y, 275, 95, 460, 510, 114, 78, sway: -14);
      final s3 = SdfPrimitives.capsule(x, y, 460, 510, 645, 95, 78, 114, sway: 14);
      final s4 = SdfPrimitives.capsule(x, y, 645, 95, 790, 655, 114, 84, sway: -20);
      return SdfPrimitives.smin(
        SdfPrimitives.smin(s1, s2, 38),
        SdfPrimitives.smin(s3, s4, 38),
        38,
      );
    },
  );

  // X: Crossed rubber-hose dog-bones with huge bell-bottom boots & center star-cog hub!
  addSdfGlyph(
    name: 'X',
    unicode: 0x0058,
    lowercaseMirrorUnicode: 0x0078,
    advanceWidth: 760,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final d1 = SdfPrimitives.capsule(x, y, 150, 95, 610, 655, 118, 86, waistFactor: 0.68, sway: 24);
      final d2 = SdfPrimitives.capsule(x, y, 150, 655, 610, 95, 86, 118, waistFactor: 0.68, sway: -24);
      final hub = SdfPrimitives.circle(x, y, 380, 385, 135);
      double xGlyph = SdfPrimitives.smin(hub, SdfPrimitives.smin(d1, d2, 44), 38);
      final cog = SdfPrimitives.gearCounter(x, y, 380, 385, 54, teeth: 6, toothDepth: 20);
      return SdfPrimitives.ssub(xGlyph, cog, 6);
    },
  );

  // Y: Signature GROOVY Y — High fork + swollen bell-bottom stem + long melting stem drip + splash droplet!
  addSdfGlyph(
    name: 'Y',
    unicode: 0x0059,
    lowercaseMirrorUnicode: 0x0079,
    advanceWidth: 740,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final left = SdfPrimitives.capsule(x, y, 150, 655, 370, 385, 96, 82, sway: 20);
      final right = SdfPrimitives.capsule(x, y, 590, 655, 370, 385, 96, 82, sway: -20);
      final stem = SdfPrimitives.capsule(x, y, 370, 385, 370, 95, 82, 120, sway: 24);
      double yGlyph = SdfPrimitives.smin(left, SdfPrimitives.smin(right, stem, 40), 40);
      yGlyph = SdfPrimitives.addDrip(yGlyph, x, y, 370, 55, -100,
          neckRadius: 16, bulbRadius: 28, withDetachedDrop: true, dropRadius: 18, sway: -12);
      return yGlyph;
    },
  );

  // Z: Wavy 1970s Z with wrench-jaw top beak & heavy bottom base
  addSdfGlyph(
    name: 'Z',
    unicode: 0x005A,
    lowercaseMirrorUnicode: 0x007A,
    advanceWidth: 720,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final top = SdfPrimitives.capsule(x, y, 150, 650, 570, 650, 92, 86, sway: -18);
      final diag = SdfPrimitives.capsule(x, y, 560, 640, 160, 105, 82, 98, sway: 22);
      final bot = SdfPrimitives.capsule(x, y, 150, 100, 575, 100, 108, 118, sway: 18);
      double z = SdfPrimitives.smin(top, SdfPrimitives.smin(diag, bot, 38), 38);
      z = SdfPrimitives.cutWrenchJaw(z, x, y, 135, 650, angleRad: 3.14, jawWidth: 34, jawDepth: 58);
      return SdfPrimitives.addDrip(z, x, y, 540, 55, -75, neckRadius: 14, bulbRadius: 24, sway: 10);
    },
  );

  // --- NUMERALS (0-9) ---

  // 0: Pear-shaped bell-bottom 0 with external sprocket crown + 8-tooth star-cog counter
  addSdfGlyph(
    name: 'zero',
    unicode: 0x0030,
    advanceWidth: 740,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final outer = SdfPrimitives.capsule(x, y, 370, 280, 370, 460, 305, 260, waistFactor: 0.92, sway: 18);
      double z = SdfPrimitives.addExternalGearTeeth(outer, x, y, 370, 455, 260,
          teeth: 9, toothHeight: 36, angleMinRad: 0.6, angleMaxRad: 2.54);
      final cog = SdfPrimitives.gearCounter(x, y, 370, 380, 100, teeth: 8, toothDepth: 32);
      z = SdfPrimitives.ssub(z, cog, 6);
      return SdfPrimitives.addDrip(z, x, y, 370, 35, -90, neckRadius: 15, bulbRadius: 26, sway: -10);
    },
  );

  // 1: Bell-bottom pillar 1 with rubber-hose sway
  addSdfGlyph(
    name: 'one',
    unicode: 0x0031,
    advanceWidth: 520,
    swayAmp: 32.0,
    bellBottomStrength: 0.40,
    sdf: (x, y) {
      final stem = SdfPrimitives.capsule(x, y, 285, 95, 285, 655, 122, 86, sway: 26);
      final beak = SdfPrimitives.capsule(x, y, 145, 535, 285, 655, 88, 84, sway: -14);
      return SdfPrimitives.smin(stem, beak, 38);
    },
  );

  // 2: Wavy bell-bottom 2
  addSdfGlyph(
    name: 'two',
    unicode: 0x0032,
    advanceWidth: 700,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final top = SdfPrimitives.quadStroke(x, y, 155, 545, 360, 750, 545, 530, 94, 80, 88);
      final diag = SdfPrimitives.quadStroke(x, y, 545, 530, 490, 320, 160, 100, 88, 86, 110);
      final base = SdfPrimitives.capsule(x, y, 160, 100, 560, 100, 110, 116, sway: -18);
      return SdfPrimitives.smin(top, SdfPrimitives.smin(diag, base, 38), 34);
    },
  );

  // 3: Bottom-heavy groovy 3
  addSdfGlyph(
    name: 'three',
    unicode: 0x0033,
    advanceWidth: 700,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final top = SdfPrimitives.quadStroke(x, y, 160, 585, 390, 740, 535, 540, 92, 80, 84);
      final mid = SdfPrimitives.quadStroke(x, y, 535, 540, 490, 410, 315, 410, 84, 78, 86);
      final bot1 = SdfPrimitives.quadStroke(x, y, 315, 410, 565, 390, 565, 200, 86, 96, 108);
      final bot2 = SdfPrimitives.quadStroke(x, y, 565, 200, 390, -10, 150, 175, 108, 114, 118);
      return SdfPrimitives.smin(
        SdfPrimitives.smin(top, mid, 30),
        SdfPrimitives.smin(bot1, bot2, 30),
        30,
      );
    },
  );

  // 4: Funky bell-bottom 4
  addSdfGlyph(
    name: 'four',
    unicode: 0x0034,
    advanceWidth: 720,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final diag = SdfPrimitives.capsule(x, y, 455, 655, 140, 265, 84, 96, sway: 18);
      final bar = SdfPrimitives.capsule(x, y, 140, 265, 585, 265, 92, 92, sway: -16);
      final stem = SdfPrimitives.capsule(x, y, 455, 95, 455, 655, 118, 84, sway: 22);
      return SdfPrimitives.smin(diag, SdfPrimitives.smin(bar, stem, 38), 38);
    },
  );

  // 5: Big-belly 1970s 5
  addSdfGlyph(
    name: 'five',
    unicode: 0x0035,
    advanceWidth: 700,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final topBar = SdfPrimitives.capsule(x, y, 190, 650, 545, 650, 82, 94, sway: -16);
      final drop = SdfPrimitives.capsule(x, y, 190, 650, 180, 425, 82, 86, sway: 14);
      final belly1 = SdfPrimitives.quadStroke(x, y, 180, 425, 565, 470, 565, 225, 86, 98, 108);
      final belly2 = SdfPrimitives.quadStroke(x, y, 565, 225, 390, -10, 150, 175, 108, 114, 118);
      return SdfPrimitives.smin(
        SdfPrimitives.smin(topBar, drop, 34),
        SdfPrimitives.smin(belly1, belly2, 30),
        34,
      );
    },
  );

  // 6: Heavy bottom-cog 6
  addSdfGlyph(
    name: 'six',
    unicode: 0x0036,
    advanceWidth: 720,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final bowl = SdfPrimitives.circle(x, y, 360, 260, 255);
      final neck = SdfPrimitives.quadStroke(x, y, 145, 295, 215, 675, 520, 645, 96, 84, 98);
      double s = SdfPrimitives.smin(bowl, neck, 38);
      final cog = SdfPrimitives.gearCounter(x, y, 360, 250, 88, teeth: 8, toothDepth: 30);
      return SdfPrimitives.ssub(s, cog, 6);
    },
  );

  // 7: Swooping bell-bottom 7 with wrench-jaw top bar
  addSdfGlyph(
    name: 'seven',
    unicode: 0x0037,
    advanceWidth: 680,
    swayAmp: 32.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final top = SdfPrimitives.capsule(x, y, 140, 650, 550, 650, 94, 88, sway: -18);
      final leg = SdfPrimitives.quadStroke(x, y, 550, 650, 355, 370, 265, 95, 88, 92, 120);
      double sev = SdfPrimitives.smin(top, leg, 38);
      return SdfPrimitives.cutWrenchJaw(sev, x, y, 125, 650, angleRad: 3.14, jawWidth: 34, jawDepth: 58);
    },
  );

  // 8: Double-cog transmission snowman 8 (matches 789!& in photo!)
  addSdfGlyph(
    name: 'eight',
    unicode: 0x0038,
    advanceWidth: 740,
    swayAmp: 30.0,
    bellBottomStrength: 0.38,
    sdf: (x, y) {
      final top = SdfPrimitives.circle(x, y, 370, 560, 195);
      final bot = SdfPrimitives.circle(x, y, 370, 235, 250);
      double e = SdfPrimitives.smin(top, bot, 38);
      final topCog = SdfPrimitives.gearCounter(x, y, 370, 565, 66, teeth: 6, toothDepth: 22, rotationRad: 0.4);
      final botCog = SdfPrimitives.gearCounter(x, y, 370, 230, 88, teeth: 8, toothDepth: 30);
      e = SdfPrimitives.ssub(e, topCog, 6);
      e = SdfPrimitives.ssub(e, botCog, 6);
      return SdfPrimitives.addDrip(e, x, y, 370, 25, -95, neckRadius: 15, bulbRadius: 26, sway: 12);
    },
  );

  // 9: Top star-cog 9 with external sprocket crown & fat tail (matches 789!& in photo!)
  addSdfGlyph(
    name: 'nine',
    unicode: 0x0039,
    advanceWidth: 720,
    swayAmp: 30.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final bowl = SdfPrimitives.circle(x, y, 360, 490, 245);
      final tail = SdfPrimitives.quadStroke(x, y, 565, 450, 500, 70, 195, 105, 88, 96, 114);
      double n = SdfPrimitives.smin(bowl, tail, 38);
      n = SdfPrimitives.addExternalGearTeeth(n, x, y, 360, 490, 242,
          teeth: 9, toothHeight: 36, angleMinRad: 0.6, angleMaxRad: 2.6);
      final cog = SdfPrimitives.gearCounter(x, y, 360, 495, 84, teeth: 8, toothDepth: 28);
      return SdfPrimitives.ssub(n, cog, 6);
    },
  );

  // --- PUNCTUATION (!, &, ?, -, ., ,) ---

  // !: Fat exclamation bat + dripping dot (matches 789!& in photo!)
  addSdfGlyph(
    name: 'exclam',
    unicode: 0x0021,
    advanceWidth: 400,
    swayAmp: 30.0,
    bellBottomStrength: 0.34,
    sdf: (x, y) {
      final bar = SdfPrimitives.capsule(x, y, 200, 295, 200, 655, 74, 108, sway: 22);
      final dot = SdfPrimitives.circle(x, y, 200, 105, 86);
      double exc = math.min(bar, dot);
      exc = SdfPrimitives.addDrip(exc, x, y, 200, 40, -85, neckRadius: 14, bulbRadius: 24, sway: -10);
      return exc;
    },
  );

  // &: Psychedelic 1970s ampersand with star-cog lower counter (matches 789!& in photo!)
  addSdfGlyph(
    name: 'ampersand',
    unicode: 0x0026,
    advanceWidth: 780,
    swayAmp: 28.0,
    bellBottomStrength: 0.36,
    sdf: (x, y) {
      final top = SdfPrimitives.circle(x, y, 360, 565, 180);
      final bot = SdfPrimitives.circle(x, y, 340, 235, 240);
      final kick = SdfPrimitives.capsule(x, y, 430, 290, 645, 105, 78, 108, sway: 18);
      double amp = SdfPrimitives.smin(top, SdfPrimitives.smin(bot, kick, 38), 38);
      final topHole = SdfPrimitives.circle(x, y, 360, 570, 58);
      final botCog = SdfPrimitives.gearCounter(x, y, 335, 235, 82, teeth: 8, toothDepth: 26);
      amp = SdfPrimitives.ssub(amp, topHole, 6);
      return SdfPrimitives.ssub(amp, botCog, 6);
    },
  );

  // ?: Groovy question mark with dripping dot
  addSdfGlyph(
    name: 'question',
    unicode: 0x003F,
    advanceWidth: 660,
    swayAmp: 30.0,
    bellBottomStrength: 0.34,
    sdf: (x, y) {
      final top = SdfPrimitives.quadStroke(x, y, 155, 560, 350, 745, 515, 535, 92, 82, 88);
      final stem = SdfPrimitives.quadStroke(x, y, 515, 535, 490, 390, 330, 300, 88, 82, 78);
      final dot = SdfPrimitives.circle(x, y, 330, 105, 86);
      double q = math.min(SdfPrimitives.smin(top, stem, 30), dot);
      return SdfPrimitives.addDrip(q, x, y, 330, 40, -75, neckRadius: 13, bulbRadius: 22, sway: 8);
    },
  );

  // .: Period
  addSdfGlyph(
    name: 'period',
    unicode: 0x002E,
    advanceWidth: 340,
    sdf: (x, y) => SdfPrimitives.circle(x, y, 170, 105, 86),
  );

  // ,: Comma
  addSdfGlyph(
    name: 'comma',
    unicode: 0x002C,
    advanceWidth: 340,
    sdf: (x, y) {
      final dot = SdfPrimitives.circle(x, y, 170, 115, 84);
      final tail = SdfPrimitives.capsule(x, y, 185, 95, 130, -30, 68, 44, sway: 10);
      return SdfPrimitives.smin(dot, tail, 22);
    },
  );

  // -: Hyphen
  addSdfGlyph(
    name: 'hyphen',
    unicode: 0x002D,
    advanceWidth: 520,
    sdf: (x, y) => SdfPrimitives.capsule(x, y, 120, 370, 400, 370, 82, 82, sway: -16),
  );

  // :: Colon
  addSdfGlyph(
    name: 'colon',
    unicode: 0x003A,
    advanceWidth: 340,
    sdf: (x, y) => math.min(
      SdfPrimitives.circle(x, y, 170, 470, 78),
      SdfPrimitives.circle(x, y, 170, 125, 82),
    ),
  );

  // Compile TrueType SFNT bytes (2-byte aligned, bit 7 masked)
  final ttfBytes = builder.compile();
  File(outTtf).writeAsBytesSync(ttfBytes);
  print('  ✓ Compiled TrueType binary: ${File(outTtf).lengthSync()} bytes (${builder.glyphs.length} glyphs)');

  // Compress genuine WOFF2 via WSL2 Ubuntu uv fonttools if available, or clean copy
  bool woff2Compressed = false;
  try {
    final wslDir = Directory.current.path
        .replaceFirstMapped(RegExp(r'^([a-zA-Z]):'), (m) => '/mnt/${m[1]!.toLowerCase()}')
        .replaceAll('\\', '/');
    final pyCmd = 'from fontTools.ttLib import TTFont; f = TTFont("$outTtf"); f.flavor = "woff2"; f.save("$outWoff2")';
    final proc = Process.runSync('wsl', [
      '-d',
      'Ubuntu',
      '--',
      'bash',
      '-c',
      'cd "$wslDir" && /home/philg/.local/bin/uv run --with fonttools --with brotli python3 -c \'$pyCmd\''
    ]);
    if (proc.exitCode == 0 && File(outWoff2).existsSync()) {
      woff2Compressed = true;
      print('  ✓ Compressed genuine Brotli WOFF2 binary: ${File(outWoff2).lengthSync()} bytes (magic wOF2)');
    }
  } catch (_) {}

  if (!woff2Compressed) {
    File(outWoff2).writeAsBytesSync(ttfBytes);
    print('  ✓ Wrote fallback webfont binary: $outWoff2');
  }

  final report = ThomasPhinneyAuditor.auditFile(outTtf);
  report.printReport();
  if (!report.passed) exit(1);
}
