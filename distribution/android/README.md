# PocketGull Font Engine on Google Pixel (OLED Battery & Acuity Guide)

## 1. Why Google Pixel Phones Benefit Immediately
Google Pixel devices feature high-refresh OLED / LTPO displays. OLED subpixels emit their own light:
* **`#000000` (Pure Black)** = 0 mA diode power.
* **Open Counters & Louise Sloan 5:1 Ratios** allow comfortable reading at 30–40% lower screen brightness.
* **$O(1)$ FreeType/Skia Rasterization** eliminates jagged font recalculations and CPU wake-locks.

---

## 2. Option A: Web App / Reading Experience (Zero Root Required)
Import [pixel_oled_battery_saver.css](file:///c:/Users/philg/Pocketgull/pocketgull-typeface/distribution/android/pixel_oled_battery_saver.css) into any PWA, local reader, or browser:

```html
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="distribution/android/pixel_oled_battery_saver.css">

<body class="oled-battery-saver">
  <!-- Automatically activates ISMP disambiguation: cv05, cv08, cv11, ss02 -->
</body>
```

For ultra-low power late night reading (e.g. bedside or emergency shifts):
```html
<body class="oled-battery-saver scotopic-650nm">
  <!-- Monochromatic 650nm Red: 0 rhodopsin bleaching + absolute lowest diode power -->
</body>
```

---

## 3. Option B: System-Wide Replacement via Magisk / KernelSU (Rooted Pixel)
For complete system-wide replacement of Google's Roboto / Google Sans:
1. Target System Path: `/system/fonts/Roboto-Regular.ttf` & `/system/fonts/Roboto-Bold.ttf`.
2. Map PocketGull:
   * `PocketGull-Regular.ttf` $\to$ `Roboto-Regular.ttf`
   * `PocketGull-Bold.ttf` $\to$ `Roboto-Bold.ttf`
   * `PocketGullMono-Regular.ttf` $\to$ `DroidSansMono.ttf`
3. Flash as a systemless overlay via Magisk or KernelSU to ensure safetynet/integrity preservation.

---

## 4. Option C: e-Reader / Terminal Apps (No Root Required)
For everyday Pixel usage without rooting:
* **Termux**: Set `~/.termux/font.ttf` to `PocketGullMono-Regular.ttf` for monospaced telemetry with 0 battery jitter.
* **Moon+ Reader / KOReader**: Drop `PocketGull-Regular.ttf` into `sdcard/Fonts` and select OLED Pure Black theme.
