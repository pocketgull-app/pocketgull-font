/**
 * PocketGull Commercial Licensing — PayPal REST API v2 Engine
 * Pure Node.js ESM implementation for digital foundry sales & webhook fulfillment.
 */

import crypto from 'node:crypto';

export const POCKETGULL_TIERS = {
  solo: {
    id: 'solo',
    name: 'Solo Designer / Indie Practitioner',
    price: '49.00',
    currency: 'USD',
    seats: 1,
    workstations: 3,
    apps: 2,
    pageviews: 'Unlimited',
    description: 'PocketGull Commercial Superfamily License — Solo Practitioner (1 Seat, 3 Workstations)'
  },
  studio: {
    id: 'studio',
    name: 'Studio / Agency',
    price: '149.00',
    currency: 'USD',
    seats: 10,
    workstations: 10,
    apps: 10,
    pageviews: 'Unlimited',
    description: 'PocketGull Commercial Superfamily License — Studio/Agency (10 Seats, Unlimited Client Work)'
  },
  enterprise: {
    id: 'enterprise',
    name: 'Enterprise / Health System & EHR',
    price: '499.00',
    currency: 'USD',
    seats: -1, // Unlimited
    workstations: -1,
    apps: -1,
    pageviews: 'Unlimited',
    description: 'PocketGull Commercial Superfamily License — Enterprise/EHR (Unlimited Seats, Bedside Telemetry & Indemnification)'
  }
};

let cachedToken = null;
let tokenExpiresAt = 0;

/**
 * Returns the base PayPal API URL.
 */
export function getPayPalBaseUrl(isSandbox = true) {
  return isSandbox
    ? 'https://api-m.sandbox.paypal.com'
    : 'https://api-m.paypal.com';
}

/**
 * Obtains an OAuth 2.0 Access Token using client credentials grant.
 */
export async function getAccessToken({ clientId, clientSecret, isSandbox = true }) {
  if (cachedToken && Date.now() < tokenExpiresAt - 60000) {
    return cachedToken;
  }

  if (!clientId || !clientSecret) {
    throw new Error('Missing PayPal credentials: clientId and clientSecret are required.');
  }

  const baseUrl = getPayPalBaseUrl(isSandbox);
  const auth = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  const res = await fetch(`${baseUrl}/v1/oauth2/token`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'grant_type=client_credentials'
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`PayPal OAuth failed (${res.status}): ${errorText}`);
  }

  const data = await res.json();
  cachedToken = data.access_token;
  tokenExpiresAt = Date.now() + (data.expires_in * 1000);
  return cachedToken;
}

/**
 * Creates a PayPal v2 Checkout Order for a given license tier.
 */
export async function createOrder({
  clientId,
  clientSecret,
  isSandbox = true,
  tierKey = 'solo',
  licenseeName = 'Independent Licensee',
  returnUrl = 'https://font.pocketgull.app/commercial-success.html',
  cancelUrl = 'https://font.pocketgull.app/commercial.html'
}) {
  const tier = POCKETGULL_TIERS[tierKey.toLowerCase()];
  if (!tier) {
    throw new Error(`Invalid license tier "${tierKey}". Valid tiers: ${Object.keys(POCKETGULL_TIERS).join(', ')}`);
  }

  const token = await getAccessToken({ clientId, clientSecret, isSandbox });
  const baseUrl = getPayPalBaseUrl(isSandbox);

  const customMetadata = JSON.stringify({
    tier: tier.id,
    licensee: licenseeName.trim().slice(0, 120),
    version: '3.1.0'
  });

  const payload = {
    intent: 'CAPTURE',
    purchase_units: [
      {
        reference_id: `PG-${tier.id.toUpperCase()}-${Date.now()}`,
        description: tier.description,
        custom_id: customMetadata,
        amount: {
          currency_code: tier.currency,
          value: tier.price
        }
      }
    ],
    application_context: {
      brand_name: 'PocketGull Typefoundry (GearArts)',
      landing_page: 'NO_PREFERENCE',
      user_action: 'PAY_NOW',
      return_url: returnUrl,
      cancel_url: cancelUrl
    }
  };

  const res = await fetch(`${baseUrl}/v2/checkout/orders`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`PayPal Create Order failed (${res.status}): ${errorText}`);
  }

  return await res.json();
}

/**
 * Captures payment for an authorized PayPal Order.
 */
export async function captureOrder({ clientId, clientSecret, isSandbox = true, orderId }) {
  if (!orderId) throw new Error('orderId is required to capture an order');

  const token = await getAccessToken({ clientId, clientSecret, isSandbox });
  const baseUrl = getPayPalBaseUrl(isSandbox);

  const res = await fetch(`${baseUrl}/v2/checkout/orders/${orderId}/capture`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`PayPal Capture Order failed (${res.status}): ${errorText}`);
  }

  return await res.json();
}

/**
 * Cryptographically verifies an incoming PayPal Webhook signature.
 */
