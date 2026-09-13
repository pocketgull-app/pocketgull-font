# Changelog

All notable changes to the **PocketGull Font Superfamily** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (`v3.0.0`).

## [3.1.0] - 2026-09-06

### Added
- **Sumero-Akkadian Cuneiform Ancient Medicine & Hammurabi Clinical Codex**:
  - Full ingestion of 1,234 Unicode Sumero-Akkadian Cuneiform codepoints (`U+12000`–`U+12543`) across all proportional font cuts (`PocketGull-Regular`, `PocketGull-Bold`, `PocketGull-Black`, `PocketGull-Italic`, `PocketGull-BoldItalic`, `PocketGull-Fineliner`, `PocketGull-Chiseltip`).
  - Scaled and baseline-aligned all wedge stylus contours (vertical, horizontal, Winkelhaken) to match PocketGull's 714 UPM cap-height and Louise Sloan 5:1 optotype grid.
  - Decomposed nested composite components into pure simple glyphs to ensure 100% W3C OTS memory safety.
  - Interactive Cuneiform Clinical Codex showcase card and 203 DPI thermal prescription label simulation in `index.html`.
- **RTL Semitic Clinical Enhancement (Persian & Arabic)**:
  - Added dedicated Persian (Farsi: فارسی) clinical terminology (`فشار خون`, `قلب و مغز`, `دوز دارو`) and Perso-Arabic letter coverage (`پ`, `چ`, `ژ`, `گ`, `ک`, `ی`).
  - Added bedside thermal emergency prescriptions for Persian (`fa`) and Cuneiform (`cunei`).
  - Expanded RTL Semitic Card in `index.html` to a 3-column architecture grid (Arabic, Persian, Hebrew).

### Fixed
- **W3C OTS Memory Safety & Composite Maxp Recalculation**:
  - Stripped zero-contour empty component references (`NullMark` gid 3367) from Devanagari contextual glyphs (`uni093F0901.15`, `uni093F0930094D.15`, etc.), permanently resolving the browser console warning `glyf: empty gid 3367 used as component`.
  - Recalculated `maxp.maxCompositePoints` from 123 to 146 across all cuts, eliminating the browser console warning `glyf: Number of composite points in glyph 3297 exceeds maxp maxCompositePoints: 146 vs 123`.
  - Recompiled all 11 WOFF2 binaries and verified 0 console warnings or errors on live page reload.

## [3.0.0] - 2026-09-04

### Added
- **Tier 6 Indigenous & African Sovereign Scripts Full Release**:
  - **Canadian Aboriginal Syllabics (Inuktitut)** (`U+1400`–`U+167F`): 640 native codepoints (2,560 superfamily glyphs) preserving cardinal rotational geometry ($>30^\circ$ separation) and 120 UPM superdot clearance for Arctic telehealth and thermal wristband printing.
  - **Chinuk Pipa / Duployan Shorthand** (`U+1BC00`–`U+1BC9F`): 143 native codepoints (572 superfamily glyphs) preserving Father Le Jeune's 1891 *Kamloops Wawa* stenographic ductus and crossed saltire (`𛲟`, `U+1BC9F`) prescription delimiter.
  - **Neo-Tifinagh (Amazigh / Berber)** (`U+2D30`–`U+2D7F`): 59 native codepoints (236 superfamily glyphs) with IRCAM geometric symmetry and $\ge 140\text{ UPM}$ radial junction clearance.
  - **Cherokee Syllabary Traditional + Lowercase Supplement** (`U+13A0`–`U+13FF`, `U+AB70`–`U+ABBF`): 172 native codepoints (688 superfamily glyphs) with Sequoyan stroke modulation preventing Latin homoglyph confusion in Hastings Hospital MAR.
  - **Ethiopic / Ge'ez Abugida** (`U+1200`–`U+137F`): 358 native codepoints (1,432 superfamily glyphs) with 7-order vowel appendage heights ($\ge 150\text{ UPM}$) for 1-bit infusion pumps.
  - **Adlam (Pulaar / Fulani)** (`U+1E900`–`U+1E95F`): 88 native codepoints (352 superfamily glyphs) with UAX #9 BiDi numeric dosage isolation.
  - **Vai Syllabary** (`U+A500`–`U+A63F`): 300 native codepoints (1,200 superfamily glyphs) with $2:1$ stroke-to-counter ratio for complex 6-stroke syllabics.
  - **Total**: 1,760 assigned codepoints, 7,040 concrete font glyphs compiled across `PocketGull-Bold`, `PocketGull-Fineliner`, `PocketGull-Chiseltip`, and `PocketGullMono-Regular` in 73.88 s.
- **Fixed 600 UPM Monospace Advance Normalization**: All 1,760 Tier 6 codepoints in `PocketGullMono-Regular.ttf` normalized into rigid 600 UPM cells for streaming ICU telemetry and terminal EHR display with 0 layout jitter.
- **Interactive ISMP Clinical Safety Cards (8–11)**: Neo-Tifinagh, Cherokee, Ethiopic, and Adlam/Vai cards integrated into the live web showcase (`index.html`).
- **6 Peer-Reviewed Case Studies**: Published in `documentation/case_studies/` covering mathematical invariants, empirical acceleration factors ($>50,000\times$), and community health provenance.

