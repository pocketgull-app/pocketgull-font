# PocketGull Math Telemetry & Scientific Visualization Guide
**Document Reference**: `PGL-MATH-VIS-2026-V1`  
**Classification**: Mathematical OpenType Font Superfamily (`PocketGull-Math.ttf` / `PocketGull-Math.woff2`)  
**Foundry Governance**: SIL Open Font License 1.1 (Zero RFN Debt)  
**Standard**: ISO/IEC 14496-22 OpenType MATH Table Specification  

---

## Executive Overview
The **PocketGull Math** superfamily (`PocketGull-Math.ttf` / `.woff2`) bridges a critical divide in scientific computing, clinical decision support (CDS), and telemetry dashboards: the friction between high-precision mathematical typesetting and crisp humanist legibility.

Standard scientific visualization frameworks (such as Matplotlib) typically default to *DejaVu Sans* or *Computer Modern*, creating visual dissonance in dark-mode telemetry dashboards, generic numeral spacing, and an awkward reliance on heavy external LaTeX compilers (`dvipng`, `ghostscript`, `texlive`).

Furthermore, in developer documentation (Mermaid DAGs, Markdown code blocks, and inline SVG plates), mixing mathematical operators ($\sum, \int, \alpha, \beta, \gamma, \mathcal{L}$) with box-drawing glyphs (`┌─┐│└─┘`) routinely causes **horizontal shear and column drift** because operating systems fall back to mismatched system fonts with incompatible advance widths and baseline metrics.

**PocketGull Math** resolves these failures fundamentally by anchoring all mathematical symbols, operators, Greek letterforms, and structural box primitives to the **exact same 1000 UPM grid** with standardized baseline alignment ($y = 0$), axis height ($y = 260\text{ UPM}$), and stem weight ($w = 68\text{ UPM}$).

---

## 1. Matplotlib: Publication-Grade Clinical & Scientific Telemetry

### 1.1 The Four Architectural Pillars
| Pillar | Technical Mechanism | Clinical & Telemetry Benefit |
| :--- | :--- | :--- |
| **1. Tabular Figures (`tnum`)** | Digits `0`–`9` and decimal separators share uniform advance widths. | Coordinate readouts, axes ticks (`0.00`, `0.25`, `0.50`, `0.75`, `1.00`), and timecodes render with zero horizontal jitter. |
| **2. ISMP Disambiguation (`cv08`, `cv05`, `ss02`)** | Slashed zero (`0̸`), curved lowercase `l`, and bilobe capital `I`. | Eliminates fatal ambiguities between `0` vs `O`, `1` vs `l` vs `I`, and `2` vs `Z` on dosage curves and ROC axes. |
| **3. Native Math Without LaTeX** | Complete OpenType MATH glyph set ($\int, \sum, \mathcal{L}, \alpha, \beta, \gamma, \sqrt{}$). | Renders complex equations natively inside Matplotlib's `mathtext` engine with zero external TeX dependencies. Critical for air-gapped hospital networks. |
| **4. Vector SVG Export Fidelity** | Emits `<text font-family="PocketGull Math">` tags directly. | Produces resolution-independent vector graphics for 4K HUDs, clinical paper reprints, and web mirrors. |

