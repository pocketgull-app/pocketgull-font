# PocketGull Unicode Security, PUA & Anti-Spoofing Specification (UTR #36 / CVE-2021-42574)

**Document ID**: `PG-SEC-UNICODE-2026`  
**Status**: Active Foundry Invariant (v3.1.0)  
**Compliance**: Unicode Technical Report #36 (Unicode Security Considerations), Unicode Technical Standard #39 (Unicode Security Mechanisms), CVE-2021-42574 (Trojan Source), W3C OpenType Sanitizer (OTS)

---

## 1. Why Font-Level & Context-Aware Unicode Cybersecurity Matters

Most developers, clinicians, and everyday users assume a font is passive artwork. In reality, modern text-rendering engines (Windows DirectWrite, Chromium Blink/Skia, macOS CoreText, Linux HarfBuzz) and AI/MCP pipelines rely on a font's `cmap` (character map), `OS/2` Unicode range bitmasks, and context-aware codepoint inspection to decide how to display or hide characters.

Three major cybersecurity failure modes occur in standard fonts and naive scanners:

1. **The Invisible Fallback Trap & Emoji Smuggling (`CVE-2021-42574`, Variation Selectors Supplement, & Tag Payloads)**:
   - **Trojan Source (`CVE-2021-42574`)**: Attackers inject invisible **Bidirectional (BiDi) Override** characters (`U+202E` `RLO`, `U+2066` `LRI`) or **Fake-Space Fillers** (`U+3164` `Hangul Filler`) into source code, terminal commands, URLs, or electronic health record (EHR) drug dosages.
   - **Emoji Smuggling & Steganographic Prompt Injection**: Attackers encode arbitrary hidden bytes or LLM/MCP prompt-injection instructions into **Variation Selectors Supplement (`U+E0100`–`U+E01EF`, VS17–VS256)**, **Detached Unicode Tags (`U+E0001`, `U+E0020`–`U+E007E`)**, or **Invisible Math Operators (`U+2061`–`U+2064`)** attached to an innocent character or emoji (`🔥`).
   - **Why Deleting from `cmap` Fails**: If a developer font simply *deletes* these codepoints from its `cmap`, the OS font-fallback engine silently hands the character over to a system font (`Segoe UI`, `Arial`), which renders it as **0-pixel invisible whitespace**—allowing the attack to succeed in plain sight.
2. **The Naive Range-Block False-Positive Trap ("Crying Wolf" on Sovereign Scripts & Emoji)**:
   - As demonstrated in `agentmetry` PR #182 (`fix(mcp): the concealed-text check fired on flags, emoji and Persian`) and `guillaumemeyer/watermarks-remover` (Layer A Context-Aware Inspection), **blanket range-based blocking or visible-badge flagging across all zero-width/tag characters breaks real-world text**:
     - **Persian, Arabic, Mongolian & Indic (`U+200C` `ZWNJ`, `U+061C` `ALM`, `U+180E` `MVS`)**: `U+200C` is required Persian orthography (e.g. *می‌روم* in the *Rubáiyát* observatory), not decoration. Rendering a visible `[!]` badge on `U+200C` corrupts legitimate non-Latin text.
     - **Family & Profession Emoji (`U+200D` `ZWJ`, `U+FE0E`/`U+FE0F`)**: Standard emoji sequences (`👨‍👩‍👧`, `🏳️‍🌈`) require `U+200D` and Variation Selector-16 (`U+FE0F`).
     - **Subdivision Flags (`U+E0000`–`U+E007F` inside `U+1F3F4 ... U+E007F`)**: Scotland (`🏴󠁧󠁢󠁳󠁣󠁴󠁿`), Wales (`🏴󠁧󠁢󠁷󠁬󠁳󠁿`), and England (`🏴󠁧󠁢󠁥󠁮󠁧󠁿`) flags use `U+1F3F4` followed by tag letters and `U+E007F`.
   - **The PocketGull Rule**: A defense that fires false positives on Persian poetry or family emoji is one an operator immediately disables—leaving nothing protected.
