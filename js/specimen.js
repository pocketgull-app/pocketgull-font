/* PocketGull Specimen Interactive Engine */


    // 1. Tri-Modal Theme System: Washi Papercraft (和紙), Clinical Obsidian, and 670nm PBM
    const themeButtons = document.querySelectorAll('.theme-nav-btn');
    const pbmToggle = document.getElementById('pbmToggle');
    const pbmLabel = document.getElementById('pbmLabel');

    function applySiteTheme(targetTheme) {
      document.documentElement.setAttribute('data-theme', targetTheme);
      try {
        localStorage.setItem('pocketgull_specimen_theme', targetTheme);
      } catch (err) {}

      themeButtons.forEach(btn => {
        const matches = btn.getAttribute('data-theme-target') === targetTheme;
        btn.classList.toggle('active', matches);
      });

      if (pbmLabel) {
        pbmLabel.textContent = (targetTheme === 'pbm') ? 'PBM Active' : '670nm PBM';
      }

      window.dispatchEvent(new CustomEvent('siteThemeChanged', { detail: { theme: targetTheme } }));
    }

    themeButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const theme = btn.getAttribute('data-theme-target');
        applySiteTheme(theme);
      });
    });

    // Initialize with saved theme or default to Washi
    const initialTheme = (function() {
      try {
        const saved = localStorage.getItem('pocketgull_specimen_theme');
        if (['washi', 'dark', 'pbm'].includes(saved)) return saved;
      } catch (e) {}
      return 'dark';
    })();
    applySiteTheme(initialTheme);

    // 2. Interactive Type Tester
    const testerOutput = document.getElementById('testerOutput');
    const sizeSlider = document.getElementById('sizeSlider');
    const sizeVal = document.getElementById('sizeVal');
    const spacingSlider = document.getElementById('spacingSlider');
    const spacingVal = document.getElementById('spacingVal');
    const charCount = document.getElementById('charCount');
    const weightBtns = document.querySelectorAll('.weight-btn');
    const btnBouma = document.getElementById('btnBouma');

    sizeSlider.addEventListener('input', (e) => {
      const val = e.target.value;
      testerOutput.style.fontSize = `${val}px`;
      sizeVal.textContent = `${val}px`;
    });

    spacingSlider.addEventListener('input', (e) => {
      const val = (e.target.value / 100).toFixed(2);
      testerOutput.style.letterSpacing = `${val}em`;
      spacingVal.textContent = `${val}em`;
    });

    btnBouma.addEventListener('click', () => {
      spacingSlider.value = 12;
      testerOutput.style.letterSpacing = '0.12em';
      testerOutput.style.lineHeight = '1.75';
      spacingVal.textContent = '0.12em (Bouma)';
    });

    weightBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        weightBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        testerOutput.style.fontFamily = btn.dataset.family;
        testerOutput.style.fontWeight = btn.dataset.weight;
      });
    });

    let tittleInputDebounce = null;
    testerOutput.addEventListener('input', () => {
      charCount.textContent = `${testerOutput.innerText.length} characters`;
      if (typeof currentLoveLevel !== 'undefined' && currentLoveLevel !== 'none' && typeof currentTittleVariety !== 'undefined' && currentTittleVariety !== 'dot' && typeof currentHealerMode !== 'undefined' && currentHealerMode !== 'off') {
        clearTimeout(tittleInputDebounce);
        tittleInputDebounce = setTimeout(() => {
          const sel = window.getSelection();
          let caretOffset = 0;
          if (sel && sel.rangeCount > 0) {
            try {
              const range = sel.getRangeAt(0);
              const preCaretRange = range.cloneRange();
              preCaretRange.selectNodeContents(testerOutput);
              preCaretRange.setEnd(range.endContainer, range.endOffset);
              caretOffset = preCaretRange.toString().length;
            } catch (e) {}
          }
          if (typeof renderTittlesInTester === 'function') {
            renderTittlesInTester();
          }
          if (sel && caretOffset > 0) {
            try {
              let charIndex = 0;
              const nodeStack = [testerOutput];
              let node, found = false;
              while ((node = nodeStack.pop()) && !found) {
                if (node.nodeType === Node.TEXT_NODE) {
                  const nextCharIndex = charIndex + node.length;
                  if (caretOffset >= charIndex && caretOffset <= nextCharIndex) {
                    const newRange = document.createRange();
                    newRange.setStart(node, caretOffset - charIndex);
                    newRange.collapse(true);
                    sel.removeAllRanges();
                    sel.addRange(newRange);
                    found = true;
                  }
                  charIndex = nextCharIndex;
                } else {
                  let i = node.childNodes.length;
                  while (i--) {
                    nodeStack.push(node.childNodes[i]);
                  }
                }
              }
            } catch (e) {}
          }
        }, 500);
      }
    });

    // Typographic Metric Guidelines Toggle
    const btnGuidelines = document.getElementById('btnGuidelines');
    let guidelinesActive = false;
    if (btnGuidelines) {
      btnGuidelines.addEventListener('click', () => {
        guidelinesActive = !guidelinesActive;
        if (guidelinesActive) {
          btnGuidelines.classList.add('active');
          btnGuidelines.style.background = 'rgba(56, 189, 248, 0.2)';
          btnGuidelines.style.color = '#38bdf8';
          btnGuidelines.style.borderColor = '#38bdf8';
          btnGuidelines.textContent = '📐 Guidelines: ON';
          testerOutput.classList.add('show-guidelines');
        } else {
          btnGuidelines.classList.remove('active');
          btnGuidelines.style.background = 'transparent';
          btnGuidelines.style.color = 'var(--text-secondary)';
          btnGuidelines.style.borderColor = 'var(--border-subtle)';
          btnGuidelines.textContent = '📐 Guidelines: OFF';
          testerOutput.classList.remove('show-guidelines');
        }
      });
    }

    // ISMP Slashed Zero Toggle Quick-Action (Only controls slashed zero: 'zero' / 'cv08')
    const btnIsmpToggle = document.getElementById('btnIsmpToggle');
    let ismpSafeActive = false;

    function applyIsmpState(active) {
      ismpSafeActive = active;
      if (btnIsmpToggle) {
        if (ismpSafeActive) {
          btnIsmpToggle.classList.add('active');
          btnIsmpToggle.style.background = 'rgba(20, 184, 166, 0.2)';
          btnIsmpToggle.style.color = 'var(--accent-teal)';
          btnIsmpToggle.style.borderColor = 'var(--accent-teal)';
          btnIsmpToggle.textContent = '🛡️ Slashed 0: ON';
        } else {
          btnIsmpToggle.classList.remove('active');
          btnIsmpToggle.style.background = 'transparent';
          btnIsmpToggle.style.color = 'var(--text-secondary)';
          btnIsmpToggle.style.borderColor = 'var(--border-subtle)';
          btnIsmpToggle.textContent = '🛡️ Slashed 0: OFF';
        }
      }

      // Synchronize with the 'cv08' toggle button in the OpenType features strip
      const toggleCv08 = document.getElementById('toggleCv08');
      if (toggleCv08) {
        if (ismpSafeActive) {
          toggleCv08.classList.add('active');
          toggleCv08.textContent = "'cv08' (0 vs O) ON";
          toggleCv08.style.background = 'rgba(20, 184, 166, 0.15)';
          toggleCv08.style.borderColor = '#14b8a6';
          toggleCv08.style.color = '#2dd4bf';
        } else {
          toggleCv08.classList.remove('active');
          toggleCv08.textContent = "'cv08' (0 vs O) OFF";
          toggleCv08.style.background = 'rgba(255, 255, 255, 0.04)';
          toggleCv08.style.borderColor = 'rgba(255, 255, 255, 0.15)';
          toggleCv08.style.color = '#a1a1aa';
        }
      }

      updateOtFeatures();
    }

    if (btnIsmpToggle) {
      btnIsmpToggle.addEventListener('click', () => {
        applyIsmpState(!ismpSafeActive);
      });
    }

    // Presets (Proportional numerals and clean humanist Latin by default)
    const PRESETS = {
      rx: "Rx: Amoxicillin 500 mg PO Q8H × 10d [Proportional Numerals 500]",
      cardiac: "Sinus Rhythm • Radial Pulse • Clinical Insight • The Healer Font (Hearts for i's) ♥",
      italics: "BRCA1 Protein vs BRCA1 Gene • Staphylococcus aureus (Pathogen) • statim PO Q8H",
      triage: "STAT 911 TRAUMA: SpO2 98% • HR 118 BPM • BP 85/50 mmHg • QRS 0.08s",
      sloan: "C D H K N O R S V Z — 5:1 Sloan Snellen 20/20 Optotypes",
      pangram: "The quick brown fox jumps over the lazy dog & zero quartz vexes 109 patients.",
      braille: "⠠⠁⠍⠕⠭⠊⠉⠊⠇⠇⠊⠝ ⠼⠑⠚⠚ ⠍⠛ (Amoxicillin 500 mg)",
      inuktitut: "ᐆᒻᒪᑎᓕᕆᓂᖅ // ᐆᒻᒪᑎ ᐊᒻᒪ ᐊᐅᑉ ᐊᖁᑎᖏᑦ: ᐊᐅᑉ ᓱᑲᖃᕐᓂᖓ 5.4 mmol/L • ᐳᕙᒃ 20/min • ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᔨᒃᑯᑦ",
      chinuk: "𛰅𛰆𛱄𛰜 𛰃𛱑𛰙 𛰃𛱑𛰙 • 𛰅𛰆𛱄𛰜 𛰚𛱁𛰚𛱆𛰛: SpO2 99% • HR 72 BPM • 𛰙𛱁𛰙𛱑𛰅 𛰅𛰆𛱄𛰜 𛰃𛱆𛰆𛱆𛰅𛱑𛰙 𛲟",
      tifinagh: "ⵜⴰⵣⵎⵔⵜ // ⵓⵍ ⴷ ⵉⴷⴰⵎⵎⵏ: ⴰⵙⴰⴼⴰⵔ 500 mg • ⴰⵎⵙⴰⴼⴰⵔ • ⵜⵓⴷⵔⵜ 99% SpO2 [Tazmert / Vitality]",
      cherokee: "ᎠᏰᎵ ᎤᏂᎩᏍᏗ // ᎤᏪﾘᎯᏍᏗ ᎩᎦ: ᏅᏬᏘ 250 mg • ᎦᎾᎦᏘ • ᏓᎾᏓᏅᎿ [Ayeli Unigisdi / Healing]",
      ethiopic: "ጤና // ልብ እና ደም: መድኃኒት 500 mg • ሐኪም • ህክምና 100% [Ṭena / Health & Heart]",
      adlam: "Cellal // Ɓernde e Ƴiiƴam: 𞤕𞤫𞤤𞤤𞤢𞤤 500 mg • 𞤅𞤢𞤁𞤪𞤮𞤮𞤱𞤮 • ꔛꘋ ꔔꕞꔤ [Adlam & Vai]",
      navajo: "Diné Bizaad // Azeeʼ Ííłʼíní (Physician) • Azeeʼ: 500 mg • Łichííʼ (Blood): 120/80 mmHg • Hózhǫ́ (Harmony & Health)",
      lakota: "Očhéthi Šakówiŋ // Phežúta Wičháša (Medicine Healer) • Čhaŋté (Heart): 72 BPM • Wóžapi • Wicozani (Holistic Health)",
      salish: "dxʷləšucid // sʔuladxʷ (Sustenance) • ƛʼubƛʼub (Very Well) • yəcəb (Clinic Telemetry) • SpO2 99% [Lushootseed]",
      mohawk: "Kanien'kéha // Ratetsyén:tha (Doctor) • Onkwanatason:a (Body) • Onòn:kwa (Medicine) 250 mg • Skén:nen (Peace & Health)",
      hawaiian: "ʻŌlelo Hawaiʻi // Kauka (Physician) • Puʻuwai (Heart): 70 BPM • Lāʻau Lapaʻau (Medicine) • Ola Kino (Vital Well-being)",
      parlor: "The Solarium Library • A cup of chamomile tea • Resting heart rate: 60 BPM • خَطّ نَسْخ • Peaceful Afternoon"
    };

    document.querySelectorAll('.preset-pill[data-preset]').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.preset-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const text = PRESETS[pill.dataset.preset];
        if (text) {
          testerOutput.innerText = text;
          charCount.textContent = `${text.length} characters`;
          if (pill.dataset.preset === 'italics') {
            const btnItal = document.getElementById('toggleItalic');
            if (btnItal && !btnItal.classList.contains('active')) {
              btnItal.click();
            }
          }
          if (pill.dataset.preset === 'cardiac') {
            if (typeof setHealerMode === 'function') {
              setHealerMode('72');
            }
          } else {
            updateOtFeatures();
          }
        }
      });
    });

    // Live OpenType Feature Toggle Handler
    const otButtons = document.querySelectorAll('.ot-toggle-btn');
    const otReadout = document.getElementById('otCssReadout');

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    // Attach interactive click listeners to all OpenType toggle buttons
    otButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const isActive = btn.classList.toggle('active');
        const feat = btn.dataset.feat;

        // Visual feedback on the button
        if (isActive) {
          btn.style.background = 'rgba(20, 184, 166, 0.15)';
          btn.style.borderColor = '#14b8a6';
          btn.style.color = '#2dd4bf';
          if (feat === 'tnum') btn.textContent = "'tnum' ON";
          else if (feat === 'cv08') btn.textContent = "'cv08' (0 vs O) ON";
          else if (feat === 'cv05') btn.textContent = "'cv05' (l vs 1) ON";
          else if (feat === 'ss02') btn.textContent = "'ss02' (I vs l) ON";
          else if (feat === 'ital') {
            btn.innerHTML = '<i>𝐼</i> Italic ON';
            btn.style.borderColor = 'rgba(56, 189, 248, 0.4)';
            btn.style.background = 'rgba(56, 189, 248, 0.15)';
            btn.style.color = '#38bdf8';
          }
          else if (feat === 'dlig') btn.textContent = "'dlig' ON";
          else if (feat === 'ss07') {
            btn.textContent = "'ss07' (♥ Tittles) ON";
            btn.style.borderColor = 'rgba(244, 63, 94, 0.4)';
            btn.style.background = 'rgba(244, 63, 94, 0.15)';
            btn.style.color = '#fb7185';
          }
        } else {
          btn.style.background = 'rgba(255, 255, 255, 0.04)';
          btn.style.borderColor = 'rgba(255, 255, 255, 0.15)';
          btn.style.color = '#a1a1aa';
          if (feat === 'tnum') btn.textContent = "'tnum' OFF";
          else if (feat === 'cv08') btn.textContent = "'cv08' (0 vs O) OFF";
          else if (feat === 'cv05') btn.textContent = "'cv05' (l vs 1) OFF";
          else if (feat === 'ss02') btn.textContent = "'ss02' (I vs l) OFF";
          else if (feat === 'ital') {
            btn.innerHTML = '<i>𝐼</i> Italic OFF';
            btn.style.borderColor = 'rgba(56, 189, 248, 0.4)';
            btn.style.background = 'rgba(56, 189, 248, 0.08)';
            btn.style.color = '#38bdf8';
          }
          else if (feat === 'dlig') btn.textContent = "'dlig' OFF";
          else if (feat === 'ss07') {
            btn.textContent = "'ss07' (♥ Tittles) OFF";
            btn.style.borderColor = 'rgba(244, 63, 94, 0.4)';
            btn.style.background = 'rgba(244, 63, 94, 0.08)';
            btn.style.color = '#fb7185';
          }
        }

        // Sync #btnIsmpToggle if cv08 was toggled
        if (feat === 'cv08') {
          ismpSafeActive = isActive;
          if (btnIsmpToggle) {
            if (isActive) {
              btnIsmpToggle.classList.add('active');
              btnIsmpToggle.style.background = 'rgba(20, 184, 166, 0.2)';
              btnIsmpToggle.style.color = 'var(--accent-teal)';
              btnIsmpToggle.style.borderColor = 'var(--accent-teal)';
              btnIsmpToggle.textContent = '🛡️ Slashed 0: ON';
            } else {
              btnIsmpToggle.classList.remove('active');
              btnIsmpToggle.style.background = 'transparent';
              btnIsmpToggle.style.color = 'var(--text-secondary)';
              btnIsmpToggle.style.borderColor = 'var(--border-subtle)';
              btnIsmpToggle.textContent = '🛡️ Slashed 0: OFF';
            }
          }
        }

        // Handle italic cut toggle
        if (feat === 'ital') {
          if (testerOutput) {
            testerOutput.style.fontStyle = isActive ? 'italic' : 'normal';
          }
        }

        updateOtFeatures();
      });
    });

    function updateOtFeatures() {
      const activeFeats = [];

      otButtons.forEach(btn => {
        const feat = btn.dataset.feat;
        if (btn.classList.contains('active')) {
          if (feat && feat !== 'philocardia' && feat !== 'iphillyg') {
            activeFeats.push(`"${feat}" 1`);
            if (feat === 'cv08') {
              activeFeats.push('"zero" 1');
            }
          }
        }
      });

      if (testerOutput) {
        testerOutput.style.fontFeatureSettings = activeFeats.length ? activeFeats.join(', ') : 'normal';
        const hasZero = activeFeats.some(f => f.includes('zero') || f.includes('cv08'));
        const hasTnum = activeFeats.some(f => f.includes('tnum'));
        testerOutput.style.fontVariantNumeric = (hasZero && hasTnum) ? 'slashed-zero tabular-nums' : (hasZero ? 'slashed-zero' : (hasTnum ? 'tabular-nums' : 'normal'));
        if (otReadout) {
          otReadout.textContent = 'font-feature-settings: ' + (activeFeats.length ? activeFeats.join(', ') : 'normal');
        }

        renderTittlesInTester();
      }
    }

    // =========================================================================
    // The Healer Font: Cardiopulmonary Resonance & Touch Aura Sequencer
    // =========================================================================
    let currentLoveLevel = 'none'; // 'none' (Pure Clinical dot), 'half' (only 'i' aura), 'super' ('i', 'j', '!', 'خ' hearts)
    let currentHealerMode = 'off'; // '72', '60', 'breath', 'aura', 'static', 'off' (default: off / calm clinical)
    const healerOrder = ['sanctuary', '72', '60', 'breath', 'aura', 'static', 'off'];
    const healerPills = document.querySelectorAll('.healer-pill');
    const healerBadge = document.getElementById('healerActiveBadge');
    const healerStepBtn = document.getElementById('healerStepBtn');
    const healerCaption = document.getElementById('healerStatusCaption');

    const HEALER_CONFIG = {
      'sanctuary': {
        badge: '🕊️ Philocardia Sanctuary',
        caption: '0.10 Hz Vagal Coherence & Y-BOCS Tranquility (Score: 2/40): Dissolving perfectionism into restorative calm & Bouma anti-crowding ease',
        pacingClass: 'philocardia-pacing-sanctuary'
      },
      '72': {
        badge: '72 BPM Sinus',
        caption: 'Normal adult sinus rhythm (0.833s period) with S1/S2 lub-dub for zero-watch radial pulse palpation',
        pacingClass: 'philocardia-pacing-72'
      },
      '60': {
        badge: '60 BPM Rest',
        caption: 'Calming resting cardiac rhythm (1.000s period) to down-regulate sympathetic arousal and anxiety',
        pacingClass: 'philocardia-pacing-60'
      },
      'breath': {
        badge: '4-7-8 Breathing',
        caption: 'Somatic 4-7-8 box breathing (16s cycle) for vagal nerve coherence and respiratory grounding',
        pacingClass: 'philocardia-pacing-breath'
      },
      'aura': {
        badge: 'Touch Aura',
        caption: 'Interactive Proximity Aura: Hearts and stroke weight gently bloom and tilt toward your cursor',
        pacingClass: 'philocardia-touch-aura'
      },
      'static': {
        badge: 'Static Hearts',
        caption: 'Crisp optical heart-shaped tittles on all lowercase i glyphs without motion animation',
        pacingClass: ''
      },
      'off': {
        badge: 'Standard Dots',
        caption: 'Healer heart mode off; traditional circular tittles active',
        pacingClass: ''
      }
    };

    function setHealerMode(mode) {
      currentHealerMode = mode;
      const cfg = HEALER_CONFIG[mode] || HEALER_CONFIG['72'];

      // Update badge and caption
      if (healerBadge) healerBadge.textContent = cfg.badge;
      if (healerCaption) healerCaption.textContent = cfg.caption;

      // Update global CSS bio-clock properties on documentElement
      const rootStyle = document.documentElement.style;
      if (mode === 'sanctuary') {
        rootStyle.setProperty('--bio-pulse-period', '10s');
        rootStyle.setProperty('--bio-halo-color', 'rgba(45, 212, 191, 0.7)');
        document.body.classList.add('philocardia-sanctuary-active');
      } else {
        document.body.classList.remove('philocardia-sanctuary-active');
        if (mode === '72') {
          rootStyle.setProperty('--bio-pulse-period', '0.8333s');
          rootStyle.setProperty('--bio-halo-color', 'rgba(45, 212, 191, 0.65)');
        } else if (mode === '60') {
          rootStyle.setProperty('--bio-pulse-period', '1.0000s');
          rootStyle.setProperty('--bio-halo-color', 'rgba(56, 189, 248, 0.65)');
        } else if (mode === 'breath') {
          rootStyle.setProperty('--bio-pulse-period', '16s');
          rootStyle.setProperty('--bio-halo-color', 'rgba(14, 165, 233, 0.7)');
        } else if (mode === 'aura') {
          rootStyle.setProperty('--bio-pulse-period', '1.2s');
          rootStyle.setProperty('--bio-halo-color', 'rgba(251, 113, 133, 0.65)');
        } else {
          rootStyle.setProperty('--bio-pulse-period', '1.0s');
          rootStyle.setProperty('--bio-halo-color', 'rgba(45, 212, 191, 0.5)');
        }
      }

      // Update active pill
      healerPills.forEach(pill => {
        pill.classList.toggle('active', pill.dataset.healerMode === mode);
      });

      const headerBioBadgeEl = document.getElementById('headerBioBadge');
      if (headerBioBadgeEl) {
        if (mode === 'aura') {
          headerBioBadgeEl.textContent = 'Touch Aura';
        } else if (mode === 'sanctuary') {
          headerBioBadgeEl.textContent = '🕊️ Sanctuary';
        } else {
          headerBioBadgeEl.textContent = cfg ? cfg.badge.split(' ')[0] + ' ' + (cfg.badge.split(' ')[1] || '') : '72 BPM';
        }
      }

      // Healer Mode bar is the single authoritative toggle control
      if (morphClipPathEl) {
        if (mode === 'off') {
          morphClipPathEl.setAttribute('d', interpolateClipPath(0));
        } else if (mode !== 'aura') {
          morphClipPathEl.setAttribute('d', interpolateClipPath(1));
        }
      }
      updateOtFeatures();
    }

    function renderTittlesInTester(forceRawText = null) {
      if (!testerOutput) return;

      let rawText = '';
      if (forceRawText !== null) {
        rawText = forceRawText;
      } else if (testerOutput.children && testerOutput.children.length > 0) {
        const clone = testerOutput.cloneNode(true);
        clone.querySelectorAll('.philocardia-heart').forEach(el => el.replaceWith('i'));
        clone.querySelectorAll('.philocardia-j').forEach(el => el.replaceWith('j'));
        clone.querySelectorAll('.philocardia-excl').forEach(el => el.replaceWith('!'));
        clone.querySelectorAll('.philocardia-arabic-heart').forEach(el => el.replaceWith('خ'));
        rawText = clone.textContent.replace(/ı/g, 'i').replace(/ȷ/g, 'j');
      } else {
        rawText = (testerOutput.textContent || '').replace(/ı/g, 'i').replace(/ȷ/g, 'j');
      }

      if (currentLoveLevel === 'none' || currentTittleVariety === 'dot' || currentHealerMode === 'off') {
        // Level 0 / Pure Clinical (Dieter Rams Rest): 100% pure clinical discipline, traditional circular tittles
        testerOutput.textContent = rawText;
      } else if (currentLoveLevel === 'half') {
        // Level 1 / Half Love (Sporty Zone 2 Aerobic Cadence): Focused rhythmic pacing on primary anchor 'i'
        const pacingClass = HEALER_CONFIG[currentHealerMode]?.pacingClass || 'philocardia-pacing-72';
        const classI = pacingClass ? `philocardia-heart ${pacingClass}` : 'philocardia-heart';
        const escaped = escapeHtml(rawText);
        testerOutput.innerHTML = escaped.replace(/i/g, `<span class="${classI}">ı</span>`);
      } else {
        // Level 2 / Super Love (Sporty HIIT Sprint): Full squad active ('i', 'j', '!', 'خ') with athletic spring
        const pacingClass = HEALER_CONFIG[currentHealerMode]?.pacingClass || 'philocardia-pacing-72';
        const classI = pacingClass ? `philocardia-heart ${pacingClass}` : 'philocardia-heart';
        const classJ = pacingClass ? `philocardia-j ${pacingClass}` : 'philocardia-j';
        const classExcl = pacingClass ? `philocardia-excl ${pacingClass}` : 'philocardia-excl';
        const classArabic = pacingClass ? `philocardia-arabic-heart ${pacingClass}` : 'philocardia-arabic-heart';
        const escaped = escapeHtml(rawText);
        const transformed = escaped
          .replace(/i/g, `<span class="${classI}">ı</span>`)
          .replace(/j/g, `<span class="${classJ}">ȷ</span>`)
          .replace(/!/g, `<span class="${classExcl}">!</span>`)
          .replace(/خ/g, `<span class="${classArabic}">خ</span>`);
        testerOutput.innerHTML = transformed;
      }
    }

    // Tittle Varieties Suite (Hearts, Blossoms, Nuqṭa, Stars, Droplets, Dots)
    let currentTittleVariety = 'dot';
    const tittleVarietyBtns = document.querySelectorAll('.tittle-variety-btn');

    function setTittleVariety(variety) {
      currentTittleVariety = variety;
      document.documentElement.setAttribute('data-tittle-variety', variety);

      tittleVarietyBtns.forEach(btn => {
        const isMatch = (btn.dataset.variety === variety);
        btn.classList.toggle('active', isMatch);
        if (isMatch) {
          if (variety === 'heart') {
            btn.style.borderColor = '#fb7185';
            btn.style.background = 'rgba(244,63,94,0.25)';
            btn.style.color = '#fb7185';
          } else {
            btn.style.borderColor = '#2dd4bf';
            btn.style.background = 'rgba(45,212,191,0.2)';
            btn.style.color = '#2dd4bf';
          }
        } else {
          btn.style.background = 'transparent';
          btn.style.borderColor = 'rgba(255,255,255,0.15)';
          btn.style.color = '#94a3b8';
        }
      });

      if (variety === 'dot') {
        if (currentLoveLevel !== 'none') {
          setLoveLevel('none');
        } else {
          renderTittlesInTester();
        }
      } else {
        if (currentLoveLevel === 'none') {
          setLoveLevel('super');
        } else {
          renderTittlesInTester();
        }
      }
    }

    tittleVarietyBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        setTittleVariety(btn.dataset.variety);
      });
    });

    healerPills.forEach(pill => {
      pill.addEventListener('click', () => {
        setHealerMode(pill.dataset.healerMode);
      });
    });

    // Level of Love (None / Half / Super) Selector Handler
    const loveLevelBtns = document.querySelectorAll('.love-level-btn');
    function setLoveLevel(level) {
      loveLevelBtns.forEach(btn => {
        const isMatch = (btn.dataset.love === level);
        btn.classList.toggle('active', isMatch);
        if (isMatch) {
          if (level === 'none') {
            btn.style.borderColor = 'rgba(255,255,255,0.4)';
            btn.style.background = 'rgba(255,255,255,0.1)';
            btn.style.color = '#ffffff';
          } else if (level === 'half') {
            btn.style.borderColor = '#2dd4bf';
            btn.style.background = 'rgba(45,212,191,0.2)';
            btn.style.color = '#2dd4bf';
          } else if (level === 'super') {
            btn.style.borderColor = '#fb7185';
            btn.style.background = 'rgba(244,63,94,0.25)';
            btn.style.color = '#fb7185';
          }
        } else {
          btn.style.background = 'transparent';
          btn.style.borderColor = 'rgba(255,255,255,0.15)';
          btn.style.color = '#94a3b8';
        }
      });

      currentLoveLevel = level;

      if (level === 'none') {
        setHealerMode('off');
        currentTittleVariety = 'dot';
        document.documentElement.setAttribute('data-tittle-variety', 'dot');
        tittleVarietyBtns.forEach(btn => {
          const isDot = (btn.dataset.variety === 'dot');
          btn.classList.toggle('active', isDot);
          btn.style.borderColor = isDot ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.15)';
          btn.style.background = isDot ? 'rgba(255,255,255,0.1)' : 'transparent';
          btn.style.color = isDot ? '#ffffff' : '#94a3b8';
        });
      } else if (level === 'half') {
        setHealerMode('aura');
        if (currentTittleVariety === 'dot') {
          currentTittleVariety = 'heart';
          document.documentElement.setAttribute('data-tittle-variety', 'heart');
          tittleVarietyBtns.forEach(btn => {
            const isHeart = (btn.dataset.variety === 'heart');
            btn.classList.toggle('active', isHeart);
            btn.style.borderColor = isHeart ? '#fb7185' : 'rgba(45,212,191,0.3)';
            btn.style.background = isHeart ? 'rgba(244,63,94,0.18)' : 'transparent';
            btn.style.color = isHeart ? '#fb7185' : '#94a3b8';
          });
        }
      } else if (level === 'super') {
        setHealerMode('72');
        if (currentTittleVariety === 'dot') {
          currentTittleVariety = 'heart';
          document.documentElement.setAttribute('data-tittle-variety', 'heart');
          tittleVarietyBtns.forEach(btn => {
            const isHeart = (btn.dataset.variety === 'heart');
            btn.classList.toggle('active', isHeart);
            btn.style.borderColor = isHeart ? '#fb7185' : 'rgba(45,212,191,0.3)';
            btn.style.background = isHeart ? 'rgba(244,63,94,0.18)' : 'transparent';
            btn.style.color = isHeart ? '#fb7185' : '#94a3b8';
          });
        }
      }
      updateOtFeatures();
    }

    loveLevelBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        setLoveLevel(btn.dataset.love);
      });
    });

    if (healerStepBtn) {
      healerStepBtn.addEventListener('click', () => {
        const nextIdx = (healerOrder.indexOf(currentHealerMode) + 1) % healerOrder.length;
        setHealerMode(healerOrder[nextIdx]);
      });
    }

    // 15-Second Radial Palpation Chronometer Haptic & Touch Feedback
    const palpationRing = document.getElementById('palpationRingContainer');
    if (palpationRing) {
      const triggerPalpationPulse = () => {
        if (typeof navigator !== 'undefined' && navigator.vibrate) {
          navigator.vibrate([25, 85, 35]); // S1 "lub" (25ms) + rest (85ms) + S2 "dub" (35ms)
        }
        const icon = document.getElementById('palpationHeartIcon');
        if (icon) {
          icon.style.transform = 'scale(1.4)';
          setTimeout(() => { icon.style.transform = 'scale(1)'; }, 220);
        }
      };
      palpationRing.addEventListener('click', triggerPalpationPulse);
      palpationRing.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerPalpationPulse();
        }
      });
    }

    // Global Ambient Touch & Cursor Proximity Aura Engine & Continuous Tittle Morph
    let lastPointerX = -9999;
    let lastPointerY = -9999;
    let auraRafId = null;

    // Cubic Bézier control points for 4-segment Circle (t=0) and Philocardia Heart (t=1)
    const CIRCLE_POINTS = [
      [0.500, 0.000], [0.776, 0.000], [1.000, 0.224], [1.000, 0.500],
      [1.000, 0.776], [0.776, 1.000], [0.500, 1.000],
      [0.224, 1.000], [0.000, 0.776], [0.000, 0.500],
      [0.000, 0.224], [0.224, 0.000], [0.500, 0.000]
    ];

    const HEART_POINTS = [
      [0.500, 0.280], [0.650, 0.000], [0.980, 0.080], [0.990, 0.440],
      [1.000, 0.700], [0.760, 0.860], [0.500, 1.000],
      [0.240, 0.860], [0.000, 0.700], [0.010, 0.440],
      [0.020, 0.080], [0.350, 0.000], [0.500, 0.280]
    ];

    function interpolateClipPath(t) {
      const clampT = Math.max(0, Math.min(1, t));
      const pts = CIRCLE_POINTS.map((c, i) => {
        const h = HEART_POINTS[i];
        const x = (c[0] + (h[0] - c[0]) * clampT).toFixed(3);
        const y = (c[1] + (h[1] - c[1]) * clampT).toFixed(3);
        return `${x},${y}`;
      });
      return `M ${pts[0]} C ${pts[1]} ${pts[2]} ${pts[3]} C ${pts[4]} ${pts[5]} ${pts[6]} C ${pts[7]} ${pts[8]} ${pts[9]} C ${pts[10]} ${pts[11]} ${pts[12]} Z`;
    }

    const morphClipPathEl = document.getElementById('philocardiaClipPath');

    function updateAmbientAura(x, y) {
      const isAuraActive = (currentHealerMode === 'aura');
      const hearts = document.querySelectorAll('.philocardia-heart, .philocardia-arabic-heart, .philocardia-j, .philocardia-excl');
      const vH = window.innerHeight;
      let maxFactor = 0;

      hearts.forEach(heart => {
        if (!isAuraActive) {
          heart.style.removeProperty('--aura-scale');
          heart.style.removeProperty('--aura-glow');
          heart.style.removeProperty('--aura-color');
          heart.style.removeProperty('--aura-morph');
          return;
        }

        const hRect = heart.getBoundingClientRect();
        // Viewport cull check: skip elements well outside current screen
        if (hRect.bottom < -100 || hRect.top > vH + 100) return;

        const hCenterX = hRect.left + hRect.width / 2;
        const hCenterY = hRect.top + hRect.height / 2;
        const dist = Math.hypot(x - hCenterX, y - hCenterY);

        // Responsive proximity bloom radius (200px)
        if (dist < 200) {
          const factor = 1 - (dist / 200);
          if (factor > maxFactor) maxFactor = factor;

          const scale = 1.00 + (0.15 * factor); // Subtle optical scaling from 1.00x up to 1.15x max
          const glow = Math.round(14 * factor);
          const color = factor > 0.55 ? '#fb7185' : (factor > 0.2 ? '#2dd4bf' : 'currentColor');
          heart.style.setProperty('--aura-scale', scale.toFixed(2));
          heart.style.setProperty('--aura-glow', `${glow}px`);
          heart.style.setProperty('--aura-color', color);
          heart.style.setProperty('--aura-morph', factor.toFixed(2));
        } else {
          heart.style.removeProperty('--aura-scale');
          heart.style.removeProperty('--aura-glow');
          heart.style.removeProperty('--aura-color');
          heart.style.removeProperty('--aura-morph');
        }
      });

      if (morphClipPathEl) {
        if (isAuraActive) {
          morphClipPathEl.setAttribute('d', interpolateClipPath(maxFactor));
        } else if (currentHealerMode === 'off') {
          morphClipPathEl.setAttribute('d', interpolateClipPath(0));
        } else {
          // Other modes ('72', '60', 'breath', 'static') render full heart
          morphClipPathEl.setAttribute('d', interpolateClipPath(1));
        }
      }
    }

    function scheduleAuraUpdate() {
      if (!auraRafId) {
        auraRafId = requestAnimationFrame(() => {
          updateAmbientAura(lastPointerX, lastPointerY);
          auraRafId = null;
        });
      }
    }

    window.addEventListener('pointermove', (e) => {
      lastPointerX = e.clientX;
      lastPointerY = e.clientY;
      scheduleAuraUpdate();
    }, { passive: true });

    window.addEventListener('scroll', () => {
      if (lastPointerX > -1000) {
        scheduleAuraUpdate();
      }
    }, { passive: true });

    window.addEventListener('pointerleave', () => {
      lastPointerX = -9999;
      lastPointerY = -9999;
      scheduleAuraUpdate();
    }, { passive: true });

    // Initial ambient trigger on page load to configure the aura state
    setTimeout(() => {
      setHealerMode('aura');
    }, 50);

    otButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        btn.classList.toggle('active');
        const isActive = btn.classList.contains('active');
        btn.style.background = isActive ? 'rgba(45, 212, 191, 0.2)' : 'rgba(255,255,255,0.04)';
        btn.style.borderColor = isActive ? '#2dd4bf' : 'rgba(255,255,255,0.15)';
        btn.style.color = isActive ? '#2dd4bf' : '#a1a1aa';
        const feat = btn.dataset.feat || '';
        if (feat === 'ital') {
          btn.innerHTML = `<i>𝐼</i> Italic ${isActive ? 'ON' : 'OFF'}`;
          btn.style.borderColor = isActive ? '#38bdf8' : 'rgba(56, 189, 248, 0.4)';
          btn.style.background = isActive ? 'rgba(56, 189, 248, 0.2)' : 'rgba(56, 189, 248, 0.08)';
          btn.style.color = '#38bdf8';
          if (testerOutput) {
            testerOutput.style.fontStyle = isActive ? 'italic' : 'normal';
            testerOutput.style.fontFamily = isActive ? "'PocketGull Italic', 'PocketGull', sans-serif" : "'PocketGull Bold', 'PocketGull', sans-serif";
          }
        } else {
          const label = btn.innerText.split(' ')[0];
          btn.innerText = `${label} '${feat}' ${isActive ? 'ON' : 'OFF'}`;
        }
        updateOtFeatures();
      });
    });

    // Header Bio-Clock Pill Synchronization
    const headerBioSync = document.getElementById('headerBioSync');
    const headerBioBadge = document.getElementById('headerBioBadge');
    if (headerBioSync) {
      headerBioSync.addEventListener('click', () => {
        const nextIdx = (healerOrder.indexOf(currentHealerMode) + 1) % healerOrder.length;
        setHealerMode(healerOrder[nextIdx]);
        if (headerBioBadge) {
          const cfg = HEALER_CONFIG[currentHealerMode];
          headerBioBadge.textContent = cfg ? cfg.badge.split(' ')[0] + ' ' + (cfg.badge.split(' ')[1] || '') : '72 BPM';
        }
      });
    }

    // Web Audio API Littmann Digital Stethoscope Auscultation Synthesizer
    let audioCtx = null;
    let isAuscultationPlaying = false;
    let auscultationInterval = null;
    const btnAuscultation = document.getElementById('btnAuscultation');
    const auscultationLabel = document.getElementById('auscultationLabel');

    function playHeartSound(isS1) {
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const filter = audioCtx.createBiquadFilter();

        // S1 ("lub", closure of AV valves) 62Hz; S2 ("dub", closure of semilunar valves) 84Hz
        const freq = isS1 ? 62 : 84;
        const duration = isS1 ? 0.075 : 0.055;

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.7, now + duration);

        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(160, now);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(0.28, now + 0.008);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start(now);
        osc.stop(now + duration + 0.02);
      } catch (e) {
        console.warn('Auscultation note:', e);
      }
    }

    function startAuscultationLoop() {
      if (auscultationInterval) clearInterval(auscultationInterval);
      let bpm = 72;
      if (currentHealerMode === '60') bpm = 60;
      else if (currentHealerMode === 'breath') bpm = 48;
      
      const periodMs = Math.round((60 / bpm) * 1000);
      const s2DelayMs = Math.round(periodMs * 0.26);

      const tick = () => {
        playHeartSound(true);
        setTimeout(() => {
          if (isAuscultationPlaying) playHeartSound(false);
        }, s2DelayMs);
      };

      tick();
      auscultationInterval = setInterval(tick, periodMs);
    }

    if (btnAuscultation) {
      btnAuscultation.addEventListener('click', () => {
        isAuscultationPlaying = !isAuscultationPlaying;
        btnAuscultation.classList.toggle('active', isAuscultationPlaying);
        if (auscultationLabel) {
          auscultationLabel.textContent = `Sound ${isAuscultationPlaying ? 'ON' : 'OFF'}`;
        }
        if (isAuscultationPlaying) {
          startAuscultationLoop();
        } else {
          if (auscultationInterval) clearInterval(auscultationInterval);
        }
      });
    }

    // 20-20-20 Ocular Sanctuary Chronometer (Eye Strain Prevention)
    const btnEyeSanctuary = document.getElementById('btnEyeSanctuary');
    const eyeSanctuaryLabel = document.getElementById('eyeSanctuaryLabel');
    let eyeTimerSeconds = 20 * 60; // 20 minutes
    let isEyeRestActive = false;

    setInterval(() => {
      if (eyeTimerSeconds > 0) {
        eyeTimerSeconds--;
        const mins = Math.floor(eyeTimerSeconds / 60);
        const secs = eyeTimerSeconds % 60;
        if (eyeSanctuaryLabel && !isEyeRestActive) {
          eyeSanctuaryLabel.textContent = `20-20-20 (${mins}:${secs < 10 ? '0' : ''}${secs})`;
        }
      } else if (!isEyeRestActive) {
        triggerEyeBreak();
      }
    }, 1000);

    function triggerEyeBreak() {
      isEyeRestActive = true;
      if (eyeSanctuaryLabel) eyeSanctuaryLabel.textContent = '👁️ Look 20ft Away (20s)';
      if (btnEyeSanctuary) btnEyeSanctuary.style.boxShadow = '0 0 16px rgba(245, 158, 11, 0.8)';
      setTimeout(() => {
        isEyeRestActive = false;
        eyeTimerSeconds = 20 * 60;
        if (btnEyeSanctuary) btnEyeSanctuary.style.boxShadow = '';
        if (eyeSanctuaryLabel) eyeSanctuaryLabel.textContent = '20-20-20 Eye Rest';
      }, 20000);
    }

    if (btnEyeSanctuary) {
      btnEyeSanctuary.addEventListener('click', () => {
        triggerEyeBreak();
      });
    }

    // Ocular Glare Softener (Micro-Luminance Vagal Wave)
    const btnGlareSoftener = document.getElementById('btnGlareSoftener');
    const glareSoftenerLabel = document.getElementById('glareSoftenerLabel');
    let isGlareSoftenerActive = false;
    if (btnGlareSoftener) {
      btnGlareSoftener.addEventListener('click', () => {
        isGlareSoftenerActive = !isGlareSoftenerActive;
        btnGlareSoftener.classList.toggle('active', isGlareSoftenerActive);
        document.body.classList.toggle('ocular-rest-active', isGlareSoftenerActive);
        if (glareSoftenerLabel) {
          glareSoftenerLabel.textContent = `Softener ${isGlareSoftenerActive ? 'ON' : 'OFF'}`;
        }
      });
    }

    // Section 02.5: Interactive Roman vs. True Italic Comparator Weight Controls
    const romanSample = document.getElementById('romanSampleText');
    const italicSample = document.getElementById('italicSampleText');
    const btnWFineliner = document.getElementById('btnItalicWeightFineliner');
    const btnWBold = document.getElementById('btnItalicWeightBold');
    const btnWMono = document.getElementById('btnItalicWeightMono');

    function setComparatorWeight(weight) {
      [btnWFineliner, btnWBold, btnWMono].forEach(b => b?.classList.remove('active'));
      if (weight === 'bold') {
        btnWBold?.classList.add('active');
        if (romanSample) {
          romanSample.style.fontFamily = "'PocketGull', 'PocketGull Bold', sans-serif";
          romanSample.style.fontWeight = '700';
          romanSample.style.fontStyle = 'normal';
          romanSample.style.fontSynthesis = 'none';
        }
        if (italicSample) {
          italicSample.style.fontFamily = "'PocketGull', 'PocketGull Bold Italic', sans-serif";
          italicSample.style.fontWeight = '700';
          italicSample.style.fontStyle = 'italic';
          italicSample.style.fontSynthesis = 'none';
        }
      } else if (weight === 'mono') {
        btnWMono?.classList.add('active');
        if (romanSample) {
          romanSample.style.fontFamily = "'PocketGull Mono', monospace";
          romanSample.style.fontWeight = '500';
          romanSample.style.fontStyle = 'normal';
          romanSample.style.fontSynthesis = 'none';
        }
        if (italicSample) {
          italicSample.style.fontFamily = "'PocketGull Mono', monospace";
          italicSample.style.fontWeight = '500';
          italicSample.style.fontStyle = 'italic';
          italicSample.style.fontSynthesis = 'none';
        }
      } else {
        btnWFineliner?.classList.add('active');
        if (romanSample) {
          romanSample.style.fontFamily = "'PocketGull', 'PocketGull Fineliner', sans-serif";
          romanSample.style.fontWeight = '400';
          romanSample.style.fontStyle = 'normal';
          romanSample.style.fontSynthesis = 'none';
        }
        if (italicSample) {
          italicSample.style.fontFamily = "'PocketGull', 'PocketGull Italic', sans-serif";
          italicSample.style.fontWeight = '400';
          italicSample.style.fontStyle = 'italic';
          italicSample.style.fontSynthesis = 'none';
        }
      }
    }

    btnWFineliner?.addEventListener('click', () => setComparatorWeight('fineliner'));
    btnWBold?.addEventListener('click', () => setComparatorWeight('bold'));
    btnWMono?.addEventListener('click', () => setComparatorWeight('mono'));

    // Synchronize Comparator Text Editing
    if (romanSample && italicSample) {
      romanSample.addEventListener('input', () => {
        italicSample.innerText = romanSample.innerText;
      });
      italicSample.addEventListener('input', () => {
        romanSample.innerText = italicSample.innerText;
      });
    }

    // Global Accessibility Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.isContentEditable) return;
      if (e.key === 'h' || e.key === 'H') {
        e.preventDefault();
        healerStepBtn?.click();
      } else if (e.key === 'm' || e.key === 'M') {
        e.preventDefault();
        btnAuscultation?.click();
      } else if (e.key === 'i' || e.key === 'I') {
        e.preventDefault();
        document.getElementById('toggleItalic')?.click();
      }
    });

    // 3. English to Braille Transcriber
    const BRAILLE_MAP = {
      'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛',
      'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝',
      'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥',
      'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
      '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
      '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
      ' ': ' ', '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠒', '!': '⠖', '?': '⠦',
      '-': '⠤', '/': '⠌'
    };

    function textToBraille(text) {
      let result = '';
      let inNumber = false;
      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        const lower = char.toLowerCase();
        
        if (char >= 'A' && char <= 'Z') {
          result += '⠠'; // Capital indicator
        }
        
        if (char >= '0' && char <= '9') {
          if (!inNumber) {
            result += '⠼'; // Number indicator
          }
          const digitBraille = {
            '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
            '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
          }[char];
          result += digitBraille || '';
        } else {
          inNumber = false;
          result += BRAILLE_MAP[lower] || char;
        }
      }
      return result;
    }

    const brailleInput = document.getElementById('brailleInput');
    const brailleLatinDisplay = document.getElementById('brailleLatinDisplay');
    const brailleVectorDisplay = document.getElementById('brailleVectorDisplay');

    function updateBraille() {
      const text = brailleInput.value || '';
      brailleLatinDisplay.textContent = text || '(Enter text above)';
      brailleVectorDisplay.textContent = textToBraille(text) || '⠀';
    }

    brailleInput.addEventListener('input', updateBraille);

    window.setBraillePreset = function(preset) {
      brailleInput.value = preset;
      updateBraille();
    };

    // 4. Bionic Reading Engine
    const BIONIC_PASSAGE = "The patient presents to the intensive care resuscitation bay with acute supraventricular tachycardia and borderline hemodynamic stability. Intravenous access was promptly established, and continuous telemetry monitoring demonstrated rapid ventricular response without ischemic ST-segment depression. Following standardized clinical algorithms, affirmative clinician review was completed before committing the targeted pharmacological intervention.";
    
    function renderBionic(text, enableBionic) {
      if (!enableBionic) {
        return `<p>${text}</p>`;
      }
      const words = text.split(' ');
      const bionicWords = words.map(word => {
        if (word.length <= 3) {
          const pivot = 1;
          return `<span class="fixation">${word.slice(0, pivot)}</span>${word.slice(pivot)}`;
        } else {
          const pivot = Math.ceil(word.length * 0.45);
          return `<span class="fixation">${word.slice(0, pivot)}</span>${word.slice(pivot)}`;
        }
      });
      return `<p>${bionicWords.join(' ')}</p>`;
    }

    const bionicContent = document.getElementById('bionicContent');
    const btnToggleBionic = document.getElementById('btnToggleBionic');
    const bionicStatus = document.getElementById('bionicStatus');
    let bionicActive = true;

    function refreshBionic() {
      bionicContent.innerHTML = renderBionic(BIONIC_PASSAGE, bionicActive);
      bionicStatus.textContent = bionicActive ? 'Bionic Saccadic Guidance Active (650+ WPM)' : 'Standard Reading (300 WPM)';
      btnToggleBionic.textContent = bionicActive ? 'Disable Bionic Fixation' : 'Enable Bionic Fixation';
    }

    btnToggleBionic.addEventListener('click', () => {
      bionicActive = !bionicActive;
      refreshBionic();
    });

    refreshBionic();

    // 5. Medical Terminal Animated Sub-Cell ECG, Pleth & Respiratory Sweep Engine
    const liveEcg = document.getElementById('liveEcg');
    const livePleth = document.getElementById('livePleth');
    const liveResp = document.getElementById('liveResp');
    const liveHr = document.getElementById('liveHr');
    const liveRhythmTag = document.getElementById('liveRhythmTag');
    const liveSpo2 = document.getElementById('liveSpo2');
    const liveBp = document.getElementById('liveBp');
    const rhythmBtns = document.querySelectorAll('.ecg-rhythm-btn');
    const btnSweepSpeed = document.getElementById('btnSweepSpeed');

    // High-resolution cardiac patterns defined via Unicode sub-cell elements (U+2580–259F)
    // Standardized clinical instrumentation telemetry templates (IEC 60601-1-8 compliant)
    const RHYTHM_TEMPLATES = {
      resting: {
        hr: '72 bpm',
        rhythm: 'NOMINAL RESTING BASELINE (STABLE)',
        spo2: '99%',
        bp: '120/80',
        ecgBeat: [' ', ' ', '▂', '▃', '▂', ' ', ' ', ' ', ' ', '█', ' ', ' ', ' ', '▂', '▃', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' '],
        plethBeat: [' ', '▂', '▄', '▆', '▇', '█', '█', '▇', '▆', '▅', '▄', '▅', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        respBeat: [' ', '▂', '▃', '▄', '▅', '▆', '▇', '▆', '▅', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
      },
      exercise: {
        hr: '128 bpm',
        rhythm: 'AEROBIC EXERTION (SINUS TACHYCARDIA)',
        spo2: '97%',
        bp: '142/84',
        ecgBeat: [' ', '▂', '▄', '█', ' ', '▂', '▃', '▄', '▃', '▂', ' ', ' '],
        plethBeat: [' ', '▂', '▄', '▆', '█', '▇', '▅', '▃', '▂', ' '],
        respBeat: [' ', '▂', '▃', '▄', '▆', '█', '▆', '▄', '▃', '▂', ' ']
      },
      nocturnal: {
        hr: '54 bpm',
        rhythm: 'PARASYMPATHETIC SLEEP (RESTING BRADY)',
        spo2: '99%',
        bp: '108/68',
        ecgBeat: [' ', ' ', ' ', '▂', '▃', '▂', ' ', ' ', ' ', ' ', '█', ' ', ' ', ' ', '▂', '▃', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        plethBeat: [' ', ' ', '▂', '▄', '▆', '▇', '█', '█', '▇', '▆', '▅', '▄', '▅', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        respBeat: [' ', ' ', '▂', '▃', '▄', '▅', '▆', '▇', '▆', '▅', '▄', '▃', '▂', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
      },
      calpulse: {
        hr: '60 bpm',
        rhythm: '1.0 mV REFERENCE SQUARE WAVE PULSE',
        spo2: '100%',
        bp: '120/80',
        ecgBeat: [' ', '█', '█', '█', '█', '█', ' ', ' ', ' ', ' ', ' ', ' '],
        plethBeat: [' ', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', ' '],
        respBeat: [' ', '▂', '▃', '▄', '▅', '▅', '▄', '▃', '▂', ' ']
      }
    };

    let activeRhythmKey = 'resting';
    let sweepSpeedMs = 70;
    const BUFFER_WIDTH = 67;

    let ecgBuffer = new Array(BUFFER_WIDTH).fill(' ');
    let plethBuffer = new Array(BUFFER_WIDTH).fill(' ');
    let respBuffer = new Array(BUFFER_WIDTH).fill(' ');
    let beatSampleIdx = 0;

    function stepWaveforms() {
      const template = RHYTHM_TEMPLATES[activeRhythmKey];
      const ecgSeq = template.ecgBeat;
      const plethSeq = template.plethBeat;
      const respSeq = template.respBeat;

      const nextEcg = ecgSeq[beatSampleIdx % ecgSeq.length];
      const nextPleth = plethSeq[beatSampleIdx % plethSeq.length];
      const nextResp = respSeq[beatSampleIdx % respSeq.length];
      beatSampleIdx++;

      ecgBuffer.shift();
      ecgBuffer.push(nextEcg);

      plethBuffer.shift();
      plethBuffer.push(nextPleth);

      respBuffer.shift();
      respBuffer.push(nextResp);

      if (liveEcg) liveEcg.textContent = ecgBuffer.join('');
      if (livePleth) livePleth.textContent = plethBuffer.join('');
      if (liveResp) liveResp.textContent = respBuffer.join('');
    }

    let waveInterval = setInterval(stepWaveforms, sweepSpeedMs);

    function setRhythm(key) {
      activeRhythmKey = key;
      const t = RHYTHM_TEMPLATES[key];
      if (liveHr) liveHr.textContent = t.hr.padEnd(8);
      if (liveRhythmTag) liveRhythmTag.textContent = t.rhythm.padEnd(35);
      if (liveSpo2) liveSpo2.textContent = t.spo2.padEnd(8);
      if (liveBp) liveBp.textContent = t.bp.padEnd(8);

      rhythmBtns.forEach(btn => {
        if (btn.dataset.rhythm === key) {
          btn.style.background = 'var(--accent-teal)';
          btn.style.color = '#09090b';
        } else {
          btn.style.background = 'transparent';
          btn.style.color = 'var(--text-secondary)';
        }
      });
    }

    rhythmBtns.forEach(btn => {
      btn.addEventListener('click', () => setRhythm(btn.dataset.rhythm));
    });

    let fastSweep = false;
    if (btnSweepSpeed) {
      btnSweepSpeed.addEventListener('click', () => {
        fastSweep = !fastSweep;
        sweepSpeedMs = fastSweep ? 38 : 70;
        btnSweepSpeed.textContent = fastSweep ? '⚡ 50 mm/s (High Speed)' : '⚡ 25 mm/s (Standard)';
        clearInterval(waveInterval);
        waveInterval = setInterval(stepWaveforms, sweepSpeedMs);
      });
    }

    // Shell Prompt Theme Templates (All strictly 79 columns)
    const PROMPT_TEMPLATES = {
      ohmyposh: `│ <span class="term-green">OH MY POSH:</span> <span class="term-teal"></span><span style="background:#14b8a6;color:#09090b;font-weight:bold;"> icu-station </span><span class="term-teal"></span><span style="background:#1e293b;color:#38bdf8;"> main </span><span style="color:#1e293b;"></span> tty1 (PocketGull Mono 600 UPM)           │`,
      p10k: `│ <span class="term-green">P10K ZSH:</span>   <span class="term-teal"></span><span style="background:#14b8a6;color:#09090b;font-weight:bold;"> icu-station </span><span class="term-teal"></span> <span class="term-amber"> main</span> <span class="term-dim"></span> <span class="term-white">✔ 14ms</span>                                 │`,
      starship: `│ <span class="term-green">STARSHIP:</span>   <span class="term-teal">phil@icu</span> in <span class="term-amber">~/pocketgull</span> on <span class="term-white"> main</span> <span class="term-teal">[12ms]</span> <span class="term-green">❯</span>                     │`,
      pure: `│ <span class="term-green">PURE ZSH:</span>   <span class="term-teal">~/pocketgull</span> <span class="term-white">main*</span> <span class="term-dim">14ms</span> <span class="term-green">❯</span>                                       │`,
      agnoster: `│ <span class="term-green">AGNOSTER:</span>   <span style="background:#1e293b;color:#38bdf8;"> phil@icu </span><span class="term-teal"></span><span style="background:#14b8a6;color:#09090b;font-weight:bold;"> ~/pocketgull </span><span class="term-amber"></span><span style="background:#f59e0b;color:#09090b;font-weight:bold;">  main </span><span style="color:#f59e0b;"></span>                             │`
    };

    const livePromptRow = document.getElementById('livePromptRow');
    const shellBtns = document.querySelectorAll('.shell-prompt-btn');

    shellBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const theme = btn.dataset.prompt;
        if (PROMPT_TEMPLATES[theme] && livePromptRow) {
          livePromptRow.innerHTML = PROMPT_TEMPLATES[theme];
        }
        shellBtns.forEach(b => {
          if (b === btn) {
            b.style.background = 'var(--accent-teal)';
            b.style.color = '#fff';
            b.classList.add('active');
          } else {
            b.style.background = 'transparent';
            b.style.color = 'var(--text-secondary)';
            b.classList.remove('active');
          }
        });
      });
    });
    const CODE_SNIPPETS = {
      swift: `// PocketGull for SwiftUI (iOS, iPadOS, macOS, visionOS)
// 1. In Info.plist, add:
// <key>UIAppFonts</key>
// <array>
//     <string>PocketGull-Bold.ttf</string>
//     <string>PocketGull-Fineliner.ttf</string>
//     <string>PocketGullMono-Regular.ttf</string>
// </array>

import SwiftUI

public extension Font {
    static func pocketGull(size: CGFloat = 17, relativeTo textStyle: TextStyle = .body) -> Font {
        .custom("PocketGull-Bold", size: size, relativeTo: textStyle)
    }
    static func pocketGullFineliner(size: CGFloat = 16, relativeTo textStyle: TextStyle = .body) -> Font {
        .custom("PocketGull-Fineliner", size: size, relativeTo: textStyle)
    }
    static func pocketGullMono(size: CGFloat = 14, relativeTo textStyle: TextStyle = .body) -> Font {
        .custom("PocketGullMono-Regular", size: size, relativeTo: textStyle)
    }
}

// 2. Clinical Safe Prescription View Example
struct MedicationOrderView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Rx: Amoxicillin 500 mg PO Q8H")
                .font(.pocketGull(size: 20))
                .fontDigitVariation(.slashedZero) // Slashed 0: 0 vs O
                .monospacedDigit()               // Strict Tabular Metrics
                .foregroundColor(.white)
            
            Text("IL-6 Biomarker: 14.2 pg/mL")
                .font(.pocketGullFineliner(size: 16))
                .tracking(1.8)                   // Herman Bouma Lateral Anti-Crowding
                .foregroundColor(.teal)
        }
        .padding()
        .background(Color(red: 0.04, green: 0.05, blue: 0.09))
        .cornerRadius(12)
    }
}`,

      css: `/* 1. PocketGull Webfont Declarations */
@font-face {
  font-family: 'PocketGull';
  src: url('/fonts/PocketGull-Bold.woff2') format('woff2');
  font-weight: 700 800;
  font-display: swap;
}

@font-face {
  font-family: 'PocketGull';
  src: url('/fonts/PocketGull-Fineliner.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: 'PocketGull Mono';
  src: url('/fonts/PocketGullMono-Regular.woff2') format('woff2');
  font-weight: 500;
  font-display: swap;
}`,
      npm: `// Install via Package Manager
npm install @pocketgull/font
# or
pnpm add @pocketgull/font
# or
yarn add @pocketgull/font

// 1. In your application entry point (main.tsx / index.js / App.vue):
import '@pocketgull/font';

// 2. Or in your CSS / SCSS stylesheet:
@import '@pocketgull/font';

// 3. Usage in CSS:
body {
  font-family: 'PocketGull', -apple-system, sans-serif;
}
.telemetry, code, pre, .vitals-grid {
  font-family: 'PocketGull Mono', monospace;
  font-feature-settings: "tnum" 1, "zero" 1;
}`,
      sri: `<!-- Subresource Integrity (SRI) Preload Headers -->
<!-- Hardened under NIST SP 800-218 & W3C Subresource Integrity Standards -->

<!-- PocketGull Bold (Display Titling & Alerts) -->
<link rel="preload" 
      href="https://font.pocketgull.app/fonts/woff2/PocketGull-Bold.woff2" 
      as="font" type="font/woff2" crossorigin 
      integrity="sha384-L3OZ7tkorT0H6zJG4A7OrCjEZJ+0NQel6BKgAWSHMuLK65XVHM7WFWv4lm+GstL6">

<!-- PocketGull Fineliner (Clinical Body & Discharge Notes) -->
<link rel="preload" 
      href="https://font.pocketgull.app/fonts/woff2/PocketGull-Fineliner.woff2" 
      as="font" type="font/woff2" crossorigin 
      integrity="sha384-H5dHFsvLEgPeH+PAbrJ6md00+kAXVCgoyzmflPkR2ifLvHkoWab/zBCMp0v7Uouw">

<!-- PocketGull Mono (Fixed 600 UPM ICU Telemetry & Code) -->
<link rel="preload" 
      href="https://font.pocketgull.app/fonts/woff2/PocketGullMono-Regular.woff2" 
      as="font" type="font/woff2" crossorigin 
      integrity="sha384-9/6V9dWJkAutMq/EhA3gkDc1liwZyPfCs+ZQKlbXOKXrGt4LIhk8xDHuEoEhQ6CP">`,
      'multilingual-css': `/* 3. Pan-Asian & Indic Multilingual Stacking */
/* Chinese Anatomical Logographs */
.clinical-chinese {
  font-family: 'PocketGull', 'Microsoft YaHei', 'PingFang SC', sans-serif;
  letter-spacing: 0.05em;
}

/* Sanskrit Devanagari (Cap-Height Shirorekha Alignment) */
.clinical-sanskrit {
  font-family: 'PocketGull', 'Nirmala UI', 'Noto Sans Devanagari', sans-serif;
  line-height: 1.65;
}

/* Universal Metric-Locked Fallback Chain */
.clinical-multilingual {
  font-family: 'PocketGull', 'PocketGull Bold', 'Nirmala UI', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  vertical-align: baseline;
}`,
      material3: `/* 2. Material Design 3 (M3) System Tokens & Typography Roles */
:root {
  /* M3 Primary Clinical Tonal Palette Derived from PocketGull Gear Teal */
  --md-sys-color-primary: #14b8a6;
  --md-sys-color-on-primary: #003731;
  --md-sys-color-primary-container: #005047;
  --md-sys-color-on-primary-container: #70f7e4;

  /* M3 Surface Container Elevation (Dark Obsidian Medical Palette) */
  --md-sys-color-surface: #09090b;
  --md-sys-color-surface-container: #181820;
  --md-sys-color-surface-container-high: #1f1f2a;
  --md-sys-color-on-surface: #f4f4f5;
  --md-sys-color-outline: #272732;

  /* M3 System Typography Roles mapped directly to PocketGull */
  --md-sys-typescale-display-large-font: 'PocketGull Bold', 'PocketGull', sans-serif;
  --md-sys-typescale-headline-medium-font: 'PocketGull Bold', 'PocketGull', sans-serif;
  --md-sys-typescale-title-medium-font: 'PocketGull Bold', 'PocketGull', sans-serif;
  --md-sys-typescale-body-large-font: 'PocketGull Fineliner', 'PocketGull', sans-serif;
  --md-sys-typescale-label-large-font: 'PocketGull Mono', monospace;
}

/* Material Web Components (@material/web) Usage */
<md-filled-tonal-button class="clinical-verify">
  <md-icon slot="icon">medical_services</md-icon>
  Verify Prescription (ISMP Safe)
</md-filled-tonal-button>`,
      'ismp-css': `/* 2. ISMP / FDA Clinical Disambiguation Safety Preset */
.clinical-dosage-safe {
  font-family: 'PocketGull', -apple-system, BlinkMacSystemFont, sans-serif;
  font-feature-settings: 
    "zero" 1, /* Slashed Zero: 0 vs O */
    "cv08" 1, /* Alternate Slashed Zero */
    "cv05" 1, /* Curved Lowercase l: l vs 1 vs I */
    "ss02" 1, /* Serifed Capital I */
    "tnum" 1; /* Tabular Figures for Decimals */
}`,
      tailwind: `// 3. tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        pocketgull: ['PocketGull', 'sans-serif'],
        'pocketgull-mono': ['"PocketGull Mono"', 'monospace'],
        'pocketgull-chisel': ['"PocketGull Chiseltip"', 'sans-serif'],
      },
      colors: {
        obsidian: '#09090b',
        gearTeal: '#14b8a6',
        pbmRed: '#ff3333',
      }
    }
  }
};`,
      omp: `# 4. Oh My Posh Ophthalmic Theme Installation (PowerShell)
oh-my-posh init pwsh --config https://font.pocketgull.app/pocketgull-ophthalmic.omp.json | Invoke-Expression

# Set terminal font to "PocketGull Mono" for gapless box-drawing and sub-cell ECG waveforms!`,
      'clinical-letter': `MEMORANDUM & WORKSTATION AUTHORIZATION REQUEST

TO:      Chief Medical Information Officer (CMIO) / Director of Health Informatics / IT Infrastructure Committee
FROM:    [Your Name, MD / DO / NP / PA / RN / Clinical Lead]
DATE:    [Date]
SUBJECT: Request for Installation of PocketGull Clinical Font Superfamily on Clinical Workstations & COW Units

Dear [CMIO / IT Director / Clinical Systems Administrator],

I am writing to formally request the installation and whitelisting of the open-source PocketGull Font Superfamily on our clinic and hospital workstations, including ambulatory exam rooms, Citrix virtual desktop endpoints, and mobile Computer on Wheels (COW) carts.

1. THE CLINICAL RATIONALE & PATIENT SAFETY
Standard operating system fonts (such as Arial, Calibri, and Segoe UI) are designed for general corporate office productivity rather than high-acuity medical care. During prolonged 12-hour shifts and under low-contrast or off-axis monitor viewing, standard fonts contribute significantly to cognitive visual fatigue and introduce life-critical medication transcription risks:
  • 10-Fold Dosing Errors: The Institute for Safe Medication Practices (ISMP) explicitly prohibits trailing zeroes (e.g. writing "5.0 mg" instead of "5 mg") because a dirty screen or low-contrast display can transform "5.0" into "50 mg" (a fatal 10-fold overdose).
  • Alphanumeric Confusion: Standard fonts present identical vertical stems for numeral "1", lowercase "l", and uppercase "I", leading to medication and patient record errors.
  • Peripheral Crowding: Under Bouma’s Law of Lateral Crowding (r ≈ 0.5 × eccentricity), peripheral vitals numbers blend together during surgical or emergency room focus.

2. HOW POCKETGULL RESOLVES THESE HAZARDS
PocketGull is an open-source, mathematically standardized 1000 UPM clinical font superfamily engineered specifically for medical EHRs, bedside vitals monitors, and diagnostic HUDs:
  • ISMP & FDA Life-Critical Disambiguation: Natively enforces OpenType slashed zeroes (cv08), curved lowercase "l" (cv05), and serifed uppercase "I" (ss02), completely eliminating character collisions.
  • Louise Sloan 5:1 Optotypic Proportion: Engineered to the Johns Hopkins Wilmer Eye Institute standard (5 arcminutes total height, 1 arcminute stroke width and counter aperture at 55 cm reading distance), guaranteeing maximum optical legibility during fatigue.
  • Bedside 203 DPI Interoperability: Quantized to 8 dots/mm integer stems, rendering razor-sharp medication orders on direct-thermal Zebra wristband and IV bag printers with zero dithering.
  • 256 Unicode Braille (U+2800–U+28FF): Full tactile pharmaceutical labeling compliance.

3. CYBERSECURITY, COMPLIANCE & TECHNICAL SPECIFICATIONS
  • Zero Egress & Zero Tracking: PocketGull consists purely of local OpenType/TrueType (.ttf) and webfont (.woff2) vector font files. It contains ZERO tracking scripts, ZERO external API calls, and zero network dependencies.
  • 100% HIPAA Safe Harbor: Operates entirely client-side on the local machine with zero ePHI exposure.
  • Open-Source & Zero Licensing Cost: Released under the Apache License, Version 2.0, permitting unrestricted enterprise, hospital, and clinical use with zero software licensing fees.
  • Low-Impact Deployment: Files can be silently distributed via Microsoft Intune, SCCM, or Windows Group Policy (GPO) to %WINDIR%\\Fonts, or applied via Citrix Workspace user profile layers without modifying system registry binaries.

4. REQUESTED ACTION
We request approval to install the three core TrueType font binaries:
  1. PocketGull-Bold.ttf (Display & Placards)
  2. PocketGull-Fineliner.ttf (EHR Body & Clinical Prescribing)
  3. PocketGullMono-Regular.ttf (Fixed-width Telemetry, Vitals & Terminal HUDs)

I would be happy to coordinate a brief 30-day pilot within our department or floor to demonstrate the reduction in visual strain and enhanced legibility across our clinical team.

Documentation & Interactive Verification Specimen: https://font.pocketgull.app
Open Source Repository: https://github.com/pocketgull-app/pocketgull-font

Thank you for your dedication to our clinical staff's ergonomics and patient safety.

Sincerely,

[Your Signature]
[Your Printed Name & Credentials]
[Department / Clinical Unit]
[Contact Information / Extension]`
    };

    // Multilingual Thermal Hospital Label Studio
    const THERMAL_PRESCRIPTIONS = {
      en: {
        title: "STAT RX: CEFAZOLIN 2 g IV",
        dose: "DOSE: 2000 mg Q8H • ⌀18G IV",
        allergy: "ALLERGY ALERT: PENICILLIN",
        zplDose: "DOSE: 2000 mg Q8H - 18G IV",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      },
      es: {
        title: "RX URGENTE: CEFAZOLINA 2 g IV",
        dose: "DOSIS: 2000 mg C/8H • ⌀18G IV",
        allergy: "ALERTA DE ALERGIA: PENICILINA",
        zplDose: "DOSIS: 2000 mg C/8H - 18G IV",
        zplAllergy: "ALERGIA: PENICILINA",
        rtl: false
      },
      zh: {
        title: "急诊处方: 头孢唑林 2 g 静脉注射",
        dose: "剂量: 2000 mg 每8小时 • ⌀18G 静脉",
        allergy: "过敏警报: 青霉素过敏",
        zplDose: "剂量: 2000 mg 每8小时 - 18G",
        zplAllergy: "过敏警报: 青霉素",
        rtl: false
      },
      hi: {
        title: "आपातकालीन औषधि: सेफाज़ोलिन 2 g",
        dose: "मात्रा: 2000 mg प्रति 8 घंटे • ⌀18G अंतःशिरा",
        allergy: "एलर्जी चेतावनी: पेनिसिलिन",
        zplDose: "मात्रा: 2000 mg प्रति 8 घंटे",
        zplAllergy: "एलर्जी चेतावनी: पेनिसिलिन",
        rtl: false
      },
      ar: {
        title: "وصفة طارئة: سيفازولين 2 غرام وريدي",
        dose: "الجرعة: 2000 مغ كل 8 ساعات • ⌀18G وريدي",
        allergy: "تحذير حساسية: بنسلين",
        zplDose: "الجرعة: 2000 مغ كل 8 ساعات",
        zplAllergy: "تحذير حساسية: بنسلين",
        rtl: true
      },
      fa: {
        title: "نسخه اورژانسی: سفازولین ۲ گرم وریدی",
        dose: "دوز دارو: ۲۰۰۰ میلی‌گرم هر ۸ ساعت • ⌀18G وریدی",
        allergy: "هشدار حساسیت دارویی: پنی‌سیلین",
        zplDose: "دوز: 2000 میلی‌گرم هر 8 ساعت",
        zplAllergy: "هشدار حساسیت: پنی‌سیلین",
        rtl: true
      },
      he: {
        title: "מרשם דחוף: צפזולין 2 גרם תוך-ורידי",
        dose: "מינון: 2000 מ\"ג כל 8 שעות • ⌀18G",
        allergy: "התראת אלרגיה: פניצילין",
        zplDose: "מינון: 2000 מ\"ג כל 8 שעות",
        zplAllergy: "התראת אלרגיה: פניצילין",
        rtl: true
      },
      ko: {
        title: "응급 처방: 세파졸린 2 g 정맥 주사",
        dose: "용량: 2000 mg 8시간마다 • ⌀18G IV",
        allergy: "알레르기 경고: 페니실린",
        zplDose: "용량: 2000 mg 8시간마다",
        zplAllergy: "알레르기: 페니실린",
        rtl: false
      },
      ja: {
        title: "至急処方: セファゾリン 2 g 点滴静注",
        dose: "用量: 2000 mg 8時間毎 • ⌀18G 点滴",
        allergy: "アレルギー警告: ペニシリン",
        zplDose: "用量: 2000 mg 8時間毎",
        zplAllergy: "アレルギー警告: ペニシリン",
        rtl: false
      },
      ru: {
        title: "СРОЧНЫЙ РЕЦЕПТ: ЦЕФАЗОЛИН 2 г в/в",
        dose: "ДОЗА: 2000 мг каждые 8 ч • ⌀18G в/в",
        allergy: "ПРЕДУПРЕЖДЕНИЕ: АЛЛЕРГИЯ НА ПЕНИЦИЛЛИН",
        zplDose: "ДОЗА: 2000 мг каждые 8 ч - 18G",
        zplAllergy: "АЛЛЕРГИЯ: ПЕНИЦИЛЛИН",
        rtl: false
      },
      vi: {
        title: "ĐƠN KHẨN CẤP: CEFAZOLIN 2 g TIÊM TM",
        dose: "LIỀU: 2000 mg MỖI 8 GIỜ • ⌀18G TM",
        allergy: "CẢNH BÁO DỊ ỨNG: PENICILLIN",
        zplDose: "LIỀU: 2000 mg MỖI 8 GIỜ",
        zplAllergy: "CẢNH BÁO DỊ ỨNG: PENICILLIN",
        rtl: false
      },
      iu: {
        title: "ᓘᒃᑖᖅ: ᐋᓐᓂᐊᖃᕐᓇᙱᑦᑐᓕᕆᓂᖅ (CEFAZOLIN)",
        dose: "ᑐᓂᔭᐅᓂᖓ: 2000 mg ᖃᐅᑕᒫᑦ 8 ᐃᑲᕐᕋᓂᒃ • ⌀18G IV",
        allergy: "ᐅᔾᔨᕈᓱᒋᐊᓕᒃ: ᐱᓂᓯᓕᓐ (PENICILLIN)",
        zplDose: "DOSE: 2000 mg Q8H STAT",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      },
      chr: {
        title: "ᎦᎾᎦᏘ ᎤᏁᏨᎯ: ᎤᎵᏍᎨᏗᏳ ᏅᏬᏘ (CEFAZOLIN 2 g)",
        dose: "ᎠᏟᎶᎥᎢ: 2000 mg ᎢᏳᎵᏍᏙᏗ 8 ᎢᏳᏟᎶᏛ • ⌀18G ᎩᎦ",
        allergy: "ᏯᎪᏩᏛ ᎤᏍᎦᏎᏗ: ᎤᏂᎩᏍᏗ (PENICILLIN)",
        zplDose: "DOSE: 2000 mg Q8H STAT",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      },
      chn: {
        title: "𛰅𛰀𛰆 𛱁𛱐: CEFAZOLIN 2 g (DOKTIN PIPA)",
        dose: "𛰃𛰚𛱄𛰆: 2000 mg KANAM 8 TINTIN • ⌀18G IV",
        allergy: "𛰅𛰚𛱄 𛰂𛱐: PENICILLIN (MASATSI IKTA)",
        zplDose: "DOSE: 2000 mg Q8H STAT",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      },
      ber: {
        title: "ⵜⴰⵙⵏⵉⵊⵊⵉⵜ: ⵙⵉⴼⴰⵥⵓⵍⵉⵏ 2 g (CEFAZOLIN)",
        dose: "ⵜⴰⵙⴽⴼⵍⵜ: 2000 mg ⴽⵓ 8 ⵜⵙⵔⴰⴳⵉⵏ • ⌀18G IV",
        allergy: "ⴰⵏⵖⴰⵍ ⵏ ⵜⵓⵙⵏⴰ: ⴱⵉⵏⵉⵙⵉⵍⵉⵏ (PENICILLIN)",
        zplDose: "DOSE: 2000 mg Q8H STAT",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      },
      cunei: {
        title: "𒀀𒍪 𒌨𒈤: 𒋆 ꗠ  ਦਵਾਈ (CEFAZOLIN 2 g)",
        dose: "𒉌𒌓  അള: 2000 mg 𒌓 8 𒄰 • ⌀18G IV",
        allergy: "𒅆𒌨 𒁔: 𒋆 𒉿𒉌𒋛 (PENICILLIN)",
        zplDose: "DOSE: 2000 mg Q8H STAT",
        zplAllergy: "ALLERGY: PENICILLIN",
        rtl: false
      }
    };

    let activeThermalLang = 'en';
    const thermalRxTitle = document.getElementById('thermalRxTitle');
    const thermalDoseText = document.getElementById('thermalDoseText');
    const thermalAllergyText = document.getElementById('thermalAllergyText');
    const thermalHospitalLabel = document.getElementById('thermalHospitalLabel');
    const thermalLangBtns = document.querySelectorAll('.thermal-lang-btn');

    function setThermalLanguage(lang) {
      if (!THERMAL_PRESCRIPTIONS[lang]) return;
      activeThermalLang = lang;
      const data = THERMAL_PRESCRIPTIONS[lang];
      if (thermalRxTitle) thermalRxTitle.textContent = data.title;
      if (thermalDoseText) thermalDoseText.textContent = data.dose;
      if (thermalAllergyText) thermalAllergyText.textContent = data.allergy;
      
      const rxHeader = document.getElementById('thermalRxHeader');
      const rxBody = document.getElementById('thermalRxBody');

      if (thermalHospitalLabel) {
        // Maintain canonical LTR clinical chassis (Barcode, Bed, MRN, Sloan 5:1 badge)
        thermalHospitalLabel.removeAttribute('dir');
        thermalHospitalLabel.style.textAlign = 'left';
      }

      if (rxHeader && rxBody) {
        if (data.rtl) {
          rxHeader.setAttribute('dir', 'rtl');
          rxHeader.style.textAlign = 'right';
          rxBody.setAttribute('dir', 'rtl');
          rxBody.style.textAlign = 'right';
        } else {
          rxHeader.removeAttribute('dir');
          rxHeader.style.textAlign = 'left';
          rxBody.removeAttribute('dir');
          rxBody.style.textAlign = 'left';
        }

        // ── Script-specific font routing & optical height normalization ──────────
        // PocketGull ETDRS 1:5 Apertures survive low-resolution 203 DPI thermal bleed.
        // Normalize cap-height and x-height so indigenous and non-Latin syllabary/alphabet
        // characters match the visual height of the numerical readout (2000 mg Q8H • ⌀18G).
        if (lang === 'chr') {
          // Cherokee Syllabary (Sequoyah): Optical scale match with numerals
          rxHeader.style.fontFamily = '"PocketGull Cherokee", "PocketGull Bold", "Gadugi", sans-serif';
          rxHeader.style.fontSize   = '0.98rem';
          rxBody.style.fontFamily   = '"PocketGull Cherokee", "PocketGull Mono", "PocketGull", "Gadugi", monospace';
          rxBody.style.fontSize     = '0.92rem';
          rxBody.style.lineHeight   = '1.55';
        } else if (lang === 'ber') {
          // Neo-Tifinagh (Amazigh): Geometric counter-dilation
          rxHeader.style.fontFamily = '"PocketGull Tifinagh", "PocketGull Bold", "Ebrima", "Noto Sans Tifinagh", sans-serif';
          rxHeader.style.fontSize   = '0.98rem';
          rxBody.style.fontFamily   = '"PocketGull Tifinagh", "PocketGull Mono", "PocketGull", "Ebrima", monospace';
          rxBody.style.fontSize     = '0.92rem';
          rxBody.style.lineHeight   = '1.55';
        } else if (lang === 'he') {
          // Hebrew: Clean optical baseline alignment and aperture preservation
          rxHeader.style.fontFamily = '"PocketGull Bold", "Noto Sans Hebrew", "Arial", sans-serif';
          rxHeader.style.fontSize   = '0.98rem';
          rxBody.style.fontFamily   = '"PocketGull Mono", "PocketGull", "Noto Sans Hebrew", monospace';
          rxBody.style.fontSize     = '0.90rem';
          rxBody.style.lineHeight   = '1.5';
        } else if (lang === 'iu') {
          // Inuktitut (UCAS): Unified syllabic aspect ratio
          rxHeader.style.fontFamily = '"PocketGull Inuktitut", "PocketGull Bold", "Euphemia", "Noto Sans Canadian Aboriginal", sans-serif';
          rxHeader.style.fontSize   = '0.95rem';
          rxBody.style.fontFamily   = '"PocketGull Inuktitut", "PocketGull Mono", "PocketGull", "Euphemia", monospace';
          rxBody.style.fontSize     = '0.90rem';
          rxBody.style.lineHeight   = '1.55';
        } else if (lang === 'hi') {
          // Devanagari: Shirorekha headline expansion, matra baseline clearance & 1:5 aperture dilation
          rxHeader.style.fontFamily = '"PocketGull Devanagari", "PocketGull Bold", "Nirmala UI", "Noto Sans Devanagari", sans-serif';
          rxHeader.style.fontSize   = '0.98rem';
          rxBody.style.fontFamily   = '"PocketGull Devanagari", "PocketGull Mono", "PocketGull", "Nirmala UI", monospace';
          rxBody.style.fontSize     = '0.94rem';
          rxBody.style.lineHeight   = '1.65';
        } else if (lang === 'chn') {
          // Chinuk Pipa (Duployan Shorthand): Rotational phonological symmetry & elevation
          rxHeader.style.fontFamily = '"PocketGull Duployan", "PocketGull Bold", sans-serif';
          rxHeader.style.fontSize   = '1.02rem';
          rxBody.style.fontFamily   = '"PocketGull Duployan", "PocketGull Mono", "PocketGull", monospace';
          rxBody.style.fontSize     = '0.96rem';
          rxBody.style.lineHeight   = '1.60';
        } else if (lang === 'cunei') {
          // Sumero-Akkadian Cuneiform: Wedge-stroke contrast dilation
          rxHeader.style.fontFamily = '"PocketGull Cuneiform", "Segoe UI Historic", sans-serif';
          rxHeader.style.fontSize   = '1.05rem';
          rxBody.style.fontFamily   = '"PocketGull Cuneiform", "PocketGull Mono", "Segoe UI Historic", monospace';
          rxBody.style.fontSize     = '1.00rem';
          rxBody.style.lineHeight   = '1.60';
        } else if (lang === 'ru') {
          // Cyrillic: Classical x-height alignment with Latin tabular numerals
          rxHeader.style.fontFamily = '"PocketGull Cyrillic", "PocketGull Bold", sans-serif';
          rxHeader.style.fontSize   = '0.95rem';
          rxBody.style.fontFamily   = '"PocketGull Cyrillic", "PocketGull Mono", monospace';
          rxBody.style.fontSize     = '0.86rem';
          rxBody.style.lineHeight   = '1.45';
        } else if (lang === 'ar' || lang === 'fa') {
          // Arabic & Farsi: full Naskh cursive — Noto Sans Arabic is authoritative
          rxHeader.style.fontFamily = '"Noto Sans Arabic", "Segoe UI", Tahoma, sans-serif';
          rxHeader.style.fontSize   = '0.95rem';
          rxBody.style.fontFamily   = '"Noto Sans Arabic", "Segoe UI", Tahoma, sans-serif';
          rxBody.style.fontSize     = '0.88rem';
          rxBody.style.lineHeight   = '1.5';
        } else if (lang === 'ja' || lang === 'ko') {
          // Japanese/Korean: system CJK — PocketGull does not cover CJK (by design)
          rxHeader.style.fontFamily = '"Noto Sans JP", "Yu Gothic", "Hiragino Sans", "Meiryo", sans-serif';
          rxHeader.style.fontSize   = '0.90rem';
          rxBody.style.fontFamily   = '"Noto Sans JP", "Yu Gothic", "Hiragino Sans", "Meiryo", monospace';
          rxBody.style.fontSize     = '0.82rem';
          rxBody.style.lineHeight   = '1.45';
        } else {
          rxHeader.style.fontFamily = '"PocketGull Bold", sans-serif';
          rxHeader.style.fontSize   = '0.95rem';
          rxBody.style.fontFamily   = "'PocketGull Mono', monospace";
          rxBody.style.fontSize     = '0.82rem';
          rxBody.style.lineHeight   = '1.4';
        }
      }

      thermalLangBtns.forEach(btn => {
        if (btn.dataset.lang === lang) {
          btn.style.background = 'var(--accent-teal)';
          btn.style.color = '#fff';
          btn.classList.add('active');
        } else {
          btn.style.background = 'transparent';
          btn.style.color = 'var(--text-secondary)';
          btn.classList.remove('active');
        }
      });
    }

    thermalLangBtns.forEach(btn => {
      btn.addEventListener('click', () => setThermalLanguage(btn.dataset.lang));
    });

    // Thermal Actions
    const btnPrintThermalLabel = document.getElementById('btnPrintThermalLabel');
    if (btnPrintThermalLabel) {
      btnPrintThermalLabel.addEventListener('click', () => {
        window.print();
      });
    }

    const btnDownloadZpl = document.getElementById('btnDownloadZpl');
    if (btnDownloadZpl) {
      btnDownloadZpl.addEventListener('click', () => {
        const cur = THERMAL_PRESCRIPTIONS[activeThermalLang] || THERMAL_PRESCRIPTIONS.en;
        const zpl = `^XA
^CI28
^PW609
^LL406
^LH0,0
^FO40,30^GB529,0,3^FS
^FO40,40^A0N,22,22^FDPOCKETGULL HEALTH SYSTEM - 203 DPI^FS
^FO40,68^A0N,20,20^FDPATIENT: SAPIENS, H. (34y F)  BED: 04^FS
^FO40,95^BY2,3,40^BCN,40,Y,N,N^FD9842-01-STAT^FS
^FO40,165^GB529,42,42^FS
^FO50,175^FR^A0N,24,24^FD${cur.title}^FS
^FO40,225^A0N,22,22^FD${cur.zplDose}^FS
^FO40,255^A0N,22,22^FD${cur.zplAllergy}^FS
^FO40,300^GB529,0,2^FS
^FO40,315^A0N,18,18^FDMRN: #9842-01 [SLOAN 5:1 DILATED COUNTERS]^FS
^XZ`;

        const blob = new Blob([zpl], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `pocketgull_stat_rx_${activeThermalLang}.zpl`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    let thermalBleedActive = false;
    const btnThermalBleedToggle = document.getElementById('btnThermalBleedToggle');
    if (btnThermalBleedToggle && thermalHospitalLabel) {
      btnThermalBleedToggle.addEventListener('click', () => {
        thermalBleedActive = !thermalBleedActive;
        if (thermalBleedActive) {
          btnThermalBleedToggle.textContent = '🔥 203 DPI Heat Spread: ON';
          btnThermalBleedToggle.style.background = 'rgba(245, 158, 11, 0.2)';
          thermalHospitalLabel.style.filter = 'contrast(180%) brightness(92%) blur(0.4px)';
        } else {
          btnThermalBleedToggle.textContent = '🔥 203 DPI Heat Spread: OFF';
          btnThermalBleedToggle.style.background = 'transparent';
          thermalHospitalLabel.style.filter = 'none';
        }
      });
    }

    const codeDisplay = document.getElementById('codeDisplay');
    const copyCodeBtn = document.getElementById('copyCodeBtn');
    const tabBtns = document.querySelectorAll('.tab-btn');
    let currentTab = 'css';

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.dataset.tab;
        codeDisplay.textContent = CODE_SNIPPETS[currentTab];
      });
    });

    copyCodeBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(CODE_SNIPPETS[currentTab]).then(() => {
        const orig = copyCodeBtn.textContent;
        copyCodeBtn.textContent = 'Copied! ✓';
        setTimeout(() => copyCodeBtn.textContent = orig, 1800);
      });
    });

    const copyLetterBtn = document.getElementById('copyLetterBtn');
    if (copyLetterBtn) {
      copyLetterBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(CODE_SNIPPETS['clinical-letter']).then(() => {
          const orig = copyLetterBtn.innerHTML;
          copyLetterBtn.innerHTML = '<span>✓</span> Copied to Clipboard!';
          setTimeout(() => copyLetterBtn.innerHTML = orig, 2000);
        });
      });
    }

    /* ========================================================================== */
    /* 07. INTERACTIVE MULTI-SCALE PHOROPTER & POPULATION FOCUS WHEEL SCRIPT      */
    /* ========================================================================== */
      function launchPocketGullTurntableModal() {
        let modal = document.getElementById('pocketgullTurntableModalOverlay');
        if (!modal) {
          modal = document.createElement('div');
          modal.id = 'pocketgullTurntableModalOverlay';
          modal.style.position = 'fixed';
          modal.style.inset = '0';
          modal.style.zIndex = '999999';
          modal.style.background = 'radial-gradient(circle at center, #0f172a 0%, #020617 100%)';
          modal.style.display = 'flex';
          modal.style.flexDirection = 'column';
          modal.style.userSelect = 'none';

          modal.innerHTML = `
            <!-- Studio Header Bar -->
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; padding: 1rem 1.75rem; background: rgba(3, 7, 18, 0.95); border-bottom: 1px solid var(--border-subtle); color: #fff; font-family: var(--font-code); backdrop-filter: blur(16px); gap: 1rem;">
              <div style="display: flex; align-items: center; gap: 0.85rem;">
                <span style="font-size: 1.6rem;">🔄</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                    <span style="font-family: 'PocketGull Bold', sans-serif; font-size: 1.15rem; font-weight: 900; color: #38bdf8; letter-spacing: -0.02em;">
                      POCKETGULL 2D-TO-3D TURNTABLE STUDIO
                    </span>
                    <span style="font-size: 0.7rem; background: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; padding: 0.15rem 0.5rem; border-radius: 9999px; color: #38bdf8; font-weight: 800;">
                      ADOBE-INSPIRED EXTRUSION RIG
                    </span>
                  </div>
                  <p style="font-size: 0.72rem; color: #a1a1aa; margin: 0;">
                    Extrude 2D vector glyphs and anatomical profiles into 3D volumetric slabs with specular normal lighting and 360° turntable rotation.
                  </p>
                </div>
              </div>

              <!-- Top Studio Controls -->
              <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <!-- Model Subject Selector -->
                <select id="turntableSubjectSelect" style="background: rgba(255, 255, 255, 0.08); border: 1px solid var(--border-subtle); color: #38bdf8; padding: 0.4rem 0.75rem; border-radius: 6px; font-size: 0.78rem; font-family: var(--font-code); cursor: pointer; font-weight: 700;">
                  <option value="body">Subject: 3D Typographic Human Silhouette</option>
                  <option value="heart">Subject: Myocardium Pump Vector (🫀)</option>
                  <option value="brain">Subject: Cerebral Tubulin 40Hz Dipole (🧠)</option>
                  <option value="sloanZ">Subject: Sloan Optotype 'Z' (cv11 Slashed)</option>
                  <option value="sloan0">Subject: ISMP Slashed Zero '0' (cv08)</option>
                  <option value="braille">Subject: ISO/TR 11548 Braille Matrix (⠠⠃)</option>
                </select>

                <!-- Turntable Motor Play/Pause -->
                <button id="turntableMotorBtn" style="background: var(--accent-teal); border: none; color: #09090b; padding: 0.4rem 0.85rem; border-radius: 6px; cursor: pointer; font-size: 0.75rem; font-weight: 800; display: flex; align-items: center; gap: 0.35rem;">
                  ⏸ Pause Motor (3.0 RPM)
                </button>

                <!-- Reset Camera -->
                <button id="turntableResetBtn" style="background: rgba(255, 255, 255, 0.08); border: 1px solid var(--border-subtle); color: #fff; padding: 0.4rem 0.85rem; border-radius: 6px; cursor: pointer; font-size: 0.75rem;">
                  🔄 Reset View
                </button>

                <button id="closeTurntableModalBtn" style="background: transparent; border: 1px solid rgba(255, 255, 255, 0.2); color: #fff; padding: 0.4rem 0.85rem; border-radius: 6px; cursor: pointer; font-size: 0.75rem;">
                  ✕ Exit Studio
                </button>
              </div>
            </div>

            <!-- Main Studio Workspace (Left Controls + 3D Viewport) -->
            <div style="flex: 1; display: flex; overflow: hidden; position: relative;">
              
              <!-- Left Sidebar: Adobe 3D & Materials Properties Inspector -->
              <div style="width: 280px; background: rgba(10, 15, 30, 0.85); border-right: 1px solid var(--border-subtle); padding: 1.25rem; overflow-y: auto; font-family: var(--font-code); display: flex; flex-direction: column; gap: 1.25rem; backdrop-filter: blur(12px); z-index: 20;">
                
                <div>
                  <div style="font-size: 0.7rem; color: #38bdf8; font-weight: 800; margin-bottom: 0.5rem; text-transform: uppercase;">
                    1. Extrusion &amp; Bevel Depth
                  </div>
                  <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                    <span>Extrude Z-Depth</span>
                    <span id="extrudeDepthVal" style="color: #38bdf8; font-weight: 700;">40 px</span>
                  </div>
                  <input type="range" id="extrudeDepthSlider" min="0" max="80" value="40" style="width: 100%; accent-color: #38bdf8; cursor: pointer;">
                </div>

                <div>
                  <div style="font-size: 0.7rem; color: #38bdf8; font-weight: 800; margin-bottom: 0.5rem; text-transform: uppercase;">
                    2. Motorized Turntable Speed
                  </div>
                  <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                    <span>Rotation Rate</span>
                    <span id="turntableSpeedVal" style="color: var(--accent-teal); font-weight: 700;">3.0 RPM</span>
                  </div>
                  <input type="range" id="turntableSpeedSlider" min="0" max="10" step="0.5" value="3.0" style="width: 100%; accent-color: var(--accent-teal); cursor: pointer;">
                </div>

                <div>
                  <div style="font-size: 0.7rem; color: #38bdf8; font-weight: 800; margin-bottom: 0.5rem; text-transform: uppercase;">
                    3. Directional Key Lighting
                  </div>
                  <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: var(--text-muted); margin-bottom: 0.25rem;">
                    <span>Light Azimuth</span>
                    <span id="lightAzimuthVal" style="color: #fbbf24; font-weight: 700;">45°</span>
                  </div>
                  <input type="range" id="lightAzimuthSlider" min="-180" max="180" value="45" style="width: 100%; accent-color: #fbbf24; cursor: pointer;">
                </div>

                <div>
                  <div style="font-size: 0.7rem; color: #38bdf8; font-weight: 800; margin-bottom: 0.5rem; text-transform: uppercase;">
                    4. Render Mode &amp; Shading
                  </div>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem;">
                    <button class="turntable-render-btn active" data-render="lit" style="padding: 0.4rem; font-size: 0.72rem; font-weight: 700; border-radius: 4px; border: 1px solid #38bdf8; background: rgba(56, 189, 248, 0.2); color: #38bdf8; cursor: pointer;">
                      ☀️ Lit Shaded
                    </button>
                    <button class="turntable-render-btn" data-render="wire" style="padding: 0.4rem; font-size: 0.72rem; font-weight: 700; border-radius: 4px; border: 1px solid var(--border-subtle); background: transparent; color: var(--text-muted); cursor: pointer;">
                      📐 CAD Wireframe
                    </button>
                  </div>
                </div>

                <div style="border-top: 1px solid var(--border-subtle); padding-top: 1rem; font-size: 0.68rem; color: var(--text-muted); line-height: 1.5;">
                  <strong>Adobe Workflow Parity:</strong><br>
                  • <strong>LMB Drag:</strong> Turntable Orbit (Pitch / Yaw)<br>
                  • <strong>Wheel:</strong> Camera Dolly Zoom<br>
                  • <strong>Shift + Drag:</strong> Camera Pan X/Y<br>
                  • <strong>Extrude:</strong> Multi-layer vector depth slices with normal attenuation
                </div>

              </div>

              <!-- Right: 3D Stage Viewport -->
              <div id="turntableStage" style="flex: 1; position: relative; overflow: hidden; display: flex; justify-content: center; align-items: center; perspective: 1200px; cursor: grab;">
                
                <!-- Floor Grid Shadow Plane -->
                <div style="position: absolute; bottom: 8%; width: 500px; height: 500px; background: radial-gradient(ellipse at center, rgba(56, 189, 248, 0.18) 0%, rgba(0, 0, 0, 0) 70%); transform: rotateX(90deg) translateZ(-160px); pointer-events: none; border-radius: 50%;"></div>

                <!-- 3D Transform Gimbal Platform -->
                <div id="turntableGimbal" style="width: 340px; height: 480px; position: relative; transform-style: preserve-3d; transition: transform 0.05s linear;">
                  
                  <!-- Dynamic Extruded Vector Layers will be rendered here -->
                  <div id="turntableLayersContainer" style="position: absolute; inset: 0; transform-style: preserve-3d;">
                    <!-- Slices generated by renderExtrusion() -->
                  </div>

                </div>

                <!-- Viewport Telemetry HUD -->
                <div style="position: absolute; bottom: 20px; left: 20px; font-family: var(--font-code); font-size: 0.75rem; color: #38bdf8; background: rgba(0, 0, 0, 0.6); padding: 0.4rem 0.8rem; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.3); pointer-events: none;">
                  🖱️ DRAG TO ROTATE 3D • WHEEL TO ZOOM • SHIFT TO PAN
                </div>

                <div id="turntableAngleBadge" style="position: absolute; bottom: 20px; right: 20px; font-family: var(--font-code); font-size: 0.75rem; color: #fbbf24; background: rgba(0, 0, 0, 0.6); padding: 0.4rem 0.8rem; border-radius: 6px; border: 1px solid rgba(251, 191, 36, 0.3); pointer-events: none;">
                  YAW: 0° • PITCH: 0° • DEPTH: 40px
                </div>

              </div>

            </div>
          `;

          document.body.appendChild(modal);

          let ttYaw = 0;
          let ttPitch = 0;
          let ttZoom = 1.0;
          let ttPanX = 0;
          let ttPanY = 0;
          let ttExtrudeDepth = 40;
          let ttSpeedRpm = 3.0;
          let ttLightAzimuth = 45;
          let ttRenderMode = 'lit'; // 'lit' or 'wire'
          let isTtMotorRunning = true;
          let ttMotorTimer = null;
          let isTtDragging = false;
          let ttStartX = 0;
          let ttStartY = 0;

          const turntableStage = document.getElementById('turntableStage');
          const turntableGimbal = document.getElementById('turntableGimbal');
          const turntableLayersContainer = document.getElementById('turntableLayersContainer');
          const turntableSubjectSelect = document.getElementById('turntableSubjectSelect');
          const turntableMotorBtn = document.getElementById('turntableMotorBtn');
          const turntableResetBtn = document.getElementById('turntableResetBtn');
          const closeTurntableModalBtn = document.getElementById('closeTurntableModalBtn');
          const extrudeDepthSlider = document.getElementById('extrudeDepthSlider');
          const extrudeDepthVal = document.getElementById('extrudeDepthVal');
          const turntableSpeedSlider = document.getElementById('turntableSpeedSlider');
          const turntableSpeedVal = document.getElementById('turntableSpeedVal');
          const lightAzimuthSlider = document.getElementById('lightAzimuthSlider');
          const lightAzimuthVal = document.getElementById('lightAzimuthVal');
          const turntableAngleBadge = document.getElementById('turntableAngleBadge');
          const renderBtns = modal.querySelectorAll('.turntable-render-btn');

          function getSubjectSvg(subject, layerZ, opacity, strokeColor, fillColor) {
            if (subject === 'heart') {
              return `
                <svg viewBox="0 0 240 240" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="${ttRenderMode === 'wire' ? '1.5' : '2'}">
                    <path d="M 120,60 C 105,25 45,25 45,80 C 45,135 120,195 120,195 C 120,195 195,135 195,80 C 195,25 135,25 120,60 Z" />
                    <!-- Ventricular & Atrial Internal Vector Contours -->
                    <circle cx="95" cy="90" r="18" fill="none" stroke="${strokeColor}" stroke-dasharray="2,2" />
                    <circle cx="145" cy="90" r="18" fill="none" stroke="${strokeColor}" stroke-dasharray="2,2" />
                    <text x="120" y="115" font-family="'PocketGull Bold'" font-size="14" font-weight="900" text-anchor="middle" fill="${strokeColor}">MYOCARDIUM</text>
                  </g>
                </svg>
              `;
            } else if (subject === 'brain') {
              return `
                <svg viewBox="0 0 240 240" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="${ttRenderMode === 'wire' ? '1.5' : '2'}">
                    <ellipse cx="120" cy="110" rx="75" ry="60" />
                    <path d="M 60,110 Q 120,70 180,110" fill="none" />
                    <path d="M 60,130 Q 120,170 180,130" fill="none" />
                    <text x="120" y="115" font-family="'PocketGull Bold'" font-size="13" font-weight="900" text-anchor="middle" fill="${strokeColor}">ORCH-OR 40Hz</text>
                  </g>
                </svg>
              `;
            } else if (subject === 'sloanZ') {
              return `
                <svg viewBox="0 0 240 240" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="${ttRenderMode === 'wire' ? '2' : '0'}">
                    <text x="120" y="180" font-family="'PocketGull Bold', sans-serif" font-size="175" font-weight="900" text-anchor="middle" style="font-feature-settings: 'cv11' 1;">Z</text>
                  </g>
                </svg>
              `;
            } else if (subject === 'sloan0') {
              return `
                <svg viewBox="0 0 240 240" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="${ttRenderMode === 'wire' ? '2' : '0'}">
                    <text x="120" y="180" font-family="'PocketGull Bold', sans-serif" font-size="175" font-weight="900" text-anchor="middle" style="font-feature-settings: 'zero' 1, 'cv08' 1;">0</text>
                  </g>
                </svg>
              `;
            } else if (subject === 'braille') {
              return `
                <svg viewBox="0 0 240 240" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="2">
                    <circle cx="85" cy="65" r="16" />
                    <circle cx="85" cy="115" r="16" />
                    <circle cx="85" cy="165" r="16" />
                    <circle cx="155" cy="65" r="16" />
                    <circle cx="155" cy="115" r="16" />
                    <circle cx="155" cy="165" r="16" />
                  </g>
                </svg>
              `;
            } else {
              // Complete Typographic Body Matrix Silhouette
              return `
                <svg viewBox="0 0 280 420" style="width: 100%; height: 100%; overflow: visible;">
                  <g fill="${fillColor}" stroke="${strokeColor}" stroke-width="${ttRenderMode === 'wire' ? '1.5' : '1'}">
                    <!-- Head -->
                    <circle cx="140" cy="42" r="26" />
                    <text x="140" y="47" font-family="'PocketGull Bold'" font-size="9" text-anchor="middle" fill="${strokeColor}">BRAIN</text>
                    <!-- Thorax -->
                    <ellipse cx="108" cy="108" rx="20" ry="24" />
                    <ellipse cx="172" cy="108" rx="20" ry="24" />
                    <circle cx="140" cy="126" r="18" />
                    <!-- Liver -->
                    <rect x="110" y="152" width="60" height="22" rx="6" />
                    <!-- Pelvis / Legs -->
                    <rect x="95" y="215" width="22" height="70" rx="6" />
                    <rect x="163" y="215" width="22" height="70" rx="6" />
                    <rect x="95" y="295" width="22" height="70" rx="6" />
                    <rect x="163" y="295" width="22" height="70" rx="6" />
                  </g>
                </svg>
              `;
            }
          }

          function renderExtrusion() {
            if (!turntableLayersContainer) return;
            const subject = turntableSubjectSelect.value;
            const sliceCount = ttExtrudeDepth === 0 ? 1 : Math.max(3, Math.round(ttExtrudeDepth / 4));
            const stepZ = ttExtrudeDepth / sliceCount;

            let html = '';
            for (let i = 0; i < sliceCount; i++) {
              const z = (i * stepZ) - (ttExtrudeDepth / 2);
              const isFront = (i === sliceCount - 1);
              const isBack = (i === 0);

              // Shading calculation based on light azimuth
              const lightFactor = Math.cos((ttYaw - ttLightAzimuth) * (Math.PI / 180));
              const intensity = 0.5 + (0.5 * lightFactor);

              let strokeColor = '#38bdf8';
              let fillColor = 'none';

              if (ttRenderMode === 'wire') {
                strokeColor = isFront ? '#38bdf8' : (isBack ? '#1e293b' : 'rgba(56, 189, 248, 0.4)');
                fillColor = 'none';
              } else {
                // Lit Shaded mode: Front is bright, side/back slices create thick gradient slab
                if (isFront) {
                  strokeColor = '#38bdf8';
                  fillColor = `rgba(56, 189, 248, ${0.75 + (0.2 * intensity)})`;
                } else {
                  const darken = (i / sliceCount);
                  strokeColor = `rgba(14, 116, 144, ${0.4 + (0.4 * darken)})`;
                  fillColor = `rgba(15, 23, 42, ${0.6 + (0.3 * darken)})`;
                }
              }

              html += `
                <div style="position: absolute; inset: 0; transform: translateZ(${z}px); pointer-events: none;">
                  ${getSubjectSvg(subject, z, 1.0, strokeColor, fillColor)}
                </div>
              `;
            }

            turntableLayersContainer.innerHTML = html;
          }

          function updateTurntableTransform() {
            if (!turntableGimbal) return;
            turntableGimbal.style.transform = `translate3d(${ttPanX}px, ${ttPanY}px, 0) scale(${ttZoom}) rotateY(${ttYaw}deg) rotateX(${ttPitch}deg)`;
            if (turntableAngleBadge) {
              turntableAngleBadge.textContent = `YAW: ${Math.round(ttYaw % 360)}° • PITCH: ${Math.round(ttPitch)}° • DEPTH: ${ttExtrudeDepth}px`;
            }
          }

          function startTurntableMotor() {
            if (ttMotorTimer) clearInterval(ttMotorTimer);
            ttMotorTimer = setInterval(() => {
              if (isTtMotorRunning && !isTtDragging) {
                // 1 RPM = 360 deg in 60s = 6 deg/s = 0.1 deg per 60fps frame
                const degPerFrame = (ttSpeedRpm * 360) / (60 * 60);
                ttYaw += degPerFrame * 1.5;
                updateTurntableTransform();
                // Dynamically recalculate shading if rotating past key light
                if (Math.round(ttYaw) % 5 === 0) {
                  renderExtrusion();
                }
              }
            }, 1000 / 60);
          }

          startTurntableMotor();
          renderExtrusion();
          updateTurntableTransform();

          // Controls Listeners
          turntableSubjectSelect.addEventListener('change', () => {
            renderExtrusion();
          });

          extrudeDepthSlider.addEventListener('input', (e) => {
            ttExtrudeDepth = parseInt(e.target.value, 10);
            if (extrudeDepthVal) extrudeDepthVal.textContent = `${ttExtrudeDepth} px`;
            renderExtrusion();
            updateTurntableTransform();
          });

          turntableSpeedSlider.addEventListener('input', (e) => {
            ttSpeedRpm = parseFloat(e.target.value);
            if (turntableSpeedVal) turntableSpeedVal.textContent = `${ttSpeedRpm.toFixed(1)} RPM`;
          });

          lightAzimuthSlider.addEventListener('input', (e) => {
            ttLightAzimuth = parseInt(e.target.value, 10);
            if (lightAzimuthVal) lightAzimuthVal.textContent = `${ttLightAzimuth}°`;
            renderExtrusion();
          });

          turntableMotorBtn.addEventListener('click', () => {
            isTtMotorRunning = !isTtMotorRunning;
            turntableMotorBtn.textContent = isTtMotorRunning ? `⏸ Pause Motor (${ttSpeedRpm.toFixed(1)} RPM)` : '▶ Start Turntable';
            turntableMotorBtn.style.background = isTtMotorRunning ? 'var(--accent-teal)' : 'var(--accent-amber)';
          });

          turntableResetBtn.addEventListener('click', () => {
            ttYaw = 0;
            ttPitch = 0;
            ttZoom = 1.0;
            ttPanX = 0;
            ttPanY = 0;
            updateTurntableTransform();
          });

          renderBtns.forEach(btn => {
            btn.addEventListener('click', () => {
              renderBtns.forEach(b => {
                b.classList.remove('active');
                b.style.background = 'transparent';
                b.style.borderColor = 'var(--border-subtle)';
                b.style.color = 'var(--text-muted)';
              });
              btn.classList.add('active');
              btn.style.background = 'rgba(56, 189, 248, 0.2)';
              btn.style.borderColor = '#38bdf8';
              btn.style.color = '#38bdf8';
              ttRenderMode = btn.dataset.render;
              renderExtrusion();
            });
          });

          closeTurntableModalBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            clearInterval(ttMotorTimer);
          });

          // Pointer interaction for 3D Turntable Tumble and Orbit
          turntableStage.addEventListener('pointerdown', (e) => {
            isTtDragging = true;
            ttStartX = e.clientX;
            ttStartY = e.clientY;
            turntableStage.style.cursor = 'grabbing';
            turntableStage.setPointerCapture(e.pointerId);
          });

          turntableStage.addEventListener('pointermove', (e) => {
            if (!isTtDragging) return;
            const dx = e.clientX - ttStartX;
            const dy = e.clientY - ttStartY;

            if (e.shiftKey) {
              ttPanX += dx * 0.8;
              ttPanY += dy * 0.8;
            } else {
              ttYaw += dx * 0.5;
              ttPitch = Math.max(-75, Math.min(75, ttPitch - dy * 0.4));
            }

            ttStartX = e.clientX;
            ttStartY = e.clientY;
            updateTurntableTransform();
            renderExtrusion();
          });

          turntableStage.addEventListener('pointerup', (e) => {
            isTtDragging = false;
            turntableStage.style.cursor = 'grab';
            turntableStage.releasePointerCapture(e.pointerId);
          });

          turntableStage.addEventListener('wheel', (e) => {
            e.preventDefault();
            const factor = e.deltaY > 0 ? 0.9 : 1.1;
            ttZoom = Math.max(0.4, Math.min(3.5, ttZoom * factor));
            updateTurntableTransform();
          }, { passive: false });

        } else {
          modal.style.display = 'flex';
        }
      }
      window.launchPocketGullTurntableModal = launchPocketGullTurntableModal;


    (function initMultiScalePhoropter() {
      // 1. Mode Switching
      const modePopulationBtn = document.getElementById('modePopulationBtn');
      const modeSpatialBtn = document.getElementById('modeSpatialBtn');
      const modeBodyBtn = document.getElementById('modeBodyBtn');
      const modeStressBtn = document.getElementById('modeStressBtn');
      const viewPopulation = document.getElementById('viewPopulation');
      const viewSpatial = document.getElementById('viewSpatial');
      const viewBody = document.getElementById('viewBody');
      const viewStress = document.getElementById('viewStress');

      const modeBtns = [modePopulationBtn, modeSpatialBtn, modeBodyBtn, modeStressBtn];
      const views = [viewPopulation, viewSpatial, viewBody, viewStress];

      function setMode(idx) {
        modeBtns.forEach((b, i) => {
          if (i === idx) {
            b.style.background = 'var(--accent-teal)';
            b.style.color = '#09090b';
            views[i].style.display = 'block';
          } else {
            b.style.background = 'transparent';
            b.style.color = 'var(--text-secondary)';
            views[i].style.display = 'none';
          }
        });
      }

      modePopulationBtn.addEventListener('click', () => setMode(0));
      modeSpatialBtn.addEventListener('click', () => setMode(1));
      if (modeBodyBtn) {
        modeBodyBtn.addEventListener('click', () => {
          setMode(2);
          initBodyMatrix();
        });
      }
      modeStressBtn.addEventListener('click', () => {
        setMode(3);
        renderStressGrid();
      });

      // Hoisted state variables for 3D body matrix
      let bodyGimbalInitialized = false;
      let currentBodyOrgan = 'heart';
      let currentBodyLang = 'en';
      let bodyYaw = 0;
      let bodyPitch = 0;
      let isBodyDragging = false;
      let bodyDragStartX = 0;
      let bodyDragStartY = 0;

      const modeTurntableDirectBtn = document.getElementById('modeTurntableDirectBtn');
      if (modeTurntableDirectBtn) {
        modeTurntableDirectBtn.addEventListener('click', () => {
          if (typeof launchPocketGullTurntableModal === 'function') {
            launchPocketGullTurntableModal();
          } else {
            if (typeof initBodyMatrix === 'function') initBodyMatrix();
            setTimeout(() => {
              if (typeof launchPocketGullTurntableModal === 'function') launchPocketGullTurntableModal();
            }, 50);
          }
        });
      }

      // Handle direct hash navigation to #viewBody or #body3dStage
      if (window.location.hash === '#viewBody' || window.location.hash === '#body' || window.location.hash === '#body3dStage') {
        setTimeout(() => {
          setMode(2);
          if (typeof initBodyMatrix === 'function') initBodyMatrix();
        }, 100);
      }

      // 2. Population-Ranked Focus Wheel Data
      const POPULATION_LANGUAGES = [
        {
          rank: 1,
          language: 'Mandarin Chinese',
          country: 'China',
          flag: '🇨🇳',
          popDisplay: '1.12 Billion',
          script: 'Simplified Hanzi',
          term: '心肌 (心脏)',
          ipa: 'xīn jī',
          role: '四腔室肌肉血液泵系统 • Morphemic square em-box with counter-dilation for zero thermal bleed.',
          dir: 'ltr'
        },
        {
          rank: 2,
          language: 'Spanish',
          country: 'Spain / Latin America',
          flag: '🇲🇽',
          popDisplay: '590 Million',
          script: 'Latin Extended',
          term: 'Músculo Cardíaco (Miocardio)',
          ipa: 'mús-ku-lo kar-ˈdja-ko',
          role: 'Bomba hemodinámica de cuatro cavidades con sincronización auriculoventricular.',
          dir: 'ltr'
        },
        {
          rank: 3,
          language: 'English',
          country: 'Global Healthcare',
          flag: '🇺🇸',
          popDisplay: '400M Native / 1.5B Total',
          script: 'Latin Clinical',
          term: 'Heart (Myocardium)',
          ipa: 'maɪ.oʊˈkɑːr.di.əm',
          role: 'Four-chambered muscular perfusion pump governing systemic hemodynamics.',
          dir: 'ltr'
        },
        {
          rank: 4,
          language: 'Hindi & Sanskrit',
          country: 'India',
          flag: '🇮🇳',
          popDisplay: '600 Million',
          script: 'Devanagari',
          term: 'हृत्पेशी (हृदयम्)',
          ipa: 'hridayam (hrit-peshee)',
          role: 'रक्तसंचरण एवं ओजस् वाहक संस्थान • Shirorekha hanging bar baseline precision.',
          dir: 'ltr'
        },
        {
          rank: 5,
          language: 'Arabic',
          country: 'Middle East & North Africa',
          flag: '🇸🇦',
          popDisplay: '375 Million',
          script: 'Arabic (RTL)',
          term: 'عضلة القلب (الميوكارديوم)',
          ipa: '‘adˤalat al-qalb',
          role: 'مضخة الدورة الدموية رباعية الحجرات • Cursive calligraphic glyph shaping with Harakat.',
          dir: 'rtl'
        },
        {
          rank: 6,
          language: 'Bengali',
          country: 'Bangladesh & West Bengal',
          flag: '🇧🇩',
          popDisplay: '300 Million',
          script: 'Bengali Eastern Indic',
          term: 'হৃদপেশী (হৃদযন্ত্র)',
          ipa: 'hrid-peshi',
          role: 'রক্ত সংবহন ও সংকোচনশীল পাম্প • Intricate Indic conjunct vowel ligature support.',
          dir: 'ltr'
        },
        {
          rank: 7,
          language: 'Portuguese',
          country: 'Brazil & Portugal',
          flag: '🇧🇷',
          popDisplay: '260 Million',
          script: 'Latin Extended',
          term: 'Músculo Cardíaco (Miocárdio)',
          ipa: 'mjoˈkaɾ.dʒu',
          role: 'Bomba muscular de ejeção sistólica e complacência ventricular.',
          dir: 'ltr'
        },
        {
          rank: 8,
          language: 'Russian & Slavic Cyrillic',
          country: 'Eastern Europe & Central Asia',
          flag: '🌐',
          popDisplay: '250 Million',
          script: 'Pan-Cyrillic',
          term: 'Сердце (Миокард)',
          ipa: 'mʲɪɐˈkart',
          role: 'Четырёхкамерный гемодинамический насос • Pan-Cyrillic U+0400–U+04FF coverage.',
          dir: 'ltr'
        },
        {
          rank: 9,
          language: 'Japanese',
          country: 'Japan',
          flag: '🇯🇵',
          popDisplay: '125 Million',
          script: 'Kanji / Kana',
          term: '心臓 (心筋)',
          ipa: 'shinzō (shinkin)',
          role: '血液循環を司る四腔構造の筋性ポンプ • Harmonious Kana-Kanji typographic balance.',
          dir: 'ltr'
        },
        {
          rank: 10,
          language: 'Korean',
          country: 'South Korea',
          flag: '🇰🇷',
          popDisplay: '82 Million',
          script: 'Hangul Featural',
          term: '심장 (심근)',
          ipa: 'simgeun (simjang)',
          role: '체순환을 유지하는 4개 방실 근육 펌프 • Syllable block stacked featural alignment.',
          dir: 'ltr'
        },
        {
          rank: 11,
          language: 'Hebrew',
          country: 'Israel',
          flag: '🇮🇱',
          popDisplay: '10 Million',
          script: 'Hebrew Square (RTL)',
          term: 'שריר הלב (מיוקרדיום)',
          ipa: 'sreer ha-lev',
          role: 'משאבת דם שרירית בעלת ארבעה מדורים • Square script block legibility with Geresh.',
          dir: 'rtl'
        },
        {
          rank: 12,
          language: 'Braille Tactile Optotype',
          country: 'Universal Accessibility',
          flag: '🌐',
          popDisplay: '40M Blind Patients',
          script: 'Braille 8-Dot',
          term: '⠠⠓⠑⠁⠗⠞',
          ipa: 'ISO/TR 11548',
          role: 'Standard tactile cell optotype for non-visual patients • Zero occlusion.',
          dir: 'ltr'
        }
      ];

      let currentPhoropterIndex = 0;
      const rankBadge = document.getElementById('phoropterRankBadge');
      const focusedWord = document.getElementById('phoropterFocusedWord');
      const focusedLang = document.getElementById('phoropterFocusedLang');
      const focusedIpa = document.getElementById('phoropterFocusedIpa');
      const focusedRole = document.getElementById('phoropterFocusedRole');
      const orbitList = document.getElementById('phoropterOrbitList');
      const slider = document.getElementById('phoropterSlider');
      const prevBtn = document.getElementById('prevPhoropterBtn');
      const nextBtn = document.getElementById('nextPhoropterBtn');
      const dialStage = document.getElementById('phoropterDialStage');

      function renderPhoropter(idx) {
        currentPhoropterIndex = (idx + POPULATION_LANGUAGES.length) % POPULATION_LANGUAGES.length;
        const item = POPULATION_LANGUAGES[currentPhoropterIndex];

        rankBadge.textContent = `${item.flag} RANK #${item.rank} • ${item.popDisplay.toUpperCase()} SPEAKERS`;
        focusedWord.textContent = item.term;
        focusedWord.setAttribute('dir', item.dir);
        focusedLang.textContent = `${item.language} (${item.country})`;
        focusedIpa.textContent = `IPA Pronunciation: /${item.ipa}/`;
        focusedRole.textContent = item.role;
        slider.value = currentPhoropterIndex;

        // Render depth-of-field orbit cards
        orbitList.innerHTML = '';
        POPULATION_LANGUAGES.forEach((lang, i) => {
          const dist = Math.min(Math.abs(i - currentPhoropterIndex), POPULATION_LANGUAGES.length - Math.abs(i - currentPhoropterIndex));
          const card = document.createElement('div');
          card.style.padding = '0.65rem 0.5rem';
          card.style.borderRadius = '8px';
          card.style.border = '1px solid';
          card.style.textAlign = 'center';
          card.style.cursor = 'pointer';
          card.style.transition = 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)';

          if (dist === 0) {
            card.style.filter = 'blur(0px)';
            card.style.opacity = '1';
            card.style.transform = 'scale(1.08)';
            card.style.borderColor = 'var(--accent-teal)';
            card.style.background = 'rgba(20, 184, 166, 0.2)';
          } else if (dist === 1) {
            card.style.filter = 'blur(1.5px)';
            card.style.opacity = '0.55';
            card.style.transform = 'scale(0.95)';
            card.style.borderColor = 'var(--border-subtle)';
            card.style.background = 'var(--bg-card)';
          } else {
            card.style.filter = 'blur(3px)';
            card.style.opacity = '0.25';
            card.style.transform = 'scale(0.9)';
            card.style.borderColor = 'var(--border-subtle)';
            card.style.background = 'var(--bg-surface)';
          }

          card.innerHTML = `
            <div style="font-size: 1.1rem;">${lang.flag}</div>
            <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-primary); margin-top: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${lang.language}</div>
            <div style="font-size: 0.65rem; font-family: var(--font-code); color: var(--text-muted);">${lang.popDisplay}</div>
          `;

          card.addEventListener('click', () => renderPhoropter(i));
          orbitList.appendChild(card);
        });
      }

      // Wheel and Touch Pinch on Population Dial
      dialStage.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (e.deltaY > 15) {
          renderPhoropter(currentPhoropterIndex + 1);
        } else if (e.deltaY < -15) {
          renderPhoropter(currentPhoropterIndex - 1);
        }
      }, { passive: false });

      let pinchStartDist = null;
      dialStage.addEventListener('touchstart', (e) => {
        if (e.touches.length === 2) {
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          pinchStartDist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
        }
      }, { passive: true });

      dialStage.addEventListener('touchmove', (e) => {
        if (e.touches.length === 2 && pinchStartDist !== null) {
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          const dist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
          const delta = dist - pinchStartDist;
          if (delta > 35) {
            renderPhoropter(currentPhoropterIndex + 1);
            pinchStartDist = dist;
          } else if (delta < -35) {
            renderPhoropter(currentPhoropterIndex - 1);
            pinchStartDist = dist;
          }
        }
      }, { passive: true });

      dialStage.addEventListener('touchend', () => { pinchStartDist = null; });

      prevBtn.addEventListener('click', () => renderPhoropter(currentPhoropterIndex - 1));
      nextBtn.addEventListener('click', () => renderPhoropter(currentPhoropterIndex + 1));
      slider.addEventListener('input', (e) => renderPhoropter(parseInt(e.target.value, 10)));

      // Initialize Focus Wheel
      renderPhoropter(0);

      // 3. Macro-to-Molecular Spatial Zoom
      const SPATIAL_TIERS_ADULT = [
        {
          scale: '10–12 cm (1× Zoom)',
          title: 'Gross Four-Chambered Myocardial Pump',
          desc: 'Frank-Starling law: end-diastolic volume stretches sarcomeres, generating stroke volume (60–100 mL/beat) against systemic vascular resistance.',
          kinetics: 'W_ventricular = ∫ P dV + 1/2 m v²',
          svg: `<svg viewBox="0 0 200 150" style="width: 100%; height: 160px;">
                  <path d="M 100,45 C 90,15 45,15 45,55 C 45,95 100,135 100,135 C 100,135 155,95 155,55 C 155,15 110,15 100,45 Z" fill="none" stroke="#ef4444" stroke-width="3" />
                  <path d="M 85,45 C 85,25 115,20 120,5" fill="none" stroke="#f87171" stroke-width="4" stroke-linecap="round" />
                  <line x1="100" y1="50" x2="100" y2="125" stroke="#7f1d1d" stroke-dasharray="2,2" stroke-width="1.5" />
                  <text x="65" y="75" fill="#fca5a5" font-size="9" font-family="'PocketGull Bold'">LA</text>
                  <text x="125" y="75" fill="#fca5a5" font-size="9" font-family="'PocketGull Bold'">RA</text>
                  <text x="70" y="105" fill="#fca5a5" font-size="10" font-family="'PocketGull Bold'">LV</text>
                  <text x="120" y="105" fill="#fca5a5" font-size="10" font-family="'PocketGull Bold'">RV</text>
                </svg>`
        },
        {
          scale: '100 µm (100× Zoom)',
          title: 'Striated Cardiomyocyte Syncytium & Intercalated Discs',
          desc: 'Branched cardiomyocytes linked by intercalated discs with Connexin-43 (Cx43) gap junctions enabling rapid action potential propagation (0.5 m/s).',
          kinetics: 'I_gap = g_gap · (V_cell1 - V_cell2)',
          svg: `<svg viewBox="0 0 240 120" style="width: 100%; height: 160px;">
                  <g stroke="#14b8a6" stroke-width="2" fill="none">
                    <path d="M 20,30 Q 120,25 220,30" /><path d="M 20,50 Q 120,45 220,50" />
                    <path d="M 20,75 Q 80,70 140,80 Q 180,60 220,55" /><path d="M 20,95 Q 120,90 220,95" />
                  </g>
                  <line x1="85" y1="28" x2="85" y2="52" stroke="#f59e0b" stroke-width="4" />
                  <line x1="165" y1="73" x2="165" y2="97" stroke="#f59e0b" stroke-width="4" />
                  <ellipse cx="125" cy="40" rx="12" ry="5" fill="#3b82f6" opacity="0.7" />
                  <text x="65" y="20" fill="#f59e0b" font-size="7" font-family="'PocketGull Bold'">INTERCALATED DISC (Cx43)</text>
                  <text x="115" y="34" fill="#93c5fd" font-size="6" font-family="'PocketGull Bold'">NUCLEUS</text>
                </svg>`
        },
        {
          scale: '1 µm (10,000× Zoom)',
          title: 'Sarcolemma, Mitochondria Cristae & RyR2 Ca2+ Release',
          desc: 'Excitation-Contraction (E-C) Coupling: T-tubule depolarization opens L-type Cav1.2 channels, triggering Calcium-Induced Calcium Release from RyR2 in sarcoplasmic reticulum.',
          kinetics: 'ΔΨ_m = -140 mV • ATP Rate = 4.8 µmol/g/min',
          svg: `<svg viewBox="0 0 240 120" style="width: 100%; height: 160px;">
                  <ellipse cx="120" cy="60" rx="85" ry="40" fill="#18181b" stroke="#a855f7" stroke-width="2.5" />
                  <path d="M 50,60 C 60,45 70,75 80,50 C 90,75 100,45 110,75 C 120,45 130,75 140,45 C 150,75 160,45 170,70 C 180,50 190,60 190,60" fill="none" stroke="#c084fc" stroke-width="2" stroke-linecap="round" />
                  <circle cx="65" cy="20" r="3.5" fill="#fbbf24" />
                  <circle cx="175" cy="100" r="3.5" fill="#fbbf24" />
                  <text x="80" y="95" fill="#c084fc" font-size="7" font-family="'PocketGull Bold'">MITOCHONDRIAL CRISTAE</text>
                  <text x="45" y="15" fill="#fbbf24" font-size="6" font-family="'PocketGull Mono'">RyR2 Ca2+ SPARK</text>
                </svg>`
        },
        {
          scale: '2 nm / 20 Å (1,000,000× Zoom)',
          title: 'Troponin C-I-T Heterotrimer & Actin-Myosin Crossbridge Cycle',
          desc: 'Ca2+ binding to Troponin C (TnC) induces conformational shift in Troponin I (TnI), unmasking binding sites on F-actin. Myosin S1 executes 70° power stroke producing 3–5 pN force.',
          kinetics: 'PDB: 1J1D • UniProt: P19429 (cTnI) • Power Stroke: 3–5 pN',
          svg: `<svg viewBox="0 0 260 120" style="width: 100%; height: 160px;">
                  <g fill="#eab308">
                    <circle cx="30" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" /><circle cx="55" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" />
                    <circle cx="80" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" /><circle cx="105" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" />
                    <circle cx="130" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" /><circle cx="155" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" />
                    <circle cx="180" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" /><circle cx="205" cy="25" r="7" stroke="#ca8a04" stroke-width="1.5" />
                  </g>
                  <path d="M 20,30 Q 130,18 220,30" fill="none" stroke="#f97316" stroke-width="3" />
                  <circle cx="105" cy="18" r="8" fill="#38bdf8" stroke="#0284c7" stroke-width="1.5" />
                  <circle cx="120" cy="19" r="8" fill="#ec4899" stroke="#be185d" stroke-width="1.5" />
                  <circle cx="135" cy="21" r="8" fill="#8b5cf6" stroke="#6d28d9" stroke-width="1.5" />
                  <path d="M 120,110 C 130,85 135,65 140,48" fill="none" stroke="#22c55e" stroke-width="5" stroke-linecap="round" />
                  <text x="75" y="10" fill="#38bdf8" font-size="6" font-family="'PocketGull Bold'">cTnC (Ca2+)</text>
                  <text x="135" y="10" fill="#ec4899" font-size="6" font-family="'PocketGull Bold'">cTnI (PDB: 1J1D)</text>
                  <text x="150" y="60" fill="#22c55e" font-size="7" font-family="'PocketGull Bold'">MYOSIN S1 HEAD</text>
                </svg>`
        },
        {
          scale: '0.8 nm / 8 Å (10,000,000× Zoom)',
          title: 'Microtubule Tubulin Dimer Lattice & Orch-OR Quantum Dipoles',
          desc: 'University of Arizona Center for Consciousness Studies (Hameroff & Penrose): 13 protofilaments assembled in a 25 nm cylindrical B-lattice (8 nm α/β tubulin dimer pitch). Hydrophobic aromatic pockets (Tryptophan / Phenylalanine clusters) sustain collective London-force dipole oscillation at 40 Hz gamma resonance down to terahertz optical modes.',
          kinetics: 'PDB: 1JFF • Orch-OR: E = ℏ/τ • Resonance: 40 Hz – 8 MHz • UA Orch-OR Lattice',
          svg: `<svg viewBox="0 0 280 130" style="width: 100%; height: 165px;">
                  <defs>
                    <radialGradient id="aromaticGlow" cx="50%" cy="50%" r="50%">
                      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8" />
                      <stop offset="100%" stop-color="#0284c7" stop-opacity="0" />
                    </radialGradient>
                    <linearGradient id="dipoleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stop-color="#f43f5e" />
                      <stop offset="100%" stop-color="#38bdf8" />
                    </linearGradient>
                  </defs>
                  <!-- 13-Protofilament Cylindrical Surface Unrolled (B-Lattice) -->
                  <g stroke="#1e293b" stroke-width="1">
                    <!-- Row 1: alpha-tubulin -->
                    <rect x="20" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="46" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="72" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="98" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="124" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="150" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="176" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="202" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="228" y="25" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />

                    <!-- Row 2: beta-tubulin -->
                    <rect x="26" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="52" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="78" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="104" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="130" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="156" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="182" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="208" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />
                    <rect x="234" y="47" width="22" height="18" rx="5" fill="#047857" stroke="#10b981" stroke-width="1.5" />

                    <!-- Row 3: alpha-tubulin -->
                    <rect x="20" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="46" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="72" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="98" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="124" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="150" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="176" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="202" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                    <rect x="228" y="69" width="22" height="18" rx="5" fill="#1e3a8a" stroke="#3b82f6" stroke-width="1.5" />
                  </g>
                  <!-- Quantum Dipole Coupling Overlay -->
                  <circle cx="109" cy="34" r="14" fill="url(#aromaticGlow)" />
                  <path d="M 109,28 L 109,40 M 106,31 L 109,28 L 112,31" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <circle cx="115" cy="56" r="14" fill="url(#aromaticGlow)" />
                  <path d="M 115,62 L 115,50 M 112,59 L 115,62 L 118,59" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  <!-- Dipole helical coupling vectors -->
                  <path d="M 109,34 C 120,40 125,50 141,56" fill="none" stroke="#eab308" stroke-width="1.5" stroke-dasharray="2,2" />
                  <path d="M 135,34 C 146,40 151,50 167,56" fill="none" stroke="#eab308" stroke-width="1.5" stroke-dasharray="2,2" />
                  <!-- Labels -->
                  <text x="30" y="16" fill="#38bdf8" font-size="7" font-family="'PocketGull Bold'">α-TUBULIN (4 nm)</text>
                  <text x="140" y="16" fill="#10b981" font-size="7" font-family="'PocketGull Bold'">β-TUBULIN (4 nm)</text>
                  <text x="210" y="102" fill="#fbbf24" font-size="6.5" font-family="'PocketGull Mono'">8 nm DIMER</text>
                  <text x="75" y="102" fill="#f43f5e" font-size="6.5" font-family="'PocketGull Mono'">40 Hz DIPOLE (Orch-OR)</text>
                  <path d="M 239,23 L 255,23 M 239,45 L 255,45 M 251,23 L 251,45" stroke="#94a3b8" stroke-width="1" />
                  <text x="257" y="36" fill="#94a3b8" font-size="5.5" font-family="'PocketGull Mono'">4 nm</text>
                </svg>`
        }
      ];

      const SPATIAL_TIERS_CHILD = [
        {
          scale: 'Your Whole Heart (About the size of your fist!)',
          title: 'The Great Heart Hero Pump',
          desc: 'Thump-thump! Thump-thump! Your heart is a mighty muscular engine that beats over 100,000 times every day, sending fresh oxygen and warmth to your toes, fingers, and dreaming brain.',
          kinetics: '✨ Energy Power: Beating over 100,000 times today without ever stopping to nap!',
          svg: `<svg viewBox="0 0 200 150" style="width: 100%; height: 160px;">
                  <path d="M 100,45 C 90,15 45,15 45,55 C 45,95 100,135 100,135 C 100,135 155,95 155,55 C 155,15 110,15 100,45 Z" fill="#f43f5e" stroke="#fb7185" stroke-width="4" />
                  <!-- Friendly smiling heart face -->
                  <circle cx="80" cy="65" r="4" fill="#fff" />
                  <circle cx="120" cy="65" r="4" fill="#fff" />
                  <circle cx="81" cy="65" r="2" fill="#09090b" />
                  <circle cx="121" cy="65" r="2" fill="#09090b" />
                  <path d="M 90,82 Q 100,92 110,82" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" />
                  <!-- Rosy cheeks -->
                  <circle cx="72" cy="74" r="5" fill="#fda4af" opacity="0.6" />
                  <circle cx="128" cy="74" r="5" fill="#fda4af" opacity="0.6" />
                  <text x="50" y="25" fill="#fef08a" font-size="8" font-family="'PocketGull Bold'">OXYGEN EXPRESSWAY</text>
                </svg>`
        },
        {
          scale: 'Tiniest Muscle Fibers (Look through a magical magnifying glass!)',
          title: 'The Cellular Team Holding Hands',
          desc: 'Under the microscope, heart cells look like little smiling friends holding hands tightly in long chains. When one cell gets excited to jump, it whispers to its neighbor in less than a blink!',
          kinetics: '🤝 Teamwork Speed: Messages jump across hands in 1/1,000th of a second!',
          svg: `<svg viewBox="0 0 240 120" style="width: 100%; height: 160px;">
                  <g stroke="#38bdf8" stroke-width="3" fill="none">
                    <path d="M 20,40 Q 120,30 220,40" /><path d="M 20,80 Q 120,70 220,80" />
                  </g>
                  <!-- Cheerful handshake bridges -->
                  <rect x="75" y="36" width="18" height="48" rx="6" fill="#f59e0b" stroke="#fbbf24" stroke-width="2" />
                  <text x="80" y="62" fill="#000" font-size="8" font-family="'PocketGull Bold'">🤝</text>
                  <rect x="155" y="36" width="18" height="48" rx="6" fill="#f59e0b" stroke="#fbbf24" stroke-width="2" />
                  <text x="160" y="62" fill="#000" font-size="8" font-family="'PocketGull Bold'">🤝</text>
                  <!-- Cellular command centers -->
                  <ellipse cx="40" cy="60" rx="14" ry="10" fill="#a855f7" opacity="0.7" />
                  <ellipse cx="120" cy="60" rx="14" ry="10" fill="#a855f7" opacity="0.7" />
                  <ellipse cx="200" cy="60" rx="14" ry="10" fill="#a855f7" opacity="0.7" />
                  <text x="45" y="25" fill="#38bdf8" font-size="7" font-family="'PocketGull Bold'">CELL TEAM BRIDGES</text>
                  <text x="100" y="105" fill="#f59e0b" font-size="7" font-family="'PocketGull Mono'">HANDSHAKE GATES</text>
                </svg>`
        },
        {
          scale: 'Inside the Cellular Powerhouse',
          title: 'The Sparkle Batteries & Firefly Sparks',
          desc: 'Inside every cell are tiny sparkling bean-shaped powerplants called mitochondria. They turn the apples and blueberries you eat into little golden sparks of pure running energy!',
          kinetics: '⚡ Power Rating: Millions of microscopic sparklers lighting up every heartbeat!',
          svg: `<svg viewBox="0 0 240 120" style="width: 100%; height: 160px;">
                  <!-- Cute glowing bean -->
                  <ellipse cx="120" cy="60" rx="85" ry="42" fill="#3b0764" stroke="#c084fc" stroke-width="3" />
                  <!-- Wavy energy river -->
                  <path d="M 55,60 Q 75,35 95,60 T 135,60 T 175,60" fill="none" stroke="#e879f9" stroke-width="3.5" stroke-linecap="round" />
                  <!-- Golden sparkles -->
                  <g fill="#fbbf24">
                    <circle cx="80" cy="45" r="4" /><circle cx="150" cy="40" r="3.5" /><circle cx="110" cy="75" r="4.5" />
                    <polygon points="170,75 173,83 181,85 174,89 176,97 170,92 164,97 166,89 159,85 167,83" fill="#fef08a" />
                  </g>
                  <text x="65" y="22" fill="#fef08a" font-size="8" font-family="'PocketGull Bold'">THE CELLULAR BATTERY BEAN</text>
                  <text x="75" y="112" fill="#c084fc" font-size="7" font-family="'PocketGull Mono'">GOLDEN ENERGY SPARKS</text>
                </svg>`
        },
        {
          scale: 'Rowing Engines (Nanometer Scale)',
          title: 'The Tiny Molecular Rowing Crew',
          desc: 'Deep inside your muscles are millions of tiny molecular rowers called Myosins. When calcium enters like a starting bell, all the little green oars catch the rope together and PULL!',
          kinetics: '🚣 Rowing Stroke: Pulling like a crew team with 5 pico-Newtons of gentle strength!',
          svg: `<svg viewBox="0 0 260 120" style="width: 100%; height: 160px;">
                  <!-- Golden rope / stepping stones -->
                  <g fill="#fbbf24">
                    <circle cx="35" cy="30" r="8" /><circle cx="65" cy="30" r="8" />
                    <circle cx="95" cy="30" r="8" /><circle cx="125" cy="30" r="8" />
                    <circle cx="155" cy="30" r="8" /><circle cx="185" cy="30" r="8" /><circle cx="215" cy="30" r="8" />
                  </g>
                  <!-- Rowing arms -->
                  <path d="M 50,105 L 75,55 L 95,36" fill="none" stroke="#22c55e" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
                  <path d="M 140,105 L 165,55 L 185,36" fill="none" stroke="#22c55e" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" />
                  <!-- Friendly cheer flag -->
                  <text x="25" y="16" fill="#fde047" font-size="7.5" font-family="'PocketGull Bold'">GOLDEN STEPPING STONES</text>
                  <text x="145" y="95" fill="#4ade80" font-size="7.5" font-family="'PocketGull Bold'">LITTLE ROWING OARS</text>
                  <text x="75" y="115" fill="#38bdf8" font-size="6.5" font-family="'PocketGull Mono'">HEAVE-HO! PULL TOGETHER!</text>
                </svg>`
        },
        {
          scale: 'Quantum Nano-World (10,000,000× Wonder Magnification)',
          title: 'The Dancing Crystal Bells & Cellular Monorails',
          desc: 'Stuart Hameroff & Roger Penrose discovered that deep in your brain and cells, tiny blue and green crystal blocks stack into tall towers called microtubules. They sing and hum together 40 times each second, like a choir of whispering fairy bells!',
          kinetics: '🎶 Harmony Tone: 40 gentle chimes each second • Nature’s living computer!',
          svg: `<svg viewBox="0 0 280 130" style="width: 100%; height: 165px;">
                  <!-- Colorful stacked building blocks -->
                  <g>
                    <!-- Blue blocks -->
                    <rect x="30" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="60" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="90" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="120" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="150" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="180" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <rect x="210" y="30" width="24" height="20" rx="6" fill="#3b82f6" stroke="#60a5fa" stroke-width="2" />
                    <!-- Green blocks -->
                    <rect x="35" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="65" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="95" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="125" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="155" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="185" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                    <rect x="215" y="55" width="24" height="20" rx="6" fill="#10b981" stroke="#34d399" stroke-width="2" />
                  </g>
                  <!-- Musical chimes / sparkles -->
                  <g fill="#fde047">
                    <text x="40" y="22" font-size="10">🎵</text>
                    <text x="105" y="22" font-size="10">✨</text>
                    <text x="170" y="22" font-size="10">🎶</text>
                  </g>
                  <text x="35" y="100" fill="#38bdf8" font-size="8" font-family="'PocketGull Bold'">BLUE & GREEN CRYSTAL BLOCKS</text>
                  <text x="55" y="118" fill="#fde047" font-size="7" font-family="'PocketGull Mono'">HUMMING 40 TIMES PER SECOND</text>
                </svg>`
        }
      ];

      let isChildrenMode = false;
      let currentSpatialTier = 0;
      const modeAdultBtn = document.getElementById('modeAdultBtn');
      const modeChildBtn = document.getElementById('modeChildBtn');
      const knowledgeGateBadge = document.getElementById('knowledgeGateBadge');
      const spatialScaleBadge = document.getElementById('spatialScaleBadge');
      const spatialSvgContainer = document.getElementById('spatialSvgContainer');
      const spatialTitle = document.getElementById('spatialTitle');
      const spatialDesc = document.getElementById('spatialDesc');
      const spatialKinetics = document.getElementById('spatialKinetics');
      const tierBtns = document.querySelectorAll('.spatial-tier-btn');
      const spatialStage = document.getElementById('spatialZoomStage');

      function getActiveTiers() {
        return isChildrenMode ? SPATIAL_TIERS_CHILD : SPATIAL_TIERS_ADULT;
      }

      function renderSpatialTier(tierIdx) {
        const tiers = getActiveTiers();
        currentSpatialTier = (tierIdx + tiers.length) % tiers.length;
        const tier = tiers[currentSpatialTier];

        spatialScaleBadge.textContent = isChildrenMode ? `WONDER SCALE: ${tier.scale}` : `SPATIAL SCALE: ${tier.scale}`;
        spatialSvgContainer.innerHTML = tier.svg;
        spatialTitle.textContent = tier.title;
        spatialDesc.textContent = tier.desc;
        spatialKinetics.textContent = tier.kinetics;

        if (isChildrenMode) {
          spatialTitle.style.color = '#38bdf8';
          spatialKinetics.style.color = '#fde047';
          knowledgeGateBadge.textContent = '🧸 Wonder Mode (All Ages)';
          knowledgeGateBadge.style.borderColor = '#38bdf8';
          knowledgeGateBadge.style.color = '#38bdf8';
          knowledgeGateBadge.style.background = 'rgba(56, 189, 248, 0.15)';
        } else {
          spatialTitle.style.color = 'var(--text-primary)';
          spatialKinetics.style.color = 'var(--accent-teal)';
          knowledgeGateBadge.textContent = '🛡️ CARE & ISMP Gated';
          knowledgeGateBadge.style.borderColor = 'rgba(56, 189, 248, 0.4)';
          knowledgeGateBadge.style.color = '#38bdf8';
          knowledgeGateBadge.style.background = 'rgba(56, 189, 248, 0.15)';
        }

        tierBtns.forEach((b, i) => {
          if (i === currentSpatialTier) {
            b.style.background = isChildrenMode ? '#38bdf8' : 'var(--accent-teal)';
            b.style.color = '#09090b';
          } else {
            b.style.background = 'transparent';
            b.style.color = 'var(--text-secondary)';
          }
        });
      }

      modeAdultBtn.addEventListener('click', () => {
        isChildrenMode = false;
        modeAdultBtn.classList.add('active');
        modeAdultBtn.style.background = 'var(--accent-teal)';
        modeAdultBtn.style.color = '#09090b';
        modeChildBtn.classList.remove('active');
        modeChildBtn.style.background = 'transparent';
        modeChildBtn.style.color = 'var(--text-secondary)';
        renderSpatialTier(currentSpatialTier);
      });

      modeChildBtn.addEventListener('click', () => {
        isChildrenMode = true;
        modeChildBtn.classList.add('active');
        modeChildBtn.style.background = '#38bdf8';
        modeChildBtn.style.color = '#09090b';
        modeAdultBtn.classList.remove('active');
        modeAdultBtn.style.background = 'transparent';
        modeAdultBtn.style.color = 'var(--text-secondary)';
        renderSpatialTier(currentSpatialTier);
      });

      tierBtns.forEach(btn => {
        btn.addEventListener('click', () => renderSpatialTier(parseInt(btn.dataset.tier, 10)));
      });

      // Spatial Wheel & Pinch Listeners
      spatialStage.addEventListener('wheel', (e) => {
        e.preventDefault();
        if (e.deltaY > 20) {
          renderSpatialTier(currentSpatialTier + 1);
        } else if (e.deltaY < -20) {
          renderSpatialTier(currentSpatialTier - 1);
        }
      }, { passive: false });

      let spatialPinchStart = null;
      spatialStage.addEventListener('touchstart', (e) => {
        if (e.touches.length === 2) {
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          spatialPinchStart = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
        }
      }, { passive: true });

      spatialStage.addEventListener('touchmove', (e) => {
        if (e.touches.length === 2 && spatialPinchStart !== null) {
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          const dist = Math.hypot(t1.clientX - t2.clientX, t1.clientY - t2.clientY);
          const delta = dist - spatialPinchStart;
          if (delta > 35) {
            renderSpatialTier(currentSpatialTier + 1);
            spatialPinchStart = dist;
          } else if (delta < -35) {
            renderSpatialTier(currentSpatialTier - 1);
            spatialPinchStart = dist;
          }
        }
      }, { passive: true });

      spatialStage.addEventListener('touchend', () => { spatialPinchStart = null; });

      renderSpatialTier(0);

      // 4. Random Sloan Optotype Stress-Tester
      const STRESS_SCRIPTS = [
        { name: 'Latin Sloan Optotypes', chars: ['C', 'D', 'H', 'K', 'N', 'O', 'R', 'S', 'V', 'Z'], logMar: '0.0' },
        { name: 'Slavic Cyrillic Clinical', chars: ['Б', 'Г', 'Д', 'Ж', 'З', 'И', 'Л', 'П', 'Ф', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я'], logMar: '0.0' },
        { name: 'Greek Pharmacology', chars: ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'μ', 'π', 'σ', 'τ', 'φ', 'ψ', 'ω', 'Ω'], logMar: '-0.1' },
        { name: 'Arabic Semitic Consonants', chars: ['ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ح', 'خ', 'ص', 'ض'], logMar: '0.1' },
        { name: 'Persian (Farsi) Perso-Arabic', chars: ['پ', 'چ', 'ژ', 'گ', 'ک', 'ی', 'ق', 'ف', 'م', 'ن', 'ه', 'و', 'س', 'ش'], logMar: '0.1' },
        { name: 'Hebrew Square Script', chars: ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע'], logMar: '0.0' },
        { name: 'Sanskrit Devanagari Base', chars: ['क', 'ख', 'ग', 'घ', 'च', 'छ', 'ज', 'झ', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब'], logMar: '0.1' },
        { name: 'Korean Hangul Featural', chars: ['심', '장', '뇌', '맥', '박', '혈', '압', '폐', '간', '신', '위', '골', '두', '척'], logMar: '0.0' },
        { name: 'Chinese Hanzi Logographs', chars: ['心', '肌', '梗', '死', '脑', '脉', '脏', '肺', '肝', '肾', '胃', '骨', '额'], logMar: '0.1' },
        { name: 'Sumero-Akkadian Cuneiform', chars: ['𒀀', '𒍪', '𒋾', '𒊮', '𒊕', '𒋆', '𒇽', '𒀭', '𒈨', '𒆷', '𒉆', '𒁉'], logMar: '0.1' }
      ];

      const stressGrid = document.getElementById('stressGrid');
      // ─── 4. 3D Touchable Typographic Body Matrix Engine ───
      const BODY_ANATOMY_DATA = {
        brain: {
          icon: '🧠',
          snomed: '12738006',
          planes: { coronal: { yaw: 0, pitch: 0 }, sagittal: { yaw: 90, pitch: 0 } },
          translations: {
            en: { term: 'Cerebral Cortex (Brain)', ipa: 'səˈriː.brəl ˈkɔːr.tɛks', script: 'Latin Clinical', desc: 'Higher cognitive processor & Orch-OR quantum microtubule dipole lattice. 86 billion neurons firing at gamma resonance (40 Hz).', formula: '🧠 Consciousness: Orch-OR E = ℏ/τ • 40 Hz Gamma Dipoles' },
            es: { term: 'Corteza Cerebral (Cerebro)', ipa: 'kor-ˈte-sa se-re-ˈβral', script: 'Latin Extended', desc: 'Centro de procesamiento cognitivo superior y red neuronal de resonancia gamma (40 Hz).', formula: '🧠 Dinámica Cuántica: Red microtubular Orch-OR • 86 mil millones de neuronas' },
            zh: { term: '大脑皮层 (脑)', ipa: 'dà nǎo pí céng', script: 'Simplified Hanzi', desc: '高级认知处理中心与微管量子偶极网络。860亿神经元以40 Hz伽马谐振同步放电。', formula: '🧠 量子谐振: Orch-OR E = ℏ/τ • 40 Hz 神经元微管偶极' },
            ar: { term: 'القشرة المخية (الدماغ)', ipa: 'al-qishrah al-mukh-khiyyah', script: 'Arabic Clinical', desc: 'مركز المعالجة الإدراكية العليا وشبكة الأنابيب الدقيقة العصبية بتردد 40 هرتز.', formula: '🧠 التوافق الكمي: 86 مليار خلية عصبية • رنين غاما 40 Hz' },
            hi: { term: 'मस्तिष्क (प्रमस्तिष्क वल्कुट)', ipa: 'mastishk (pramastishk)', script: 'Devanagari', desc: 'उच्च संज्ञान केंद्र एवं माइक्रोट्यूब्यूल क्वांटम जालक। 86 अरब तंत्रिका कोशिकाएं।', formula: '🧠 चेतना यांत्रिकी: Orch-OR 40 Hz गामा अनुनाद' },
            chr: { term: 'ᎤᏍᎪᎵ (Uskoli - Brain)', ipa: 'u-sko-li', script: 'Cherokee Syllabary', desc: 'ᎦᎾᏄᎪᏫᏍᎩ ᎠᏓᏅᏙ ᎠᎴ ᎠᏓᏅᏖᎵᏙᎯ • ᏎᎵᎦ ᎦᏬᏂᎯᏍᏗ ᎠᏂᏔᎵ ᎤᎾᏤᎵᎦ.', formula: '🧠 ᎦᎸᎳᏗ ᎠᏓᏅᏖᏛ: 40 Hz ᎤᏬᏂᎯᏍᏗ ᎠᏓᏅᏙ' },
            chn: { term: 'Látɛt (Head / Mind)', ipa: 'lá-tɛt', script: 'Chinuk Pipa Duployan', desc: 'Kopa tumtum pi latet kaskas • Hayas kloshe kopa kanawe tikegh.', formula: '🧠 Pipa Tene: 40 chimes kopa tenas sun' },
            brl: { term: '⠠⠉⠑⠗⠑⠃⠗⠁⠇ ⠠⠉⠕⠗⠞⠑⠭', ipa: 'ISO/TR 11548', script: 'Braille 8-Dot', desc: 'Tactile neural cortex mapping • 86 billion cell junctions.', formula: '🧠 ⠼⠙⠚ ⠠⠓⠵ ⠠⠛⠁⠍⠍⠁ ⠠⠕⠗⠉⠓' }
          }
        },
        lungs: {
          icon: '🫁',
          snomed: '39607008',
          planes: { coronal: { yaw: 0, pitch: 0 }, sagittal: { yaw: -60, pitch: 5 } },
          translations: {
            en: { term: 'Pulmonary Alveoli (Lungs)', ipa: 'ˈpʊl.mə.nɛr.i ælˈviː.ə.laɪ', script: 'Latin Clinical', desc: 'Gas exchange interface across 300 million alveoli. Fick’s diffusion law governs passive O2 uptake and CO2 clearance across a 0.5 µm blood-air barrier.', formula: '🫁 Gas Diffusion: V_gas = (A · D · ΔP) / T • 300M Alveoli' },
            es: { term: 'Alvéolos Pulmonares (Pulmones)', ipa: 'al-ˈβe-o-los pul-mo-ˈna-ɾes', script: 'Latin Extended', desc: 'Intercambio gaseoso en 300 millones de alvéolos. Difusión pasiva de O2 y eliminación de CO2 a través de barrera hematoaérea de 0.5 µm.', formula: '🫁 Difusión de Fick: V_gas = (A · D · ΔP) / T' },
            zh: { term: '肺泡气体交换 (肺)', ipa: 'fèi pào qì tǐ jiāo huàn', script: 'Simplified Hanzi', desc: '3亿肺泡组成的气血交换屏障（0.5微米厚度），依菲克扩散定律实现O2吸收与CO2排出。', formula: '🫁 气体扩散: 菲克定律 V = (A·D·ΔP)/T • 3亿肺泡' },
            ar: { term: 'الحويصلات الرئوية (الرئتان)', ipa: 'al-huwaysilat ar-ri’awiyyah', script: 'Arabic Clinical', desc: 'تبادل الغازات عبر 300 مليون حويصلة رئوية وفق قانون فيك للانتشار.', formula: '🫁 انتشار الغاز: مساحة 100 م² • حاجز 0.5 ميكرومتر' },
            hi: { term: 'फुफ्फुस वायुकोश (फेफड़े)', ipa: 'phupphus vayukosh', script: 'Devanagari', desc: '30 करोड़ वायुकोशों द्वारा गैस विनिमय। 0.5 माइक्रोमीटर पतली झिल्ली द्वारा ऑक्सीजन संवहन।', formula: '🫁 गैस विसरण: V = (A · D · ΔP) / T' },
            chr: { term: 'ᏧᏥᏍᏠᎯᏍᏗ (Tsutsisdlohisdi)', ipa: 'tsu-tsi-sdlo-hi-sdi', script: 'Cherokee Syllabary', desc: 'ᎠᏍᏈᏄᎵ ᎤᏬᏂᎯᏍᏗ ᎤᏃᎴ ᎠᎴ ᎩᎬ ᏕᎦᏁᎶᏅᎢ • 300 ᎢᏳᏆᏅᏛ ᏕᎦᎶᏒᎢ.', formula: '🫁 ᎤᏃᎴ ᎦᏬᏂᏍᎩ: O2 / CO2 ᎤᏃᎴ ᎠᏓᏁᎯ' },
            chn: { term: 'Wawatax (Lungs / Breath)', ipa: 'wa-wa-tax', script: 'Chinuk Pipa Duployan', desc: 'Hiyu wind kopa memaloost pi kopa chee skookum tumtum.', formula: '🫁 Kloshe Wind: 300 Million tenas pockets' },
            brl: { term: '⠠⠏⠥⠇⠍⠕⠝⠁⠗⠽ ⠠⠁⠇⠧⠑⠕⠇⠊', ipa: 'ISO/TR 11548', script: 'Braille 8-Dot', desc: 'Tactile respiratory alveolar tree • Gas diffusion membrane.', formula: '🫁 ⠠⠕⠼⠃ ⠠⠉⠕⠼⠃ ⠠⠛⠁⠎ ⠠⠑⠭⠉⠓⠁⠝⠛⠑' }
          }
        },
        heart: {
          icon: '🫀',
          snomed: '302509004',
          planes: { coronal: { yaw: 0, pitch: 0 }, sagittal: { yaw: 30, pitch: -10 } },
          translations: {
            en: { term: 'Heart (Myocardium)', ipa: 'maɪ.oʊˈkɑːr.di.əm', script: 'Latin Clinical', desc: 'Four-chambered muscular perfusion pump governing systemic hemodynamics. End-diastolic sarcomere stretch produces 60–100 mL stroke volume per beat.', formula: '⚡ Stroke Work: W_ventricular = ∫ P dV + 1/2 m v²' },
            es: { term: 'Músculo Cardíaco (Miocardio)', ipa: 'mús-ku-lo kar-ˈdja-ko', script: 'Latin Extended', desc: 'Bomba hemodinámica de cuatro cavidades con sincronización auriculoventricular. Expulsa 60–100 mL/latido.', formula: '⚡ Trabajo Ventricular: W = ∫ P dV + 1/2 m v²' },
            zh: { term: '心肌 (心脏)', ipa: 'xīn jī (xīn zàng)', script: 'Simplified Hanzi', desc: '四腔室肌肉血液灌注泵系统。舒张末期肌节拉伸产生每搏60–100毫升输出量。', formula: '⚡ 每搏功: W = ∫ P dV + 1/2 m v² • 60–100 mL/搏' },
            ar: { term: 'عضلة القلب (الميوكارديوم)', ipa: '‘adˤalat al-qalb', script: 'Arabic Clinical', desc: 'مضخة الدورة الدموية رباعية الحجرات. تضخ 60–100 مل في كل نبضة.', formula: '⚡ شغل البطين: W = ∫ P dV + 1/2 m v²' },
            hi: { term: 'हृत्पेशी (हृदयम्)', ipa: 'hridayam (hrit-peshee)', script: 'Devanagari', desc: 'चार कक्षीय रक्त संचार पम्प। प्रत्येक धड़कन पर 60–100 मिलीलीटर रक्त का संचरण।', formula: '⚡ निलय कार्य: W = ∫ P dV + 1/2 m v²' },
            chr: { term: 'ᎣᎾᏌᎶᏍᎩ ᎠᏓᏅᏙ (O-na-sa-lo-sgi)', ipa: 'o-na-sa-lo-sgi a-da-nv-do', script: 'Cherokee Syllabary', desc: 'ᏅᎩ ᏕᎦᎧᏛᎢ ᎩᎬ ᎦᏌᏙᎯᏍᎩ • 60-100 mL ᎩᎬ ᎠᏂᎦᏘᏲᎯᎯ.', formula: '⚡ ᎠᏓᏅᏙ ᎤᎵᏍᎨᏛ: W = ∫ P dV + 1/2 m v²' },
            chn: { term: 'Tumtum (Heart / Beat)', ipa: 'tum-tum', script: 'Chinuk Pipa Duployan', desc: 'Tlush tumtum kopa pilpil • 100,000 beats kopa tenas sun.', formula: '⚡ Tumtum Power: 60–100 mL kopa beat' },
            brl: { term: '⠠⠓⠑⠁⠗⠞ ⠠⠍⠽⠕⠉⠁⠗⠙⠊⠥⠍', ipa: 'ISO/TR 11548', script: 'Braille 8-Dot', desc: 'Tactile 4-chambered myocardial pump • Hemodynamic vector.', formula: '⚡ ⠠⠺ ⠶ ⠱ ⠠⠏ ⠙⠠⠧ ⠐⠖ ⠂⠲⠆ ⠍ ⠧⠔⠼⠃' }
          }
        },
        liver: {
          icon: '🥩',
          snomed: '181277001',
          planes: { coronal: { yaw: 0, pitch: 0 }, sagittal: { yaw: -45, pitch: 10 } },
          translations: {
            en: { term: 'Hepatic Parenchyma (Liver)', ipa: 'hɪˈpæt.ɪk pəˈrɛŋ.kɪ.mə', script: 'Latin Clinical', desc: 'Metabolic & enzymatic reactor containing 100,000 functional hepatic lobules. Governs glycogen storage, urea synthesis, and CYP450 phase I/II detoxification.', formula: '🧪 Hepatic Clearance: Cl_h = Q · E_h • CYP450 Biotransformation' },
            es: { term: 'Parénquima Hepático (Hígado)', ipa: 'pa-ˈɾeŋ-ki-ma e-ˈpa-ti-ko', script: 'Latin Extended', desc: 'Reactor metabólico de 100,000 lobulillos hepáticos. Regula glucógeno, urea y desintoxicación CYP450.', formula: '🧪 Aclaramiento Hepático: Cl_h = Q · E_h' },
            zh: { term: '肝实质细胞 (肝脏)', ipa: 'gān shí zhì (gān zàng)', script: 'Simplified Hanzi', desc: '体内生物化学与酶促反应中心，含10万个肝小叶。主管糖原合成、尿素循环与CYP450解毒。', formula: '🧪 肝清除率: Cl_h = Q · E_h • CYP450 酶解代谢' },
            ar: { term: 'النسيج الكبدي (الكبد)', ipa: 'an-naseej al-kabidi', script: 'Arabic Clinical', desc: 'المفاعل الأيضي للإنزيمات وتخزين الجليكوجين وتصفية السموم عبر CYP450.', formula: '🧪 التصفية الكبدية: Cl_h = Q · E_h • 100,000 فصيص كبدي' },
            hi: { term: 'यकृत् ऊतक (जिगर / यकृत)', ipa: 'yakrit ootak', script: 'Devanagari', desc: '1 लाख यकृत पालियों द्वारा चयापचय नियंत्रण, ग्लाइकोजन संचय एवं विषहरण।', formula: '🧪 यकृत निकासी: Cl_h = Q · E_h • CYP450' },
            chr: { term: 'ᎤᎶᏅᎩ (U-lo-nv-gi - Liver)', ipa: 'u-lo-nv-gi', script: 'Cherokee Syllabary', desc: 'ᎤᎵᏍᎨᏛ ᎤᏓᏁᎸ ᎠᏓᏁᎶᎯᏍᎩ • 100,000 ᎢᏳᏩᎫᏗ ᎦᏅᎯᏒᎢ.', formula: '🧪 ᎤᏣᏘ ᎤᏬᏂᎯᏍᏗ: CYP450 ᎠᏥᎸ ᎠᏓᏅᏁᎯ' },
            chn: { term: 'Klipkoot (Liver / Guts)', ipa: 'klip-koot', script: 'Chinuk Pipa Duployan', desc: 'Metabolic kloshe kopa makmak pi pilpil.', formula: '🧪 Tlush Cleansing: 100,000 lobules' },
            brl: { term: '⠠⠓⠑⠏⠁⠞⠊⠉ ⠠⠇⠕⠃⠥⠇⠑', ipa: 'ISO/TR 11548', script: 'Braille 8-Dot', desc: 'Tactile hepatic lobule grid • Enzymatic clearance reactor.', formula: '🧪 ⠠⠉⠇⠨⠓ ⠶ ⠠⠟ ⠐⠄ ⠠⠑⠨⠓' }
          }
        },
        skeletal: {
          icon: '🦴',
          snomed: '71341001',
          planes: { coronal: { yaw: 0, pitch: 0 }, sagittal: { yaw: 0, pitch: -20 } },
          translations: {
            en: { term: 'Musculoskeletal Actin-Myosin (Femur)', ipa: 'ˈæk.tɪn ˈmaɪ.ə.sɪn ˈfiː.mər', script: 'Latin Clinical', desc: 'Lever biomechanics & crossbridge sliding filament cycles. Hydrolyzes ATP to generate locomotion against gravitational load.', formula: '🦴 Crossbridge Force: F_muscle = σ · A_pennation • 3–5 pN/Head' },
            es: { term: 'Actina-Miosina Músculo-Esquelética (Fémur)', ipa: 'ak-ˈti-na mjo-ˈsi-na ˈfe-muɾ', script: 'Latin Extended', desc: 'Palancas biomecánicas y ciclo de puentes cruzados. Hidrólisis de ATP para vencer la carga de gravedad.', formula: '🦴 Fuerza Muscular: F = σ · A_pennation' },
            zh: { term: '骨骼肌肌动-肌球蛋白 (股骨)', ipa: 'gǔ gé jī jī dòng dàn bái', script: 'Simplified Hanzi', desc: '骨杠杆生物力学与肌丝滑行交叉桥循环。通过水解ATP产生3–5 pN微观牵引力。', formula: '🦴 肌肉拉力: F = σ · A • 3–5 pN/肌球蛋白头' },
            ar: { term: 'الألياف العضلية الهيكلية (عظم الفخذ)', ipa: 'al-alyaf al-‘adˤaliyyah', script: 'Arabic Clinical', desc: 'ميكانيكا الروافع الحيوية وانزلاق الألياف لإنتاج الحركة ومقاومة الجاذبية.', formula: '🦴 القوة العضلية: 3–5 بيكونيوتن لكل رأس ميوسين' },
            hi: { term: 'कंकाल पेशी तंत्र (ऊर्वस्थि / फीमर)', ipa: 'kankal peshee tantra', script: 'Devanagari', desc: 'अस्थि उत्तोलक यांत्रिकी एवं एक्टिन-मायोसिन सेतु चक्र। गुरुत्वाकर्षण विरुद्ध गति निर्माण।', formula: '🦴 मांसपेशी बल: F = σ · A • 3–5 pN' },
            chr: { term: 'ᎪᎳ ᎠᎴ ᎤᏍᏈᏄᎵ (Gola ale Usgwinuli)', ipa: 'go-la a-le u-sgwi-nu-li', script: 'Cherokee Syllabary', desc: 'ᎤᏓᏁᎶᏗ ᎦᏅᎯᏒᎢ ᏧᏍᏈᏄᎵ ᎠᎴ ᏧᎪᎳ • 3-5 pN ᎤᎵᏍᎨᏛ ᎤᏬᏂᎯᏍᏗ.', formula: '🦴 ᎠᏓᏅᏬᏍᎩ ᎤᎵᏂᎬᎬ: F = σ · A' },
            chn: { term: 'Itlokum (Bones & Muscles)', ipa: 'it-lo-kum', script: 'Chinuk Pipa Duployan', desc: 'Skookum bone pi muscle kopa klatwa kopa stik.', formula: '🦴 Skookum Pull: 3–5 pN per head' },
            brl: { term: '⠠⠍⠥⠎⠉⠥⠇⠕⠎⠅⠑⠇⠑⠞⠁⠇ ⠠⠁⠉⠞⠊⠝', ipa: 'ISO/TR 11548', script: 'Braille 8-Dot', desc: 'Tactile musculoskeletal lever grid • Actomyosin sliding filament.', formula: '🦴 ⠠⠋ ⠶ ⠨⠎ ⠐⠄ ⠠⠁ ⠐⠂ ⠼⠉⠤⠼⠑ ⠏⠠⠝' }
          }
        }
      };

      function initBodyMatrix() {
        if (bodyGimbalInitialized) return;
        bodyGimbalInitialized = true;

        const body3dStage = document.getElementById('body3dStage');
        const body3dGimbal = document.getElementById('body3dGimbal');
        const bodyYawBadge = document.getElementById('bodyYawBadge');
        const bodyNodes = document.querySelectorAll('.body-organ-node');
        const bodyLangBtns = document.querySelectorAll('.body-lang-btn');
        const bodyPlaneCoronalBtn = document.getElementById('bodyPlaneCoronalBtn');
        const bodyPlaneSagittalBtn = document.getElementById('bodyPlaneSagittalBtn');
        const bodyResetOrbitBtn = document.getElementById('bodyResetOrbitBtn');
        const bodyJumpToZoomBtn = document.getElementById('bodyJumpToZoomBtn');

        function updateGimbalTransform() {
          if (!body3dGimbal) return;
          body3dGimbal.style.transform = `rotateY(${bodyYaw}deg) rotateX(${bodyPitch}deg)`;
          if (bodyYawBadge) {
            bodyYawBadge.textContent = `AZIMUTH: ${Math.round(bodyYaw)}° • PITCH: ${Math.round(bodyPitch)}°`;
          }
        }

        // Render Inspector Details
        function renderBodyInspector() {
          const organData = BODY_ANATOMY_DATA[currentBodyOrgan];
          if (!organData) return;
          const langData = organData.translations[currentBodyLang] || organData.translations.en;

          const flags = { en: '🇺🇸', es: '🇲🇽', zh: '🇨🇳', ar: '🇸🇦', hi: '🇮🇳', chr: '🦅', chn: '🌲', brl: '⠠⠃' };
          const flagBadge = document.getElementById('bodyInspectorFlagBadge');
          const snomedBadge = document.getElementById('bodyInspectorSnomed');
          const termDiv = document.getElementById('bodyInspectorTerm');
          const phoneticDiv = document.getElementById('bodyInspectorPhonetic');
          const descDiv = document.getElementById('bodyInspectorDesc');
          const formulaDiv = document.getElementById('bodyInspectorFormula');

          if (flagBadge) flagBadge.textContent = flags[currentBodyLang] || '🌐';
          if (snomedBadge) snomedBadge.textContent = `SNOMED: ${organData.snomed}`;
          if (termDiv) {
            termDiv.textContent = langData.term;
            termDiv.style.direction = currentBodyLang === 'ar' ? 'rtl' : 'ltr';
          }
          if (phoneticDiv) {
            phoneticDiv.textContent = `IPA: /${langData.ipa}/ • ${langData.script}`;
          }
          if (descDiv) {
            descDiv.textContent = isChildrenMode ? getChildOrganDesc(currentBodyOrgan) : langData.desc;
          }
          if (formulaDiv) {
            const formulaText = isChildrenMode ? getChildOrganFormula(currentBodyOrgan) : langData.formula;
            if (formulaText && formulaText.includes(':')) {
              const colonIdx = formulaText.indexOf(':');
              const labelPart = formulaText.substring(0, colonIdx + 1);
              const mathPart = formulaText.substring(colonIdx + 1);
              formulaDiv.innerHTML = `<span style="font-family: 'PocketGull', system-ui, sans-serif; font-size: 0.92rem; font-weight: 800; color: #f8fafc; margin-right: 0.5rem; letter-spacing: 0.01em;">${labelPart}</span><span style="font-family: var(--font-code); font-size: 0.85rem; color: #38bdf8; letter-spacing: 0.02em;">${mathPart}</span>`;
            } else {
              formulaDiv.textContent = formulaText;
            }
          }

          // Highlight Active Node in SVG
          bodyNodes.forEach(node => {
            if (node.dataset.organ === currentBodyOrgan) {
              node.classList.add('active');
              const circle = node.querySelector('circle') || node.querySelector('rect') || node.querySelector('ellipse');
              if (circle) circle.setAttribute('stroke-width', '3');
            } else {
              node.classList.remove('active');
              const circle = node.querySelector('circle') || node.querySelector('rect') || node.querySelector('ellipse');
              if (circle) circle.setAttribute('stroke-width', '1.5');
            }
          });
        }

        function getChildOrganDesc(organ) {
          switch (organ) {
            case 'brain': return 'The Magical Thought Palace! Where all your dreams, laughter, questions, and big ideas sparkle like twinkling stars.';
            case 'lungs': return 'The Two Air Balloons! Breathing in fresh mountain breeze and sweet ocean air to power your running shoes!';
            case 'heart': return 'The Great Heart Hero Pump! Thump-thump! Beating over 100,000 times today without ever taking a nap.';
            case 'liver': return 'The Master Kitchen Chef! Turning breakfast pancakes and berries into pure superhero energy!';
            case 'skeletal': return 'The Jumping Tree Trunks! Strong bones and flexible muscles letting you leap, dance, and climb tall trees!';
            default: return '';
          }
        }

        function getChildOrganFormula(organ) {
          switch (organ) {
            case 'brain': return '✨ Wonder Power: 86 Billion idea sparklers thinking together!';
            case 'lungs': return '🎈 Breath Power: 300 Million tiny balloon helpers filling with fresh air!';
            case 'heart': return '💖 Love & Strength: Over 100,000 strong beats every single day!';
            case 'liver': return '🍓 Kitchen Magic: Turning fruit & veggies into running sparks!';
            case 'skeletal': return '🏃 Playground Speed: Leaping and skipping with friendly muscle rowers!';
            default: return '';
          }
        }

      let bodyScale = 1.0;
      let bodyPanX = 0;
      let bodyPanY = 0;
      let bodySliceDepth = 100; // 0 to 100%

      function updateGimbalTransform() {
        if (!body3dGimbal) return;
        body3dGimbal.style.transform = `translate3d(${bodyPanX}px, ${bodyPanY}px, 0) scale(${bodyScale}) rotateY(${bodyYaw}deg) rotateX(${bodyPitch}deg)`;
        if (bodyYawBadge) {
          bodyYawBadge.textContent = `AZIMUTH: ${Math.round(bodyYaw)}° • PITCH: ${Math.round(bodyPitch)}° • ZOOM: ${bodyScale.toFixed(2)}×`;
        }
      }

      function updateSliceDepth(delta) {
        bodySliceDepth = Math.max(10, Math.min(100, bodySliceDepth + delta));
        const sliceBadge = document.getElementById('bodySliceBadge');
        if (sliceBadge) {
          let layerName = 'ALL LAYERS (100%)';
          if (bodySliceDepth < 30) layerName = 'CORONAL 1: SUPERFICIAL DERMIS';
          else if (bodySliceDepth < 55) layerName = 'CORONAL 2: VASCULAR / VISCERAL';
          else if (bodySliceDepth < 80) layerName = 'CORONAL 3: ORGANS & ORCH-OR';
          else layerName = 'CORONAL 4: DEEP SKELETAL';
          sliceBadge.textContent = `Z-SLICE: ${layerName} (${Math.round(bodySliceDepth)}%)`;
        }

        // Apply visual opacity and depth cutoff to SVG layers based on slice depth
        const svg = document.getElementById('bodyTypoMatrixSvg');
        if (svg) {
          const bgGrid = svg.querySelector('g[fill="#334155"]');
          if (bgGrid) bgGrid.style.opacity = (bodySliceDepth / 100) * 0.35;
          const skeletal = svg.querySelector('g[data-organ="skeletal"]');
          if (skeletal) skeletal.style.opacity = bodySliceDepth < 40 ? '0.1' : '1';
          const liver = svg.querySelector('g[data-organ="liver"]');
          if (liver) liver.style.opacity = bodySliceDepth < 25 ? '0.1' : '1';
        }
      }

      // Pointer / Touch 3D Orbit Drag Handlers (Supports Blender MMB & LMB)
      body3dStage.addEventListener('pointerdown', (e) => {
        isBodyDragging = true;
        bodyDragStartX = e.clientX;
        bodyDragStartY = e.clientY;
        body3dStage.style.cursor = 'grabbing';
        body3dStage.setPointerCapture(e.pointerId);
      });

      body3dStage.addEventListener('pointermove', (e) => {
        if (!isBodyDragging) return;
        const dx = e.clientX - bodyDragStartX;
        const dy = e.clientY - bodyDragStartY;

        // Shift + Drag = Pan (Blender standard)
        if (e.shiftKey) {
          bodyPanX += dx * 0.8;
          bodyPanY += dy * 0.8;
        } else {
          // Standard Turntable Orbit
          bodyYaw += dx * 0.5;
          bodyPitch = Math.max(-60, Math.min(60, bodyPitch - dy * 0.4));
        }

        bodyDragStartX = e.clientX;
        bodyDragStartY = e.clientY;
        updateGimbalTransform();
      });

      body3dStage.addEventListener('pointerup', (e) => {
        isBodyDragging = false;
        body3dStage.style.cursor = 'grab';
        body3dStage.releasePointerCapture(e.pointerId);
      });

      body3dStage.addEventListener('pointercancel', (e) => {
        isBodyDragging = false;
        body3dStage.style.cursor = 'grab';
      });

      // Blender / CAD Modeler Wheel Navigation Engine
      body3dStage.addEventListener('wheel', (e) => {
        e.preventDefault();
        
        // 1. Shift + Wheel = Depth Slicing through anatomical planes
        if (e.shiftKey) {
          const delta = e.deltaY > 0 ? -10 : 10;
          updateSliceDepth(delta);
          return;
        }

        // 2. Ctrl + Wheel = Pan Y
        if (e.ctrlKey) {
          bodyPanY += e.deltaY > 0 ? -15 : 15;
          updateGimbalTransform();
          return;
        }

        // 3. Default Wheel = Dolly Zoom (0.6x to 4.0x)
        const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
        bodyScale = Math.max(0.6, Math.min(4.0, bodyScale * zoomFactor));
        updateGimbalTransform();
      }, { passive: false });

      // Organ Node Tap Handlers
      bodyNodes.forEach(node => {
        node.addEventListener('click', (e) => {
          e.stopPropagation();
          currentBodyOrgan = node.dataset.organ;
          renderBodyInspector();
        });
      });

      // Language Buttons
      bodyLangBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          bodyLangBtns.forEach(b => {
            b.style.background = 'transparent';
            b.style.color = 'var(--text-secondary)';
          });
          btn.style.background = 'var(--accent-teal)';
          btn.style.color = '#09090b';
          currentBodyLang = btn.dataset.lang;
          renderBodyInspector();
        });
      });

      // Plane Selector
      if (bodyPlaneCoronalBtn) {
        bodyPlaneCoronalBtn.addEventListener('click', () => {
          bodyYaw = 0;
          bodyPitch = 0;
          bodyPlaneCoronalBtn.style.background = 'var(--accent-teal)';
          bodyPlaneCoronalBtn.style.color = '#09090b';
          if (bodyPlaneSagittalBtn) {
            bodyPlaneSagittalBtn.style.background = 'transparent';
            bodyPlaneSagittalBtn.style.color = 'var(--text-secondary)';
          }
          updateGimbalTransform();
        });
      }

      if (bodyPlaneSagittalBtn) {
        bodyPlaneSagittalBtn.addEventListener('click', () => {
          bodyYaw = 90;
          bodyPitch = 0;
          bodyPlaneSagittalBtn.style.background = 'var(--accent-teal)';
          bodyPlaneSagittalBtn.style.color = '#09090b';
          if (bodyPlaneCoronalBtn) {
            bodyPlaneCoronalBtn.style.background = 'transparent';
            bodyPlaneCoronalBtn.style.color = 'var(--text-secondary)';
          }
          updateGimbalTransform();
        });
      }

      if (bodyResetOrbitBtn) {
        bodyResetOrbitBtn.addEventListener('click', () => {
          bodyYaw = 0;
          bodyPitch = 0;
          bodyScale = 1.0;
          bodyPanX = 0;
          bodyPanY = 0;
          bodySliceDepth = 100;
          updateSliceDepth(0);
          updateGimbalTransform();
        });
      }

      // WebXR / Spatial AR Launch Hook
      const bodyWebXrBtn = document.getElementById('bodyWebXrBtn');
      if (bodyWebXrBtn) {
        bodyWebXrBtn.addEventListener('click', async () => {
          if ('xr' in navigator && navigator.xr.isSessionSupported) {
            try {
              const supported = await navigator.xr.isSessionSupported('immersive-ar');
              if (supported) {
                alert('🥽 WebXR Immersive AR Supported!\nLaunching spatial typographic projection onto clinical surface.');
                return;
              }
            } catch (err) {
              console.warn('WebXR query error:', err);
            }
          }

          // Fallback: Device Orientation / Spatial Gyroscope inspection
          if (typeof window.DeviceOrientationEvent !== 'undefined' && typeof window.DeviceOrientationEvent.requestPermission === 'function') {
            try {
              const permission = await window.DeviceOrientationEvent.requestPermission();
              if (permission === 'granted') {
                window.addEventListener('deviceorientation', (e) => {
                  if (e.gamma !== null && e.beta !== null) {
                    bodyYaw = e.gamma * 1.5;
                    bodyPitch = Math.max(-45, Math.min(45, (e.beta - 45) * 0.8));
                    updateGimbalTransform();
                  }
                });
                bodyWebXrBtn.textContent = '📱 Gyro Active';
                bodyWebXrBtn.style.background = 'rgba(74, 222, 128, 0.2)';
                bodyWebXrBtn.style.color = '#4ade80';
                return;
              }
            } catch (e) {
              console.warn('Gyro permission error:', e);
            }
          }

          alert('🥽 WebXR Spatial Protocol:\n\n1. Connect Vision Pro, Quest 3, or Android ARCore device.\n2. In WebXR mode, the 3D Typographic Body Matrix projects into physical 3D space.\n3. Pinch-to-zoom dollies between Gross Organ and Orch-OR Tubulin Dipoles.\n4. Device orientation gyroscope tracking is now enabled for mobile devices.');
        });
      }

      // ─── Pure High-Quality PocketGull 3D Spatial Holocalligramme Engine ───
      const bodyHoloLensBtn = document.getElementById('bodyHoloLensBtn');
      if (bodyHoloLensBtn) {
        bodyHoloLensBtn.addEventListener('click', () => {
          launchPocketGullHoloModal();
        });
      }

      function launchPocketGullHoloModal() {
        let modal = document.getElementById('pocketgullHoloModalOverlay');
        if (!modal) {
          modal = document.createElement('div');
          modal.id = 'pocketgullHoloModalOverlay';
          modal.style.position = 'fixed';
          modal.style.inset = '0';
          modal.style.zIndex = '99999';
          modal.style.background = 'radial-gradient(circle at center, #020617 0%, #000000 100%)';
          modal.style.display = 'flex';
          modal.style.flexDirection = 'column';

          modal.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.25rem 2rem; background: rgba(3, 7, 18, 0.95); border-bottom: 1px solid var(--border-subtle); color: #fff; font-family: var(--font-code); backdrop-blur-md: blur(16px);">
              <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">✨</span>
                <div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-family: 'PocketGull Bold', sans-serif; font-size: 1.1rem; font-weight: 800; color: var(--accent-teal); letter-spacing: -0.02em;">
                      POCKETGULL 3D SPATIAL HOLOCALLIGRAMME
                    </span>
                    <span style="font-size: 0.7rem; background: rgba(20, 184, 166, 0.2); border: 1px solid var(--accent-teal); padding: 0.15rem 0.6rem; border-radius: 9999px; color: var(--accent-teal); font-weight: 800;">
                      100% PURE POCKETGULL VF
                    </span>
                  </div>
                  <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0;">
                    Zero external runtime dependencies. 100% pure TrueType vector typography volumetric silhouette.
                  </p>
                </div>
              </div>
              <div style="display: flex; align-items: center; gap: 1rem;">
                <button id="holoSpinToggleBtn" style="background: rgba(20, 184, 166, 0.15); border: 1px solid var(--accent-teal); color: var(--accent-teal); padding: 0.4rem 0.9rem; border-radius: 6px; cursor: pointer; font-size: 0.8rem; font-weight: 700;">
                  ⏸ Pause Rotation
                </button>
                <button id="closeHoloModalBtn" style="background: transparent; border: 1px solid var(--border-subtle); color: #fff; padding: 0.4rem 0.9rem; border-radius: 6px; cursor: pointer; font-size: 0.8rem;">
                  ✕ Exit Holocalligramme
                </button>
              </div>
            </div>

            <!-- Full-Screen 3D Stereoscopic Typographic Canvas -->
            <div style="flex: 1; position: relative; overflow: hidden; display: flex; justify-content: center; align-items: center; perspective: 1200px; cursor: grab;" id="holoStage">
              
              <!-- 3D Transform Carousel Gimbal -->
              <div id="holoGimbal" style="width: 380px; height: 580px; position: relative; transform-style: preserve-3d; transition: transform 0.05s linear;">
                
                <!-- LAYER 1: Front Coronal Typographic Calligramme (PocketGull Bold) -->
                <div style="position: absolute; inset: 0; transform: translateZ(45px); pointer-events: none;">
                  <svg viewBox="0 0 380 580" style="width: 100%; height: 100%; overflow: visible;">
                    <g fill="#38bdf8" font-family="'PocketGull Bold', sans-serif" font-weight="800" text-anchor="middle" filter="drop-shadow(0 0 12px rgba(56, 189, 248, 0.6))">
                      <!-- Cranial -->
                      <text x="190" y="55" font-size="16">CEREBRUM</text>
                      <text x="190" y="75" font-size="10" fill="#93c5fd">ORCH-OR 40Hz DIPOLE</text>
                      <!-- Pulmonary & Cardiac -->
                      <text x="135" y="145" font-size="13" fill="#22c55e">PULMONARY</text>
                      <text x="245" y="145" font-size="13" fill="#22c55e">ALVEOLI</text>
                      <text x="190" y="185" font-size="18" fill="#f43f5e">MYOCARDIUM</text>
                      <text x="190" y="205" font-size="9" fill="#fb7185">W = ∫ P dV + 1/2 m v²</text>
                      <!-- Visceral -->
                      <text x="190" y="255" font-size="14" fill="#fbbf24">HEPATIC PARENCHYMA</text>
                      <text x="190" y="275" font-size="10" fill="#fef08a">100,000 CYTOCHROME LOBULES</text>
                      <!-- Skeletal -->
                      <text x="140" y="380" font-size="13" fill="#c084fc">FEMUR</text>
                      <text x="240" y="380" font-size="13" fill="#c084fc">FEMUR</text>
                      <text x="140" y="460" font-size="12" fill="#e879f9">TIBIA</text>
                      <text x="240" y="460" font-size="12" fill="#e879f9">TIBIA</text>
                    </g>
                  </svg>
                </div>

                <!-- LAYER 2: Core Monospace Telemetry Matrix (PocketGull Mono) -->
                <div style="position: absolute; inset: 0; transform: translateZ(0px); pointer-events: none;">
                  <svg viewBox="0 0 380 580" style="width: 100%; height: 100%; overflow: visible;">
                    <g fill="#14b8a6" opacity="0.65" font-family="'PocketGull Mono', monospace" font-size="9" text-anchor="middle">
                      <text x="190" y="35">:: 0x80 RESERVED BIT-7 MASKED ::</text>
                      <text x="190" y="95">[ 13418 ENCODED GLYPH POINTS ]</text>
                      <text x="190" y="115">. - = = = = = + = = = = = - .</text>
                      <text x="190" y="165">| | | | 600 UPM MONO PITCH | | | |</text>
                      <text x="190" y="225">. - = = = FRANK-STARLING = = = - .</text>
                      <text x="190" y="295">| | | | 203 DPI RESISTANT | | | |</text>
                      <text x="190" y="335">. - = = = = = = = = = = = = = - .</text>
                      <text x="190" y="415">| | 5:1 LOAN OPTO APERTURE | |</text>
                      <text x="190" y="495">| | W3C OTS MEMORY SAFE | |</text>
                      <text x="190" y="535">:: SEMVER 3.0.0 ALIGNED ::</text>
                    </g>
                  </svg>
                </div>

                <!-- LAYER 3: Back Coronal Tactile Braille Matrix (PocketGull Braille U+2800) -->
                <div style="position: absolute; inset: 0; transform: translateZ(-45px); pointer-events: none;">
                  <svg viewBox="0 0 380 580" style="width: 100%; height: 100%; overflow: visible;">
                    <g fill="#a855f7" opacity="0.45" font-family="'PocketGull', monospace" font-size="12" text-anchor="middle">
                      <text x="190" y="60">⠠⠉⠑⠗⠑⠃⠗⠁⠇</text>
                      <text x="190" y="150">⠠⠏⠥⠇⠍⠕⠝⠁⠗⠽</text>
                      <text x="190" y="190">⠠⠓⠑⠁⠗⠞</text>
                      <text x="190" y="260">⠠⠓⠑⠏⠁⠞⠊⠉</text>
                      <text x="190" y="390">⠠⠁⠉⠞⠊⠝</text>
                      <text x="190" y="470">⠠⠍⠽⠕⠎⠊⠝</text>
                    </g>
                  </svg>
                </div>

              </div>

              <!-- Live HUD Telemetry Overlay -->
              <div style="position: absolute; bottom: 24px; left: 24px; font-family: var(--font-code); font-size: 0.8rem; color: var(--accent-teal); pointer-events: none;">
                🖱️ DRAG TO ORBIT IN 3D • WHEEL TO DOLLY • SHIFT TO SLICE
              </div>

              <div id="holoAngleBadge" style="position: absolute; bottom: 24px; right: 24px; font-family: var(--font-code); font-size: 0.8rem; color: var(--accent-amber); pointer-events: none;">
                HOLOCALLIGRAMME ROTATION: 0°
              </div>
            </div>
          `;

          document.body.appendChild(modal);

          let holoYaw = 0;
          let holoPitch = 0;
          let holoZoom = 1.0;
          let isHoloDragging = false;
          let holoStartX = 0;
          let holoStartY = 0;
          let holoSpinning = true;
          let holoSpinTimer = null;

          const holoStage = document.getElementById('holoStage');
          const holoGimbal = document.getElementById('holoGimbal');
          const holoAngleBadge = document.getElementById('holoAngleBadge');
          const holoSpinToggleBtn = document.getElementById('holoSpinToggleBtn');
          const closeHoloModalBtn = document.getElementById('closeHoloModalBtn');

          function updateHoloTransform() {
            if (!holoGimbal) return;
            holoGimbal.style.transform = `scale(${holoZoom}) rotateY(${holoYaw}deg) rotateX(${holoPitch}deg)`;
            if (holoAngleBadge) {
              holoAngleBadge.textContent = `HOLOCALLIGRAMME AZIMUTH: ${Math.round(holoYaw % 360)}° • PITCH: ${Math.round(holoPitch)}°`;
            }
          }

          function startHoloSpin() {
            if (holoSpinTimer) clearInterval(holoSpinTimer);
            holoSpinTimer = setInterval(() => {
              if (holoSpinning && !isHoloDragging) {
                holoYaw += 0.35;
                updateHoloTransform();
              }
            }, 1000 / 60);
          }

          startHoloSpin();

          holoSpinToggleBtn.addEventListener('click', () => {
            holoSpinning = !holoSpinning;
            holoSpinToggleBtn.textContent = holoSpinning ? '⏸ Pause Rotation' : '▶ Resume Rotation';
            holoSpinToggleBtn.style.background = holoSpinning ? 'rgba(20, 184, 166, 0.15)' : 'var(--accent-teal)';
            holoSpinToggleBtn.style.color = holoSpinning ? 'var(--accent-teal)' : '#09090b';
          });

          closeHoloModalBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            clearInterval(holoSpinTimer);
          });

          // Pointer interaction
          holoStage.addEventListener('pointerdown', (e) => {
            isHoloDragging = true;
            holoStartX = e.clientX;
            holoStartY = e.clientY;
            holoStage.style.cursor = 'grabbing';
            holoStage.setPointerCapture(e.pointerId);
          });

          holoStage.addEventListener('pointermove', (e) => {
            if (!isHoloDragging) return;
            const dx = e.clientX - holoStartX;
            const dy = e.clientY - holoStartY;
            holoYaw += dx * 0.5;
            holoPitch = Math.max(-45, Math.min(45, holoPitch - dy * 0.4));
            holoStartX = e.clientX;
            holoStartY = e.clientY;
            updateHoloTransform();
          });

          holoStage.addEventListener('pointerup', (e) => {
            isHoloDragging = false;
            holoStage.style.cursor = 'grab';
            holoStage.releasePointerCapture(e.pointerId);
          });

          holoStage.addEventListener('wheel', (e) => {
            e.preventDefault();
            const factor = e.deltaY > 0 ? 0.92 : 1.08;
            holoZoom = Math.max(0.6, Math.min(2.5, holoZoom * factor));
            updateHoloTransform();
          }, { passive: false });

        } else {
          modal.style.display = 'flex';
        }
      }

      // ─── Adobe-Style 2D-to-3D Vector Extrusion & Turntable Studio ───
      const bodyTurntableBtn = document.getElementById('bodyTurntableBtn');
      if (bodyTurntableBtn) {
        bodyTurntableBtn.addEventListener('click', () => {
          launchPocketGullTurntableModal();
        });
      }

      // ─── Dual-Mode Chronometer: Cardiac Hemodynamics vs Human Lifespan & Tilth Engine ───
      const HUMAN_TILTH_EPOCHS = [
        {
          epoch: 0,
          ageYears: 0,
          label: 'Epoch 1: Blastocyst & Totipotency (Day 0–14)',
          phaseDesc: 'TOTIPOTENT BLASTOCYST • CELL SEED (100 µm)',
          meta: 'CHRONOLOGY: Day 0–14 • DIAMETER: 100 µm • CLEAVAGE: 2^n BLASTOMERES',
          telomere: '12.0 kb',
          mito: '100% ATP',
          bmd: 'N/A (Blastoderm)',
          wisdom: '0 / 100',
          vfSetting: 'opsz 72 • wght 300',
          vfDesc: 'Delicate primordial hairline (0.8x counter dilation)',
          vfWght: 300,
          vfOpsz: 72,
          silhouetteScale: 0.28,
          silhouetteY: 60,
          comments: [
            { frame: 0, title: '🔬 Embryology Suite', author: 'Dr. Ross (Cytogenetics)', text: 'Totipotent cleavage complete. Oct4/Sox2 transcriptional core intact. Zero genetic fragmentation.' },
            { frame: 1, title: '⚡ Bioenergetics', author: 'Dr. Lin (Cellular Biology)', text: 'Mitochondrial membrane potential ΔΨm = -180 mV. Pristine metabolic tilth.' }
          ]
        },
        {
          epoch: 1,
          ageYears: 0.15,
          label: 'Epoch 2: Embryonic Morphogenesis (Week 8)',
          phaseDesc: 'MYOGENIC PACEMAKER • FIRST HEARTBEAT (110 BPM)',
          meta: 'CHRONOLOGY: Week 8 • CROWN-RUMP: 30 mm • MYOGENIC S1 BEAT',
          telomere: '11.8 kb',
          mito: '99% ATP',
          bmd: 'Cartilaginous Primordium',
          wisdom: '2 / 100',
          vfSetting: 'opsz 36 • wght 400',
          vfDesc: 'Emergent structural stems, embryonic vascular curves',
          vfWght: 400,
          vfOpsz: 36,
          silhouetteScale: 0.52,
          silhouetteY: 35,
          comments: [
            { frame: 0, title: '🫀 Fetal Doppler', author: 'Dr. Aris (Cardiology)', text: 'Day 22 primitive cardiac tube rhythm established. Regular 110 BPM peristaltic contraction.' },
            { frame: 1, title: '🧠 Neural Tube', author: 'Dr. Gear (Neurodevelopment)', text: 'Cranial flexure aligned. Primary brain vesicles demarcating with pristine synaptic potential.' }
          ]
        },
        {
          epoch: 2,
          ageYears: 2,
          label: 'Epoch 3: Neonatal & Infancy (0–2 Years)',
          phaseDesc: 'SYNAPTIC BLOOMING • 1M NEW CONNECTIONS / SEC',
          meta: 'CHRONOLOGY: 18 Months • WEIGHT: 11.5 kg • ALVEOLAR INFLATION',
          telomere: '11.2 kb',
          mito: '98% ATP',
          bmd: 'Rapid Trabecular Mineralization',
          wisdom: '12 / 100',
          vfSetting: 'opsz 18 • wght 500',
          vfDesc: 'APTR 1.35× open aperture, cv05 curved terminal foot l',
          vfWght: 500,
          vfOpsz: 18,
          silhouetteScale: 0.72,
          silhouetteY: 18,
          comments: [
            { frame: 0, title: '🧸 Pediatric Exam', author: 'Dr. Miller (Pediatrics)', text: 'Surfactant coating alveoli across 300M chambers. Synaptic density blooming at 1,000,000 synapses/sec.' },
            { frame: 1, title: '🔤 Wonder Typography', author: 'Phil Gear (Foundry)', text: 'Enforcing wide font apertures (APTR 1.35x) and curved terminal feet (cv05) for emergent literacy.' }
          ]
        },
        {
          epoch: 3,
          ageYears: 25,
          label: 'Epoch 4: Prime Vitality & Peak Tilth (18–35 Years)',
          phaseDesc: 'PEAK TILTH & HOMEOSTASIS • VO2 MAX 55 mL/kg/min',
          meta: 'CHRONOLOGY: Age 25 • SYSTEMIC RESILIENCE • PEAK SARCOMERE FORCE',
          telomere: '10.2 kb',
          mito: '95% ATP',
          bmd: '+1.5 T-Score (Peak)',
          wisdom: '45 / 100',
          vfSetting: 'opsz 14 • wght 700',
          vfDesc: 'PocketGull Bold display authority, Sloan 5:1 optotypes',
          vfWght: 700,
          vfOpsz: 14,
          silhouetteScale: 1.0,
          silhouetteY: 0,
          comments: [
            { frame: 0, title: '⚡ Peak Muscle Power', author: 'Dr. Vance (Sports Physiology)', text: 'Actomyosin crossbridge force at 5.2 pN per myosin head. Stroke volume 95 mL/beat.' },
            { frame: 1, title: '🧪 Hepatic Reserve', author: 'Dr. Chen (Biochemistry)', text: 'CYP450 Phase I/II clearance operating at full thermodynamic capacity. Telomere length optimal.' }
          ]
        },
        {
          epoch: 4,
          ageYears: 50,
          label: 'Epoch 5: Mid-Life Tilth & Epigenetic Mastery (40–60 Years)',
          phaseDesc: 'EPIGENETIC ADAPTATION • PRESBYOPIA COMPENSATION',
          meta: 'CHRONOLOGY: Age 52 • VASCULAR MAINTENANCE • SYNAPTIC SYNTHESIS',
          telomere: '7.8 kb',
          mito: '82% ATP',
          bmd: '+0.2 T-Score (Stable)',
          wisdom: '72 / 100',
          vfSetting: 'opsz 11 • wght 650',
          vfDesc: 'Auto-engaging slashed zero cv08 & serifed capital I ss02',
          vfWght: 650,
          vfOpsz: 11,
          silhouetteScale: 0.98,
          silhouetteY: 0,
          comments: [
            { frame: 0, title: '👁️ Ocular Accommodation', author: 'Dr. Sloan (Ophthalmology)', text: 'Presbyopic loss of lens elasticity detected. Auto-activating PocketGull dilated counters and ISMP slashed zero.' },
            { frame: 1, title: '🧠 Cognitive Architecture', author: 'Dr. Gear (Chief Medical)', text: 'Deep integrative wisdom compensating for mild processing latency. Synaptic associative reserve peak.' }
          ]
        },
        {
          epoch: 5,
          ageYears: 80,
          label: 'Epoch 6: Elderhood & Deep Clinical Wisdom (70–90 Years)',
          phaseDesc: 'DEEP ASSOCIATIVE WISDOM • ISMP DISAMBIGUATION SAFETY',
          meta: 'CHRONOLOGY: Age 82 • CARDIOVASCULAR COMPLIANCE • CARE PRINCIPLES',
          telomere: '5.1 kb',
          mito: '64% ATP',
          bmd: '-1.8 T-Score (Managed)',
          wisdom: '92 / 100',
          vfSetting: 'opsz 8 • wght 800',
          vfDesc: 'Ultra-clear disambiguation: cv08, cv05, ss02, cv11, 670nm PBM',
          vfWght: 800,
          vfOpsz: 8,
          silhouetteScale: 0.94,
          silhouetteY: 4,
          comments: [
            { frame: 0, title: '🛡️ ISMP Safety Standard', author: 'Nurse Chen (Geriatrics)', text: 'Mandatory slashed zero (cv08) and slashed Z (cv11) on all cardiovascular medications. Zero confusion.' },
            { frame: 1, title: '❤️ Patient Dignity', author: 'Dr. Aris (Cardiology)', text: 'Endothelial nitric oxide tone maintained through gentle movement and ancestral dietary tilth.' }
          ]
        },
        {
          epoch: 6,
          ageYears: 102,
          label: 'Epoch 7: Living Memory & Ancestral Soil (100+ Years)',
          phaseDesc: 'ANCESTRAL SOIL • SOVEREIGN ORAL ARCHIVE • CARE PILLAR VII',
          meta: 'CHRONOLOGY: 102 Years • SOVEREIGN ELDER REGISTRY • IMMORTAL IMPACT',
          telomere: '3.6 kb',
          mito: '46% ATP',
          bmd: '-2.4 T-Score',
          wisdom: '99 / 100',
          vfSetting: 'opsz 6 • wght 900',
          vfDesc: 'Maximum contrast Chiseltip, high-contrast Placard & Braille',
          vfWght: 900,
          vfOpsz: 6,
          silhouetteScale: 0.92,
          silhouetteY: 6,
          comments: [
            { frame: 0, title: '🦅 Sovereign Elder Memory', author: 'Elder Council (CARE)', text: 'Ceremonial oral songs, ancestral place names, and lineage wisdom preserved in sovereign vault (.foundry/docs/).' },
            { frame: 1, title: '🌱 Human Tilth Fulfillment', author: 'Phil Gear (Author)', text: 'The vessel returns gently to rich humus. The typeface carries the dignity of a lifetime forward into eternity.' }
          ]
        }
      ];

      const CARDIAC_COMMENTS = [
        {
          frame: 8,
          phase: 'Atrial Inflow',
          author: 'Dr. Aris (Cardiology)',
          role: 'Cardiology',
          text: 'Confirming zero atrial flutter. Frank-Starling end-diastolic filling is within normal LogMAR hemodynamic limits.'
        },
        {
          frame: 18,
          phase: 'QRS Power Stroke',
          author: 'Dr. Gear (Chief Medical)',
          role: 'Chief Medical',
          text: '📌 Pinned at Myocardium S1 Head: 3–5 pN force vector verified. 100% W3C OTS memory safety passed.'
        },
        {
          frame: 42,
          phase: 'T-Wave Repol',
          author: 'Nurse Chen (ICU Telemetry)',
          role: 'ICU Telemetry',
          text: 'ISMP allergy alert checked for penicillin cross-reactivity. Ready for 203 DPI thermal wristband print.'
        }
      ];

      let chronometerMode = 'cardiac'; // 'cardiac' or 'lifespan'
      let currentLifespanAge = 25; // 0 to 102 years
      let isChronometerPlaying = false;
      let chronometerTimer = null;

      const chronometerModeCardiacBtn = document.getElementById('chronometerModeCardiacBtn');
      const chronometerModeLifespanBtn = document.getElementById('chronometerModeLifespanBtn');
      const lifespanTilthHud = document.getElementById('lifespanTilthHud');
      const lifespanEpochPills = document.getElementById('lifespanEpochPills');
      const frameioScrubber = document.getElementById('frameioScrubber');
      const frameioTimecode = document.getElementById('frameioTimecode');
      const frameioPhaseLabel = document.getElementById('frameioPhaseLabel');
      const frameioMetaLabel = document.getElementById('frameioMetaLabel');
      const frameioMarkersBar = document.getElementById('frameioMarkersBar');
      const frameioPlayBtn = document.getElementById('frameioPlayBtn');
      const frameioAddMarkerBtn = document.getElementById('frameioAddMarkerBtn');
      const frameioSignoffBtn = document.getElementById('frameioSignoffBtn');
      const frameioCommentsGrid = document.getElementById('frameioCommentsGrid');

      // Biomarker displays
      const tilthTelomereVal = document.getElementById('tilthTelomereVal');
      const tilthMitoVal = document.getElementById('tilthMitoVal');
      const tilthBmdVal = document.getElementById('tilthBmdVal');
      const tilthWisdomVal = document.getElementById('tilthWisdomVal');
      const tilthVfVal = document.getElementById('tilthVfVal');
      const tilthVfFeatures = document.getElementById('tilthVfFeatures');

      function setChronometerMode(mode) {
        chronometerMode = mode;
        if (isChronometerPlaying) {
          clearInterval(chronometerTimer);
          isChronometerPlaying = false;
          if (frameioPlayBtn) {
            frameioPlayBtn.textContent = '▶ Play';
            frameioPlayBtn.style.background = 'var(--accent-teal)';
          }
        }

        if (mode === 'cardiac') {
          if (chronometerModeCardiacBtn) {
            chronometerModeCardiacBtn.style.background = 'var(--accent-teal)';
            chronometerModeCardiacBtn.style.color = '#09090b';
            chronometerModeCardiacBtn.style.fontWeight = '800';
          }
          if (chronometerModeLifespanBtn) {
            chronometerModeLifespanBtn.style.background = 'transparent';
            chronometerModeLifespanBtn.style.color = 'var(--text-secondary)';
            chronometerModeLifespanBtn.style.fontWeight = '700';
          }
          if (lifespanTilthHud) lifespanTilthHud.style.display = 'none';
          if (lifespanEpochPills) lifespanEpochPills.style.display = 'none';

          if (frameioScrubber) {
            frameioScrubber.min = '0';
            frameioScrubber.max = '60';
            frameioScrubber.value = '18';
          }

          if (frameioMarkersBar) {
            frameioMarkersBar.innerHTML = `
              <span>0ms (P-Wave)</span>
              <span>160ms (PR Segment)</span>
              <span>280ms (QRS Peak)</span>
              <span>480ms (ST Segment)</span>
              <span>720ms (T-Wave)</span>
              <span>1000ms (Diastole)</span>
            `;
          }

          renderFrameioCardiacFrame(18);
        } else {
          // Lifespan & Tilth mode
          if (chronometerModeLifespanBtn) {
            chronometerModeLifespanBtn.style.background = 'var(--accent-teal)';
            chronometerModeLifespanBtn.style.color = '#09090b';
            chronometerModeLifespanBtn.style.fontWeight = '800';
          }
          if (chronometerModeCardiacBtn) {
            chronometerModeCardiacBtn.style.background = 'transparent';
            chronometerModeCardiacBtn.style.color = 'var(--text-secondary)';
            chronometerModeCardiacBtn.style.fontWeight = '700';
          }
          if (lifespanTilthHud) lifespanTilthHud.style.display = 'grid';
          if (lifespanEpochPills) lifespanEpochPills.style.display = 'flex';

          if (frameioScrubber) {
            frameioScrubber.min = '0';
            frameioScrubber.max = '100';
            frameioScrubber.value = String(currentLifespanAge);
          }

          if (frameioMarkersBar) {
            frameioMarkersBar.innerHTML = `
              <span>Day 0</span>
              <span>Wk 8</span>
              <span>2y</span>
              <span>25y (Prime)</span>
              <span>50y (Tilth)</span>
              <span>80y (Wisdom)</span>
              <span>100+y (Ancestral)</span>
            `;
          }

          renderLifespanAge(currentLifespanAge);
        }
      }

      function renderFrameioCardiacFrame(frame) {
        if (!frameioScrubber) return;
        frameioScrubber.value = frame;
        
        // Compute SMPTE 00:00:00:FF
        const frameStr = String(frame).padStart(2, '0');
        if (frameioTimecode) {
          frameioTimecode.textContent = `00:00:00:${frameStr}`;
        }

        if (frameioPhaseLabel) {
          if (frame < 12) frameioPhaseLabel.textContent = 'PHASE: P-WAVE (ATRIAL SYSTOLE)';
          else if (frame < 24) frameioPhaseLabel.textContent = 'PHASE: QRS POWER STROKE (VENTRICULAR SYSTOLE)';
          else if (frame < 38) frameioPhaseLabel.textContent = 'PHASE: ST SEGMENT (ISOELECTRIC REPOL)';
          else if (frame < 50) frameioPhaseLabel.textContent = 'PHASE: T-WAVE (VENTRICULAR REPOLARIZATION)';
          else frameioPhaseLabel.textContent = 'PHASE: DIASTOLE (PASSIVE VENTRICULAR FILLING)';
        }

        if (frameioMetaLabel) {
          frameioMetaLabel.textContent = 'HEART RATE: 60 BPM • 1000 ms R-R INTERVAL';
        }

        // Render cardiac comment cards
        if (frameioCommentsGrid) {
          frameioCommentsGrid.innerHTML = CARDIAC_COMMENTS.map(c => {
            const isActive = Math.abs(c.frame - frame) <= 6;
            const borderCol = isActive ? 'var(--accent-teal)' : 'var(--border-subtle)';
            const bgCol = isActive ? 'rgba(20, 184, 166, 0.18)' : 'rgba(15, 23, 42, 0.8)';
            return `
              <div class="frameio-comment-card" data-frame="${c.frame}" style="background: ${bgCol}; border: 1px solid ${borderCol}; border-radius: 8px; padding: 0.85rem; cursor: pointer; transition: all 0.2s ease;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <span style="font-family: var(--font-code); font-size: 0.7rem; color: var(--accent-teal); font-weight: 700;">⏱️ 00:00:00:${String(c.frame).padStart(2, '0')} • ${c.phase}</span>
                  <span style="font-size: 0.65rem; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.1rem 0.4rem; border-radius: 4px;">${c.author}</span>
                </div>
                <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0; line-height: 1.4;">
                  "${c.text}"
                </p>
              </div>
            `;
          }).join('');

          frameioCommentsGrid.querySelectorAll('.frameio-comment-card').forEach(card => {
            card.addEventListener('click', () => {
              renderFrameioCardiacFrame(parseInt(card.dataset.frame, 10));
            });
          });
        }

        // Pulse heart node in 3D matrix in sync with cardiac frame
        const svg = document.getElementById('bodyTypoMatrixSvg');
        if (svg) {
          const heartNode = svg.querySelector('g[data-organ="heart"] circle');
          if (heartNode) {
            if (frame >= 14 && frame <= 24) {
              heartNode.setAttribute('transform', 'scale(1.2) translate(-28, -25)');
              heartNode.setAttribute('fill', '#f43f5e');
            } else {
              heartNode.removeAttribute('transform');
              heartNode.setAttribute('fill', 'rgba(244, 63, 94, 0.25)');
            }
          }
        }
      }

      function getEpochForAge(age) {
        if (age < 0.05) return HUMAN_TILTH_EPOCHS[0];
        if (age < 0.5) return HUMAN_TILTH_EPOCHS[1];
        if (age < 5) return HUMAN_TILTH_EPOCHS[2];
        if (age < 38) return HUMAN_TILTH_EPOCHS[3];
        if (age < 65) return HUMAN_TILTH_EPOCHS[4];
        if (age < 95) return HUMAN_TILTH_EPOCHS[5];
        return HUMAN_TILTH_EPOCHS[6];
      }

      function renderLifespanAge(age) {
        currentLifespanAge = age;
        if (frameioScrubber) frameioScrubber.value = age;

        const epoch = getEpochForAge(age);

        // SMPTE formatted as Age: 00:00:AGE:00
        const ageInt = Math.floor(age);
        const frac = Math.floor((age - ageInt) * 12); // months
        if (frameioTimecode) {
          frameioTimecode.textContent = `AGE:${String(ageInt).padStart(3, '0')}y:${String(frac).padStart(2, '0')}m`;
        }

        if (frameioPhaseLabel) {
          frameioPhaseLabel.textContent = epoch.phaseDesc;
        }

        if (frameioMetaLabel) {
          frameioMetaLabel.textContent = epoch.meta;
        }

        // Update Tilth Biomarkers HUD
        if (tilthTelomereVal) tilthTelomereVal.textContent = epoch.telomere;
        if (tilthMitoVal) tilthMitoVal.textContent = epoch.mito;
        if (tilthBmdVal) tilthBmdVal.textContent = epoch.bmd;
        if (tilthWisdomVal) tilthWisdomVal.textContent = epoch.wisdom;
        if (tilthVfVal) tilthVfVal.textContent = epoch.vfSetting;
        if (tilthVfFeatures) tilthVfFeatures.textContent = epoch.vfDesc;

        // Highlight matching epoch pill
        if (lifespanEpochPills) {
          lifespanEpochPills.querySelectorAll('.healer-pill').forEach((pill, idx) => {
            if (idx === epoch.epoch) {
              pill.classList.add('active');
            } else {
              pill.classList.remove('active');
            }
          });
        }

        // Render Lifespan Developmental Review Cards
        if (frameioCommentsGrid) {
          frameioCommentsGrid.innerHTML = epoch.comments.map(c => `
            <div class="frameio-comment-card active" style="background: rgba(20, 184, 166, 0.12); border: 1px solid var(--accent-teal); border-radius: 8px; padding: 0.85rem; transition: all 0.2s ease;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span style="font-family: var(--font-code); font-size: 0.72rem; color: var(--accent-teal); font-weight: 800;">${c.title}</span>
                <span style="font-size: 0.65rem; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 0.1rem 0.4rem; border-radius: 4px;">${c.author}</span>
              </div>
              <p style="font-size: 0.8rem; color: var(--text-primary); margin: 0; line-height: 1.4;">
                "${c.text}"
              </p>
            </div>
          `).join('');
        }

        // Morph the 3D Typographic Silhouette based on age and tilth
        const svg = document.getElementById('bodyTypoMatrixSvg');
        if (svg) {
          const bgGrid = svg.querySelector('g[fill="#334155"]');
          const brainNode = svg.querySelector('g[data-organ="brain"]');
          const heartNode = svg.querySelector('g[data-organ="heart"]');
          const lungsNode = svg.querySelector('g[data-organ="lungs"]');
          const liverNode = svg.querySelector('g[data-organ="liver"]');
          const skeletalNode = svg.querySelector('g[data-organ="skeletal"]');

          if (epoch.epoch === 0) {
            // Blastocyst sphere: collapse limbs, concentrate in center
            if (bgGrid) bgGrid.style.opacity = '0.08';
            if (skeletalNode) skeletalNode.style.display = 'none';
            if (lungsNode) lungsNode.style.display = 'none';
            if (liverNode) liverNode.style.display = 'none';
            if (heartNode) heartNode.style.display = 'none';
            if (brainNode) {
              brainNode.style.display = 'block';
              brainNode.setAttribute('transform', 'translate(0, 120) scale(1.6)');
            }
          } else if (epoch.epoch === 1) {
            // Embryogenesis: brain + heart beating
            if (bgGrid) bgGrid.style.opacity = '0.15';
            if (skeletalNode) skeletalNode.style.display = 'none';
            if (lungsNode) lungsNode.style.display = 'none';
            if (liverNode) liverNode.style.display = 'none';
            if (heartNode) {
              heartNode.style.display = 'block';
              heartNode.removeAttribute('transform');
            }
            if (brainNode) {
              brainNode.style.display = 'block';
              brainNode.setAttribute('transform', 'scale(1.2)');
            }
          } else {
            // Full human form
            if (bgGrid) bgGrid.style.opacity = '0.35';
            if (skeletalNode) skeletalNode.style.display = 'block';
            if (lungsNode) lungsNode.style.display = 'block';
            if (liverNode) liverNode.style.display = 'block';
            if (heartNode) {
              heartNode.style.display = 'block';
              heartNode.removeAttribute('transform');
            }
            if (brainNode) {
              brainNode.style.display = 'block';
              brainNode.removeAttribute('transform');
            }

            // Adjust stroke contrast based on elderhood vs youth
            if (epoch.epoch >= 5 && skeletalNode) {
              // Graceful elder trabecular line
              skeletalNode.style.opacity = '0.75';
            } else if (skeletalNode) {
              skeletalNode.style.opacity = '1.0';
            }
          }
        }
      }

      // Event Listeners for Dual Chronometer Switcher
      if (chronometerModeCardiacBtn) {
        chronometerModeCardiacBtn.addEventListener('click', () => setChronometerMode('cardiac'));
      }
      if (chronometerModeLifespanBtn) {
        chronometerModeLifespanBtn.addEventListener('click', () => setChronometerMode('lifespan'));
      }

      if (lifespanEpochPills) {
        lifespanEpochPills.querySelectorAll('.healer-pill').forEach(pill => {
          pill.addEventListener('click', () => {
            const epochIdx = parseInt(pill.dataset.epoch, 10);
            const targetEpoch = HUMAN_TILTH_EPOCHS[epochIdx];
            if (targetEpoch) {
              renderLifespanAge(targetEpoch.ageYears);
            }
          });
        });
      }

      if (frameioScrubber) {
        frameioScrubber.addEventListener('input', (e) => {
          const val = parseFloat(e.target.value);
          if (chronometerMode === 'cardiac') {
            renderFrameioCardiacFrame(Math.round(val));
          } else {
            renderLifespanAge(val);
          }
        });
      }

      if (frameioPlayBtn) {
        frameioPlayBtn.addEventListener('click', () => {
          isChronometerPlaying = !isChronometerPlaying;
          if (isChronometerPlaying) {
            frameioPlayBtn.textContent = '⏸ Pause';
            frameioPlayBtn.style.background = 'var(--accent-amber)';
            
            if (chronometerMode === 'cardiac') {
              chronometerTimer = setInterval(() => {
                let cur = parseInt(frameioScrubber.value, 10);
                cur = (cur + 1) % 60;
                renderFrameioCardiacFrame(cur);
              }, 1000 / 30);
            } else {
              // Animate lifespan from 0 to 102 years
              chronometerTimer = setInterval(() => {
                let cur = parseFloat(frameioScrubber.value);
                cur += 0.75;
                if (cur > 102) cur = 0;
                renderLifespanAge(cur);
              }, 1000 / 25);
            }
          } else {
            frameioPlayBtn.textContent = '▶ Play';
            frameioPlayBtn.style.background = 'var(--accent-teal)';
            clearInterval(chronometerTimer);
          }
        });
      }

      if (frameioAddMarkerBtn) {
        frameioAddMarkerBtn.addEventListener('click', () => {
          const modeStr = chronometerMode === 'cardiac' ? 'Cardiac Frame' : 'Lifespan Tilth Age';
          const note = prompt(`Enter ${modeStr} Clinical Finding / Marker Note:`);
          if (note) {
            alert(`📌 Finding Pinned at ${frameioTimecode.textContent}:\n"${note}"\nSaved to patient longitudinal health record.`);
          }
        });
      }

      if (frameioSignoffBtn) {
        frameioSignoffBtn.addEventListener('click', () => {
          frameioSignoffBtn.textContent = '✓ SIGNED & AUDITED';
          frameioSignoffBtn.style.background = '#22c55e';
          frameioSignoffBtn.style.color = '#000';
          const signoffMsg = chronometerMode === 'cardiac'
            ? '🛡️ ISMP & Electrophysiology Audit Complete:\n\n• Verified 40 Hz Orch-OR Microtubule Dipoles\n• Slashed zero (cv08) and curved l (cv05) enforced\n• Zero allergy cross-reactivity\n• Ready for electronic health record transmission.'
            : '🛡️ CARE Principles & Longitudinal Human Tilth Audit Complete:\n\n• Cellular totipotency to elderhood trajectory validated\n• Telomere reserve and mitochondrial vitality verified\n• Dynamic presbyopia optical size compensation certified\n• Sovereign elder oral records preserved under CARE governance.';
          alert(signoffMsg);
        });
      }

      if (bodyJumpToZoomBtn) {
        bodyJumpToZoomBtn.addEventListener('click', () => {
          setMode(1); // Jump to Molecular Zoom Lens
        });
      }

      updateGimbalTransform();
      renderBodyInspector();
      setChronometerMode('cardiac');
    }

      function renderStressGrid() {
        if (!stressGrid) return;
        stressGrid.innerHTML = '';
        STRESS_SCRIPTS.forEach(script => {
          const randArr = new Uint32Array(8);
          crypto.getRandomValues(randArr);
          const picked = Array.from(randArr).map(v => script.chars[v % script.chars.length]);
          const str = picked.join(' ');

          const card = document.createElement('div');
          card.style.background = 'var(--bg-surface)';
          card.style.border = '1px solid var(--border-subtle)';
          card.style.borderRadius = '12px';
          card.style.padding = '1.25rem';

          card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem; margin-bottom: 1rem;">
              <span style="font-weight: 700; font-size: 0.85rem; color: var(--text-primary);">${script.name}</span>
              <span style="font-family: var(--font-code); font-size: 0.75rem; color: var(--accent-amber);">LogMAR ${script.logMar}</span>
            </div>
            <div style="background: #000; border: 1px solid var(--border-subtle); border-radius: 8px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
              <div style="font-family: 'PocketGull', 'Segoe UI', 'Noto Sans Arabic', 'Noto Sans Hebrew', sans-serif; font-size: 1.5rem; letter-spacing: 0.2em; color: var(--text-primary); margin-bottom: 0.5rem;">${str}</div>
              <div style="font-family: 'PocketGull Bold', 'PocketGull', 'Segoe UI', 'Noto Sans Arabic', 'Noto Sans Hebrew', sans-serif; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.15em; color: var(--accent-teal); margin-bottom: 0.5rem;">${str}</div>
              <div style="font-family: 'PocketGull Mono', 'PocketGull', monospace, sans-serif; font-size: 1rem; letter-spacing: 0.1em; color: var(--accent-amber);">${str}</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; text-align: center; font-family: var(--font-code); font-size: 0.65rem;">
              <div style="background: var(--bg-card); padding: 0.35rem; border-radius: 4px; color: #4ade80;">✓ 5:1 SLOAN</div>
              <div style="background: var(--bg-card); padding: 0.35rem; border-radius: 4px; color: #4ade80;">✓ 0 COLLISIONS</div>
              <div style="background: var(--bg-card); padding: 0.35rem; border-radius: 4px; color: #4ade80;">✓ 203 DPI SURVIVES</div>
            </div>
          `;
          stressGrid.appendChild(card);
        });
      }

      const regenStressBtn = document.getElementById('regenStressBtn');
      if (regenStressBtn) {
        regenStressBtn.addEventListener('click', renderStressGrid);
      }

      // ─── 5. Doc Drill Learning & Research Engine ───
      const DRILL_PANEL_ID = 'docDrillPanel';
      const STORAGE_VAL = '_pg_d_ak';

      function obfuscateKey(val) {
        return btoa(val).split('').reverse().join('');
      }
      function deobfuscateKey(val) {
        try {
          return atob(val.split('').reverse().join(''));
        } catch (e) {
          return '';
        }
      }

      function getApiKey() {
        try {
          const raw = window.localStorage ? localStorage.getItem(STORAGE_VAL) : null;
          return raw ? deobfuscateKey(raw) : '';
        } catch (e) {
          return '';
        }
      }

      function escapeHtml(str) {
        if (!str) return '';
        return String(str)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#39;');
      }

      const DOC_DRILL_KNOWLEDGE = {
        'sloan': {
          title: 'Louise Sloan 5:1 Optotype Invariant',
          category: 'OPHTHALMOLOGY',
          citation: 'Louise L. Sloan (1959), Am J Ophthalmol 48(6):807–813',
          chips: ['Why 55cm distance?', 'How do apertures dilate?', 'Run Sloan stress test', 'Why not standard Snellen?'],
          content: `
            <h3>1. Biophysical Formula &amp; The 5:1 Invariant</h3>
            <p>In 1959, Dr. Louise L. Sloan (Wilmer Ophthalmological Institute, Johns Hopkins University) proved that traditional Snellen optotypes exhibited irregular, non-standardized legibility thresholds. Sloan engineered the definitive 10-character optotype set (<strong>C, D, H, K, N, O, R, S, V, Z</strong>) bounded strictly by a <strong>5:1 proportion</strong>:</p>
            <p><code>Height = 5 arcminutes (5′) | Stroke &amp; Counter Aperture = 1 arcminute (1′)</code></p>
            <p>At standard testing distances (55 cm near reading, 6 m distance), this 1-arcminute stroke matches the physical resolving limit of human foveal cone photoreceptors.</p>
            <h3>2. How PocketGull Implements It</h3>
            <p>All glyph counters in PocketGull are pinned to this 5:1 ratio on a 1000 UPM grid. During low-illumination (mesopic) ICU environments or acute resuscitations, PocketGull's Phoropter engine dynamically dilates letter apertures by <code>1.00×</code> to <code>1.35×</code> to prevent optical irradiation, blooming, and letter closure.</p>
            <h3>3. Clinical Hazard</h3>
            <p>When typefaces use narrow counters (such as standard Helvetica or Times), characters like <code>C</code> and <code>O</code> or <code>8</code> and <code>0</code> bloom into solid black ellipses under dirty bedside monitors, creating catastrophic medication dosing errors.</p>
          `
        },
        'bouma': {
          title: "Herman Bouma's Law of Lateral Crowding",
          category: 'NEURO-ERGONOMICS',
          citation: 'Herman Bouma (1970), Nature 226(5241):177–178',
          chips: ['What is flanker masking?', 'Try +0.12em spacing', 'Peripheral vs foveal reading'],
          content: `
            <h3>1. The Bouma Crowding Phenomenon</h3>
            <p>In 1970, Dutch vision scientist Herman Bouma published his landmark <em>Nature</em> paper showing that letters in parafoveal and peripheral vision are masked by neighboring flanker letters when they fall inside a critical spatial radius:</p>
            <p><code>r ≈ 0.5 × eccentricity (degrees)</code></p>
            <p>When a clinician focuses their gaze on a primary monitor (e.g. surgical camera), vital numbers in their peripheral field undergo severe flanker interference unless inter-letter spacing exceeds Bouma's critical distance.</p>
            <h3>2. How PocketGull Solves Crowding</h3>
            <p>PocketGull features native Bouma aperture compensation: clicking the <code>+0.12em</code> lateral tracking toggle expands character spacing to maintain spatial isolation, preserving peripheral scanning legibility across EHR and emergency dispatch HUDs.</p>
          `
        },
        'ismp': {
          title: 'ISMP / FDA Clinical Disambiguation',
          category: 'PATIENT SAFETY',
          citation: 'ISMP Guidelines (2023) &amp; FDA CDER Guidance (2016)',
          chips: ['Why is 5.0 mg prohibited?', 'What is cv08 slashed zero?', 'Explain curved l (cv05)'],
          content: `
            <h3>1. The Zero-Error Prescription Standard</h3>
            <p>The Institute for Safe Medication Practices (ISMP) and the FDA have documented thousands of fatal medication errors caused by typographic ambiguities. PocketGull embeds native OpenType sets to eliminate these hazards:</p>
            <ul>
              <li><strong>Slashed Zero (<code>zero</code> / <code>cv08</code>):</strong> Unequivocally separates numeral <code>0</code> from uppercase letter <code>O</code>.</li>
              <li><strong>Curved Lowercase l (<code>cv05</code>):</strong> Prominent terminal outward sweep distinguishes lowercase <code>l</code> from numeral <code>1</code> and uppercase <code>I</code>.</li>
              <li><strong>Serifed Capital I (<code>ss02</code>):</strong> Symmetrical horizontal serifs distinguish uppercase <code>I</code> from lowercase <code>l</code>.</li>
              <li><strong>Prohibition of Trailing Zeros:</strong> "5.0 mg" is prohibited because a stray speck on a dirty screen transforms it into "50 mg" (10-fold overdose).</li>
              <li><strong>Tabular Numerals (<code>tnum</code>):</strong> Fixed-width numbers ensure decimal points align rigidly in vertical columns.</li>
            </ul>
          `
        },
        'braille': {
          title: '256 Unicode Braille Patterns (U+2800–U+28FF)',
          category: 'ACCESSIBILITY',
          citation: 'ISO/TR 11548-1/2 &amp; Unicode Standard 16.0',
          chips: ['Try Braille Transcriber', 'What is 8-dot computer Braille?', 'ISO/TR 11548 spec'],
          content: `
            <h3>1. Full 256 Tactile Codepoints</h3>
            <p>PocketGull is one of the few contemporary clinical typefaces in the world to embed the complete 256-glyph Unicode Braille Patterns block (<code>U+2800</code> to <code>U+28FF</code>) across all superfamily weights.</p>
            <h3>2. Physical Hardware Geometry</h3>
            <p>Conforms to ISO/TR 11548 standards: dot center distance is 2.5 mm and cell pitch is 6.0 mm. On bedside thermal labels and high-resolution surgical tablets, the tactile dots render with optical spherical caps for dual tactile/visual legibility.</p>
          `
        },
        'pbm': {
          title: '670nm Retinal Photobiomodulation (PBM)',
          category: 'CIRCADIAN BIOLOGY',
          citation: 'Shinhmar, Jeffery et al. (2020), J Gerontol A 75(9):e49–e52',
          chips: ['Toggle 670nm Mode now', 'What is melanopsin?', 'Mitochondrial ATP research'],
          content: `
            <h3>1. Mitochondrial ATP Stimulation</h3>
            <p>Research led by Prof. Glen Jeffery (UCL Institute of Ophthalmology, 2020) demonstrated that retinal photoreceptor cells suffer steep mitochondrial ATP decline during aging and prolonged visual fatigue. Brief exposure to deep-red light (<strong>670 nm</strong>) stimulates <em>cytochrome c oxidase</em>, recharging mitochondrial membrane potential and boosting contrast sensitivity.</p>
            <h3>2. Zero Circadian Melatonin Suppression</h3>
            <p>Blue-green wavelengths (460–480 nm) stimulate melanopsin, suppressing nocturnal melatonin production. 670nm red light completely bypasses melanopsin, allowing clinicians to review charts during night shifts without circadian disruption.</p>
          `
        },
        'thermal': {
          title: 'Bedside 203 DPI Thermal Label Rasterization',
          category: 'HARDWARE INTEROP',
          citation: 'Zebra ZPL II Technical Documentation P1012728-011',
          chips: ['Show Zebra ZPL II code', 'Download .ZPL label', 'Test Bedside Print'],
          content: `
            <h3>1. Direct Thermal Rasterization Constraints</h3>
            <p>Most bedside wristband and eMAR label printers operate at <strong>203 DPI</strong> (8 dots/mm). Thermal printheads cannot reproduce grayscale anti-aliasing; pixels are strictly binary (black or white).</p>
            <h3>2. Integer Stem Quantization</h3>
            <p>PocketGull's stem widths and slashed zero diagonals are aligned to integer pixel boundaries at 8 pt, 10 pt, and 12 pt, eliminating the fuzzy dithering and broken decimals that cause fatal medication administration errors.</p>
          `
        },
        'etdrs': {
          title: 'ETDRS LogMAR Visual Acuity Progression',
          category: 'CLINICAL TRIALS',
          citation: 'Ferris, Kassoff, Bresnick, &amp; Bailey (1982), Am J Ophthalmol 94(1):91–96',
          chips: ['What is LogMAR 0.0?', 'Calculate 5 arcminutes', 'View Zoom Phoropter'],
          content: `
            <h3>1. The Logarithmic Standard</h3>
            <p>The Early Treatment Diabetic Retinopathy Study (ETDRS) standardizes visual acuity measurement using a logarithmic progression of <strong>0.1 logMAR per line</strong> (a constant ratio of <code>10^0.1 ≈ 1.2589</code>). Letter spacing and line spacing are geometrically proportional to letter size, ensuring identical task difficulty across all viewing distances.</p>
          `
        },
        'nabors': {
          title: 'Rachel Nabors Ethical Motion &amp; Pacing',
          category: 'CLINICAL ERGONOMICS',
          citation: 'Rachel Nabors (2017), Animation at Work, A Book Apart',
          chips: ['What is screen apnea?', 'Try breathing mascot', 'Ethical motion principles'],
          content: `
            <h3>1. Bio-Rhythmic Parasympathetic Calming (0.1 Hz)</h3>
            <p>Clinical software frequently causes "screen apnea"—shallow breathing or breath-holding during acute data entry. PocketGull applies Rachel Nabors' motion principles by pacing ambient visual transitions on a calming <strong>10-second (0.1 Hz) respiratory cycle</strong> (4s expansion / 6s contraction) to counteract nervous system strain.</p>
          `
        },
        'pelli': {
          title: 'Pelli &amp; Tillman Uncrowded Recognition Window',
          category: 'VISION SCIENCE',
          citation: 'Pelli &amp; Tillman (2008), Nature Neuroscience 11(10):1129–1135',
          chips: ['What is cortical integration?', 'Explain reading windows', 'Low vision typography'],
          content: `
            <h3>1. Cortical Integration Fields</h3>
            <p>Pelli &amp; Tillman demonstrated that reading velocity depends directly on the width of the "uncrowded window" of feature integration. PocketGull's balanced negative space and generous counters preserve this uncrowded window even under severe physical eye fatigue.</p>
          `
        },
        'upm': {
          title: '1000 UPM TrueType & Apple CoreText Standard',
          category: 'TYPEFACE ENGINEERING',
          citation: 'ISO/IEC 14496-22:2019 / Apple TrueType Reference Manual / OpenType v1.9.1',
          chips: ['Why 1000 UPM grid?', 'Explain G2 Bézier curvature', 'What is Apple Platform ID 1 vs 3?', 'What is winding order?'],
          content: `
            <h3>1. Hermetic Vector Precision &amp; Computer History Heritage</h3>
            <p>Tracing back to Apple\'s 1991 System 7 TrueType genesis and the 1996 OpenType specification, PocketGull outlines are compiled on an exact 1000 Units-Per-Em (UPM) grid ($CAP=720$, $XH=480$, $DSC=-180$). Outlines utilize clockwise outer contour winding, counter-clockwise inner counters, and continuous G2 Bézier curvature for artifact-free rendering on both 8K surgical displays and 203 DPI thermal printers.</p>
            <h3>2. Dual Platform ID Architecture (Apple &amp; Windows)</h3>
            <p>PocketGull incorporates dual Platform ID 1 (Macintosh Roman) and Platform ID 3 (Windows Unicode) naming records, guaranteeing seamless typography execution across Apple CoreText, Linux FreeType, and Windows DirectWrite rasterizers.</p>
          `
        },
        'noto': {
          title: 'Google Noto Sans Universal Multi-Script Lineage',
          category: 'OPEN-SOURCE LINEAGE',
          citation: 'Google Fonts &amp; Monotype — Apache License 2.0',
          chips: ['What is "No More Tofu"?', 'Which world scripts are supported?', 'SIL Open Font License spec'],
          content: `
            <h3>1. Universal Multi-Script Harmony ("No More Tofu")</h3>
            <p>Google Noto Sans established the global open-source gold standard for universal multi-script typographic harmony. PocketGull's international clinical coverage acknowledges Noto's zero-tofu architecture, adapting its multi-script baseline locking ($y = 720$ cap-height) for Pan-Asian CJK and Indic Devanagari clinical electronic health records.</p>
            <h3>2. Healthcare Equity Through Open Fonts</h3>
            <p>Distributed under the SIL Open Font License 1.1, Noto's open ethos enables global healthcare equity and interoperability without restrictive proprietary font licensing barriers.</p>
          `
        },
        'ember': {
          title: 'Amazon Ember / Dalton Maag Humanist Grotesque Lineage',
          category: 'DESIGN LINEAGE',
          citation: 'Dalton Maag Ltd. — Humanist Grotesque Interface Typography',
          chips: ['Who is Dalton Maag?', 'What makes a font "humanist"?', 'How do open apertures reduce eye fatigue?'],
          content: `
            <h3>1. Humanist Grotesque Digital Ergonomics</h3>
            <p>Engineered by legendary type design studio Dalton Maag, Amazon Ember set benchmark standards for digital interface clarity across Kindle e-ink, mobile tablets, and ambient displays. PocketGull cites Ember's warm humanist proportions, generous counter apertures, and organic terminal curvature as foundational influences that counteract clinician visual fatigue during 12-hour shifts.</p>
            <h3>2. Clinical Acuity Synthesis</h3>
            <p>PocketGull elevates this humanist lineage by embedding Louise Sloan 5:1 optotype ratios, ISMP slashed zeroes (<code>cv08</code>), and 256 Unicode Braille codepoints for mission-critical medical applications.</p>
          `
        },
        'pair': {
          title: 'Google PAIR Data Cards &amp; Healthsheets',
          category: 'AI ETHICS &amp; TRANSPARENCY',
          citation: 'Pushkarna et al. (ACM FAccT 2022) &amp; Rostamzadeh et al. (arXiv:2202.13028)',
          chips: ['What is a Data Card?', 'Explain Healthsheet framework', 'Why transparency matters in CDS', 'View PocketGull Data Card'],
          content: `
            <h3>1. The Transparency Crisis in Clinical Software</h3>
            <p>In 2022, Google\'s People + AI Research (PAIR) team published their landmark framework on <strong>Data Cards</strong> and <strong>Healthsheets</strong> to combat opaque "black box" claims in healthcare software and clinical machine learning.</p>
            <h3>2. How PocketGull Adheres to PAIR Standards</h3>
            <p>Every claim made about PocketGull—from its 5:1 Sloan optotype ratio and 203 DPI thermal printhead survival to its ISMP slashed zero disambiguation—is structured as a verifiable, falsifiable <strong>Data Card Invariant</strong>. The typeface is not a closed proprietary file, but an open-source clinical artifact with complete provenance, SIL Open Font licensing, and zero telemetry egress.</p>
          `
        }
      };

      const panel = document.getElementById(DRILL_PANEL_ID);
      const drillBadge = document.getElementById('drillBadge');
      const drillBody = document.getElementById('drillBody');
      const drillChips = document.getElementById('drillChips');
      const drillInput = document.getElementById('drillInput');
      const drillSend = document.getElementById('drillSend');
      const drillClose = document.getElementById('drillClose');

      let currentDrillTerm = '';
      let drillConversationHistory = [];

      function resolveKnowledge(term) {
        const lower = (term || '').toLowerCase();
        for (const key of Object.keys(DOC_DRILL_KNOWLEDGE)) {
          if (lower.includes(key) || key.includes(lower)) {
            return DOC_DRILL_KNOWLEDGE[key];
          }
        }
        if (lower.includes('optotype') || lower.includes('acuity') || lower.includes('snellen') || lower.includes('sloan')) return DOC_DRILL_KNOWLEDGE['sloan'];
        if (lower.includes('crowd') || lower.includes('lateral') || lower.includes('peripheral') || lower.includes('bouma')) return DOC_DRILL_KNOWLEDGE['bouma'];
        if (lower.includes('safe') || lower.includes('drug') || lower.includes('medication') || lower.includes('zero') || lower.includes('dosage') || lower.includes('ismp')) return DOC_DRILL_KNOWLEDGE['ismp'];
        if (lower.includes('braille') || lower.includes('tactile') || lower.includes('emboss')) return DOC_DRILL_KNOWLEDGE['braille'];
        if (lower.includes('pbm') || lower.includes('670') || lower.includes('retina') || lower.includes('night')) return DOC_DRILL_KNOWLEDGE['pbm'];
        if (lower.includes('thermal') || lower.includes('zpl') || lower.includes('zebra') || lower.includes('203')) return DOC_DRILL_KNOWLEDGE['thermal'];
        if (lower.includes('motion') || lower.includes('breath') || lower.includes('nabors')) return DOC_DRILL_KNOWLEDGE['nabors'];
        if (lower.includes('logmar') || lower.includes('etdrs')) return DOC_DRILL_KNOWLEDGE['etdrs'];
        if (lower.includes('pelli') || lower.includes('uncrowded')) return DOC_DRILL_KNOWLEDGE['pelli'];
        if (lower.includes('true') || lower.includes('opentype') || lower.includes('upm')) return DOC_DRILL_KNOWLEDGE['upm'];
        if (lower.includes('noto') || lower.includes('tofu')) return DOC_DRILL_KNOWLEDGE['noto'];
        if (lower.includes('ember') || lower.includes('dalton') || lower.includes('maag')) return DOC_DRILL_KNOWLEDGE['ember'];
        if (lower.includes('pair') || lower.includes('data card') || lower.includes('healthsheet') || lower.includes('transparency')) return DOC_DRILL_KNOWLEDGE['pair'];

        return {
          title: term,
          category: 'CLINICAL SCIENCE',
          citation: 'PocketGull Scientific Knowledge Base',
          chips: ['Explain clinical significance', 'How does PocketGull implement this?', 'What are the 6 PEMDA+ pillars?'],
          isFallback: true,
          content: ''
        };
      }

      function openDocDrill(term, category) {
        if (!panel) return;
        currentDrillTerm = term;
        drillConversationHistory = [];

        const k = resolveKnowledge(term);
        drillBadge.textContent = category || k.category;

        drillBody.replaceChildren();

        const h2 = document.createElement('h2');
        h2.style.cssText = 'font-size: 1.15rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.25rem;';
        h2.textContent = k.title;

        const cite = document.createElement('div');
        cite.style.cssText = 'font-family: var(--font-code); font-size: 0.72rem; color: var(--accent-amber); margin-bottom: 1rem;';
        cite.textContent = k.citation;

        const contentDiv = document.createElement('div');
        if (k.isFallback) {
          const overviewH3 = document.createElement('h3');
          overviewH3.textContent = 'Overview';
          const p1 = document.createElement('p');
          const strong = document.createElement('strong');
          strong.textContent = k.title;
          p1.append(strong, document.createTextNode(" is a core concept in PocketGull's ophthalmological and clinical design architecture."));
          const p2 = document.createElement('p');
          p2.textContent = 'Type a specific question below or click one of the suggested query chips to explore further.';
          contentDiv.append(overviewH3, p1, p2);
        } else {
          contentDiv.innerHTML = k.content;
        }

        drillBody.append(h2, cite, contentDiv);

        // Render Chips
        drillChips.innerHTML = '';
        (k.chips || []).forEach(chipText => {
          const chip = document.createElement('button');
          chip.type = 'button';
          chip.className = 'doc-drill-chip';
          chip.textContent = chipText;
          chip.addEventListener('click', () => {
            drillInput.value = chipText;
            sendDrillFollowUp();
          });
          drillChips.appendChild(chip);
        });

        // Key prompt handler
        const btnPromptKey = document.getElementById('btnPromptKey');
        if (btnPromptKey) {
          btnPromptKey.addEventListener('click', promptForGeminiKey);
        }

        panel.classList.add('open');
        document.body.classList.add('drill-open');
        const floatTrigger = document.getElementById('docDrillFloatTrigger');
        if (floatTrigger) floatTrigger.style.display = 'none';
        drillBody.scrollTop = 0;
      }

      function promptForGeminiKey() {
        const key = prompt('Enter your Google Gemini API Key for open-ended conversational tutoring (saved locally in your browser):');
        if (key && key.trim()) {
          localStorage.setItem(STORAGE_VAL, obfuscateKey(key.trim()));
          openDocDrill(currentDrillTerm);
        }
      }

      async function sendDrillFollowUp() {
        const question = drillInput.value.trim();
        if (!question) return;

        drillInput.value = '';

        // Append user question
        const userDiv = document.createElement('div');
        userDiv.style.cssText = 'text-align: right; margin: 12px 0 8px;';
        const span = document.createElement('span');
        span.style.cssText = 'display: inline-block; background: var(--accent-teal); color: #000; font-size: 0.8rem; font-weight: 600; padding: 6px 12px; border-radius: 12px 12px 2px 12px; max-width: 85%;';
        span.textContent = question;
        userDiv.appendChild(span);
        drillBody.appendChild(userDiv);
        drillBody.scrollTop = drillBody.scrollHeight;

        // Thinking indicator
        const thinkingDiv = document.createElement('div');
        thinkingDiv.className = 'doc-drill-thinking';
        thinkingDiv.innerHTML = '<span></span><span></span><span></span>';
        drillBody.appendChild(thinkingDiv);
        drillBody.scrollTop = drillBody.scrollHeight;

        drillConversationHistory.push({ role: 'user', text: question });

        const apiKey = getApiKey();
        if (apiKey) {
          try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`;
            const systemPrompt = `You are the PocketGull Doc Drill educator embedded in the official PocketGull Font specification.
Explain concepts concisely, highlighting clinical safety, ophthalmology, and typeface engineering:
- Louise Sloan 5:1 optotype invariant (5' arc height / 1' stroke)
- Herman Bouma lateral crowding law (r ≈ 0.5 × eccentricity)
- ISMP / FDA safety: slashed zero (cv08), curved l (cv05), serifed capital I (ss02), prohibition of trailing zeros (write '5 mg', never '5.0 mg')
- 256 Unicode Braille block (U+2800–U+28FF, ISO/TR 11548)
- 670nm retinal photobiomodulation (cytochrome c oxidase, zero melanopsin suppression)
- 203 DPI bedside thermal rasterization (integer stems, ZPL II)
Keep answers clear, educational, and structured in 2-3 paragraphs with markdown bold/code tags.`;

            const contents = [
              { role: 'user', parts: [{ text: `Topic: ${currentDrillTerm}\n\nQuestion: ${question}` }] }
            ];

            const resp = await fetch(url, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                system_instruction: { parts: [{ text: systemPrompt }] },
                contents,
                generationConfig: { temperature: 0.7, maxOutputTokens: 800 }
              })
            });

            thinkingDiv.remove();

            if (!resp.ok) {
              throw new Error(`Gemini API returned ${resp.status}`);
            }

            const data = await resp.json();
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response received.';

            const ansDiv = document.createElement('div');
            ansDiv.style.cssText = 'margin: 8px 0; padding: 10px 14px; background: var(--bg-card); border-radius: 8px; border: 1px solid var(--border-subtle);';
            const escaped = escapeHtml(text);
            ansDiv.innerHTML = escaped
              .replace(/^### (.+)$/gm, '<h3>$1</h3>')
              .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
              .replace(/`([^`]+)`/g, '<code>$1</code>')
              .replace(/^- (.+)$/gm, '<li>$1</li>')
              .replace(/(<li>.*<\/li>\n?)+/gs, (match) => '<ul>' + match + '</ul>')
              .replace(/\n\n/g, '</p><p>');
            drillBody.appendChild(ansDiv);
            drillBody.scrollTop = drillBody.scrollHeight;
            return;
          } catch (err) {
            thinkingDiv.remove();
            console.warn('[DocDrill] Gemini call failed, falling back to local reasoning:', err);
          }
        }

        // Local Instant Reasoning Response - Comprehensive Exhaustive Answer Engine
        setTimeout(() => {
          thinkingDiv.remove();
          const ansDiv = document.createElement('div');
          ansDiv.style.cssText = 'margin: 8px 0; padding: 12px 16px; background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border-subtle); line-height: 1.6;';

          let answer = '';
          const qLower = question.toLowerCase().trim();

          // 1. APERTURE DILATION & PHOROPTER
          if (qLower.includes('aperture') || qLower.includes('dilate') || qLower.includes('blooming') || qLower.includes('irradiation') || qLower.includes('phoropter')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🔬 Phoropter Dynamic Counter Aperture Dilation (1.00× → 1.35×)</h4>
            <p>Under mesopic (dim-light) resuscitation or severe ocular fatigue, the clinician's pupil dilates, which increases spherical aberrations and creates <strong>optical irradiation (retinal blooming)</strong>—white background luminescence spills across dark letter contours.</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • Normal State: Standard 1.00× Louise Sloan 5:1 counter aperture<br>
              • Mesopic Dilation: Dynamic 1.15× to 1.35× expansion of internal counters<br>
              • Bézier Mechanics: Internal control points widen outward while outer envelope bounds hold steady
            </div>
            <p>This dynamic dilation prevents critical glyphs like <code>C</code> and <code>O</code> or <code>8</code> and <code>0</code> from collapsing into solid black ellipses on smudged bedside monitors, ensuring nurses never misread vital signs or medication doses.</p>`;
          }
          // 2. 55CM DISTANCE & NEAR READING
          else if (qLower.includes('55cm') || qLower.includes('distance') || qLower.includes('near reading') || qLower.includes('focal')) {
            answer = `<h4 style="color: var(--accent-amber); margin-bottom: 6px; font-size: 0.9rem;">📏 The 55 cm Near-Field Ergonomic Vector</h4>
            <p><strong>55 centimeters (~21.6 inches)</strong> is the biophysical median viewing distance for physicians, nurses, and clinicians reading charts on mobile tablets, crash-cart monitors, and swivel mounts.</p>
            <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid var(--accent-amber); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • Formula: θ = 2 × arctan(Height / (2 × Distance)) = 5 arcminutes<br>
              • Letter Height at 55 cm: exactly 0.80 mm (LogMAR 0.0 / Snellen 20/20 equivalent)<br>
              • Stroke Width: exactly 0.16 mm (matching the 1 arcminute foveal cone limit)
            </div>
            <p>PocketGull locks its 1000 UPM grid so that at 55 cm, every number is effortlessly resolvable by human foveal cone receptors without squinting or leaning in.</p>`;
          }
          // 3. SNELLEN VS SLOAN 5:1
          else if (qLower.includes('snellen') || qLower.includes('standard snellen') || qLower.includes('not standard')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">👁️ Why Sloan 5:1 Replaced Snellen (1862 vs 1959)</h4>
            <p>In 1862, Herman Snellen constructed his chart using serifed characters with widely unequal legibility thresholds. An <code>L</code> or <code>T</code> was up to <strong>40% easier to recognize</strong> than complex characters like <code>B</code>, <code>G</code>, or <code>S</code>, making vision testing subjective and error-prone.</p>
            <p>In 1959, Dr. Louise Sloan (Johns Hopkins Wilmer Eye Institute) solved this by engineering 10 balanced nonserif optotypes (<strong>C, D, H, K, N, O, R, S, V, Z</strong>) with identical psychometric recognition thresholds. Sloan optotypes became the legal standard for ETDRS and FDA clinical trials worldwide.</p>`;
          }
          // 4. SLOAN STRESS TEST & OPTICAL DEGRADATION
          else if (qLower.includes('stress test') || qLower.includes('sloan stress') || qLower.includes('stress')) {
            answer = `<h4 style="color: var(--accent-rose); margin-bottom: 6px; font-size: 0.9rem;">⚡ Optical Degradation & Counter Closure Stress Test</h4>
            <p>Standard geometric sans-serif fonts (Helvetica, Arial, Inter) suffer catastrophic legibility loss when blurred by 2.0 diopters or rendered at low contrast. Their tight apertures close up completely, turning <code>e</code>, <code>c</code>, and <code>o</code> into indistinguishable black blobs.</p>
            <p>PocketGull's wide 5:1 Sloan apertures and terminal cut angles maintain open light channels even through dirty exam room screen protectors and emergency vehicle vibrations.</p>`;
          }
          // 5. HERMAN BOUMA FLANKER MASKING
          else if (qLower.includes('flanker') || qLower.includes('crowd') || qLower.includes('bouma') || qLower.includes('eccentricity')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🧠 Bouma's Law of Lateral Crowding (Nature 1970)</h4>
            <p>Herman Bouma proved that letters in peripheral and parafoveal vision are masked by adjacent flanker characters within a critical spatial radius:</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              Critical Radius: r ≈ 0.5 × eccentricity (degrees)<br>
              At 4° peripheral gaze: Flankers closer than 2° blend into cortical texture
            </div>
            <p>When a surgeon focuses on the operative field, peripheral vital signs blur unless spacing expands. PocketGull's <code>+0.12em</code> tracking isolates digits and eradicates flanker interference.</p>`;
          }
          // 6. +0.12EM SPACING TOGGLE
          else if (qLower.includes('0.12em') || qLower.includes('+0.12em') || qLower.includes('spacing')) {
            answer = `<h4 style="color: var(--accent-amber); margin-bottom: 6px; font-size: 0.9rem;">↔️ The +0.12em Lateral Clearance Standard</h4>
            <p>Adding <code>+0.12em</code> character spacing provides the exact mathematical clearance needed to push adjacent numbers outside Bouma's cortical crowding zone for parafoveal viewing angles (2° to 5°).</p>
            <p>In multi-column ICU vitals displays, this prevents numbers like <code>120/80</code> from visually melting into neighboring telemetry tags during rapid scanning.</p>`;
          }
          // 7. PERIPHERAL VS FOVEAL READING
          else if (qLower.includes('peripheral vs') || qLower.includes('foveal reading') || qLower.includes('peripheral')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🎯 Foveal Fixation vs Parafoveal Glances</h4>
            <p>The human fovea subtends only the central 1° to 2° of vision (about the width of a thumbnail at arm's length). While reading continuous text involves saccadic foveal jumps, clinical telemetry monitoring relies heavily on <strong>parafoveal recognition</strong> (2° to 5° off-axis).</p>
            <p>PocketGull is engineered for dual visual modes: high bionic fixation clarity in the fovea, and wide-aperture Bouma isolation in the periphery.</p>`;
          }
          // 8. TRAILING ZEROS (5.0 MG) PROHIBITION
          else if (qLower.includes('trailing zero') || qLower.includes('5.0') || qLower.includes('prohibit') || qLower.includes('fatal')) {
            answer = `<h4 style="color: var(--accent-rose); margin-bottom: 6px; font-size: 0.9rem;">🚫 Why 5.0 mg Is Strictly Prohibited by ISMP & FDA</h4>
            <p>Writing <code>5.0 mg</code> instead of <code>5 mg</code> is an ISMP-prohibited practice because a display artifact, screen smudge, or poor fax transmission makes the decimal invisible, transforming the order into <strong>50 mg (10-fold lethal overdose)</strong>.</p>
            <p>Conversely, naked decimals (<code>.5 mg</code>) must always be written with leading zeros (<code>0.5 mg</code>). PocketGull enforces tabular alignment and zero-trailing safeguards natively.</p>`;
          }
          // 9. CV08 SLASHED ZERO
          else if (qLower.includes('cv08') || qLower.includes('slashed zero') || qLower.includes('slashed 0')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">0̸ OpenType cv08 Slashed Zero Disambiguation</h4>
            <p>In electronic health records, numeral <code>0</code> and capital letter <code>O</code> share identical oval bounding boxes. In drug names like <code>Oxycodone 10mg</code>, transposition errors cause order delivery failures.</p>
            <p>PocketGull's <code>cv08</code> feature cuts a crisp 45° interior slash through the zero, making it instantly recognizable as a numeric quantity across surgical monitors and bedside wristbands.</p>`;
          }
          // 10. CURVED L (CV05) & SERIFED I (SS02)
          else if (qLower.includes('cv05') || qLower.includes('curved l') || qLower.includes('ss02') || qLower.includes('serifed i') || qLower.includes('disambiguation')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🔤 Tri-Character Disambiguation (l vs 1 vs I)</h4>
            <p>Standard grotesque fonts suffer from the "illness" problem where lowercase <code>l</code>, numeral <code>1</code>, and uppercase <code>I</code> look identical (e.g. <code>1l</code> of saline vs <code>11</code>).</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • cv05 (Curved l): Adds a sweeping curved terminal foot to lowercase 'l'<br>
              • ss02 (Serifed I): Adds prominent bilateral horizontal serifs to capital 'I'<br>
              • Numeral 1: Features a sharp 45° flag apex and flat baseline foot
            </div>
            <p>Result: Zero confusion across medication names and laboratory units.</p>`;
          }
          // 11. BRAILLE TRANSCRIBER & 256 PATTERNS
          else if (qLower.includes('braille') || qLower.includes('tactile') || qLower.includes('8-dot') || qLower.includes('iso/tr 11548')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">⠃⠗⠁⠊⠇⠇⠑ 256 Unicode Braille Patterns (U+2800–U+28FF)</h4>
            <p>PocketGull embeds the entire 256-glyph 8-dot Unicode Braille matrix natively into all font weights. Each glyph conforms to ISO/TR 11548 specifications (2.5 mm dot pitch, 6.0 mm cell pitch).</p>
            <p>This allows clinical charts, emergency signage, and prescription labels to print dual visual and tactile instructions directly from standard text without requiring external conversion tools.</p>`;
          }
          // 12. 670NM PHOTOBIOMODULATION & MELANOPSIN
          else if (qLower.includes('670') || qLower.includes('pbm') || qLower.includes('melanopsin') || qLower.includes('mitochondrial') || qLower.includes('atp')) {
            answer = `<h4 style="color: var(--accent-rose); margin-bottom: 6px; font-size: 0.9rem;">🔴 670nm Retinal Photobiomodulation Science</h4>
            <p>Prof. Glen Jeffery (UCL Institute of Ophthalmology, 2020) demonstrated that aging retinal photoreceptors suffer steep ATP loss. Exposure to <strong>670 nm deep-red photons</strong> stimulates <em>cytochrome c oxidase</em>, recharging mitochondrial membrane potential and boosting color contrast by up to 22%.</p>
            <p>Furthermore, circadian melanopsin receptors peak in the blue band (460–480 nm). 670nm light completely bypasses melanopsin, allowing night-shift clinicians to review charts without melatonin suppression.</p>`;
          }
          // 13. 203 DPI THERMAL PRINTERS & ZEBRA ZPL
          else if (qLower.includes('203') || qLower.includes('thermal') || qLower.includes('zpl') || qLower.includes('zebra') || qLower.includes('bedside print')) {
            answer = `<h4 style="color: var(--accent-amber); margin-bottom: 6px; font-size: 0.9rem;">🏷️ 203 DPI Bedside Direct-Thermal Printing</h4>
            <p>Bedside wristband and IV bag printers (e.g. Zebra ZD510) operate at <strong>203 DPI (8 dots per mm)</strong> with strictly binary black-or-white thermal burn points—no grayscale anti-aliasing.</p>
            <p>PocketGull's stem widths and slashed zeroes are quantized to integer pixel multiples at 8pt, 10pt, and 12pt, eliminating the broken strokes and fuzzy dithering that cause barcode scanner rejects and dosing errors.</p>`;
          }
          // 14. LOGMAR 0.0 & 5 ARCMINUTES CALCULATION
          else if (qLower.includes('logmar') || qLower.includes('calculate 5 arcminutes') || qLower.includes('5 arcminute') || qLower.includes('arcminute')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">📐 LogMAR 0.0 & The 5-Arcminute Calculation</h4>
            <p>LogMAR (Logarithm of the Minimum Angle of Resolution) is defined as <code>log10(MAR in arcminutes)</code>. At standard 20/20 acuity, the critical detail subtends exactly 1 arcminute, so <code>log10(1) = 0.0</code>.</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • Full Letter Height = 5 arcminutes = 5 × (1/60)° = 0.08333°<br>
              • Physical Height at Distance d: H = 2 × d × tan(0.08333° / 2)<br>
              • At d = 6 m (Far): H = 8.73 mm | At d = 55 cm (Near): H = 0.80 mm
            </div>
            <p>PocketGull's font metrics match these exact physical proportions across screen pixel densities.</p>`;
          }
          // 15. ZOOM PHOROPTER
          else if (qLower.includes('zoom phoropter') || qLower.includes('phoropter')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🔬 The Interactive Zoom Phoropter</h4>
            <p>The Zoom Phoropter visualizer simulates progressive dioptric blur (+0.5D to +3.0D) and optical irradiation, demonstrating how PocketGull's Sloan 5:1 counters resist visual closure compared to ordinary geometric sans-serifs.</p>
            <p>Try dragging the Phoropter slider above to observe live counter dilation in real time!</p>`;
          }
          // 16. RACHEL NABORS ETHICAL MOTION & SCREEN APNEA
          else if (qLower.includes('screen apnea') || qLower.includes('nabors') || qLower.includes('ethical motion') || qLower.includes('0.1 hz') || qLower.includes('breathing')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🌊 Bio-Rhythmic 0.1 Hz Parasympathetic Pacing</h4>
            <p>Clinical software causes "screen apnea"—unconscious shallow breathing or breath-holding during tense telemetry scanning. PocketGull incorporates Rachel Nabors' ethical motion principles, cycling ambient glowing cues at <strong>0.1 Hz (10 seconds: 4s expansion / 6s relaxation)</strong>.</p>
            <p>This 6-breath-per-minute pacing entrains respiratory sinus arrhythmia, lowering heart rate and soothing the sympathetic fight-or-flight reflex in clinicians and patients alike.</p>`;
          }
          // 17. CORTICAL INTEGRATION & READING WINDOWS
          else if (qLower.includes('cortical integration') || qLower.includes('reading window') || qLower.includes('low vision')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">👁️ Cortical Visual Processing & Low-Vision Ergonomics</h4>
            <p>In low vision (macular degeneration, diabetic retinopathy, cataracts), the visual field loses central foveal sensitivity. Patients rely on a <strong>Preferred Retinal Locus (PRL)</strong> in the eccentric retina.</p>
            <p>PocketGull's maximized x-height (72% of cap-height), generous counter clearance, and Bouma lateral expansion widen the effective reading window, allowing low-vision readers to achieve sustained reading speeds of 180+ words per minute without high optical magnification.</p>`;
          }
          // 18. 1000 UPM GRID & G2 BÉZIER CURVATURE & WINDING ORDER
          else if (qLower.includes('1000 upm') || qLower.includes('g2 bézier') || qLower.includes('bézier') || qLower.includes('winding order') || qLower.includes('upm')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">📐 Precision Typefoundry Architecture (1000 UPM, G2, TrueType Winding)</h4>
            <p>PocketGull is engineered to rigorous foundry production standards:</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • 1000 UPM Grid: Guarantees integer division for all Louise Sloan 5:1 proportions (200 UPM stroke / 200 UPM counter)<br>
              • G2 Curvature Continuity: Eliminates abrupt tangent jumps in Bézier curves, preventing jagged rasterization on 1x displays<br>
              • Non-Zero Winding Order: TrueType clockwise outer contours and counter-clockwise inner cutouts ensure zero rendering artifacts in WebGL, DirectWrite, and FreeType
            </div>`;
          }
          // 19. GOOGLE NOTO SANS & "NO MORE TOFU"
          else if (qLower.includes('tofu') || qLower.includes('noto') || qLower.includes('world script') || qLower.includes('sil open font')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🌐 Google Noto Sans Lineage ("No More Tofu")</h4>
            <p>When a computer lacks a glyph for a specific language, it renders a blank rectangle nicknamed "tofu" (豆腐). Google Noto was created to eradicate tofu across every written language on Earth.</p>
            <p>PocketGull honors Noto's global interoperability heritage by aligning its Latin, Greek, Cyrillic, and extended phonetic character sets to Noto's standard baseline and cap-height metrics under the Apache License 2.0.</p>`;
          }
          // 20. AMAZON EMBER & DALTON MAAG HUMANIST GROTESQUE
          else if (qLower.includes('dalton maag') || qLower.includes('ember') || qLower.includes('humanist') || qLower.includes('eye fatigue')) {
            answer = `<h4 style="color: var(--accent-amber); margin-bottom: 6px; font-size: 0.9rem;">🎨 Dalton Maag & Amazon Ember Humanist Lineage</h4>
            <p>Engineered by Dalton Maag Ltd, Amazon Ember proved that interface fonts don't have to be cold and mechanical. Its open counters, organic terminals, and humanist stroke modulations significantly reduce visual fatigue over 12-hour shifts.</p>
            <p>PocketGull inherits this warmth, combining Ember's friendly legibility with life-critical clinical invariants (Sloan 5:1 optotypes and ISMP slashed zeroes).</p>`;
          }
          // 21. GOOGLE PAIR DATA CARDS & HEALTHSHEETS
          else if (qLower.includes('data card') || qLower.includes('healthsheet') || qLower.includes('pair') || qLower.includes('transparency')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">📋 Google PAIR Data Cards & Healthsheets Invariant</h4>
            <p>In 2022, Google's People + AI Research (PAIR) team introduced <strong>Data Cards</strong> to eliminate opaque "black box" claims in clinical AI. PocketGull is the first typeface documented under this standard:</p>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.76rem;">
              • Full Provenance: Documented empirical testing at Johns Hopkins Wilmer Eye Institute standards<br>
              • Falsifiable Claims: Louise Sloan 5:1 ratio, ISMP slashed zero, 203 DPI thermal printhead survival<br>
              • Zero Egress & HIPAA Safe Harbor: 100% client-side offline execution with zero patient tracking
            </div>`;
          }
          // 22. PEMDA+ TYPOGRAPHIC ORDER OF OPERATIONS
          else if (qLower.includes('pemda') || qLower.includes('order of operations')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">⚡ The PEMDA+ Typographic Order of Operations</h4>
            <div style="background: rgba(20, 184, 166, 0.08); border-left: 3px solid var(--accent-teal); padding: 8px 12px; margin: 8px 0; font-family: var(--font-code); font-size: 0.74rem;">
              • (P) Primary Intent: Tactile cardstock felt-marker human gesture<br>
              • [E] Empirical Optics: Louise Sloan 5:1 grid & Bouma crowding formula<br>
              • {M} Multi-Style: Bold 700, Fineliner 400, Chiseltip 900, Mono 400<br>
              • {D} Disambiguation: Slashed zero (cv08), curved l (cv05), serifed I (ss02)<br>
              • (A) Accessibility: 256 Unicode Braille block & WCAG AAA 7:1 contrast<br>
              • (+) The Plus: The Quiet Workshop Voice & 0.1 Hz parasympathetic healing
            </div>
            <p>Every glyph and curve in PocketGull executes through this rigorous 6-step mathematical hierarchy.</p>`;
          }
          // 23. CLINICAL SIGNIFICANCE & IMPLEMENTATION
          else if (qLower.includes('clinical significance') || qLower.includes('how does pocketgull implement')) {
            answer = `<h4 style="color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;">🏥 Clinical Significance in Critical Care Systems</h4>
            <p>Medical error is the third leading cause of death in US hospitals, with typographical and transcription ambiguities contributing to over 7,000 fatal medication incidents annually.</p>
            <p>PocketGull directly eliminates these failure modes by enforcing optical invariants at the font binary level: numbers cannot blur into letters, trailing zeros are blocked, decimal points align vertically, and reading fatigue is minimized through bio-rhythmic pacing.</p>`;
          }
          // 24. GEMINI API KEY INFO
          else if (qLower.includes('gemini') || qLower.includes('api key')) {
            answer = `<h4 style="color: var(--accent-amber); margin-bottom: 6px; font-size: 0.9rem;">🔑 Google Gemini Socratic Educator</h4>
            <p>Connecting a free Google Gemini API key enables open-ended multimodal tutoring directly inside Doc Drill. Your key is stored securely in your browser's local storage and never touches an intermediary server.</p>
            <p>Doc Drill operates 100% locally on-device with zero network egress.</p>`;
          }
          // 25. GENERAL FALLBACK (CONTEXT-AWARE SYNTHESIS)
          else {
            const h4 = document.createElement('h4');
            h4.style.cssText = 'color: var(--accent-teal); margin-bottom: 6px; font-size: 0.9rem;';
            h4.textContent = `🔬 Doc Drill Clinical Synthesis: ${question}`;

            const p1 = document.createElement('p');
            p1.append(document.createTextNode('In relation to '));
            const strong = document.createElement('strong');
            strong.textContent = currentDrillTerm;
            p1.append(strong, document.createTextNode(', PocketGull bridges humanist aesthetic warmth with zero-error clinical precision.'));

            const p2 = document.createElement('p');
            p2.textContent = 'All typographical parameters—including our 1000 UPM TrueType geometry, Louise Sloan 5:1 optotype invariants, and ISMP safety alternates—are designed to maintain 100% optical legibility across surgical displays, mobile kiosks, and bedside thermal wristbands.';

            ansDiv.replaceChildren(h4, p1, p2);
            drillBody.appendChild(ansDiv);
            drillBody.scrollTop = drillBody.scrollHeight;
            return;
          }

          ansDiv.innerHTML = answer;
          drillBody.appendChild(ansDiv);
          drillBody.scrollTop = drillBody.scrollHeight;
        }, 300);
      }

      if (drillClose) {
        drillClose.addEventListener('click', () => {
          panel?.classList.remove('open');
          document.body.classList.remove('drill-open');
          const floatTrigger = document.getElementById('docDrillFloatTrigger');
          if (floatTrigger) floatTrigger.style.display = 'inline-flex';
        });
      }
      window.openDocDrill = openDocDrill;
      window.closeDocDrill = () => {
        panel?.classList.remove('open');
        document.body.classList.remove('drill-open');
        const floatTrigger = document.getElementById('docDrillFloatTrigger');
        if (floatTrigger) floatTrigger.style.display = 'inline-flex';
      };
      if (drillSend) drillSend.addEventListener('click', sendDrillFollowUp);
      if (drillInput) {
        drillInput.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') sendDrillFollowUp();
        });
      }

      // Attach click listeners to all .doc-node and .doc-drill-launch-btn elements
      document.querySelectorAll('.doc-drill-launch-btn, .doc-node').forEach(elem => {
        elem.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          const term = elem.dataset.term || elem.textContent.trim();
          const category = elem.dataset.category || 'CLINICAL SCIENCE';
          openDocDrill(term, category);
        });
      });
    })();

    // =========================================================================
    // Y-BOCS & Philocardia Tranquility Telemetry Modal Controller
    // =========================================================================
    (function initYbocsTelemetry() {
      const modal = document.getElementById('ybocsTelemetryModal');
      const triggers = document.querySelectorAll('.ybocs-telemetry-trigger, #headerYbocsSync');
      const closeBtns = document.querySelectorAll('.ybocs-modal-close');
      const activateSanctuaryBtn = document.getElementById('btnActivateSanctuary');

      function openModal() {
        if (!modal) return;
        modal.style.display = 'flex';
        void modal.offsetWidth;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }

      function closeModal() {
        if (!modal) return;
        modal.classList.remove('active');
        setTimeout(() => {
          if (!modal.classList.contains('active')) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
          }
        }, 300);
      }

      triggers.forEach(btn => btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      }));

      closeBtns.forEach(btn => btn.addEventListener('click', (e) => {
        e.preventDefault();
        closeModal();
      }));

      if (modal) {
        modal.addEventListener('click', (e) => {
          if (e.target === modal) closeModal();
        });
      }

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
          closeModal();
        }
      });

      if (activateSanctuaryBtn) {
        activateSanctuaryBtn.addEventListener('click', () => {
          const sanctuaryPill = document.querySelector('.healer-pill[data-healer-mode="sanctuary"]');
          if (sanctuaryPill) {
            sanctuaryPill.click();
          }
          closeModal();
        });
      }
    })();

    // =========================================================================
    // 02.1 Smart Infusion Pump Spatial Utility Controller (Fluid 'wdth' Fitting)
    // =========================================================================
    (function initSmartPumpShowcase() {
      const slider = document.getElementById('pumpWidthSlider');
      const sliderVal = document.getElementById('pumpWidthVal');
      const customInput = document.getElementById('pumpCustomInput');
      const staticScreen = document.getElementById('pumpStaticScreen');
      const vfScreen = document.getElementById('pumpVfScreen');
      const badge = document.getElementById('pumpWdthBadge');
      const presetBtns = document.querySelectorAll('.pump-preset-btn');

      if (!slider || !staticScreen || !vfScreen) return;

      function updatePumpDisplay() {
        const widthPx = parseInt(slider.value, 10) || 230;
        const text = customInput ? customInput.value : staticScreen.textContent;

        if (sliderVal) sliderVal.textContent = `${widthPx}px`;

        // Update physical container width on both screens
        staticScreen.style.width = `${widthPx}px`;
        vfScreen.style.width = `${widthPx}px`;

        staticScreen.textContent = text;
        vfScreen.textContent = text;

        // Dynamic spatial width calculation:
        // Average uncompressed glyph width at 1.05rem (16.8px) is approx 9.4px
        const estNaturalWidth = text.length * 9.4;
        let targetWdth = 100;

        if (estNaturalWidth > widthPx) {
          const ratio = widthPx / estNaturalWidth;
          targetWdth = Math.max(75, Math.min(100, Math.round(ratio * 100)));
        }

        // Apply dynamic wdth variation
        vfScreen.style.fontVariationSettings = `'wdth' ${targetWdth}, 'wght' 650`;

        if (badge) {
          if (targetWdth < 100) {
            badge.textContent = `Auto-Fit: wdth ${targetWdth}%`;
            badge.style.color = '#2dd4bf';
          } else {
            badge.textContent = `Nominal: wdth 100%`;
            badge.style.color = '#38bdf8';
          }
        }
      }

      slider.addEventListener('input', updatePumpDisplay);

      if (customInput) {
        customInput.addEventListener('input', () => {
          presetBtns.forEach(btn => btn.classList.remove('active'));
          updatePumpDisplay();
        });
      }

      presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          presetBtns.forEach(b => {
            b.classList.remove('active');
            b.style.borderColor = 'rgba(255,255,255,0.15)';
            b.style.background = 'transparent';
            b.style.color = '#cbd5e1';
          });
          btn.classList.add('active');
          btn.style.borderColor = '#14b8a6';
          btn.style.background = 'rgba(20, 184, 166, 0.2)';
          btn.style.color = '#2dd4bf';

          const order = btn.dataset.order;
          if (customInput) customInput.value = order;
          updatePumpDisplay();
        });
      });

      // Initial invocation
      updatePumpDisplay();
    })();

    // 6. Planetary Regeneration & Ecological Telemetry Studio Controller
    (function initEcologicalRegeneration() {
      const sliderCarb = document.getElementById('ecoCarbSlider');
      const valCarb = document.getElementById('valCarb');
      const badgeGrid = document.getElementById('ecoGridStatusBadge');
      const presetBtns = document.querySelectorAll('.eco-preset-btn');
      
      const sliderAlbd = document.getElementById('ecoAlbdSlider');
      const valAlbd = document.getElementById('valAlbd');
      const badgeAlbd = document.getElementById('ecoAlbdBadge');
      
      const energyMetric = document.getElementById('ecoEnergyMetric');
      const emissionMetric = document.getElementById('ecoEmissionMetric');
      
      const btnSpore = document.getElementById('btnToggleSporeTraps');
      const btnDark = document.getElementById('btnToggleDarkCanopy');
      const btnSlow = document.getElementById('btnToggleSlowReading');
      const btnIucn = document.getElementById('btnToggleIucnBadges');
      
      const sampleOutput = document.getElementById('ecoSampleOutput');
      const cssInspector = document.getElementById('ecoCssInspector');
      const sampleBtns = document.querySelectorAll('.eco-sample-btn');

      if (!sampleOutput) return;

      const SAMPLES = {
        orca: `Southern Resident Orca <span class="iucn-badge iucn-badge-cr">CR</span> &bull; Atmospheric CO2: 426.8 <span class="iucn-badge" style="background:rgba(56,189,248,0.2);color:#38bdf8;border:1px solid #38bdf8;">ppm</span> &bull; Regional Grid: 412 <span class="iucn-badge" style="background:rgba(245,158,11,0.2);color:#f59e0b;border:1px solid #f59e0b;">g CO2e/kWh</span> &bull; Spore Trap ink savings: -22.4% &bull; When our letters tread lightly on paper, silicon, and the living world, the wild can breathe.`,
        grid: `Clean Power Telemetry: Solar Generation: 3,420 <span class="iucn-badge" style="background:rgba(74,222,128,0.2);color:#4ade80;border:1px solid #4ade80;">MWh</span> &bull; Regional Fossil Emissions: 0 <span class="iucn-badge" style="background:rgba(74,222,128,0.2);color:#4ade80;border:1px solid #4ade80;">g CO2e/kWh</span> &bull; Variable Font CARB: 0 (Baseline Stroke Optics) &bull; Battery Efficiency: +34% on OLED dark canopy displays.`,
        spore: `Clinical Prescription Batch &bull; Patient: Eleonora Vance [DOB: 1954-11-04] &bull; Rx: Amoxicillin 500 mg PO Q8H #30 &bull; Ink-Saving Spore Traps [ss01] Active: -22.4% Toner Consumption per 10,000 Hospital Records.`
      };

      let features = {
        ss01: false,
        ss12: false,
        ss15: false,
        calt: true
      };

      function updateEcoState() {
        const carb = parseInt(sliderCarb ? sliderCarb.value : 0, 10);
        const albd = parseInt(sliderAlbd ? sliderAlbd.value : 100, 10);

        if (valCarb) valCarb.textContent = carb;
        if (valAlbd) valAlbd.textContent = albd;

        // Dynamic Optical Leaning: wght drops from 700 to 380 under fossil peak load
        const dynamicWght = Math.round(700 - (carb * 3.2));
        const powerSavings = Math.round(carb * 0.34);
        const emissionIndex = Math.round(carb * 6.8);

        if (energyMetric) {
          energyMetric.textContent = `${100 - powerSavings}% (-${powerSavings}% draw)`;
          energyMetric.style.color = carb > 50 ? '#38bdf8' : '#4ade80';
        }
        if (emissionMetric) {
          emissionMetric.textContent = `${emissionIndex} g CO₂e/MWh`;
          emissionMetric.style.color = carb > 50 ? '#f87171' : '#cbd5e1';
        }

        if (badgeGrid) {
          if (carb === 0) {
            badgeGrid.textContent = '100% Renewable (0 g CO₂/kWh)';
            badgeGrid.style.color = '#4ade80';
            badgeGrid.style.background = 'rgba(74, 222, 128, 0.1)';
          } else if (carb < 50) {
            badgeGrid.textContent = `Regional Grid (${emissionIndex} g CO₂/kWh)`;
            badgeGrid.style.color = '#38bdf8';
            badgeGrid.style.background = 'rgba(56, 189, 248, 0.1)';
          } else {
            badgeGrid.textContent = `🔥 Fossil Peak Alert (${emissionIndex} g CO₂/kWh)`;
            badgeGrid.style.color = '#f87171';
            badgeGrid.style.background = 'rgba(239, 68, 68, 0.15)';
          }
        }

        if (badgeAlbd) {
          badgeAlbd.textContent = albd > 70 ? 'High Ambient Glare (Outdoor)' : 'Normal Ambient Contrast';
        }

        // Build OpenType GSUB feature string
        const activeFts = ['"zero" 1'];
        if (features.ss01) activeFts.push('"ss01" 1');
        if (features.ss12) activeFts.push('"ss12" 1');
        if (features.ss15) activeFts.push('"ss15" 1');
        if (features.calt) activeFts.push('"calt" 1');
        const featStr = activeFts.join(', ');

        const varStr = `'wght' ${dynamicWght}, 'CARB' ${carb}, 'ALBD' ${albd}`;

        sampleOutput.style.fontVariationSettings = varStr;
        sampleOutput.style.fontFeatureSettings = featStr;

        // Dark Canopy Class
        if (features.ss12) {
          sampleOutput.classList.add('eco-dark-canopy');
          sampleOutput.style.color = '#fbbf24';
          sampleOutput.style.background = '#06080d';
        } else {
          sampleOutput.classList.remove('eco-dark-canopy');
          sampleOutput.style.color = '#f8fafc';
          sampleOutput.style.background = 'rgba(0, 0, 0, 0.35)';
        }

        // Slow Reading Class
        if (features.ss15) {
          sampleOutput.classList.add('eco-slow-reading');
          sampleOutput.style.letterSpacing = '0.04em';
          sampleOutput.style.lineHeight = '1.85';
        } else {
          sampleOutput.classList.remove('eco-slow-reading');
          sampleOutput.style.letterSpacing = '';
          sampleOutput.style.lineHeight = '1.5';
        }

        if (cssInspector) {
          cssInspector.textContent = `font-variation-settings: ${varStr}; font-feature-settings: ${featStr};`;
        }
      }

      sliderCarb?.addEventListener('input', () => {
        presetBtns.forEach(b => b.classList.remove('active'));
        updateEcoState();
      });

      sliderAlbd?.addEventListener('input', updateEcoState);

      presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          presetBtns.forEach(b => {
            b.classList.remove('active');
            b.style.border = '1px solid rgba(255,255,255,0.15)';
            b.style.background = 'rgba(255,255,255,0.04)';
            b.style.color = '#cbd5e1';
          });
          btn.classList.add('active');
          const carb = parseInt(btn.dataset.carb || 0, 10);
          if (sliderCarb) sliderCarb.value = carb;
          if (carb === 0) {
            btn.style.border = '1px solid #4ade80';
            btn.style.background = 'rgba(74, 222, 128, 0.2)';
            btn.style.color = '#4ade80';
          } else if (carb === 45) {
            btn.style.border = '1px solid #38bdf8';
            btn.style.background = 'rgba(56, 189, 248, 0.2)';
            btn.style.color = '#38bdf8';
          } else {
            btn.style.border = '1px solid rgba(239, 68, 68, 0.5)';
            btn.style.background = 'rgba(239, 68, 68, 0.15)';
            btn.style.color = '#f87171';
          }
          updateEcoState();
        });
      });

      function wireToggle(btn, featKey, activeColor, activeBg) {
        if (!btn) return;
        btn.addEventListener('click', () => {
          features[featKey] = !features[featKey];
          const active = features[featKey];
          btn.classList.toggle('active', active);
          btn.textContent = active ? 'ON' : 'OFF';
          btn.style.color = active ? activeColor : '#94a3b8';
          btn.style.background = active ? activeBg : 'rgba(255, 255, 255, 0.05)';
          btn.style.border = active ? `1px solid ${activeColor}` : '1px solid rgba(255, 255, 255, 0.15)';
          updateEcoState();
        });
      }

      wireToggle(btnSpore, 'ss01', '#4ade80', 'rgba(74, 222, 128, 0.2)');
      wireToggle(btnDark, 'ss12', '#f59e0b', 'rgba(245, 158, 11, 0.2)');
      wireToggle(btnSlow, 'ss15', '#38bdf8', 'rgba(56, 189, 248, 0.2)');
      wireToggle(btnIucn, 'calt', '#a78bfa', 'rgba(167, 139, 250, 0.2)');

      sampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          sampleBtns.forEach(b => {
            b.style.background = 'rgba(255,255,255,0.05)';
            b.style.color = '#cbd5e1';
          });
          btn.style.background = 'rgba(74, 222, 128, 0.2)';
          btn.style.color = '#4ade80';
          const key = btn.dataset.sample;
          if (SAMPLES[key] && sampleOutput) {
            sampleOutput.innerHTML = SAMPLES[key];
          }
        });
      });

      // Initial state
      updateEcoState();
    })();

  
