/**
 * PocketGull Commercial Licensing — PayPal Webhook HTTP Handler
 * Handles PAYMENT.CAPTURE.COMPLETED events from PayPal, cryptographically verifies
 * signatures, issues signed 48-hour download links, and logs commercial fulfillment.
 */

import {
  verifyWebhookSignature,
  generateSignedLicensePayload,
  generateLicenseCertificate,
  POCKETGULL_TIERS
} from './paypal_service.mjs';

/**
 * Main Webhook Dispatcher
 * @param {object} options
 * @param {object} options.headers - Incoming HTTP request headers
 * @param {string|object} options.body - Incoming raw body string or parsed JSON
 * @param {object} options.env - Environment variables ({ PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_WEBHOOK_ID, DOWNLOAD_HMAC_SECRET, IS_SANDBOX })
 * @returns {Promise<{ status: number, body: object }>}
 */
export async function handlePayPalWebhook({ headers, body, env }) {
  const {
    PAYPAL_CLIENT_ID,
    PAYPAL_CLIENT_SECRET,
    PAYPAL_WEBHOOK_ID,
    DOWNLOAD_HMAC_SECRET = 'pocketgull-default-hmac-salt-dev-change-in-prod',
    IS_SANDBOX = 'true'
  } = env;

  const isSandbox = String(IS_SANDBOX).toLowerCase() === 'true';

  // 1. Parse body if passed as string
  const rawBody = typeof body === 'string' ? body : JSON.stringify(body);
  let event;
  try {
    event = typeof body === 'object' ? body : JSON.parse(body);
  } catch (err) {
    return { status: 400, body: { error: `Invalid JSON payload: ${err.message}` } };
  }

  // 2. Cryptographic signature check (bypassed only in local test mock mode)
  if (PAYPAL_CLIENT_ID && PAYPAL_CLIENT_SECRET && PAYPAL_WEBHOOK_ID) {
    try {
      const isValid = await verifyWebhookSignature({
        clientId: PAYPAL_CLIENT_ID,
        clientSecret: PAYPAL_CLIENT_SECRET,
        isSandbox,
        webhookId: PAYPAL_WEBHOOK_ID,
        headers,
        rawBody
      });

      if (!isValid) {
        console.error('❌ PayPal Webhook signature verification rejected.');
        return { status: 401, body: { error: 'Invalid PayPal Webhook signature' } };
      }
    } catch (err) {
      console.error('❌ PayPal Webhook verification API error:', err);
      return { status: 502, body: { error: `Webhook verification service error: ${err.message}` } };
    }
  } else {
    console.warn('⚠️ PayPal credentials not fully supplied in env; running in unverified test mode.');
  }

  // 3. Process the event type
  const eventType = event.event_type;
  console.log(`📦 Processing PayPal Webhook event: ${eventType} (ID: ${event.id})`);

  if (eventType === 'PAYMENT.CAPTURE.COMPLETED' || eventType === 'CHECKOUT.ORDER.APPROVED') {
    const resource = event.resource;
    const orderId = resource.id || resource.supplementary_data?.related_ids?.order_id || event.id;
    
    // Extract payer info
    const payer = resource.payer || {};
    const customerEmail = payer.email_address || 'licensee@unknown.com';
    const payerName = payer.name 
      ? `${payer.name.given_name || ''} ${payer.name.surname || ''}`.trim() 
      : 'Commercial Licensee';

    // Parse custom metadata if available
    let customData = {};
    try {
      if (resource.custom_id) {
        customData = JSON.parse(resource.custom_id);
      }
    } catch {
      customData = { tier: 'solo', licensee: payerName };
    }

    const tierKey = (customData.tier || 'solo').toLowerCase();
    const licenseeName = customData.licensee || payerName || 'Commercial Licensee';
    const tier = POCKETGULL_TIERS[tierKey] || POCKETGULL_TIERS.solo;

    // 4. Generate signed expiring download payload
    const licenseDelivery = generateSignedLicensePayload({
      orderId,
      tierKey: tier.id,
      licenseeName,
      customerEmail,
      secret: DOWNLOAD_HMAC_SECRET,
      expiresInMs: 48 * 60 * 60 * 1000 // 48 hours
    });

    // 5. Generate formatted commercial EULA certificate
    const certificateText = generateLicenseCertificate({
      orderId,
      tierKey: tier.id,
      licenseeName,
      customerEmail,
      purchaseDate: new Date().toISOString()
    });

    const deliveryRecord = {
      orderId,
      transactionId: resource.id,
      status: 'FULFILLED',
      tier: tier.id,
      tierName: tier.name,
      amount: resource.amount ? `${resource.amount.value} ${resource.amount.currency_code}` : `$${tier.price} USD`,
      licensee: licenseeName,
      email: customerEmail,
      downloadUrl: `https://font.pocketgull.app/commercial-success.html?${licenseDelivery.downloadQuery}`,
      expiresAt: new Date(licenseDelivery.expiresAt).toISOString(),
      certificate: certificateText
    };

    console.log('✅ License successfully generated & fulfilled:', {
      orderId,
      tier: tier.id,
      licensee: licenseeName,
      email: customerEmail
    });

    return {
      status: 200,
      body: {
        success: true,
        message: 'Order processed and commercial license dispatched',
        fulfillment: deliveryRecord
      }
    };
  }

  // Acknowledge other events (e.g. BILLING, DISPUTES, etc.)
  return {
    status: 200,
    body: { success: true, message: `Event ${eventType} acknowledged.` }
  };
}
