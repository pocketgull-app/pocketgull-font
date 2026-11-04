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
console.log('⚡ [WOFF2 Compressor] Compressing webfonts via Brotli Q11 (WSL2 Ubuntu persistent runtime)...');

let executed = false;
try {
  const wslScriptPath = scriptPath.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
  const wslWorkDir = rootDir.replace(/^[a-zA-Z]:/, (m) => `/mnt/${m[0].toLowerCase()}`).replace(/\\/g, '/');
  const passedArgs = args.map(a => `"${a}"`).join(' ');

  const uvCandidates = [
    '/home/philg/.local/bin/uv',
    'uv',
  ];

  for (const uvBin of uvCandidates) {
    const check = spawnSync('wsl', ['-d', 'Ubuntu', '--', uvBin, '--version'], { stdio: 'ignore' });
    if (check.status === 0) {
      console.log(`[WOFF2 Compressor] Running via WSL2 Ubuntu uv (${uvBin})...`);
      const result = spawnSync('wsl', [
        '-d',
        'Ubuntu',
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
  console.warn(`[WOFF2 Compressor] WSL2 Ubuntu execution note: ${err.message}`);
}

if (!executed) {
  console.warn('[WOFF2 Compressor] Notice: WSL2 Ubuntu uv not reachable. WOFF2 compression deferred.');
  process.exit(0);
}
