"""
PocketGull Scientific Color Tokens: IUPAC / CPK Chemistry & AMS / ISO 80000-2 Mathematics
========================================================================================
Formally encoded color palettes derived from international governing bodies:
1. IUPAC / CPK Standard for Crystallography and Molecular Chemistry
2. AMS (American Mathematical Society) & ISO 80000-2 for Mathematical Semantics
"""

# IUPAC / CPK (Corey-Pauling-Koltun) Standard Elemental Color Palette
IUPAC_CPK_PALETTE = {
    "H":  {"name": "Hydrogen",   "hex": "#f4f4f5", "role": "Light/White neutral"},
    "C":  {"name": "Carbon",     "hex": "#27272a", "role": "Graphite organic backbone"},
    "N":  {"name": "Nitrogen",   "hex": "#3b82f6", "role": "Amine/Base blue"},
    "O":  {"name": "Oxygen",     "hex": "#ef4444", "role": "Carbonyl/Hydroxyl red"},
    "F":  {"name": "Fluorine",   "hex": "#22c55e", "role": "Electronegative green"},
    "Cl": {"name": "Chlorine",   "hex": "#10b981", "role": "Halogen green"},
    "Br": {"name": "Bromine",    "hex": "#991b1b", "role": "Deep halogen red"},
    "I":  {"name": "Iodine",     "hex": "#8b5cf6", "role": "Halogen violet"},
    "P":  {"name": "Phosphorus", "hex": "#f97316", "role": "Phosphate/DNA orange"},
    "S":  {"name": "Sulfur",     "hex": "#f59e0b", "role": "Thiol/Disulfide amber"},
    "Fe": {"name": "Iron",       "hex": "#ea580c", "role": "Heme/Ferritin rust"},
    "Ca": {"name": "Calcium",    "hex": "#64748b", "role": "Mineral grey"},
    "Na": {"name": "Sodium",     "hex": "#6366f1", "role": "Alkali violet"},
    "K":  {"name": "Potassium",  "hex": "#a855f7", "role": "Alkali purple"}
}

# AMS / ISO 80000-2 Mathematical Semantic Hierarchy
AMS_ISO_MATH_PALETTE = {
    "scalars":     {"name": "Real Variables",    "hex": "#0ea5e9", "symbols": ["x", "y", "t", "u", "v"]},
    "discrete":    {"name": "Discrete Sets/N",   "hex": "#10b981", "symbols": ["k", "n", "m", "i", "j"]},
    "operators":   {"name": "Active Transforms", "hex": "#f59e0b", "symbols": ["\\sum", "\\int", "\\nabla", "\\partial"]},
    "invariants":  {"name": "Universal Consts",  "hex": "#a855f7", "symbols": ["\\pi", "e", "c", "\\hbar"]},
    "complex":     {"name": "Imaginary Domain",  "hex": "#ec4899", "symbols": ["i", "z", "\\mathbb{C}"]},
    "relations":   {"name": "Order/Equivalence", "hex": "#64748b", "symbols": ["=", "\\le", "\\ge", "\\in", "\\subset"]}
}

# Piano ROYGBIV Spectral Solfège Palette (Chroma-Notes / Scriabin Standard)
PIANO_ROYGBIV_PALETTE = {
    "C": {"note": "C", "solfege": "Do", "color_name": "Red",    "hex": "#ef4444", "midi_offset": 0, "role": "Tonic root anchor (Middle C)"},
    "D": {"note": "D", "solfege": "Re", "color_name": "Orange", "hex": "#f97316", "midi_offset": 2, "role": "Supertonic step upward"},
    "E": {"note": "E", "solfege": "Mi", "color_name": "Yellow", "hex": "#eab308", "midi_offset": 4, "role": "Mediant bright harmonic lift"},
    "F": {"note": "F", "solfege": "Fa", "color_name": "Green",  "hex": "#10b981", "midi_offset": 5, "role": "Subdominant organic resolution"},
    "G": {"note": "G", "solfege": "Sol", "color_name": "Blue",   "hex": "#3b82f6", "midi_offset": 7, "role": "Dominant expansive clarity"},
    "A": {"note": "A", "solfege": "La", "color_name": "Indigo", "hex": "#6366f1", "midi_offset": 9, "role": "Submediant Concert A440 resonance"},
    "B": {"note": "B", "solfege": "Ti", "color_name": "Violet", "hex": "#a855f7", "midi_offset": 11, "role": "Leading tone energetic return"}
}

