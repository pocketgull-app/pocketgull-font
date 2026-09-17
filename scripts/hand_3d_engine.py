#!/usr/bin/env python3
"""
PocketGull Typefoundry — Procedural 3D (X, Y, Z) Kinematic Hand Engine
=====================================================================
Synthesizes:
1. 21-Joint 3D Kinematic Skeletal Hand Model
2. Elsie Lincoln Benedict (1921) Biometric Archetype Deformation Tensors:
   - Alimentive (Circle / Plump, Dimpled Knuckles, S_z=1.25)
   - Thoracic   (Wedge / Conical Taper, High Apex, Narrow Wrist 0.72)
   - Muscular   (1:1 Cube / Square Palm, Spatulate Paddle Tips)
   - Osseous    (Oblong / Knotty Condyle Nodes, Hollowed Shafts)
   - Cerebral   (Needle / Frail Parallel Slender, Zero Knot Swelling)
3. 3D Euler Camera Projection (R_x(phi) * R_y(theta)):
   - Dorsal (0°, 0°)
   - Palmar (180°, 0°)
   - Lateral Profile (90°, 0°)
   - 3/4 Volumetric (45°, 15°)
4. Full Procedural Overlays Across ALL Perspectives:
   - Layer 1: Volumetric Mass Envelope (.layer-mass)
   - Layer 2: 3D Primitives Wireframe (.layer-primitives)
   - Layer 3: 3D Biometric Ratios & Calipers (.layer-ratios)
   - Layer 4: Louise Sloan 5:1 Optotype Grid (.layer-sloan)
   - Layer 5: Anatomical Contour (.layer-contour)
   - Layer 6: Anatomical Details & Nails (.layer-details)
   - Layer 7: Lateral Joint Cutaway Inset (.layer-inset)
   - Layer 8: Diagnostic Leader Callouts (.layer-callouts)
5. Kinematic ASL Pose Library for Procedural Fingerspelling (A-Z).
"""

import math
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# =============================================================================
# 1. 3D VECTOR MATH & CAMERA PROJECTION
# =============================================================================

@dataclass
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, o: 'Vec3') -> 'Vec3':
        return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)

    def __sub__(self, o: 'Vec3') -> 'Vec3':
        return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)

    def __mul__(self, s: float) -> 'Vec3':
        return Vec3(self.x * s, self.y * s, self.z * s)

    def length(self) -> float:
        return math.hypot(self.x, self.y, self.z)

    def normalized(self) -> 'Vec3':
        l = self.length()
        return Vec3(self.x / l, self.y / l, self.z / l) if l > 1e-6 else Vec3(0, 0, 0)

    def rotate_y(self, angle_deg: float) -> 'Vec3':
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vec3(self.x * cos_a + self.z * sin_a, self.y, -self.x * sin_a + self.z * cos_a)

    def rotate_x(self, angle_deg: float) -> 'Vec3':
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vec3(self.x, self.y * cos_a - self.z * sin_a, self.y * sin_a + self.z * cos_a)

    def rotate_z(self, angle_deg: float) -> 'Vec3':
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vec3(self.x * cos_a - self.y * sin_a, self.x * sin_a + self.y * cos_a, self.z)


def project_3d(v: Vec3, yaw_deg: float, pitch_deg: float,
               cx: float = 240.0, cy: float = 380.0,
               fov: float = 900.0, scale: float = 1.0) -> Tuple[float, float, float]:
    """
    Applies Euler rotation R_x(pitch) * R_y(yaw) and perspective projection.
    Returns (x_svg, y_svg, depth_z).
    Note: SVG coordinate Y increases downward, whereas 3D hand model Y increases upward.
    """
    v_rot = v.rotate_y(yaw_deg).rotate_x(pitch_deg)
    
    # Camera at (0, 0, fov) looking towards origin
    # z_depth: positive towards viewer
    z = v_rot.z
    denom = fov + z
    if denom < 50.0:
        denom = 50.0
    k = (fov / denom) * scale
    
    px = cx + v_rot.x * k
    py = cy - v_rot.y * k  # Invert Y for SVG screen coordinates
    return px, py, z


# =============================================================================
# 2. BIOMETRIC ARCHETYPE DEFINITIONS (1921 BENEDICT STANDARDS)
# =============================================================================

