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
