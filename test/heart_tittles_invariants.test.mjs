import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

function parseSfntTables(buf) {
  const sfntVersion = buf.readUInt32BE(0);
  assert.equal(sfntVersion, 0x00010000, 'Must be SFNT TrueType 0x00010000');
  const numTables = buf.readUInt16BE(4);
  const tables = {};
  for (let i = 0; i < numTables; i++) {
    const off = 12 + i * 16;
    const tag = buf.subarray(off, off + 4).toString('ascii');
    const tOff = buf.readUInt32BE(off + 8);
    const tLen = buf.readUInt32BE(off + 12);
    tables[tag] = buf.subarray(tOff, tOff + tLen);
  }
  return tables;
}

function getSortedGsubFeatures(gsubBuf) {
  const flOffset = gsubBuf.readUInt16BE(6);
  const featureCount = gsubBuf.readUInt16BE(flOffset);
  const tags = [];
  const lookupsByTag = {};
  for (let i = 0; i < featureCount; i++) {
    const recOff = flOffset + 2 + i * 6;
    const tag = gsubBuf.subarray(recOff, recOff + 4).toString('ascii');
    const fOff = flOffset + gsubBuf.readUInt16BE(recOff + 4);
    const lookupCount = gsubBuf.readUInt16BE(fOff + 2);
    const lidxs = [];
    for (let k = 0; k < lookupCount; k++) {
      lidxs.push(gsubBuf.readUInt16BE(fOff + 4 + k * 2));
    }
    tags.push(tag);
    lookupsByTag[tag] = lidxs;
  }
  return { tags, lookupsByTag };
}

test('Philocardia Invariant: All 38 non-Sign TTFs expose sorted cv09, cv10, cv19, ss07..ss11 before liga & zero split-brain', () => {
  const ttfDir = path.join('fonts', 'ttf');
  const skip = new Set(['PocketGull-ASL.ttf', 'PocketGull-Sign.ttf', 'PocketGull-Sign-VF.ttf']);
  const files = fs.readdirSync(ttfDir).filter(f => f.endsWith('.ttf') && !skip.has(f)).sort();
  assert.equal(files.length, 38, 'Expected 38 non-Sign TTF files');

  const expectedTags = ['cv09', 'cv10', 'cv19', 'ss07', 'ss08', 'ss09', 'ss10', 'ss11'];
  for (const file of files) {
    const buf = fs.readFileSync(path.join(ttfDir, file));
    assert.equal(buf.length % 2, 0, `${file} must be 2-byte aligned`);
    const tables = parseSfntTables(buf);
    assert.ok(tables.GSUB, `${file} must have GSUB table`);

    const { tags, lookupsByTag } = getSortedGsubFeatures(tables.GSUB);
    const sortedTags = [...tags].sort();
    assert.deepEqual(tags, sortedTags, `${file} GSUB FeatureList must be alphabetically sorted`);

    for (const t of expectedTags) {
      assert.ok(lookupsByTag[t]?.length >= 1, `${file} must expose GSUB feature ${t}`);
    }
    assert.equal(lookupsByTag.cv09.length, 1, `${file} cv09 must reference 1 letter lookup`);
    assert.equal(lookupsByTag.cv10.length, 1, `${file} cv10 must reference 1 punctuation lookup`);
    assert.equal(lookupsByTag.cv19.length, 1, `${file} cv19 must reference 1 dotless stem lookup`);
    assert.deepEqual(
      lookupsByTag.ss07,
      [lookupsByTag.cv09[0], lookupsByTag.cv10[0]],
      `${file} ss07 must combine cv09 and cv10 lookups cleanly`
    );

    if (lookupsByTag.liga?.length) {
      const minLiga = Math.min(...lookupsByTag.liga);
      for (const t of expectedTags) {
        assert.ok(
          Math.max(...lookupsByTag[t]) < minLiga,
          `${file} ${t} lookups (${lookupsByTag[t]}) must execute strictly before liga (${minLiga})`
        );
      }
    }
  }
});

test('Philocardia Invariant: Root, ofl, apache & tracked distribution mirrors match canonical fonts/ binaries byte-for-byte', () => {
  const checkMirror = (mirrorPath, canonPath) => {
    assert.ok(fs.existsSync(canonPath), `Canonical binary missing for ${mirrorPath}`);
    const a = fs.readFileSync(mirrorPath);
    const b = fs.readFileSync(canonPath);
    assert.equal(Buffer.compare(a, b), 0, `Stale mirror detected: ${mirrorPath} != ${canonPath}`);
  };

  for (const file of fs.readdirSync('.')) {
    if (file.startsWith('PocketGull') && (file.endsWith('.ttf') || file.endsWith('.woff2'))) {
      if (file.includes('-ASL.') || file.includes('-Sign')) continue;
      const canon = path.join('fonts', file.endsWith('.ttf') ? 'ttf' : 'woff2', file);
      checkMirror(file, canon);
    }
  }

  for (const dir of ['ofl', 'apache']) {
    for (const sub of fs.readdirSync(dir)) {
      const subDir = path.join(dir, sub);
      if (!fs.statSync(subDir).isDirectory()) continue;
      for (const file of fs.readdirSync(subDir)) {
        if (file.endsWith('.ttf')) {
          checkMirror(path.join(subDir, file), path.join('fonts', 'ttf', file));
        }
      }
    }
  }

  const distDirs = [
    path.join('distribution', 'python', 'pocketgull_math', 'fonts'),
    path.join('distribution', 'r', 'inst', 'fonts'),
    path.join('distribution', 'upcycled'),
  ];
  for (const d of distDirs) {
    if (!fs.existsSync(d)) continue;
    for (const file of fs.readdirSync(d)) {
      if (file.endsWith('.ttf') || file.endsWith('.woff2')) {
        const canon = path.join('fonts', file.endsWith('.ttf') ? 'ttf' : 'woff2', file);
        if (fs.existsSync(canon)) {
          checkMirror(path.join(d, file), canon);
        }
      }
    }
  }
});