### 1.2 Production Python / Matplotlib Implementation Recipe
```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. Register PocketGull-Math natively in Matplotlib
font_path = r"fonts/ttf/PocketGull-Math.ttf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)

# 2. Configure rcParams to use PocketGull Math for primary text and mathtext
plt.rcParams['font.family'] = 'PocketGull Math'
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'PocketGull Math'
plt.rcParams['mathtext.it'] = 'PocketGull Math:italic'
plt.rcParams['mathtext.bf'] = 'PocketGull Math:bold'

# 3. Create a dark obsidian clinical plot
fig, ax = plt.subplots(figsize=(8, 5), facecolor='#09090b')
ax.set_facecolor('#121217')

# Plot Clinical ROC-AUC Curve
ax.plot([0, 0.05, 0.15, 0.35, 1.0], [0, 0.65, 0.82, 0.92, 1.0], 
        color='#14b8a6', lw=2.5, label=r'Gen-9 DINOv2 ($\mathrm{AUC} = 0.854$)')
ax.plot([0, 1], [0, 1], color='#52525b', ls='--', lw=1.5, label=r'Chance Baseline ($\mathrm{AUC} = 0.500$)')

# Axis labels & title with mathematical formulas (evaluated via mathtext)
ax.set_title(r'$\mathcal{L}_{\mathrm{ASL}} = -\sum_{k=1}^{12} y_k(1-p_k)^{\gamma_+} \log(p_k)$  |  $\eta_t = 2 \times 10^{-6}$', 
             color='#f4f4f5', fontsize=12, pad=14)
ax.set_xlabel(r'False Positive Rate ($1 - \mathrm{Specificity}$)', color='#a1a1aa', fontsize=10)
ax.set_ylabel(r'True Positive Rate ($\mathrm{Sensitivity}$)', color='#a1a1aa', fontsize=10)

# PocketGull styling & chrome integration
ax.tick_params(colors='#a1a1aa', labelsize=10)
for spine in ax.spines.values():
    spine.set_color('#272732')

# Legend styling
legend = ax.legend(loc='lower right', facecolor='#181820', edgecolor='#272732', labelcolor='#f4f4f5')
for text in legend.get_texts():
    text.set_fontfamily('PocketGull Math')

# Export resolution-independent SVG with embedded font references
plt.savefig("clinical_roc_curve.svg", format="svg", bbox_inches="tight")
plt.close()
```

---

## 2. Mermaid & Markdown Graphs: Mathematical Flowcharts & Pipeline DAGs

Mermaid natively supports runtime theme customization through the `%%{init: ...}%%` declaration. By configuring the font cascade to prioritize `PocketGull Math`, complex machine learning, biophysical, and pharmacokinetic DAGs can display mathematical Greek parameters ($\eta, \alpha, \gamma$), operators ($\sum, \int, \le$), and calligraphic notations ($\mathcal{L}$) directly inside nodes and edge labels.

### 2.1 Complete Mermaid DAG Recipe
```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'fontFamily': 'PocketGull Math, PocketGull Mono, monospace',
    'fontSize': '12px',
    'primaryColor': '#121217',
    'primaryTextColor': '#f4f4f5',
    'primaryBorderColor': '#14b8a6',
    'lineColor': '#14b8a6',
    'tertiaryColor': '#181820',
    'edgeLabelBackground': '#09090b'
  }
}}%%
flowchart LR
    subgraph S1["1. High-Res Spatial Ingestion"]
      A["MRI Slabs: [z-1, z, z+1]<br/>(392 × 392 Slices)"] --> B["DINOv2 ViT Backing<br/>(28 × 28 Patches)"]
    end
    subgraph S2["2. Staged Metaplasticity"]
      B --> C["Blocks 0–9: Frozen Cortical<br/>(η = 0)"]
      C --> D["Blocks 10–11: Unfrozen Critical Period<br/>(η = 2 × 10⁻⁶)"]
    end
    subgraph S3["3. Objective & Bayesian HUD"]
      D --> E["StudyMIL Pooling Head<br/>z = ∑ᵢ αᵢ hᵢ"]
      E --> F["Asymmetric Loss: ℒ_ASL<br/>γ₊ = 1.0, γ₋ = 5.0"]
      F --> G["Bayesian Co-Occurrence Prior<br/>P(Medial Men | ACL) = 54.5%"]
    end
```

### 2.2 `600 UPM` Box-Drawing Binary Tree in Mermaid (Sloan-5 Harmonic Scale: `20px → 16px → 15px → 12.5px`)

Following Dieter Rams' Law 10 (*"Weniger, aber besser"*), Edward Tufte's rule against `1 + 1 = 3` double-border interference, and **Louise Sloan's `5:1` (`200 UPM`) optotype module**, each level of the Mermaid binary tree is assigned a harmonic typographic scale step (`classDef`) where `600 UPM` advance widths, `200 UPM` Sloan strokes, `125 UPM` eighth-blocks (`▁▂▄█▂▁`), and `40 UPM` box hairlines (`─`) snap to exact integer or Retina half-pixel grids:

