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

test('Emotion Tokens, Atmospheric Blends & Spatial Directions: Archetypal Semiosis', async () => {
  const { EMOTION_TOKENS, ATMOSPHERIC_BLENDS, SPATIAL_DIRECTIONS, ClosedCaptionStudio } = await import('../js/closed_caption_studio.js');

  assert.ok(EMOTION_TOKENS.intimate, 'Must define intimate emotion token');
  assert.ok(EMOTION_TOKENS.panic, 'Must define panic emotion token');
  assert.ok(EMOTION_TOKENS.relief, 'Must define relief emotion token');
  assert.ok(EMOTION_TOKENS.awe, 'Must define awe emotion token');

  assert.ok(ATMOSPHERIC_BLENDS.clinical_teal, 'Must define clinical_teal atmospheric blend');
  assert.ok(ATMOSPHERIC_BLENDS.noir_shadow, 'Must define noir_shadow atmospheric blend');
  assert.ok(ATMOSPHERIC_BLENDS.hearth_amber, 'Must define hearth_amber atmospheric blend');
  assert.ok(ATMOSPHERIC_BLENDS.arctic_frost, 'Must define arctic_frost atmospheric blend');

  assert.ok(SPATIAL_DIRECTIONS.left, 'Must define left spatial direction');
  assert.ok(SPATIAL_DIRECTIONS.center, 'Must define center spatial direction');
  assert.ok(SPATIAL_DIRECTIONS.right, 'Must define right spatial direction');

  const studio = new ClosedCaptionStudio();
  assert.strictEqual(studio.setEmotion('panic')?.id, 'panic');
  assert.strictEqual(studio.setAtmosphericBlend('hearth_amber')?.id, 'hearth_amber');
  assert.strictEqual(studio.setSpatialDirection('left')?.id, 'left');

  // Verify CSS classes exist for acoustic blooming and photometric diffusion
  const cssContent = fs.readFileSync(path.join(ROOT_DIR, 'css', 'closed_caption_studio.css'), 'utf8');
  assert.ok(cssContent.includes('.cc-acoustic-bloom'), 'CSS must declare .cc-acoustic-bloom animation class');
  assert.ok(cssContent.includes('@keyframes cc-bloom-attack'), 'CSS must declare @keyframes cc-bloom-attack');
  assert.ok(cssContent.includes('.cc-photometric-diffusion'), 'CSS must declare .cc-photometric-diffusion');
  assert.ok(cssContent.includes('.cc-spatial-left'), 'CSS must declare .cc-spatial-left');
  assert.ok(cssContent.includes('.cc-spatial-right'), 'CSS must declare .cc-spatial-right');

  // Verify HTML contains emotion, blend, and bloom triggers
  const htmlContent = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  assert.ok(htmlContent.includes('id="triggerBloomBtn"'), 'HTML must declare triggerBloomBtn');
  assert.ok(htmlContent.includes('data-emotion="intimate"'), 'HTML must declare intimate emotion pill');
  assert.ok(htmlContent.includes('data-blend="clinical_teal"'), 'HTML must declare clinical_teal blend pill');
  assert.ok(htmlContent.includes('data-spatial="left"'), 'HTML must declare left spatial pill');
});

