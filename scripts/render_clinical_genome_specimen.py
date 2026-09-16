#!/usr/bin/env python3
"""
PocketGull Genome: High-Resolution Clinical Genomics Specimen Renderer
======================================================================
Renders an ultra-sharp proof plate showcasing PocketGull Genome rendering
life-critical bioinformatics sequences, NGS alignments, CRISPR-Cas9 cleavage,
and cytogenetic karyotype notations:
1. CRISPR-Cas9 Targeted Gene Editing at HBB (Sickle Cell Locus)
2. NGS / Sanger Multiline Read Alignment with Zero Horizontal Drift
3. IUPAC Degenerate Ambiguity Codes & Hydrogen Bond Pairing
4. Cytogenetics & Chromosomal Translocations (Philadelphia Chromosome t(9;22))
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_GENOME = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Genome.ttf")
FONT_BOLD = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Bold.ttf")
FONT_REGULAR = os.path.join(ROOT_DIR, "fonts", "ttf", "PocketGull-Regular.ttf")
OUT_IMG = os.path.join(ROOT_DIR, "documentation", "images", "clinical_genome_specimen_plate.png")

def render_genome_plate():
    WIDTH, HEIGHT = 2000, 1550
    BG_COLOR = (10, 16, 26)  # Deep clinical slate
    TEXT_WHITE = (248, 250, 252)
    TEAL_ACCENT = (45, 212, 191)   # #2dd4bf
    CYAN_ACCENT = (56, 189, 248)   # #38bdf8
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
    font_seq_large = ImageFont.truetype(FONT_GENOME, 34)
    font_seq_med = ImageFont.truetype(FONT_GENOME, 28)
    font_meta = ImageFont.truetype(FONT_REGULAR, 17)

    # Header
    draw.text((100, 50), "POCKETGULL GENOME: CLINICAL GENOMICS & BIOINFORMATICS", font=font_title, fill=TEAL_ACCENT)
    draw.text((100, 108), "Fixed 600 UPM Monospace \u2022 CRISPR-Cas9 Cleavage \u2022 Zero-Drift NGS Alignment \u2022 IUPAC Degenerate Codes", font=font_subtitle, fill=MUTED_TEXT)
    draw.line([(100, 150), (1900, 150)], fill=CARD_BORDER, width=2)

    cards = [
        {
            "title": "1. CRISPR-CAS9 TARGETED CLEAVAGE AT HBB (SICKLE CELL LOCUS)",
            "subtitle": "Blunt DSB cleavage 3 bp upstream of Protospacer Adjacent Motif [NGG] with sgRNA hairpin",
            "seq1": "5' \ue92a C C T G A G G A G A A G \u2702 T C T G C C G T T \ue921 [NGG] \ue92a 3'",
            "seq2": "3' \ue92b G G A C T C C T C T T C   A G A C G G C A A \ue921 [NCC] \ue92b 5'",
            "clinical": "Exa-cel (Casgevy) gene therapy: BCL11A enhancer edit restores fetal hemoglobin (HbF) production.",
            "color": ROSE_ACCENT,
            "y": 180
        },
        {
            "title": "2. NEXT-GENERATION SEQUENCING (NGS) MULTILINE READ DEPTH ALIGNMENT",
            "subtitle": "Strict 600 UPM pitch guarantees pixel-perfect vertical column alignment with zero drift",
            "seq1": "Ref:    A T G G C C A T T G T A A T G G G C C G C T G A C T G A",
            "seq2": "Read 1: A T G G C C A T T G T A A T G G G C C G C T G A C T G A\nRead 2: A T G G C C A T T G T A A T G G G C - G C T G A C T G A\nRead 3: A T G G C C A T T G T A A T T G C C G C T G A C T G A  [SNP: C>T, Q38]",
            "clinical": "Phred Q38 base call quality (P_error < 0.00016). ISMP-disambiguated C vs. G eliminates indel false positives.",
            "color": CYAN_ACCENT,
            "y": 480
        },
        {
            "title": "3. IUPAC DEGENERATE BASES & HYDROGEN BOND COMPLEMENTARITY",
            "subtitle": "Universal degenerate primer ambiguity codes with thermodynamic H-bond indicators",
            "seq1": "A \ue923 T [2 H-Bonds]    G \ue924 C [3 H-Bonds]    G \ue925 U [Wobble Non-Watson-Crick]",
            "seq2": "IUPAC Ambiguity Codes: R(A/G) Y(C/T) S(G/C) W(A/T) K(G/T) M(A/C) N(Any)",
            "clinical": "Thermodynamic primer annealing (Tm = 62.4 \u00b0C). Distinguishes high-stability GC clamps from AT repeats.",
            "color": AMBER_ACCENT,
            "y": 790
        },
        {
            "title": "4. CLINICAL CYTOGENETICS & PHILADELPHIA CHROMOSOME TRANSLOCATION",
            "subtitle": "Karyotype ideograms, centromeres, telomeres, and reciprocal translocation notation",
            "seq1": "46,XX,\ue92c t(9;22)(q34.1;q11.2)  [BCR-ABL1 Fusion: Tyrosine Kinase]",
            "seq2": "p-arm \ue926 Centromere \ue927 Telomere     Epigenetics: \ue928 m5C-Methylation  \ue929 m6A-RNA",
            "clinical": "Imatinib / Gleevec targeted therapy in Chronic Myeloid Leukemia (CML). Monospace karyotype standard.",
            "color": TEAL_ACCENT,
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
        draw.text((140, y0 + 88), card["seq1"], font=font_seq_med, fill=TEXT_WHITE)
        draw.text((140, y0 + 138), card["seq2"], font=font_seq_med, fill=TEAL_ACCENT)
        draw.text((140, y0 + 230), f"\u00bb Clinical Context: {card['clinical']}", font=font_meta, fill=(203, 213, 225))

    # Bottom Banner: Specialized Genomics Glyph Set
    draw.rounded_rectangle([(100, 1370), (1900, 1515)], radius=12, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.text((130, 1385), "SPECIALIZED CLINICAL GENOMICS GLYPH SET:", font=font_section, fill=TEAL_ACCENT)
    
    sample_symbols = "\u2702  \ue920  \ue921  \ue922  \ue923  \ue924  \ue925  \ue926  \ue927  \ue92a  \ue92b  \ue928  \ue929  \ue92c"
    sample_legend = "DSB Scissors \u2022 PAM Motif \u2022 Hairpin Loop \u2022 A=T (2H) \u2022 G\u2261C (3H) \u2022 G\u00b7U Wobble \u2022 Centromere \u2022 Telomere \u2022 5'->3' \u2022 3'->5' \u2022 m5C \u2022 m6A \u2022 t(A;B)"
    draw.text((130, 1425), sample_symbols, font=font_seq_med, fill=TEXT_WHITE)
    draw.text((130, 1475), sample_legend, font=font_meta, fill=MUTED_TEXT)

    os.makedirs(os.path.dirname(OUT_IMG), exist_ok=True)
    im.save(OUT_IMG, "PNG")
    print(f"[OK] Clinical genomics specimen plate rendered to {OUT_IMG} ({os.path.getsize(OUT_IMG)} bytes)")

if __name__ == "__main__":
    render_genome_plate()
