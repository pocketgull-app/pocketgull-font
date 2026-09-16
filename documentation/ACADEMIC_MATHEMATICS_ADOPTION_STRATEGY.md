# PocketGull Math: Academic & Mathematician Adoption Strategy
**Document Reference**: `PGL-MATH-ADOPT-2026-V1`  
**Classification**: Foundry Strategy, Distribution & Ecosystem Outreach  
**Superfamily**: `PocketGull-Math.ttf` / `PocketGull-Math.woff2`  
**Foundry Governance**: SIL Open Font License 1.1 (Zero RFN Debt)  

---

## Executive Summary
For over four decades, academic mathematics and quantitative sciences have remained anchored to Donald Knuth’s **Computer Modern** (1978). While historically monumental, Computer Modern was designed for high-pressure chemical ink-spread on physical paper with low-resolution 300 DPI phototypesetters.

In modern scientific computing—dominated by 4K/5K displays, dark-mode IDEs, OLED telemetry monitors, and automated clinical decision support (CDS)—Computer Modern suffers from acute **hairline collapse (<20 UPM stem weight)**, severe **variable collisions ($\nu$ vs $v$, $\chi$ vs $x$, $0$ vs $O$, $1$ vs $l$ vs $I$)**, and zero integration with modern reactive plotting pipelines (Matplotlib, Typst, Quarto).

**PocketGull Math** presents the world's first **humanist clinical sans-serif OpenType math font**, combining:
1. Full ISO/IEC 14496-22 `MATH` table parameters (`AxisHeight = 260 UPM`, `ScriptPercentScaleDown = 70%`, `FractionRuleThickness = 68 UPM`).
2. Louise Sloan 5:1 optotypic legibility ratios and ISMP life-critical character disambiguation.
3. Universal cross-ecosystem distribution across **LaTeX (CTAN)**, **Typst**, **Quarto**, **Python (Matplotlib)**, and **Web/SVG**.

---

## 1. The 5-Tier Ecosystem Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ POCKETGULL MATH ECOSYSTEM MAP                                                          │
├───────────────────────┬───────────────────────────────┬────────────────────────────────┤
│ Ecosystem Tier        │ Distribution Channel          │ User Invocation                │
├───────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ 1. LaTeX / TeX Live   │ CTAN (`macros/latex/contrib`)  │ \usepackage{pocketgull-math}   │
│ 2. Modern Typst       │ Typst Universe (@preview)     │ #import "@preview/pocketgull"  │
│ 3. Reproducible Quarto│ Quarto Extension Registry     │ quarto add pocketgull-math     │
│ 4. Python Scientific  │ PyPI (`pocketgull-math`)      │ pocketgull_math.use('dark')    │
│ 5. Universal Vector   │ Base64 Embedded SVG / WOFF2   │ 100% Zero-Dependency Standalone│
└───────────────────────┴───────────────────────────────┴────────────────────────────────┘
```

---

## 2. Phase 1: The LaTeX & CTAN Gateway

LaTeX remains the primary toolchain for pure mathematics, theoretical physics, and computer science.

### 2.1 Package Architecture
The repository packages [`distribution/latex/`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/distribution/latex/) ready for CTAN:
* `pocketgull-math.sty`: Keyval options (`slashedzero`, `curvedl`, `serifedI`, `tabular`, `fontpath`).
* `pocketgull-math.tex`: Comprehensive demonstration document.
* `README.md`: CTAN metadata specifications.

### 2.2 CTAN Submission Checklist
1. **Directory Structure**:
   ```text
   pocketgull-math/
   ├── README.md
   ├── doc/
   │   ├── pocketgull-math.pdf
   │   └── pocketgull-math.tex
   ├── fonts/
   │   └── truetype/
   │       └── PocketGull-Math.ttf
   └── tex/
       └── latex/
           └── pocketgull-math.sty
   ```
2. **License Harmonization**: SIL Open Font License 1.1 for font binaries; LPPL 1.3c for `.sty` macro wrappers.
3. **TeX Live Inclusion**: Once approved on CTAN, package enters TeX Live and MacTeX annual distributions, enabling zero-install `\usepackage{pocketgull-math}` for millions of academic researchers.

---

## 3. Phase 2: Capturing Modern STEM (Typst & Quarto)

Typst and Quarto represent the rapid migration vector for next-generation researchers.

### 3.1 Typst Universe (`@preview/pocketgull-math:3.1.0`)
* Native integration with Typst's rust-based math layout engine.
* Configured in [`distribution/typst/`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/distribution/typst/) with `typst.toml`, `lib.typ`, and `example.typ`.
* Allows researchers to toggle dark clinical obsidian mode and ISMP features with a single `#show` rule.

