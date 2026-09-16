# PocketGull Font Superfamily (Upstream Release & Foundry Governance)

## Project Overview
PocketGull is an open-source clinical sans-serif, display, and telemetry monospace font superfamily engineered by Phil Gear. Originating from tactile felt marker lettering created on physical cardstock for GearArts, PocketGull synthesizes humanist stroke warmth with Louise Sloan 5:1 optotypic legibility and Institute for Safe Medication Practices (ISMP) character disambiguation standards for life-critical healthcare environments.

## The Superfamily & Classification
- **Primary Google Fonts Category**: `SANS_SERIF` (with `DISPLAY` and `MONOSPACE` members).
- **PocketGull Bold** (`PocketGull-Bold.ttf`, wght: 700 / 800): Display titling, Bionic reading anchors, trauma alarms.
- **PocketGull Fineliner** (`PocketGull-Fineliner.ttf`, wght: 400): EHR clinical charts, long-form reading, patient discharge summaries.
- **PocketGull Chiseltip** (`PocketGull-Chiseltip.ttf`, wght: 900): Black calligraphic signage, high-contrast placards.
- **PocketGull Mono** (`PocketGullMono-Regular.ttf`, wght: 400 / 500): Fixed 600 UPM pitch, ICU telemetry, box drawing (`U+2500`–`U+257F`), Powerline chevrons (`uniE0B0`–`uniE0B6`), and sub-cell ECG waveforms.
- **PocketGull VF** (`PocketGull-VF.ttf`, wght: 400–900): Dynamic variable font with continuous weight axis.

## 🕊️ Typographic Principles
- **Let Latin be Latin**: Crisp, disambiguated (ISMP), humanist, and readable.
- **Let Arabic be Arabic**: Honor the authentic reed-pen angle and calligraphic stroke contrast rather than artificial geometric flattening.
- **Let Braille be Braille**: Preserve standard tactile cell geometries, dot pitch, and negative space (ISO/TR 11548 & ISO 17049).
- **Let Canadian Syllabics be Syllabics**: Respect rotational symmetry, optical stroke weights, and stroke terminals.
- **Let Stenography be Stenography**: Respect phonemic size ratios without forcing shorthand into Roman metal boxes.
- **Keep the binary engine clean**: Pad bytes to keep OTS happy (`loca[i] % 2 == 0`), ensuring memory safety across all systems.

---

## 🏛️ The Seven Invariant Quality Pillars

### 1. Standard 1000 UPM Em-Square
- All styles locked to standard 1000 UPM conforming to ISO/IEC 14496-22 and Google Fonts specifications.
- `USE_TYPO_METRICS` flag enabled (`fsSelection` bit 7) across all styles.
- Vertical metrics: `sTypoAscender = 780`, `sTypoDescender = -180`, `sTypoLineGap = 100`, `usWinAscent = 960` (or 1230 for display), `usWinDescent = 240` (or 520 for display).

### 2. TrueType 2-Byte Word-Alignment Invariant (`loca` & `glyf`)
- Every glyph record in `glyf` MUST be padded with a trailing `0x00` byte if odd.
- Every offset in `loca` MUST be an even integer (`loca[i] % 2 == 0`).
- Odd offsets cause unaligned memory access in DirectWrite and Chromium OTS, triggering silent font eviction after ~1 second.

### 3. Reserved Bit-7 Flag Masking
- In the TrueType `glyf` point flags byte, Bit 7 (`0x80` / flag 128) is strictly reserved and MUST be zero (`flag & 0x3F`).
- Pass all curves through quadratic conversion (`Cu2Qu`) before emitting to `TTGlyphPen`.

### 4. ISMP Life-Critical Clinical Disambiguation
- **Slashed Zero (`zero` / `cv08`)**: Mandatory on all dosages (`500 mg`). Optical thinning at contour junctions prevents ink clotting.
- **Curved Lowercase `l` (`cv05`)**: Prominent terminal foot outward sweep eliminates `1 / l / I` collisions.
- **Serifed Capital `I` (`ss02`)**: Bilobe horizontal serifs at cap-height and baseline eliminate ambiguity in biomarkers (`IL-6`, `IgA`).
- **Slashed `Z` (`cv11`)**: Distinct crossbar stroke differentiates `Z` from `2`.

### 5. Full 256 Unicode Braille Coverage (`U+2800`–`U+28FF`)
- Full ISO/TR 11548 tactile 8-dot geometry across all styles. Zero `.notdef` across the block.

### 6. Monospace Pitch Invariant (Fixed 600 UPM)
- `PocketGullMono-Regular` strictly declares `isFixedPitch = 1` in `post` and `OS/2.panose.bProportion = 9`.
- Every single glyph maintains an advance width of exactly 600 UPM.

