# PocketGull™ Typeface Superfamily
### Commercial & Enterprise Edition — Version 3.1.0
**Designed by Phillip Gear | Geararts LLC**  
*Optotypically Calibrated Clinical & Telemetry Superfamily*

Thank you for licensing the **PocketGull™ Typeface Superfamily**. PocketGull was born on physical cardstock with felt markers and rigorously engineered into an industrial-grade, 38-cut typeface designed for high-stress reading environments, life-critical clinical telemetry, and human-centered design.

---

## 📁 Package Contents

```text
PocketGull-v3.1.0-Commercial/
├── fonts/
│   ├── ttf/                     # 38 TrueType Desktop cuts (Print, Office, Desktop apps)
│   ├── woff2/                   # 38 WOFF2 Web cuts (High compression for modern web)
│   └── variable/                # 2-Axis Continuous Variable Fonts (Weight: 100-900, Slant)
├── css/
│   ├── pocketgull.css           # Complete pre-compiled CSS font-face declarations
│   └── pocketgull-telemetry.css # Monospace ICU and lab telemetry styles
├── specimens/                   # High-resolution clinical & architectural broadsides
├── documentation/
│   ├── ISMP_SAFETY_MATRIX.md    # Medication safety and collision avoidance guide
│   └── POCKETGULL_TELEMETRY.md  # 600 UPM fixed-pitch ICU grid specs
└── COMMERCIAL_LICENSE_EULA.md   # Your perpetual commercial license agreement
```

---

## ⚡ Instant Web Implementation

### 1. Link the Stylesheet
Place the `pocketgull.css` file in your web assets and include it:
```html
<link rel="stylesheet" href="/assets/fonts/pocketgull.css">
```

### 2. Clinical Prescription & Dosage Safety (ISMP Disambiguated)
Activate slashed zero (`0̸`), curved foot `l`, and bilobe serif `I` to eliminate dosage confusion:
```css
.prescription-safe {
  font-family: 'PocketGull', system-ui, sans-serif;
  font-feature-settings: "zero" 1, "cv08" 1, "cv05" 1, "ss02" 1, "tnum" 1;
}
```

### 3. ICU & Diagnostic Telemetry (Zero Column Shear)
Strict 600 UPM pitch invariant with gapless box-drawing (`U+2500`–`U+257F`):
```css
.icu-monitor {
  font-family: 'PocketGull Mono', monospace;
  font-variant-numeric: tabular-nums;
  line-height: 1.0;
}
```

### 4. Pediatric & Calming Interfaces ("The Healer")
Activate cardiac heart tittles on lowercase `i` and `j` to reduce pediatric anxiety:
```css
.pediatric-care {
  font-family: 'PocketGull VF', 'PocketGull', sans-serif;
  font-feature-settings: "cv09" 1, "ss07" 1;
}
```

---

## 🛠️ Need Custom Cuts, Assistance, or Enterprise Invoicing?

For enterprise vendor compliance, custom weights, or procurement invoicing:
* **Designer & Engineer:** Phillip Gear
* **Email:** `licensing@pocketgull.app` / `philgear@gmail.com`
* **Portfolio & Live Specimen:** [https://font.pocketgull.app](https://font.pocketgull.app)
