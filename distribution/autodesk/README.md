# PocketGull Typography for Autodesk (AutoCAD & Revit)

Brings **Louise Sloan 5:1 optotypic legibility** and **ISMP character disambiguation** standards to architectural, clinical hospital facility layout, and mechanical engineering blueprints.

## Why PocketGull for CAD?
* **Zero Number Misreads**: In critical construction and hospital gas line schematics, mistaking `0` for `8` or `1` for `7` or `l` causes catastrophic field errors. PocketGull provides slashed zeros (`0̸`), curved feet on `1` and `l`, and cross-slashed `Z`.
* **Standard 2.5 mm Optometric Text**: Calibrated to Louise Sloan 5:1 aspect ratios, ensuring legible dimension callouts on both 4K monitors and printed D-size (24" × 36") paper blueprints.

## AutoCAD Quick Setup (`pocketgull_setup.lsp`)

1. Ensure PocketGull TrueType fonts are installed on Windows (`winget install PocketGull.Typeface` or install from `fonts/ttf/`).
2. In AutoCAD, run the `APPLOAD` command (or type `(load "pocketgull_setup.lsp")`).
3. Three standard styles are automatically created and assigned:
   * `POCKETGULL-STANDARD`: General dimensions and room labels (`PocketGull-Fineliner.ttf`).
   * `POCKETGULL-MONO`: Coordinate tables, schedule blocks, and telemetry specs (`PocketGullMono-Regular.ttf`).
   * `POCKETGULL-BOLD`: Sheet titles and safety placards (`PocketGull-Bold.ttf`).

## Autodesk Revit Setup

1. Go to **Manage** > **Additional Settings** > **Annotation Styles** > **Dimension Styles**.
2. Select your dimension family (e.g. `Linear Dimension Style`).
3. Set **Text Font** to `PocketGull Fineliner` or `PocketGull`.
4. Set **Text Size** to `2.5 mm` (or `3/32"` imperial).
