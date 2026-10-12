/**
 * @file lv_font_pocketgull_16.h
 * @brief PocketGull Clinical Monospace Font descriptor for LVGL (v8/v9)
 *
 * Provides Louise Sloan 5:1 optotypes and ISMP character disambiguation
 * for embedded medical monitors, smartwatch dials, and microcontrollers (ESP32/RP2040).
 */

#ifndef LV_FONT_POCKETGULL_16_H
#define LV_FONT_POCKETGULL_16_H

#ifdef __cplusplus
extern "C" {
#endif

#include "lvgl/lvgl.h"

/* Declare PocketGull font instances */
extern const lv_font_t lv_font_pocketgull_16;
extern const lv_font_t lv_font_pocketgull_mono_16;

/**
 * @brief Helper to initialize PocketGull style on an LVGL label or chart
 */
static inline void lv_style_set_pocketgull(lv_style_t * style) {
    lv_style_set_text_font(style, &lv_font_pocketgull_mono_16);
    lv_style_set_text_letter_space(style, 1);
}

#ifdef __cplusplus
} /*extern "C"*/
#endif

#endif /*LV_FONT_POCKETGULL_16_H*/
