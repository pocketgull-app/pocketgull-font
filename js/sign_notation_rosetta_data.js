/**
 * PocketGull Sign Notation Rosetta Dataset
 * ========================================
 * Synthesizes the morphological bridge between Elsie Lincoln Benedict's 1921
 * Five Hand Types and the world's 6 major sign language notation systems:
 *
 * 1. Sutton SignWriting (U+1D800–U+1DAAF, ISO/Unicode)
 * 2. Stokoe Notation (William C. Stokoe 1960: Tab / Dez / Sig)
 * 3. Hamburg Notation System (HamNoSys v4.0: Avatar Kinematics)
 * 4. International Movement Writing Alphabet (IMWA: >27,000 movement symbols)
 * 5. ASL-phabet (Dr. Sam Supalla: Pediatric Deaf Literacy)
 * 6. Si5s / ASLwrite (Robert Arnold 2003 & Adrean Clark 2011: Cursive Orthography)
 */

window.SIGN_NOTATION_SYSTEMS = {
  "sutton": {
    "name": "Sutton SignWriting",
    "developer": "Valerie Sutton (1974)",
    "unicode": "U+1D800–U+1DAAF",
    "standard": "ISO / Unicode 8.0+",
    "expertTag": "Expert R (SIGN)",
    "paradigm": "2D Visual-Spatial Orthography",
    "description": "Full written orthography arranging iconic hand, movement, contact, and facial glyphs in vertical 2D spatial clusters representing signs from the receptive signer's view."
  },
  "stokoe": {
    "name": "Stokoe Notation",
    "developer": "William C. Stokoe (1960)",
    "unicode": "Latin / Custom Font",
    "standard": "Phonemic Cherology",
    "expertTag": "PocketGull-ASL",
    "paradigm": "Tab (Location) + Dez (Handshape) + Sig (Movement)",
    "description": "The foundational linguistic transcription breaking ASL signs into 3 cheremic parameters: Tab (where), Dez (what shape, 19 manual archetypes), and Sig (how it moves)."
  },
  "hamnosys": {
    "name": "Hamburg Notation System (HamNoSys)",
    "developer": "University of Hamburg (1984/1989)",
    "unicode": "Private Use Area / HamNoSys Font",
    "standard": "Phonetic Joint Telemetry",
    "expertTag": "Kinematic Synthesis",
    "paradigm": "Linear Morpho-Syntactic Operators",
    "description": "Rigorous phonetic notation designed for computational linguistics, computer vision, and avatar animation, parameterizing exact DIP, PIP, and MCP joint flexion angles."
  },
  "imwa": {
    "name": "International Movement Writing Alphabet (IMWA)",
    "developer": "Valerie Sutton (1974–2008)",
    "unicode": "IMWA Catalog Numbers",
    "standard": "Universal Human Kinesiology",
    "expertTag": "Multi-Plane Kinematics",
    "paradigm": "Somatic Coordinate Taxonomy (>27,000 symbols)",
    "description": "Universal kinesiological taxonomy encoding total body posture, dance, facial expression, and manual sign kinematics across transverse, frontal, and sagittal planes."
  },
  "aslphabet": {
    "name": "ASL-phabet",
    "developer": "Dr. Sam Supalla (Univ. of Arizona)",
    "unicode": "Educational Phonemic Glyphs",
    "standard": "Pediatric Deaf Literacy",
    "expertTag": "Early Literacy Invariant",
    "paradigm": "Handshape (22) + Location (5) + Movement (5)",
    "description": "Minimalist phonemic script designed to empower young deaf children with intuitive sign-reading and dictionary lookup without borrowing English phonetic structures."
  },
  "si5s": {
    "name": "Si5s / ASLwrite",
    "developer": "Robert Arnold (2003) & Adrean Clark (2011)",
    "unicode": "OpenType Ductus Ligatures",
    "standard": "Cursive Handwritten Orthography",
    "expertTag": "Felt-Marker Ductus",
    "paradigm": "Digits + Locatives + Movement Marks",
    "description": "Organic, cursive script designed for rapid handwriting on paper. Features single-stroke fluid ligatures and pen pressure modulation matching natural signer kinetics."
  }
};

