import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Observatory 125+ Invariant: _headers enforces all mandatory security headers', () => {
  const headersPath = path.join('_headers');
  assert.ok(fs.existsSync(headersPath), '_headers file must exist in repository root');
  const content = fs.readFileSync(headersPath, 'utf8');

  // Mandatory 125+ Header Checks
  assert.match(
    content,
    /Strict-Transport-Security:\s*max-age=31536000;\s*includeSubDomains;\s*preload/,
    '_headers must declare HSTS max-age=31536000; includeSubDomains; preload (+10 pts)'
  );
  assert.match(
    content,
    /Cross-Origin-Opener-Policy:\s*same-origin/,
    '_headers must declare COOP same-origin (+5 pts)'
  );
  assert.match(
    content,
    /Cross-Origin-Resource-Policy:\s*same-origin/,
    '_headers must declare CORP same-origin (+5 pts)'
  );
  assert.match(
    content,
    /Cross-Origin-Embedder-Policy:\s*credentialless/,
    '_headers must declare COEP credentialless'
  );
  assert.match(
    content,
    /Referrer-Policy:\s*strict-origin-when-cross-origin/,
    '_headers must declare Referrer-Policy strict-origin-when-cross-origin (+5 pts)'
  );
  assert.match(
    content,
    /X-Frame-Options:\s*SAMEORIGIN/,
    '_headers must declare X-Frame-Options SAMEORIGIN'
  );
  assert.match(
    content,
    /X-Content-Type-Options:\s*nosniff/,
    '_headers must declare X-Content-Type-Options nosniff'
  );

  // CSP Bonus-Gate Invariant: zero 'unsafe-inline' in script-src
  assert.doesNotMatch(
    content,
    /script-src[^;]*'unsafe-inline'/,
    '_headers CSP must NOT contain unsafe-inline in script-src (prevents -20 penalty & preserves bonus gate)'
  );
  assert.doesNotMatch(
    content,
    /script-src[^;]*'unsafe-eval'/,
    '_headers CSP must NOT contain unsafe-eval in script-src'
  );
});

test('Observatory 125+ Invariant: firebase.json enforces all mandatory security headers', () => {
  const firebasePath = path.join('firebase.json');
  assert.ok(fs.existsSync(firebasePath), 'firebase.json file must exist in repository root');
  const config = JSON.parse(fs.readFileSync(firebasePath, 'utf8'));

  assert.ok(config.hosting && config.hosting.headers, 'firebase.json must configure hosting.headers');
  const headers = config.hosting.headers[0].headers;
  const headerMap = new Map(headers.map(h => [h.key, h.value]));

  assert.equal(
    headerMap.get('Strict-Transport-Security'),
    'max-age=31536000; includeSubDomains; preload'
  );
  assert.equal(headerMap.get('Cross-Origin-Opener-Policy'), 'same-origin');
  assert.equal(headerMap.get('Cross-Origin-Resource-Policy'), 'same-origin');
  assert.equal(headerMap.get('Cross-Origin-Embedder-Policy'), 'credentialless');
  assert.equal(headerMap.get('Referrer-Policy'), 'strict-origin-when-cross-origin');
  assert.equal(headerMap.get('X-Frame-Options'), 'SAMEORIGIN');
  assert.equal(headerMap.get('X-Content-Type-Options'), 'nosniff');

  const csp = headerMap.get('Content-Security-Policy');
  assert.ok(csp, 'Content-Security-Policy must be configured');
  assert.doesNotMatch(
    csp,
    /script-src[^;]*'unsafe-inline'/,
    'firebase.json CSP must NOT contain unsafe-inline in script-src'
  );
});

test('Performance Invariant: _headers and firebase.json enforce efficient cache lifetimes (1-year immutable fonts)', () => {
  const headersContent = fs.readFileSync(path.join('_headers'), 'utf8');
  assert.match(
    headersContent,
    /Cache-Control:\s*public,\s*max-age=31536000,\s*immutable/,
    '_headers must declare 1-year immutable caching for font binaries'
  );

  const firebaseConfig = JSON.parse(fs.readFileSync(path.join('firebase.json'), 'utf8'));
  const fontRule = firebaseConfig.hosting.headers.find(h => h.source === 'fonts/**' || h.source.includes('woff2'));
  assert.ok(fontRule, 'firebase.json must contain explicit cache rule for font assets');
  const fontHeaders = new Map(fontRule.headers.map(h => [h.key, h.value]));
  assert.equal(
    fontHeaders.get('Cache-Control'),
    'public, max-age=31536000, immutable',
    'firebase.json must declare 1-year immutable caching for font assets'
  );
});

test('Storefront SEO & Discoverability Invariant: Product JSON-LD, OpenGraph, Storefront CTAs, and Sitemap parity', () => {
  const indexHtml = fs.readFileSync(path.join('index.html'), 'utf8');
  const artisanHtml = fs.readFileSync(path.join('artisan_foundry.html'), 'utf8');
  const commercialHtml = fs.readFileSync(path.join('commercial.html'), 'utf8');
  const sitemapXml = fs.readFileSync(path.join('sitemap.xml'), 'utf8');
  const llmsTxt = fs.readFileSync(path.join('llms.txt'), 'utf8');

  // 1. Direct storefront links surfaced on index.html
  assert.match(indexHtml, /href="artisan_foundry\.html"/, 'index.html must link directly to artisan_foundry.html');
  assert.match(indexHtml, /href="commercial\.html"/, 'index.html must link directly to commercial.html');
  assert.match(indexHtml, /class="btn-nav-shop"/, 'index.html header must display top-level Pro Packs button');

  // 2. Valid JSON-LD Schema.org Product / SoftwareApplication structured data
  for (const [name, html] of [
    ['index.html', indexHtml],
    ['artisan_foundry.html', artisanHtml],
    ['commercial.html', commercialHtml]
  ]) {
    const ldStart = html.indexOf('<script type="application/ld+json">');
    assert.ok(ldStart !== -1, `${name} must embed JSON-LD structured data`);
    const bodyStart = ldStart + '<script type="application/ld+json">'.length;
    const ldEnd = html.indexOf('</script>', bodyStart);
    assert.ok(ldEnd > bodyStart, `${name} JSON-LD tag must close cleanly`);
    const parsed = JSON.parse(html.slice(bodyStart, ldEnd));
    assert.equal(parsed['@context'], 'https://schema.org', `${name} JSON-LD must declare https://schema.org`);
    assert.ok(parsed.offers, `${name} JSON-LD must declare product offers`);
  }

  // 3. Zero broken PayPal sandbox SDK ('client-id=sb') in production commercial.html
  assert.doesNotMatch(
    commercialHtml,
    /client-id=sb/,
    'commercial.html must NOT load sandbox PayPal SDK (client-id=sb) in production'
  );

  // 4. Sitemap & llms.txt catalog parity
  assert.match(sitemapXml, /artisan_foundry\.html/, 'sitemap.xml must index artisan_foundry.html');
  assert.match(sitemapXml, /commercial\.html/, 'sitemap.xml must index commercial.html');
  assert.match(llmsTxt, /PG-BOTANICA-29/, 'llms.txt must index Botanica SKU');
  assert.match(llmsTxt, /PG-KINPAKU-29/, 'llms.txt must index Kinpaku SKU');
  assert.match(llmsTxt, /PG-ENTERPRISE-499/, 'llms.txt must index Enterprise SKU');
});


