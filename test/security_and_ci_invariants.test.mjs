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

