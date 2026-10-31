# PocketGull Foundry & Hardware OEM Security Blueprint

**Document ID**: `PG-SEC-OEM-FOUNDRY-2026`  
**Status**: Active Open-Source Reference Standard (v3.2.0)  
**License**: SIL Open Font License 1.1 (Zero Reserved Font Name) / Apache 2.0  
**Related Specifications**: [SECURITY.md](../SECURITY.md) | [UNICODE_SECURITY_AND_PUA_SPECIFICATION.md](UNICODE_SECURITY_AND_PUA_SPECIFICATION.md)

---

## 1. Why This Guide Exists: Lessons from Stuxnet, Pegasus & Legacy Hardware

For decades, software and hardware engineers treated font files (`.ttf`, `.otf`, `.woff2`) as harmless static pictures, while type designers worked in visual curve editors unaware of how OS kernels and embedded firmware parse binary tables. That disconnect produced two systemic failures:

1. **The Kernel, Shaper & Firmware Exploit Surface (`Stuxnet`, `Pegasus`, & Modern 2025–2026 Font CVEs)**:
   - **Stuxnet (`CVE-2010-2743` / MS10-073) & Duqu (`CVE-2011-3402`)**: Exploited the Windows kernel font driver (`win32k.sys`) by feeding malformed TrueType tables and hinting bytecode into a Ring 0 parser.
   - **Pegasus / FORCEDENTRY (`CVE-2021-30860`) & Apple `FontParser` (`CVE-2025-43400`)**: Exploited zero-click background rendering via monochrome glyph/text compression streams (`JBIG2`) and out-of-bounds writes in system font parsers before the user ever opened a message.
   - **FreeType Composite & Variable Font Heap Bugs (`CVE-2025-27363` CISA KEV, `CVE-2026-23865`, `CVE-2026-50811`)**: `CVE-2025-27363` (CVSS 8.1, exploited in the wild on `FreeType <= 2.13.0`) triggered an out-of-bounds heap write via signed-short wraparound in composite/variable subglyph counts (`src/truetype/ttgload.c`), followed by `HVAR`/`VVAR`/`MVAR` variation-store integer overflows (`CVE-2026-23865`, fixed in `2.14.2`) and `ttgxvar.c` design-coordinate out-of-bounds reads (`CVE-2026-50811`, `<= 2.14.3`).
   - **HarfBuzz In-Font WebAssembly (`Wasm`) Shaper Bugs (`CVE-2026-113679`, `CVE-2026-113680`)**: HarfBuzz `8.0.0`–`14.6.0` introduced an experimental `'Wasm'` SFNT table (`0x5761736D`), re-introducing an embedded virtual machine inside fonts that suffered WAMR host-import out-of-bounds writes (`CVE-2026-113679`) and NULL pointer dereferences (`CVE-2026-113680`).
   - **Foundry Build-Chain & Webfont Decoder Bugs (`CVE-2025-66034`, `CVE-2026-111497`)**: Crafted `.designspace` sources in `fontTools.varLib` (`< 4.60.2`) enabled arbitrary file writes and XML injection (`CVE-2025-66034`), while *"Node2Shell"* (`CVE-2026-111497`, `brotli < 1.2.1`) exposed an out-of-bounds write in Brotli decoders handling WOFF2/HTTP streams.
2. **Legacy Hardware & Out-of-Date Font Disruption**:
   - Millions of hospital workstations, ICU telemetry monitors, Citrix thin clients, laser printers, and rural school devices still run 10-to-20-year-old hardware and pre-2017 rasterizers (`GDI`, older `FreeType`).
   - Out-of-date system fonts expose these machines to bytecode VM bugs and clinical `1 / l / I` or `0 / O` misreads, while poorly engineered modern fonts crash legacy devices via unaligned `loca` offsets, variable-only (`gvar`) tables, or over-aggressive zero-width character blocking.

This blueprint provides **copy-pasteable engineering standards** for both **fellow font creators** and **hardware/firmware manufacturers**.

---

