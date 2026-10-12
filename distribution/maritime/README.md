# PocketGull Typography for Marine Navigation & Aviation GIS (OpenCPN & QGIS)

Engineered for wheelhouse chart plotters, AIS radar overlays, and cockpit flight decks where vibration, salt spray, and extreme glare cause numerical misreads.

## Why PocketGull for Marine & Aviation?
* **Zero Coordinate Confusion**: Latitude and longitude minutes, seconds, and bearing degrees are rendered with tabular monospace numbers, eliminating coordinate drift during GPS track rendering.
* **Scotopic 650nm Red Mode**: Peak red wavelength emission preserves the watchkeeper's rhodopsin (dark adaptation) on night voyages while conserving bridge display battery power.

## QGIS Integration

1. In QGIS, open **Settings** > **Style Manager**.
2. Click **Import/Export** > **Import Items**.
3. Select [pocketgull_navigation_styles.xml](qgis/pocketgull_navigation_styles.xml).
4. Apply the `PocketGull Navigation Day` or `PocketGull Scotopic 650nm Night Vision` text format to your vector nautical charts, sounding soundings, and waypoint layers.
