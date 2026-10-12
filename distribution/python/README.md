# pocketgull-math — Python / Matplotlib Telemetry Integration

Drop-in Matplotlib styling and font registration for **PocketGull Math**, the world's first humanist clinical sans-serif OpenType math font.

## Quickstart

```python
import matplotlib.pyplot as plt
import pocketgull_math

# 1-Line Setup: registers font and applies clinical dark obsidian theme
pocketgull_math.use(theme="dark", vector_paths=True)

# Generate publication-grade clinical plot
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1], label=r'Chance ($\mathrm{AUC}=0.500$)')
ax.set_title(r'$\mathcal{L}_{\mathrm{ASL}} = - \sum_{k=1}^K y_k (1-p_k)^{\gamma_+} \log(p_k)$')
ax.legend()
plt.savefig("clinical_roc.svg")  # 100% self-contained vector paths!
```

## Kaggle & Google Colab Integration

In any Kaggle or Colab notebook cell:

```python
# 1. Install directly in notebook
!pip install -q git+https://github.com/pocketgull-app/pocketgull-font.git#subdirectory=distribution/python

# 2. 1-Line Setup
import matplotlib.pyplot as plt
import pocketgull_math

pocketgull_math.use(theme="dark", vector_paths=True)

# 3. Seaborn & Matplotlib figures automatically inherit Louise Sloan 5:1 optotypes!
import seaborn as sns
sns.set_theme(style="darkgrid", rc={"font.family": "PocketGull"})
```

## Features
* **Zero TeX Dependency**: Evaluates equations natively via Matplotlib's `mathtext` parser with OpenType `MATH` table parameters.
* **100% Visual Parity**: When `vector_paths=True` (default), SVGs and PDFs are saved as pure bezier curves—rendering identically on any machine without installing fonts.
* **Tabular Lining Numerals (`tnum`)**: Eliminates horizontal coordinate flutter during live streaming and video exports.
* **Dark Obsidian & Light Medical Styles**: Includes `pocketgull-dark.mplstyle`, `pocketgull-light.mplstyle`, and `pocketgull-astro-night.mplstyle` (650nm red OLED preservation).

