# Google Bug Hunters (VRP) & Google Fonts Upstream Technical Brief

**Document ID**: `PG-VRP-BRIEF-2026`  
**Author**: Phil Gear (The PocketGull Project Authors / GearArts)  
**Repository**: `https://github.com/pocketgull-app/pocketgull-font`  
**Reference Commit**: `c4196d3e`  
**Target Portals**:
1. **Google Bug Hunters / Chrome & OSS VRP**: [https://bughunters.google.com/report](https://bughunters.google.com/report)
2. **Google Fonts Upstream (`google/fonts` / `fontspector`)**: [https://github.com/google/fonts](https://github.com/google/fonts)

---

## Executive Summary (Copy-Paste Title & Abstract)

**Title**:  
`Font-Fallback Spoofing Bypass ("The Invisible Fallback Trap") for Trojan Source BiDi (CVE-2021-42574) & Blank Fillers in Developer/Clinical Monospace Fonts + OS/2 Bit 57 PUA Eviction`

**Abstract**:  
When a developer or clinical monospace font (such as fonts served via Google Fonts or bundled in Chromium/Electron IDEs) omits explicit glyph mappings for **Bidirectional (BiDi) Override control characters** (`U+202A`–`U+202E`, `U+2066`–`U+2069`, `U+061C`), **Zero-Width spoofers** (`U+200B`–`U+200D`, `U+2060`, `U+FEFF`), or **Hangul/Mongolian Blank Fillers** (`U+115F`, `U+1160`, `U+180E`, `U+3164`, `U+FFA0`), the OS/browser text-shaping engine (Windows DirectWrite, Chromium Blink/Skia, HarfBuzz) triggers **silent system font fallback** (`Segoe UI`, `Arial`, `Malgun Gothic`). Because those system fallback fonts map these codepoints to **0-contour invisible whitespace**, stripping dangerous codepoints from a developer font *fails* to block spoofing and instead enables silent Trojan Source (`CVE-2021-42574`) and identifier homograph attacks in terminals, web code viewers, and clinical EHRs.

---

## Finding 1: The Invisible Fallback Trap (CVE-2021-42574 & Blank Filler Bypass)

### 1.1 Vulnerability Mechanism
1. A developer or clinician configures a trusted monospace font (`font-family: 'Developer Mono', monospace;`) in a Chromium-based IDE, web terminal, or EHR dosage viewer.
2. An attacker injects a Trojan Source BiDi override (`U+202E` `RIGHT-TO-LEFT OVERRIDE`) or a Hangul Filler (`U+3164` `HANGUL CAEUM`) into a command string, pull request diff, or medication order.
3. Because the primary monospace font does not contain `U+202E` or `U+3164` in its `cmap` table, Chromium/DirectWrite walks the fallback chain to the OS system font (`Segoe UI` / `Malgun Gothic`), which renders the character as **100% invisible** (zero contours), hiding the payload from human visual review.

### 1.2 Minimal 3-Line Proof of Concept (HTML / Chromium / DirectWrite)
Save as `poc_fallback_trap.html` and open locally in any Chromium browser or Electron shell:
```html
<!doctype html>
<pre style="font-family: Consolas, monospace; font-size: 20px;">
  1. Trojan Source BiDi (U+202E): access_level = "user&#x202E; &#x2066;// Check if admin&#x2069; &#x2066;"
  2. Hangul Blank Spoof (U+3164): sudo&#x3164;rm -rf /
  3. Zero-Width Spoof   (U+200B):500&#x200B;mg Epinephrine
</pre>
```
* **Observed Behavior with Standard Monospace Fonts**: Because `Consolas` / standard monospace fonts omit `U+202E`, `U+3164`, and `U+200B`, DirectWrite falls back to `Segoe UI` / `Malgun Gothic` and renders the injected characters invisibly.
* **Observed Behavior with PocketGull v3.1.0 (`uni202E.guard`)**: PocketGull actively captures all 22 spoofing codepoints in its Format 4 and Format 12 `cmap` subtables and maps them to `uni202E.guard`—a high-contrast, 600-UPM **`[!]` Warning Pill Badge**—preventing OS fallback and immediately exposing the hidden characters.

### 1.3 Proposed Upstream Remediation for Google Fonts & `fontspector`
We propose adding an advisory check to **Google Fonts (`fontbakery` / `fontspector`)** for `MONOSPACE` families (`OS/2.panose.bProportion == 9` / `post.isFixedPitch == 1`):
- Warn when a developer/monospace font leaves Trojan Source BiDi (`U+202A`–`U+202E`, `U+2066`–`U+2069`) or blank fillers (`U+3164`, `U+FFA0`) unmapped (triggering invisible OS fallback), or recommend mapping them to a visible non-empty warning glyph (`numberOfContours > 0`).

---

## Finding 2: DirectWrite / Chromium `OS/2.ulUnicodeRange2` Bit 57 PUA Eviction

### 2.1 Technical Mechanism
When a TrueType/OpenType font includes Private Use Area (PUA) glyphs (`U+E000`–`U+F8FF`, such as Powerline terminal symbols `U+E0A0`–`U+E0B7`) in its `cmap` and `glyf` tables, but leaves **Bit 25 of `OS/2.ulUnicodeRange2` (overall Bit 57: Plane 0 Private Use Area)** unset (`0`), Windows DirectWrite and Chromium font-fallback scanners skip the font when resolving PUA codepoints in secondary fallback chains, rendering `.notdef` tofu boxes (`□`) even though valid contours exist in `glyf`.

### 2.2 Remediation Implemented in PocketGull (`c4196d3e`)
1. Explicitly set `OS/2.ulUnicodeRange2 |= (1 << 25)` (Bit 57: Plane 0 PUA), `Bit 5` (Misc. Technical `U+2300`–`U+23FF`), and `Bit 13` (Geometric Shapes `U+25A0`–`U+25FF`).
2. Dual-mapped all Powerline PUA symbols (`U+E0A0`–`U+E0B7`) to their **Official Unicode Standard** counterparts (`U+2387` `⎇`, `U+26BF` `⚿`, `U+25B6` `▶`, `U+25B7` `▷`, `U+25C0` `◀`, `U+25C1` `◁`, `U+25D7` `◗`, `U+25D6` `◖`) so modern applications can migrate off Private Use Area hacks onto standard Unicode codepoints.

---

## Reference Links for Submission
* **Specification**: `https://github.com/pocketgull-app/pocketgull-font/blob/main/standards/UNICODE_SECURITY_AND_PUA_SPECIFICATION.md`
* **Synthesizer Implementation**: `https://github.com/pocketgull-app/pocketgull-font/blob/main/scripts/synthesize_clinical_terminal_glyphs.py`
* **Security Policy**: `https://github.com/pocketgull-app/pocketgull-font/blob/main/SECURITY.md`
