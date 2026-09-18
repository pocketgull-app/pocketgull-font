# PocketGull Accessibility & Neuro-Ergonomic Typographic Specification

**The PocketGull Font Superfamily**  
*A Clinical, Optometric & Neuro-Ergonomic Typographic Architecture for Life-Critical Environments*

**Lead Architect**: Phil Gear & The PocketGull Project Authors  
**Standard**: Google Fonts Specification, OpenType 1.9, Louise Sloan 5:1 Optotypes, ISMP / FDA CDRH Guidelines, WCAG 2.2 AAA  
**Version**: 3.2.0  

---

## 🏛️ 1. Executive Summary & Problem Space

Clinical, diagnostic, and emergency software demands typographic systems that exceed standard aesthetic graphic design conventions. When a patient in an intensive care unit (ICU) is non-verbal, when a flight medic operates a tablet in a vibrating medical helicopter, when a color-blind clinician reviews telemetry under flickering fluorescent lights, or when a dyslexic nurse verifies a chemotherapy dosage after a 12-hour shift, character misinterpretation introduces severe clinical hazards.

This specification formalizes the **PocketGull Accessibility (A11y) & Neuro-Ergonomic Typographic Architecture**, establishing deterministic mathematical, optometric, and cognitive invariants across six core domains.

```
+-----------------------------------------------------------------------------+
|               POCKETGULL ACCESSIBILITY ARCHITECTURAL DOMAINS                |
+------------------------------------+----------------------------------------+
| 1. Low Vision & Aging Eyes         | Retinal Irradiation (IRRD) & MTF Cutoff|
| 2. Neurodiversity & Dyslexia       | Mirror Disambiguation & Bouma Crowding |
| 3. Clinical Telemetry & Motion     | Monochromatic Enclosures & Vibration   |
| 4. Assistive Tech & Screen Readers | Strict Unicode & Nemeth Braille Duality|
| 5. Non-Verbal ICU AAC              | Wong-Baker FACES & Need Pictograms     |
| 6. Multi-Sensory Wayfinding        | Slice-Ready 3D Tactile Profiles        |
+------------------------------------+----------------------------------------+
```

---

## 👁️ 2. Domain 1: Low Vision, Aging Eyes & Optometric Acuity

### 2.1 Retinal Irradiation / Halation Compensation in Dark Mode (`IRRD` / `ss15`)
* **The Optical Phenomenon**: When bright white text ($\ge 250\text{ cd/m}^2$) is viewed against true-black OLED backgrounds in dark environments, corneal aberrations, early-stage cataracts, and high astigmatism induce **optical halation (irradiation)**. Light from high-luminance stroke vectors scatters across the retinal fovea, bleeding inward into enclosed counters. Delicate letter loops (`e`, `a`, `s`, `B`, `8`) get visually choked by glare, triggering visual fatigue, loss of word-shape recognition, and photophobia.
* **The Mathematical Compensation Formula**:
  $$\text{Stroke}_{\text{Dark}} = \text{Stroke}_{\text{Light}} \times (1 - \delta_{\text{irrd}}), \quad \delta_{\text{irrd}} \in [0.03, 0.05]$$
  $$\text{Counter}_{\text{Dark}} = \text{Counter}_{\text{Light}} + \Delta_{\text{counter}}, \quad \Delta_{\text{counter}} \ge 15\text{ UPM}$$
* **Implementation**:
  * An Irradiation Compensation mode (`.pg-irrd-compensated` or stylistic set `ss15`) reduces stroke weight by exactly $4\%$ while dilating inner counter-apertures by $15\text{ UPM}$ specifically on obsidian and OLED black themes (`background: #000000` / `#060912`), neutralizing optical glare before it strikes the retina.

### 2.2 Aperture Collapse Prevention under Loss of Contrast Sensitivity (MTF Cutoff)
* **The Optical Phenomenon**: In aging eyes, diabetic retinopathy, and macular degeneration, the eye's Modulation Transfer Function (MTF) drops sharply at spatial frequencies above $6\text{ cycles/degree}$. Closed-aperture fonts (e.g., Helvetica, Arial) featuring curled terminals cause characters like `c`, `e`, `o`, and `s` to collapse into solid dark blobs.
* **The PocketGull Invariant**:
  * All curved terminals terminate at distinct $45^\circ$ or $90^\circ$ outward vectors with an aperture opening $\ge 200\text{ UPM}$ on the standard 1000 UPM em-square (the Louise Sloan 5:1 optotype standard).
  * This guarantees that even when retinal image blur exceeds LogMAR 0.6, the character envelope remains open and identifiable.

