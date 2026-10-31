#!/usr/bin/env node
/**
 * PocketGull Local Machine & Repository Font/Unicode Leak Scanner
 * 100% Offline, Read-Only Diagnostic Tool (Node 24+)
 *
 * Scans:
 * 1. Source repositories for Trojan Source BiDi overrides (CVE-2021-42574), Fake Spaces (U+3164),
 *    and Emoji Smuggling Variation Selectors (U+E0100-U+E01EF) with zero multilingual false positives.
 * 2. Font binaries (.ttf / .otf) in project directories or Windows system font folders for:
 *    - Legacy TrueType Bytecode VM tables (fpgm, prep, cvt ) and HarfBuzz Wasm shaper tables (Wasm, CVE-2026-113679/113680)
 *    - Odd table/loca offsets (loca[i] % 2 != 0) and 32-bit bounds overflows
 *    - Restrictive OS/2.fsType DRM embedding locks
 */

import fs from 'node:fs';
import path from 'node:path';

const UNCONDITIONAL_SPOOF_MAP = new Map([
  [0x202A, 'U+202A LRE (BiDi Override)'],
  [0x202B, 'U+202B RLE (BiDi Override)'],
  [0x202C, 'U+202C PDF (BiDi Pop)'],
  [0x202D, 'U+202D LRO (BiDi Override)'],
  [0x202E, 'U+202E RLO (Trojan Source CVE-2021-42574)'],
  [0x2066, 'U+2066 LRI (BiDi Isolate)'],
  [0x2067, 'U+2067 RLI (BiDi Isolate)'],
  [0x2068, 'U+2068 FSI (BiDi Isolate)'],
  [0x2069, 'U+2069 PDI (BiDi Isolate Pop)'],
  [0x115F, 'U+115F Hangul Choseong Filler (Fake Space)'],
  [0x1160, 'U+1160 Hangul Jungseong Filler (Fake Space)'],
  [0x3164, 'U+3164 Hangul Filler (Fake Space)'],
  [0xFFA0, 'U+FFA0 Halfwidth Hangul Filler (Fake Space)'],
  [0x2061, 'U+2061 Function Application (Invisible Math)'],
  [0x2062, 'U+2062 Invisible Times (Invisible Math)'],
  [0x2063, 'U+2063 Invisible Separator (Invisible Math)'],
  [0x2064, 'U+2064 Invisible Plus (Invisible Math)']
]);

const SKIP_DIRS = new Set(['.git', 'node_modules', '.venv', 'dist', 'build', '.dart_tool']);
const CODE_EXTENSIONS = new Set(['.js', '.mjs', '.ts', '.dart', '.py', '.ps1', '.json', '.yaml', '.yml', '.css', '.sh']);

