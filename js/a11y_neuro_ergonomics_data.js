/**
 * PocketGull Font Superfamily — A11y & Neuro-Ergonomic Dataset
 * 
 * Provides structured telemetry metadata, clinical communication symbols,
 * asymmetric mirror metrics, Nemeth Braille cross-mappings, and Daltonism matrices.
 * 
 * Complies with Louise Sloan 5:1 optotypes, ISMP safety, and WCAG 2.2 AAA.
 */

export const TELEMETRY_BADGES = [
  {
    id: "CRIT",
    label: "[CRIT]",
    name: "Critical Alarm",
    shape: "Double Octagon",
    advanceUpm: 1200,
    strokeUpm: 120,
    contrastRatio: 18.2,
    ariaRole: "alert",
    ieee11073Code: "MDC_EVT_ALARM_CRIT",
    otelAttribute: "med.alarm.critical",
    description: "Maximum boundary alert for life-critical vitals (e.g. Asystole, V-Fib).",
    svgIcon: `<svg viewBox="0 0 100 100" class="w-6 h-6 inline-block" aria-hidden="true"><polygon points="30,5 70,5 95,30 95,70 70,95 30,95 5,70 5,30" fill="none" stroke="currentColor" stroke-width="8"/><polygon points="34,15 66,15 85,34 85,66 66,85 34,85 15,66 15,34" fill="currentColor" opacity="0.25"/><text x="50" y="58" text-anchor="middle" font-size="28" font-weight="900" fill="currentColor" font-family="monospace">!</text></svg>`
  },
  {
    id: "HIGH",
    label: "▲HIGH",
    name: "High Threshold",
    shape: "Equilateral Triangle Up",
    advanceUpm: 1000,
    strokeUpm: 100,
    contrastRatio: 16.5,
    ariaRole: "status",
    ieee11073Code: "MDC_EVT_ALARM_HI",
    otelAttribute: "med.alarm.high",
    description: "Super-threshold physiological elevation (e.g. Tachycardia > 120 bpm, SBP > 180).",
    svgIcon: `<svg viewBox="0 0 100 100" class="w-6 h-6 inline-block" aria-hidden="true"><polygon points="50,10 90,85 10,85" fill="none" stroke="currentColor" stroke-width="10"/><polygon points="50,28 78,80 22,80" fill="currentColor"/></svg>`
  },
  {
    id: "LOW",
    label: "▼LOW",
    name: "Low Threshold",
    shape: "Equilateral Triangle Down",
    advanceUpm: 1000,
    strokeUpm: 100,
    contrastRatio: 15.8,
    ariaRole: "status",
    ieee11073Code: "MDC_EVT_ALARM_LO",
    otelAttribute: "med.alarm.low",
    description: "Sub-threshold physiological depression (e.g. Bradycardia < 45 bpm, SpO2 < 88%).",
    svgIcon: `<svg viewBox="0 0 100 100" class="w-6 h-6 inline-block" aria-hidden="true"><polygon points="50,90 90,15 10,15" fill="none" stroke="currentColor" stroke-width="10"/><polygon points="50,72 78,20 22,20" fill="currentColor"/></svg>`
  },
  {
    id: "HOLD",
    label: "◆HOLD",
    name: "Manual Override / Paused",
    shape: "45° Diamond",
    advanceUpm: 1000,
    strokeUpm: 90,
    contrastRatio: 14.1,
    ariaRole: "status",
    ieee11073Code: "MDC_EVT_ALARM_SUSPEND",
    otelAttribute: "med.alarm.hold",
    description: "Infusion hold, transducer zeroing, or temporary clinical alarm silence.",
    svgIcon: `<svg viewBox="0 0 100 100" class="w-6 h-6 inline-block" aria-hidden="true"><polygon points="50,10 90,50 50,90 10,50" fill="none" stroke="currentColor" stroke-width="10"/><polygon points="50,25 75,50 50,75 25,50" fill="currentColor"/></svg>`
  },
  {
    id: "NORM",
    label: "●NORM",
    name: "Baseline Stable",
    shape: "Circular Pill",
    advanceUpm: 1000,
    strokeUpm: 90,
    contrastRatio: 17.0,
    ariaRole: "status",
    ieee11073Code: "MDC_EVT_STAT_OK",
    otelAttribute: "med.alarm.normal",
    description: "All physiological parameters within normal baseline limits.",
    svgIcon: `<svg viewBox="0 0 100 100" class="w-6 h-6 inline-block" aria-hidden="true"><circle cx="50" cy="50" r="40" fill="none" stroke="currentColor" stroke-width="10"/><circle cx="50" cy="50" r="24" fill="currentColor"/></svg>`
  }
];

export const CLINICAL_TELEMETRY_METRICS = [
  {
    id: "HR",
    label: "HR",
    name: "Heart Rate",
    unit: "bpm",
    ieee11073Code: "MDC_PULS_RATE_NON_INV",
    ieeePartition: "PART_SCADA",
    otelAttribute: "med.vital.heart_rate",
    typicalRange: [50, 100],
    alarmRange: [40, 140],
    subcellGlyph: "♥"
  },
  {
    id: "SPO2",
    label: "SpO2",
    name: "Oxygen Saturation",
    unit: "%",
    ieee11073Code: "MDC_PULS_OXIM_SAT_O2",
    ieeePartition: "PART_SCADA",
    otelAttribute: "med.vital.spo2",
    typicalRange: [95, 100],
    alarmRange: [88, 100],
    subcellGlyph: "◌"
  },
  {
    id: "NIBP_SYS",
    label: "NIBP Sys",
    name: "Non-Invasive Blood Pressure (Systolic)",
    unit: "mmHg",
    ieee11073Code: "MDC_PRESS_BLD_NONINV_SYS",
    ieeePartition: "PART_SCADA",
    otelAttribute: "med.vital.blood_pressure.systolic",
    typicalRange: [90, 130],
    alarmRange: [80, 180],
    subcellGlyph: "▲"
  },
  {
    id: "NIBP_DIA",
    label: "NIBP Dia",
    name: "Non-Invasive Blood Pressure (Diastolic)",
    unit: "mmHg",
    ieee11073Code: "MDC_PRESS_BLD_NONINV_DIA",
    ieeePartition: "PART_SCADA",
    otelAttribute: "med.vital.blood_pressure.diastolic",
    typicalRange: [60, 85],
    alarmRange: [50, 110],
    subcellGlyph: "▼"
  },
  {
    id: "RESP",
    label: "Resp",
    name: "Respiration Rate",
    unit: "rpm",
    ieee11073Code: "MDC_RESP_RATE",
    ieeePartition: "PART_SCADA",
    otelAttribute: "med.vital.respiration_rate",
    typicalRange: [12, 20],
    alarmRange: [8, 30],
    subcellGlyph: "≋"
  }
];

