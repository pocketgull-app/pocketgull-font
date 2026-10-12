# PocketGull Typography for Embedded Displays (LVGL, ESP32, RP2040, Arduino)

Brings **Louise Sloan 5:1 optotypic legibility** and **ISMP disambiguation** to SPI/I2C displays, handheld medical devices, and microcontroller telemetry monitors.

## 1. LVGL (Light and Versatile Graphics Library v8 / v9)

Use LVGL's official font converter tool:

```bash
# Convert TTF to compact 4-bit antialiased C array for ESP32/RP2040
npx lv_font_conv --font fonts/ttf/PocketGullMono-Regular.ttf -r 0x20-0x7F,0xB0,0x3BC --size 16 --bpp 4 --format lvgl -o lv_font_pocketgull_mono_16.c
```

In your C/C++ firmware:
```c
#include "lv_font_pocketgull_16.h"

lv_obj_t * label = lv_label_create(lv_scr_act());
lv_obj_set_style_text_font(label, &lv_font_pocketgull_mono_16, 0);
lv_label_set_text(label, "SPO2: 98%  HR: 72 bpm");
```

## 2. Adafruit GFX (OLED 128x64 & TFT)

Generate a custom header using `fontconvert`:
```bash
fontconvert fonts/ttf/PocketGullMono-Regular.ttf 12 > PocketGullMono12pt7b.h
```
