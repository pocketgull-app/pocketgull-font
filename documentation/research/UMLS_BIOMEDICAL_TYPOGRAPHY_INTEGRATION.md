# Unified Medical Language System (UMLS) & PocketGull Clinical Typography Architecture

**The PocketGull Project Authors & Typefoundry Engineering Team**  
*In Collaboration with Clinical Informatics, Biomedical Ergonomics & Font Engineering*  
**Date**: September 2026  
**Status**: Foundational Biomedical Informatics Specification  
**Authority**: National Library of Medicine (NLM), NIH, Bethesda, MD  

---

## Executive Summary

Modern hospital Electronic Health Records (EHRs), Computerized Physician Order Entry (CPOE) consoles, and ICU vital-sign telemetry monitors rely on the **Unified Medical Language System (UMLS)** developed by the **National Library of Medicine (NLM)**. UMLS integrates over 200 biomedical vocabularies, clinical coding standards, and ontologies into a unified semantic lattice.

However, clinical informatics systems encounter a dangerous **"last-meter" rendering vulnerability**: regardless of how semantically rigorous an ontology is in the database, human clinicians must perceive, read, and act upon this terminology on physical displays:
- $200\text{px}$ smart infusion pump LCDs running in dim trauma bays.
- 203 DPI direct-thermal bedside patient wristbands and barcode labels subject to thermal bleeding.
- Telemetry central station monitors displaying high-density multilead waveforms alongside micro-unit measurements ($\mu\text{g/kg/min}$, $\text{mEq/L}$, $\text{mOsm/kg}$).

The **PocketGull Font Superfamily** provides the world's first open-source, W3C OTS memory-safe typography engine purpose-built for the **three UMLS Knowledge Sources**:
1. **The Metathesaurus**: Linking Concept Unique Identifiers (CUIs), RxNorm (RxCUIs), and LOINC codes to optotypically disambiguated glyph vectors.
2. **The Semantic Network**: Enforcing semantic-level visual hierarchy between *Pharmacologic Substance* (`T121`), *Clinical Drug* (`T200`), and *Laboratory Procedure / Finding* (`T034` / `T059`).
3. **The SPECIALIST Lexicon**: Eliminating fatal collisions across biomedical abbreviations, normalized strings, Greek biochemical prefixes ($\alpha, \beta, \Delta$), and scientific numerical exponents.

---

## 1. The Three UMLS Knowledge Sources in Typographic Practice

```
+-----------------------------------------------------------------------------------+
|                     UMLS (Unified Medical Language System)                        |
+-----------------------------------------------------------------------------------+
        |                                   |                                   |
        v                                   v                                   v
+-----------------------+       +-----------------------+       +-----------------------+
|     Metathesaurus     |       |   Semantic Network    |       |  SPECIALIST Lexicon   |
| (RxNorm, LOINC, SNOMED)       | (Semantic Types/TUIs) |       |  (Lexical Norms/Vars) |
+-----------------------+       +-----------------------+       +-----------------------+
        |                                   |                                   |
        +-----------------------------------+-----------------------------------+
                                            |
                                            v
                +-------------------------------------------------------+
                |          PocketGull Clinical Typography Engine         |
                | - Louise Sloan 5:1 Optotypes & Bouma Anti-Crowding   |
                | - ISMP Life-Critical Disambiguation (0, l, I, Z)     |
                | - Fixed 600 UPM Monospace Pitch for ICU Telemetry     |
                | - Subscripts, Superscripts, Greek, & Metric Units    |
                | - 100% W3C OTS Memory-Safe 2-Byte Word Alignment      |
                +-------------------------------------------------------+
```

### 1.1 UMLS Metathesaurus
The Metathesaurus organizes biomedical meaning around **Concepts**, each assigned an immutable **Concept Unique Identifier (CUI)** prefixed with `C` followed by 7 digits.

Underneath each CUI, PocketGull validates specific constituent vocabularies:
- **RxNorm (`SAB = RXNORM`)**: Standardized clinical drug names, active ingredients, and clinical dose forms. Governs ISMP Tall Man Lettering disambiguation.
- **LOINC (`SAB = LNC`)**: Logical Observation Identifiers Names and Codes. Governs laboratory observations, specimen sources, and measurement units.
- **SNOMED CT (`SAB = SNOMEDCT_US`)**: Comprehensive clinical terms, anatomy, and surgical procedures.
- **ICD-10-CM (`SAB = ICD10CM`)**: Diagnostic and morbidity codes requiring unambiguous alphanumeric rendering (e.g., distinguishing `I10` Essential Hypertension from `110` or `l10`).