export async function verifyWebhookSignature({
  clientId,
  clientSecret,
  isSandbox = true,
  webhookId,
  headers,
  rawBody
}) {
  if (!webhookId) throw new Error('webhookId is required to verify webhook signature');

  const token = await getAccessToken({ clientId, clientSecret, isSandbox });
  const baseUrl = getPayPalBaseUrl(isSandbox);

  const verificationPayload = {
    auth_algo: headers['paypal-auth-algo'] || headers['PAYPAL-AUTH-ALGO'],
    cert_url: headers['paypal-cert-url'] || headers['PAYPAL-CERT-URL'],
    transmission_id: headers['paypal-transmission-id'] || headers['PAYPAL-TRANSMISSION-ID'],
    transmission_sig: headers['paypal-transmission-sig'] || headers['PAYPAL-TRANSMISSION-SIG'],
    transmission_time: headers['paypal-transmission-time'] || headers['PAYPAL-TRANSMISSION-TIME'],
    webhook_id: webhookId,
    webhook_event: typeof rawBody === 'string' ? JSON.parse(rawBody) : rawBody
  };

  const res = await fetch(`${baseUrl}/v1/notifications/verify-webhook-signature`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(verificationPayload)
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Webhook verification request failed (${res.status}): ${errorText}`);
  }

  const result = await res.json();
  return result.verification_status === 'SUCCESS';
}

/**
 * Generates an HMAC-SHA256 signed download token for secure file delivery.
 */
export function generateSignedLicensePayload({
  orderId,
  tierKey,
  licenseeName,
  customerEmail,
  secret,
  expiresInMs = 172800000 // 48 hours default
}) {
  if (!secret) throw new Error('A secret key is required to sign license payloads');

  const tier = POCKETGULL_TIERS[tierKey.toLowerCase()] || POCKETGULL_TIERS.solo;
  const issuedAt = Date.now();
  const expiresAt = issuedAt + expiresInMs;

  const payload = {
    orderId,
    tier: tier.id,
    tierName: tier.name,
    licensee: licenseeName,
    email: customerEmail,
    issuedAt,
    expiresAt,
    asset: 'PocketGull-v3.1.0-Superfamily.zip'
  };

  const serialized = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto
    .createHmac('sha256', secret)
    .update(serialized)
    .digest('base64url');

  return {
    token: serialized,
    signature,
    expiresAt,
    downloadQuery: `token=${serialized}&sig=${signature}`
  };
}

/**
 * Validates a signed download token.
 */
export function verifySignedLicensePayload(token, signature, secret) {
  if (!token || !signature || !secret) return { valid: false, reason: 'Missing arguments' };

  const expectedSig = crypto
    .createHmac('sha256', secret)
    .update(token)
    .digest('base64url');

  const sigBuffer = Buffer.from(signature);
  const expBuffer = Buffer.from(expectedSig);

  if (sigBuffer.length !== expBuffer.length || !crypto.timingSafeEqual(sigBuffer, expBuffer)) {
    return { valid: false, reason: 'Invalid cryptographic signature' };
  }

  try {
    const raw = Buffer.from(token, 'base64url').toString('utf8');
    const data = JSON.parse(raw);

    if (Date.now() > data.expiresAt) {
      return { valid: false, reason: 'Download link has expired', data };
    }

    return { valid: true, data };
  } catch (err) {
    return { valid: false, reason: `Malformed token data: ${err.message}` };
  }
}

/**
 * Generates a customized, formatted EULA Certificate based on purchase data.
 */
export function generateLicenseCertificate({
  orderId,
  tierKey,
  licenseeName,
  customerEmail,
  purchaseDate = new Date().toISOString()
}) {
  const tier = POCKETGULL_TIERS[tierKey.toLowerCase()] || POCKETGULL_TIERS.solo;

  return `# POCKETGULL™ TYPEFACE SUPERFAMILY — COMMERCIAL CERTIFICATE OF LICENSE
--------------------------------------------------------------------------------
CERTIFICATE IDENTIFIER : PG-LIC-${orderId}
DATE OF ISSUANCE       : ${purchaseDate}
AUTHORIZED LICENSEE    : ${licenseeName}
LICENSEE CONTACT EMAIL : ${customerEmail}
PURCHASED TIER         : ${tier.name.toUpperCase()} ($${tier.price} USD)
CONFERRED SEAT COUNT   : ${tier.seats === -1 ? 'UNLIMITED (ENTERPRISE-WIDE)' : `${tier.seats} User(s) / ${tier.workstations} Workstations`}
EMBEDDED APPLICATIONS  : ${tier.apps === -1 ? 'UNLIMITED APPLICATIONS & FIRMWARE' : `Up to ${tier.apps} Applications`}
MONTHLY WEBPAGE VIEWS  : UNLIMITED (Zero Impression Caps)
SUPERFAMILY VERSION    : 3.1.0 (38 Cuts + Variable VF Suite)
GOVERNING JURISDICTION : State of Oregon, United States of America
DESIGNER & FOUNDRY     : Phillip Gear / Geararts LLC (https://font.pocketgull.app)

TERMS & INDEMNIFICATION SUMMARY:
1. Grant of License: Phillip Gear / Geararts LLC grants the Authorized Licensee a perpetual,
   worldwide, non-exclusive license to utilize PocketGull in branding, software, print, web,
   and telemetry systems within the parameters of the purchased tier.
2. Life-Critical & Clinical Acuity: Fully validated against ISMP 2026 character disambiguation
   standards and Louise Sloan 5:1 optotype standards.
3. Open Source Coexistence: Incorporates full proprietary 38-cut desktop (.ttf), webfont (.woff2),
   and 2-axis variable (.ttf) suite with dedicated font foundry support.

This document serves as legal proof of perpetual commercial license and indemnification.
--------------------------------------------------------------------------------
Verification Fingerprint (SHA-256): ${crypto.createHash('sha256').update(`${orderId}:${licenseeName}:${tier.id}`).digest('hex')}
`;
}