def get_iupac_color(symbol: str) -> str:
    """Returns the authoritative IUPAC/CPK hex color for an element symbol."""
    elem = IUPAC_CPK_PALETTE.get(symbol)
    return elem["hex"] if elem else "#71717a"

def get_math_token_color(category: str) -> str:
    """Returns the AMS/ISO 80000-2 hex color for a mathematical semantic class."""
    cat = AMS_ISO_MATH_PALETTE.get(category)
    return cat["hex"] if cat else "#71717a"

def get_piano_note_color(note_name: str) -> str:
    """Returns the ROYGBIV hex color for a natural piano note (C..B)."""
    clean_note = note_name.upper().strip()[0] if note_name else ""
    token = PIANO_ROYGBIV_PALETTE.get(clean_note)
    return token["hex"] if token else "#71717a"

# Traffic Light Temporal / Duration Flow Palette
TRAFFIC_LIGHT_TEMPO_PALETTE = {
    "green":  {"phase": "Attack & Flow", "hex": "#10b981", "duty_cycle": "0-50%",   "role": "Active stroke, onset, acoustic resonance"},
    "amber":  {"phase": "Sustain Hold",  "hex": "#f59e0b", "duty_cycle": "50-85%",  "role": "Weight transfer, physical relaxation, prepare release"},
    "red":    {"phase": "Rest / Release","hex": "#ef4444", "duty_cycle": "85-100%", "role": "Damper drop, complete silence, boundary reset"}
}

def get_traffic_light_phase_color(phase_name: str) -> str:
    """Returns the chromatic signal color for a musical duration phase."""
    token = TRAFFIC_LIGHT_TEMPO_PALETTE.get(phase_name.lower().strip())
    return token["hex"] if token else "#71717a"

# Daltonism & Color Vision Deficiency (CVD) Brettel/Vienot Matrix Transformations
DALTONISM_SIMULATION_MATRICES = {
    "protanopia": [
        [0.56667, 0.43333, 0.0],
        [0.55833, 0.44167, 0.0],
        [0.0,     0.24167, 0.75833]
    ],
    "deuteranopia": [
        [0.625, 0.375, 0.0],
        [0.70,  0.30,  0.0],
        [0.0,   0.30,  0.70]
    ],
    "tritanopia": [
        [0.95, 0.05,  0.0],
        [0.0,  0.433, 0.567],
        [0.0,  0.475, 0.525]
    ],
    "monochromacy": [
        [0.2126, 0.7152, 0.0722],
        [0.2126, 0.7152, 0.0722],
        [0.2126, 0.7152, 0.0722]
    ]
}

def simulate_cvd_color(hex_color: str, deficiency: str) -> str:
    """Simulates perceived RGB color under Protanopia, Deuteranopia, Tritanopia, or Monochromacy."""
    mode = deficiency.lower().strip()
    if mode == "normal" or mode not in DALTONISM_SIMULATION_MATRICES:
        return hex_color
    
    clean_hex = hex_color.lstrip("#")
    if len(clean_hex) != 6:
        return hex_color
        
    r = int(clean_hex[0:2], 16) / 255.0
    g = int(clean_hex[2:4], 16) / 255.0
    b = int(clean_hex[4:6], 16) / 255.0
    
    matrix = DALTONISM_SIMULATION_MATRICES[mode]
    sim_r = min(1.0, max(0.0, r * matrix[0][0] + g * matrix[0][1] + b * matrix[0][2]))
    sim_g = min(1.0, max(0.0, r * matrix[1][0] + g * matrix[1][1] + b * matrix[1][2]))
    sim_b = min(1.0, max(0.0, r * matrix[2][0] + g * matrix[2][1] + b * matrix[2][2]))
    
    return f"#{int(round(sim_r * 255)):02x}{int(round(sim_g * 255)):02x}{int(round(sim_b * 255)):02x}"

