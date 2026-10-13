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

export const PROSODY_PRESETS = {
  whisper: { weight: 240, slant: -7, letterSpacing: '0.04em', label: 'Whisper / Quiet (240)' },
  dialogue: { weight: 400, slant: 0, letterSpacing: '0em', label: 'Conversational (400)' },
  narrator: { weight: 360, slant: -8, letterSpacing: '0.02em', label: 'Voiceover (360)' },
  urgent: { weight: 700, slant: 0, letterSpacing: '-0.01em', label: 'Urgent Alert (700)' },
  shout: { weight: 900, slant: 0, letterSpacing: '-0.02em', label: 'Shout / Siren (900)' },
  soundfx: { weight: 500, slant: 0, letterSpacing: '0.02em', label: 'Non-Speech FX (500)' }
};

export const EMOTION_TOKENS = {
  intimate: {
    id: 'intimate',
    name: 'Intimate / Whisper',
    weight: 230,
    width: 98,
    slant: -6.5,
    tracking: '0.04em',
    aptr: 65,
    scrimHue: '210, 30%, 10%',
    scrimAlpha: 0.78,
    aura: '0 0 16px rgba(56, 189, 248, 0.15)',
    pacingMs: 3800,
    sampleText: 'I never wanted anyone else to know about this.'
  },
  panic: {
    id: 'panic',
    name: 'Trauma / Acute Panic',
    weight: 820,
    width: 88,
    slant: 0,
    tracking: '-0.01em',
    aptr: 95,
    scrimHue: '0, 45%, 8%',
    scrimAlpha: 0.88,
    aura: '0 0 20px rgba(239, 68, 68, 0.35)',
    pacingMs: 2200,
    sampleText: 'DEFIBRILLATOR CHARGED TO 200 JOULES! ALL CLEAR!'
  },
  relief: {
    id: 'relief',
    name: 'Vagal Relief / Grounding',
    weight: 390,
    width: 100,
    slant: 0,
    tracking: '0.02em',
    aptr: 70,
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
    tracking: '0.08em',
    aptr: 80,
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
  }

  getScene(id = this.currentSceneId) {
    return BROADCAST_SCENES[id] || BROADCAST_SCENES.trauma_bay;
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
      this.currentSceneId = id;
      this.currentCueIndex = 0;
      this.rollupBuffer = [];
    }
  }

  setSpeed(multiplier) {
    this.speedMultiplier = Math.max(0.5, Math.min(3.0, multiplier));
  }

  setMode(mode) {
    if (['pop-on', 'roll-up', 'paint-on'].includes(mode)) {
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
      this.cardiacPacing = CARDIAC_PACING_PRESETS[pacingId].cssClass;
      return CARDIAC_PACING_PRESETS[pacingId];
    }
    return CARDIAC_PACING_PRESETS.pace_72;
  }

  calculateLineFit(text, targetCpl = 37) {
    // Calculates optical width adjustment (75% to 100%) to fit text within broadcast CPL
    if (!text || text.length <= targetCpl) return 100;
    const ratio = targetCpl / text.length;
    const widthPercent = Math.max(75, Math.min(100, Math.round(ratio * 100)));
    return widthPercent;
  }
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

// Global browser initializer
if (typeof window !== 'undefined') {
  window.PocketGullCC = {
    BROADCAST_SCENES,
    PROSODY_PRESETS,
    EMOTION_TOKENS,
    ATMOSPHERIC_BLENDS,
    SPATIAL_DIRECTIONS,
    TITTLE_VARIETIES,
    CARDIAC_PACING_PRESETS,
    renderPhilocardiaNodes,
    ClosedCaptionStudio
  };
}