ARCHETYPES = {
    'alimentive': {
        'name': 'The Alimentive Hand',
        'subtitle': 'The Vital / Nutrition Type',
        'color': '#f59e0b',
        'historicalChart': 'Chart 2 (Page 40) · Alimentive Hand & Face',
        'dominantSystem': 'Digestive System (Assimilation & Vital Storage)',
        'geometricArchetype': 'The Circle / Spherical Mass',
        'bookQuote': 'Fat, chubby, short-fingered with dimpled knuckles and soft, plump cushions.',
        'hciImplication': 'Requires enlarged touch targets (minimum 48×48 dp) with high tactile visual contrast.',
        'ratios': {
            'fingerToPalm': '0.78 : 1.00 (Short Digits)',
            'wristToKnuckle': '0.88 : 1.00 (Wide, Fleshy Wrist)',
            'thicknessToWidth': '0.72 : 1.00 (Maximum Depth)'
        },
        'keyDiagnoses': [
            'Short, plump fingers with rounded, soft pulp tips',
            'Negative knuckle condyles (dimples instead of bone knots)',
            'Thick, fleshy thenar eminence with rounded base',
            'Round nail plates, broader than long, with low curvature',
            'Full palmar fat cushions dampening tactile shock'
        ],
        'scale_x': 1.15,
        'scale_y': 0.78,
        'scale_z': 1.25,
        'wrist_w': 110,
        'knuckle_w': 125,
        'condyle_bulge': -0.15,  # Dimple / inward crease at joint
        'shaft_waist': 1.06,     # Puffy inter-joint shaft
        'tip_radius': 14.0,
        'tip_shape': 'round',
        'thenar_bulk': 1.35,
        'palm_shape': 'circle',
        'callouts': {
            'dorsal': [
                (175, 160, -25, 150, "Short, Puffy Digits", "0.78:1.00 finger-to-palm ratio", "end"),
                (240, 105, -25, 80, "Knuckle Dimples", "Fat deposits conceal bony condyles", "end"),
                (378, 250, 485, 240, "Plump Thumb", "Short, rounded 30° reach", "start"),
                (280, 440, 485, 430, "Fleshy Wrist", "0.88:1.00 wrist-to-knuckle ratio", "start")
            ],
            'palmar': [
                (155, 370, -25, 360, "Hypothenar Cushion", "Full fatty shock-absorbing pad", "end"),
                (290, 365, 485, 360, "Voluminous Thenar", "Robust thumb muscle mound", "start"),
                (245, 290, 485, 280, "Soft Creases", "Deep curved palmar flexion rings", "start")
            ],
            'lateral': [
                (205, 105, -25, 95, "Plump Pulp Profile", "Cushioned palmar finger pad", "end"),
                (215, 215, -25, 210, "Dimpled Knuckle Dip", "Smooth fatty depression", "end"),
                (325, 235, 485, 230, "Thick Thumb Pad", "High dorso-palmar mass", "start")
            ],
            'threeQuarter': [
                (185, 150, -25, 140, "Volumetric Spheres", "Stacked ellipsoidal mass hierarchy", "end"),
                (445, 255, 485, 250, "Full Radial Depth", "1.25x thickness factor", "start")
            ]
        }
    },
    'thoracic': {
        'name': 'The Thoracic Hand',
        'subtitle': 'The Circulatory / Responsive Type',
        'color': '#ec4899',
        'historicalChart': 'Chart 4 (Page 88) · Thoracic Hand & Face',
        'dominantSystem': 'Respiratory & Circulatory (Rapid Energy & High Heart Acuity)',
        'geometricArchetype': 'The Conical Wedge',
        'bookQuote': 'Long, graceful, tapering fingers with narrow wrist, delicate skin, and pointed tips.',
        'hciImplication': 'Optimized for high-velocity precision gestures and agile micro-swipes.',
        'ratios': {
            'fingerToPalm': '1.18 : 1.00 (Long Digits)',
            'wristToKnuckle': '0.72 : 1.00 (Highly Tapered Wrist)',
            'thicknessToWidth': '0.50 : 1.00 (Slender Depth)'
        },
        'keyDiagnoses': [
            'Conspicuously elongated digits with high middle finger apex',
            'Sharp conical tapering from knuckle to fingertip',
            'Narrow, graceful wrist flaring outward to metacarpals',
            'Conical nail plates with pointed terminal free edges',
            'Rapid vascular reactivity with pronounced pink flush'
        ],
        'scale_x': 0.88,
        'scale_y': 1.18,
        'scale_z': 0.85,
        'wrist_w': 76,
        'knuckle_w': 106,
        'condyle_bulge': 0.05,   # Gentle smooth knuckle
        'shaft_waist': 0.88,     # Conical taper
        'tip_radius': 8.0,
        'tip_shape': 'conical',
        'thenar_bulk': 0.88,
        'palm_shape': 'wedge',
        'callouts': {
            'dorsal': [
                (170, 130, -25, 120, "Tapering Conical Digits", "Smooth continuous narrowing", "end"),
                (240, 60, -25, 50, "High Middle Apex", "1.18:1.00 finger-to-palm ratio", "end"),
                (382, 240, 485, 230, "Graceful Thumb", "Elongated 38° radial projection", "start"),
                (275, 445, 485, 435, "Tapered Wrist", "0.72:1.00 narrow wrist ratio", "start")
            ],
            'palmar': [
                (150, 365, -25, 355, "Streamlined Hypothenar", "Frail ulnar boundary", "end"),
                (285, 360, 485, 350, "Elongated Thenar", "Agile opposition architecture", "start"),
                (240, 280, 485, 270, "Fine Crease Filigree", "High neural vascular sensitivity", "start")
            ],
            'lateral': [
                (200, 75, -25, 65, "Conical Tip Wedge", "Delicate pointed free edge", "end"),
                (210, 195, -25, 190, "Smooth Joint Transition", "Zero bony joint obstruction", "end"),
                (315, 220, 485, 215, "Slender Elevation", "High agile arc", "start")
            ],
            'threeQuarter': [
                (180, 120, -25, 110, "Conical Converging Wedge", "Angular lateral taper", "end"),
                (440, 240, 485, 235, "Graceful Elevation", "Rapid flexor tracking", "start")
            ]
        }
    },
    'muscular': {
        'name': 'The Muscular Hand',
        'subtitle': 'The Locomotor / Endurance Type',
        'color': '#06b6d4',
        'historicalChart': 'Chart 6 (Page 142) · Muscular Hand & Face',
        'dominantSystem': 'Muscular & Skeletal (Sustained Mechanical Force & Power)',
        'geometricArchetype': 'The Square / 1:1 Cube',
        'bookQuote': 'Heavy, firm, square palm with thick blunt fingers and broad spatulate tips.',
        'hciImplication': 'Requires robust mechanical feedback, strong tactile click detents, and wide buttons.',
        'ratios': {
            'fingerToPalm': '1.00 : 1.00 (Equilateral Palm)',
            'wristToKnuckle': '0.95 : 1.00 (Solid Heavy Wrist)',
            'thicknessToWidth': '0.65 : 1.00 (Dense Compact Depth)'
        },
        'keyDiagnoses': [
            '1:1 equilateral square palm (width strictly equals length)',
            'Heavy, thick, parallel-sided cylindrical fingers',
            'Broad spatulate paddle tips with strong mechanical purchase',
            'Square nail plates with horizontal cuticle and free edge',
            'Dense, muscular thenar ball with maximal grip force'
        ],
        'scale_x': 1.05,
        'scale_y': 1.00,
        'scale_z': 1.10,
        'wrist_w': 112,
        'knuckle_w': 118,
        'condyle_bulge': 0.18,   # Firm square knuckles
        'shaft_waist': 0.98,     # Parallel cylinder
        'tip_radius': 16.0,
        'tip_shape': 'square',
        'thenar_bulk': 1.30,
        'palm_shape': 'square',
        'callouts': {
            'dorsal': [
                (175, 140, -25, 130, "Parallel Cylinders", "Uniform width across phalanges", "end"),
                (240, 80, -25, 70, "Square Paddle Tips", "Broad spatulate mechanical surface", "end"),
                (385, 250, 485, 240, "Powerful Thumb", "Heavy square block terminal", "start"),
                (280, 445, 485, 435, "Solid Heavy Wrist", "0.95:1.00 muscular wrist ratio", "start")
            ],
            'palmar': [
                (155, 375, -25, 365, "Dense Hypothenar", "Power-grip bracing shelf", "end"),
                (295, 370, 485, 360, "Muscular Thenar Mound", "Maximal grip clamp power", "start"),
                (245, 285, 485, 275, "Deep Flexor Chasm", "Pronounced transverse crease", "start")
            ],
            'lateral': [
                (205, 85, -25, 75, "Square Spatulate End", "Firm horizontal terminal", "end"),
                (215, 205, -25, 200, "Firm Articular Block", "Dense condylar structure", "end"),
                (320, 230, 485, 225, "Heavy Thumb Root", "Sturdy carpal foundation", "start")
            ],
            'threeQuarter': [
                (185, 135, -25, 125, "1:1 Cuboid Mass", "Equilateral volumetric block", "end"),
                (445, 250, 485, 245, "Dense Grip Cylinder", "High torque mechanical structure", "start")
            ]
        }
    },
    'osseous': {
        'name': 'The Osseous Hand',
        'subtitle': 'The Skeletal / Framework Type',
        'color': '#10b981',
        'historicalChart': 'Chart 8 (Page 184) · Osseous Hand & Face',
        'dominantSystem': 'Bony Skeleton (Structural Rigidity & Angular Resistance)',
        'geometricArchetype': 'The Oblong / Articulated Nodes',
        'bookQuote': 'Large, bony, knotty knuckles with sunken inter-joint spaces and oblong nails.',
        'hciImplication': 'Requires high spatial tolerance for non-planar knuckle articulation.',
        'ratios': {
            'fingerToPalm': '1.08 : 1.00 (Long Knotted Digits)',
            'wristToKnuckle': '0.76 : 1.00 (Prominent Bony Process)',
            'thicknessToWidth': '0.55 : 1.00 (Rigid Angular Depth)'
        },
        'keyDiagnoses': [
            'Protruding, knotty articular condyles at MCP, PIP, and DIP',
            'Deeply sunken/hollowed inter-joint phalanx shafts',
            'Prominent ulnar styloid process visible at wrist',
            'Oblong nail plates, noticeably longer than wide',
            'Angular, sinewy extensor tendons standing in sharp relief'
        ],
        'scale_x': 0.92,
        'scale_y': 1.08,
        'scale_z': 0.90,
        'wrist_w': 82,
        'knuckle_w': 108,
        'condyle_bulge': 0.35,   # Highly prominent bone knots
        'shaft_waist': 0.76,     # Deeply sunken inter-condylar shaft
        'tip_radius': 11.0,
        'tip_shape': 'oblong',
        'thenar_bulk': 0.92,
        'palm_shape': 'oblong',
        'callouts': {
            'dorsal': [
                (170, 135, -25, 125, "Hollowed Shafts", "Sunken inter-joint waist (0.76x)", "end"),
                (240, 72, -25, 60, "Knotty Condyles", "Prominent articular bone nodes", "end"),
                (380, 245, 485, 235, "Articulated Thumb", "Large knotty IP knuckle", "start"),
                (275, 445, 485, 435, "Ulnar Styloid Bump", "Prominent bony wrist process", "start")
            ],
            'palmar': [
                (150, 365, -25, 355, "Sinewy Hypothenar", "Firm osteological anchor", "end"),
                (285, 360, 485, 350, "Bony Thenar Ridge", "Tight ligamentous attachment", "start"),
                (240, 280, 485, 270, "Angular Creases", "Deeply incised joint lines", "start")
            ],
            'lateral': [
                (200, 80, -25, 70, "Oblong Tip Profile", "Rigid angular terminal", "end"),
                (215, 200, -25, 195, "Dorsal Condyle Peak", "Protruding articular knob", "end"),
                (315, 225, 485, 220, "Angular IP Knuckle", "Stark skeletal outline", "start")
            ],
            'threeQuarter': [
                (180, 125, -25, 115, "Articulated Node Skeleton", "Dual-condyle bone architecture", "end"),
                (440, 245, 485, 240, "Prominent Carpal Bridge", "Sinewy structural framework", "start")
            ]
        }
    },
    'cerebral': {
        'name': 'The Cerebral Hand',
        'subtitle': 'The Nervous / Mental Acuity Type',
        'color': '#8b5cf6',
        'historicalChart': 'Chart 10 (Page 228) · Cerebral Hand & Face',
        'dominantSystem': 'Central Nervous System (Cognition, Thought & High Sensory Acuity)',
        'geometricArchetype': 'The Slender Needle / Slender Oval',
        'bookQuote': 'Delicate, frail, slender fingers with straight parallel lines, no knots, and narrow wrist.',
        'hciImplication': 'Requires lightweight zero-pressure touch thresholds and micro-haptic confirmation.',
        'ratios': {
            'fingerToPalm': '1.12 : 1.00 (Slender Digits)',
            'wristToKnuckle': '0.69 : 1.00 (Delicate Frail Wrist)',
            'thicknessToWidth': '0.45 : 1.00 (Whisper-Thin Depth)'
        },
        'keyDiagnoses': [
            'Frail, slender, delicate fingers with smooth continuous outlines',
            'Zero articular knot swelling and zero fatty puffiness',
            'Exceptionally narrow, delicate wrist structure',
            'Pointed filbert (slender almond) nail plates',
            'Smooth, uniform phalanx shafts with clean parallel margins'
        ],
        'scale_x': 0.80,
        'scale_y': 1.12,
        'scale_z': 0.70,
        'wrist_w': 68,
        'knuckle_w': 98,
        'condyle_bulge': 0.00,   # Pure smooth straight lines
        'shaft_waist': 0.96,     # Slender straight shaft
        'tip_radius': 7.0,
        'tip_shape': 'filbert',
        'thenar_bulk': 0.75,
        'palm_shape': 'slender',
        'callouts': {
            'dorsal': [
                (170, 135, -25, 125, "Smooth Parallel Margins", "Zero knuckle nodes or bulges", "end"),
                (240, 68, -25, 55, "Frail & Slender", "Delicate 1.12:1.00 finger ratio", "end"),
                (378, 245, 485, 235, "Slender Upward Thumb", "Delicate 32° radial reach", "start"),
                (275, 445, 485, 435, "Delicate Frail Wrist", "0.69:1.00 narrow wrist ratio", "start")
            ],
            'palmar': [
                (150, 365, -25, 355, "Delicate Hypothenar", "Minimal muscular mass", "end"),
                (280, 360, 485, 350, "Frail Thenar Mound", "High-frequency sensory nerve density", "start"),
                (240, 280, 485, 270, "Delicate Skin Etchings", "Whisper-thin sensory folds", "start")
            ],
            'lateral': [
                (200, 75, -25, 65, "Filbert Slender Tip", "Delicate pointed almond free edge", "end"),
                (210, 195, -25, 190, "Pure Straight Profile", "Zero dorsal knuckle elevation", "end"),
                (315, 225, 485, 220, "Frail Thumb Reach", "Whisper-thin sagittal contour", "start")
            ],
            'threeQuarter': [
                (180, 125, -25, 115, "Slender Oval Prisms", "Minimal volumetric displacement", "end"),
                (440, 245, 485, 240, "Frail Spatial Arch", "Delicate high-acuity gesture", "start")
            ]
        }
    }
}


