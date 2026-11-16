/**
 * PocketGull Closed Caption & Broadcast Teletext Engine
 * =====================================================
 * Real-time variable font captioning, CEA-708 & WebVTT delivery simulation,
 * auditory prosody weight-mapping, and optometric A/B benchmarking.
 *
 * Licensed under SIL Open Font License 1.1
 */

export const BROADCAST_SCENES = {
  trauma_bay: {
    id: 'trauma_bay',
    title: '🏥 Trauma Resuscitation (Code Blue)',
    badge: 'CLINICAL TELEMETRY',
    description: 'High-stress resuscitation with rapid drug orders, fluctuating vitals, and ISMP dosage disambiguation.',
    sceneClass: 'cc-scene-trauma',
    cues: [
      {
        speaker: 'DR. ARIS',
        text: 'Patient in severe ventricular tachycardia. Pulse is thready.',
        prosody: 'dialogue',
        weight: 400,
        width: 100,
        slant: 0
      },
      {
        speaker: 'MONITOR',
        text: '[♪ critical telemetry alarm: 178 BPM chime ♪]',
        prosody: 'soundfx',
        weight: 500,
        width: 100,
        slant: 0,
        icon: '🔔'
      },
      {
        speaker: 'DR. ARIS',
        text: 'Administer Adenosine 6.0 mg rapid IV push immediately!',
        prosody: 'urgent',
        weight: 700,
        width: 94,
        slant: 0
      },
      {
        speaker: 'NURSE CHEN',
        text: 'Adenosine 6.0 mg delivered. Flushed with 20 mL saline.',
        prosody: 'dialogue',
        weight: 420,
        width: 100,
        slant: 0
      },
      {
        speaker: 'DR. ARIS',
        text: 'Rhythm converting. Sinus rhythm restored at 74 BPM.',
        prosody: 'whisper',
        weight: 300,
        width: 100,
        slant: -4
      }
    ]
  },

  blizzard_glare: {
    id: 'blizzard_glare',
    title: '❄️ Arctic Blizzard (High-Key Glare)',
    badge: 'HIGH-LUMINANCE APERTURE',
    description: 'Whiteout snowstorm background testing optical counter apertures (APTR) and anti-blooming legibility.',
    sceneClass: 'cc-scene-blizzard',
    cues: [
      {
        speaker: 'METEOROLOGIST',
        text: 'Extreme blizzard warning in effect across the Hudson Bay region.',
        prosody: 'dialogue',
        weight: 400,
        width: 100,
        slant: 0
      },
      {
        speaker: 'ENVIRONMENT',
        text: '[💨 howling gale force winds: 95 km/h sustained 💨]',
        prosody: 'soundfx',
        weight: 500,
        width: 100,
        slant: 0,
        icon: '❄️'
      },
      {
        speaker: 'METEOROLOGIST',
        text: 'Zero visibility reported. Optical apertures expanded.',
        prosody: 'urgent',
        weight: 650,
        width: 92,
        slant: 0
      },
      {
        speaker: 'CIVIL NOTICE',
        text: 'SHELTER IN PLACE UNTIL 08:00 AM TOMORROW.',
        prosody: 'shout',
        weight: 880,
        width: 86,
        slant: 0
      }
    ]
  },

  midnight_noir: {
    id: 'midnight_noir',
    title: '🎬 Midnight Noir (Low-Key Cinema)',
    badge: 'SCOTOPIC 650nm CINE',
    description: 'Intimate dramatic sequence with whispered dialogue, scotopic ambient lighting, and non-speech sound cues.',
    sceneClass: 'cc-scene-noir',
    cues: [
      {
        speaker: 'NARRATOR (V.O.)',
        text: 'The docks were silent, holding their breath before the dawn.',
        prosody: 'narrator',
        weight: 350,
        width: 100,
        slant: -8
      },
      {
        speaker: 'AMBIENCE',
        text: '[🌧️ steady midnight rain pattering against glass 🌧️]',
        prosody: 'soundfx',
        weight: 320,
        width: 100,
        slant: 0,
        icon: '🌧️'
      },
      {
        speaker: 'DETECTIVE REED',
        text: 'Did anyone notice the missing case ledger?',
        prosody: 'whisper',
        weight: 240,
        width: 100,
        slant: -6
      },
      {
        speaker: 'ELENA',
        text: 'He took it before midnight. He knew we were coming.',
        prosody: 'dialogue',
        weight: 400,
        width: 100,
        slant: 0
      }
    ]
  },

  eas_alert: {
    id: 'eas_alert',
    title: '⚡ Emergency Alert System (Civil Broadcast)',
    badge: 'EAS / SL Sloan 5:1',
    description: 'Federal civil emergency broadcast with high-decibel alert headers, roll-up ticker, and rapid acquisition.',
    sceneClass: 'cc-scene-eas',
    cues: [
      {
        speaker: 'CIVIL DEFENSE',
        text: 'THE NATIONAL WEATHER SERVICE HAS ISSUED A TORNADO WARNING.',
        prosody: 'urgent',
        weight: 750,
        width: 90,
        slant: 0
      },
      {
        speaker: 'SIREN',
        text: '[⚡ continuous two-tone 853 Hz & 960 Hz alert tone ⚡]',
        prosody: 'soundfx',
        weight: 820,
        width: 95,
        slant: 0,
        icon: '⚡'
      },
      {
        speaker: 'INSTRUCTION',
        text: 'TAKE SHELTER IMMEDIATELY IN AN INTERIOR ROOM OR BASEMENT.',
        prosody: 'shout',
        weight: 900,
        width: 84,
        slant: 0
      },
      {
        speaker: 'LOCATIONS',
        text: 'COUNTIES: KING, PIERCE, SNOHOMISH. MOVE INWARD NOW.',
        prosody: 'dialogue',
        weight: 500,
        width: 100,
        slant: 0
      }
    ]
  },

  sovereign_aptn: {
    id: 'sovereign_aptn',
    title: '🌐 Indigenous Broadcast (APTN Inuktitut & Syllabics)',
    badge: 'UNDRIP SOVEREIGN TRACK',
    description: 'Sovereign Northern broadcast (APTN) with Canadian Aboriginal Syllabics and Chinuk Pipa stenography.',
    sceneClass: 'cc-scene-aptn',
    cues: [
      {
        speaker: 'APTN NEWS',
        text: 'ᑐᓴᒐᒃᓴᑦ: ᐃᓄᒃᑎᑐᑦ ᑐᓴᒐᒃᓴᓕᕆᓂᖅ ᐅᓪᓗᒥ.',
        prosody: 'dialogue',
        weight: 400,
        width: 100,
        slant: 0
      },
      {
        speaker: 'TRANSLATION',
        text: '[Inuktitut Broadcast: Arctic Healthcare & Community Telemetry]',
        prosody: 'narrator',
        weight: 360,
        width: 100,
        slant: -6
      },
      {
        speaker: 'CHINUK PIPA',
        text: 'Chinuk Pipa Shorthand: ɬush wawa kopa munk-kʰanawi tilixam.',
        prosody: 'dialogue',
        weight: 450,
        width: 96,
        slant: 0
      },
      {
        speaker: 'HEALING',
        text: 'ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ: ᑕᒪᕐᒥᒃ ᓄᓇᓖᑦ ᐱᔨᑦᑎᕋᖅᑕᐅᔪᑦ.',
        prosody: 'urgent',
        weight: 700,
        width: 100,
        slant: 0
      }
    ]
  }
};

export function normalizeAptr(value, fallback = 0.5) {
  const num = Number(value);
  if (!Number.isFinite(num)) return fallback;
  const scaled = num > 1 ? num / 100 : num;
  return Number(Math.max(0, Math.min(1, scaled)).toFixed(2));
}

export function buildVariationString(axes = {}) {
  const w = Number.isFinite(Number(axes.weight)) ? Number(axes.weight) : 400;
  const wd = Number.isFinite(Number(axes.width)) ? Number(axes.width) : 100;
  const sl = Number.isFinite(Number(axes.slant)) ? Number(axes.slant) : 0;
  const opsz = Math.max(6, Math.min(72, Number.isFinite(Number(axes.opsz)) ? Number(axes.opsz) : 20));
  const aptr = normalizeAptr(axes.aptr !== undefined ? axes.aptr : 0.5);
  const clamp01 = (v, def = 0) => {
    const n = Number(v);
    return Number.isFinite(n) ? Number(Math.max(0, Math.min(1, n)).toFixed(2)) : def;
  };
  const soft = clamp01(axes.soft, 0.25);
  const hlng = clamp01(axes.hlng, 0.2);
  const boum = clamp01(axes.boum, 0.1);
  const thrm = clamp01(axes.thrm, 0);
  const grav = clamp01(axes.grav, 0.1);
  return `'wght' ${w}, 'wdth' ${wd}, 'slnt' ${sl}, 'opsz' ${opsz}, 'APTR' ${aptr}, 'SOFT' ${soft}, 'HLNG' ${hlng}, 'BOUM' ${boum}, 'THRM' ${thrm}, 'GRAV' ${grav}`;
}

