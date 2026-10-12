# arXiv Submission Guide: PocketGull Math & Clinical Typography

This guide details how authors can submit papers typeset with **PocketGull Math** and **PocketGull Sans** to [arXiv](https://arxiv.org).

---

## 1. The arXiv TeX Engine Reality

* **Default arXiv Engine**: arXiv compiles submissions using standard **pdfLaTeX** by default.
* **LuaLaTeX / XeLaTeX on arXiv**: While arXiv primarily compiles with pdfLaTeX, arXiv officially supports pre-generated PDFs via the **PDF-only submission track** or using self-contained Type 1 / OpenType font embeddings.

There are two recommended approaches for arXiv submission:

---

## 2. Approach A: Direct PDF Submission (Recommended for arXiv)

For full OpenType math (`MATH` table, ISMP character disambiguation, slashed zeroes, and Sloan optotypes):

1. **Compile Locally** using **LuaLaTeX** or **XeLaTeX**:
   ```bash
   xelatex paper.tex
   bibtex paper
   xelatex paper.tex
   xelatex paper.tex
   ```
2. **Submit directly to arXiv** under the PDF format option:
   * Select **"PDF only"** submission on arXiv.org.
   * Attach your final compiled `paper.pdf`.
   * OpenType fonts (`PocketGull-Math.ttf` and `PocketGull-Fineliner.ttf`) are fully embedded inside the PDF as vector subsets, guaranteeing bit-exact rendering across all devices.

---

## 3. Approach B: Source Submission with Self-Contained Font Directory

If submitting full LaTeX source code to arXiv using LuaTeX:

1. Place `pocketgull-math.sty` and the font binaries in your paper's root directory:
   ```
   my-arxiv-paper/
   ├── paper.tex
   ├── references.bib
   ├── pocketgull-math.sty
   ├── PocketGull-Math.ttf
   ├── PocketGull-Fineliner.ttf
   └── PocketGull-Bold.ttf
   ```

2. Point to the local directory in `paper.tex`:
   ```latex
   \documentclass{article}
   \usepackage{amsmath, mathtools}
   \usepackage[fontpath=./, slashedzero, curvedl, serifedI]{pocketgull-math}

   \setmainfont{PocketGull-Fineliner.ttf}[
     Path = ./,
     BoldFont = PocketGull-Bold.ttf
   ]

   \begin{document}
   \title{Louise Sloan 5:1 Optotypes in Clinical Machine Learning}
   \author{Jane Doe \and John Smith}
   \maketitle

   The pharmacokinetic decay is modeled as:
   \[
   C_p(t) = \left[ \frac{D \cdot k_a}{V_d (k_a - k_e)} \right] \left( e^{-k_e t} - e^{-k_a t} \right)
   \]
   \end{document}
   ```

3. Include an `00README.XXX` file at the root telling arXiv's automated build processor:
   ```
   paper.tex xelatex
   ```

---

## 4. Figures & Plots (Matplotlib / Python / R) for arXiv

If generating figures with Python (`matplotlib`) or R (`ggplot2`):
* Always export figures as **PDF** or **SVG with vector paths**:
  ```python
  import pocketgull_math
  pocketgull_math.use(theme="light", vector_paths=True)
  # All text and math symbols compile to pure Bézier paths!
  plt.savefig("figure1.pdf") 
  ```
* This ensures arXiv's PDF compiler never throws missing font errors during build.
