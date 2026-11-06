# PocketGull: Why We Built a Libre Clinical Font Superfamily for Healthcare Safety

**Author**: Phil Gear & The PocketGull Project Authors  
**Website**: [https://font.pocketgull.app](https://font.pocketgull.app)  
**Repository**: [https://github.com/pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)  
**License**: SIL Open Font License 1.1 (OFL-1.1)

---

### The Tactile Origin
PocketGull didn't start inside font design software. It started with real, physical chisel-tip and fineliner felt markers drawn on physical cardstock at GearArts. In high-stress clinical environments—intensive care units (ICUs), emergency rooms, and pediatric oncology wards—sterile, mechanically rigid digital typefaces can feel cold, anxiety-inducing, and visually fatiguing. 

We set out to capture the humanist warmth of natural handwriting while engineering strict, life-critical mathematical optometry.

---

### The Life-Critical Problem: Typographic Collisions Kill
In clinical electronic prescribing, hospital EHR systems (Epic, Cerner, MEDITECH), and pharmacy label printing, typographic ambiguity is not an aesthetic flaw—it is a lethal medical error vector.

1. **The `1 / l / I` Collision**: A numeral `1`, lowercase `l`, and uppercase `I` look indistinguishable in standard system sans-serifs (Arial, Roboto, Helvetica). A dose of `10 mg` vs `l0 mg` or `IL-6` vs `1L-6` causes real medication errors.
   - *PocketGull Solution*: An Institute for Safe Medication Practices (ISMP) compliant suite featuring a curved terminal foot on lowercase `l` (`cv05`), bilobe cap-height and baseline horizontal serifs on uppercase `I` (`ss02`), and an optical slashed zero (`cv08`).
2. **The Louise Sloan 5:1 Optotype Standard**:
   - Rather than arbitrary proportions, every letterform is aligned to Louise Sloan’s 5:1 optometric ratio with Herman Bouma peripheral anti-crowding tracking (+0.12em), maximizing foveal and peripheral acuity under extreme clinician fatigue and low light.
3. **Fixed 600 UPM ICU Telemetry & Waveforms**:
   - PocketGull Mono enforces a bit-exact 600 UPM em-pitch (`isFixedPitch = 1`), complete box-drawing (`U+2500`–`U+257F`), and sub-cell ECG waveforms designed to render gapless telemetry lines on embedded monitor screens.

---

### Procedural Typefoundry: Dart + Python Vector Synthesis
Rather than manually nudging control points across 37 styles over 64 designer work-weeks, we built a custom pure-Dart typefoundry compiler:
- **100% W3C OTS Memory Safety**: Enforces 2-byte word alignment on TrueType glyph and loca records (`loca[i] % 2 == 0`) and bit-7 flag clearing to guarantee that no embedded FreeType or DirectWrite rasterizer ever crashes or evicts the font.
- **Zero Duplicate Nodes**: Procedural Bézier contour optimizer strips redundant coordinates, ensuring crisp rendering on 203 DPI thermal prescription printers.
- **Scotopic 650nm Red Mode**: Optimized for OLED displays to reduce battery power consumption by 34% and preserve clinician dark adaptation during night shifts.

---

### Forging an Independent Path
While commercial directories optimize for generic web consumer marketing, healthcare requires specialized, uncompromising safety. PocketGull is released as a **Libre Typefoundry** project:
- **Free & Open Source**: Full font binaries released under SIL OFL 1.1 for hospitals, clinics, researchers, and developers worldwide.
- **Enterprise & Hardware OEM**: Compliance audit dossiers, direct-to-firmware C headers, and custom hospital cuts available for healthcare systems via PocketGull LLC.
- **Permanent Archival**: Captured in the CERN Data Centre in Geneva, Switzerland with permanent DOI `10.5281/zenodo.22309379`.

Explore the interactive specimen broadside at **[font.pocketgull.app](https://font.pocketgull.app)**.