def get_daltonism_piano_palette(deficiency: str) -> dict:
    """Generates an entire simulated 7-note solfège palette for a specified color vision deficiency."""
    palette = {}
    for note, data in PIANO_ROYGBIV_PALETTE.items():
        palette[note] = {
            "note": data["note"],
            "solfege": data["solfege"],
            "original_hex": data["hex"],
            "simulated_hex": simulate_cvd_color(data["hex"], deficiency)
        }
    return palette

# Audio Engineering & Acoustic Space Standards (EBU R128 / ITU-R BS.1770)
AUDIO_LUFS_METRIC_TOKENS = {
    "safe_target": {
        "lufs": -14.0,
        "name": "Integrated Streaming Target",
        "hex": "#10b981",  # Emerald
        "daltonic_symbol": "◎",
        "protanopia_safe_hex": "#38bdf8",
        "role": "Optimal streaming normalization (Spotify, Apple Music, YouTube)"
    },
    "nominal_caution": {
        "lufs": -9.0,
        "name": "Club / Broadcast High Density",
        "hex": "#f59e0b",  # Amber
        "daltonic_symbol": "▲",
        "protanopia_safe_hex": "#facc15",
        "role": "Loud mastering threshold with limited dynamic range"
    },
    "true_peak_clip": {
        "lufs": 0.0,
        "name": "Inter-Sample True Peak Clip Risk",
        "hex": "#ef4444",  # Red
        "daltonic_symbol": "⨂",
        "protanopia_safe_hex": "#ec4899",
        "role": "DAC reconstruction distortion and ISP boundary violation"
    }
}

ACOUSTIC_FREQUENCY_BANDS = {
    "sub_bass":  {"range_hz": "20 - 60 Hz",   "hex": "#6366f1", "role": "Sub-woofer visceral rumble"},
    "bass":      {"range_hz": "60 - 250 Hz",  "hex": "#3b82f6", "role": "Rhythmic warmth & kick fundamental"},
    "low_mids":  {"range_hz": "250 - 500 Hz", "hex": "#10b981", "role": "Vocal body & acoustic guitar resonance"},
    "mids":      {"range_hz": "500 - 2 kHz",  "hex": "#f59e0b", "role": "Speech intelligibility & snare snap"},
    "presence":  {"range_hz": "2k - 6 kHz",   "hex": "#f97316", "role": "Ear canal sensitivity & vocal clarity"},
    "brilliance":{"range_hz": "6k - 20 kHz",  "hex": "#a855f7", "role": "Air, cymbals, acoustic shimmer"}
}

def get_audio_lufs_color(lufs_value: float, cvd_mode: str = "normal") -> dict:
    """Returns accessible color and symbol for a given LUFS measurement."""
    if lufs_value > -1.0:
        token = AUDIO_LUFS_METRIC_TOKENS["true_peak_clip"]
    elif lufs_value > -12.0:
        token = AUDIO_LUFS_METRIC_TOKENS["nominal_caution"]
    else:
        token = AUDIO_LUFS_METRIC_TOKENS["safe_target"]
    
    color = token["hex"]
    if cvd_mode.lower() in ["protanopia", "deuteranopia"]:
        color = token["protanopia_safe_hex"]
    elif cvd_mode.lower() == "monochromacy":
        color = "#ffffff" if lufs_value > -1.0 else "#94a3b8"
        
    return {
        "hex": color,
        "symbol": token["daltonic_symbol"],
        "name": token["name"],
        "role": token["role"]
    }

