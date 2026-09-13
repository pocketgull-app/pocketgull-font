# Adobe Fonts Foundry Partner Submission Dossier

**Superfamily**: PocketGull  
**Foundry**: PocketGull Clinical Typefoundry / GearArts  
**Principal Designer**: Phil Gear (ORCID: 0009-0008-1372-5381)  
**Specimen Site**: [https://font.pocketgull.app](https://font.pocketgull.app)  
**License**: SIL Open Font License 1.1  
**Category**: Sans-Serif, Display, Slab Serif, Monospace  

---

## 1. Executive Summary & Design Vision

PocketGull is a life-critical, optotypically calibrated clinical and telemetry font superfamily engineered by Phil Gear. Originating from tactile felt marker lettering created on physical cardstock for GearArts, PocketGull bridges humanist stroke warmth with Louise Sloan 5:1 optotypic legibility (the gold standard in clinical ophthalmology) and Institute for Safe Medication Practices (ISMP) character disambiguation.

While corporate medical environments have historically relied on sterile, mechanical grotesque typefaces (e.g., Arial, Helvetica) that exhibit high error rates during dosage comprehension, PocketGull introduces **Aggressive Gentleness**—a design philosophy proving that life-saving legibility does not require clinical sterility.

---

## 2. The Superfamily Architecture (17 Masters + Variable)

PocketGull spans the entire continuum from 203 DPI thermal bedside wristband printers to 8K surgical monitors:

1. **PocketGull Fineliner (wght 400)**: High-legibility EHR clinical charts, long-form patient discharge summaries, and informed consent documentation.
2. **PocketGull Bold (wght 700 / 800)**: Display titling, Bionic reading anchors, trauma alarm banners, and pharmaceutical warning headers.
3. **PocketGull Chiseltip (wght 900)**: Black calligraphic signage, high-contrast placards, and clinical wayfinding.
4. **PocketGull Marker Raw (wght 900)**: The authentic cardstock felt-marker cut preserving tactile stroke bleed, energetic felt-tip fiber texture, and humanist warmth.
5. **PocketGull Slab (Regular 400 & Bold 700)**: Bracketed humanist slab serifs engineered for extended clinical reading measures, surgical manuals, and editorial prestige.
6. **PocketGull Mono (Regular 400 & Bold 700)**: Fixed 600 UPM pitch, ICU telemetry, sub-cell ECG waveforms, box-drawing characters (`U+2500`–`U+257F`), and Powerline chevrons.
7. **PocketGull Micro (wght 500)**: ETDRS 1:5 aperture dilation tailored for 203 DPI thermal wristbands, ampoules, and cryogenic vials.
8. **PocketGull VF (wght 400–900, slnt -10.5°–0°, opsz 14–96)**: Continuous variable font offering seamless dynamic responsive scaling.

---

## 3. Scientific & Clinical Innovations

### A. ISMP & FDA Life-Critical Medication Safety
* **Slashed Zero (`zero` / `cv08`)**: Mandatory slashed interior prevents catastrophic confusion between numeral `0` and capital `O` in prescriptions (e.g., `10 mg` vs `100 mg`).
* **Curved Foot Lowercase `l` (`cv05`)**: Prominent terminal foot outward sweep decisively eliminates the fatal `1 / l / I` collision.
* **Serifed Capital `I` (`ss02`)**: Bilobe horizontal serifs at cap-height and baseline distinguish `I` from numeral `1` in critical biomarkers (`IL-6`, `IgA`).
* **Slashed `Z` (`cv11`)**: Distinct crossbar stroke differentiates `Z` from `2`.

### B. Louise Sloan 5:1 Optotypic Calibration
* Letterforms conform strictly to the 5:1 height-to-stroke ratio established by Louise Sloan (1959) and the National Research Council Committee on Vision, maximizing visual acuity retention under low-illumination and degraded visual conditions.

### C. Sovereign Script Inclusivity (CARE Principles)
* Complete 100% canonical Unicode coverage across 7 sovereign indigenous writing systems:
  - **Cherokee Syllabary** (`U+13A0`–`U+13FF`, `U+AB70`–`U+ABBF`)
  - **Ethiopic Geʻez** (`U+1200`–`U+137F`)
  - **Canadian Aboriginal / Inuktitut Syllabics** (`U+1400`–`U+167F`, `U+18B0`–`U+18FF`)
  - **Adlam & Vai** (`U+1E800`–`U+1E8DF`, `U+A500`–`U+A63F`)
  - **Neo-Tifinagh** (`U+2D30`–`U+2D7F`)
  - **Chinuk Pipa Shorthand** (`U+1BC00`–`U+1BC9F`)
  - **Full 256 Unicode Braille** (`U+2800`–`U+28FF`) with ISO/TR 11548 tactile 8-dot geometry.
* All non-Latin scripts are anchored to **680 UPM optical cap-height parity** (Invariant Pillar 8), ensuring zero miniature speck artifacts when mixed with Latin text.

---

## 4. Forensic Technical Quality & Standards

PocketGull undergoes rigorous automated and forensic validation before any release:
* **Standard 1000 UPM Em-Square**: Fully ISO/IEC 14496-22 compliant with `USE_TYPO_METRICS` (fsSelection bit 7) enabled across all styles.
* **TrueType 2-Byte Word Alignment**: Every glyph record padded to even bytes; `loca[i] % 2 == 0` strictly enforced (100% W3C OTS valid).
* **Zero Duplicate Nodes**: Outlines pass automated node-deduplication with clean quadratic Béziers.
* **Reserved Bit-7 Masking**: Point flag bit 7 (`0x80`) is strictly zero.
* **DirectWrite / ClearType `gasp` Table**: Version 1 table configured with `GASP_DOGRAY` and `GASP_SYMMETRIC_SMOOTHING`.
* **Adobe AFDKO Validation**: Passes standard Adobe Font Development Kit inspections with clean glyph name tables and OpenType layout features.

---

## 5. Creative Cloud Use Cases for Adobe Users

* **InDesign**: Setting hospital discharge summaries, clinical trial documentation, and pharmaceutical packaging with automated OpenType tabular lining figures and ISMP stylistic sets.
* **Photoshop & Illustrator**: Creating tactile, warm healthcare branding, medical infographics, and wayfinding signage using PocketGull Marker Raw and Chiseltip.
* **Premiere Pro & After Effects**: High-contrast, zero-flicker ICU monitor readouts, telemetry title cards, and accessible closed captions.

---

## 6. Submission Contacts & Links

* **Foundry Website**: [https://font.pocketgull.app](https://font.pocketgull.app)
* **GitHub Repository**: [https://github.com/pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)
* **Inquiry Email**: philgear@gmail.com