export const PROSODY_PRESETS = {
  whisper: { weight: 240, slant: -7, aptr: 0.35, soft: 0.8, hlng: 0.6, boum: 0.3, thrm: 0, grav: 0.1, opsz: 18, letterSpacing: '0.04em', label: 'Whisper / Quiet (240)' },
  dialogue: { weight: 400, slant: 0, aptr: 0.55, soft: 0.25, hlng: 0.2, boum: 0.1, thrm: 0, grav: 0.1, opsz: 20, letterSpacing: '0em', label: 'Conversational (400)' },
  narrator: { weight: 360, slant: -8, aptr: 0.5, soft: 0.4, hlng: 0.45, boum: 0.2, thrm: 0, grav: 0.1, opsz: 22, letterSpacing: '0.02em', label: 'Voiceover (360)' },
  urgent: { weight: 700, slant: 0, aptr: 0.9, soft: 0, hlng: 0, boum: 0, thrm: 0.35, grav: 0.2, opsz: 36, letterSpacing: '-0.01em', label: 'Urgent Alert (700)' },
  shout: { weight: 900, slant: 0, aptr: 1.0, soft: 0, hlng: 0, boum: 0, thrm: 0.65, grav: 0.3, opsz: 48, letterSpacing: '-0.02em', label: 'Shout / Siren (900)' },
  soundfx: { weight: 500, slant: 0, aptr: 0.65, soft: 0.35, hlng: 0.3, boum: 0.25, thrm: 0, grav: 0.1, opsz: 24, letterSpacing: '0.02em', label: 'Non-Speech FX (500)' }
};

export const EMOTION_TOKENS = {
  intimate: {
    id: 'intimate',
    name: 'Intimate / Whisper',
    weight: 240,
    width: 98,
    slant: -6.5,
    opsz: 18,
    tracking: '0.04em',
    aptr: 0.35,
    soft: 0.85,
    hlng: 0.70,
    boum: 0.45,
    thrm: 0.0,
    grav: 0.15,
    scrimHue: '210, 30%, 10%',
    scrimAlpha: 0.78,
    aura: '0 0 16px rgba(56, 189, 248, 0.15)',
    pacingMs: 3800,
    sampleText: 'I never wanted anyone else to know about this.'
  },
  panic: {
    id: 'panic',
    name: 'Trauma / Acute Panic',
    weight: 850,
    width: 86,
    slant: 0,
    opsz: 48,
    tracking: '-0.015em',
    aptr: 1.00,
    soft: 0.00,
    hlng: 0.00,
    boum: 0.00,
    thrm: 0.65,
    grav: 0.30,
    scrimHue: '0, 45%, 8%',
    scrimAlpha: 0.88,
    aura: '0 0 20px rgba(239, 68, 68, 0.35)',
    pacingMs: 2200,
    sampleText: 'DEFIBRILLATOR CHARGED TO 200 JOULES! ALL CLEAR!'
  },
  relief: {
    id: 'relief',
    name: 'Vagal Relief / Grounding',
    weight: 410,
    width: 100,
    slant: 0,
    opsz: 24,
    tracking: '0.02em',
    aptr: 0.70,
    soft: 0.90,
    hlng: 1.00,
    boum: 0.60,
    thrm: 0.00,
    grav: 0.40,
    scrimHue: '160, 30%, 8%',
    scrimAlpha: 0.80,
    aura: '0 0 16px rgba(16, 185, 129, 0.2)',
    pacingMs: 4200,
    sampleText: 'The pulse has stabilized. Normal sinus rhythm restored.'
  },
  awe: {
    id: 'awe',
    name: 'Cosmic Awe / Reverence',
    weight: 280,
    width: 100,
    slant: 0,
    opsz: 56,
    tracking: '0.08em',
    aptr: 0.85,
    soft: 0.45,
    hlng: 0.85,
    boum: 0.90,
    thrm: 0.00,
    grav: 0.00,
    scrimHue: '260, 35%, 8%',
    scrimAlpha: 0.75,
    aura: '0 0 24px rgba(168, 85, 247, 0.28)',
    pacingMs: 4600,
    sampleText: 'Beyond the horizon, the northern lights began to sing.'
  }
};

export const ATMOSPHERIC_BLENDS = {
  clinical_teal: {
    id: 'clinical_teal',
    name: 'Hospital Surgical Teal',
    scrimBg: 'rgba(4, 20, 28, 0.85)',
    scrimBorder: 'rgba(6, 182, 212, 0.28)',
    textTint: '#f0fdfa',
    aura: '0 4px 20px rgba(6, 182, 212, 0.18)'
  },
  noir_shadow: {
    id: 'noir_shadow',
    name: 'Midnight Noir Shadow',
    scrimBg: 'rgba(5, 7, 14, 0.88)',
    scrimBorder: 'rgba(255, 255, 255, 0.1)',
    textTint: '#f8fafc',
    aura: '0 4px 18px rgba(0, 0, 0, 0.7)'
  },
  hearth_amber: {
    id: 'hearth_amber',
    name: 'Warm Hearth Candlelight',
    scrimBg: 'rgba(24, 14, 6, 0.86)',
    scrimBorder: 'rgba(245, 158, 11, 0.32)',
    textTint: '#fffbeb',
    aura: '0 4px 22px rgba(245, 158, 11, 0.22)'
  },
  arctic_frost: {
    id: 'arctic_frost',
    name: 'Arctic Frost Diffusion',
    scrimBg: 'rgba(215, 230, 245, 0.88)',
    scrimBorder: 'rgba(147, 197, 253, 0.65)',
    textTint: '#032541',
    aura: '0 4px 18px rgba(147, 197, 253, 0.35)'
  }
};

export const SPATIAL_DIRECTIONS = {
  left: {
    id: 'left',
    name: 'Off-Screen Left',
    slant: -5.5,
    align: 'left',
    label: '◄ Left Speaker'
  },
  center: {
    id: 'center',
    name: 'On-Screen Center',
    slant: 0,
    align: 'center',
    label: '▲ Center Dialogue'
  },
  right: {
    id: 'right',
    name: 'Off-Screen Right',
    slant: -1.5,
    align: 'right',
    label: 'Right Speaker ►'
  }
};

export class ClosedCaptionStudio {
  constructor(options = {}) {
    this.currentSceneId = options.sceneId || 'trauma_bay';
    this.currentCueIndex = 0;
    this.isPlaying = false;
    this.playbackTimer = null;
    this.speedMultiplier = 1.0;
    this.mode = 'pop-on'; // 'pop-on' | 'roll-up' | 'paint-on'
    this.scrimMode = 'translucent'; // 'solid' | 'translucent' | 'minimal' | 'clear'
    this.filterMode = 'none'; // 'none' | 'blur' | 'distance' | 'vibe'
    this.abFont = 'arial'; // 'arial' | 'trebuchet' | 'roboto' | 'courier'

    // Variable Font Overrides
    this.overrideWeight = null;
    this.overrideWidth = null;
    this.overrideSlant = null;
    this.aperture = 50;

    // Roll-up line buffer (for roll-up mode)
    // Roll-up line buffer (for roll-up mode)
    this.rollupBuffer = [];

    // Emotion & Atmospheric Scene Blending
    this.currentEmotion = null;
    this.currentAtmosphericBlend = 'clinical_teal';
    this.currentSpatialDirection = 'center';

    // Philocardia Hearts & Tittle Varieties
    this.philocardiaEnabled = false;
    this.tittleVariety = 'dot';
    this.cardiacPacing = 'philocardia-pacing-72';
    this.cardiacPacingId = 'pace_72';
    this.safeAreaVisible = false;
    this.activeCustomScene = null;
    this.includeDeconstructionNotes = false;
    this.deconstructionStance = 'negotiate';
    this.activeThinkerLens = 'postman';
  }

  setIncludeDeconstructionNotes(enabled) {
    this.includeDeconstructionNotes = Boolean(enabled);
    return this.includeDeconstructionNotes;
  }

  setDeconstructionStance(stance) {
    if (['assent', 'resist', 'negotiate'].includes(stance)) {
      this.deconstructionStance = stance;
    }
    return this.deconstructionStance;
  }

  setThinkerLens(thinkerId) {
    if (PHL197_THINKER_LENSES[thinkerId]) {
      this.activeThinkerLens = thinkerId;
    }
    return PHL197_THINKER_LENSES[this.activeThinkerLens];
  }

  getScene(id) {
    if (this.activeCustomScene && (!id || id === 'narrative_arc')) {
      return this.activeCustomScene;
    }
    const targetId = id || this.currentSceneId;
    return BROADCAST_SCENES[targetId] || BROADCAST_SCENES.trauma_bay;
  }

