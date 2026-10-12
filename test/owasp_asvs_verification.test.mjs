import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

/**
 * OWASP Application Security Verification Standard (ASVS v4.0.3 / v5)
 * Comprehensive Local Machine Audit Harness
 * 
 * Evaluates Level 1 (Opportunistic), Level 2 (Standard / Defense-in-Depth), 
 * and Level 3 (Advanced / Life-Critical Telemetry) across all local assets.
 */

test('OWASP ASVS V1: Architecture, Design & Threat Modeling', () => {
  // V1.1: Security Architecture and Threat Model Documentation
  assert.ok(fs.existsSync('GEMINI.md'), 'Security baseline & architecture rules must exist in GEMINI.md');
  const gemini = fs.readFileSync('GEMINI.md', 'utf8');
  assert.match(gemini, /CI & SAST Security Invariants/, 'Must formalize CI & SAST security invariants');
  assert.match(gemini, /DOM-Based XSS Prevention/, 'Must formalize DOM XSS prevention architecture');
  assert.match(gemini, /Porter-Gull Autonomous Triage Protocol/, 'Must document autonomous triage & decision matrix');
  
  // V1.14: Build, deployment, and configuration verification
  assert.ok(fs.existsSync('.github/workflows/validate.yml'), 'Automated CI verification workflow must exist');
});

test('OWASP ASVS V5: Validation, Sanitization & Encoding (Level 1, 2, 3)', () => {
  // V5.1: Input Validation — Maximum lengths and character set restrictions
  const htmlFiles = ['index.html', 'asl_studio.html', 'sign_studio.html', 'a11y_studio.html'];
  for (const file of htmlFiles) {
    if (fs.existsSync(file)) {
      const content = fs.readFileSync(file, 'utf8');
      
      // All text, search, and email user inputs must declare explicit maxlength attributes
      const inputsWithoutMax = content.match(/<input\b(?=[^>]*\btype=['"](?:text|search|email|url)['"])(?![^>]*\bmaxlength=)[^>]*>/gi);
      assert.equal(
        inputsWithoutMax,
        null,
        `Found text/search inputs in ${file} lacking explicit maxlength bounds: ${JSON.stringify(inputsWithoutMax)}`
      );
    }
  }

  // V5.2: Output Encoding & Injection Prevention
  // Ensure that no JS file uses unescaped document.write or eval
  const jsDir = 'js';
  if (fs.existsSync(jsDir)) {
    const jsFiles = fs.readdirSync(jsDir).filter(f => f.endsWith('.js'));
    for (const f of jsFiles) {
      const code = fs.readFileSync(path.join(jsDir, f), 'utf8');
      assert.doesNotMatch(code, /\bdocument\.write\s*\(/, `${f} must not use dangerous document.write`);
      assert.doesNotMatch(code, /\beval\s*\(/, `${f} must not use dangerous eval()`);
    }
  }

  // V5.3: Memory-safe OpenType table inputs
  const cpalPath = path.join('tool', 'foundry', 'cpal_colr_engine.dart');
  if (fs.existsSync(cpalPath)) {
    const cpalCode = fs.readFileSync(cpalPath, 'utf8');
    assert.match(cpalCode, /& 0xFF/, 'Color parser must mask 8-bit color channels');
  }
});

test('OWASP ASVS V9: Communications & Transport Security Baseline', () => {
  // V9.1: Transport Layer Security & Strict-Transport-Security (HSTS)
  const headersPath = '_headers';
  assert.ok(fs.existsSync(headersPath), '_headers configuration must exist');
  const headers = fs.readFileSync(headersPath, 'utf8');

  // Verify full Mozilla Observatory 125+ Grade A+ Header Battery
  assert.match(headers, /Strict-Transport-Security:\s*max-age=31536000;\s*includeSubDomains;\s*preload/i, 'Must enforce HSTS preload');
  assert.match(headers, /X-Content-Type-Options:\s*nosniff/i, 'Must enforce nosniff');
  assert.match(headers, /X-Frame-Options:\s*SAMEORIGIN/i, 'Must enforce X-Frame-Options');
  assert.match(headers, /Referrer-Policy:\s*strict-origin-when-cross-origin/i, 'Must enforce Referrer-Policy');
  assert.match(headers, /Cross-Origin-Opener-Policy:\s*same-origin/i, 'Must enforce COOP same-origin');
  assert.match(headers, /Cross-Origin-Embedder-Policy:\s*credentialless/i, 'Must enforce COEP credentialless');
  assert.match(headers, /Cross-Origin-Resource-Policy:\s*same-origin/i, 'Must enforce CORP same-origin');

  // V9.2: Content Security Policy (Zero unsafe-inline / unsafe-eval in script-src)
  assert.match(headers, /Content-Security-Policy:/i, 'Must declare Content Security Policy');
  assert.doesNotMatch(headers, /script-src[^;]*'unsafe-eval'/, 'CSP script-src must prohibit unsafe-eval');
});

test('OWASP ASVS V11: Business Logic & Negative Space Invariants', () => {
  // V11.1: Strict boundary prohibitions (Foundry Negative Space Invariants)
  const gemini = fs.readFileSync('GEMINI.md', 'utf8');
  assert.match(gemini, /Not a Medical Device \(SaMD\)/, 'Must declare SaMD boundary prohibition');
  assert.match(gemini, /Not an Automated ASL Translator/, 'Must declare ASL translation boundary prohibition');
  assert.match(gemini, /Not an Accessibility Overlay/, 'Must declare DOM-hijacking overlay prohibition');
  assert.match(gemini, /Zero Telemetry \/ Zero PHI Egress/, 'Must declare zero telemetry invariant');
});

test('OWASP ASVS V13: Anti-Automation & Abuse Prevention (Level 2 & 3)', () => {
  // V13.1: Automated request throttling and form protection
  const pages = ['asl_studio.html', 'sign_studio.html'];
  for (const page of pages) {
    if (fs.existsSync(page)) {
      const html = fs.readFileSync(page, 'utf8');
      assert.match(html, /formHpWebsite/, `${page} must contain an anti-automation honeypot field`);
      assert.match(html, /SUBMIT_COOLDOWN_MS/, `${page} must implement rate limiting cooldown`);
      assert.match(html, /MIN_INTERACTION_MS/, `${page} must implement time-trap anti-bot validation`);
    }
  }
});

test('OWASP ASVS V14: Build, Dependency & Supply Chain Security (Level 1, 2, 3)', () => {
  // V14.1: Cryptographic lockfile pinning (Reproducible builds)
  assert.ok(fs.existsSync('requirements.lock'), 'requirements.lock must exist');
  const reqLock = fs.readFileSync('requirements.lock', 'utf8');
  assert.match(reqLock, /--hash=sha256:/, 'Python dependencies must be cryptographically pinned with SHA-256 hashes');

  // V14.2: Zero runtime dependencies in web / client package.json
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  const runtimeDeps = Object.keys(pkg.dependencies || {});
  assert.equal(runtimeDeps.length, 0, 'package.json must declare 0 runtime dependencies to eliminate attack surface');

  // V14.3: Secret scanning & credential defense
  assert.ok(!fs.existsSync('.env'), '.env file must never exist in repository root');
  assert.ok(!fs.existsSync('private_key.pem'), 'Private keys must never exist in workspace');
});