| Binary Tree Depth | Scale Class (`classDef`) | Font Size (`px` / `pt`) | Classical Interval | `600 UPM` Cell Width | `200 UPM` Sloan Stroke | `40 UPM` Box Rule / `125 UPM` Step |
| :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| **Level 0 (Root)** | `:::scaleRoot` | **`20.0 px`** (`15pt` Georgia) | **$1.000 \times$ Reference** | **`12.0 px`** (Exact int) | **`4.0 px`** (Exact int) | `0.8 px` rule · `2.5 px` 1/8th step |
| **Level 1 (Major Branch)** | `:::scaleBranch` | **`16.0 px`** (`12pt` Pica) | **$4:5$ Major Third** | `9.6 px` | `3.2 px` | **`2.0 px`** exact integer 1/8th step |
| **Level 2 (Subtree Gate)** | `:::scaleGate` | **`15.0 px`** (`11.25pt` Small Pica) | **$3:4$ Perfect Fourth** | **`9.0 px`** (Exact int) | **`3.0 px`** (Exact int) | `0.6 px` rule · `(4.5, 4.5)` centroid |
| **Level 3 (Telemetry Leaf)** | `:::scaleLeaf` | **`12.5 px`** (`9.375pt` Bourgeois) | **$5:6$ Minor Third** | **`7.5 px`** (`15px @ 2x`) | **`2.5 px`** (`5px @ 2x`) | **`0.5 px`** (`1.0px` Retina hairline!) |

```mermaid
%%{init: {
  'theme': 'base',
  'flowchart': {
    'nodeSpacing': 16,
    'rankSpacing': 42,
    'padding': 12,
    'curve': 'stepAfter'
  },
  'themeVariables': {
    'fontFamily': 'PocketGull Mono, PocketGull Math, monospace',
    'fontSize': '12.5px',
    'primaryColor': '#0d1522',
    'primaryTextColor': '#f8fafc',
    'primaryBorderColor': '#1e293b',
    'lineColor': '#334155',
    'edgeLabelBackground': '#05080e'
  }
}}%%
flowchart LR
    classDef scaleRoot fill:#0d1522,stroke:#06b6d4,stroke-width:2px,color:#ffffff,font-size:20px,font-weight:700;
    classDef scaleBranch fill:#0d1522,stroke:#334155,stroke-width:1.5px,color:#f8fafc,font-size:16px,font-weight:600;
    classDef scaleGate fill:#090d16,stroke:#334155,stroke-width:1.25px,color:#cbd5e1,font-size:15px,font-weight:600;
    classDef scaleLeaf fill:#05080e,stroke:#1e293b,stroke-width:1px,color:#e2e8f0,font-size:12.5px;
    classDef scaleAccent fill:#05080e,stroke:#06b6d4,stroke-width:1.25px,stroke-dasharray:4 2,color:#ffffff,font-size:12.5px;

    ROOT[["PocketGull v4.0"]]:::scaleRoot

    subgraph SG0["0 · PROPORTIONAL READING (SLOAN 5:1 · 25u CORNER)"]
        direction LR
        B0["0 · Proportional"]:::scaleBranch
        G00["00 · Clinical EHR"]:::scaleGate
        G01["01 · Editorial & Ink"]:::scaleGate
        L000["000 · Sans & 16-Axis VF  |  0̸ l I Z"]:::scaleLeaf
        L001["001 · Philocardia Soft  |  i/j ♥ 72 BPM"]:::scaleLeaf
        L010["010 · Serif, Slab & Marker  |  9,722g"]:::scaleLeaf
        L011["011 · Halftone & Kinpaku  |  ░▒▓█ −45.8%"]:::scaleLeaf
    end

    subgraph SG1["1 · FIXED-GRID TELEMETRY & WORLD (600 UPM PITCH)"]
        direction LR
        B1["1 · Fixed 600 UPM"]:::scaleBranch
        G10["10 · ICU Box & Math"]:::scaleGate
        G11["11 · Tactile & World"]:::scaleGate
        L100["100 · Mono 600 UPM  |  ▁▂▄█▂▁ 072 BPM"]:::scaleAccent
        L101["101 · Math 68u Stem  |  ∑ ∫ √ ℒ"]:::scaleAccent
        L110["110 · Braille & ASL VF  |  ⠿ 256 Cells"]:::scaleLeaf
        L111["111 · 27+ Scripts  |  ᐃᓄᒃᑎᑐᑦ · [!]"]:::scaleLeaf
    end

    ROOT --- B0
    ROOT --- B1
    B0 --- G00
    B0 --- G01
    B1 --- G10
    B1 --- G11
    G00 --- L000
    G00 --- L001
    G01 --- L010
    G01 --- L011
    G10 --- L100
    G10 --- L101
    G11 --- L110
    G11 --- L111

    style SG0 fill:#090d16,stroke:#1e293b,stroke-width:1px,stroke-dasharray:4 2,color:#94a3b8
    style SG1 fill:#090d16,stroke:#1e293b,stroke-width:1px,stroke-dasharray:4 2,color:#94a3b8
    linkStyle 0,1 stroke:#06b6d4,stroke-width:2px;
    linkStyle 2,3,4,5 stroke:#475569,stroke-width:1.4px;
    linkStyle 6,7,8,9,10,11,12,13 stroke:#334155,stroke-width:1px;
```

