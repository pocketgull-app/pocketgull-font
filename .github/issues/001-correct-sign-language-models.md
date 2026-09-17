# Issue #001: Correct the Sign Language Models (ASL Phonological Invariants & Benedict Biometrics)

**Status**: Open / In Progress  
**Priority**: High (Clinical & Accessibility Accuracy)  
**Components**: `scripts/generate_morphological_asl_svgs.py`, `scripts/compile_sign_font.py`, `js/asl_morph_svg_data.js`, `asl_studio.html`, `five_hand_types.html`  
**Tags**: `accessibility`, `asl`, `typography`, `biometrics`, `clinical-safety`

---

## 1. Problem Statement & Motivation
While the initial procedural synthesizers for the PocketGull Sign Language subfamily successfully proved the concept of variable morphological hand types, several characters and orientations deviate from authentic American Sign Language (ASL) phonological standards (Stokoe 1960, Battison 1978) and exhibit geometric bounding-box collisions.

In life-critical clinical environments (ICU bedside communication, emergency triage for non-verbal and deaf patients), handshape ambiguity can lead to severe miscommunication. Furthermore, previous documentation contained archaic terminology ("Kite") which is phonetically and visually confounding.

---

## 2. Mandatory Phonological Invariants (Stokoe & Battison)

### A. Battison Medial Radial Orientation for Inward Digits (G & H)
- **Defect**: Early 2D vector SVGs rendered the letter **G** and **H** with an outward dorsal or palmar projection with fingers pointing upward or horizontally outward.
- **Correction Requirement**: In authentic ASL, **G** (index extended) and **H** (index + middle extended) are signed with the radial edge up, dorsal surface of the fingers facing forward/outward, and fingers pointing *horizontally across the signer's torso toward the non-dominant side* (Medial Radial profile). The wrist enters from the lateral bottom, and the knuckle block faces the viewer.

### B. Battison Inferior Pronated Drop for Downward Digits (P & Q)
- **Defect**: Signs for **P** and **Q** were missing or rendered upright.
- **Correction Requirement**:
  - **P**: Morphologically equivalent to a **K** handshape, but with the forearm pronated and wrist flexed downward so that the index finger points strictly inferiorly (towards the floor) and the middle finger extends horizontally inward with the thumb braced against its first interphalangeal joint.
  - **Q**: Morphologically equivalent to a **G** handshape, but pronated downward with index finger and thumb pointing directly inferiorly toward the floor.

### C. Stokoe Fist Disambiguation Suite (A / S / T / M / N)
- **Defect**: Early fist models shared identical contour silhouettes, failing ISMP optical disambiguation.
- **Correction Requirement**:
  - **A**: Thumb strictly erect, adducted flush alongside the lateral radial margin of the closed index knuckle.
  - **B/S**: In **S**, the thumb wraps transversely across the anterior mid-phalanges of all four clenched digits.
  - **T**: The thumb tip penetrates interdigitally between the index and middle fingers, protruding prominently above the knuckle crest.
  - **M**: The thumb is tucked under the first three digits (index, middle, ring), emerging slightly between ring and pinky.
  - **N**: The thumb is tucked under the first two digits (index, middle), emerging between middle and ring.

### D. Strict "Closed E" Shelf Discipline
- **Defect**: Initial models exhibited an open "screaming claw" posture with curled fingertips floating above an open palm.
- **Correction Requirement**: Authentic clinical ASL requires a "Closed E" where all four distal fingernail pads rest firmly on the horizontal shelf created by the adducted thumb across the optical waistline ($y \approx 65\text{ UPM}$ in SVG space).

### E. Louise Sloan 5:1 Acuity for Multi-Finger Uprights (U vs. V vs. W vs. B)
- **Defect**: Insufficient angular distinction between U and V at low optical resolutions ($\le 16\text{px}$).
- **Correction Requirement**:
  - **U**: Digits II and III strictly parallel and adducted ($0^\circ$ separation, touching contours).
  - **V**: Digits II and III abducted at a distinct angular wedge ($22^\circ$–$28^\circ$ depending on hand archetype).
  - **W**: Digits II, III, and IV uniformly abducted in a balanced three-digit trident fan ($14^\circ$–$18^\circ$ inter-finger separation).

### F. Kinetic Trajectory Vectors for Dynamic Signs (J & Z)
- **Defect**: Static vector glyphs cannot represent signs whose fundamental phoneme is path movement (SIG).
- **Correction Requirement**: Synthesize high-contrast dashed motion trajectory paths (e.g. vibrant amber `#f59e0b` stroked bezier) showing the J-hook wrist swivel and the Z triple-stroke zigzag.

---

## 3. Benedict Morphological Hand Types Standardization

All signs must dynamically adapt across the five Elsie Lincoln Benedict (1921) archetypes without compromising the phonological invariants above:

1. **Alimentive**: Spherical / Chubby (dimples at knuckle folds, short conical/spatulate fingers, low joint protrusion, ratio $0.85:1$).
2. **Thoracic**: **The Conical Wedge** ($\Diamond$, narrow wrist $0.72:1$, elongated conical fingers, dominant middle finger apex, high agile elevation).  
   *Note: All legacy occurrences of the term "Kite" have been permanently removed and replaced with "Wedge / Conical".*
3. **Muscular**: The Square (orthogonal palm, sturdy rectangular fingers, firm square nail beds, ratio $0.95:1$).
4. **Osseous**: The Oblong / Knotty (prominent calcified knuckle nodes, sunken interosseous spaces, elongated rectangular phalanx bars).
5. **Cerebral**: The Inverted Triangle (slender tapering palm, delicate needle fingertips, graceful thumb elevation, ratio $1.15:1$).

---

## 4. Typographic & Vector Invariants
- **100% PocketGull Typography**: All specimen labels, calipers, badges, and instructional headers must be rendered exclusively in `PocketGull` and `PocketGull Mono`. External fallback fonts (`Atkinson Hyperlegible`, generic sans-serif) are prohibited.
- **Bounding Box Integrity**: Zero contour, leader line, or caliper text may exceed the designated SVG `viewBox` ($0\ 0\ 100\ 120$ for single signs, $-100\ 0\ 680\ 520$ for 5-hand plates).
- **Font Binary Health**: Compiled sign fonts (`PocketGull-Sign.ttf`, `PocketGull-ASL.ttf`) must maintain 2-byte word boundaries (`loca[i] % 2 == 0`), bit-7 flag masking, and 100% pass rate in W3C OTS sanitization.
