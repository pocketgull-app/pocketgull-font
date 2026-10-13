/**
 * test/closed_caption_studio.test.mjs
 * ====================================
 * Automated Test Suite for PocketGull Closed Caption & Broadcast Teletext Studio:
 * 1. Broadcast Scene Presets and Timed Cue Integrity
 * 2. Variable Font Audio Prosody Weight-Mapping (100..900)
 * 3. CEA-708 & WebVTT Delivery Mode Invariants (Pop-On, Roll-Up, Paint-On)
 * 4. Line-Fitting Dynamic Width Algorithm (75%..100% CPL compliance)
 * 5. Sovereign Indigenous Track & UNDRIP Accord (Inuktitut & Chinuk Pipa)
 * 6. DOM Security & XSS Prevention (Strict textContent Invariant)
 * 7. WCAG AAA & Scotopic 650nm Red Mode Tokens
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

// Import JS Engine
import {
  BROADCAST_SCENES,
  PROSODY_PRESETS,
  ClosedCaptionStudio
} from '../js/closed_caption_studio.js';

test('Closed Caption Studio: Asset Integrity & File Existence', () => {
  const htmlPath = path.join(ROOT_DIR, 'closed_caption_studio.html');
  const cssPath = path.join(ROOT_DIR, 'css', 'closed_caption_studio.css');
  const jsPath = path.join(ROOT_DIR, 'js', 'closed_caption_studio.js');

  assert.ok(fs.existsSync(htmlPath), 'closed_caption_studio.html must exist');
  assert.ok(fs.existsSync(cssPath), 'css/closed_caption_studio.css must exist');
  assert.ok(fs.existsSync(jsPath), 'js/closed_caption_studio.js must exist');
});

test('Broadcast Scene Presets: Completeness & Timed Cues', () => {
  const expectedScenes = ['trauma_bay', 'blizzard_glare', 'midnight_noir', 'eas_alert', 'sovereign_aptn'];
  const actualScenes = Object.keys(BROADCAST_SCENES);

  assert.deepEqual(actualScenes.sort(), expectedScenes.sort(), 'Must define all 5 canonical broadcast scenes');

  for (const [id, scene] of Object.entries(BROADCAST_SCENES)) {
    assert.equal(scene.id, id, `Scene ${id} id must match dictionary key`);
    assert.ok(scene.title.length > 0, `Scene ${id} must have non-empty title`);
    assert.ok(scene.badge.length > 0, `Scene ${id} must declare technical badge`);
    assert.ok(Array.isArray(scene.cues), `Scene ${id} cues must be an array`);
    assert.ok(scene.cues.length >= 4, `Scene ${id} must contain at least 4 timed dialogue cues`);

    for (const cue of scene.cues) {
      assert.ok(cue.speaker.length > 0, `Cue in ${id} must specify speaker`);
      assert.ok(cue.text.length > 0, `Cue in ${id} must contain subtitle text`);
      assert.ok(cue.weight >= 100 && cue.weight <= 900, `Cue weight (${cue.weight}) must be within 100..900`);
      assert.ok(cue.width >= 75 && cue.width <= 100, `Cue width (${cue.width}) must be within 75%..100%`);
      assert.ok(cue.slant <= 0 && cue.slant >= -10.5, `Cue slant (${cue.slant}) must be within 0..-10.5 deg`);
    }
  }
});

test('Variable Font Audio Prosody: Weight Modulation Invariants', () => {
  assert.ok(PROSODY_PRESETS.whisper.weight <= 260, 'Whisper prosody must be light (<= 260 wght)');
  assert.equal(PROSODY_PRESETS.dialogue.weight, 400, 'Conversational dialogue must be regular (400 wght)');
  assert.ok(PROSODY_PRESETS.urgent.weight >= 700, 'Urgent alerts must be bold (>= 700 wght)');
  assert.ok(PROSODY_PRESETS.shout.weight >= 850, 'Shouts and sirens must be heavy display (>= 850 wght)');

  // Verify whisper slant for off-screen/interior monologue
  assert.ok(PROSODY_PRESETS.whisper.slant < 0, 'Whisper prosody should include subtle slant/oblique');
});

test('Line-Fitting Dynamic Width Algorithm: CPL Compliance', () => {
  const studio = new ClosedCaptionStudio();

  // Short line under 37 CPL should remain 100% width
  const normalText = 'Patient heart rate is stable.';
  assert.equal(studio.calculateLineFit(normalText, 37), 100);

  // Long line exceeding 37 CPL should compress width (down to 75% floor)
  const longText = 'Administer Adenosine 6.0 mg rapid IV push immediately with 20 mL saline flush!';
  const compressedWidth = studio.calculateLineFit(longText, 37);
  assert.ok(compressedWidth < 100, 'Long text must trigger width compression');
  assert.ok(compressedWidth >= 75, 'Width compression must not drop below 75% optical floor');
});

test('Sovereign Indigenous Track (UNDRIP Accord): Syllabics & Chinuk Pipa', () => {
  const aptnScene = BROADCAST_SCENES.sovereign_aptn;
  assert.ok(aptnScene, 'Sovereign APTN scene must exist');

  // Verify Inuktitut Syllabics unicode range coverage (U+1400..U+167F)
  const hasInuktitut = aptnScene.cues.some(c => /[\u1400-\u167F]/.test(c.text));
  assert.ok(hasInuktitut, 'APTN scene must contain authentic Canadian Aboriginal Syllabics (ᐆᒫᑦᓱᓯᕆᓂᖅ / ᐃᓄᒃᑎᑐᑦ)');

  // Verify Chinuk Pipa presence
  const hasChinuk = aptnScene.cues.some(c => c.speaker.includes('CHINUK') || c.text.includes('Chinuk'));
  assert.ok(hasChinuk, 'APTN scene must feature Chinuk Pipa / Duployan stenography track');
});

test('Security & DOM Invariant: Strict textContent & Safe Element Construction', () => {
  const htmlContent = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');

  // Must NOT assign dynamic variables to .innerHTML
  assert.ok(!htmlContent.includes('.innerHTML ='), 'closed_caption_studio.html must never use .innerHTML assignment');

  // Must construct roll-up lines and dynamic captions using textContent
  assert.ok(htmlContent.includes('.textContent ='), 'Must use safe .textContent assignment');
  assert.ok(htmlContent.includes('document.createElement'), 'Must use programmatic createElement for DOM construction');
});

test('WCAG AAA & Scotopic 650nm Red Mode: Stylesheet Tokens', () => {
  const cssContent = fs.readFileSync(path.join(ROOT_DIR, 'css', 'closed_caption_studio.css'), 'utf8');

  // Must declare scotopic theme with 650nm red tokens
  assert.ok(cssContent.includes('[data-theme="scotopic"]'), 'Must declare [data-theme="scotopic"]');
  assert.ok(cssContent.includes('#ef4444') || cssContent.includes('#fca5a5'), 'Scotopic theme must use 650nm red/rose tokens');

  // Must declare 16:9 aspect ratio container
  assert.ok(cssContent.includes('aspect-ratio: 16 / 9'), 'Broadcast screen must declare 16:9 aspect ratio');
});

test('Ergonomics & Vibration Isolation: Scoped Vibration & Auto-Reset Timeout', () => {
  const cssContent = fs.readFileSync(path.join(ROOT_DIR, 'css', 'closed_caption_studio.css'), 'utf8');
  const htmlContent = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');

  // Must scope cc-filter-vibe strictly to in-monitor caption elements
  assert.ok(cssContent.includes('.cc-caption-box.cc-filter-vibe'), 'Vibration must be scoped to .cc-caption-box');
  assert.ok(cssContent.includes('.cc-rollup-container.cc-filter-vibe'), 'Vibration must be scoped to .cc-rollup-container');
  assert.ok(cssContent.includes('prefers-reduced-motion'), 'Must support prefers-reduced-motion');

  // Must NOT attach vibration to samplePocketgull or sampleFallback
  assert.ok(!htmlContent.includes('samplePocketgull.classList.add(\'cc-filter-vibe\')'), 'A/B sample must not vibrate');
  assert.ok(!htmlContent.includes('sampleFallback.classList.add(\'cc-filter-vibe\')'), 'A/B fallback must not vibrate');

  // Must have auto-reset timeout
  assert.match(htmlContent, /setTimeout\(\(\)\s*=>\s*\{\s*resetToNormalAcuity\(\);?\s*\},\s*4000\)/, 'Must automatically reset vibration after 4 seconds');
});
