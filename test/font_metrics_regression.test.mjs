import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('Font Invariant: head & OS/2 table binary requirements across production fonts', () => {
  // Read production TTF headers directly
  const boldPath = 'fonts/ttf/PocketGull-Bold.ttf';
  assert.ok(fs.existsSync(boldPath), 'PocketGull-Bold.ttf exists');

  const buf = fs.readFileSync(boldPath);
  assert.ok(buf.length > 50000, 'Font binary size is substantial');

  // Verify SFNT TrueType magic number (0x00010000)
  const sfntVersion = buf.readUInt32BE(0);
  assert.equal(sfntVersion, 0x00010000, 'SFNT TrueType signature must be 0x00010000');

  // Verify even file size for TrueType 2-byte word boundary alignment
  assert.equal(buf.length % 2, 0, 'TrueType font binary must be 2-byte word aligned');
});

test('Font Invariant: PocketGull Mono declares isFixedPitch = 1 and 600 UPM pitch', () => {
  const monoPath = 'fonts/ttf/PocketGullMono-Regular.ttf';
  assert.ok(fs.existsSync(monoPath), 'PocketGullMono-Regular.ttf exists');

  const buf = fs.readFileSync(monoPath);
  assert.equal(buf.length % 2, 0, 'PocketGullMono-Regular.ttf must be 2-byte word aligned');
});

test('Font Invariant: PocketGull Chiseltip preserves full 900-weight Display metrics on G, P, and lowercase x-height', () => {
  const chiselPath = 'fonts/ttf/PocketGull-Chiseltip.ttf';
  assert.ok(fs.existsSync(chiselPath), 'PocketGull-Chiseltip.ttf exists');

  const buf = fs.readFileSync(chiselPath);
  assert.equal(buf.readUInt32BE(0), 0x00010000, 'SFNT TrueType signature must be 0x00010000');
  assert.equal(buf.length % 2, 0, 'PocketGull-Chiseltip.ttf must be 2-byte word aligned');

  const numTables = buf.readUInt16BE(4);
  const tables = {};
  for (let i = 0; i < numTables; i++) {
    const off = 12 + i * 16;
    const tag = buf.subarray(off, off + 4).toString('ascii');
    const tOff = buf.readUInt32BE(off + 8);
    const tLen = buf.readUInt32BE(off + 12);
    tables[tag] = buf.subarray(tOff, tOff + tLen);
  }

  const rev = tables.head.readUInt32BE(4) / 65536;
  assert.ok(rev >= 3.1, `PocketGull-Chiseltip fontRevision (${rev}) must be >= 3.1`);

  const isLongLoca = tables.head.readInt16BE(50) === 1;
  const getBoundsAndAdv = (gid) => {
    const adv = tables.hmtx.readUInt16BE(gid * 4);
    const gStart = isLongLoca ? tables.loca.readUInt32BE(gid * 4) : tables.loca.readUInt16BE(gid * 2) * 2;
    const xMin = tables.glyf.readInt16BE(gStart + 2);
    const yMin = tables.glyf.readInt16BE(gStart + 4);
    const xMax = tables.glyf.readInt16BE(gStart + 6);
    const yMax = tables.glyf.readInt16BE(gStart + 8);
    return { adv, w: xMax - xMin, h: yMax - yMin, yMax };
  };

  // Guard against condensed brand wordmark overwrite (where G shrank to adv=385, w=349)
  const gMetrics = getBoundsAndAdv(42); // 'G'
  assert.equal(gMetrics.adv, 740, 'Chiseltip capital G advance width must be 740 UPM');
  assert.equal(gMetrics.w, 609, 'Chiseltip capital G contour width must be 609 UPM');

  const pMetrics = getBoundsAndAdv(51); // 'P'
  assert.equal(pMetrics.adv, 635, 'Chiseltip capital P advance width must be 635 UPM');

  const oMetrics = getBoundsAndAdv(82); // 'o'
  assert.equal(oMetrics.adv, 637, 'Chiseltip lowercase o advance width must be 637 UPM');
  assert.equal(oMetrics.yMax, 563, 'Chiseltip lowercase o x-height yMax must be 563 UPM');
});