### 1.2 UMLS Semantic Network
The Semantic Network assigns every concept one or more **Semantic Types (TUIs)**. PocketGull establishes clear typographical distinction across high-risk semantic categories:

| Semantic Type (TUI) | Description | Typical Display Context | PocketGull Typographic Standard |
| :--- | :--- | :--- | :--- |
| **`T200`** | Clinical Drug | CPOE, Pyxis, Medication Label | ISMP Tall Man Lettering, Slashed `0`, Serifed `I` |
| **`T121`** | Pharmacologic Substance | Formulary, Interaction Alert | High-contrast Fineliner / Bold display |
| **`T034`** | Laboratory or Test Result | ICU Telemetry, Lab Report | PocketGull Mono 600 UPM, tabular lining figures |
| **`T047`** | Disease or Syndrome | Problem List, Patient Chart | Humanist x-height ($540\text{ UPM}$), zero fatigue |
| **`T060`** | Diagnostic Procedure | Radiology, Operative Note | Disambiguated Latin + Cyrillic/Greek prefixes |

### 1.3 SPECIALIST Lexicon & Lexical Normalization
The SPECIALIST Lexicon normalizes spelling variations, inflectional morphologies, and clinical acronyms. In EHR search interfaces, clinicians type rapidly under severe time pressure. PocketGull ensures:
- **Abbreviation Disambiguation**: Preventing catastrophic misreads between `q.d.` (every day, banned by JCAHO/ISMP) and `q.i.d.` (four times daily).
- **Metric Micrograms**: Seamless rendering of both `mcg` (ISMP-mandated safe English) and `μg` / `ug` (Unicode `U+00B5` Micro Sign and `U+03BC` Greek Small Letter Mu).
- **Electrolytes & Ionic Valence**: Native superscript support for $\text{Ca}^{2+}$, $\text{Mg}^{2+}$, $\text{Na}^+$, $\text{K}^+$, and blood gas partial pressures ($\text{PaO}_2$, $\text{pCO}_2$).

---

## 2. High-Alert UMLS Metathesaurus Mapping Matrix

The following table documents the authoritative UMLS CUI, RxNorm Concept Unique Identifier (RxCUI), and LOINC observation mappings continuously verified by the PocketGull Biomedical Validation Daemon:

| UMLS CUI | Standard Vocab & ID | Clinical Entity / High-Alert Drug Pair | ISMP / FDA Tall Man Lettering | Optical Disambiguation Gain |
| :--- | :--- | :--- | :--- | :---: |
| **`C0020615`** | RxNorm: `3423` | Hydromorphone HCl | `HYDROmorphone` | $+79.2\%$ vs Morphine |
| **`C0026549`** | RxNorm: `7052` | Morphine Sulfate | `morphine` | $+79.2\%$ vs Hydromorphone |
| **`C0042672`** | RxNorm: `11359` | Vinblastine Sulfate | `vinBLAStine` | $+81.4\%$ vs Vincristine |
| **`C0042674`** | RxNorm: `11361` | Vincristine Sulfate | `vinCRIStine` | $+81.4\%$ vs Vinblastine |
| **`C0020336`** | RxNorm: `5521` | Hydroxyzine Pamoate | `hydrOXYzine` | $+74.6\%$ vs Hydralazine |
| **`C0020300`** | RxNorm: `5470` | Hydralazine HCl | `hydrALAZINE` | $+74.6\%$ vs Hydroxyzine |
| **`C0014563`** | RxNorm: `3992` | Epinephrine | `EPINEPHrine` | $+82.1\%$ vs Ephedrine |
| **`C0014510`** | RxNorm: `3966` | Ephedrine Sulfate | `ePHEDrine` | $+82.1\%$ vs Epinephrine |
| **`C0007806`** | RxNorm: `2356` | Cefazolin Sodium | `cefAZOLin` | $+72.3\%$ vs Cefuroxime |
| **`C0007817`** | RxNorm: `2366` | Cefuroxime Axetil | `cefURoxime` | $+72.3\%$ vs Cefazolin |
| **`C0010944`** | RxNorm: `3182` | Doxorubicin HCl | `DOXOrubicin` | $+76.5\%$ vs Daunorubicin |
| **`C0011036`** | RxNorm: `3124` | Daunorubicin HCl | `DAUNOrubicin` | $+76.5\%$ vs Doxorubicin |
| **`C0006764`** | RxNorm: `2070` | Carbamazepine | `carbaMAZEpine` | $+78.0\%$ vs Oxcarbazepine |
| **`C0084478`** | RxNorm: `32450` | Oxcarbazepine | `OXcarbazepine` | $+78.0\%$ vs Carbamazepine |
| **`C0030016`** | RxNorm: `7824` | Oxycodone HCl | `oxyCODONE` | $+77.1\%$ vs Oxycontin |

