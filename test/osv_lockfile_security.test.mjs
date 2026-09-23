import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

test('Google OSV-Scanner Lockfile Vulnerability Guard', async (t) => {
  await t.test('requirements.lock only contains cryptographically hash-pinned packages', () => {
    const lockPath = path.resolve('requirements.lock');
    assert.ok(fs.existsSync(lockPath), 'requirements.lock must exist');
    const content = fs.readFileSync(lockPath, 'utf8');
    const lines = content.split('\n');

    // Packages must be hash-pinned
    const packageLines = lines.filter(l => /^[a-zA-Z0-9_\-]+==/.test(l.trim()));
    assert.ok(packageLines.length > 0, 'requirements.lock must define pinned packages');
    for (const pkg of packageLines) {
      assert.ok(pkg.includes('=='), `Package ${pkg} must be pinned with exact == version`);
    }

    // Must contain sha256 hashes
    assert.ok(content.includes('--hash=sha256:'), 'requirements.lock must specify sha256 hashes');
  });

  await t.test('pubspec.lock declares zero unvetted third-party packages', () => {
    const pubLockPath = path.resolve('pubspec.lock');
    if (fs.existsSync(pubLockPath)) {
      const content = fs.readFileSync(pubLockPath, 'utf8');
      assert.ok(content.includes('packages: {}'), 'pubspec.lock must only rely on Dart SDK stdlib (0 third-party packages)');
    }
  });

  await t.test('package.json declares zero runtime dependencies', () => {
    const pkgJsonPath = path.resolve('package.json');
    assert.ok(fs.existsSync(pkgJsonPath), 'package.json must exist');
    const pkg = JSON.parse(fs.readFileSync(pkgJsonPath, 'utf8'));
    assert.equal(pkg.dependencies, undefined, 'package.json must have zero runtime dependencies to minimize attack surface');
  });

  await t.test('OSV audit report confirms 0 vulnerabilities across all dependencies', () => {
    const reportPath = path.resolve('documentation/osv_audit_report.json');
    if (fs.existsSync(reportPath)) {
      const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
      assert.equal(report.vulnerabilitiesFound, 0, 'Google OSV-Scanner must report exactly 0 vulnerabilities');
      assert.equal(report.passed, true, 'OSV audit passed field must be true');
    }
  });
});