test('Philocardia Invariant: Web CSS & HTML wire all 6 varieties, 6 glyphs, cv19 dotless stems & monochrome text emoji', () => {
  const css = fs.readFileSync('fonts.css', 'utf8');
  for (const cls of [
    '.font-feature-hearts',
    '.font-feature-hearts-punct',
    '.font-feature-hearts-suite',
    '.font-feature-blossom',
    '.font-feature-nuqta',
    '.font-feature-star',
    '.font-feature-droplet',
    '.font-feature-punct-dotless',
    '.philocardia-question',
    '.philocardia-excl-down',
    '.philocardia-question-down',
    '.philocardia-stillness::after',
  ]) {
    assert.ok(css.includes(cls), `fonts.css must define ${cls}`);
  }
  assert.ok(css.includes('"cv19" 1'), 'fonts.css must enable cv19 dotless stems on Philocardia spans');
  assert.ok(css.includes('font-variant-emoji: text'), 'fonts.css must enforce monochrome text emoji presentation');
  assert.ok(css.includes('--tittle-translate: translateX(-50%)'), '.philocardia-excl::after must set --tittle-translate');
  assert.ok(css.includes('var(--tittle-translate, translate(-50%, -50%))'), 'keyframes must honor --tittle-translate');

  const html = fs.readFileSync('index.html', 'utf8');
  assert.ok(html.includes('id="ismpHeartComparison" aria-label="clinical"'), '#ismpHeartComparison must have aria-label="clinical"');
  assert.ok(html.includes("activeVar === 'blossom'"), 'index.html must map non-heart varieties to ss08..ss11 without ss07 bleed');
  assert.ok(html.includes('philocardia-question'), 'index.html must wrap question marks');
  assert.ok(html.includes('philocardia-question-down'), 'index.html must wrap inverted question marks');

  for (const file of ['js/closed_caption_studio.js', 'closed_caption_studio.html']) {
    const src = fs.readFileSync(file, 'utf8');
    assert.ok(src.includes('philocardia-excl'), `${file} must wrap exclamation marks`);
    assert.ok(src.includes('philocardia-question'), `${file} must wrap question marks`);
    assert.ok(src.includes('philocardia-excl-down'), `${file} must wrap inverted exclamation marks`);
    assert.ok(src.includes('philocardia-question-down'), `${file} must wrap inverted question marks`);
  }

  const broadside = fs.readFileSync('specimen-broadside.html', 'utf8');
  assert.ok(broadside.includes("comp.style.fontFeatureSettings = 'normal'"), 'specimen-broadside.html must restore clean dot mode');
  assert.ok(broadside.includes('[data-tittle-variety="blossom"] .ismp-feat-heart'), 'specimen-broadside.html must style ss08..ss11 variety rules');
  assert.ok(broadside.includes('id="broadsideHeartComparison" aria-label="clinical"'), 'specimen-broadside.html must set aria-label="clinical"');
  assert.ok(broadside.includes("getElementById('broadsideHeartBpmBadge')"), 'specimen-broadside.html must wire #broadsideHeartBpmBadge click cycler');

  const posters = fs.readFileSync('posters_gallery.html', 'utf8');
  for (const tag of ['"ss07" 1', '"ss08" 1', '"ss09" 1', '"ss10" 1', '"ss11" 1']) {
    assert.ok(posters.includes(tag), `posters_gallery.html must showcase ${tag}`);
  }
  assert.ok(posters.includes('i j ! ? ¡ ¿'), 'posters_gallery.html must showcase all 6 Philocardia characters');

  const tactileLab = fs.readFileSync('philocardia_tactile_lab.html', 'utf8');
  for (const cls of ['philocardia-heart', 'philocardia-j', 'philocardia-excl', 'philocardia-question', 'philocardia-excl-down', 'philocardia-question-down']) {
    assert.ok(tactileLab.includes(cls), `philocardia_tactile_lab.html must map ${cls}`);
  }

  const stemStudio = fs.readFileSync('stem_studio.html', 'utf8');
  assert.ok(!stemStudio.includes('TouchMath Subitizing Numerals (ss08)'), 'stem_studio.html must not conflate PUA TouchMath numerals with Philocardia Blossom ss08');
  assert.ok(!stemStudio.includes('?v=3.100'), 'stem_studio.html must use SSOT ?v=4.0.0 preload strings');

  const musicStudio = fs.readFileSync('music_studio.html', 'utf8');
  assert.ok(!musicStudio.includes('?v=3.100'), 'music_studio.html must use SSOT ?v=4.0.0 preload strings');

  const specimenJs = fs.readFileSync('js/specimen.js', 'utf8');
  assert.ok(specimenJs.includes('.philocardia-question-down'), 'js/specimen.js ambient aura must cover all 6 Philocardia classes');
});
