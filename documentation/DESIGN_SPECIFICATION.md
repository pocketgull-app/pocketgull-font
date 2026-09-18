# PocketGull Font Design Specification (v4.0.0)

## 1. Design Vision

**PocketGull** is an open-source, mathematically unified clinical vector font superfamily. Engineered for life-critical healthcare computing, digital health platforms, and high-stress clinical environments, PocketGull harmonizes tactile humanist warmth with zero-error ophthalmological legibility.

### Current Status (v4.0.0 — Production Google Fonts Standard)

| Metric | Value |
|--------|-------|
| Master Glyphs | 820+ Fully Formed Vectors |
| UPM Grid | **1000 UPM TrueType Standard** |
| Vertical Metrics | $CAP = 720$, $XH = 480$, $BL = 0$, $DSC = -180$ |
| Optical Stroke Aspect | Louise Sloan 5:1 Optotype Ratio (Snellen 20/20 & LogMAR 0.0) |
| Lateral Spacing | Herman Bouma Anti-Crowding Law ($b > 0.5 \times \theta$) |
| Braille Coverage | Complete 256 Unicode Braille Patterns Block (`U+2800`–`U+28FF`) |
| Font Variants | 4 Core Golden Masters (`Bold`, `Fineliner`, `Chiseltip`, `Mono`) |
| GSUB Features | `zero` (slashed 0), `cv05` (curved l), `ss02` (serifed I for IL-6/IgA), `tnum`, `liga` |
| Sanity & Safety | 100% W3C OTS Compliant (0 bit-7 flags, word-aligned tables) |
| License | SIL Open Font License 1.1 |

---

## 2. Standard 1000 UPM Grid & Coordinate System

Conforming to modern OpenType and Google Fonts engineering conventions:
- **Units Per Em (UPM)**: 1000
- **Cap Height**: 720 UPM
- **Ascender**: 780 UPM
- **x-Height (Display Master)**: 500 UPM
- **x-Height (Text & Reading Standard)**: 538 UPM (effective $53.8\%$ via `size-adjust: 108%` web volume equalization)
- **Baseline**: 0 UPM
- **Descender**: -180 UPM
- **Line Gap**: 100 UPM

All coordinates feature clockwise outer contours and counter-clockwise inner counter loops, with Bézier inflection control points locked to integer coordinates.

---

## 3. Stroke Anatomy & Optical Physics

- **Vertical Stems**: Bold felt-tip marker structure with organic calligraphic curvature.
- **Terminal Caps**: Continuous $G^2$ filleted rounded corners simulating wet felt marker ink-bleed without harsh pixel clipping.
- **Apertures & Counters**: Expanded $160\text{ UPM}$ internal apertures in `e`, `c`, `s`, `a`, and `o` to prevent ink/pixel fill-in at small sizes (10–14pt) and low-resolution 203 DPI thermal label printers.
- **45° Retinal Inktraps**: Stress-relief junction inktraps at acute diagonal intersections (`M`, `W`, `N`, `v`, Cyrillic `ж`, `щ`) preventing visual clotting under rasterization.
- **Vertical-LR Script Scaling**: 1.18× Optical Scale Invariant (`size-adjust: 118%`) for Traditional Mongolian (`U+1800`–`U+18AF`) and Manchu to achieve optical parity with Latin x-height.
- **ISMP Symmetrical Serifs**: Capital `I` features bilateral horizontal serifs at cap-height and baseline to unequivocally eliminate confusion with lowercase `l` and numeral `1` in critical biomarkers (`IL-6`, `IgA`).

---

## 4. Superfamily Styles & Release Binaries

| Master Style | PostScript Name | Weight | Primary Purpose |
|--------------|-----------------|:------:|-----------------|
| **PocketGull Bold** | `PocketGull-Bold` | 700 / 800 | Display headers, brand lettering, Bionic fixation anchors |
| **PocketGull Fineliner** | `PocketGull-Fineliner` | 400 | Long-form clinical notes, EHR documentation, patient leaflets |
| **PocketGull Chiseltip** | `PocketGull-Chiseltip` | 900 | $45^\circ$ calligraphic chamfers for emergency placards & alarms |
| **PocketGull Mono** | `PocketGullMono-Regular` | 500 | Fixed 600 UPM pitch for vitals telemetry, ECG waveforms, and CLI |

---

### 4.5 Sparse Mixture of Experts (SMoE) Architecture (Experts A–T)

PocketGull routes multi-script typography dynamically via 20 specialized SMoE experts, avoiding monolithic font bloat while guaranteeing zero Cumulative Layout Shift (CLS = 0.000):
- **Expert A (`LATN` / `BRL`)**: Latin Core, ISMP Safety & 256-Glyph Braille (`U+0020-00FF`, `U+2800-28FF`)
- **Expert B (`CANS`)**: Canadian Aboriginal Syllabics (`U+1400-167F`)
- **Expert C (`DUPL`)**: Chinuk Pipa & Duployan Shorthand (`U+1BC00-1BC9F`)
- **Expert D (`TFNG`)**: Neo-Tifinagh Amazigh (`U+2D30-2D7F`)
- **Expert E (`CHER`)**: Cherokee Syllabary (`U+13A0-13FF`, `U+AB70-ABBF`)
- **Expert F (`ETHI`)**: Ethiopic / Ge'ez Abugida (`U+1200-137F`)
- **Expert G (`ADLM` / `VAII`)**: West African Sovereign Scripts (`U+1E900-1E95F`, `U+A500-A63F`)
- **Expert H (`ARAB`)**: Arabic & Perso-Arabic (`U+0600-06FF`)
- **Expert J (`HEBR`)**: Hebrew & Aramaic (`U+0590-05FF`)
- **Expert K (`DEVA`)**: Indic Core & South Asian (`U+0900-0D7F`)
- **Expert L (`CJK`)**: CJK Unified Ideographs & Kana (`U+4E00-9FFF`)
- **Expert SE Asian**: Thai, Lao, Khmer, Burmese, Tibetan (`U+0E00-17FF`)
- **Expert M (`MONG`)**: Traditional Mongolian & Manchu (`U+1800-18AF`, `U+11660-1167F`)
- **Expert N (`NKOO`)**: N'Ko Alphabet (`U+07C0-07FF`)
- **Expert O (`OSGE`)**: Osage Sovereign Siouan (`U+104B0-104FB`)
- **Expert P (`OGHM`)**: Ogham Celtic Tree Alphabet (`U+1680-169F`)
- **Expert Q (`ORKH`)**: Old Turkic / Orkhon Runes (`U+10C00-10C4F`)
- **Expert R (`SIGN`)**: Sutton SignWriting (`U+1D800-1DAAF`)
- **Expert S (`CARD`)**: ICU Sub-Cell ECG & Telemetry (`U+E000-E0FF`)
- **Expert T (`BLIS`)**: Blissymbolics AAC Communication (`U+E100-E17F`)

---

## 5. Directory Hierarchy (Google Fonts Standard)

```
pocketgull-typeface/
├── fonts/
│   ├── ttf/                         <-- Desktop OFL TrueType submission
│   └── woff2/                       <-- Compressed webfonts for web & npm
├── sources/                         <-- Canonical build scripts (compile_superfamily.py)
├── documentation/                   <-- Specifications & image assets
├── index.html                       <-- Interactive Web Specimen & Live Studio
├── METADATA.pb                      <-- Google Fonts upstream specification
├── OFL.txt                          <-- SIL Open Font License 1.1
└── DESCRIPTION.en_us.html           <-- fonts.google.com catalog copy
```
