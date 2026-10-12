-- WezTerm Configuration for PocketGull Mono
-- Enables ISMP disambiguation, slashed zero, curved 'l', and amber/scotopic phosphor themes

local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font_with_fallback({
  {
    family = 'PocketGull Mono',
    weight = 'Regular',
    harfbuzz_features = {
      'zero=1', -- Slashed zero
      'cv08=1', -- ISMP slashed zero
      'cv05=1', -- Curved lowercase l
      'cv11=1', -- Slashed Z
      'ss02=1', -- Serifed capital I
    },
  },
  'Consolas',
  'Noto Color Emoji',
})

config.font_size = 13.0
config.line_height = 1.15

-- Vintage Amber CRT (P3 Phosphor) Color Palette
config.colors = {
  foreground = '#fbbf24',
  background = '#0a0d12',
  cursor_bg = '#fbbf24',
  cursor_fg = '#0a0d12',
  cursor_border = '#fbbf24',
  selection_fg = '#0a0d12',
  selection_bg = '#d97706',
  ansi = {
    '#05080c', '#ef4444', '#22c55e', '#f59e0b',
    '#3b82f6', '#a855f7', '#06b6d4', '#f4f4f5',
  },
  brights = {
    '#52525b', '#f87171', '#4ade80', '#fbbf24',
    '#60a5fa', '#c084fc', '#22d3ee', '#ffffff',
  },
}

return config
