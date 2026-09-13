# Contributing to PocketGull Font

Thank you for your interest in contributing to the **PocketGull Font Superfamily**! 

PocketGull is an open-source clinical and ophthalmological font superfamily engineered to bridge tactile humanist warmth with life-critical clinical precision. We welcome contributions from type designers, font developers, clinical informaticians, and accessibility advocates.

---

## Code of Conduct

All contributors and maintainers agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (Contributor Covenant 2.1).

---

## Development & Font Engineering Setup

PocketGull uses the official **Google Fonts Project Template** architecture:
* **Source format**: Unified Font Object (`sources/*.ufo`, UFO3 standard)
* **Build system**: `fontmake` via `gftools-builder sources/config.yaml`
* **Forensic validation**: `fontbakery` (Google Fonts profile) and Dart `pocketgull_foundry`

### Prerequisites
* **Python 3.11+**
* `fontmake` (`pip install fontmake gftools fontbakery`)
* **Dart 3.5+** (for forensic TrueType table audits)

### Building the Fonts
```bash
# Build TrueType and WOFF2 binaries from UFO sources
gftools-builder sources/config.yaml
```

---

## Quality & Security Invariants (OpenSSF & Google Fonts Standard)

Every contribution must satisfy our 5 core engineering invariants before pull request acceptance:

1. **Semantic Versioning (`v2.0.0`)**:
   * Versioning strictly follows SemVer 2.0.0.
   * Font revision (`head.fontRevision`) must match `nameID 5` and `sources/*.ufo/fontinfo.plist`.
2. **W3C OTS Memory Safety**:
   * All binaries must pass the W3C OpenType Sanitizer with zero errors.
3. **2-Byte Word Alignment**:
   * TrueType `.glyf` contours must be padded so `loca[i] % 2 == 0`.
4. **Fontbakery QA**:
   * `fontbakery check-googlefonts fonts/ttf/*.ttf` must pass with **0 FAILs** and **0 FATALs**.
5. **Clinical Disambiguation & Sloan 5:1 Acuity**:
   * Do not alter the ISMP slashed zero (`cv08`), curved `l` (`cv05`), or serifed `I` (`ss02`) disambiguation glyphs.
   * Monospace advance width must remain strictly **600 UPM**.

---

## Pull Request Guidelines

1. **Branch Naming**: Use descriptive branch names (e.g. `feat/new-glyph-set`, `fix/ot-metrics`).
2. **Conventional Commits**:
   * Follow the Conventional Commits specification: `<type>(<scope>): <description>`
   * **Strict Length Limit**: Subject line must be **72 characters or fewer**.
   * Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `security`.
3. **Hermetic Proof**: Include terminal outputs from Fontbakery and OTS validation in your PR description.
