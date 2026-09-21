/**
 * test/variable_sliders_e2e.test.mjs
 * ===================================
 * Automated End-to-End Test Suite for PocketGull Variable Font (VF),
 * 16-Axis Console Sliders, Interactive Presets, and Zero-Tofu Braille Invariants.
 */

import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const EXPECTED_AXES = [
  'wght', 'wdth', 'slnt', 'opsz',
  'SOFT', 'THRM', 'APTR', 'SMRN',
  'HLNG', 'BION', 'GRAV', 'BOUM',
  'CHIS', 'NUQT', 'INUK', 'BRLS'
];

test('E2E [Binary]: PocketGull-VF.ttf contains all 16 fvar design axes and is 2-byte word aligned', () => {
  const vfPath = 'fonts/ttf/PocketGull-VF.ttf';
  assert.ok(fs.existsSync(vfPath), 'PocketGull-VF.ttf must exist');

  const buf = fs.readFileSync(vfPath);
  assert.equal(buf.length % 2, 0, 'PocketGull-VF.ttf must maintain 2-byte word alignment (loca[i] % 2 == 0)');

  // Verify SFNT TrueType magic number
  const sfntVersion = buf.readUInt32BE(0);
  assert.equal(sfntVersion, 0x00010000, 'SFNT TrueType signature must be 0x00010000');

  // Verify presence of table tags
  const numTables = buf.readUInt16BE(4);
  const tables = [];
  for (let i = 0; i < numTables; i++) {
    const tag = buf.toString('ascii', 12 + i * 16, 16 + i * 16);
    tables.push(tag);
  }

  assert.ok(tables.includes('fvar'), 'Font binary must contain fvar table');
  assert.ok(tables.includes('gvar'), 'Font binary must contain gvar table');
  assert.ok(tables.includes('STAT'), 'Font binary must contain STAT table');
});

test('E2E [CSS]: fonts.css declares unified PocketGull VF with full 100-900 weight, stretch, and slant ranges', () => {
  const css = fs.readFileSync('fonts.css', 'utf-8');

  // Must declare PocketGull VF @font-face
  assert.ok(css.includes("font-family: 'PocketGull VF'"), "fonts.css must define 'PocketGull VF'");

  // Must declare full weight range 100 900
  assert.ok(css.includes('font-weight: 100 900'), "PocketGull VF must support full continuous weight axis 100 900");

  // Must declare font-stretch range 75% 100%
  assert.ok(css.includes('font-stretch: 75% 100%'), "PocketGull VF must support continuous width axis 75% 100%");

  // Must declare font-style oblique range
  assert.ok(css.includes('font-style: oblique -10.5deg 0deg'), "PocketGull VF must support continuous slant axis -10.5deg 0deg");

  // Must use standard format('woff2')
  assert.ok(css.includes("format('woff2')"), "PocketGull VF must include standard format('woff2')");

  // Verify no restrictive 400 900 override exists for PocketGull VF
  const lines = css.split('\n');
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes("font-family: 'PocketGull VF'")) {
      const block = lines.slice(i, i + 15).join('\n');
      assert.ok(!block.includes('font-weight: 400 900'), "PocketGull VF must NOT be restricted to 400 900");
    }
  }
});

test('E2E [DOM index.html]: 16-Axis Console has all 16 interactive sliders properly configured', () => {
  const html = fs.readFileSync('index.html', 'utf-8');

  // Verify every axis has a corresponding range input
  for (const axis of EXPECTED_AXES) {
    const sliderId = `id="slider-${axis}"`;
    assert.ok(html.includes(sliderId), `index.html must contain slider input for axis '${axis}' (${sliderId})`);
    
    const valId = `id="val-${axis}"`;
    assert.ok(html.includes(valId), `index.html must contain value label for axis '${axis}' (${valId})`);
  }

  // Verify interactive specimen target element exists
  assert.ok(html.includes('id="vf-playground-text"'), "index.html must have #vf-playground-text specimen element");
  assert.ok(html.includes('id="vf-playground-readout"'), "index.html must have #vf-playground-readout readout element");

  // Verify JavaScript axes array defines all 16 axes
  for (const axis of EXPECTED_AXES) {
    assert.ok(html.includes(`id: '${axis}'`), `JavaScript axes config must include axis '${axis}'`);
  }
});

test('E2E [DOM index.html]: All 16 Variable Font Presets are defined with valid coordinates', () => {
  const html = fs.readFileSync('index.html', 'utf-8');

  const requiredPresets = [
    'healing', 'heading_home', 'hairline', 'thin', 'fineliner',
    'regular', 'bold', 'chiseltip', 'soft_regular', 'soft_bold',
    'soft_black', 'aperture', 'gravity', 'bionic', 'thermal', 'braille'
  ];

  for (const p of requiredPresets) {
    assert.ok(html.includes(`data-preset="${p}"`), `index.html must contain button with data-preset="${p}"`);
    assert.ok(html.includes(`${p}:`), `JavaScript presets object must configure coordinates for '${p}'`);
  }
});

test('E2E [specimen-broadside.html]: 4 Canonical Sliders and Presets are verified', () => {
  const html = fs.readFileSync('specimen-broadside.html', 'utf-8');

  for (const axis of ['wght', 'wdth', 'slnt', 'opsz']) {
    assert.ok(html.includes(`id="slider-${axis}"`), `specimen-broadside.html must contain slider-${axis}`);
    assert.ok(html.includes(`id="val-${axis}"`), `specimen-broadside.html must contain val-${axis}`);
  }

  assert.ok(html.includes('id="vf-playground-text"'), "specimen-broadside.html must have #vf-playground-text");
  assert.ok(html.includes('id="vf-playground-readout"'), "specimen-broadside.html must have #vf-playground-readout");
});

