import { chromium } from 'playwright';
import path from 'node:path';

const ARTIFACT_DIR = 'C:/Users/philg/.gemini/antigravity/brain/b0fbcb78-bfcd-49ed-b814-64138625d977';

async function runPixel9Audit() {
  console.log('🚀 Starting Google Pixel 9 Mobile E2E Audit...');
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // Pixel 9 Portrait Context (412 x 924, DPR 2.625)
  const portraitContext = await browser.newContext({
    viewport: { width: 412, height: 924 },
    deviceScaleFactor: 2.625,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
  });

  const page = await portraitContext.newPage();
  
  const consoleErrors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  console.log('📱 Loading index.html on port 8770 in Pixel 9 Portrait...');
  await page.goto('http://127.0.0.1:8770/index.html', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);

  // 1. Audit World Map Studio on Portrait
  console.log('🌍 Auditing World Map Studio on Pixel 9 Portrait...');
  const mapStudio = page.locator('#world-map-studio');
  await mapStudio.scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);

  const mapSvg = page.locator('#worldMapSvg');
  const svgBox = await mapSvg.boundingBox();
  console.log(`📐 SVG World Map Bounding Box in Portrait: width=${svgBox?.width?.toFixed(1)}px, height=${svgBox?.height?.toFixed(1)}px`);

  if (!svgBox || svgBox.width < 300) {
    throw new Error(`FAIL: World map SVG width is too small (${svgBox?.width}px)! Expected > 300px.`);
  }

  // Check pin touch hitbox
  const pins = page.locator('#mapPinLayer .map-pin');
  const pinCount = await pins.count();
  console.log(`📍 Found ${pinCount} SVG map pins rendered.`);
  
  // Tap the Japan pin (jpn) via dispatchEvent (SVG elements inside scaled viewbox)
  const japanPin = page.locator('#mapPinLayer .map-pin[data-id="jpn"]');
  if (await japanPin.count() > 0) {
    console.log('👆 Tapping Japan map pin (SVG click event)...');
    await japanPin.dispatchEvent('click');
    await page.waitForTimeout(400);

    const hudName = await page.locator('#hudCountryName').textContent();
    console.log(`🇯🇵 Active Country in HUD after pin tap: "${hudName}"`);
    if (!hudName.includes('Japan')) {
      throw new Error(`FAIL: Expected HUD to show Japan, got: ${hudName}`);
    }
  }

  // Tap an Indigenous pill in quick switcher bar (e.g. Cree Nation)
  const creePill = page.locator('#countryPillBar .country-pill[data-id="cre"]');
  if (await creePill.count() > 0) {
    console.log('👆 Tapping Cree / Inuktitut pill in quick switcher...');
    await creePill.dispatchEvent('click');
    await page.waitForTimeout(400);

    const hudName = await page.locator('#hudCountryName').textContent();
    console.log(`🪶 Active Country in HUD after pill click: "${hudName}"`);
    if (!hudName.includes('Cree')) {
      throw new Error(`FAIL: Expected HUD to show Cree, got: ${hudName}`);
    }
  }

  // Test View Switcher to Vexillological Pavilion
  console.log('🚩 Testing View Switcher to Vexillological Pavilion...');
  const switchPavilion = page.locator('#viewSwitchPavilion');
  await switchPavilion.dispatchEvent('click');
  await page.waitForTimeout(400);

  const pavilion = page.locator('#vexillologicalPavilionContainer');
  const isPavilionVisible = await pavilion.isVisible();
  console.log(`🚩 Vexillological Pavilion visible: ${isPavilionVisible}`);

  // Switch back to map
  const switchMap = page.locator('#viewSwitchMap');
  await switchMap.dispatchEvent('click');
  await page.waitForTimeout(300);

  // Capture Portrait World Map Studio Screenshot
  const mapScreenshotPath = path.join(ARTIFACT_DIR, 'pixel9_world_map_portrait_fixed.png');
  await mapStudio.screenshot({ path: mapScreenshotPath });
  console.log(`📸 Saved Portrait World Map screenshot to ${mapScreenshotPath}`);

  // 2. Audit Periodic Table on Portrait
  console.log('🧪 Auditing Periodic Table on Pixel 9 Portrait...');
  const ptableSection = page.locator('#periodic-table');
  await ptableSection.scrollIntoViewIfNeeded();
  await page.waitForTimeout(500);

  console.log('DBG 1: panel class before ptable interaction:', await page.evaluate(() => document.getElementById('docDrillPanel')?.className));

  // Check scroll hint
  const scrollHint = page.locator('#periodic-table .mobile-scroll-hint');
  const isHintVisible = await scrollHint.isVisible();
  console.log(`↔ Mobile scroll hint visible: ${isHintVisible}`);

  // Ensure Doc Drill drawer is closed
  await page.evaluate(() => {
    const p = document.getElementById('docDrillPanel');
    if (p) p.classList.remove('open');
    document.body.classList.remove('drill-open');
    const f = document.getElementById('docDrillFloatTrigger');
    if (f) f.style.display = 'none'; // hide float trigger during screenshot
  });
  await page.waitForTimeout(300);
  console.log('DBG 2: panel class after explicit classList.remove:', await page.evaluate(() => document.getElementById('docDrillPanel')?.className));

  // Click an element cell (Hydrogen Z=1 in col 1, then Iron Z=26)
  const hCell = page.locator('#fullPeriodicTableGrid .ptable-cell[data-z="1"]');
  if (await hCell.count() > 0) {
    console.log('👆 Clicking Hydrogen (H) cell in column 1...');
    await hCell.dispatchEvent('click');
    await page.waitForTimeout(300);
    const heroName = await page.locator('#fullPtableHeroName').textContent();
    console.log(`🔬 Active Element Hero: "${heroName}"`);
  }

  const feCell = page.locator('#fullPeriodicTableGrid .ptable-cell[data-z="26"]');
  if (await feCell.count() > 0) {
    console.log('👆 Clicking Iron (Fe) cell...');
    await feCell.dispatchEvent('click');
    await page.waitForTimeout(300);
    const heroName = await page.locator('#fullPtableHeroName').textContent();
    console.log(`🔬 Active Element Hero after Iron selection: "${heroName}"`);
  }

  console.log('DBG 3: panel class after cell click:', await page.evaluate(() => document.getElementById('docDrillPanel')?.className));

  // Ensure Doc Drill is closed for clean screenshot
  await page.evaluate(() => {
    const p = document.getElementById('docDrillPanel');
    if (p) p.classList.remove('open');
    document.body.classList.remove('drill-open');
    const f = document.getElementById('docDrillFloatTrigger');
    if (f) f.style.display = 'none';
  });
  await page.waitForTimeout(300);
  console.log('DBG 4: panel class before screenshot:', await page.evaluate(() => document.getElementById('docDrillPanel')?.className));

  // Capture Portrait Periodic Table Screenshot
  const ptableScreenshotPath = path.join(ARTIFACT_DIR, 'pixel9_ptable_portrait.png');
  await ptableSection.screenshot({ path: ptableScreenshotPath });
  console.log(`📸 Saved Portrait Periodic Table screenshot to ${ptableScreenshotPath}`);

  await portraitContext.close();

  // -------------------------------------------------------------
  // Pixel 9 Landscape Context (924 x 412, DPR 2.625)
  // -------------------------------------------------------------
  console.log('\n📱 Opening Pixel 9 Landscape Context (924 x 412)...');
  const landscapeContext = await browser.newContext({
    viewport: { width: 924, height: 412 },
    deviceScaleFactor: 2.625,
    isMobile: true,
    hasTouch: true,
    userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
  });

  const landPage = await landscapeContext.newPage();
  await landPage.goto('http://127.0.0.1:8770/index.html', { waitUntil: 'domcontentloaded' });
  await landPage.waitForTimeout(1000);

  // Ensure Doc Drill closed
  await landPage.evaluate(() => {
    if (typeof window.closeDocDrill === 'function') window.closeDocDrill();
  });

  // Audit World Map Studio in Landscape
  const landMapStudio = landPage.locator('#world-map-studio');
  await landMapStudio.scrollIntoViewIfNeeded();
  await landPage.waitForTimeout(500);

  const landSvgBox = await landPage.locator('#worldMapSvg').boundingBox();
  console.log(`📐 SVG World Map Bounding Box in Landscape: width=${landSvgBox?.width?.toFixed(1)}px, height=${landSvgBox?.height?.toFixed(1)}px`);

  const landMapScreenshotPath = path.join(ARTIFACT_DIR, 'pixel9_world_map_landscape_fixed.png');
  await landMapStudio.screenshot({ path: landMapScreenshotPath });
  console.log(`📸 Saved Landscape World Map screenshot to ${landMapScreenshotPath}`);

  // Audit Periodic Table in Landscape
  const landPtable = landPage.locator('#periodic-table');
  await landPtable.scrollIntoViewIfNeeded();
  await landPage.waitForTimeout(500);

  const landPtableScreenshotPath = path.join(ARTIFACT_DIR, 'pixel9_ptable_landscape.png');
  await landPtable.screenshot({ path: landPtableScreenshotPath });
  console.log(`📸 Saved Landscape Periodic Table screenshot to ${landPtableScreenshotPath}`);

  await landscapeContext.close();
  await browser.close();

  if (consoleErrors.length > 0) {
    console.warn(`⚠️ Console errors captured:`, consoleErrors);
  }

  console.log('\n🎉 Pixel 9 Mobile E2E Audit successfully completed with 0 fatal errors!');
}

runPixel9Audit().catch(err => {
  console.error('❌ Audit Error:', err);
  process.exit(1);
});
