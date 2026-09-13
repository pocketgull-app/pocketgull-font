# Google Fonts Pull Request Blueprint

Use this template when opening a PR to [`google/fonts`](https://github.com/google/fonts) to onboard the PocketGull superfamily.

---

## PR Title
```text
[New Font] PocketGull Superfamily (Bold, Fineliner, Chiseltip, Mono)
```

## Pull Request Description
```markdown
### Summary
This PR onboards the **PocketGull** font superfamily, an open-source clinical and handwriting typeface designed by Phil Gear. Originating from hand-inked felt marker lettering created on physical cardstock for GearArts, the superfamily bridges tactile humanist warmth with Louise Sloan 5:1 optotypic legibility and Institute for Safe Medication Practices (ISMP) disambiguation standards.

- **Family Name**: `PocketGull` & `PocketGull Mono`
- **Styles**: 
  - `PocketGull-Bold.ttf` (Weight: 700 / 800 Display)
  - `PocketGull-Fineliner.ttf` (Weight: 300 / 400 Light Text)
  - `PocketGull-Chiseltip.ttf` (Weight: 900 Black Calligraphic Display)
  - `PocketGullMono-Regular.ttf` (Weight: 400 Monospace Telemetry, 600 UPM pitch)
- **License**: SIL Open Font License, Version 1.1 (zero Reserved Font Names)
- **Upstream Repository**: https://github.com/pocketgull-app/pocketgull-font
- **Interactive Specimen**: https://pocketgull.app (or local index.html)

### Technical Specifications & Quality Assurance
- **Grid Resolution**: Standard 1000 UPM grid across all styles.
- **Embedding (`fsType`)**: `0x0000` (Installable embedding).
- **Vertical Metrics**: `USE_TYPO_METRICS` flag enabled (`fsSelection` bit 7) across all styles.
- **Monospace Metadata**: `post.isFixedPitch = 1` and `OS/2.panose.bProportion = 9`.
- **OpenType STAT Table**: Included in all 4 static fonts, linking `'wght'`, `'wdth'`, and `'ital'` axis values.
- **Outline Quality**: 0 zero-length segments, 100% integer coordinates, closed contours, clockwise outer contours.
- **Glyph Coverage**: 3,350+ Unicode glyphs exceeding GF Latin Core, GF Latin Extended-A, and the complete 256-glyph Unicode Braille block (`U+2800`–`U+28FF`).
- **Copyright & License**: `name` ID 0 matches `OFL.txt` line 1 character-for-character.

### Associated Designer Profile
- Contained in `catalog/designers/philgear/`:
  - `info.pb` (designer: "Phil Gear", link: "https://pocketgull.app", avatar: "philgear.png")
  - `bio.html` (3rd-person biography, ~60 words, valid hyperlinks)
  - `philgear.png` (300x300 square PNG)

### Checklist
- [x] All authors/contributors credited in `AUTHORS.txt` and `CONTRIBUTORS.txt`.
- [x] Google Contributor License Agreement (CLA) signed.
- [x] `METADATA.pb` validated and verified.
- [x] `upstream.yaml` configured for automated upgrading via `gftools packager`.
- [x] `article/ARTICLE.en_us.html` included.
- [x] Pre-flight validation script passes 100% (`python sources/validate_fonts.py`).
```
