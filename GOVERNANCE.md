# Project Governance & Typographic Oversight Policy

**PocketGull Font Superfamily**  
*Open Source Governance, Clinical & Ophthalmological Typography Review Board, and Release Protocol*

---

## 🏛️ 1. Governance Principles

PocketGull Font Superfamily is an open-source medical, ophthalmological, and Pan-Tribal typography project developed by **PocketGull LLC** in collaboration with clinical researchers, optometrists, vision scientists, type designers, and Indigenous language keepers.

Our governance model ensures:
1. **Ophthalmological Rigor & Evidence Grounding**: All letterform metrics, stroke contrasts, x-height ratios, and counter spaces must be grounded in peer-reviewed vision science literature (Louise Sloan 5:1 acuity, Hermann Bouma crowding coefficients, ISO/TR 11548 Braille dimensions, DIN 1450 legibility standards).
2. **Deterministic Safety Precedence**: Stylistic flourishes never compromise clinical readability or the Institute for Safe Medication Practices (ISMP) zero-error character disambiguation rules.
3. **Radical Transparency & Libre Licensing**: 100% open-source font distribution under the **SIL Open Font License 1.1** (with build tooling under Apache 2.0), open vector sources (UFO3 / Glyphs), reproducible build toolchains, and public issue tracking.
4. **Binary Integrity & Memory Safety**: Zero W3C OpenType Sanitizer (OTS) violations, 2-byte word boundary alignment, and hermetic CI validation.
5. **Multi-Script Respect & Inclusivity**: Orthographies and scripts are designed in accordance with established writing systems and community input, preserving authentic calligraphic stroke traditions without mechanical flattening.

### 1.1 Foundry Governance & Quality Pillars

To maintain mathematical vector determinism, binary safety, and upstream open-source adoption, PocketGull establishes three core pillars:

* **🕊️ Respectful Multi-Script Typography**:
  * **Authentic Stroke Traditions**: Respect the authentic reed-pen footprint of Arabic, the standard 8-dot geometry of Braille (ISO/TR 11548), and the rotational symmetry of Syllabics.
  * **Zero Synthetic Flattening**: Ground non-Latin scripts to the optical baseline and x-height without forcing non-Latin letterforms into rigid Latin boxes.
  * **Community Input**: Orthographic additions adhere to verified orthographic standards and Unicode specifications.
* **✒️ Mathematical Determinism & OTS Safety**:
  * **2-Byte Word Boundary Invariant**: `loca[i] % 2 == 0` across all glyph records. Zero OTS memory eviction in DirectWrite or Chromium.
  * **Bit-7 Flag Masking**: Point flags byte bit 7 (`0x80`) strictly zero.
  * **Sloan Acuity & ISMP Disambiguation**: Louise Sloan 5:1 optotypes, mandatory `cv08` slashed zero, `cv05` curved l, `ss02` serifed I, `cv11` slashed Z.
  * **Pure Dart 3.11 Toolchain**: Deterministic SFNT compilation, 0 duplicate nodes, hermetic table layout.
* **🌐 Google Fonts Parity & Upstream Harmony**:
  * **Minimalist Versioning**: `head.fontRevision == 3.1`, `nameID 5 == 'Version 3.100; The PocketGull Project Authors; OFL 1.1'`.
  * **Zero RFN Debt**: SIL Open Font License 1.1 with no Reserved Font Name restriction (see [TRADEMARKS.md](TRADEMARKS.md) for brand coexistence policy).
  * **Full CFF & Zenodo DOI Sync**: Permanent DOI `10.5281/zenodo.22309379` mapped to CERN open science index.
  * **Pre-Flight Checks**: Complete fontbakery check-googlefonts compliance, WOFF2 Brotli 11, designer profile dossier.

### 1.2 UNDRIP Typographic Accord & Indigenous Data Sovereignty

PocketGull formally commits to and implements the **United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP)** across all font families, character sets, and OpenType layouts:

1. **Digital Infrastructure for Language Transmission (Articles 13.1 & 14.1)**:
   - Indigenous peoples have the inherent right to revitalize, use, develop, and transmit their languages, oral traditions, philosophies, writing systems, and literatures to future generations.
   - PocketGull provides complete, zero-`.notdef` digital infrastructure across Canadian Aboriginal Syllabics (`U+1400`–`U+167F`), Duployan / Chinuk Pipa (`U+1BC00`–`U+1BC9F`), Cherokee (`U+13A0`–`U+13FF`, `U+AB70`–`U+ABBF`), Osage (`U+104B0`–`U+104FB`), and Pan-Tribal Latin orthographies covering 574+ federally recognized tribes in the U.S. and 630+ First Nations in Canada.
   - The SIL Open Font License 1.1 guarantees that tribal schools, immersion programs, elders, and community publishers can freely use, subset, modify, embed, and distribute the fonts without royalties, proprietary lock-in, or internet connectivity requirements.

2. **Rejection of Typographic Colonialism & Cultural Integrity (Articles 11.1 & 31.1)**:
   - Indigenous scripts possess their own authentic geometric logic, rotational semantics, and calligraphic traditions. PocketGull strictly prohibits "Latinization"—the distortion of non-Latin characters to conform to Roman cap-heights or Western typographic grids.
   - Rotational symmetry in Canadian Aboriginal Syllabics is preserved with exact optical centering to ensure vowel distinctions remain unambiguous.
   - In accordance with the **First Nations OCAP® Principles** (Ownership, Control, Access, and Possession) and **UNDRIP Article 31**, cultural symbols, clan insignia, and sacred motifs will never be unilaterally extracted or commodified. Any inclusion of specialized tribal emblems requires explicit Free, Prior, and Informed Consent (FPIC) through authorized community channels.

3. **Equitable Healthcare Acuity & Triage Life-Safety (Articles 13.2 & 24.1)**:
   - Article 24 affirms Indigenous rights to the highest attainable standard of physical and mental health, while Article 13.2 mandates that Indigenous peoples must be understood in administrative and health proceedings.
   - PocketGull applies the exact same life-critical Louise Sloan 5:1 optotype clarity, ISMP error prevention, and anti-clipping vertical margins (>= 110 UPM headspace for stacked high-tone nasals like *ą́*, *ę́*, *į́*, *ǫ́*) to Indian Health Service (IHS) and First Nations electronic health records (EHR), prescription labeling, and emergency signage as it does to Latin clinical dosage charts.

### 1.3 The "Clean Pipe" Invariant & Negative Space Charter (The Prohibitions)

To maintain ethical rigor, clinical humility, and community trust, PocketGull explicitly delineates what it **MUST NEVER DO**:

1. **PROHIBITION 1: No Medical Device Claims or Diagnostic Overreach**
   - PocketGull is a passive optometric and typographical conduit. It is **not** Software as a Medical Device (SaMD) under FDA 510(k) or EU MDR regulations.
   - The typeface never makes diagnostic assertions, calculates medication dosages, or claims to "treat" dyslexia or vision loss. It improves legibility through optical physics (Louise Sloan 5:1 ratio, ISMP character disambiguation), but never replaces clinical vigilance or institutional double-checks.

2. **PROHIBITION 2: No Simulated Automated Sign Language (ASL) "Translation"**
   - American Sign Language (ASL) and world sign languages are complete, natural 3D visual-spatial languages with complex syntax, spatial grammars, and Deaf cultural heritage—not a word-for-word substitution cipher of spoken English.
   - PocketGull provides 2D cheremic transcription glyphs (Sutton SignWriting, Stokoe notation) strictly for linguistic documentation and academic pedagogy. It will **never** market itself as an automated "ASL translation engine" or presume to replace certified Deaf interpreters.

3. **PROHIBITION 3: No Invasive Accessibility Overlays**
   - PocketGull strictly rejects third-party JavaScript "accessibility overlay" widgets that inject DOM wrappers or attempt to override browser accessibility APIs, which frequently disrupt screen readers (NVDA, JAWS, VoiceOver).
   - PocketGull adheres exclusively to native semantic HTML, high-contrast CSS (WCAG AAA 7:1 ratio), and standard 256 Unicode Braille codepoints (`U+2800`–`U+28FF`).

4. **PROHIBITION 4: Zero Telemetry Egress & Zero PHI Tracking**
   - In healthcare environments and sovereign tribal clinics, text entered into an interface often constitutes Protected Health Information (PHI) under HIPAA, PIPEDA, and OCAP®.
   - PocketGull enforces a strict **Zero-Egress Invariant**: no tracking pixels, no analytics beacons, no keystroke recording, and no remote license verification calls. Fonts execute 100% locally on client hardware or from immutable static edge CDNs without request logging.

