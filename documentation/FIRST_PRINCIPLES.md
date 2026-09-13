# First Principles: Stripping Away False Constraints in Typography & Typefoundry Engineering

> *"Rather than fixing downstream bugs in runtime memory, system architecture must make entire classes of bugs impossible by structural construction."*  
> — Eskil Steenberg, *Debugging and the art of avoiding bugs*

---

## Overview: The Living Typographic Charter

As the PocketGull Font Superfamily matured from felt-marker cardstock drawings into a multi-script clinical and telemetry typefoundry, it accrued numerous rigid technical rules. Upon forensic re-examination from first principles, we recognized where well-intentioned geometric constraints can fight the authentic nature of human language and writing systems.

This document establishes the foundational critique and the resulting **Living Typographic Charter**.

---

## The 7 Tensions: What Might Not Truly Make Sense

### 1. "Making Everything Plumb" vs. The Reality of the Calligraphic Hand
* **The Rule**: All tittles, nuqṭas, and diacritics must sit strictly at $0^\circ$ (zero slant, true vertical gravity).
* **Where it doesn't make sense**:
  * **In Arabic (Nuqṭa)**: A nuqṭa in traditional Arabic calligraphy (*Naskh*, *Ruq‘ah*, *Thuluth*) is literally the footprint of a reed pen (*qalam*) cut at a deliberate angle ($45^\circ\text{–}70^\circ$). Rotating a nuqṭa to $0^\circ$ turns it into a sterile diamond or square, stripping away the natural biomechanics of the hand. To native readers, it can look rigid, computerized, or foreign.
  * **The PocketGull Origin**: PocketGull originated from **felt marker on physical cardstock**. Human handwriting is never $0^\circ$ plumb—it has natural slant, rhythm, and cadence. Demanding absolute mathematical zero-degree plumbness fights the humanist warmth the font was born with.

---

### 2. Grounding Braille to Latin $x$-Height and Baseline
* **The Rule**: Lock Braille cells to Latin baseline ($y=0$) and cap-height ($y=720$), boosting dot radius to $r=78\text{ UPM}$.
* **Where it doesn't make sense**:
  * **Braille is tactile, not visual**: Braille was engineered for fingertips sweeping across an embossed page or refreshable pin matrix, not for sighted eyeballs reading on an OLED screen alongside 12pt Helvetica.
  * **Destruction of the 8-Dot Matrix**: In standard 8-dot Braille (ISO/TR 11548), Dots 7 and 8 sit below Dot 3. If Dot 3 is grounded on the Latin baseline ($y=0$), Dots 7 and 8 plunge into negative descender space.
  * **Dot Collision**: Boosting dot radius to $r=78\text{ UPM}$ to "match bold Latin stroke weight" reduces the negative space between dots. In tactile reading, that inter-dot negative space is what allows the mechanoreceptors in the fingerpad to distinguish a 2 from a 3 or a colon.

---

### 3. Scaling Shorthand (Duployan / Chinuk Pipa) to Latin $x$-Height
* **The Rule**: Scale stenographic circle vowels ($a, o, u$) by $1.85\times$ to fill lowercase Latin counter height ($y=540\text{ UPM}$).
* **Where it doesn't make sense**:
  * **Size is Phonemic in Stenography**: In Duployan, the relative size of a circle determines the vowel sound (e.g., a tiny circle is one vowel, a medium circle is another, a large circle is an open vowel or nasal). Artificially magnifying circles to match Latin $x$-height risks collapsing the phonemic distinction between small and large vowel loops.
  * **Shorthand is cursive and fluid**: Stenography was designed for rapid pencil shorthand, flowing naturally across lines. Forcing it to obey Latin typographic boxes treats a cursive stream as if it were a set of Roman metal type punches.

---

### 4. Louise Sloan 5:1 Optotypes in Continuous Body Text
* **The Rule**: Apply Sloan 5:1 optotype ratios (stroke width = 1/5 height) for clinical legibility.
* **Where it doesn't make sense**:
  * Sloan letters were designed for **ETDRS eye charts**—isolated, unspaced capital letters viewed at distance thresholds to measure the absolute minimum angle of resolution.
  * **Continuous reading is not an acuity test**: When reading long EHR clinical notes, discharge summaries, or code, forcing rigid 5:1 ratios across lowercase letters (`e`, `a`, `s`) creates dark clumps of ink and uneven optical density. Real typography requires optical compensations (thinning crossbars, opening apertures), not rigid geometric ratios.

---

### 5. Fixed 600 UPM Monospace for Global Scripts
* **The Rule**: Every glyph in `PocketGullMono` must have an advance width of exactly 600 UPM (`isFixedPitch = 1`).
* **Where it doesn't make sense**:
  * 600 UPM works great for Latin, numbers, and box drawing.
  * But cramming **CJK ideographs**, **Tibetan multi-vowel stacks**, or **Khmer consonant clusters** into a 600 UPM box violently distorts their proportions. In East Asian typography, ideographs are standardly fullwidth (1000 UPM / duospaced). Forcing complex multi-stroke Hanzi into 600 UPM makes them unreadable at telemetry sizes.

---

### 6. Treating Archaic 1990s TrueType Quirks as "Sacred Pillars"
* **The Rule**: 2-byte word alignment on `loca`/`glyf` and bit-7 flag masking as core "Invariant Quality Pillars."
* **Where it doesn't make sense**:
  * These rules originate from 30-year-old TrueType 1.0 memory quirks and aggressive OTS sanitizers from early 2010s browser engines.
  * While complying with them is great defensive programming (avoiding parser rejections), elevating byte-padding to the same moral status as clinical patient safety or Braille accessibility is a category error. One is an obscure binary serialization detail; the other affects human lives.

---

### 7. The PEMDAS Fallacy: Treating Language Like an Equation
* **The Rule**: Seeking a rigid algorithmic hierarchy (like PEMDAS in arithmetic) to make people feel "loved and safe" when reading.
* **Where it doesn't make sense**:
  * Math has strict precedence ($P \rightarrow E \rightarrow MD \rightarrow AS$) because it operates in a closed formal system.
  * **Language is emotional, cultural, and living**. When typography becomes too dogmatic—imposing Western Latin geometric rules (baselines, $x$-heights, $0^\circ$ plumbness, em-boxes) onto indigenous shorthands, tactile dot systems, and non-Latin calligraphic traditions—it can inadvertently erase the very soul and voice of those scripts.

---

## 🏛️ The Fivefold Resolution

As Eskil Steenberg teaches, **good engineering is about clarity of purpose and stripping away false constraints**:

1. **Let Latin be Latin**: Crisp, disambiguated (ISMP), humanist, and readable.
2. **Let Arabic be Arabic**: Let the nuqṭa keep its natural pen angle (the authentic reed-pen footprint, honoring calligraphy rather than sterile mechanical plumbness).
3. **Let Braille be Braille**: Preserve standard tactile cell geometries and negative space (ISO/TR 11548 & ISO 17049).
4. **Let Shorthand be Shorthand**: Respect the phonemic size ratios of stenography without forcing it into Roman metal boxes.
5. **Keep the binary engine clean**: Pad bytes to keep OTS happy (`loca[i] % 2 == 0`), but don't confuse memory alignment with typographic beauty.