  setCustomScene(sceneObj) {
    if (sceneObj && Array.isArray(sceneObj.cues) && sceneObj.cues.length > 0) {
      this.activeCustomScene = sceneObj;
      this.currentSceneId = 'narrative_arc';
      this.currentCueIndex = 0;
      this.rollupBuffer = [];
      return this.activeCustomScene;
    }
    return null;
  }

  clearCustomScene() {
    this.activeCustomScene = null;
  }

  getCurrentCue() {
    const scene = this.getScene();
    return scene.cues[this.currentCueIndex] || scene.cues[0];
  }

  nextCue() {
    const scene = this.getScene();
    this.currentCueIndex = (this.currentCueIndex + 1) % scene.cues.length;
    return this.getCurrentCue();
  }

  prevCue() {
    const scene = this.getScene();
    this.currentCueIndex = (this.currentCueIndex - 1 + scene.cues.length) % scene.cues.length;
    return this.getCurrentCue();
  }

  setScene(id) {
    if (BROADCAST_SCENES[id]) {
      this.activeCustomScene = null;
      this.currentSceneId = id;
      this.currentCueIndex = 0;
      this.rollupBuffer = [];
    }
  }

  setSpeed(multiplier) {
    this.speedMultiplier = Math.max(0.5, Math.min(3.0, multiplier));
  }

  setMode(mode) {
    if (['pop-on', 'roll-up', 'paint-on', 'teletext'].includes(mode)) {
      this.mode = mode;
      this.rollupBuffer = [];
    }
  }

  setFilter(filter) {
    this.filterMode = filter;
  }

  setScrim(scrim) {
    this.scrimMode = scrim;
  }

  setAbFont(font) {
    this.abFont = font;
  }

  setEmotion(id) {
    if (EMOTION_TOKENS[id]) {
      this.currentEmotion = id;
      return EMOTION_TOKENS[id];
    }
    this.currentEmotion = null;
    return null;
  }

  setAtmosphericBlend(id) {
    if (ATMOSPHERIC_BLENDS[id]) {
      this.currentAtmosphericBlend = id;
      return ATMOSPHERIC_BLENDS[id];
    }
    return ATMOSPHERIC_BLENDS.clinical_teal;
  }

  setSpatialDirection(id) {
    if (SPATIAL_DIRECTIONS[id]) {
      this.currentSpatialDirection = id;
      return SPATIAL_DIRECTIONS[id];
    }
    return SPATIAL_DIRECTIONS.center;
  }

  setPhilocardia(enabled) {
    this.philocardiaEnabled = Boolean(enabled);
    if (this.philocardiaEnabled && this.tittleVariety === 'dot') {
      this.tittleVariety = 'heart';
    } else if (!this.philocardiaEnabled) {
      this.tittleVariety = 'dot';
    }
    return this.philocardiaEnabled;
  }

  setTittleVariety(variety) {
    if (TITTLE_VARIETIES[variety]) {
      this.tittleVariety = variety;
      this.philocardiaEnabled = (variety !== 'dot');
      return TITTLE_VARIETIES[variety];
    }
    this.tittleVariety = 'dot';
    this.philocardiaEnabled = false;
    return TITTLE_VARIETIES.dot;
  }

  setCardiacPacing(pacingId) {
    if (CARDIAC_PACING_PRESETS[pacingId]) {
      this.cardiacPacingId = pacingId;
      this.cardiacPacing = CARDIAC_PACING_PRESETS[pacingId].cssClass;
      return CARDIAC_PACING_PRESETS[pacingId];
    }
    this.cardiacPacingId = 'pace_72';
    this.cardiacPacing = CARDIAC_PACING_PRESETS.pace_72.cssClass;
    return CARDIAC_PACING_PRESETS.pace_72;
  }

  calculateLineFit(text, targetCpl = 37) {
    // Calculates optical width adjustment (75% to 100%) to fit text within broadcast CPL
    if (!text || text.length <= targetCpl) return 100;
    const ratio = targetCpl / text.length;
    const widthPercent = Math.max(75, Math.min(100, Math.round(ratio * 100)));
    return widthPercent;
  }

  evaluateReadingMetrics(text, baseDurationSec = 3.4) {
    const clean = (text || '').trim();
    const effectiveSec = Math.max(0.5, baseDurationSec / (this.speedMultiplier || 1.0));
    const charCount = clean.length;
    const wordCount = clean ? clean.split(/\s+/).length : 0;
    const cps = Number((charCount / effectiveSec).toFixed(1));
    const wpm = Math.round((wordCount / effectiveSec) * 60);
    const recommendedWidth = this.calculateLineFit(clean, 37);
    const tier = cps <= 17 ? 'optimal' : cps <= 20 ? 'elevated' : 'exceeds';
    return { charCount, wordCount, cps, wpm, recommendedWidth, tier, durationSec: Number(effectiveSec.toFixed(2)) };
  }

  resolveCueCardiacState(manualPacingOverride = false) {
    if (this.currentEmotion === 'panic') {
      return { bpm: 164, morphology: 'vtach', color: '#ef4444', label: 'SYMPATHETIC SURGE · 164 BPM', spo2: 93 };
    }
    if (this.currentEmotion === 'relief') {
      return { bpm: 64, morphology: 'sinus', color: '#10b981', label: 'VAGAL RELIEF · 64 BPM SINUS', spo2: 99 };
    }
    if (!manualPacingOverride && this.activeCustomScene && this.currentSceneId === 'narrative_arc') {
      const cue = this.getCurrentCue();
      if (cue && typeof cue.bpm === 'number') {
        const morph = cue.morphology || (cue.bpm >= 135 ? 'vtach' : cue.bpm >= 100 ? 'adenosine' : 'sinus');
        const color = cue.bpm >= 135 ? '#ef4444' : cue.bpm >= 100 ? '#f59e0b' : '#10b981';
        const spo2 = cue.bpm >= 135 ? 93 : cue.bpm >= 100 ? 96 : 99;
        return {
          bpm: cue.bpm,
          morphology: morph,
          color,
          label: `${(cue.beatName || 'STORY BEAT').toUpperCase()} · ${cue.bpm} BPM`,
          spo2
        };
      }
    }
    if (manualPacingOverride || this.currentSceneId !== 'trauma_bay') {
      if (this.cardiacPacingId === 'stillness') {
        return { bpm: 0, morphology: 'stillness', color: '#64748b', label: 'STILLNESS · STATIC TRACE', spo2: 99 };
      }
      if (this.cardiacPacingId === 'pace_breath') {
        return { bpm: 58, morphology: 'sinus', color: '#38bdf8', label: '4-7-8 BREATH RSA · 58 BPM', spo2: 99 };
      }
      if (this.cardiacPacingId === 'pace_60') {
        return { bpm: 60, morphology: 'sinus', color: '#10b981', label: 'VAGAL COHERENCE · 60 BPM', spo2: 99 };
      }
      if (this.currentSceneId !== 'trauma_bay') {
        return { bpm: 72, morphology: 'sinus', color: '#10b981', label: 'AUTONOMIC SINUS · 72 BPM', spo2: 99 };
      }
    }

    // Cue-reactive physiological progression across Trauma Resuscitation
    if (this.currentCueIndex <= 1) {
      return { bpm: 178, morphology: 'vtach', color: '#ef4444', label: 'VTACH · 178 BPM CRITICAL', spo2: 91 };
    }
    if (this.currentCueIndex <= 3) {
      return { bpm: 108, morphology: 'adenosine', color: '#f59e0b', label: 'ADENOSINE CONVERTING · 108 BPM', spo2: 95 };
    }
    return { bpm: 74, morphology: 'sinus', color: '#10b981', label: 'NORMAL SINUS RESTORED · 74 BPM', spo2: 99 };
  }

