# 🕊️ PocketGull Clinical, Mathematical & Telemetry Font Superfamily (`v4.0.0`)

**Canonical Kaggle Dataset Slug**: [`https://www.kaggle.com/datasets/philgear/pocketgull-font`](https://www.kaggle.com/datasets/philgear/pocketgull-font)  
**Subtitle** *(80 chars max for Kaggle)*:  
`Optotypically calibrated 1000 UPM vector fonts for EHRs, ICU telemetry & STEM`

---

## 1. Kaggle UI Metadata Fields (10.0 Usability Checklist)

### 👤 Authors & Bios

| Author Name | Bio |
| :--- | :--- |
| **Phil Gear** | `American graphic designer, computer scientist, and photographer based in the Pacific Northwest; founder of GearArts and Lead Architect of the PocketGull Font Superfamily (ORCID: 0009-0008-1372-5381). Engineered PocketGull from physical cardstock felt-marker lettering to unite humanist warmth with Louise Sloan 5:1 optotypes, ISO tactile Braille, and ISMP medication safety standards.` |
| **The PocketGull Project Authors** | `Open-source clinical typography, optometry, and UNDRIP sovereign orthography collective (https://font.pocketgull.app).` |

---

### 🗓️ Temporal & Geospatial Coverage

| Field | Value | Rationale |
| :--- | :--- | :--- |
| **Temporal Coverage Start Date** | `2026-05-01` | Original `v1.0.0` cardstock vector digitization & CERN Zenodo archival release (`10.5281/zenodo.18879500`). |
| **Temporal Coverage End Date** | `2026-11-11` | Current `v4.0.0` production superfamily + Botanica v3 / Kintsugi v2 release (`10.5281/zenodo.22309379`). |
| **Geospatial Coverage** | `Global (Pacific Northwest, USA; Pan-Tribal North America; Arctic Inuktitut; Global Clinical & Astronomical Observatories)` | Select **`Global` / `World`** (engineered in **Washington State / Pacific Northwest, USA**; covers 20+ world scripts including Salishan, Osage, Chinuk Pipa, Inuktitut Syllabics, Cherokee, Neo-Tifinagh, Ethiopic Ge'ez, Adlam, and Vai). |

---

### 📜 Provenance, License & DOI

- **License**: **SIL Open Font License 1.1 (`OFL-1.1`)** for all 41 font binaries (`OFL.txt`, zero Reserved Font Name restrictions); **Apache License 2.0** for companion verification/telemetry scripts (`LICENSE-APACHE-2.0.txt`).
- **CERN / Zenodo Permanent DOI**: [`10.5281/zenodo.22309379`](https://doi.org/10.5281/zenodo.22309379)
- **Source Provenance**:
  > Originating from physical cardstock felt-marker lettering drawn by Phil Gear at GearArts, digitized into 1000 UPM quadratic TrueType (`glyf`) outlines conforming to ISO/IEC 14496-22, ISO 15008 telemetry ergonomics, and Google Fonts / Rust `fontspector v1.9.0` (`0 FAIL` across `39/39` core + `2/2` upcycled cuts). Validated at 100% pass rate against W3C OpenType Sanitizer (OTS), OpenType 2-byte word-boundary alignment (`loca[i] % 2 == 0`), Zero-VM bytecode safety (`0` `fpgm`/`cvt ` bytes), Louise Sloan 5:1 optotype geometry, and Institute for Safe Medication Practices (ISMP) character disambiguation standards.

---

## 2. What's New in `v4.0.0` (Dataset Highlights)

1. **Out-of-the-Box `Il1` Disambiguation in Base `cmap`**: Proportional humanist cuts and `PocketGull-VF.ttf` now feature a rightward curved clinical foot on base `U+006C` (`l`) and bilateral serifs on base `U+0049` (`I`)—eliminating `1 / l / I` collisions automatically in Matplotlib, R `ggplot2`, and Seaborn without requiring OpenType CSS feature flags.
2. **41 Audited TrueType Cuts + Tabular Data Explorer (`fonts/pocketgull_v4_sfnt_telemetry.csv`)**: Includes all 39 core superfamily cuts (`PocketGull`, `Serif`, `Slab`, `Soft`, `Mono`, `Math`, `Chem`, `Lab`, `Genome`, `Algo`, `Music`, `ASL`/`Sign`, `VF`) plus **2 Circular-Economy Upcycled Cuts**:
   - **`PocketGull-Botanica.ttf` (v3)**: Living Bézier vine arbors, acuminate phyllotaxis leaves, and 6 herbarium specimens.
   - **`PocketGull-Kintsugi.ttf` (v2)**: Avian trabecular bone biomimicry achieving **`-45.8%` eco-ink conservation**.
3. **16-Axis Variable Font (`PocketGull-VF`) & Z-Layered Anatomical `ASL`/`Sign`**: Restored `8,603` live 16-axis `gvar` + `O(1)` `HVAR` tuples and rebuilt all 36 manual alphabet/numeral handshapes (`A–Z`, `0–9`) via 2D Z-buffered Signed Distance Fields.
4. **Native `liga`, `tnum`, & `GPOS` PairPos Kerning**: Standard `fi`/`fl` ligatures, 600 UPM tabular numerals (`tnum` + `zero.slash.tnum`), and GID-sorted kerning across technical cuts.

---

## 3. Cognitive Science & Game Theory Foundations (4-Level Notebook Walkthrough)

The companion notebook (`pocketgull_kaggle_showcase.ipynb`) uses **Progressive Disclosure** (honoring Nelson Cowan's **4-item working memory limit**) to demonstrate four empirical pillars:
1. **Level 1 — Pre-Attentive Vision (`< 200 ms`) & Separating Equilibrium**: Eliminates `0 / O`, `1 / l / I`, and `2 / Z` collisions (*Spence Signaling*) out of the box in base `cmap` so the reader's eye never makes backward *regressive saccades* (*Karl Friston*).
2. **Level 2 — Defeating Hick's Law & 650nm Scotopic Night Vision**: Reduces 41 font files to **3 core archetypes** (`PocketGullMono-Regular.ttf` for fixed `600 UPM` telemetry/code, `PocketGull-Fineliner.ttf` for reading/plots, `PocketGull-VF.woff2` for web) and demonstrates a `650nm` rhodopsin-preserving ICU ECG plot.
3. **Level 3 — Bottom-Up Salience Gating (`[!]`)**: Converts invisible *Trojan Source* (`U+202E`) and fake spaces (`U+3164`) into a visible `600 UPM` `[!]` badge (`uni202E.guard`) to prevent silent OS font fallback, while keeping multilingual joiners (`U+200C` / `U+200D`) clean.
4. **Level 4 — Cognitive Offloading & Zero-VM Memory Safety**: Loads `pocketgull_v4_sfnt_telemetry.csv` and live-audits all 41 `.ttf` binaries (`loca[i] % 2 == 0`, `0` `fpgm`/`cvt ` bytecode VM bytes, `head.fontRevision == 4.0`).

---

## 4. Quickstart in a Kaggle Python Notebook (`matplotlib`)

```python
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 1. Register PocketGull v4.0.0 directly from the Kaggle dataset input directory
font_dirs = ["/kaggle/input/pocketgull-font/fonts/ttf"]
for font_file in font_manager.findSystemFonts(fontpaths=font_dirs):
    font_manager.fontManager.addfont(font_file)

# 2. Apply PocketGull for high-acuity, ISMP-disambiguated scientific plots
plt.rcParams["font.family"] = "PocketGull"
plt.rcParams["axes.edgecolor"] = "#334155"
plt.rcParams["axes.linewidth"] = 0.8
```