---

## 3. Pure Unicode / ASCII Markdown Graphs: Zero-Shear Alignment

### 3.1 The Font Fallback Shearing Problem
In standard monospaced fonts (e.g., Courier, Consolas, or un-augmented web fonts), Unicode mathematical characters ($\sum, \int, \alpha, \beta, \gamma, \to, \ge, \mathcal{L}$) are missing from the primary font file. The rendering engine borrows them from arbitrary system fallback fonts (e.g., Arial, Lucida Grande, or Segoe UI Symbol).

Because the fallback glyphs have non-matching advance widths, line heights, and vertical bounding boxes, multi-line ASCII/Unicode tables experience severe **horizontal shear**:
```text
┌────────────────────────────────────────┐
│ UNMATCHED FALLBACK FONT DRIFT (SHEAR)  │  <-- Column alignment breaks
├────────────────────────────────────────┤
│ StudyMIL: z = ∑ α_i h_i   │ Status: OK│  <-- Mismatched width in '∑' causes edge shift
└────────────────────────────────────────┘
```

### 3.2 The PocketGull Math Solution
Because **PocketGull Math** compiles both standard alphanumeric Latin, the complete Greek mathematical set, procedural operators, and box-drawing primitives into the same 1000 UPM em-square, every column maintains exact mathematical pitch:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ GENERATION 9 PIPELINE GRAPH                                            │
├────────────────────────────────────────────────────────────────────────┤
│  [Input MRI: 392×392] ──► DINOv2 ViT ──► Metaplasticity (η = 2×10⁻⁶)   │
│                                                │                       │
│                                                ▼                       │
│                           StudyMIL Head (z = ∑ᵢ αᵢ hᵢ)                 │
│                                                │                       │
│                                                ▼                       │
│                           ℒ_ASL (γ₊=1.0, γ₋=5.0) ──► Macro-AUC ≥ 0.850 │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.3 The Four Font Box-Drawing Vector Techniques (`MonospaceHudEngine`)

Synthesized by [`tool/foundry/monospace_hud.dart`](../tool/foundry/monospace_hud.dart), PocketGull's box-drawing and telemetry primitives obey four exact geometric laws:

| Technique | OpenType / Vector Mechanism (`PocketGullMono` & `PocketGull-Math`) | Telemetry & Mermaid Rendering Benefit |
| :--- | :--- | :--- |
| **1. Full-Bleed Cell Joinery (`U+2500`–`U+257F`)** | Horizontal rules (`40 UPM` stroke) span `x = 0..600 UPM` (`LSB = 0, RSB = 0`) centered at `y = 300`; vertical rules span `y = -200..800 UPM` (`1000 UPM` total cell height) centered at `x = 300`. | Eliminates 1–2 px horizontal row seams so `│`, `║`, and `┼` fuse into continuous vertical walls across multi-line blocks. |
| **2. 4-Bit `NESW` Cardinal Centroid (`(300, 300)`)** | Every junction (`┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘`, `╔ ╦ ╗`, `┏ ┳ ┓`, `╭ ╮ ╰ ╯`) locks its cardinal arms (`North, East, South, West`) to the exact `(x = 300, y = 300)` optical center. | Mixed-weight junctions (`╞`, `╡`, `╤`, `╧`, `╪`) share the exact `(300, 300)` intersection centroid with zero step offset. |
| **3. Sub-Cell 1/8th Sparklines (`U+2581`–`U+2588`)** | Eight stepped block heights (`blockH = (1000 * eighths) ~/ 8`, rising in `+125 UPM` increments from `y = -200` to `y = 800`) + 4-level stipples (`░ ▒ ▓ █`) and Powerline chevrons (`U+E0B0 `). | Delivers **8 vertical resolution steps per text row** for inline ECG waveforms (`▁▂▄█▂▁`) and density bars inside plain-text labels. |
| **4. Zero-Shear Math & Spoof-Guard Invariance** | Math operators (`∑`, `∫`, `±`, `≥`, `ℒ` at `68 UPM` stem, `260 UPM` axis), slashed zero (`0̸`), and the Trojan-Source `[!]` badge (`uni202E.guard`) are compiled directly onto the `600 UPM` advance grid. | Prevents OS fallback to proportional system fonts, keeping right-hand box walls (`│`, `║`) locked to integer multiples of `600 UPM`. |

