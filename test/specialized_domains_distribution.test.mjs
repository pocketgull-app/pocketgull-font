import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Observability & NOC: Grafana CSS theme integrity', () => {
  const cssPath = path.join('distribution', 'observability', 'grafana-pocketgull.css');
  const readmePath = path.join('distribution', 'observability', 'README.md');

  assert.ok(fs.existsSync(cssPath), 'grafana-pocketgull.css must exist');
  assert.ok(fs.existsSync(readmePath), 'Observability README must exist');

  const css = fs.readFileSync(cssPath, 'utf8');
  assert.match(css, /PocketGull Mono/, 'Must configure PocketGull Mono');
  assert.match(css, /tabular-nums/, 'Must enforce tabular-nums');
  assert.match(css, /slashed-zero/, 'Must enforce slashed-zero');
});

test('Embedded Systems: LVGL header and conversion guide', () => {
  const hPath = path.join('distribution', 'embedded', 'lvgl', 'lv_font_pocketgull_16.h');
  const readmePath = path.join('distribution', 'embedded', 'README.md');

  assert.ok(fs.existsSync(hPath), 'lv_font_pocketgull_16.h must exist');
  assert.ok(fs.existsSync(readmePath), 'Embedded README must exist');

  const header = fs.readFileSync(hPath, 'utf8');
  assert.match(header, /lv_font_pocketgull_mono_16/, 'Must declare lv_font_pocketgull_mono_16');
  assert.match(header, /LV_FONT_POCKETGULL_16_H/, 'Must include header guard');
});

test('Clinical Pharmacy: ZPL prescription template integrity', () => {
  const zplPath = path.join('distribution', 'clinical-labels', 'zpl', 'prescription_label_ismp.zpl');
  const readmePath = path.join('distribution', 'clinical-labels', 'README.md');

  assert.ok(fs.existsSync(zplPath), 'prescription_label_ismp.zpl must exist');
  assert.ok(fs.existsSync(readmePath), 'Clinical labels README must exist');

  const zpl = fs.readFileSync(zplPath, 'utf8');
  assert.match(zpl, /\^XA/, 'ZPL must start with ^XA');
  assert.match(zpl, /\^XZ/, 'ZPL must end with ^XZ');
  assert.match(zpl, /hydrOXYzine/, 'Must demonstrate ISMP Tall Man lettering');
  assert.match(zpl, /hydrALAzine/, 'Must demonstrate lookalike collision warning');
});

test('Maritime & GIS: QGIS style XML definition integrity', () => {
  const xmlPath = path.join('distribution', 'maritime', 'qgis', 'pocketgull_navigation_styles.xml');
  const readmePath = path.join('distribution', 'maritime', 'README.md');

  assert.ok(fs.existsSync(xmlPath), 'pocketgull_navigation_styles.xml must exist');
  assert.ok(fs.existsSync(readmePath), 'Maritime README must exist');

  const xml = fs.readFileSync(xmlPath, 'utf8');
  assert.match(xml, /qgis_style/, 'Must declare valid qgis_style XML tag');
  assert.match(xml, /PocketGull Scotopic 650nm Night Vision/, 'Must define scotopic night vision textformat');
  assert.match(xml, /PocketGull Mono/, 'Must utilize PocketGull Mono for coordinates and soundings');
});