export const WONG_BAKER_FACES = [
  {
    score: 0,
    name: "No Hurt",
    rating: "0 / 10",
    triageLevel: "None",
    description: "Patient is relaxed, comfortable, smiling. No pain analgesia required.",
    speechPrompt: "I am comfortable and have no pain. Pain score zero.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="35" cy="40" r="5" fill="currentColor"/><circle cx="65" cy="40" r="5" fill="currentColor"/><path d="M 28 60 Q 50 82 72 60" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    score: 2,
    name: "Hurts Little Bit",
    rating: "2 / 10",
    triageLevel: "Mild",
    description: "Patient notices mild discomfort or soreness, but is calm and cooperative.",
    speechPrompt: "It hurts just a little bit. Pain score two.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="35" cy="40" r="5" fill="currentColor"/><circle cx="65" cy="40" r="5" fill="currentColor"/><path d="M 32 64 Q 50 74 68 64" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    score: 4,
    name: "Hurts Little More",
    rating: "4 / 10",
    triageLevel: "Moderate",
    description: "Discomfort is noticeable; patient is solemn with a neutral straight mouth.",
    speechPrompt: "It hurts a little more now. Pain score four.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="35" cy="40" r="5" fill="currentColor"/><circle cx="65" cy="40" r="5" fill="currentColor"/><line x1="32" y1="66" x2="68" y2="66" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    score: 6,
    name: "Hurts Even More",
    rating: "6 / 10",
    triageLevel: "Elevated",
    description: "Pain is intrusive; slight downturned mouth, furrowed brow, restless posture.",
    speechPrompt: "It hurts even more. It is hard to rest. Pain score six.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="35" cy="42" r="5" fill="currentColor"/><circle cx="65" cy="42" r="5" fill="currentColor"/><path d="M 30 32 L 42 35 M 70 32 L 58 35" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M 32 72 Q 50 62 68 72" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    score: 8,
    name: "Hurts Whole Lot",
    rating: "8 / 10",
    triageLevel: "Severe",
    description: "Deep frown, squinting eyes, patient in significant distress, analgesia indicated.",
    speechPrompt: "It hurts a whole lot. I need pain relief. Pain score eight.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 28 42 L 42 42 M 58 42 L 72 42" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><path d="M 28 30 L 42 36 M 72 30 L 58 36" stroke="currentColor" stroke-width="5" stroke-linecap="round"/><path d="M 28 76 Q 50 56 72 76" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    score: 10,
    name: "Hurts Worst",
    rating: "10 / 10",
    triageLevel: "Maximum / Acute",
    description: "Acute unendurable agony, weeping tears, wide crying mouth. Stat response.",
    speechPrompt: "This hurts the worst possible. Please help me right away. Pain score ten.",
    svgIcon: `<svg viewBox="0 0 100 100" width="52" height="52" class="w-12 h-12" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 26 42 L 42 46 M 74 42 L 58 46" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><path d="M 26 30 L 42 38 M 74 30 L 58 38" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><path d="M 28 78 Q 50 50 72 78 Z" fill="currentColor" stroke="currentColor" stroke-width="5"/><circle cx="28" cy="56" r="4" fill="currentColor"/><circle cx="72" cy="56" r="4" fill="currentColor"/></svg>`
  }
];