### 3.4 Highland Tactile Linen & Decorative Scissor-Blade Drafting Recipe (`theme=linen` × `style=deckle`)

For light-mode academic preprints, Kaggle workbench notebooks, and physical cardstock broadsides, pair the **Sloan-5 Harmonic Scale (`20px → 16px → 15px → 12.5px`)** with the **Highland Tactile Linen** drafting palette (`#FDFAF2` cream cardstock, `#F3EFE6` recessed paper well, `#1F2E4C` Prussian drafting-ink borders, `#b45309` 2px ochre drafting rail, `#0e7490` cyan rail, `#047857` emerald rail, and `#9B1C23` colonial crimson rail):

```mermaid
%%{init: {
  'theme': 'base',
  'flowchart': {
    'nodeSpacing': 16,
    'rankSpacing': 42,
    'padding': 12,
    'curve': 'stepAfter'
  },
  'themeVariables': {
    'fontFamily': 'PocketGull Mono, PocketGull Math, monospace',
    'fontSize': '12.5px',
    'primaryColor': '#FDFAF2',
    'primaryTextColor': '#1F2E4C',
    'primaryBorderColor': '#1F2E4C',
    'lineColor': '#1F2E4C',
    'edgeLabelBackground': '#E2DACB'
  }
}}%%
flowchart LR
    classDef linenRoot fill:#FDFAF2,stroke:#b45309,stroke-width:2px,color:#1F2E4C,font-size:20px,font-weight:700;
    classDef linenBranch fill:#FDFAF2,stroke:#1F2E4C,stroke-width:1.5px,color:#1F2E4C,font-size:16px,font-weight:600;
    classDef linenGate fill:#F3EFE6,stroke:#1F2E4C,stroke-width:1.25px,color:#1F2E4C,font-size:15px,font-weight:600;
    classDef linenLeaf fill:#FDFAF2,stroke:#1F2E4C,stroke-width:1px,color:#2C2C2C,font-size:12.5px;
    classDef linenDeckle fill:#FDFAF2,stroke:#b45309,stroke-width:1.25px,stroke-dasharray:4 2,color:#1F2E4C,font-size:12.5px;

    ROOT[["PocketGull v4.0"]]:::linenRoot

    subgraph LN0["0 · HIGHLAND LINEN · PROPORTIONAL READING"]
        direction LR
        B0["0 · Proportional"]:::linenBranch
        G00["00 · Clinical EHR"]:::linenGate
        G01["01 · Editorial & Ink"]:::linenGate
        L000["000 · Sans & 16-Axis VF  |  0̸ l I Z"]:::linenLeaf
        L001["001 · Philocardia Soft  |  i/j ♥ 72 BPM"]:::linenLeaf
        L010["010 · Serif, Slab & Marker  |  9,722g"]:::linenLeaf
        L011["011 · Halftone & Kinpaku  |  ░▒▓█ −45.8%"]:::linenLeaf
    end

    subgraph LN1["1 · DECKLE DRAFTING WELL · 600 UPM & WORLD"]
        direction LR
        B1["1 · Fixed 600 UPM"]:::linenBranch
        G10["10 · ICU Box & Math"]:::linenGate
        G11["11 · Tactile & World"]:::linenGate
        L100["100 · Mono 600 UPM  |  ▁▂▄█▂▁ 072 BPM"]:::linenDeckle
        L101["101 · Math 68u Stem  |  ∑ ∫ √ ℒ"]:::linenDeckle
        L110["110 · Braille & ASL VF  |  ⠿ 256 Cells"]:::linenLeaf
        L111["111 · 27+ Scripts  |  ᐃᓄᒃᑎᑐᑦ · [!]"]:::linenLeaf
    end

    ROOT --- B0
    ROOT --- B1
    B0 --- G00
    B0 --- G01
    B1 --- G10
    B1 --- G11
    G00 --- L000
    G00 --- L001
    G01 --- L010
    G01 --- L011
    G10 --- L100
    G10 --- L101
    G11 --- L110
    G11 --- L111

    style LN0 fill:#F3EFE6,stroke:#1F2E4C,stroke-width:1px,stroke-dasharray:4 2,color:#57534E
    style LN1 fill:#F3EFE6,stroke:#b45309,stroke-width:1px,stroke-dasharray:4 2,color:#b45309
    linkStyle 0,1 stroke:#b45309,stroke-width:2px;
    linkStyle 2,3,4,5 stroke:#1F2E4C,stroke-width:1.4px;
    linkStyle 6,7,8,9,10,11,12,13 stroke:#57534E,stroke-width:1px;
```

