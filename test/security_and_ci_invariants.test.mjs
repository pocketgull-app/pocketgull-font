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

test('Governance Invariant: GOVERNANCE.md, GEMINI.md, and case studies enforce UNDRIP Typographic Accord', () => {
  const govPath = 'GOVERNANCE.md';
  assert.ok(fs.existsSync(govPath), 'GOVERNANCE.md must exist');
  const govText = fs.readFileSync(govPath, 'utf8');

  // Verify UNDRIP and specific key articles are mandated
  assert.match(govText, /United Nations Declaration on the Rights of Indigenous Peoples \(UNDRIP\)/);
  assert.match(govText, /Articles 13\.1 & 14\.1/);
  assert.match(govText, /Articles 11\.1 & 31\.1/);
  assert.match(govText, /Articles 13\.2 & 24\.1/);
  assert.match(govText, /OCAP® Principles/);
  assert.match(govText, /Free, Prior, and Informed Consent/);

  // Verify GEMINI.md and AGENTS.md document the sovereign charter
  const geminiText = fs.readFileSync('GEMINI.md', 'utf8');
  assert.match(geminiText, /Let Indigenous Scripts be Sovereign \(UNDRIP Accord\)/);

  // Verify Pan-Tribal case study cites UNDRIP
  const caseStudy07Path = path.join('documentation', 'case_studies', 'CASE_STUDY_07_PAN_TRIBAL_ORTHOGRAPHIES.md');
  const case07Text = fs.readFileSync(caseStudy07Path, 'utf8');
  assert.match(case07Text, /UNDRIP \(Articles 11, 13, 14, 24, 31\)/);
});

test('Typographic Invariant: Salishan GPOS mark/mkmk anchors and UFO sources present', () => {
  const ufoList = [
    'sources/PocketGull-Fineliner.ufo',
    'sources/PocketGull-Bold.ufo',
    'sources/PocketGull-Chiseltip.ufo',
    'sources/PocketGullMono-Regular.ufo'
  ];

  for (const ufo of ufoList) {
    // Check features.fea exists and defines mark and mkmk
    const feaPath = path.join(ufo, 'features.fea');
    assert.ok(fs.existsSync(feaPath), `${feaPath} must exist`);
    const feaContent = fs.readFileSync(feaPath, 'utf8');
    assert.match(feaContent, /feature mark/);
    assert.match(feaContent, /feature mkmk/);
    assert.match(feaContent, /MarkToBase_Salishan/);

    // Check base glyph glifs have calibrated anchors
    const xGlif = fs.readFileSync(path.join(ufo, 'glyphs', 'x.glif'), 'utf8');
    assert.match(xGlif, /<anchor\s+[^>]*name="top"/);

    const qGlif = fs.readFileSync(path.join(ufo, 'glyphs', 'q.glif'), 'utf8');
    assert.match(qGlif, /<anchor\s+[^>]*name="commaaccent"/);

    const kGlif = fs.readFileSync(path.join(ufo, 'glyphs', 'k.glif'), 'utf8');
    assert.match(kGlif, /<anchor\s+[^>]*name="commaaccent"/);
  }

  // Check forensic audit report exists
  const reportPath = path.join('documentation', 'reports', 'salishan_combining_marks_and_osage_audit.md');
  assert.ok(fs.existsSync(reportPath), 'Salishan & Osage audit report must exist');
});

test('Security Invariant: OWASP Anti-Automation (Honeypot, Rate Limiting, Input Limits) enforced on studio forms', () => {
  const formPages = ['asl_studio.html', 'sign_studio.html'];
  for (const page of formPages) {
    assert.ok(fs.existsSync(page), `${page} must exist`);
    const content = fs.readFileSync(page, 'utf8');

    // 1. Anti-bot honeypot field
    assert.match(content, /id="formHpWebsite"/, `${page} must contain honeypot input field`);
    assert.match(content, /tabindex="-1"/, `${page} honeypot must be excluded from keyboard tab order`);

    // 2. Input length bounds (OWASP ASVS V5)
    assert.match(content, /id="formTargetLetter"[^>]*maxlength="64"/, `${page} must cap formTargetLetter length`);
    assert.match(content, /id="formComments"[^>]*maxlength="2000"/, `${page} must cap formComments length`);

    // 3. Script validation, sanitization, time-trap, and cooldown
    assert.match(content, /function validateSubmission\(\)/, `${page} must define validateSubmission guard`);
    assert.match(content, /function sanitizeInput\(/, `${page} must sanitize user inputs`);
    assert.match(content, /SUBMIT_COOLDOWN_MS/, `${page} must declare submission cooldown rate limiter`);
    assert.match(content, /MIN_INTERACTION_MS/, `${page} must declare time-trap anti-bot delay`);
  }

  // Verify index.html Doc Drill input limits and rate limiting
  const indexContent = fs.readFileSync('index.html', 'utf8');
  assert.match(indexContent, /id="drillInput"[^>]*maxlength="300"/, 'index.html drillInput must cap length at 300 chars');
  assert.match(indexContent, /DRILL_SUBMIT_COOLDOWN_MS/, 'index.html must throttle Doc Drill submissions');
});


