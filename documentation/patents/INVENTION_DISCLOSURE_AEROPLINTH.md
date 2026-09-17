# PATENT INVENTION DISCLOSURE DOCUMENT (IDD)
**CONFIDENTIAL & PROPRIETARY — PREPARED FOR PROVISIONAL PATENT APPLICATION (USPTO / PCT)**

---

## 1. TITLE OF THE INVENTION
**DIRECTIONAL PHOSPHORESCENT OPTICAL INTERACTION PLINTH AND VELOCITY-MODULATED VECTOR PROJECTION SYSTEM FOR CONFINED PASSENGER CABINS**

*Short Commercial Reference*: **AeroPlinth™ / SanctuaryPlinth™ / ChronoGlow™**

---

## 2. INVENTOR(S) & ASSIGNEE
* **Lead Inventor**: Phil Gear (Chief Foundry Engineer & Digital Typographer)
* **Assignee / Entity**: The PocketGull Project / GearArts
* **Filing Target**: United States Patent and Trademark Office (USPTO) Provisional Patent Application (35 U.S.C. § 111(b)), with subsequent Patent Cooperation Treaty (PCT) International Application.
* **Date of Conception**: September 4, 2026
* **Governing Ethics**: Tripartite Governance Standard (Pillar VII); all Indigenous Traditional Ecological Knowledge (TEK) and linguistic motifs are explicitly disclaimed from private ownership and reserved under sovereign biocultural stewardship.

---

## 3. TECHNICAL FIELD OF THE INVENTION
The present invention relates generally to commercial aircraft passenger service equipment, human-machine interfaces (HMI), solid-state laser projection, and in-flight wellness systems. More specifically, the invention relates to a low-power, localized, eye-safe optical projection and persistent phosphorescent afterglow system integrated into an aircraft tray table and overhead reading unit to provide tactile vector drawing, calligraphic variable-stroke rendering, circadian photobiomodulation (PBM), and acoustic-optical biofeedback within a strictly confined personal passenger envelope.

---

## 4. BACKGROUND & DEFICIENCIES OF THE PRIOR ART

### 4.1 Passenger Strains in Commercial Aviation
Long-duration passenger transit (commercial aviation flights ranging from 3 to 16 hours) subjects passengers to severe sensory, physiological, and psychological stressors:
1. **Sensory Entrapment & Boredom**: Passengers are confined to a static seated posture for extended durations with monotonous acoustic stimulation (continuous $\sim 80\text{ dB}$ cabin turbofan engine rumble).
2. **Circadian Desynchrony & Jet Lag**: Conventional seatback in-flight entertainment (IFE) screens emit high concentrations of short-wavelength blue light ($\sim 450\text{ nm}$), which aggressively suppresses pineal melatonin secretion, disrupting circadian rhythm and exacerbating post-flight fatigue.
3. **Visual Fatigue & Retinal Hypoxia**: Airplane cabins are typically pressurized to an equivalent altitude of $6{,}000\text{ to }8{,}000\text{ feet}$ above sea level, reducing arterial oxygen saturation ($\text{SpO}_2$) to $90\%\text{--}93\%$. This hypobaric hypoxia impairs retinal mitochondrial respiration, causing ocular fatigue, dry eyes, and headaches.
4. **Lack of Tactile Agency**: Existing IFE systems are overwhelmingly passive (passengers passively watch pre-recorded movies or play clunky touchscreen games). There is no outlet for tactile creative expression, manual mindfulness, or somatic grounding.

### 4.2 Inherent Failures of Existing Solutions
* **Seatback Video Displays (LCD/OLED IFE)**:
  - Add enormous weight ($\sim 4.5\text{ kg}$ per seat including display, structural reinforcement, seat electronics box, and copper wiring harnesses).
  - High capital expenditure ($\$2{,}500\text{ to }\$5{,}000$ per seat).
  - Continuous electrical draw ($15\text{--}30\text{ W}$ per seat), generating parasitic heat that burdens cabin environmental control systems.
* **Physical Print Media (e.g., SkyMall, In-Flight Magazines)**:
  - Static, passive, non-interactive, and generates substantial physical waste and logistic weight penalties.
