---
library_name: peft
base_model: google/gemma-3-1b-it
license: other
license_name: gemma
license_link: https://ai.google.dev/gemma/terms
language:
  - en
pipeline_tag: text-generation
tags:
  - gemma3
  - lora
  - opentype
  - variable-font
  - typography
  - screenplay
  - closed-captions
  - pocketgull
---

# PocketGull Prosody Gemma (`pocketgull-prosody-gemma-3-1b`)

A compact Gemma 3 1B LoRA / Q4_K_M GGUF model trained to convert raw screenplay dialogue, parenthetical directions (`(whispers)`, `(tightly)`, `(exhales softly)`), and closed-caption lines into **10-axis OpenType variable font keyframes** calibrated for **PocketGull VF**.

## Schema & Output Contract

Given a JSON list of dialogue beats (`speaker`, `direction`, `text`), the model returns structured JSON matching the PocketGull Closed Caption Studio schema:

```json
{
  "beats": [
    {
      "index": 0,
      "emotion": "intimate",
      "instance": "soft_light",
      "weight": 300,
      "width": 99,
      "slant": -4.0,
      "soft": 1.0,
      "hlng": 0.65,
      "boum": 0.40,
      "aptr": 0.45,
      "grav": 0.15,
      "chis": 0,
      "tension": 44,
      "bpm": 66
    }
  ]
}
```

### Axis & Variation Bounds (`PocketGull-VF.ttf`)
| Axis | Bounds | Role in Emotion & Variation |
| :--- | :--- | :--- |
| `instance` | Named `fvar` | `soft_light`, `soft_regular`, `soft_bold`, `soft_black`, `healing_calm`, `recovery_72bpm`, `chiseltip_45`, `dyslexia_gravity`, `default` |
| `weight` (`wght`) | `100 .. 900` | Whisper delicacy (`240`) / Soft Light (`300`) to Alert (`850`) / Chiseltip (`900`) |
| `width` (`wdth`) | `75 .. 100` | Line-fitting compression under urgent alarms |
| `slant` (`slnt`) | `-10.5 .. 0` | Confessional / internal oblique (`-6.5`) |
| `SOFT` | `0.0 .. 1.0` | Felt-marker rounded terminals (`1.0` across all Soft family weights vs. `0.0` crisp alert) |
| `HLNG` | `0.0 .. 1.0` | Warm humanist healing curvature (`1.0` Healing Calm / Vagal Relief) |
| `BOUM` | `0.0 .. 1.0` | Open Bouma letterform body expansion (`0.90` Cosmic Awe) |
| `APTR` | `0.0 .. 1.0` | Louise Sloan counter aperture anti-bloom (`0.35` intimate .. `1.0` wide) |
| `GRAV` | `0.0 .. 1.0` | Heavy baseline gravity anchor (`1.0` Dyslexia Gravity) |
| `CHIS` | `0 .. 45` | Broad 45° chisel-tip nib angle (`45` dramatic placards & chapter titles) |

## Negative Space & Privacy Boundaries
- Runs **100% locally** (`127.0.0.1` via Ollama or llama.cpp) so unpublished screenplays and clinical simulation scripts never egress to external APIs.
- Strictly **assistive typographic & editorial curation** — never provides medical advice, diagnosis, or automated clinical triage.

## Training & Local Usage
```bash
# 1. Regenerate dataset from PocketGull studio scenes & screenplay beats
node scripts/build-prosody-dataset.mjs

# 2. Fine-tune QLoRA on Gemma 3 1B IT (Colab / GPU Linux)
python distribution/huggingface/pocketgull-prosody-gemma/train_qlora_gemma.py

# 3. Create instant local Ollama model from Gemma 3 1B base or exported GGUF
ollama create pocketgull-prosody-gemma -f distribution/huggingface/pocketgull-prosody-gemma/Modelfile
```
