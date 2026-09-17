import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const typefaceCssPath = path.join('pocketgull.css');
const markerCssPath = path.join('..', 'pocketgull', 'src', 'styles', 'pocketgull-marker-font.css');

test('Clinical Typographic Spellcheck: CSS contains wavy red underline error selectors', () => {
  assert.ok(fs.existsSync(typefaceCssPath), 'pocketgull.css must exist');
  const css = fs.readFileSync(typefaceCssPath, 'utf8');

  assert.match(css, /underline wavy #ef4444/, 'pocketgull.css must define red wavy underline for clinical spellcheck errors');
  assert.match(css, /data-clinical-error/, 'pocketgull.css must support [data-clinical-error]');
  assert.match(css, /data-dosage-status="overdose"/, 'pocketgull.css must support [data-dosage-status="overdose"]');
  assert.match(css, /naked-decimal-error/, 'pocketgull.css must define .naked-decimal-error');
  assert.match(css, /trailing-zero-error/, 'pocketgull.css must define .trailing-zero-error');
  assert.match(css, /posology-age-mismatch/, 'pocketgull.css must define .posology-age-mismatch');
});

test('Clinical Typographic Spellcheck: Caution & Misalignment amber wavy underlines', () => {
  const css = fs.readFileSync(typefaceCssPath, 'utf8');
  assert.match(css, /underline wavy #f59e0b/, 'pocketgull.css must define amber wavy underline for warnings/misalignment');
  assert.match(css, /data-misaligned/, 'pocketgull.css must support [data-misaligned]');
  assert.match(css, /subtherapeutic/, 'pocketgull.css must support subtherapeutic warnings');
});

test('Multi-Paradigm OpenType Modes: All five epistemological paradigms present', () => {
  const css = fs.readFileSync(typefaceCssPath, 'utf8');
  assert.match(css, /\.font-paradigm-allopathic/, '.font-paradigm-allopathic must be defined');
  assert.match(css, /\.font-paradigm-ayurvedic/, '.font-paradigm-ayurvedic must be defined');
  assert.match(css, /\.font-paradigm-tcm/, '.font-paradigm-tcm must be defined');
  assert.match(css, /\.font-paradigm-osteopathic/, '.font-paradigm-osteopathic must be defined');
  assert.match(css, /\.font-paradigm-homeopathic/, '.font-paradigm-homeopathic must be defined');
});

test('Chemical Formula Stoichiometry & 0.1Hz Breathing rules', () => {
  const css = fs.readFileSync(typefaceCssPath, 'utf8');
  assert.match(css, /\.font-pocketgull-chem-formula/, '.font-pocketgull-chem-formula must be defined');
  assert.match(css, /sinf/, 'sinf feature must be enabled for chemistry');
  assert.match(css, /\.font-parasympathetic-breathing/, '.font-parasympathetic-breathing must be defined');
  assert.match(css, /parasympatheticPacing/, 'parasympatheticPacing keyframes must be present');
  assert.match(css, /prefers-reduced-motion/, 'prefers-reduced-motion override must be present');
});

test('Web Client Marker CSS: pocketgull-marker-font.css has full parity with typeface CSS', () => {
  if (fs.existsSync(markerCssPath)) {
    const markerCss = fs.readFileSync(markerCssPath, 'utf8');
    assert.match(markerCss, /underline wavy #ef4444/, 'marker CSS must contain clinical red wavy error underline');
    assert.match(markerCss, /posology-neonate/, 'marker CSS must contain neonate posology');
    assert.match(markerCss, /posology-pediatric/, 'marker CSS must contain pediatric posology');
    assert.match(markerCss, /posology-geriatric/, 'marker CSS must contain geriatric posology');
    assert.match(markerCss, /bmp-fishbone/, 'marker CSS must contain BMP fishbone');
    assert.match(markerCss, /cbc-fishbone/, 'marker CSS must contain CBC fishbone');
  }
});