* **Conventional Laser & Projection Systems**:
  - Unsuited for aircraft cabins due to beam spill light disturbing neighboring sleeping passengers.
  - Risk of ocular hazard if beams stray into passenger eyes.
  - Suffer from severe keystone distortion and focal blur when projected from oblique overhead angles.
  - Suffer from mirror inertia ringing, corner rounding, and speckle noise.

There is an acute unmet need for an ultra-lightweight ($<0.2\text{ kg}$ per seat), hyper-cost-efficient ($<\$30$ BOM), eye-safe, zero-spill optical interaction system that transforms dormant flight boredom into active tactile creation, restores circadian biological vitality, and operates silently without disturbing adjacent passengers.

---

## 5. SUMMARY OF THE INVENTION

The present invention solves the aforementioned deficiencies by introducing an integrated optoelectronic ecosystem comprising:
1. **An Overhead Beam-Steering Engine (PSU Module)**: A miniaturized, solid-state laser module retrofitted into an existing aircraft Passenger Service Unit (PSU) reading light aperture. The module incorporates a dual-wavelength solid-state laser diode source ($405\text{ nm}$ persistent phosphor charging + $670\text{ nm}$ photobiomodulation), a 2-axis micro-electro-mechanical system (MEMS) resonant/quasi-static scanning mirror, a custom doublet aspheric collimator, and an internal knife-edge optical aperture mask that geometrically confines all projected photons strictly to the rectangular boundary of the passenger's personal tray table.
2. **A Photoluminescent Interactive Plinth (Tray Table Surface)**: A multi-layer composite plinth permanently or removably laminated to the upper surface of a passenger tray table. The plinth comprises a sintered alkaline earth aluminate phosphor layer ($\text{SrAl}_2\text{O}_4:\text{Eu}^{2+},\text{Dy}^{3+}$) encapsulated beneath a micro-etched, oleophobic matte polycarbonate hardcoat conforming to FAA FAR 25.853 flammability standards. When excited by the $405\text{ nm}$ beam, the surface emits an intense, soothing aquamarine afterglow ($490\text{ nm}$) that persists for $45\text{--}90\text{ seconds}$, enabling real-time optical calligraphy and vector drawing without requiring continuous photon emission.
3. **An Embedded Real-Time Kinematic Trajectory Processor**:
   - Executes a factory-calibrated $3 \times 3$ affine projective homography matrix in hardware fixed-point arithmetic, perfectly rectifying oblique keystone distortion ($20^\circ\text{--}35^\circ$ projection angle) across the entire tray plinth.
   - Executes a 3rd-order jerk-limited S-curve look-ahead algorithm that injects microsecond laser blanking and dwell times at geometric vertices, preserving razor-sharp corners on serif typography, syllabics, and line graphics without mirror ringing.
   - Modulates laser traverse velocity inversely to stroke width ($v \propto 1/\text{energy density}$), allowing the system to render variable-weight humanist calligraphic strokes (thick downstrokes, hairline flourishes) without requiring analog laser diode power modulation.
4. **Autonomous Telemetry & Circadian Biofeedback Entrainment**:
   - Communicates with onboard flight avionics to read GPS position, solar elevation angle, and flight duration, automatically switching the optical source to pure $670\text{ nm}$ deep-red photobiomodulation (PBM) during nocturnal cruise to stimulate retinal cytochrome c oxidase and safeguard melatonin secretion.
   - Synthesizes an expanding/contracting $0.10\text{ Hz}$ Mayer-wave Lissajous laser harmonograph coupled to $432\text{ Hz}$ cabin noise-canceling audio to provide biofeedback vagal nerve stimulation and alleviate cabin claustrophobia.
5. **Multi-Tier Safety Interlock Architecture**:
   - An optical reflection sensor and inductive table-stowed switch that automatically cuts laser diode power in $<2\text{ ms}$ whenever the tray table is folded or an obstruction (e.g., passenger hand, face, or foreign object) breaches a safety boundary, guaranteeing permanent Class 1 accessible emission limits.