  generateWebVtt(customText = '') {
    const scene = this.getScene();
    const lines = [
      'WEBVTT - PocketGull Variable Prosody & ISMP Clinical Broadcast Track',
      `NOTE Scene: ${scene.title} | Protocol: ${this.mode.toUpperCase()} | License: SIL OFL 1.1`,
      '',
      'STYLE',
      '::cue {',
      '  font-family: "PocketGull VF", "PocketGull", sans-serif;',
      '  font-feature-settings: "zero" 1, "cv08" 1, "cv05" 1, "ss02" 1, "cv11" 1;',
      '  font-variant-numeric: slashed-zero;',
      '}',
      '::cue(.whisper) { font-variation-settings: "wght" 240, "slnt" -7, "APTR" 0.35, "SOFT" 0.80, "HLNG" 0.60, "BOUM" 0.30; }',
      '::cue(.urgent)  { font-variation-settings: "wght" 700, "wdth" 94, "APTR" 0.90, "SOFT" 0.00, "HLNG" 0.00, "THRM" 0.35; }',
      '::cue(.shout)   { font-variation-settings: "wght" 900, "wdth" 86, "APTR" 1.00, "SOFT" 0.00, "HLNG" 0.00, "THRM" 0.65; }',
      ''
    ];

    const pad2 = (n) => String(n).padStart(2, '0');
    const formatTs = (sec) => {
      const whole = Math.floor(sec);
      const ms = String(Math.round((sec - whole) * 1000)).padStart(3, '0');
      const m = Math.floor(whole / 60);
      const s = whole % 60;
      return `00:${pad2(m)}:${pad2(s)}.${ms}`;
    };

    const cues = customText && customText.trim().length > 0
      ? [{ speaker: 'CUSTOM', text: customText.trim(), prosody: 'dialogue', weight: 400, width: this.calculateLineFit(customText.trim(), 37), slant: 0 }]
      : scene.cues;

    if (this.includeDeconstructionNotes) {
      const thinker = PHL197_THINKER_LENSES[this.activeThinkerLens] || PHL197_THINKER_LENSES.postman;
      lines.push(`NOTE [PHL-197 DECONSTRUCTION] Lens: ${thinker.name} | Stance: ${this.deconstructionStance.toUpperCase()} | Prompt: "How do I know?"`);
      lines.push('');
    }

    const stepSec = 3.4 / (this.speedMultiplier || 1.0);
    cues.forEach((c, idx) => {
      const t0 = idx * stepSec;
      const t1 = (idx + 1) * stepSec - 0.12;
      const cls = c.prosody && ['whisper', 'urgent', 'shout'].includes(c.prosody) ? `.${c.prosody}` : '';
      if (this.includeDeconstructionNotes) {
        const decon = evaluateDeconstructionLens(c, scene, this.deconstructionStance, this.activeThinkerLens);
        lines.push(`NOTE [PHL-197 Cue ${idx + 1}] Frame=${decon.framingMode} | How do I know? ${decon.howDoIKnow}`);
      }
      lines.push(`${idx + 1}`);
      lines.push(`${formatTs(t0)} --> ${formatTs(Math.max(t0 + 0.5, t1))} line:85% align:${this.currentSpatialDirection}`);
      lines.push(`<v${cls} ${c.speaker}>${c.text}</v>`);
      lines.push('');
    });

    return lines.join('\n');
  }
}

export const TELETEXT_SPEAKER_PALETTE = {
  primary: '#fde047',   // WST Yellow (Lead Speaker)
  secondary: '#22d3ee', // WST Cyan (Second Speaker)
  soundfx: '#4ade80',   // WST Green (Non-Speech Audio / Environment)
  alert: '#ffffff'      // WST White-on-Red (Emergency Civil / Code Blue)
};

export function getTeletextSpeakerStyle(speaker, prosody, index = 0) {
  if (prosody === 'soundfx') {
    return { fg: TELETEXT_SPEAKER_PALETTE.soundfx, bg: '#000000', tag: 'SFX' };
  }
  if (prosody === 'shout') {
    return { fg: TELETEXT_SPEAKER_PALETTE.alert, bg: '#b91c1c', tag: 'ALT' };
  }
  const hash = (speaker || '').split('').reduce((acc, ch) => acc + ch.charCodeAt(0), index);
  const fg = hash % 2 === 0 ? TELETEXT_SPEAKER_PALETTE.primary : TELETEXT_SPEAKER_PALETTE.secondary;
  return { fg, bg: '#000000', tag: 'CC1' };
}

export const TITTLE_VARIETIES = {
  heart: { id: 'heart', name: 'Philocardia Heart', glyph: '♥', desc: 'Optical S1/S2 heart tittle with cardiac pacing' },
  blossom: { id: 'blossom', name: 'Regenerative Blossom', glyph: '✤', desc: 'Fireweed 4-petal botanical rebirth' },
  star: { id: 'star', name: 'Celestial Star', glyph: '✦', desc: '4-point astrometric diamond star' },
  droplet: { id: 'droplet', name: 'Somatic Droplet', glyph: '💧', desc: 'Tranquil fluid teardrop' },
  nuqta: { id: 'nuqta', name: 'Calligraphic Nuqṭa', glyph: '◆', desc: 'Authentic 45° reed-pen diamond' },
  dot: { id: 'dot', name: 'Louise Sloan Dot', glyph: '●', desc: 'Standard circular optotype dot' }
};

export const CARDIAC_PACING_PRESETS = {
  pace_72: { id: 'pace_72', name: '72 BPM Resting Pulse', cssClass: 'philocardia-pacing-72', bpm: 72 },
  pace_60: { id: 'pace_60', name: '60 BPM Vagal Coherence', cssClass: 'philocardia-pacing-60', bpm: 60 },
  pace_breath: { id: 'pace_breath', name: '0.10 Hz 4-7-8 Breath', cssClass: 'philocardia-pacing-breath', bpm: 15 },
  stillness: { id: 'stillness', name: 'Stillness (Static Heart)', cssClass: 'philocardia-stillness', bpm: 0 }
};

/**
 * Renders raw text with Philocardia heart tittles safely using programmatic DOM nodes.
 * Guarantees zero DOM XSS and preserves strict stem alignment.
 */
export function renderPhilocardiaNodes(container, rawText, pacingClass = 'philocardia-pacing-72', variety = 'heart') {
  container.replaceChildren();
  if (variety === 'dot') {
    container.textContent = rawText;
    if (container.dataset) {
      delete container.dataset.tittleVariety;
    }
    if (typeof container.removeAttribute === 'function') {
      container.removeAttribute('data-tittle-variety');
    }
    return;
  }

  container.dataset.tittleVariety = variety;

  for (let i = 0; i < rawText.length; i++) {
    const ch = rawText[i];
    if (ch === 'i') {
      const span = document.createElement('span');
      span.className = `philocardia-heart ${pacingClass}`;
      span.textContent = 'ı'; // dotless i
      container.appendChild(span);
    } else if (ch === 'j') {
      const span = document.createElement('span');
      span.className = `philocardia-j ${pacingClass}`;
      span.textContent = 'ȷ'; // dotless j
      container.appendChild(span);
    } else {
      container.appendChild(document.createTextNode(ch));
    }
  }
}

