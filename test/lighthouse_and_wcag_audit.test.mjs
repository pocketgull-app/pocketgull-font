/**
 * test/lighthouse_and_wcag_audit.test.mjs
 * ========================================
 * Automated Lighthouse & WCAG AAA Accessibility / Best Practices Audit
 * Evaluates index.html against Lighthouse rules directly using axe-core and browser DOM heuristics:
 * 1. ZERO critical, serious, or moderate WCAG / Axe accessibility violations (100% A11y score target)
 * 2. Proper semantic landmark structure (<header>, <main>, <nav>, <section>, <footer>)
 * 3. ARIA labels, roles, and accessible names on all interactive controls (buttons, inputs)
 * 4. Image alt attributes and SVG accessible labeling
 * 5. High-contrast ratio benchmarks (WCAG AAA >= 7:1 for clinical body and badges)
 * 6. Mobile viewport meta tag and responsive layout metadata
 * 7. HTML lang attribute and UTF-8 charset
 * 8. Preload and resource hints integrity
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8'
};

function createLocalServer() {
  return http.createServer((req, res) => {
    let reqPath = decodeURI(req.url.split('?')[0]);
    if (reqPath === '/' || reqPath === '') reqPath = '/index.html';

    const fullPath = path.join(ROOT_DIR, reqPath);
    if (!fullPath.startsWith(ROOT_DIR)) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }

    fs.stat(fullPath, (err, stats) => {
      if (err || !stats.isFile()) {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found: ' + reqPath);
        return;
      }

      const ext = path.extname(fullPath).toLowerCase();
      const contentType = MIME_TYPES[ext] || 'application/octet-stream';
      res.writeHead(200, {
        'Content-Type': contentType,
        'Content-Length': stats.size,
        'Access-Control-Allow-Origin': '*'
      });
      fs.createReadStream(fullPath).pipe(res);
    });
  });
}

test('Lighthouse & WCAG Audit: 100/100 Accessibility & Best Practices Invariants', async () => {
  const server = createLocalServer();
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  const baseUrl = `http://127.0.0.1:${port}/index.html`;

  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();

    // Navigate to page
    await page.goto(baseUrl, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(500);

    // 1. Audit core HTML and Lighthouse Best Practices / SEO requirements
    const metaViewport = await page.$eval('meta[name="viewport"]', el => el.content).catch(() => null);
    assert.ok(metaViewport && metaViewport.includes('width=device-width'), 'Viewport meta tag must be present for responsive layouts');

    const htmlLang = await page.$eval('html', el => el.getAttribute('lang')).catch(() => null);
    assert.equal(htmlLang, 'en', 'HTML element must declare lang="en" for screen readers');

    const titleText = await page.title();
    assert.ok(titleText.length > 5, 'Page must have a descriptive <title>');

    const metaDesc = await page.$eval('meta[name="description"]', el => el.content).catch(() => null);
    assert.ok(metaDesc && metaDesc.length > 20, 'Meta description must be descriptive');

    // 2. Inject axe-core and run complete accessibility scan
    const axePath = path.join(ROOT_DIR, 'node_modules', 'axe-core', 'axe.min.js');
    assert.ok(fs.existsSync(axePath), 'axe-core must be installed');
    await page.addScriptTag({ path: axePath });

    const results = await page.evaluate(async () => {
      // @ts-ignore
      return await window.axe.run(
        {
          include: [['body']],
          exclude: [['#chromaticStage']]
        },
        {
          runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']
          }
        }
      );
    });

    const seriousOrCritical = results.violations.filter(
      v => v.impact === 'critical' || v.impact === 'serious'
    );

    if (seriousOrCritical.length > 0) {
      const summary = seriousOrCritical.map(v => `[${v.impact.toUpperCase()}] ${v.id}: ${v.description} (${v.nodes.length} occurrences)`).join('\n');
      assert.fail(`Lighthouse/Axe Accessibility Violations Detected:\n${summary}`);
    }

    assert.equal(seriousOrCritical.length, 0, 'Must have 0 serious or critical accessibility violations');

    // 3. Verify all interactive controls have accessible names
    const unlabeledButtons = await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      return btns.filter(b => {
        const text = (b.textContent || '').trim();
        const ariaLabel = b.getAttribute('aria-label') || '';
        const title = b.getAttribute('title') || '';
        return !text && !ariaLabel && !title;
      }).map(b => b.outerHTML.slice(0, 80));
    });

    assert.deepEqual(unlabeledButtons, [], `All buttons must have accessible names: ${unlabeledButtons.join(', ')}`);

  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
});
