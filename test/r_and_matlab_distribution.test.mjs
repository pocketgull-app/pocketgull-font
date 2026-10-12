import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('R Package: DESCRIPTION and theme_pocketgull.R integrity', () => {
  const descPath = path.join('distribution', 'r', 'DESCRIPTION');
  const rThemePath = path.join('distribution', 'r', 'R', 'theme_pocketgull.R');
  const readmePath = path.join('distribution', 'r', 'README.md');

  assert.ok(fs.existsSync(descPath), 'R DESCRIPTION must exist');
  assert.ok(fs.existsSync(rThemePath), 'R theme_pocketgull.R must exist');
  assert.ok(fs.existsSync(readmePath), 'R README.md must exist');

  const descContent = fs.readFileSync(descPath, 'utf8');
  assert.match(descContent, /Package:\s*pocketgullr/, 'Package name must be pocketgullr');
  assert.match(descContent, /Version:\s*3\.1\.0/, 'Version must match SemVer 3.1.0');
  assert.match(descContent, /Imports:\s*[\r\n]+\s*ggplot2/, 'Must import ggplot2');

  const rThemeContent = fs.readFileSync(rThemePath, 'utf8');
  assert.match(rThemeContent, /theme_pocketgull\s*<-\s*function/, 'Must export theme_pocketgull function');
  assert.match(rThemeContent, /use_pocketgull\s*<-\s*function/, 'Must export use_pocketgull function');
  assert.match(rThemeContent, /#f43f5e/, 'Must define scotopic 650nm red color token');
});

test('MATLAB Integration: theme_pocketgull.m and README integrity', () => {
  const mScriptPath = path.join('distribution', 'matlab', 'theme_pocketgull.m');
  const readmePath = path.join('distribution', 'matlab', 'README.md');

  assert.ok(fs.existsSync(mScriptPath), 'theme_pocketgull.m must exist');
  assert.ok(fs.existsSync(readmePath), 'MATLAB README.md must exist');

  const mContent = fs.readFileSync(mScriptPath, 'utf8');
  assert.match(mContent, /function\s+theme_pocketgull/, 'Must declare theme_pocketgull function');
  assert.match(mContent, /fontName\s*=\s*'PocketGull';/, 'Must configure PocketGull font');
  assert.match(mContent, /scotopic/, 'Must support scotopic mode');
  assert.match(mContent, /findall\(fig,\s*'Type',\s*'axes'\)/, 'Must update all axes on figure');
});
