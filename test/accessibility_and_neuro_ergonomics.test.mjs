import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

// Import data module
import {
  TELEMETRY_BADGES,
  WONG_BAKER_FACES,
  ICU_PHYSIOLOGICAL_NEEDS,
  ASYMMETRIC_MIRROR_PAIRS,
  ISMP_DISAMBIGUATION_DATA,
  NEMETH_BRAILLE_MAPPINGS,
  DALTONISM_FILTERS,
  BUILTIN_LANGUAGES,
  generateLanguageTemplateJson,
  serializeBedsideBoard,
  deserializeBedsideBoard
} from '../js/a11y_neuro_ergonomics_data.js';

test('A11y Dataset: Telemetry Badges & Monochromatic Redundancy (WCAG 1.4.1)', () => {
  assert.equal(TELEMETRY_BADGES.length, 5, 'Must contain all 5 canonical telemetry status badges');

  const requiredIds = ['CRIT', 'HIGH', 'LOW', 'HOLD', 'NORM'];
  const foundIds = TELEMETRY_BADGES.map(b => b.id);
  assert.deepEqual(foundIds, requiredIds, 'Must declare exact telemetry badge IDs');

  const shapes = new Set();
  for (const badge of TELEMETRY_BADGES) {
    assert.ok(badge.label.length > 0, `Badge ${badge.id} must have non-empty label`);
    assert.ok(badge.shape.length > 0, `Badge ${badge.id} must have non-empty geometric shape`);
    shapes.add(badge.shape);

    // Vibration-proof minimum stroke floor (>= 75 UPM)
    assert.ok(
      badge.strokeUpm >= 75,
      `Badge ${badge.id} stroke (${badge.strokeUpm} UPM) must meet vibration floor (>= 75 UPM)`
    );

    // WCAG AAA Luminous Contrast benchmark (>= 7:1)
    assert.ok(
      badge.contrastRatio >= 7.0,
      `Badge ${badge.id} contrast (${badge.contrastRatio}:1) must exceed WCAG AAA (>= 7:1)`
    );

    // Standard tabular em-square advance metrics (600, 1000, or 1200 UPM)
    assert.ok(
      [600, 1000, 1200].includes(badge.advanceUpm),
      `Badge ${badge.id} advance (${badge.advanceUpm} UPM) must be tabular integer`
    );
  }

  // Non-reliance on color: every badge has a unique geometric silhouette
  assert.equal(shapes.size, 5, 'Every telemetry badge must feature a unique geometric shape');
});

test('A11y Dataset: Wong-Baker FACES Pain Scale Completeness (0-10)', () => {
  assert.equal(WONG_BAKER_FACES.length, 6, 'Must contain all 6 standard Wong-Baker pain steps');

  const expectedScores = [0, 2, 4, 6, 8, 10];
  const actualScores = WONG_BAKER_FACES.map(f => f.score);
  assert.deepEqual(actualScores, expectedScores, 'Scores must be 0, 2, 4, 6, 8, 10');

  for (const face of WONG_BAKER_FACES) {
    assert.ok(face.name.length > 0, `Face ${face.score} must have descriptive title`);
    assert.ok(face.triageLevel.length > 0, `Face ${face.score} must have triage severity`);
    assert.ok(face.speechPrompt.length > 0, `Face ${face.score} must have Web Speech utterance`);
    assert.ok(face.svgIcon.includes('<svg'), `Face ${face.score} must have vector SVG path`);
  }
});

test('A11y Dataset: ICU Physiological & Emotional Need Board (12 Tiles)', () => {
  assert.equal(ICU_PHYSIOLOGICAL_NEEDS.length, 12, 'Must provide 12 emergency communication tiles');

  const requiredKeys = ['WATER', 'PAIN', 'COLD', 'WARM', 'REPOSITION', 'FAMILY', 'SUCTION', 'MEDICINE', 'RESTROOM', 'LIGHTS', 'QUESTION', 'YES_NO'];
  const actualKeys = ICU_PHYSIOLOGICAL_NEEDS.map(n => n.id);
  assert.deepEqual(actualKeys, requiredKeys, 'Must cover essential ICU communication intents');

  for (const item of ICU_PHYSIOLOGICAL_NEEDS) {
    assert.ok(item.title.length > 0, `Need ${item.id} must have title`);
    assert.ok(item.category.length > 0, `Need ${item.id} must have category`);
    assert.ok(item.spokenText.length > 0, `Need ${item.id} must have natural speech prompt`);
    assert.ok(item.codePoint.startsWith('U+E1'), `Need ${item.id} must declare AAC codePoint`);
  }
});

