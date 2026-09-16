# pocketgull-math — Humanist Clinical OpenType Math Font for LaTeX

* **Package Name**: `pocketgull-math`
* **Version**: 3.100 (2026/09/15)
* **Author**: The PocketGull Project Authors
* **License**: SIL Open Font License 1.1 (Font) / LaTeX Project Public License 1.3c (Package code)
* **CTAN Archive Location**: `macros/latex/contrib/pocketgull-math`
* **Engines Supported**: LuaLaTeX, XeLaTeX (`unicode-math`)

---

## Description
`pocketgull-math` provides seamless LaTeX integration for the PocketGull Math superfamily (`PocketGull-Math.ttf`), the world's first humanist clinical sans-serif OpenType math font. 

Featuring complete ISO/IEC 14496-22 `MATH` table parameters (`AxisHeight = 260 UPM`, `ScriptPercentScaleDown = 70%`, `FractionRuleThickness = 68 UPM`), PocketGull Math is engineered for dark-mode telemetry, high-contrast healthcare dashboards, and publication-grade mathematical papers where legibility and ISMP life-critical character disambiguation are paramount.

---

## Installation

### In TeX Live / MacTeX (Global)
Place the files in your local TeX directory:
```bash
# Style file:
TEXMFHOME/tex/latex/pocketgull-math/pocketgull-math.sty

# Documentation:
TEXMFHOME/doc/latex/pocketgull-math/pocketgull-math.pdf
TEXMFHOME/doc/latex/pocketgull-math/README.md

# TrueType Math Font:
TEXMFHOME/fonts/truetype/pocketgull/PocketGull-Math.ttf
```
Then refresh the filename database:
```bash
texhash
# or: mktexlsr
```

---

## Basic Usage

Compile with **LuaLaTeX** or **XeLaTeX**:

```latex
\documentclass{article}
\usepackage{amsmath, mathtools}
\usepackage[slashedzero, curvedl, serifedI]{pocketgull-math}

\begin{document}
The asymmetric loss is:
\[
\mathcal{L}_{\mathrm{ASL}} = - \sum_{k=1}^K y_k (1 - p_k)^{\gamma_+} \log(p_k)
\]
\end{document}
```

---

## Package Options

| Option | Default | Description |
| :--- | :--- | :--- |
| `slashedzero` | `false` | Enables OpenType `cv08` slashed zero ($0̸$) to prevent confusion with capital $O$. |
| `curvedl` | `false` | Enables OpenType `cv05` curved lowercase $l$ foot to eliminate $1 / l / I$ ambiguity. |
| `serifedI` | `false` | Enables OpenType `ss02` bilobe serifed capital $I$. |
| `tabular` | `false` | Enables OpenType `tnum` tabular lining numerals for zero-jitter alignment. |
| `fontpath=<dir>`| empty | Explicit relative or absolute path to directory containing `PocketGull-Math.ttf`. |

---

## Repository & Development
* Upstream Repository: [https://github.com/pocketgull-app/pocketgull-font](https://github.com/pocketgull-app/pocketgull-font)
* Issue Tracker: [https://github.com/pocketgull-app/pocketgull-font/issues](https://github.com/pocketgull-app/pocketgull-font/issues)
