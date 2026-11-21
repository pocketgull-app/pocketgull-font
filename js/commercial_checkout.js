/**
 * PocketGull Commercial Licensing — Client Checkout Controller
 * Fully accessible, WCAG AAA compliant, zero-unsafe-inline CSP compliant.
 */

(function () {
  'use strict';

  const TIERS = {
    solo: {
      id: 'solo',
      sku: 'PG-SOLO-49',
      name: 'Solo Designer / Indie Practitioner',
      price: '49.00',
      seats: '1 User (Up to 3 Workstations)',
      apps: '2 Applications',
      stripeUrl: 'https://buy.stripe.com/cNibJ21eqcw5dntguL33W02',
      stripeLabel: '💳 Checkout via Stripe — $49.00',
      description: 'Ideal for freelance designers, solo app developers, and independent creators.'
    },
    studio: {
      id: 'studio',
      sku: 'PG-STUDIO-149',
      name: 'Studio / Agency',
      price: '149.00',
      seats: 'Up to 10 Workstations',
      apps: '10 Applications & Client SaaS',
      stripeUrl: 'https://buy.stripe.com/7sY3cw3my53Ddnt4M333W03',
      stripeLabel: '💳 License Agency Suite via Stripe',
      description: 'Full commercial rights across client campaigns, publishing, and digital studios.'
    },
    enterprise: {
      id: 'enterprise',
      sku: 'PG-ENTERPRISE-499',
      name: 'Enterprise / Health System & EHR',
      price: '499.00',
      seats: 'Unlimited Enterprise-wide Users',
      apps: 'Unlimited EHR, Medical Devices & Telemetry',
      stripeUrl: 'mailto:licensing@pocketgull.app?subject=PocketGull%20Enterprise%20Health%20System%20License%20(%24499)',
      stripeLabel: '🏥 Request Enterprise Stripe Link / PO ($499)',
      description: 'Complete legal indemnification, bedside monitor rights, and hospital hardware firmware embedding.'
    }
  };

  let currentTier = 'studio';

  function sanitizeLicensee(raw) {
    return String(raw || '').replace(/[^\w\s.,&'-]/g, '').trim().slice(0, 120);
  }

  function buildPayPalDirectUrl(tier, licenseeName) {
    const url = new URL('https://www.paypal.com/cgi-bin/webscr');
    url.searchParams.set('cmd', '_xclick');
    url.searchParams.set('business', 'philgear@gmail.com');
    const suffix = licenseeName ? ` (${licenseeName})` : '';
    url.searchParams.set('item_name', `PocketGull Commercial License - ${tier.name}${suffix}`);
    url.searchParams.set('item_number', tier.sku);
    url.searchParams.set('amount', tier.price);
    url.searchParams.set('currency_code', 'USD');
    url.searchParams.set('no_shipping', '1');
    return url.toString();
  }

  function updateCheckoutControls() {
    const info = TIERS[currentTier] || TIERS.studio;
    const priceDisplay = document.getElementById('selected-price-display');
    const tierNameDisplay = document.getElementById('selected-tier-name');
    const licenseSummary = document.getElementById('selected-license-summary');
    const stripeBtn = document.getElementById('direct-stripe-btn');
    const paypalBtn = document.getElementById('direct-paypal-btn');
    const licenseeInput = document.getElementById('licensee-name-input');
    const licensee = sanitizeLicensee(licenseeInput ? licenseeInput.value : '');

    if (priceDisplay) priceDisplay.textContent = `$${info.price}`;
    if (tierNameDisplay) tierNameDisplay.textContent = info.name;
    if (licenseSummary) licenseSummary.textContent = `${info.seats} • ${info.apps}`;

    if (stripeBtn) {
      stripeBtn.setAttribute('href', info.stripeUrl);
      stripeBtn.textContent = info.stripeLabel;
    }

    if (paypalBtn) {
      paypalBtn.setAttribute('href', buildPayPalDirectUrl(info, licensee));
      paypalBtn.textContent = `Pay $${info.price} via PayPal Direct →`;
    }
  }

  function selectTier(tierKey) {
    if (!TIERS[tierKey]) return;
    currentTier = tierKey;
    const tierCards = document.querySelectorAll('.tier-card');
    tierCards.forEach(function (c) {
      const active = c.getAttribute('data-tier') === tierKey;
      c.classList.toggle('active', active);
      c.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    updateCheckoutControls();
  }

  document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const requestedTier = params.get('tier');
    if (requestedTier && TIERS[requestedTier]) {
      currentTier = requestedTier;
    }

    const tierCards = document.querySelectorAll('.tier-card');
    tierCards.forEach(function (card) {
      card.addEventListener('click', function () {
        selectTier(card.getAttribute('data-tier'));
      });
      card.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter' || ev.key === ' ') {
          ev.preventDefault();
          selectTier(card.getAttribute('data-tier'));
        }
      });
    });

    const licenseeInput = document.getElementById('licensee-name-input');
    if (licenseeInput) {
      licenseeInput.addEventListener('input', updateCheckoutControls);
    }

    selectTier(currentTier);
  });
})();
