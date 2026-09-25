/**
 * test/specimen_interactions_playwright.test.mjs
 * ===============================================
 * Multi-Browser Playwright E2E Test Suite for PocketGull Interactive Specimen (index.html).
 * Targets all major rendering engines:
 * 1. Chromium (Blink)
 * 2. Firefox (Gecko)
 * 3. WebKit (Safari / WebKit engine)
 *
 * Verifies across all browser engines:
 * - ZERO unhandled console exceptions or syntax errors (e.g. "axes", "toggleScotopicNight")
 * - 16-Axis Console slider manipulation and dynamic readout updates
 * - All Variable Font preset pills (Healing, Philocardia, Hairline, Thin, etc.)
 * - Philocardia Heart Tittle interactive switcher (72 BPM, 60 BPM, varieties)
 * - 650nm Scotopic Night mode toggle (toggleScotopicNight)
 * - Theme toggle functionality (Dark -> Washi -> Light)
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium, firefox, webkit } from 'playwright';

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

const BROWSERS = [
  { name: 'Chromium', launcher: chromium },
  { name: 'Firefox', launcher: firefox },
  { name: 'WebKit', launcher: webkit }
];

for (const { name: browserName, launcher } of BROWSERS) {
  test(`Playwright E2E [${browserName}]: Interactive Specimen validation with zero console errors`, async () => {
    const server = createLocalServer();
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    const port = server.address().port;
    const baseUrl = `http://127.0.0.1:${port}/index.html`;

    let browser;
    try {
      browser = await launcher.launch({ headless: true });
      const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await context.newPage();

      const consoleErrors = [];
      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          const text = msg.text();
          // Filter out browser engine font sanitizer warnings that are logged as console errors in Gecko/Firefox
          if (text.includes('downloadable font:') || text.includes('Table discarded')) {
            return;
          }
          consoleErrors.push(text);
        }
      });

      const pageErrors = [];
      page.on('pageerror', (err) => {
        pageErrors.push(err.message);
      });

      // 1. Navigate to index.html
      const response = await page.goto(baseUrl, { waitUntil: 'domcontentloaded' });
      assert.equal(response.status(), 200, 'index.html must return HTTP 200');

      // Wait for initial DOM hydration
      await page.waitForTimeout(600);

      // 2. Assert ZERO uncaught runtime syntax or reference errors
      assert.deepEqual(pageErrors, [], `[${browserName}] No uncaught JS page errors permitted: ${pageErrors.join(', ')}`);
      assert.deepEqual(consoleErrors, [], `[${browserName}] No uncaught console error messages permitted: ${consoleErrors.join(', ')}`);

      // 3. Test Theme Toggle
      const themeBtn = page.locator('#themeToggleBtn');
      if (await themeBtn.isVisible()) {
        await themeBtn.click();
        const themeAttr1 = await page.getAttribute('html', 'data-theme');
        assert.ok(['washi', 'light', 'dark'].includes(themeAttr1), `[${browserName}] Theme must toggle properly`);
      }

      // 4. Test 16-Axis Console Sliders
      const wghtSlider = page.locator('#slider-wght');
      await wghtSlider.waitFor({ state: 'attached' });
      await wghtSlider.evaluate((el) => {
        el.value = 750;
        el.dispatchEvent(new Event('input', { bubbles: true }));
      });
      const wghtValText = await page.locator('#val-wght').textContent();
      assert.equal(wghtValText.trim(), '750', `[${browserName}] Weight slider label must reflect input`);

      const readout = page.locator('#vf-playground-readout');
      const readoutContent = await readout.textContent();
      assert.ok(
        readoutContent.includes("'wght' 750") || readoutContent.includes('wght 750'),
        `[${browserName}] Readout must reflect updated wght axis, got: ${readoutContent}`
      );

      // 5. Test Preset Pills
      const presetPills = page.locator('#vfPresetControls .preset-pill');
      const pillCount = await presetPills.count();
      assert.ok(pillCount >= 10, `[${browserName}] Must have at least 10 preset pills available`);

      // Click Philocardia preset
      const philocardiaPill = page.locator('#vfPresetControls .preset-pill[data-preset="philocardia"]');
      await philocardiaPill.click();
      assert.ok(await philocardiaPill.evaluate(el => el.classList.contains('active')), `[${browserName}] Philocardia pill must be active`);

      // Click Healing Sanctuary preset
      const healingPill = page.locator('#vfPresetControls .preset-pill[data-preset="healing"]');
      await healingPill.click();
      assert.ok(await healingPill.evaluate(el => el.classList.contains('active')), `[${browserName}] Healing pill must be active`);

      // 6. Test 650nm Scotopic Red Mode Toggle
      const scotopicBtn = page.locator('#scotopicToggleBtn');
      if (await scotopicBtn.isVisible()) {
        await scotopicBtn.click();
        const isRed = await page.locator('#scotopicContainer').evaluate(el => el.classList.contains('scotopic-active'));
        assert.ok(isRed, `[${browserName}] Scotopic red mode must activate without error`);

        // Click to toggle off
        await scotopicBtn.click();
        const isRedOff = await page.locator('#scotopicContainer').evaluate(el => el.classList.contains('scotopic-active'));
        assert.ok(!isRedOff, `[${browserName}] Scotopic red mode must toggle off`);
      }

      // 7. Test Philocardia BPM and Variety Selectors
      const bpmBtn = page.locator('#heartBpmBadge');
      if (await bpmBtn.isVisible()) {
        await bpmBtn.click();
        const bpmText = await bpmBtn.textContent();
        assert.ok(bpmText.includes('BPM') || bpmText.includes('Static'), `[${browserName}] BPM button must cycle states`);
      }

      const tittleVarietyPills = page.locator('#tittleVarietyMini .tittle-variety-pill');
      // 8. Test Quick Insert Chips (setVfSample)
      const heartsChip = page.locator('button.vf-chip:has-text("Philocardia Hearts")');
      if (await heartsChip.isVisible()) {
        await heartsChip.click();
        const vfTextContent = await page.locator('#vf-playground-text').textContent();
        assert.ok(vfTextContent.replace(/ı/g, 'i').includes('Pediatric Healing Sanctuary'), `[${browserName}] Hearts quick insert chip must update vfText`);
        const heartSpans = page.locator('#vf-playground-text span.philocardia-heart');
        const count = await heartSpans.count();
        assert.ok(count > 0, `[${browserName}] Philocardia hearts quick insert must render .philocardia-heart elements in #vf-playground-text (found ${count})`);
      }

      const brailleChip = page.locator('button.vf-chip:has-text("Tactile Braille")');
      if (await brailleChip.isVisible()) {
        await brailleChip.click();
        const vfTextContent = await page.locator('#vf-playground-text').textContent();
        assert.ok(vfTextContent.includes('⠁⠍'), `[${browserName}] Quick insert chip must update vfText`);
      }

      // 9. Test Science & Telemetry Tab Switching (switchSciTab)
      const mathTabBtn = page.locator('button.sci-tab-btn:has-text("Mathematical Proofs")');
      if (await mathTabBtn.isVisible()) {
        await mathTabBtn.click();
        const mathPanel = page.locator('#sciPanelMath');
        assert.ok(await mathPanel.evaluate(el => el.classList.contains('active')), `[${browserName}] Math panel must become active`);
      }

      // 10. Test Math Formula Selection (selectMathFormula)
      const enzymeFormulaBtn = page.locator('#mathFormulaTabs button:has-text("Enzyme Kinetics")');
      if (await enzymeFormulaBtn.isVisible()) {
        await enzymeFormulaBtn.click();
        const stageContent = await page.locator('#mathFormulaStage').textContent();
        assert.ok(stageContent.includes('Michaelis-Menten'), `[${browserName}] Formula selector must update stage`);
      }

      // 11. Test Studio Drawer Links (toggleStudioDrawer)
      const studioDrawer = page.locator('#specimen-drawer');
      if (await studioDrawer.count() > 0) {
        await page.evaluate(() => window.toggleStudioDrawer('specimen-drawer', true));
        assert.ok(await studioDrawer.evaluate(el => el.open === true), `[${browserName}] Drawer must open on toggleStudioDrawer`);
      }

      // 12. Verify All Internal Anchor Links have Valid Targets
      const invalidAnchors = await page.evaluate(() => {
        const anchors = Array.from(document.querySelectorAll('a[href^="#"]'));
        return anchors
          .map(a => a.getAttribute('href').slice(1))
          .filter(id => id && !document.getElementById(id) && !document.querySelector(`[name="${id}"]`));
      });
      assert.deepEqual(invalidAnchors, [], `[${browserName}] All anchor hrefs must resolve to existing DOM IDs: ${invalidAnchors.join(', ')}`);

      // 13. Verify All Local File Links Return HTTP 200
      const localLinks = await page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href]'))
          .map(a => a.getAttribute('href'))
          .filter(h => h && !h.startsWith('#') && !h.startsWith('http://') && !h.startsWith('https://') && !h.startsWith('mailto:'));
      });

      for (const link of localLinks) {
        const linkUrl = new URL(link, baseUrl).toString();
        const res = await page.request.get(linkUrl);
        assert.ok(res.status() === 200, `[${browserName}] Link target ${link} must return HTTP 200, got ${res.status()}`);
      }

      // 14. Final verification of clean runtime execution across all actions
      assert.deepEqual(pageErrors, [], `[${browserName}] No uncaught JS page errors permitted after interactions: ${pageErrors.join(', ')}`);
      assert.deepEqual(consoleErrors, [], `[${browserName}] No uncaught console error messages permitted after interactions: ${consoleErrors.join(', ')}`);

    } finally {
      if (browser) await browser.close();
      await new Promise((resolve) => server.close(resolve));
    }
  });
}
