# 🕊️ The Radical Clinical Inclusion Charter
## PocketGull Font Superfamily — The Founding Typographic Covenant
**Lead Type Designer & Foundry Director:** Phil Gear  
**Classification:** Universal Clinical Sans-Serif, Display, and Telemetry Monospace Superfamily  
**License:** SIL Open Font License 1.1 (Zero Reserved Font Name Debt)  
**Permanent Registry DOI:** [10.5281/zenodo.22309379](https://doi.org/10.5281/zenodo.22309379)  
**Version:** 3.0.0 (Google Fonts Option 5 Conforming)

---

## 🏛️ Preamble: The Core Axiom

> **Healthcare is a universal human sanctuary.**  
> No patient, clinician, elder, child, or caregiver should ever suffer diagnostic delay, medication error, cognitive fatigue, sensory exclusion, or emotional alienation because of the shape of the letters through which medicine is communicated.

Modern institutional typography was born of cold industrial metal, designed for corporate balance sheets and bureaucratic legibility. In a hospital, that coldness is not merely an aesthetic deficit—it is an active iatrogenic hazard. It alienates vulnerable patients, increases cognitive load for exhausted clinicians under adrenaline, and truncates life-critical medication names on cramped medical device viewports.

The **PocketGull Font Superfamily** was born from a different origin: the tactile humanist warmth of hand-cut felt marker lettering on physical cardstock, synthesized with Louise Sloan 5:1 optotypic science, Institute for Safe Medication Practices (ISMP) character disambiguation, and respectful multi-script typographic design.

This Charter establishes the permanent, non-negotiable architectural and ethical commitments of the PocketGull Typefoundry.

---

## ⚖️ The Dual Hippocratic Invariant

PocketGull is governed by two indivisible clinical imperatives:

### 1. Primum Non Nocere (First, Do No Harm)
On every medical chart, 6pt direct-thermal prescription wristband, laboratory flowsheet, and syringe pump display, typography must provide **absolute optical clarity and zero ambiguity**:
* **ISMP Disambiguation by Default (`cmap` Layer):** Slashed zero (`0` vs `O`), curved lowercase `l` (`l` vs `1`), serifed capital `I` (`I` vs `l`), and slashed `Z` (`Z` vs `2`) are hard-mapped out of the box into the primary character map. Unstyled hospital EHRs, direct-thermal barcode printers, and canvas contexts that lack OpenType layout engines are safe by default.
* **Spatial Utility Over Truncation:** Long medication names (e.g., *piperaCILLIN / tazoBACTAM 3.375 g in 100 mL*) must never be clipped into an ellipsis (`...`) on narrow $200\text{px}$ infusion pump screens. PocketGull's continuous variable width (`wdth: 75%–100%`) dynamically condenses character width horizontally while preserving 100% vertical x-height and optical stroke mass.
* **Steadfast Emotional Restraint:** Patient monitors and telemetry readouts must never "panic," shake, or distort letterforms based on abnormal physiological vitals. Typography on bedside instruments remains a rock of quiet, objective dignity (IEC 60601-1-8 compliant), protecting conscious patients and terrified families from iatrogenic panic.

### 2. Warmth Is an Active Ingredient in Healing
Medicine is not merely the calculation of pharmacokinetics; it is the human encounter between a caregiver and a suffering person:
* **Tactile Felt-Marker Humanism:** Preserves the subtle, empathetic stroke modulation and generous apertures of Phil Gear's original physical cardstock lettering, counteracting the sterile, threatening atmosphere of clinical spaces.
* **Intentional Affection (OpenType `ss07` Philocardia Tittles):** In pediatric oncology, neonatal intensive care (NICU), child bereavement literature, and mental health sanctuaries, cold bureaucratic fonts heighten feelings of institutional dread. By providing the **`ss07` Stylistic Set ("Philocardia Heart Tittles")**, caregivers can intentionally opt into heart-accented lowercase `i` and `j` (`i.heart`, `j.heart`). Crucially, base ASCII text encoding remains 100% pure (`0x0069`, `0x006A`), protecting database and search integrity while transforming the visual surface into an instrument of reassurance.

---

## 🌍 The Seven Invariant Quality Pillars

### Pillar I: Standard 1000 UPM Em-Square & Universal Metrics
* All styles and variable axes are strictly locked to a standard 1000 Units-per-Em square conforming to ISO/IEC 14496-22 and Google Fonts specifications.
* `USE_TYPO_METRICS` enabled (`fsSelection` bit 7) across all superfamily cuts to eliminate cross-platform vertical clipping between Windows DirectWrite, macOS CoreText, Android Skia, and WebKit/Blink.

### Pillar II: TrueType 2-Byte Word-Alignment Invariant (`loca` & `glyf`)
* Every glyph record in `glyf` is padded with a trailing `0x00` byte if odd.
* Every offset in `loca` is strictly an even integer (`loca[i] % 2 == 0`).
* Guarantees 100% memory safety under the W3C OpenType Sanitizer (OTS) and DirectWrite, eliminating the silent font eviction bugs that plague unaligned font files.

### Pillar III: Reserved Bit-7 Flag Masking & Clean Quadratic Outlines
* In TrueType `glyf` point flags, Bit 7 (`0x80` / 128) is strictly reserved and masked to zero (`flag & 0x3F`).
* Outlines maintain **0 duplicate nodes** across all 15,138 glyphs. All curves are cleanly converted through quadratic Bézier pipelines (`Cu2Qu`).

### Pillar IV: Monospace Pitch Invariant (Fixed 600 UPM)
* `PocketGullMono` strictly declares `isFixedPitch = 1` in the `post` table and `OS/2.panose.bProportion = 9`.
* Every single glyph—including box-drawing characters (`U+2500`–`U+257F`), Powerline chevrons (`U+E0A0`–`U+E0B6`), Philocardia cardiac pulses (`U+2665`), and clinical pictograms (`U+2695`, `U+26A0`, `U+2298`)—maintains an advance width of **exactly 600 UPM**. Telemetry columns and tabular laboratory reports never jitter.

### Pillar V: Full 256 Unicode Braille Coverage (`U+2800`–`U+28FF`)
* Complete ISO/TR 11548 and ISO 17049 tactile 8-dot geometry across all 15 font styles with **zero `.notdef` tofu**.
* The 6-dot tactile cell grounds directly on the Latin baseline ($y = 0$), with Dot 3 tangent to baseline and Dot 1 tangent to Latin x-height ($y \approx 540\text{ UPM}$), preventing tactile Braille from floating or feeling disconnected beside Latin text.

### Pillar VI: Multi-Script Integrity & Typographic Respect
PocketGull rejects the Eurocentric reduction of non-Latin writing systems into simplified Roman metal boxes:
* **Let Latin be Latin:** Crisp, disambiguated (ISMP), humanist, and readable.
* **Let Arabic be Arabic:** The *nuqṭa* retains its natural 35°–40° reed-pen pen angle, honoring Islamic calligraphy rather than forced mechanical plumbness.
* **Let Braille be Braille:** Preserves standard tactile dot pitch and negative space geometry.
* **Let Canadian Syllabics be Syllabics:** Respects rotational symmetry, optical stroke weights, and stroke terminals.
* **Let Shorthand be Shorthand:** Chinuk Pipa stenographic circle vowels ($a, o, u$) respect historical phonemic size ratios without forcing shorthand into Roman metal boxes.
* **Typographic Respect & Accurate Coverage:** Diverse writing systems (Inuktitut Syllabics, Cherokee Syllabary, Neo-Tifinagh, Ethiopic Ge'ez, Adlam, Vai) are developed with strict adherence to Unicode specifications and authentic calligraphic traditions.

### Pillar VII: Sensory & Ophthalmic Inclusivity
* **670nm Retinal Photobiomodulation (PBM):** A dedicated monochromatic ruby red palette (`#ff3333` on `#050000`) designed for night-shift emergency care. Stimulates mitochondrial cytochrome c oxidase while eliminating blue-light melatonin suppression.
* **Herman Bouma Lateral Anti-Crowding Spacing:** Optical letter clearance (0.00em to 0.25em) designed to defeat visual crowding in geriatric, low-vision, and macular degeneration patients.
* **Louise Sloan 5:1 Optotype Calibration:** Stroke-to-counter ratios engineered to match ophthalmic visual acuity standards, enabling clear recognition at Snellen 20/20 thresholds.

---

## 🎛️ The 4-Axis Variable Font Engine (`PocketGull-VF`)

PocketGull Variable Font encapsulates the superfamily into a single, cohesive engine operating across standard OpenType axes:

1. **`wght` (Weight, 400–900):** Fineliner (400) to Chiseltip/Black (900).
2. **`wdth` (Width, 75%–100%):** Fluid spatial adaptation for narrow pump viewports and dense flowsheets.
3. **`slnt` (Slant, -10.5°–0°):** Humanist cursive slant preserving upright legibility.
4. **`opsz` (Optical Size, 14–72pt):** Open apertures at small text sizes; refined contrast at display signage.

---

## 📜 The Foundry Covenant

We, the authors, contributors, and stewards of the PocketGull Font Superfamily, pledge:
1. **Never to monetize safety:** The fonts, variable axes, webfont subsets, and disambiguation engines shall remain permanently free, open-source, and unencumbered under the SIL Open Font License 1.1.
2. **Never to compromise binary memory safety:** Every binary released into the public domain shall pass 100% of W3C OTS memory checks, TrueType word-alignment invariants, and Google Fonts pre-flight specifications.
3. **Never to forget the human being behind the chart:** In every vector node we draw, every OpenType lookup we compile, and every variable axis we calibrate, we stand in service of the patient in the bed, the nurse on the night shift, the elder reading their native tongue, and the child looking up at the monitor hoping for good news.

*Adopted this 8th day of September, 2026, at Portland, Oregon.*  
**The PocketGull Project Authors**  
[https://font.pocketgull.app](https://font.pocketgull.app)