test('Philocardia Heart Tittles & Cardiac Pacing Invariants: Grounding & Pacing Rules', async () => {
  const {
    TITTLE_VARIETIES,
    CARDIAC_PACING_PRESETS,
    renderPhilocardiaNodes,
    ClosedCaptionStudio
  } = await import('../js/closed_caption_studio.js');

  // Verify all 6 tittle varieties are registered
  const expectedVarieties = ['heart', 'blossom', 'star', 'droplet', 'nuqta', 'dot'];
  assert.deepEqual(Object.keys(TITTLE_VARIETIES).sort(), expectedVarieties.sort());

  // Verify all 4 cardiac pacing presets
  const expectedPacing = ['pace_72', 'pace_60', 'pace_breath', 'stillness'];
  assert.deepEqual(Object.keys(CARDIAC_PACING_PRESETS).sort(), expectedPacing.sort());

  // Test Studio instance manipulation
  const studio = new ClosedCaptionStudio();
  assert.equal(studio.philocardiaEnabled, false);
  assert.equal(studio.tittleVariety, 'dot');

  studio.setPhilocardia(true);
  assert.equal(studio.philocardiaEnabled, true);
  assert.equal(studio.tittleVariety, 'heart');

  studio.setTittleVariety('blossom');
  assert.equal(studio.tittleVariety, 'blossom');
  assert.equal(studio.philocardiaEnabled, true);

  studio.setCardiacPacing('pace_breath');
  assert.equal(studio.cardiacPacing, 'philocardia-pacing-breath');

  // Test DOM rendering helper (mock container)
  const mockChildren = [];
  const mockContainer = {
    dataset: {},
    replaceChildren() { this.children = []; },
    appendChild(node) { this.children.push(node); },
    children: [],
    removeAttribute(key) { delete this.dataset[key]; }
  };

  // Mock global document if in Node
  const originalDoc = globalThis.document;
  globalThis.document = {
    createElement(tag) {
      return { tagName: tag.toUpperCase(), className: '', textContent: '' };
    },
    createTextNode(text) {
      return { textContent: text, nodeType: 3 };
    }
  };

  try {
    // Render text with 'i' and 'j' in Philocardia mode
    renderPhilocardiaNodes(mockContainer, 'vital sign', 'philocardia-pacing-72', 'heart');
    assert.equal(mockContainer.dataset.tittleVariety, 'heart');
    const heartNodes = mockContainer.children.filter(n => n.className && n.className.includes('philocardia-heart'));
    assert.equal(heartNodes.length, 2, 'Must create 2 philocardia-heart nodes for "vital sign"');
    assert.equal(heartNodes[0].textContent, 'ı', 'Philocardia heart must use dotless i (ı) to prevent double tittle collision');

    // Render with dot (standard) mode
    renderPhilocardiaNodes(mockContainer, 'vital sign', 'philocardia-pacing-72', 'dot');
    assert.equal(mockContainer.textContent, 'vital sign');
    assert.equal(mockContainer.dataset.tittleVariety, undefined);
  } finally {
    globalThis.document = originalDoc;
  }

  // Verify HTML contains Philocardia triggers and reads
  const htmlContent = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  assert.ok(htmlContent.includes('id="togglePhilocardiaBtn"'), 'HTML must declare togglePhilocardiaBtn');
  assert.ok(htmlContent.includes('data-tittle="heart"'), 'HTML must declare heart tittle button');
  assert.ok(htmlContent.includes('data-pacing="pace_72"'), 'HTML must declare pace_72 button');
  assert.ok(htmlContent.includes('data-pacing="stillness"'), 'HTML must declare stillness button');

  // Verify CSS contains stillness override and caption box active glow
  const cssContent = fs.readFileSync(path.join(ROOT_DIR, 'css', 'closed_caption_studio.css'), 'utf8');
  assert.ok(cssContent.includes('.philocardia-stillness::after'), 'CSS must declare .philocardia-stillness::after');
  assert.ok(cssContent.includes('.cc-caption-box.cc-philocardia-active'), 'CSS must declare .cc-caption-box.cc-philocardia-active');
});

test('Physiological Sinus Rhythm & Phosphor-Sweep Telemetry: Zero Phase-Wrap Jump & 600 UPM Column Lock', async () => {
  await import('../js/sinus_telemetry_engine.js');
  const engine = globalThis.PocketGullSinusEngine;
  assert.ok(engine, 'PocketGullSinusEngine must attach to globalThis');

  // 1. Periodic boundary continuity (eliminates wrap-around jump defect)
  const vStart = engine.evaluateCardiacLeadII(0.0, 'sinus', 0);
  const vEnd = engine.evaluateCardiacLeadII(0.9999, 'sinus', 0);
  assert.ok(Math.abs(vStart - vEnd) < 0.005, 'Sinus Lead II must be continuous across phase wrap 1.0 -> 0.0');

  // 2. Cushioned R-wave peak & S-wave nadir anatomy
  const rPeak = engine.evaluateCardiacLeadII(0.35, 'sinus', 0);
  const sNadir = engine.evaluateCardiacLeadII(0.39, 'sinus', 0);
  assert.ok(rPeak > 0.85, `R-wave peak (${rPeak}) must exceed +0.85 normalized mV`);
  assert.ok(sNadir < -0.15, `S-wave nadir (${sNadir}) must dip below -0.15 normalized mV`);

  // 3. Fixed-width PocketGull Mono sub-cell waveform column lock
  for (const cursor of [0, 19, 42, 76]) {
    const leadLine = engine.generateMonospaceWaveString(77, cursor, 72, 'sinus', 4.6);
    const plethLine = engine.generateMonospaceWaveString(77, cursor, 72, 'pleth', 4.6);
    assert.equal(leadLine.length, 77, 'ECG monospace string must maintain exact 77-column width');
    assert.equal(plethLine.length, 77, 'Pleth monospace string must maintain exact 77-column width');
  }

  // 4. Discontinuous stroke-dasharray hack must be absent from closed_caption_studio.html & index.html #hudCardiacStrip
  const ccHtml = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  assert.ok(!ccHtml.includes('id="ccEcgSvg"'), 'Discontinuous ccEcgSvg stroke-dasharray element must be replaced');
  assert.ok(ccHtml.includes('id="ccEcgCanvas"'), 'Phosphor-sweep ccEcgCanvas must be present');
});

