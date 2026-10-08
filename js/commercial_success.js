/**
 * PocketGull Commercial Licensing — Success & Download Controller
 * Pure DOM textContent security (OWASP & CodeQL safe).
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const orderId = params.get('orderId') || 'PG-' + Date.now();
    const tier = params.get('tier') || 'studio';
    const licensee = params.get('licensee') || 'Valued Commercial Licensee';
    const email = params.get('email') || 'licensee@example.com';
    const token = params.get('token');
    const sig = params.get('sig');

    const tierLabels = {
      solo: 'Solo Designer / Indie Practitioner (1 User, 3 Workstations)',
      studio: 'Studio / Agency (Up to 10 Workstations, 10 Apps)',
      enterprise: 'Enterprise / Health System & EHR (Unlimited Enterprise-wide)'
    };

    // Populate Receipt Fields
    const elOrder = document.getElementById('out-order-id');
    const elLicensee = document.getElementById('out-licensee');
    const elTier = document.getElementById('out-tier');
    const btnDownload = document.getElementById('btn-main-download');
    const btnCert = document.getElementById('btn-cert-download');

    if (elOrder) elOrder.textContent = orderId;
    if (elLicensee) elLicensee.textContent = licensee;
    if (elTier) elTier.textContent = tierLabels[tier.toLowerCase()] || tierLabels.studio;

    // Configure primary download button if signed token is present
    if (token && sig && btnDownload) {
      btnDownload.href = `/api/download?token=${encodeURIComponent(token)}&sig=${encodeURIComponent(sig)}`;
    }

    // Configure Certificate Download
    if (btnCert) {
      btnCert.addEventListener('click', () => {
        const certText = `================================================================================
POCKETGULL™ TYPEFACE SUPERFAMILY — COMMERCIAL CERTIFICATE OF LICENSE
================================================================================
Transaction ID       : ${orderId}
Issue Date           : ${new Date().toISOString()}
Authorized Licensee  : ${licensee}
Registered Email     : ${email}
License Tier         : ${(tierLabels[tier.toLowerCase()] || tier).toUpperCase()}
Superfamily Version  : 3.1.0 (38 Cuts + Variable VF Suite)
Foundry & Designer   : Phillip Gear / Geararts LLC (https://font.pocketgull.app)
Governing Law        : State of Oregon, United States of America

SUMMARY OF PERMITTED USE & COMMERCIAL WARRANTY:
1. Grant of License: Phillip Gear / Geararts LLC grants the Licensee a perpetual,
   worldwide, non-exclusive license to utilize PocketGull under the purchased tier.
2. Clinical Disambiguation: Adheres to ISMP (Institute for Safe Medication Practices)
   and Louise Sloan 5:1 optotype legibility standards.
3. Open Source Coexistence: Incorporates full proprietary 38-cut suite (Telemetry,
   Math, Chem, Genome, ASL, Slab, Soft, Halftone, and 2-Axis Variable builds).

Counter-signed: Phillip Gear, Type Designer & Foundry Director
================================================================================
`;
        const blob = new Blob([certText], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `PocketGull-License-Certificate-${orderId}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }
  });
})();
