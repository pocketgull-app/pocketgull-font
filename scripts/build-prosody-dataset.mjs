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
  NAMED_VF_VARIATIONS,
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
  '{index, emotion, instance, weight, width, slant, soft, hlng, boum, aptr, grav, chis, tension, bpm}. ' +
  'emotion in ["intimate","panic","relief","awe","dialogue","soundfx"]; ' +
  'instance in ["soft_light","soft_regular","soft_bold","soft_black","healing_calm","recovery_72bpm","chiseltip_45","dyslexia_gravity","default"]; ' +
  'weight 100..900, width 75..100, slant -10.5..0, soft/hlng/boum/aptr/grav 0.0..1.0, chis 0..45, tension 5..100, bpm 54..175.';

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
  { speaker: 'TECH', direction: 'matter-of-fact', text: 'Please confirm your badge number at the east corridor terminal.', affect: 'dialogue', instance: 'default' },
  { speaker: 'OPERATOR', direction: 'neutral check', text: 'Archive reel twelve starts at timecode zero zero fourteen.', affect: 'dialogue', instance: 'default' },
  { speaker: 'CLERK', direction: 'conversational', text: 'We moved the ledger index to the second shelf before lunch.', affect: 'dialogue', instance: 'default' },
  { speaker: 'AMBIENCE', direction: 'foley cue', text: '[♪ brass pendulum ticks slower inside an empty clocktower ♪]', affect: 'soundfx', instance: 'default' },

  // Dedicated Soft & Companion Named Variation contrast beats
  { speaker: 'MOTHER', direction: 'tender, vulnerable softness', text: 'Stay close until the fever breaks; I am right beside your pillow.', affect: 'intimate', instance: 'soft_light' },
  { speaker: 'NURSE', direction: 'gentle soothing bedtime check', text: 'Warm blankets are ready, and the hallway lights are dimmed for sleep.', affect: 'relief', instance: 'soft_regular' },
  { speaker: 'PEDIATRICIAN', direction: 'pediatric comfort, warm reassurance', text: 'You were brave today. One small sip of water and we are all done.', affect: 'relief', instance: 'soft_bold' },
  { speaker: 'HOST', direction: 'friendly rounded marquee warmth', text: 'WELCOME BACK TO HARBOR FESTIVAL RADIO NIGHT!', affect: 'relief', instance: 'soft_black' },
  { speaker: 'TITLE CARD', direction: 'chiseled placard epigraph', text: 'CHAPTER IV · THE WINTER WATCH AT POINT NO POINT', affect: 'panic', instance: 'chiseltip_45' },
  { speaker: 'DISPATCH', direction: 'dyslexia ground clarity', text: 'Confirm 15 mg dose vs 50 mg tablet; keep every baseline glyph distinct.', affect: 'dialogue', instance: 'dyslexia_gravity' }
];

