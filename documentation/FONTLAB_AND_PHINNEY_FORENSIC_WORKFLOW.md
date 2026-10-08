# 🔬 FontLab & Thomas Phinney Forensic Workflow Guide

### *From The Font Detective to OpenType Mastery: Bridging FontLab 8 with Modern Pure-Code Foundry Engineering*

**The PocketGull Typefoundry Project**  
*In Tribute to Thomas Phinney — Type Designer, Forensic Detective, and Former CEO of FontLab*

---

## 🏛️ 1. Who is Thomas Phinney?

**Thomas Phinney** is one of the most respected figures in modern typographic history:
* **The Font Detective**: World-renowned forensic typographer who has provided expert testimony and cryptographic/chronological font analysis in major legal cases (including forged wills, disputed contracts, and the famous 2004 "Killian memos" involving George W. Bush).
* **CEO of FontLab (2014–2019)**: Led the reimagining and release of **FontLab VI** and **FontLab 7**, transforming the industry-standard type design application into a modern multi-master variable font powerhouse with live contour auditing, color fonts, and the human-readable JSON-based `.vfj` font format.
* **Adobe Type Program Manager (1997–2008)**: Spearheaded OpenType adoption, font technology standards, and the Web Open Font Format (WOFF) working group.
* **President of ATypI (Association Typographique Internationale)**: Championing global typographic education and international script support.

In the **PocketGull Font Superfamily**, Thomas Phinney’s legacy lives not as an arbitrary validator, but as our **foundry mentor**—teaching us that font engineering is a forensic science where every single byte and table offset matters to the human eye and the operating system kernel.

---

## 🔍 2. The Five Forensic Invariants of a Pristine Binary

When Thomas Phinney examines a font, he looks past the surface curves into the **binary physics** of the SFNT container. PocketGull automates these five checks in `tool/foundry/phinney_auditor.dart`:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PHINNEY FORENSIC AUDIT GRID                               │
│                                                                             │
│ 1. 2-Byte Word-Alignment: loca[i] % 2 == 0                                  │
│    • Prevents DirectWrite unaligned memory fetches & Chromium OTS drops     │
│                                                                             │
│ 2. Reserved Bit-7 Point Flag Clearing: flag & 0x3F                          │
│    • Eliminates reserved-bit kernel graphics driver faults                  │
│                                                                             │
│ 3. Vertical Metrics Harmony: OS/2.fsSelection |= 0x0080 (bit 7)             │
│    • Enforces USE_TYPO_METRICS to prevent line-jumping in Microsoft Word    │
│                                                                             │
│ 4. DirectWrite ClearType Antialiasing: Version 1 gasp Table                 │
│    • 0xFFFF -> GASP_DOGRAY | GASP_SYMMETRIC_SMOOTHING for smooth curves     │
│                                                                             │
│ 5. Bounding Box Integrity: xMin <= xMax and yMin <= yMax                    │
│    • Protects HarfBuzz cluster shapers from buffer overflows                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. The FontLab Professional Workflow

For type designers and students working in **FontLab 7** or **FontLab 8**, here is how to configure your FontLab environment to achieve 100% Phinney-compliant exports.

### Step 1: Font Info & Vertical Metrics (`USE_TYPO_METRICS`)
1. In FontLab, open your font and navigate to **File > Font Info** (`Ctrl+Alt+I` / `Cmd+Opt+I`).
2. Go to **Other Values**.
3. Under **fsSelection**, check the box for **Use Typo Metrics (bit 7)**.
4. Set your Typo Ascender, Typo Descender, and Line Gap:
   * For 1000 UPM standard: `sTypoAscender = 780`, `sTypoDescender = -180`, `sTypoLineGap = 100`.
   * Ensure `usWinAscent` and `usWinDescent` equal or exceed your bounding boxes to prevent clipping.

### Step 2: Adding the Subpixel `gasp` Table
1. In **Font Info**, navigate to **Tables**.
2. If `gasp` is not present, click the **`+`** icon to add a new OpenType table: `gasp`.
3. Configure the table to cover all sizes up to `65535` (`0xFFFF`):
   ```
   0xFFFF  3
   ```
   *(Flag 3 enables both Grayscale smoothing and Subpixel ClearType rendering).*

