# 🏛️ CERN & Zenodo Open Science Archival Guide

**PocketGull Font Superfamily**  
*Permanent Scientific Digital Preservation, DataCite DOI Governance, and CERN Infrastructure*

---

## 🔬 1. The CERN & Zenodo Preservation Framework

**Zenodo** is an open-access scientific repository developed by **CERN** (the European Organization for Nuclear Research, Geneva, Switzerland) under the EU OpenAIRE project. Hosted in the CERN Data Centre in Meyrin, Switzerland, Zenodo provides persistent, tamper-evident digital preservation for open-source scientific software, research data, and clinical tools.

For the **PocketGull Font Superfamily**, depositing on CERN/Zenodo achieves three critical milestones:
1. **Permanent Digital Object Identifier (DOI)**: Immutable DataCite DOI [`10.5281/zenodo.22309379`](https://doi.org/10.5281/zenodo.22309379) and published repository record at [zenodo.org/records/22309379](https://zenodo.org/records/22309379) that can be cited in peer-reviewed journals (e.g. *Ophthalmology*, *Nature Biomedical Engineering*, *BMJ Health & Care Informatics*).
2. **Archival Preservation at CERN**: Ensures font binaries (`.ttf`, `.woff2`), vector UFO master sources, OpenType table specifications, and clinical validation scripts remain accessible indefinitely, even across long-term institutional shifts.
3. **Scholarly Citation & Attribution**: Links the typeface repository directly to **Phil Gear** ([ORCID: 0009-0008-1372-5381](https://orcid.org/0009-0008-1372-5381)), **PocketGull LLC**, and the CMS NPI registry.

---

## 🛠️ 2. Repository Architecture & Metadata Alignment

This repository contains two synchronized metadata standards designed for CERN and academic ecosystems:

### A. `.zenodo.json` (CERN Deposition Schema)
Located at the root of `pocketgull-typeface`, this configuration file governs how CERN's DataCite ingest pipeline indexes the repository:
* **Title**: `PocketGull Font Superfamily: Optotypically Calibrated Clinical & Ophthalmological Vector Letterforms`
* **Upload Type**: `software`
* **License**: `OFL-1.1` (SIL Open Font License 1.1)
* **Creators**: Phil Gear (`orcid: 0009-0008-1372-5381`, `affiliation: PocketGull LLC`) and The PocketGull Project Authors
* **Keywords**: `typography`, `typeface`, `clinical-safety`, `ophthalmology`, `optotypes`, `ismp-medication-safety`, `braille`, `bionic-reading`, `open-science`, `cern-zenodo`, `wcag-aaa`
* **Related Identifiers**: Cross-linked to the companion clinical intelligence platform ([DOI: 10.5281/zenodo.20647514](https://doi.org/10.5281/zenodo.20647514) / [zenodo.org/records/20647514](https://zenodo.org/records/20647514)), ORCID, and NPI Registry.

### B. `CITATION.cff` (Citation File Format 1.2.0)
Powers GitHub’s native **"Cite this repository"** sidebar button, exporting instant BibTeX, APA, and EndNote citations for clinical researchers.

---

## 🚀 3. Step-by-Step Activation Instructions

You can establish the dedicated CERN/Zenodo record for `pocketgull-font` via either of the following two pathways:

### Option 1: Automatic GitHub Release Webhook (Recommended)
1. Navigate to [Zenodo GitHub Settings](https://zenodo.org/account/settings/github/).
2. Locate `pocketgull-app/pocketgull-font` in your repository list.
3. Toggle the switch to **ON** (Enables the CERN webhook).
4. Whenever a new GitHub Release (e.g. `v2.0.0`) is published, CERN Zenodo will:
   * Download the release archive.
   * Parse `.zenodo.json` from the repository root.
   * Mint a new Version DOI and reserve the Concept DOI.
   * Provide an embeddable DOI badge for `README.md`.

### Option 2: Command-Line REST Synchronization (`scripts/zenodo-sync.mjs`)
We have engineered a dedicated sync script right in this repository:

```bash
# 1. Validate local metadata & check CERN API connectivity
node scripts/zenodo-sync.mjs

# 2. Test in the CERN Zenodo Sandbox (Optional)
node scripts/zenodo-sync.mjs --sandbox

# 3. Create a live draft deposition (Requires token)
$env:ZENODO_ACCESS_TOKEN = "your_zenodo_token_here"
node scripts/zenodo-sync.mjs --create-draft
```

To create a Personal Access Token on Zenodo:
1. Go to [Zenodo Applications / Tokens](https://zenodo.org/account/settings/applications/tokens/new/).
2. Name the token `PocketGull Font Deposition`.
3. Check scopes: `deposit:actions`, `deposit:write`.
4. Click **Create** and set the environment variable.

---

## 📖 4. Recommended Citation Formats

### BibTeX
```bibtex
@software{gear_pocketgull_font_2026,
  author       = {Gear, Phil and {The PocketGull Project Authors}},
  title        = {{PocketGull Font Superfamily: Optotypically Calibrated Clinical \& Ophthalmological Vector Letterforms}},
  month        = sep,
  year         = 2026,
  publisher    = {CERN / Zenodo},
  version      = {3.0.0},
  doi          = {10.5281/zenodo.22309379},
  url          = {https://font.pocketgull.app},
  license      = {OFL-1.1}
}
```

### APA 7th Edition
> Gear, P., & The PocketGull Project Authors. (2026). *PocketGull Font Superfamily: Optotypically Calibrated Clinical & Ophthalmological Vector Letterforms* (Version 3.0.0) [Computer software]. CERN / Zenodo. https://doi.org/10.5281/zenodo.22309379

---

<p align="center">
  <sub>Preserved under the CERN Data Centre Open Science Architecture & SIL Open Font License 1.1.</sub>
</p>
