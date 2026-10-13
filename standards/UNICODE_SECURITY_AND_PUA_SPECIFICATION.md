# PocketGull Unicode Security, PUA & Anti-Spoofing Specification (UTR #36 / CVE-2021-42574)

**Document ID**: `PG-SEC-UNICODE-2026`  
**Status**: Active Foundry Invariant (v3.1.0)  
**Compliance**: Unicode Technical Report #36 (Unicode Security Considerations), Unicode Technical Standard #39 (Unicode Security Mechanisms), CVE-2021-42574 (Trojan Source), W3C OpenType Sanitizer (OTS)

---

## 1. Why Font-Level Cybersecurity Matters

Most developers, clinicians, and everyday users assume a font is passive artwork. In reality, modern text-rendering engines (Windows DirectWrite, Chromium Blink/Skia, macOS CoreText, Linux HarfBuzz) rely on a font's `cmap` (character map) and `OS/2` Unicode range bitmasks to decide how to display or hide characters.

Two major cybersecurity failure modes occur in standard system fonts:

1. **The Invisible Fallback Trap (CVE-2021-42574 "Trojan Source")**:
   - Attackers inject invisible **Bidirectional (BiDi) Override** characters (`U+202E` `RLO`, `U+2066` `LRI`) or **Zero-Width / Blank Spoofers** (`U+200B` `ZWSP`, `U+3164` `Hangul Filler`) into source code, terminal commands, URLs, or electronic health record (EHR) drug dosages.
   - If a developer font simply *deletes* these codepoints from its `cmap`, the OS font-fallback engine silently hands the character over to a system font (`Segoe UI`, `Arial`), which renders it as **0-pixel invisible whitespace**—allowing the attack to succeed undetected.
2. **The PUA Bitmask Blindspot (`OS/2.ulUnicodeRange2` Bit 57)**:
   - Developer tools (Powerline, Starship, Oh My Posh, VS Code, Antigravity) use Private Use Area (PUA) codepoints (`U+E0A0`–`U+E0B7`) for status bars and Git branch telemetry.
   - If a font includes PUA contours in `glyf` and `cmap` but forgets to set **Bit 25 of `OS/2.ulUnicodeRange2` (overall Bit 57: Plane 0 Private Use Area)**, DirectWrite and Chromium skip the font during fallback scanning and render broken tofu boxes (`□`).

---

## 2. The Three-Layer PocketGull Defense Architecture

### Layer 1: Active Capture & Exposure of Trojan Source Codepoints (`uni202E.guard`)
Instead of leaving dangerous control characters unmapped (which triggers invisible OS fallback) or mapping them to blank space, **PocketGull actively captures all 22 high-risk spoofing codepoints** and maps them to a high-contrast, 600-UPM **Warning Pill Badge (`[!]`)**:

| Threat Category | Captured Codepoints | Standard Name | PocketGull Rendering |
| :--- | :--- | :--- | :--- |
| **Trojan Source BiDi Overrides** *(CVE-2021-42574)* | `U+202A`, `U+202B`, `U+202C`, `U+202D`, `U+202E`<br>`U+2066`, `U+2067`, `U+2068`, `U+2069`<br>`U+200E`, `U+200F`, `U+061C` | `LRE`, `RLE`, `PDF`, `LRO`, `RLO`<br>`LRI`, `RLI`, `FSI`, `PDI`<br>`LRM`, `RLM`, `ALM` | **Visible 600-UPM Warning Badge (`[!]`)** — Impossible to hide in code or terminal prompts. |
| **Zero-Width Identifier Spoofers** | `U+200B`, `U+200C`, `U+200D`, `U+2060`, `U+FEFF` | `ZWSP`, `ZWNJ`, `ZWJ`, `Word Joiner`, `BOM` | **Visible 600-UPM Warning Badge (`[!]`)** — Prevents hidden characters inside variable names or commands. |
| **Invisible Blank Fillers** *(Filename / Auth Bypass)* | `U+115F`, `U+1160`, `U+180E`, `U+3164`, `U+FFA0` | Hangul Choseong/Jungseong/Caeum Fillers, Mongolian Vowel Separator | **Visible 600-UPM Warning Badge (`[!]`)** — Eliminates fake-space spoofing. |

---

### Layer 2: Dual-Mapped PUA & Official Unicode Standard Telemetry Symbols
To support legacy developer tools while guiding the ecosystem toward official, non-private Unicode standards, PocketGull maps every status-bar symbol to **both** its de-facto Powerline PUA codepoint and its **Official Unicode Standard** counterpart:

| Visual Symbol | De-Facto Powerline / Nerd Font PUA | Official Unicode Standard Codepoint | Block & OS/2 Bitmask |
| :--- | :--- | :--- | :--- |
| **Git Branch / Alternative Key** | `U+E0A0` (``), `U+F418`, `U+F126`, `U+E725` | **`U+2387` (`⎇`)** & **`U+2397` (`⎗`)** | Misc. Technical (`ulUnicodeRange2` Bit 5) |
| **Line / Column Number (`LN`)** | `U+E0A1` (``), `U+E0A3` (``) | Standard ASCII `Ln` / `Col` | Basic Latin + PUA (`ulUnicodeRange2` Bit 25) |
| **Read-Only Padlock** | `U+E0A2` (``) | **`U+26BF` (`⚿`)** & **`U+1F512` (`🔒`)** | Misc. Symbols (`ulUnicodeRange2` Bit 25) |
| **Right Solid Chevron** | `U+E0B0` (``) | **`U+25B6` (`▶`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Right Thin Chevron** | `U+E0B1` (``) | **`U+25B7` (`▷`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Solid Chevron** | `U+E0B2` (``) | **`U+25C0` (`◀`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Thin Chevron** | `U+E0B3` (``) | **`U+25C1` (`◁`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Right Rounded Pill Cap** | `U+E0B4` (``), `U+E0B5` (``) | **`U+25D7` (`◗`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Rounded Pill Cap** | `U+E0B6` (``), `U+E0B7` (``) | **`U+25D6` (`◖`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |

---

### Layer 3: Binary Memory Safety (W3C OTS & DirectWrite Invariants)
Every synthesized glyph in PocketGull strictly satisfies:
1. **2-Byte Word Alignment (`loca[i] % 2 == 0`)**: Prevents unaligned memory reads in Windows `fontdrvhost.exe` and Chromium OTS.
2. **Reserved Bit-7 Flag Masking (`flag & 0x3F`)**: Guarantees zero illegal TrueType point flags.
3. **Zero Duplicate Nodes**: Eliminates division-by-zero rasterizer hazards in FreeType and DirectWrite.

---

## 4. Google & Alphabet Vulnerability Reward Program (VRP) Rules & Researcher Safe Harbor

Because PocketGull is engineered for upstream **Google Fonts (`google/fonts`)** onboarding and renders inside **Chromium (Blink / Skia / HarfBuzz / W3C OTS)**, **Android**, and **Antigravity**, our security research and vulnerability handling align with the official **[Google and Alphabet Vulnerability Reward Program (VRP) Rules](https://bughunters.google.com/about/rules/google-friends/google-and-alphabet-vulnerability-reward-program-vrp-rules)**:

### 4.1 Rules of Engagement for Security Researchers (VRP Alignment)
1. **Test Only Against Your Own Local / Isolated Environments**:
   - Researchers testing font-parsing edge cases, SFNT table fuzzing, or Unicode BiDi spoofing (`CVE-2021-42574`) must execute tests exclusively on their own local accounts, air-gapped containers, or local specimen instances (`http://pocketgull.localhost:8770`).
   - Never target, disrupt, or attempt to access another user's session, clinical workstation, or production CDN traffic.
2. **Zero Disruption / Zero DoS / Zero Social Engineering**:
   - Prohibited actions include Denial of Service (DoS) against font delivery endpoints, automated high-volume traffic flooding, spam, or phishing/social-engineering using homograph domains.
3. **Valid Attack Scenario Requirement**:
   - Every security report must demonstrate a concrete, reproducible attack scenario (e.g., an SFNT table out-of-bounds read in OTS/FreeType/DirectWrite, a bypass of `uni202E.guard` BiDi capture, or a DOM XSS vector in interactive specimen tooling).

### 4.2 Coordinated Disclosure Channels (PocketGull vs. Upstream Google VRP)
Depending on where a discovered vulnerability resides, researchers should route reports as follows:

| Vulnerability Target | Primary Disclosure Channel | Reference / Portal |
| :--- | :--- | :--- |
| **PocketGull Font Binaries (`.ttf`, `.woff2`), Dart Foundry Toolchain, or Specimen Web App** | **PocketGull Private Security Advisory** *(or `dpo@pocketgull.app`)* | [GitHub Security Advisories](https://github.com/pocketgull-app/pocketgull-font/security/advisories/new) & [SECURITY.md](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/SECURITY.md) |
| **Google Fonts Upstream Infrastructure, `fontbakery`, or Google Hosted Webfont APIs (`fonts.googleapis.com`)** | **Google and Alphabet VRP** | [Google Bug Hunters VRP Rules](https://bughunters.google.com/about/rules/google-friends/google-and-alphabet-vulnerability-reward-program-vrp-rules) |
| **Chromium Blink, Skia, HarfBuzz, FreeType, or W3C OpenType Sanitizer (OTS)** | **Chrome VRP / Google OSS VRP** | [bughunters.google.com](https://bughunters.google.com/) |

