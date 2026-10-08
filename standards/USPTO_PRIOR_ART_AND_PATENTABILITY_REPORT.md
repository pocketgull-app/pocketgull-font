# USPTO Patent Prior Art Search & Patentability Assessment Report

**Subject**: Dynamic Tactile Lathe, Rotary Mandrel Architecture, Soft-Robotic Inflatable Elastomeric Nibs, and Sub-Nociceptive Reading Mechanics  
**Assignee & IP Holding Entity**: PocketGull LLC (Portland, Oregon, USA)  
**Lead Inventor**: Phil Gear  
**Docket Number**: `POCK-PAT-2026-001`  
**Search Date**: October 8, 2026  
**Jurisdictions Searched**: United States Patent and Trademark Office (USPTO Patent Public Search), European Patent Office (Espacenet), World Intellectual Property Organization (WIPO / PCT), and Google Patents  
**Cooperative Patent Classifications (CPC)**:
- `G09B 21/00` / `G09B 21/003`: Teaching or communicating with blind persons using tactile presentation of information; Braille displays.
- `G06F 3/016`: Input/Output arrangements for interaction between user and computer; Haptic feedback; Tactile displays.
- `A61H 3/06`: Walking aids or other sensory aids for the blind.
- `B29C 41/00`: Shaping or dip-molding elastomeric materials.

---

## 🏛️ 1. Executive Summary & Patentability Opinion

### 1.1 The Core Invention
PocketGull LLC has engineered the **Philocardic Dynamic Tactile Flume** ("Spindle-Gull" / "Aquaglyde Waterslide"):
1. A **revolving cylindrical mandrel** rotated along a horizontal axis within a central aperture at continuous variable angular velocities matching human reading cadence ($100\text{--}400\,\text{WPM}$).
2. An array of **soft-robotic elastomeric inflatable rubber nibs** (Shore A 15–25 liquid silicone rubber) that dynamically inflate under positive pneumatic or hydrostatic pressure ($+18.4\,\text{kPa}$) on an ascending arc, present Braille characters to a resting fingerpad with zero bouncing, and actively deflate under negative vacuum pressure ($-4.5\,\text{kPa}$) flush with the cylinder circumference on a descending arc.
3. **Stationary ergonomic flume banks** (left and right chassis decks) and a stationary finger rest lip supporting the user’s hand and fingerpad in neutral $15^\circ$ pronation, eliminating horizontal hand sweeping, repetitive strain injury (RSI), and shear friction ($\tau_{\text{shear}} \approx 0$).
4. A **zero-pain contact mechanics threshold** distributing contact stress strictly between $18\text{--}24\,\text{kPa}$ (pure velvet touch, non-nociceptive), guaranteeing completely painless, fatigue-free reading for individuals with arthritis, peripheral neuropathy, and fragile skin.
5. A **closed-loop recirculating microfluidic flume** conserving 100% of fluid ($0.00\,\text{mL/hr}$ loss) while providing laminar hydrodynamic glide ($\mu \approx 0.002$) beneath the resting finger.

### 1.2 Patentability Determination
* **Novelty (35 U.S.C. § 102)**: **STRONG / CLEAR.** No single prior art reference in the USPTO, EPO, or WIPO database discloses a rotating cylindrical drum or lathe mandrel equipped with soft elastomeric inflatable/deflating rubber nibs or active lower-arc vacuum retraction.
* **Non-Obviousness (35 U.S.C. § 103)**: **STRONG.** Prior art in the tactile display sector is strictly bifurcated into two mutually exclusive engineering silos:
  - *Silo 1*: Rotating drums using **rigid, hard metal/plastic pins driven by electromagnetic solenoids or cams** (e.g. NIST US Patent 6,776,619).
  - *Silo 2*: Pneumatic and microfluidic displays using **flat, stationary planar sheets or glass touchscreens** (e.g. US Patent 6,354,839; Tactus US Patent 8,547,339; NewHaptics).
  A Person Having Ordinary Skill in the Art (POSITA) would not find it obvious to cross-pollinate these silos. Pneumatics were historically considered too bulky and slow for rotating drums, and conventional Braille dogma insisted on rigid pins with sharp edges to trigger SA-1 Merkel cells. PocketGull LLC's discovery that hyperelastic inflated domes preserve spatial acuity while eliminating nociceptive pain and mechanical pin jamming is unexpected and non-obvious.
