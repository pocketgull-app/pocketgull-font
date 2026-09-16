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

## Features
* **Zero TeX Dependency**: Evaluates equations natively via Matplotlib's `mathtext` parser with OpenType `MATH` table parameters.
* **100% Visual Parity**: When `vector_paths=True` (default), SVGs are saved as pure bezier curves—rendering identically for viewers without the font installed.
* **Tabular Lining Numerals (`tnum`)**: Eliminates horizontal coordinate flutter during live streaming.
* **Dark Obsidian & Light Medical Styles**: Includes `pocketgull-dark.mplstyle` and `pocketgull-light.mplstyle`.