export const NARRATIVE_ARC_GENRES = {
  noir_mystery: {
    id: 'noir_mystery',
    name: 'Noir Mystery',
    badge: 'KISHŌTENKETSU · SCOTOPIC NOIR',
    structure: '4-Act Noir Turn + Echo',
    defaultSeed: 'the harbor ledger',
    defaultBlend: 'noir_shadow',
    sceneClass: 'cc-scene-noir',
    accent: '#38bdf8',
    beats: [
      {
        act: 'I · Hook',
        beatName: 'Rain & Ledger',
        speaker: 'NARRATOR (V.O.)',
        prosody: 'narrator',
        weight: 320,
        slant: -7.5,
        aptr: 60,
        tension: 24,
        bpm: 66,
        morphology: 'sinus',
        template: 'Midnight mist settles over {{SEED}} while dock lamps flicker on.'
      },
      {
        act: 'II · Shift',
        beatName: 'Whispered Alibi',
        speaker: 'DETECTIVE',
        prosody: 'whisper',
        weight: 240,
        slant: -6,
        aptr: 70,
        tension: 48,
        bpm: 78,
        morphology: 'sinus',
        template: 'Check timecode 02:14 — someone rewrote {{SEED}} before dawn.'
      },
      {
        act: 'III · Turn',
        beatName: 'Submerged Proof',
        speaker: 'AMBIENCE',
        prosody: 'soundfx',
        weight: 520,
        slant: 0,
        aptr: 80,
        tension: 76,
        bpm: 106,
        morphology: 'adenosine',
        icon: '🌧️',
        template: '[♪ sodium shutter snaps over {{SEED}}: 106 BPM pulse ♪]'
      },
      {
        act: 'IV · Confrontation',
        beatName: 'The Missing Page',
        speaker: 'ELENA',
        prosody: 'urgent',
        weight: 760,
        slant: 0,
        aptr: 90,
        tension: 92,
        bpm: 138,
        morphology: 'vtach',
        template: 'Leave {{SEED}} in the vault — the harbor pilot already knows!'
      },
      {
        act: 'V · Echo',
        beatName: 'Dawn Resolve',
        speaker: 'NARRATOR (V.O.)',
        prosody: 'whisper',
        weight: 300,
        slant: -6.5,
        aptr: 65,
        tension: 30,
        bpm: 64,
        morphology: 'sinus',
        template: 'Morning fog clears over {{SEED}}; only the inked margin remains.'
      }
    ]
  },

  scifi_telemetry: {
    id: 'scifi_telemetry',
    name: 'Hard Sci-Fi Telemetry',
    badge: 'FREYTAG PYRAMID · ORBITAL',
    structure: '5-Beat Telemetry Escalation',
    defaultSeed: 'Relay Station 09',
    defaultBlend: 'clinical_teal',
    sceneClass: 'cc-scene-aptn',
    accent: '#22d3ee',
    beats: [
      {
        act: 'I · Exposition',
        beatName: 'Nominal Orbit',
        speaker: 'FLIGHT DECK',
        prosody: 'dialogue',
        weight: 400,
        slant: 0,
        aptr: 55,
        tension: 18,
        bpm: 64,
        morphology: 'sinus',
        template: '{{SEED}} telemetry locked at 0.02 Hz drift; hull pressure nominal.'
      },
      {
        act: 'II · Rising',
        beatName: 'Phase Anomaly',
        speaker: 'SENSOR ARRAY',
        prosody: 'soundfx',
        weight: 540,
        slant: 0,
        aptr: 75,
        tension: 54,
        bpm: 98,
        morphology: 'adenosine',
        icon: '📡',
        template: '[♪ sub-band Doppler chime detected around {{SEED}} ♪]'
      },
      {
        act: 'III · Climax',
        beatName: 'Containment Breach',
        speaker: 'COMMANDER',
        prosody: 'shout',
        weight: 880,
        slant: 0,
        aptr: 95,
        tension: 96,
        bpm: 162,
        morphology: 'vtach',
        template: 'VENT BUS B AT {{SEED}} NOW! OVERRIDE THRUST TO 104 kN!'
      },
      {
        act: 'IV · Falling',
        beatName: 'Manual Trim',
        speaker: 'ENGINEER',
        prosody: 'urgent',
        weight: 660,
        slant: 0,
        aptr: 85,
        tension: 62,
        bpm: 108,
        morphology: 'adenosine',
        template: '{{SEED}} gimbal stabilized at 0.4 deg; coolant flow recovering.'
      },
      {
        act: 'V · Denouement',
        beatName: 'Signal Silence',
        speaker: 'FLIGHT DECK',
        prosody: 'whisper',
        weight: 280,
        slant: -5,
        aptr: 60,
        tension: 22,
        bpm: 62,
        morphology: 'sinus',
        template: 'Horizon beacon at {{SEED}} steady. Crew breathing rate normal.'
      }
    ]
  },

  clinical_documentary: {
    id: 'clinical_documentary',
    name: 'Field & Medical Doc',
    badge: 'BRAIDED CASE ARC · ISMP',
    structure: '5-Stage Clinical Vignette',
    defaultSeed: 'Ward B · 12-Lead Monitor',
    defaultBlend: 'clinical_teal',
    sceneClass: 'cc-scene-trauma',
    accent: '#10b981',
    beats: [
      {
        act: 'I · Baseline',
        beatName: 'Field Arrival',
        speaker: 'CLINICIAN',
        prosody: 'dialogue',
        weight: 400,
        slant: 0,
        aptr: 55,
        tension: 25,
        bpm: 74,
        morphology: 'sinus',
        template: 'Morning handoff at {{SEED}}: baseline SpO2 98%, clear airways.'
      },
      {
        act: 'II · Complication',
        beatName: 'Rhythm Drift',
        speaker: 'TELEMETRY',
        prosody: 'soundfx',
        weight: 560,
        slant: 0,
        aptr: 75,
        tension: 60,
        bpm: 112,
        morphology: 'adenosine',
        icon: '🩺',
        template: '[♪ atrial premature alarm triggered on {{SEED}} ♪]'
      },
      {
        act: 'III · Intervention',
        beatName: 'ISMP Order',
        speaker: 'ATTENDING',
        prosody: 'urgent',
        weight: 760,
        slant: 0,
        aptr: 90,
        tension: 90,
        bpm: 158,
        morphology: 'vtach',
        template: 'Verify 1.0 mg vial at {{SEED}} — administer 0.5 mL slow IV push!'
      },
      {
        act: 'IV · Turn',
        beatName: 'Rate Conversion',
        speaker: 'NURSE',
        prosody: 'dialogue',
        weight: 450,
        slant: 0,
        aptr: 70,
        tension: 52,
        bpm: 92,
        morphology: 'adenosine',
        template: '{{SEED}} trace widening cleanly; patient reporting ease of breath.'
      },
      {
        act: 'V · Resolution',
        beatName: 'Vagal Coherence',
        speaker: 'CLINICIAN',
        prosody: 'whisper',
        weight: 300,
        slant: -4,
        aptr: 60,
        tension: 18,
        bpm: 64,
        morphology: 'sinus',
        template: 'Normal sinus rhythm restored on {{SEED}} at 64 BPM.'
      }
    ]
  },

  folktale_awen: {
    id: 'folktale_awen',
    name: 'Folktale / Highland Ballad',
    badge: 'AWEN GROVE · HERO CIRCLE',
    structure: '5-Step Threshold Circle',
    defaultSeed: 'the moss clock tower',
    defaultBlend: 'hearth_amber',
    sceneClass: 'cc-scene-noir',
    accent: '#f59e0b',
    beats: [
      {
        act: 'I · Hearth',
        beatName: 'Ordinary Grove',
        speaker: 'CHRONICLER',
        prosody: 'narrator',
        weight: 360,
        slant: -6,
        aptr: 55,
        tension: 20,
        bpm: 62,
        morphology: 'sinus',
        template: 'Long before roads crossed the ridge, mist kept {{SEED}} hidden.'
      },
      {
        act: 'II · Threshold',
        beatName: 'Runic Summons',
        speaker: 'TRAVELLER',
        prosody: 'whisper',
        weight: 260,
        slant: -7,
        aptr: 65,
        tension: 45,
        bpm: 74,
        morphology: 'sinus',
        template: 'Listen — silver chimes are rising beneath the roots of {{SEED}}.'
      },
      {
        act: 'III · Ordeal',
        beatName: 'Tempest & Trial',
        speaker: 'GROVE WIND',
        prosody: 'urgent',
        weight: 740,
        slant: 0,
        aptr: 85,
        tension: 86,
        bpm: 132,
        morphology: 'adenosine',
        icon: '🌿',
        template: 'Speak your true vow at {{SEED}} before the solstice tide turns!'
      },
      {
        act: 'IV · Boon',
        beatName: 'Candlelight Pact',
        speaker: 'TRAVELLER',
        prosody: 'dialogue',
        weight: 420,
        slant: 0,
        aptr: 65,
        tension: 42,
        bpm: 72,
        morphology: 'sinus',
        template: 'The brass pendulum of {{SEED}} steadies beside an open lantern.'
      },
      {
        act: 'V · Return',
        beatName: 'Stillness at Dusk',
        speaker: 'CHRONICLER',
        prosody: 'whisper',
        weight: 310,
        slant: -5,
        aptr: 60,
        tension: 16,
        bpm: 58,
        morphology: 'sinus',
        template: 'We carry warmth back down the trail, remembering {{SEED}}.'
      }
    ]
  },

  thriller_pulse: {
    id: 'thriller_pulse',
    name: 'Psychological Thriller',
    badge: 'SAWTOOTH ESCALATION · LIVE',
    structure: '5-Beat Sawtooth Pulse',
    defaultSeed: 'Platform 04',
    defaultBlend: 'noir_shadow',
    sceneClass: 'cc-scene-eas',
    accent: '#f43f5e',
    beats: [
      {
        act: 'I · False Calm',
        beatName: 'Quiet Concourse',
        speaker: 'COMMUTER',
        prosody: 'dialogue',
        weight: 380,
        slant: 0,
        aptr: 55,
        tension: 30,
        bpm: 72,
        morphology: 'sinus',
        template: 'Only three passengers remain on {{SEED}} after the 23:40 express.'
      },
      {
        act: 'II · Uncanny',
        beatName: 'Footstep Echo',
        speaker: 'SFX',
        prosody: 'soundfx',
        weight: 500,
        slant: 0,
        aptr: 75,
        tension: 66,
        bpm: 110,
        morphology: 'adenosine',
        icon: '⚡',
        template: '[♪ fluorescent ballast buzzes above {{SEED}} as a radio clicks ♪]'
      },
      {
        act: 'III · Drop',
        beatName: 'False Relief',
        speaker: 'DISPATCH',
        prosody: 'whisper',
        weight: 250,
        slant: -7,
        aptr: 70,
        tension: 40,
        bpm: 80,
        morphology: 'sinus',
        template: 'All clear on {{SEED}}... wait, why is the stairwell camera dark?'
      },
      {
        act: 'IV · Fracture',
        beatName: 'Peak Pursuit',
        speaker: 'VOICE (OFF)',
        prosody: 'shout',
        weight: 900,
        slant: 0,
        aptr: 95,
        tension: 98,
        bpm: 170,
        morphology: 'vtach',
        template: 'DO NOT OPEN THE SERVICE DOOR ON {{SEED}} — RUN!'
      },
      {
        act: 'V · Aftershock',
        beatName: 'Cold Daylight',
        speaker: 'INSPECTOR',
        prosody: 'dialogue',
        weight: 420,
        slant: -3,
        aptr: 65,
        tension: 52,
        bpm: 84,
        morphology: 'sinus',
        template: 'Tape ends at 00:07 on {{SEED}}. Lock the archive before briefing.'
      }
    ]
  }
};

export class NarrativeArcGenerator {
  static getGenres() {
    return Object.values(NARRATIVE_ARC_GENRES);
  }