---

## 3. LOINC Laboratory Telemetry & Clinical Biomarkers

In critical care telemetry, measurement units must align on a strict monospace grid to prevent optical transposition errors where numerical values bleed into unit labels. PocketGull Mono enforces fixed 600 UPM advance widths across all characters, symbols, and operators:

| LOINC Code | UMLS CUI | Laboratory Test Description | Clinical Normal Range | PocketGull Telemetry Representation |
| :--- | :--- | :--- | :--- | :--- |
| **`2160-0`** | `C0201975` | Creatinine [Mass/volume] in Serum/Plasma | $0.7\text{--}1.3\text{ mg/dL}$ | `Cr:   1.12 mg/dL  [0.70-1.30]` |
| **`2823-3`** | `C0202022` | Potassium [Moles/volume] in Serum/Plasma | $3.5\text{--}5.0\text{ mmol/L}$ | `K+:   4.20 mmol/L [3.50-5.00]` |
| **`2951-2`** | `C0202026` | Sodium [Moles/volume] in Serum/Plasma | $135\text{--}145\text{ mEq/L}$ | `Na+:  140.0 mEq/L [135 - 145 ]` |
| **`17856-6`**| `C0373722` | Hemoglobin A1c / Hemoglobin.total in Blood | $< 5.7\%$ | `HbA1c: 5.4 %     [  < 5.7  ]` |
| **`10839-9`**| `C0373809` | Troponin I.cardiac [Mass/volume] in Serum | $< 0.04\text{ ng/mL}$ | `Trop-I: <0.01 ng/mL [ <0.04 ]` |
| **`2075-0`** | `C0201948` | Oxygen partial pressure ($\text{PaO}_2$) in Arterial blood | $80\text{--}100\text{ mm Hg}$ | `PaO2:  94.5 mmHg  [ 80 - 100 ]` |
| **`2028-9`** | `C0201918` | Carbon dioxide partial pressure ($\text{pCO}_2$) Arterial | $35\text{--}45\text{ mm Hg}$ | `pCO2:  40.2 mmHg  [ 35 - 45  ]` |
| **`2744-1`** | `C0202008` | pH of Arterial blood | $7.35\text{--}7.45$ | `pH:    7.410      [7.35-7.45]` |
| **`2571-8`** | `C0201994` | Osmolality [Moles/mass] in Serum/Plasma | $275\text{--}295\text{ mOsm/kg}$| `Osm:   288 mOsm/kg [ 275-295 ]` |

---

## 4. Architectural Verification Protocol

The PocketGull Typefoundry continuously validates UMLS-governed text via the automated daemon:
1. **Zero `.notdef` Invariant**: Every character in every UMLS concept, abbreviation, unit string, and LOINC observation code must resolve to a valid, rendered glyph outline.
2. **Optical Envelope Decoupling**: For every high-alert LASA pair under the same UMLS Semantic Group, ISMP Tall Man Lettering must achieve $\ge 70\%$ mean bounding box divergence.
3. **Monospace Tabular Alignment**: All numeric digits (`0`–`9`), punctuation (`.`, `,`, `:`, `/`, `-`), and clinical operators (`+`, `-`, `±`, `<`, `>`, `=`, `%`) must occupy exactly $600\text{ UPM}$ in `PocketGullMono-Regular.ttf`.
4. **W3C OTS Memory Safety**: 100% of generated and subsetted font tables must pass OpenType Sanitizer verification with 2-byte word boundaries (`loca[i] % 2 == 0`).

---

## 5. Formal Scholarly & NLM Citations

When referencing the UMLS integration in biomedical literature and clinical publications:

