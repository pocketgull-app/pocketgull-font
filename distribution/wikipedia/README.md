# PocketGull Typography for Wikipedia & Wikimedia

**Brings Louise Sloan 5:1 Optotypes, 540 UPM Optical Volume Parity, ISMP Clinical Disambiguation, and Multi-Script Vertical Stabilization to the Free Encyclopedia.**

---

## 🕊️ Overview

Reading Wikipedia shouldn't cause eyestrain or clinical confusion. Wikipedia's default fonts can feel diminutive at small sizes, confuse numbers and letters in medical articles (`0` vs `O`, `1` vs `l`), and struggle with complex scripts like Traditional Mongolian (`writing-mode: vertical-lr`).

This distribution kit integrates the **PocketGull Font Superfamily** into Wikipedia and Wikimedia projects using pure W3C standards and Wikipedia's native Content Security Policy (CSP).

### What PocketGull Upgrades on Wikipedia:
1. **540 UPM Optical Volume Parity (`size-adjust: 108%`)**: Elevates PocketGull's physical 500 UPM x-height to match the generous reading footprint of modern UI fonts (Segoe UI, Roboto, Inter) without manual zoom.
2. **ISMP Life-Critical Clinical Disambiguation**: Enforces slashed zeroes (`0̸`, `cv08`), curved lowercase `l` (`cv05`), serifed capital `I` (`ss02`), and slashed `Z` (`cv11`) across all drug infoboxes and medical tables.
3. **W3C Writing Modes Level 3 for Traditional Mongolian**: Tames the vertical inline script (`ᠮᠣᠩᠭᠣᠯ ᠪᠢᠴᠢᠭ`), seating it stably within English running text without line-box blowout.
4. **SMoE Multi-Script Routing**: Seamlessly routes Latin, Cyrillic, Greek, Braille, Cherokee, Inuktitut, and Mongolian through featherweight Brotli Q11 subsets.

---

## 🚀 Installation Options

### Option 1: Browser UserScript (Tampermonkey / Violentmonkey)
*Works automatically on every Wikipedia and Wikimedia page, even if your IP is blocked from editing.*

1. Install the [Tampermonkey extension](https://www.tampermonkey.net/) (or Violentmonkey) in Chrome, Firefox, Edge, or Brave.
2. Open [`pocketgull-wikipedia.user.js`](pocketgull-wikipedia.user.js) and click **Install**.
3. Visit any Wikipedia article (e.g. [Prednisone](https://en.wikipedia.org/wiki/Prednisone) or [Mongolian script](https://en.wikipedia.org/wiki/Mongolian_script)).

### Option 2: Browser Extension (Stylus UserCSS)
1. Install the [Stylus extension](https://github.com/openstyles/stylus).
2. Click **Write new style**, name it `PocketGull Wikipedia`, and paste the contents of [`pocketgull-wikipedia.css`](pocketgull-wikipedia.css).
3. Click **Save**.

### Option 3: Wikipedia Account UserScript (`Special:MyPage/common.js`)
If your Wikipedia account is in good standing and not under an IP block:
1. Navigate to **`Special:MyPage/common.js`** on English Wikipedia.
2. Add:
   ```javascript
   mw.loader.using(['mediawiki.util'], function () {
     $('head').append('<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/pocketgull-app/pocketgull-font@main/fonts.css">');
     $('head').append('<link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/pocketgull-app/pocketgull-font@main/distribution/wikipedia/pocketgull-wikipedia.css">');
   });
   ```
3. Bypass your cache with `Ctrl + F5` (or `Cmd + Shift + R`).

---

## 🏛️ Upstream Wikimedia Adoption (Universal Language Selector)

For Wikimedia Foundation sysops and Language Engineering:
* **Binary Health**: 100% W3C OTS compliant (`loca[i] % 2 == 0`, bit-7 masked, 0 duplicate nodes).
* **Licensing**: Pure SIL Open Font License 1.1 with **Zero Reserved Font Names (RFN)**.
* **Archival**: CERN Zenodo permanent DOI (`10.5281/zenodo.22309379`).
* **Integration Target**: MediaWiki `UniversalLanguageSelector/data/fontrepo/`.
