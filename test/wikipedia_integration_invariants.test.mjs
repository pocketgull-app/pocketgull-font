import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Webfont Metric Scaling: fonts.css declares size-adjust: 108% volume parity', () => {
  const cssContent = fs.readFileSync('fonts.css', 'utf8');

  // Verify that size-adjust: 108% is declared in primary cuts
  assert.match(cssContent, /size-adjust:\s*108%/, 'fonts.css must declare size-adjust: 108% for optical volume parity');
  assert.match(cssContent, /ascent-override:\s*96%/, 'fonts.css must declare ascent-override: 96%');
  assert.match(cssContent, /descent-override:\s*22%/, 'fonts.css must declare descent-override: 22%');
});

test('SMoE Expert M: Traditional Mongolian script is declared with 1.18x optical scaling', () => {
  const cssContent = fs.readFileSync('fonts.css', 'utf8');

  // Verify Expert M declaration and unicode-range
  assert.match(cssContent, /Expert M: Traditional Mongolian & Manchu Script/, 'fonts.css must declare Expert M');
  assert.match(cssContent, /font-family:\s*'PocketGull Mongolian'/, 'fonts.css must define PocketGull Mongolian');
  assert.match(cssContent, /unicode-range:[^;]*U\+1800-18AF/, 'PocketGull Mongolian must cover U+1800-18AF');
  assert.match(cssContent, /size-adjust:\s*118%/, 'PocketGull Mongolian must declare 1.18x optical scaling (size-adjust: 118%)');
});

test('SMoE Expansion Experts N–T: Sovereign scripts, telemetry & assistive AAC declared', () => {
  const cssContent = fs.readFileSync('fonts.css', 'utf8');

  assert.match(cssContent, /Expert N: N'Ko Alphabet/, 'fonts.css must declare Expert N (NKOO)');
  assert.match(cssContent, /font-family:\s*'PocketGull NKo'/, 'fonts.css must declare PocketGull NKo');
  assert.match(cssContent, /unicode-range:[^;]*U\+07C0-07FF/, 'NKo must cover U+07C0-07FF');

  assert.match(cssContent, /Expert O: Osage Sovereign Alphabet/, 'fonts.css must declare Expert O (OSGE)');
  assert.match(cssContent, /font-family:\s*'PocketGull Osage'/, 'fonts.css must declare PocketGull Osage');
  assert.match(cssContent, /unicode-range:[^;]*U\+104B0-104FB/, 'Osage must cover U+104B0-104FB');

  assert.match(cssContent, /Expert P: Ogham/, 'fonts.css must declare Expert P (OGHM)');
  assert.match(cssContent, /font-family:\s*'PocketGull Ogham'/, 'fonts.css must declare PocketGull Ogham');
  assert.match(cssContent, /unicode-range:[^;]*U\+1680-169F/, 'Ogham must cover U+1680-169F');

  assert.match(cssContent, /Expert Q: Old Turkic \/ Orkhon Runes/, 'fonts.css must declare Expert Q (ORKH)');
  assert.match(cssContent, /font-family:\s*'PocketGull Old Turkic'/, 'fonts.css must declare PocketGull Old Turkic');
  assert.match(cssContent, /unicode-range:[^;]*U\+10C00-10C4F/, 'Old Turkic must cover U+10C00-10C4F');

  assert.match(cssContent, /Expert R: Sutton SignWriting/, 'fonts.css must declare Expert R (SIGN)');
  assert.match(cssContent, /font-family:\s*'PocketGull SignWriting'/, 'fonts.css must declare PocketGull SignWriting');
  assert.match(cssContent, /unicode-range:[^;]*U\+1D800-1DAAF/, 'SignWriting must cover U+1D800-1DAAF');

  assert.match(cssContent, /Expert S: Sub-Cell ICU ECG & Arrhythmia Telemetry/, 'fonts.css must declare Expert S (CARD)');
  assert.match(cssContent, /font-family:\s*'PocketGull Telemetry ECG'/, 'fonts.css must declare PocketGull Telemetry ECG');
  assert.match(cssContent, /unicode-range:[^;]*U\+E000-E0FF/, 'ECG Telemetry must cover U+E000-E0FF');

  assert.match(cssContent, /Expert T: Blissymbolics AAC/, 'fonts.css must declare Expert T (BLIS)');
  assert.match(cssContent, /font-family:\s*'PocketGull Bliss AAC'/, 'fonts.css must declare PocketGull Bliss AAC');
  assert.match(cssContent, /unicode-range:[^;]*U\+E100-E17F/, 'Blissymbolics must cover U+E100-E17F');
});

test('Wikipedia Integration Kit: Distribution files exist and maintain CSP invariants', () => {
  const userJsPath = path.join('distribution', 'wikipedia', 'pocketgull-wikipedia.user.js');
  const userCssPath = path.join('distribution', 'wikipedia', 'pocketgull-wikipedia.css');
  const readmePath = path.join('distribution', 'wikipedia', 'README.md');

  assert.ok(fs.existsSync(userJsPath), 'pocketgull-wikipedia.user.js must exist');
  assert.ok(fs.existsSync(userCssPath), 'pocketgull-wikipedia.css must exist');
  assert.ok(fs.existsSync(readmePath), 'distribution/wikipedia/README.md must exist');

  const userJsContent = fs.readFileSync(userJsPath, 'utf8');
  assert.match(userJsContent, /\/\/ ==UserScript==/, 'UserScript must contain standard header');
  assert.match(userJsContent, /@match\s+\*:\/\/\*\.wikipedia\.org\/\*/, 'UserScript must match wikipedia.org');
  assert.match(userJsContent, /cdn\.jsdelivr\.net/, 'UserScript must load via CSP-whitelisted jsDelivr');
  assert.match(userJsContent, /--font-family-sans/, 'UserScript must mount Vector 2022 design tokens');
  assert.match(userJsContent, /cv08/, 'UserScript must enable ISMP slashed zero');

  const userCssContent = fs.readFileSync(userCssPath, 'utf8');
  assert.match(userCssContent, /@-moz-document/, 'UserCSS must target domain rules');
  assert.match(userCssContent, /--font-family-sans/, 'UserCSS must declare design tokens');
});

test('Font Sources Invariant: Master source defines 540 UPM x-height screen standard', () => {
  const glyphsContent = fs.readFileSync(path.join('sources', 'PocketGull.glyphs'), 'utf8');
  const matches = glyphsContent.match(/xHeight = (\d+);/g);
  assert.ok(matches && matches.length >= 3, 'PocketGull.glyphs must contain master xHeight declarations');
  for (const m of matches) {
    assert.equal(m, 'xHeight = 540;', 'All masters in PocketGull.glyphs must declare modern 540 UPM x-height standard');
  }
});