test('A11y Dataset: Multilingual ICU Packs & Bedside Board Co-Creation', () => {
  // Builtin languages
  assert.ok(BUILTIN_LANGUAGES.en, 'Must have English pack');
  assert.ok(BUILTIN_LANGUAGES.es, 'Must have Spanish pack');
  assert.ok(BUILTIN_LANGUAGES.fr, 'Must have French pack');
  assert.ok(BUILTIN_LANGUAGES.de, 'Must have German pack');

  for (const [langKey, lang] of Object.entries(BUILTIN_LANGUAGES)) {
    assert.equal(lang.code, langKey);
    assert.ok(lang.name.length > 0);
    assert.ok(lang.nativeName.length > 0);
    assert.equal(Object.keys(lang.needs).length, 12, `${langKey} must translate all 12 ICU needs`);
    assert.equal(Object.keys(lang.faces).length, 6, `${langKey} must translate all 6 Wong-Baker faces`);
  }

  // Template generation
  const templateJson = generateLanguageTemplateJson("Tagalog", "tl");
  const parsed = JSON.parse(templateJson);
  assert.equal(parsed.code, "tl");
  assert.equal(Object.keys(parsed.needs).length, 12);
  assert.equal(Object.keys(parsed.faces).length, 6);

  // Bedside serialization & roundtrip
  const testTiles = [
    { title: "Grandkids", spokenText: "Could you tell me about the grandkids?", category: "Family", emoji: "👶" },
    { title: "Hold Hand", spokenText: "Could you please hold my hand?", category: "Comfort", emoji: "🤝" }
  ];

  const serialized = serializeBedsideBoard(testTiles);
  assert.ok(serialized.length > 0, 'Must produce Base64 serialized string');

  const deserialized = deserializeBedsideBoard(serialized);
  assert.equal(deserialized.length, 2, 'Must deserialize exactly 2 tiles');
  assert.equal(deserialized[0].title, "Grandkids");
  assert.equal(deserialized[0].spokenText, "Could you tell me about the grandkids?");
  assert.equal(deserialized[0].emoji, "👶");
  assert.equal(deserialized[1].title, "Hold Hand");
});

test('A11y Dataset: Asymmetric Mirror Disambiguation Pairs (b/d, p/q, n/u, m/w)', () => {
  assert.equal(ASYMMETRIC_MIRROR_PAIRS.length, 4, 'Must define all 4 primary dyslexic mirror confusions');

  const pairs = ASYMMETRIC_MIRROR_PAIRS.map(p => p.pair);
  assert.ok(pairs.includes('b / d'), 'b/d pair must be defined');
  assert.ok(pairs.includes('p / q'), 'p/q pair must be defined');
  assert.ok(pairs.includes('n / u'), 'n/u pair must be defined');
  assert.ok(pairs.includes('m / w'), 'm/w pair must be defined');

  for (const p of ASYMMETRIC_MIRROR_PAIRS) {
    assert.ok(p.pocketGullSolution.length > 0, `Pair ${p.pair} must define geometric solution`);
    assert.ok(p.apexAngleA.length > 0, `Pair ${p.pair} must specify apex feature A`);
    assert.ok(p.apexAngleB.length > 0, `Pair ${p.pair} must specify apex feature B`);
  }
});