3. **The PUA Bitmask Blindspot (`OS/2.ulUnicodeRange2` Bit 57)**:
   - Developer tools (Powerline, Starship, Oh My Posh, VS Code, Antigravity) use Private Use Area (PUA) codepoints (`U+E0A0`–`U+E0B7`) for status bars and Git branch telemetry.
   - If a font includes PUA contours in `glyf` and `cmap` but forgets to set **Bit 25 of `OS/2.ulUnicodeRange2` (overall Bit 57: Plane 0 Private Use Area)**, DirectWrite and Chromium skip the font during fallback scanning and render broken tofu boxes (`□`).

---

## 2. The Three-Layer PocketGull Defense Architecture

### Layer 1: Active Capture of Spoofing & Smuggling Codepoints (`uni202E.guard`) with Zero Multilingual False Positives
Instead of leaving dangerous control characters unmapped (which triggers invisible OS fallback) or crying wolf on legitimate non-Latin orthographies and emoji, **PocketGull separates unconditional spoofing/smuggling vectors from context-dependent script joiners**:

| Category | Codepoints | Standard Name / Vector | PocketGull Font Rendering & Scanner Posture |
| :--- | :--- | :--- | :--- |
| **1. Trojan Source Explicit BiDi Overrides & Isolates** *(CVE-2021-42574)* | `U+202A`–`U+202E`,<br>`U+2066`–`U+2069` | `LRE`, `RLE`, `PDF`, `LRO`, `RLO`,<br>`LRI`, `RLI`, `FSI`, `PDI` | **Visible 600-UPM Warning Badge (`[!]`)** — Impossible to hide in source code or terminal prompts (host HarfBuzz terminals should pass `HB_BUFFER_FLAG_PRESERVE_DEFAULT_IGNORABLES`). |
| **2. Fake-Space Filename & CLI Spoofers** | `U+115F`, `U+1160`, `U+3164`, `U+FFA0` | Hangul Choseong/Jungseong/Caeum & Halfwidth Fillers (`Lo` letters) | **Visible 600-UPM Warning Badge (`[!]`)** — Unconditionally caught across all shapers; eliminates fake-space authentication and CLI argument spoofing. |
| **3. Emoji Smuggling, ASCII Tag Prompt Injection & Invisible Math** | `U+2061`–`U+2064`,<br>`U+E0000`–`U+E007F`,<br>`U+E0100`–`U+E01EF` | Invisible Math, **Unicode ASCII Tags**, & **Variation Selectors Supplement (`VS17`–`VS256`)** | **Visible 600-UPM Warning Badge (`[!]`)** — In `PocketGullMono` & `PocketGull-Numerics`, `U+E0000`–`U+E007F` routes unconditionally to `uni202E.guard` (`[!]`). In proportional cuts, `U+E0000`–`U+E007F` maps to `uni202E.guard` (`[!]`) by default in `cmap` with a contextual `GSUB` rule substituting `uni200C.joiner` only after `U+1F3F4` (`Waving Black Flag`). |
| **4. Context-Dependent Orthographic Joiners & Presentation Selectors** *(Zero False Positives)* | `U+00AD`, `U+061C`, `U+180E`, `U+200B`–`U+200F`, `U+2060`, `U+FE00`–`U+FE0F`, `U+FEFF` | `SHY`, `ALM`, `MVS`, `ZWSP`, `ZWNJ`, `ZWJ`, `LRM`, `RLM`, `WJ`, `VS1`–`VS16`, `BOM` | **Clean Non-Marking Control Glyph (`uni200C.joiner`)** at the font layer so Persian (*Rubáiyát* `ZWNJ`), Arabic (`ALM`), Mongolian (`MVS`), and family emoji (`ZWJ`/`VS16`) never break; paired with **Contextual AST/MCP Inspection**. |

---

### Layer 2: Dual-Mapped PUA & Official Unicode Standard Telemetry Symbols
To support legacy developer tools while guiding the ecosystem toward official, non-private Unicode standards, PocketGull maps every status-bar symbol to **both** its de-facto Powerline PUA codepoint and its **Official Unicode Standard** counterpart:

| Visual Symbol | De-Facto Powerline / Nerd Font PUA | Official Unicode Standard Codepoint | Block & OS/2 Bitmask |
| :--- | :--- | :--- | :--- |
| **Git Branch / Alternative Key** | `U+E0A0` (``), `U+F418`, `U+F126`, `U+E725` | **`U+2387` (`⎇`)** & **`U+2397` (`⎗`)** | Misc. Technical (`ulUnicodeRange2` Bit 5) |
| **Line / Column Number (`LN`)** | `U+E0A1` (``), `U+E0A3` (``) | Standard ASCII `Ln` / `Col` | Basic Latin + PUA (`ulUnicodeRange2` Bit 25) |
| **Read-Only Padlock** | `U+E0A2` (``) | **`U+26BF` (`⚿`)** & **`U+1F512` (`🔒︎`)** | Misc. Symbols (`ulUnicodeRange2` Bit 15 & Bit 25) |
| **Right Solid Chevron** | `U+E0B0` (``) | **`U+25B6` (`▶︎`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Right Thin Chevron** | `U+E0B1` (``) | **`U+25B7` (`▷`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Solid Chevron** | `U+E0B2` (``) | **`U+25C0` (`◀︎`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Thin Chevron** | `U+E0B3` (``) | **`U+25C1` (`◁`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Right Rounded Pill Cap** | `U+E0B4` (``), `U+E0B5` (``) | **`U+25D7` (`◗`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |
| **Left Rounded Pill Cap** | `U+E0B6` (``), `U+E0B7` (``) | **`U+25D6` (`◖`)** | Geometric Shapes (`ulUnicodeRange2` Bit 13) |

---

### Layer 3: Binary Memory Safety (W3C OTS & DirectWrite Invariants)
Every synthesized glyph in PocketGull strictly satisfies:
1. **2-Byte Word Alignment (`loca[i] % 2 == 0`) & 4-Byte SFNT Table Alignment (`offset & 3 == 0`)**: Prevents unaligned memory reads in Windows `fontdrvhost.exe` and Chromium OTS.
2. **Dual Bit-6 & Bit-7 Flag Masking (`flag & 0x3F`)**: Masks off both Bit 7 (`0x80` Reserved) and Bit 6 (`0x40` `OVERLAP_SIMPLE`) once overlaps are removed at build time, ensuring pre-2017 rasterizer safety and 0 OTS violations.
3. **Zero Duplicate Nodes**: Eliminates division-by-zero rasterizer hazards in FreeType and DirectWrite.

---

## 3. Google Open Source (OSS VRP) Alignment & Researcher Safe Harbor

Because PocketGull is engineered for upstream **Google Fonts (`google/fonts`)** onboarding and renders inside **Chromium (Blink / Skia / HarfBuzz / W3C OTS)**, **Android**, and **Antigravity**, our security research and vulnerability handling align with the official **[Google and Alphabet Vulnerability Reward Program (VRP) Rules](https://bughunters.google.com/about/rules/google-friends/google-and-alphabet-vulnerability-reward-program-vrp-rules)**:

### 3.1 Rules of Engagement for Security Researchers
1. **Test Only Against Your Own Local / Isolated Environments**:
   - Researchers testing font-parsing edge cases, SFNT table fuzzing, or Unicode BiDi spoofing (`CVE-2021-42574`) must execute tests exclusively on their own local accounts, air-gapped containers, or local specimen instances (`http://pocketgull.localhost:8770`).
   - Never target, disrupt, or attempt to access another user's session, clinical workstation, or production CDN traffic.
2. **Zero Disruption / Zero DoS / Zero Social Engineering**:
   - Prohibited actions include Denial of Service (DoS) against font delivery endpoints, automated high-volume traffic flooding, spam, or phishing/social-engineering using homograph domains.
3. **Valid Attack Scenario vs. W3C Font-Fallback Design**:
   - Standard CSS/OS font fallback is intended W3C behavior rather than an exploitable software vulnerability on sandbox domains (`*.googleapis.com`). Font-level anti-spoofing improvements (`uni202E.guard`) should be submitted as upstream engineering proposals to `googlefonts/fontspector` or `google/fonts`, while memory-corruption or parser exploits in OTS/HarfBuzz/FreeType should be reported via Google OSS VRP.

### 3.2 Coordinated Disclosure Channels

| Target Component | Primary Channel | Reference / Portal |
| :--- | :--- | :--- |
| **PocketGull Font Binaries (`.ttf`, `.woff2`), Dart Foundry Toolchain, or Specimen Web App** | **PocketGull Private Security Advisory** *(or `dpo@pocketgull.app`)* | [GitHub Security Advisories](https://github.com/pocketgull-app/pocketgull-font/security/advisories/new) & [SECURITY.md](../SECURITY.md) |
| **Upstream Monospace QA Checks (`google/fonts`, `googlefonts/fontspector`, `fontbakery`)** | **Google Fonts Upstream GitHub** | [googlefonts/fontspector](https://github.com/googlefonts/fontspector/issues) & [google/fonts](https://github.com/google/fonts/issues) |
| **Parser Memory Safety in Chromium Blink, Skia, HarfBuzz, FreeType, or W3C OTS** | **Chrome VRP / Google OSS VRP** | [bughunters.google.com](https://bughunters.google.com/) |

---

## 4. Field Guide: What PocketGull Glyphs Mean on Your Machine & How to Verify Font Safety

When you install PocketGull on a workstation, clinical terminal, or legacy device, the font uses distinct visual shapes to protect you from hidden text attacks and reading errors without disrupting normal work.

### 4.1 What the Glyphs Mean When Installed (`Field Guide for Users`)

| Glyph / Visual Shape | Codepoints / OpenType Feature | What It Means on Your Screen | Recommended Action |
| :--- | :--- | :--- | :--- |
| **`[!]` Warning Badge**<br>*(`uni202E.guard`)* | `U+202A`–`U+202E`, `U+2066`–`U+2069` *(BiDi)*,<br>`U+115F`, `U+1160`, `U+3164`, `U+FFA0` *(Fake Spaces)*,<br>`U+2061`–`U+2064`, `U+E0100`–`U+E01EF` *(`VS17`–`VS256`)* | **Hidden Spoofing or Smuggling Character Detected.** Reveals an invisible character trying to reverse text direction (*Trojan Source* `CVE-2021-42574`), fake a space in a CLI command/filename, or smuggle hidden LLM prompt bytes. | **Pause and inspect.** Do not run the command or approve the record until the hidden character is removed or re-typed cleanly. |
| **Clean Non-Marking Join**<br>*(`uni200C.joiner`)* | `U+200C` (`ZWNJ`), `U+200D` (`ZWJ`), `U+061C` (`ALM`), `U+180E` (`MVS`), `U+FE00`–`U+FE0F`, `U+E0000`–`U+E007F` | **Legitimate Multilingual Joiner or Emoji Selector.** Required for natural shaping in Persian (*Rubáiyát*), Arabic, Mongolian, family emoji (`👨‍👩‍👧`), and regional subdivision flags (`🏴󠁧󠁢󠁳󠁣󠁴󠁿`). | **No action needed in prose.** Renders cleanly with zero false-positive `[!]` badges so non-Latin scripts and emoji work naturally. |
| **`0̸` Slashed Zero, Curved `l`, Serifed `I`, Crossbar `Ƶ`** | ASCII `0` (`zero`/`cv08`), `l` (`cv05`), `I` (`ss02`), `Z` (`cv11`) | **ISMP Clinical Disambiguation.** Built-in optical distinction so `0` never looks like `O`, `1` never looks like `l` or `I`, and `2` never looks like `Z` (`500 mg`, `IL-6`, `IgA`). | **Normal reading.** Engineered to prevent human transcription and dosage misreads on both modern and aging low-contrast displays. |
| **`⎇` Branch, `⚿` Padlock, `▶︎` Chevron, `LN` Line** | Official `U+2387`, `U+26BF`, `U+25B6`–`U+25D7` + Dual PUA `U+E0A0`–`U+E0B7` | **Developer & Terminal HUD Telemetry.** Indicates an active Git branch (`⎇`), a read-only/locked file (`⚿`), or prompt segment dividers in VS Code, Windows Terminal, and Starship. | **Normal HUD status.** Dual-mapped so both legacy Powerline tools and modern Unicode terminals render crisp icons instead of broken boxes. |
| **`.notdef` Box (`□`)** | `GID 0` *(Unmapped Codepoint)* | **Unsupported Character or Encoding Mismatch.** The text contains a codepoint outside the installed font subset or a corrupted non-UTF-8 byte sequence. | **Check encoding or load subset.** Verify the file is `UTF-8` or enable the matching PocketGull specialist pack (`Math`, `Chem`, `ASL`). |

---

### 4.2 How Anyone Can Ensure a Font Is Safe (Modern & Legacy Hardware Checklist)

Learned from historical font-layer vulnerabilities (**Stuxnet** `CVE-2010-2743` in `win32k.sys` and **Pegasus / FORCEDENTRY** `CVE-2021-30860`), use this 6-point checklist to verify that a font is safe for both modern workstations and older hardware:

| Safety Check | Legacy Danger (What Used to Break) | What Safe Fonts (PocketGull) Do | How to Verify Locally |
| :--- | :--- | :--- | :--- |
| **1. Zero Bytecode VM (`instructionLength = 0`)** | Legacy TrueType hinting tables (`fpgm`, `prep`, `cvt `) run a stack-based virtual machine inside the OS/printer rasterizer—historically exploited for Ring 0 kernel execution. | Omit `fpgm`/`prep` VM bytecode and set `instructionLength = 0` on every glyph, using declarative `gasp` smoothing (`0x0006`) instead. | `dart run tool/pocketgull_foundry.dart audit` |
| **2. 2-Byte Word Alignment (`loca[i] % 2 == 0`)** | Odd-length glyph records in `glyf` cause unaligned memory reads in Windows `fontdrvhost.exe`, legacy printer firmware, and Chromium W3C OTS. | Pad every `glyf` record with `0x00` to an even byte boundary and mask all point flags to `flag & 0x3F` (Bit 7 = `0`). | `dart run tool/pocketgull_foundry.dart audit` |
| **3. Flat Contours & Zero Duplicate Nodes** | Deeply nested composite glyphs (`numberOfContours == -1`) and 0-length segments trigger stack overflows or division-by-zero crashes in older `FreeType` / `CoreText` engines. | Flatten outlines into closed quadratic contours (`numberOfContours > 0`) with `0` duplicate control points and valid bounding boxes (`xMin <= xMax`). | `python sources/validate_fonts.py` |
| **4. Static `.ttf` Fallback for Pre-2017 Hardware** | Shipping *only* a Variable Font (`gvar`/`fvar`) breaks pre-2017 OS engines, Citrix thin clients, and embedded medical monitors that cannot parse `gvar` deltas. | Ship static `.ttf` and `.woff2` binaries (`Fineliner`, `Bold`, `Chiseltip`, `Mono`) alongside `PocketGull-VF` and cascade `.woff2` $\to$ `.ttf` in `fonts.css`. | Check `fonts/ttf/` and `fonts.css` `@font-face` rules |
| **5. Zero DRM Print Locks (`OS/2.fsType = 0x0000`)** | Restrictive `fsType` bits cause legacy hospital PDF archivers and printer spoolers to silently reject or drop embedded fonts when printing charts. | Lock `OS/2.fsType = 0x0000` (*Installable Embedding*) across all styles so legacy printers and PDF tools never block output. | `python sources/validate_fonts.py` |
| **6. Cryptographic SHA-256 & SRI Verification** | Unsigned fonts downloaded over unverified mirrors can be modified in transit. | Verify release binaries against `fonts/SHA256SUMS`, W3C `sha384` hashes (`fonts/sri-hashes.json`), and GitHub Sigstore SLSA attestations. | `sha256sum -c fonts/SHA256SUMS` |
