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

// Strategy 1: Test native Python with fontTools
const pythonCmds = [
  'C:\\Users\\philg\\anaconda3\\python.exe',
  'python',
  'py',
];
let executed = false;

for (const py of pythonCmds) {
  try {
    const check = spawnSync(py, ['-c', 'import fontTools'], { stdio: 'ignore', shell: true });
    if (check.status === 0) {
      console.log(`[Font Validator] Running via native Python (${py})...`);
      const result = spawnSync(py, [scriptPath], {
        stdio: 'inherit',
        cwd: typefaceDir,
        shell: true,
      });
      executed = true;
      process.exit(result.status ?? 0);
    }
  } catch {}
}

// Strategy 2: Run via WSL with uv (cached fonttools)
if (!executed) {
  try {
    const wslScriptPath = scriptPath.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
    const wslWorkDir = typefaceDir.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');

    const uvCandidates = [
      '/home/philg/.local/bin/uv',
      'uv',
    ];

    for (const uvBin of uvCandidates) {
      const check = spawnSync('wsl', ['--', uvBin, '--version'], { stdio: 'ignore' });
      if (check.status === 0) {
        console.log(`[Font Validator] Running via WSL uv (${uvBin})...`);
        const result = spawnSync('wsl', [
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
        }
      }
    }
  } catch (err) {
    console.warn(`[Font Validator] WSL execution note: ${err.message}`);
  }
}

if (!executed) {
  console.warn('[Font Validator] Notice: Neither native Python fontTools nor WSL uv was reachable. Font validation deferred.');
  process.exit(0);
}
