/**
 * PocketGull Commercial Licensing — Standalone Node HTTP Microservice
 * Zero third-party dependencies (Native Node 18+ / 24+ ESM).
 * 
 * Provides:
 * - POST /api/create-order     : Creates PayPal v2 Checkout order
 * - POST /api/capture-order    : Captures authorized order & issues download token
 * - POST /api/paypal-webhook   : Handles PayPal webhook events with cryptographic validation
 * - GET  /api/download         : HMAC-verified, tamper-proof download stream for Superfamily.zip
 */

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  createOrder,
  captureOrder,
  generateSignedLicensePayload,
  verifySignedLicensePayload,
  generateLicenseCertificate,
  POCKETGULL_TIERS
} from './paypal_service.mjs';
import { handlePayPalWebhook } from './paypal_webhook.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const ZIP_PATH = path.join(ROOT_DIR, 'PocketGull-v3.1.0-Superfamily.zip');

const PORT = process.env.PORT || 8780;
const ENV = {
  PAYPAL_CLIENT_ID: process.env.PAYPAL_CLIENT_ID || '',
  PAYPAL_CLIENT_SECRET: process.env.PAYPAL_CLIENT_SECRET || '',
  PAYPAL_WEBHOOK_ID: process.env.PAYPAL_WEBHOOK_ID || '',
  DOWNLOAD_HMAC_SECRET: process.env.DOWNLOAD_HMAC_SECRET || 'pocketgull-foundry-secret-key-change-in-prod',
  IS_SANDBOX: process.env.IS_SANDBOX || 'true'
};

const server = http.createServer(async (req, res) => {
  // CORS & Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, paypal-client-metadata-id, paypal-auth-algo, paypal-cert-url, paypal-transmission-id, paypal-transmission-sig, paypal-transmission-time');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  // 1. POST /api/create-order
  if (req.method === 'POST' && pathname === '/api/create-order') {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', async () => {
      try {
        const body = raw ? JSON.parse(raw) : {};
        const tier = body.tier || 'solo';
        const licenseeName = body.licenseeName || 'Independent Licensee';

        if (!ENV.PAYPAL_CLIENT_ID || !ENV.PAYPAL_CLIENT_SECRET) {
          // Mock mode if credentials not configured yet
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            id: `MOCK-ORDER-${Date.now()}`,
            status: 'CREATED',
            mock: true,
            tier,
            licenseeName,
            message: 'PayPal credentials not set in environment. Running in mock demonstration mode.'
          }));
          return;
        }

        const order = await createOrder({
          clientId: ENV.PAYPAL_CLIENT_ID,
          clientSecret: ENV.PAYPAL_CLIENT_SECRET,
          isSandbox: ENV.IS_SANDBOX === 'true',
          tierKey: tier,
          licenseeName
        });

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(order));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // 2. POST /api/capture-order
  if (req.method === 'POST' && pathname === '/api/capture-order') {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', async () => {
      try {
        const body = raw ? JSON.parse(raw) : {};
        const { orderId, tier = 'solo', licenseeName = 'Licensee', email = 'customer@example.com' } = body;

        let captureResult = { id: orderId, status: 'COMPLETED' };
        if (ENV.PAYPAL_CLIENT_ID && ENV.PAYPAL_CLIENT_SECRET && !orderId?.startsWith('MOCK-')) {
          captureResult = await captureOrder({
            clientId: ENV.PAYPAL_CLIENT_ID,
            clientSecret: ENV.PAYPAL_CLIENT_SECRET,
            isSandbox: ENV.IS_SANDBOX === 'true',
            orderId
          });
        }

        const tokenData = generateSignedLicensePayload({
          orderId: captureResult.id || orderId,
          tierKey: tier,
          licenseeName,
          customerEmail: email,
          secret: ENV.DOWNLOAD_HMAC_SECRET
        });

        const certificate = generateLicenseCertificate({
          orderId: captureResult.id || orderId,
          tierKey: tier,
          licenseeName,
          customerEmail: email
        });

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: true,
          capture: captureResult,
          downloadUrl: `/commercial-success.html?${tokenData.downloadQuery}`,
          downloadApiUrl: `/api/download?${tokenData.downloadQuery}`,
          certificate
        }));
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // 3. POST /api/paypal-webhook
  if (req.method === 'POST' && pathname === '/api/paypal-webhook') {
    let raw = '';
    req.on('data', chunk => { raw += chunk; });
    req.on('end', async () => {
      const result = await handlePayPalWebhook({
        headers: req.headers,
        body: raw,
        env: ENV
      });

      res.writeHead(result.status, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result.body));
    });
    return;
  }

  // 4. GET /api/download (Secure File Delivery Gate)
  if (req.method === 'GET' && pathname === '/api/download') {
    const token = url.searchParams.get('token');
    const sig = url.searchParams.get('sig');

    const verification = verifySignedLicensePayload(token, sig, ENV.DOWNLOAD_HMAC_SECRET);
    if (!verification.valid) {
      res.writeHead(403, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(`
        <!DOCTYPE html>
        <html>
        <head><title>Download Authorization Failed</title><style>body{background:#0e1117;color:#fff;font-family:sans-serif;padding:40px;text-align:center;}</style></head>
        <body>
          <h2>🔒 Access Denied</h2>
          <p>${verification.reason}</p>
          <p>Please contact <a href="mailto:licensing@pocketgull.app" style="color:#6ee7b7">licensing@pocketgull.app</a> with your PayPal receipt.</p>
        </body>
        </html>
      `);
      return;
    }

    if (!fs.existsSync(ZIP_PATH)) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Font superfamily package not found on server.');
      return;
    }

    const stat = fs.statSync(ZIP_PATH);
    res.writeHead(200, {
      'Content-Type': 'application/zip',
      'Content-Length': stat.size,
      'Content-Disposition': 'attachment; filename="PocketGull-v3.1.0-Superfamily.zip"',
      'Cache-Control': 'no-store, no-cache, must-revalidate'
    });

    const stream = fs.createReadStream(ZIP_PATH);
    stream.pipe(res);
    return;
  }

  // Fallthrough 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Endpoint not found' }));
});

if (process.env.NODE_ENV !== 'test') {
  server.listen(PORT, () => {
    console.log(`🕊️ PocketGull PayPal Licensing Microservice listening on http://localhost:${PORT}`);
    console.log(`   - Sandbox Mode: ${ENV.IS_SANDBOX}`);
    console.log(`   - Webhook Path: http://localhost:${PORT}/api/paypal-webhook`);
    console.log(`   - File Delivery: ${ZIP_PATH} (${fs.existsSync(ZIP_PATH) ? 'Ready' : 'Missing'})`);
  });
}

export default server;
