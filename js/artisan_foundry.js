/**
 * PocketGull Artisan Foundry Controller (artisan_foundry.html)
 * External module for CSP Observatory 125+ zero-unsafe-inline compliance.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var stage = document.getElementById('kintsugiTester');
    var card = stage ? stage.closest('.specimen-kintsugi') : null;
    var btns = document.querySelectorAll('.pal-btn');

    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');

        var pal = btn.getAttribute('data-palette');
        var bg = btn.getAttribute('data-bg');
        if (stage && pal) {
          stage.style.fontPalette = pal;
        }
        if (card && bg) {
          card.style.background = bg;
          var isLight = bg !== '#0f172a';
          card.style.color = isLight ? '#1c1917' : '#f8fafc';
          var desc = card.querySelector('.kintsugi-desc');
          if (desc) {
            desc.style.color = isLight ? '#44403c' : '#cbd5e1';
          }
          var palTitle = card.querySelector('.kintsugi-pal-title');
          if (palTitle) {
            palTitle.style.color = isLight ? '#78350f' : '#fde68a';
          }
        }
      });
    });

    // Post-Checkout Instant ZIP Delivery Handler (?paid=1&tier=...&session_id=...)
    var params = new URLSearchParams(window.location.search);
    if (params.get('paid') === '1') {
      var tier = params.get('tier') || 'artisan_duo_patron';
      var sessionId = params.get('session_id') || '';
      var bundles = {
        botanica_pro: {
          title: 'PocketGull Botanica™ v3 — Herbarium Pro Pack Ready!',
          zip: 'fonts/foundry/PocketGull-Botanica-Pro-v4.0.0.zip',
          btn: '⬇ Download Botanica v3 Pro Pack (.ZIP)'
        },
        kinpaku_pro: {
          title: 'PocketGull Kinpaku™ (金箔) — 24k Gold COLR Pro Pack Ready!',
          zip: 'fonts/foundry/PocketGull-Kinpaku-Pro-v4.0.0.zip',
          btn: '⬇ Download Kinpaku 24k Gold Pro Pack (.ZIP)'
        },
        kintsugi_pro: {
          title: 'PocketGull Kinpaku™ (金箔) — 24k Gold COLR Pro Pack Ready!',
          zip: 'fonts/foundry/PocketGull-Kinpaku-Pro-v4.0.0.zip',
          btn: '⬇ Download Kinpaku 24k Gold Pro Pack (.ZIP)'
        },
        artisan_duo_patron: {
          title: 'PocketGull Artisan Duo™ & Patron Pass Ready!',
          zip: 'fonts/foundry/PocketGull-Artisan-Pro-Pack-v4.0.0.zip',
          btn: '⬇ Download Complete Artisan Duo Suite (.ZIP)'
        },
        foundry_agency: {
          title: 'PocketGull Unlimited Agency Suite & Warranty Ready!',
          zip: 'fonts/foundry/PocketGull-Artisan-Pro-Pack-v4.0.0.zip',
          btn: '⬇ Download Unlimited Agency Suite (.ZIP)'
        }
      };

      var cfg = bundles[tier] || bundles.artisan_duo_patron;
      var banner = document.getElementById('paidDeliveryBanner');
      var titleEl = document.getElementById('paidTitle');
      var metaEl = document.getElementById('paidMeta');
      var linkEl = document.getElementById('paidDownloadLink');

      if (banner && titleEl && linkEl) {
        titleEl.textContent = cfg.title;
        linkEl.setAttribute('href', cfg.zip);
        linkEl.textContent = cfg.btn;
        if (metaEl && /^cs_(live|test)_[A-Za-z0-9_]+$/.test(sessionId)) {
          metaEl.textContent = 'Stripe Session Reference: ' + sessionId + ' • Perpetual Commercial Studio EULA & Eco-Ink Attestation included inside archive.';
        }
        banner.classList.add('visible');
      }
    }
  });
})();