test('A11y Dataset: Nemeth Braille STEM Math Duality (U+2800 Block)', () => {
  assert.ok(NEMETH_BRAILLE_MAPPINGS.length >= 10, 'Must include at least 10 core mathematical operators');

  for (const mapping of NEMETH_BRAILLE_MAPPINGS) {
    assert.ok(mapping.visual.length > 0, `Mapping ${mapping.name} must have visual symbol`);
    assert.ok(mapping.brailleChar.length > 0, `Mapping ${mapping.name} must have tactile braille char`);

    // Verify Braille chars fall within Unicode Braille block U+2800..U+28FF
    for (const char of mapping.brailleChar) {
      const cp = char.codePointAt(0);
      assert.ok(
        cp >= 0x2800 && cp <= 0x28FF,
        `Braille char "${char}" in ${mapping.name} must be within U+2800..U+28FF`
      );
    }
  }
});

test('A11y Dataset: Daltonism Color Matrix Specifications', () => {
  assert.equal(DALTONISM_FILTERS.length, 5, 'Must define 5 vision modes');

  for (const filter of DALTONISM_FILTERS) {
    const values = filter.matrix.trim().split(/\s+/).map(Number);
    assert.equal(values.length, 20, `Filter ${filter.id} matrix must have 20 matrix values (4x5)`);
    assert.ok(values.every(v => !isNaN(v)), `Filter ${filter.id} must have valid numerical values`);
  }
});

test('A11y CSS Invariants: BDA Spacing & IRRD OLED Compensation', () => {
  const cssPath = path.join(ROOT_DIR, 'css', 'a11y_neuro_ergonomics.css');
  assert.ok(fs.existsSync(cssPath), 'css/a11y_neuro_ergonomics.css must exist');

  const css = fs.readFileSync(cssPath, 'utf8');

  // Retinal Irradiation mode
  assert.ok(css.includes('.pg-irrd-compensated'), 'Must declare .pg-irrd-compensated');
  assert.ok(css.includes('font-weight: 385'), 'Must declare optical weight thinning');

  // British Dyslexia Association (BDA) & WCAG 1.4.12 Text Spacing
  assert.ok(css.includes('.pg-crowding-relief'), 'Must declare .pg-crowding-relief');
  assert.ok(css.includes('letter-spacing: 0.12em'), 'Must declare BDA letter-spacing: 0.12em');
  assert.ok(css.includes('word-spacing: 0.18em'), 'Must declare BDA word-spacing: 0.18em');

  // Telemetry status badge styles
  assert.ok(css.includes('.pg-badge-crit'), 'Must declare .pg-badge-crit');
  assert.ok(css.includes('.pg-badge-high'), 'Must declare .pg-badge-high');
  assert.ok(css.includes('.pg-badge-low'), 'Must declare .pg-badge-low');
  assert.ok(css.includes('.pg-badge-hold'), 'Must declare .pg-badge-hold');
  assert.ok(css.includes('.pg-badge-norm'), 'Must declare .pg-badge-norm');
});

test('A11y Web Specimen: a11y_studio.html Security & DOM Invariants', () => {
  const htmlPath = path.join(ROOT_DIR, 'a11y_studio.html');
  assert.ok(fs.existsSync(htmlPath), 'a11y_studio.html must exist');

  const html = fs.readFileSync(htmlPath, 'utf8');

  // Check structure
  assert.ok(html.includes('id="panel-irrd"'), 'Must have Retinal Glare panel');
  assert.ok(html.includes('id="panel-neuro"'), 'Must have Neurodiversity panel');
  assert.ok(html.includes('id="panel-telemetry"'), 'Must have Telemetry panel');
  assert.ok(html.includes('id="panel-aac"'), 'Must have Non-Verbal ICU AAC panel');
  assert.ok(html.includes('id="panel-nemeth"'), 'Must have Nemeth Braille STEM panel');

  // Check SVG Daltonism filters
  assert.ok(html.includes('id="filter-protanopia"'), 'Must define Protanopia filter');
  assert.ok(html.includes('id="filter-deuteranopia"'), 'Must define Deuteranopia filter');
  assert.ok(html.includes('id="filter-tritanopia"'), 'Must define Tritanopia filter');
  assert.ok(html.includes('id="filter-monochromacy"'), 'Must define Monochromacy filter');

  // Check DOM XSS safety: Bionic reading must construct DOM elements safely
  assert.ok(html.includes('document.createElement(\'span\')'), 'Bionic rendering must use safe DOM elements');
  assert.ok(html.includes('document.createTextNode'), 'Bionic rendering must use safe text nodes');
});

