<div align="center">

# 🕊️ PocketGull Font Superfamily

[![OFL 1.1 License](https://img.shields.io/badge/License-SIL_OFL_1.1-blue.svg?style=flat-square)](OFL.txt)
[![SemVer 3.1.0](https://img.shields.io/badge/SemVer-3.1.0-blue.svg?style=flat-square)](CHANGELOG.md)
[![W3C OTS Validated](https://img.shields.io/badge/W3C_OTS-100%25_Valid-emerald.svg?style=flat-square)](https://github.com/googlefonts/ots)
[![Fontbakery QA](https://img.shields.io/badge/Fontbakery-711%2F711_Passed-brightgreen.svg?style=flat-square)](https://github.com/googlefonts/fontbakery)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--1372--5381-A6C900?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0008-1372-5381)
[![Google Developers](https://img.shields.io/badge/Google_Developers-Phil_Gear-4285F4?style=flat-square&logo=google&logoColor=white)](https://me.developers.google.com/u/philgear)
[![CERN Zenodo](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.22309379-024c9c.svg?style=flat-square)](https://zenodo.org/records/22309379)
[![WCAG 2.1 AAA](https://img.shields.io/badge/WCAG_2.1-AAA_100%25-emerald.svg?style=flat-square)](index.html)

### 🌐 [Live Interactive Specimen](https://font.pocketgull.app) &nbsp;•&nbsp; 🛠️ [STEM &amp; Fabrication Studio](stem_studio.html) &nbsp;•&nbsp; 🎼 [Music Studio](music_studio.html) &nbsp;•&nbsp; 🤟 [Sign &amp; ASL Studio](asl_studio.html) &nbsp;•&nbsp; 🕊️ [First Principles](documentation/FIRST_PRINCIPLES.md) &nbsp;•&nbsp; 💾 [Download Fonts (.ZIP)](pocketgull-font-v3.1.0.zip) &nbsp;•&nbsp; 📦 [UFO Sources](sources/) &nbsp;•&nbsp; 📄 [OFL 1.1 License](OFL.txt)

</div>

<div align="center">

<table>
  <tr>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_healer_hero.jpg" alt="PocketGull The Healer (Hearts for i's)" width="100%" />
      <br/><sub><strong>PocketGull The Healer: Felt Marker Cardstock DNA</strong></sub>
    </td>
    <td width="50%" align="center">
      <img src="documentation/images/pocketgull_telemetry_terminal.jpg" alt="PocketGull Telemetry Monospace & Box Drawing" width="100%" />
      <br/><sub><strong>PocketGull Mono: 600 UPM ICU Telemetry &amp; ECG</strong></sub>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="documentation/images/math_comparison_plate.png" alt="PocketGull Math vs Computer Modern" width="100%" />
      <br/><sub><strong>PocketGull Math: 68 UPM Stem Weight (Zero Dark-Mode Hairline Collapse)</strong></sub>
    </td>
    <td width="50%" align="center">
      <img src="documentation/images/astronomy_night_telemetry_plate.png" alt="PocketGull Scotopic 650nm Night Vision HUD" width="100%" />
      <br/><sub><strong>Scotopic 650nm Red Mode: Zero-Photobleaching FITS Observational Console</strong></sub>
    </td>
  </tr>
</table>

</div>

<br/>

**PocketGull** is an open-source clinical sans-serif, display, slab, and telemetry monospace font superfamily designed by Phil Gear. Originating from felt marker lettering created on physical cardstock, PocketGull blends warm humanist stroke dynamics with clear character disambiguation (ISMP standards), Louise Sloan 5:1 optotypic legibility, and fixed 600 UPM telemetry monospace.

Designed for comfortable long-form reading, clinical charts, dashboards, and developer telemetry, PocketGull is built on a standard 1000 UPM em-square with extensive multi-script and tactile Braille support.

---

## 🕊️ The Living Typographic Charter

Grounded in [First Principles](documentation/FIRST_PRINCIPLES.md) and systems engineering (Eskil Steenberg: *avoiding bugs by construction*):

1. **Let Latin be Latin**: Crisp, disambiguated (ISMP), humanist, and readable.
2. **Let Arabic be Arabic**: Let the nuqṭa keep its natural pen angle (the authentic reed-pen footprint, honoring calligraphy rather than sterile mechanical plumbness).
3. **Let Braille be Braille**: Preserve standard tactile cell geometries and negative space (ISO/TR 11548 &amp; ISO 17049).
4. **Let Shorthand be Shorthand**: Respect the phonemic size ratios of stenography without forcing it into Roman metal boxes.
5. **Keep the binary engine clean**: Pad bytes to keep OTS happy (`loca[i] % 2 == 0`), but don't confuse memory alignment with typographic beauty.

---

## 🗂️ Superfamily Architecture: Typefaces & Font Instances

PocketGull is engineered on a standardized 1000 UPM grid. In strict typographic taxonomy, **PocketGull** is the visual typeface design system, and the compiled `.woff2` and `.ttf` binaries are its concrete font software implementations:

| Typeface Subfamily | Google Fonts Canonical | Font Binary File | PostScript Name | Weight | Advance Metric | Primary Clinical Use Case |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **PocketGull Bold** | `Pocket Gull Bold` | `PocketGull-Bold.woff2` / `.ttf` | `PocketGull-Bold` | 700 / 800 | Proportional | Prescription markers, Bionic reading anchors, alarms |
| **PocketGull Fineliner** | `Pocket Gull Regular` | `PocketGull-Regular.woff2` / `.ttf` (`PocketGull-Fineliner`) | `PocketGull-Regular` | 400 | Proportional | Long-form clinical notes, EHR charts, patient leaflets |
| **PocketGull Chiseltip** | `Pocket Gull Black` | `PocketGull-Black.woff2` / `.ttf` (`PocketGull-Chiseltip`) | `PocketGull-Black` | 900 | Proportional | Expressive signage, trauma alerts, high-contrast placards |
| **PocketGull Slab** | `Pocket Gull Slab` | `PocketGull-Slab-Regular.woff2` / `.ttf` | `PocketGull-Slab-Regular` | 400 / 700 | Proportional | Sturdy humanist slab serifs, display titling, editorial reading |
| **PocketGull Mono** | `Pocket Gull Mono Regular` | `PocketGullMono-Regular.woff2` / `.ttf` | `PocketGullMono-Regular` | 400 / 500 | Fixed 600 UPM | ICU telemetry, tabular vitals, gapless box drawing |
| **PocketGull Outline** | `Pocket Gull Outline` | `PocketGull-Outline.woff2` / `.ttf` | `PocketGull-Outline` | Display | Locked to Bold | Multi-color lithography, header silhouettes, hollow display |
| **PocketGull Inline** | `Pocket Gull Inline` | `PocketGull-Inline.woff2` / `.ttf` | `PocketGull-Inline` | Display | Locked to Bold | Engraved titling, hairline center grooves, layered signage |
| **PocketGull Halftone** | `Pocket Gull Halftone` | `PocketGull-Halftone.woff2` / `.ttf` | `PocketGull-Halftone` | Display | Locked to Bold | 45° Ben-Day screen tone lithography, zero-registration multi-color print |
| **PocketGull Algo** | `Pocket Gull Algo` | `PocketGull-Algo.woff2` / `.ttf` | `PocketGull-Algo` | 400 / 500 | Fixed 600 UPM | Computer science, AST & DAG tree graphs, Big-O complexity, formal semantics, memory inspection |
| **PocketGull Learn** | `Pocket Gull Learn` | `PocketGull-Learn.woff2` / `.ttf` | `PocketGull-Learn` | 400 | Proportional | K-12 education, D'Nealian continuous guidelines (ss06), dyslexia basal grounding, TouchMath dots |
| **PocketGull Lab** | `Pocket Gull Lab` | `PocketGull-Lab.woff2` / `.ttf` | `PocketGull-Lab` | 400 | Proportional | Clinical pathology SOPs, RCF centrifugation (×g), micropipette badges (P10–P1000), BSL badges |
| **PocketGull Press** | `Pocket Gull Press` | `PocketGull-Press.woff2` / `.ttf` | `PocketGull-Press` | 400 | Proportional | 3D Printing (FDM/SLA nozzle badges, fits, infills, overhangs), paper dot-gain, packaging dielines, CAD GD&T |
| **PocketGull VF** | `Pocket Gull Variable` | `PocketGull-VF.woff2` / `.ttf` | `PocketGull-VF` | 100–900 | Variable | 16 continuous axes: Hairline to Black, Softness, Sloan 5:1, ISMP |

---

## 🔬 Core Highlights

* **🔍 Character Disambiguation Suite**: Native OpenType layout feature tables for slashed zero (`cv08`), curved lowercase `l` (`cv05`), serifed uppercase `I` (`ss02`), and tabular numbers (`tnum`).
* **❤️ The Healer Alternate (Hearts for i's)**: Playful heart-shaped tittles on lowercase *i* (`.philocardia-heart`, cv09 alternate) bringing warmth, friendliness, and distinctive personality to headings.
* **⠃ Tactile Braille Block (`U+2800`–`U+28FF`)**: Full 256-glyph ISO/TR 11548 tactile matrix calibrated with standard negative space and Latin baseline alignment.
* **𛰀 Optical Proportioning for Chinuk Pipa**: Duployan shorthand loops and stems proportioned to harmonize naturally alongside Latin text.
* **👁️ Sloan 5:1 Optotypes**: Proportioned for high legibility, comfortable reading distances, and anti-crowding clarity.
* **💻 Fixed 600 UPM Monospace**: Strict 600 UPM gapless box drawing (`U+2500`–`U+257F`), sub-cell waveforms, and clean developer telemetry.
* **🎨 Chromatic Layering Engine**: Exact-matching advance widths across Solid Base, Halftone, Hairline Inline, and Outline cuts for multi-color lithography and design work.

---

## 🏛️ Foundry Governance & Technical Standards

PocketGull adheres to strict engineering, typographic, and open-source standards:

### ✒️ Typographic Precision & Binary Safety
* **2-Byte Word Boundary Invariant**: DirectWrite and W3C OTS memory buffers discard fonts with odd byte offsets. Every glyph record is strictly padded to 2-byte alignment (`loca[i] % 2 == 0`).
* **Zero Duplicate Nodes**: Bézier contours are cleaned with zero co-located control points, guaranteeing clean rasterizer scan conversion on high-resolution displays and thermal wristband printers.
* **Forensic Table Verification**: 100% pass across all SFNT tables with zero reserved flags set.

### 🌐 Open Source & Upstream Delivery
* **SIL Open Font License 1.1**: Free for personal, commercial, academic, and clinical use with zero licensing fees and zero RFN debt.
* **Specification Parity**: Exact SemVer parity across `head.fontRevision == 3.1` and `nameID 5 == "Version 3.100; The PocketGull Project Authors; OFL 1.1"`.
* **Clean Single Source of Truth**: Lightweight vector sources and reproducible build toolchains.

### 🕊️ Grounded Multi-Script Design
* **Authentic Script Proportions**: Non-Latin scripts (Arabic, Canadian Syllabics, Duployan, Cherokee, Ethiopic) are designed according to their own typographic traditions and calligraphic rules, rather than forced into Latin geometric molds.
* **Standard Unicode Alignment**: Glyphs are mapped strictly to canonical Unicode points with proper bi-directional and layout metadata.


---

## 🌐 Universal World Scripts Coverage & Support

To support healthcare communication across diverse global communities, PocketGull supports major world writing systems, eliminating missing-glyph boxes across global medical and informational interfaces:

| Script Family | Writing Systems | Coverage in PocketGull | Status |
| :--- | :--- | :---: | :---: |
| **Latin, Cyrillic & Greek** | Basic Latin, Extended-A/B, Cyrillic, Greek, ICU Telemetry | 3,350+ characters | 🟢 **100% Complete** |
| **Braille & Tactile** | 256-cell ISO/TR 11548 8-dot matrix (`U+2800`–`U+28FF`) | 256 codepoints | 🟢 **100% Complete** |
| **RTL & Semitic** | Arabic, Hebrew, Syriac, Thaana (BiDi & Cursive) | 957 CPs, 3,828 superfamily glyphs | 🟢 **100% Complete** |
| **South Asian & Indic** | Devanagari, Bengali, Tamil, Telugu, Gurmukhi, Gujarati, Oriya, Kannada, Malayalam, Sinhala | 7,344 superfamily glyphs across 10 scripts | 🟢 **Complete** |
| **Southeast Asian** | Thai, Lao, Khmer, Burmese, Tibetan | 746 CPs, 2,984 superfamily glyphs | 🟢 **100% Complete** |
| **East Asian (CJK)** | Top 3,500 Hanzi, Radicals, Kana, Hangul featural blocks | 4,806 CPs, 19,224 superfamily glyphs | 🟢 **100% Complete** |
| **Indigenous & African Writing Systems** | Canadian Aboriginal Syllabics (Inuktitut), Duployan (Chinuk Pipa), Neo-Tifinagh, Cherokee, Ethiopic, Adlam, Vai | 1,760 CPs, 7,040 superfamily glyphs | 🟢 **100% Complete** |

*Multi-Script Case Studies*: Seven multi-script case studies are documented with typographic and historical analysis:
- Case Study 01: [`CASE_STUDY_01_INUKTITUT_SYLLABICS.md`](documentation/case_studies/CASE_STUDY_01_INUKTITUT_SYLLABICS.md) (Arctic Nunavut Telehealth)
- Case Study 02: [`CASE_STUDY_02_CHINUK_PIPA.md`](documentation/case_studies/CASE_STUDY_02_CHINUK_PIPA.md) (Grand Ronde & Pacific Northwest)
- Case Study 03: [`CASE_STUDY_03_NEO_TIFINAGH.md`](documentation/case_studies/CASE_STUDY_03_NEO_TIFINAGH.md) (North African Amazigh Vitality)
- Case Study 04: [`CASE_STUDY_04_CHEROKEE_SYLLABARY.md`](documentation/case_studies/CASE_STUDY_04_CHEROKEE_SYLLABARY.md) (Sequoyah Syllabary & Hastings Hospital)
- Case Study 05: [`CASE_STUDY_05_ETHIOPIC_GEEZ.md`](documentation/case_studies/CASE_STUDY_05_ETHIOPIC_GEEZ.md) (Horn of Africa 7-Order Abugida)
- Case Study 06: [`CASE_STUDY_06_WEST_AFRICAN_SCRIPTS.md`](documentation/case_studies/CASE_STUDY_06_WEST_AFRICAN_SCRIPTS.md) (Adlam & Vai Community Health)
- Case Study 07: [`CASE_STUDY_07_PAN_TRIBAL_ORTHOGRAPHIES.md`](documentation/case_studies/CASE_STUDY_07_PAN_TRIBAL_ORTHOGRAPHIES.md) (Indigenous Orthographies & Stacked Diacritics)

PocketGull pairs seamlessly with Google Noto Sans (`sCapHeight=714`, `sxHeight=536` exact metric match on 1000 UPM grid) and system CJK/Indic typefaces with zero baseline jitter.


---

## 🚀 Quickstart

Link via CSS:
```html
<link rel="stylesheet" href="https://font.pocketgull.app/fonts.css">
```

Enable clinical dosage disambiguation:
```css
.clinical-dosage-safe {
  font-family: 'PocketGull', sans-serif;
  font-feature-settings: "zero" 1, "cv08" 1, "cv05" 1, "ss02" 1, "tnum" 1;
}
```

---

## 📦 Global Package Registries & Distribution

PocketGull maintains independent foundry distribution across major system package managers and scientific ecosystems:

| Platform / Ecosystem | Command / Package | Description |
| :--- | :--- | :--- |
| **macOS / Homebrew** | `brew install --cask font-pocketgull` | Complete 29-style TrueType superfamily |
| **Windows / Winget** | `winget install PocketGull.Font` | Native portable Windows font installation |
| **Node.js / NPM** | `npm install @fontsource/pocketgull` | Zero-CLS self-hosted webfonts |
| **Python / PyPI** | `pip install pocketgull-math` | Matplotlib stylesheets & scientific telemetry |
| **Typst Universe** | `#import "@preview/pocketgull-math:3.1.0": *` | Academic STEM paper typesetting |
| **LaTeX / CTAN** | `\usepackage{pocketgull-math}` | 68 UPM robust stem formulas |

---

## 📚 Documentation & Specifications

* 📖 **[Design Specification](documentation/DESIGN_SPECIFICATION.md)** — Architectural guidelines and design history
* 🔬 **[Scientific Bibliography](documentation/BIBLIOGRAPHY.md)** — Peer-reviewed ophthalmology & vision science literature
* 🏛️ **[CERN & Zenodo Archival Guide](documentation/CERN_ZENODO_ARCHIVAL_GUIDE.md)** — Permanent Open Science preservation
* ⚖️ **[Project Governance](GOVERNANCE.md)** — Oversight policy and review board
* 👁️ **[Responsible Typography Framework](RESPONSIBLE_TYPOGRAPHY.md)** — Clinical safety and optotypic invariants
* 🏥 **[Workstation Authorization Memo](documentation/WORKSTATION_AUTHORIZATION_LETTER.md)** — Institutional deployment request for CMIOs and IT
* 🛠️ **[Building from UFO Sources](sources/)** — Compiler setup with `fontmake` and `gftools-builder`
* 🛡️ **[Security Policy](SECURITY.md)** — OpenSSF vulnerability disclosure and W3C OTS verification
* 📝 **[Changelog](CHANGELOG.md)** — Semantic Versioning history (SemVer 2.0.0)

---

## 🔬 Academic Citation & CERN / Zenodo DOI

* **Official Published Zenodo Record (Typeface)**: [zenodo.org/records/22309379](https://zenodo.org/records/22309379)
* **Permanent DOI (Typeface)**: [`10.5281/zenodo.22309379`](https://doi.org/10.5281/zenodo.22309379)
* **Companion Clinical Suite Record (Pocket-Gull)**: [zenodo.org/records/20647514](https://zenodo.org/records/20647514)
* **Companion Clinical Suite DOI**: [`10.5281/zenodo.20647514`](https://doi.org/10.5281/zenodo.20647514)
* **Preservation Archive**: CERN Data Centre (Geneva, Switzerland)

If you use the PocketGull Font Superfamily in your clinical research, healthcare software, or vision science publications, please cite it using [`CITATION.cff`](CITATION.cff) or the BibTeX entry below:

```bibtex
@software{gear_pocketgull_font_2026,
  author       = {Gear, Phil and {The PocketGull Project Authors}},
  title        = {{PocketGull Font Superfamily: Optotypically Calibrated Clinical \& Ophthalmological Vector Letterforms}},
  month        = sep,
  year         = 2026,
  publisher    = {CERN / Zenodo},
  version      = {3.0.0},
  doi          = {10.5281/zenodo.22309379},
  url          = {https://font.pocketgull.app},
  license      = {Apache-2.0}
}
```

---

## 🙏 Acknowledgements & Thanks

We extend our sincere gratitude to the people and open-source projects that help make PocketGull possible:
* **The Dart Programming Language & Google Engineering** ([dart.dev](https://dart.dev)): For providing the clean, high-performance tooling and scripting platform that powers our procedural vector synthesis and build pipelines.
* **Open Source Typography Communities**: For decades of foundational contributions to open-source software, font development, and Unicode typography.
* **Vision Science Pioneers**: Louise L. Sloan (5:1 optotypes), Herman Bouma (visual anti-crowding), and the Institute for Safe Medication Practices (ISMP) for character disambiguation guidance.

See **[THANKS.md](THANKS.md)** for our full dedication and community acknowledgements.

---

## 📜 License & Open Source Standards

PocketGull font binaries and source code are distributed under the **[Apache License, Version 2.0](LICENSE.txt)** (and SIL Open Font License 1.1).  
Free for personal, academic, clinical, and commercial use.

* **Documentation**: See [GOVERNANCE.md](GOVERNANCE.md) and [SECURITY.md](SECURITY.md) for build verification, quality pillars, and open-source release standards.

**Copyright (c) 2026 The PocketGull Project Authors** ([GitHub Repository](https://github.com/pocketgull-app/pocketgull-font)).  
*Crafted with care. Engineered for clarity. 🕊️*