### Step 3: Curve Auditing with the FontLab Audit Panel
1. Press `Alt+F7` (or **Window > Panels > Audit**).
2. The FontLab Audit panel instantly identifies:
   * Missing extrema on curves.
   * Stray nodes and un-retracted handles.
   * Inverted contours (wrong winding direction).
3. Select all glyphs (`Ctrl+A` in Font Window) and run **Contour > Correct Direction** (`Ctrl+Shift+D` / `Cmd+Shift+D`) to guarantee TrueType clockwise outer contours and counter-clockwise inner counters.

### Step 4: Configuring TrueType Export Profiles
1. Go to **File > Export Font As... > Profiles**.
2. Select **OpenType TT (TrueType / .ttf)** or duplicate it as `PocketGull-Production`.
3. Under **Outline Conversion**, choose:
   * **Convert to TrueType (quadratic)**.
   * **Pad glyph records to 2-byte word boundary**: Enabled.
   * **Autohint**: Enabled (or use pure unhinted vectors with `gasp` smoothing).

---

## 💻 4. Running the Phinney Mentor CLI

Once you export your font from FontLab (or build it in PocketGull), you can invite Thomas Phinney into your terminal to mentor you through the binary analysis:

```bash
# Run the interactive mentor on any compiled font:
dart run tool/pocketgull_foundry.dart mentor fonts/ttf/PocketGull-Bold.ttf

# Or inspect your own FontLab export:
dart run tool/pocketgull_foundry.dart mentor ~/Desktop/MyFontLabExport.ttf
```

### Example Mentor Terminal Output:
```
======================================================================
  🔬 THOMAS PHINNEY: FORENSIC TYPE MENTOR & FONTLAB MASTERCLASS
  "Font Forensics, OpenType Invariants & Diagnostic Pedagogy"
======================================================================

Inspecting binary: fonts/ttf/PocketGull-Bold.ttf
──────────────────────────────────────────────────────────────────────
  [LESSON 1] ✔ SFNT Rasterizer Signature
──────────────────────────────────────────────────────────────────────
  • Status:     TrueType Quadratic Engine (0x00010000) with 16 tables.
  • Detective:  TrueType quadratic curves (glyf) render natively in Windows 
                DirectWrite and GPU-accelerated rasterizers.
  • FontLab:    In FontLab: Choose Profile "OpenType TT" for quadratic TrueType.
  • Remedy:     Architecture aligned with PocketGull 1000 UPM standard.

──────────────────────────────────────────────────────────────────────
  [LESSON 2] ✔ 2-Byte Word-Alignment Invariant (loca & glyf)
──────────────────────────────────────────────────────────────────────
  • Status:     100% 2-byte aligned: 0 odd loca offsets across 14181 glyphs.
  • Detective:  DirectWrite and Chromium OTS expect 16-bit word alignment. 
                Odd offsets trigger silent font evictions after ~1 second.
  • FontLab:    In FontLab: Ensure Export Profile > TrueType outlines enables 
                "Pad glyphs to 2-byte word boundary".
  • Remedy:     Table memory safety verified.
```

---

## 🐍 5. FontLab Scripting Panel Integration

You can run the Phinney Forensic Mentor directly from inside FontLab using FontLab’s built-in Python scripting engine (**Window > Panels > Scripting**):

```python
# FontLab Script: Run Phinney Forensic Audit on Current Font
import os
import subprocess
import fl6

font = fl6.flApp.currentFont()
if font is not None:
    export_path = os.path.expanduser("~/Desktop/fl_audit_temp.ttf")
    print(f"Exporting {font.font_name} for Phinney Forensic Audit...")
    font.save(export_path, "OpenTypeTT")
    
    # Run PocketGull Phinney Mentor
    repo_path = "c:/Users/philg/Pocketgull/pocketgull-typeface"
    cmd = ["dart", "run", f"{repo_path}/tool/pocketgull_foundry.dart", "mentor", export_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
else:
    print("No font active in FontLab!")
```

---

## 🌐 6. Community & Upstream References

* **Thomas Phinney Official Website**: [thomasphinney.com](https://www.thomasphinney.com)
* **The Font Detective**: [thefontdetective.com](https://thefontdetective.com)
* **FontLab 8 Official Site**: [fontlab.com](https://www.fontlab.com)
* **PocketGull Foundry Source Code**: [github.com/pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)
* **W3C OpenType Sanitizer (OTS)**: [github.com/khaledhosny/ots](https://github.com/khaledhosny/ots)