## 2. For Fellow Font Creators & Type Foundries: The 6-Step Safe Font Recipe

Any type designer using Glyphs, FontLab, RoboFont, or `fontTools` can adopt PocketGull's open-source security architecture (`SIL OFL 1.1`, zero Reserved Font Name restrictions):

### Step 2.1: Separate Spoofing Guards (`uni202E.guard`) from Legitimate Joiners (`uni200C.joiner`)
* **Never simply delete BiDi overrides from `cmap`**: If a developer or clinical font omits `U+202E` (`RLO`) or `U+3164` (`Hangul Filler`), the OS fallback engine silently renders them using a system font as **0-pixel invisible whitespace**—allowing *Trojan Source* (`CVE-2021-42574`) attacks to succeed unseen.
* **Never flag all zero-width characters with a visible `[!]`**: Flagging `U+200C` (`ZWNJ`) or `U+200D` (`ZWJ`) corrupts legitimate Persian (*Rubáiyát*), Arabic, Indic, family emoji (`👨‍👩‍👧`), and regional subdivision flags (`🏴󠁧󠁢󠁳󠁣󠁴󠁿`).
* **The PocketGull Mapping Pattern** (copyable directly from `sources/PocketGull-Fineliner.ufo`):
  - **Map to `uni202E.guard` (Visible 600-UPM `[!]` Warning Badge)**:
    - `U+202A`–`U+202E` (`LRE`, `RLE`, `PDF`, `LRO`, `RLO`)
    - `U+2066`–`U+2069` (`LRI`, `RLI`, `FSI`, `PDI`)
    - `U+115F`, `U+1160`, `U+3164`, `U+FFA0` (Hangul & Halfwidth Fake-Space Fillers — categorized as `Lo` letters, so `uni202E.guard` catches them unconditionally across all shapers)
    - `U+2061`–`U+2064` (Invisible Math Operators)
    - `U+E0100`–`U+E01EF` (Variation Selectors Supplement `VS17`–`VS256` used in Emoji Smuggling)
    - **`U+E0000`–`U+E007F` (Unicode Tags — Keep the Binary Simple & Inert)**:
      - *In Monospace & Clinical Cuts (`PocketGullMono` / `PocketGull-Numerics`)*: Route `U+E0000`–`U+E007F` unconditionally to **`uni202E.guard` (`[!]`)** in `cmap`. Monochrome code terminals and ICU monitors never render color subdivision flags (`🏴󠁧󠁢󠁳󠁣󠁴󠁿`), so a direct `cmap` entry catches ASCII tag smuggling with zero `GSUB` state-machine complexity.
      - *In Proportional UI Cuts*: Route `U+E0000`–`U+E007F` to `uni200C.joiner` so regional flags continue to work, leaving application-level prompt/input sanitization to the host IDE or linter rather than turning the font's `GSUB` table into a stateful firewall.
  - **Map to `uni200C.joiner` (Clean 0-Width Non-Marking Control Glyph)**:
    - `U+00AD`, `U+061C`, `U+180E`, `U+200B`–`U+200F`, `U+2060`, `U+FE00`–`U+FE0F`, `U+FEFF`