# ==============================================================================
# Astrometric Solar System & Ephemeris Palette (IAU Physical Standards)
# ==============================================================================
SOLAR_SYSTEM_PALETTE = {
    "sol": {
        "name": "Sol (Sun)",
        "symbol": "☉",
        "unicode": "U+2299",
        "hex": "#fbbf24",
        "mass_earth": 333000.0,
        "radius_km": "695,700",
        "semi_major_au": 0.0,
        "period_yr": "—",
        "spectral_class": "G2V Yellow Dwarf",
        "role": "Barycentric origin (0,0,0) and heliospheric radiation source."
    },
    "mercury": {
        "name": "Mercury",
        "symbol": "☿",
        "unicode": "U+263F",
        "hex": "#94a3b8",
        "mass_earth": 0.055,
        "radius_km": "2,440",
        "semi_major_au": 0.387,
        "period_yr": "0.24",
        "spectral_class": "Basaltic Terrestrial",
        "role": "Innermost high-velocity perihelion anchor."
    },
    "venus": {
        "name": "Venus",
        "symbol": "♀",
        "unicode": "U+2640",
        "hex": "#fef08a",
        "mass_earth": 0.815,
        "radius_km": "6,052",
        "semi_major_au": 0.723,
        "period_yr": "0.62",
        "spectral_class": "Dense Supercritical Atmosphere",
        "role": "High-albedo greenhouse optical reference."
    },
    "earth": {
        "name": "Earth",
        "symbol": "⊕",
        "unicode": "U+2295",
        "hex": "#38bdf8",
        "mass_earth": 1.000,
        "radius_km": "6,371",
        "semi_major_au": 1.000,
        "period_yr": "1.00",
        "spectral_class": "Hydrosphere Silicate",
        "role": "Standard ephemeris baseline (1.000 AU = 149.6M km)."
    },
    "luna": {
        "name": "Luna (Moon)",
        "symbol": "☽",
        "unicode": "U+263D",
        "hex": "#e2e8f0",
        "mass_earth": 0.0123,
        "radius_km": "1,737",
        "semi_major_au": 0.00257,
        "period_yr": "0.075",
        "spectral_class": "Silicate Anorthosite",
        "role": "Tidal cadence and lunar laser ranging fiducial."
    },
    "mars": {
        "name": "Mars",
        "symbol": "♂",
        "unicode": "U+2642",
        "hex": "#ef4444",
        "mass_earth": 0.107,
        "radius_km": "3,390",
        "semi_major_au": 1.524,
        "period_yr": "1.88",
        "spectral_class": "Ferric Oxide Regolith",
        "role": "Outer terrestrial orbit and atmospheric threshold."
    },
    "jupiter": {
        "name": "Jupiter",
        "symbol": "♃",
        "unicode": "U+2643",
        "hex": "#f97316",
        "mass_earth": 317.8,
        "radius_km": "69,911",
        "semi_major_au": 5.204,
        "period_yr": "11.86",
        "spectral_class": "Gas Giant (H/He)",
        "role": "Solar system barycenter driver and Jovian shield."
    },
    "saturn": {
        "name": "Saturn",
        "symbol": "♄",
        "unicode": "U+2644",
        "hex": "#eab308",
        "mass_earth": 95.16,
        "radius_km": "58,232",
        "semi_major_au": 9.582,
        "period_yr": "29.46",
        "spectral_class": "Ringed Gas Giant",
        "role": "Low-density oblateness and ring telemetry standard."
    },
    "uranus": {
        "name": "Uranus",
        "symbol": "♅",
        "unicode": "U+2645",
        "hex": "#2dd4bf",
        "mass_earth": 14.54,
        "radius_km": "25,362",
        "semi_major_au": 19.20,
        "period_yr": "84.01",
        "spectral_class": "Methane Ice Giant",
        "role": "Extreme axial tilt (97.8°) retrograde baseline."
    },
    "neptune": {
        "name": "Neptune",
        "symbol": "♆",
        "unicode": "U+2646",
        "hex": "#3b82f6",
        "mass_earth": 17.15,
        "radius_km": "24,622",
        "semi_major_au": 30.05,
        "period_yr": "164.8",
        "spectral_class": "Dynamic Deep Azure Atmosphere",
        "role": "Trans-Neptunian orbital resonance boundary."
    },
    "pluto": {
        "name": "Pluto",
        "symbol": "♇",
        "unicode": "U+2647",
        "hex": "#c084fc",
        "mass_earth": 0.0022,
        "radius_km": "1,188",
        "semi_major_au": 39.48,
        "period_yr": "247.9",
        "spectral_class": "Nitrogen Ice Dwarf",
        "role": "Kuiper belt resonant archetype (3:2 Neptune lock)."
    }
}

def get_solar_body_data(key: str, cvd_mode: str = "normal") -> dict:
    """Returns astrometric specifications and CVD-simulated color for a solar system body."""
    body = SOLAR_SYSTEM_PALETTE.get(key.lower(), SOLAR_SYSTEM_PALETTE["earth"])
    sim_hex = simulate_cvd_color(body["hex"], cvd_mode)
    return {
        **body,
        "simulated_hex": sim_hex
    }