window.SIGN_NOTATION_ROSETTA = [
  {
    "id": "A",
    "name": "Compact Fist (A)",
    "stokoeChereme": "A",
    "stokoeDez": "Compact fist, thumb upright against radial margin of index MCP",
    "sutton": {
      "hex": "U+1D800",
      "char": "𝠀",
      "name": "SIGNWRITING HAND-FIST",
      "primitive": "Solid Square Base (◻)",
      "orientation": "Palm facing receiver, thumb extended radially upward",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"12\" y=\"14\" width=\"22\" height=\"24\" rx=\"2\"/><path d=\"M34 26 L39 26 L39 12 L34 12 Z\" fill=\"currentColor\"/></svg>"
    },
    "hamnosys": {
      "code": "HamFistThumbSide",
      "label": "[FIST] + [THUMB-SIDE]",
      "transcription": "",
      "flexion": "MCP 90°, PIP 90°, DIP 90° (all 4 digits); thumb adducted firmly against index phalanx I",
      "kinematicState": "Zero aperture fist, maximum flexor digitorum profundus tension"
    },
    "imwa": {
      "id": "01-01-001-01-01-01",
      "group": "Hand / Fist",
      "plane": "Frontal plane resting on neutral torso box"
    },
    "aslphabet": {
      "graphemeId": "HS-01",
      "glyphDesc": "Block fist with upward thumb wing",
      "pediatricNote": "Primary consonant anchor; taught first in elementary deaf vocabulary"
    },
    "si5s": {
      "mark": "Digit 1 (Thumb-Rest)",
      "ductus": "Clockwise loop terminating in sharp vertical ascender stroke"
    },
    "morphology": {
      "alimentive": "Dimpled knuckle pads conceal the bone line; thumb sinks into fleshy thenar mound. Optical sensors risk classifying this as 'O' or 'E'. Remedy: Enforce radial boundary expansion (+12% thumb offset).",
      "thoracic": "Conical index MCP creates an elevated thumb perch. Fist appears elongated along the vertical axis. Remedy: Normalize vertical bounding box to standard Sloan 5:1 1000 UPM em-square.",
      "muscular": "Ideal planar square; 1:1 palm ratio gives maximum optical contrast. Knuckles align in a crisp horizontal bar matching Louise Sloan 5:1 grid lines exactly.",
      "osseous": "Knotted articular nodes protrude sharply, creating prominent dorsal ridges. Optical edge detectors may trigger false joint points. Remedy: Apply morphological closing filter across MCP axis.",
      "cerebral": "Slender, smooth digits with minimal muscular padding; thumb appears disproportionately long and delicate. Zero false edge noise."
    },
    "sloanCalibration": "Maintain exactly 1.0 stroke-width counter-space between thumb pad and index lateral wall to preserve 20/200 recognition under fatigue."
  },
  {
    "id": "B",
    "name": "Flat Hand (B)",
    "stokoeChereme": "B",
    "stokoeDez": "Flat 4-finger blade held tightly together, thumb tucked horizontally across volar palm",
    "sutton": {
      "hex": "U+1D818",
      "char": "𝠘",
      "name": "SIGNWRITING HAND-FLAT",
      "primitive": "Rectangle Blade with 4 Extension Bars",
      "orientation": "Vertical fingers pointing zenith, thumb tucked at palmar base",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"14\" y=\"24\" width=\"20\" height=\"18\" rx=\"2\"/><line x1=\"17\" y1=\"8\" x2=\"17\" y2=\"24\"/><line x1=\"22\" y1=\"6\" x2=\"22\" y2=\"24\"/><line x1=\"27\" y1=\"7\" x2=\"27\" y2=\"24\"/><line x1=\"31\" y1=\"10\" x2=\"31\" y2=\"24\"/><path d=\"M14 32 L8 32 L8 38 L14 38 Z\" fill=\"currentColor\"/></svg>"
    },
    "hamnosys": {
      "code": "HamFlatThumbAcross",
      "label": "[FLAT-4] + [THUMB-ACROSS]",
      "transcription": "",
      "flexion": "MCP 0°, PIP 0°, DIP 0° (digits II–V); thumb MCP flexed 45°, IP flexed 30° across volar face",
      "kinematicState": "Maximum extensor digitorum tension; complete planar finger adduction"
    },
    "imwa": {
      "id": "01-01-012-01-01-01",
      "group": "Hand / Flat Blade",
      "plane": "Sagittal or frontal vertical wall"
    },
    "aslphabet": {
      "graphemeId": "HS-02",
      "glyphDesc": "Vertical 4-bar comb with horizontal thumb base",
      "pediatricNote": "Foundational flat-hand grapheme for signs like DOOR, BOOK, BLUE"
    },
    "si5s": {
      "mark": "Digit 2 (Blade)",
      "ductus": "Long upward vertical stroke with sharp horizontal baseline tick"
    },
    "morphology": {
      "alimentive": "Fleshy pulp cushions create tight palmar seal. Zero interdigital daylight; thumb completely buried against thenar cushion. Optotype ratio stays exceptionally clean.",
      "thoracic": "Digit III (middle finger) projects 15–20% higher than digits II and IV, producing an optical apex. Must not be confused with specialized pointed handshapes.",
      "muscular": "Uniform spatulate fingertips form a level horizontal roof. High surface area makes contact signs (e.g., AGAIN, TABLE) acoustically and visually resonant.",
      "osseous": "Knotted articular nodes prevent full side-by-side contact. Daylight shines between proximal phalanges, causing optical classifiers to falsely detect '4' or '5'. Normalizer masks inter-knuckle gaps.",
      "cerebral": "Fingers are hyper-parallel and paper-thin. Optical silhouette has high transmittance; requires stroke-width boost to satisfy Louise Sloan 5:1 20% thickness rule."
    },
    "sloanCalibration": "Stroke thickness must be locked to 200 UPM (1/5 em-square) so the 4 conjoined fingers appear as a monolithic blade at low optical resolutions."
  },
  {
    "id": "5",
    "name": "Spread Open Hand (5)",
    "stokoeChereme": "5",
    "stokoeDez": "Fully splayed open hand with all 5 digits maximally abducted",
    "sutton": {
      "hex": "U+1D82A",
      "char": "𝠪",
      "name": "SIGNWRITING HAND-SPREAD",
      "primitive": "Open Arc with 5 Splayed Rays",
      "orientation": "All digits abducted radially at ~22° intervals",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><circle cx=\"24\" cy=\"30\" r=\"10\"/><line x1=\"12\" y1=\"18\" x2=\"18\" y2=\"25\"/><line x1=\"17\" y1=\"10\" x2=\"21\" y2=\"21\"/><line x1=\"24\" y1=\"8\" x2=\"24\" y2=\"20\"/><line x1=\"31\" y1=\"10\" x2=\"27\" y2=\"21\"/><line x1=\"36\" y1=\"18\" x2=\"30\" y2=\"25\"/></svg>"
    },
    "hamnosys": {
      "code": "HamOpenSpread5",
      "label": "[SPREAD-5] + [MAX-ABDUCTION]",
      "transcription": "",
      "flexion": "MCP 0°, PIP 0°, DIP 0° (digits I–V); maximum abduction (dorsal interossei activation)",
      "kinematicState": "Maximum volumetric footprint; 180° radial perimeter sweep"
    },
    "imwa": {
      "id": "01-01-025-01-01-01",
      "group": "Hand / Five Spread",
      "plane": "Frontal plane wide display"
    },
    "aslphabet": {
      "graphemeId": "HS-05",
      "glyphDesc": "5-point star fan radiating from semi-circle palm",
      "pediatricNote": "Universal counting and color base (FINE, MOTHER, FATHER, COLOR)"
    },
    "si5s": {
      "mark": "Digit 5 (Star Fan)",
      "ductus": "Five rapid radiating radial ticks fanning from left to right"
    },
    "morphology": {
      "alimentive": "Short conical digits limit total angular spread; webbing appears higher between fingers due to adipose cushions. Angular spread measures ~18° vs standard 24°.",
      "thoracic": "Extensive reach envelope. Middle finger projects prominently upward; total span can exceed 230mm, creating massive visual presence in public lecturing.",
      "muscular": "Heavy, rigid splay with thick webbing. Spatulate paddle tips create bold geometric endpoints at every vertex.",
      "osseous": "Severe angular divergence. Bony phalanges create stark negative-space wedges. Optical acuity is highest in this type due to extreme contrast.",
      "cerebral": "Graceful spider-like splay; straight phalangeal lines with zero knuckle distortion. Extremely low visual weight requires high-contrast backlighting."
    },
    "sloanCalibration": "Interdigital angular separation must be calibrated to ensure the narrowest counter-space between digits is >= 1 stroke width (200 UPM) at the base webbing."
  },
  {
    "id": "C",
    "name": "Open Arc / Cup (C)",
    "stokoeChereme": "C",
    "stokoeDez": "Curved hand forming smooth circular C-arc facing medially",
    "sutton": {
      "hex": "U+1D80C",
      "char": "𝠌",
      "name": "SIGNWRITING HAND-CUP",
      "primitive": "Open Circle Profile (○)",
      "orientation": "Digits curved in smooth semicircular arc opposed to thumb",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\"><path d=\"M34 14 C22 14 14 20 14 28 C14 36 22 42 34 42\" stroke-linecap=\"round\"/></svg>"
    },
    "hamnosys": {
      "code": "HamCupCurveC",
      "label": "[CURVE-C] + [OPPOSED-THUMB]",
      "transcription": "",
      "flexion": "MCP 35°, PIP 35°, DIP 20° across all digits; thumb CMC abducted and opposed 45°",
      "kinematicState": "Semicircular aperture enclosing cylindrical cylindrical grasping volume"
    },
    "imwa": {
      "id": "01-01-008-01-01-01",
      "group": "Hand / Curved Arc",
      "plane": "Sagittal view displaying inner circular negative space"
    },
    "aslphabet": {
      "graphemeId": "HS-03",
      "glyphDesc": "Classic open crescent C opening to right",
      "pediatricNote": "Teaches circular grasping concept (CUP, CLASS, COOKIE)"
    },
    "si5s": {
      "mark": "Digit 3 (Arc Grasp)",
      "ductus": "Smooth counter-clockwise crescent stroke with rounded terminals"
    },
    "morphology": {
      "alimentive": "Naturally embodies the Benedict Circle archetype. Finger curvature is continuous and fleshy, creating an almost complete torus. High optical legibility.",
      "thoracic": "Elongated elliptical arc rather than a true circle; middle finger apex creates an asymmetrical oval.",
      "muscular": "Robust, blocky arc; proximal joints bend in crisp angular facets rather than a continuous curve. Resembles an octagonal bracket.",
      "osseous": "Articular nodes produce prominent sharp corners along the arc perimeter; inner aperture has irregular bony contours. Normalizer applies quadratic bezier smoothing.",
      "cerebral": "Slender, whisper-thin crescent. High inner negative space aperture; zero tissue occlusion."
    },
    "sloanCalibration": "Inner counter-space diameter must equal exactly 3 stroke units (600 UPM) within the 1000 UPM em-square to ensure Louise Sloan 5:1 optometric compliance."
  },
  {
    "id": "1",
    "name": "Index Point (1 / D)",
    "stokoeChereme": "G",
    "stokoeDez": "Index finger extended vertically, remaining digits closed in fist with thumb resting on middle finger",
    "sutton": {
      "hex": "U+1D810",
      "char": "𝠐",
      "name": "SIGNWRITING HAND-INDEX",
      "primitive": "Square Fist with 1 Vertical Beam",
      "orientation": "Single vertical digit pointing zenith, solid closed fist base",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"14\" y=\"22\" width=\"20\" height=\"20\" rx=\"2\"/><line x1=\"20\" y1=\"6\" x2=\"20\" y2=\"22\" stroke-width=\"3\" stroke-linecap=\"round\"/></svg>"
    },
    "hamnosys": {
      "code": "HamIndexPointG",
      "label": "[INDEX-EXT] + [FIST-BASE]",
      "transcription": "",
      "flexion": "Digit II MCP 0°, PIP 0°, DIP 0°; digits III–V MCP 90°, PIP 90°, DIP 90°; thumb flexed across digit III",
      "kinematicState": "Unilateral extensor indicis proprius activation; maximum pointing vector"
    },
    "imwa": {
      "id": "01-01-015-01-01-01",
      "group": "Hand / Index Pointer",
      "plane": "Directional vector arrow path"
    },
    "aslphabet": {
      "graphemeId": "HS-04",
      "glyphDesc": "Vertical stem rooted in closed fist box",
      "pediatricNote": "Most frequent deixis pointer in ASL (ME, YOU, WHO, WHERE)"
    },
    "si5s": {
      "mark": "Digit 4 (Pointer)",
      "ductus": "Sharp vertical stroke originating from tight basal loop"
    },
    "morphology": {
      "alimentive": "Index finger is short and chubby; knuckle dimple at index MCP. The closed fist base is rounded. Normalizer sharpens vertical stem ratio to prevent confusing with 'X' (bent index).",
      "thoracic": "Exceptionally long index finger with sharp conical taper. Pointing vector is hyper-pronounced.",
      "muscular": "Square spatulate tip creates a broad chisel-like pointer terminal, ideal for high-contrast optical edge tracking.",
      "osseous": "Knotted interphalangeal nodes give the extended index finger an undulating, segmented silhouette. Calibrator straightens ray vector.",
      "cerebral": "Needle-thin straight pointer; smooth continuous edges with zero lateral deviation."
    },
    "sloanCalibration": "Vertical index stem width must be locked to 200 UPM with 25 UPM corner fillets on the terminal tip to prevent stroke erosion at low display PPI."
  },
  {
    "id": "V",
    "name": "V-Wedge / Two Digits (V)",
    "stokoeChereme": "V",
    "stokoeDez": "Index and middle fingers extended in spread V-shape, remaining digits closed in fist",
    "sutton": {
      "hex": "U+1D814",
      "char": "𝠔",
      "name": "SIGNWRITING HAND-V",
      "primitive": "Square Fist with 2 Splayed Beams",
      "orientation": "Digits II and III abducted at ~24° wedge angle",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"14\" y=\"24\" width=\"20\" height=\"18\" rx=\"2\"/><line x1=\"18\" y1=\"8\" x2=\"22\" y2=\"24\" stroke-width=\"3\" stroke-linecap=\"round\"/><line x1=\"30\" y1=\"8\" x2=\"26\" y2=\"24\" stroke-width=\"3\" stroke-linecap=\"round\"/></svg>"
    },
    "hamnosys": {
      "code": "HamTwoSpreadV",
      "label": "[TWO-V] + [SPLAY-WEDGE]",
      "transcription": "",
      "flexion": "Digits II & III extended 0°, abducted 25°; digits IV & V fully flexed; thumb over ring finger",
      "kinematicState": "Bilateral extension with active first dorsal interosseous abduction"
    },
    "imwa": {
      "id": "01-01-018-01-01-01",
      "group": "Hand / Two Spread",
      "plane": "Frontal plane wedge angle"
    },
    "aslphabet": {
      "graphemeId": "HS-06",
      "glyphDesc": "Classic V-wedge fork",
      "pediatricNote": "Essential for SEE, LOOK, TWO, SCISSORS"
    },
    "si5s": {
      "mark": "Digit 6 (Fork)",
      "ductus": "Single continuous down-up stroke forming a sharp acute notch"
    },
    "morphology": {
      "alimentive": "Thick fleshy interdigital webbing narrows the apparent V-angle from 24° down to 16°, risking collision with 'U' (closed two-finger blade). Normalizer applies +8° Sloan wedge spread.",
      "thoracic": "Middle finger extends significantly higher than index, creating an asymmetrical V-top. Aesthetic normalizer balances optical height.",
      "muscular": "Parallel paddle shafts with a crisp triangular crotch. High contrast and clean geometric vertices.",
      "osseous": "Articular nodes at PIP joints rub together if fingers are slightly brought in; when splayed, the crotch is deeply sunken and bony.",
      "cerebral": "Razor-sharp, clean wedge with wide counter-space opening all the way down to the MCP baseline."
    },
    "sloanCalibration": "Acute angle must never pinch below 1.0 stroke width (200 UPM) at the base crotch, guaranteeing disambiguation between ASL 'U' (adducted) and 'V' (abducted)."
  },
  {
    "id": "O",
    "name": "Closed O-Ring (O)",
    "stokoeChereme": "O",
    "stokoeDez": "All four fingertips curved and touching the distal pad of thumb, forming a closed optical circle",
    "sutton": {
      "hex": "U+1D808",
      "char": "𝠈",
      "name": "SIGNWRITING HAND-RING",
      "primitive": "Closed Oval / Circle (⬭)",
      "orientation": "Closed ring aperture facing receiver",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"3\"><circle cx=\"24\" cy=\"24\" r=\"14\" stroke-linecap=\"round\"/></svg>"
    },
    "hamnosys": {
      "code": "HamClosedRingO",
      "label": "[RING-O] + [ZERO-APERTURE]",
      "transcription": "",
      "flexion": "Digits II–V flexed at MCP 45°, PIP 60°, DIP 40°; thumb fully opposed with pads in contact",
      "kinematicState": "Closed kinematic loop; zero aperture escape"
    },
    "imwa": {
      "id": "01-01-005-01-01-01",
      "group": "Hand / Closed Circle",
      "plane": "Enclosed volumetric ocular aperture"
    },
    "aslphabet": {
      "graphemeId": "HS-07",
      "glyphDesc": "Continuous closed ring loop",
      "pediatricNote": "Teaches complete closure (NONE, ZERO, ONCE)"
    },
    "si5s": {
      "mark": "Digit 7 (Closed Loop)",
      "ductus": "Single continuous counter-clockwise oval circle closing upon itself"
    },
    "morphology": {
      "alimentive": "Fleshy pads compress heavily upon contact, squeezing the inner circular hole down to a tiny slit. Can be misread as solid fist. Remedy: Enforce minimum 180 UPM inner diameter.",
      "thoracic": "Forms an elongated, pear-shaped or teardrop aperture due to extended middle digit.",
      "muscular": "Firm, robust oval ring with broad planar contact pad. Heavy structural boundary.",
      "osseous": "Bony fingertips touch with minimal cushion; inner aperture is large, angular, and polygonal (pentagonal loop) rather than smooth circular.",
      "cerebral": "Delicate, fine ring like a jeweler's hoop. Maximum inner aperture transparency."
    },
    "sloanCalibration": "Inner circular aperture diameter must be maintained at >= 200 UPM (1 stroke width) to prevent optical hole filling in clinical displays."
  },
  {
    "id": "F",
    "name": "Pinch Index / Three Spread (F)",
    "stokoeChereme": "F",
    "stokoeDez": "Thumb and index finger touching in circle, middle/ring/pinky extended and splayed",
    "sutton": {
      "hex": "U+1D824",
      "char": "𝠤",
      "name": "SIGNWRITING HAND-PINCH",
      "primitive": "Circle Ring with 3 Splayed Beams",
      "orientation": "Index-thumb ring at base with 3 upward radial digits",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><circle cx=\"18\" cy=\"30\" r=\"8\"/><line x1=\"28\" y1=\"8\" x2=\"24\" y2=\"24\" stroke-width=\"2.5\"/><line x1=\"34\" y1=\"10\" x2=\"27\" y2=\"25\" stroke-width=\"2.5\"/><line x1=\"39\" y1=\"15\" x2=\"30\" y2=\"28\" stroke-width=\"2.5\"/></svg>"
    },
    "hamnosys": {
      "code": "HamPinchThreeUpF",
      "label": "[PINCH-INDEX] + [SPREAD-3-UP]",
      "transcription": "",
      "flexion": "Digit II + thumb in closed pinch loop; digits III–V extended 0° and abducted",
      "kinematicState": "Simultaneous focal pinch grasping and tri-finger display splay"
    },
    "imwa": {
      "id": "01-01-022-01-01-01",
      "group": "Hand / Pinch Fan",
      "plane": "Mixed contact loop and radial fan"
    },
    "aslphabet": {
      "graphemeId": "HS-08",
      "glyphDesc": "Bottom ring with 3-feather crown",
      "pediatricNote": "Key handshape for CAT, NINE, IMPORTANT"
    },
    "si5s": {
      "mark": "Digit 8 (Crown Ring)",
      "ductus": "Lower loop that whips upward into three feather ticks"
    },
    "morphology": {
      "alimentive": "Pinch loop is thick; the 3 splayed digits have reduced clearance, appearing crowded. Normalizer expands inter-digit spacing between digits III, IV, and V.",
      "thoracic": "Middle finger extends high above the ring and little finger, giving the 3-finger fan an ascending cascade.",
      "muscular": "Clean, distinct paddle tips on the 3 splayed fingers; pinch loop forms a stable, square-shouldered base.",
      "osseous": "Knuckles on the 3 extended digits create jagged silhouette; pinch loop has visible knuckle ridges.",
      "cerebral": "Feather-light silhouette; high separation between all 3 extended digits and the pinch loop."
    },
    "sloanCalibration": "Clearance between the pinch loop and digit III must be >= 1 stroke width (200 UPM) to prevent visual bridge clotting under DirectWrite ClearType."
  },
  {
    "id": "S",
    "name": "Transverse Fist (S)",
    "stokoeChereme": "S",
    "stokoeDez": "Closed fist with thumb wrapped transversely across the front of all fingers",
    "sutton": {
      "hex": "U+1D801",
      "char": "𝠁",
      "name": "SIGNWRITING HAND-FIST-THUMB-ACROSS",
      "primitive": "Solid Square Base with Horizontal Belt Bar",
      "orientation": "Palm facing receiver, thumb crossing transversely over fingers II and III",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"14\" y=\"14\" width=\"20\" height=\"24\" rx=\"2\"/><rect x=\"12\" y=\"22\" width=\"24\" height=\"8\" rx=\"1.5\" fill=\"currentColor\"/></svg>"
    },
    "hamnosys": {
      "code": "HamFistThumbAcrossS",
      "label": "[FIST] + [THUMB-TRANSVERSE]",
      "transcription": "",
      "flexion": "Digits II–V fully flexed 90°; thumb flexed at CMC, MCP, and IP across volar phalanx II",
      "kinematicState": "Maximum structural fist lockdown; transverse clasping force"
    },
    "imwa": {
      "id": "01-01-002-01-01-01",
      "group": "Hand / Locked Fist",
      "plane": "Frontal plane locked fist"
    },
    "aslphabet": {
      "graphemeId": "HS-09",
      "glyphDesc": "Block fist with horizontal belt line",
      "pediatricNote": "Essential fist contrast against 'A' and 'T' (YES, SORRY, ICE-CREAM)"
    },
    "si5s": {
      "mark": "Digit 9 (Belt Fist)",
      "ductus": "Solid rounded block crossed with a firm horizontal bar"
    },
    "morphology": {
      "alimentive": "Fleshy fingers and plump thumb blend together into a single rounded mass. Thumb contour is difficult for cameras to detect. Calibrator adds high-contrast contour groove.",
      "thoracic": "Long thumb wraps all the way across past digit IV, reaching nearly to digit V. Gives fist an asymmetrical diagonal belt angle.",
      "muscular": "Classic boxer's fist; thumb sits exactly across fingers II and III in a level horizontal bar with 1:1 square stability.",
      "osseous": "Bony thumb knuckle nodes ride high over finger knuckles, creating high topographic relief and casting strong shadow lines.",
      "cerebral": "Fist is compact and narrow; thumb wraps lightly with minimal muscular tension."
    },
    "sloanCalibration": "Transverse thumb bar must have explicit 25 UPM chamfered relief grooves on both borders so it is instantly distinguishable from 'A' (thumb upright) and 'T' (thumb under index)."
  },
  {
    "id": "I",
    "name": "Pinky Extended (I / J)",
    "stokoeChereme": "I",
    "stokoeDez": "Little finger (digit V) extended vertically, remaining digits in fist with thumb resting over index and middle",
    "sutton": {
      "hex": "U+1D813",
      "char": "𝠓",
      "name": "SIGNWRITING HAND-PINKY",
      "primitive": "Square Fist with 1 Right-Hand Vertical Ray",
      "orientation": "Single small vertical digit on ulnar side pointing zenith",
      "svgIcon": "<svg viewBox=\"0 0 48 48\" width=\"48\" height=\"48\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\"><rect x=\"14\" y=\"22\" width=\"20\" height=\"20\" rx=\"2\"/><line x1=\"30\" y1=\"8\" x2=\"30\" y2=\"22\" stroke-width=\"3\" stroke-linecap=\"round\"/></svg>"
    },
    "hamnosys": {
      "code": "HamPinkyOnlyI",
      "label": "[PINKY-EXT] + [FIST-BASE]",
      "transcription": "",
      "flexion": "Digit V extended 0°; digits II–IV flexed 90°; thumb adducted across digits II & III",
      "kinematicState": "Isolated extensor digiti minimi activation"
    },
    "imwa": {
      "id": "01-01-017-01-01-01",
      "group": "Hand / Little Finger",
      "plane": "Ulnar margin vertical ray"
    },
    "aslphabet": {
      "graphemeId": "HS-10",
      "glyphDesc": "Fist with delicate right-hand needle stem",
      "pediatricNote": "Used in I, J, YELLOW, ART, THIN"
    },
    "si5s": {
      "mark": "Digit 10 (Ulnar Needle)",
      "ductus": "Basal loop with fine upward needle flick on the right"
    },
    "morphology": {
      "alimentive": "Pinky is short and baby-like with a conical tip and dimpled base. Can be eclipsed by the heavy palm mass. Normalizer ensures minimum 220 UPM extension height.",
      "thoracic": "Slender pinky with elegant upward curve; delicate ulnar margin.",
      "muscular": "Stout, robust pinky with a firm spatulate tip. Equal in visual weight to standard glyph stems.",
      "osseous": "Prominent PIP node on digit V creates a curved or knobby needle; easily distinguished from other digits.",
      "cerebral": "Hyper-slender, almost hairline digit V. Highly expressive in fast fingerspelling."
    },
    "sloanCalibration": "Extended pinky stem must maintain full 200 UPM stroke width matching all other digits to satisfy Louise Sloan 5:1 optotype legibility."
  }
];