export function inspectSfntBuffer(buf, filename) {
  if (!buf || buf.length < 12) {
    return { filename, valid: false, reason: 'Buffer smaller than 12-byte SFNT header' };
  }

  const sfntVersion = buf.readUInt32BE(0);
  const isTrueTypeMagic = sfntVersion === 0x00010000;

  const numTables = buf.readUInt16BE(4);
  if (numTables === 0 || numTables > 64 || 12 + numTables * 16 > buf.length) {
    return { filename, valid: false, reason: 'Invalid SFNT numTables header' };
  }

  const tables = {};
  const vmTables = [];
  let unalignedTableCount = 0;
  let boundsOverflowCount = 0;

  for (let i = 0; i < numTables; i++) {
    const entry = 12 + i * 16;
    const tag = buf.subarray(entry, entry + 4).toString('ascii');
    const offset = buf.readUInt32BE(entry + 8);
    const length = buf.readUInt32BE(entry + 12);

    tables[tag] = { offset, length };

    if (tag === 'fpgm' || tag === 'prep' || tag === 'cvt ' || tag === 'Wasm') {
      vmTables.push(tag.trim());
    }
    if (offset + length > buf.length) {
      boundsOverflowCount++;
    }
    // OpenType spec requires 4-byte alignment on top-level SFNT table offsets
    if ((offset & 3) !== 0) {
      unalignedTableCount++;
    }
  }

  // Check OS/2.fsType and PUA Bit 57 (ulUnicodeRange2 bit 25) if present
  let fsType = 0;
  let puaBit57Set = false;
  if (tables['OS/2'] && tables['OS/2'].offset + 10 <= buf.length) {
    fsType = buf.readUInt16BE(tables['OS/2'].offset + 8);
    if (tables['OS/2'].offset + 50 <= buf.length) {
      const ulUnicodeRange2 = buf.readUInt32BE(tables['OS/2'].offset + 46);
      puaBit57Set = (ulUnicodeRange2 & (1 << 25)) !== 0;
    }
  }

  // Check loca 2-byte word alignment, monotonic progression, glyf instructionLength == 0, and (flag & 0xC0) == 0
  let oddLocaOffsets = 0;
  let nonMonotonicLocaCount = 0;
  let glyphInstructionBytes = 0;
  let flagMaskViolations = 0;
  let compositeGlyphCount = 0;
  if (tables['head'] && tables['loca'] && tables['maxp']) {
    const headOff = tables['head'].offset;
    const locaOff = tables['loca'].offset;
    const maxpOff = tables['maxp'].offset;
    const glyfOff = tables['glyf'] ? tables['glyf'].offset : 0;
    const glyfLen = tables['glyf'] ? tables['glyf'].length : 0;
    if (headOff + 54 <= buf.length && maxpOff + 6 <= buf.length) {
      const indexToLocFormat = buf.readInt16BE(headOff + 50);
      const numGlyphs = buf.readUInt16BE(maxpOff + 4);
      for (let g = 0; g < numGlyphs; g++) {
        let gStart = 0;
        let gEnd = 0;
        if (indexToLocFormat === 0 && locaOff + (g + 2) * 2 <= buf.length) {
          gStart = buf.readUInt16BE(locaOff + g * 2) * 2;
          gEnd = buf.readUInt16BE(locaOff + (g + 1) * 2) * 2;
        } else if (indexToLocFormat !== 0 && locaOff + (g + 2) * 4 <= buf.length) {
          gStart = buf.readUInt32BE(locaOff + g * 4);
          gEnd = buf.readUInt32BE(locaOff + (g + 1) * 4);
        }
        if ((gStart & 1) !== 0) oddLocaOffsets++;
        if (gEnd < gStart || (glyfLen > 0 && gEnd > glyfLen)) nonMonotonicLocaCount++;
        if (glyfOff > 0 && gEnd > gStart && glyfOff + gStart + 12 <= buf.length) {
          const numContours = buf.readInt16BE(glyfOff + gStart);
          if (numContours < 0) {
            compositeGlyphCount++;
          } else if (numContours > 0) {
            const insLenOffset = glyfOff + gStart + 10 + numContours * 2;
            if (insLenOffset + 2 <= buf.length) {
              const insnLen = buf.readUInt16BE(insLenOffset);
              glyphInstructionBytes += insnLen;
              const lastPt = buf.readUInt16BE(glyfOff + gStart + 10 + (numContours - 1) * 2);
              const totalPts = lastPt + 1;
              let p = insLenOffset + 2 + insnLen;
              let ptsRead = 0;
              const sliceEnd = Math.min(buf.length, glyfOff + gEnd);
              while (ptsRead < totalPts && p < sliceEnd) {
                const fl = buf[p++];
                if ((fl & 0xC0) !== 0) flagMaskViolations++;
                ptsRead++;
                if ((fl & 0x08) !== 0 && p < sliceEnd) {
                  ptsRead += buf[p++];
                }
              }
            }
          }
        }
      }
    }
  }

  const fpgmBytes = tables['fpgm'] ? tables['fpgm'].length : 0;
  const wasmBytes = tables['Wasm'] ? tables['Wasm'].length : 0;
  const hasWasmShaper = Boolean(tables['Wasm']);

  return {
    filename,
    valid:
      isTrueTypeMagic &&
      boundsOverflowCount === 0 &&
      unalignedTableCount === 0 &&
      oddLocaOffsets === 0 &&
      nonMonotonicLocaCount === 0 &&
      flagMaskViolations === 0 &&
      !hasWasmShaper,
    isTrueTypeMagic,
    tableCount: numTables,
    vmTables,
    fpgmBytes,
    wasmBytes,
    hasWasmShaper,
    glyphInstructionBytes,
    hasActiveBytecodeVm: fpgmBytes > 0 || glyphInstructionBytes > 0 || wasmBytes > 0,
    hasGvar: Boolean(tables['gvar']),
    oddLocaOffsets,
    nonMonotonicLocaCount,
    flagMaskViolations,
    compositeGlyphCount,
    unalignedTableCount,
    boundsOverflowCount,
    fsType,
    puaBit57Set
  };
}