---

## 🧠 3. Domain 2: Neurodiversity & Cognitive Accessibility (Dyslexia, ADHD, TBI)

### 3.1 Asymmetric Mirror Inversion Disambiguation
* **The Neurological Phenomenon**: The human visual cortex has an innate biological evolutionary bias toward "mirror invariance" (recognizing a predator regardless of whether it faces left or right). For dyslexic readers and individuals with developmental coordination differences, this symmetry causes rotational letter confusion between reversible pairs: `b` ↔ `d`, `p` ↔ `q`, `n` ↔ `u`, and `m` ↔ `w`.
* **PocketGull Asymmetric Invariant Matrix**:
  | Confusable Pair | Glyph A (Invariant Feature) | Glyph B (Invariant Feature) | Asymmetry Delta |
  | :--- | :--- | :--- | :--- |
  | **`b` vs `d`** | Straight ascender with $45^\circ$ spur at $y=780$; weighted lower bowl. | Curved neck terminal at $y=780$ with open counter entry angle. | Ascender apex and bowl juncture asymmetry ($>40\text{ UPM}$). |
  | **`p` vs `q`** | Descender with $30\text{ UPM}$ vertical overshoot above baseline. | Distinct $35^\circ$ diagonal terminal exit foot at baseline. | Terminal foot presence vs. continuous descender drop. |
  | **`n` vs `u`** | Flat bilateral shoulder arch ($y=540$) with left baseline foot. | Curved trough cradle ($y=0$) with right vertical exit stem. | Asymmetric vertical tension and terminal stroke ends. |
  | **`m` vs `w`** | Rounded double arches grounded on baseline; center stem reaches baseline. | Sharp angled apexes with inverted $15^\circ$ diagonal outward flair. | Angular vs. arch contour topology. |

### 3.2 Herman Bouma Visual Crowding Alleviation (`TRCK` / `ss16`)
* **The Neurological Phenomenon**: Under Herman Bouma's Law, lateral masking (visual crowding) in peripheral vision occurs within a critical distance $r \approx 0.5 \times \text{eccentricity}$. In dyslexia and visual stress, inter-letter lateral interference degrades reading speed and causes saccadic regression.
* **The Specification**:
  * PocketGull incorporates a dynamic Tracking / Crowding Relief mode (`.pg-crowding-relief` / `ss16`):
    * Letter-spacing expanded by $+0.12\text{em}$ ($+120\text{ UPM}$).
    * Word-spacing expanded by $+0.18\text{em}$ ($+180\text{ UPM}$).
    * Conforms directly to the **British Dyslexia Association (BDA)** and **WCAG 2.2 Success Criterion 1.4.12 (Text Spacing)**.

### 3.3 Fixation Saccade Anchors (Bionic Reading)
* **The Mechanism**: Readers with ADHD, traumatic brain injuries (TBI), or post-ICU cognitive exhaustion benefit from visual fixation anchors that guide eye saccades through dense multi-paragraph clinical notes.
* **The Specification**:
  * Initial consonant/vowel clusters of content words are dynamically weighted with `font-weight: 700` (`PocketGull-Bold`) while remaining syllables render in `PocketGull-Fineliner` (`font-weight: 400`), generating an effortless cognitive rhythm across diagnostic summaries.

---

## ⚡ 4. Domain 3: Clinical & Life-Critical Telemetry (Color Blindness & High-Stress Motion)

