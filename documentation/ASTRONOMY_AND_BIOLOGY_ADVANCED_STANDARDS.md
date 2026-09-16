# PocketGull Superfamily: Advanced Standards for Astronomy & Biology
**Document Reference**: `PGL-ASTRO-BIO-2026-V1`  
**Classification**: Domain-Specific Scientific Visualization & Telemetry Standards  
**Superfamily Binaries**: `PocketGull-Math.ttf`, `PocketGull-Genome.ttf`, `PocketGull-Chem.ttf`, `PocketGullMono-Regular.ttf`  
**Foundry Governance**: SIL Open Font License 1.1 (Zero RFN Debt)  

---

## Executive Overview
While standard typography treats scientific publishing as generic paragraph text with occasional inline symbols, **astronomers** and **biologists** operate under extreme physiological, mechanical, and informational constraints:

1. **Astronomers & Astrophysicists** operate in light-controlled telescope control rooms and mountaintop observatories (Mauna Kea, Paranal, La Palma) where monitor backlights must strictly preserve **scotopic dark adaptation** ($\approx 630\text{--}650\text{ nm}$ monochromatic red), parse 80-column FITS header matrices without character shear, and format celestial coordinates ($hh^{\mathrm{h}} mm^{\mathrm{m}} ss^{\mathrm{s}}, \pm dd^\circ mm' ss''$) with tabular precision.
2. **Biologists & Bioinformaticians** analyze gigabase-scale genomic sequences, CRISPR-Cas9 cleavage constructs, mass spectrometry peaks, single-cell RNA-seq UMAPs, and pharmacokinetic rate equations where misidentifying an IUPAC nucleotide ambiguity code ($R, Y, S, W, K, M$) or a microgram vs. milligram dosage has life-critical consequences.

The **PocketGull Superfamily** provides dedicated domain-specific font binaries and visualization styles engineered specifically for these two scientific frontiers.

---

## Part 1: Advanced Astronomy & Astrophysics Standards

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ POCKETGULL ASTRO: 5 CORE TYPOGRAPHIC PILLARS                                          │
├──────────────────────────┬─────────────────────────────────────────────────────────────┤
│ 1. Scotopic Red HUD      │ Monochromatic 630–650 nm red on pitch black (#000000)       │
│                          │ prevents rhodopsin bleaching in telescope control rooms      │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 2. WCS Celestial Grids   │ Tabular Right Ascension (RA) & Declination (Dec) superscripts│
│                          │ 12ʰ 45ᵐ 23.4ˢ  |  +42° 15' 22''  (zero baseline flutter)    │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 3. Astronomical Constants│ Native solar, planetary & terrestrial symbols:              │
│                          │ M_☉ (Solar mass), M_⊕ (Earth mass), M_♃ (Jupiter mass)      │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 4. FITS 80-Column Cards  │ Strict 600 UPM fixed pitch (PocketGull-Mono) guarantees     │
│                          │ zero column drift in header blocks (CRVAL1, CDELT, BITPIX)  │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 5. Astropy Integration   │ Drop-in `pocketgull-astro-night.mplstyle` for WCSAxes plots │
└──────────────────────────┴─────────────────────────────────────────────────────────────┘
```

### 1.1 Scotopic Dark-Adaptation Preservation
Human dark adaptation relies on rod rhodopsin, which has zero sensitivity to deep red light beyond $630\text{ nm}$. Under monochromatic red ambient light:
* **The Failure of Standard Fonts**: Thin typefaces (such as Computer Modern or Helvetica Light) become invisible because the human eye loses spatial resolution in scotopic conditions.
* **The PocketGull Solution**: The calibrated $68\text{ UPM}$ operator stem width and Louise Sloan 5:1 optotypic stroke-to-height ratio guarantee sharp legibility at high observation altitudes without requiring high display luminance.
* **Observatory Matplotlib Style**: `pocketgull_math.use(theme="astro-night")` activates `pocketgull-astro-night.mplstyle` with pure `#000000` canvas and scotopic `#ff3333` / `#ff4d4d` monochromatic curves.

### 1.2 Celestial Coordinate Formatting
Astronomical coordinates require tight pairing between decimal numerals and non-breaking unit superscripts:
* **Right Ascension (RA)**: $12^{\mathrm{h}} 45^{\mathrm{m}} 23.456^{\mathrm{s}}$
* **Declination (Dec)**: $+42^\circ 15' 22.4''$
* **Astrometric Tolerances**: Parallax ($\pi = 4.25\text{ mas}$), proper motion ($\mu_\alpha = -12.4\text{ mas/yr}$), and surface brightness ($\mu_V = 21.98\text{ mag/arcsec}^2$).
* **Typographic Engine**: With `tnum` (tabular lining figures) active, coordinates line up perfectly across multi-catalog cross-match tables.

### 1.3 Astronomical Symbol Set
PocketGull Math compiles authentic glyphs for astronomical and astrophysical literature:
* Solar: $M_\odot, R_\odot, L_\odot$ (`U+2299` / `U+2609`)
* Earth: $M_\oplus, R_\oplus$ (`U+2295` / `U+2641`)
* Planetary: $M_{\jupiter}$ (`U+2643`), $M_{\saturn}$ (`U+2644`), $\leftmoon$ (`U+263D`)
* Spectral Classification: $O, B, A, F, G, K, M, L, T, Y$

### 1.4 Astropy WCSAxes Python Recipe
```python
import matplotlib.pyplot as plt
from astropy.wcs import WCS
import pocketgull_math

# 1. Activate Observatory Night-Vision Mode
pocketgull_math.use(theme="astro-night", vector_paths=True)

# 2. Plot FITS WCS coordinates
wcs = WCS(header_dict)
fig, ax = plt.subplots(subplot_kw={'projection': wcs})
ax.coords['ra'].set_axislabel(r'Right Ascension (J2000: $\alpha$)')
ax.coords['dec'].set_axislabel(r'Declination (J2000: $\delta$)')
ax.set_title(r'JWST NIRCam F200W Deep Field • $M_{\mathrm{UV}} \le -21.0$ • $z = 10.4$')
plt.savefig("observatory_wcs_hud.svg")
```

---

## Part 2: Advanced Biology, Genomics & Chemistry Standards

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ POCKETGULL BIO & GENOME: 5 CORE TYPOGRAPHIC PILLARS                                   │
├──────────────────────────┬─────────────────────────────────────────────────────────────┤
│ 1. Nucleotide Monospace  │ PocketGull-Genome (600 UPM fixed pitch) for FASTA & FASTQ:  │
│                          │ A, C, G, T, U and IUPAC degenerates (R, Y, S, W, K, M, B, N)│
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 2. CRISPR/Cas9 Badges    │ Native glyphs: Cleavage Scissors (U+E920), PAM motif badge  │
│                          │ [NGG] (U+E921), sgRNA hairpin loops (U+E922), 5'->3' arrows │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 3. Base-Pairing Badges   │ Double H-Bond A=T (U+E923), Triple H-Bond G≡C (U+E924),     │
│                          │ Wobble G·U (U+E925), Epigenetic m5C (U+E928) & m6A (U+E929) │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 4. Chemical Kinetics     │ PocketGull-Chem: equilibrium arrows (⇌), transition states  │
│                          │ (‡), Michaelis-Menten v = V_max[S] / (K_m + [S])            │
├──────────────────────────┼─────────────────────────────────────────────────────────────┤
│ 5. Single-Cell & Omics   │ Drop-in `pocketgull-bio.mplstyle` for scRNA-seq UMAPs,     │
│                          │ volcano plots, and Clustal/RasMol sequence alignments        │
└──────────────────────────┴─────────────────────────────────────────────────────────────┘
```

### 2.1 Genomic Sequence Alignment (FASTA / FASTQ)
In multi-sequence alignments (MSA) with thousands of rows:
* **Zero Kerning Jitter**: Every nucleotide ($A, C, G, T, U$) and gap marker ($-$) maintains an advance width of exactly $600\text{ UPM}$.
* **IUPAC Degenerate Codes**: Distinct glyphs for $R$ (purine: $A/G$), $Y$ (pyrimidine: $C/T$), $S$ ($G/C$), $W$ ($A/T$), $K$ ($G/T$), $M$ ($A/C$), $B$ ($C/G/T$), $D$ ($A/G/T$), $H$ ($A/C/T$), $V$ ($A/C/G$), and $N$ (any).
* **Phred Quality Score Matrix**: ASCII characters $33\text{--}126$ share the exact same pitch for aligning Sanger / Illumina base-call quality.

### 2.2 CRISPR-Cas9 & Genetic Architecture (`PocketGull-Genome.ttf`)
Compiled in [`scripts/compile_genome_font.py`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/scripts/compile_genome_font.py), PocketGull Genome includes dedicated molecular architecture symbols:
* **Double-Strand Break (DSB) Cleavage Scissors**: `U+2702` / `U+E920`
* **PAM Motif Recognition Badge `[NGG]`**: `U+E921`
* **sgRNA Hairpin Stem-Loop**: `U+E922`
* **Strand Orientation Indicators**: $5' \to 3'$ (`U+E92A`) and $3' \to 5'$ (`U+E92B`)
* **Epigenetic Modification Badges**: $m^5\text{C}$ (`U+E928`) and $m^6\text{A}$ (`U+E929`)
* **Centromere Constriction & Telomere End-Caps**: `U+E926`, `U+E927`

### 2.3 Chemical Kinetics & Pharmacology (`PocketGull-Chem.ttf`)
Compiled in [`scripts/compile_chem_font.py`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/scripts/compile_chem_font.py):
* **Reaction Arrows**: Forward ($\to$), reverse ($\gets$), equilibrium ($\rightleftharpoons$), resonance ($\leftrightarrow$).
* **Transition State Marker**: $\ddagger$ (`U+2021`).
* **Enzyme Kinetics**:
  $$\text{Michaelis-Menten: } \quad v = \frac{V_{\max}[S]}{K_m + [S]}$$
  $$\text{Hill Cooperativity: } \quad \theta = \frac{[L]^{n_H}}{K_d + [L]^{n_H}}$$
* **Stereochemical Configuration**: Distinct optical shapes for chiral stereocenters ($(2R, 3S)$-tartaric acid), $D/L$, and $E/Z$ alkene isomers.

### 2.4 Bioinformatics Single-Cell Python Recipe
```python
import matplotlib.pyplot as plt
import pocketgull_math

# 1. Activate Clinical Bioinformatics Theme
pocketgull_math.use(theme="bio", vector_paths=True)

# 2. Render scRNA-seq UMAP Cluster Figure
fig, ax = plt.subplots(figsize=(7, 6))
# Scatter clusters with Clustal/RasMol color cycle:
ax.scatter(umap_x, umap_y, c=clusters, cmap='viridis', s=12, alpha=0.8)
ax.set_title(r'Single-Cell PBMC Atlas (10x Genomics) • $12,480\text{ Cells}$ • $\mathrm{nFeature\_RNA} \ge 2500$')
ax.set_xlabel(r'$\mathrm{UMAP}_1$')
ax.set_ylabel(r'$\mathrm{UMAP}_2$')
plt.savefig("scrna_seq_umap.svg")
```

---

## Part 3: Actionable Outreach & Adoption Strategy

To secure widespread adoption across astronomy and biology departments:

### 3.1 Astronomical Community Outreach
1. **Astropy Ecosystem Integration**:
   * Propose a pull request to `astropy.visualization` documenting `pocketgull-astro-night.mplstyle` as the official dark-sky observatory theme.
2. **Major Observatories & Survey Collaborations**:
   * Reach out to software leads at **Vera C. Rubin Observatory (LSST)**, **JWST Operations**, and the **European Southern Observatory (ESO)**. Demonstrating that PocketGull preserves night vision on telemetry screens during 12-hour observing shifts provides immediate ergonomic value.
3. **AAS (American Astronomical Society) Author Tooling**:
   * Provide a ready-to-use template for `AAS Journals` (ApJ, AJ) utilizing `pocketgull-math.sty`.

### 3.2 Biological & Bioinformatics Community Outreach
1. **Bioconductor & Scanpy Communities**:
   * Add a tutorial for **Scanpy** (Python) and **Seurat** (R) showcasing publication-ready single-cell figures with PocketGull Genome and Math.
2. **BioPython FASTA Formatter**:
   * Publish a 1-line sequence renderer script that outputs color-coded SVG alignments typeset in `PocketGull-Genome.ttf`.
3. **Synthetic Biology & CRISPR Foundations**:
   * Present at **SynBioBeta** and bioinformatics workshops: *"Typesetting the Double Helix: How Dedicated Font Tables Prevent Annotation Drift in Synthetic Biology."*
4. **bioRxiv Pre-Print Template**:
   * Provide a 1-click Typst and LaTeX preprint template tailored for bioRxiv and medRxiv submissions.