test('Broadcast Teletext P888, Cue-Reactive Cardiac State, Reading Metrics & WebVTT Exporter', async () => {
  const { ClosedCaptionStudio, getTeletextSpeakerStyle } = await import('../js/closed_caption_studio.js');
  const studio = new ClosedCaptionStudio();

  // 1. Cue-reactive physiological conversion across Trauma Bay (VTach -> Adenosine -> 74 BPM Sinus)
  studio.setScene('trauma_bay');
  assert.equal(studio.resolveCueCardiacState().morphology, 'vtach');
  assert.equal(studio.resolveCueCardiacState().bpm, 178);

  studio.nextCue(); // Cue 1
  studio.nextCue(); // Cue 2 (Adenosine)
  assert.equal(studio.resolveCueCardiacState().morphology, 'adenosine');
  assert.equal(studio.resolveCueCardiacState().bpm, 108);

  studio.nextCue(); // Cue 3
  studio.nextCue(); // Cue 4 (Sinus restored at 74 BPM)
  assert.equal(studio.resolveCueCardiacState().morphology, 'sinus');
  assert.equal(studio.resolveCueCardiacState().bpm, 74);

  // 2. WST Page 888 Broadcast Teletext delivery protocol
  studio.setMode('teletext');
  assert.equal(studio.mode, 'teletext');
  const sfxStyle = getTeletextSpeakerStyle('MONITOR', 'soundfx', 1);
  assert.equal(sfxStyle.fg, '#4ade80', 'Sound FX must map to WST Teletext green');
  const shoutStyle = getTeletextSpeakerStyle('INSTRUCTION', 'shout', 2);
  assert.equal(shoutStyle.bg, '#b91c1c', 'Emergency shouts must map to WST red alert background');

  // 3. FCC / BBC Saccadic Reading-Speed Metrics
  const calmMetrics = studio.evaluateReadingMetrics('Pulse is stable at 72 bpm.', 3.4);
  assert.equal(calmMetrics.tier, 'optimal');
  const rapidMetrics = studio.evaluateReadingMetrics('DEFIBRILLATOR CHARGED TO 200 JOULES! ADMINISTER EPINEPHRINE 1.0 MG IV STAT IMMEDIATELY!', 3.4);
  assert.equal(rapidMetrics.tier, 'exceeds');
  assert.ok(rapidMetrics.recommendedWidth < 100);

  // 4. Live W3C WebVTT + Variable ::cue Generator
  const vtt = studio.generateWebVtt();
  assert.ok(vtt.startsWith('WEBVTT'), 'Must start with canonical WEBVTT header');
  assert.ok(vtt.includes('::cue(.whisper)'), 'Must include variable ::cue(.whisper) prosody rule');
  assert.ok(vtt.includes('"cv08" 1'), 'Must declare ISMP slashed-zero OpenType feature in ::cue');
});

