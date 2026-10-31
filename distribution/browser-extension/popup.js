'use strict';

/**
 * PocketGull Unicode & Font Leak Inspector (Manifest V3 Popup Controller)
 * Strictly enforces DOM XSS prevention (uses textContent / createElement only, zero innerHTML).
 * Zero network egress; runs only when triggered by the user on the active tab.
 */

function inspectActiveDocument(revealBadges) {
  const UNCONDITIONAL_SPOOF_VECTORS = new Map([
    [0x202A, 'U+202A LRE (BiDi Override)'],
    [0x202B, 'U+202B RLE (BiDi Override)'],
    [0x202C, 'U+202C PDF (BiDi Pop)'],
    [0x202D, 'U+202D LRO (BiDi Override)'],
    [0x202E, 'U+202E RLO (Trojan Source CVE-2021-42574)'],
    [0x2066, 'U+2066 LRI (BiDi Isolate)'],
    [0x2067, 'U+2067 RLI (BiDi Isolate)'],
    [0x2068, 'U+2068 FSI (BiDi Isolate)'],
    [0x2069, 'U+2069 PDI (BiDi Isolate Pop)'],
    [0x115F, 'U+115F Hangul Choseong Filler (Fake Space)'],
    [0x1160, 'U+1160 Hangul Jungseong Filler (Fake Space)'],
    [0x3164, 'U+3164 Hangul Filler (Fake Space)'],
    [0xFFA0, 'U+FFA0 Halfwidth Hangul Filler (Fake Space)'],
    [0x2061, 'U+2061 Function Application (Invisible Math)'],
    [0x2062, 'U+2062 Invisible Times (Invisible Math)'],
    [0x2063, 'U+2063 Invisible Separator (Invisible Math)'],
    [0x2064, 'U+2064 Invisible Plus (Invisible Math)']
  ]);

  const SAFE_JOINERS = new Set([0x200C, 0x200D, 0x061C, 0x180E, 0xFE0E, 0xFE0F, 0xFEFF]);

  const bodyText = document.body ? document.body.innerText : '';
  const spoofCounts = {};
  let safeJoinerCount = 0;
  let emojiSmugglingCount = 0;
  let inSubdivisionFlag = false;

  for (const ch of bodyText) {
    const cp = ch.codePointAt(0);
    if (cp === 0x1F3F4) {
      inSubdivisionFlag = true;
      continue;
    }
    if (cp >= 0xE0000 && cp <= 0xE007F) {
      if (inSubdivisionFlag) {
        safeJoinerCount++;
      } else {
        const tagLabel = 'U+E0000..U+E007F Detached ASCII Tag (Prompt Injection)';
        spoofCounts[tagLabel] = (spoofCounts[tagLabel] || 0) + 1;
      }
      if (cp === 0xE007F) inSubdivisionFlag = false;
      continue;
    }
    inSubdivisionFlag = false;

    if (UNCONDITIONAL_SPOOF_VECTORS.has(cp)) {
      const label = UNCONDITIONAL_SPOOF_VECTORS.get(cp);
      spoofCounts[label] = (spoofCounts[label] || 0) + 1;
    } else if (cp >= 0xE0100 && cp <= 0xE01EF) {
      emojiSmugglingCount++;
    } else if (SAFE_JOINERS.has(cp)) {
      safeJoinerCount++;
    }
  }

  // Audit <link rel="preload" as="font"> for missing Subresource Integrity (SRI) or crossorigin
  const fontLinks = Array.from(document.querySelectorAll('link[as="font"], link[rel="preload"][href*=".woff"], link[rel="preload"][href*=".ttf"]'));
  let missingSriCount = 0;
  let missingCorsCount = 0;
  for (const link of fontLinks) {
    const href = link.getAttribute('href') || '';
    if (href.startsWith('http') && !link.getAttribute('integrity')) {
      missingSriCount++;
    }
    if (!link.hasAttribute('crossorigin')) {
      missingCorsCount++;
    }
  }

  if (revealBadges && document.body) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    while (walker.nextNode()) {
      textNodes.push(walker.currentNode);
    }
    for (const node of textNodes) {
      let updated = '';
      let changed = false;
      let nodeInFlag = false;
      for (const ch of node.nodeValue) {
        const cp = ch.codePointAt(0);
        if (cp === 0x1F3F4) {
          nodeInFlag = true;
          updated += ch;
          continue;
        }
        if (cp >= 0xE0000 && cp <= 0xE007F) {
          if (nodeInFlag) {
            updated += ch;
          } else {
            updated += '[!U+' + cp.toString(16).toUpperCase() + ']';
            changed = true;
          }
          if (cp === 0xE007F) nodeInFlag = false;
          continue;
        }
        nodeInFlag = false;
        if (UNCONDITIONAL_SPOOF_VECTORS.has(cp) || (cp >= 0xE0100 && cp <= 0xE01EF)) {
          updated += '[!U+' + cp.toString(16).toUpperCase() + ']';
          changed = true;
        } else {
          updated += ch;
        }
      }
      if (changed) {
        node.nodeValue = updated;
      }
    }
  }

  return {
    spoofCounts,
    emojiSmugglingCount,
    safeJoinerCount,
    fontLinkCount: fontLinks.length,
    missingSriCount,
    missingCorsCount
  };
}