### 4.1 Monochromatic Redundancy for Color-Blind Clinicians (WCAG 2.2 SC 1.4.1)
* **The Problem**: Over $8\%$ of male clinicians and $0.5\%$ of female clinicians live with congenital color vision deficiencies (Deuteranopia, Protanopia, Tritanopia). Modern telemetry monitors rely heavily on color-coding alone (green for normal, amber for warning, red for critical alarm). In high-stress triage or black-and-white printouts (thermal strips, faxed lab reports), color information is completely erased.
* **The PocketGull Invariant**:
  * Every telemetry status indicator is bound to a **geometric enclosure badge** that provides $100\%$ visual comprehension without relying on color:
    1. **`[CRIT]`**: Double-walled regular octagon ($\ge 8\text{-sided}$ perimeter) conveying maximum boundary alert.
    2. **`▲HIGH`**: Equilateral upward-pointing solid triangle indicating super-threshold elevation.
    3. **`▼LOW`**: Equilateral downward-pointing solid triangle indicating sub-threshold depression.
    4. **`◆HOLD`**: Regular $45^\circ$ diamond indicating paused or manual override states.
    5. **`●NORM`**: Continuous circular pill indicating stable baseline telemetry.
  * All badges share exact tabular advance metrics ($600\text{ UPM}$ or $1200\text{ UPM}$), guaranteeing **Zero Cumulative Layout Shift (CLS = 0)** when an alarm triggers.

### 4.2 High-Vibration Legibility (Ambulances & HEMS Helicopters)
* **The Problem**: Ground ambulances and emergency medical helicopters subject clinician tablets to high-amplitude vibration in the $4\text{--}12\text{ Hz}$ frequency range. Delicate hairpins, thin crossbars, and unbracketed serifs disappear into retinal motion blur.
* **The Invariant**:
  * Minimum optical stroke floor: every visible vector stem in PocketGull maintains a stroke thickness $\ge 75\text{ UPM}$ ($0.075\text{em}$), ensuring characters survive extreme mechanical vibration without spatial dissolution.

---

## 🔊 5. Domain 4: Assistive Technology (AT) & Screen Reader Symbiosis

### 5.1 Strict Unicode Semantic Mapping (No PUA Misuse)
* **The Problem**: Poorly engineered "icon fonts" and medical fonts map critical symbols to Private Use Area (PUA) codepoints or replace letters with unpronounceable ligature sequences, causing screen readers (NVDA, JAWS, Apple VoiceOver, Android TalkBack) to speak incomprehensible jargon or skip life-critical dosages.
* **The PocketGull Invariant**:
  * **Slashed Zero**: Always encoded as standard ASCII `0` (`U+0030`) with OpenType `cv08` substitution. Screen readers speak *"zero"*, never *"diameter"* or *"null set"*.
  * **Curved `l`**: Always encoded as standard ASCII `l` (`U+006C`) with OpenType `cv05` substitution. Screen readers speak *"ell"*, never *"one"*.
  * **Tall-Man Lettering**: Encoded using standard uppercase Latin codepoints (`DOXOrubicin` vs `DAUNOrubicin`). Screen readers pronounce the phonemes accurately without tripping over synthetic PUA characters.

### 5.2 Dual Visual / Nemeth Braille Code STEM Duality
* **The Architecture**: PocketGull integrates mathematical telemetry symbols with tactile **Nemeth Braille** representations within the `U+2800`–`U+28FF` block:
  * Sighted educators, clinicians, and blind STEM students can review simultaneous parallel streams of visual math and 8-dot Nemeth Braille without translation drift.

---

## 🤝 6. Domain 5: Non-Verbal ICU Communication & Augmentative/Alternative Communication (AAC)

