import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Autodesk Integration: AutoLISP script and README integrity', () => {
  const lspPath = path.join('distribution', 'autodesk', 'pocketgull_setup.lsp');
  const readmePath = path.join('distribution', 'autodesk', 'README.md');

  assert.ok(fs.existsSync(lspPath), 'pocketgull_setup.lsp must exist');
  assert.ok(fs.existsSync(readmePath), 'Autodesk README.md must exist');

  const lspContent = fs.readFileSync(lspPath, 'utf8');
  assert.match(lspContent, /defun\s+c:PocketGullSetup/, 'Must define c:PocketGullSetup command');
  assert.match(lspContent, /POCKETGULL-STANDARD/, 'Must define POCKETGULL-STANDARD style');
  assert.match(lspContent, /POCKETGULL-MONO/, 'Must define POCKETGULL-MONO style');
  assert.match(lspContent, /POCKETGULL-BOLD/, 'Must define POCKETGULL-BOLD style');
  assert.match(lspContent, /DIMTXSTY/, 'Must configure DIMTXSTY system variable');
});
