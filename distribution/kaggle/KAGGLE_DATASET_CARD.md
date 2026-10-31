# 🕊️ PocketGull Clinical, Mathematical & Telemetry Font Superfamily (`v3.1.0`)

**Subtitle** *(80 chars max for Kaggle)*:  
`Optotypically calibrated 1000 UPM vector fonts for EHRs, ICU telemetry & STEM`

---

## 1. Kaggle UI Metadata Fields (10.0 Usability Checklist)

### 👤 Authors & Bios

| Author Name | Bio |
| :--- | :--- |
| **Phil Gear** | `American graphic designer, computer scientist, and photographer based in the Pacific Northwest; founder of GearArts and Lead Architect of the PocketGull Font Superfamily (ORCID: 0009-0008-1372-5381). Engineered PocketGull from physical cardstock felt-marker lettering to unite humanist warmth with Louise Sloan 5:1 optotypes, ISO tactile Braille, and ISMP medication safety standards.` |
| **Emma Marichal** | `Type designer and open-source font engineering contributor (https://github.com/emmamarichal).` |
| **The PocketGull Project Authors** | `Open-source clinical typography, optometry, and UNDRIP sovereign orthography collective (https://font.pocketgull.app).` |

---

### 🗓️ Temporal & Geospatial Coverage

| Field | Value | Rationale |
| :--- | :--- | :--- |
| **Temporal Coverage Start Date** | `2026-05-01` | Original `v1.0.0` cardstock vector digitization & CERN Zenodo archival release (`10.5281/zenodo.18879500`). |
| **Temporal Coverage End Date** | `2026-10-14` | Current `v3.1.0` / `v3.2.0` production superfamily release (`10.5281/zenodo.22309379`). |
| **Geospatial Coverage** | `Global (Pacific Northwest, USA; Pan-Tribal North America; Arctic Inuktitut; Global Clinical & Astronomical Observatories)` | Or select **`Global` / `World`** (engineered in **Washington State / Pacific Northwest, USA**; covers 20+ world scripts including Salishan, Chinuk Pipa, Inuktitut Syllabics, Cherokee, Neo-Tifinagh, Ethiopic Ge'ez, Adlam, and Vai). |

---

### 📜 Provenance, License & DOI

- **License**: `Other (specified in description)` $\to$ **SIL Open Font License 1.1 (OFL-1.1)** with zero Reserved Font Name (RFN) restrictions (`OFL.txt`).
- **CERN / Zenodo Permanent DOI**: [`10.5281/zenodo.22309379`](https://doi.org/10.5281/zenodo.22309379)
- **Source Provenance**:
  > Originating from physical cardstock felt-marker lettering drawn by Phil Gear at GearArts, digitized into 1000 UPM quadratic TrueType (`glyf`) outlines conforming to ISO/IEC 14496-22 and Google Fonts specifications. Validated at 100% pass rate against W3C OpenType Sanitizer (OTS), OpenType 2-byte word-boundary alignment (`loca[i] % 2 == 0`), Louise Sloan 5:1 optotype geometry (5 arcminutes height, 1 arcminute stroke/aperture), and Institute for Safe Medication Practices (ISMP) character disambiguation standards.

---

## 2. Dataset Overview & Scientific Utility (Kaggle Description Body)

**PocketGull** is an open-source clinical sans-serif, display, mathematical, and telemetry monospace font superfamily designed for **zero-error data visualization**, **electronic health records (EHR)**, **ICU waveform monitoring**, and **scientific publishing** (`Matplotlib`, `Seaborn`, `R ggplot2`, `MATLAB`, `LaTeX`, and `Typst`).

### Cognitive Science & Game Theory Foundations (4-Level Notebook Walkthrough)
The companion notebook (`pocketgull_kaggle_showcase.ipynb`) uses **Progressive Disclosure** (honoring Nelson Cowan's **4-item working memory limit**) to demonstrate four empirical pillars:
1. **Level 1 — Pre-Attentive Vision (`< 200 ms`) & Separating Equilibrium**: Eliminates `0 / O`, `1 / l / I`, and `2 / Z` collisions (*Spence Signaling*) so the reader's eye never makes backward *regressive saccades* (*Karl Friston*).
2. **Level 2 — Defeating Hick's Law & 650nm Scotopic Night Vision**: Reduces 39 font files to **3 core archetypes** (`PocketGullMono-Regular.ttf` for fixed `600 UPM` telemetry/code, `PocketGull-Fineliner.ttf` for reading/plots, `PocketGull-VF.woff2` for web) and demonstrates a `650nm` rhodopsin-preserving ICU ECG plot.
3. **Level 3 — Bottom-Up Salience Gating (`[!]`)**: Converts invisible *Trojan Source* (`U+202E`) and fake spaces (`U+3164`) into a visible `600 UPM` `[!]` badge (`uni202E.guard`) to prevent silent OS font fallback, while keeping multilingual joiners (`U+200C` / `U+200D`) clean.
4. **Level 4 — Cognitive Offloading & Zero-VM Memory Safety**: Every `.ttf` binary is 2-byte word-aligned (`loca[i] % 2 == 0`) with `0` `fpgm`/`cvt ` bytecode VM bytes (`instructionLength = 0`) and bit-6/bit-7 flags masked (`flag & 0x3F`).

---

## 3. Quickstart in a Kaggle Python Notebook (`matplotlib`)

```python
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 1. Register PocketGull directly from the Kaggle dataset input directory
font_dirs = ["/kaggle/input/pocketgull-clinical-font-superfamily/fonts/ttf"]
for font_file in font_manager.findSystemFonts(fontpaths=font_dirs):
    font_manager.fontManager.addfont(font_file)

# 2. Apply PocketGull for high-acuity, ISMP-disambiguated scientific plots
plt.rcParams["font.family"] = "PocketGull"
plt.rcParams["axes.edgecolor"] = "#334155"
plt.rcParams["axes.linewidth"] = 0.8
```
