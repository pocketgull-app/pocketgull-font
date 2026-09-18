import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const ROSETTA_JS_PATH = path.resolve('js/sign_notation_rosetta_data.js');

test('Sign Notation Rosetta: Dataset File and Global Exports', () => {
  assert.ok(fs.existsSync(ROSETTA_JS_PATH), 'sign_notation_rosetta_data.js must exist');
  const code = fs.readFileSync(ROSETTA_JS_PATH, 'utf8');

  // Execute in VM context simulating browser window
  const context = { window: {} };
  vm.createContext(context);
  vm.runInContext(code, context);

  const { SIGN_NOTATION_SYSTEMS, SIGN_NOTATION_ROSETTA } = context.window;

  assert.ok(SIGN_NOTATION_SYSTEMS, 'window.SIGN_NOTATION_SYSTEMS must be defined');
  assert.ok(Array.isArray(SIGN_NOTATION_ROSETTA), 'window.SIGN_NOTATION_ROSETTA must be an array');
  assert.equal(SIGN_NOTATION_ROSETTA.length, 10, 'Must contain exactly 10 canonical handshapes');
});

test('Sign Notation Rosetta: All 6 Notation Frameworks Registered', () => {
  const code = fs.readFileSync(ROSETTA_JS_PATH, 'utf8');
  const context = { window: {} };
  vm.createContext(context);
  vm.runInContext(code, context);

  const systems = context.window.SIGN_NOTATION_SYSTEMS;
  const requiredSystems = ['sutton', 'stokoe', 'hamnosys', 'imwa', 'aslphabet', 'si5s'];

  for (const sys of requiredSystems) {
    assert.ok(systems[sys], `System "${sys}" must be present in SIGN_NOTATION_SYSTEMS`);
    assert.ok(systems[sys].name, `System "${sys}" must have a name`);
    assert.ok(systems[sys].paradigm, `System "${sys}" must declare its notation paradigm`);
    assert.ok(systems[sys].developer, `System "${sys}" must cite its developer`);
  }
});

test('Sign Notation Rosetta: Sutton SignWriting Unicode Range Invariants', () => {
  const code = fs.readFileSync(ROSETTA_JS_PATH, 'utf8');
  const context = { window: {} };
  vm.createContext(context);
  vm.runInContext(code, context);

  const rosetta = context.window.SIGN_NOTATION_ROSETTA;

  for (const item of rosetta) {
    assert.ok(item.sutton, `Handshape ${item.id} must have Sutton data`);
    assert.ok(item.sutton.hex, `Handshape ${item.id} must have Sutton Unicode hex`);
    
    // Check codepoint falls within U+1D800 - U+1DAAF
    const cp = item.sutton.char.codePointAt(0);
    assert.ok(
      cp >= 0x1D800 && cp <= 0x1DAAF,
      `Handshape ${item.id} Sutton char ${item.sutton.char} (${cp.toString(16)}) must be in SignWriting block U+1D800-1DAAF`
    );
  }
});

test('Sign Notation Rosetta: Morphological Coverage Across All 5 Benedict Types', () => {
  const code = fs.readFileSync(ROSETTA_JS_PATH, 'utf8');
  const context = { window: {} };
  vm.createContext(context);
  vm.runInContext(code, context);

  const rosetta = context.window.SIGN_NOTATION_ROSETTA;
  const requiredTypes = ['alimentive', 'thoracic', 'muscular', 'osseous', 'cerebral'];

  for (const item of rosetta) {
    assert.ok(item.morphology, `Handshape ${item.id} must have morphology field`);
    for (const t of requiredTypes) {
      assert.ok(item.morphology[t], `Handshape ${item.id} must have morphology description for ${t}`);
      assert.ok(item.morphology[t].length > 20, `Handshape ${item.id} morphology for ${t} must be non-trivial`);
    }
    assert.ok(item.sloanCalibration, `Handshape ${item.id} must have Louise Sloan 5:1 calibration rule`);
    assert.match(item.sloanCalibration, /Sloan|UPM|stroke/i, `Handshape ${item.id} calibration must reference Sloan metrics`);
  }
});

test('Sign Notation Rosetta: Multi-System Cheremic and Phonetic Completeness', () => {
  const code = fs.readFileSync(ROSETTA_JS_PATH, 'utf8');
  const context = { window: {} };
  vm.createContext(context);
  vm.runInContext(code, context);

  const rosetta = context.window.SIGN_NOTATION_ROSETTA;

  for (const item of rosetta) {
    // Stokoe
    assert.ok(item.stokoeChereme, `Handshape ${item.id} must declare Stokoe Chereme`);
    assert.ok(item.stokoeDez, `Handshape ${item.id} must declare Stokoe Dez definition`);

    // HamNoSys
    assert.ok(item.hamnosys.code, `Handshape ${item.id} must declare HamNoSys code`);
    assert.ok(item.hamnosys.flexion, `Handshape ${item.id} must declare joint flexion angles`);

    // IMWA
    assert.ok(item.imwa.id, `Handshape ${item.id} must declare IMWA catalog ID`);
    assert.ok(item.imwa.group, `Handshape ${item.id} must declare IMWA group`);

    // ASL-phabet
    assert.ok(item.aslphabet.graphemeId, `Handshape ${item.id} must declare ASL-phabet grapheme ID`);
    assert.ok(item.aslphabet.pediatricNote, `Handshape ${item.id} must declare pediatric literacy note`);

    // Si5s
    assert.ok(item.si5s.mark, `Handshape ${item.id} must declare Si5s digit/mark`);
    assert.ok(item.si5s.ductus, `Handshape ${item.id} must declare handwritten ductus kinetic flow`);
  }
});
