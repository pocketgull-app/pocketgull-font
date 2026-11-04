import { spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');

// Target validate_fonts.py
const candidatePaths = [
  path.resolve(rootDir, 'sources', 'validate_fonts.py'),
  path.resolve(rootDir, 'validate_fonts.py'),
];

const scriptPath = candidatePaths.find(p => fs.existsSync(p));

if (!scriptPath) {
  console.warn('[Font Validator] Warning: validate_fonts.py not found in workspace candidate paths. Skipping.');
  process.exit(0);
}

const scriptDir = path.dirname(scriptPath);
const typefaceDir = path.resolve(scriptDir, '..');

console.log(`🔤 [Font Validator] Target: ${scriptPath}`);

// Strategy 1: Run via persistent WSL2 Ubuntu runtime (avoids Windows Smart App Control blocks on host python.exe)
let executed = false;
try {
  const wslScriptPath = scriptPath.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
  const wslWorkDir = typefaceDir.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');

  const uvCandidates = [
    '/home/philg/.local/bin/uv',
    'uv',
  ];

  for (const uvBin of uvCandidates) {
    const check = spawnSync('wsl', ['-d', 'Ubuntu', '--', uvBin, '--version'], { stdio: 'ignore' });
    if (check.status === 0) {
      console.log(`[Font Validator] Running via WSL2 Ubuntu uv (${uvBin})...`);
      const result = spawnSync('wsl', [
        '-d',
        'Ubuntu',
        '--',
        'bash',
        '-c',
        `cd "${wslWorkDir}" && ${uvBin} run --with fonttools python3 "${wslScriptPath}"`
      ], {
        stdio: 'inherit',
      });

      if (result.status === 0) {
        executed = true;
        process.exit(0);
      } else {
        process.exit(result.status ?? 1);
      }
    }
  }
} catch (err) {
  console.warn(`[Font Validator] WSL2 Ubuntu execution note: ${err.message}`);
}

// Strategy 2: Fallback to Pure-Dart 3.11 Compliance Auditor
if (!executed) {
  console.log('[Font Validator] Falling back to Pure-Dart 3.11 Compliance Auditor...');
  const dartRes = spawnSync('dart', ['run', 'tool/pocketgull_foundry.dart', 'compliance'], {
    stdio: 'inherit',
    cwd: typefaceDir,
  });
  process.exit(dartRes.status ?? 0);
}
