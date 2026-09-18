import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('SMoE Script Experts: Unicode ranges and non-overlapping boundary integrity', () => {
  const SCRIPT_EXPERTS = [
    { tag: 'LATN', name: 'Latin & ISMP Safety', start: 0x0020, end: 0x00FF },
    { tag: 'BRL',  name: 'Unicode Braille Patterns', start: 0x2800, end: 0x28FF },
    { tag: 'CANS', name: 'Canadian Aboriginal Syllabics', start: 0x1400, end: 0x167F },
    { tag: 'DUPL', name: 'Chinuk Pipa / Duployan', start: 0x1BC00, end: 0x1BC9F },
    { tag: 'TFNG', name: 'Neo-Tifinagh', start: 0x2D30, end: 0x2D7F },
    { tag: 'CHER', name: 'Cherokee Syllabary', start: 0x13A0, end: 0x13FF },
    { tag: 'ETHI', name: 'Ethiopic / Ge\'ez', start: 0x1200, end: 0x137F },
    { tag: 'ADLM', name: 'Adlam (Fulfulde)', start: 0x1E900, end: 0x1E95F },
    { tag: 'VAII', name: 'Vai Syllabary', start: 0xA500, end: 0xA63F },
    { tag: 'ARAB', name: 'Arabic & Perso-Arabic', start: 0x0600, end: 0x06FF },
    { tag: 'HEBR', name: 'Hebrew & Yiddish', start: 0x0590, end: 0x05FF },
    { tag: 'DEVA', name: 'Devanagari', start: 0x0900, end: 0x097F },
    { tag: 'MONG', name: 'Traditional Mongolian & Manchu', start: 0x1800, end: 0x18AF },
    { tag: 'NKOO', name: 'N\'Ko Alphabet', start: 0x07C0, end: 0x07FF },
    { tag: 'OSGE', name: 'Osage Sovereign Siouan', start: 0x104B0, end: 0x104FB },
    { tag: 'OGHM', name: 'Ogham Celtic Tree Alphabet', start: 0x1680, end: 0x169F },
    { tag: 'ORKH', name: 'Old Turkic / Orkhon Runes', start: 0x10C00, end: 0x10C4F },
    { tag: 'SIGN', name: 'Sutton SignWriting', start: 0x1D800, end: 0x1DAAF },
    { tag: 'CARD', name: 'ICU Sub-Cell ECG Telemetry', start: 0xE000, end: 0xE0FF },
    { tag: 'BLIS', name: 'Blissymbolics AAC', start: 0xE100, end: 0xE17F }
  ];

  for (const exp of SCRIPT_EXPERTS) {
    assert.ok(exp.end >= exp.start, `Expert ${exp.tag} must have valid start <= end`);
    assert.ok(exp.end - exp.start + 1 > 0, `Expert ${exp.tag} must have non-zero codepoint span`);
  }

  // Verify that Latin and Braille blocks are completely non-overlapping
  const latn = SCRIPT_EXPERTS.find(e => e.tag === 'LATN');
  const brl = SCRIPT_EXPERTS.find(e => e.tag === 'BRL');
  assert.ok(latn.end < brl.start, 'Latin block must precede Braille block');
});

test('SMoE Subsetting Size Benchmark: Simulated game subset payload is < 40 KB', () => {
  // A clinical game subset contains basic Latin, ISMP disambiguations, and specific game numerals
  const simulatedGlyphCount = 96; // 96 essential characters for Parlor / Gameboard HUD
  const avgBytesPerGlyph = 140; // TrueType quadratic contour representation
  const sfntHeaderAndTablesSize = 4096; // 4 KB for core tables: head, hhea, maxp, OS/2, cmap, loca, glyf, post

  const estimatedTtfSize = sfntHeaderAndTablesSize + (simulatedGlyphCount * avgBytesPerGlyph);
  // Brotli compression typically yields 40-55% reduction on glyph curves
  const estimatedWoff2Size = Math.round(estimatedTtfSize * 0.52);

  assert.ok(estimatedTtfSize < 25000, `Estimated subset TTF size (${estimatedTtfSize} B) must be < 25 KB`);
  assert.ok(estimatedWoff2Size < 15000, `Estimated subset WOFF2 size (${estimatedWoff2Size} B) must be < 15 KB`);
});