### 7. DirectWrite / ClearType Antialiasing (`gasp`)
- Version 1 `gasp` table mapping `0xFFFF` to `GASP_DOGRAY` (0x02) and `GASP_SYMMETRIC_SMOOTHING` (0x04).

### 8. Multi-Script Proportions & Grounding
- **Unicode Braille (`U+2800`–`U+28FF`)**: Respects ISO/TR 11548 & ISO 17049 standard 8-dot tactile dome geometry ($r=60\text{ UPM}$, $2.5\text{ mm}$ pitch, authentic negative space), grounded on Latin baseline ($y = 0$) to prevent floating cell artifacts.
- **Duployan / Chinuk Pipa (`U+1BC00`–`U+1BC9F`)**: Respects phonemic size ratios ($130\text{ UPM}$ vowel loops vs. consonant stems), anchored along the optical waist ($y = 270\text{ UPM}$) to harmonize with Latin x-height.

---

## 📐 Dieter Rams & Human-Computer Interaction (HCI) Design Invariants

All future glyphs, icons, indicators, and symbols synthesized into PocketGull must strictly adhere to the Ten Ramsian & HCI Laws:

1. **Innovative (Avoid Bugs by Construction)**: No gratuitous curves. Every contour must satisfy 2-byte word boundaries (`loca[i] % 2 == 0`), bit-7 flag clearing, and zero consecutive identical nodes.
2. **Useful (Life-Critical Acuity)**: Every glyph must maximize recognition under fatigue, stress, and low light (Louise Sloan 5:1 optotype ratio, ISMP disambiguation).
3. **Aesthetic (Harmonic Felt-Marker Warmth)**: Stroke weights and terminal corner radii (locked to 25 UPM) must harmonize with Phil Gear's humanist felt-marker cardstock DNA.
4. **Understandable (Archetypal Semiosis)**: Self-explanatory pictograms (Susan Kare principle). An icon is a hieroglyph, not an illustration. Eliminate ambiguity immediately.
5. **Unobtrusive (Zero Cognitive Friction)**: Monochromatic vector glyphs sharing the luminance and weight of surrounding text. Prohibit multi-color cartoon emoji fallback that hijacks the fovea.
6. **Honest (True to the Vector Engine)**: Pure closed quadratic TrueType contours (`glyf`). No fake skeuomorphic chrome or unhinted micro-artifacts.
7. **Long-Lasting (Timeless Geometry)**: Resist ephemeral stylistic fads. Anchor designs in enduring geometric archetypes (the circle, the golden proportion, the Sloan ratio).
8. **Thorough Down to the Last Detail**: Every coordinate, advance width, side bearing, and bounding box is mathematically intentional. 0 redundant control points (Casey Muratori semantic compression).
9. **Ecological (Digital & Human Energy Conservation)**: Minimal vertex count for O(1) rasterizer performance; Brotli Q11 compression; Scotopic 650nm red mode for zero rhodopsin bleaching and OLED battery conservation.
10. **As Little Design as Possible (Weniger, aber besser)**: Strictly eliminate micro-ticks, decorative filigree, and visual clutter (Edward Tufte 1+1=3 noise) that collapse into blur at <= 16px.

---

## 🚀 Independent Foundry Packaging & Global Distribution

PocketGull maintains independent typefoundry distribution governed by Phil Gear:
- **Global Package Registries**:
  - **Homebrew Cask**: `distribution/homebrew/font-pocketgull.rb` (`brew install --cask font-pocketgull`)
  - **Windows Package Manager (Winget)**: `distribution/winget/PocketGull.Typeface.yaml` (`winget install PocketGull.Typeface`)
  - **Fontsource (NPM)**: `distribution/fontsource/metadata.json` (`npm install @fontsource/pocketgull`)
  - **Adobe Fonts Partner Portfolio**: `distribution/adobe/ADOBE_FONTS_PORTFOLIO.md`
- **Minimalist Versioning (`nameID 5`)**: `Version 3.1.0; The PocketGull Project Authors; OFL 1.1`. `head.fontRevision` locked to exact float `3.1`.
- **Copyright & License**: `nameID 0` matches `OFL.txt` (`Copyright 2026 The PocketGull Project Authors (https://github.com/pocketgull-app/pocketgull-font)`).
- **Zero Reserved Font Names (RFN)**: SIL Open Font License 1.1 with no RFN restriction.
- **Brotli Compression**: WOFF2 binaries compressed at Brotli quality 11.

---

## 🛠️ Mandatory Pre-Flight Verification Chain

Before approving any commit or release:
```powershell
# 1. Forensic W3C OTS & word-alignment audit (Dart 3.11)
dart run tool/pocketgull_foundry.dart audit

# 2. Python Google Fonts pre-flight specification validator
python sources/validate_fonts.py

# 3. Synchronize verified binaries to web app mirror (if app is present)
dart run tool/pocketgull_foundry.dart sync
```