test('Dart Foundry Engine: a11y_engine.dart Exists & Has Geometric Methods', () => {
  const dartPath = path.join(ROOT_DIR, 'tool', 'foundry', 'a11y_engine.dart');
  assert.ok(fs.existsSync(dartPath), 'tool/foundry/a11y_engine.dart must exist');

  const dart = fs.readFileSync(dartPath, 'utf8');
  assert.ok(dart.includes('class A11yEngine'), 'Must declare A11yEngine class');
  assert.ok(dart.includes('generateOctagonCrit'), 'Must implement generateOctagonCrit');
  assert.ok(dart.includes('generateTriangleHigh'), 'Must implement generateTriangleHigh');
  assert.ok(dart.includes('generateTriangleLow'), 'Must implement generateTriangleLow');
  assert.ok(dart.includes('generateDiamondHold'), 'Must implement generateDiamondHold');
  assert.ok(dart.includes('generateCircleNorm'), 'Must implement generateCircleNorm');
  assert.ok(dart.includes('generateWongBakerFace'), 'Must implement generateWongBakerFace');
});

test('A11y Dataset: ISMP Disambiguation Suite & Bézier Geometry Invariants', () => {
  assert.ok(ISMP_DISAMBIGUATION_DATA, 'ISMP_DISAMBIGUATION_DATA must be exported');
  const expectedKeys = [
    'b_vs_d', 'p_vs_q', 'n_vs_u', 'm_vs_w',
    'slashed_zero', 'curved_l', 'serifed_I', 'slashed_z',
    'tall_man', 'bionic_reading', 'philocardia_hearts', 'asclepius'
  ];

  for (const key of expectedKeys) {
    const item = ISMP_DISAMBIGUATION_DATA[key];
    assert.ok(item, `Entry for ${key} must exist`);
    assert.ok(item.cardTitle.length > 0, `${key} must have cardTitle`);
    assert.ok(item.featureName.length > 0, `${key} must have featureName`);
    assert.ok(item.badgeLabel.length > 0, `${key} must have badgeLabel`);
    assert.ok(item.failureModePrevented.length > 0, `${key} must have failureModePrevented`);
    assert.ok(item.gravitationalOffset.length > 0, `${key} must have gravitationalOffset`);
    assert.ok(item.regulatoryClause.length > 0, `${key} must cite regulatory standard clause`);
  }

  // Check enriched ASYMMETRIC_MIRROR_PAIRS
  for (const pair of ASYMMETRIC_MIRROR_PAIRS) {
    assert.ok(pair.bezierControlPolygonA.length > 0, `${pair.pair} must have Bézier polygon A`);
    assert.ok(pair.bezierControlPolygonB.length > 0, `${pair.pair} must have Bézier polygon B`);
    assert.ok(pair.deCasteljauMidpoint, `${pair.pair} must declare De Casteljau midpoint`);
    assert.equal(pair.deCasteljauMidpoint.t, 0.5, `${pair.pair} midpoint parameter t must be 0.5`);
    assert.ok(pair.optometricApertureClearance >= 200, `${pair.pair} aperture clearance must meet Louise Sloan floor (>= 200 UPM)`);
  }
});

