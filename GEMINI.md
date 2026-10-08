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
- **Let Indigenous Scripts be Sovereign (UNDRIP Accord)**: Adhere strictly to the United Nations Declaration on the Rights of Indigenous Peoples (Articles 11, 13, 14, 24, 31). Zero forced Latinization, unencumbered libre licensing (SIL OFL 1.1) for native schools and publishers, OCAP® data sovereignty, and equal clinical optotype legibility across all tribal orthographies.
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

### 8. Multi-Script Proportions & Grounding (UNDRIP Invariant)
- **Unicode Braille (`U+2800`–`U+28FF`)**: Respects ISO/TR 11548 & ISO 17049 standard 8-dot tactile dome geometry (r = 60 UPM, 2.5 mm pitch, authentic negative space), grounded on Latin baseline (y = 0) to prevent floating cell artifacts.
- **Duployan / Chinuk Pipa (`U+1BC00`–`U+1BC9F`)**: Respects phonemic size ratios (130 UPM vowel loops vs. consonant stems), anchored along the optical waist (y = 270 UPM) to harmonize with Latin x-height.
- **Pan-Tribal Orthographies & Syllabics**: Stacked diacritic elevation (>= 110 UPM clearance for *ą́*, *ę́*, *į́*, *ǫ́*), barred consonant contrast (crossbar >= 1.4x optical aperture for *Ł*, *ł*, *ƛ*), and first-class glottal letter status (*ʼ*, *ʻ*, *ʔ*). Conforms to UNDRIP Articles 11, 13, 14, 24, and 31.

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
  - **Homebrew Tap**: `distribution/homebrew/font-pocketgull.rb` (`brew install --cask pocketgull-app/tap/font-pocketgull`)
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

# 2. Automated SWE Security & CI Regression Tests (Node 24)
npm run test:unit

# 3. Python Google Fonts pre-flight specification validator
python sources/validate_fonts.py

# 4. Synchronize verified binaries to web app mirror (if app is present)
dart run tool/pocketgull_foundry.dart sync
```

---

## 🛡️ CI & SAST Security Invariants
1. **GitHub CodeQL Native Default Setup**: Do **NOT** commit or restore a `.github/workflows/codeql.yml` workflow file. The repository relies on GitHub's native Default Setup (`state: configured`). Adding an advanced workflow causes SARIF upload rejection conflicts.
2. **DOM-Based XSS Prevention**: Never interpolate unescaped user input or URL query parameters into `.innerHTML`. Always construct DOM trees using `textContent`, `document.createTextNode()`, and `document.createElement()`.
3. **Safe HTML & Tag Parsing Invariant (CodeQL Alert 80)**: Never parse or extract `<script>` or other HTML tags using naive regular expressions (e.g. `/<script\b[^>]*>...<\/script>/`). CodeQL flags these under `js/bad-tag-filter`. Use deterministic string boundaries (`indexOf` / `lastIndexOf`) or proper AST / DOM parsers.
4. **Windows Smart App Control & Playwright Sandbox Resilience**: End-to-end browser tests running on Windows host environments must gracefully handle unsigned browser engine launches (such as Playwright WebKit) blocked by Windows Smart App Control or local sandbox policies, falling back cleanly with non-fatal warnings while strictly asserting on available production engines (Chromium / Firefox).
5. **Automated Enforcement**: Enforced at build and pre-flight time via `test/security_and_ci_invariants.test.mjs`.

---

## 📦 Distribution, Supply Chain & Repository Hygiene Invariants

1. **Multi-Channel Distribution Baseline**:
   - **Homebrew Tap**: `pocketgull-app/tap/font-pocketgull` (32 styles).
   - **Windows Package Manager**: `PocketGull.Typeface` (manifests in `distribution/winget/`).
   - **Global Edge CDN (jsDelivr)**: `https://cdn.jsdelivr.net/gh/pocketgull-app/pocketgull-font@3.1.0/fonts.css` (CORS-enabled, zero-quota edge delivery).
2. **Dependabot & CI Python Environment Lock**:
   - CI environment is pinned to Python 3.11. Never merge dependency bumps that require Python >= 3.12 (e.g. `networkx >= 3.7`) without migrating the CI runner first.
   - Respect strict peer constraints (e.g. `fontbakery 1.1.0` pins `freetype-py < 2.4.0`). Keep conflicting major/minor bumps ignored in `.github/dependabot.yml`.
3. **Repository Cleanliness (Google Fonts Project Template Standard)**:
   - Public repository strictly contains open-source code, fonts, build sources, and specimen documentation.
   - Internal business memos, email pitches, legal assignments, and patent disclosures MUST reside in `private/` or `local/` and are strictly ignored by `.gitignore`.
   - Never leave dirty or experimental font binary re-exports in the working tree (`fonts/ttf/`, `fonts/woff2/`).

---

## 🌐 Universal Adoption & Single-Source-of-Truth (SSOT) Versioning Rules

1. **Single Source of Truth (SSOT) SemVer Invariant**:
   - `package.json` (`version: "X.Y.Z"`) is the single source of truth for repository SemVer.
   - OpenType `head.fontRevision` MUST be derived programmatically as decimal float $X + \frac{Y}{10} + \frac{Z}{100}$ (e.g. `3.1.0` $\to$ `3.1`, `nameID 5` $\to$ `"Version 3.100; ..."`).
   - In `fonts.css` and HTML specimens, asset cache-busting query strings (`?v=...`) MUST always match the active package SemVer (`?v=3.1.0`) to eliminate version confusion between OpenType fixed-point floats and SemVer strings.
2. **Unified Variable Font (VF) Default for Web**:
   - Web applications, specimen pages, and CDN integrations MUST prioritize `PocketGull-VF.woff2` (weight 100..900) as the primary font face to prevent loading multi-megabyte cascades of static fonts.
   - Always declare zero-CLS font-metric overrides (`ascent-override`, `descent-override`, `size-adjust: 108%`) to eliminate layout shifts against system fallback optotypes.
3. **Multi-Channel Distribution Parity**:
   - Any version release MUST synchronize simultaneously across:
     - **Homebrew Tap**: `distribution/homebrew/font-pocketgull.rb`
     - **Windows Package Manager**: `distribution/winget/PocketGull.Typeface/`
     - **LaTeX CTAN Package**: `distribution/latex/` (`pocketgull-math.sty`)
     - **Python Telemetry Package**: `distribution/python/` (`pocketgull_math/__init__.py`)
     - **Cryptographic Hashes**: `fonts/sri-hashes.json`, `fonts/SHA256SUMS`, and `CHECKSUMS.sha256`
   - Release archive generation (`pocketgull-font-vX.Y.Z.zip`) is automated via the Dart foundry toolchain, eliminating manual checksum drifts.
4. **Sub-Second Acuity & Fast Loading (HCI Invariant)**:
   - Only preload critical display fonts (`PocketGull-Fineliner.woff2`, `PocketGull-Bold.woff2`, or `PocketGull-VF.woff2`).
   - All secondary/specialty fonts (`Math`, `Emoji`, `ASL`) MUST declare `font-display: swap` and be loaded lazily on demand.