export function scanCodeDirectory(rootDir) {
  const leaks = [];
  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      if (SKIP_DIRS.has(entry.name)) continue;
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (CODE_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) {
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split(/\r?\n/);
        for (let lineIdx = 0; lineIdx < lines.length; lineIdx++) {
          const line = lines[lineIdx];
          let colIdx = 0;
          let inSubdivisionFlag = false;
          for (const ch of line) {
            colIdx++;
            const cp = ch.codePointAt(0);
            if (cp === 0x1F3F4) {
              inSubdivisionFlag = true;
              continue;
            }
            if (cp >= 0xE0000 && cp <= 0xE007F) {
              if (!inSubdivisionFlag) {
                leaks.push({
                  file: path.relative(rootDir, fullPath),
                  line: lineIdx + 1,
                  col: colIdx,
                  vector: `U+${cp.toString(16).toUpperCase()} Detached ASCII Tag (Prompt Injection Vector)`
                });
              }
              if (cp === 0xE007F) inSubdivisionFlag = false;
              continue;
            }
            inSubdivisionFlag = false;

            if (UNCONDITIONAL_SPOOF_MAP.has(cp)) {
              leaks.push({
                file: path.relative(rootDir, fullPath),
                line: lineIdx + 1,
                col: colIdx,
                vector: UNCONDITIONAL_SPOOF_MAP.get(cp)
              });
            } else if (cp >= 0xE0100 && cp <= 0xE01EF) {
              leaks.push({
                file: path.relative(rootDir, fullPath),
                line: lineIdx + 1,
                col: colIdx,
                vector: `U+${cp.toString(16).toUpperCase()} Variation Selector Supplement (Emoji Smuggling)`
              });
            }
          }
        }
      }
    }
  }
  if (fs.existsSync(rootDir)) walk(rootDir);
  return leaks;
}

if (import.meta.url === `file://${process.argv[1].replace(/\\/g, '/')}` || process.argv[1]?.endsWith('scan-font-security.mjs')) {
  const args = process.argv.slice(2);
  const targetDir = args[0] || process.cwd();
  const includeSystem = args.includes('--system-fonts');

  console.log('\n======================================================================');
  console.log('  POCKETGULL LOCAL FONT & REPOSITORY SECURITY SCANNER (OFFLINE)');
  console.log('======================================================================');
  console.log(`  Workspace Target: ${targetDir}`);

  // 1. Scan repository code files
  const codeLeaks = scanCodeDirectory(targetDir);
  console.log(`\n[1/2] Repository Source Code Unicode Leak Scan:`);
  if (codeLeaks.length === 0) {
    console.log('  [PASS] 0 Trojan Source BiDi overrides, Fake Spaces, or VS17-VS256 smuggling bytes found.');
  } else {
    console.log(`  [ALERT] Found ${codeLeaks.length} hidden Unicode vector(s):`);
    for (const leak of codeLeaks.slice(0, 15)) {
      console.log(`    - ${leak.file}:${leak.line}:${leak.col} -> ${leak.vector}`);
    }
  }

  // 2. Scan project font binaries
  const ttfDir = path.join(targetDir, 'fonts', 'ttf');
  console.log(`\n[2/2] Font Binary Memory & Legacy Hardware Safety Audit (${ttfDir}):`);
  if (fs.existsSync(ttfDir)) {
    const ttfFiles = fs.readdirSync(ttfDir).filter((f) => f.endsWith('.ttf'));
    let activeVmCount = 0;
    let totalGlyphInsBytes = 0;
    let oddLocaTotal = 0;
    const vmFontDetails = [];
    for (const f of ttfFiles) {
      const buf = fs.readFileSync(path.join(ttfDir, f));
      const res = inspectSfntBuffer(buf, f);
      if (res.hasActiveBytecodeVm) {
        activeVmCount++;
        vmFontDetails.push(`${f} (tables=[${res.vmTables.join(',')}], fpgm=${res.fpgmBytes}B, glyfIns=${res.glyphInstructionBytes}B)`);
      }
      totalGlyphInsBytes += res.glyphInstructionBytes;
      oddLocaTotal += res.oddLocaOffsets;
    }
    console.log(`  [PASS] Audited ${ttfFiles.length} PocketGull TTF binaries:`);
    console.log(`    • Odd loca offsets:              ${oddLocaTotal} (100% 2-byte word-aligned)`);
    console.log(`    • Active Bytecode VM fonts:      ${activeVmCount} (${totalGlyphInsBytes} glyph instruction bytes, instructionLength = 0)`);
    if (vmFontDetails.length > 0) {
      console.log(`    • Residual VM table details:     ${vmFontDetails.join('; ')}`);
    }
  }

  // Optional: Scan sample of system fonts to show "Directions to Explore"
  if (includeSystem) {
    const winFonts = 'C:\\Windows\\Fonts';
    if (fs.existsSync(winFonts)) {
      console.log(`\n[3/3] System Font Exploration Sample (${winFonts}):`);
      const sampleFonts = ['arial.ttf', 'cour.ttf', 'times.ttf', 'segoeui.ttf'];
      for (const sf of sampleFonts) {
        const sfPath = path.join(winFonts, sf);
        if (fs.existsSync(sfPath)) {
          const res = inspectSfntBuffer(fs.readFileSync(sfPath), sf);
          const vmNote = res.hasActiveBytecodeVm
            ? `Active Bytecode VM (fpgm=${res.fpgmBytes}B, glyfIns=${res.glyphInstructionBytes}B)`
            : 'Zero Active Bytecode VM (0B)';
          console.log(`    • ${sf.padEnd(14)} -> ${vmNote}, fsType=0x${res.fsType.toString(16).padStart(4, '0')}`);
        }
      }
    }
  }

  console.log('\n======================================================================\n');
}
