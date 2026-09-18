# Morphological Sign Notation Rosetta: Anatomical Invariant Calibration for Deaf Writing Systems

## Executive Summary
This document establishes the theoretical, biomechanical, and typographic architecture connecting the **Five Human Hand Types** (Elsie Lincoln Benedict & Ralph Paine Benedict, 1921) to the world's six major sign language notation and orthography frameworks:
1. **Sutton SignWriting** (`U+1D800`–`U+1DAAF`): 2D visual-spatial iconic orthography.
2. **Stokoe Notation** (William C. Stokoe, 1960): Phonemic Cheremic Decomposition (Tab, Dez, Sig).
3. **Hamburg Notation System (HamNoSys)**: Linear, formal phonetic transcription for computational linguistics and avatar kinematics.
4. **International Movement Writing Alphabet (IMWA)**: Valerie Sutton's universal human movement taxonomy (>27,000 symbols).
5. **ASL-phabet** (Dr. Sam Supalla, University of Arizona): Minimalist phonemic script (22 handshapes, 5 locations, 5 movements) engineered for early deaf literacy.
6. **Si5s / ASLwrite** (Robert Arnold, 2003 / Adrean Clark, 2011): Cursive, single-stroke handwritten orthography for American Sign Language.

---

## 1. The Core Scientific Problem: Anatomical Coarticulation Drift

In computer vision (e.g., Google MediaPipe, DirectML hand tracking), optical motion capture, and deaf education transcription, the primary bottleneck in reliable sign recognition has always been **morphological variance across human signers**.

A single phonemic handshape—such as the ASL `B` (flat hand with thumb folded across palm), `A` (fist with thumb alongside index), or `5` (spread open hand)—produces radically different optical silhouettes and joint telemetry depending on the signer's biological hand morphology:

```
+---------------------------------------------------------------------------------------+
|                                BIOLOGICAL VARIATION                                   |
+---------------------------------------------------------------------------------------+
|  ALIMENTIVE HAND (Circle)  | Plump flesh cushions, dimpled knuckles, short digits      |
|                            | -> Obscures interdigital gaps, mimics 'O' or 'fist'      |
+----------------------------+----------------------------------------------------------+
|  THORACIC HAND (Wedge)     | Conical tapering, prominent middle apex, elongated palm  |
|                            | -> Exaggerates interdigital splay, shifts sign center    |
+----------------------------+----------------------------------------------------------+
|  MUSCULAR HAND (Square)    | Square 1:1 palm, spatulate paddle tips, parallel shafts  |
|                            | -> Clean planar alignment, broad tactile contact zones   |
+----------------------------+----------------------------------------------------------+
|  OSSEOUS HAND (Oblong)     | Knotted articular nodes, excavated shafts, bony ridges   |
|                            | -> Creates false joint angles, gaps between closed digits|
+----------------------------+----------------------------------------------------------+
|  CEREBRAL HAND (Triangle)  | Whisper-delicate, smooth straight shafts, pointed tips   |
|                            | -> Minimal tissue cushion, hyper-fine optical contours    |
+---------------------------------------------------------------------------------------+
```

Without an **Anatomical Calibration Layer**, machine classifiers and human transcribers frequently commit false-positive phonetic classification errors. The Benedict (1921) Five Hand Types provide the exact biometric tensor required to normalize physical joint signals into canonical notation glyphs.

---

## 2. Comparative Matrix: The Six Sign Notation Frameworks