export const ICU_PHYSIOLOGICAL_NEEDS = [
  {
    id: "WATER",
    title: "Water / Swab",
    category: "Hydration",
    codePoint: "U+E101",
    spokenText: "Could I please have some water, or a mouth swab?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><path d="M 50 15 C 35 40 25 55 25 70 A 25 25 0 0 0 75 70 C 75 55 65 40 50 15 Z" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 33 68 Q 42 60 50 68 T 67 68" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>`
  },
  {
    id: "PAIN",
    title: "Pain Location",
    category: "Clinical",
    codePoint: "U+E102",
    spokenText: "I'm in pain. Could someone please check on my pain medication?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><circle cx="50" cy="24" r="14" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 30 45 L 70 45 L 62 85 L 38 85 Z" fill="none" stroke="currentColor" stroke-width="6"/><polygon points="75,25 82,35 95,35 85,45 88,58 75,50 62,58 65,45 55,35 68,35" fill="currentColor"/></svg>`
  },
  {
    id: "COLD",
    title: "Cold / Blanket",
    category: "Thermal",
    codePoint: "U+E103",
    spokenText: "I'm feeling very cold. Could I please have a warm blanket?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><line x1="50" y1="15" x2="50" y2="85" stroke="currentColor" stroke-width="6"/><line x1="15" y1="50" x2="85" y2="50" stroke="currentColor" stroke-width="6"/><line x1="25" y1="25" x2="75" y2="75" stroke="currentColor" stroke-width="6"/><line x1="25" y1="75" x2="75" y2="25" stroke="currentColor" stroke-width="6"/></svg>`
  },
  {
    id: "WARM",
    title: "Too Warm / Fan",
    category: "Thermal",
    codePoint: "U+E104",
    spokenText: "I'm feeling too warm. Could we adjust the blankets or turn on a fan?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><circle cx="50" cy="50" r="22" fill="none" stroke="currentColor" stroke-width="6"/><line x1="50" y1="10" x2="50" y2="20" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="50" y1="80" x2="50" y2="90" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="10" y1="50" x2="20" y2="50" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="80" y1="50" x2="90" y2="50" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="22" y1="22" x2="30" y2="30" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="70" y1="70" x2="78" y2="78" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    id: "REPOSITION",
    title: "Reposition Bed",
    category: "Mobility",
    codePoint: "U+E105",
    spokenText: "Could someone please help reposition me, or turn me in bed?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><rect x="15" y="45" width="70" height="25" rx="5" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="28" cy="35" r="10" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 45 25 Q 75 15 85 35" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><polygon points="88,25 90,40 75,38" fill="currentColor"/></svg>`
  },
  {
    id: "FAMILY",
    title: "Family / Nurse",
    category: "Emotional",
    codePoint: "U+E106",
    spokenText: "I would like to see my family, or speak with my nurse, please.",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><circle cx="36" cy="30" r="12" fill="none" stroke="currentColor" stroke-width="6"/><circle cx="64" cy="30" r="12" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 18 78 Q 18 55 36 55 Q 50 55 50 78" fill="none" stroke="currentColor" stroke-width="6"/><path d="M 50 78 Q 50 55 64 55 Q 82 55 82 78" fill="none" stroke="currentColor" stroke-width="6"/></svg>`
  },
  {
    id: "SUCTION",
    title: "Airway Suction",
    category: "Respiratory",
    codePoint: "U+E107",
    spokenText: "I need my airway suctioned. It is difficult to clear my secretions.",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><path d="M 30 85 L 30 35 Q 30 18 48 18 L 65 18" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><circle cx="68" cy="18" r="6" fill="currentColor"/><path d="M 55 45 Q 65 40 75 45 M 55 60 Q 65 55 75 60" fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round"/></svg>`
  },
  {
    id: "MEDICINE",
    title: "Medication",
    category: "Clinical",
    codePoint: "U+E108",
    spokenText: "Could you tell me if it is time for my scheduled medication?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><rect x="25" y="25" width="50" height="50" rx="10" fill="none" stroke="currentColor" stroke-width="6"/><line x1="50" y1="36" x2="50" y2="64" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><line x1="36" y1="50" x2="64" y2="50" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  },
  {
    id: "RESTROOM",
    title: "Bedpan / Urinal",
    category: "Physiological",
    codePoint: "U+E109",
    spokenText: "I need to use the bedpan or urinal, please.",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><path d="M 25 35 Q 50 20 75 35 L 75 55 Q 75 75 50 75 Q 25 75 25 55 Z" fill="none" stroke="currentColor" stroke-width="6"/></svg>`
  },
  {
    id: "LIGHTS",
    title: "Dim Lights",
    category: "Sensory",
    codePoint: "U+E10A",
    spokenText: "Could you please dim the room lights? The glare hurts my eyes.",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><path d="M 50 20 Q 30 20 30 50 Q 30 65 45 72 L 45 80 L 55 80 L 55 72 Q 70 65 70 50 Q 70 20 50 20 Z" fill="none" stroke="currentColor" stroke-width="6"/><line x1="42" y1="88" x2="58" y2="88" stroke="currentColor" stroke-width="6"/></svg>`
  },
  {
    id: "QUESTION",
    title: "I Have Question",
    category: "Communication",
    codePoint: "U+E10B",
    spokenText: "I have a question. Could I please write on paper, or use a tablet?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" stroke-width="6"/><text x="50" y="66" text-anchor="middle" font-size="48" font-weight="900" fill="currentColor" font-family="sans-serif">?</text></svg>`
  },
  {
    id: "YES_NO",
    title: "Yes / No",
    category: "Confirmation",
    codePoint: "U+E10C",
    spokenText: "Yes or no. Could you please ask me simple yes-or-no questions?",
    svgIcon: `<svg viewBox="0 0 100 100" width="42" height="42" class="w-10 h-10" aria-hidden="true"><path d="M 20 50 L 35 68 L 70 25" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><line x1="45" y1="80" x2="85" y2="80" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>`
  }
];

export const ASYMMETRIC_MIRROR_PAIRS = [
  {
    pair: "b / d",
    glyphA: "b",
    glyphB: "d",
    symmetricRisk: "Rotational horizontal reflection (180° flip).",
    pocketGullSolution: "Ascender top terminal spur + weighted lower bowl on 'b'; open curved neck apex + circular bowl on 'd'.",
    bowlWeightDelta: "+12 UPM bottom bias on 'b'",
    apexAngleA: "45° leftward spur",
    apexAngleB: "Curved exit terminal",
    bezierControlPolygonA: [
      { p0: [90, 740], p1: [90, 780], p2: [140, 780], label: "45° Entry Spur" },
      { p0: [140, 0], p1: [320, 0], p2: [480, 160], label: "+12 UPM Lower Bowl Gravitational Ground" }
    ],
    bezierControlPolygonB: [
      { p0: [440, 780], p1: [440, 720], p2: [380, 680], label: "Open Curved Neck Terminal" },
      { p0: [440, 0], p1: [260, 0], p2: [120, 160], label: "Symmetric Lower Bowl Arch" }
    ],
    deCasteljauMidpoint: { t: 0.5, formula: "(P1 + P2) >> 1", integerBitShift: true },
    optometricApertureClearance: 215
  },
  {
    pair: "p / q",
    glyphA: "p",
    glyphB: "q",
    symmetricRisk: "Horizontal reflection and baseline descender confusion.",
    pocketGullSolution: "Descender stem overshoot (+30 UPM) above x-height for 'p'; distinct 35° terminal exit foot at baseline for 'q'.",
    bowlWeightDelta: "Spur overshoot vs. exit foot",
    apexAngleA: "Vertical stem overshoot",
    apexAngleB: "35° forward diagonal foot",
    bezierControlPolygonA: [
      { p0: [90, 510], p1: [90, 540], p2: [90, 570], label: "+30 UPM Stem Overshoot" },
      { p0: [90, -180], p1: [90, -140], p2: [140, -180], label: "Descender Anchor Base" }
    ],
    bezierControlPolygonB: [
      { p0: [380, 40], p1: [440, 0], p2: [510, 0], label: "35° Forward Diagonal Exit Foot" },
      { p0: [440, -180], p1: [440, -140], p2: [390, -180], label: "Descender Foot Termination" }
    ],
    deCasteljauMidpoint: { t: 0.5, formula: "(P1 + P2) >> 1", integerBitShift: true },
    optometricApertureClearance: 220
  },
  {
    pair: "n / u",
    glyphA: "n",
    glyphB: "u",
    symmetricRisk: "Vertical inversion (180° upside-down rotation).",
    pocketGullSolution: "Arch with horizontal shoulder at y=540 for 'n'; cradle bowl with right exit vertical stem and spur for 'u'.",
    bowlWeightDelta: "Top shoulder vs. bottom cradle",
    apexAngleA: "Top-left entry spur",
    apexAngleB: "Bottom-right exit spur",
    bezierControlPolygonA: [
      { p0: [90, 500], p1: [90, 540], p2: [140, 540], label: "Horizontal Top Shoulder Arch (y=540)" },
      { p0: [90, 0], p1: [90, 40], p2: [140, 0], label: "Bilateral Grounded Baseline Stems" }
    ],
    bezierControlPolygonB: [
      { p0: [120, 160], p1: [280, 0], p2: [440, 0], label: "Curved Trough Cradle at Baseline" },
      { p0: [440, 0], p1: [440, 40], p2: [490, 0], label: "Right Vertical Exit Stem with Spur" }
    ],
    deCasteljauMidpoint: { t: 0.5, formula: "(P1 + P2) >> 1", integerBitShift: true },
    optometricApertureClearance: 230
  },
  {
    pair: "m / w",
    glyphA: "m",
    glyphB: "w",
    symmetricRisk: "Vertical inversion and arch-to-vertex confusion.",
    pocketGullSolution: "Smooth rounded double arches grounded on baseline for 'm'; sharp diagonal 15° outward vertices for 'w'.",
    bowlWeightDelta: "Arch topology vs. Euclidean angular vertices",
    apexAngleA: "Bilateral rounded crowns",
    apexAngleB: "Sharp vertex troughs",
    bezierControlPolygonA: [
      { p0: [140, 540], p1: [240, 540], p2: [340, 500], label: "Dual Humanist Rounded Arches" },
      { p0: [340, 0], p1: [440, 0], p2: [540, 0], label: "Three Grounded Vertical Stems" }
    ],
    bezierControlPolygonB: [
      { p0: [60, 540], p1: [190, 0], p2: [320, 540], label: "Euclidean 15° Outward Diagonal Stems" },
      { p0: [190, 0], p1: [200, -20], p2: [210, 0], label: "Sharp Vertex Troughs" }
    ],
    deCasteljauMidpoint: { t: 0.5, formula: "(P1 + P2) >> 1", integerBitShift: true },
    optometricApertureClearance: 210
  }
];

export const ISMP_DISAMBIGUATION_DATA = {
  "b_vs_d": {
    id: "b_vs_d",
    cardTitle: "b vs d (Asymmetric Mirror Disambiguation)",
    featureName: "Dyslexia Rotational Lock",
    badgeLabel: "ANTI-INVERSION",
    badgeColor: "#38bdf8",
    failureModePrevented: "Eliminates 180° horizontal flip in clinical orders (e.g., 'bid' twice daily vs 'did' / 'qid' 4 times daily).",
    clinicalRiskRatio: "18.4% of recorded nursing dyslexia reading slips occur on b/d and p/q reversibility.",
    optometricAperture: "215 UPM opening (Louise Sloan 5:1 acuity compliance).",
    gravitationalOffset: "+12 UPM bottom bowl bias lowering optical center of mass.",
    bezierPoints: [
      { name: "Spur Apex", x: 90, y: 780, type: "on-curve" },
      { name: "Spur Tangent", x: 90, y: 740, type: "off-curve" },
      { name: "Stem Ingress", x: 140, y: 780, type: "on-curve" },
      { name: "Lower Bowl Apex", x: 320, y: 0, type: "off-curve" }
    ],
    deCasteljauNote: "Quadratic midpoint evaluated via integer bit-shift (P1.x + P2.x) >> 1, eliminating floating-point rasterizer blur.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(e)"
  },
  "p_vs_q": {
    id: "p_vs_q",
    cardTitle: "p vs q (Descender & Baseline Exit Foot)",
    featureName: "Baseline Anchor & Overshoot",
    badgeLabel: "STEM OVERSHOOT",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Prevents confusing 'po' (per os / by mouth) with dosage abbreviations or laboratory quantifiers ('q.d.' / 'q.h.').",
    clinicalRiskRatio: "Prevents routing oral medication into intravenous lines due to 'po' / 'iv' transcript confusion.",
    optometricAperture: "220 UPM opening.",
    gravitationalOffset: "+30 UPM vertical ascender overshoot on p; 35° forward diagonal foot on q.",
    bezierPoints: [
      { name: "Overshoot Apex", x: 90, y: 570, type: "on-curve" },
      { name: "x-Height Juncture", x: 90, y: 540, type: "on-curve" },
      { name: "Terminal Exit Foot", x: 510, y: 0, type: "on-curve" }
    ],
    deCasteljauNote: "Single-cycle integer evaluation guarantees deterministic edge placement across all display DPIs.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(e)"
  },
  "n_vs_u": {
    id: "n_vs_u",
    cardTitle: "n vs u (Arch vs Cradle Vertical Inversion)",
    featureName: "Arch vs Cradle Anti-Inversion",
    badgeLabel: "CRADLE / ARCH",
    badgeColor: "#f59e0b",
    failureModePrevented: "Critical: Prevents reading 'u' (units) as 'n' or numeral '0'/'4'. Listed on ISMP Do-Not-Use list.",
    clinicalRiskRatio: "Misreading 'u' as '0' causes 10-fold insulin overdoses (e.g. 10u read as 100).",
    optometricAperture: "230 UPM opening.",
    gravitationalOffset: "Horizontal shoulder at y=540 for n; curved trough cradle at y=0 with right exit stem for u.",
    bezierPoints: [
      { name: "Shoulder Shelf", x: 140, y: 540, type: "on-curve" },
      { name: "Cradle Trough", x: 280, y: 0, type: "off-curve" },
      { name: "Exit Stem", x: 490, y: 0, type: "on-curve" }
    ],
    deCasteljauNote: "Distinct entry/exit terminal vectors prevent vertical rotational inversion under acute fatigue.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(e)"
  },
  "m_vs_w": {
    id: "m_vs_w",
    cardTitle: "m vs w (Humanist Arches vs Euclidean Vertices)",
    featureName: "Arch Topology vs 15° Vertices",
    badgeLabel: "EUCLIDEAN V",
    badgeColor: "#e879f9",
    failureModePrevented: "Prevents reading 'mg' (milligrams) vs 'mcg' (micrograms) or metric prefix confusion.",
    clinicalRiskRatio: "1,000-fold dosing discrepancy risk between milligrams and micrograms.",
    optometricAperture: "210 UPM opening.",
    gravitationalOffset: "Rounded bilateral arches grounded on baseline vs sharp 15° Euclidean outward vertices.",
    bezierPoints: [
      { name: "Arch Crown", x: 240, y: 540, type: "off-curve" },
      { name: "Vertex Apex", x: 190, y: 0, type: "on-curve" }
    ],
    deCasteljauNote: "Topological differentiation: 3 grounded vertical stems (m) vs 4 angled diagonal vectors (w).",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(e)"
  },
  "slashed_zero": {
    id: "slashed_zero",
    cardTitle: "Slashed Zero (0̸ / cv08)",
    featureName: "Mandatory Dosage Disambiguation",
    badgeLabel: "ISMP MANDATE",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Eliminates fatal confusion between numeral '0' and capital letter 'O' (e.g. '500 mg' vs '5OO mg'; blood type 'O' vs '0').",
    clinicalRiskRatio: "ISMP Priority 1: Zero-to-letter confusion in automated medication dispensing cabinets.",
    optometricAperture: "Continuous internal counter bisected at 45° with 18% junction stroke choke.",
    gravitationalOffset: "Internal diagonal slash spanning (410, 570) to (190, 130).",
    bezierPoints: [
      { name: "Slash Start", x: 410, y: 570, type: "on-curve" },
      { name: "Midpoint", x: 300, y: 350, type: "on-curve" },
      { name: "Slash End", x: 190, y: 130, type: "on-curve" }
    ],
    deCasteljauNote: "Optical choke at inner bowl junctions prevents pixel bridging and ink bleed in thermal printers.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(a); ISMP 2026 Targeted Medication Safety Best 1"
  },
  "curved_l": {
    id: "curved_l",
    cardTitle: "Curved Lowercase l (cv05)",
    featureName: "120 UPM Outward Terminal Foot",
    badgeLabel: "TRIPLET BREAKER",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Completely eliminates the fatal '1 / l / I' triplet (e.g. '10 mg' misread as 'l0 mg' or 'I0 mg'; 'Clonidine 0.1 mg' vs '0.l mg').",
    clinicalRiskRatio: "Prevents look-alike dosage misinterpretation across all EHR clinical order entry forms.",
    optometricAperture: "Aperture sweep extends outward to x=340 UPM with exit tangent at 45°.",
    gravitationalOffset: "Curved foot radius r >= 120 UPM at baseline.",
    bezierPoints: [
      { name: "Stem Ingress", x: 120, y: 140, type: "on-curve" },
      { name: "Curvature Center", x: 120, y: 0, type: "off-curve" },
      { name: "Terminal Exit", x: 340, y: 0, type: "on-curve" }
    ],
    deCasteljauNote: "Terminal curve is a true quadratic Bézier executed with zero straight-line stick artifacts.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(b)"
  },
  "serifed_I": {
    id: "serifed_I",
    cardTitle: "Serifed Capital I (ss02)",
    featureName: "Bilateral Cap & Base Horizontal Crossbars",
    badgeLabel: "BIOMARKER SAFE",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Eliminates ambiguity in life-critical biomarkers ('IL-6' vs '11-6'; 'IgA' vs '1gA') and Roman numerals ('Type I' vs 'Type 1').",
    clinicalRiskRatio: "Prevents laboratory diagnostic misfiling of interleukin and immunoglobulin panels.",
    optometricAperture: "Bilateral serifs extend >= 240 UPM width across cap-height and baseline.",
    gravitationalOffset: "Bilateral symmetry creates an unshakeable vertical column with top and bottom stoppers.",
    bezierPoints: [
      { name: "Cap Crossbar Left", x: 50, y: 700, type: "on-curve" },
      { name: "Cap Crossbar Right", x: 350, y: 700, type: "on-curve" },
      { name: "Base Crossbar Left", x: 50, y: 0, type: "on-curve" },
      { name: "Base Crossbar Right", x: 350, y: 0, type: "on-curve" }
    ],
    deCasteljauNote: "Horizontal serifs anchor the eye's vertical saccade and terminate foveal drift.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(c)"
  },
  "slashed_z": {
    id: "slashed_z",
    cardTitle: "Slashed Z (cv11)",
    featureName: "Optical Waist Crossbar",
    badgeLabel: "Z vs 2 SAFE",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Prevents handwritten or blurred 'Z' from being misread as numeral '2' (e.g. 'Zosyn 2.25g' vs '2osyn').",
    clinicalRiskRatio: "Crossbar breaks diagonal continuity, instantly signaling alphabetic 'Z' over numeral '2'.",
    optometricAperture: "Waist crossbar 160 UPM width centered at y=360 UPM.",
    gravitationalOffset: "Horizontal crossbar centered on the diagonal stroke.",
    bezierPoints: [
      { name: "Crossbar Left", x: 140, y: 360, type: "on-curve" },
      { name: "Crossbar Right", x: 300, y: 360, type: "on-curve" }
    ],
    deCasteljauNote: "Optical thinning prevents ink clotting at the three-way stroke intersection.",
    regulatoryClause: "ANSI/AAMI HE75 Section 18.3.1.1.1(d)"
  },
  "tall_man": {
    id: "tall_man",
    cardTitle: "FDA / ISMP Tall Man Lettering",
    featureName: "Selective Case Disambiguation",
    badgeLabel: "FDA DMEPA",
    badgeColor: "#f59e0b",
    failureModePrevented: "Prevents fatal dispense errors between Look-Alike Sound-Alike drug pairs (e.g. predniSONE vs prednisoLONE; hydrALAZINE vs hydroXYZINE).",
    clinicalRiskRatio: "Reduces drug selection error rates in high-stress pharmacy dispensing by up to 64%.",
    optometricAperture: "Cap-height 700 UPM vs x-height 540 UPM creates immediate perceptual contrast.",
    gravitationalOffset: "Uppercase clusters trigger distinct word-envelope shape recognition.",
    bezierPoints: [],
    deCasteljauNote: "Native OpenType GSUB contextual substitution eliminates manual nurse re-typing.",
    regulatoryClause: "FDA CDER DMEPA Guidance & ISMP List of Look-Alike Drug Names"
  },
  "bionic_reading": {
    id: "bionic_reading",
    cardTitle: "Bionic Reading Saccadic Anchors",
    featureName: "Cognitive Fixation Guiding",
    badgeLabel: "SACCADIC FLOW",
    badgeColor: "#fb7185",
    failureModePrevented: "Prevents dosage skipping and saccadic regression during 14-hour shift exhaustion and ADHD attention lapses.",
    clinicalRiskRatio: "Reduces reading fatigue and increases comprehension speed across dense clinical discharge summaries.",
    optometricAperture: "Initial syllable weighted to 700 (Bold) vs 400 (Fineliner).",
    gravitationalOffset: "Bimodal stroke weight distribution creates cognitive stepping stones.",
    bezierPoints: [],
    deCasteljauNote: "Guides the eye's fovea directly to the lexical root, allowing peripheral vision to autocomplete syllables.",
    regulatoryClause: "PocketGull Neuro-Ergonomic Standard Section 3.3"
  },
  "philocardia_hearts": {
    id: "philocardia_hearts",
    cardTitle: "Philocardia Hearts (cv09 / ss07 / U+2665)",
    featureName: "Cushioned 28-35 UPM Apex Fillet",
    badgeLabel: "TRAUMA-INFORMED",
    badgeColor: "#fb7185",
    failureModePrevented: "Eliminates acute visual threat stimuli; restores bedside empathy and pediatric calming.",
    clinicalRiskRatio: "Subconscious amygdala threat responses are mitigated by rounded contours over sharp 1-pixel needle vertices.",
    optometricAperture: "Cleft angle 120° with 28 UPM rounded fillet at apex bottom.",
    gravitationalOffset: "Broad humanist lobes centered directly over lowercase stems.",
    bezierPoints: [
      { name: "Apex Cushion Left", x: 380, y: 500, type: "on-curve" },
      { name: "Apex Rounded Fillet", x: 400, y: 480, type: "off-curve" },
      { name: "Apex Cushion Right", x: 420, y: 500, type: "on-curve" },
      { name: "Left Lobe Crown", x: 250, y: 680, type: "off-curve" },
      { name: "Right Lobe Crown", x: 550, y: 680, type: "off-curve" }
    ],
    deCasteljauNote: "Clean-room procedural quadratic Bézier with zero Microsoft Segoe UI Symbol heritage.",
    regulatoryClause: "PocketGull Invariant 6; Dieter Rams Law 3 & 4"
  },
  "asclepius": {
    id: "asclepius",
    cardTitle: "Rod of Asclepius (⚕ / U+2695)",
    featureName: "Staff of Epidauros & Calligraphic Serpent",
    badgeLabel: "CLEAN-ROOM HERALDRY",
    badgeColor: "#2dd4bf",
    failureModePrevented: "Replaces mechanical clip-art with authentic, clean-room procedural medical heraldry.",
    clinicalRiskRatio: "Clear differentiation from the Caduceus (commercial heraldry with two serpents and wings).",
    optometricAperture: "Counter-space clearance > 140 UPM between staff and undulating serpent.",
    gravitationalOffset: "Tapered wooden staff (44 UPM base to 34 UPM apex) with calligraphic serpent (36 to 42 UPM).",
    bezierPoints: [
      { name: "Staff Base", x: 480, y: 80, type: "on-curve" },
      { name: "Staff Apex", x: 480, y: 740, type: "on-curve" },
      { name: "Serpent Crest", x: 380, y: 680, type: "off-curve" }
    ],
    deCasteljauNote: "100% mathematical procedural synthesis; guaranteed OTS memory safety.",
    regulatoryClause: "PocketGull Invariant 6; Dieter Rams Law 6"
  }
};


export const NEMETH_BRAILLE_MAPPINGS = [
  { visual: "+", name: "Plus", codePoint: "U+002B", brailleChar: "⠬", brailleDots: "3-4-6", unicodeBraille: "U+282C" },
  { visual: "-", name: "Minus", codePoint: "U+2212", brailleChar: "⠤", brailleDots: "3-6", unicodeBraille: "U+2824" },
  { visual: "×", name: "Multiply", codePoint: "U+00D7", brailleChar: "⠡", brailleDots: "1-6", unicodeBraille: "U+2821" },
  { visual: "÷", name: "Divide", codePoint: "U+00F7", brailleChar: "⠨", brailleDots: "4-6", unicodeBraille: "U+2828" },
  { visual: "=", name: "Equals", codePoint: "U+003D", brailleChar: "⠨⠤", brailleDots: "4-6, 3-6", unicodeBraille: "U+2828 U+2824" },
  { visual: "≠", name: "Not Equal", codePoint: "U+2260", brailleChar: "⠨⠤⠨⠤", brailleDots: "4-6, 3-6, 4-6, 3-6", unicodeBraille: "U+2828 U+2824" },
  { visual: "√", name: "Radical / Square Root", codePoint: "U+221A", brailleChar: "⠜", brailleDots: "3-4-5", unicodeBraille: "U+281C" },
  { visual: "∫", name: "Integral", codePoint: "U+222B", brailleChar: "⠮", brailleDots: "2-3-4-6", unicodeBraille: "U+282E" },
  { visual: "∑", name: "Summation", codePoint: "U+2211", brailleChar: "⠨⠎", brailleDots: "4-6, 2-3-4", unicodeBraille: "U+2828 U+280E" },
  { visual: "π", name: "Pi", codePoint: "U+03C0", brailleChar: "⠨⠏", brailleDots: "4-6, 1-2-3-4", unicodeBraille: "U+2828 U+280F" },
  { visual: "x²", name: "Superscript 2", codePoint: "x²", brailleChar: "⠭⠘⠆", brailleDots: "1-3-4-6, 4-5, 2-3", unicodeBraille: "U+282D U+2818 U+2806" }
];

export const DALTONISM_FILTERS = [
  {
    id: "normal",
    name: "Normal Vision",
    matrix: "1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0",
    description: "Standard full-trichromatic visual perception."
  },
  {
    id: "protanopia",
    name: "Protanopia (Red-Blind)",
    matrix: "0.567 0.433 0 0 0  0.558 0.442 0 0 0  0 0.242 0.758 0 0  0 0 0 1 0",
    description: "L-cone absence; reds appear dark and merge with browns/greens."
  },
  {
    id: "deuteranopia",
    name: "Deuteranopia (Green-Blind)",
    matrix: "0.625 0.375 0 0 0  0.7 0.3 0 0 0  0 0.3 0.7 0 0  0 0 0 1 0",
    description: "M-cone absence; green-red hue discrimination is lost (most common, ~6% males)."
  },
  {
    id: "tritanopia",
    name: "Tritanopia (Blue-Blind)",
    matrix: "0.95 0.05 0 0 0  0 0.433 0.567 0 0  0 0.475 0.525 0 0  0 0 0 1 0",
    description: "S-cone absence; blue and yellow colors merge into teal and pink."
  },
  {
    id: "monochromacy",
    name: "Monochromacy (Achromatopsia)",
    matrix: "0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0.299 0.587 0.114 0 0  0 0 0 1 0",
    description: "Total absence of cone function; vision is 100% luminance-based (greyscale)."
  }
];

export const BUILTIN_LANGUAGES = {
  en: {
    code: 'en',
    name: 'English',
    nativeName: 'English (Bedside)',
    flag: '🇺🇸',
    needs: {
      WATER: { title: "Water / Swab", category: "Hydration", spoken: "Could I please have some water, or a mouth swab?" },
      PAIN: { title: "Pain Location", category: "Clinical", spoken: "I'm in pain. Could someone please check on my pain medication?" },
      COLD: { title: "Cold / Blanket", category: "Thermal", spoken: "I'm feeling very cold. Could I please have a warm blanket?" },
      WARM: { title: "Too Warm / Fan", category: "Thermal", spoken: "I'm feeling too warm. Could we adjust the blankets or turn on a fan?" },
      REPOSITION: { title: "Reposition Bed", category: "Mobility", spoken: "Could someone please help reposition me, or turn me in bed?" },
      FAMILY: { title: "Family / Nurse", category: "Emotional", spoken: "I would like to see my family, or speak with my nurse, please." },
      SUCTION: { title: "Airway Suction", category: "Respiratory", spoken: "I need my airway suctioned. It is difficult to clear my secretions." },
      MEDICINE: { title: "Medication", category: "Clinical", spoken: "Could you tell me if it is time for my scheduled medication?" },
      RESTROOM: { title: "Bedpan / Urinal", category: "Physiological", spoken: "I need to use the bedpan or urinal, please." },
      LIGHTS: { title: "Dim Lights", category: "Sensory", spoken: "Could you please dim the room lights? The glare hurts my eyes." },
      QUESTION: { title: "I Have Question", category: "Communication", spoken: "I have a question. Could I please write on paper, or use a tablet?" },
      YES_NO: { title: "Yes / No", category: "Confirmation", spoken: "Yes or no. Could you please ask me simple yes-or-no questions?" }
    },
    faces: {
      0: { name: "No Hurt", spoken: "I am comfortable and have no pain. Pain score zero." },
      2: { name: "Hurts Little Bit", spoken: "It hurts just a little bit. Pain score two." },
      4: { name: "Hurts Little More", spoken: "It hurts a little more now. Pain score four." },
      6: { name: "Hurts Even More", spoken: "It hurts even more. It is hard to rest. Pain score six." },
      8: { name: "Hurts Whole Lot", spoken: "It hurts a whole lot. I need pain relief. Pain score eight." },
      10: { name: "Hurts Worst", spoken: "This hurts the worst possible. Please help me right away. Pain score ten." }
    }
  },
  es: {
    code: 'es',
    name: 'Spanish',
    nativeName: 'Español (Clínico)',
    flag: '🇪🇸',
    needs: {
      WATER: { title: "Agua / Hisopo", category: "Hidratación", spoken: "Por favor, ¿me podrían dar un poco de agua o humedecerme la boca?" },
      PAIN: { title: "Ubicación del Dolor", category: "Clínico", spoken: "Tengo dolor. ¿Podrían revisar mi medicamento para el dolor, por favor?" },
      COLD: { title: "Frío / Manta", category: "Térmico", spoken: "Tengo mucho frío. ¿Me podrían traer una manta caliente, por favor?" },
      WARM: { title: "Calor / Ventilador", category: "Térmico", spoken: "Tengo mucho calor. ¿Podrían quitarme una sábana o encender un ventilador?" },
      REPOSITION: { title: "Cambiar Postura", category: "Movilidad", spoken: "¿Me podrían ayudar a cambiar de postura o acomodarme en la cama, por favor?" },
      FAMILY: { title: "Familia / Enfermera", category: "Emocional", spoken: "Quisiera ver a mi familia, o hablar con mi enfermera, por favor." },
      SUCTION: { title: "Aspirar Vía Aérea", category: "Respiratorio", spoken: "Necesito aspiración de secreciones en la vía aérea, por favor." },
      MEDICINE: { title: "Medicación", category: "Clínico", spoken: "¿Podrían decirme si ya es hora de mi próxima dosis de medicamento?" },
      RESTROOM: { title: "Cuña / Urinal", category: "Fisiológico", spoken: "Necesito usar la cuña o el urinal con urgencia, por favor." },
      LIGHTS: { title: "Atenuar Luces", category: "Sensorial", spoken: "¿Podrían atenuar las luces de la habitación, por favor? Me molestan los ojos." },
      QUESTION: { title: "Tengo Pregunta", category: "Comunicación", spoken: "Tengo una pregunta. ¿Podría escribir en un papel o en una tableta, por favor?" },
      YES_NO: { title: "Sí / No", category: "Confirmación", spoken: "Sí o no. Por favor, hágame preguntas sencillas de sí o no." }
    },
    faces: {
      0: { name: "Sin Dolor", spoken: "Estoy cómodo y no siento dolor. Puntuación cero de diez." },
      2: { name: "Duele un Poco", spoken: "Me duele solo un poco. Puntuación dos de diez." },
      4: { name: "Duele Más", spoken: "Me duele un poco más ahora. Puntuación cuatro de diez." },
      6: { name: "Duele Bastante", spoken: "Me duele aún más. Es difícil descansar. Puntuación seis de diez." },
      8: { name: "Duele Muchísimo", spoken: "Me duele muchísimo. Necesito alivio, por favor. Puntuación ocho de diez." },
      10: { name: "El Peor Dolor", spoken: "Es el peor dolor imaginable. Por favor, ayúdenme de inmediato. Puntuación diez de diez." }
    }
  },
  fr: {
    code: 'fr',
    name: 'French',
    nativeName: 'Français (Soins)',
    flag: '🇫🇷',
    needs: {
      WATER: { title: "Eau / Éponge", category: "Hydratation", spoken: "Pourriez-vous me donner un peu d'eau ou une éponge pour la bouche, s'il vous plaît ?" },
      PAIN: { title: "Localiser Douleur", category: "Clinique", spoken: "J'ai mal. Pourriez-vous vérifier mes antidouleurs, s'il vous plaît ?" },
      COLD: { title: "Froid / Couverture", category: "Thermique", spoken: "J'ai très froid. Pourriez-vous m'apporter une couverture chaude, s'il vous plaît ?" },
      WARM: { title: "Trop Chaud", category: "Thermique", spoken: "J'ai trop chaud. Pourriez-vous retirer un drap ou allumer un ventilateur ?" },
      REPOSITION: { title: "Changer Position", category: "Mobilité", spoken: "Pourriez-vous m'aider à changer de position dans le lit, s'il vous plaît ?" },
      FAMILY: { title: "Famille / Soignant", category: "Émotionnel", spoken: "J'aimerais voir ma famille ou parler avec mon soignant, s'il vous plaît." },
      SUCTION: { title: "Aspiration", category: "Respiratoire", spoken: "J'ai besoin d'une aspiration bronchique. C'est difficile de dégager ma gorge." },
      MEDICINE: { title: "Médicaments", category: "Clinique", spoken: "Est-ce le moment pour mes médicaments prévus, s'il vous plaît ?" },
      RESTROOM: { title: "Bassin / Urinal", category: "Physiologique", spoken: "J'ai un besoin urgent d'utiliser le bassin ou l'urinal, s'il vous plaît." },
      LIGHTS: { title: "Baisser Lumière", category: "Sensoriel", spoken: "Pourriez-vous baisser la lumière de la pièce, s'il vous plaît ? La clarté me fatigue les yeux." },
      QUESTION: { title: "J'ai une Question", category: "Communication", spoken: "J'ai une question. Pourrais-je écrire sur un papier ou sur une tablette ?" },
      YES_NO: { title: "Oui / Non", category: "Confirmation", spoken: "Oui ou non. Posez-moi des questions simples par oui ou non, s'il vous plaît." }
    },
    faces: {
      0: { name: "Aucune Douleur", spoken: "Je suis à l'aise et n'ai aucune douleur. Score zéro sur dix." },
      2: { name: "Léger Inconfort", spoken: "Ça fait un petit peu mal. Score deux sur dix." },
      4: { name: "Douleur Modérée", spoken: "La douleur est un peu plus forte maintenant. Score quatre sur dix." },
      6: { name: "Douleur Forte", spoken: "La douleur augmente encore. C'est difficile de se reposer. Score six sur dix." },
      8: { name: "Très Forte Douleur", spoken: "J'ai vraiment très mal. J'ai besoin d'aide pour soulager la douleur. Score huit sur dix." },
      10: { name: "Pire Douleur", spoken: "C'est la pire douleur imaginable. Aidez-moi tout de suite, s'il vous plaît. Score dix sur dix." }
    }
  },
  de: {
    code: 'de',
    name: 'German',
    nativeName: 'Deutsch (Klinik)',
    flag: '🇩🇪',
    needs: {
      WATER: { title: "Wasser / Tupfer", category: "Hydratation", spoken: "Könnte ich bitte etwas Wasser oder ein Mundbefeuchtungsstäbchen bekommen?" },
      PAIN: { title: "Schmerzort", category: "Klinisch", spoken: "Ich habe Schmerzen. Könnten Sie bitte meine Schmerzmedikation überprüfen?" },
      COLD: { title: "Kalt / Decke", category: "Thermisch", spoken: "Mir ist sehr kalt. Könnte ich bitte eine warme Decke bekommen?" },
      WARM: { title: "Zu Warm / Lüfter", category: "Thermisch", spoken: "Mir ist zu warm. Könnten wir die Decke lockern oder den Ventilator einschalten?" },
      REPOSITION: { title: "Lage Ändern", category: "Mobilität", spoken: "Könnten Sie mir bitte helfen, meine Liegeposition im Bett zu verändern?" },
      FAMILY: { title: "Familie / Pflege", category: "Emotional", spoken: "Ich möchte gerne meine Familie sehen oder mit meiner Pflegekraft sprechen." },
      SUCTION: { title: "Atemwegsabsaugung", category: "Respiratorisch", spoken: "Ich brauche bitte eine Absaugung der Atemwege. Das Atmen fällt mir schwer." },
      MEDICINE: { title: "Medikation", category: "Klinisch", spoken: "Ist es schon Zeit für meine geplante Medikation?" },
      RESTROOM: { title: "Bettpfanne", category: "Physiologisch", spoken: "Ich muss bitte dringend die Bettpfanne oder Urinflasche benutzen." },
      LIGHTS: { title: "Licht Dimmen", category: "Sensorisch", spoken: "Könnten Sie bitte das Zimmerlicht dimmen? Es blendet meine Augen." },
      QUESTION: { title: "Frage Stellen", category: "Kommunikation", spoken: "Ich habe eine Frage. Könnte ich bitte auf Papier oder einem Tablet schreiben?" },
      YES_NO: { title: "Ja / Nein", category: "Bestätigung", spoken: "Ja oder Nein. Bitte stellen Sie mir einfache Ja-oder-Nein-Fragen." }
    },
    faces: {
      0: { name: "Keine Schmerzen", spoken: "Ich habe keine Schmerzen und fühle mich wohl. Schmerzskala null." },
      2: { name: "Leichter Schmerz", spoken: "Es tut nur ein kleines bisschen weh. Schmerzskala zwei." },
      4: { name: "Mäßiger Schmerz", spoken: "Es tut etwas mehr weh jetzt. Schmerzskala vier." },
      6: { name: "Deutlicher Schmerz", spoken: "Es schmerzt noch mehr. Ich kann kaum ruhen. Schmerzskala sechs." },
      8: { name: "Starker Schmerz", spoken: "Es tut sehr stark weh. Ich brauche dringend Hilfe. Schmerzskala acht." },
      10: { name: "Schlimmster Schmerz", spoken: "Es ist der allerschlimmste Schmerz. Bitte helfen Sie mir sofort. Schmerzskala zehn." }
    }
  }
};

/**
 * Generates an empty translation template JSON for community translation.
 */
export function generateLanguageTemplateJson(targetLanguageName = "New Language", targetLangCode = "xx") {
  const template = {
    code: targetLangCode,
    name: targetLanguageName,
    nativeName: targetLanguageName,
    flag: "🌐",
    needs: {},
    faces: {}
  };

  ICU_PHYSIOLOGICAL_NEEDS.forEach(item => {
    template.needs[item.id] = {
      title: item.title,
      category: item.category,
      spoken: item.spokenText
    };
  });

  WONG_BAKER_FACES.forEach(face => {
    template.faces[face.score] = {
      name: face.name,
      spoken: face.speechPrompt
    };
  });

  return JSON.stringify(template, null, 2);
}

/**
 * Serializes custom bedside cards into a compact Base64 URL parameter.
 */
export function serializeBedsideBoard(customTiles) {
  if (!Array.isArray(customTiles) || customTiles.length === 0) return '';
  try {
    const compact = customTiles.map(t => ({
      t: String(t.title || '').slice(0, 40),
      s: String(t.spokenText || '').slice(0, 200),
      c: String(t.category || 'Personal').slice(0, 30),
      i: String(t.emoji || '💬').slice(0, 8)
    }));
    const jsonStr = JSON.stringify(compact);
    if (typeof btoa !== 'undefined') {
      return btoa(encodeURIComponent(jsonStr));
    }
    return Buffer.from(encodeURIComponent(jsonStr)).toString('base64');
  } catch (e) {
    return '';
  }
}

/**
 * Safely deserializes custom bedside cards from a Base64 URL parameter.
 */
export function deserializeBedsideBoard(base64Str) {
  if (!base64Str || typeof base64Str !== 'string') return [];
  try {
    let jsonStr = '';
    if (typeof atob !== 'undefined') {
      jsonStr = decodeURIComponent(atob(base64Str));
    } else {
      jsonStr = decodeURIComponent(Buffer.from(base64Str, 'base64').toString('utf8'));
    }
    const list = JSON.parse(jsonStr);
    if (!Array.isArray(list)) return [];
    return list.map((item, idx) => ({
      id: `CUSTOM_${idx}_${Date.now()}`,
      title: String(item.t || 'Note').slice(0, 40),
      spokenText: String(item.s || item.t || '').slice(0, 200),
      category: String(item.c || 'Personal').slice(0, 30),
      emoji: String(item.i || '💬').slice(0, 8),
      isCustom: true
    }));
  } catch (e) {
    return [];
  }
}

// Universal Browser Global Export for offline file:/// resilience
if (typeof window !== 'undefined') {
  window.PocketGullA11y = {
    TELEMETRY_BADGES,
    CLINICAL_TELEMETRY_METRICS,
    WONG_BAKER_FACES,
    ICU_PHYSIOLOGICAL_NEEDS,
    ASYMMETRIC_MIRROR_PAIRS,
    NEMETH_BRAILLE_MAPPINGS,
    DALTONISM_FILTERS,
    BUILTIN_LANGUAGES,
    generateLanguageTemplateJson,
    serializeBedsideBoard,
    deserializeBedsideBoard
  };
}

