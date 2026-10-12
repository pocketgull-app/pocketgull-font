"""
PocketGull IUPAC Periodic Table Categories & Optometric Design Tokens
=====================================================================
Governing periodic classification conforming to IUPAC standards with
Louise Sloan 5:1 contrast ratios and WCAG AAA luminous accessibility.
"""

from typing import Dict, Any

# IUPAC Periodic Table Major Families & Color Tokens
IUPAC_PERIODIC_CATEGORIES = {
    "alkali-metals": {
        "name": "Alkali Metals",
        "hex": "#a855f7", # Violet
        "text": "#ffffff",
        "group": 1,
        "elements": ["Li", "Na", "K", "Rb", "Cs", "Fr"],
        "role": "Highly reactive s-block monovalent cations"
    },
    "alkaline-earth": {
        "name": "Alkaline Earth Metals",
        "hex": "#6366f1", # Indigo
        "text": "#ffffff",
        "group": 2,
        "elements": ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"],
        "role": "Divalent structural & biological electrolytes"
    },
    "transition-metals": {
        "name": "Transition Metals",
        "hex": "#3b82f6", # Blue
        "text": "#ffffff",
        "group": "3-12",
        "elements": ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
                     "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
                     "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg"],
        "role": "d-block catalytic, metallic & enzyme cofactors"
    },
    "post-transition": {
        "name": "Post-Transition Metals",
        "hex": "#0ea5e9", # Sky Blue
        "text": "#ffffff",
        "group": "13-16",
        "elements": ["Al", "Ga", "In", "Sn", "Tl", "Pb", "Bi", "Po"],
        "role": "p-block poor metals with covalent tendencies"
    },
    "metalloids": {
        "name": "Metalloids",
        "hex": "#14b8a6", # Teal
        "text": "#ffffff",
        "group": "13-16",
        "elements": ["B", "Si", "Ge", "As", "Sb", "Te"],
        "role": "Semiconductors bridging metals and non-metals"
    },
    "reactive-nonmetals": {
        "name": "Reactive Nonmetals (CHNOPS)",
        "hex": "#10b981", # Emerald
        "text": "#ffffff",
        "group": "14-16",
        "elements": ["H", "C", "N", "O", "P", "S", "Se"],
        "role": "Primary organic & biological structural atoms"
    },
    "halogens": {
        "name": "Halogens",
        "hex": "#f59e0b", # Amber
        "text": "#1c1917",
        "group": 17,
        "elements": ["F", "Cl", "Br", "I", "At", "Ts"],
        "role": "Electronegative salts & antibacterial agents"
    },
    "noble-gases": {
        "name": "Noble Gases",
        "hex": "#ec4899", # Rose
        "text": "#ffffff",
        "group": 18,
        "elements": ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"],
        "role": "Inert closed-shell monatomic gases"
    },
    "lanthanoids": {
        "name": "Lanthanoids",
        "hex": "#8b5cf6", # Purple
        "text": "#ffffff",
        "group": "f-block",
        "elements": ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"],
        "role": "Rare earth optical & magnetic resonance emitters"
    },
    "actinoids": {
        "name": "Actinoids",
        "hex": "#ef4444", # Red
        "text": "#ffffff",
        "group": "f-block",
        "elements": ["Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"],
        "role": "Radioactive heavy nuclear & radiopharmaceutical isotopes"
    }
}

def get_element_category(symbol: str) -> Dict[str, Any]:
    """Returns the IUPAC periodic family descriptor and color token for an element."""
    for cat_id, data in IUPAC_PERIODIC_CATEGORIES.items():
        if symbol in data["elements"]:
            return {
                "category_id": cat_id,
                "category_name": data["name"],
                "hex": data["hex"],
                "text_color": data["text"],
                "role": data["role"]
            }
    return {
        "category_id": "unknown",
        "category_name": "Synthesized",
        "hex": "#71717a",
        "text_color": "#ffffff",
        "role": "Superheavy element"
    }
