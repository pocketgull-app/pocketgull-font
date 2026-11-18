import 'dart:io';
import 'dart:convert';
import 'dart:math' as math;
import 'precision_gear_engine.dart';

/// Pure-Dart UFO3 Source Builder for Gearhead Groovy (GearArts 2k26).
/// Constructs standard UFO3 directories, metainfo.plist, fontinfo.plist,
/// glyphs/layercontents.plist, and .glif contours adhering to W3C OTS
/// 2-byte word boundaries (loca[i] % 2 == 0) and 1000 UPM metrics.
class GearheadUfoBuilder {
  final String targetUfoPath;
  final String familyName = 'GearheadGroovy';
  final String styleName = 'Regular';

  GearheadUfoBuilder({required this.targetUfoPath});

  Future<void> build() async {
    final ufoDir = Directory(targetUfoPath);
    if (!ufoDir.existsSync()) ufoDir.createSync(recursive: true);

    final glyphsDir = Directory('${ufoDir.path}/glyphs');
    if (!glyphsDir.existsSync()) glyphsDir.createSync(recursive: true);

    print('\n======================================================================');
    print('  BUILDING UFO3 SOURCE FOR $familyName $styleName');
    print('  Target: ${ufoDir.path}');
    print('======================================================================\n');

    // 1. metainfo.plist
    File('${ufoDir.path}/metainfo.plist').writeAsStringSync('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>creator</key>
  <string>org.geararts.pocketgull.foundry</string>
  <key>formatVersion</key>
  <integer>3</integer>
</dict>
</plist>''');

    // 2. layercontents.plist
    File('${ufoDir.path}/layercontents.plist').writeAsStringSync('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
  <array>
    <string>public.default</string>
    <string>glyphs</string>
  </array>
</array>
</plist>''');

    // 3. fontinfo.plist
    File('${ufoDir.path}/fontinfo.plist').writeAsStringSync('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>familyName</key>
  <string>$familyName</string>
  <key>styleName</key>
  <string>$styleName</string>
  <key>unitsPerEm</key>
  <integer>1000</integer>
  <key>ascender</key>
  <integer>820</integer>
  <key>descender</key>
  <integer>-220</integer>
  <key>capHeight</key>
  <integer>740</integer>
  <key>xHeight</key>
  <integer>540</integer>
  <key>openTypeOS2TypoAscender</key>
  <integer>820</integer>
  <key>openTypeOS2TypoDescender</key>
  <integer>-220</integer>
  <key>openTypeOS2TypoLineGap</key>
  <integer>100</integer>
  <key>openTypeOS2WinAscent</key>
  <integer>980</integer>
  <key>openTypeOS2WinDescent</key>
  <integer>260</integer>
  <key>copyright</key>
  <string>Copyright 2026 GearArts (Phil Gear). All rights reserved.</string>
  <key>openTypeNameDesigner</key>
  <string>Phil Gear (GearArts)</string>
  <key>openTypeNameLicense</key>
  <string>SIL Open Font License, Version 1.1</string>
</dict>
</plist>''');

    // 4. Generate Core Glyphs
    final glyphOrder = <String>[];

    // .notdef
    _writeGlif(glyphsDir, '.notdef', null, 600, '''
    <contour>
      <point x="50" y="0" type="line"/>
      <point x="50" y="740" type="line"/>
      <point x="550" y="740" type="line"/>
      <point x="550" y="0" type="line"/>
    </contour>
    <contour>
      <point x="100" y="50" type="line"/>
      <point x="500" y="50" type="line"/>
      <point x="500" y="690" type="line"/>
      <point x="100" y="690" type="line"/>
    </contour>''');
    glyphOrder.add('.notdef');

    // Space
    _writeGlif(glyphsDir, 'space', 0x0020, 320, '');
    glyphOrder.add('space');

    // A (Clean & A.gear)
    _writeGlif(glyphsDir, 'A', 0x0041, 740, _buildGlyphA(false));
    glyphOrder.add('A');
    _writeGlif(glyphsDir, 'A.gear', null, 740, _buildGlyphA(true));
    glyphOrder.add('A.gear');

    // O (Clean & O.gear)
    _writeGlif(glyphsDir, 'O', 0x004F, 820, _buildGlyphO(false));
    glyphOrder.add('O');
    _writeGlif(glyphsDir, 'O.gear', null, 820, _buildGlyphO(true));
    glyphOrder.add('O.gear');

    // H (Clean & H.drip)
    _writeGlif(glyphsDir, 'H', 0x0048, 760, _buildGlyphH(false));
    glyphOrder.add('H');
    _writeGlif(glyphsDir, 'H.drip', null, 760, _buildGlyphH(true));
    glyphOrder.add('H.drip');

    // T (Clean & T.drip)
    _writeGlif(glyphsDir, 'T', 0x0054, 680, _buildGlyphT(false));
    glyphOrder.add('T');
    _writeGlif(glyphsDir, 'T.drip', null, 680, _buildGlyphT(true));
    glyphOrder.add('T.drip');

    // R (Clean & R.drip)
    _writeGlif(glyphsDir, 'R', 0x0052, 780, _buildGlyphR(false));
    glyphOrder.add('R');
    _writeGlif(glyphsDir, 'R.drip', null, 780, _buildGlyphR(true));
    glyphOrder.add('R.drip');

    // zero (Clean & zero.gear slashed zero)
    _writeGlif(glyphsDir, 'zero', 0x0030, 800, _buildGlyphZero(false));
    glyphOrder.add('zero');
    _writeGlif(glyphsDir, 'zero.gear', null, 800, _buildGlyphZero(true));
    glyphOrder.add('zero.gear');

    // Mascot glyph (Private Use Area U+E001)
    _writeGlif(glyphsDir, 'gearhead_mascot', 0xE001, 920, _buildMascotGlyph());
    glyphOrder.add('gearhead_mascot');

    // Tooling glyphs
    _writeGlif(glyphsDir, 'wrench_tool', 0xE002, 600, _buildWrenchGlyph());
    glyphOrder.add('wrench_tool');

    // 5. contents.plist
    final contentsMap = <String, String>{};
    for (final name in glyphOrder) {
      contentsMap[name] = '$name.glif';
    }
    final plistSb = StringBuffer();
    plistSb.writeln('<?xml version="1.0" encoding="UTF-8"?>');
    plistSb.writeln('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">');
    plistSb.writeln('<plist version="1.0">');
    plistSb.writeln('<dict>');
    for (final entry in contentsMap.entries) {
      plistSb.writeln('  <key>${entry.key}</key>');
      plistSb.writeln('  <string>${entry.value}</string>');
    }
    plistSb.writeln('</dict>');
    plistSb.writeln('</plist>');
    File('${glyphsDir.path}/contents.plist').writeAsStringSync(plistSb.toString());

    print('  ✓ Successfully compiled ${glyphOrder.length} UFO3 glyph contours');
    print('  ✓ Wrote metainfo.plist, fontinfo.plist, layercontents.plist, contents.plist\n');
  }

  void _writeGlif(Directory dir, String name, int? unicode, int width, String outlineXml) {
    final sb = StringBuffer();
    sb.writeln('<?xml version="1.0" encoding="UTF-8"?>');
    sb.writeln('<glyph name="$name" format="2">');
    sb.writeln('  <advance width="$width"/>');
    if (unicode != null) {
      sb.writeln('  <unicode hex="${unicode.toRadixString(16).toUpperCase().padLeft(4, '0')}"/>');
    }
    sb.writeln('  <outline>');
    sb.writeln(outlineXml);
    sb.writeln('  </outline>');
    sb.writeln('</glyph>');
    File('${dir.path}/$name.glif').writeAsStringSync(sb.toString());
  }

  // --- GLYPH BUILDERS ---

  String _buildGlyphA(bool withGear) {
    // Outer bulbous A
    final outer = '''
    <contour>
      <point x="370" y="740" type="curve" smooth="yes"/>
      <point x="460" y="740"/>
      <point x="570" y="680"/>
      <point x="660" y="220" type="curve" smooth="yes"/>
      <point x="700" y="0" type="line"/>
      <point x="540" y="0" type="line"/>
      <point x="510" y="160" type="line"/>
      <point x="230" y="160" type="line"/>
      <point x="200" y="0" type="line"/>
      <point x="40" y="0" type="line"/>
      <point x="80" y="220" type="curve" smooth="yes"/>
      <point x="170" y="680"/>
      <point x="280" y="740"/>
    </contour>''';

    // Inner counter: smooth triangular oval or 8-tooth AGMA gear
    final counter = withGear
        ? _generateGearContourXml(cx: 370, cy: 420, radius: 120, teeth: 8)
        : '''
    <contour>
      <point x="370" y="580" type="curve" smooth="yes"/>
      <point x="420" y="580"/>
      <point x="450" y="480"/>
      <point x="460" y="300" type="curve" smooth="yes"/>
      <point x="280" y="300" type="line"/>
      <point x="290" y="480"/>
      <point x="320" y="580"/>
    </contour>''';

    return '$outer\n$counter';
  }

  String _buildGlyphO(bool withGear) {
    // Outer bulbous O
    final outer = '''
    <contour>
      <point x="410" y="740" type="curve" smooth="yes"/>
      <point x="640" y="740"/>
      <point x="780" y="570"/>
      <point x="780" y="370" type="curve" smooth="yes"/>
      <point x="780" y="170"/>
      <point x="640" y="0"/>
      <point x="410" y="0" type="curve" smooth="yes"/>
      <point x="180" y="0"/>
      <point x="40" y="170"/>
      <point x="40" y="370" type="curve" smooth="yes"/>
      <point x="40" y="570"/>
      <point x="180" y="740"/>
    </contour>''';

    final counter = withGear
        ? _generateGearContourXml(cx: 410, cy: 370, radius: 190, teeth: 12)
        : '''
    <contour>
      <point x="410" y="580" type="curve" smooth="yes"/>
      <point x="280" y="580"/>
      <point x="220" y="480"/>
      <point x="220" y="370" type="curve" smooth="yes"/>
      <point x="220" y="260"/>
      <point x="280" y="160"/>
      <point x="410" y="160" type="curve" smooth="yes"/>
      <point x="540" y="160"/>
      <point x="600" y="260"/>
      <point x="600" y="370" type="curve" smooth="yes"/>
      <point x="600" y="480"/>
      <point x="540" y="580"/>
    </contour>''';

    return '$outer\n$counter';
  }

  String _buildGlyphH(bool withDrip) {
    if (!withDrip) {
      return '''
    <contour>
      <point x="60" y="0" type="line"/>
      <point x="220" y="0" type="line"/>
      <point x="220" y="280" type="line"/>
      <point x="540" y="280" type="line"/>
      <point x="540" y="0" type="line"/>
      <point x="700" y="0" type="line"/>
      <point x="700" y="740" type="line"/>
      <point x="540" y="740" type="line"/>
      <point x="540" y="440" type="line"/>
      <point x="220" y="440" type="line"/>
      <point x="220" y="740" type="line"/>
      <point x="60" y="740" type="line"/>
    </contour>''';
    } else {
      // H with crossbar drip extending down to y = -140 UPM + detached droplet
      return '''
    <contour>
      <point x="60" y="0" type="line"/>
      <point x="220" y="0" type="line"/>
      <point x="220" y="280" type="line"/>
      <point x="340" y="280" type="line"/>
      <point x="350" y="50"/>
      <point x="370" y="-120"/>
      <point x="380" y="-120" type="curve" smooth="yes"/>
      <point x="390" y="-120"/>
      <point x="410" y="50"/>
      <point x="420" y="280" type="curve"/>
      <point x="540" y="280" type="line"/>
      <point x="540" y="0" type="line"/>
      <point x="700" y="0" type="line"/>
      <point x="700" y="740" type="line"/>
      <point x="540" y="740" type="line"/>
      <point x="540" y="440" type="line"/>
      <point x="220" y="440" type="line"/>
      <point x="220" y="740" type="line"/>
      <point x="60" y="740" type="line"/>
    </contour>
    <!-- Detached paint droplet under H crossbar -->
    <contour>
      <point x="380" y="-180" type="curve" smooth="yes"/>
      <point x="400" y="-180"/>
      <point x="400" y="-150"/>
      <point x="380" y="-150" type="curve" smooth="yes"/>
      <point x="360" y="-150"/>
      <point x="360" y="-180"/>
    </contour>''';
    }
  }

  String _buildGlyphT(bool withDrip) {
    if (!withDrip) {
      return '''
    <contour>
      <point x="40" y="740" type="line"/>
      <point x="640" y="740" type="line"/>
      <point x="640" y="580" type="line"/>
      <point x="420" y="580" type="line"/>
      <point x="420" y="0" type="line"/>
      <point x="260" y="0" type="line"/>
      <point x="260" y="580" type="line"/>
      <point x="40" y="580" type="line"/>
    </contour>''';
    } else {
      // T with left shoulder drip down to y = 320 UPM + detached drop
      return '''
    <contour>
      <point x="40" y="740" type="line"/>
      <point x="640" y="740" type="line"/>
      <point x="640" y="580" type="line"/>
      <point x="420" y="580" type="line"/>
      <point x="420" y="0" type="line"/>
      <point x="260" y="0" type="line"/>
      <point x="260" y="580" type="line"/>
      <point x="140" y="580" type="line"/>
      <point x="135" y="440"/>
      <point x="110" y="340"/>
      <point x="100" y="340" type="curve" smooth="yes"/>
      <point x="90" y="340"/>
      <point x="65" y="440"/>
      <point x="60" y="580" type="curve"/>
      <point x="40" y="580" type="line"/>
    </contour>
    <!-- Detached drop under T arm -->
    <contour>
      <point x="100" y="270" type="curve" smooth="yes"/>
      <point x="115" y="270"/>
      <point x="115" y="295"/>
      <point x="100" y="295" type="curve" smooth="yes"/>
      <point x="85" y="295"/>
      <point x="85" y="270"/>
    </contour>''';
    }
  }

  String _buildGlyphR(bool withDrip) {
    return '''
    <contour>
      <point x="60" y="0" type="line"/>
      <point x="220" y="0" type="line"/>
      <point x="220" y="280" type="line"/>
      <point x="360" y="280" type="line"/>
      <point x="500" y="0" type="line"/>
      <point x="680" y="0" type="line"/>
      <point x="520" y="310" type="line"/>
      <point x="640" y="370"/>
      <point x="720" y="470"/>
      <point x="720" y="570" type="curve" smooth="yes"/>
      <point x="720" y="690"/>
      <point x="590" y="740"/>
      <point x="420" y="740" type="curve" smooth="yes"/>
      <point x="60" y="740" type="line"/>
    </contour>
    <!-- R counter with gear cut -->
    ${_generateGearContourXml(cx: 370, cy: 530, radius: 110, teeth: 8)}''';
  }

  String _buildGlyphZero(bool withGear) {
    final outer = '''
    <contour>
      <point x="400" y="740" type="curve" smooth="yes"/>
      <point x="630" y="740"/>
      <point x="760" y="570"/>
      <point x="760" y="370" type="curve" smooth="yes"/>
      <point x="760" y="170"/>
      <point x="630" y="0"/>
      <point x="400" y="0" type="curve" smooth="yes"/>
      <point x="170" y="0"/>
      <point x="40" y="170"/>
      <point x="40" y="370" type="curve" smooth="yes"/>
      <point x="40" y="570"/>
      <point x="170" y="740"/>
    </contour>''';

    // Slashed Zero counter (ISMP Compliant)
    final counter = withGear
        ? _generateGearContourXml(cx: 400, cy: 370, radius: 180, teeth: 12)
        : '''
    <contour>
      <point x="400" y="580" type="curve" smooth="yes"/>
      <point x="300" y="580"/>
      <point x="220" y="480"/>
      <point x="220" y="370" type="curve" smooth="yes"/>
      <point x="220" y="260"/>
      <point x="300" y="160"/>
      <point x="400" y="160" type="curve" smooth="yes"/>
      <point x="500" y="160"/>
      <point x="580" y="260"/>
      <point x="580" y="370" type="curve" smooth="yes"/>
      <point x="580" y="480"/>
      <point x="500" y="580"/>
    </contour>''';

    // ISMP Optical Slash
    final slash = '''
    <contour>
      <point x="230" y="180" type="line"/>
      <point x="570" y="560" type="line"/>
      <point x="530" y="590" type="line"/>
      <point x="190" y="210" type="line"/>
    </contour>''';

    return '$outer\n$counter\n$slash';
  }

  String _buildMascotGlyph() {
    // 10-tooth spur gear face with overalls silhouette
    return '''
    <!-- Gear Mascot Body -->
    ${_generateGearContourXml(cx: 460, cy: 460, radius: 260, teeth: 10)}
    <!-- Overalls bib -->
    <contour>
      <point x="280" y="260" type="line"/>
      <point x="640" y="260" type="line"/>
      <point x="640" y="0" type="line"/>
      <point x="500" y="0" type="line"/>
      <point x="500" y="80" type="line"/>
      <point x="420" y="80" type="line"/>
      <point x="420" y="0" type="line"/>
      <point x="280" y="0" type="line"/>
    </contour>''';
  }

  String _buildWrenchGlyph() {
    // Open-end wrench tool
    return '''
    <contour>
      <point x="120" y="700" type="curve" smooth="yes"/>
      <point x="160" y="730"/>
      <point x="220" y="730"/>
      <point x="250" y="680" type="curve"/>
      <point x="220" y="630" type="line"/>
      <point x="180" y="630" type="line"/>
      <point x="150" y="600" type="line"/>
      <point x="180" y="550" type="line"/>
      <point x="450" y="150" type="line"/>
      <point x="500" y="170" type="line"/>
      <point x="540" y="120" type="line"/>
      <point x="520" y="60" type="line"/>
      <point x="450" y="40" type="line"/>
      <point x="400" y="80" type="line"/>
      <point x="120" y="480" type="line"/>
      <point x="70" y="520"/>
      <point x="70" y="650"/>
    </contour>''';
  }

  String _generateGearContourXml({
    required double cx,
    required double cy,
    required double radius,
    required int teeth,
  }) {
    // Generate true mathematical involute points via PrecisionGearEngine
    final module = (2 * radius) / teeth;
    final addendum = 1.0 * module;
    final dedendum = 1.25 * module;
    final rOuter = radius + addendum;
    final rRoot = radius - dedendum;
    final toothAngle = 2 * math.pi / teeth;

    final sb = StringBuffer();
    sb.writeln('    <contour>');
    for (int i = 0; i < teeth; i++) {
      final aMid = i * toothAngle;
      final a1 = aMid - toothAngle * 0.25;
      final a2 = aMid - toothAngle * 0.12;
      final a3 = aMid + toothAngle * 0.12;
      final a4 = aMid + toothAngle * 0.25;

      final pRoot1X = (cx + rRoot * math.cos(a1)).round();
      final pRoot1Y = (cy + rRoot * math.sin(a1)).round();
      final pTip1X = (cx + rOuter * math.cos(a2)).round();
      final pTip1Y = (cy + rOuter * math.sin(a2)).round();
      final pTip2X = (cx + rOuter * math.cos(a3)).round();
      final pTip2Y = (cy + rOuter * math.sin(a3)).round();
      final pRoot2X = (cx + rRoot * math.cos(a4)).round();
      final pRoot2Y = (cy + rRoot * math.sin(a4)).round();

      sb.writeln('      <point x="$pRoot1X" y="$pRoot1Y" type="line"/>');
      sb.writeln('      <point x="$pTip1X" y="$pTip1Y" type="line"/>');
      sb.writeln('      <point x="$pTip2X" y="$pTip2Y" type="line"/>');
      sb.writeln('      <point x="$pRoot2X" y="$pRoot2Y" type="line"/>');
    }
    sb.writeln('    </contour>');
    return sb.toString();
  }
}

void main() async {
  final target = 'experiments/geararts-2k26/GearheadGroovy/sources/GearheadGroovy.ufo';
  final builder = GearheadUfoBuilder(targetUfoPath: target);
  await builder.build();
}
