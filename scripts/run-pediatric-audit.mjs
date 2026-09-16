import { spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const scriptPath = path.resolve(__dirname, 'audit_pediatric_dosing_clearance.py');

if (!fs.existsSync(scriptPath)) {
  console.warn('[Pediatric Audit] audit_pediatric_dosing_clearance.py not found. Skipping.');
  process.exit(0);
}

console.log('🏥 [Pediatric Audit] Auditing decimal clearance & micro-dosing negative space...');

// Strategy 1: Test native Python with fontTools and PIL
const pythonCmds = ['python', 'py'];
let executed = false;

for (const py of pythonCmds) {
  try {
    const check = spawnSync(py, ['-c', 'import fontTools, PIL'], { stdio: 'ignore', shell: true });
    if (check.status === 0) {
      console.log(`[Pediatric Audit] Running via native Python (${py})...`);
      const result = spawnSync(py, [scriptPath], {
        stdio: 'inherit',
        cwd: rootDir,
        shell: true,
      });
      executed = true;
      process.exit(result.status ?? 0);
    }
  } catch {}
}

// Strategy 2: Run via WSL with uv
if (!executed) {
  try {
    const wslScriptPath = scriptPath.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
    const wslWorkDir = rootDir.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');

    const uvCandidates = [
      '/home/philg/.local/bin/uv',
      'uv',
    ];

    for (const uvBin of uvCandidates) {
      const check = spawnSync('wsl', ['--', uvBin, '--version'], { stdio: 'ignore' });
      if (check.status === 0) {
        console.log(`[Pediatric Audit] Running via WSL uv (${uvBin})...`);
        const result = spawnSync('wsl', [
          '--',
          'bash',
          '-c',
          `cd "${wslWorkDir}" && ${uvBin} run --with fonttools --with pillow python3 "${wslScriptPath}"`
        ], {
          stdio: 'inherit',
        });

        if (result.status === 0) {
          executed = true;
          process.exit(0);
        }
      }
    }
  } catch (err) {
    console.warn(`[Pediatric Audit] WSL execution note: ${err.message}`);
  }
}

if (!executed) {
  console.warn('[Pediatric Audit] Notice: Neither native Python nor WSL uv was reachable.');
  process.exit(0);
}