function buildStructuredExample(cues) {
  const inputBeats = cues.map((c, index) => ({
    index,
    speaker: c.speaker,
    direction: c.parenthetical || c.beatName || c.prosody || '',
    text: c.text
  }));
  const targetBeats = cues.map((c, index) => {
    const inferred = inferCueAffect(c.text, c.parenthetical || '', c.speaker);
    return {
      index,
      emotion: c.emotion || inferred.emotion,
      instance: c.instance || inferred.instance || 'default',
      weight: Math.max(100, Math.min(900, Math.round(Number(c.weight || inferred.weight || 400)))),
      width: Math.max(75, Math.min(100, Math.round(Number(c.width || inferred.width || 100)))),
      slant: Number(Math.max(-10.5, Math.min(0, Number(c.slant !== undefined ? c.slant : inferred.slant))).toFixed(1)),
      soft: Number(Math.max(0, Math.min(1, Number(c.soft !== undefined ? c.soft : inferred.soft))).toFixed(2)),
      hlng: Number(Math.max(0, Math.min(1, Number(c.hlng !== undefined ? c.hlng : inferred.hlng))).toFixed(2)),
      boum: Number(Math.max(0, Math.min(1, Number(c.boum !== undefined ? c.boum : inferred.boum))).toFixed(2)),
      aptr: Number(Math.max(0, Math.min(1, Number(c.aptr > 1 ? c.aptr / 100 : (c.aptr !== undefined ? c.aptr : inferred.aptr)))).toFixed(2)),
      grav: Number(Math.max(0, Math.min(1, Number(c.grav !== undefined ? c.grav : inferred.grav))).toFixed(2)),
      chis: Math.max(0, Math.min(45, Math.round(Number(c.chis !== undefined ? c.chis : (inferred.chis || 0))))),
      tension: Math.max(5, Math.min(100, Math.round(Number(c.tension || inferred.tension || 35)))),
      bpm: Math.max(48, Math.min(185, Math.round(Number(c.bpm || inferred.bpm || 72))))
    };
  });

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

  // 4. Counterfactual Screenplay Subtext + Named Variation Contrast Pairs
  const craftedCues = CRAFTED_SCREENPLAY_BEATS.map((item) => {
    const inst = item.instance && NAMED_VF_VARIATIONS[item.instance] ? NAMED_VF_VARIATIONS[item.instance] : null;
    const tok = EMOTION_TOKENS[item.affect];
    const base = inst
      ? {
          emotion: item.affect,
          instance: inst.id,
          weight: inst.weight,
          width: inst.width,
          slant: inst.slant,
          soft: inst.soft,
          hlng: inst.hlng,
          boum: inst.boum,
          aptr: inst.aptr,
          grav: inst.grav,
          chis: inst.chis,
          tension: inst.id === 'chiseltip_45' ? 86 : item.affect === 'panic' ? 92 : 24,
          bpm: inst.id === 'chiseltip_45' ? 122 : item.affect === 'panic' ? 160 : 66
        }
      : tok
      ? {
          emotion: item.affect,
          instance: 'default',
          weight: tok.weight,
          width: tok.width,
          slant: tok.slant,
          soft: tok.soft,
          hlng: tok.hlng,
          boum: tok.boum,
          aptr: tok.aptr,
          grav: tok.grav,
          chis: 0,
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

  // 5. Named VF Instance Anchors (Soft Light..Black, Healing Calm, Chiseltip, Gravity)
  for (const nv of Object.values(NAMED_VF_VARIATIONS)) {
    const emo = nv.id.startsWith('soft_light') ? 'intimate'
      : nv.id === 'chiseltip_45' ? 'panic'
      : (nv.id === 'healing_calm' || nv.id === 'recovery_72bpm' || nv.id.startsWith('soft')) ? 'relief'
      : 'dialogue';
    records.push(buildStructuredExample([{
      speaker: 'VOICE',
      parenthetical: nv.name.toLowerCase(),
      text: `Expressive tone anchored in ${nv.name} with balanced optotype clarity.`,
      emotion: emo,
      instance: nv.id,
      weight: nv.weight,
      width: nv.width,
      slant: nv.slant,
      soft: nv.soft,
      hlng: nv.hlng,
      boum: nv.boum,
      aptr: nv.aptr,
      grav: nv.grav,
      chis: nv.chis,
      tension: emo === 'panic' ? 84 : 26,
      bpm: emo === 'panic' ? 124 : 68
    }]));
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
    axesSchema: ['emotion', 'instance', 'weight', 'width', 'slant', 'soft', 'hlng', 'boum', 'aptr', 'grav', 'chis', 'tension', 'bpm'],
    negativeSpaceCompliance: 'Zero PHI; non-diagnostic assistive screenplay & caption keyframing only.'
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + '\n', 'utf8');

  console.log(`Generated ${train.length} train + ${evalSet.length} eval records (${total} total) in ${OUT_DIR}`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  main();
}
