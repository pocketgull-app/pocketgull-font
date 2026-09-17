/**
 * PocketGull 360° Volumetric 3D Spinning Hand & Kinematic ROM Inspector
 * =====================================================================
 * Inspired by the PocketGull 3D Spatial Holocalligramme and Adobe Substance 3D Turntable:
 * - Pure 3D Stereoscopic Transform Carousel (perspective: 1200px, preserve-3d)
 * - 3 Volumetric Anatomical Layers:
 *     Layer 1 (+28px): Dorsal/Volar Contours & Nails (Tactile Felt-Marker DNA)
 *     Layer 2 (  0px): Osteological Joint Matrix & Kinematic ROM Rings (MCP/PIP/DIP)
 *     Layer 3 (-28px): Deep Tendon Tracks & Palmar Telemetry Grid (600 UPM Monospace)
 * - 60 FPS requestAnimationFrame continuous orbital spin
 * - Interactive pointer drag orbit (azimuth + pitch), wheel dolly/zoom, preset snaps
 * - Multi-Morphology: Sloan 5:1, Alimentive, Thoracic, Muscular, Osseous, Cerebral
 */

const ASL_KINEMATICS_DATA = {
  "A": {
    name: "Fist / Pollex Adduction",
    mcp: 90, pip: 105, dip: 80, cmc: 15,
    motionArc: "MCP flex 90°, PIP 105° tight curl, thumb medial clamp against index radial margin.",
    comfort: 96,
    activeJoints: ["MCP", "PIP", "DIP", "CMC"],
    contactPoint: { x: 30, y: 56, label: "Thumb / Index Contact" }
  },
  "B": {
    name: "Flat Blade / Pollex Fold",
    mcp: 0, pip: 0, dip: 0, cmc: 65,
    motionArc: "Full digit extension (0°), thumb adduction & transverse flexion across proximal palm.",
    comfort: 98,
    activeJoints: ["CMC"],
    contactPoint: { x: 50, y: 72, label: "Thumb Pad / Palmar Crease" }
  },
  "C": {
    name: "Arcuate Cusp (Louise Sloan 5:1)",
    mcp: 45, pip: 50, dip: 40, cmc: 45,
    motionArc: "Smooth continuous arc across all 3 phalanges; thumb abducted into opposing 5:1 optical arc.",
    comfort: 99,
    activeJoints: ["MCP", "PIP", "DIP", "CMC"],
    contactPoint: null
  },
  "D": {
    name: "Index Isolation / Ring Clasp",
    mcp: 85, pip: 95, dip: 75, cmc: 55,
    motionArc: "Index kept at 0° extension; Middle, Ring, Pinky curled into tight loop with thumb pad.",
    comfort: 94,
    activeJoints: ["PIP", "DIP", "CMC"],
    contactPoint: { x: 56, y: 68, label: "Thumb / Middle Pad Ring" }
  },
  "E": {
    name: "Claw Hook / Thumb Shelf",
    mcp: 85, pip: 95, dip: 20, cmc: 60,
    motionArc: "Fingers flex at PIP onto horizontal thumb shelf; DIP flattened into Louise Sloan optotype shelf.",
    comfort: 92,
    activeJoints: ["PIP", "CMC"],
    contactPoint: { x: 60, y: 72, label: "Fingertip / Thumb Shelf Lock" }
  },
  "F": {
    name: "Index-Thumb O-Ring / Tri-Spread",
    mcp: 0, pip: 0, dip: 0, cmc: 50,
    motionArc: "Index & Thumb meet at tip forming clean aperture; Middle, Ring, Pinky splayed vertical.",
    comfort: 95,
    activeJoints: ["Index MCP", "Thumb CMC"],
    contactPoint: { x: 32, y: 56, label: "Index / Thumb Pinch Node" }
  },
  "G": {
    name: "Horizontal Index / Thumb Pinch",
    mcp: 90, pip: 90, dip: 0, cmc: 30,
    motionArc: "Index extended horizontally; thumb parallel above; forearm pronated 90°.",
    comfort: 94,
    activeJoints: ["Pronation", "Thumb CMC"],
    contactPoint: null
  },
  "H": {
    name: "Twin Horizontal Blades",
    mcp: 90, pip: 0, dip: 0, cmc: 40,
    motionArc: "Index and Middle extended horizontally parallel; Ring & Pinky curled.",
    comfort: 95,
    activeJoints: ["Index", "Middle"],
    contactPoint: null
  },
  "I": {
    name: "Pinky Isolation",
    mcp: 0, pip: 0, dip: 0, cmc: 60,
    motionArc: "Pinky in pure 0° vertical extension; Index, Middle, Ring locked in fist by thumb.",
    comfort: 97,
    activeJoints: ["Pinky Extensor"],
    contactPoint: { x: 50, y: 70, label: "Thumb / Ring Clasp" }
  },
  "K": {
    name: "Victory Pitch / Thumb Saddle Wedge",
    mcp: 0, pip: 25, dip: 10, cmc: 35,
    motionArc: "Index straight up, Middle angled 25° forward; Thumb tip wedged into Middle MCP crook.",
    comfort: 91,
    activeJoints: ["Middle MCP", "Thumb Saddle"],
    contactPoint: { x: 48, y: 46, label: "Thumb Tip / Middle Phalanx Registration" }
  },
  "L": {
    name: "Orthogonal Right Angle",
    mcp: 0, pip: 0, dip: 0, cmc: 90,
    motionArc: "Index straight up (0°), Thumb in maximal 90° radial abduction; 3 digits in palm.",
    comfort: 99,
    activeJoints: ["Thumb Abduction"],
    contactPoint: null
  },
  "M": {
    name: "Tri-Drape Fist (Thumb Under 3)",
    mcp: 90, pip: 100, dip: 80, cmc: 75,
    motionArc: "Thumb slides across palm under Index, Middle, and Ring; thumb tip emerges under Ring.",
    comfort: 88,
    activeJoints: ["Deep Flexor", "Pollex Opposition"],
    contactPoint: { x: 64, y: 74, label: "Thumb / Ring Emergence Point" }
  },
  "N": {
    name: "Bi-Drape Fist (Thumb Under 2)",
    mcp: 90, pip: 100, dip: 80, cmc: 65,
    motionArc: "Thumb slides under Index and Middle; thumb tip emerges under Middle digit.",
    comfort: 91,
    activeJoints: ["Deep Flexor", "Pollex Opposition"],
    contactPoint: { x: 54, y: 74, label: "Thumb / Middle Emergence Point" }
  },
  "O": {
    name: "Full Palmar Aperture Loop",
    mcp: 60, pip: 70, dip: 45, cmc: 60,
    motionArc: "All 4 fingertips curve to touch thumb tip, forming an open Louise Sloan 5:1 oval ring.",
    comfort: 97,
    activeJoints: ["Circumduction", "DIP Curl"],
    contactPoint: { x: 56, y: 54, label: "Fingertip-Thumb Ring Junction" }
  },
  "S": {
    name: "Transverse Front Thumb Clasp",
    mcp: 95, pip: 105, dip: 85, cmc: 70,
    motionArc: "Full fist clenched; thumb flexes horizontally across the anterior dorsal surface of all digits.",
    comfort: 95,
    activeJoints: ["Thumb Horizontal Flexion"],
    contactPoint: { x: 60, y: 62, label: "Thumb Cross-Fist Lock" }
  },
  "T": {
    name: "Index-Over-Thumb Interlock",
    mcp: 90, pip: 100, dip: 80, cmc: 40,
    motionArc: "Thumb tip hyperextends up between Index and Middle knuckles; Index drapes over thumb tip.",
    comfort: 90,
    activeJoints: ["Thumb IP", "Index Drapery"],
    contactPoint: { x: 44, y: 46, label: "Thumb Tip Between Index/Middle" }
  }
};