  static generateArc(genreId = 'noir_mystery', rawSeed = '') {
    const genre = NARRATIVE_ARC_GENRES[genreId] || NARRATIVE_ARC_GENRES.noir_mystery;
    const cleanedSeed = (rawSeed || '').replace(/[\r\n<>]+/g, ' ').trim().slice(0, 48);
    const seed = cleanedSeed || genre.defaultSeed;
    const measurer = new ClosedCaptionStudio();

    const cues = genre.beats.map((b) => {
      const text = b.template.replace(/\{\{SEED\}\}/g, seed);
      const autoWidth = measurer.calculateLineFit(text, 37);
      const preset = PROSODY_PRESETS[b.prosody] || PROSODY_PRESETS.dialogue;
      return {
        act: b.act,
        beatName: b.beatName,
        tension: b.tension,
        bpm: b.bpm,
        morphology: b.morphology,
        speaker: b.speaker,
        text,
        prosody: b.prosody,
        weight: b.weight,
        width: autoWidth,
        slant: b.slant,
        aptr: normalizeAptr(b.aptr !== undefined ? b.aptr : preset.aptr),
        soft: b.soft !== undefined ? b.soft : preset.soft,
        hlng: b.hlng !== undefined ? b.hlng : preset.hlng,
        boum: b.boum !== undefined ? b.boum : preset.boum,
        thrm: b.thrm !== undefined ? b.thrm : preset.thrm,
        grav: b.grav !== undefined ? b.grav : preset.grav,
        opsz: b.opsz !== undefined ? b.opsz : preset.opsz,
        icon: b.icon
      };
    });

    return {
      id: 'narrative_arc',
      genreId: genre.id,
      genreName: genre.name,
      title: `🎭 ${genre.name}: ${seed}`,
      badge: genre.badge,
      structure: genre.structure,
      defaultBlend: genre.defaultBlend,
      sceneClass: genre.sceneClass,
      accent: genre.accent,
      seed,
      cues
    };
  }
}

export const PHL197_STANCES = {
  assent: { id: 'assent', label: 'Assent (Accept Claim)', desc: 'Provisional agreement after checking evidence and framing.' },
  negotiate: { id: 'negotiate', label: 'Negotiate (Separate Tone vs. Claim)', desc: 'Accept verifiable facts while stripping typographic or emotional spin.' },
  resist: { id: 'resist', label: 'Resist (Reject Manufactured Frame)', desc: 'Challenge the implicit urgency, ideology, or unverified source authority.' }
};

export const PHL197_THINKER_LENSES = {
  postman: {
    id: 'postman',
    name: 'Neil Postman · Amusing Ourselves to Death',
    thesis: 'Electronic broadcast turns complex inquiry into emotional entertainment.',
    question: 'Does this typography invite slow verification, or demand immediate visceral arousal?'
  },
  mcluhan: {
    id: 'mcluhan',
    name: 'Marshall McLuhan · The Medium is the Massage',
    thesis: 'The medium alters sensory ratios before the audience evaluates content.',
    question: 'What assumptions about authority or urgency are baked into the font weight and scrim?'
  },
  gleick: {
    id: 'gleick',
    name: 'James Gleick · The Information',
    thesis: 'Channel capacity and symbol disambiguation decide whether truth survives noise.',
    question: 'Are digits and lookalikes (0/O, 1/l/I, Z/2) legible without distortion under stress?'
  },
  baudrillard: {
    id: 'baudrillard',
    name: 'Jean Baudrillard · Hyperreality',
    thesis: 'Simulations and aesthetic codes can feel more real than underlying reality.',
    question: 'Are the story beats or chyron alarms pointing to reality, or manufacturing an artificial crisis?'
  }
};

export function evaluateDeconstructionLens(cue, scene, stance = 'negotiate', thinkerId = 'postman') {
  const activeCue = cue || { speaker: 'UNKNOWN', text: '', prosody: 'dialogue', weight: 400, width: 100, slant: 0, aptr: 0.5 };
  const activeScene = scene || BROADCAST_SCENES.trauma_bay;
  const w = Number(activeCue.weight || 400);
  const wd = Number(activeCue.width || 100);
  const sl = Number(activeCue.slant || 0);
  const ap = normalizeAptr(activeCue.aptr !== undefined ? activeCue.aptr : 0.5);
  const text = activeCue.text || '';
  const hasAllCaps = text.length > 6 && text === text.toUpperCase() && /[A-Z]/.test(text);
  const hasDosageOrNumber = /\d+(?:\.\d+)?\s*(?:mg|ml|bpm|hz|kn|km\/h|%|am|pm)/i.test(text);

  let framingMode = 'Deliberative Baseline';
  let conventionStatus = 'Balanced documentary convention — neutral stroke weight leaves cognitive room.';
  if (w >= 700 || hasAllCaps || activeCue.prosody === 'shout') {
    framingMode = 'High-Arousal Chyron / Alarm';
    conventionStatus = 'Broadcast urgency convention: condensed/heavy strokes compress time and nudge compliance.';
  } else if (activeCue.prosody === 'soundfx') {
    framingMode = 'Acoustic Priming Event';
    conventionStatus = 'Non-speech FX bracket primes emotional expectation ahead of spoken facts.';
  } else if (activeCue.prosody === 'whisper' || sl < -3) {
    framingMode = 'Intimate Affective Hook';
    conventionStatus = 'Oblique light-weight cue narrows distance, creating conspiratorial or somatic intimacy.';
  }

  const thinker = PHL197_THINKER_LENSES[thinkerId] || PHL197_THINKER_LENSES.postman;
  const stanceInfo = PHL197_STANCES[stance] || PHL197_STANCES.negotiate;

  const howDoIKnow = hasDosageOrNumber
    ? `Verify quantified telemetry (${text.match(/\d+(?:\.\d+)?\s*(?:mg|ml|bpm|hz|kn|km\/h|%|am|pm)/i)[0]}) independently of speaker ${activeCue.speaker}; check ISMP glyphs cleanly.`
    : `Separate ${activeCue.speaker}'s prosody (wght ${w}) from verifiable primary evidence: what source proves "${text.slice(0, 56)}"?`;

  return {
    framingMode,
    sourceSummary: `Speaker "${activeCue.speaker}" inside "${activeScene.title || activeScene.id}". Ask: Who benefits if I react before checking?`,
    productSummary: `wght ${w} · wdth ${wd}% · slnt ${sl} · APTR ${ap.toFixed(2)} — ${conventionStatus}`,
    audienceSummary: `Stance: ${stanceInfo.label}. ${hasAllCaps ? 'All-caps casts viewer as passive responder.' : 'Mixed-case allows selective verification.'}`,
    thinkerNote: `${thinker.name}: ${thinker.question}`,
    howDoIKnow
  };
}

export const SCREENPLAY_SAMPLE_PRESETS = {
  er_handoff: {
    id: 'er_handoff',
    title: 'ER Night Shift Handoff',
    script: `INT. TRAUMA BAY 2 - NIGHT

NURSE ELENA
(whispers, checking chart)
Did anyone else see the 02:14 potassium entry? Look closely at the handwriting.

DR. ARIS
(urgent, sharp)
CHARGED TO 200 JOULES! CLEAR THE BED NOW!

NURSE ELENA
(exhales softly, relieved)
Normal sinus rhythm restored. Breathe slow; pulse steady at 68 bpm.

RESIDENT
(in quiet awe)
Look at the snow falling outside the skylight. Not a sound on the street.`
  },
  noir_confession: {
    id: 'noir_confession',
    title: 'Harbor Noir Confession',
    script: `EXT. FOGGY PIER - 03:00 AM

DETECTIVE MARA (V.O.)
(softly, confessional)
I kept the torn ledger page inside my coat for seven winters.

HARBOR PILOT
(tightly, panicked)
STOP! Do NOT open that locker before the cutter clears the buoy!

DETECTIVE MARA
(warmly, exhaling)
It is over now. You can set the lantern down and rest.`
  },
  orbital_log: {
    id: 'orbital_log',
    title: 'Orbital Telemetry Log',
    script: `INT. RELAY STATION 09 - CUPOLA

FLIGHT CAPTAIN
(calmly)
Hull pressure nominal at 101.3 kPa. Starboard array aligned.

SENSOR ARRAY
(alarming)
[♪ hull micrometeorite warning klaxon — delta-v critical! ♪]

ENGINEER
(breathless, urgent)
SEAL BULKHEAD 4! Manual gimbal override engaged!

FLIGHT CAPTAIN
(wondrous, quiet)
Look below... the aurora is wrapping the entire terminator in emerald.`
  }
};

