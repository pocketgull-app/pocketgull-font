# Upstream Feature Proposal: Dynamic HarfBuzz Shaping Verification for Salishan & Athabaskan Combining Sequences in Shaperglot

- **Target Repository**: [`googlefonts/shaperglot`](https://github.com/googlefonts/shaperglot) & [`googlefonts/fontbakery`](https://github.com/googlefonts/fontbakery)
- **Author**: The PocketGull Project Authors & Typefoundry Engineering Team
- **Date**: 2026-09-26
- **Category**: Feature Enhancement / Language Enablement QA / Indigenous Digital Sovereignty
- **Applicable Frameworks**: United Nations Declaration on the Rights of Indigenous Peoples (UNDRIP, Articles 13, 14, 31)

---

## 1. Executive Summary

`shaperglot` is Google Fonts' primary automated engine for testing language support across the open-source typeface catalog. Currently, Shaperglot determines language support primarily through **`cmap` character set intersection**, asserting that the individual Unicode codepoints required for an orthography exist in the font binary.

While this approach works effectively for European and Asian languages with precomposed Unicode code points, it produces a critical **false positive** for Pacific Northwest Indigenous orthographies (Lushootseed, Halkomelem, St'át'imcets, Nuxalk, Nuu-chah-nulth, Kwak'wala, Tlingit). These languages rely extensively on **uncomposed combining mark sequences**:

$$\text{Base Letter} + \text{U+0313 (Combining Comma Above)} + \text{U+02B7 (Modifier Letter Small W)}$$

When a font passes Shaperglot's `cmap` check but lacks OpenType GPOS `mark` anchors:
1. **The Rightward Displacement Defect**: Zero-width marks default to logical cursor positioning ($x = \text{advance}_{\text{base}}$), shifting **+236 UPM to +322 UPM** (46% to 54% of base advance) off the letter's optical center.
2. **Labializer Occlusion**: In labialized ejective stops (**q̓ʷ**, **k̓ʷ**), the rightward-displaced comma directly collides with superscript **ʷ** (`U+02B7`), rendering essential tribal health and educational materials as illegible black blobs.

We propose adding a lightweight, targeted **Dynamic HarfBuzz Mark Shaping Check** in Shaperglot for languages utilizing uncomposed ejective and glottal diacritic clusters.

---

## 2. Empirical Telemetry & Problem Demonstration

Testing conducted with HarfBuzz (`uharfbuzz`) on fonts that passed standard Google Fonts validation:

| Language | Sequence | Unicode Composition | Unanchored Behavior (Status Quo) | Calibrated GPOS Anchor Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Lushootseed** | **x̌** | `x` (`0078`) + `uni030C` (`030C`) | `x_off = 0` (Mark lands at $x = 551$, $+286$ UPM right-shifted) | `x_off = -305` (Mark centered at $x = 246$ UPM) |
| **Halkomelem** | **q̓** | `q` (`0071`) + `uni0313` (`0313`) | `x_off = 0, y_off = 0` (Mark cuts through bowl counter) | `x_off = -341, y_off = 140` (Mark elevated $+140$ UPM above bowl) |
| **St'át'imcets** | **q̓ʷ** | `q` + `uni0313` + `uni02B7` | Comma collides with $ʷ$ ($68$ UPM overlap) | Zero collision ($+273$ UPM clear negative space) |
| **Nuu-chah-nulth** | **ƛ̓** | `uni019B` + `uni0313` | Mark floats right into subsequent vowel | Mark centered over barred ascender apex ($x = 350$) |

### Cognitive & Clinical Impact
In rural tribal clinics and emergency departments using telemedicine portals:
- Patients and practitioners cannot distinguish a plain labialized uvular stop (**qʷ**) from an ejective labialized stop (**q̓ʷ**).
- Misidentifying dosage terms or anatomical directives introduces avoidable diagnostic and pharmaceutical risks.

---

## 3. Proposed Shaperglot Implementation

Rather than brute-force shaping of all possible combinations, Shaperglot can define an optional `shaping_checks` stanza in language definition YAML files for orthographies with known combining requirements:

```yaml
# languages/sal.yaml (Salishan Family)
name: Lushootseed / Halkomelem / Salishan Orthographies
shaping_checks:
  - sequence: "q\u0313"
    description: "Uvular ejective stop must center over bowl"
    assert_bounds:
      x_offset_min: -400
      x_offset_max: -100
      y_offset_min: 50
  - sequence: "x\u030C"
    description: "Uvular fricative with caron must center over centroid"
    assert_bounds:
      x_offset_min: -350
      x_offset_max: -150
  - sequence: "q\u0313\u02B7"
    description: "Labialized ejective must maintain positive clearance"
    assert_no_collision: true
```

### Python Verification Method (for `shaperglot/checker.py`)

```python
import uharfbuzz as hb

def check_ejective_mark_centering(font_path, base_char, mark_char):
    with open(font_path, "rb") as f:
        face = hb.Face(hb.Blob(f.read()))
    font = hb.Font(face)
    
    buf = hb.Buffer()
    buf.add_str(f"{base_char}{mark_char}")
    buf.guess_segment_properties()
    hb.shape(font, buf)
    
    positions = buf.glyph_positions
    base_pos = positions[0]
    mark_pos = positions[1]
    
    # If mark has x_offset == 0 on a wide base, it defaulted to advance cursor without GPOS
    if mark_pos.x_offset == 0 and base_pos.x_advance > 400:
        return False, f"Mark {mark_char!r} on {base_char!r} lacks GPOS centering (x_offset = 0)"
    
    return True, "Valid mark attachment"
```

---

## 4. UNDRIP Digital Sovereignty Alignment

The **United Nations Declaration on the Rights of Indigenous Peoples** states:
- **Article 13.1**: *"Indigenous peoples have the right to revitalize, use, develop and transmit to future generations their histories, languages, oral traditions, philosophies, writing systems and literatures..."*
- **Article 14.1**: *"Indigenous peoples have the right to establish and control their educational systems and institutions providing education in their own languages..."*

By enhancing Shaperglot to verify OpenType mark attachment for uncomposed Indigenous characters, Google Fonts can guarantee that fonts advertised as supporting Indigenous languages deliver authentic, legible, and respectful typographic quality out of the box.

---

## 5. Reference Implementation

PocketGull Typefoundry has implemented and verified this exact anchor matrix across 7 styles in production. Working code, OpenType feature syntax (`features.fea`), and HarfBuzz telemetry are available in the open-source repository:
- Repository: [https://github.com/pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)
- Full Technical Report: [`documentation/reports/salishan_combining_marks_and_osage_audit.md`](salishan_combining_marks_and_osage_audit.md)