---

## 4. Embeddable Inline SVG Micro-Graphs & Telemetry Plates

For rich markdown reports, Astro static sites, and web applications, PocketGull Math supports lightweight inline `<svg>` blocks that run directly in modern browsers without needing external graphing libraries.

### 4.1 Master Telemetry Plate Reference
The verified master plate is available in the repository at:
* **Interactive SVG**: [`documentation/images/pocketgull_math_telemetry_plate.svg`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/pocketgull_math_telemetry_plate.svg)
* **HTML Standalone Viewer**: [`documentation/images/pocketgull_math_telemetry_plate.html`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/pocketgull_math_telemetry_plate.html)

### 4.2 Telemetry Plate Architecture
The plate proves four concurrent domains rendered in dark obsidian (`#09090b` / `#121217`):
1. **Machine Learning ROC-AUC Card**:
   * True Positive Rate ($\text{Sensitivity}$) vs. False Positive Rate ($1 - \text{Specificity}$).
   * Direct numeric readout: $\mathrm{AUC} = 0.854$, $95\%\text{ CI }[0.832, 0.876]$, $p < 0.001$.
2. **Mathematical CDS Formulations Card**:
   * Asymmetric Focal Loss ($\mathcal{L}_{\mathrm{ASL}}$) with asymmetric weighting ($\gamma_+ = 1.0, \gamma_- = 5.0$).
   * Cosine Metaplasticity learning rate schedule ($\eta_t$).
   * Optical Hyperfocal distance formulation ($H = \frac{f^2}{N \cdot c} + f$).
3. **Host Hardware Telemetry Card**:
   * CPU core and thread allocation (`20 Cores / 28 Threads`).
   * DDR5 memory bandwidth (`32.0 GB @ 5600 MT/s • 89.6 GB/s`).
   * AMD Radeon RX 6650 XT DirectML / Vulkan topology (`32 CUs • 2,048 SPs`).
4. **pgphototrek Optical & Ephemeris Telemetry Card**:
   * Solar Altitude & Azimuth ($+42.3^\circ\text{ / }180.0^\circ\text{ S}$).
   * Optical exposure values ($\text{EV}_{100} = 14.3 \implies f/8.0, 1/250\text{s}, \text{ISO }100$).
   * Dark sky vault rating ($\text{Bortle Class 1 • SQM }21.98$).
   * Somatic respiratory pacer ($0.10\text{ Hz • 6 Breaths/min}$).

---

## 5. Mathematical OpenType Table Parameters

Compiled via [`scripts/compile_math_font.py`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/scripts/compile_math_font.py), PocketGull Math strictly adheres to the ISO/IEC 14496-22 specification:

```python
AXIS_HEIGHT = 260       # Half of Latin x-height (520 UPM)
STROKE_WIDTH = 68       # Harmonized operator stem width
DEFAULT_ADVANCE = 600   # Standard operator advance width

# Key OpenType MathConstants
ScriptPercentScaleDown = 70
ScriptScriptPercentScaleDown = 52
DelimitedSubFormulaMinHeight = 1500
DisplayOperatorMinHeight = 1400
FractionRuleThickness = 68
OverbarRuleThickness = 68
RadicalRuleThickness = 68
```

### Stepped Vertical Delimiters (`MathVariants`)
Parentheses `()`, brackets `[]`, braces `{}`, and radicals `√` are procedurally generated in 4 stepped heights:
* Level 1: $1200\text{ UPM}$
* Level 2: $1600\text{ UPM}$
* Level 3: $2000\text{ UPM}$
* Level 4: $2400\text{ UPM}$

This guarantees that nested fractions, matrix groupings, and large integral bounds scale gracefully without pixelation or vector distortion.
