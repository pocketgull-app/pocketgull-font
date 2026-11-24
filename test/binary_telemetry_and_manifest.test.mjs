import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import '../js/binary_gvar_inspector.js';

const { parseSfntBuffer } = globalThis.PocketGullBinaryInspector;

test('Innovation 1 [Zero-Reflow Polarity]: pocketgull.css & fonts.css bind GRAD and THRM to dark & 670nm scotopic modes', () => {
  for (const cssPath of ['pocketgull.css', 'fonts.css']) {
    const css = fs.readFileSync(cssPath, 'utf8');
    assert.match(css, /@property --pg-grad\s*\{/, `${cssPath} must register Houdini @property --pg-grad`);
    assert.match(css, /@property --pg-thrm\s*\{/, `${cssPath} must register Houdini @property --pg-thrm`);
    assert.match(css, /\[data-theme="dark"\][\s\S]*?--pg-grad:\s*-25/, `${cssPath} must set --pg-grad: -25 in dark ICU mode`);
    assert.match(css, /\[data-theme="dark"\][\s\S]*?--pg-thrm:\s*0\.35/, `${cssPath} must set --pg-thrm: 0.35 in dark ICU mode`);
    assert.match(css, /\[data-theme="pbm"\][\s\S]*?--pg-grad:\s*-45/, `${cssPath} must set --pg-grad: -45 in 670nm scotopic mode`);
    assert.match(css, /\[data-theme="pbm"\][\s\S]*?--pg-thrm:\s*0\.60/, `${cssPath} must set --pg-thrm: 0.60 in 670nm scotopic mode`);
    assert.match(css, /\.pg-halation-guard/, `${cssPath} must expose .pg-halation-guard cascade-safe class`);
  }
});

test('Innovation 2 [Live Binary gvar Telemetry]: DataView SFNT reader decodes real glyf contours, gvar deltas, and 0px THRM reflow', () => {
  const vfBuf = fs.readFileSync('fonts/ttf/PocketGull-VF.ttf');
  const engine = parseSfntBuffer(vfBuf);
  assert.equal(engine.unitsPerEm, 1000);
  assert.equal(engine.axes.length, 16);

  const proofChars = ['0', 'e', 'a', 'l', 'I', 'i', 'ᐃ', '⠁'];
  for (const ch of proofChars) {
    const base = engine.inspectGlyph(ch, {});
    assert.ok(base.gid > 0, `Glyph '${ch}' must resolve to non-zero GID`);
    assert.equal(base.wordAligned, true, `Glyph '${ch}' (gid ${base.gid}) must satisfy loca[i] % 2 == 0`);
    assert.equal(base.bit7Clean, true, `Glyph '${ch}' (gid ${base.gid}) must clear reserved bit 7`);
    assert.ok(base.points.length >= 4, `Glyph '${ch}' must decode real TrueType contour points`);
  }

  // Verify THRM halation compensation insets contours on '0', 'e', 'a' with 0 UPM advance-width reflow
  for (const ch of ['0', 'e', 'a']) {
    const base = engine.inspectGlyph(ch, {});
    const scotopic = engine.inspectGlyph(ch, { THRM: 0.6 });
    assert.equal(
      scotopic.variedAw,
      base.baseAw,
      `THRM halation inset on '${ch}' must keep advance width locked (0px horizontal reflow)`
    );
    assert.ok(
      scotopic.maxDeltaMag > 5,
      `THRM halation inset on '${ch}' must produce real non-zero gvar contour displacement (got ${scotopic.maxDeltaMag} UPM)`
    );
  }

  // Verify smoe_engine.js and index.html wire live binary inspector with zero synthetic samplePoints
  const smoeCode = fs.readFileSync('js/smoe_engine.js', 'utf8');
  assert.ok(!smoeCode.includes('samplePoints'), 'smoe_engine.js must not use synthetic samplePoints');
  assert.ok(smoeCode.includes('PocketGullBinaryInspector'), 'smoe_engine.js must delegate to PocketGullBinaryInspector');

  const indexHtml = fs.readFileSync('index.html', 'utf8');
  assert.ok(indexHtml.includes('js/binary_gvar_inspector.js'), 'index.html must load js/binary_gvar_inspector.js');
  assert.ok(indexHtml.includes('id="upmInspectorDetails"'), 'index.html must include #upmInspectorDetails live telemetry drawer');
  assert.ok(indexHtml.includes('id="upmInspectorCanvas"'), 'index.html must include #upmInspectorCanvas');
});

test('Innovation 3 [Compiler-Emitted OpenType Manifest]: fonts/opentype-manifest.json matches binary SFNT & package.json SSOT', () => {
  const manifestPath = 'fonts/opentype-manifest.json';
  assert.ok(fs.existsSync(manifestPath), 'fonts/opentype-manifest.json must exist');

  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

  assert.equal(manifest.semver, pkg.version, 'Manifest semver must match package.json SSOT');
  assert.equal(manifest.primaryVariableFont.unitsPerEm, 1000);
  assert.equal(manifest.primaryVariableFont.wordAligned2Byte, true);
  assert.equal(manifest.primaryVariableFont.oddLocaOffsets, 0);
  assert.equal(manifest.primaryVariableFont.axes.length, 16);

  const thrmAxis = manifest.primaryVariableFont.axes.find((a) => a.tag === 'THRM');
  assert.ok(thrmAxis, 'Manifest must include THRM axis');
  assert.equal(thrmAxis.hvarAffectsAdvanceWidth, false, 'THRM must be verified HVAR-invariant in manifest');
  assert.equal(thrmAxis.zeroReflowContourOnly, true, 'THRM must be marked zeroReflowContourOnly');

  const gsubTags = manifest.primaryVariableFont.gsubFeatures.map((f) => f.tag);
  for (const requiredFeat of ['zero', 'tnum', 'ss02', 'ss07', 'cv05', 'cv08']) {
    assert.ok(gsubTags.includes(requiredFeat), `Manifest GSUB features must include '${requiredFeat}'`);
  }
});
