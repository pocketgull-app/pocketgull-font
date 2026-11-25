import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Kinetic Laboratory CSP Compliance: external js/kinetic_lab.js and zero inline scripts', () => {
  const html = fs.readFileSync('kinetic_laboratory.html', 'utf8');
  const externalScriptTag = '<script src="js/kinetic_lab.js" defer></script>';
  const lowerHtml = html.toLowerCase();

  // Enforce deterministic string boundaries (CodeQL Alerts #80 / #82 safe tag inspection):
  // verify strictly one <script ... </script> element exists and matches externalScriptTag byte-for-byte.
  const firstOpenIdx = lowerHtml.indexOf('<script');
  const lastOpenIdx = lowerHtml.lastIndexOf('<script');
  assert.notEqual(firstOpenIdx, -1, 'kinetic_laboratory.html must include external script tag');
  assert.equal(
    firstOpenIdx,
    lastOpenIdx,
    'kinetic_laboratory.html must contain strictly one <script> element (zero inline <script> blocks for Observatory CSP compliance)'
  );
  assert.equal(
    html.slice(firstOpenIdx, firstOpenIdx + externalScriptTag.length),
    externalScriptTag,
    'kinetic_laboratory.html sole <script> tag must load external js/kinetic_lab.js with defer'
  );

  const firstCloseIdx = lowerHtml.indexOf('</script>');
  const lastCloseIdx = lowerHtml.lastIndexOf('</script>');
  assert.equal(firstCloseIdx, lastCloseIdx, 'kinetic_laboratory.html must contain strictly one closing </script> tag');

  assert.match(html, /\[data-theme="scotopic"\]/, 'kinetic_laboratory.html must define scotopic 650nm theme CSS variables');
});

test('Kinetic Laboratory Engine Invariants: zero innerHTML, offscreen glyph collider, TIM parts & states', () => {
  const jsPath = path.join('js', 'kinetic_lab.js');
  const code = fs.readFileSync(jsPath, 'utf8');

  assert.ok(
    !/\.innerHTML\s*=/.test(code),
    'js/kinetic_lab.js must contain zero .innerHTML assignments'
  );

  assert.match(code, /class\s+Ramp\b/, 'js/kinetic_lab.js must define Ramp contraption part');
  assert.match(code, /class\s+Bumper\b/, 'js/kinetic_lab.js must define Bumper contraption part');
  assert.match(code, /class\s+Fan\b/, 'js/kinetic_lab.js must define Fan contraption part');
  assert.match(code, /class\s+TargetBell\b/, 'js/kinetic_lab.js must define TargetBell win trigger');
  assert.match(code, /buildCollider\s*\(/, 'InstrumentGlyph must define offscreen bitmap buildCollider()');
  assert.match(code, /\bsimState\s*:/, 'state must track Blueprint/Run simState');
  assert.match(code, /'scotopic'/, 'theme switcher must support scotopic mode');
  assert.match(code, /function\s+serializeBlueprint\s*\(/, 'js/kinetic_lab.js must define serializeBlueprint()');
  assert.match(code, /function\s+loadBlueprintFromHash\s*\(/, 'js/kinetic_lab.js must define loadBlueprintFromHash()');

  const html = fs.readFileSync('kinetic_laboratory.html', 'utf8');
  assert.match(html, /id="btnShareBlueprint"/, 'kinetic_laboratory.html must include #btnShareBlueprint');
});
