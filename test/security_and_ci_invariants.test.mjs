import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('CI Invariant: .github/workflows/codeql.yml must NOT exist (Default Setup active)', () => {
  const codeqlWorkflowPath = path.join('.github', 'workflows', 'codeql.yml');
  const exists = fs.existsSync(codeqlWorkflowPath);
  assert.ok(
    !exists,
    'Conflicting workflow .github/workflows/codeql.yml detected! PocketGull uses GitHub native Default Setup for CodeQL SAST. Adding a manual codeql.yml causes SARIF upload rejection.'
  );
});

test('Security Invariant: asl_turntable_engine.js enforces strict alphanumeric validation on setChar', () => {
  const enginePath = path.join('js', 'asl_turntable_engine.js');
  assert.ok(fs.existsSync(enginePath), 'asl_turntable_engine.js must exist');
  const code = fs.readFileSync(enginePath, 'utf8');

  // Verify alphanumeric sanitation regex exists in setChar
  assert.match(
    code,
    /replace\(\/\[\^A-Z0-9\]\/g,\s*''\)/,
    'asl_turntable_engine.js must sanitize setChar input to [A-Z0-9] to prevent DOM XSS'
  );

  // Verify fallback SVG uses createElementNS and textContent rather than innerHTML interpolation
  assert.match(
    code,
    /document\.createElementNS\('http:\/\/www\.w3\.org\/2000\/svg',\s*'text'\)/,
    'asl_turntable_engine.js must use programmatic SVG text element with textContent'
  );
});

test('Security Invariant: asl_studio.html and sign_studio.html use safe DOM text nodes for cards and comparative views', () => {
  const files = ['asl_studio.html', 'sign_studio.html'];
  for (const f of files) {
    assert.ok(fs.existsSync(f), `${f} must exist`);
    const code = fs.readFileSync(f, 'utf8');

    // Ensure hand-char-label and posture-desc are populated via textContent
    assert.match(
      code,
      /charLabel\.textContent\s*=\s*char;/,
      `${f} must assign char to charLabel via textContent`
    );
    assert.match(
      code,
      /postureDesc\.textContent\s*=\s*data\.desc;/,
      `${f} must assign desc to postureDesc via textContent`
    );

    // Ensure comparative view builds DOM elements rather than innerHTML concatenation
    assert.match(
      code,
      /compBSL\.textContent\s*=\s*'';/,
      `${f} must clear compBSL using textContent`
    );
    assert.match(
      code,
      /compJSL\.textContent\s*=\s*'';/,
      `${f} must clear compJSL using textContent`
    );
  }
});

test('Security Invariant: dymaxion_cube.html does not use flawed regex HTML stripping', () => {
  const cubePath = 'dymaxion_cube.html';
  assert.ok(fs.existsSync(cubePath), 'dymaxion_cube.html must exist');
  const code = fs.readFileSync(cubePath, 'utf8');

  assert.doesNotMatch(
    code,
    /\.replace\(\/<\[\^>\]\*>(\?\/gm|;\s*)/,
    'dymaxion_cube.html must not use flawed regex tag-stripping (incomplete sanitization)'
  );
  assert.match(
    code,
    /markerCaption\.textContent\s*=\s*'';/,
    'dymaxion_cube.html must construct markerCaption safely using DOM nodes'
  );
});

test('Security Invariant: healing_cinema.html uses renderBionic with DOM nodes rather than innerHTML', () => {
  const cinemaPath = 'healing_cinema.html';
  assert.ok(fs.existsSync(cinemaPath), 'healing_cinema.html must exist');
  const code = fs.readFileSync(cinemaPath, 'utf8');

  assert.match(
    code,
    /renderBionic\(container,\s*text\)/,
    'healing_cinema.html must provide renderBionic(container, text) DOM node builder'
  );
  assert.doesNotMatch(
    code,
    /document\.getElementById\("heroText"\)\.innerHTML\s*=\s*cinema\.formatBionic/,
    'healing_cinema.html must not assign formatBionic output to innerHTML'
  );
});