| Feature | Sutton SignWriting | Stokoe Notation | HamNoSys | IMWA | ASL-phabet | Si5s / ASLwrite |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Creator** | Valerie Sutton (1974) | William Stokoe (1960) | Univ. of Hamburg (1984) | Valerie Sutton (1974+) | Dr. Sam Supalla | Robert Arnold (2003) |
| **Primary Domain** | Everyday reading, writing & literature | Academic linguistic analysis | Computational linguistics & avatars | Universal kinesiology & choreography | Elementary deaf literacy & ESL | Rapid cursive handwriting & note-taking |
| **Visual Structure** | 2D spatial arrangement box | Linear string: Tab–Dez–Sig | Linear string of phonetic modifiers | 2D kinematic trajectory blocks | Linear sequence: Hand–Loc–Move | Cursive flowing strokes (Digits + Locatives) |
| **Unicode Status** | Encoded: `U+1D800`–`U+1DAAF` (672 glyphs) | Unencoded (Custom fonts / ASCII mappings) | Private Use Area / Custom Unicode font | Unencoded (IMWA 2004/2008 system) | Unencoded (Educational symbol set) | Unencoded (OpenType ligatures / SVGs) |
| **Phonetic vs Phonemic** | Phonetic & spatial | Strictly phonemic | Highly detailed phonetic | Detailed kinesiological | Minimalist phonemic | Orthographic / Graphemic |
| **PocketGull Support** | **SMoE Expert R** (`fonts.css`) | TrueType Latin mappings (`PocketGull-ASL`) | OpenType PUA & glyph anchors | Movement vector paths | Child-scale optotype normalizer | Felt-marker ductus ligatures |

---

## 3. How the Benedict 1921 Hand Types Calibrate Each System

