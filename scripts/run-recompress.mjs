import { spawnSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const scriptPath = path.resolve(__dirname, 'recompress_woff2.py');

if (!fs.existsSync(scriptPath)) {
  console.warn('[WOFF2 Compressor] recompress_woff2.py not found. Skipping.');
  process.exit(0);
}

const args = process.argv.slice(2);
console.log('⚡ [WOFF2 Compressor] Compressing webfonts via Brotli Q11...');

// Strategy 1: Test native Python with fontTools and brotli
const pythonCmds = ['python', 'py'];
let executed = false;

for (const py of pythonCmds) {
  try {
    const check = spawnSync(py, ['-c', 'import fontTools, brotli'], { stdio: 'ignore', shell: true });
    if (check.status === 0) {
      console.log(`[WOFF2 Compressor] Running via native Python (${py})...`);
      const result = spawnSync(py, [scriptPath, ...args], {
        stdio: 'inherit',
        cwd: rootDir,
        shell: true,
      });
      executed = true;
      process.exit(result.status ?? 0);
    }
  } catch {}
}

// Strategy 2: Run via WSL with uv (cached fonttools & brotli)
if (!executed) {
  try {
    const wslScriptPath = scriptPath.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
    const wslWorkDir = rootDir.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
    const passedArgs = args.map(a => `"${a}"`).join(' ');

    const uvCandidates = [
      '/home/philg/.local/bin/uv',
      'uv',
    ];

    for (const uvBin of uvCandidates) {
      const check = spawnSync('wsl', ['--', uvBin, '--version'], { stdio: 'ignore' });
      if (check.status === 0) {
        console.log(`[WOFF2 Compressor] Running via WSL uv (${uvBin})...`);
        const result = spawnSync('wsl', [
          '--',
          'bash',
          '-c',
          `cd "${wslWorkDir}" && ${uvBin} run --with fonttools --with brotli python3 "${wslScriptPath}" ${passedArgs}`
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
    console.warn(`[WOFF2 Compressor] WSL execution note: ${err.message}`);
  }
}

if (!executed) {
  console.warn('[WOFF2 Compressor] Notice: Neither native Python nor WSL uv available. WOFF2 compression deferred.');
  process.exit(0);
}