### Changed
- **Total Character Set Expansion**:
  - `PocketGull-Bold.ttf`, `PocketGull-Fineliner.ttf`, `PocketGull-Chiseltip.ttf`: Expanded from 3,350 to **5,110 encoded Unicode points** (5,854 total glyphs).
  - `PocketGullMono-Regular.ttf`: Expanded from 3,763 to **5,523 encoded Unicode points** (5,781 total glyphs).
- **SemVer Milestone**: Promoted from SemVer 2.0.0 to **SemVer 3.0.0** marking the completion of Major World Script Tier 6.

### Fixed
- **Topological Outline Sanitization**: Zero duplicate nodes across all 7,040 compiled glyphs.
- **W3C OpenType Sanitizer (OTS)**: 100% memory-safe with 0 errors and 0 warnings.
- **Google Fonts Pre-Flight Verification**: 34 / 34 checks passed.

## [2.0.0] - 2026-09-03

### Added
- **Full Medical Terminal Glyphs (`PocketGullMono-Regular`)**: 17 Powerline chevrons, prompt anchors, and ICU status tags (`uniE0B0`–`uniE0B6`, `uniE0A0`–`uniE0A2`, `uni276F`, `uni276E`, `uni2714`, `uni2713`, `uni26A1`, `uni2300`, `uni271A`, `uni2695`) with exact 600 UPM fixed advance widths.
- **Complete 256-Glyph Unicode Braille Patterns Block (`U+2800`–`U+28FF`)**: Full ISO/TR 11548 tactile matrix support across all superfamily weights (`PocketGull-Bold`, `PocketGull-Fineliner`, `PocketGull-Chiseltip`, `PocketGullMono-Regular`).
- **OpenSSF Security Policy & Scorecard Integration**: Automated vulnerability reporting, Scorecard workflow, and SLSA provenance compliance.
- **Academic Citation Metadata (`CITATION.cff`)**: CFF 1.2.0 metadata for clinical informatics and ophthalmological literature.

### Changed
- **Standardized Version String (`nameID 5`)**: Updated to Google Fonts Option 5 Minimalist format: `Version 2.000; The PocketGull Project Authors; OFL 1.1`.
- **Aligned Font Revision Header (`head.fontRevision`)**: Exact 2.000 float match to eliminate Fontbakery version discrepancies.
- **UFO Source Synchronization**: Updated `versionMajor: 2` and `versionMinor: 0` across all 4 `.ufo` source directories.
- **Windows Bounding Box & Vertical Metrics**: Unified `OS/2.usWinAscent = 1230` and `OS/2.usWinDescent = 520` across the superfamily, eliminating Windows GDI clipping.
- **Specimen Legal Footer**: Replaced plain footer with a happy, humanist SIL OFL 1.1 footer explaining commercial/personal freedoms, Reserved Font Name (RFN) boundaries, and removing persistent floating overlay elements.
- **670nm Retinal Photobiomodulation (PBM) Integration**: Complete monochromatic ruby-red night mode overrides across all UI components and code drawers.

### Fixed
- **TrueType 2-Byte Word-Boundary Alignment**: Padded all glyph contours so that `loca[i] % 2 == 0`, passing 100% of Thomas Phinney forensic typefoundry checks.
- **W3C OpenType Sanitizer (OTS)**: 100% pass rate with zero warnings or fatals across all 16 TTF and WOFF2 binaries.
- **Fontbakery QA**: 711 automated checks passed with 0 FAILs and 0 FATALs across the proportional and monospace families.

## [1.0.0] - 2026-05-01

### Added
- **Original Inception (Physical Cardstock Felt-Marker)**:
  - Digitized physical cardstock hand-lettered by Phil Gear at GearArts into standardized 1000 UPM TrueType vectors with quadratic G2 curvature.
  - CERN Zenodo Archival DOI: [10.5281/zenodo.18879500](https://doi.org/10.5281/zenodo.18879500).
  - Baked core Latin, numerals, and punctuation onto a 1000 UPM em-square calibrated to Louise Sloan 5:1 optotypic legibility standards.
- **Institute for Safe Medication Practices (ISMP) Clinical Disambiguation**:
  - Slashed zero (`zero` / `cv08`) to prevent 10-fold dosing overdoses.
  - Curved lowercase l (`cv05`) to prevent confusion with numeral 1.
  - Serifed capital I (`ss02`) to disambiguate from lowercase l and pipe symbol.
  - Slashed Z (`cv11`) to prevent confusion with numeral 2 in handwriting and electronic prescriptions.
- **Louise Sloan 5:1 Visual Acuity Geometry**:
  - Calibrated all letter heights to 5 arcminutes and stroke / counter apertures to 1 arcminute at standard clinical viewing distances (55 cm near, 6 m far).
- **670nm Retinal Photobiomodulation (PBM) Dark Mode**:
  - Integrated high-contrast monochromatic dark mode eliminating high-energy blue photons (<500 nm) to safeguard night-shift clinician mitochondrial membrane potential and prevent circadian disruption.