---

## 6. SYSTEM ARCHITECTURE & BLOCK DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AIRCRAFT PASSENGER SERVICE UNIT (PSU)                    │
│                                                                             │
│  [28V DC Aircraft Rail] ──────► [Buck Converter: 3.3V / 5V DC]              │
│                                       │                                     │
│  [Avionics Telemetry]                 ▼                                     │
│  (GPS, Alt, Solar Elev) ────► [ESP32-S3 / RP2350 Microcontroller]            │
│                                  │              │                           │
│  [Passenger BYOD Device]         │              ▼                           │
│  (BLE / In-Flight Wi-Fi) ────────┘   [Look-Ahead Jerk Filter & 3x3 Matrix]  │
│                                                 │                           │
│                                  ┌──────────────┴──────────────┐            │
│                                  ▼                             ▼            │
│                       [Laser Diode Drivers]          [MEMS 2-Axis Mirror]   │
│                       • 405nm (Phosphor Excitation)  • X-Axis Resonant      │
│                       • 670nm (PBM Circadian)        • Y-Axis Quasi-Static  │
│                                  │                             │            │
│                                  └──────────────┬──────────────┘            │
│                                                 ▼                           │
│                                      [Aspheric Doublet Lens]                │
│                                                 │                           │
│                                      [Optical Knife-Edge Mask]              │
│                                      (Zero-Spill Perimeter Cutoff)          │
└─────────────────────────────────────────────────┼───────────────────────────┘
                                                  │ Focused Beam Cone
                                                  │ (Class 1 Eye-Safe)
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PASSENGER SEAT / FLIP-DOWN TRAY TABLE                     │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │ [Top Layer]: Micro-Etched Oleophobic Matte Polycarbonate Hardcoat    │   │
│   │              (Tactile drag coefficient: 0.35, Wacom paper feel)     │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │ [Phosphor Layer]: Sintered SrAl2O4:Eu2+,Dy3+ Matrix (150µm)         │   │
│   │                   (Aquamarine 490nm emission, 60s persistent decay) │   │
│   ├─────────────────────────────────────────────────────────────────────┤   │
│   │ [Structural Base]: Flame-Retardant Aviation Alloy (FAR 25.853)      │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   [Inductive Stowed Sensor] ───► Interlock Loop (Cuts Power if Stowed)      │
│   [TOF Proximity Sensor]    ───► Interlock Loop (Cuts Power if Obstructed)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. DETAILED DESCRIPTION OF PREFERRED EMBODIMENTS

### 7.1 Overhead Beam-Steering Engine (PSU Retrofit Module)
The overhead projection module is dimensioned to fit within the standard circular or rectangular aperture of an existing Boeing 737/777/787 or Airbus A320/A350 passenger reading light housing.
* **Laser Source**:
  - A first solid-state semiconductor laser diode emitting at a peak wavelength of $\lambda_1 = 405\text{ nm} \pm 5\text{ nm}$ (near-ultraviolet / violet), configured for resonant excitation of strontium aluminate.
  - A second solid-state semiconductor laser diode emitting at a peak wavelength of $\lambda_2 = 670\text{ nm} \pm 5\text{ nm}$ (deep red), configured for photobiomodulation of mammalian retinal cells.
  - Both diodes are combined along a single optical path using a dichroic beam combiner cube ($450\text{ nm}$ long-pass filter).
* **Collimation Optics**:
  - An anti-reflective coated optical glass doublet lens with a numerical aperture of $0.25$, configured to focus the combined beam to a waist diameter of $w_0 \le 0.28\text{ mm}$ at a working distance of $D = 650\text{ mm} \pm 75\text{ mm}$ (the nominal distance from the overhead reading unit to the deployed tray table).
* **Scanning Mechanism**:
  - A single two-axis MEMS mirror fabricated from single-crystal silicon, featuring electrostatic or piezoelectric actuation. The fast axis ($X$) operates in resonant oscillation at $18\text{--}24\text{ kHz}$, while the slow axis ($Y$) operates in quasi-static linear deflection from $0\text{ to }60\text{ Hz}$.
