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

test('Security & CodeQL SAST: Web MIDI & Laboratory controllers enforce strict bounds and sanitization', () => {
  const indexContent = fs.readFileSync('index.html', 'utf8');

  // 1. Web MIDI strict byte masking and clamping
  assert.match(indexContent, /status\s*=\s*Number\(msg\.data\[0\]\)\s*&\s*0xFF/, 'Web MIDI must mask status byte to 8 bits');
  assert.match(indexContent, /noteNumber\s*=\s*Number\(msg\.data\[1\]\)\s*&\s*0x7F/, 'Web MIDI must mask note number to 7 bits');
  assert.match(indexContent, /rawVel\s*=\s*Number\(msg\.data\[2\]\)\s*&\s*0x7F/, 'Web MIDI must mask velocity byte to 7 bits');
  assert.match(indexContent, /Math\.min\(127,\s*Math\.max\(1,\s*rawVel\)\)/, 'Web MIDI must clamp velocity within [1, 127]');

  // 2. Safe DOM manipulation in Audio Simulator
  assert.match(indexContent, /window\.toggleAudioTelemetrySim\s*=/, 'index.html must export toggleAudioTelemetrySim');
  assert.match(indexContent, /window\.setDaltonismFilter\s*=/, 'index.html must export setDaltonismFilter');
  assert.match(indexContent, /window\.switchSciTab\s*=/, 'index.html must export switchSciTab');
});

test('Global Health Atlas & World Map Studio Invariants: Authentic Cree Syllabics, Negative Space Compliance, and CSS/JSON Exporter', () => {
  const indexContent = fs.readFileSync('index.html', 'utf8');

  // 1. Zero Katakana corruption in Cree Syllabics (must use ᐏန် U+140F U+1423, never Katakana ウィン)
  assert.ok(!indexContent.includes('ウィン'), 'Cree Syllabics must not contain corrupted Japanese Katakana ウィン');
  assert.ok(indexContent.includes('ᒥᔪ ᐱᒫᑎᓯᐏန်'), 'Cree Nation entry must contain authentic Cree Syllabics ᒥᔪ ᐱᒫᑎᓯᐏန်');
  assert.ok(indexContent.includes('ᓀᐦᐃᔭᐍᐏန်'), 'Doc Drill UNDRIP entry must contain authentic Cree Syllabics ᓀᐦᐃᔭᐍᐏန်');

  // 2. Negative Space Invariant #9.5: Zero mock milligram DOSE prescriptions in GLOBAL_HEALTH_ATLAS
  const atlasStart = indexContent.indexOf('const GLOBAL_HEALTH_ATLAS = [');
  const atlasEnd = indexContent.indexOf('function initWorldMapStudio()');
  assert.ok(atlasStart !== -1 && atlasEnd > atlasStart, 'GLOBAL_HEALTH_ATLAS block must exist');
  const atlasSection = indexContent.slice(atlasStart, atlasEnd);
  assert.ok(!/dosageAlert:\s*'DOSE:/i.test(atlasSection), 'GLOBAL_HEALTH_ATLAS must not contain mock milligram DOSE prescriptions');

  // 3. Dual CSS/JSON profile exporter and continent landmass click handlers
  assert.match(indexContent, /id="btnFormatCss"/, 'World Map HUD must include CSS format toggle button');
  assert.match(indexContent, /id="btnFormatJson"/, 'World Map HUD must include JSON format toggle button');
  assert.match(indexContent, /function buildCountryJson\(/, 'World Map studio must define deterministic JSON profile builder');
  assert.match(indexContent, /indigenous:\s*\{\s*x:\s*60,\s*y:\s*30,\s*w:\s*500,\s*h:\s*430\s*\}/, 'Indigenous region bounds must encompass South American and African sovereign scripts');

  // 4. Zero vertical scroll-hijacking in World Map pill bar & Google Maps Platform Live compliance
  assert.ok(!indexContent.includes('pill.scrollIntoView'), 'selectCountry must not call pill.scrollIntoView (causes vertical viewport jump to Section 6/7)');
  assert.match(indexContent, /pillBar\.scrollTo\(/, 'selectCountry must scroll pillBar horizontally via pillBar.scrollTo');
  assert.match(indexContent, /id="viewSwitchGoogleMap"/, 'World Map Studio must include Google Maps Live view toggle');
  assert.match(indexContent, /id="googleMapCanvas"/, 'World Map Studio must include Google Maps canvas container');
  assert.match(indexContent, /importLibrary\("maps"\)/, 'Google Maps integration must use dynamic importLibrary("maps")');
  assert.match(indexContent, /importLibrary\("marker"\)/, 'Google Maps integration must use dynamic importLibrary("marker")');
  assert.match(indexContent, /AdvancedMarkerElement/, 'Google Maps integration must use AdvancedMarkerElement');
  assert.match(indexContent, /mapId:\s*'DEMO_MAP_ID'/, 'Google Maps integration must specify DEMO_MAP_ID for AdvancedMarkerElement');
  assert.match(indexContent, /internalUsageAttributionIds:\s*\['gmp_git_agentskills_v1'\]/, 'Google Maps integration must include internalUsageAttributionIds');

  // 5. Modular Written-Language Builder & Flag-Free Written Language Switcher
  assert.match(indexContent, /id="languagePackBuilder"/, 'Chapter 7 must include the interactive Mix Your Written Languages Builder');
  assert.match(indexContent, /function initLanguagePackBuilder\(\)/, 'index.html must define initLanguagePackBuilder()');
  assert.match(indexContent, /id="viewSwitchWrittenLang"/, 'World Map Studio must include the By Written Language switcher button');
  assert.match(indexContent, /WRITTEN_LANGUAGE_METADATA/, 'World Map Studio must define flag-free WRITTEN_LANGUAGE_METADATA mappings');
});