* **Implementer Note for HarfBuzz / GUI Terminal Authors (`Default_Ignorable_Code_Point`)**:
  Full OpenType shapers (`HarfBuzz`, `DirectWrite`, `CoreText`) apply the Unicode Bidirectional Algorithm (UAX #9) at the character-buffer layer and, by default, suppress glyphs for codepoints with the `Default_Ignorable_Code_Point` property (`U+202A`–`U+202E`, `U+2060`–`U+2069`, `U+E0000`–`U+E01EF`) unless the host application passes **`HB_BUFFER_FLAG_PRESERVE_DEFAULT_IGNORABLES`**. GUI terminal and code-editor authors using HarfBuzz should enable `HB_BUFFER_FLAG_PRESERVE_DEFAULT_IGNORABLES` so the font's `[!]` outline (`uni202E.guard`) is never suppressed by the shaper.

### Step 2.2: Omit In-Font Virtual Machines (`fpgm`/`prep`/`cvt ` Bytecode & HarfBuzz `Wasm`)
* Instead of embedding 1980s stack-based TrueType bytecode programs (`fpgm`, `prep`, `cvt `) or experimental HarfBuzz WebAssembly shaper modules (`Wasm`, `0x5761736D` — `CVE-2026-113679` / `CVE-2026-113680`), emit **`instructionLength = 0`** on every glyph, omit all VM tables, and include a declarative **Version 1 `gasp` table** mapping range `0xFFFF` to `0x0006` (`GASP_DOGRAY | GASP_SYMMETRIC_SMOOTHING`).
* This guarantees that even if your font is installed on an unpatched legacy OS, printer, or WAMR-enabled HarfBuzz build, **no in-font virtual machine is ever executed**.

### Step 2.3: Enforce 2-Byte Word Alignment & Dual Bit-6/Bit-7 Flag Masking (`flag & 0x3F`)
* **Word Alignment (`loca[i] % 2 == 0`)**: Pad every glyph record in the `glyf` table with a trailing `0x00` byte if its byte length is odd. Unaligned `loca` offsets trigger memory faults in legacy printer firmware and immediate font rejection in Chromium's W3C OpenType Sanitizer (`OTS`).
* **Dual Bit-6 & Bit-7 Flag Clearing (`flag & 0x3F` vs. `0x7F`)**: In the OpenType `glyf` Simple Glyph Flags specification, **Bit 7 (`0x80`)** is the Reserved bit (must be `0`), and **Bit 6 (`0x40`)** is `OVERLAP_SIMPLE` (introduced in OpenType 1.8). Once contour overlaps are removed at build time, applying **`flag & 0x3F` (`0b00111111`)** clears **both** Bit 7 (`0x80` Reserved) and Bit 6 (`0x40` `OVERLAP_SIMPLE`). This prevents pre-2017 rasterizers from choking on OpenType 1.8 flags and ensures binary auditors testing `0x3F` vs. `0x7F` never diverge.
* **Flatten Composite Recursion (`numberOfContours > 0`)**: Decompose nested composite glyphs at build time and strip duplicate consecutive nodes (`coords[i] == coords[i+1]`) to prevent stack overflows, division-by-zero rasterizer errors, and composite-subglyph signed-short wraparound heap overflows (`CVE-2025-27363`).

### Step 2.4: Set the PUA Range Bitmask & Dual-Map Developer Symbols
* If your font includes Powerline or status-bar symbols (`U+E0A0`–`U+E0B7`), always set **Bit 25 of `OS/2.ulUnicodeRange2` (Overall Bit 57: Plane 0 Private Use Area)** so Windows `DirectWrite` does not skip your font during fallback scanning.
* Dual-map PUA glyphs to their **Official Unicode Standard** codepoints (`U+E0A0` $\leftrightarrow$ `U+2387` `⎇`, `U+E0A2` $\leftrightarrow$ `U+26BF` `⚿`, `U+E0B0` $\leftrightarrow$ `U+25B6` `▶︎`).

### Step 2.5: Ship Static `.ttf` Fallbacks & Unlock `OS/2.fsType`
* Always ship static `.ttf` and `.woff2` weights (`400`, `700`, `900`) alongside Variable Fonts (`gvar`/`fvar`) so pre-2017 operating systems and embedded displays never render blank text.
* Lock **`OS/2.fsType = 0x0000`** (*Installable Embedding*) so legacy hospital PDF archivers and print spoolers never block document printing.

### Step 2.6: Harden Foundry Build Pipelines & WOFF2 Toolchains
* Pin **`fonttools >= 4.60.2`** to block `.designspace` XML injection and arbitrary file writes in `fontTools.varLib` (**`CVE-2025-66034`**), and pin **`brotli >= 1.2.1`** to close the *"Node2Shell"* Brotli decoder out-of-bounds write (**`CVE-2026-111497`**).
* Audit embedded C wheels in Python QA suites (such as `freetype-py < 2.4.0` pinned by legacy `fontbakery`), preferring system-linked `libfreetype >= 2.14.4` or Rust-based **`fontspector`** in CI.

---

## 3. Appendix for Firmware Engineers: `FreeType` Flags & SFNT Bounds Reference

> **Scope Boundary (Inert Font vs. Host Firmware)**: PocketGull is a clean, inert typographic asset—not an application firewall or certified C middleware library. Safety-critical OEMs should either pre-rasterize glyphs into static bitmap arrays at compile time or load signed firmware images from read-only flash, **verifying the SHA-384 / SHA-256 hash of the font file in flash** against [`fonts/sri-hashes.json`](../fonts/sri-hashes.json) or [`fonts/SHA256SUMS`](../fonts/SHA256SUMS).

### 3.1 Compile Out the TrueType Bytecode VM in Embedded `FreeType` (`ftoption.h`)
When pairing your display with an `instructionLength = 0` static font, you can disable the TrueType bytecode virtual machine at compile time in `include/freetype/config/ftoption.h`:

```c
/* =========================================================================
 * POCKETGULL HARDWARE OEM HARDENED FREETYPE CONFIGURATION (ftoption.h)
 * Eliminates Stuxnet/Duqu-class (CVE-2010-2743) bytecode VM attack surface
 * ========================================================================= */

/* 1. DISABLE the Turing-complete TrueType bytecode virtual machine (fpgm/prep) */
#undef TT_CONFIG_OPTION_BYTECODE_INTERPRETER
#undef TT_CONFIG_OPTION_SUBPIXEL_HINTING

/* 2. DISABLE unhinted auto-fitter if using high-contrast Sloan 5:1 optotypes */
#undef FT_CONFIG_OPTION_AUTOHINTER

/* 3. DISABLE legacy Type 1 / CFF / PFR / BDF / PCF & GX/Variable tables on fixed-font MCUs
 *    (Neutralizes FreeType variation-table bugs CVE-2025-27363, CVE-2026-23865, CVE-2026-50811) */
#undef FT_CONFIG_OPTION_OLD_INTERNALS
#undef TT_CONFIG_OPTION_GX_VAR_SUPPORT /* Omit gvar/fvar/HVAR/MVAR on static-TTF embedded panels */

/* 4. ENFORCE strict memory bounds and disable external file stream compression */
#undef FT_CONFIG_OPTION_USE_LZW
#undef FT_CONFIG_OPTION_USE_ZLIB
#undef FT_CONFIG_OPTION_USE_BZIP2
```

> **HarfBuzz Shaper Build Note (`-Dwasm=disabled`)**: If your embedded Linux or medical display stack links `HarfBuzz`, compile with Meson flag **`-Dwasm=disabled`** (and omit `HB_EXPERIMENTAL_API`) so the WebAssembly Micro Runtime (`WAMR`) in-font `'Wasm'` shaper (**`CVE-2026-113679`**, **`CVE-2026-113680`**) is completely excluded from the binary.

### 3.2 Reference SFNT Bounds & Alignment Check (`pg_verify_sfnt_buffer_safe`)
For firmware engineers loading raw `.ttf` buffers from flash after verifying their **SHA-384 digest**, this reference C99 snippet checks the TrueType `0x00010000` magic header, 4-byte top-level SFNT table alignment, monotonic 2-byte-aligned `loca` offsets, and `instructionLength == 0`:

```c
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

static inline uint16_t pg_read_u16_be(const uint8_t *p) {
    return ((uint16_t)p[0] << 8) | (uint16_t)p[1];
}

static inline uint32_t pg_read_u32_be(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8)  | (uint32_t)p[3];
}

/* Verifies SFNT directory bounds, 4-byte table alignment, 2-byte monotonic loca offsets,
 * zero composite glyphs (numberOfContours >= 0), and zero bytecode (instructionLength == 0) */
bool pg_verify_sfnt_buffer_safe(const uint8_t *buf, size_t len) {
    if (buf == NULL || len < 12) return false;

    /* 1. Require strict TrueType 0x00010000 sfntVersion (reject CFF 'OTTO' & 'ttcf') */
    if (pg_read_u32_be(buf) != 0x00010000U) return false;

    uint16_t num_tables = pg_read_u16_be(buf + 4);
    if (num_tables == 0 || num_tables > 64) return false;

    size_t dir_end = 12U + ((size_t)num_tables * 16U);
    if (dir_end > len) return false;

    uint32_t head_off = 0, head_len = 0;
    uint32_t maxp_off = 0, maxp_len = 0;
    uint32_t loca_off = 0, loca_len = 0;
    uint32_t glyf_off = 0, glyf_len = 0;

    for (uint16_t i = 0; i < num_tables; i++) {
        size_t entry = 12U + ((size_t)i * 16U);
        uint32_t tag    = pg_read_u32_be(buf + entry);
        uint32_t offset = pg_read_u32_be(buf + entry + 8);
        uint32_t length = pg_read_u32_be(buf + entry + 12);

        /* Prevent 32-bit addition wraparound and out-of-bounds reads */
        if ((uint64_t)offset + (uint64_t)length > (uint64_t)len) return false;

        /* OpenType spec requires 4-byte alignment on top-level SFNT table offsets */
        if ((offset & 3U) != 0U) return false;

        /* Reject embedded TrueType VM ('fpgm', 'prep', 'cvt ') & HarfBuzz WebAssembly ('Wasm') tables */
        if (tag == 0x6670676DU || tag == 0x70726570U ||
            tag == 0x63767420U || tag == 0x5761736DU) return false;

        if (tag == 0x68656164U) { head_off = offset; head_len = length; } /* 'head' */
        if (tag == 0x6D617870U) { maxp_off = offset; maxp_len = length; } /* 'maxp' */
        if (tag == 0x6C6F6361U) { loca_off = offset; loca_len = length; } /* 'loca' */
        if (tag == 0x676C7966U) { glyf_off = offset; glyf_len = length; } /* 'glyf' */
    }

    /* 2. Require mandatory TrueType outline tables with minimum valid header lengths */
    if (head_len < 54U || maxp_len < 6U || loca_len < 4U || glyf_len == 0U) {
        return false;
    }

    uint16_t num_glyphs   = pg_read_u16_be(buf + maxp_off + 4);
    uint16_t loc_format   = pg_read_u16_be(buf + head_off + 50); /* 0 = short, 1 = long */
    uint32_t loca_entries = (uint32_t)num_glyphs + 1U;

    /* 3. Verify loca table size, monotonic progression, and 2-byte glyph alignment */
    if (loc_format == 0U) {
        if (loca_len < (uint64_t)loca_entries * 2U) return false;
        uint32_t prev = 0;
        for (uint32_t g = 0; g < loca_entries; g++) {
            /* Short loca stores word offsets (multiplied by 2 -> inherently even) */
            uint32_t curr = (uint32_t)pg_read_u16_be(buf + loca_off + (g * 2U)) * 2U;
            if (curr < prev || curr > glyf_len) return false;
            prev = curr;
        }
    } else if (loc_format == 1U) {
        if (loca_len < (uint64_t)loca_entries * 4U) return false;
        uint32_t prev = 0;
        for (uint32_t g = 0; g < loca_entries; g++) {
            uint32_t curr = pg_read_u32_be(buf + loca_off + (g * 4U));
            /* Enforce monotonic non-decreasing offsets, glyf bounds, and 2-byte alignment */
            if (curr < prev || curr > glyf_len || (curr & 1U) != 0U) return false;
            prev = curr;
        }
    } else {
        return false; /* Invalid indexToLocFormat */
    }

    /* 4. Walk every glyph slice in 'glyf' to enforce:
     *    - No composite glyphs (numberOfContours >= 0)
     *    - Zero TrueType bytecode instructions (instructionLength == 0)
     */
    for (uint32_t g = 0; g < num_glyphs; g++) {
        uint32_t g_start = (loc_format == 0U)
            ? ((uint32_t)pg_read_u16_be(buf + loca_off + (g * 2U)) * 2U)
            : pg_read_u32_be(buf + loca_off + (g * 4U));
        uint32_t g_end = (loc_format == 0U)
            ? ((uint32_t)pg_read_u16_be(buf + loca_off + ((g + 1U) * 2U)) * 2U)
            : pg_read_u32_be(buf + loca_off + ((g + 1U) * 4U));

        uint32_t g_len = g_end - g_start;
        if (g_len == 0U) {
            continue; /* Legitimate empty glyph (space, uni200C.joiner) */
        }

        /* Minimum simple glyph header: 10-byte bbox + 2-byte instructionLength */
        if (g_len < 12U) return false;

        const uint8_t *glyph_ptr = buf + glyf_off + g_start;
        int16_t num_contours = (int16_t)pg_read_u16_be(glyph_ptr);

        /* Reject composite glyphs (negative numberOfContours) in firmware */
        if (num_contours < 0) return false;

        /* Verify endPtsOfContours array + instructionLength fit inside slice */
        uint32_t insn_offset = 10U + ((uint32_t)num_contours * 2U);
        if (insn_offset + 2U > g_len) return false;

        /* Enforce instructionLength == 0 (Zero-VM invariant) */
        uint16_t insn_len = pg_read_u16_be(glyph_ptr + insn_offset);
        if (insn_len != 0U) return false;
    }

    return true;
}
```

### 3.3 Recommended PocketGull Binaries by Hardware Profile

| Hardware / Embedded Target | Recommended PocketGull Binary | Footprint & Key Safety Properties |
| :--- | :--- | :--- |
| **ICU Vital-Sign Monitors & Infusion Pumps**<br>*(STM32, NXP i.MX RT, Embedded Linux)* | `fonts/ttf/PocketGull-Numerics.ttf`<br>or `fonts/ttf/PocketGullMono-Regular.ttf` | **Fixed 600-UPM pitch**, Louise Sloan 5:1 optotypes, ISMP slashed zero (`0̸`), gapless ECG sub-cell blocks (`U+2581`–`U+2588`), `instructionLength = 0`. |
| **Hospital EHR Carts, Citrix Thin Clients & Pre-2017 PCs**<br>*(Windows 7/10 LTSC, Legacy GDI)* | `fonts/ttf/PocketGull-Fineliner.ttf`<br>& `fonts/ttf/PocketGull-Bold.ttf` | **Static TrueType (`.ttf`)** (no `gvar` dependency), `OS/2.fsType = 0x0000` (never blocks PDF/print spoolers), `gasp = 0x0006` symmetric smoothing. |
| **Developer Terminals, Avionics & Industrial HUDs** | `fonts/ttf/PocketGullMono-Regular.ttf` | Active **`uni202E.guard` (`[!]`)** anti-spoofing badge, dual-mapped PUA + Official Unicode status icons (`⎇`, `⚿`, `▶︎`), 2-byte word-aligned `loca`. |
| **Modern Web, Mobile & Bandwidth-Constrained Edge** | `fonts/woff2/PocketGull-VF.woff2`<br>+ `fonts.css` SMoE Shards | **Brotli Q11 compressed**, lazy-loaded **12–35 KB `unicode-range` shards**, pinned with `sha384` Subresource Integrity (`fonts/sri-hashes.json`). |

---

## 4. Automated Verification Commands (Open-Source Toolchain)

Any font creator or hardware OEM can run PocketGull's open-source verification suite locally before flashing firmware or publishing a release:

```powershell
# 1. Run Forensic SFNT & W3C OTS Binary Auditor (2-byte loca alignment, Bit-7 flags, BBox bounds)
dart run tool/pocketgull_foundry.dart audit

# 2. Run Google Fonts & OpenType Pre-Flight Validator (UPM 1000, fsType=0, 0 duplicate nodes, OTS)
python sources/validate_fonts.py

# 3. Run Security, Anti-Spoofing & CI Invariant Suite
npm run test:unit
```