# =============================================================================
# 3. 3D KINEMATIC SKELETAL MODEL
# =============================================================================

class HandKinematicModel:
    """
    Computes 3D landmark coordinates (21 joints) based on:
    - Base morphological dimensions
    - Archetype deformation tensor (scale_x, scale_y, scale_z, wrist_w, knuckle_w)
    - Kinematic flexion angles (MCP, PIP, DIP, CMC, thumb abduction)
    """
    def __init__(self, archetype_key: str):
        self.arch_key = archetype_key
        self.arch = ARCHETYPES[archetype_key]

    def get_skeleton_3d(self, pose: Optional[Dict[str, float]] = None) -> Dict[str, Vec3]:
        """
        Calculates 3D coordinates for all 21 joints.
        Origin (0, 0, 0) is at the center of the wrist.
        +X: Radial / Thumb side (in dorsal view of left hand)
        +Y: Distal / Towards fingertips
        +Z: Dorsal / Towards back of hand
        """
        arch = self.arch
        sx = arch['scale_x']
        sy = arch['scale_y']
        sz = arch['scale_z']
        
        # Base anatomical lengths in standard 1000 UPM / canvas units
        palm_h = 160.0 * (1.0 / math.sqrt(sy))
        wrist_w = arch['wrist_w']
        knuckle_w = arch['knuckle_w']
        
        # Default neutral resting pose
        p = {
            'thumb_cmc': 35.0,  # Abduction
            'thumb_mcp': 15.0,
            'thumb_ip': 10.0,
            'index_mcp': 0.0, 'index_pip': 0.0, 'index_dip': 0.0,
            'middle_mcp': 0.0, 'middle_pip': 0.0, 'middle_dip': 0.0,
            'ring_mcp': 0.0, 'ring_pip': 0.0, 'ring_dip': 0.0,
            'little_mcp': 0.0, 'little_pip': 0.0, 'little_dip': 0.0,
        }
        if pose:
            p.update(pose)

        joints = {}
        # 1. Wrist root & carpal base
        joints['wrist'] = Vec3(0, 0, 0)
        joints['wrist_radial'] = Vec3(wrist_w * 0.5, 0, 0)
        joints['wrist_ulnar'] = Vec3(-wrist_w * 0.5, 0, 0)

        # 2. Metacarpal Heads (Knuckles / MCP joints)
        # Transverse metacarpal arch (peaks at middle finger)
        half_kw = knuckle_w * 0.5
        joints['little_mcp'] = Vec3(-half_kw * 0.85, palm_h * 0.88, -2.0 * sz)
        joints['ring_mcp']   = Vec3(-half_kw * 0.38, palm_h * 0.96,  3.0 * sz)
        joints['middle_mcp'] = Vec3( half_kw * 0.10, palm_h * 1.00,  5.0 * sz)
        joints['index_mcp']  = Vec3( half_kw * 0.58, palm_h * 0.94,  2.0 * sz)
        joints['thumb_cmc']  = Vec3( half_kw * 0.65, palm_h * 0.38, -6.0 * sz)

        # 3. Finger Lengths & Kinematic Chain
        # Digit III (Middle) is longest; IV, II, V follow Sloan optotype ratios
        finger_lengths = {
            'little': (42.0 * sy, 30.0 * sy, 22.0 * sy),
            'ring':   (56.0 * sy, 38.0 * sy, 26.0 * sy),
            'middle': (62.0 * sy, 44.0 * sy, 28.0 * sy),
            'index':  (54.0 * sy, 38.0 * sy, 25.0 * sy),
            'thumb':  (38.0 * sy, 36.0 * sy, 28.0 * sy)  # Metacarpal, Proximal, Distal
        }

        # Solve fingers (Index, Middle, Ring, Little)
        for d in ['little', 'ring', 'middle', 'index']:
            mcp_pt = joints[f'{d}_mcp']
            l_prox, l_inter, l_dist = finger_lengths[d]
            
            # Splay angles (abduction from hand axis)
            splay = {'little': -10.0, 'ring': -3.5, 'middle': 1.0, 'index': 6.0}[d]
            
            mcp_flex = p[f'{d}_mcp']
            pip_flex = p[f'{d}_pip']
            dip_flex = p[f'{d}_dip']

            # Segment 1: Proximal phalanx
            # Vector starts at MCP, rotates around splay and flexion
            v_prox = Vec3(0, l_prox, 0).rotate_z(splay).rotate_x(-mcp_flex)
            pip_pt = mcp_pt + v_prox
            joints[f'{d}_pip'] = pip_pt

            # Segment 2: Intermediate phalanx
            v_inter = Vec3(0, l_inter, 0).rotate_z(splay).rotate_x(-(mcp_flex + pip_flex))
            dip_pt = pip_pt + v_inter
            joints[f'{d}_dip'] = dip_pt

            # Segment 3: Distal phalanx & tip
            v_dist = Vec3(0, l_dist, 0).rotate_z(splay).rotate_x(-(mcp_flex + pip_flex + dip_flex))
            tip_pt = dip_pt + v_dist
            joints[f'{d}_tip'] = tip_pt

        # Solve thumb
        cmc_pt = joints['thumb_cmc']
        l_meta, l_prox, l_dist = finger_lengths['thumb']
        
        # Thumb projects outward and upward at ~35°-40°
        thumb_abd = p['thumb_cmc']
        thumb_mcp_flex = p['thumb_mcp']
        thumb_ip_flex = p['thumb_ip']

        # CMC -> MCP
        v_meta = Vec3(l_meta * 0.75, l_meta * 0.65, -4.0 * sz).rotate_z(-thumb_abd * 0.5)
        mcp_t = cmc_pt + v_meta
        joints['thumb_mcp'] = mcp_t

        # MCP -> IP
        v_t_prox = Vec3(l_prox * 0.70, l_prox * 0.70, 2.0 * sz).rotate_z(-thumb_abd * 0.7).rotate_x(-thumb_mcp_flex)
        ip_t = mcp_t + v_t_prox
        joints['thumb_ip'] = ip_t

        # IP -> Tip
        v_t_dist = Vec3(l_dist * 0.65, l_dist * 0.75, 1.0 * sz).rotate_z(-thumb_abd * 0.9).rotate_x(-(thumb_mcp_flex + thumb_ip_flex))
        tip_t = ip_t + v_t_dist
        joints['thumb_tip'] = tip_t

        return joints


