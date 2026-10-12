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

def get_iupac_color(symbol: str) -> str:
    """Returns the authoritative IUPAC/CPK hex color for an element symbol."""
    elem = IUPAC_CPK_PALETTE.get(symbol)
    return elem["hex"] if elem else "#71717a"

def get_math_token_color(category: str) -> str:
    """Returns the AMS/ISO 80000-2 hex color for a mathematical semantic class."""
    cat = AMS_ISO_MATH_PALETTE.get(category)
    return cat["hex"] if cat else "#71717a"
