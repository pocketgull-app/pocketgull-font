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
  });
})();