### 3.2 Quarto Academic Extension
* Defined in [`distribution/quarto/`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/distribution/quarto/).
* Seamless dual-compilation to HTML (using `@font-face` WOFF2) and PDF (using XeLaTeX + OpenType TrueType).

---

## 4. Phase 3: The 1-Line Python & Matplotlib Pipeline

For applied mathematicians, data scientists, and ML researchers in Jupyter/VS Code:

### 4.1 PyPI Package (`pocketgull-math`)
* Available in [`distribution/python/`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/distribution/python/).
* Delivers:
  ```python
  import pocketgull_math
  import matplotlib.pyplot as plt

  pocketgull_math.use(theme="dark", vector_paths=True)
  ```
* **Visual Parity Guarantee**: Automatically sets `svg.fonttype = 'path'`, converting text nodes to exact cubic/quadratic bezier splines. Any viewer opening the resulting `.svg` or `.pdf` sees the exact typography without having the font installed.

---

## 5. Phase 4: Confronting Computer Modern's Empirical Flaws

To convince math departments and journal editors, demonstrate clear visual evidence:

### 5.1 The Comparative Proof Plate
Generated via [`scripts/generate_math_comparison_plate.py`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/scripts/generate_math_comparison_plate.py) and permanently documented at:
* [`documentation/images/math_comparison_plate.svg`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/math_comparison_plate.svg)
* [`documentation/images/math_comparison_plate_embedded.svg`](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/documentation/images/math_comparison_plate_embedded.svg)

### 5.2 Key Pain-Point Benchmarks
| Benchmark | Computer Modern / STIX Two | PocketGull Math Solution |
| :--- | :--- | :--- |
| **Dark Mode Rendering** | Hairline stems ($<20\text{ UPM}$) wash out or disappear on high-DPI OLED screens. | Harmonized $68\text{ UPM}$ operator stem width glows crisp and solid without blinding flare. |
| **Greek vs. Latin Collisions** | $\nu$ (nu) and $v$ (vee) are nearly indistinguishable in physics formulas. | Prominent branching angles and stroke terminals differentiate $\nu \ne v$. |
| **Numeric Ambiguity** | $0$ (zero) vs. $O$ (capital letter) cause lethal clinical dosage confusion. | ISMP-compliant slashed zero (`cv08`) optical thinning at junctions. |
| **Delimiter Scaling** | Multi-line brackets stretch vertically with pixelation and mismatched corner caps. | 4-stage procedural `MathVariants` (.v1 to .v4) scale from $1200\text{ UPM}$ to $2400\text{ UPM}$. |
| **Terminal / Code Tables** | Fallback font borrowing causes ragged shearing in ASCII pipeline charts. | Unified 1000 UPM grid aligns math operators with box-drawing glyphs with zero drift. |

---

## 6. Phase 5: Applied Math & Clinical Trial Positioning

While pure mathematicians migrate slowly, **applied mathematicians, biostatisticians, and clinical ML engineers** adopt new tools rapidly because clarity is safety-critical:

1. **Biostatistics & Clinical Pharmacokinetics (PK/PD)**:
   * Target researchers publishing non-compartmental analyses, ODE clearance models, and eGFR equations where numerical clarity prevents dosage errors.
2. **Medical AI & Computer Vision (MICCAI, RSNA, CVPR)**:
   * Target authors of machine learning papers where multi-label loss functions ($\mathcal{L}_{\mathrm{ASL}}$) and confidence intervals ($95\%\text{ CI }[0.832, 0.876]$) dominate figure panels.
3. **Open-Source Scientific Conferences**:
   * Propose a 10-minute lightning talk at **SciPy**, **JuliaCon**, and **PyData**:  
     *"Why Your Telemetry and Math Plots Look Distorted on 4K Displays (And How OpenType MATH Tables Fix It)."*
4. **TeX Stack Exchange & Mastodon Math Community**:
   * Share the Overleaf sample template and interactive SVG specimen plates.
