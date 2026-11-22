import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();

test('FACTS Invariant: All 52 self-hosted zero-fallback OFL WOFF2 companions exist and are wired in fonts.css', () => {
  const dir = path.join(ROOT, 'fonts/woff2/companions');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.woff2')).sort();
  assert.equal(files.length, 52, `Expected 52 self-hosted WOFF2 companions, found ${files.length}`);
  const fontsCss = fs.readFileSync(path.join(ROOT, 'fonts.css'), 'utf8');

  for (const f of files) {
    const rel = `fonts/woff2/companions/${f}`;
    const stat = fs.statSync(path.join(dir, f));
    assert.ok(stat.size > 1024, `Companion WOFF2 unexpectedly small (${stat.size} bytes): ${rel}`);
    assert.ok(fontsCss.includes(rel), `fonts.css must reference self-hosted companion: ${rel}`);
  }
});

test('FACTS Invariant: Public surfaces contain zero stale v3.1/38-Cut/32-style/unverified-CJK claims', () => {
  const checkedFiles = [
    'README.md',
    'llms.txt',
    'commercial.html',
    'commercial-success.html',
    'specimen-broadside.html',
  ];
  const bannedPatterns = [
    /\b38-Cut\b/,
    /\b38 Cuts\b/,
    /\b32-style\b/,
    /Top 3,500 Hanzi/,
    /\b2-Axis Variable\b/,
  ];

  for (const rel of checkedFiles) {
    const text = fs.readFileSync(path.join(ROOT, rel), 'utf8');
    for (const rx of bannedPatterns) {
      assert.doesNotMatch(text, rx, `Stale or unverified claim (${rx}) found in ${rel}`);
    }
  }
});

test('FACTS Invariant: fonts/ttf/ maintains full 41-cut v4.0.0 production inventory', () => {
  const ttfs = fs
    .readdirSync(path.join(ROOT, 'fonts/ttf'))
    .filter((f) => f.endsWith('.ttf'));
  assert.equal(ttfs.length, 41, `Expected 41 TTF binaries in fonts/ttf/, found ${ttfs.length}`);
});

// Pure-Node WOFF2 table directory security scanner (zero Python/external deps)
const WOFF2_KNOWN_TAGS = [
  'cmap','head','hhea','hmtx','maxp','name','OS/2','post','cvt ','fpgm',
  'glyf','loca','prep','CFF ','VORG','EBDT','EBLC','gasp','hdmx','kern',
  'LTSH','PCLT','VDMX','vhea','vmtx','BASE','GDEF','GPOS','GSUB','EBSC',
  'JSTF','MATH','CBDT','CBLC','COLR','CPAL','SVG ','sbix','acnt','avar',
  'bdat','bloc','bsln','cvar','fdsc','feat','fmtx','fvar','gvar','hsty',
  'just','lcar','mort','morx','opbd','prop','trak','Zapf','Silf','Glat',
  'Gloc','Feat','Sill',
];
const BANNED_COMPANION_TAGS = new Set([
  'fpgm', 'prep', 'cvt ', 'CFF ', 'CFF2', 'Wasm', 'Silf', 'Glat', 'Gloc', 'Feat', 'Sill',
]);

function readUIntBase128(buf, offset) {
  let accum = 0;
  for (let i = 0; i < 5; i++) {
    const b = buf[offset++];
    accum = (accum << 7) | (b & 0x7f);
    if ((b & 0x80) === 0) return [accum, offset];
  }
  throw new Error('Invalid WOFF2 UIntBase128');
}

function parseWoff2TableTags(buf) {
  assert.equal(buf.subarray(0, 4).toString('ascii'), 'wOF2', 'Invalid WOFF2 magic');
  const numTables = buf.readUInt16BE(12);
  let off = 48; // WOFF2 header is 48 bytes
  const tags = [];
  for (let i = 0; i < numTables; i++) {
    const flags = buf[off++];
    const idx = flags & 0x3f;
    let tag;
    if (idx === 63) {
      tag = buf.subarray(off, off + 4).toString('ascii');
      off += 4;
    } else {
      tag = WOFF2_KNOWN_TAGS[idx];
    }
    tags.push(tag);
    // origLength
    [, off] = readUIntBase128(buf, off);
    // transformLength present for glyf/loca when transformVersion == 0, or non-zero transformVersion for others
    const xform = (flags >> 6) & 0x03;
    const isGlyfOrLoca = tag === 'glyf' || tag === 'loca';
    if ((isGlyfOrLoca && xform === 0) || (!isGlyfOrLoca && xform !== 0)) {
      [, off] = readUIntBase128(buf, off);
    }
  }
  return tags;
}

test('Security Invariant: Every self-hosted WOFF2 companion is pure glyf with 0 bytecode/Wasm/CFF/Graphite tables (and Hangul has 0 GSUB)', () => {
  const dir = path.join(ROOT, 'fonts/woff2/companions');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.woff2'));
  assert.equal(files.length, 52, `Expected 52 WOFF2 companions, found ${files.length}`);
  for (const f of files) {
    const tags = parseWoff2TableTags(fs.readFileSync(path.join(dir, f)));
    assert.ok(tags.includes('glyf'), `${f} must use pure TrueType glyf outlines`);
    const banned = tags.filter((t) => BANNED_COMPANION_TAGS.has(t));
    assert.deepEqual(banned, [], `${f} contains banned executable/VM/CFF tables: ${banned.join(', ')}`);
    if (f === 'PocketGull-Korean-Companion.woff2') {
      assert.ok(!tags.includes('GSUB'), 'Hangul companion must strip GSUB (precomposed syllables only)');
    }
  }
});
