/**
 * PocketGull Typefoundry — PayPal AI-Toolkit & Agentic Commerce Engine
 * Integrates PayPal Agentic Commerce tools to automate enterprise invoicing,
 * quotation generation, payment order links, and order tracking via AI.
 * 
 * Powered by:
 * - @paypal/agent-toolkit & @paypal/mcp
 * - Native PayPal REST API v2
 */

import { POCKETGULL_TIERS, getAccessToken, getPayPalBaseUrl } from '../api/paypal_service.mjs';

/**
 * Creates an official PayPal invoice for Enterprise / Health System clients
 * (e.g., when a hospital network or device manufacturer requests a formal invoice
 * with purchase order and Net-30 terms instead of instant credit card checkout).
 */
export async function createFoundryInvoice({
  clientId,
  clientSecret,
  isSandbox = true,
  licenseeName,
  licenseeEmail,
  tierKey = 'enterprise',
  poNumber = '',
  customNotes = ''
}) {
  const tier = POCKETGULL_TIERS[tierKey.toLowerCase()] || POCKETGULL_TIERS.enterprise;
  const token = await getAccessToken({ clientId, clientSecret, isSandbox });
  const baseUrl = getPayPalBaseUrl(isSandbox);

  const invoiceNumber = `PG-INV-${Date.now().toString().slice(-6)}`;
  const invoicePayload = {
    detail: {
      invoice_number: invoiceNumber,
      reference: poNumber || `REF-${tier.id.toUpperCase()}`,
      invoice_date: new Date().toISOString().split('T')[0],
      currency_code: tier.currency,
      note: customNotes || 'Thank you for licensing PocketGull. This invoice confers perpetual commercial rights under the PocketGull Commercial EULA v3.1.0 upon payment.',
      terms_and_conditions: 'Payment due upon receipt or Net 30. Confers perpetual commercial license and indemnification across all enterprise workstations, EHR consoles, and medical hardware displays.'
    },
    invoicer: {
      name: {
        given_name: 'Phillip',
        surname: 'Gear'
      },
      business_name: 'Geararts LLC / PocketGull Typefoundry',
      email_address: 'licensing@pocketgull.app',
      website: 'https://font.pocketgull.app'
    },
    primary_recipients: [
      {
        billing_info: {
          name: {
            given_name: licenseeName
          },
          email_address: licenseeEmail
        }
      }
    ],
    items: [
      {
        name: `PocketGull Typeface Superfamily — ${tier.name}`,
        description: `Complete 38-cut production suite (.ttf, .otf, .woff2) + 2-axis variable font (VF). ISMP clinical disambiguation, 600 UPM fixed telemetry, and enterprise indemnification.`,
        quantity: '1',
        unit_amount: {
          currency_code: tier.currency,
          value: tier.price
        },
        unit_of_measure: 'QUANTITY'
      }
    ]
  };

  // 1. Create draft invoice
  const draftRes = await fetch(`${baseUrl}/v2/invoicing/invoices`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(invoicePayload)
  });

  if (!draftRes.ok) {
    const errorText = await draftRes.text();
    throw new Error(`Failed to create draft invoice (${draftRes.status}): ${errorText}`);
  }

  const invoice = await draftRes.json();
  const invoiceId = invoice.id || invoice.href?.split('/').pop();

  return {
    success: true,
    invoiceId,
    invoiceNumber,
    status: 'DRAFT',
    tier: tier.name,
    amount: `$${tier.price} ${tier.currency}`,
    recipient: `${licenseeName} <${licenseeEmail}>`,
    sendUrl: `${baseUrl}/v2/invoicing/invoices/${invoiceId}/send`
  };
}

/**
 * CLI runner for manual / agentic execution:
 * Usage:
 *   node tool/paypal_ai_agent.mjs invoice "Acme Health" "billing@acmehealth.org" enterprise
 */
async function runCli() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command) {
    console.log(`
🕊️ PocketGull PayPal AI Agent Toolkit
Commands:
  invoice <companyName> <email> [tier]   - Generate an enterprise commercial invoice
  tiers                                  - List active licensing tiers and pricing
`);
    return;
  }

  if (command === 'tiers') {
    console.log('\n🕊️ PocketGull Commercial Licensing Tiers:');
    Object.values(POCKETGULL_TIERS).forEach(t => {
      console.log(`  • ${t.id.toUpperCase().padEnd(12)} : $${t.price} USD | ${t.name} (${t.seats === -1 ? 'Unlimited seats' : `${t.seats} seats`})`);
    });
    return;
  }

  if (command === 'invoice') {
    const company = args[1] || 'Commercial Licensee';
    const email = args[2] || 'procurement@client.com';
    const tier = args[3] || 'enterprise';

    const clientId = process.env.PAYPAL_CLIENT_ID;
    const clientSecret = process.env.PAYPAL_CLIENT_SECRET;
    const isSandbox = (process.env.IS_SANDBOX || 'true') === 'true';

    if (!clientId || !clientSecret) {
      console.log('\n⚠️ PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET not set in environment.');
      console.log('Running simulated mock invoice generation:\n');
      console.log(JSON.stringify({
        success: true,
        mock: true,
        invoiceNumber: `PG-INV-${Date.now().toString().slice(-6)}`,
        company,
        email,
        tier: POCKETGULL_TIERS[tier]?.name || tier,
        amount: `$${POCKETGULL_TIERS[tier]?.price || '499.00'} USD`,
        note: 'Mock invoice created. Supply live credentials to transmit to client via PayPal.'
      }, null, 2));
      return;
    }

    try {
      const res = await createFoundryInvoice({
        clientId,
        clientSecret,
        isSandbox,
        licenseeName: company,
        licenseeEmail: email,
        tierKey: tier
      });
      console.log('\n✅ PayPal Enterprise Invoice Created Successfully:');
      console.log(JSON.stringify(res, null, 2));
    } catch (err) {
      console.error('❌ Failed to create invoice:', err.message);
    }
  }
}

if (process.argv[1]?.endsWith('paypal_ai_agent.mjs')) {
  runCli();
}