export function inferCueAffect(text = '', parenthetical = '', speaker = '') {
  const cleanText = String(text || '');
  const cleanDir = String(parenthetical || '').toLowerCase();
  const cleanSpeaker = String(speaker || '').toUpperCase();
  const lower = `${cleanDir} ${cleanText.toLowerCase()}`;

  const letterCount = (cleanText.match(/[A-Za-z]/g) || []).length;
  const upperCount = (cleanText.match(/[A-Z]/g) || []).length;
  const isMostlyCaps = letterCount >= 6 && (upperCount / letterCount) >= 0.72;
  const hasExclaim = cleanText.includes('!');
  const hasBracketFx = /^\[.*\]$/.test(cleanText.trim()) || cleanText.includes('♪');

  const clamp01 = (n) => Number(Math.max(0, Math.min(1, n)).toFixed(2));
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

  const isPanic =
    isMostlyCaps ||
    /\b(panic|panicked|urgent|urgently|shout|shouting|yell|scream|sharp|tightly|alarm|alarming|warning|clear|stat|run|stop|now|emergency|critical|breach|charged)\b/.test(lower) ||
    hasExclaim;

  const isIntimate =
    /\b(whisper|whispers|whispering|softly|quietly|confess|confessional|secret|intimate|murmur|hush|tender|low voice|v\.o\.|breathless)\b/.test(lower) ||
    cleanSpeaker.includes('V.O.') ||
    cleanText.includes('...');

  const isRelief =
    /\b(relief|relieved|exhale|exhales|exhaling|calm|calmly|restored|steady|breathe|warm|warmly|gentle|safe|settle|nominal|home|rest)\b/.test(lower);

  const isAwe =
    /\b(awe|wonder|wondrous|reverence|horizon|aurora|stars|cosmos|ocean|skylight|snow|emerald|infinite|vast)\b/.test(lower);

  let emotionId = 'dialogue';
  let prosody = 'dialogue';
  let base = {
    weight: 400,
    width: 100,
    slant: 0,
    opsz: 20,
    aptr: 0.55,
    soft: 0.25,
    hlng: 0.20,
    boum: 0.15,
    thrm: 0.0,
    grav: 0.10,
    letterSpacing: '0.015em',
    tension: 32,
    bpm: 72,
    morphology: 'sinus'
  };

  if (hasBracketFx && !isPanic) {
    emotionId = 'soundfx';
    prosody = 'soundfx';
    base = { ...PROSODY_PRESETS.soundfx, width: 100, tension: 58, bpm: 98, morphology: 'adenosine' };
  } else if (isPanic && !isRelief) {
    emotionId = 'panic';
    prosody = isMostlyCaps ? 'shout' : 'urgent';
    const tok = EMOTION_TOKENS.panic;
    base = {
      weight: tok.weight,
      width: tok.width,
      slant: tok.slant,
      opsz: tok.opsz,
      aptr: tok.aptr,
      soft: tok.soft,
      hlng: tok.hlng,
      boum: tok.boum,
      thrm: tok.thrm,
      grav: tok.grav,
      letterSpacing: tok.tracking,
      tension: isMostlyCaps ? 94 : 80,
      bpm: isMostlyCaps ? 162 : 134,
      morphology: 'vtach'
    };
  } else if (isAwe) {
    emotionId = 'awe';
    prosody = 'narrator';
    const tok = EMOTION_TOKENS.awe;
    base = {
      weight: tok.weight,
      width: tok.width,
      slant: tok.slant,
      opsz: tok.opsz,
      aptr: tok.aptr,
      soft: tok.soft,
      hlng: tok.hlng,
      boum: tok.boum,
      thrm: tok.thrm,
      grav: tok.grav,
      letterSpacing: tok.tracking,
      tension: 38,
      bpm: 64,
      morphology: 'sinus'
    };
  } else if (isRelief) {
    emotionId = 'relief';
    prosody = 'dialogue';
    const tok = EMOTION_TOKENS.relief;
    base = {
      weight: tok.weight,
      width: tok.width,
      slant: tok.slant,
      opsz: tok.opsz,
      aptr: tok.aptr,
      soft: tok.soft,
      hlng: tok.hlng,
      boum: tok.boum,
      thrm: tok.thrm,
      grav: tok.grav,
      letterSpacing: tok.tracking,
      tension: 20,
      bpm: 62,
      morphology: 'sinus'
    };
  } else if (isIntimate) {
    emotionId = 'intimate';
    prosody = 'whisper';
    const tok = EMOTION_TOKENS.intimate;
    base = {
      weight: tok.weight,
      width: tok.width,
      slant: tok.slant,
      opsz: tok.opsz,
      aptr: tok.aptr,
      soft: tok.soft,
      hlng: tok.hlng,
      boum: tok.boum,
      thrm: tok.thrm,
      grav: tok.grav,
      letterSpacing: tok.tracking,
      tension: 44,
      bpm: 66,
      morphology: 'sinus'
    };
  }

  return {
    emotion: emotionId,
    prosody,
    weight: clamp(Math.round(base.weight), 100, 900),
    width: clamp(Math.round(base.width), 75, 100),
    slant: Number(clamp(base.slant, -10.5, 0).toFixed(1)),
    opsz: clamp(Math.round(base.opsz), 6, 72),
    aptr: normalizeAptr(base.aptr),
    soft: clamp01(base.soft),
    hlng: clamp01(base.hlng),
    boum: clamp01(base.boum),
    thrm: clamp01(base.thrm),
    grav: clamp01(base.grav),
    letterSpacing: base.letterSpacing || '0.015em',
    tension: clamp(Math.round(base.tension), 5, 100),
    bpm: clamp(Math.round(base.bpm), 48, 185),
    morphology: base.morphology
  };
}

export function parseScreenplayScript(rawScript = '', options = {}) {
  const cleanAngle = (s) => String(s || '').replace(/[<>]/g, '');
  const lines = String(rawScript || '').replace(/\r\n/g, '\n').split('\n');
  const measurer = new ClosedCaptionStudio();
  const maxBeats = Math.min(32, Math.max(1, Number(options.maxBeats || 24)));

  const parsedEntries = [];
  let sceneHeading = cleanAngle(options.title || 'Screenplay Table Read');
  let currentSpeaker = '';
  let currentDirection = '';
  let textBuffer = [];

  const flushBeat = () => {
    const joined = cleanAngle(textBuffer.join(' ')).replace(/\s+/g, ' ').trim();
    textBuffer = [];
    if (!joined) return;
    parsedEntries.push({
      speaker: cleanAngle(currentSpeaker || 'SPEAKER').trim() || 'SPEAKER',
      direction: cleanAngle(currentDirection).trim(),
      text: joined
    });
    currentDirection = '';
  };

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      flushBeat();
      continue;
    }
    // Skip SRT index digits and timestamp lines cleanly
    if (/^\d+$/.test(line) || /^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*--?>/.test(line)) {
      continue;
    }
    // Scene heading (INT. / EXT.)
    if (/^(?:INT\.|EXT\.|INT\/EXT\.|EST\.)/i.test(line)) {
      flushBeat();
      sceneHeading = cleanAngle(line).slice(0, 64);
      currentSpeaker = '';
      continue;
    }
    // Parenthetical stage direction: (whispers)
    if (line.startsWith('(') && line.endsWith(')') && line.length <= 80) {
      currentDirection = line.slice(1, -1).trim();
      continue;
    }
    // Inline script form: SPEAKER: (dir) dialogue text (must have whitespace after colon and <= 4 words in speaker name)
    const colonIdx = line.indexOf(':');
    if (colonIdx > 0 && colonIdx <= 28 && /\s/.test(line[colonIdx + 1] || '')) {
      const candidateSpeaker = line.slice(0, colonIdx).trim();
      const speakerWords = candidateSpeaker.split(/\s+/);
      if (
        speakerWords.length <= 4 &&
        textBuffer.length === 0 &&
        /^[A-Za-z0-9 .()\-_']+$/.test(candidateSpeaker) &&
        !/^\d/.test(candidateSpeaker) &&
        candidateSpeaker === candidateSpeaker.toUpperCase()
      ) {
        flushBeat();
        currentSpeaker = candidateSpeaker.toUpperCase();
        let rest = line.slice(colonIdx + 1).trim();
        if (rest.startsWith('(')) {
          const closeIdx = rest.indexOf(')');
          if (closeIdx > 1 && closeIdx < 60) {
            currentDirection = rest.slice(1, closeIdx).trim();
            rest = rest.slice(closeIdx + 1).trim();
          }
        }
        if (rest) textBuffer.push(rest);
        continue;
      }
    }
    // Fountain Character Cue line (ALL-CAPS short header without trailing sentence period)
    const isUpperCue =
      line.length >= 2 &&
      line.length <= 36 &&
      line === line.toUpperCase() &&
      /[A-Z]/.test(line) &&
      !/[.!?]$/.test(line) &&
      textBuffer.length === 0;
    if (isUpperCue) {
      flushBeat();
      currentSpeaker = line;
      continue;
    }
    textBuffer.push(line);
  }
  flushBeat();

  const effectiveEntries = parsedEntries.length > 0
    ? parsedEntries.slice(0, maxBeats)
    : [{ speaker: 'WRITER', direction: '', text: 'Paste dialogue or Fountain lines to audition emotional letterforms.' }];

  let cpsWarnings = 0;
  const distinctEmotions = new Set();

  const cues = effectiveEntries.map((entry, idx) => {
    const affect = inferCueAffect(entry.text, entry.direction, entry.speaker);
    const autoWidth = measurer.calculateLineFit(entry.text, 37);
    const width = Math.min(affect.width, autoWidth);
    const evalMetrics = measurer.evaluateReadingMetrics(entry.text, 3.4);
    if (evalMetrics.tier === 'exceeds') cpsWarnings++;
    distinctEmotions.add(affect.emotion);
    return {
      act: `Beat ${idx + 1}`,
      beatName: entry.direction ? entry.direction.slice(0, 22) : affect.emotion.toUpperCase(),
      speaker: entry.speaker,
      parenthetical: entry.direction,
      text: entry.text,
      emotion: affect.emotion,
      prosody: affect.prosody,
      weight: affect.weight,
      width,
      slant: affect.slant,
      opsz: affect.opsz,
      aptr: affect.aptr,
      soft: affect.soft,
      hlng: affect.hlng,
      boum: affect.boum,
      thrm: affect.thrm,
      grav: affect.grav,
      letterSpacing: affect.letterSpacing,
      tension: affect.tension,
      bpm: affect.bpm,
      morphology: affect.morphology,
      sourceMode: 'heuristic'
    };
  });

  const flatCount = cues.filter(c => c.emotion === 'dialogue').length;
  return {
    id: 'narrative_arc',
    genreId: 'screenplay_import',
    genreName: 'Screenplay Table Read',
    title: `🎬 ${sceneHeading}`,
    badge: 'OFFLINE SCRIPT PARSER · SIL OFL 1.1',
    structure: `${cues.length} Dialogue Beats · 10-Axis VF Delivery`,
    defaultBlend: 'clinical_teal',
    sceneClass: 'cc-scene-noir',
    accent: '#38bdf8',
    stats: {
      beatCount: cues.length,
      emotionVariety: distinctEmotions.size,
      flatBeats: flatCount,
      cpsWarnings
    },
    cues
  };
}

