(function () {
  'use strict';

  const prefersReducedMotion =
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- Global State ---
  const state = {
    mode: 'animusic', // 'animusic' | 'tim'
    simState: 'edit', // 'edit' | 'run' (TIM mode uses Blueprint 'edit' vs 'run'; Animusic runs continuously)
    text: 'POCKETGULL',
    audioEnabled: true,
    continuous: false,
    theme: 'dark',
    fps: 60,
    goalComplete: false,
    // Animusic parameters
    reso: 0.85,
    bpm: 96,
    timbre: 0, // 0: Marimba, 1: Glockenspiel/Bell, 2: Laser Harp, 3: Resonant String
    gravAnimusic: 0.45,
    scale: 'pentatonic',
    // TIM parameters
    gravTim: 1.0,
    restitution: 0.70,
    friction: 0.08,
    gearRpm: 60,
    timPreset: 'dosage',
    // Interactive simulation entities
    balls: [],
    glyphs: [],
    dominoes: [],
    seesaws: [],
    gears: [],
    ramps: [],
    bumpers: [],
    fans: [],
    targetBells: [],
    emitter: null,
    impactRipples: [],
    selectedPart: null,
    dragState: null,
    lastBallTime: 0,
    lastFrameTime: performance.now(),
    simAccumulator: 0,
    lastHudUpdate: 0,
    fpsAccumulator: 0,
    fpsFrames: 0
  };

  // Scales in Hz (Middle Octave Anchors)
  const SCALES = {
    pentatonic: [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 783.99, 880.00, 1046.50],
    dorian:     [261.63, 293.66, 311.13, 349.23, 392.00, 440.00, 466.16, 523.25, 587.33, 622.25, 698.46],
    lydian:     [261.63, 293.66, 329.63, 369.99, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 739.99],
    maqam:      [261.63, 277.18, 329.63, 349.23, 392.00, 415.30, 493.88, 523.25, 554.37, 659.25, 698.46],
    vitals:     [130.81, 164.81, 196.00, 246.94, 261.63, 329.63, 392.00, 493.88, 523.25, 659.25, 783.99]
  };

  const TIM_PRESET_CONFIG = {
    dosage:  { text: '500MG',   grav: 1.0, rest: 0.68, fric: 0.04, gear: 60 },
    cascade: { text: 'FALL',    grav: 1.1, rest: 0.72, fric: 0.04, gear: 70 },
    seesaw:  { text: 'VITAL72', grav: 0.9, rest: 0.68, fric: 0.04, gear: 50 },
    funnel:  { text: '0̸0̸0̸',     grav: 1.2, rest: 0.74, fric: 0.03, gear: 90 },
    arabic:  { text: 'شِفَاء',  grav: 1.0, rest: 0.70, fric: 0.04, gear: 60, scale: 'maqam' }
  };

  // --- Safe DOM Helpers (Zero innerHTML) ---
  function setButtonIconLabel(btn, iconText, labelText) {
    if (!btn) return;
    btn.textContent = '';
    const iconSpan = document.createElement('span');
    iconSpan.textContent = iconText;
    btn.appendChild(iconSpan);
    btn.appendChild(document.createTextNode(' ' + labelText));
  }

  function setInfoCardContent(el, leadText, bodyText) {
    if (!el) return;
    el.textContent = '';
    const strong = document.createElement('strong');
    strong.textContent = leadText;
    el.appendChild(strong);
    el.appendChild(document.createTextNode(' ' + bodyText));
  }

  function getThemeColor(cssVar, fallback) {
    const val = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim();
    return val || fallback;
  }

  // --- WebAudio Physical-Modeling Engine ---
  let audioCtx = null;
  let masterGain = null;
  let analyser = null;
  let scopeDataArray = null;

  function initAudio() {
    if (audioCtx) {
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      return;
    }
    try {
      const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextCtor) return;
      audioCtx = new AudioContextCtor();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 128;
      scopeDataArray = new Uint8Array(analyser.frequencyBinCount);

      masterGain = audioCtx.createGain();
      masterGain.gain.setValueAtTime(0.3, audioCtx.currentTime);

      masterGain.connect(analyser);
      analyser.connect(audioCtx.destination);
    } catch (e) {
      console.warn('WebAudio not available', e);
    }
  }

  function playAnimusicChime(freq, velocity = 0.8) {
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const now = audioCtx.currentTime;
    const dur = Math.max(0.2, state.reso * 2.8);
    const vel = Math.max(0.05, Math.min(1, velocity));

    if (state.timbre === 0) {
      const carrier = audioCtx.createOscillator();
      const modulator = audioCtx.createOscillator();
      const modGain = audioCtx.createGain();
      const carrierGain = audioCtx.createGain();

      carrier.type = 'sine';
      carrier.frequency.setValueAtTime(freq, now);

      modulator.type = 'triangle';
      modulator.frequency.setValueAtTime(freq * 3.84, now);

      modGain.gain.setValueAtTime(freq * 1.5 * vel, now);
      modGain.gain.exponentialRampToValueAtTime(0.01, now + 0.08);

      modulator.connect(modGain);
      modGain.connect(carrier.frequency);

      carrierGain.gain.setValueAtTime(0.5 * vel, now);
      carrierGain.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.7);

      carrier.connect(carrierGain);
      carrierGain.connect(masterGain);

      carrier.start(now);
      modulator.start(now);
      carrier.stop(now + dur);
      modulator.stop(now + dur);
    } else if (state.timbre === 1) {
      const partials = [1.0, 2.76, 5.40, 8.93];
      const weights = [0.6, 0.35, 0.15, 0.08];

      partials.forEach((mult, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq * mult, now);

        gain.gain.setValueAtTime(weights[i] * vel * 0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + dur * (1.2 / (i + 1)));

        osc.connect(gain);
        gain.connect(masterGain);

        osc.start(now);
        osc.stop(now + dur * 1.5);
      });
    } else if (state.timbre === 2) {
      const osc = audioCtx.createOscillator();
      const filter = audioCtx.createBiquadFilter();
      const gain = audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq * 1.8, now);
      osc.frequency.exponentialRampToValueAtTime(freq, now + 0.04);

      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(freq * 2, now);
      filter.Q.setValueAtTime(8, now);

      gain.gain.setValueAtTime(0.4 * vel, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + dur * 0.5);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + dur * 0.6);
    } else {
      const osc = audioCtx.createOscillator();
      const filter = audioCtx.createBiquadFilter();
      const gain = audioCtx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq / 2, now);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(freq * 4, now);
      filter.frequency.exponentialRampToValueAtTime(freq, now + dur);

      gain.gain.setValueAtTime(0.6 * vel, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + dur);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + dur);
    }
  }

  function playTimFoley(type = 'bounce', intensity = 0.5) {
    if (!state.audioEnabled) return;
    initAudio();
    if (!audioCtx) return;

    const now = audioCtx.currentTime;
    const amp = Math.max(0.05, Math.min(1, intensity));

    if (type === 'bounce') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const pitch = 580 + Math.random() * 240;

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(pitch, now);
      osc.frequency.exponentialRampToValueAtTime(pitch * 0.5, now + 0.03);

      gain.gain.setValueAtTime(0.32 * amp, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);

      osc.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + 0.08);
    } else if (type === 'domino') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const pitch = 1200 + Math.random() * 350;

      osc.type = 'square';
      osc.frequency.setValueAtTime(pitch, now);

      gain.gain.setValueAtTime(0.18 * amp, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.025);

      osc.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + 0.03);
    } else if (type === 'ratchet') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(800 + Math.random() * 100, now);

      gain.gain.setValueAtTime(0.14 * amp, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.02);

      osc.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + 0.025);
    } else if (type === 'seesaw') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(140, now);
      osc.frequency.exponentialRampToValueAtTime(60, now + 0.08);

      gain.gain.setValueAtTime(0.45 * amp, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

      osc.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + 0.14);
    } else if (type === 'bumper') {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(220, now);
      osc.frequency.exponentialRampToValueAtTime(660, now + 0.06);
      osc.frequency.exponentialRampToValueAtTime(340, now + 0.16);

      gain.gain.setValueAtTime(0.45 * amp, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);

      osc.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + 0.2);
    } else if (type === 'bell') {
      const chord = [523.25, 659.25, 783.99, 1046.50];
      chord.forEach((f, idx) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const t = now + idx * 0.05;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, t);

        gain.gain.setValueAtTime(0.28 * amp, t);
        gain.gain.exponentialRampToValueAtTime(0.0005, t + 1.1);

        osc.connect(gain);
        gain.connect(masterGain);

        osc.start(t);
        osc.stop(t + 1.15);
      });
    }
  }

  // --- Canvas Setup & High DPI Handling ---
  const canvas = document.getElementById('kineticCanvas');
  const ctx = canvas.getContext('2d');
  let width = 0;
  let height = 0;
  let dpr = 1;

  function resizeCanvas() {
    dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    width = rect.width || 800;
    height = rect.height || 560;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buildLayout();
  }
  window.addEventListener('resize', resizeCanvas);

  function getFloorY() {
    return height - 118;
  }

  function addRipple(x, y, maxRadius, color) {
    if (prefersReducedMotion) return;
    state.impactRipples.push({
      x,
      y,
      radius: 5,
      maxRadius,
      color,
      life: 1.0
    });
  }

  // --- Kinetic Models & Data Structures ---

  class Ball {
    constructor(x, y, vx, vy, radius, isChrome = true) {
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.radius = radius;
      this.isChrome = isChrome;
      this.life = 0;
      this.trailTimer = 0;
      this.color = isChrome ? '#38bdf8' : '#f59e0b';
      this.glow = isChrome ? 'rgba(56, 189, 248, 0.4)' : 'rgba(245, 158, 11, 0.4)';
      this.history = [];
    }

    update(dt) {
      this.life += dt;
      this.trailTimer += dt;

      const g = (state.mode === 'animusic' ? state.gravAnimusic : state.gravTim) * 980;
      this.vy += g * dt;

      // Subtle air damping
      const drag = Math.pow(0.992, dt * 60);
      this.vx *= drag;
      this.vy *= drag;

      // Speed cap to keep solver stable
      const maxSpeed = 1200;
      const speedSq = this.vx * this.vx + this.vy * this.vy;
      if (speedSq > maxSpeed * maxSpeed) {
        const s = maxSpeed / Math.sqrt(speedSq);
        this.vx *= s;
        this.vy *= s;
      }

      this.x += this.vx * dt;
      this.y += this.vy * dt;

      const maxHistory = prefersReducedMotion ? 2 : 8;
      if (this.trailTimer >= 0.025) {
        this.trailTimer = 0;
        this.history.push({ x: this.x, y: this.y });
        if (this.history.length > maxHistory) this.history.shift();
      }

      // Walls
      const rest = state.mode === 'animusic' ? 0.8 : state.restitution;
      if (this.x - this.radius < 0) {
        this.x = this.radius;
        this.vx = Math.abs(this.vx) * rest;
      } else if (this.x + this.radius > width) {
        this.x = width - this.radius;
        this.vx = -Math.abs(this.vx) * rest;
      }

      // Ceiling gentle bounce
      if (this.y - this.radius < 0) {
        this.y = this.radius;
        this.vy = Math.abs(this.vy) * rest;
      }

      // Floor
      const floorY = getFloorY();
      if (this.y + this.radius > floorY) {
        this.y = floorY - this.radius;
        const preVy = this.vy;
        this.vy = -Math.abs(this.vy) * (state.mode === 'animusic' ? 0.75 : rest);
        this.vx *= Math.max(0.85, 1 - state.friction * dt * 30);

        if (Math.abs(preVy) > 55) {
          if (state.mode === 'animusic') {
            playAnimusicChime(220, Math.min(1, Math.abs(preVy) / 500));
          } else {
            playTimFoley('bounce', Math.min(1, Math.abs(preVy) / 500));
          }
        }
      }
    }

    draw(c) {
      if (this.history.length > 1) {
        c.beginPath();
        c.moveTo(this.history[0].x, this.history[0].y);
        for (let i = 1; i < this.history.length; i++) {
          c.lineTo(this.history[i].x, this.history[i].y);
        }
        c.strokeStyle = this.glow;
        c.lineWidth = this.radius * 0.55;
        c.lineCap = 'round';
        c.stroke();
      }

      c.save();
      c.beginPath();
      c.arc(this.x, this.y, this.radius, 0, Math.PI * 2);

      const grad = c.createRadialGradient(
        this.x - this.radius * 0.3,
        this.y - this.radius * 0.3,
        this.radius * 0.1,
        this.x,
        this.y,
        this.radius
      );
      if (this.isChrome) {
        grad.addColorStop(0, '#ffffff');
        grad.addColorStop(0.3, '#bae6fd');
        grad.addColorStop(0.7, '#0284c7');
        grad.addColorStop(1, '#0c4a6e');
      } else {
        grad.addColorStop(0, '#fef08a');
        grad.addColorStop(0.4, '#f59e0b');
        grad.addColorStop(0.8, '#b45309');
        grad.addColorStop(1, '#451a03');
      }

      c.fillStyle = grad;
      c.shadowColor = this.glow;
      c.shadowBlur = 10;
      c.fill();
      c.restore();
    }
  }

  // Typographic Instrument Glyph with Real Offscreen Alpha-Bitmap Collider
  class InstrumentGlyph {
    constructor(char, x, y, size, index) {
      this.char = char;
      this.x = x;
      this.y = y;
      this.size = size;
      this.index = index;
      this.hitTime = 0;
      this.lastAudioTime = 0;
      this.squash = 1.0;
      this.oscillation = 0;

      const activeScale = SCALES[state.scale] || SCALES.pentatonic;
      this.freq = activeScale[index % activeScale.length];

      this.offCanvas = document.createElement('canvas');
      this.offCtx = this.offCanvas.getContext('2d', { willReadFrequently: true });
      this.colW = Math.ceil(this.size * 1.4);
      this.colH = Math.ceil(this.size * 1.4);
      this.alpha = null;
      this.hasInk = false;

      this.buildCollider();
    }

    buildCollider() {
      const fontSpec = `800 ${this.size}px 'PocketGull Bold', 'PocketGull Arabic', 'Noto Sans Arabic', 'PocketGull Mono', 'Segoe UI', sans-serif`;
      this.offCtx.font = fontSpec;
      const metrics = this.offCtx.measureText(this.char);
      const minDim = Math.ceil(this.size * 1.4);
      this.colW = Math.max(minDim, Math.ceil(metrics.width + 20));
      this.colH = minDim;

      this.offCanvas.width = this.colW;
      this.offCanvas.height = this.colH;

      this.offCtx.clearRect(0, 0, this.colW, this.colH);
      this.offCtx.font = fontSpec;
      this.offCtx.textAlign = 'center';
      this.offCtx.textBaseline = 'middle';
      this.offCtx.fillStyle = '#ffffff';
      this.offCtx.fillText(this.char, this.colW / 2, this.colH / 2);

      const img = this.offCtx.getImageData(0, 0, this.colW, this.colH).data;
      const len = this.colW * this.colH;
      this.alpha = new Uint8Array(len);
      let inkFound = false;
      for (let i = 0; i < len; i++) {
        const a = img[i * 4 + 3];
        this.alpha[i] = a;
        if (a > 96) inkFound = true;
      }
      this.hasInk = inkFound;
    }

    sampleSolid(lx, ly) {
      const ix = Math.round(lx);
      const iy = Math.round(ly);
      if (ix < 0 || ix >= this.colW || iy < 0 || iy >= this.colH) return false;
      return this.alpha[iy * this.colW + ix] > 96;
    }

    sampleAlpha(lx, ly) {
      const ix = Math.max(0, Math.min(this.colW - 1, Math.round(lx)));
      const iy = Math.max(0, Math.min(this.colH - 1, Math.round(ly)));
      return this.alpha[iy * this.colW + ix];
    }

    collideBall(ball) {
      if (!this.hasInk || !this.alpha) return false;

      const halfW = this.colW / 2;
      const halfH = this.colH / 2;
      const r = ball.radius;

      // Fast AABB early-out
      if (
        ball.x + r < this.x - halfW ||
        ball.x - r > this.x + halfW ||
        ball.y + r < this.y - halfH ||
        ball.y - r > this.y + halfH
      ) {
        return false;
      }

      const originX = this.x - halfW;
      const originY = this.y - halfH;
      const localBallX = ball.x - originX;
      const localBallY = ball.y - originY;

      let hitCount = 0;
      let outSumX = 0;
      let outSumY = 0;
      let contactSumX = 0;
      let contactSumY = 0;

      // 16 perimeter samples at radius + 8 inner samples at radius*0.55 + center
      const RING_SAMPLES = 16;
      for (let i = 0; i < RING_SAMPLES; i++) {
        const angle = (i * Math.PI * 2) / RING_SAMPLES;
        const cosA = Math.cos(angle);
        const sinA = Math.sin(angle);
        const sx = localBallX + cosA * r;
        const sy = localBallY + sinA * r;
        if (this.sampleSolid(sx, sy)) {
          hitCount++;
          outSumX -= cosA;
          outSumY -= sinA;
          contactSumX += originX + sx;
          contactSumY += originY + sy;
        }
      }

      const INNER_SAMPLES = 8;
      for (let i = 0; i < INNER_SAMPLES; i++) {
        const angle = (i * Math.PI * 2) / INNER_SAMPLES;
        const cosA = Math.cos(angle);
        const sinA = Math.sin(angle);
        const sx = localBallX + cosA * (r * 0.5);
        const sy = localBallY + sinA * (r * 0.5);
        if (this.sampleSolid(sx, sy)) {
          hitCount++;
          outSumX -= cosA;
          outSumY -= sinA;
          contactSumX += originX + sx;
          contactSumY += originY + sy;
        }
      }

      const centerHit = this.sampleSolid(localBallX, localBallY);
      if (hitCount === 0 && !centerHit) return false;

      let nx = outSumX;
      let ny = outSumY;
      let nLen = Math.hypot(nx, ny);

      // Finite-difference alpha gradient fallback when normal cancels symmetrically
      if (nLen < 0.001) {
        const gx = this.sampleAlpha(localBallX - 2, localBallY) - this.sampleAlpha(localBallX + 2, localBallY);
        const gy = this.sampleAlpha(localBallX, localBallY - 2) - this.sampleAlpha(localBallX, localBallY + 2);
        nLen = Math.hypot(gx, gy);
        if (nLen > 0.001) {
          nx = gx / nLen;
          ny = gy / nLen;
        } else {
          const dx = ball.x - this.x;
          const dy = ball.y - this.y;
          const d = Math.hypot(dx, dy) || 1;
          nx = dx / d;
          ny = dy / d;
        }
      } else {
        nx /= nLen;
        ny /= nLen;
      }

      // Push ball along outward normal until surface clears (max 6 micro-steps)
      for (let step = 0; step < 6; step++) {
        const probeX = ball.x - originX + nx * (r * 0.85);
        const probeY = ball.y - originY + ny * (r * 0.85);
        const frontBlocked = this.sampleSolid(ball.x - originX - nx * (r * 0.85), ball.y - originY - ny * (r * 0.85));
        const centerBlocked = this.sampleSolid(ball.x - originX, ball.y - originY);
        if (!centerBlocked && !frontBlocked && step > 0) break;
        ball.x += nx * 1.6;
        ball.y += ny * 1.6;
        if (!this.sampleSolid(probeX, probeY) && !centerBlocked && !frontBlocked) break;
      }

      const dot = ball.vx * nx + ball.vy * ny;
      if (dot < 0) {
        const rest = state.mode === 'animusic' ? 0.94 : state.restitution;
        ball.vx = (ball.vx - 2 * dot * nx) * rest;
        ball.vy = (ball.vy - 2 * dot * ny) * rest;

        // Tangential friction when rolling along glyph strokes
        if (state.mode === 'tim') {
          const tx = -ny;
          const ty = nx;
          const tanVel = ball.vx * tx + ball.vy * ty;
          ball.vx -= tx * tanVel * (state.friction * 0.35);
          ball.vy -= ty * tanVel * (state.friction * 0.35);
        }

        const impactVelocity = Math.hypot(ball.vx, ball.vy);
        if (Math.abs(dot) > 22) {
          const cx = hitCount > 0 ? contactSumX / hitCount : ball.x;
          const cy = hitCount > 0 ? contactSumY / hitCount : ball.y;
          this.triggerHit(cx, cy, nx, ny, impactVelocity);
        }
      }
      return true;
    }

    triggerHit(hitX, hitY, normalX, normalY, velocity) {
      const now = performance.now();
      this.hitTime = now;
      this.squash = prefersReducedMotion ? 0.96 : 0.86;

      if (now - this.lastAudioTime < 45) return;
      this.lastAudioTime = now;

      if (state.mode === 'animusic') {
        playAnimusicChime(this.freq, Math.min(1, velocity / 400));
        addRipple(hitX, hitY, 40 + velocity / 15, '#38bdf8');
      } else {
        playTimFoley('bounce', Math.min(1, velocity / 400));
        addRipple(hitX, hitY, 34, '#f59e0b');
      }
    }

    update() {
      const timeSinceHit = (performance.now() - this.hitTime) / 1000;
      if (timeSinceHit < 1.0) {
        const decay = Math.exp(-timeSinceHit * 5);
        const amp = prefersReducedMotion ? 0.03 : 0.14;
        this.oscillation = Math.sin(timeSinceHit * 40) * decay * amp;
        this.squash = 1.0 + this.oscillation;
      } else {
        this.squash = 1.0;
        this.oscillation = 0;
      }
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);

      const sx = 1.0 / this.squash;
      const sy = this.squash;
      c.scale(sx, sy);

      const isGlowing = performance.now() - this.hitTime < 350;

      c.font = `800 ${this.size}px 'PocketGull Bold', 'PocketGull Arabic', 'Noto Sans Arabic', 'PocketGull Mono', 'Segoe UI', sans-serif`;
      c.textAlign = 'center';
      c.textBaseline = 'middle';

      if (state.mode === 'animusic') {
        if (isGlowing) {
          c.shadowColor = '#38bdf8';
          c.shadowBlur = 24;
          c.fillStyle = '#ffffff';
        } else {
          c.fillStyle = getThemeColor('--text-main', 'rgba(248, 250, 252, 0.88)');
        }
      } else {
        if (isGlowing) {
          c.shadowColor = '#f59e0b';
          c.shadowBlur = 20;
          c.fillStyle = '#ffffff';
        } else {
          c.fillStyle = getThemeColor('--amber', 'rgba(245, 158, 11, 0.9)');
        }
      }

      c.fillText(this.char, 0, 0);

      if (state.mode === 'animusic' && isGlowing && !prefersReducedMotion) {
        c.strokeStyle = 'rgba(56, 189, 248, 0.6)';
        c.lineWidth = 2;
        c.beginPath();
        c.moveTo(-this.size * 0.4, 0);
        c.lineTo(this.size * 0.4, 0);
        c.stroke();
      }

      c.restore();

      // Subtle Blueprint contour indicator in TIM edit mode
      if (state.mode === 'tim' && state.simState === 'edit') {
        c.save();
        c.strokeStyle = 'rgba(245, 158, 11, 0.14)';
        c.setLineDash([4, 4]);
        c.strokeRect(this.x - this.colW / 2, this.y - this.colH / 2, this.colW, this.colH);
        c.restore();
      }
    }
  }

  // TIM Domino Block Object (supports +1 right-leaning or -1 left-leaning RTL cascade)
  class Domino {
    constructor(x, y, w, h, dir = 1) {
      this.x = x;
      this.y = y; // top edge when upright; pivot base is y + h
      this.w = w;
      this.h = h;
      this.dir = dir;
      this.angle = 0;
      this.angularVelocity = 0;
      this.toppled = false;
    }

    reset() {
      this.angle = 0;
      this.angularVelocity = 0;
      this.toppled = false;
    }

    update(dt) {
      const targetMax = (Math.PI / 2.6) * this.dir;
      if (this.toppled) {
        if (this.dir > 0 && this.angle < targetMax) {
          this.angularVelocity += 15 * dt;
          this.angle += this.angularVelocity * dt;
          if (this.angle >= targetMax) {
            this.angle = targetMax;
            this.angularVelocity = 0;
          }
        } else if (this.dir < 0 && this.angle > targetMax) {
          this.angularVelocity -= 15 * dt;
          this.angle += this.angularVelocity * dt;
          if (this.angle <= targetMax) {
            this.angle = targetMax;
            this.angularVelocity = 0;
          }
        }
      }
    }

    trip(forceDir) {
      if (!this.toppled) {
        if (forceDir === 1 || forceDir === -1) this.dir = forceDir;
        this.toppled = true;
        this.angularVelocity = 2.8 * this.dir;
        playTimFoley('domino', 0.8);
      }
    }

    getTipPosition() {
      const pivotY = this.y + this.h;
      return {
        x: this.x + Math.sin(this.angle) * this.h,
        y: pivotY - Math.cos(this.angle) * this.h
      };
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y + this.h);
      c.rotate(this.angle);

      c.fillStyle = this.toppled ? '#b45309' : '#f59e0b';
      c.strokeStyle = '#78350f';
      c.lineWidth = 2;

      c.beginPath();
      c.roundRect(-this.w / 2, -this.h, this.w, this.h, 3);
      c.fill();
      c.stroke();

      c.fillStyle = '#ffffff';
      c.beginPath();
      c.arc(0, -this.h / 2, 2.5, 0, Math.PI * 2);
      c.fill();

      c.restore();
    }
  }

  // TIM Seesaw Fulcrum Object (Draggable & Rotatable in Blueprint mode)
  class Seesaw {
    constructor(x, y, length, initialAngle = -0.15) {
      this.type = 'seesaw';
      this.x = x;
      this.y = y;
      this.length = length;
      this.initialAngle = initialAngle;
      this.angle = initialAngle;
      this.angularVelocity = 0;
      this.rotatable = true;
    }

    reset() {
      this.angle = this.initialAngle;
      this.angularVelocity = 0;
    }

    rotateBy(deltaRad) {
      const limit = Math.PI / 5;
      this.initialAngle = Math.max(-limit, Math.min(limit, this.initialAngle + deltaRad));
      this.angle = this.initialAngle;
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= Math.max(40, this.length * 0.52) && Math.abs(py - this.y) <= 28;
    }

    update(dt) {
      this.angularVelocity *= Math.pow(0.95, dt * 60);
      this.angle += this.angularVelocity * dt;

      const limit = Math.PI / 5;
      if (this.angle > limit) {
        this.angle = limit;
        if (Math.abs(this.angularVelocity) > 0.5) playTimFoley('seesaw', 0.6);
        this.angularVelocity = -this.angularVelocity * 0.2;
      } else if (this.angle < -limit) {
        this.angle = -limit;
        if (Math.abs(this.angularVelocity) > 0.5) playTimFoley('seesaw', 0.6);
        this.angularVelocity = -this.angularVelocity * 0.2;
      }
    }

    draw(c) {
      c.save();
      c.fillStyle = '#64748b';
      c.beginPath();
      c.moveTo(this.x, this.y);
      c.lineTo(this.x - 14, this.y + 24);
      c.lineTo(this.x + 14, this.y + 24);
      c.closePath();
      c.fill();

      c.translate(this.x, this.y);
      c.rotate(this.angle);

      c.fillStyle = '#f59e0b';
      c.strokeStyle = '#92400e';
      c.lineWidth = 2;
      c.beginPath();
      c.roundRect(-this.length / 2, -5, this.length, 10, 4);
      c.fill();
      c.stroke();
      c.restore();
    }
  }

  // TIM Rotating Spur Gear (Idle ratchet spam removed; plays only on ball engagement or click)
  class Gear {
    constructor(x, y, radius, teeth = 8, direction = 1, speedRatio = 1.0) {
      this.type = 'gear';
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.teeth = teeth;
      this.direction = direction;
      this.speedRatio = speedRatio;
      this.angle = 0;
      this.angularVelocity = 0;
      this.pulsing = 0;
      this.isMotor = direction === 1;
      this.rotatable = true;
    }

    rotateBy() {
      // Flip coupled gear train parity when rotated/toggled in edit mode
      flipGearTrainParity();
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= this.radius + 15;
    }

    update(dt) {
      const rps = (state.gearRpm / 60) * this.direction * this.speedRatio;
      this.angle += rps * Math.PI * 2 * dt;
      this.angularVelocity = rps * Math.PI * 2;

      if (this.pulsing > 0) {
        this.pulsing = Math.max(0, this.pulsing - dt * 3.5);
      }
    }

    collide(ball) {
      const dx = ball.x - this.x;
      const dy = ball.y - this.y;
      const distSq = dx * dx + dy * dy;
      const effectiveR = this.radius + 8;
      const minDist = effectiveR + ball.radius;

      if (distSq < minDist * minDist) {
        const dist = Math.sqrt(distSq) || 1;
        const nx = dx / dist;
        const ny = dy / dist;

        ball.x = this.x + nx * minDist;
        ball.y = this.y + ny * minDist;

        const tangentSpeed = this.angularVelocity * effectiveR;
        const tx = -ny * tangentSpeed;
        const ty = nx * tangentSpeed;

        const normalVel = ball.vx * nx + ball.vy * ny;
        if (normalVel < 0) {
          ball.vx = ball.vx - 1.7 * normalVel * nx + tx * 0.75;
          ball.vy = ball.vy - 1.7 * normalVel * ny + ty * 0.75;
        } else {
          ball.vx += tx * 0.6;
          ball.vy += ty * 0.6;
        }

        if (this.pulsing < 0.7) {
          playTimFoley('bounce', 0.55);
          playTimFoley('ratchet', 0.55);
          addRipple(ball.x, ball.y, 30, this.isMotor ? '#f59e0b' : '#ec4899');
        }
        this.pulsing = 1.0;
        return true;
      }
      return false;
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);

      if (this.pulsing > 0) {
        c.strokeStyle = `rgba(245, 158, 11, ${this.pulsing * 0.8})`;
        c.lineWidth = 4 + this.pulsing * 6;
        c.beginPath();
        c.arc(0, 0, this.radius + 12, 0, Math.PI * 2);
        c.stroke();
      }

      c.rotate(this.angle);

      const activeColor = this.direction >= 0 ? '#f59e0b' : '#ec4899';
      c.fillStyle = this.direction >= 0 ? 'rgba(245, 158, 11, 0.22)' : 'rgba(236, 72, 153, 0.18)';
      c.strokeStyle = activeColor;
      c.lineWidth = 3;

      c.beginPath();
      c.arc(0, 0, this.radius, 0, Math.PI * 2);
      c.fill();
      c.stroke();

      c.strokeStyle = this.direction >= 0 ? 'rgba(245, 158, 11, 0.5)' : 'rgba(236, 72, 153, 0.5)';
      c.lineWidth = 2;
      for (let s = 0; s < 4; s++) {
        const sa = (s * Math.PI) / 2;
        c.beginPath();
        c.moveTo(-Math.cos(sa) * (this.radius - 4), -Math.sin(sa) * (this.radius - 4));
        c.lineTo(Math.cos(sa) * (this.radius - 4), Math.sin(sa) * (this.radius - 4));
        c.stroke();
      }

      const step = (Math.PI * 2) / this.teeth;
      for (let i = 0; i < this.teeth; i++) {
        const a = i * step;
        const tx = Math.cos(a) * (this.radius + 6);
        const ty = Math.sin(a) * (this.radius + 6);
        c.fillStyle = this.direction >= 0 ? '#b45309' : '#be185d';
        c.beginPath();
        c.arc(tx, ty, 5, 0, Math.PI * 2);
        c.fill();
        c.stroke();
      }

      c.fillStyle = '#0f172a';
      c.strokeStyle = '#ffffff';
      c.lineWidth = 2;
      c.beginPath();
      c.arc(0, 0, 8, 0, Math.PI * 2);
      c.fill();
      c.stroke();

      c.fillStyle = '#f8fafc';
      c.beginPath();
      c.arc(0, 0, 3, 0, Math.PI * 2);
      c.fill();

      c.restore();
    }
  }

  // Part 1: Ramp (Angled brass/wood chute)
  class Ramp {
    constructor(x, y, length = 170, angle = 0.28) {
      this.type = 'ramp';
      this.x = x;
      this.y = y;
      this.length = length;
      this.angle = angle;
      this.thickness = 10;
      this.rotatable = true;
    }

    rotateBy(deltaRad) {
      this.angle += deltaRad;
    }

    getEndpoints() {
      const half = this.length / 2;
      const cosA = Math.cos(this.angle);
      const sinA = Math.sin(this.angle);
      return {
        x1: this.x - half * cosA,
        y1: this.y - half * sinA,
        x2: this.x + half * cosA,
        y2: this.y + half * sinA
      };
    }

    hitTest(px, py) {
      const { x1, y1, x2, y2 } = this.getEndpoints();
      const dx = x2 - x1;
      const dy = y2 - y1;
      const lenSq = dx * dx + dy * dy || 1;
      const t = Math.max(0, Math.min(1, ((px - x1) * dx + (py - y1) * dy) / lenSq));
      const nx = x1 + t * dx;
      const ny = y1 + t * dy;
      return Math.hypot(px - nx, py - ny) <= 18;
    }

    collide(ball, dt) {
      const { x1, y1, x2, y2 } = this.getEndpoints();
      const dx = x2 - x1;
      const dy = y2 - y1;
      const lenSq = dx * dx + dy * dy;
      if (lenSq === 0) return false;

      const t = Math.max(0, Math.min(1, ((ball.x - x1) * dx + (ball.y - y1) * dy) / lenSq));
      const nearestX = x1 + t * dx;
      const nearestY = y1 + t * dy;

      const distX = ball.x - nearestX;
      const distY = ball.y - nearestY;
      const minDist = ball.radius + this.thickness / 2;
      const distSq = distX * distX + distY * distY;

      if (distSq < minDist * minDist && distSq > 0.0001) {
        const dist = Math.sqrt(distSq);
        const nx = distX / dist;
        const ny = distY / dist;

        ball.x = nearestX + nx * minDist;
        ball.y = nearestY + ny * minDist;

        const dot = ball.vx * nx + ball.vy * ny;
        if (dot < 0) {
          const bounceRest = Math.abs(dot) < 55 ? 0.12 : state.restitution * 0.72;
          ball.vx = ball.vx - (1 + bounceRest) * dot * nx;
          ball.vy = ball.vy - (1 + bounceRest) * dot * ny;

          // Gentle rolling friction along ramp tangent
          const tx = -ny;
          const ty = nx;
          const tanVel = ball.vx * tx + ball.vy * ty;
          const fricFactor = Math.min(0.25, state.friction * dt * 8);
          ball.vx -= tx * tanVel * fricFactor;
          ball.vy -= ty * tanVel * fricFactor;

          if (Math.abs(dot) > 90) {
            playTimFoley('bounce', Math.min(0.7, Math.abs(dot) / 500));
          }
        }
        return true;
      }
      return false;
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);
      c.rotate(this.angle);

      const grad = c.createLinearGradient(0, -this.thickness / 2, 0, this.thickness / 2);
      grad.addColorStop(0, '#fcd34d');
      grad.addColorStop(0.5, '#d97706');
      grad.addColorStop(1, '#78350f');

      c.fillStyle = grad;
      c.strokeStyle = '#fef3c7';
      c.lineWidth = 1.5;

      c.beginPath();
      c.roundRect(-this.length / 2, -this.thickness / 2, this.length, this.thickness, 5);
      c.fill();
      c.stroke();

      // Brass mounting rivets
      c.fillStyle = '#0f172a';
      [-this.length / 2 + 12, 0, this.length / 2 - 12].forEach((rx) => {
        c.beginPath();
        c.arc(rx, 0, 2.5, 0, Math.PI * 2);
        c.fill();
      });

      c.restore();
    }
  }

  // Part 2: Bumper (High-restitution spring coil)
  class Bumper {
    constructor(x, y, radius = 24) {
      this.type = 'bumper';
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.pulse = 0;
      this.rotatable = false;
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= this.radius + 8;
    }

    update(dt) {
      if (this.pulse > 0) {
        this.pulse = Math.max(0, this.pulse - dt * 4);
      }
    }

    collide(ball) {
      const dx = ball.x - this.x;
      const dy = ball.y - this.y;
      const minDist = this.radius + ball.radius;
      const distSq = dx * dx + dy * dy;

      if (distSq < minDist * minDist) {
        const dist = Math.sqrt(distSq) || 1;
        const nx = dx / dist;
        const ny = dy / dist;

        ball.x = this.x + nx * minDist;
        ball.y = this.y + ny * minDist;

        const dot = ball.vx * nx + ball.vy * ny;
        if (dot < 0) {
          const boost = 1.35;
          ball.vx = (ball.vx - 2 * dot * nx) * boost;
          ball.vy = (ball.vy - 2 * dot * ny) * boost;
          // Ensure noticeable spring pop even on slow contact
          const speed = Math.hypot(ball.vx, ball.vy);
          if (speed < 340) {
            ball.vx += nx * 240;
            ball.vy += ny * 240;
          }
          this.pulse = 1.0;
          playTimFoley('bumper', 0.8);
          addRipple(this.x, this.y, this.radius * 2.2, '#38bdf8');
        }
        return true;
      }
      return false;
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);
      const scale = 1 + this.pulse * 0.22;
      c.scale(scale, scale);

      c.fillStyle = 'rgba(6, 182, 212, 0.22)';
      c.strokeStyle = this.pulse > 0.1 ? '#ffffff' : '#06b6d4';
      c.lineWidth = 3;
      c.beginPath();
      c.arc(0, 0, this.radius, 0, Math.PI * 2);
      c.fill();
      c.stroke();

      c.strokeStyle = '#f59e0b';
      c.lineWidth = 2;
      c.beginPath();
      c.arc(0, 0, this.radius * 0.62, 0, Math.PI * 2);
      c.stroke();

      c.fillStyle = '#fef08a';
      c.beginPath();
      c.arc(0, 0, this.radius * 0.25, 0, Math.PI * 2);
      c.fill();
      c.restore();
    }
  }

  // Part 3: Fan (Directional pneumatic bellows/wind corridor)
  class Fan {
    constructor(x, y, angle = 0, range = 220, strength = 1550) {
      this.type = 'fan';
      this.x = x;
      this.y = y;
      this.angle = angle;
      this.range = range;
      this.strength = strength;
      this.halfWidth = 38;
      this.bladeAngle = 0;
      this.rotatable = true;
    }

    rotateBy(deltaRad) {
      this.angle += deltaRad;
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= 28;
    }

    update(dt) {
      this.bladeAngle += dt * 14;
    }

    applyAirflow(ball, dt) {
      const cosA = Math.cos(this.angle);
      const sinA = Math.sin(this.angle);
      const relX = ball.x - this.x;
      const relY = ball.y - this.y;

      const along = relX * cosA + relY * sinA;
      const perp = -relX * sinA + relY * cosA;

      if (along > 12 && along < this.range && Math.abs(perp) < this.halfWidth + ball.radius) {
        const falloff = 1 - (along / this.range) * 0.45;
        ball.vx += cosA * this.strength * falloff * dt;
        ball.vy += sinA * this.strength * falloff * dt;
      }

      // Solid housing bounce around motor hub
      const hubDist = Math.hypot(relX, relY);
      const minDist = 18 + ball.radius;
      if (hubDist < minDist && hubDist > 0.001) {
        const nx = relX / hubDist;
        const ny = relY / hubDist;
        ball.x = this.x + nx * minDist;
        ball.y = this.y + ny * minDist;
        const dot = ball.vx * nx + ball.vy * ny;
        if (dot < 0) {
          ball.vx = (ball.vx - 2 * dot * nx) * 0.6;
          ball.vy = (ball.vy - 2 * dot * ny) * 0.6;
        }
      }
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);
      c.rotate(this.angle);

      // Wind corridor zone
      const streamGrad = c.createLinearGradient(16, 0, this.range, 0);
      streamGrad.addColorStop(0, 'rgba(56, 189, 248, 0.16)');
      streamGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
      c.fillStyle = streamGrad;
      c.fillRect(16, -this.halfWidth, this.range - 16, this.halfWidth * 2);

      // Animated breeze streaks
      if (!prefersReducedMotion) {
        const phase = (performance.now() * 0.18) % 40;
        c.strokeStyle = 'rgba(186, 230, 253, 0.35)';
        c.lineWidth = 1.5;
        for (let row = -1; row <= 1; row++) {
          const ry = row * 18;
          for (let sx = 24 + phase; sx < this.range - 16; sx += 44) {
            c.beginPath();
            c.moveTo(sx, ry);
            c.lineTo(sx + 16, ry);
            c.stroke();
          }
        }
      }

      // Fan housing
      c.fillStyle = '#1e293b';
      c.strokeStyle = '#38bdf8';
      c.lineWidth = 2.5;
      c.beginPath();
      c.roundRect(-16, -22, 32, 44, 8);
      c.fill();
      c.stroke();

      // Spinning blades
      c.save();
      c.rotate(this.bladeAngle);
      c.strokeStyle = '#e0f2fe';
      c.lineWidth = 3;
      c.beginPath();
      c.moveTo(-10, 0);
      c.lineTo(10, 0);
      c.moveTo(0, -10);
      c.lineTo(0, 10);
      c.stroke();
      c.restore();

      // Nozzle rim
      c.fillStyle = '#38bdf8';
      c.fillRect(14, -20, 4, 40);

      c.restore();
    }
  }

  // Part 4: TargetBell (5:1 Optotype Win Goal Trigger)
  class TargetBell {
    constructor(x, y, radius = 24) {
      this.type = 'bell';
      this.x = x;
      this.y = y;
      this.radius = radius;
      this.triggered = false;
      this.pulse = 0;
      this.rotatable = false;
    }

    reset() {
      this.triggered = false;
      this.pulse = 0;
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= this.radius + 10;
    }

    trigger() {
      if (this.triggered) return;
      this.triggered = true;
      this.pulse = 1.0;
      state.goalComplete = true;
      updateGoalHud();
      playTimFoley('bell', 1.0);
      addRipple(this.x, this.y, 75, '#10b981');
      addRipple(this.x, this.y, 48, '#34d399');
    }

    update(dt) {
      if (this.pulse > 0) {
        this.pulse = Math.max(0, this.pulse - dt * 1.8);
      }
    }

    checkBall(ball) {
      const dist = Math.hypot(ball.x - this.x, ball.y - this.y);
      if (dist <= this.radius + ball.radius) {
        this.trigger();
        return true;
      }
      return false;
    }

    checkDomino(dom) {
      if (!dom.toppled || Math.abs(dom.angle) < 0.45) return false;
      const tip = dom.getTipPosition();
      const dist = Math.hypot(tip.x - this.x, tip.y - this.y);
      if (dist <= this.radius + 14) {
        this.trigger();
        return true;
      }
      return false;
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);
      const scale = 1 + this.pulse * 0.25;
      c.scale(scale, scale);

      // 5:1 Optotype Target Ring
      const outerColor = this.triggered ? '#10b981' : '#f43f5e';
      c.fillStyle = this.triggered ? 'rgba(16, 185, 129, 0.24)' : 'rgba(244, 63, 94, 0.16)';
      c.strokeStyle = outerColor;
      c.lineWidth = 4;
      c.beginPath();
      c.arc(0, 0, this.radius, 0, Math.PI * 2);
      c.fill();
      c.stroke();

      c.strokeStyle = this.triggered ? '#6ee7b7' : '#fda4af';
      c.lineWidth = 2;
      c.beginPath();
      c.arc(0, 0, this.radius * 0.6, 0, Math.PI * 2);
      c.stroke();

      c.fillStyle = this.triggered ? '#ecfdf5' : '#ffe4e6';
      c.beginPath();
      c.arc(0, 0, this.radius * 0.24, 0, Math.PI * 2);
      c.fill();

      c.font = `700 10px 'PocketGull Mono', monospace`;
      c.textAlign = 'center';
      c.fillStyle = this.triggered ? '#34d399' : '#fda4af';
      c.fillText(this.triggered ? 'GOAL ✓' : 'TARGET', 0, -this.radius - 8);

      c.restore();
    }
  }

  // Emitter (Blueprint Drop Hopper)
  class Emitter {
    constructor(x, y, vx = 100, vy = 0) {
      this.type = 'emitter';
      this.x = x;
      this.y = y;
      this.vx = vx;
      this.vy = vy;
      this.rotatable = true;
    }

    rotateBy(deltaRad) {
      const speed = Math.hypot(this.vx, this.vy) || 100;
      const angle = Math.atan2(this.vy, this.vx) + deltaRad;
      this.vx = Math.cos(angle) * speed;
      this.vy = Math.sin(angle) * speed;
    }

    hitTest(px, py) {
      return Math.hypot(px - this.x, py - this.y) <= 24;
    }

    spawnBall() {
      const ball = new Ball(this.x, this.y + 14, this.vx, this.vy, 11, false);
      state.balls.push(ball);
      if (state.balls.length > 25) state.balls.shift();
      addRipple(this.x, this.y + 12, 24, '#f59e0b');
    }

    draw(c) {
      c.save();
      c.translate(this.x, this.y);

      c.fillStyle = '#1e293b';
      c.strokeStyle = '#f59e0b';
      c.lineWidth = 2.5;
      c.beginPath();
      c.moveTo(-16, -14);
      c.lineTo(16, -14);
      c.lineTo(9, 12);
      c.lineTo(-9, 12);
      c.closePath();
      c.fill();
      c.stroke();

      // Launch vector indicator
      const mag = Math.hypot(this.vx, this.vy);
      if (mag > 5) {
        const ux = (this.vx / mag) * 24;
        const uy = (this.vy / mag) * 24;
        c.strokeStyle = 'rgba(245, 158, 11, 0.75)';
        c.lineWidth = 2;
        c.beginPath();
        c.moveTo(0, 14);
        c.lineTo(ux, 14 + uy);
        c.stroke();
      }

      c.font = `700 9px 'PocketGull Mono', monospace`;
      c.textAlign = 'center';
      c.fillStyle = '#fbbf24';
      c.fillText('DROP', 0, -20);

      c.restore();
    }
  }

  // --- Coupled Gear Parity Helper ---
  function flipGearTrainParity() {
    state.gears.forEach((gear) => {
      gear.direction = -gear.direction;
      gear.pulsing = 1.0;
    });
    playTimFoley('ratchet', 0.8);
    if (state.gears[0]) {
      addRipple(state.gears[0].x, state.gears[0].y, state.gears[0].radius * 1.8, '#f59e0b');
    }
  }

  // --- Distinct Solvable TIM Contraption Presets ---
  function buildTimPreset(presetName) {
    const floorY = getFloorY();
    const centerY = height * 0.48;
    const preset = presetName || state.timPreset || 'dosage';

    state.dominoes = [];
    state.seesaws = [];
    state.gears = [];
    state.ramps = [];
    state.bumpers = [];
    state.fans = [];
    state.targetBells = [];
    state.selectedPart = null;
    state.goalComplete = false;

    const firstGlyphX = state.glyphs[0] ? state.glyphs[0].x : width * 0.25;
    const lastGlyphX = state.glyphs[state.glyphs.length - 1] ? state.glyphs[state.glyphs.length - 1].x : width * 0.75;

    if (preset === 'dosage') {
      // 500MG: Emitter -> upper ramp -> glyph contours -> wide catch ramp -> Seesaw -> Dominoes -> TargetBell
      const emX = Math.max(70, firstGlyphX - 50);
      state.emitter = new Emitter(emX, Math.max(70, height * 0.12), 145, 5);
      state.ramps.push(new Ramp(emX + 55, height * 0.23, 160, 0.34));
      state.ramps.push(new Ramp(width * 0.37, floorY - 122, 290, 0.25));
      state.seesaws.push(new Seesaw(width * 0.46, floorY - 44, Math.min(160, width * 0.22), 0.14));

      const domStart = width * 0.56;
      for (let d = 0; d < 7; d++) {
        state.dominoes.push(new Domino(domStart + d * 21, floorY - 38, 8, 38, 1));
      }
      state.targetBells.push(new TargetBell(domStart + 6 * 21 + 30, floorY - 22, 24));
      state.bumpers.push(new Bumper(width * 0.74, centerY - 55, 22));

      const g1X = Math.min(width - 135, Math.max(width * 0.82, lastGlyphX + 40));
      state.gears.push(new Gear(g1X, centerY - 40, 32, 10, 1, 1.0));
      state.gears.push(new Gear(g1X + 54, centerY - 30, 24, 8, -1, 1.333));
    } else if (preset === 'cascade') {
      // FALL: Emitter -> twin chutes + spring bumper -> 8-domino floor cascade -> TargetBell
      const emX = Math.max(80, width * 0.18);
      state.emitter = new Emitter(emX, Math.max(70, height * 0.13), 125, 0);
      state.ramps.push(new Ramp(emX + 65, height * 0.25, 165, 0.36));
      state.bumpers.push(new Bumper(emX + 185, height * 0.38, 22));
      state.ramps.push(new Ramp(width * 0.42, floorY - 120, 240, 0.26));

      const domStart = width * 0.56;
      for (let d = 0; d < 8; d++) {
        state.dominoes.push(new Domino(domStart + d * 21, floorY - 38, 8, 38, 1));
      }
      state.targetBells.push(new TargetBell(domStart + 7 * 21 + 30, floorY - 22, 22));

      state.gears.push(new Gear(width * 0.86, centerY - 60, 28, 9, 1, 1.0));
      state.gears.push(new Gear(width * 0.86 + 48, centerY - 40, 20, 7, -1, 1.333));
    } else if (preset === 'seesaw') {
      // VITAL72: Guide ramp below V-I-T -> Seesaw launch -> pneumatic Fan updraft -> catch Ramp -> TargetBell
      state.emitter = new Emitter(width * 0.18, Math.max(70, height * 0.14), 105, 15);
      state.ramps.push(new Ramp(width * 0.24, height * 0.28, 160, 0.36));
      state.ramps.push(new Ramp(width * 0.25, floorY - 152, 165, 0.30));
      state.seesaws.push(new Seesaw(width * 0.36, floorY - 82, Math.min(180, width * 0.24), 0.14));
      state.fans.push(new Fan(width * 0.50, floorY - 28, -0.42, 270, 1850));
      state.ramps.push(new Ramp(width * 0.75, floorY - 62, 190, 0.20));
      state.targetBells.push(new TargetBell(width * 0.87, floorY - 26, 26));
      state.gears.push(new Gear(width * 0.14, centerY + 30, 26, 8, 1, 1.0));
    } else if (preset === 'funnel') {
      // 0̸0̸0̸: Converging twin funnel ramps -> meshed Gear ejector -> Catch Ramp -> TargetBell
      state.emitter = new Emitter(width * 0.30, Math.max(68, height * 0.11), 120, 10);
      state.ramps.push(new Ramp(width * 0.35, height * 0.22, 160, 0.36));
      state.ramps.push(new Ramp(width * 0.41, floorY - 132, 195, 0.34));

      const gX = width * 0.52;
      const gY = floorY - 82;
      state.gears.push(new Gear(gX, gY, 32, 12, 1, 1.0));
      state.gears.push(new Gear(gX + 54, gY + 10, 22, 9, -1, 1.333));
      state.ramps.push(new Ramp(width * 0.67, floorY - 44, 240, 0.20));
      state.targetBells.push(new TargetBell(width * 0.81, floorY - 22, 28));
    } else if (preset === 'arabic') {
      // شِفَاء (RTL right-to-left cascade): Right emitter -> RTL ramp & Fan -> RTL dominoes -> Left TargetBell
      const emX = Math.min(width - 80, width * 0.82);
      state.emitter = new Emitter(emX, Math.max(68, height * 0.12), -145, 10);
      state.ramps.push(new Ramp(emX - 70, height * 0.23, 180, -0.38));
      state.fans.push(new Fan(width * 0.67, floorY - 96, Math.PI - 0.26, 250, 1650));
      state.ramps.push(new Ramp(width * 0.58, floorY - 72, 265, -0.28));

      const domStart = width * 0.43;
      for (let d = 0; d < 7; d++) {
        state.dominoes.push(new Domino(domStart - d * 21, floorY - 38, 8, 38, -1));
      }
      state.targetBells.push(new TargetBell(domStart - 6 * 21 - 30, floorY - 22, 24));
      state.gears.push(new Gear(width * 0.15, centerY - 25, 28, 9, -1, 1.0));
    }

    updateSelectionUi();
    updateGoalHud();
  }

  // --- Layout Reconstruction ---
  function buildLayout() {
    state.glyphs = [];

    const isRtl = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/.test(state.text);
    const rawText = isRtl
      ? state.text
      : (/^[a-zA-Z0-9\s.,!?:;'\-_\/\\()]+$/.test(state.text) ? state.text.toUpperCase() : state.text);

    let chars = [];
    if (typeof Intl !== 'undefined' && Intl.Segmenter) {
      const segmenter = new Intl.Segmenter(undefined, { granularity: 'grapheme' });
      chars = Array.from(segmenter.segment(rawText)).map((s) => s.segment);
    } else {
      chars = Array.from(rawText);
    }

    const count = chars.length;
    if (count === 0) return;

    const availWidth = Math.max(240, width - 120);
    const glyphSize = Math.max(32, Math.min(80, availWidth / Math.max(count, 4)));
    const startX = (width - count * glyphSize) / 2 + glyphSize / 2;
    const centerY = height * 0.46;

    chars.forEach((ch, i) => {
      const colIndex = isRtl ? count - 1 - i : i;
      const gx = startX + colIndex * glyphSize;
      const gy = centerY + Math.sin(colIndex * 0.5) * 18;
      state.glyphs.push(new InstrumentGlyph(ch, gx, gy, glyphSize, i));
    });

    if (state.mode === 'tim') {
      buildTimPreset(state.timPreset);
    } else {
      state.dominoes = [];
      state.seesaws = [];
      state.gears = [];
      state.ramps = [];
      state.bumpers = [];
      state.fans = [];
      state.targetBells = [];
      state.emitter = null;
      state.selectedPart = null;
      state.goalComplete = false;
    }

    const glyphCountEl = document.getElementById('hudGlyphCount');
    if (glyphCountEl) glyphCountEl.textContent = String(count);
  }

  // Rebuild offscreen alpha colliders once PocketGull webfonts finish loading
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(() => {
      state.glyphs.forEach((g) => g.buildCollider());
    });
  }

  // --- Ballistic Sphere Spawner ---
  function fireBall() {
    initAudio();
    if (state.mode === 'tim') {
      if (state.simState === 'edit') {
        setTimSimState('run');
        return;
      }
      if (state.emitter) {
        state.emitter.spawnBall();
        return;
      }
    }

    const startX = width * 0.2 + Math.random() * width * 0.6;
    const radius = state.mode === 'animusic' ? 7 : 11;
    const isChrome = state.mode === 'animusic';
    const vy = state.mode === 'animusic' ? 50 + Math.random() * 80 : 10 + Math.random() * 40;
    const vx = (Math.random() - 0.5) * 120;

    const ball = new Ball(startX, 30, vx, vy, radius, isChrome);
    state.balls.push(ball);
    if (state.balls.length > 25) state.balls.shift();
  }

  function resetTimSimulation() {
    state.balls = [];
    state.impactRipples = [];
    state.goalComplete = false;
    state.simAccumulator = 0;
    state.dominoes.forEach((d) => d.reset());
    state.seesaws.forEach((s) => s.reset());
    state.targetBells.forEach((b) => b.reset());
    updateGoalHud();
  }

  function setTimSimState(nextState) {
    state.simState = nextState;
    const runStopBtn = document.getElementById('btnRunStop');
    if (nextState === 'run') {
      resetTimSimulation();
      state.selectedPart = null;
      updateSelectionUi();
      if (state.emitter) {
        state.emitter.spawnBall();
      } else {
        fireBall();
      }
      setButtonIconLabel(runStopBtn, '⏹', 'Stop & Reset');
      runStopBtn?.classList.add('running');
    } else {
      resetTimSimulation();
      setButtonIconLabel(runStopBtn, '▶', 'Run Contraption');
      runStopBtn?.classList.remove('running');
    }
    updateGoalHud();
  }

  function updateGoalHud() {
    const goalChip = document.getElementById('hudGoalChip');
    const goalLabel = document.getElementById('hudGoalLabel');
    if (!goalChip || !goalLabel) return;
    if (state.mode !== 'tim') {
      goalChip.classList.add('hidden');
      return;
    }
    goalChip.classList.remove('hidden');
    if (state.goalComplete) {
      goalLabel.textContent = 'COMPLETE ✓';
      goalChip.classList.add('goal-complete');
    } else if (state.simState === 'run') {
      goalLabel.textContent = 'RUNNING';
      goalChip.classList.remove('goal-complete');
    } else {
      goalLabel.textContent = 'BLUEPRINT';
      goalChip.classList.remove('goal-complete');
    }
  }

  function updateSelectionUi() {
    const box = document.getElementById('timSelectionControls');
    const label = document.getElementById('selectedPartLabel');
    const rotLeft = document.getElementById('btnPartRotateLeft');
    const rotRight = document.getElementById('btnPartRotateRight');
    const delBtn = document.getElementById('btnPartDelete');
    if (!box || !label) return;

    if (state.mode !== 'tim' || state.simState !== 'edit' || !state.selectedPart) {
      box.classList.add('hidden');
      return;
    }

    box.classList.remove('hidden');
    const part = state.selectedPart;
    const names = {
      ramp: 'Ramp Chute',
      bumper: 'Spring Bumper',
      fan: 'Pneumatic Fan',
      bell: 'Target Bell',
      seesaw: 'Seesaw Lever',
      gear: 'Spur Gear',
      emitter: 'Marble Emitter'
    };
    let desc = names[part.type] || 'Part';
    if (typeof part.angle === 'number') {
      desc += ` (${Math.round((part.angle * 180) / Math.PI)}°)`;
    }
    label.textContent = desc;

    if (rotLeft) rotLeft.disabled = !part.rotatable;
    if (rotRight) rotRight.disabled = !part.rotatable;
    if (delBtn) delBtn.disabled = part.type === 'emitter';
  }

  function deleteSelectedPart() {
    const part = state.selectedPart;
    if (!part || part.type === 'emitter') return;
    const lists = [state.ramps, state.bumpers, state.fans, state.targetBells, state.seesaws, state.gears];
    lists.forEach((arr) => {
      const idx = arr.indexOf(part);
      if (idx !== -1) arr.splice(idx, 1);
    });
    state.selectedPart = null;
    updateSelectionUi();
  }

  // --- Ball-to-Ball Elastic Collisions ---
  function solveBallToBallCollisions() {
    const n = state.balls.length;
    if (n < 2) return;
    const rest = state.mode === 'animusic' ? 0.92 : state.restitution;

    for (let i = 0; i < n; i++) {
      const a = state.balls[i];
      for (let j = i + 1; j < n; j++) {
        const b = state.balls[j];
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const minDist = a.radius + b.radius;
        const distSq = dx * dx + dy * dy;

        if (distSq < minDist * minDist && distSq > 0.0001) {
          const dist = Math.sqrt(distSq);
          const nx = dx / dist;
          const ny = dy / dist;
          const overlap = (minDist - dist) * 0.5;

          a.x -= nx * overlap;
          a.y -= ny * overlap;
          b.x += nx * overlap;
          b.y += ny * overlap;

          const rvx = b.vx - a.vx;
          const rvy = b.vy - a.vy;
          const velAlongNormal = rvx * nx + rvy * ny;
          if (velAlongNormal < 0) {
            const jImp = (-(1 + rest) * velAlongNormal) * 0.5;
            a.vx -= jImp * nx;
            a.vy -= jImp * ny;
            b.vx += jImp * nx;
            b.vy += jImp * ny;
          }
        }
      }
    }
  }

  // --- Collision Solver ---
  function solveCollisions(dt) {
    state.balls.forEach((ball) => {
      // 1. Real Offscreen Bitmap Glyph Contours
      state.glyphs.forEach((glyph) => {
        glyph.collideBall(ball);
      });

      if (state.mode === 'tim') {
        // 2. Pneumatic Fans (Airflow before rigid impacts)
        state.fans.forEach((fan) => fan.applyAirflow(ball, dt));

        // 3. Ramps
        state.ramps.forEach((ramp) => ramp.collide(ball, dt));

        // 4. Spring Bumpers
        state.bumpers.forEach((bumper) => bumper.collide(ball));

        // 5. Seesaws
        state.seesaws.forEach((seesaw) => {
          const halfL = seesaw.length / 2;
          const cosA = Math.cos(seesaw.angle);
          const sinA = Math.sin(seesaw.angle);

          const p1x = seesaw.x - halfL * cosA;
          const p1y = seesaw.y - halfL * sinA;
          const p2x = seesaw.x + halfL * cosA;
          const p2y = seesaw.y + halfL * sinA;

          const dx = p2x - p1x;
          const dy = p2y - p1y;
          const lenSq = dx * dx + dy * dy || 1;
          const t = Math.max(0, Math.min(1, ((ball.x - p1x) * dx + (ball.y - p1y) * dy) / lenSq));

          const nearestX = p1x + t * dx;
          const nearestY = p1y + t * dy;
          const distX = ball.x - nearestX;
          const distY = ball.y - nearestY;
          const minDist = ball.radius + 5;
          const distSq = distX * distX + distY * distY;

          if (distSq < minDist * minDist && distSq > 0.0001) {
            const dist = Math.sqrt(distSq);
            const nx = distX / dist;
            const ny = distY / dist;

            ball.x = nearestX + nx * minDist;
            ball.y = nearestY + ny * minDist;

            const arm = (t - 0.5) * seesaw.length;
            seesaw.angularVelocity += arm * 0.07 * dt * 60;

            const dot = ball.vx * nx + ball.vy * ny;
            if (dot < 0) {
              ball.vx = (ball.vx - 2 * dot * nx) * state.restitution;
              ball.vy = (ball.vy - 2 * dot * ny) * state.restitution;
              if (Math.abs(dot) > 70) playTimFoley('bounce', 0.45);
            }
          }
        });

        // 6. Dominoes (Ball -> Domino)
        state.dominoes.forEach((dom) => {
          if (
            !dom.toppled &&
            ball.x + ball.radius > dom.x - dom.w &&
            ball.x - ball.radius < dom.x + dom.w &&
            ball.y + ball.radius > dom.y &&
            ball.y - ball.radius < dom.y + dom.h
          ) {
            const pushDir = ball.vx >= 0 ? 1 : -1;
            dom.trip(pushDir);
            ball.vx *= 0.65;
          }
        });

        // 7. Spur Gears
        state.gears.forEach((gear) => gear.collide(ball));

        // 8. Target Bells (Ball -> Target)
        state.targetBells.forEach((bell) => bell.checkBall(ball));
      }
    });

    if (state.mode === 'tim') {
      // Spatial Domino -> Domino chain (supports LTR or RTL cleanly)
      for (let i = 0; i < state.dominoes.length; i++) {
        const curr = state.dominoes[i];
        if (!curr.toppled || Math.abs(curr.angle) <= 0.32) continue;
        for (let j = 0; j < state.dominoes.length; j++) {
          if (i === j) continue;
          const other = state.dominoes[j];
          if (other.toppled) continue;
          const dx = other.x - curr.x;
          if ((curr.dir > 0 && dx > 0 && dx <= 28) || (curr.dir < 0 && dx < 0 && -dx <= 28)) {
            other.trip(curr.dir);
          }
        }
      }

      // Domino -> Target Bell
      state.targetBells.forEach((bell) => {
        state.dominoes.forEach((dom) => bell.checkDomino(dom));
      });
    }

    solveBallToBallCollisions();
  }

  function drawSelectionHalo(c, part) {
    if (!part) return;
    c.save();
    c.strokeStyle = '#38bdf8';
    c.lineWidth = 2;
    c.setLineDash([5, 4]);
    const pad = part.type === 'ramp' ? Math.max(30, part.length * 0.54) : part.type === 'seesaw' ? part.length * 0.54 : (part.radius || 28) + 12;
    const h = part.type === 'ramp' ? 32 : part.type === 'seesaw' ? 36 : pad;
    c.beginPath();
    c.arc(part.x, part.y, Math.max(pad, h), 0, Math.PI * 2);
    c.stroke();
    c.restore();
  }

  // --- Animation & Physics Render Loop ---
  function animate(now) {
    requestAnimationFrame(animate);

    const rawDt = (now - state.lastFrameTime) / 1000;
    const dt = Math.max(0, Math.min(0.05, rawDt));
    state.lastFrameTime = now;

    // Throttled HUD updates (4 Hz instead of 60 Hz)
    state.fpsAccumulator += rawDt;
    state.fpsFrames++;
    if (now - state.lastHudUpdate >= 250) {
      const avgFps = state.fpsAccumulator > 0 ? Math.round(state.fpsFrames / state.fpsAccumulator) : 60;
      state.fps = Math.min(120, Math.max(1, avgFps));
      const hudFps = document.getElementById('hudFps');
      const hudBalls = document.getElementById('hudBallCount');
      if (hudFps) hudFps.textContent = String(state.fps);
      if (hudBalls) hudBalls.textContent = String(state.balls.length);
      state.fpsAccumulator = 0;
      state.fpsFrames = 0;
      state.lastHudUpdate = now;
    }

    // Continuous Spawner
    const canAutoSpawn = state.mode === 'animusic' || state.simState === 'run';
    if (state.continuous && canAutoSpawn) {
      const spawnInterval = (60 / state.bpm) * 1000;
      if (now - state.lastBallTime > spawnInterval) {
        state.lastBallTime = now;
        fireBall();
      }
    }

    // Fixed-timestep Physics & Collision Solver BEFORE rendering (eliminates rAF variance & 1-frame overlap)
    const shouldSimulatePhysics = state.mode === 'animusic' || state.simState === 'run';
    if (shouldSimulatePhysics) {
      const FIXED_DT = 1 / 240;
      const MAX_STEPS = 16;
      state.simAccumulator = Math.min(state.simAccumulator + dt, FIXED_DT * MAX_STEPS);
      let steps = 0;
      while (state.simAccumulator >= FIXED_DT && steps < MAX_STEPS) {
        state.balls.forEach((ball) => ball.update(FIXED_DT));
        if (state.mode === 'tim') {
          state.dominoes.forEach((d) => d.update(FIXED_DT));
          state.seesaws.forEach((sObj) => sObj.update(FIXED_DT));
          state.gears.forEach((g) => g.update(FIXED_DT));
          state.fans.forEach((f) => f.update(FIXED_DT));
          state.bumpers.forEach((b) => b.update(FIXED_DT));
          state.targetBells.forEach((tb) => tb.update(FIXED_DT));
        }
        solveCollisions(FIXED_DT);
        state.simAccumulator -= FIXED_DT;
        steps++;
      }
    } else {
      state.simAccumulator = 0;
    }

    // Update Glyph squash animation
    state.glyphs.forEach((glyph) => glyph.update());

    // Clear Stage
    ctx.clearRect(0, 0, width, height);

    // Subtle Grid (Blueprint grid denser in TIM Edit mode)
    const isTimBlueprint = state.mode === 'tim' && state.simState === 'edit';
    ctx.strokeStyle =
      state.mode === 'animusic'
        ? 'rgba(6, 182, 212, 0.05)'
        : isTimBlueprint
        ? 'rgba(245, 158, 11, 0.09)'
        : 'rgba(245, 158, 11, 0.04)';
    ctx.lineWidth = 1;
    const gridStep = isTimBlueprint ? 32 : 40;
    ctx.beginPath();
    for (let x = 0; x < width; x += gridStep) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
    }
    for (let y = 0; y < height; y += gridStep) {
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
    }
    ctx.stroke();

    // Stage Floor Track
    const floorY = getFloorY();
    ctx.fillStyle = state.mode === 'animusic' ? 'rgba(6, 182, 212, 0.1)' : 'rgba(245, 158, 11, 0.1)';
    ctx.strokeStyle = state.mode === 'animusic' ? 'rgba(6, 182, 212, 0.4)' : 'rgba(245, 158, 11, 0.4)';
    ctx.lineWidth = 2;
    ctx.fillRect(0, floorY, width, height - floorY);
    ctx.strokeRect(0, floorY, width, 1);

    // Render Glyphs
    state.glyphs.forEach((glyph) => glyph.draw(ctx));

    // Render TIM Apparatus
    if (state.mode === 'tim') {
      state.fans.forEach((f) => f.draw(ctx));
      state.ramps.forEach((r) => r.draw(ctx));
      state.dominoes.forEach((d) => d.draw(ctx));
      state.seesaws.forEach((s) => s.draw(ctx));
      state.bumpers.forEach((b) => b.draw(ctx));
      state.gears.forEach((g) => g.draw(ctx));
      state.targetBells.forEach((tb) => tb.draw(ctx));
      if (state.emitter) state.emitter.draw(ctx);

      if (state.simState === 'edit' && state.selectedPart) {
        drawSelectionHalo(ctx, state.selectedPart);
      }
    }

    // Render Balls (post-collision)
    state.balls.forEach((ball) => ball.draw(ctx));

    // Render Shockwave Impact Ripples
    for (let i = state.impactRipples.length - 1; i >= 0; i--) {
      const r = state.impactRipples[i];
      r.radius += 80 * dt;
      r.life -= 1.8 * dt;

      if (r.life <= 0 || r.radius >= r.maxRadius) {
        state.impactRipples.splice(i, 1);
        continue;
      }

      ctx.save();
      ctx.beginPath();
      ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
      ctx.strokeStyle = r.color;
      ctx.globalAlpha = r.life;
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.restore();
    }

    renderOscilloscope();
  }

  // --- Zero-Allocation Oscilloscope Renderer ---
  const scopeCanvas = document.getElementById('scopeCanvas');
  const scopeCtx = scopeCanvas.getContext('2d');

  function renderOscilloscope() {
    const sw = scopeCanvas.width;
    const sh = scopeCanvas.height;
    scopeCtx.clearRect(0, 0, sw, sh);

    if (!analyser || !scopeDataArray || !state.audioEnabled) {
      scopeCtx.strokeStyle = 'rgba(148, 163, 184, 0.2)';
      scopeCtx.lineWidth = 1;
      scopeCtx.beginPath();
      scopeCtx.moveTo(0, sh / 2);
      scopeCtx.lineTo(sw, sh / 2);
      scopeCtx.stroke();
      return;
    }

    analyser.getByteTimeDomainData(scopeDataArray);

    scopeCtx.lineWidth = 1.5;
    scopeCtx.strokeStyle = state.mode === 'animusic' ? getThemeColor('--cyan', '#38bdf8') : getThemeColor('--amber', '#f59e0b');
    scopeCtx.beginPath();

    const bufferLength = scopeDataArray.length;
    const sliceWidth = sw / bufferLength;
    let x = 0;

    for (let i = 0; i < bufferLength; i++) {
      const v = scopeDataArray[i] / 128.0;
      const y = (v * sh) / 2;
      if (i === 0) {
        scopeCtx.moveTo(x, y);
      } else {
        scopeCtx.lineTo(x, y);
      }
      x += sliceWidth;
    }

    scopeCtx.lineTo(sw, sh / 2);
    scopeCtx.stroke();
  }

  // --- Mode Switching ---
  function switchMode(newMode) {
    state.mode = newMode;
    const tabAnimusic = document.getElementById('tabAnimusic');
    const tabTim = document.getElementById('tabTim');
    const animusicControls = document.getElementById('animusicControls');
    const timControls = document.getElementById('timControls');
    const sidebarTitle = document.getElementById('sidebarTitleText');
    const sidebarIcon = document.getElementById('sidebarIcon');
    const sidebarBadge = document.getElementById('sidebarBadge');
    const hudMode = document.getElementById('hudModeLabel');
    const fireBtn = document.getElementById('btnFireBall');
    const runStopBtn = document.getElementById('btnRunStop');
    const inputLabel = document.getElementById('inputLabel');
    const infoCard = document.getElementById('infoCardText');
    const body = document.getElementById('labBody');

    state.balls = [];
    state.impactRipples = [];

    if (newMode === 'animusic') {
      body.className = 'animusic-mode';
      tabAnimusic.classList.add('active');
      tabAnimusic.setAttribute('aria-selected', 'true');
      tabTim.classList.remove('active');
      tabTim.setAttribute('aria-selected', 'false');
      animusicControls.style.display = 'block';
      timControls.style.display = 'none';
      if (runStopBtn) runStopBtn.classList.add('hidden');

      sidebarTitle.textContent = 'Acoustic Synthesizer';
      sidebarIcon.textContent = '🎶';
      sidebarBadge.textContent = 'Physical FM';
      hudMode.textContent = 'Animusic Pipe Dream';

      fireBtn.className = 'btn-fire';
      setButtonIconLabel(fireBtn, '⚡', 'Launch Canon');
      inputLabel.textContent = 'INSTRUMENT SCORE';
      setInfoCardContent(
        infoCard,
        'Animusic Mode:',
        'Letter contours act as tuned marimba bars, crystalline bell tines, and laser harps. Polished chrome spheres bounce off real offscreen glyph geometry, triggering physical-modeling WebAudio synthesis.'
      );
    } else {
      body.className = 'tim-mode';
      tabTim.classList.add('active');
      tabTim.setAttribute('aria-selected', 'true');
      tabAnimusic.classList.remove('active');
      tabAnimusic.setAttribute('aria-selected', 'false');
      animusicControls.style.display = 'none';
      timControls.style.display = 'block';
      if (runStopBtn) {
        runStopBtn.classList.remove('hidden');
        setButtonIconLabel(runStopBtn, '▶', 'Run Contraption');
        runStopBtn.classList.remove('running');
      }

      state.simState = 'edit';
      sidebarTitle.textContent = 'Mechanical Workbench';
      sidebarIcon.textContent = '⚙️';
      sidebarBadge.textContent = 'Blueprint 2D';
      hudMode.textContent = 'TIM Rube Goldberg';

      fireBtn.className = 'btn-fire fire-tim';
      setButtonIconLabel(fireBtn, '🎳', 'Drop Marble');
      inputLabel.textContent = 'CONTRAPTION WORD';
      setInfoCardContent(
        infoCard,
        'The Incredible Machine Mode:',
        'Drag ramps, bumpers, fans, gears, and the target bell in Blueprint mode, then press Run Contraption to guide marbles across real PocketGull glyph contours into the 5:1 Optotype Bell.'
      );
    }

    buildLayout();
    updateGoalHud();
    updateSelectionUi();
  }

  // --- Slider Synchronization Helper ---
  function syncTimSliders() {
    const sGrav = document.getElementById('sliderTimGrav');
    const vGrav = document.getElementById('valTimGrav');
    const sRest = document.getElementById('sliderRest');
    const vRest = document.getElementById('valRest');
    const sFric = document.getElementById('sliderFric');
    const vFric = document.getElementById('valFric');
    const sGear = document.getElementById('sliderGear');
    const vGear = document.getElementById('valGear');

    if (sGrav) sGrav.value = String(state.gravTim);
    if (vGrav) vGrav.textContent = `${state.gravTim.toFixed(2)} g`;
    if (sRest) sRest.value = String(state.restitution);
    if (vRest) vRest.textContent = state.restitution.toFixed(2);
    if (sFric) sFric.value = String(state.friction);
    if (vFric) vFric.textContent = state.friction.toFixed(2);
    if (sGear) sGear.value = String(state.gearRpm);
    if (vGear) vGear.textContent = `${state.gearRpm} RPM`;
  }

  // --- Pointer Hit Testing for TIM Blueprint Editing ---
  function findPartAt(x, y) {
    if (state.emitter && state.emitter.hitTest(x, y)) return state.emitter;
    const collections = [state.targetBells, state.bumpers, state.fans, state.ramps, state.seesaws, state.gears];
    for (const list of collections) {
      for (let i = list.length - 1; i >= 0; i--) {
        if (list[i].hitTest(x, y)) return list[i];
      }
    }
    return null;
  }

  // --- Event Listeners ---
  document.getElementById('tabAnimusic').addEventListener('click', () => switchMode('animusic'));
  document.getElementById('tabTim').addEventListener('click', () => switchMode('tim'));

  const contraptionInput = document.getElementById('contraptionText');
  contraptionInput.addEventListener('input', (e) => {
    state.text = e.target.value || 'A';
    const isRtl = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/.test(state.text);
    contraptionInput.dir = isRtl ? 'rtl' : 'ltr';
    buildLayout();
  });

  document.getElementById('btnFireBall').addEventListener('click', () => fireBall());

  const runStopBtn = document.getElementById('btnRunStop');
  if (runStopBtn) {
    runStopBtn.addEventListener('click', () => {
      initAudio();
      setTimSimState(state.simState === 'edit' ? 'run' : 'edit');
    });
  }

  const streamBtn = document.getElementById('btnContinuousStream');
  const streamText = document.getElementById('streamText');
  streamBtn.addEventListener('click', () => {
    initAudio();
    state.continuous = !state.continuous;
    streamText.textContent = `Continuous: ${state.continuous ? 'ON' : 'OFF'}`;
    streamBtn.style.borderColor = state.continuous ? 'var(--cyan)' : 'var(--card-border)';
  });

  document.getElementById('btnClearStage').addEventListener('click', () => {
    resetTimSimulation();
  });

  // TIM Parts Palette Spawners
  document.querySelectorAll('[data-addpart]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (state.mode !== 'tim') switchMode('tim');
      if (state.simState !== 'edit') setTimSimState('edit');

      const kind = btn.getAttribute('data-addpart');
      const cx = width * 0.5 + (Math.random() - 0.5) * 60;
      const cy = height * 0.34 + (Math.random() - 0.5) * 40;
      let created = null;

      if (kind === 'ramp') {
        created = new Ramp(cx, cy, 175, 0.28);
        state.ramps.push(created);
      } else if (kind === 'bumper') {
        created = new Bumper(cx, cy, 24);
        state.bumpers.push(created);
      } else if (kind === 'fan') {
        created = new Fan(cx, cy, 0, 220, 1550);
        state.fans.push(created);
      } else if (kind === 'bell') {
        created = new TargetBell(cx, cy, 22);
        state.targetBells.push(created);
      }

      if (created) {
        state.selectedPart = created;
        updateSelectionUi();
      }
    });
  });

  document.getElementById('btnPartRotateLeft')?.addEventListener('click', () => {
    if (state.selectedPart && state.selectedPart.rotatable) {
      state.selectedPart.rotateBy(-Math.PI / 12);
      updateSelectionUi();
    }
  });

  document.getElementById('btnPartRotateRight')?.addEventListener('click', () => {
    if (state.selectedPart && state.selectedPart.rotatable) {
      state.selectedPart.rotateBy(Math.PI / 12);
      updateSelectionUi();
    }
  });

  document.getElementById('btnPartDelete')?.addEventListener('click', () => {
    deleteSelectedPart();
  });

  // Canvas Pointer Interactions (Blueprint Drag + Run Gear Parity + Ball Drop)
  canvas.addEventListener('pointerdown', (e) => {
    initAudio();
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (state.mode === 'tim' && state.simState === 'edit') {
      const hitPart = findPartAt(x, y);
      if (hitPart) {
        state.selectedPart = hitPart;
        state.dragState = {
          part: hitPart,
          offsetX: hitPart.x - x,
          offsetY: hitPart.y - y,
          startX: x,
          startY: y,
          moved: false
        };
        canvas.setPointerCapture?.(e.pointerId);
        updateSelectionUi();
        return;
      }
      state.selectedPart = null;
      updateSelectionUi();
      return;
    }

    // In TIM Run mode: clicking a gear flips the entire coupled gear train parity
    if (state.mode === 'tim') {
      for (const gear of state.gears) {
        if (gear.hitTest(x, y)) {
          flipGearTrainParity();
          return;
        }
      }
    }

    const radius = state.mode === 'animusic' ? 7 : 11;
    const isChrome = state.mode === 'animusic';
    state.balls.push(new Ball(x, y, (Math.random() - 0.5) * 60, 20, radius, isChrome));
    if (state.balls.length > 25) state.balls.shift();
  });

  canvas.addEventListener('pointermove', (e) => {
    if (!state.dragState) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (Math.hypot(x - state.dragState.startX, y - state.dragState.startY) > 4) {
      state.dragState.moved = true;
    }

    const part = state.dragState.part;
    part.x = Math.max(24, Math.min(width - 24, x + state.dragState.offsetX));
    part.y = Math.max(40, Math.min(getFloorY() - 16, y + state.dragState.offsetY));
  });

  canvas.addEventListener('pointerup', (e) => {
    if (!state.dragState) return;
    const { part, moved } = state.dragState;
    state.dragState = null;
    canvas.releasePointerCapture?.(e.pointerId);
    if (!moved && part.type === 'gear') {
      flipGearTrainParity();
    }
  });

  // Audio Mute Toggle (Zero innerHTML)
  const muteBtn = document.getElementById('btnAudioMute');
  muteBtn.addEventListener('click', () => {
    state.audioEnabled = !state.audioEnabled;
    if (state.audioEnabled) {
      initAudio();
      setButtonIconLabel(muteBtn, '🔊', 'Audio: ON');
      muteBtn.style.color = 'var(--text-main)';
    } else {
      setButtonIconLabel(muteBtn, '🔇', 'Audio: MUTED');
      muteBtn.style.color = 'var(--rose)';
    }
  });

  // Theme Switcher: Dark -> Washi -> Light -> Scotopic (650nm Red)
  const themeBtn = document.getElementById('btnThemeToggle');
  const THEME_LABELS = {
    dark: 'Dark',
    washi: 'Washi',
    light: 'Light',
    scotopic: 'Scotopic'
  };
  themeBtn.addEventListener('click', () => {
    const themes = ['dark', 'washi', 'light', 'scotopic'];
    const currentIdx = themes.indexOf(state.theme);
    const nextTheme = themes[(currentIdx + 1) % themes.length];
    state.theme = nextTheme;
    document.documentElement.setAttribute('data-theme', nextTheme);
    setButtonIconLabel(themeBtn, '◐', THEME_LABELS[nextTheme] || nextTheme);
  });

  // Mobile Drawer Toggle
  const drawerToggle = document.getElementById('btnDrawerToggle');
  const sidebarEl = document.querySelector('.control-sidebar');
  if (drawerToggle && sidebarEl) {
    drawerToggle.addEventListener('click', () => {
      const open = sidebarEl.classList.toggle('drawer-open');
      drawerToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Animusic Sliders Binding
  document.getElementById('sliderReso').addEventListener('input', (e) => {
    state.reso = parseFloat(e.target.value);
    document.getElementById('valReso').textContent = state.reso.toFixed(2);
    document.getElementById('hudReso').textContent = state.reso.toFixed(2);
  });

  document.getElementById('sliderBpm').addEventListener('input', (e) => {
    state.bpm = parseInt(e.target.value, 10);
    document.getElementById('valBpm').textContent = `${state.bpm} bpm`;
  });

  const timbreNames = ['Padauk Marimba', 'Crystalline Bell', 'Laser Harp', 'Resonant Cello'];
  document.getElementById('sliderTimbre').addEventListener('input', (e) => {
    state.timbre = parseInt(e.target.value, 10);
    document.getElementById('valTimbre').textContent = timbreNames[state.timbre];
  });

  document.getElementById('sliderGrav').addEventListener('input', (e) => {
    state.gravAnimusic = parseFloat(e.target.value);
    document.getElementById('valGrav').textContent = `${state.gravAnimusic.toFixed(2)} g`;
  });

  // TIM Sliders Binding
  document.getElementById('sliderTimGrav').addEventListener('input', (e) => {
    state.gravTim = parseFloat(e.target.value);
    document.getElementById('valTimGrav').textContent = `${state.gravTim.toFixed(2)} g`;
  });

  document.getElementById('sliderRest').addEventListener('input', (e) => {
    state.restitution = parseFloat(e.target.value);
    document.getElementById('valRest').textContent = state.restitution.toFixed(2);
  });

  document.getElementById('sliderFric').addEventListener('input', (e) => {
    state.friction = parseFloat(e.target.value);
    document.getElementById('valFric').textContent = state.friction.toFixed(2);
  });

  document.getElementById('sliderGear').addEventListener('input', (e) => {
    state.gearRpm = parseInt(e.target.value, 10);
    document.getElementById('valGear').textContent = `${state.gearRpm} RPM`;
  });

  // Melodic Scale Buttons
  document.querySelectorAll('[data-scale]').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-scale]').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      state.scale = btn.getAttribute('data-scale');
      buildLayout();
    });
  });

  // TIM Preset Buttons (Sync all sliders cleanly)
  document.querySelectorAll('[data-timpreset]').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-timpreset]').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const presetKey = btn.getAttribute('data-timpreset');
      const cfg = TIM_PRESET_CONFIG[presetKey] || TIM_PRESET_CONFIG.dosage;

      state.timPreset = presetKey;
      state.text = cfg.text;
      state.gravTim = cfg.grav;
      state.restitution = cfg.rest;
      state.friction = cfg.fric;
      state.gearRpm = cfg.gear;

      if (cfg.scale) {
        state.scale = cfg.scale;
        document.querySelectorAll('[data-scale]').forEach((b) => {
          b.classList.toggle('active', b.getAttribute('data-scale') === cfg.scale);
        });
      }

      contraptionInput.value = state.text;
      const isRtl = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/.test(state.text);
      contraptionInput.dir = isRtl ? 'rtl' : 'ltr';

      syncTimSliders();
      setTimSimState('edit');
      buildLayout();
    });
  });

  // Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    if (e.code === 'Space') {
      e.preventDefault();
      fireBall();
    } else if (e.key === 'r' || e.key === 'R') {
      if (state.mode === 'tim') {
        setTimSimState('edit');
      } else {
        resetTimSimulation();
      }
    } else if (e.key === 't' || e.key === 'T') {
      switchMode(state.mode === 'animusic' ? 'tim' : 'animusic');
    } else if (e.key === 'm' || e.key === 'M') {
      muteBtn.click();
    } else if (e.key === 'q' || e.key === 'Q') {
      if (state.mode === 'tim' && state.simState === 'edit' && state.selectedPart && state.selectedPart.rotatable) {
        state.selectedPart.rotateBy(-Math.PI / 12);
        updateSelectionUi();
      }
    } else if (e.key === 'e' || e.key === 'E') {
      if (state.mode === 'tim' && state.simState === 'edit' && state.selectedPart && state.selectedPart.rotatable) {
        state.selectedPart.rotateBy(Math.PI / 12);
        updateSelectionUi();
      }
    } else if (e.key === 'Delete' || e.key === 'Backspace') {
      if (state.mode === 'tim' && state.simState === 'edit' && state.selectedPart) {
        e.preventDefault();
        deleteSelectedPart();
      }
    }
  });

  // --- Zero-Backend Shareable Blueprints (#bp=...) ---
  function clampNum(val, min, max, fallback) {
    const n = Number(val);
    return Number.isFinite(n) ? Math.max(min, Math.min(max, n)) : fallback;
  }

  function encodeBase64Url(str) {
    const bytes = new TextEncoder().encode(str);
    let bin = '';
    for (let i = 0; i < bytes.length; i++) {
      bin += String.fromCharCode(bytes[i]);
    }
    return btoa(bin).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
  }

  function decodeBase64Url(b64u) {
    let b64 = b64u.replace(/-/g, '+').replace(/_/g, '/');
    while (b64.length % 4) b64 += '=';
    const bin = atob(b64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) {
      bytes[i] = bin.charCodeAt(i);
    }
    return new TextDecoder().decode(bytes);
  }

  function serializeBlueprint() {
    const w = width || 1;
    const h = height || 1;
    const r4 = (v) => Math.round(v * 10000) / 10000;

    const payload = {
      v: 1,
      t: String(state.text || '500MG').slice(0, 24),
      p: state.timPreset,
      g: r4(state.gravTim),
      r: r4(state.restitution),
      f: r4(state.friction),
      rpm: Math.round(state.gearRpm),
      em: state.emitter
        ? [r4(state.emitter.x / w), r4(state.emitter.y / h), r4(state.emitter.vx), r4(state.emitter.vy)]
        : null,
      rm: state.ramps.slice(0, 30).map((rm) => [r4(rm.x / w), r4(rm.y / h), r4(rm.length), r4(rm.angle)]),
      bm: state.bumpers.slice(0, 30).map((bm) => [r4(bm.x / w), r4(bm.y / h), r4(bm.radius)]),
      fn: state.fans.slice(0, 30).map((fn) => [r4(fn.x / w), r4(fn.y / h), r4(fn.angle), r4(fn.range), r4(fn.strength)]),
      tb: state.targetBells.slice(0, 30).map((tb) => [r4(tb.x / w), r4(tb.y / h), r4(tb.radius)]),
      sw: state.seesaws.slice(0, 30).map((sw) => [r4(sw.x / w), r4(sw.y / h), r4(sw.length), r4(sw.initialAngle)]),
      gr: state.gears.slice(0, 30).map((gr) => [r4(gr.x / w), r4(gr.y / h), r4(gr.radius), Math.round(gr.teeth), gr.direction >= 0 ? 1 : -1, r4(gr.speedRatio)]),
      dm: state.dominoes.slice(0, 30).map((dm) => [r4(dm.x / w), r4(dm.y / h), r4(dm.w), r4(dm.h), dm.dir < 0 ? -1 : 1])
    };
    return encodeBase64Url(JSON.stringify(payload));
  }

  function applyBlueprintData(data) {
    if (!data || typeof data !== 'object' || data.v !== 1) return false;

    const w = width || 960;
    const h = height || 600;
    const nx = (v) => clampNum(v, 0.02, 0.98, 0.5) * w;
    const ny = (v) => clampNum(v, 0.02, 0.98, 0.5) * h;

    state.timPreset = Object.prototype.hasOwnProperty.call(TIM_PRESET_CONFIG, data.p) ? data.p : 'dosage';
    state.text = typeof data.t === 'string' && data.t.length > 0 ? data.t.slice(0, 24) : '500MG';
    state.gravTim = clampNum(data.g, -1.0, 2.0, 1.0);
    state.restitution = clampNum(data.r, 0.1, 0.95, 0.70);
    state.friction = clampNum(data.f, 0.01, 0.30, 0.08);
    state.gearRpm = Math.round(clampNum(data.rpm, 0, 180, 60));

    contraptionInput.value = state.text;
    const isRtl = /[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]/.test(state.text);
    contraptionInput.dir = isRtl ? 'rtl' : 'ltr';
    if (isRtl) {
      state.scale = 'maqam';
      document.querySelectorAll('[data-scale]').forEach((b) => {
        b.classList.toggle('active', b.getAttribute('data-scale') === 'maqam');
      });
    }

    document.querySelectorAll('[data-timpreset]').forEach((b) => {
      b.classList.toggle('active', b.getAttribute('data-timpreset') === state.timPreset);
    });

    syncTimSliders();
    switchMode('tim');

    // Override preset parts with the decoded blueprint parts
    state.ramps = [];
    state.bumpers = [];
    state.fans = [];
    state.targetBells = [];
    state.seesaws = [];
    state.gears = [];
    state.dominoes = [];
    state.selectedPart = null;
    state.goalComplete = false;

    if (Array.isArray(data.em) && data.em.length >= 4) {
      state.emitter = new Emitter(
        nx(data.em[0]),
        ny(data.em[1]),
        clampNum(data.em[2], -500, 500, 100),
        clampNum(data.em[3], -500, 500, 0)
      );
    }
    if (Array.isArray(data.rm)) {
      data.rm.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 4) {
          state.ramps.push(new Ramp(nx(item[0]), ny(item[1]), clampNum(item[2], 40, 420, 170), clampNum(item[3], -Math.PI, Math.PI, 0.28)));
        }
      });
    }
    if (Array.isArray(data.bm)) {
      data.bm.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 3) {
          state.bumpers.push(new Bumper(nx(item[0]), ny(item[1]), clampNum(item[2], 12, 48, 24)));
        }
      });
    }
    if (Array.isArray(data.fn)) {
      data.fn.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 5) {
          state.fans.push(new Fan(nx(item[0]), ny(item[1]), clampNum(item[2], -Math.PI * 2, Math.PI * 2, 0), clampNum(item[3], 60, 420, 220), clampNum(item[4], 200, 3200, 1550)));
        }
      });
    }
    if (Array.isArray(data.tb)) {
      data.tb.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 3) {
          state.targetBells.push(new TargetBell(nx(item[0]), ny(item[1]), clampNum(item[2], 14, 44, 22)));
        }
      });
    }
    if (Array.isArray(data.sw)) {
      data.sw.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 4) {
          state.seesaws.push(new Seesaw(nx(item[0]), ny(item[1]), clampNum(item[2], 60, 360, 180), clampNum(item[3], -Math.PI / 5, Math.PI / 5, 0.12)));
        }
      });
    }
    if (Array.isArray(data.gr)) {
      data.gr.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 6) {
          state.gears.push(new Gear(nx(item[0]), ny(item[1]), clampNum(item[2], 12, 70, 28), Math.round(clampNum(item[3], 4, 24, 8)), item[4] < 0 ? -1 : 1, clampNum(item[5], 0.25, 4, 1)));
        }
      });
    }
    if (Array.isArray(data.dm)) {
      data.dm.slice(0, 30).forEach((item) => {
        if (Array.isArray(item) && item.length >= 5) {
          state.dominoes.push(new Domino(nx(item[0]), ny(item[1]), clampNum(item[2], 4, 20, 8), clampNum(item[3], 16, 80, 38), item[4] < 0 ? -1 : 1));
        }
      });
    }

    updateSelectionUi();
    updateGoalHud();
    return true;
  }

  function loadBlueprintFromHash() {
    const hash = window.location.hash || '';
    if (!hash.startsWith('#bp=') || hash.length > 8192) return false;
    try {
      const encoded = hash.slice(4);
      if (!/^[A-Za-z0-9\-_]+$/.test(encoded)) return false;
      const jsonStr = decodeBase64Url(encoded);
      const parsed = JSON.parse(jsonStr);
      return applyBlueprintData(parsed);
    } catch (_err) {
      return false;
    }
  }

  const shareBlueprintBtn = document.getElementById('btnShareBlueprint');
  if (shareBlueprintBtn) {
    let shareTimer = null;
    shareBlueprintBtn.addEventListener('click', () => {
      if (state.mode !== 'tim') switchMode('tim');
      const encoded = serializeBlueprint();
      window.history.replaceState(null, '', '#bp=' + encoded);
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
        navigator.clipboard.writeText(window.location.href).catch(() => {});
      }
      setButtonIconLabel(shareBlueprintBtn, '✓', 'Link Copied');
      if (shareTimer) clearTimeout(shareTimer);
      shareTimer = setTimeout(() => {
        setButtonIconLabel(shareBlueprintBtn, '🔗', 'Copy Blueprint Link');
      }, 2000);
    });
  }

  window.addEventListener('hashchange', () => {
    if (window.location.hash.startsWith('#bp=')) {
      loadBlueprintFromHash();
    }
  });

  // Init
  resizeCanvas();
  if (window.location.hash.startsWith('#bp=')) {
    loadBlueprintFromHash();
  }
  requestAnimationFrame(animate);
})();