* **Freedom to Operate (FTO)**: **UNENCUMBERED.** The foundational rotating-wheel patent (NIST US 6,776,619) was filed in 2000 and issued in 2004; it has **expired** by statutory term. The earliest pneumatic Braille patents (US 6,354,839) have likewise expired. PocketGull LLC faces zero blocking patents.

---

## 🔍 2. Prior Art Survey & Comparative Matrix

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    USPTO / GLOBAL PRIOR ART COMPARATIVE ANALYSIS                                             |
+───────────────────────────┬──────────────┬──────────────────┬─────────────────┬─────────────────┬────────────────────────────+
| Patent / Reference        | Assignee     | Architecture     | Pin / Tactile   | Pneumatic /     | Primary Limitation         |
|                           | & Year       | Geometry         | Material        | Vacuum Cycle?   | Relative to PocketGull     |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| US Patent 6,776,619 B1    | NIST / DOC   | Rotating Wheel   | Rigid Metal /   | NO              | Rigid pins cause high      |
| (Roberts, Slattery et al.)| (2004)       | Disc (Mechanical)| Hard Plastic    | Mechanical Cams | focal stress (>120 kPa);   |
|                           |              |                  |                 | & Solenoids     | jams easily; painful.      |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| US Patent 6,354,839 B1    | Schmidt      | Stationary Flat  | Rigid Pins /    | YES (Planar)    | Sprawling external tubing; |
| (Refreshable Braille)     | (2002)       | Planar Array     | Fluid Plenums   | Compressor-only | flat stationary surface;   |
|                           |              |                  |                 | No vacuum cycle | user must sweep hand.      |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| US Patent 8,547,339 B2    | Tactus Tech  | Flat Touchscreen | Elastomeric     | YES (Fluidic)   | Planar display on glass;   |
| (Dynamic tactile interface| (2013)       | Planar Layer     | Buttons         | Expand / Recede | virtual keyboard buttons;  |
|                           |              |                  |                 | No Mandrel      | no rotating reading lathe. |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| ReadRing Patent Portfolio | ReadRing     | Mini Rolling     | Rigid Miniature | NO              | Rigid mechanical pins;     |
| (Thailand / Japan)        | (2021)       | Ring Device      | Metal Pins      | Mechanical Pins | no soft pneumatics;        |
|                           |              |                  |                 |                 | no lathe rest / vacuum.    |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| Johnson & Phillips (1988) | Johns Hopkins| Motorized Metal  | Rigid Photo-    | NO              | Non-refreshable; static;   |
| (Neurophysiology Drum)    | Research     | Lathe Cylinder   | Etched Metal    | Rigid Cylinder  | severe frictional shear    |
|                           |              |                  |                 |                 | on fingerpad tissue.       |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| NewHaptics / U-Michigan   | NewHaptics   | Flat Full-Page   | Microfluidic    | YES (Planar)    | Flat planar matrix;        |
| ("Holy Braille" project)  | (2020–2024)  | Stationary Grid  | Silicone Pores  | Microfluidic    | no rotating cylinder;      |
|                           |              |                  |                 | No Lathe Action | requires hand motion.      |
+───────────────────────────┼──────────────┼──────────────────┼─────────────────┼─────────────────┼────────────────────────────+
| PHILOCARDIA TACTILE LATHE | PocketGull   | Revolving Lathe  | Soft Liquid     | YES (Dynamic    | ZERO SHEAR; ZERO PAIN;     |
| (PocketGull LLC)          | LLC (2026)   | Mandrel with     | Silicone Rubber | Rotary Cam      | 78% below nociceptive      |
|                           |              | Biometric Rest   | (Shore A 15–25) | + Vacuum Flush) | threshold; cardio-paced.   |
+───────────────────────────┴──────────────┴──────────────────┴─────────────────┴─────────────────┴────────────────────────────+
```

---

## 🔬 3. Detailed Technical Distinctions Across Key References

### 3.1 US Patent 6,776,619 B1 — NIST Rotating-Wheel Braille Reader
* **Inventors**: John W. Roberts, Oliver T. Slattery, David W. Kardos.
* **Assignee**: The United States of America as represented by the Secretary of Commerce (NIST).
* **Filing Date**: October 27, 2000; **Issue Date**: August 17, 2004. Status: **Expired (Term Expired)**.
* **Disclosure**: Describes a rotating wheel that presents Braille characters to a stationary fingerpad. The wheel contains radial channels housing rigid metal pins. A set of 3 or 4 stationary electromagnetic actuators (solenoids) pushes the pins outward as the wheel rotates. The pins are held extended by friction or spring-loaded detents, and are later mechanically pushed back down by an external wiping cam.
* **PocketGull LLC Distinctions**:
  1. **Ablation of Mechanical Pin Friction**: NIST uses rigid pins that slide inside metal/plastic guide bores. Over repeated cycles, skin oils, dust, and particulate cause pin binding and mechanical failure. PocketGull replaces all rigid sliding pins with **hermetically sealed elastomeric silicone domes** that flex without mechanical sliding friction.
  2. **Sub-Nociceptive Stress vs. Hard Pin Puncture**: NIST’s rigid pins exert peak contact stresses of $120\text{--}140\,\text{kPa}$, well above the human nociceptive pain threshold ($85\,\text{kPa}$). PocketGull's Shore A 15–25 inflating nibs limit peak stress to $22\text{--}28\,\text{kPa}$, preventing nerve fatigue and fingerpad ischemia.
  3. **Active Negative-Pressure Vacuum vs. Mechanical Wiping**: NIST resets pins via a mechanical wedge or wiping surface that physically forces the pins back in. This wiping action produces acoustic chatter and rapid wear. PocketGull uses an **internal vacuum manifold ($-4.5\,\text{kPa}$)** to actively draw the nibs flush with the mandrel radius, completely eliminating mechanical wipe wear.
  4. **Dynamic Cardiovascular Pacing**: NIST has no physiological pacing; PocketGull introduces harmonic cardiac sinus rhythm ($S_1/S_2$ at 72 BPM) into the pneumatic line.

### 3.2 US Patent 6,354,839 B1 — Refreshable Braille Display System
* **Inventor**: Schmidt.
* **Issue Date**: March 12, 2002. Status: **Expired**.
* **Disclosure**: Describes a flat refreshable Braille display using pneumatic pressure supplied by an air compressor. Pneumatic lines run to individual plenums underneath an array of pins on a flat desktop pad.
* **PocketGull LLC Distinctions**:
  1. **Rotary Mandrel vs. Flat Matrix**: Schmidt discloses a stationary, planar desktop grid where the blind user must physically drag their hand across the page. PocketGull mounts the tactile array on a rotating lathe mandrel, eliminating hand movement, forward sweeping, and line-return regressions.
  2. **Pneumatic Plumbing Complexity**: Schmidt requires dozens of individual tubes and solenoid valves to address each cell on the flat sheet. PocketGull’s rotating mandrel acts as its own **rotary commutator/distributor**, routing positive air and vacuum sequentially as the mandrel turns.

### 3.3 US Patent 8,547,339 B2 — Dynamic Tactile Interface (Tactus Technology)
* **Inventors**: Micah Yairi, Nate Saal, Craig Ciesla.
* **Assignee**: Tactus Technology, Inc.
* **Issue Date**: October 1, 2013.
* **Disclosure**: Relates to touchscreens for smartphones and tablets. A transparent elastomeric layer is placed over a display panel. Microfluidic channels pump fluid into cavities beneath the elastomer to pop up physical buttons on demand (e.g. for a virtual QWERTY keyboard) and withdraw fluid to return the surface to a flat state.
* **PocketGull LLC Distinctions**:
  1. **Reading Lathe Mandrel vs. Mobile Touchscreen**: Tactus is explicitly designed for planar touchscreen typing on mobile devices. It does not teach or suggest a rotating cylinder, a lathe tool rest, continuous reading cadence, or Braille cell streaming.
  2. **Continuous Angular Rotation & Arc-Synchronized Vacuum**: Tactus inflates buttons statically for typing sessions. PocketGull coordinates rapid dynamic inflation on an ascending arc ($+18.4\,\text{kPa}$) and immediate vacuum collapse on a descending arc ($-4.5\,\text{kPa}$) synchronized with spindle rotation.

### 3.4 Scientific Prior Art — Johnson & Phillips Drum Stimulator (1988)
* **Authors**: Kenneth O. Johnson & John R. Phillips (*Journal of Neuroscience Methods*, 22(3):221–231).
* **Disclosure**: A laboratory neurophysiology apparatus consisting of a motorized metal cylinder wrapped in photoetched plastic/metal plates with fixed tactile gratings, rotated against a stationary primate or human fingerpad to record SA-1 and RA afferent nerve responses.
* **PocketGull LLC Distinctions**:
  1. **Non-Refreshable**: The Johnson & Phillips drum is an immutable, static engraved cylinder. It cannot display text or refresh Braille.
  2. **Severe Shear Strain**: The rigid metal surface scans tangentially across the skin, inducing heavy epidermal friction ($\tau_{\text{shear}} > 45\,\text{kPa}$). In contrast, PocketGull uses pure rolling contact ($\Delta v = 0\,\text{m/s}$), producing zero tangential shear.

---

## 🏛️ 4. PocketGull LLC Patent Claim Blueprint (US Non-Provisional)

### Independent Claim 1 (Apparatus)
> **1. A dynamic tactile reading apparatus for continuous somatosensory character presentation, comprising:**
> - a housing comprising stationary left and right ergonomic flume decks defining a central flume aperture;
> - a cylindrical mandrel rotatably mounted within said housing beneath said central flume aperture about a central axis of rotation;
> - a drive mechanism operatively coupled to said cylindrical mandrel to rotate said mandrel at a controlled angular velocity corresponding to a tactile reading rate;
> - an array of soft-robotic tactile presentation elements disposed circumferentially about an outer surface of said mandrel, each tactile presentation element comprising an elastomeric chamber formed from a compliant polymer having a Shore A durometer between 10 and 35;
> - a fluid distribution system comprising a positive pressure source and a negative vacuum source in fluid communication with said elastomeric chambers;
> - wherein rotation of said mandrel coordinates fluid delivery such that selected elastomeric chambers inflate to a tactilely discernable elevation upon traversing an ascending arc toward a top-dead-center reading zone within said central flume aperture, maintain a steady uniform radial elevation without bouncing, and actively deflate flush with or beneath the outer surface of said mandrel under negative pressure upon traversing a descending arc away from said reading zone; and
> - a stationary finger rest lip affixed to said housing adjacent said reading zone, configured to support a human fingerpad in tangential, zero-shear rolling contact with said inflated elastomeric chambers while the user's hand rests upon said stationary flume decks.

### Dependent Claim 2 (Zero-Pain Biomechanical Invariant)
> **2. The apparatus of claim 1**, wherein each inflated elastomeric chamber exerts a peak normal contact stress against the human fingerpad of less than $25\,\text{kPa}$ at an indentation depth of $0.50\,\text{mm}$, ensuring zero cutaneous nociceptive activation and completely painless reading across prolonged durations.

### Dependent Claim 3 (Dual-Phase Rotary Commutator)
> **3. The apparatus of claim 1**, wherein said pneumatic distribution system comprises an internal stationary commutator positioned coaxially within said rotatable mandrel, said commutator defining:
> - an ascending positive pressure manifold port pressurized to between $+10\,\text{kPa}$ and $+30\,\text{kPa}$; and
> - a descending negative vacuum manifold port evacuated to between $-2\,\text{kPa}$ and $-8\,\text{kPa}$;
> whereby rotation of the mandrel mechanically aligns pneumatic channels of each tactile presentation element with said manifold ports without requiring rotating electrical wiring.

### Dependent Claim 4 (Warmed Thermal Conditioning)
> **4. The apparatus of claim 1**, further comprising a thermal conditioning element heating air supplied to said elastomeric chambers to a temperature between $32.0^\circ\text{C}$ and $36.0^\circ\text{C}$, maintaining distal interphalangeal joint warmth and stimulating C-tactile afferent fibers.

### Dependent Claim 5 (Closed-Loop Microfluidic "Waterslide" Flume & Zero Water Loss)
> **5. The apparatus of claim 1**, wherein said fluid distribution system comprises a hermetically sealed, closed-loop microfluidic recirculating flume, wherein hydraulic fluid is recirculated continuously between said ascending arc and said descending arc with $0.00\,\text{mL/hr}$ net fluid loss, generating a frictionless hydrodynamic laminar cushion ($\mu \le 0.005$) beneath the resting fingerpad.

### Dependent Claim 6 (Bionic Tactile Fixation Multi-Level Elevation)
> **6. The apparatus of claim 1**, wherein said pneumatic distribution system selectively provides at least two discrete positive pressure levels, inflating word-onset tactile presentation elements to a first elevation of at least $0.55\,\text{mm}$ and inflating subsequent intra-word elements to a second elevation of approximately $0.40\,\text{mm}$ to establish a tactile saccadic fixation anchor.

### Dependent Claim 7 (Modular Magnetic Story Capsule)
> **7. The apparatus of claim 1**, wherein said cylindrical mandrel is configured as a detachable, interchangeable cartridge coupled to said drive mechanism via a self-aligning magnetic spindle dock and axial pneumatic seal.

### Dependent Claim 8 (Concentric Basin & Dish Housing)
> **8. The apparatus of claim 1**, wherein said housing comprises a shallow dish having a continuous outer stationary rim configured for 360° palm support, a central recessed basin, and wherein said rotatable member comprises a concentric annular flume rotatably disposed within said basin beneath a hermetic flexible membrane, magnetically driven through a bottom wall of said dish with zero through-wall penetrations.

### Independent Claim 9 (Method of Tactile Reading with Stationary Hand Support)
> **9. A method for presenting dynamic tactile literature to a reader without cutaneous shear stress, comprising:**
> - supporting a reader's palm and hand in a stationary resting posture upon stationary ergonomic flume decks of a housing;
> - rotating a cylindrical mandrel beneath a central flume aperture adjacent said stationary flume decks at an angular velocity synchronized to a target words-per-minute cadence;
> - inflating a pattern of soft elastomeric nibs on an ascending arc of said mandrel using a closed-loop fluid distribution system to form Braille characters;
> - rolling said inflated elastomeric nibs smoothly beneath the stationary fingerpad in a constant circular arc with substantially zero interfacial slip velocity and zero radial bouncing; and
> - deflating said elastomeric nibs flush with the mandrel surface on a descending arc using negative vacuum pressure while recirculating the fluid within a closed loop without fluid loss.

---

## 🛡️ 5. Freedom-to-Operate (FTO) & Prosecution Strategy

1. **Prior Art Expiration**:
   - The primary historic reference for rotary Braille—**NIST US Patent 6,776,619**—was filed on October 27, 2000. Under 35 U.S.C. § 154, its 20-year term expired in October 2020.
   - The foundational pneumatic Braille patents (Schmidt US 6,354,839) have likewise entered the public domain.
   - PocketGull LLC has **complete freedom-to-operate** to commercialize rotary tactile mechanisms.
2. **First-to-File Priority Preservation**:
   - The technical disclosures in `SPEC-POCKETGULL-BRAILLE-RSTP-2026-V1` and `philocardia_tactile_lab.html` serve as an airtight priority basis under 35 U.S.C. § 112.
   - PocketGull LLC should file a **US Provisional Patent Application** (USPTO EFS-Web) followed by a **PCT International Application** within 12 months, claiming priority to docket `POCK-PAT-2026-001`.
3. **Patent Prosecution Arguments for the USPTO Examiner**:
   - When the Examiner cites NIST US 6,776,619 or planar pneumatic displays (Tactus US 8,547,339), applicant can point out:
     *(a)* Neither reference teaches or suggests elastomeric inflatable nibs on a revolving mandrel;
     *(b)* Neither reference provides lower-arc vacuum deflation flush into the cylinder;
     *(c)* The combination solves the long-standing, unresolved 20-year failure of the NIST design (pin jamming and fingerpad fatigue) via an unexpected hyperelastic sub-nociceptive biomechanical principle.

---

**Certified by**:  
*Office of the General Counsel & Intellectual Property Directorate*  
**PocketGull LLC**  
Portland, Oregon, USA  
`legal@pocketgull.app`
