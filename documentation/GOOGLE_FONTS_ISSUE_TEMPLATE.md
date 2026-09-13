# New Font Submission: PocketGull Superfamily

Use this markdown template when filing the submission issue on [github.com/google/fonts/issues/new/choose](https://github.com/google/fonts/issues/new/choose).

---

## Issue Title
```text
[New Font Submission] PocketGull Superfamily (Bold, Fineliner, Chiseltip, Mono)
```

## Issue Body
```markdown
### Font Family Name
PocketGull & PocketGull Mono

### Primary Script
Latin (`Latn`)

### Designer
**Phil Gear** (Principal Designer)  
Portfolio & Interactive Specimen: https://pocketgull.app  
Upstream Repository: https://github.com/pocketgull-app/pocketgull-font

### Description
PocketGull is an open-source clinical handwriting and display font superfamily designed by Phil Gear. Originating from spontaneous felt marker lettering created on physical cardstock for GearArts fine art and photographic editions, PocketGull bridges tactile humanist warmth with Institute for Safe Medication Practices (ISMP) glyph disambiguation and Louise Sloan 5:1 optotypic legibility standards.

The family contains 4 coordinated static styles:
1. **PocketGull-Bold.ttf** (Weight: 700) — Confident headline & prescription marker
2. **PocketGull-Fineliner.ttf** (Weight: 400) — Delicate text & dosage pen lettering
3. **PocketGull-Chiseltip.ttf** (Weight: 900) — Expressive calligraphic display & trauma headers
4. **PocketGullMono-Regular.ttf** (Weight: 400, Monospace 600 UPM pitch) — ICU telemetry, tabular figures, & clinical terminal output

### License
SIL Open Font License 1.1 (zero Reserved Font Names)

### Source & Build
- Upstream Git repository: https://github.com/pocketgull-app/pocketgull-font
- Automated hermetic validator: `python sources/validate_fonts.py` (30/30 checks pass)
- Standard 1000 UPM grid across all styles
- `fsType = 0x0000` (Installable)
- `USE_TYPO_METRICS` enabled across all styles
- `post.isFixedPitch = 1` and `panose.bProportion = 9` on Mono
- OpenType STAT tables included in all static fonts
- Over 3,350 Unicode glyphs per font covering GF Latin Core, GF Latin Extended-A, and the complete 256-glyph Unicode Braille block (`U+2800`–`U+28FF`).
- Clean geometry: 0 duplicate points, 0 zero-length segments, 100% integer coordinates.

### Designer Profile
Included in `catalog/designers/philgear/`:
- `info.pb`
- `bio.html`
- `philgear.png` (300×300 PNG)

### Suggested Labels for Onboarders
- `I New font`
- `II Submitted`
```