test('Phanvas Genre Narrative Arc Generator: 5-Beat Genre Synthesis, Tension BPM & WebVTT Staging', async () => {
  const {
    NARRATIVE_ARC_GENRES,
    NarrativeArcGenerator,
    ClosedCaptionStudio
  } = await import('../js/closed_caption_studio.js');

  const expectedGenres = ['noir_mystery', 'scifi_telemetry', 'clinical_documentary', 'folktale_awen', 'thriller_pulse'];
  assert.deepEqual(Object.keys(NARRATIVE_ARC_GENRES).sort(), expectedGenres.sort(), 'Must define all 5 narrative genres');

  const arc = NarrativeArcGenerator.generateArc('scifi_telemetry', 'Signalman Mira <script>');
  assert.equal(arc.id, 'narrative_arc');
  assert.equal(arc.cues.length, 5, 'Generated narrative arc must produce 5 timecoded beats');
  assert.ok(!arc.seed.includes('<script>'), 'Must strip angle brackets from story premise seed');
  assert.ok(arc.cues[2].bpm >= 140, 'Climax beat must elevate telemetry BPM');
  assert.ok(arc.cues.every(c => c.width >= 75 && c.width <= 100), 'All story beats must enforce 75..100% CPL width');

  const studio = new ClosedCaptionStudio();
  studio.setCustomScene(arc);
  assert.equal(studio.getScene().cues.length, 5);
  assert.equal(studio.resolveCueCardiacState().bpm, 64, 'Beat 0 Exposition BPM must map into cardiac monitor');

  studio.nextCue();
  studio.nextCue(); // Climax
  assert.equal(studio.resolveCueCardiacState().morphology, 'vtach', 'Climax beat must drive high-acuity morphology');

  const arcVtt = studio.generateWebVtt();
  assert.ok(arcVtt.includes('Signalman Mira'), 'Staged narrative arc seed must export into WebVTT tracks');

  // Verify HTML wiring uses zero innerHTML and contains Genre Narrative Arc controls
  const ccHtml = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  assert.ok(!ccHtml.includes('.innerHTML ='), 'closed_caption_studio.html must remain free of .innerHTML assignments');
  assert.ok(ccHtml.includes('id="ccNarrativeArcSection"'), 'HTML must expose Phanvas Genre Narrative Arc section');
  assert.ok(ccHtml.includes('id="ccArcSvg"'), 'HTML must expose interactive SVG tension spline');
});

test('PHL 197 Manufacturing Reality Deconstruction Lens, Infotainment A/B & WebVTT NOTE Rubric', async () => {
  const {
    PHL197_STANCES,
    PHL197_THINKER_LENSES,
    evaluateDeconstructionLens,
    ClosedCaptionStudio
  } = await import('../js/closed_caption_studio.js');

  assert.deepEqual(Object.keys(PHL197_STANCES).sort(), ['assent', 'negotiate', 'resist']);
  assert.deepEqual(Object.keys(PHL197_THINKER_LENSES).sort(), ['baudrillard', 'gleick', 'mcluhan', 'postman']);

  const alarmRes = evaluateDeconstructionLens(
    { speaker: 'DR. ARIS', text: 'Administer Adenosine 6.0 mg IV immediately!', prosody: 'urgent', weight: 780, width: 92, slant: 0, aptr: 85 },
    { id: 'trauma_bay', title: 'Trauma Bay' },
    'resist',
    'gleick'
  );
  assert.equal(alarmRes.framingMode, 'High-Arousal Chyron / Alarm');
  assert.ok(alarmRes.howDoIKnow.includes('6.0 mg'), 'Deconstruction lens must isolate quantified clinical claim for verification');
  assert.ok(alarmRes.thinkerNote.includes('Gleick'), 'Must cite selected syllabus thinker');

  const studio = new ClosedCaptionStudio();
  assert.equal(studio.generateWebVtt().includes('NOTE [PHL-197 DECONSTRUCTION]'), false, 'WebVTT NOTE rubric must be opt-in');

  studio.setDeconstructionStance('resist');
  studio.setThinkerLens('baudrillard');
  studio.setIncludeDeconstructionNotes(true);
  const annotatedVtt = studio.generateWebVtt();
  assert.ok(annotatedVtt.includes('NOTE [PHL-197 DECONSTRUCTION]'), 'Enabled rubric must add PHL-197 header NOTE');
  assert.ok(annotatedVtt.includes('NOTE [PHL-197 Cue 1]'), 'Enabled rubric must add per-cue How-Do-I-Know NOTE');
  assert.ok(annotatedVtt.includes('Stance: RESIST'), 'WebVTT NOTE must record active PHL 197 stance');

  const ccHtml = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  assert.ok(ccHtml.includes('id="ccPhl197Section"'), 'HTML must declare PHL 197 Deconstruction section');
  assert.ok(ccHtml.includes('id="ccInfotainmentSample"'), 'HTML must declare Infotainment framing comparator');
  assert.ok(ccHtml.includes('id="ccClinicalTruthSample"'), 'HTML must declare Clinical Truth framing comparator');
});