* **Zero-Spill Knife-Edge Mask**:
  - Located at the exit pupil of the module is an anodized aluminum optical field stop mask. The aperture geometry is laser-cut to match the exact angular subtense of the deployed tray table ($380\text{ mm} \times 250\text{ mm}$ at $D = 650\text{ mm}$). Any light ray exceeding the tray perimeter is physically intercepted and absorbed by the mask, preventing illumination of adjacent seat occupants.

### 7.2 The Photoluminescent Plinth (Tray Table Material Stack)
The tray table plinth comprises a three-layer co-extruded or laminated composite:
1. **Layer 1 (Exposed Surface)**: A $50\,\mu\text{m}$ thick fluoropolymer or polycarbonate protective top film subjected to chemical micro-etching to impart a surface roughness ($R_a$) of $0.8\text{ to }1.2\,\mu\text{m}$. This texture provides:
   - High tactile friction resembling fine archival drawing paper.
   - Complete suppression of specular reflections from overhead cabin lights.
   - Oleophobic resistance against human skin oils and food grease.
   - High chemical resistance against airline sanitization solvents (including $70\%$ isopropanol, quaternary ammonium, and bleach).
2. **Layer 2 (Phosphorescent Core)**: A $120\text{--}180\,\mu\text{m}$ thick elastomeric layer containing microscopic crystals of strontium aluminate co-doped with europium and dysprosium ($\text{SrAl}_2\text{O}_4:\text{Eu}^{2+},\text{Dy}^{3+}$). The particle size distribution is tightly controlled between $15\,\mu\text{m}$ and $35\,\mu\text{m}$ to maximize packing density ($>65\%$ by weight) while preventing optical scatter. Upon exposure to $405\text{ nm}$ photons, the crystals trap energy within long-lived metastable states and release photons through quantum luminescence with a principal peak at $490\text{ nm}$ (aquamarine) and a persistent half-life of $52\text{ seconds}$.
3. **Layer 3 (Aviation Substrate)**: A $1.5\text{ mm}$ structural backing sheet of thermoplastic sheet (Sekisui Kydex 6565 or Boltaron 4335) formulated to satisfy FAA FAR 25.853 Appendix F Part I (vertical 12-second flammability test) and OSU heat release rate standards.

### 7.3 Velocity-Modulated Calligraphy Algorithm
Conventional vector laser displays vary line brightness by modulating the analog drive current to the laser diode. However, at low current thresholds near the diode lasing transition ($I_{\text{th}}$), color shift, mode hopping, and beam divergence degrade image quality.

The present invention solves this by maintaining the laser diode at a constant, optimal operating current and modulating the **apparent line weight via traverse velocity control**.
* The optical fluence $F$ delivered to the phosphorescent surface per unit length is defined by:
  $$F = \frac{P_{\text{opt}}}{v(t) \cdot w_0}$$
  where $P_{\text{opt}}$ is the constant optical power of the laser beam, $w_0$ is the beam waist diameter, and $v(t)$ is the instantaneous linear scanning velocity of the beam across the plinth.
* Because the phosphorescent crystal saturation curve follows an exponential saturation model:
  $$L(t) = L_{\max} \left(1 - e^{-k \cdot F}\right)$$
  the initial afterglow luminance $L(t)$ is directly controlled by modulating $v(t)$.
* When rendering a calligraphic vector stroke (such as an expanding stroke of a font glyph or drawing path):
  - For broad, heavy strokes (downstrokes), the microcontroller decelerates the MEMS mirrors to a lower velocity $v_{\text{low}}$ ($50\text{--}150\text{ mm/s}$), depositing high energy density ($F \ge 0.15\text{ J/cm}^2$) and inducing saturated, wide-blooming phosphorescent luminescence.
  - For delicate hairline strokes (upstrokes, serifs), the microcontroller accelerates the MEMS mirrors to a higher velocity $v_{\text{high}}$ ($600\text{--}1200\text{ mm/s}$), depositing lower energy density ($F \le 0.03\text{ J/cm}^2$) and producing a razor-sharp, whisper-thin glowing line.

