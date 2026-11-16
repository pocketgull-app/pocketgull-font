#!/usr/bin/env node
/**
 * scripts/build-prosody-dataset.mjs
 * ==================================
 * Synthesizes a clean, zero-PHI Hugging Face supervised fine-tuning (SFT) dataset
 * for `google/gemma-3-1b-it` mapping screenplay dialogue / closed-caption beats to
 * PocketGull-VF 10-axis emotional prosody JSON keyframes.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  BROADCAST_SCENES,
  NARRATIVE_ARC_GENRES,
  NarrativeArcGenerator,
  SCREENPLAY_SAMPLE_PRESETS,
  EMOTION_TOKENS,
  parseScreenplayScript,
  inferCueAffect
} from '../js/closed_caption_studio.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const OUT_DIR = path.join(ROOT_DIR, 'distribution', 'huggingface', 'pocketgull-prosody-gemma', 'data');

const SYSTEM_PROMPT =
  'You are PocketGull Prosody Gemma, an assistive screenplay & closed-caption keyframer. ' +
  'Given {speaker, direction, text}, output ONLY valid JSON with key "beats": an array of ' +
  '{index, emotion, weight, slant, soft, hlng, boum, aptr, tension, bpm}. ' +
  'emotion in ["intimate","panic","relief","awe","dialogue","soundfx"]; ' +
  'weight 100..900, slant -10.5..0, soft/hlng/boum/aptr 0.0..1.0, tension 5..100, bpm 54..175.';

const CRAFTED_SCREENPLAY_BEATS = [
  // Counterfactual pairs teaching Gemma subtle vocal subtext vs. surface words
  { speaker: 'ELENA', direction: 'whispers, hand steady', text: 'Do not look at the door. Walk slowly toward the stairwell.', affect: 'intimate' },
  { speaker: 'ELENA', direction: 'screaming over siren', text: 'DO NOT OPEN THAT DOOR! GET TO THE STAIRWELL NOW!', affect: 'panic' },
  { speaker: 'ELENA', direction: 'exhaling softly, relieved', text: 'The lock held. You can step away from the stairwell now.', affect: 'relief' },
  { speaker: 'ELENA', direction: 'staring out the glass in awe', text: 'Look at how the stairwell opens straight onto the glacier field.', affect: 'awe' },

  { speaker: 'DOCTOR', direction: 'quiet confession', text: 'I missed the 02:14 dosage decimal on my first rotation.', affect: 'intimate' },
  { speaker: 'DOCTOR', direction: 'urgent stat call', text: 'HOLD THE 5.0 MG BOLUS! RECHECK LABEL CONCENTRATION NOW!', affect: 'panic' },
  { speaker: 'DOCTOR', direction: 'gentle bedside tone, relieved', text: 'Your labs are clear. Everything is settling nicely tonight.', affect: 'relief' },
  { speaker: 'DOCTOR', direction: 'quiet wonder', text: 'Forty years of rain, and I have never seen a dawn sky burn that violet.', affect: 'awe' },

  { speaker: 'PILOT', direction: 'tight, holding breath', text: 'Hydraulic pressure dropping fast! Manual trim offline!', affect: 'panic' },
  { speaker: 'PILOT', direction: 'low, close to mic', text: 'If telemetry drops below horizon, tell my sister the logbook is in locker four.', affect: 'intimate' },
  { speaker: 'PILOT', direction: 'relieved chuckle', text: 'Reserve bus is online. Altitude stabilized at twelve thousand feet.', affect: 'relief' },
  { speaker: 'PILOT', direction: 'breathless wonder', text: 'Look at the ring shadows sliding across the upper cloud deck.', affect: 'awe' },

  { speaker: 'NARRATOR (V.O.)', direction: 'intimate reflection', text: 'No one writes down what the harbor sounded like after the boats left.', affect: 'intimate' },
  { speaker: 'DISPATCH', direction: 'alarming', text: 'EVACUATE LOWER BERTH IMMEDIATELY! SURGE INBOUND!', affect: 'panic' },
  { speaker: 'PARAMEDIC', direction: 'warm, calming', text: 'Match your breathing to my voice. Four seconds in, calm and steady.', affect: 'relief' },
  { speaker: 'CHRONICLER', direction: 'reverent', text: 'Cedar smoke rose straight through the pine canopy toward a thousand winter stars.', affect: 'awe' },
  { speaker: 'TECH', direction: 'matter-of-fact', text: 'Please confirm your badge number at the east corridor terminal.', affect: 'dialogue' },
  { speaker: 'OPERATOR', direction: 'neutral check', text: 'Archive reel twelve starts at timecode zero zero fourteen.', affect: 'dialogue' },
  { speaker: 'CLERK', direction: 'conversational', text: 'We moved the ledger index to the second shelf before lunch.', affect: 'dialogue' },
  { speaker: 'AMBIENCE', direction: 'foley cue', text: '[♪ brass pendulum ticks slower inside an empty clocktower ♪]', affect: 'soundfx' }
];

function buildStructuredExample(cues) {
  const inputBeats = cues.map((c, index) => ({
    index,
    speaker: c.speaker,
    direction: c.parenthetical || c.beatName || c.prosody || '',
    text: c.text
  }));
  const targetBeats = cues.map((c, index) => ({
    index,
    emotion: c.emotion || inferCueAffect(c.text, c.parenthetical || '', c.speaker).emotion,
    weight: Math.max(100, Math.min(900, Math.round(Number(c.weight || 400)))),
    slant: Number(Math.max(-10.5, Math.min(0, Number(c.slant || 0))).toFixed(1)),
    soft: Number(Math.max(0, Math.min(1, Number(c.soft !== undefined ? c.soft : 0.25))).toFixed(2)),
    hlng: Number(Math.max(0, Math.min(1, Number(c.hlng !== undefined ? c.hlng : 0.20))).toFixed(2)),
    boum: Number(Math.max(0, Math.min(1, Number(c.boum !== undefined ? c.boum : 0.15))).toFixed(2)),
    aptr: Number(Math.max(0, Math.min(1, Number(c.aptr > 1 ? c.aptr / 100 : (c.aptr !== undefined ? c.aptr : 0.55)))).toFixed(2)),
    tension: Math.max(5, Math.min(100, Math.round(Number(c.tension || 35)))),
    bpm: Math.max(48, Math.min(185, Math.round(Number(c.bpm || 72))))
  }));

  return {
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: JSON.stringify({ beats: inputBeats }) },
      { role: 'assistant', content: JSON.stringify({ beats: targetBeats }) }
    ]
  };
}

export function generateDatasetRecords() {
  const records = [];

  // 1. All 5 Broadcast Scenes (enriched via inferCueAffect)
  for (const scene of Object.values(BROADCAST_SCENES)) {
    const enriched = scene.cues.map((c) => {
      const aff = inferCueAffect(c.text, c.prosody, c.speaker);
      return { ...aff, ...c, aptr: c.aptr > 1 ? Number((c.aptr / 100).toFixed(2)) : aff.aptr };
    });
    records.push(buildStructuredExample(enriched));
    for (const beat of enriched) {
      records.push(buildStructuredExample([beat]));
    }
  }

  // 2. All 5 Phanvas Genres across 4 seeds (multi-beat scene + sliding pairs)
  const seeds = ['the harbor ledger', 'Relay Station 09', 'Cedar Creek Bridge', 'Ward C Telemetry'];
  for (const genreId of Object.keys(NARRATIVE_ARC_GENRES)) {
    for (const seed of seeds) {
      const arc = NarrativeArcGenerator.generateArc(genreId, seed);
      const enriched = arc.cues.map((c) => ({
        ...inferCueAffect(c.text, c.beatName || c.prosody, c.speaker),
        ...c
      }));
      records.push(buildStructuredExample(enriched));
      for (let i = 0; i < enriched.length - 1; i++) {
        records.push(buildStructuredExample([enriched[i], enriched[i + 1]]));
      }
    }
  }

  // 3. Built-in Fountain Screenplay Sample Presets
  for (const preset of Object.values(SCREENPLAY_SAMPLE_PRESETS)) {
    const parsed = parseScreenplayScript(preset.script);
    records.push(buildStructuredExample(parsed.cues));
    for (const cue of parsed.cues) {
      records.push(buildStructuredExample([cue]));
    }
  }

  // 4. Counterfactual Screenplay Subtext Contrast Pairs
  const craftedCues = CRAFTED_SCREENPLAY_BEATS.map((item) => {
    const tok = EMOTION_TOKENS[item.affect];
    const base = tok
      ? {
          emotion: item.affect,
          weight: tok.weight,
          slant: tok.slant,
          soft: tok.soft,
          hlng: tok.hlng,
          boum: tok.boum,
          aptr: tok.aptr,
          tension: item.affect === 'panic' ? 92 : item.affect === 'intimate' ? 45 : item.affect === 'awe' ? 38 : 20,
          bpm: item.affect === 'panic' ? 160 : item.affect === 'intimate' ? 66 : item.affect === 'awe' ? 64 : 62
        }
      : inferCueAffect(item.text, item.direction, item.speaker);
    return {
      speaker: item.speaker,
      parenthetical: item.direction,
      text: item.text,
      ...base
    };
  });

  // Group into 4-beat counterfactual contrast scenes AND individual lines
  for (let i = 0; i < craftedCues.length; i += 4) {
    records.push(buildStructuredExample(craftedCues.slice(i, i + 4)));
  }
  for (const c of craftedCues) {
    records.push(buildStructuredExample([c]));
  }

  // Deterministic 85/15 train/eval split
  const train = [];
  const evalSet = [];
  records.forEach((rec, idx) => {
    if (idx % 7 === 0) evalSet.push(rec);
    else train.push(rec);
  });

  return { train, evalSet, total: records.length };
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const { train, evalSet, total } = generateDatasetRecords();

  const trainPath = path.join(OUT_DIR, 'train.jsonl');
  const evalPath = path.join(OUT_DIR, 'eval.jsonl');
  const manifestPath = path.join(OUT_DIR, 'dataset_manifest.json');

  fs.writeFileSync(trainPath, train.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf8');
  fs.writeFileSync(evalPath, evalSet.map(r => JSON.stringify(r)).join('\n') + '\n', 'utf8');

  const manifest = {
    name: 'pocketgull-prosody-gemma-dataset',
    baseModel: 'google/gemma-3-1b-it',
    ollamaBaseModel: 'gemma3:1b',
    version: '4.0.0',
    totalExamples: total,
    trainCount: train.length,
    evalCount: evalSet.length,
    axesSchema: ['emotion', 'weight', 'slant', 'soft', 'hlng', 'boum', 'aptr', 'tension', 'bpm'],
    negativeSpaceCompliance: 'Zero PHI; non-diagnostic assistive screenplay & caption keyframing only.'
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');

  console.log(`Generated ${train.length} train + ${evalSet.length} eval records (${total} total) in ${OUT_DIR}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  main();
}