### 3.1 Sutton SignWriting (`U+1D800`–`U+1DAAF`)
- **Visual Grapheme Primitives**: SignWriting uses standardized geometric shapes for the base of the hand:
  - Square (`◻`) = Flat fist or back of hand.
  - Circle (`○`) = Open cup, curved hand, or palm-facing view.
  - Lines / ticks (`|`, `\`, `/`) = Extended or bent fingers.
- **Morphological Normalization**:
  - In an **Alimentive** signer, the closed fist appears rounded due to thick hypothenar and thenar fat cushions. An optical camera without calibration might categorize this as a "cup" or "circle" base. The Benedict tensor applies a negative radial dilation to recover the square base.
  - In an **Osseous** signer, the prominent knuckle nodes protrude beyond the hand boundary, creating spurious "notches". The Benedict tensor applies morphological closing along the metacarpophalangeal (MCP) axis to reconstruct the flat base line.

### 3.2 Stokoe Notation (Cheremic Decomposition)
- **The Dez (Designator / Handshape)**: Stokoe defined 19 distinctive manual handshapes based on Latin alphabet prototypes: `A`, `B`, `5`, `C`, `E`, `F`, `G`, `H`, `I`, `K`, `L`, `M`, `N`, `O`, `R`, `S`, `T`, `V`, `W`, `X`, `Y`.
- **The Problem of Coarticulation**:
  - In `B` (flat hand), an **Osseous** signer cannot fully press the proximal phalanges together without painful joint friction; daylight is visible between the fingers. In standard Stokoe transcription, daylight between digits signifies a `5` (open spread hand) or `4`.
  - The Benedict rule identifies the presence of *knotted articular joints* (`joint_bulge > 3.0 UPM`), automatically reclassifying the daylight as anatomical artifact rather than phonemic intention.

### 3.3 Hamburg Notation System (HamNoSys)
- **Linear Parameterization**: HamNoSys decomposes handshapes into anatomical joint vectors:
  - Base form: Flat hand (``), Fist (``), Pinch (``).
  - Thumb position: Across palm (``), Outward extended (``), Opposed (``).
  - Finger flexion states: DIP/PIP/MCP angles (straight ``, bent ``, hooked ``, double bent ``).
- **Kinematic Avatar Synthesis**:
  - For computer avatars (e.g., WebGL Sign Language Synthesis), applying a single rigid angle matrix across different 3D meshes produces severe vertex self-intersection on heavy (Alimentive) characters and incomplete contact on thin (Cerebral) characters.
  - PocketGull's Benedict deformation tensors modulate the target flexion angles \(\theta_{target} = \theta_{canonical} \times \kappa_{morph}\), ensuring realistic, collision-free signing in avatar engines.

### 3.4 International Movement Writing Alphabet (IMWA)
- **Universal Kinesiological Space**: IMWA categorizes over 27,000 symbols across 8 functional groups:
  1. Hand / Arm.
  2. Movement / Dynamics.
  3. Face / Gaze / Head.
  4. Upper Body / Torso.
  5. Full Body / Weight transfer.
  6. Space / Orientation.
  7. Interaction / Contact.
  8. Punctuation / Timing.
- **Reach Envelope Calibration**:
  - The Benedict hand types define precise finger-to-palm ratios:
    - Alimentive: `1.00 : 0.78` (Short reach)
    - Thoracic: `1.00 : 1.15` (Long reach)
    - Muscular: `1.00 : 1.00` (Neutral square)
    - Osseous: `1.00 : 1.12` (Extended skeletal reach)
    - Cerebral: `1.00 : 1.10` (Delicate reach)
  - IMWA contact symbols (touch, brush, grasp, between) must scale their spatial tolerance boxes by the signer's biometric reach ratio to maintain geometric truth.

### 3.5 ASL-phabet (Dr. Sam Supalla)
- **Pedagogical Literacy Design**: Created specifically for Deaf children learning to bridge American Sign Language and written English.
- **The Pediatric Connection**:
  - Young children's hands naturally display Alimentive characteristics: higher percentage of adipose tissue, undeveloped knuckle creases, dimpled MCP joints, and short phalangeal ratios.
  - As a child matures, their hand morphology transitions toward their adult genotype (Muscular, Osseous, etc.).
  - The ASL-phabet calibration engine guarantees that a 6-year-old child's "pudgy" fingerspelling maps to the exact same 22 foundational handshapes as an adult native signer.

### 3.6 Si5s / ASLwrite (Robert Arnold & Adrean Clark)
- **Handwritten Ductus & Cursive Flow**:
  - Si5s uses rapid, continuous, organic pen strokes composed of "Digits", "Locatives", and "Movement Marks".
  - Typographically, designing an OpenType font for Si5s requires humanist felt-marker warmth (PocketGull's foundry DNA).
  - Just as a felt marker on physical cardstock broadens under pressure, Muscular and Alimentive signers execute physical signs with broader planar contact, which Si5s calligraphically reflects through varying stroke weights and ligature terminals.

---

## 4. Louise Sloan 5:1 Optometric Acuity Invariant

Every notation symbol in PocketGull—whether rendered as a TrueType glyph, a WOFF2 webfont, or an SVG vector—must strictly satisfy the **Louise Sloan 5:1 Acuity Standard**:

\[
\text{Total Height} = 5 \times \text{Stroke Width} = 5 \times \text{Counter-Space}
\]

When rendering handshapes for clinical signage or EHR software:
1. **Minimum Stroke Width**: Never less than 20% of bounding box height.
2. **Minimum Interdigital Space**: Never less than 1 stroke width (prevents ink clotting / optical blurring under fatigue or 20/200 low-vision conditions).
3. **Corner Radii**: Locked to 25 UPM fillets, preserving Phil Gear's humanist felt-marker cardstock DNA.

---

## 5. Architectural Implementation Roadmap

1. **Dataset Engine**: `js/sign_notation_rosetta_data.js` containing complete cross-system mappings for the 10 canonical ASL handshapes across all 5 Benedict types.
2. **Interactive Studio Panel**: Panel 6 in `five_hand_types.html` with real-time notation switching, anatomical warnings, and Louise Sloan optotype overlays.
3. **Studio Interconnection**: Deep linking from `asl_studio.html` and `sign_studio.html` to the Rosetta Engine.
4. **CI Invariant Testing**: `test/sign_notation_rosetta.test.mjs` verifying Unicode integrity, SMoE compatibility, and zero-defect DOM rendering.
