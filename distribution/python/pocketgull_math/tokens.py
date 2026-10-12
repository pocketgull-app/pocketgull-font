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