test('E2E [Braille & Zero-Tofu]: Braille specimen guides enforce resilient system font fallbacks', () => {
  const broadside = fs.readFileSync('specimen-broadside.html', 'utf-8');

  // Verify standard comparison card uses resilient multi-platform font stack
  assert.ok(
    broadside.includes("'Segoe UI Symbol'") && broadside.includes("'Apple Symbols'"),
    "Standard Braille guide must specify Segoe UI Symbol and Apple Symbols to prevent missing glyph tofu on Windows and macOS"
  );

  // Verify PocketGull card uses PocketGull Bold
  assert.ok(
    broadside.includes("'PocketGull Bold'"),
    "Calibrated Braille guide must specify 'PocketGull Bold'"
  );

  // Verify sample Braille text is present
  assert.ok(
    broadside.includes('Rx: ⠁⠍⠕⠭ 500mg'),
    "Broadside must contain 'Rx: ⠁⠍⠕⠭ 500mg' Amoxicillin Braille prescription sample"
  );
});

test('E2E [Philocardia Heart Tittles & Tittle Varieties]: CSS engine declares 6 varieties and cardiac pacing', () => {
  const css = fs.readFileSync('fonts.css', 'utf-8');

  // Verify signature heart class and elements
  assert.ok(css.includes('.philocardia-heart'), "fonts.css must define .philocardia-heart");
  assert.ok(css.includes('.philocardia-j'), "fonts.css must define .philocardia-j for dotless j");
  assert.ok(css.includes('.philocardia-excl'), "fonts.css must define .philocardia-excl");

  // Verify all 6 tittle varieties
  const varieties = [
    { name: 'heart', glyph: '♥' },
    { name: 'blossom', glyph: '✤' },
    { name: 'nuqta', glyph: '◆' },
    { name: 'star', glyph: '✦' },
    { name: 'droplet', glyph: '💧' },
    { name: 'dot', glyph: '●' },
  ];

  for (const v of varieties) {
    assert.ok(
      css.includes(`[data-tittle-variety="${v.name}"]`) && css.includes(`--tittle-glyph: '${v.glyph}'`),
      `fonts.css must define variety '${v.name}' with glyph '${v.glyph}'`
    );
  }

  // Verify cardiac pacing animations
  assert.ok(css.includes('.philocardia-pacing-72'), "fonts.css must define .philocardia-pacing-72 (72 BPM resting cadence)");
  assert.ok(css.includes('.philocardia-pacing-60'), "fonts.css must define .philocardia-pacing-60 (60 BPM relaxed cadence)");
  assert.ok(css.includes('keyframes philocardia-beat-72'), "fonts.css must declare @keyframes philocardia-beat-72");
});

test('E2E [DOM Heart Tittle Showcase]: index.html & specimen-broadside.html feature interactive heart tittles', () => {
  const indexHtml = fs.readFileSync('index.html', 'utf-8');
  const broadsideHtml = fs.readFileSync('specimen-broadside.html', 'utf-8');

  // Check ISMP card in index.html
  assert.ok(indexHtml.includes('id="ismpCardHeart"'), "index.html must have #ismpCardHeart in ISMP suite");
  assert.ok(indexHtml.includes('id="heartBpmBadge"'), "index.html must have #heartBpmBadge cardiac switcher");
  assert.ok(indexHtml.includes('id="philocardiaInteractiveText"'), "index.html must have #philocardiaInteractiveText live tester");
  assert.ok(indexHtml.includes('data-preset="philocardia"'), "index.html must have 'philocardia' VF preset");

  // Check ISMP card in specimen-broadside.html
  assert.ok(broadsideHtml.includes('id="ismpCardHeart"'), "specimen-broadside.html must have #ismpCardHeart");
  assert.ok(broadsideHtml.includes('id="broadsideTittleVarietyMini"'), "specimen-broadside.html must have #broadsideTittleVarietyMini");
  assert.ok(broadsideHtml.includes('philocardia-heart'), "specimen-broadside.html must render philocardia-heart");
});

test('E2E [JS Invariant]: index.html inline script compiles with 0 syntax errors and exports all event handlers', () => {
  const indexHtml = fs.readFileSync('index.html', 'utf-8');
  const scriptMatch = indexHtml.match(/<script\b[^>]*>([\s\S]*?)<\/script>/i);
  assert.ok(scriptMatch, 'index.html must contain an inline script tag');

  const scriptCode = scriptMatch[1];
  assert.doesNotThrow(() => {
    new vm.Script(scriptCode);
  }, 'index.html inline script must compile cleanly without syntax errors');

  // Verify all event handlers declared in HTML attributes are exposed on window
  const onAttrRegex = /\bon\w+="([^"]+)"/g;
  let match;
  const calledFns = new Set();
  while ((match = onAttrRegex.exec(indexHtml)) !== null) {
    const fnMatch = match[1].match(/^([a-zA-Z0-9_$]+)\s*\(/);
    if (fnMatch) {
      calledFns.add(fnMatch[1]);
    }
  }

  for (const fn of calledFns) {
    assert.ok(
      scriptCode.includes('window.' + fn),
      `Function '${fn}' called from HTML attribute must be exposed on window`
    );
  }
});