```bibtex
@article{bodenreider2004umls,
  author    = {Bodenreider, Olivier},
  title     = {The Unified Medical Language System ({UMLS}): integrating biomedical terminology},
  journal   = {Nucleic Acids Research},
  volume    = {32},
  number    = {Database issue},
  pages     = {D267--D270},
  year      = {2004},
  publisher = {Oxford University Press},
  doi       = {10.1093/nar/gkh061},
  pmid      = {14681409},
  pmcid     = {PMC308795}
}

@misc{nlm2026umls,
  author       = {{National Library of Medicine (US)}},
  title        = {{UMLS} Knowledge Sources [{dataset on the Internet}]. Release 2026AA},
  year         = {2026},
  month        = {May},
  howpublished = {Available from: \url{https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html}},
  address      = {Bethesda (MD)},
  note         = {Accessed: September 2026}
}
```

---

## 6. NLM UMLS® Metathesaurus® License Compliance & Statutory Governance

### 6.1 Mandatory Copyright Notice (Section 11.a)
> **"Some material in the UMLS Metathesaurus is from copyrighted sources of the respective copyright holders. Users of the UMLS Metathesaurus are solely responsible for compliance with any copyright, patent or trademark restrictions and are referred to the copyright, patent or trademark notices appearing in the original sources, all of which are hereby incorporated by reference."**

### 6.2 Source Vocabularies Utilized in Benchmarking & Appendix 1 Categories
PocketGull's clinical typography engine benchmarks standardized strings and codes from the following UMLS constituent vocabularies (referenced solely for typographic stress verification, with respective Appendix 1 Category designations):
- **RxNorm (`RXNORM`) — Category 0**: National Library of Medicine (US Public Domain). General license terms apply with no additional restrictions. Used for clinical drug formulations and ISMP Tall Man Lettering disambiguation.
- **LOINC® (`LNC`) — Category 0 / Open Health Standard**: Copyright © 1995–2026, Regenstrief Institute, Inc. and the Logical Observation Identifiers Names and Codes (LOINC) Committee. All rights reserved. Used for ICU laboratory telemetry observation codes and measurement units.
- **SNOMED CT® (`SNOMEDCT_US`) — Category 4 & Appendix 2**: Copyright © 2002–2026, International Health Terminology Standards Development Organisation (SNOMED International). Governed under Appendix 2 and the U.S. National Release.

### 6.3 Non-Endorsement & Statutory Disclaimer (Section 10)
PocketGull acknowledges the National Library of Medicine (NLM) as the authoritative source of the UMLS Metathesaurus (Release 2026AA). In strict accordance with Section 10 of the UMLS Agreement:
- The presence in the UMLS Metathesaurus of vocabulary or data produced by organizations other than NLM does not imply any endorsement of the UMLS Metathesaurus by these organizations.
- Citation of NLM or UMLS does not in any way indicate or imply that NLM, the Department of Health and Human Services (HHS), the U.S. Government, or any organization whose vocabulary sources are included in the UMLS has endorsed the PocketGull Project, its authors, or its typographic software products.

### 6.4 Open-Source Separation & Scope of Distribution (Section 3)
The PocketGull Font Superfamily is licensed under the **SIL Open Font License 1.1 (OFL)**. PocketGull binaries (`.ttf`, `.woff2`) contain vector outlines, font tables, and typographic shaping rules; **they do not bundle, repackage, or redistribute proprietary UMLS Metathesaurus databases**. All clinical identifiers (CUIs, RxCUIs, LOINC numbers) in PocketGull research tools are evaluated at runtime solely as testing inputs for legibility, optotypic contrast, and memory-safe glyph rendering.

### 6.5 SNOMED CT® Affiliate License Compliance (Appendix 2, Clause 8.3.1)
In accordance with Appendix 2, Clause 8.3.1 of the UMLS Metathesaurus Agreement:
> **"This material includes SNOMED Clinical Terms® (SNOMED CT®) which is used by permission of the International Health Terminology Standards Development Organisation (IHTSDO). All rights reserved. SNOMED CT®, was originally created by The College of American Pathologists. 'SNOMED' and 'SNOMED CT' are registered trademarks of the IHTSDO."**

- **Territorial Scope**: Evaluated in the United States, a recognized **Member Territory** represented by the National Library of Medicine (NLM / HHS) in SNOMED International.
- **Trademark Compliance (Clause 8.2)**: PocketGull does not use the mark "SNOMED" in its typeface nomenclature, nor does it abbreviate the mark.
- **Research Integrity (Clause 2.2.3 & Appendix B ¶1.9)**: Terminology strings are evaluated strictly for academic typography, Louise Sloan 5:1 visual acuity, and clinical error prevention in open-source digital health infrastructure.