function renderReport(report) {
  const statusLine = document.getElementById('statusLine');
  const findingsList = document.getElementById('findingsList');
  statusLine.textContent = '';
  findingsList.textContent = '';

  const spoofKeys = Object.keys(report.spoofCounts);
  const totalDanger = spoofKeys.length + (report.emojiSmugglingCount > 0 ? 1 : 0);

  const badge = document.createElement('span');
  if (totalDanger > 0) {
    badge.className = 'status-badge status-danger';
    badge.textContent = 'ALERT: Hidden Spoofing / Smuggling Detected';
  } else if (report.missingSriCount > 0 || report.missingCorsCount > 0) {
    badge.className = 'status-badge status-warn';
    badge.textContent = 'NOTICE: Webfont SRI / CORS Advisory';
  } else {
    badge.className = 'status-badge status-ok';
    badge.textContent = 'CLEAN: 0 Spoofing Leaks Found';
  }
  statusLine.appendChild(badge);

  for (const key of spoofKeys) {
    const li = document.createElement('li');
    li.textContent = `${key}: ${report.spoofCounts[key]} instance(s) [uni202E.guard]`;
    findingsList.appendChild(li);
  }

  if (report.emojiSmugglingCount > 0) {
    const li = document.createElement('li');
    li.textContent = `Variation Selectors Supplement (U+E0100-U+E01EF): ${report.emojiSmugglingCount} hidden byte(s)`;
    findingsList.appendChild(li);
  }

  const joinerLi = document.createElement('li');
  joinerLi.textContent = `Legitimate Joiners (ZWNJ/ZWJ/VS16): ${report.safeJoinerCount} preserved cleanly [uni200C.joiner]`;
  findingsList.appendChild(joinerLi);

  const fontLi = document.createElement('li');
  fontLi.textContent = `Preloaded Font Links: ${report.fontLinkCount} (${report.missingSriCount} missing external SRI, ${report.missingCorsCount} missing crossorigin)`;
  findingsList.appendChild(fontLi);
}

function triggerScan(revealBadges) {
  if (!chrome || !chrome.tabs || !chrome.scripting) return;
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs || !tabs[0] || !tabs[0].id) return;
    chrome.scripting.executeScript(
      {
        target: { tabId: tabs[0].id },
        func: inspectActiveDocument,
        args: [revealBadges]
      },
      (results) => {
        if (results && results[0] && results[0].result) {
          renderReport(results[0].result);
        }
      }
    );
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const btnScan = document.getElementById('btnScanPage');
  const btnReveal = document.getElementById('btnRevealBadges');
  if (btnScan) btnScan.addEventListener('click', () => triggerScan(false));
  if (btnReveal) btnReveal.addEventListener('click', () => triggerScan(true));
});
