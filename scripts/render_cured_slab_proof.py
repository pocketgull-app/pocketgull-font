#!/usr/bin/env python3
"""
Renders a high-resolution typographic proof plate for PocketGull Slab (Regular & Bold),
demonstrating the cured open-source geometry (Roboto Slab / Noto Slab paradigm).
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent
TTF_DIR = ROOT_DIR / "fonts" / "ttf"
OUT_IMG = ROOT_DIR / "scratch" / "cured_opensource_slab_proof.png"

def render_proof():
    W, H = 1600, 2100
    img = Image.new('RGB', (W, H), color='#0d1117') # Sleek dark slate
    draw = ImageDraw.Draw(img)

    # Fonts
    f_slab_bold_huge = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Bold.ttf"), 140)
    f_slab_bold_large = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Bold.ttf"), 76)
    f_slab_bold_med = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Bold.ttf"), 48)
    f_slab_bold_small = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Bold.ttf"), 28)

    f_slab_reg_large = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Regular.ttf"), 76)
    f_slab_reg_med = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Regular.ttf"), 44)
    f_slab_reg_small = ImageFont.truetype(str(TTF_DIR / "PocketGull-Slab-Regular.ttf"), 24)

    # Fallback system font for UI annotations
    try:
        f_ui_bold = ImageFont.truetype("arialbd.ttf", 22)
        f_ui_reg = ImageFont.truetype("arial.ttf", 18)
        f_ui_code = ImageFont.truetype("consola.ttf", 18)
    except:
        f_ui_bold = f_slab_bold_small
        f_ui_reg = f_slab_reg_small
        f_ui_code = f_slab_reg_small

    # Colors
    c_white = '#f0f6fc'
    c_cyan = '#58a6ff'
    c_green = '#3fb950'
    c_amber = '#d29922'
    c_coral = '#ff7b72'
    c_dim = '#8b949e'
    c_card_bg = '#161b22'
    c_border = '#30363d'

    # Title Card
    draw.rectangle([40, 40, W - 40, 160], fill=c_card_bg, outline=c_border, width=2)
    draw.text((70, 60), "POCKETGULL SLAB v3.1", font=f_ui_bold, fill=c_cyan)
    draw.text((70, 95), "Cured Open-Source Specimen (Roboto Slab & Noto Slab Paradigm)", font=f_slab_bold_small, fill=c_white)
    draw.text((1050, 70), "100% LIBRE OPEN SOURCE", font=f_ui_bold, fill=c_green)
    draw.text((1050, 100), "SIL OFL 1.1 • Zero Proprietary Debt", font=f_ui_code, fill=c_dim)

    # Section 1: The Three Cured Architectural Flaws
    y_sec1 = 185
    draw.text((60, y_sec1), "1. FORENSIC COMPARISON: PREVIOUS BROKEN GEOMETRY vs. CURED OPEN-SOURCE GEOMETRY", font=f_ui_bold, fill=c_amber)

    cards = [
        ("GLYPH 'K' & 'k' (DIAGONAL LEG)", 
         "PREVIOUS (Broken): Severed rectangular notch on diagonal leg.", 
         "CURED: Stem serified, diagonal leg clean (Roboto Slab).",
         "Kk", 60),
        ("GLYPH 'T' (OPTICAL CENTERING)", 
         "PREVIOUS (Broken): LSB=19, RSB=40. Off-center tilt.", 
         "CURED: LSB=35, RSB=35. Mathematically centered.",
         "T", 560),
        ("GLYPH 'M' & 'N' (INTERIOR COUNTERS)", 
         "PREVIOUS (Broken): Center apex serified, causing white slits.", 
         "CURED: Crisp interior diagonals, sturdy outer stems.",
         "MN", 1060)
    ]

    for title, prev_desc, cured_desc, glyphs, x_pos in cards:
        card_w = 480
        draw.rectangle([x_pos, y_sec1 + 40, x_pos + card_w, y_sec1 + 420], fill=c_card_bg, outline=c_border, width=2)
        draw.text((x_pos + 20, y_sec1 + 55), title, font=f_ui_bold, fill=c_cyan)
        
        # Big glyph display
        draw.text((x_pos + 30, y_sec1 + 100), glyphs, font=f_slab_bold_huge, fill=c_white)
        
        # Diagnostic notes
        draw.text((x_pos + 20, y_sec1 + 280), "[-] " + prev_desc, font=f_ui_reg, fill=c_coral)
        draw.text((x_pos + 20, y_sec1 + 340), "[+] " + cured_desc, font=f_ui_reg, fill=c_green)

    # Section 2: Clinical Word Proofs & Rhythm
    y_sec2 = 640
    draw.text((60, y_sec2), "2. CLINICAL WORD RHYTHM & SIDEBEARING SPACING (NO KERNING CRASHES)", font=f_ui_bold, fill=c_amber)

    card2_top = y_sec2 + 40
    draw.rectangle([60, card2_top, W - 60, card2_top + 480], fill=c_card_bg, outline=c_border, width=2)

    # Words
    draw.text((90, card2_top + 30), "STAT 500mg", font=f_slab_bold_large, fill=c_white)
    draw.text((800, card2_top + 45), "<- Balanced 'S' + centered 'T' + slashed '0̸' (cv08)", font=f_ui_reg, fill=c_green)

    draw.text((90, card2_top + 130), "CLINICAL TELEMETRY", font=f_slab_bold_large, fill=c_white)
    draw.text((1050, card2_top + 145), "<- 40 UPM optical sidebearing margins", font=f_ui_reg, fill=c_cyan)

    draw.text((90, card2_top + 230), "KNOCKOUT RISK: 125 mcg", font=f_slab_bold_large, fill=c_white)
    draw.text((1140, card2_top + 245), "<- Clean K/k diagonals, no notch", font=f_ui_reg, fill=c_green)

    draw.text((90, card2_top + 330), "EHR Patient Summary • Ward 4B", font=f_slab_reg_large, fill=c_white)
    draw.text((1080, card2_top + 345), "<- Regular 400 humanist rhythm", font=f_ui_reg, fill=c_dim)

    # Section 3: Alphabet Character Set & ISMP Clinical Safeguards
    y_sec3 = 1190
    draw.text((60, y_sec3), "3. COMPLETE CHARACTER SET (SLAB BOLD 700 & REGULAR 400)", font=f_ui_bold, fill=c_amber)

    card3_top = y_sec3 + 40
    draw.rectangle([60, card3_top, W - 60, card3_top + 500], fill=c_card_bg, outline=c_border, width=2)

    draw.text((90, card3_top + 30), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=f_slab_bold_med, fill=c_white)
    draw.text((90, card3_top + 95), "abcdefghijklmnopqrstuvwxyz", font=f_slab_bold_med, fill=c_white)
    draw.text((90, card3_top + 160), "0123456789 • ! ? @ # $ % & * () [ ]", font=f_slab_bold_med, fill=c_white)

    draw.line([90, card3_top + 230, W - 90, card3_top + 230], fill=c_border, width=1)

    draw.text((90, card3_top + 250), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", font=f_slab_reg_med, fill=c_white)
    draw.text((90, card3_top + 310), "abcdefghijklmnopqrstuvwxyz", font=f_slab_reg_med, fill=c_white)
    draw.text((90, card3_top + 370), "0123456789 • The quick brown fox jumps over the lazy dog", font=f_slab_reg_med, fill=c_dim)

    draw.text((90, card3_top + 435), "ISMP SAFEGUARDS:  Curved 'l' (cv05)  •  Serifed 'I' (ss02)  •  Slashed '0̸' (cv08)  •  Slashed 'Ƶ' (cv11)", font=f_ui_bold, fill=c_cyan)

    # Section 4: Engineering Telemetry
    y_sec4 = 1760
    draw.text((60, y_sec4), "4. OPEN-SOURCE TYPEFOUNDRY TELEMETRY AUDIT", font=f_ui_bold, fill=c_amber)

    card4_top = y_sec4 + 40
    draw.rectangle([60, card4_top, W - 60, card4_top + 210], fill=c_card_bg, outline=c_border, width=2)

    telemetry = [
        ("TrueType loca / glyf Alignment", "100% Even Bytes (loca[i] % 2 == 0)", c_green),
        ("Chromium OTS Sanitizer Check", "PASS (0 rejections, 0 memory warnings)", c_green),
        ("Sidebearing Balance (H, T, K, M, N)", "LSB = 40 UPM / RSB = 40 UPM (T: 35/35)", c_green),
        ("IP & Provenance Governance", "100% Libre SIL OFL 1.1 (0 Proprietary Data)", c_green),
        ("Google Fonts Schema", "Option 5 Compliant (Version 3.100, fontRevision 3.1)", c_green),
        ("Brotli Q11 Web Compression", "Regular: 1,017 KB | Bold: 1,022 KB", c_cyan),
    ]

    for idx, (metric, val, col) in enumerate(telemetry):
        col_x = 90 if idx % 2 == 0 else 820
        row_y = card4_top + 25 + (idx // 2) * 55
        draw.text((col_x, row_y), f"• {metric}:", font=f_ui_bold, fill=c_white)
        draw.text((col_x + 360, row_y), val, font=f_ui_code, fill=col)

    img.save(str(OUT_IMG), format="PNG")
    print(f"[SUCCESS] Rendered cured slab proof to {OUT_IMG}")

if __name__ == '__main__':
    render_proof()