class ASLTurntable {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.azimuth = 0;          // 0° to 360°
    this.elevation = 12;       // -30° to +60°
    this.zoom = 1.0;           // 0.7x to 1.6x
    this.currentChar = 'A';
    this.currentModel = 'sloan';
    this.showROM = true;
    this.isAutoSpinning = true; // SPINNING BY DEFAULT!
    this.animationFrameId = null;
    this.isDragging = false;
    this.startX = 0;
    this.startY = 0;

    this.renderWidget();
    this.bindEvents();
    this.drawTurntable();
    this.startSpinLoop();
  }

  renderWidget() {
    this.container.innerHTML = `
      <div class="turntable-wrapper" style="background: var(--surface-inner); border: 1px solid var(--card-border); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem; position: relative; overflow: hidden;">
        
        <!-- Turntable Header -->
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1rem; border-bottom: 1px solid var(--card-border); padding-bottom: 0.85rem;">
          <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, var(--cyan), var(--indigo)); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 0 12px var(--cyan-glow);">
              🌐
            </div>
            <div>
              <div style="font-size: 1.05rem; font-weight: 800; color: var(--text-main); letter-spacing: -0.01em; display: flex; align-items: center; gap: 8px;">
                <span>3D Volumetric Spinning Hand</span>
                <span style="font-size: 0.65rem; background: rgba(6, 182, 212, 0.15); border: 1px solid var(--cyan); color: var(--cyan); padding: 2px 6px; border-radius: 9999px; font-weight: 800;">
                  60 FPS ORBIT
                </span>
              </div>
              <div style="font-size: 0.76rem; color: var(--text-muted);">
                Adobe Substance 3D spatial turntable &bull; 3-Layer stereoscopic depth &bull; Range of Motion (ROM) kinematics
              </div>
            </div>
          </div>
          
          <!-- Quick Presets -->
          <div style="display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;">
            <button type="button" class="btn-tt-preset" data-azim="0" data-elev="10" title="Receptive / Viewer Perspective (0°)">👁️ Receptive (0°)</button>
            <button type="button" class="btn-tt-preset" data-azim="45" data-elev="18" title="3/4 Depth Oblique (45°)">📐 3/4 Depth (45°)</button>
            <button type="button" class="btn-tt-preset" data-azim="90" data-elev="5" title="Radial Profile (90°)">🔍 Radial (90°)</button>
            <button type="button" class="btn-tt-preset" data-azim="180" data-elev="25" title="Expressive / Signer Look-Down (180°)">🙌 Signer (180°)</button>
            <button type="button" class="btn-tt-preset" id="btnAutoSpin" style="background: rgba(16, 185, 129, 0.15); border-color: #10b981; color: #10b981; font-weight: 800;">
              ⏸ Pause 3D Spin
            </button>
          </div>
        </div>

        <!-- Main Workspace: Stage Canvas + Kinematic Telemetry Panel -->
        <div style="display: grid; grid-template-columns: 1fr 340px; gap: 1.25rem; align-items: start;" id="ttGridWrap">
          
          <!-- Left: 3D Stage Viewport (Perspective 1200px) -->
          <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
            <div id="ttViewport" style="width: 100%; height: 380px; background: radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.5) 0%, rgba(7, 11, 18, 0.98) 80%); border: 1px solid var(--card-border); border-radius: 12px; position: relative; cursor: grab; display: flex; align-items: center; justify-content: center; user-select: none; overflow: hidden; perspective: 1200px; box-shadow: inset 0 0 40px rgba(0,0,0,0.8);">
              
              <!-- Subtle Holographic 3D Ring Grid on Stage Floor -->
              <svg style="position: absolute; bottom: 15px; width: 280px; height: 90px; opacity: 0.45; pointer-events: none;" viewBox="0 0 200 65">
                <ellipse cx="100" cy="32" rx="90" ry="25" fill="none" stroke="var(--cyan)" stroke-width="1.6" stroke-dasharray="4,4" />
                <ellipse cx="100" cy="32" rx="60" ry="17" fill="none" stroke="#10b981" stroke-width="1.2" stroke-dasharray="3,3" />
                <ellipse cx="100" cy="32" rx="30" ry="8" fill="none" stroke="var(--card-border)" stroke-width="0.8" />
                <line x1="10" y1="32" x2="190" y2="32" stroke="var(--cyan)" stroke-width="0.8" opacity="0.6" />
                <line x1="100" y1="7" x2="100" y2="57" stroke="var(--cyan)" stroke-width="0.8" opacity="0.6" />
                <circle cx="100" cy="32" r="3" fill="var(--cyan)" />
              </svg>

              <!-- 3D Transform Carousel Gimbal (Volumetric Stereoscopic Hand) -->
              <div id="ttHandGimbal" style="width: 240px; height: 280px; position: relative; transform-style: preserve-3d; transition: transform 0.04s linear;">
                
                <!-- LAYER 1: Front Coronal Skin & Silhouette (+26px) -->
                <div id="ttLayerFront" style="position: absolute; inset: 0; transform: translateZ(26px); pointer-events: none; display: flex; align-items: center; justify-content: center; filter: drop-shadow(0 4px 16px rgba(0,0,0,0.6));">
                  <!-- Injected SVG -->
                </div>

                <!-- LAYER 2: Core Osteological Skeleton & ROM Telemetry Rings (0px) -->
                <div id="ttLayerMid" style="position: absolute; inset: 0; transform: translateZ(0px); pointer-events: none; display: flex; align-items: center; justify-content: center;">
                  <!-- Injected Skeletal Elements -->
                </div>

                <!-- LAYER 3: Deep Tendon Pulleys & Monospace Matrix (-26px) -->
                <div id="ttLayerBack" style="position: absolute; inset: 0; transform: translateZ(-26px); pointer-events: none; display: flex; align-items: center; justify-content: center; opacity: 0.55;">
                  <!-- Injected Deep Tendon Tracks -->
                </div>

              </div>

              <!-- Top Left: Angle Compass Badge -->
              <div id="ttCompassBadge" style="position: absolute; top: 12px; left: 12px; background: rgba(9, 13, 22, 0.88); border: 1px solid var(--card-border); border-radius: 6px; padding: 4px 9px; font-size: 0.72rem; font-family: monospace; color: var(--cyan); display: flex; align-items: center; gap: 6px; backdrop-filter: blur(8px);">
                <span>🧭</span>
                <span id="compassText">Azim: 0° | Elev: 12°</span>
              </div>

              <!-- Top Right: Perspective Status Badge -->
              <div id="ttPerspectiveBadge" style="position: absolute; top: 12px; right: 12px; background: rgba(9, 13, 22, 0.88); border: 1px solid var(--card-border); border-radius: 6px; padding: 4px 9px; font-size: 0.72rem; font-weight: 700; color: var(--text-main); backdrop-filter: blur(8px);">
                👁️ Receptive (Viewer)
              </div>

              <!-- Bottom Overlay Hint -->
              <div style="position: absolute; bottom: 12px; left: 14px; font-size: 0.68rem; color: var(--text-muted); pointer-events: none;">
                🖱️ DRAG TO SPIN IN 3D &bull; SCROLL TO ZOOM &bull; CLICK ANY SIGN TO LOAD
              </div>
            </div>

            <!-- Orbital Sliders Bar -->
            <div style="width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.85rem;">
              <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: var(--text-muted); margin-bottom: 2px;">
                  <span>Azimuth Orbit (360° Horizontal)</span>
                  <span id="lblAzim" style="color: var(--cyan); font-weight: 700;">0°</span>
                </div>
                <input type="range" id="sliderAzim" min="0" max="360" value="0" style="width: 100%; accent-color: var(--cyan);">
              </div>
              <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.74rem; color: var(--text-muted); margin-bottom: 2px;">
                  <span>Elevation Tilt (-30° to +60° Vertical)</span>
                  <span id="lblElev" style="color: var(--cyan); font-weight: 700;">12°</span>
                </div>
                <input type="range" id="sliderElev" min="-30" max="60" value="12" style="width: 100%; accent-color: var(--cyan);">
              </div>
            </div>
          </div>

          <!-- Right: Kinematic Range of Motion (ROM) Telemetry Panel -->
          <div style="background: rgba(13, 21, 34, 0.6); border: 1px solid var(--card-border); border-radius: 10px; padding: 1.1rem; display: flex; flex-direction: column; gap: 0.9rem;">
            
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="font-size: 0.85rem; font-weight: 800; color: var(--text-main); text-transform: uppercase; letter-spacing: 0.05em;">
                Digit Kinematics (ROM)
              </div>
              <label style="display: flex; align-items: center; gap: 4px; font-size: 0.74rem; color: var(--cyan); cursor: pointer;">
                <input type="checkbox" id="chkShowROM" checked style="accent-color: var(--cyan);">
                Overlay
              </label>
            </div>

            <!-- Active Letter Selector Pill Bar -->
            <div>
              <div style="font-size: 0.72rem; color: var(--text-muted); margin-bottom: 4px;">Inspect Character Sign:</div>
              <div id="ttLetterBar" style="display: flex; gap: 4px; flex-wrap: wrap; max-height: 76px; overflow-y: auto; padding-bottom: 4px;"></div>
            </div>

            <!-- Joint Angular Degrees of Freedom (DoF) Grid -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px;">
              <div style="background: var(--surface-inner); border: 1px solid var(--card-border); border-radius: 6px; padding: 6px; text-align: center;">
                <div style="font-size: 0.65rem; color: var(--text-muted);">MCP Hinge</div>
                <div id="valMCP" style="font-size: 1.05rem; font-weight: 800; color: var(--cyan);">90°</div>
                <div style="font-size: 0.58rem; color: var(--text-muted);">0°–90°</div>
              </div>
              <div style="background: var(--surface-inner); border: 1px solid var(--card-border); border-radius: 6px; padding: 6px; text-align: center;">
                <div style="font-size: 0.65rem; color: var(--text-muted);">PIP Mid-Bend</div>
                <div id="valPIP" style="font-size: 1.05rem; font-weight: 800; color: var(--amber);">105°</div>
                <div style="font-size: 0.58rem; color: var(--text-muted);">0°–110°</div>
              </div>
              <div style="background: var(--surface-inner); border: 1px solid var(--card-border); border-radius: 6px; padding: 6px; text-align: center;">
                <div style="font-size: 0.65rem; color: var(--text-muted);">DIP Tip Curl</div>
                <div id="valDIP" style="font-size: 1.05rem; font-weight: 800; color: var(--rose);">80°</div>
                <div style="font-size: 0.58rem; color: var(--text-muted);">0°–80°</div>
              </div>
            </div>

            <!-- Trajectory & Actuation Instructions -->
            <div style="background: var(--surface-inner); border: 1px solid var(--card-border); border-radius: 6px; padding: 8px 10px;">
              <div style="font-size: 0.7rem; font-weight: 700; color: var(--text-main); margin-bottom: 2px;">
                Kinetic Actuation Trajectory:
              </div>
              <div id="txtMotionArc" style="font-size: 0.74rem; color: var(--text-muted); line-height: 1.4;">
                Flex at MCP, tight curl across PIP/DIP, pollex adducts flush against index radial wall.
              </div>
            </div>

            <!-- Comfort & Fatigue Index -->
            <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 6px; padding: 6px 10px;">
              <div>
                <div style="font-size: 0.68rem; color: var(--text-muted);">Ergonomic Comfort Index:</div>
                <div id="valComfort" style="font-size: 0.85rem; font-weight: 800; color: #10b981;">96% &bull; Low Strain</div>
              </div>
              <span style="font-size: 1.3rem;">🫱</span>
            </div>

          </div>

        </div>

      </div>
    `;
  }

  bindEvents() {
    const vp = document.getElementById('ttViewport');
    const sliderAzim = document.getElementById('sliderAzim');
    const sliderElev = document.getElementById('sliderElev');
    const btnAutoSpin = document.getElementById('btnAutoSpin');
    const chkShowROM = document.getElementById('chkShowROM');

    // Populate letter buttons
    const letterBar = document.getElementById('ttLetterBar');
    const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'S', 'T'];
    letters.forEach(char => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'tt-char-pill' + (char === this.currentChar ? ' active' : '');
      btn.style.cssText = 'padding: 3px 7px; font-size: 0.74rem; font-weight: 700; border-radius: 4px; border: 1px solid var(--card-border); background: var(--card-bg); color: var(--text-main); cursor: pointer;';
      btn.textContent = char;
      btn.addEventListener('click', () => {
        this.currentChar = char;
        letterBar.querySelectorAll('.tt-char-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.updateKinematicsUI();
        this.drawTurntable();
      });
      letterBar.appendChild(btn);
    });

    // Azimuth slider
    sliderAzim.addEventListener('input', () => {
      this.azimuth = parseInt(sliderAzim.value, 10);
      document.getElementById('lblAzim').textContent = `${this.azimuth}°`;
      this.updateCompass();
      this.drawTurntable();
    });

    // Elevation slider
    sliderElev.addEventListener('input', () => {
      this.elevation = parseInt(sliderElev.value, 10);
      document.getElementById('lblElev').textContent = `${this.elevation}°`;
      this.updateCompass();
      this.drawTurntable();
    });

    // Preset buttons
    this.container.querySelectorAll('.btn-tt-preset[data-azim]').forEach(btn => {
      btn.addEventListener('click', () => {
        this.stopAutoSpin();
        this.azimuth = parseInt(btn.dataset.azim, 10);
        this.elevation = parseInt(btn.dataset.elev, 10);
        sliderAzim.value = this.azimuth;
        sliderElev.value = this.elevation;
        document.getElementById('lblAzim').textContent = `${this.azimuth}°`;
        document.getElementById('lblElev').textContent = `${this.elevation}°`;
        this.updateCompass();
        this.drawTurntable();
      });
    });

    // Auto-spin button
    btnAutoSpin.addEventListener('click', () => {
      if (this.isAutoSpinning) {
        this.stopAutoSpin();
      } else {
        this.startAutoSpin();
      }
    });

    // ROM Checkbox
    chkShowROM.addEventListener('change', () => {
      this.showROM = chkShowROM.checked;
      this.drawTurntable();
    });

    // Drag-to-rotate in 3D viewport
    vp.addEventListener('pointerdown', (e) => {
      this.isDragging = true;
      this.startX = e.clientX;
      this.startY = e.clientY;
      vp.style.cursor = 'grabbing';
      vp.setPointerCapture(e.pointerId);
    });

    vp.addEventListener('pointermove', (e) => {
      if (!this.isDragging) return;
      const dx = e.clientX - this.startX;
      const dy = e.clientY - this.startY;
      this.startX = e.clientX;
      this.startY = e.clientY;

      this.azimuth = (this.azimuth + dx * 0.75 + 360) % 360;
      this.elevation = Math.max(-30, Math.min(60, this.elevation - dy * 0.4));

      sliderAzim.value = Math.round(this.azimuth);
      sliderElev.value = Math.round(this.elevation);
      document.getElementById('lblAzim').textContent = `${Math.round(this.azimuth)}°`;
      document.getElementById('lblElev').textContent = `${Math.round(this.elevation)}°`;

      this.updateCompass();
      this.drawTurntable();
    });

    vp.addEventListener('pointerup', (e) => {
      if (this.isDragging) {
        this.isDragging = false;
        vp.style.cursor = 'grab';
        try { vp.releasePointerCapture(e.pointerId); } catch (_) {}
      }
    });

    // Wheel to Zoom / Dolly
    vp.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.zoom = Math.max(0.7, Math.min(1.6, this.zoom - e.deltaY * 0.001));
      this.drawTurntable();
    }, { passive: false });
  }

  startSpinLoop() {
    const loop = () => {
      if (this.isAutoSpinning && !this.isDragging) {
        this.azimuth = (this.azimuth + 0.45) % 360;
        const sliderAzim = document.getElementById('sliderAzim');
        const lblAzim = document.getElementById('lblAzim');
        if (sliderAzim) sliderAzim.value = Math.round(this.azimuth);
        if (lblAzim) lblAzim.textContent = `${Math.round(this.azimuth)}°`;
        this.updateCompass();
        this.drawTurntable();
      }
      this.animationFrameId = requestAnimationFrame(loop);
    };
    this.animationFrameId = requestAnimationFrame(loop);
  }

  startAutoSpin() {
    this.isAutoSpinning = true;
    const btn = document.getElementById('btnAutoSpin');
    if (btn) {
      btn.textContent = '⏸ Pause 3D Spin';
      btn.style.background = 'rgba(16, 185, 129, 0.15)';
      btn.style.borderColor = '#10b981';
      btn.style.color = '#10b981';
    }
  }

  stopAutoSpin() {
    this.isAutoSpinning = false;
    const btn = document.getElementById('btnAutoSpin');
    if (btn) {
      btn.textContent = '▶ Resume 3D Spin';
      btn.style.background = 'rgba(6, 182, 212, 0.15)';
      btn.style.borderColor = 'var(--cyan)';
      btn.style.color = 'var(--cyan)';
    }
  }

  updateCompass() {
    const badge = document.getElementById('ttCompassBadge');
    const pBadge = document.getElementById('ttPerspectiveBadge');
    if (badge) {
      document.getElementById('compassText').textContent = `Azim: ${Math.round(this.azimuth)}° | Elev: ${Math.round(this.elevation)}°`;
    }

    if (pBadge) {
      const a = this.azimuth;
      if (a >= 315 || a <= 45) {
        pBadge.textContent = '👁️ Receptive (Viewer POV)';
        pBadge.style.color = 'var(--cyan)';
      } else if (a > 45 && a < 135) {
        pBadge.textContent = '🔍 Radial Profile (Thumb Side)';
        pBadge.style.color = 'var(--amber)';
      } else if (a >= 135 && a <= 225) {
        pBadge.textContent = '🙌 Expressive (Signer Look-Down)';
        pBadge.style.color = '#10b981';
      } else {
        pBadge.textContent = '📐 Ulnar Profile (Pinky Side)';
        pBadge.style.color = 'var(--purple)';
      }
    }
  }

  updateKinematicsUI() {
    const data = ASL_KINEMATICS_DATA[this.currentChar] || {
      name: "Manual Gestural Posture",
      mcp: 75, pip: 80, dip: 60, cmc: 45,
      motionArc: "Actuate intrinsic hand musculature to form distinct digit silhouettes.",
      comfort: 95
    };

    document.getElementById('valMCP').textContent = `${data.mcp}°`;
    document.getElementById('valPIP').textContent = `${data.pip}°`;
    document.getElementById('valDIP').textContent = `${data.dip}°`;
    document.getElementById('txtMotionArc').textContent = data.motionArc;
    document.getElementById('valComfort').textContent = `${data.comfort}% • ${data.comfort > 92 ? 'Optimal Comfort' : 'Moderate Engagement'}`;
  }

  setModel(model) {
    this.currentModel = model;
    this.drawTurntable();
  }

  setChar(char) {
    this.currentChar = char.toUpperCase();
    this.updateKinematicsUI();
    this.drawTurntable();
  }

  drawTurntable() {
    const gimbal = document.getElementById('ttHandGimbal');
    const layerFront = document.getElementById('ttLayerFront');
    const layerMid = document.getElementById('ttLayerMid');
    const layerBack = document.getElementById('ttLayerBack');
    if (!gimbal || !layerFront || !layerMid || !layerBack) return;

    // Fetch base SVG for character & current hand model
    let svgRaw = '';
    if (typeof ASL_MORPH_DATA !== 'undefined' && ASL_MORPH_DATA[this.currentModel] && ASL_MORPH_DATA[this.currentModel][this.currentChar]) {
      svgRaw = ASL_MORPH_DATA[this.currentModel][this.currentChar];
    } else if (typeof ASL_SVG_DATA !== 'undefined' && ASL_SVG_DATA[this.currentChar]) {
      svgRaw = ASL_SVG_DATA[this.currentChar];
    } else {
      svgRaw = `<svg viewBox="0 0 100 120"><text x="50" y="70" font-size="48" text-anchor="middle" fill="var(--cyan)">${this.currentChar}</text></svg>`;
    }

    // LAYER 1: Front Coronal Skin & Nails
    layerFront.innerHTML = svgRaw;

    // LAYER 2: Core Osteological Skeleton & Kinematic Rings
    const kd = ASL_KINEMATICS_DATA[this.currentChar] || { mcp: 80, pip: 90, dip: 70 };
    layerMid.innerHTML = `
      <svg viewBox="0 0 100 120" style="width: 100%; height: 100%;" fill="none" stroke="#10b981" stroke-width="1.5">
        <!-- Metacarpal Ray Bones -->
        <line x1="36" y1="108" x2="33" y2="76" stroke="#10b981" stroke-width="1.2" opacity="0.6" stroke-dasharray="2,2" />
        <line x1="45" y1="108" x2="44" y2="74" stroke="#10b981" stroke-width="1.2" opacity="0.6" stroke-dasharray="2,2" />
        <line x1="55" y1="108" x2="55" y2="74" stroke="#10b981" stroke-width="1.2" opacity="0.6" stroke-dasharray="2,2" />
        <line x1="64" y1="108" x2="66" y2="76" stroke="#10b981" stroke-width="1.2" opacity="0.6" stroke-dasharray="2,2" />

        <!-- Joint Kinematic Rings & Badges -->
        <circle cx="50" cy="74" r="6" stroke="#f59e0b" stroke-width="2" fill="rgba(245, 158, 11, 0.25)" />
        <text x="50" y="76.5" font-size="5" font-weight="900" text-anchor="middle" fill="#f59e0b">${kd.mcp}°</text>

        <circle cx="50" cy="54" r="5" stroke="#06b6d4" stroke-width="2" fill="rgba(6, 182, 212, 0.25)" />
        <text x="50" y="56" font-size="4.5" font-weight="900" text-anchor="middle" fill="#06b6d4">${kd.pip}°</text>

        <circle cx="50" cy="38" r="4.5" stroke="#ec4899" stroke-width="2" fill="rgba(236, 72, 153, 0.25)" />
        <text x="50" y="40" font-size="4.5" font-weight="900" text-anchor="middle" fill="#ec4899">${kd.dip}°</text>

        <!-- Kinetic Trajectory Vector Arc -->
        <path d="M 76 25 C 90 40 88 68 72 78" stroke="#10b981" stroke-width="2.4" stroke-dasharray="3,3" fill="none" />
        <polygon points="70,76 77,80 70,84" fill="#10b981" stroke="none" />
      </svg>
    `;

    // LAYER 3: Deep Tendon Matrix & 600 UPM Monospace Telemetry
    layerBack.innerHTML = `
      <svg viewBox="0 0 100 120" style="width: 100%; height: 100%;" fill="none">
        <!-- Deep Flexor Tendons -->
        <line x1="33" y1="76" x2="33" y2="46" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="1.5,1.5" />
        <line x1="44" y1="74" x2="44" y2="44" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="1.5,1.5" />
        <line x1="55" y1="74" x2="55" y2="45" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="1.5,1.5" />
        <line x1="66" y1="76" x2="66" y2="48" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="1.5,1.5" />

        <!-- 600 UPM Telemetry Grid -->
        <text x="50" y="112" font-size="3.5" font-family="'PocketGull Mono', monospace" fill="#8b5cf6" text-anchor="middle">:: 600 UPM MONO ::</text>
      </svg>
    `;

    // Visibility toggle for ROM layers
    layerMid.style.display = this.showROM ? 'flex' : 'none';
    layerBack.style.display = this.showROM ? 'flex' : 'none';

    // 3D Orbital Transform Application on Gimbal
    const rotY = this.azimuth;
    const rotX = -this.elevation;
    gimbal.style.transform = `scale(${this.zoom}) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
  }
}

// Global initialization helper
let GLOBAL_TURNTABLE = null;
function initASLTurntable(containerId) {
  if (document.getElementById(containerId)) {
    GLOBAL_TURNTABLE = new ASLTurntable(containerId);
  }
}