5. **PROHIBITION 5: No Cultural Overreach or Mock Prescriptions**
   - Traditional Indigenous words for wellness, sacred botany, or ceremonial practices will **never** be appropriated, commercialized, or converted into synthetic pharmaceutical dosage orders (e.g., mock milligram prescriptions).
   - Specimen copy for sovereign orthographies must remain strictly focused on authentic technical glyph verification, vowel rotation matrices, diacritic stacking clearance, and verified public educational or human rights declarations.

---

## 👥 2. Roles & Responsibilities

### 2.1 Lead Systems Architect & Benevolent Dictator for Now (BDFN)
* **Lead Architect**: **Phil Gear** ([ORCID: 0009-0008-1372-5381](https://orcid.org/0009-0008-1372-5381))
* Retains final architectural, licensing, and security decision-making authority over core repository branches, font naming, and cryptographic release seals.

### 2.2 Typographic & Clinical Review Board (TCRB)
* Composed of vision researchers, clinicians, ophthalmologists, and type engineers.
* Reviews all Pull Requests touching:
  * ISMP high-risk medication safety glyphs (cv08 slashed zero, cv05 curved l, ss02 serifed I).
  * Unicode Braille patterns (U+2800..U+28FF) and tactile embossing metrics.
  * Dyslexia-conscious baseline weighting and saccadic reading anchors.
  * Monospace 600 UPM advance metrics and ICU vitals table alignment.
  * Photobiomodulation (670nm PBM) optical contrast calibration.

### 2.3 Core Maintainers
* Review daily pull requests, maintain CI/CD pipelines, and enforce pre-flight test suites (`sources/validate_fonts.py`, `fontbakery check-googlefonts`).

### 2.4 Multi-Script, Indigenous & Linguistic Advisory
* Governs orthographic expansion, syllabic accuracy, and script integrity across Indigenous and sovereign writing systems (Canadian Syllabics, Duployan Chinuk Pipa, Cherokee, Osage, Diné Bizaad, Lakȟótiyapi, Lushootseed, Arabic, Cyrillic, Greek, Hebrew).
* Collaborates with Indigenous language keepers, tribal immersion educators, and verified linguistic standards to uphold UNDRIP compliance and community orthographic conventions.
* Ensures accurate encoding and alignment with Unicode standards and verified linguistic reference materials.

---

## 📜 3. Decision-Making & RFC Process

Significant architectural, metric, or glyph set changes follow a lightweight **Request for Comments (RFC)** process:

1. **RFC Proposal**: Contributor opens an issue with the `[TYPOGRAPHY-RFC]` template or starts a GitHub Discussion.
2. **Review Period**: 7-day public review period for community feedback, clinical verification, and language keeper attestation.
3. **Proof-of-Work Verification**: Implementation must provide 100% passing tests via `sources/validate_fonts.py` and Fontbakery (0 FAILs, 0 FATALs).
4. **Consensus & Merge**: Merged upon approval by the Lead Architect.

---

## 🛡️ 4. Emergency Patch Protocol (STAT Override)

In the event of an identified clinical safety hazard, OTS memory violation, or critical table corruption:
1. Maintainers may push an emergency fix directly to a hotfix branch on `main`.
2. The hotfix must satisfy the mandatory OTS sanitizer and `validate_fonts.py` test suites.
3. A post-mortem incident report will be published in `SECURITY.md` within 48 hours.

---

## 🤖 5. Machine Learning Reservation & AI Ingestion Covenants

1. **Text and Data Mining Reservation (TDMR)**: PocketGull expressly reserves all rights against text and data mining, automated scraping, extraction, and harvesting for the purposes of training generative AI, foundational models, or large language models under **Article 4(3) of EU Directive 2019/790** and international copyright conventions.
2. **Machine-Readable Opt-Out**: Machine-readable reservations are asserted across `robots.txt`, `.aiignore`, `llms.txt`, and HTTP headers (`TDM-Reservation: 1`).
3. **Humanitarian & Clinical Exemption**: Font binaries may be embedded freely in software, clinical EHR systems, medical telemetry devices, and printed educational materials under the Apache 2.0 without restriction, but raw linguistic and glyph data may not be aggregated into base model training corpora.

---

<p align="center">
  <sub>© 2026 PocketGull LLC & Phil Gear. Distributed under the SIL Open Font License 1.1.</sub>
</p>
