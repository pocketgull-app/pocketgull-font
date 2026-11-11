// Pure Node.js SFNT parser, Windows Installer Manifest Sync, and Kaggle v4.0.0 Telemetry Generator.
// Zero unsigned native C-extensions (100% Smart App Control compliant).

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function parseSfnt(filePath) {
  const buf = fs.readFileSync(filePath);
  const sha256 = crypto.createHash('sha256').update(buf).digest('hex');
  const numTables = buf.readUInt16BE(4);
  const tables = new Map();

  for (let i = 0; i < numTables; i++) {
    const off = 12 + i * 16;
    const tag = buf.subarray(off, off + 4).toString('ascii');
    const tOff = buf.readUInt32BE(off + 8);
    const tLen = buf.readUInt32BE(off + 12);
    tables.set(tag, { offset: tOff, length: tLen });
  }

  // head table
  const head = tables.get('head');
  const fontRevFixed = buf.readInt32BE(head.offset + 4);
  const fontRevision = Number((fontRevFixed / 65536).toFixed(3));
  const upm = buf.readUInt16BE(head.offset + 18);
  const indexToLocFormat = buf.readInt16BE(head.offset + 50);

  // maxp table
  const maxp = tables.get('maxp');
  const numGlyphs = buf.readUInt16BE(maxp.offset + 4);

  // OS/2 table
  let weightClass = 400;
  let useTypoMetrics = false;
  let isMonospace = false;
  if (tables.has('OS/2')) {
    const os2 = tables.get('OS/2');
    weightClass = buf.readUInt16BE(os2.offset + 4);
    const bProportion = buf.readUInt8(os2.offset + 32 + 3);
    const fsSelection = buf.readUInt16BE(os2.offset + 62);
    useTypoMetrics = (fsSelection & 0x80) !== 0;
    isMonospace = bProportion === 9;
  }

  // post table
  if (tables.has('post')) {
    const post = tables.get('post');
    const isFixedPitch = buf.readUInt32BE(post.offset + 12);
    if (isFixedPitch !== 0) isMonospace = true;
  }

  // loca 2-byte word alignment
  let oddLocaOffsets = 0;
  if (tables.has('loca') && indexToLocFormat !== 0) {
    const loca = tables.get('loca');
    const count = Math.floor(loca.length / 4);
    for (let i = 0; i < count; i++) {
      const val = buf.readUInt32BE(loca.offset + i * 4);
      if (val % 2 !== 0) oddLocaOffsets++;
    }
  }

  const fpgmBytes = tables.has('fpgm') ? tables.get('fpgm').length : 0;
  const cvtBytes = tables.has('cvt ') ? tables.get('cvt ').length : 0;
  const hasGvar = tables.has('gvar');
  const hasMath = tables.has('MATH');
  const hasGpos = tables.has('GPOS');
  const hasGsub = tables.has('GSUB');

  // name table (decode UTF-16BE platformID 3 or 0, fallback platformID 1)
  const names = new Map();
  if (tables.has('name')) {
    const nameTbl = tables.get('name');
    const count = buf.readUInt16BE(nameTbl.offset + 2);
    const strStorage = nameTbl.offset + buf.readUInt16BE(nameTbl.offset + 4);
    for (let i = 0; i < count; i++) {
      const rec = nameTbl.offset + 6 + i * 12;
      const platformID = buf.readUInt16BE(rec);
      const encodingID = buf.readUInt16BE(rec + 2);
      const languageID = buf.readUInt16BE(rec + 4);
      const nameID = buf.readUInt16BE(rec + 6);
      const length = buf.readUInt16BE(rec + 8);
      const strOff = strStorage + buf.readUInt16BE(rec + 10);
      if (platformID === 3 && (languageID === 0x0409 || !names.has(nameID))) {
        let decoded = '';
        for (let b = 0; b + 1 < length; b += 2) {
          decoded += String.fromCharCode(buf.readUInt16BE(strOff + b));
        }
        if (decoded.trim()) names.set(nameID, decoded.trim());
      } else if (platformID === 1 && !names.has(nameID)) {
        const decoded = buf.subarray(strOff, strOff + length).toString('latin1').trim();
        if (decoded) names.set(nameID, decoded);
      }
    }
  }

  const familyName = names.get(16) || names.get(1) || path.basename(filePath, '.ttf');
  const subfamilyName = names.get(17) || names.get(2) || 'Regular';
  const fullName = names.get(4) || path.basename(filePath, '.ttf');
  const postScriptName = names.get(6) || path.basename(filePath, '.ttf');
  const versionString = names.get(5) || '';

  return {
    fileName: path.basename(filePath),
    relPath: path.relative(ROOT, filePath).replace(/\\/g, '/'),
    sizeBytes: buf.length,
    sizeKB: Number((buf.length / 1024).toFixed(1)),
    familyName,
    subfamilyName,
    fullName,
    postScriptName,
    versionString,
    fontRevision,
    upm,
    numGlyphs,
    weightClass,
    isMonospace,
    isVariable: hasGvar,
    hasOpenTypeMath: hasMath,
    hasGsub,
    hasGpos,
    useTypoMetrics,
    oddLocaOffsets,
    ots2ByteAligned: oddLocaOffsets === 0,
    fpgmVmBytes: fpgmBytes + cvtBytes,
    zeroBytecodeVm: (fpgmBytes + cvtBytes) === 0,
    sha256,
  };
}

