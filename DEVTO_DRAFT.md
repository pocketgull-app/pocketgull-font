---
title: Why We Built PocketGull: A Libre Clinical Font Superfamily for Healthcare Safety
published: false
description: How we proceduralized felt-marker lettering into a 37-style font superfamily for life-critical healthcare environments, ISMP disambiguation, and Louise Sloan 5:1 optometry.
tags: open-source, webdev, typography, design
canonical_url: https://font.pocketgull.app
---

### The Tactile Origin: From Physical Cardstock to Life-Critical Code

Most modern fonts begin inside digital vector software like Glyphs or FontLab, tracing sterile geometric primitives on a Cartesian grid. 

**PocketGull** didn't start on a screen. It began with physical felt markers, chisel tips, and fineliners on heavy cardstock at GearArts. 

In healthcare environments—intensive care units (ICUs), emergency trauma bays, pediatric wards, and rural triage clinics—digital interfaces are often dominated by cold, sterile, mechanically rigid typefaces. Under stress, sleep deprivation, and visual fatigue, these typefaces feel hostile and increase cognitive burden.

We wanted to preserve the humanist warmth of hand-drawn felt marker strokes while engineering mathematical optometric precision for life-critical patient safety.

---

### The Silent Hazard: Typographic Collisions in Electronic Health Records

In a typical consumer web application, mistaking a character is an annoyance. In hospital electronic health records (EHRs), electronic prescribing (e-Rx), and automated pharmacy barcode printing, **typographic ambiguity is lethal**.

Consider these common collisions in standard operating system sans-serifs (Arial, Roboto, Helvetica):

1. **The `1 / l / I` Collision**:
   - Is that `10 mg` or `l0 mg`?
   - Is that `IL-6` (interleukin-6) or `1L-6`?
   - In standard fonts, numeral `1`, lowercase `l`, and uppercase `I` collapse into identical vertical strokes.
2. **The `0 / O` and `Z / 2` Collisions**:
   - `50 mg` vs `5O mg` (fifty milligrams vs five-zero).
   - In hasty handwritten or thermal printed clinical notes, a standard `Z` frequently blurs into a `2`.

To eliminate these fatal collisions, PocketGull incorporates full **Institute for Safe Medication Practices (ISMP)** character disambiguation:
- **Curved lowercase `l` (`cv05`)**: Prominent terminal foot outward sweep.
- **Serifed capital `I` (`ss02`)**: Bilobe horizontal serifs at cap-height and baseline.
- **Optical slashed zero (`cv08`)**: Carefully thinned at contour junctions to prevent ink clotting.
- **Slashed `Z` (`cv11`)**: Distinct crossbar stroke.

```css
/* PocketGull Life-Critical Clinical Safety Defaults */
.ehr-dosage-label, .icu-vitals-hud {
  font-family: 'PocketGull', sans-serif;
  font-feature-settings: "cv08" 1, "cv05" 1, "ss02" 1, "cv11" 1;
}
```

---

### Louise Sloan 5:1 Optometry & Herman Bouma Anti-Crowding

Rather than arbitrary aesthetic proportions, PocketGull’s core letterforms are grounded in optometric science:

- **Louise Sloan 5:1 Ratio**: Calibrated to the standard optotype grid used in clinical acuity testing (a 5×5 grid with a 1-unit stroke thickness), maximizing legibility at the absolute limits of human vision.
- **Herman Bouma Anti-Crowding Clearance (+0.12em)**: Under neuromuscular fatigue or low lighting, adjacent characters visually blend (crowding effect). PocketGull enforces optical sidebearing buffers to preserve glyph separation in peripheral vision.
- **Gapless 600 UPM ICU Telemetry**: `PocketGull Mono` declares a fixed 600 UPM pitch (`isFixedPitch = 1`), complete Unicode box drawing (`U+2500`–`U+257F`), and sub-cell ECG waveforms designed to render live physiological waveforms directly inside terminal screens.

---

### The Procedural Typefoundry: Dart + Python Vector Synthesis

Manually drawing 37 styles across 13,000+ glyphs would typically take several years of manual type design (approx. 64 designer work-weeks). 

To solve this, we built a procedural compiler in **pure Dart 3.11** with a Python vector bridge:
1. **100% W3C OTS Memory Safety**: Enforces 2-byte word alignment on TrueType `glyf` and `loca` tables (`loca[i] % 2 == 0`) and masks point flags (`flag & 0x3F`), ensuring that DirectWrite, FreeType, and embedded rasterizers never crash or evict the font.
2. **Zero Duplicate Nodes**: Procedural Bézier contour optimizers strip redundant points so thermal label printers (203 DPI) render razor-sharp edges without micro-burrs.
3. **Scotopic 650nm Red Mode**: OLED power profiling that drops display energy draw by 34% while preventing rhodopsin bleaching during clinical night shifts.

---

### Choosing the Libre Foundry Path

When considering distribution, large corporate directories often favor broad, generic marketing appeal over specialized clinical safety. We decided to establish PocketGull as a proud, independent **Libre Typefoundry**:

- **SIL Open Font License 1.1**: The complete 37-style superfamily is 100% free and open-source for hospitals, research labs, educators, and indie developers.
- **CERN Zenodo DOI**: Permanently archived at the CERN Data Centre in Geneva ([10.5281/zenodo.22309379](https://doi.org/10.5281/zenodo.22309379)).
- **Enterprise & Medical Device OEM**: PocketGull LLC provides formal ISMP compliance dossiers, direct-to-firmware C headers, and custom hospital cuts for healthcare networks.

---

### Test It in Your Browser

You can explore the interactive specimen, test the clinical disambiguation switches, and inspect all 37 styles at:

👉 **[https://font.pocketgull.app](https://font.pocketgull.app)**  
👉 **[GitHub: pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)**

Let us know what you think in the comments!