### 7.4 Oblique Keystone Homography Matrix Calibration
Because the overhead reading pod is mounted at an angle $\theta = 28^\circ \pm 7^\circ$ relative to the tray table normal vector, an uncorrected square would project as an elongated trapezoid.

The embedded firmware executes a real-time projective transformation:
$$\begin{bmatrix} X_{\text{MEMS}} \\ Y_{\text{MEMS}} \\ W \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & 1 \end{bmatrix} \begin{bmatrix} x_{\text{virtual}} \\ y_{\text{virtual}} \\ 1 \end{bmatrix}$$
$$x_{\text{steer}} = \frac{X_{\text{MEMS}}}{W}, \quad y_{\text{steer}} = \frac{Y_{\text{MEMS}}}{W}$$
The matrix coefficients $h_{ij}$ are determined during factory seat calibration using a 4-point optical sensor array embedded into the corners of the plinth. This ensures that:
- Orthogonal cartesian grids remain mathematically square ($\pm 0.15\text{ mm}$ error across a $350\text{ mm}$ span).
- Circular figures (such as the Zen medicine stone or singing bowl) maintain an eccentricity $e < 0.02$.

### 7.5 Circadian Photobiomodulation & Biofeedback Entrainment
The system connects to the aircraft’s ARINC 429 / Ethernet avionics data bus to acquire real-time flight telemetry (UTC time, latitude, longitude, solar elevation angle, and flight duration):
1. **Daytime / Awakening Phase**: The system utilizes the $405\text{ nm}$ beam to provide high-contrast interactive drawing, navigational terrain radar, and cultural storytelling.
2. **Night Flight / Melatonin Protection Phase**: When cabin lights are dimmed for sleep and solar elevation drops below $-6^\circ$, the controller locks out the $405\text{ nm}$ diode and activates only the $670\text{ nm}$ deep-red laser.
   - Projects non-disruptive, soothing nocturnal constellations, contour maps, or breathing circles.
   - Photons at $670\text{ nm}$ do not stimulate melanopsin-expressing intrinsically photosensitive retinal ganglion cells (ipRGCs), allowing natural endogenous melatonin synthesis.
   - Concurrently delivers a low-level therapeutic photon flux ($4\text{ to }8\text{ mW/cm}^2$) to the passenger’s visual field, stimulating cytochrome c oxidase in ocular mitochondria to reverse altitude hypoxia.
3. **$0.10\text{ Hz}$ Mayer-Wave Vagal Entrainment**:
   - The laser projects an organically expanding and contracting concentric mandala at a fundamental frequency of $f = 0.10\text{ Hz}$ ($10\text{ second}$ cycle: $4\text{s}$ expansion $\to 2\text{s}$ pause $\to 4\text{s}$ contraction).
   - This frequency matches the intrinsic sympathetic/parasympathetic baroreflex Mayer wave in human arterial circulation. Seated passengers aligning their breathing with the visual rhythm experience clinical reduction in heart rate, stabilization of heart rate variability (HRV), and alleviation of flight confinement anxiety.

---

## 8. PRELIMINARY PATENT CLAIMS

### What Is Claimed Is:

**1. A localized optical interaction system for a passenger vehicle cabin, comprising:**
- an overhead projection housing mounted in a passenger service unit above a passenger seating position;
- a solid-state laser source disposed within said housing, comprising at least one semiconductor laser diode configured to emit an optical beam;
- a two-axis micro-electro-mechanical system (MEMS) scanning mirror positioned along an optical axis of said optical beam to steer the beam in two dimensions;
- an optical field stop mask positioned at an exit pupil of said housing, wherein said field stop mask mechanically constrains said optical beam within a defined personal angular envelope;
- a deployable tray table plinth positioned below said passenger service unit within said personal angular envelope, said plinth comprising an upper photoluminescent layer exhibiting persistent optical luminescence; and
- a controller operatively coupled to said laser source and said MEMS scanning mirror, wherein said controller directs said optical beam across said photoluminescent layer to generate persistent glowing vector graphics on said plinth without exceeding the boundary of said plinth.