function collectAllTtfs() {
  const ttfDir = path.join(ROOT, 'fonts', 'ttf');
  const upcycledDir = path.join(ROOT, 'distribution', 'upcycled');
  const files = [];

  for (const f of fs.readdirSync(ttfDir).sort()) {
    if (f.endsWith('.ttf')) files.push(path.join(ttfDir, f));
  }
  if (fs.existsSync(upcycledDir)) {
    for (const f of fs.readdirSync(upcycledDir).sort()) {
      if (f.endsWith('.ttf')) files.push(path.join(upcycledDir, f));
    }
  }
  return files.map(parseSfnt);
}

function csvEscape(val) {
  const s = String(val ?? '');
  if (s.includes(',') || s.includes('"') || s.includes('\n')) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function writeKaggleTelemetryCsv(records) {
  const columns = [
    'file_name',
    'relative_path',
    'family_name',
    'subfamily_name',
    'full_name',
    'postscript_name',
    'font_revision',
    'upm',
    'glyph_count',
    'weight_class',
    'is_monospace',
    'is_variable',
    'has_opentype_math',
    'has_gsub',
    'has_gpos',
    'use_typo_metrics',
    'ots_2byte_aligned',
    'odd_loca_offsets',
    'fpgm_vm_bytes',
    'size_kb',
    'sha256',
  ];

  const lines = [columns.join(',')];
  for (const r of records) {
    lines.push([
      r.fileName,
      r.relPath,
      r.familyName,
      r.subfamilyName,
      r.fullName,
      r.postScriptName,
      r.fontRevision.toFixed(1),
      r.upm,
      r.numGlyphs,
      r.weightClass,
      r.isMonospace,
      r.isVariable,
      r.hasOpenTypeMath,
      r.hasGsub,
      r.hasGpos,
      r.useTypoMetrics,
      r.ots2ByteAligned,
      r.oddLocaOffsets,
      r.fpgmVmBytes,
      r.sizeKB.toFixed(1),
      r.sha256,
    ].map(csvEscape).join(','));
  }

  const outCsv = path.join(ROOT, 'fonts', 'pocketgull_v4_sfnt_telemetry.csv');
  fs.writeFileSync(outCsv, lines.join('\n') + '\n', 'utf8');
  return outCsv;
}

function syncWindowsInstallerManifests(records) {
  const outDir = path.join(ROOT, 'distribution', 'windows-installer');
  const stageDir = path.join(outDir, 'stage_ttf');
  fs.rmSync(stageDir, { recursive: true, force: true });
  fs.mkdirSync(stageDir, { recursive: true });

  const skipAliases = new Set([
    'PocketGullSerif[wght].ttf',
    'PocketGull-Soft.ttf',
    'PocketGull-Sign-VF.ttf',
  ]);

  const seenFullNames = new Set();
  const entries = [];
  for (const r of records) {
    if (skipAliases.has(r.fileName)) continue;
    if (seenFullNames.has(r.fullName)) continue;
    seenFullNames.add(r.fullName);
    fs.copyFileSync(path.join(ROOT, r.relPath), path.join(stageDir, r.fileName));
    entries.push({ fileName: r.fileName, fullName: r.fullName });
  }

  // 1. Update specimen-info.rtf
  const rtf = [
    '{\\rtf1\\ansi\\deff0',
    '{\\fonttbl{\\f0\\fswiss\\fcharset0 Segoe UI;}{\\f1\\fmodern\\fcharset0 Consolas;}}',
    '{\\colortbl;\\red15\\green118\\blue110;\\red24\\green24\\blue27;\\red180\\green83\\blue9;}',
    '\\viewkind4\\uc1\\pard\\cf1\\b\\f0\\fs24 PocketGull Typeface Superfamily (v4.0.0)\\par',
    '\\cf2\\b0\\fs18 Sans, Serif, Slab, Monospace, Upcycled Display, and Technical Fonts\\par',
    '\\pard\\sa120\\sl276\\slmult1\\cf2\\fs18\\par',
    'Designed by \\b Phil Gear\\b0  (\\i The PocketGull Project Authors\\i0 ). PocketGull is an open-source typeface ',
    'family engineered for clinical interfaces, scientific publishing, and high-legibility technical documentation, ',
    'with explicit character disambiguation (\\b 0/O\\b0 , \\b 1/l/I\\b0 , \\b Z/2\\b0 , \\b b/d\\b0 , \\b p/q\\b0 ).\\par',
    `\\cf1\\b Included in this package (${entries.length} TrueType fonts):\\b0\\cf2\\par`,
    '\\f1\\fs16  - PocketGull Sans (Regular, Italic, Bold, BoldItalic, Black, Condensed)\\par',
    ' - PocketGull Display (Fineliner, Chiseltip, MarkerRaw, Halftone, Inline, Outline, Micro, Botanica, Kintsugi)\\par',
    ' - PocketGull Serif, Slab & Soft (Regular, Bold, Variable Fonts)\\par',
    ' - PocketGull Mono (Regular, Italic, Bold Fixed-Width Monospace)\\par',
    ' - PocketGull Technical & Accessibility (Math, Chem, Lab, Genome, Algo, Music, Numerics, Learn, Sign, ASL)\\par',
    '\\pard\\sa120\\sl276\\slmult1\\f0\\fs18\\par',
    '\\cf3\\b License:\\b0\\cf2  SIL Open Font License 1.1 (OFL-1.1) \\emdash  Free for commercial, clinical, academic, and personal use.\\par',
    '}',
  ].join('');
  fs.writeFileSync(path.join(outDir, 'assets', 'specimen-info.rtf'), rtf, 'ascii');

  // 2. Write Inno Setup (.iss)
  const issLines = [
    '; PocketGull Font Superfamily v4.0.0 — Official Windows & WinGet Installer',
    '[Setup]',
    'AppId={{8D692F2F-D44B-451D-A62F-E95528567C5F}',
    'AppName=PocketGull Font',
    'AppVersion=4.0.0',
    'AppVerName=PocketGull Font 4.0.0',
    'AppPublisher=The PocketGull Project Authors',
    'AppPublisherURL=https://font.pocketgull.app',
    'AppSupportURL=https://github.com/pocketgull-app/pocketgull-font/issues',
    'AppUpdatesURL=https://github.com/pocketgull-app/pocketgull-font/releases',
    'VersionInfoVersion=4.0.0.0',
    'VersionInfoCompany=The PocketGull Project Authors',
    'VersionInfoDescription=PocketGull Clinical & Scientific Typeface Installer',
    'VersionInfoCopyright=Copyright (c) 2026 The PocketGull Project Authors (OFL-1.1)',
    'DefaultDirName={autopf}\\PocketGull Font',
    'DisableDirPage=yes',
    'DisableProgramGroupPage=yes',
    'PrivilegesRequired=admin',
    'PrivilegesRequiredOverridesAllowed=dialog commandline',
    'OutputDir=dist',
    'OutputBaseFilename=PocketGull-Font-Setup-v4.0.0',
    'Compression=lzma2/ultra64',
    'SolidCompression=yes',
    'WizardStyle=modern',
    'WizardImageFile=assets\\wizard-banner.bmp',
    'WizardSmallImageFile=assets\\wizard-small.bmp',
    'SetupIconFile=assets\\pocketgull.ico',
    'UninstallDisplayIcon={app}\\pocketgull.ico',
    'UninstallDisplayName=PocketGull Font',
    'LicenseFile=..\\..\\OFL.txt',
    'InfoBeforeFile=assets\\specimen-info.rtf',
    'ArchitecturesInstallIn64BitMode=x64compatible',
    '',
    '[Languages]',
    'Name: "english"; MessagesFile: "compiler:Default.isl"',
    '',
    '[Files]',
    'Source: "assets\\pocketgull.ico"; DestDir: "{app}"; Flags: ignoreversion',
    'Source: "..\\..\\OFL.txt"; DestDir: "{app}"; Flags: ignoreversion',
    'Source: "..\\..\\README.md"; DestDir: "{app}"; Flags: ignoreversion',
  ];
  for (const e of entries) {
    issLines.push(`Source: "stage_ttf\\${e.fileName}"; DestDir: "{autofonts}"; FontInstall: "${e.fullName}"; Flags: ignoreversion restartreplace`);
  }
  fs.writeFileSync(path.join(outDir, 'PocketGullFont.iss'), issLines.join('\r\n') + '\r\n', 'utf8');

  // 3. Write NSIS (.nsi)
  const nsiLines = [
    '; PocketGull Font Superfamily v4.0.0 — Open-Source NSIS Installer (zlib/libpng license)',
    '!include "MUI2.nsh"',
    '!include "WinMessages.nsh"',
    '',
    'Name "PocketGull Font"',
    'OutFile "dist\\PocketGull-Font-Setup-v4.0.0.exe"',
    'Unicode True',
    'SetCompressor /SOLID lzma',
    'InstallDir "$PROGRAMFILES64\\PocketGull Font"',
    'RequestExecutionLevel admin',
    'BrandingText "PocketGull Typeface v4.0.0 (SIL OFL-1.1)"',
    '',
    'VIProductVersion "4.0.0.0"',
    'VIAddVersionKey "ProductName" "PocketGull Font"',
    'VIAddVersionKey "CompanyName" "The PocketGull Project Authors"',
    'VIAddVersionKey "FileDescription" "PocketGull Clinical & Scientific Typeface Installer"',
    'VIAddVersionKey "FileVersion" "4.0.0.0"',
    'VIAddVersionKey "ProductVersion" "4.0.0"',
    'VIAddVersionKey "LegalCopyright" "Copyright (c) 2026 The PocketGull Project Authors (OFL-1.1)"',
    '',
    '!define MUI_ICON "assets\\pocketgull.ico"',
    '!define MUI_UNICON "assets\\pocketgull.ico"',
    '!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\\nsis-welcome.bmp"',
    '!define MUI_UNWELCOMEFINISHPAGE_BITMAP "assets\\nsis-welcome.bmp"',
    '!define MUI_HEADERIMAGE',
    '!define MUI_HEADERIMAGE_BITMAP "assets\\nsis-header.bmp"',
    '!define MUI_HEADERIMAGE_RIGHT',
    '',
    '!define MUI_WELCOMEPAGE_TITLE "PocketGull Typeface Superfamily (v4.0.0)"',
    `!define MUI_WELCOMEPAGE_TEXT "This package installs ${entries.length} PocketGull TrueType fonts (Sans, Serif, Slab, Rounded, Fixed-Width Monospace, Upcycled Display, Mathematics, Sciences, Braille, and Sign Language) to your Windows Fonts folder.$\\r$\\n$\\r$\\nDesigned by Phil Gear (The PocketGull Project Authors) with explicit character disambiguation (0/O, 1/l/I, Z/2, b/d, p/q).$\\r$\\n$\\r$\\nLicense: SIL Open Font License 1.1 (OFL-1.1).$\\r$\\n$\\r$\\nClick Install to register the fonts on your system."`,
    '!define MUI_PAGE_CUSTOMFUNCTION_SHOW WelcomeChangeNextToInstall',
    '!insertmacro MUI_PAGE_WELCOME',
    '!insertmacro MUI_PAGE_INSTFILES',
    '!insertmacro MUI_PAGE_FINISH',
    '',
    '!insertmacro MUI_UNPAGE_CONFIRM',
    '!insertmacro MUI_UNPAGE_INSTFILES',
    '',
    '!insertmacro MUI_LANGUAGE "English"',
    '',
    'Function WelcomeChangeNextToInstall',
    '  GetDlgItem $0 $HWNDPARENT 1',
    '  SendMessage $0 ${WM_SETTEXT} 0 "STR:&Install"',
    'FunctionEnd',
    '',
    'Section "Install" SecMain',
    '  SetRegView 64',
    '  SetOutPath "$INSTDIR"',
    '  SetOverwrite try',
    '  File "assets\\pocketgull.ico"',
    '  File "..\\..\\OFL.txt"',
    '  File "..\\..\\README.md"',
    '',
    '  SetOutPath "$FONTS"',
  ];

  for (const e of entries) {
    nsiLines.push(`  File "stage_ttf\\${e.fileName}"`);
    nsiLines.push(`  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" "${e.fullName} (TrueType)" "${e.fileName}"`);
  }

  nsiLines.push(
    '',
    '  WriteUninstaller "$INSTDIR\\Uninstall.exe"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayName" "PocketGull Font"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayVersion" "4.0.0"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "Publisher" "The PocketGull Project Authors"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "URLInfoAbout" "https://font.pocketgull.app"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "DisplayIcon" "$INSTDIR\\pocketgull.ico"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "InstallLocation" "$INSTDIR"',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "UninstallString" "$\\"$INSTDIR\\Uninstall.exe$\\""',
    '  WriteRegStr HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "QuietUninstallString" "$\\"$INSTDIR\\Uninstall.exe$\\" /S"',
    '  WriteRegDWORD HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "NoModify" 1',
    '  WriteRegDWORD HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font" "NoRepair" 1',
    '  SetErrorLevel 0',
    'SectionEnd',
    '',
    'Section "Uninstall"',
    '  SetRegView 64',
  );

  for (const e of entries) {
    nsiLines.push(`  DeleteRegValue HKLM "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" "${e.fullName} (TrueType)"`);
    nsiLines.push(`  Delete /REBOOTOK "$FONTS\\${e.fileName}"`);
  }

  nsiLines.push(
    '  Delete "$INSTDIR\\pocketgull.ico"',
    '  Delete "$INSTDIR\\OFL.txt"',
    '  Delete "$INSTDIR\\README.md"',
    '  Delete "$INSTDIR\\Uninstall.exe"',
    '  RMDir "$INSTDIR"',
    '  DeleteRegKey HKLM "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PocketGull.Font"',
    '  SetErrorLevel 0',
    'SectionEnd',
  );

  fs.writeFileSync(path.join(outDir, 'PocketGullFont.nsi'), nsiLines.join('\r\n') + '\r\n', 'utf8');
  return entries;
}

function stageKaggleUploadBundle() {
  const stageDir = path.join(ROOT, 'local', 'kaggle_v4_upload');
  fs.rmSync(stageDir, { recursive: true, force: true });
  fs.mkdirSync(path.join(stageDir, 'fonts', 'ttf'), { recursive: true });
  fs.mkdirSync(path.join(stageDir, 'fonts', 'woff2'), { recursive: true });
  fs.mkdirSync(path.join(stageDir, 'distribution', 'upcycled'), { recursive: true });

  // 1. Copy Kaggle dataset-metadata.json to bundle root
  fs.copyFileSync(
    path.join(ROOT, 'distribution', 'kaggle', 'dataset-metadata.json'),
    path.join(stageDir, 'dataset-metadata.json'),
  );
  fs.copyFileSync(path.join(ROOT, 'OFL.txt'), path.join(stageDir, 'OFL.txt'));
  fs.copyFileSync(path.join(ROOT, 'CITATION.cff'), path.join(stageDir, 'CITATION.cff'));
  fs.copyFileSync(
    path.join(ROOT, 'fonts', 'pocketgull_v4_sfnt_telemetry.csv'),
    path.join(stageDir, 'fonts', 'pocketgull_v4_sfnt_telemetry.csv'),
  );
  fs.copyFileSync(
    path.join(ROOT, 'fonts', 'sri-hashes.json'),
    path.join(stageDir, 'fonts', 'sri-hashes.json'),
  );

  // 2. Copy all 39 TTFs + WOFF2s + 2 Upcycled cuts
  for (const f of fs.readdirSync(path.join(ROOT, 'fonts', 'ttf'))) {
    if (f.endsWith('.ttf')) {
      fs.copyFileSync(path.join(ROOT, 'fonts', 'ttf', f), path.join(stageDir, 'fonts', 'ttf', f));
    }
  }
  for (const f of fs.readdirSync(path.join(ROOT, 'fonts', 'woff2'))) {
    if (f.endsWith('.woff2')) {
      fs.copyFileSync(path.join(ROOT, 'fonts', 'woff2', f), path.join(stageDir, 'fonts', 'woff2', f));
    }
  }
  for (const f of fs.readdirSync(path.join(ROOT, 'distribution', 'upcycled'))) {
    if (f.endsWith('.ttf') || f.endsWith('.woff2')) {
      fs.copyFileSync(
        path.join(ROOT, 'distribution', 'upcycled', f),
        path.join(stageDir, 'distribution', 'upcycled', f),
      );
    }
  }
  return stageDir;
}

const records = collectAllTtfs();
const csvPath = writeKaggleTelemetryCsv(records);
const installerEntries = syncWindowsInstallerManifests(records);
const kaggleStageDir = stageKaggleUploadBundle();

console.log(JSON.stringify({
  totalTtfs: records.length,
  allOtsAligned: records.every(r => r.ots2ByteAligned),
  allZeroVm: records.every(r => r.zeroBytecodeVm),
  csvPath: path.relative(ROOT, csvPath),
  installerCount: installerEntries.length,
  kaggleStageDir: path.relative(ROOT, kaggleStageDir),
}, null, 2));
