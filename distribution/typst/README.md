# Typst Package: pocketgull-math

**PocketGull Math** package for [Typst](https://typst.app), enabling humanist clinical sans-serif mathematical typesetting with OpenType `MATH` table parameters and ISMP character disambiguation.

## Quickstart

Import the package in your `.typ` document:

```typst
#import "@preview/pocketgull-math:3.1.0": *

#show: pocketgull-math-rules.with(
  slashed-zero: true,
  curved-l: true,
  serifed-I: true,
  dark-mode: true,  // Clinical obsidian dark theme
)

$ L_ASL = - sum_(k=1)^K y_k (1 - p_k)^(gamma_+) log(p_k) $
```

## Features
- **Slashed Zero (`cv08`)**: Clearly distinguishes $0$ from $O$.
- **Curved `l` (`cv05`)**: Resolves ambiguity with numeral $1$ and capital $I$.
- **Dark-Mode Calibrated**: Solid $68\text{ UPM}$ operator stem width prevents the hairline wash-out common with Computer Modern on OLED screens.
- **OpenType Math Compliance**: Seamless integration with Typst's native math equation engine.