**2. The system of claim 1, wherein:**
- said solid-state laser source comprises a first laser diode emitting at a peak wavelength between $400\text{ nm}$ and $415\text{ nm}$, and a second laser diode emitting at a peak wavelength between $660\text{ nm}$ and $680\text{ nm}$.

**3. The system of claim 2, wherein:**
- said photoluminescent layer comprises sintered crystals of alkaline earth aluminate doped with europium and dysprosium ($\text{SrAl}_2\text{O}_4:\text{Eu}^{2+},\text{Dy}^{3+}$) exhibiting an emission peak between $485\text{ nm}$ and $495\text{ nm}$ and a luminous afterglow persistence exceeding $45\text{ seconds}$ following excitation by said first laser diode.

**4. The system of claim 1, wherein:**
- said plinth further comprises a micro-etched, oleophobic polymer protective surface layer disposed above said photoluminescent layer, wherein said surface layer satisfies FAA FAR 25.853 flammability requirements and exhibits a surface roughness ($R_a$) between $0.8\,\mu\text{m}$ and $1.2\,\mu\text{m}$.

**5. The system of claim 1, wherein:**
- said controller modulates the apparent stroke weight of graphics drawn upon said photoluminescent layer by varying the scanning velocity of said MEMS mirror inversely to intended line width while maintaining optical power of said laser diode at a substantially constant level.

**6. The system of claim 1, wherein:**
- said controller executes a projective homography transformation matrix in real time to correct keystone distortion resulting from an oblique angle of projection between said overhead housing and said deployable tray table plinth.

**7. The system of claim 1, wherein:**
- said controller implements a look-ahead kinematic trajectory algorithm that introduces laser blanking and mirror dwell times at vertices of vector paths to maintain geometric corner sharpness without ringing.

**8. The system of claim 1, further comprising:**
- a safety interlock subsystem comprising an obstruction sensor, wherein said interlock subsystem automatically interrupts power to said laser source within $2\text{ milliseconds}$ upon detecting an object within a predetermined safety distance of said housing or upon detecting stowing of said tray table plinth.

**9. The system of claim 2, wherein:**
- said controller is configured to receive aircraft flight telemetry comprising altitude and solar elevation data, and wherein said controller automatically disables said first laser diode and activates said second laser diode ($660\text{--}680\text{ nm}$) during nocturnal flight conditions to provide circadian photobiomodulation without melatonin suppression.

**10. A method for providing localized interactive vector graphics and biofeedback in a passenger cabin, comprising:**
- projecting a steerable laser beam from an overhead passenger service unit toward a deployable tray table plinth comprising a persistent photoluminescent substrate;
- constraining said laser beam strictly to the surface of said tray table plinth via an optical field stop mask;
- steering said laser beam across said substrate in accordance with vector coordinates using a two-axis MEMS mirror;
- modulating the linear scanning velocity of said laser beam inversely to intended line weight to generate variable-width calligraphic strokes on said photoluminescent substrate; and
- periodically projecting an oscillatory breathing pacer pattern at a fundamental frequency of approximately $0.10\text{ Hz}$ to facilitate passenger heart rate variability entrainment.

---

## 9. COMMERCIAL APPLICATIONS & REVENUE VECTORS
1. **Commercial Aviation Retrofit**: Low-cost drop-in replacement for reading light fixtures on Boeing (737/777/787) and Airbus (A320/A350) aircraft.
2. **First / Business Class Suites**: Bespoke luxury plinths with custom executive calligraphy and circadian wellness programs.
3. **High-Speed Passenger Rail**: Long-haul sleeper trains (Amtrak, Shinkansen, SNCF, Eurostar).
4. **Autonomous EV Interiors**: Interactive in-cabin entertainment for autonomous passenger vehicles.
5. **Healthcare / Clinical Inpatient Beds**: Bedside table interactive art and photobiomodulation for long-term hospital patients.

---

*Document prepared by The PocketGull Project & GearArts — September 2026*  
*Status: Ready for USPTO Provisional Patent Application Drafting*
