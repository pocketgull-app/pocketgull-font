/**
 * PocketGull Physiological Sinus Rhythm & Phosphor-Sweep Telemetry Engine
 * =======================================================================
 * Replaces discontinuous CSS stroke-dasharray hacks with an authentic 60fps
 * circular-buffer ICU phosphor-sweep oscilloscope (25 mm/s clinical sweep bar,
 * C-infinity smooth McSharry-Gaussian P-Q-R-S-T morphology with cushioned apex
 * fillets, zero wrap-around jump, and fixed-pitch PocketGull Mono sub-cell
 * Unicode waveform tickers).
 *
 * 100% offline, zero telemetry, zero innerHTML. Passive visual demonstration
 * only (PocketGull Negative Space Invariant: Not a Medical Device / SaMD).
 *
 * Licensed under SIL Open Font License 1.1 / Apache 2.0
 */
(function (global) {
  'use strict';

  function gaussian(phase, mu, sigma, amp) {
    var d = phase - mu;
    if (d > 0.5) d -= 1.0;
    if (d < -0.5) d += 1.0;
    return amp * Math.exp(-(d * d) / (2 * sigma * sigma));
  }

  /**
   * Evaluates normalized Lead II cardiac potential in [-0.45, +1.0] for phase in [0, 1).
   * Smooth periodic boundary V(0) ~ V(1) ~ 0 eliminates phase-wrap discontinuities.
   */
  function evaluateCardiacLeadII(phase, morphology, timeSec) {
    var p = ((phase % 1) + 1) % 1;
    var t = timeSec || 0;

    if (morphology === 'flat' || morphology === 'stillness') {
      return 0;
    }

    if (morphology === 'vtach') {
      // Wide-complex monomorphic ventricular tachycardia (~178 BPM), bounded cleanly inside [-0.52, +0.82]
      var vMain = Math.sin(p * Math.PI * 2) * 0.56 + 0.12;
      var vHarmonic = Math.sin(p * Math.PI * 4 - 0.55) * 0.16;
      var avWander = Math.sin(t * 2.3) * 0.04;
      return vMain + vHarmonic + avWander;
    }

    if (morphology === 'adenosine') {
      // Transient vagal slowing with wide->narrow cardioversion capture beat
      var pWave = gaussian(p, 0.22, 0.032, 0.11);
      var qDip = gaussian(p, 0.34, 0.011, -0.10);
      var rPeak = gaussian(p, 0.38, 0.018, 0.88);
      var sDip = gaussian(p, 0.43, 0.016, -0.24);
      var tDome = gaussian(p, 0.66, 0.055, 0.26);
      var baseline = Math.sin(t * 1.8) * 0.03;
      return pWave + qDip + rPeak + sDip + tDome + baseline;
    }

    // Canonical Lead II Normal Sinus Rhythm (McSharry 5-Gaussian P-Q-R-S-T)
    // Cushioned Gaussian R-apex honors PocketGull's 25 UPM felt-marker fillet DNA.
    var pAtrial = gaussian(p, 0.18, 0.028, 0.14);
    var qSeptal = gaussian(p, 0.315, 0.009, -0.11);
    var rVentricular = gaussian(p, 0.35, 0.0145, 0.96);
    var sBasal = gaussian(p, 0.39, 0.012, -0.23);
    var tRepolar = gaussian(p, 0.62, 0.048, 0.28);
    var uSubtle = gaussian(p, 0.79, 0.022, 0.035);
    return pAtrial + qSeptal + rVentricular + sBasal + tRepolar + uSubtle;
  }

  /**
   * Evaluates pulse oximetry plethysmograph (SpO2) wave with dicrotic notch in [0, 1].
   */
  function evaluatePlethWave(phase) {
    var p = ((phase % 1) + 1) % 1;
    var systolic = gaussian(p, 0.26, 0.075, 0.95);
    var dicrotic = gaussian(p, 0.50, 0.095, 0.44);
    var v = systolic + dicrotic;
    return Math.max(0, Math.min(1, v));
  }

  function prefersReducedMotion() {
    return Boolean(
      global.matchMedia &&
      global.matchMedia('(prefers-reduced-motion: reduce)').matches
    );
  }

  /**
   * Circular-Buffer Clinical Phosphor-Sweep Canvas Oscilloscope
   */
  function PhosphorEcgMonitor(canvas, options) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    var opts = options || {};
    this.bpm = typeof opts.bpm === 'number' ? opts.bpm : 72;
    this.morphology = opts.morphology || 'sinus';
    this.color = opts.color || '#10b981';
    this.gridColor = opts.gridColor || 'rgba(148, 163, 184, 0.08)';
    this.majorGridColor = opts.majorGridColor || 'rgba(148, 163, 184, 0.15)';
    this.showGrid = opts.showGrid !== false;
    this.sweepSeconds = opts.sweepSeconds || 3.6; // full screen = 3.6s (~4.3 beats at 72 BPM)
    this.eraseGapCols = opts.eraseGapCols || 18;
    this.lineWidth = opts.lineWidth || 2.2;
    this.paused = Boolean(opts.paused);
    this.onBeat = typeof opts.onBeat === 'function' ? opts.onBeat : null;

    this.width = 0;
    this.height = 0;
    this.dpr = 1;
    this.samples = null;
    this.cursor = 0;
    this.cardiacPhase = 0;
    this.prevCardiacPhase = 0;
    this.subColAccum = 0;
    this.lastTs = 0;
    this.elapsedSec = 0;
    this.rafId = null;
    this._destroyed = false;

    var self = this;
    this._resizeHandler = function () {
      self.resize();
    };

    if (typeof ResizeObserver !== 'undefined') {
      this._ro = new ResizeObserver(this._resizeHandler);
      this._ro.observe(canvas);
    } else {
      global.addEventListener('resize', this._resizeHandler);
    }

    this.resize();
    this.start();
  }

  PhosphorEcgMonitor.prototype.resize = function () {
    if (!this.canvas) return;
    var rect = this.canvas.getBoundingClientRect();
    var cssW = Math.max(120, Math.round(rect.width || this.canvas.clientWidth || 480));
    var cssH = Math.max(26, Math.round(rect.height || this.canvas.clientHeight || 40));
    var dpr = Math.min(global.devicePixelRatio || 1, 2);

    if (cssW === this.width && cssH === this.height && dpr === this.dpr && this.samples) {
      return;
    }

    this.width = cssW;
    this.height = cssH;
    this.dpr = dpr;
    this.canvas.width = Math.round(cssW * dpr);
    this.canvas.height = Math.round(cssH * dpr);

    var n = cssW;
    this.samples = new Float32Array(n);

    // Pre-populate buffer with continuous steady-state waveform so initial paint has zero blank void
    var beatsAcrossScreen = (Math.max(this.bpm, 1) / 60) * this.sweepSeconds;
    for (var i = 0; i < n; i++) {
      var ph = ((i / n) * beatsAcrossScreen) % 1;
      this.samples[i] = this.bpm <= 0 ? 0 : evaluateCardiacLeadII(ph, this.morphology, i * 0.01);
    }
    this.cursor = Math.floor(n * 0.82);
    this.cardiacPhase = ((this.cursor / n) * beatsAcrossScreen) % 1;
    this.drawFrame();
  };

  PhosphorEcgMonitor.prototype.setConfig = function (cfg) {
    var reseed = false;
    if (cfg.bpm !== undefined && cfg.bpm !== this.bpm) {
      this.bpm = cfg.bpm;
      if (prefersReducedMotion() || this.bpm === 0) reseed = true;
    }
    if (cfg.morphology !== undefined && cfg.morphology !== this.morphology) {
      this.morphology = cfg.morphology;
      if (prefersReducedMotion()) reseed = true;
    }
    if (cfg.color !== undefined) this.color = cfg.color;
    if (cfg.paused !== undefined) this.paused = Boolean(cfg.paused);

    if (reseed && this.samples) {
      var n = this.samples.length;
      var beatsAcrossScreen = (Math.max(this.bpm || 60, 1) / 60) * this.sweepSeconds;
      for (var i = 0; i < n; i++) {
        var ph = ((i / n) * beatsAcrossScreen) % 1;
        this.samples[i] = this.bpm <= 0 ? 0 : evaluateCardiacLeadII(ph, this.morphology, 0);
      }
      this.drawFrame();
    }
  };

  PhosphorEcgMonitor.prototype.stepSimulation = function (dtSec) {
    if (!this.samples || this.samples.length === 0) return;
    if (this.paused || prefersReducedMotion()) return;

    var n = this.samples.length;
    var colsPerSec = n / this.sweepSeconds;
    this.subColAccum += dtSec * colsPerSec;
    var steps = Math.min(Math.floor(this.subColAccum), n);
    if (steps <= 0) return;
    this.subColAccum -= steps;

    var dtPerCol = 1 / colsPerSec;
    var effectiveBpm = Math.max(0, this.bpm);

    for (var s = 0; s < steps; s++) {
      this.elapsedSec += dtPerCol;
      if (effectiveBpm > 0) {
        // Subtle physiological respiratory sinus arrhythmia (+/- 2% natural vagal variability)
        var rsaFactor = this.morphology === 'sinus' ? (1 + 0.022 * Math.sin(this.elapsedSec * 1.15)) : 1;
        var dPhase = (effectiveBpm * rsaFactor / 60) * dtPerCol;
        this.prevCardiacPhase = this.cardiacPhase;
        this.cardiacPhase = (this.cardiacPhase + dPhase) % 1;

        // Trigger optional S1/S2 callback as phase crosses R-wave onset (0.34)
        if (this.onBeat && this.prevCardiacPhase < 0.34 && this.cardiacPhase >= 0.34) {
          this.onBeat(effectiveBpm, this.morphology);
        }
      }

      this.cursor = (this.cursor + 1) % n;
      this.samples[this.cursor] = effectiveBpm <= 0
        ? 0
        : evaluateCardiacLeadII(this.cardiacPhase, this.morphology, this.elapsedSec);
    }
  };

  PhosphorEcgMonitor.prototype.drawFrame = function () {
    var ctx = this.ctx;
    var w = this.width;
    var h = this.height;
    if (!ctx || !this.samples || w <= 0 || h <= 0) return;

    ctx.save();
    ctx.scale(this.dpr, this.dpr);
    ctx.clearRect(0, 0, w, h);

    // 1. Clinical 5mm / 25mm calibration grid
    if (this.showGrid) {
      var minor = Math.max(8, Math.round(h / 6));
      var major = minor * 5;
      ctx.lineWidth = 1;

      ctx.strokeStyle = this.gridColor;
      ctx.beginPath();
      for (var gx = 0; gx < w; gx += minor) {
        ctx.moveTo(gx + 0.5, 0);
        ctx.lineTo(gx + 0.5, h);
      }
      for (var gy = 0; gy < h; gy += minor) {
        ctx.moveTo(0, gy + 0.5);
        ctx.lineTo(w, gy + 0.5);
      }
      ctx.stroke();

      ctx.strokeStyle = this.majorGridColor;
      ctx.beginPath();
      for (var mx = 0; mx < w; mx += major) {
        ctx.moveTo(mx + 0.5, 0);
        ctx.lineTo(mx + 0.5, h);
      }
      for (var my = 0; my < h; my += major) {
        ctx.moveTo(0, my + 0.5);
        ctx.lineTo(w, my + 0.5);
      }
      ctx.stroke();
    }

    var baseY = h * 0.64;
    var ampY = h * 0.50;
    var n = this.samples.length;
    var reduced = prefersReducedMotion() || this.bpm <= 0 || this.paused;
    var gap = reduced ? 0 : Math.min(this.eraseGapCols, Math.floor(n * 0.08));

    // Resolve CSS variable color if needed (e.g. 'var(--emerald)')
    var strokeHex = this.color;
    if (strokeHex.indexOf('var(') === 0 && global.getComputedStyle) {
      var varName = strokeHex.slice(4, -1).trim();
      var resolved = global.getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
      if (resolved) strokeHex = resolved;
    }

    if (reduced) {
      ctx.beginPath();
      for (var rx = 0; rx < n; rx++) {
        var ry = baseY - this.samples[rx] * ampY;
        if (rx === 0) ctx.moveTo(rx, ry);
        else ctx.lineTo(rx, ry);
      }
      ctx.strokeStyle = strokeHex;
      ctx.lineWidth = this.lineWidth;
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.stroke();
      ctx.restore();
      return;
    }

    // 2. Draw phosphor persistence trace in 4 age bands from oldest -> newest cursor
    var drawable = n - gap;
    var bands = 4;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.strokeStyle = strokeHex;

    for (var b = 0; b < bands; b++) {
      var startAge = Math.floor((b / bands) * drawable);
      var endAge = Math.floor(((b + 1) / bands) * drawable);
      var alpha = 0.22 + 0.78 * ((b + 1) / bands);
      ctx.globalAlpha = alpha;
      ctx.lineWidth = b === bands - 1 ? this.lineWidth : Math.max(1.4, this.lineWidth - 0.35);
      ctx.beginPath();

      var penDown = false;
      for (var age = startAge; age <= endAge; age++) {
        // age=0 is oldest sample just ahead of erase bar; age=drawable is newest at this.cursor
        var idx = (this.cursor + gap + age) % n;
        var prevIdx = (idx - 1 + n) % n;
        var y = baseY - this.samples[idx] * ampY;

        if (!penDown || idx === 0) {
          if (penDown && idx === 0) {
            ctx.stroke();
            ctx.beginPath();
          }
          if (age > startAge && idx > 0) {
            ctx.moveTo(idx - 1, baseY - this.samples[prevIdx] * ampY);
            ctx.lineTo(idx, y);
          } else {
            ctx.moveTo(idx, y);
          }
          penDown = true;
        } else {
          ctx.lineTo(idx, y);
        }
      }
      ctx.stroke();
    }

    // 3. Luminous phosphor leading-edge cursor dot
    var headX = this.cursor;
    var headY = baseY - this.samples[headX] * ampY;
    ctx.globalAlpha = 1;
    ctx.shadowColor = strokeHex;
    ctx.shadowBlur = 8;
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(headX, headY, Math.max(2.3, this.lineWidth * 0.95), 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
  };

  PhosphorEcgMonitor.prototype.start = function () {
    if (this.rafId !== null || this._destroyed) return;
    var self = this;
    function loop(ts) {
      if (self._destroyed) return;
      if (!self.lastTs) self.lastTs = ts;
      var dt = Math.min(0.08, Math.max(0, (ts - self.lastTs) / 1000));
      self.lastTs = ts;
      self.stepSimulation(dt);
      self.drawFrame();
      self.rafId = global.requestAnimationFrame(loop);
    }
    this.rafId = global.requestAnimationFrame(loop);
  };

  PhosphorEcgMonitor.prototype.destroy = function () {
    this._destroyed = true;
    if (this.rafId !== null) {
      global.cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
    if (this._ro) this._ro.disconnect();
    global.removeEventListener('resize', this._resizeHandler);
  };

  /**
   * Generates a fixed-width monospace sub-cell Teletext / ICU waveform string
   * using Unicode block elements (▁▂▃▄▅▆▇█) with an advancing phosphor erase gap.
   * Preserves exact character length for PocketGull Mono 600 UPM box alignment.
   */
  var BLOCK_RAMP = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];
  function generateMonospaceWaveString(cols, cursorCol, bpm, mode, sweepSeconds) {
    var width = Math.max(8, cols || 76);
    var gap = 3;
    var beats = (Math.max(bpm || 72, 1) / 60) * (sweepSeconds || 4.8);
    var chars = new Array(width);
    for (var i = 0; i < width; i++) {
      var distAhead = (i - cursorCol + width) % width;
      if (distAhead > 0 && distAhead <= gap) {
        chars[i] = ' ';
        continue;
      }
      var ph = ((i / width) * beats) % 1;
      var level;
      if (mode === 'pleth') {
        var pv = evaluatePlethWave(ph);
        level = Math.round(pv * 7);
      } else {
        var ev = evaluateCardiacLeadII(ph, mode || 'sinus', 0);
        // Map [-0.28, +0.96] -> [0..7] with baseline at index 2 ('▃')
        level = Math.round(((ev + 0.28) / 1.24) * 7);
      }
      var clamped = Math.max(0, Math.min(7, level));
      chars[i] = i === cursorCol ? '█' : BLOCK_RAMP[clamped];
    }
    return chars.join('');
  }

  /**
   * Gentle Low-Frequency Harmonic Stethoscope Synthesizer (WebAudio)
   * Honors Project Ataxia Acoustic Sensitivity: warm low-pass 58Hz/76Hz S1-S2 lub-dub,
   * zero harsh square-wave beeps, strictly muted until explicitly enabled by user.
   */
  function HarmonicCardiacAudio() {
    this.enabled = false;
    this.ctx = null;
  }

  HarmonicCardiacAudio.prototype.toggle = function (forceState) {
    this.enabled = forceState !== undefined ? Boolean(forceState) : !this.enabled;
    if (this.enabled && !this.ctx) {
      var AudioCtx = global.AudioContext || global.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.enabled && this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    return this.enabled;
  };

  HarmonicCardiacAudio.prototype.triggerLubDub = function (bpm, morphology) {
    if (!this.enabled || !this.ctx) return;
    try {
      var now = this.ctx.currentTime;
      var isUrgent = morphology === 'vtach' || bpm > 130;
      var s1Freq = isUrgent ? 88 : 58;
      var s2Freq = isUrgent ? 112 : 76;
      var systoleGap = Math.max(0.14, Math.min(0.28, 60 / Math.max(bpm || 72, 40) * 0.32));

      this._playTone(now, s1Freq, 0.085, 0.09);
      this._playTone(now + systoleGap, s2Freq, 0.065, 0.065);
    } catch (_) {
      // Ignore autoplay restrictions gracefully
    }
  };

  HarmonicCardiacAudio.prototype._playTone = function (startTime, freq, duration, peakGain) {
    var osc = this.ctx.createOscillator();
    var gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq * 1.12, startTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 0.78, startTime + duration);

    gain.gain.setValueAtTime(0.0001, startTime);
    gain.gain.linearRampToValueAtTime(peakGain, startTime + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(startTime);
    osc.stop(startTime + duration + 0.01);
  };

  /**
   * Auto-enhance index.html elements if present (zero inline script modification required).
   */
  function initBroadsideMonitors() {
    if (typeof document === 'undefined') return;

    var monitors = [];

    // 1. Inspector HUD Autonomic Sinus Rhythm (#hudCardiacCanvas)
    var hudCanvas = document.getElementById('hudCardiacCanvas');
    if (hudCanvas) {
      monitors.push(new PhosphorEcgMonitor(hudCanvas, {
        bpm: 72,
        morphology: 'sinus',
        color: '#10b981',
        showGrid: true,
        lineWidth: 2.0,
        sweepSeconds: 3.2
      }));
    }

    // 2. Always-visible Philocardia Healer Live Sinus Strip (#healerSinusCanvas)
    var healerCanvas = document.getElementById('healerSinusCanvas');
    var healerLabel = document.getElementById('healerSinusReadout');
    if (healerCanvas) {
      monitors.push(new PhosphorEcgMonitor(healerCanvas, {
        bpm: 72,
        morphology: 'sinus',
        color: '#10b981',
        showGrid: true,
        lineWidth: 2.1,
        sweepSeconds: 3.6
      }));
    }

    // Synchronize with Philocardia Cadence buttons (72 BPM / 60 BPM / Static)
    document.querySelectorAll('.healer-cadence-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var cad = btn.getAttribute('data-cadence');
        var bpm = cad === '60' ? 60 : cad === 'static' ? 0 : 72;
        var morph = cad === 'static' ? 'sinus' : 'sinus';
        monitors.forEach(function (m) {
          m.setConfig({ bpm: bpm, morphology: morph, paused: cad === 'static' });
        });
        if (healerLabel) {
          healerLabel.textContent = cad === 'static'
            ? 'STATIC SNAPSHOT · CUSHIONED 25 UPM APEX'
            : 'LIVE LEAD II · ' + bpm + ' BPM SINUS · 25 mm/s';
        }
      });
    });

    // 3. Plate 4.1 Fixed 600 UPM PocketGull Mono Sub-Cell Waveform Ticker
    var leadTrack = document.getElementById('icuLeadTrack');
    var plethTrack = document.getElementById('icuPlethTrack');
    if ((leadTrack || plethTrack) && !prefersReducedMotion()) {
      var leadCols = leadTrack ? leadTrack.textContent.length : 77;
      var plethCols = plethTrack ? plethTrack.textContent.length : 77;
      var colCursor = Math.floor(leadCols * 0.78);
      setInterval(function () {
        colCursor = (colCursor + 1) % leadCols;
        if (leadTrack) {
          leadTrack.textContent = generateMonospaceWaveString(leadCols, colCursor, 72, 'sinus', 4.6);
        }
        if (plethTrack) {
          plethTrack.textContent = generateMonospaceWaveString(plethCols, colCursor % plethCols, 72, 'pleth', 4.6);
        }
      }, 65);
    }
  }

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initBroadsideMonitors);
    } else {
      initBroadsideMonitors();
    }
  }

  global.PocketGullSinusEngine = {
    evaluateCardiacLeadII: evaluateCardiacLeadII,
    evaluatePlethWave: evaluatePlethWave,
    generateMonospaceWaveString: generateMonospaceWaveString,
    PhosphorEcgMonitor: PhosphorEcgMonitor,
    HarmonicCardiacAudio: HarmonicCardiacAudio
  };
})(typeof globalThis !== 'undefined' ? globalThis : window);
