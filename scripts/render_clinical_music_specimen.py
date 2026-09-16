#!/usr/bin/env python3
"""
PocketGull Music: High-Resolution Clinical Music & SMuFL Specimen Renderer
==========================================================================
Renders an ultra-sharp proof plate showcasing PocketGull Music rendering
W3C SMuFL standard music notation, clinical music therapy, and audiology telemetry:
1. W3C SMuFL Standard Staves, Clefs, Noteheads & Barlines
2. Accidentals, Rests & Musical Dynamics
3. Clinical Music Therapy & Cardiac Entrainment Pacing (60 BPM Metronome)
4. Pure-Tone Audiology Telemetry (Air & Bone Conduction Decibel Thresholds)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_MUSIC = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Music.ttf")
FONT_BOLD = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Bold.ttf")
FONT_REGULAR = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Regular.ttf")
OUT_IMG = os.path.join(ROOT_DIR, "documentation", "images", "clinical_music_specimen_plate.png")

def render_music_plate():
    WIDTH, HEIGHT = 2000, 1550
    BG_COLOR = (10, 16, 26)  # Deep clinical slate
    TEXT_WHITE = (248, 250, 252)
    INDIGO_ACCENT = (129, 140, 248)  # #818cf8
    CYAN_ACCENT = (56, 189, 248)
    AMBER_ACCENT = (245, 158, 11)
    ROSE_ACCENT = (244, 63, 94)
    EMERALD_ACCENT = (52, 211, 153)
    MUTED_TEXT = (148, 163, 184)
    CARD_BG = (17, 24, 39)
    CARD_BORDER = (45, 55, 72)

    im = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype(FONT_BOLD, 44)
    font_subtitle = ImageFont.truetype(FONT_REGULAR, 21)
    font_section = ImageFont.truetype(FONT_BOLD, 25)
    font_mus_large = ImageFont.truetype(FONT_MUSIC, 42)
    font_mus_med = ImageFont.truetype(FONT_MUSIC, 30)
    font_meta = ImageFont.truetype(FONT_REGULAR, 17)

    # Header
    draw.text((100, 50), "POCKETGULL MUSIC: CLINICAL MUSIC THERAPY & W3C SMuFL NOTATION", font=font_title, fill=INDIGO_ACCENT)
    draw.text((100, 108), "W3C SMuFL Standard \u2022 Clefs & Noteheads \u2022 Cardiac Vagal Pacing \u2022 Pure-Tone Audiology Telemetry", font=font_subtitle, fill=MUTED_TEXT)
    draw.line([(100, 150), (1900, 150)], fill=CARD_BORDER, width=2)

    cards = [
        {
            "title": "1. W3C SMuFL NOTATION: CLEFS, NOTEHEADS, BARLINES & BEAMS",
            "subtitle": "Standard Music Font Layout PUA codepoints (U+E014-U+E8E0) with 2-byte word alignment",
            "line1": "\ue050  Treble   \ue062  Bass   \ue05c  Alto   \ue030 Bar   \ue031 Dbl   \ue032 Final   \ue040 StartRep   EndRep \ue041",
            "line2": "Noteheads & Beams: \ue0a2 (Whole)  \ue0a3 (Half)  \ue0a4 (Quarter)  \ue0db (Harmonic)  \ue8e0 (Beam Bar)  \ue210 (Stem)",
            "clinical": "SMuFL compliance enables direct interoperability with Dorico, Sibelius, MuseScore, and EHR sound therapy engines.",
            "color": INDIGO_ACCENT,
            "y": 180
        },
        {
            "title": "2. TWO-STORY TIME SIGNATURES, ACCIDENTALS & MUSICAL DYNAMICS",
            "subtitle": "Gould-compliant stacked meters (no slash/fraction bar), common/cut time, and accidentals",
            "line1": "Meters: \ue08a (Common C)   \ue08b (Cut C|)   \ue940 (2/4)   \ue941 (3/4)   \ue942 (4/4)   \ue943 (6/8)   \ue944 (7/8)   \ue947 (12/8)",
            "line2": "Accidentals & Dynamics: \ue261 (Natural)  \ue262 (Sharp)  \ue260 (Flat)  \ue263 (x)  \ue4e5 (Rest)  \ue520 (p)  \ue522 (f)",
            "clinical": "Proper engraving strictly stacks numerals vertically (zero slash/bar); prevents confusion with mathematical fractions.",
            "color": CYAN_ACCENT,
            "y": 480
        },
        {
            "title": "3. CLINICAL MUSIC THERAPY & CARDIAC ENTRAINMENT PACING",
            "subtitle": "Isochronic acoustic anchors for heart rate variability (HRV) and autonomic nervous system regulation",
            "line1": "\ue935  Prescription: Cardiac Entrainment at 60 BPM [Vagal Parasympathetic Activation]",
            "line2": "Neuro-Acoustic EEG Targets: \u03b1 (Alpha 8-13 Hz: Relaxation)  \u03b8 (Theta 4-8 Hz: Hypnagogic Repair)",
            "clinical": "Used in ICU delirium prevention, neonatal soothing, and Parkinson's rhythmic auditory stimulation (RAS).",
            "color": EMERALD_ACCENT,
            "y": 790
        },
        {
            "title": "4. CLINICAL AUDIOLOGY TELEMETRY & HEARING THRESHOLD MAPPING",
            "subtitle": "Pure-tone audiogram symbols conforming to ANSI S3.21 and ISO 8253 diagnostic standards",
            "line1": "Right Ear Air: \ue930 [Red Circle]     Left Ear Air: \ue931 [Blue Cross]     Bone: \ue932 Right  \ue933 Left",
            "line2": "Thresholds: 125 Hz \u2192 8000 Hz, 0 dB HL (Normal Hearing) vs. >70 dB HL (Severe Sensorineural Loss)",
            "clinical": "ANSI S3.21 acoustic standards prevent confusion between conductively masked and unmasked patient responses.",
            "color": ROSE_ACCENT,
            "y": 1090
        }
    ]

    for card in cards:
        y0 = card["y"]
        y1 = y0 + 275
        draw.rounded_rectangle([(100, y0), (1900, y1)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
        draw.rounded_rectangle([(100, y0), (112, y1)], radius=4, fill=card["color"])

        draw.text((140, y0 + 16), card["title"], font=font_section, fill=card["color"])
        draw.text((140, y0 + 48), card["subtitle"], font=font_subtitle, fill=MUTED_TEXT)
        draw.text((140, y0 + 90), card["line1"], font=font_mus_large, fill=TEXT_WHITE)
        draw.text((140, y0 + 155), card["line2"], font=font_mus_med, fill=INDIGO_ACCENT)
        draw.text((140, y0 + 230), f"\u00bb Clinical Context: {card['clinical']}", font=font_meta, fill=(203, 213, 225))

    # Bottom Banner: Specialized Music & Audiology Glyph Set
    draw.rounded_rectangle([(100, 1370), (1900, 1515)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((130, 1385), "SPECIALIZED MUSIC & AUDIOLOGY GLYPH SET:", font=font_section, fill=INDIGO_ACCENT)
    
    sample_symbols = "\ue050  \ue062  \ue05c  \ue030  \ue031  \ue032  \ue040  \ue041  \ue08a  \ue08b  \ue941  \ue942  \ue943  \ue8e0  \ue0a4  \ue0a3  \ue0a2  \ue261  \ue262  \ue260  \ue263  \ue4e5  \ue520  \ue522  \ue935"
    sample_legend = "Treble \u2022 Bass \u2022 Alto \u2022 Barlines (Single, Dbl, Final, Repeats) \u2022 Common & Cut \u2022 Stacked Meters (3/4, 4/4, 6/8) \u2022 Beams \u2022 Notes \u2022 Accidentals \u2022 Rests \u2022 Dynamics \u2022 Metronome"
    draw.text((130, 1425), sample_symbols, font=font_mus_med, fill=TEXT_WHITE)
    draw.text((130, 1475), sample_legend, font=font_meta, fill=MUTED_TEXT)

    os.makedirs(os.path.dirname(OUT_IMG), exist_ok=True)
    im.save(OUT_IMG, "PNG")
    print(f"[OK] Clinical music specimen plate rendered to {OUT_IMG} ({os.path.getsize(OUT_IMG)} bytes)")

if __name__ == "__main__":
    render_music_plate()