test('Regulatory Standard: FDA_ISMP_CLINICAL_DIGITAL_TYPOGRAPHY_SPECIFICATION.md Exists & Validated', () => {
  const specPath = path.join(ROOT_DIR, 'standards', 'FDA_ISMP_CLINICAL_DIGITAL_TYPOGRAPHY_SPECIFICATION.md');
  assert.ok(fs.existsSync(specPath), 'standards/FDA_ISMP_CLINICAL_DIGITAL_TYPOGRAPHY_SPECIFICATION.md must exist');

  const spec = fs.readFileSync(specPath, 'utf8');

  // Verify Core Consensus Designations & Regulatory Frameworks
  assert.ok(spec.includes('POCKETGULL-STD-2026-01'), 'Must declare standard designation POCKETGULL-STD-2026-01');
  assert.ok(spec.includes('AAMI/ISMP CDTS-1'), 'Must declare AAMI/ISMP CDTS-1');
  assert.ok(spec.includes('FDA CDRH'), 'Must reference FDA CDRH MDDT');
  assert.ok(spec.includes('FDA CDER DMEPA'), 'Must reference FDA CDER DMEPA');
  assert.ok(spec.includes('ANSI/AAMI HE75'), 'Must reference ANSI/AAMI HE75');

  // Verify Central Clinical Case Study: Neurodiversity & Circadian Exhaustion (The Curb-Cut Effect)
  assert.ok(spec.includes('Curb-Cut Effect'), 'Must detail the Curb-Cut Effect');
  assert.ok(spec.includes('Neurodiversity'), 'Must establish Neurodiversity as central case study');
  assert.ok(spec.includes('Dyslexia'), 'Must detail dyslexia mirror-inversion');
  assert.ok(spec.includes('Circadian Exhaustion') || spec.includes('Circadian Inversion'), 'Must detail circadian exhaustion');

  // Verify The 6 Mandatory Invariants
  assert.ok(spec.includes('Louise Sloan 5:1 Optotype Proportions'), 'Must mandate Invariant 1: Sloan 5:1 Optotypes');
  assert.ok(spec.includes('Asymmetric Gravitational Grounding'), 'Must mandate Invariant 2: Asymmetric Grounding');
  assert.ok(spec.includes('ISMP Clinical Disambiguation Quartet'), 'Must mandate Invariant 3: ISMP Quartet');
  assert.ok(spec.includes('Monochromatic Telemetry Enclosures'), 'Must mandate Invariant 4: Monochromatic Enclosures');
  assert.ok(spec.includes('De Casteljau Midpoint Subdivision'), 'Must mandate Invariant 5: De Casteljau Subdivision');
  assert.ok(spec.includes('Trauma-Informed Sensory Ergonomics'), 'Must mandate Invariant 6: Trauma-Informed Ergonomics');

  // Verify ANSI/AAMI HE75 Amendment Language
  assert.ok(spec.includes('Section 18.3.1.1'), 'Must provide proposed ANSI/AAMI HE75 Section 18.3 amendment language');
  assert.ok(spec.includes('loca[i] % 2 == 0'), 'Must enforce 2-byte word alignment invariant');
});

test('Interactive Specimen: On-Hover Neuro-Ergonomic Inspector HUD Invariants', () => {
  const indexPath = path.join(ROOT_DIR, 'index.html');
  assert.ok(fs.existsSync(indexPath), 'index.html must exist');
  const indexHtml = fs.readFileSync(indexPath, 'utf8');

  // Verify HUD and Controls in index.html
  assert.ok(indexHtml.includes('id="neuroErgonomicInspectorHud"'), 'index.html must contain #neuroErgonomicInspectorHud');
  assert.ok(indexHtml.includes('id="hudVectorSvg"'), 'index.html must contain SVG vector viewport');
  assert.ok(indexHtml.includes('id="hudDynamicVectors"'), 'index.html must contain #hudDynamicVectors');
  assert.ok(indexHtml.includes('id="toggleInspectorModeBtn"'), 'index.html must contain inspector toggle button');
  assert.ok(indexHtml.includes('initNeuroErgonomicInspector'), 'index.html must initialize inspector controller');

  // Verify data-inspect attributes on cards
  assert.ok(indexHtml.includes('data-inspect="b_vs_d"'), 'Must have data-inspect="b_vs_d"');
  assert.ok(indexHtml.includes('data-inspect="slashed_zero"'), 'Must have data-inspect="slashed_zero"');
  assert.ok(indexHtml.includes('data-inspect="philocardia_hearts"'), 'Must have data-inspect="philocardia_hearts"');

  // Verify link to consensus standard
  assert.ok(indexHtml.includes('standards/FDA_ISMP_CLINICAL_DIGITAL_TYPOGRAPHY_SPECIFICATION.md'), 'Must link to FDA/ISMP standard');
});