# =============================================================================
# 4. PROCEDURAL MULTI-PERSPECTIVE SVG GENERATOR
# =============================================================================

class HandSVGDirector:
    """
    Builds the complete multi-layer diagnostic SVG for any given archetype and perspective.
    Guarantees that ALL 5 overlays exist and function in ALL 4 perspectives.
    """
    def __init__(self, archetype_key: str):
        self.arch_key = archetype_key
        self.arch = ARCHETYPES[archetype_key]
        self.kinematics = HandKinematicModel(archetype_key)

    def _get_projected_nodes(self, yaw: float, pitch: float,
                            cx: float = 240.0, cy: float = 380.0, scale: float = 1.0) -> Dict[str, Tuple[float, float, float]]:
        joints = self.kinematics.get_skeleton_3d()
        projected = {}
        for name, v in joints.items():
            projected[name] = project_3d(v, yaw, pitch, cx, cy, fov=900.0, scale=scale)
        return projected

    def generate_svg(self, perspective: str) -> str:
        """
        Generates full SVG markup for perspective:
        - 'dorsal': (yaw=0, pitch=0)
        - 'palmar': (yaw=180, pitch=0)
        - 'lateral': (yaw=90, pitch=0)
        - 'threeQuarter': (yaw=45, pitch=15)
        """
        c = self.arch['color']
        arch = self.arch

        if perspective == 'dorsal':
            yaw, pitch = 0.0, 0.0
            sub_title = "DORSAL (POSTERIOR / BACK VIEW)"
        elif perspective == 'palmar':
            yaw, pitch = 180.0, 0.0
            sub_title = "PALMAR (ANTERIOR / VOLAR VIEW)"
        elif perspective == 'lateral':
            yaw, pitch = 90.0, 0.0
            sub_title = "LATERAL PROFILE (SAGITTAL VIEW)"
        else: # threeQuarter
            yaw, pitch = 45.0, 15.0
            sub_title = "3/4 VOLUMETRIC ISOMETRIC ANGLE"

        # Projected joints
        nodes = self._get_projected_nodes(yaw, pitch)

        # SVG header and styling
        out = [
            f'<svg viewBox="-100 0 680 520" class="hand-vector-svg" xmlns="http://www.w3.org/2000/svg">',
            f'  <defs>',
            f'    <filter id="shadow_{self.arch_key}_{perspective}" x="-20%" y="-20%" width="140%" height="140%">',
            f'      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="{c}" flood-opacity="0.14"/>',
            f'    </filter>',
            f'    <filter id="badgeShadow" x="-20%" y="-20%" width="140%" height="140%">',
            f'      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.6"/>',
            f'    </filter>',
            f'  </defs>',
            f'  <rect x="-100" y="0" width="680" height="520" fill="#090d16"/>',
            f'  <text x="240" y="40" text-anchor="middle" fill="{c}" font-family="monospace" font-size="12" letter-spacing="1">PERSPECTIVE: {sub_title}</text>',
            f'  <text x="240" y="56" text-anchor="middle" fill="#64748b" font-family="monospace" font-size="9.5">BIOMETRIC TENSOR: {arch["geometricArchetype"].upper()}</text>'
        ]

        # LAYER 1: MASS ENVELOPE (.layer-mass)
        out.append(self._build_layer_mass(perspective, nodes, c))

        # LAYER 2: 3D PRIMITIVES WIREFRAME (.layer-primitives)
        out.append(self._build_layer_primitives(perspective, nodes, c))

        # LAYER 3: BIOMETRIC RATIOS (.layer-ratios)
        out.append(self._build_layer_ratios(perspective, nodes, c))

        # LAYER 4: SLOAN 5:1 OPTOTYPE GRID (.layer-sloan)
        out.append(self._build_layer_sloan(perspective, nodes, c))

        # LAYER 5: MAIN HAND CONTOUR (.layer-contour)
        out.append(self._build_layer_contour(perspective, nodes, c))

        # LAYER 6: DETAILS & NAILS (.layer-details)
        out.append(self._build_layer_details(perspective, nodes, c))

        # LAYER 7: LATERAL JOINT INSET PROFILE (.layer-inset)
        out.append(self._build_layer_inset(perspective, nodes, c))

        # LAYER 8: UNCLIPPED CALLOUT BADGES (.layer-callouts)
        out.append(self._build_layer_callouts(perspective, nodes, c))

        out.append('</svg>')
        return '\n'.join(out)

    # -------------------------------------------------------------------------
    # Layer Builders
    # -------------------------------------------------------------------------

    def _build_layer_mass(self, perspective: str, nodes: Dict, c: str) -> str:
        geom = self.arch['geometricArchetype']
        
        # Calculate bounding box of primary nodes
        all_pts = [nodes[k] for k in ['wrist', 'index_tip', 'middle_tip', 'little_tip', 'thumb_tip']]
        min_x = min(p[0] for p in all_pts)
        max_x = max(p[0] for p in all_pts)
        min_y = min(p[1] for p in all_pts)
        max_y = max(p[1] for p in all_pts)
        cx = (min_x + max_x) * 0.5
        cy = (min_y + max_y) * 0.5
        w = max_x - min_x
        h = max_y - min_y

        if 'Circle' in geom or self.arch_key == 'alimentive':
            path_mass = f'<ellipse cx="{cx}" cy="{cy + 20}" rx="{w*0.52}" ry="{h*0.50}" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 6"/>'
        elif 'Wedge' in geom or self.arch_key == 'thoracic':
            p_top = f"{cx} {min_y}"
            p_left = f"{min_x - 10} {min_y + h*0.45}"
            p_right = f"{max_x + 10} {min_y + h*0.45}"
            p_bl = f"{cx - w*0.22} {max_y}"
            p_br = f"{cx + w*0.22} {max_y}"
            path_mass = f'<polygon points="{p_top} {p_right} {p_br} {p_bl} {p_left}" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 6"/>'
        elif 'Square' in geom or self.arch_key == 'muscular':
            path_mass = f'<rect x="{min_x - 15}" y="{min_y + h*0.15}" width="{w + 30}" height="{h*0.85}" rx="8" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 6"/>'
        elif 'Oblong' in geom or self.arch_key == 'osseous':
            path_mass = f'<rect x="{min_x - 10}" y="{min_y}" width="{w + 20}" height="{h}" rx="24" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 6"/>'
        else: # Cerebral
            path_mass = f'<ellipse cx="{cx}" cy="{cy}" rx="{w*0.38}" ry="{h*0.52}" fill="{c}" fill-opacity="0.08" stroke="{c}" stroke-width="1.8" stroke-dasharray="6 6"/>'

        return f'''  <!-- LAYER 1: MASS ENVELOPE -->
  <g class="layer-mass">
    {path_mass}
    <text x="{cx}" y="{max_y + 24}" text-anchor="middle" fill="{c}" font-family="monospace" font-size="9" opacity="0.8">PHASE 1: {geom.upper()} ENVELOPE</text>
  </g>'''

    def _build_layer_primitives(self, perspective: str, nodes: Dict, c: str) -> str:
        elems = []

        if perspective == 'lateral':
            # Lateral profile primitives: sagittal blocks
            idx_tip = nodes['index_tip']
            w_pt = nodes['wrist']
            mcp = nodes['index_mcp']
            elems.append(f'<line x1="{w_pt[0]}" y1="{w_pt[1]}" x2="{mcp[0]}" y2="{mcp[1]}" stroke="{c}" stroke-width="3" opacity="0.4"/>')
            elems.append(f'<line x1="{mcp[0]}" y1="{mcp[1]}" x2="{idx_tip[0]}" y2="{idx_tip[1]}" stroke="{c}" stroke-width="2.5" opacity="0.4"/>')
            elems.append(f'<circle cx="{mcp[0]}" cy="{mcp[1]}" r="9" fill="none" stroke="{c}" stroke-width="1.6" stroke-dasharray="3 3"/>')
            elems.append(f'<circle cx="{nodes["index_pip"][0]}" cy="{nodes["index_pip"][1]}" r="7" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="3 3"/>')
            elems.append(f'<circle cx="{nodes["index_dip"][0]}" cy="{nodes["index_dip"][1]}" r="5" fill="none" stroke="{c}" stroke-width="1.2" stroke-dasharray="3 3"/>')
        else:
            # Multi-digit primitives
            for d in ['thumb', 'index', 'middle', 'ring', 'little']:
                tip_key = f'{d}_tip'
                mcp_key = f'{d}_mcp' if d != 'thumb' else 'thumb_cmc'
                if tip_key in nodes and mcp_key in nodes:
                    p1 = nodes[mcp_key]
                    p2 = nodes[tip_key]
                    elems.append(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{c}" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.5"/>')
                
                # Draw joint rings
                for j in ['mcp', 'pip', 'dip']:
                    k = f'{d}_{j}'
                    if k in nodes:
                        r = 6 if j == 'mcp' else (5 if j == 'pip' else 4)
                        if self.arch_key == 'alimentive':
                            elems.append(f'<circle cx="{nodes[k][0]}" cy="{nodes[k][1]}" r="{r+2}" fill="{c}" fill-opacity="0.15" stroke="{c}" stroke-width="1.2"/>')
                        elif self.arch_key == 'muscular':
                            elems.append(f'<rect x="{nodes[k][0]-r}" y="{nodes[k][1]-r}" width="{r*2}" height="{r*2}" rx="1" fill="{c}" fill-opacity="0.15" stroke="{c}" stroke-width="1.2"/>')
                        elif self.arch_key == 'osseous':
                            elems.append(f'<ellipse cx="{nodes[k][0]}" cy="{nodes[k][1]}" rx="{r+3}" ry="{r}" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.5"/>')
                        else:
                            elems.append(f'<circle cx="{nodes[k][0]}" cy="{nodes[k][1]}" r="{r}" fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="1"/>')

        return f'''  <!-- LAYER 2: 3D PRIMITIVES WIREFRAME -->
  <g class="layer-primitives" style="display: none;">
    {chr(10).join(elems)}
  </g>'''

    def _build_layer_ratios(self, perspective: str, nodes: Dict, c: str) -> str:
        r = self.arch['ratios']
        m_tip = nodes['middle_tip']
        m_mcp = nodes['middle_mcp']
        wrist = nodes['wrist']

        lines = [
            f'<!-- Caliper: Finger Length -->',
            f'<line x1="125" y1="{m_tip[1]}" x2="125" y2="{m_mcp[1]}" stroke="{c}" stroke-width="1.5"/>',
            f'<line x1="118" y1="{m_tip[1]}" x2="132" y2="{m_tip[1]}" stroke="{c}" stroke-width="1.5"/>',
            f'<line x1="118" y1="{m_mcp[1]}" x2="132" y2="{m_mcp[1]}" stroke="{c}" stroke-width="1.5"/>',
            f'<text x="112" y="{(m_tip[1] + m_mcp[1])*0.5 + 4}" text-anchor="end" fill="{c}" font-family="monospace" font-size="9" font-weight="bold">{r["fingerToPalm"].split()[0]}</text>',
            
            f'<!-- Caliper: Palm Length -->',
            f'<line x1="125" y1="{m_mcp[1]}" x2="125" y2="{wrist[1]}" stroke="{c}" stroke-width="1.5" stroke-dasharray="2 2"/>',
            f'<line x1="118" y1="{wrist[1]}" x2="132" y2="{wrist[1]}" stroke="{c}" stroke-width="1.5"/>',
            f'<text x="112" y="{(m_mcp[1] + wrist[1])*0.5 + 4}" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="8.5">Palm: 1.00</text>',

            f'<!-- Caliper: Wrist Width -->',
            f'<line x1="180" y1="{wrist[1] + 18}" x2="300" y2="{wrist[1] + 18}" stroke="{c}" stroke-width="1.2"/>',
            f'<line x1="180" y1="{wrist[1] + 12}" x2="180" y2="{wrist[1] + 24}" stroke="{c}" stroke-width="1.2"/>',
            f'<line x1="300" y1="{wrist[1] + 12}" x2="300" y2="{wrist[1] + 24}" stroke="{c}" stroke-width="1.2"/>',
            f'<text x="240" y="{wrist[1] + 32}" text-anchor="middle" fill="{c}" font-family="monospace" font-size="8.5">Wrist:Knuckle = {r["wristToKnuckle"]}</text>'
        ]

        if perspective == 'lateral':
            lines.append(f'<text x="240" y="{wrist[1] + 44}" text-anchor="middle" fill="#38bdf8" font-family="monospace" font-size="8.5">Sagittal Depth Ratio = {r["thicknessToWidth"]}</text>')

        return f'''  <!-- LAYER 3: BIOMETRIC RATIOS -->
  <g class="layer-ratios" style="display: none;">
    {chr(10).join(lines)}
  </g>'''

    def _build_layer_sloan(self, perspective: str, nodes: Dict, c: str) -> str:
        unit = 65
        start_x = 240 - (2.5 * unit)
        start_y = 260 - (2.5 * unit)
        lines = []
        for i in range(6):
            x = start_x + (i * unit)
            y = start_y + (i * unit)
            lines.append(f'<line x1="{x}" y1="{start_y}" x2="{x}" y2="{start_y + 5*unit}" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.3"/>')
            lines.append(f'<line x1="{start_x}" y1="{y}" x2="{start_x + 5*unit}" y2="{y}" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.3"/>')
        lines.append(f'<rect x="{start_x}" y="{start_y - 20}" width="165" height="17" rx="3" fill="#090d16" stroke="#38bdf8" stroke-width="0.8" opacity="0.85"/>')
        lines.append(f'<text x="{start_x + 6}" y="{start_y - 8}" fill="#38bdf8" font-family="monospace" font-size="9" font-weight="bold">SLOAN 5×5 OPTOTYPE (1U=65px)</text>')

        return f'''  <!-- LAYER 4: SLOAN 5x5 OPTOTYPE GRID -->
  <g class="layer-sloan" style="display: none;">
    {chr(10).join(lines)}
  </g>'''

    def _build_layer_contour(self, perspective: str, nodes: Dict, c: str) -> str:
        """
        Generates the smooth anatomical contour tailored to the archetype and perspective.
        """
        arch_k = self.arch_key
        flt = f"url(#shadow_{arch_k}_{perspective})"

        if perspective == 'dorsal':
            return self._build_dorsal_contour_path(c, flt)
        elif perspective == 'palmar':
            return self._build_palmar_contour_path(c, flt)
        elif perspective == 'lateral':
            return self._build_lateral_contour_path(c, flt)
        else: # threeQuarter
            return self._build_three_quarter_contour_path(c, flt)

    def _build_dorsal_contour_path(self, c: str, flt: str) -> str:
        k = self.arch_key
        if k == 'alimentive':
            d = ("M 175 440 "
                 "C 170 380, 140 330, 138 275 "
                 "C 134 240, 126 195, 140 162 "
                 "C 146 142, 172 142, 176 162 "
                 "L 176 255 L 188 255 "
                 "L 188 128 "
                 "C 194 108, 222 108, 226 128 "
                 "L 226 250 L 238 250 "
                 "L 238 98 "
                 "C 244 76, 274 76, 280 98 "
                 "L 280 252 L 292 252 "
                 "L 292 135 "
                 "C 298 115, 326 115, 332 135 "
                 "L 332 258 "
                 "C 336 275, 345 285, 360 278 "
                 "C 374 270, 395 245, 412 232 "
                 "C 424 220, 442 228, 436 245 "
                 "C 426 270, 420 310, 404 345 "
                 "C 382 385, 345 420, 295 440 Z")
        elif k == 'thoracic':
            d = ("M 195 445 "
                 "C 190 385, 170 335, 168 275 "
                 "C 162 235, 150 185, 158 135 "
                 "C 162 115, 180 115, 184 135 "
                 "L 184 252 L 194 252 "
                 "L 194 95 "
                 "C 198 75, 218 75, 222 95 "
                 "L 222 248 L 232 248 "
                 "L 232 62 "
                 "C 236 42, 256 42, 260 62 "
                 "L 260 250 L 270 250 "
                 "L 270 102 "
                 "C 274 82, 294 82, 298 102 "
                 "L 298 258 "
                 "C 304 278, 316 288, 332 278 "
                 "C 346 268, 368 240, 384 225 "
                 "C 394 212, 410 220, 404 235 "
                 "C 396 260, 390 305, 376 340 "
                 "C 354 380, 318 420, 270 445 Z")
        elif k == 'muscular':
            d = ("M 172 445 "
                 "C 168 385, 150 335, 148 275 "
                 "C 142 235, 134 185, 145 145 "
                 "L 175 145 "
                 "L 175 255 L 188 255 "
                 "L 188 112 "
                 "L 220 112 "
                 "L 220 250 L 234 250 "
                 "L 234 82 "
                 "L 268 82 "
                 "L 268 252 L 282 252 "
                 "L 282 120 "
                 "L 314 120 "
                 "L 314 260 "
                 "C 320 280, 332 290, 348 280 "
                 "C 362 270, 385 245, 402 232 "
                 "L 426 242 "
                 "C 420 272, 412 318, 398 350 "
                 "C 378 388, 342 425, 298 445 Z")
        elif k == 'osseous':
            d = ("M 188 445 "
                 "C 184 385, 162 335, 158 275 "
                 "C 148 238, 140 185, 150 142 "
                 "C 155 125, 175 125, 180 142 "
                 "L 178 252 L 190 252 "
                 "L 188 105 "
                 "C 192 88, 216 88, 222 105 "
                 "L 220 248 L 232 248 "
                 "L 230 75 "
                 "C 235 56, 260 56, 265 75 "
                 "L 262 250 L 274 250 "
                 "L 272 112 "
                 "C 278 95, 300 95, 305 112 "
                 "L 302 258 "
                 "C 308 278, 320 288, 335 278 "
                 "C 348 268, 370 242, 386 228 "
                 "C 396 215, 412 222, 408 238 "
                 "C 398 265, 390 310, 378 345 "
                 "C 358 385, 322 422, 276 445 Z")
        else: # cerebral
            d = ("M 195 445 "
                 "C 192 385, 178 335, 174 278 "
                 "C 170 240, 160 195, 164 142 "
                 "C 166 122, 182 122, 184 142 "
                 "L 184 255 L 196 255 "
                 "L 196 102 "
                 "C 198 82, 216 82, 218 102 "
                 "L 218 255 L 230 255 "
                 "L 230 78 "
                 "C 232 58, 250 58, 252 78 "
                 "L 252 255 L 264 255 "
                 "L 264 112 "
                 "C 266 92, 282 92, 284 112 "
                 "L 284 255 L 296 255 "
                 "L 296 148 "
                 "C 298 130, 312 130, 314 148 "
                 "C 316 200, 308 258, 304 278 "
                 "C 300 295, 312 305, 326 295 "
                 "C 338 285, 354 265, 368 248 "
                 "C 376 236, 390 242, 386 256 "
                 "C 380 278, 378 318, 366 348 "
                 "C 348 382, 315 418, 275 445 Z")

        return f'''  <!-- LAYER 5: MAIN HAND CONTOUR -->
  <g class="layer-contour">
    <path d="{d}" fill="#1e293b" stroke="{c}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round" filter="{flt}"/>
  </g>'''

    def _build_palmar_contour_path(self, c: str, flt: str) -> str:
        k = self.arch_key
        th_b = self.arch['thenar_bulk']
        thenar_x = int(round(365 + (th_b - 1.0) * 25))
        
        if k == 'alimentive':
            d = ("M 175 440 "
                 "C 170 380, 140 330, 138 275 "
                 "C 134 240, 126 195, 140 162 "
                 "C 146 142, 172 142, 176 162 "
                 "L 176 255 L 188 255 "
                 "L 188 128 "
                 "C 194 108, 222 108, 226 128 "
                 "L 226 250 L 238 250 "
                 "L 238 98 "
                 "C 244 76, 274 76, 280 98 "
                 "L 280 252 L 292 252 "
                 "L 292 135 "
                 "C 298 115, 326 115, 332 135 "
                 "L 332 258 "
                 "C 336 275, 345 285, 360 278 "
                 "C 374 270, 395 245, 412 232 "
                 "C 424 220, 442 228, 436 245 "
                 "C 426 270, 420 310, 404 345 "
                 "C 382 385, 345 420, 295 440 Z")
        elif k == 'muscular':
            d = ("M 172 445 "
                 "C 168 385, 150 335, 148 275 "
                 "C 142 235, 134 185, 145 145 "
                 "L 175 145 "
                 "L 175 255 L 188 255 "
                 "L 188 112 "
                 "L 220 112 "
                 "L 220 250 L 234 250 "
                 "L 234 82 "
                 "L 268 82 "
                 "L 268 252 L 282 252 "
                 "L 282 120 "
                 "L 314 120 "
                 "L 314 260 "
                 "C 320 280, 332 290, 348 280 "
                 "C 362 270, 385 245, 402 232 "
                 "L 426 242 "
                 "C 420 272, 412 318, 398 350 "
                 "C 378 388, 342 425, 298 445 Z")
        elif k == 'osseous':
            d = ("M 188 445 "
                 "C 184 385, 162 335, 158 275 "
                 "C 148 238, 140 185, 150 142 "
                 "C 155 125, 175 125, 180 142 "
                 "L 178 252 L 190 252 "
                 "L 188 105 "
                 "C 192 88, 216 88, 222 105 "
                 "L 220 248 L 232 248 "
                 "L 230 75 "
                 "C 235 56, 260 56, 265 75 "
                 "L 262 250 L 274 250 "
                 "L 272 112 "
                 "C 278 95, 300 95, 305 112 "
                 "L 302 258 "
                 "C 308 278, 320 288, 335 278 "
                 "C 348 268, 370 242, 386 228 "
                 "C 396 215, 412 222, 408 238 "
                 "C 398 265, 390 310, 378 345 "
                 "C 358 385, 322 422, 276 445 Z")
        else:
            d = (f"M 160 445 "
                 f"C 155 390, 138 340, 142 275 "
                 f"C 138 245, 130 200, 140 165 "
                 f"C 146 145, 170 145, 174 165 "
                 f"L 174 252 L 186 252 "
                 f"L 186 118 "
                 f"C 192 98, 218 98, 224 118 "
                 f"L 224 248 L 236 248 "
                 f"L 236 85 "
                 f"C 242 65, 270 65, 276 85 "
                 f"L 276 250 L 288 250 "
                 f"L 288 125 "
                 f"C 294 105, 320 105, 326 125 "
                 f"L 326 260 "
                 f"C 332 280, 344 290, 358 280 "
                 f"C 370 270, 388 245, 402 232 "
                 f"C 412 220, 428 228, 424 242 "
                 f"C 416 268, {thenar_x} 315, 396 348 "
                 f"C 374 385, 340 422, 290 445 Z")

        return f'''  <!-- LAYER 5: MAIN HAND CONTOUR (PALMAR) -->
  <g class="layer-contour">
    <!-- Volar palmar face of left hand -->
    <g transform="translate(480, 0) scale(-1, 1)">
      <path d="{d}" fill="#1e293b" stroke="{c}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round" filter="{flt}"/>
    </g>
  </g>'''

    def _build_lateral_contour_path(self, c: str, flt: str) -> str:
        sz = self.arch['scale_z']
        condyle = self.arch['condyle_bulge']
        tip_r = self.arch['tip_radius']
        
        bump = int(round(condyle * 18))
        d_knuckle_x = 210 - bump
        palm_thick = int(round(55 * sz))
        wrist_thick = int(round(45 * sz))

        d = (f"M 210 445 "
             f"L 210 330 "
             f"C {d_knuckle_x} 290, {d_knuckle_x} 240, {210 - bump*2} 200 "
             f"C {205 - bump} 160, 210 120, 214 85 "
             f"C 218 70, {218 + int(tip_r*1.2)} 70, {222 + int(tip_r*1.2)} 85 "
             f"C {228 + int(tip_r*0.5)} 120, 232 160, 232 200 "
             f"C 240 230, 248 255, 258 270 "
             f"C 272 250, 290 230, 310 220 "
             f"C 322 215, 332 225, 328 238 "
             f"C 320 260, 298 285, 282 310 "
             f"C {245 + palm_thick} 335, {235 + wrist_thick} 380, {210 + wrist_thick} 445 "
             f"Z")

        return f'''  <!-- LAYER 5: MAIN HAND CONTOUR (LATERAL PROFILE) -->
  <g class="layer-contour">
    <path d="{d}" fill="#1e293b" stroke="{c}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round" filter="{flt}"/>
  </g>'''

    def _build_three_quarter_contour_path(self, c: str, flt: str) -> str:
        k = self.arch_key
        sy = self.arch['scale_y']
        
        d = ("M 170 445 "
             "C 165 395, 155 340, 165 285 "
             "C 155 240, 150 185, 165 135 "
             "C 172 118, 190 118, 196 135 "
             "C 202 185, 198 235, 204 250 "
             "C 208 190, 214 105, 228 75 "
             "C 238 60, 256 60, 264 75 "
             "C 274 105, 270 190, 274 250 "
             "C 280 205, 286 128, 298 120 "
             "C 308 108, 324 110, 330 125 "
             "C 338 165, 332 215, 336 250 "
             "C 342 220, 350 175, 362 165 "
             "C 370 155, 384 158, 386 172 "
             "C 388 205, 376 265, 370 285 "
             "C 368 298, 382 305, 396 295 "
             "C 410 282, 426 260, 436 245 "
             "C 445 232, 456 240, 452 255 "
             "C 442 280, 435 325, 415 355 "
             "C 395 390, 360 425, 315 445 Z")

        return f'''  <!-- LAYER 5: MAIN HAND CONTOUR (3/4 PERSPECTIVE) -->
  <g class="layer-contour">
    <path d="{d}" fill="#1e293b" stroke="{c}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round" filter="{flt}"/>
  </g>'''

    def _build_layer_details(self, perspective: str, nodes: Dict, c: str) -> str:
        elems = []
        k = self.arch_key

        if perspective == 'dorsal':
            elems.append(f'<path d="M 230 430 C 230 360, 205 290, 205 255" fill="none" stroke="{c}" stroke-width="1.2" opacity="0.35"/>')
            elems.append(f'<path d="M 238 430 C 240 360, 245 290, 245 250" fill="none" stroke="{c}" stroke-width="1.2" opacity="0.35"/>')
            elems.append(f'<path d="M 246 430 C 255 360, 278 290, 278 252" fill="none" stroke="{c}" stroke-width="1.2" opacity="0.35"/>')
            elems.append(f'<path d="M 252 430 C 275 370, 310 310, 335 275" fill="none" stroke="{c}" stroke-width="1.2" opacity="0.35"/>')

            from generate_five_hand_types_svg import get_nail_svg
            if k == 'alimentive':
                elems.append(get_nail_svg(158, 162, 16, 14, 'round', 0, c))
                elems.append(get_nail_svg(207, 128, 18, 16, 'round', 0, c))
                elems.append(get_nail_svg(259, 98, 20, 17, 'round', 0, c))
                elems.append(get_nail_svg(312, 135, 17, 15, 'round', 0, c))
                elems.append(get_nail_svg(425, 235, 18, 16, 'round', 30, c))
            elif k == 'thoracic':
                elems.append(get_nail_svg(171, 135, 12, 18, 'conical', 0, c))
                elems.append(get_nail_svg(208, 95, 14, 20, 'conical', 0, c))
                elems.append(get_nail_svg(246, 62, 14, 22, 'conical', 0, c))
                elems.append(get_nail_svg(284, 102, 13, 19, 'conical', 0, c))
                elems.append(get_nail_svg(396, 228, 14, 20, 'conical', 38, c))
            elif k == 'muscular':
                elems.append(get_nail_svg(160, 145, 18, 18, 'square', 0, c))
                elems.append(get_nail_svg(204, 112, 20, 20, 'square', 0, c))
                elems.append(get_nail_svg(251, 82, 22, 22, 'square', 0, c))
                elems.append(get_nail_svg(298, 120, 19, 19, 'square', 0, c))
                elems.append(get_nail_svg(416, 235, 20, 20, 'square', 42, c))
            elif k == 'osseous':
                elems.append(get_nail_svg(165, 142, 13, 20, 'oblong', 0, c))
                elems.append(get_nail_svg(205, 105, 15, 22, 'oblong', 0, c))
                elems.append(get_nail_svg(247, 75, 16, 24, 'oblong', 0, c))
                elems.append(get_nail_svg(288, 112, 14, 21, 'oblong', 0, c))
                elems.append(get_nail_svg(400, 230, 15, 22, 'oblong', 40, c))
            else: # cerebral
                elems.append(get_nail_svg(174, 142, 10, 16, 'cerebral', 0, c))
                elems.append(get_nail_svg(207, 102, 12, 18, 'cerebral', 0, c))
                elems.append(get_nail_svg(241, 78, 12, 20, 'cerebral', 0, c))
                elems.append(get_nail_svg(274, 112, 11, 17, 'cerebral', 0, c))
                elems.append(get_nail_svg(376, 252, 12, 18, 'cerebral', 32, c))

        elif perspective == 'palmar':
            elems.append(f'<path d="M 235 285 C 265 320, 275 370, 245 420" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/>')
            elems.append(f'<path d="M 235 285 C 195 295, 160 325, 140 345" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>')
            elems.append(f'<path d="M 130 280 C 175 265, 215 265, 255 275" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/>')
            elems.append(f'<line x1="145" y1="200" x2="168" y2="200" stroke="{c}" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>')
            elems.append(f'<line x1="190" y1="175" x2="218" y2="175" stroke="{c}" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>')
            elems.append(f'<line x1="242" y1="155" x2="270" y2="155" stroke="{c}" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>')
            elems.append(f'<line x1="292" y1="185" x2="320" y2="185" stroke="{c}" stroke-width="1.8" stroke-linecap="round" opacity="0.7"/>')
            th_r = int(round(35 * self.arch['thenar_bulk']))
            elems.append(f'<ellipse cx="285" cy="370" rx="{th_r}" ry="45" fill="{c}" fill-opacity="0.14" stroke="{c}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            elems.append(f'<text x="285" y="374" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9.5" font-weight="bold">Thenar Eminence</text>')
            elems.append(f'<ellipse cx="155" cy="375" rx="26" ry="38" fill="{c}" fill-opacity="0.10" stroke="{c}" stroke-width="1.2" stroke-dasharray="3 3"/>')
            elems.append(f'<text x="155" y="379" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="9">Hypothenar Pad</text>')

        elif perspective == 'lateral':
            elems.append(f'<path d="M 214 88 Q 224 78 234 88" fill="none" stroke="{c}" stroke-width="2.4"/>')
            elems.append(f'<rect x="218" y="84" width="14" height="5" rx="1.5" fill="{c}" fill-opacity="0.45"/>')
            elems.append(f'<path d="M 258 270 C 275 250, 298 235, 318 225" fill="none" stroke="{c}" stroke-width="1.8" stroke-dasharray="3 3"/>')
            elems.append(f'<ellipse cx="320" cy="225" rx="6" ry="4" fill="{c}" fill-opacity="0.45" transform="rotate(25, 320, 225)"/>')

        else: # threeQuarter
            elems.append(f'<path d="M 165 285 Q 235 305 370 285" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="3 3" opacity="0.65"/>')
            elems.append(f'<path d="M 175 350 Q 240 375 345 385" fill="none" stroke="{c}" stroke-width="1.4" stroke-dasharray="3 3" opacity="0.65"/>')

        return f'''  <!-- LAYER 6: ANATOMICAL DETAILS & NAILS -->
  <g class="layer-details">
    {chr(10).join(elems)}
  </g>'''

    def _build_layer_inset(self, perspective: str, nodes: Dict, c: str) -> str:
        k = self.arch_key
        lines = [
            f'<rect x="-10" y="-10" width="135" height="140" rx="8" fill="#090d16" stroke="{c}" stroke-width="1.4" filter="url(#badgeShadow)"/>',
            f'<text x="57" y="10" text-anchor="middle" fill="{c}" font-family="system-ui" font-size="10" font-weight="bold">LATERAL CUTAWAY</text>'
        ]
        
        if k == 'alimentive':
            lines.extend([
                f'<text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"Dimpled Knuckle" Profile</text>',
                f'<rect x="48" y="32" width="18" height="75" rx="8" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>',
                f'<circle cx="57" cy="68" r="4.5" fill="#090d16" stroke="{c}" stroke-width="1.5"/>',
                f'<line x1="28" y1="68" x2="48" y2="68" stroke="{c}" stroke-width="1.2"/>',
                f'<text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Dimple</text>',
                f'<text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Depression</text>'
            ])
        elif k == 'thoracic':
            lines.extend([
                f'<text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"Conical Taper" Profile</text>',
                f'<polygon points="44,105 70,105 60,30 54,30" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>',
                f'<ellipse cx="57" cy="30" rx="3.5" ry="5" fill="{c}" fill-opacity="0.6"/>',
                f'<line x1="28" y1="68" x2="48" y2="68" stroke="{c}" stroke-width="1.2"/>',
                f'<text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Taper</text>',
                f'<text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">0.72 Ratio</text>'
            ])
        elif k == 'muscular':
            lines.extend([
                f'<text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"1:1 Block" Profile</text>',
                f'<rect x="46" y="32" width="22" height="75" rx="2" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="2"/>',
                f'<rect x="48" y="30" width="18" height="6" rx="1" fill="{c}" fill-opacity="0.5"/>',
                f'<line x1="28" y1="68" x2="44" y2="68" stroke="{c}" stroke-width="1.2"/>',
                f'<text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Parallel</text>',
                f'<text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Uniform Width</text>'
            ])
        elif k == 'osseous':
            lines.extend([
                f'<text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"Articular Node" Profile</text>',
                f'<path d="M 50 105 L 50 85 C 40 80, 40 60, 50 55 L 50 32 L 64 32 L 64 55 C 74 60, 74 80, 64 85 L 64 105 Z" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.9"/>',
                f'<circle cx="57" cy="70" r="8" fill="{c}" fill-opacity="0.45" stroke="{c}" stroke-width="1.4"/>',
                f'<line x1="28" y1="70" x2="48" y2="70" stroke="{c}" stroke-width="1.2"/>',
                f'<text x="25" y="73" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Bony Node</text>',
                f'<text x="25" y="81" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">+0.35 Bulge</text>'
            ])
        else: # cerebral
            lines.extend([
                f'<text x="57" y="22" text-anchor="middle" fill="#94a3b8" font-family="system-ui" font-size="8.5">"Smooth Finger" Profile</text>',
                f'<rect x="50" y="32" width="14" height="75" fill="{c}" fill-opacity="0.25" stroke="{c}" stroke-width="1.8"/>',
                f'<ellipse cx="57" cy="30" rx="5" ry="4" fill="{c}" fill-opacity="0.5"/>',
                f'<line x1="28" y1="68" x2="48" y2="68" stroke="{c}" stroke-width="1.2"/>',
                f'<text x="25" y="71" text-anchor="end" fill="{c}" font-family="monospace" font-size="8">Straight</text>',
                f'<text x="25" y="79" text-anchor="end" fill="#94a3b8" font-family="monospace" font-size="7.5">Edges</text>'
            ])

        return f'''  <!-- LAYER 7: LATERAL JOINT INSET PROFILE -->
  <g class="layer-inset" style="display: none;" transform="translate(420, 80)">
    {chr(10).join(lines)}
  </g>'''

    def _build_layer_callouts(self, perspective: str, nodes: Dict, c: str) -> str:
        callouts = self.arch['callouts'].get(perspective, self.arch['callouts']['dorsal'])
        from generate_five_hand_types_svg import get_callout_badge
        badges = []
        for x1, y1, x2, y2, title, sub, anchor in callouts:
            badges.append(get_callout_badge(x1, y1, x2, y2, title, sub, c, anchor))
        return f'''  <!-- LAYER 8: UNCLIPPED CALLOUT BADGES -->
  <g class="layer-callouts">
    {chr(10).join(badges)}
  </g>'''

if __name__ == '__main__':
    print("Testing HandKinematicModel & HandSVGDirector...")
    for ak in ['alimentive', 'thoracic', 'muscular', 'osseous', 'cerebral']:
        director = HandSVGDirector(ak)
        for p in ['dorsal', 'palmar', 'lateral', 'threeQuarter']:
            svg = director.generate_svg(p)
            print(f"Generated {ak} [{p}]: {len(svg)} bytes, class count: {svg.count('class=')}")
    print("All archetypes & perspectives tested successfully!")
