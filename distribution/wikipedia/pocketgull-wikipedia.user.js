// ==UserScript==
// @name         PocketGull Typography for Wikipedia & Wikimedia
// @namespace    https://pocketgull.app/
// @version      3.1.0
// @description  Brings Louise Sloan 5:1 optotypes, 540 UPM optical volume parity, ISMP clinical disambiguation, and multi-script vertical stabilization to Wikipedia.
// @author       The PocketGull Project Authors
// @match        *://*.wikipedia.org/*
// @match        *://*.wikimedia.org/*
// @match        *://*.wiktionary.org/*
// @match        *://*.wikibooks.org/*
// @match        *://*.wikidata.org/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  const FONT_LINK_ID = 'pocketgull-webfont-link';
  const STYLE_ID = 'pocketgull-wikipedia-engine';

  function injectPocketGull() {
    // 1. Clean up any existing instances (Idempotent)
    document.getElementById(FONT_LINK_ID)?.remove();
    document.getElementById(STYLE_ID)?.remove();

    // 2. Inject PocketGull webfont stylesheet via Wikipedia CSP-whitelisted jsDelivr CDN
    const link = document.createElement('link');
    link.id = FONT_LINK_ID;
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = 'https://cdn.jsdelivr.net/gh/pocketgull-app/pocketgull-font@main/fonts.css';
    (document.head || document.documentElement).appendChild(link);

    // 3. Mount Typography Design Tokens & Multi-Script Stabilization
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      /* ======================================================================
         1. VECTOR 2022 & CODEX CSS DESIGN TOKENS
         Overrides MediaWiki tokens at root level for seamless UI integration
         ====================================================================== */
      :root, html {
        --font-family-sans: 'PocketGull', system-ui, -apple-system, sans-serif !important;
        --font-family-serif: 'PocketGull Serif', 'PocketGull', Georgia, serif !important;
        --font-family-monospace: 'PocketGull Mono', 'Courier New', monospace !important;
        --font-size-browser: 16px;
        --line-height-base: 1.7;
      }

      /* ======================================================================
         2. ENCYCLOPEDIC BODY COPY & OPTICAL VOLUME EQUALIZATION
         size-adjust: 108% lifts 500 UPM x-height to 540 UPM reading standard
         ====================================================================== */
      body, .mw-body, .mw-parser-output, .mw-parser-output p {
        font-family: var(--font-family-sans) !important;
        font-size: 1.05rem !important;
        line-height: 1.72 !important;
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      /* ======================================================================
         3. SECTION HEADINGS & BIONIC ANCHORING
         ====================================================================== */
      h1, h2, h3, h4, h5, h6, .mw-first-heading {
        font-family: var(--font-family-sans) !important;
        font-weight: 700 !important;
        letter-spacing: -0.018em;
      }

      /* ======================================================================
         4. W3C WRITING MODES LEVEL 3: VERTICAL MONGOLIAN INLINE STABILIZATION
         Prevents line-box blowout and leading disruption in running text
         ====================================================================== */
      .font-mong, span[lang="mn-Mong"], [dir="ltr"] > [style*="vertical-lr"] {
        display: inline-block !important;
        font-size: 1.14em !important;
        line-height: 1.0 !important;
        vertical-align: -0.20em !important;
        margin: 0 0.22em !important;
        box-sizing: border-box !important;
      }

      /* ======================================================================
         5. ISMP / FDA CLINICAL LIFE-SAFETY DISAMBIGUATION
         Slashed Zero (cv08), Curved l (cv05), Serifed I (ss02), Slashed Z (cv11)
         ====================================================================== */
      .infobox, .wikitable, .infobox-drug, .drugbox, .medical-table,
      .infobox-medical-condition, .chembox {
        font-family: var(--font-family-sans) !important;
        font-feature-settings: "cv08" 1, "cv05" 1, "ss02" 1, "cv11" 1 !important;
      }

      /* ======================================================================
         6. FIXED-PITCH TELEMETRY & UNICODE TABLES
         ====================================================================== */
      code, pre, .mw-code, .monospaced {
        font-family: var(--font-family-monospace) !important;
        font-feature-settings: "zero" 1 !important;
      }

      /* ======================================================================
         7. PHONETICS (IPA) & SCHOLARLY TRANSLITERATION DIACRITICS
         ====================================================================== */
      .IPA, [title*="International Phonetic Alphabet"], [lang="und-Latn-fonipa"] {
        font-family: 'PocketGull', 'Gentium Plus', serif !important;
        letter-spacing: 0.035em !important;
      }
    `;
    (document.head || document.documentElement).appendChild(style);
  }

  // Execute immediately if DOM is ready, or on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectPocketGull);
  } else {
    injectPocketGull();
  }
})();
