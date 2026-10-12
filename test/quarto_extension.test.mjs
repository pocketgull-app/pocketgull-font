import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Quarto Extension: manifest _extension.yml structure and formats', () => {
  const extPath = path.join('distribution', 'quarto', '_extension.yml');
  assert.ok(fs.existsSync(extPath), '_extension.yml must exist');
  const yamlContent = fs.readFileSync(extPath, 'utf8');

  // Verify extension metadata
  assert.match(yamlContent, /title:\s*PocketGull Math Academic Format/, 'Extension title must match');
  assert.match(yamlContent, /version:\s*3\.1\.0/, 'Version must match SemVer 3.1.0');
  assert.match(yamlContent, /quarto-required:\s*">=1\.4\.0"/, 'Must require Quarto >= 1.4.0');

  // Verify format contributions
  assert.match(yamlContent, /theme:\s*\[cosmo,\s*pocketgull-math\.scss\]/, 'HTML format must include pocketgull-math.scss');
  assert.match(yamlContent, /mainfont:\s*"PocketGull"/, 'Mainfont must be PocketGull');
  assert.match(yamlContent, /monofont:\s*"PocketGull Mono"/, 'Monofont must be PocketGull Mono');
  assert.match(yamlContent, /pdf-engine:\s*xelatex/, 'PDF engine must be xelatex');
  assert.match(yamlContent, /\\setmathfont\{PocketGull-Math\.ttf\}/, 'Must declare unicode-math PocketGull-Math.ttf');
  assert.match(yamlContent, /pocketgull-math-html:/, 'Must declare pocketgull-math-html format');
  assert.match(yamlContent, /pocketgull-math-pdf:/, 'Must declare pocketgull-math-pdf format');
});

test('Quarto Extension: SCSS theme rules and OpenType feature flags', () => {
  const scssPath = path.join('distribution', 'quarto', 'pocketgull-math.scss');
  assert.ok(fs.existsSync(scssPath), 'pocketgull-math.scss must exist');
  const scssContent = fs.readFileSync(scssPath, 'utf8');

  // Verify scss sections and font fallback stacks
  assert.match(scssContent, /\/\*-- scss:defaults --\*\//, 'Must declare SCSS defaults section');
  assert.match(scssContent, /\/\*-- scss:rules --\*\//, 'Must declare SCSS rules section');
  assert.match(scssContent, /\$font-family-sans-serif:\s*"PocketGull"/, 'Must configure default sans-serif font');
  assert.match(scssContent, /\$font-family-monospace:\s*"PocketGull Mono"/, 'Must configure default monospace font');

  // Verify math and telemetry rules
  assert.match(scssContent, /\.math,\s*\.katex,\s*\.MathJax/, 'Must target math containers');
  assert.match(scssContent, /"cv05"\s*1,\s*"cv08"\s*1,\s*"ss02"\s*1,\s*"tnum"\s*1/, 'Must enable ISMP disambiguation on math');
  assert.match(scssContent, /"zero"\s*1/, 'Must enable slashed zero on code blocks');
});

test('Quarto Extension: scientific template and README documentation', () => {
  const templatePath = path.join('distribution', 'quarto', 'template.qmd');
  const readmePath = path.join('distribution', 'quarto', 'README.md');

  assert.ok(fs.existsSync(templatePath), 'template.qmd must exist');
  assert.ok(fs.existsSync(readmePath), 'README.md must exist');

  const templateContent = fs.readFileSync(templatePath, 'utf8');
  assert.match(templateContent, /pocketgull-math-pdf:\s*default/, 'Template must use pocketgull-math-pdf');
  assert.match(templateContent, /pocketgull-math-html:\s*default/, 'Template must use pocketgull-math-html');
  assert.match(templateContent, /C_p\(t\)\s*=/, 'Template must feature pharmacokinetic equations');

  const readmeContent = fs.readFileSync(readmePath, 'utf8');
  assert.match(readmeContent, /quarto add pocketgull-app\/pocketgull-font\/distribution\/quarto/, 'README must specify valid git add path');
});