### 6.1 Direct Vector Glyphs for Intubated & Non-Verbal Patients
* **The Problem**: Intubated ICU patients, acute stroke survivors experiencing expressive aphasia, and individuals living with ALS or cerebral palsy rely on emergency communication boards. These boards frequently depend on raster image libraries (PNG/JPEG) that suffer from bandwidth latency, pixelation, or broken URLs.
* **The PocketGull Invariant**:
  * Embed standard clinical communication pictograms natively into the vector font:
    1. **Wong-Baker FACES Pain Rating Scale ($0\text{--}10$)**:
       * `0`: No Hurt (wide smiling curve, open relaxed eyes).
       * `2`: Hurts Little Bit (gentle smile, level gaze).
       * `4`: Hurts Little More (straight neutral mouth, attentive eyes).
       * `6`: Hurts Even More (slight downturned mouth, furrowed brow).
       * `8`: Hurts Whole Lot (pronounced frown, squinting eyes).
       * `10`: Hurts Worst (deep weeping frown, closed crying teardrops).
    2. **Core Physiological Need Glyphs**:
       * `NEED_WATER`: Teardrop tumbler with water wave silhouette.
       * `NEED_PAIN`: Anatomical human silhouette with localized radial starburst.
       * `NEED_TEMP`: Thermometer with dual snowflake / sun heat indicators.
       * `NEED_REPOSITION`: Bed frame with $180^\circ$ rotational arrows.
       * `NEED_FAMILY`: Two holding hands silhouette.
       * `NEED_SUCTION`: Suction catheter cannula with airflow vectors.
  * All glyphs scale losslessly, inherit CSS `currentColor`, render instantly without network latency, and support direct Web Speech API synthesis on selection.

### 6.2 Bedside Co-Creation, Community Translations & Neural Speech Synthesis
* **The Clinical Need**: Patients in ICU recovery, palliative care, or stroke rehabilitation experience distinct personal needs ("Hold my hand", "Grandkids photos", "Pet dog", "Glasses") that no static vocabulary covers. Furthermore, diverse patient populations require immediate bedside communication in their native tongue without cumbersome translation delays.
* **The PocketGull Invariant**:
  1. **Bedside Co-Creation Protocol**: Caregivers, speech-language pathologists (SLPs), or family members can add custom tiles dynamically with zero technical overhead. Custom cards persist in local storage and encode losslessly into portable Base64 URL fragments (`#board=...`).
  2. **High-Contrast Physical Placard Export (`@media print`)**: When tablets or power are constrained in critical telemetry zones, one-click printing formats all faces and tiles into a crisp, high-contrast black-and-white grid suitable for physical bedside charting and bed-rail mounting.
  3. **Community Language Packs (JSON)**: Open JSON schema (`generateLanguageTemplateJson`) enabling global translation into Indigenous, heritage, or regional languages (e.g. Navajo, Inuktitut, Ukrainian, Tagalog, Vietnamese) with zero compilation requirements.
  4. **Neural Voice Prioritization**: Replaces legacy robotic desktop synthesizers (SAPI5 formant engines) with deep neural network voices (`Microsoft Jenny (Natural)`, `Microsoft Guy (Natural)`, `Google WaveNet`, `Microsoft Elvira (Natural)`) tuned to a gentle $0.93\times$ bedside cadence and warm $0.98$ pitch lift.

---

## 📐 7. Domain 6: Multi-Sensory Wayfinding & 3D Tactile Profiles (ADA Title III & ISO 21542)

### 7.1 CNC & 3D-Printable Slice-Ready Profiles
* Standard TrueType fonts frequently contain self-intersecting loops, overlapping contours, or sub-integer bezier curves that cause slicer engines (PrusaSlicer, Cura, Bambu Studio) and CNC milling software to generate manifold errors or knife-edge burrs.
* **The PocketGull Invariant**:
  * Every glyph contour is strictly 2-byte word aligned, closed, and quadratic.
  * All sharp external corners feature a unified $25\text{ UPM}$ fillet radius. When extruded into $2.5\text{D}$ signage for tactile hospital wayfinding, the letterforms provide smooth, non-cutting edges for tactile finger-tracing conforming to **ADA Section 703** and **ISO 21542:2021 (Building Construction — Accessibility and Usability of the Built Environment)**.

---

## 🛡️ 8. Automated Verification Chain

Every commit touching the A11y & Neuro-Ergonomic architecture must satisfy:
1. **Automated Unit Invariants**: `node --test test/accessibility_and_neuro_ergonomics.test.mjs`
2. **Binary Table Word-Alignment & W3C OTS**: `dart run tool/pocketgull_foundry.dart audit`
3. **Contrast Benchmarks**: WCAG 2.2 AAA luminous contrast ratio $\ge 7:1$ across all normal text and $\ge 4.5:1$ across telemetry badges.
4. **Zero-Tofu Verification**: Zero `.notdef` across the Braille block (`U+2800`–`U+28FF`) and registered AAC codepoints.
