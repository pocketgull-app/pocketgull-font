import test from 'node:test';
import assert from 'node:assert/strict';
import {
  POCKETGULL_TIERS,
  generateSignedLicensePayload,
  verifySignedLicensePayload,
  generateLicenseCertificate
} from '../api/paypal_service.mjs';

test('PayPal Service: Tier definitions integrity', () => {
  assert.ok(POCKETGULL_TIERS.solo, 'Solo tier must exist');
  assert.equal(POCKETGULL_TIERS.solo.price, '49.00');
  assert.equal(POCKETGULL_TIERS.solo.seats, 1);

  assert.ok(POCKETGULL_TIERS.studio, 'Studio tier must exist');
  assert.equal(POCKETGULL_TIERS.studio.price, '149.00');
  assert.equal(POCKETGULL_TIERS.studio.seats, 10);

  assert.ok(POCKETGULL_TIERS.enterprise, 'Enterprise tier must exist');
  assert.equal(POCKETGULL_TIERS.enterprise.price, '499.00');
  assert.equal(POCKETGULL_TIERS.enterprise.seats, -1); // Unlimited
});

test('PayPal Service: Signed license payload generation & verification', () => {
  const secret = 'test-secret-salt-pocketgull-2026';
  const licenseData = generateSignedLicensePayload({
    orderId: 'PG-ORD-998877',
    tierKey: 'studio',
    licenseeName: 'Acme Medical Systems',
    customerEmail: 'admin@acmemed.com',
    secret,
    expiresInMs: 3600000 // 1 hour
  });

  assert.ok(licenseData.token, 'Token string must be present');
  assert.ok(licenseData.signature, 'Signature must be present');
  assert.match(licenseData.downloadQuery, /token=.*&sig=.*/, 'Query string must format properly');

  // Verify valid token
  const result = verifySignedLicensePayload(licenseData.token, licenseData.signature, secret);
  assert.equal(result.valid, true, 'Verification of untouched token must succeed');
  assert.equal(result.data.orderId, 'PG-ORD-998877');
  assert.equal(result.data.tier, 'studio');
  assert.equal(result.data.licensee, 'Acme Medical Systems');
});

test('PayPal Service: Tampered signature rejection', () => {
  const secret = 'test-secret-salt-pocketgull-2026';
  const licenseData = generateSignedLicensePayload({
    orderId: 'PG-ORD-12345',
    tierKey: 'enterprise',
    licenseeName: 'Health Corp',
    customerEmail: 'dev@healthcorp.com',
    secret
  });

  // Tamper with signature
  const fakeSig = licenseData.signature.slice(0, -4) + 'AAAA';
  const result = verifySignedLicensePayload(licenseData.token, fakeSig, secret);
  assert.equal(result.valid, false);
  assert.match(result.reason, /Invalid cryptographic signature/);
});

test('PayPal Service: Expired token rejection', () => {
  const secret = 'test-secret-salt-pocketgull-2026';
  const licenseData = generateSignedLicensePayload({
    orderId: 'PG-ORD-EXPIRED',
    tierKey: 'solo',
    licenseeName: 'Solo Dev',
    customerEmail: 'dev@solo.io',
    secret,
    expiresInMs: -1000 // Already expired in the past
  });

  const result = verifySignedLicensePayload(licenseData.token, licenseData.signature, secret);
  assert.equal(result.valid, false);
  assert.match(result.reason, /expired/i);
});

test('PayPal Service: EULA certificate generation contains required indemnification clauses', () => {
  const cert = generateLicenseCertificate({
    orderId: 'TXN-777888',
    tierKey: 'enterprise',
    licenseeName: 'Mayo Regional Clinic',
    customerEmail: 'it@mayoregional.org',
    purchaseDate: '2026-10-06T12:00:00Z'
  });

  assert.match(cert, /CERTIFICATE IDENTIFIER : PG-LIC-TXN-777888/);
  assert.match(cert, /AUTHORIZED LICENSEE    : Mayo Regional Clinic/);
  assert.match(cert, /PURCHASED TIER         : ENTERPRISE/);
  assert.match(cert, /UNLIMITED \(ENTERPRISE-WIDE\)/);
  assert.match(cert, /ISMP 2026/);
  assert.match(cert, /Louise Sloan 5:1/);
  assert.match(cert, /Verification Fingerprint/);
});