test('Emotional Letterform Fine-Tuning: Normalized 0..1 APTR, Multi-Axis gvar Morphology & Smooth Transitions', async () => {
  const {
    EMOTION_TOKENS,
    PROSODY_PRESETS,
    normalizeAptr,
    buildVariationString
  } = await import('../js/closed_caption_studio.js');

  assert.equal(normalizeAptr(65), 0.65, 'Legacy 0..100 integer APTR must normalize to 0.65');
  assert.equal(normalizeAptr(0.35), 0.35, '0..1 APTR values must remain unchanged');
  assert.equal(normalizeAptr(1.8), 0.02, 'Out-of-range >1 inputs normalize cleanly within [0,1]');

  for (const [id, token] of Object.entries(EMOTION_TOKENS)) {
    assert.ok(token.aptr >= 0 && token.aptr <= 1, `Emotion ${id} aptr (${token.aptr}) must fit VF fvar 0..1`);
    assert.ok(token.soft >= 0 && token.soft <= 1, `Emotion ${id} soft must fit VF fvar 0..1`);
    assert.ok(token.hlng >= 0 && token.hlng <= 1, `Emotion ${id} hlng must fit VF fvar 0..1`);
    assert.ok(token.boum >= 0 && token.boum <= 1, `Emotion ${id} boum must fit VF fvar 0..1`);
    assert.ok(token.opsz >= 6 && token.opsz <= 72, `Emotion ${id} opsz must fit VF fvar 6..72`);
  }

  const intimate = EMOTION_TOKENS.intimate;
  const panic = EMOTION_TOKENS.panic;
  const relief = EMOTION_TOKENS.relief;
  const awe = EMOTION_TOKENS.awe;
  assert.ok(intimate.soft > panic.soft, 'Intimate whisper state must soften terminals more than panic');
  assert.ok(relief.hlng > panic.hlng, 'Vagal relief state must elevate healing curve above panic');
  assert.ok(awe.boum > panic.boum, 'Cosmic awe state must elevate bouma swell above panic');
  assert.ok(PROSODY_PRESETS.whisper.aptr >= 0 && PROSODY_PRESETS.whisper.aptr <= 1);

  const varStr = buildVariationString(EMOTION_TOKENS.relief);
  assert.ok(varStr.includes("'SOFT' 0.9"), 'Variation string must drive SOFT axis');
  assert.ok(varStr.includes("'HLNG' 1"), 'Variation string must drive HLNG axis');
  assert.ok(varStr.includes("'BOUM' 0.6"), 'Variation string must drive BOUM axis');
  assert.ok(varStr.includes("'APTR' 0.7"), 'Variation string must drive normalized APTR axis');

  const ccHtml = fs.readFileSync(path.join(ROOT_DIR, 'closed_caption_studio.html'), 'utf8');
  const ccCss = fs.readFileSync(path.join(ROOT_DIR, 'css', 'closed_caption_studio.css'), 'utf8');

  assert.ok(ccHtml.includes('id="aptrSlider" min="0" max="1"'), 'APTR slider must span 0..1 matching PocketGull-VF fvar');
  assert.ok(ccHtml.includes('id="softSlider"'), 'HTML must expose SOFT emotional slider');
  assert.ok(ccHtml.includes('id="hlngSlider"'), 'HTML must expose HLNG emotional slider');
  assert.ok(ccHtml.includes('id="boumSlider"'), 'HTML must expose BOUM emotional slider');
  assert.ok(ccHtml.includes('id="ccEmotionMorphGrid"'), 'HTML must expose Emotion Morph Comparison Strip');
  assert.ok(ccHtml.includes('studio.setEmotion(null)'), 'Toggling emotion off must reset studio.currentEmotion');
  assert.ok(!ccHtml.includes('.innerHTML ='), 'HTML must preserve zero .innerHTML assignments');
  assert.ok(ccCss.includes('font-variation-settings 0.36s'), 'Caption line must smoothly transition font-variation-settings');
  assert.ok(!ccCss.includes("'APTR' 95"), 'CSS keyframes/samples must not clamp APTR above 1.0');
});


