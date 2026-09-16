#!/usr/bin/env python3
"""
PocketGull Chem: High-Resolution Clinical Chemistry & Stereochemistry Specimen Renderer
========================================================================================
Renders an ultra-sharp proof plate showcasing PocketGull Chem rendering
life-critical chemical formulas, stereochemical enantiomers, reaction dynamics,
and radiopharmaceutical nuclide notations:
1. Chiral Stereochemistry & Teratogenic Disambiguation (Thalidomide R vs S)
2. Radiopharmaceuticals & 4-Quadrant Nuclide Box (Technetium-99m, Iodine-131)
3. Blood Gas Buffer & Acid-Base Equilibrium Dynamics (Bicarbonate Buffer)
4. Aromatic Pharmacophores & Enzyme Kinetics (Aspirin & COX-1/2 Delocalized Ring)
5. Archetypal Stereochemical Bonds & Harpoon Reaction Arrows
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_CHEM = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Chem.ttf")
FONT_BOLD = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Bold.ttf")
FONT_REGULAR = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Regular.ttf")
OUT_IMG = os.path.join(ROOT_DIR, "documentation", "images", "clinical_chem_specimen_plate.png")

def render_chem_plate():
    WIDTH, HEIGHT = 2000, 1550
    BG_COLOR = (10, 16, 26)  # Deep clinical slate (#0A101A)
    TEXT_WHITE = (248, 250, 252)
    EMERALD_ACCENT = (52, 211, 153)  # #34d399
    CYAN_ACCENT = (56, 189, 248)
    AMBER_ACCENT = (245, 158, 11)
    ROSE_ACCENT = (244, 63, 94)
    MUTED_TEXT = (148, 163, 184)
    CARD_BG = (17, 24, 39)
    CARD_BORDER = (45, 55, 72)

    im = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype(FONT_BOLD, 44)
    font_subtitle = ImageFont.truetype(FONT_REGULAR, 21)
    font_section = ImageFont.truetype(FONT_BOLD, 25)
    font_chem_large = ImageFont.truetype(FONT_CHEM, 36)
    font_chem_med = ImageFont.truetype(FONT_CHEM, 28)
    font_meta = ImageFont.truetype(FONT_REGULAR, 17)

    # Header
    draw.text((100, 50), "POCKETGULL CHEM: CLINICAL PHARMACOLOGY & MOLECULAR TYPEFACE", font=font_title, fill=EMERALD_ACCENT)
    draw.text((100, 108), "Stereochemical Wedges • 4-Quadrant Nuclides • Dynamic Equilibrium Harpoons • ISMP Disambiguated", font=font_subtitle, fill=MUTED_TEXT)
    draw.line([(100, 150), (1900, 150)], fill=CARD_BORDER, width=2)

    # 4 Clinical Chemistry Cards
    cards = [
        {
            "title": "1. CHIRAL STEREOCHEMISTRY & TERATOGENIC SEPARATION",
            "subtitle": "Solid & hashed wedged bonds prevent catastrophic optical confusion between enantiomers",
            "formula": "(R)-Thalidomide [Sedative]  vs.  (S)-Thalidomide [Teratogen: Phocomelia Risk]",
            "bonds": "C\u25C0NH\u2082  [Solid Wedge Outward]     C \ue902 OH  [Hashed Wedge Inward Receding]",
            "clinical": "Racemizes in vivo (t_1/2 = 4.5 h). Preserves Louise Sloan 5:1 optical proportion for pregnancy warnings.",
            "color": ROSE_ACCENT,
            "y": 180
        },
        {
            "title": "2. RADIOPHARMACEUTICAL DOSIMETRY & 4-QUADRANT NUCLIDE BOX",
            "subtitle": "Elevated atomic mass numbers and distinct nuclear metastable states (preventing 10-fold dose spikes)",
            "formula": "\u2079\u2079\u1d50\u2084\u2083Tc  [Technetium-99m: 140.5 keV \u03b3, T_\u00bd = 6.01 h]   \u2192   \u2079\u2079\u2084\u2083Tc + \u03b3",
            "bonds": "\u00b9\u00b3\u00b9\u2085\u2083I  [Iodine-131 Ablation: \u03b2\u207b + \u03b3, 8.02 d]   and   \u00b9\u2078\u2089F-FDG [PET Scan: \u03b2\u207a, 109.8 min]",
            "clinical": "Clear quadrant separation eliminates bridging between atomic number Z, nucleon number A, and ionic charge.",
            "color": CYAN_ACCENT,
            "y": 480
        },
        {
            "title": "3. BLOOD GAS HOMEOSTASIS & LE CHATELIER EQUILIBRIUM DYNAMICS",
            "subtitle": "Paired asymmetric harpoons distinguish reactant-favored vs. product-favored pulmonary buffering",
            "formula": "CO\u2082 (g)\u2191 + H\u2082O (l)   \u21cc   H\u2082CO\u2083 (aq)   \u21cc   HCO\u2083\u207b (aq) + H\u207a (aq)",
            "bonds": "Hyperventilation Shift:  H\u207a + HCO\u2083\u207b  \ue907  CO\u2082\u2191 + H\u2082O  [Left-Favored Exhalation]",
            "clinical": "Arterial Blood Gas (ABG): Normal HCO\u2083\u207b = 22\u221226 mEq/L. Dissociation constants locked to 1000 UPM axis.",
            "color": AMBER_ACCENT,
            "y": 780
        },
        {
            "title": "4. AROMATIC PHARMACOPHORES & ENZYMATIC ACTIVE SITES",
            "subtitle": "Benzene ring with delocalized aromatic circle and coordination dative covalent bonds",
            "formula": "C\u2086H\u2084(OCOCH\u2083)COOH  [Aspirin / Acetylsalicylic Acid]   \u27F9   \u2B21-Ring Disconnection",
            "bonds": "Coordination Complex:  Fe\u00b2\u207a \ue903 O\u2082  [Oxyhemoglobin]  vs.  Fe\u00b2\u207a \ue903 CO  [Carboxyhemoglobin, 200\u00d7 Affinity]",
            "clinical": "Dative coordination arrows differentiate competitive carbon monoxide asphyxiation from oxygen delivery.",
            "color": EMERALD_ACCENT,
            "y": 1080
        }
    ]

    for card in cards:
        y0 = card["y"]
        y1 = y0 + 265
        # Card outline & background
        draw.rounded_rectangle([(100, y0), (1900, y1)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
        # Colored left indicator bar
        draw.rounded_rectangle([(100, y0), (112, y1)], radius=4, fill=card["color"])

        draw.text((140, y0 + 18), card["title"], font=font_section, fill=card["color"])
        draw.text((140, y0 + 52), card["subtitle"], font=font_subtitle, fill=MUTED_TEXT)
        draw.text((140, y0 + 95), card["formula"], font=font_chem_large, fill=TEXT_WHITE)
        draw.text((140, y0 + 155), card["bonds"], font=font_chem_med, fill=EMERALD_ACCENT)
        draw.text((140, y0 + 215), f"\u00bb Clinical Context: {card['clinical']}", font=font_meta, fill=(203, 213, 225))

    # Bottom Banner: Specialized Chemical Glyphs & Enantiomer Badges
    draw.rounded_rectangle([(100, 1380), (1900, 1500)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((130, 1400), "SPECIALIZED CLINICAL CHEMISTRY GLYPH SET:", font=font_section, fill=EMERALD_ACCENT)
    
    sample_symbols = "\u25C0  \u25B6  \ue902  \ue903  \ue904  \u2B21  \u21CC  \ue906  \ue907  \u27F7  \u27F9  \u2193  \u2191  \u2021  \u00B0  \ue909  \ue90A  \ue90B  \ue90C"
    sample_legend = "Solid Wedge \u2022 Hashed Wedge \u2022 Dative Bond \u2022 H-Bond \u2022 Benzene \u2022 Harpoons \u2022 Resonance \u2022 Precipitate \u2022 Gas \u2022 (R)/(S)/(E)/(Z)"
    draw.text((130, 1440), sample_symbols, font=font_chem_med, fill=TEXT_WHITE)
    draw.text((850, 1445), sample_legend, font=font_meta, fill=MUTED_TEXT)

    os.makedirs(os.path.dirname(OUT_IMG), exist_ok=True)
    im.save(OUT_IMG, "PNG")
    print(f"[OK] Clinical chemistry specimen plate rendered to {OUT_IMG} ({os.path.getsize(OUT_IMG)} bytes)")

if __name__ == "__main__":
    render_chem_plate()
