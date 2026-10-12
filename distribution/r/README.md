# pocketgullr: Clinical Typography for R & ggplot2

The `pocketgullr` package brings **PocketGull's Louise Sloan 5:1 optotypic legibility** and **ISMP character disambiguation** standards to R graphics and `ggplot2`.

## Installation

Install directly from GitHub via `remotes` or `pak`:

```r
# Using remotes
remotes::install_github("pocketgull-app/pocketgull-font", subdir = "distribution/r")

# Or using pak
pak::pkg_install("pocketgull-app/pocketgull-font/distribution/r")
```

## Quick Start with ggplot2

```r
library(ggplot2)
library(pocketgullr)

# 1. Register PocketGull fonts for R graphics devices
use_pocketgull()

# 2. Plot with optotypic acuity
ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  labs(
    title = "Clinical Pharmacokinetics & Biomarker Clearance",
    subtitle = "Louise Sloan 5:1 optotypes with ISMP character disambiguation",
    x = "Weight (1000 lbs)",
    y = "Clearance Velocity (mL/min)",
    color = "Cylinders"
  ) +
  theme_pocketgull()
```

### Scotopic 650nm Red Mode (Night Shift / OLED Battery Saving)

```r
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point(color = "#f43f5e", size = 3) +
  theme_pocketgull(mode = "scotopic")
```
