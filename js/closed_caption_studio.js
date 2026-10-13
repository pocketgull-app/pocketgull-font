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
    this.rollupBuffer = [];
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

  calculateLineFit(text, targetCpl = 37) {
    // Calculates optical width adjustment (75% to 100%) to fit text within broadcast CPL
    if (!text || text.length <= targetCpl) return 100;
    const ratio = targetCpl / text.length;
    const widthPercent = Math.max(75, Math.min(100, Math.round(ratio * 100)));
    return widthPercent;
  }
}

// Global browser initializer
if (typeof window !== 'undefined') {
  window.PocketGullCC = {
    BROADCAST_SCENES,
    PROSODY_PRESETS,
    ClosedCaptionStudio
  };
}
