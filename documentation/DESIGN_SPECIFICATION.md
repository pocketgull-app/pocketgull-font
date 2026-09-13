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
- **x-Height**: 480 UPM
- **Baseline**: 0 UPM
- **Descender**: -180 UPM
- **Line Gap**: 100 UPM

All coordinates feature clockwise outer contours and counter-clockwise inner counter loops, with Bézier inflection control points locked to integer coordinates.

---

## 3. Stroke Anatomy & Optical Physics

- **Vertical Stems**: Bold felt-tip marker structure with organic calligraphic curvature.
- **Terminal Caps**: Continuous $G^2$ filleted rounded corners simulating wet felt marker ink-bleed without harsh pixel clipping.
- **Apertures & Counters**: Deeply scooped internal apertures in `e`, `c`, `s`, `a`, and `o` to prevent ink/pixel fill-in at small sizes (10–12pt) and low-resolution 203 DPI thermal label printers.
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
