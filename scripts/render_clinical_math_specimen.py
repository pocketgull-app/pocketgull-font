#!/usr/bin/env python3
"""
PocketGull Math: High-Resolution Clinical Equation Specimen Renderer
====================================================================
Renders a visual proof plate showcasing PocketGull Math rendering
life-critical mathematical equations:
1. Two-Compartment Pharmacokinetic Bolus Decay
2. CKD-EPI eGFR Clinical Renal Clearance Formula
3. Michaelis-Menten Enzymatic Drug Saturation
4. Henderson-Hasselbalch Arterial Blood Gas Equilibrium
5. Blackboard Bold Sets & Logic Quantifiers (R, N, Z, C, in, forall, exists)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_MATH = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Math.ttf")
FONT_BOLD = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Bold.ttf")
FONT_REGULAR = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Regular.ttf")
OUT_IMG = os.path.join(ROOT_DIR, "documentation", "images", "clinical_math_specimen_plate.png")

def render_math_plate():
    WIDTH, HEIGHT = 2000, 1500
    BG_COLOR = (11, 15, 25)  # Clinical dark slate (#0B0F19)
    TEXT_WHITE = (248, 250, 252)
    CYAN_ACCENT = (56, 189, 248)
    AMBER_ACCENT = (245, 158, 11)
    EMERALD_ACCENT = (16, 185, 129)
    MUTED_TEXT = (148, 163, 184)
    CARD_BG = (22, 29, 47)
    CARD_BORDER = (45, 55, 72)

    im = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype(FONT_BOLD, 46)
    font_subtitle = ImageFont.truetype(FONT_REGULAR, 22)
    font_section = ImageFont.truetype(FONT_BOLD, 26)
    font_eq_large = ImageFont.truetype(FONT_MATH, 34)
    font_eq_med = ImageFont.truetype(FONT_MATH, 28)
    font_meta = ImageFont.truetype(FONT_REGULAR, 18)

    # Header
    draw.text((100, 60), "POCKETGULL MATH: CLINICAL OPENTYPE MATHEMATICS", font=font_title, fill=CYAN_ACCENT)
    draw.text((100, 120), "ISO/IEC 14496-22 MATH Table • AxisHeight = 260 UPM • W = 68 UPM Stem Weight • ISMP Life-Critical Precision", font=font_subtitle, fill=MUTED_TEXT)
    draw.line([(100, 165), (1900, 165)], fill=CARD_BORDER, width=2)

    # 4 Formula Cards
    cards = [
        {
            "title": "1. TWO-COMPARTMENT PHARMACOKINETIC BOLUS DECAY (PK/PD)",
            "subtitle": "First-order absorption and elimination with guaranteed decimal spacing",
            "equation": "C_p(t) = [ D · k_a / (V_d · (k_a − k_e)) ] · ( e^(−k_e · t) − e^(−k_a · t) )",
            "clinical": "Target therapeutic window: C_max ≤ 1.25 mcg/mL, t_1/2 = 4.2 h. ISMP Slashed Zero active.",
            "color": CYAN_ACCENT,
            "y": 200
        },
        {
            "title": "2. CKD-EPI RENAL CREATININE CLEARANCE / eGFR FORMULA",
            "subtitle": "Continuous piecewise dosage adjustment for life-critical nephrotoxic drugs",
            "equation": "eGFR = 142 · min(S_cr / κ, 1)^α · max(S_cr / κ, 1)^(−1.200) · 0.9938^Age · [1.012 if ♀]",
            "clinical": "Vancomycin titration: If eGFR < 30 mL/min/1.73m², extend dosing interval from 12h to 24h.",
            "color": EMERALD_ACCENT,
            "y": 480
        },
        {
            "title": "3. MICHAELIS-MENTEN SATURATION KINETICS & CALCULUS",
            "subtitle": "Non-linear hepatic enzymatic clearance with differential operators",
            "equation": "v = (V_max · [S]) / (K_m + [S])    and    dC/dt = − (V_max · C) / (K_m + C)",
            "clinical": "Phenytoin zero-order transition: small dosage increases yield disproportionate toxic serum spikes.",
            "color": AMBER_ACCENT,
            "y": 760
        },
        {
            "title": "4. HENDERSON-HASSELBALCH ARTERIAL BLOOD GAS (ABG) EQUILIBRIUM",
            "subtitle": "Logarithmic bicarbonate-carbonic acid ratio in acute metabolic acidosis",
            "equation": "pH = pK_a + log_10 ( [HCO_3^−] / [α · P_aCO_2] )    where  α = 0.0307 mmol/(L · mmHg)",
            "clinical": "ICU Ventilator Management: Normal arterial target pH = 7.35 − 7.45, P_aCO_2 = 35 − 45 mmHg.",
            "color": (236, 72, 153),  # Rose
            "y": 1040
        }
    ]

    for card in cards:
        y0 = card["y"]
        y1 = y0 + 240
        # Rounded card background
        draw.rounded_rectangle([(100, y0), (1900, y1)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
        # Accent indicator
        draw.rounded_rectangle([(100, y0), (112, y1)], radius=4, fill=card["color"])

        draw.text((140, y0 + 20), card["title"], font=font_section, fill=card["color"])
        draw.text((140, y0 + 58), card["subtitle"], font=font_subtitle, fill=MUTED_TEXT)
        draw.text((140, y0 + 105), card["equation"], font=font_eq_large, fill=TEXT_WHITE)
        draw.text((140, y0 + 185), f"▶ Clinical Safety Context: {card['clinical']}", font=font_meta, fill=(203, 213, 225))

    # Bottom Banner: Mathematical Logic, Operators, and Blackboard Bold
    draw.rounded_rectangle([(100, 1320), (1900, 1440)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((140, 1340), "NATIVE OPERATORS & BLACKBOARD BOLD:", font=font_section, fill=CYAN_ACCENT)
    symbols_line = "+  −  ×  ÷  =  ≠  ≈  ≤  ≥  ∫  ∬  ∑  ∏  ∂  ∇  √  ∞  ∈  ∉  ⊂  ∪  ∩  ∀  ∃  →  ←  ⇒   |   R  N  Z  C"
    draw.text((140, 1380), symbols_line, font=font_eq_large, fill=TEXT_WHITE)

    os.makedirs(os.path.dirname(OUT_IMG), exist_ok=True)
    im.save(OUT_IMG, "PNG")
    print(f"[SUCCESS] Exported clinical math specimen plate to: {OUT_IMG}")

if __name__ == "__main__":
    render_math_plate()