export function isLoopbackEndpoint(urlString = '') {
  try {
    const parsed = new URL(String(urlString || '').trim());
    const host = parsed.hostname.toLowerCase();
    return (parsed.protocol === 'http:' || parsed.protocol === 'https:') &&
      (host === '127.0.0.1' || host === 'localhost' || host === '[::1]');
  } catch {
    return false;
  }
}

export function applyRefinedAffectToScene(scene, refinedArray = []) {
  if (!scene || !Array.isArray(scene.cues) || !Array.isArray(refinedArray)) return scene;
  const clamp01 = (n, fallback) => {
    const num = Number(n);
    return Number.isFinite(num) ? Number(Math.max(0, Math.min(1, num)).toFixed(2)) : fallback;
  };
  const clamp = (n, min, max, fallback) => {
    const num = Number(n);
    return Number.isFinite(num) ? Math.max(min, Math.min(max, num)) : fallback;
  };
  const validEmotions = new Set(['intimate', 'panic', 'relief', 'awe', 'dialogue', 'soundfx']);

  const updatedEmotions = new Set();
  const nextCues = scene.cues.map((cue, idx) => {
    const patch = refinedArray.find(r => Number(r && r.index) === idx) || refinedArray[idx];
    if (!patch || typeof patch !== 'object') {
      updatedEmotions.add(cue.emotion);
      return cue;
    }
    const emo = validEmotions.has(patch.emotion) ? patch.emotion : cue.emotion;
    updatedEmotions.add(emo);
    const sl = Number(clamp(patch.slant, -10.5, 0, cue.slant).toFixed(1));
    const tension = Math.round(clamp(patch.tension, 5, 100, cue.tension));
    const bpm = Math.round(clamp(patch.bpm, 48, 185, tension >= 80 ? 156 : tension >= 55 ? 104 : 68));
    return {
      ...cue,
      emotion: emo,
      prosody: emo === 'intimate' ? 'whisper' : emo === 'panic' ? 'urgent' : emo === 'awe' ? 'narrator' : cue.prosody,
      weight: Math.round(clamp(patch.weight, 100, 900, cue.weight)),
      slant: sl,
      aptr: clamp01(patch.aptr, cue.aptr),
      soft: clamp01(patch.soft, cue.soft),
      hlng: clamp01(patch.hlng, cue.hlng),
      boum: clamp01(patch.boum, cue.boum),
      tension,
      bpm,
      morphology: bpm >= 135 ? 'vtach' : bpm >= 100 ? 'adenosine' : 'sinus',
      sourceMode: 'local_llm'
    };
  });

  return {
    ...scene,
    badge: 'LOCAL 127.0.0.1 LLM TAGGED · ZERO EGRESS',
    stats: {
      ...scene.stats,
      emotionVariety: updatedEmotions.size
    },
    cues: nextCues
  };
}

export async function refineScriptWithLocalModel(scene, config = {}) {
  const endpoint = String(config.endpoint || 'http://127.0.0.1:11434/api/chat').trim();
  if (!isLoopbackEndpoint(endpoint)) {
    return { ok: false, reason: 'Blocked non-loopback endpoint (must be 127.0.0.1 or localhost).', scene };
  }
  if (!scene || !Array.isArray(scene.cues) || scene.cues.length === 0) {
    return { ok: false, reason: 'No cues to refine.', scene };
  }

  const timeoutMs = Math.max(1000, Math.min(20000, Number(config.timeoutMs || 6500)));
  const model = String(config.model || 'llama3.2:3b').trim();
  const payloadSummary = scene.cues.map((c, index) => ({
    index,
    speaker: c.speaker,
    direction: c.parenthetical || '',
    text: c.text
  }));

  const systemPrompt =
    'Return ONLY valid JSON with key "beats": an array of objects {index, emotion, weight, slant, soft, hlng, boum, aptr, tension, bpm}. ' +
    'emotion in ["intimate","panic","relief","awe","dialogue"]. weight 100..900, slant -10.5..0, soft/hlng/boum/aptr 0.0..1.0, tension 5..100, bpm 54..175.';
  const isOllamaNative = endpoint.includes('/api/chat');
  const body = isOllamaNative
    ? {
        model,
        stream: false,
        format: 'json',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: JSON.stringify({ beats: payloadSummary }) }
        ]
      }
    : {
        model,
        temperature: 0.2,
        response_format: { type: 'json_object' },
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: JSON.stringify({ beats: payloadSummary }) }
        ]
      };

  const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  try {
    const fetchImpl = config.fetchImpl || globalThis.fetch;
    const res = await fetchImpl(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller ? controller.signal : undefined
    });
    if (!res || !res.ok) {
      return { ok: false, reason: `Local endpoint returned HTTP ${res ? res.status : 'error'} — using offline parser.`, scene };
    }
    const json = await res.json();
    const rawContent = isOllamaNative
      ? (json && json.message && json.message.content)
      : (json && json.choices && json.choices[0] && json.choices[0].message && json.choices[0].message.content);
    const parsedJson = typeof rawContent === 'string' ? JSON.parse(rawContent) : rawContent;
    const beats = Array.isArray(parsedJson) ? parsedJson : (parsedJson && Array.isArray(parsedJson.beats) ? parsedJson.beats : null);
    if (!beats || beats.length === 0) {
      return { ok: false, reason: 'Local model response lacked "beats" JSON array — using offline parser.', scene };
    }
    return {
      ok: true,
      reason: `Refined ${beats.length} beats privately via ${model} on 127.0.0.1.`,
      scene: applyRefinedAffectToScene(scene, beats)
    };
  } catch (err) {
    return { ok: false, reason: `Offline heuristic active (${err && err.name === 'AbortError' ? 'local timeout' : 'no 127.0.0.1 LLM detected'}).`, scene };
  } finally {
    if (timer) clearTimeout(timer);
  }
}

// Global browser initializer
if (typeof window !== 'undefined') {
  window.PocketGullCC = {
    normalizeAptr,
    buildVariationString,
    SCREENPLAY_SAMPLE_PRESETS,
    inferCueAffect,
    parseScreenplayScript,
    isLoopbackEndpoint,
    applyRefinedAffectToScene,
    refineScriptWithLocalModel,
    BROADCAST_SCENES,
    PROSODY_PRESETS,
    EMOTION_TOKENS,
    ATMOSPHERIC_BLENDS,
    SPATIAL_DIRECTIONS,
    TITTLE_VARIETIES,
    CARDIAC_PACING_PRESETS,
    TELETEXT_SPEAKER_PALETTE,
    NARRATIVE_ARC_GENRES,
    NarrativeArcGenerator,
    PHL197_STANCES,
    PHL197_THINKER_LENSES,
    evaluateDeconstructionLens,
    getTeletextSpeakerStyle,
    renderPhilocardiaNodes,
    ClosedCaptionStudio
  };
}
