# Wikipedia Submission Checklist

The article draft is [`PocketGull_Wikipedia_Entry.wiki`](./PocketGull_Wikipedia_Entry.wiki).

## 1. Notability (WP:GNG) — the main blocker
Every current citation is self-published. Wikipedia needs significant coverage from sources independent of the project. Obtain at least 2–3 of:
- [ ] Google Fonts listing / Google Fonts blog or Knowledge entry (after onboarding)
- [ ] Design press (Typewolf, Fonts In Use, Print, Creative Bloq, Eye on Design)
- [ ] Healthcare / human-factors press or journal mention (peer-reviewed paper, ISMP, HIMSS)
- [ ] Independent reviews or Fonts In Use entries showing real-world deployment

Then replace the `repo` and `specimen` refs with these where possible.

## 2. Conflict of interest (WP:COI)
- [ ] Disclose the COI on your Wikipedia user page (WP:PAID/COI)
- [ ] Submit via Articles for Creation (Wikipedia:Articles for creation) instead of publishing directly
- [ ] Discuss changes on the article Talk page

## 3. Assets
- [ ] Upload a specimen image to Wikimedia Commons under a free license, then add `| image =` to the infobox
- [ ] Optionally add a disambiguation-matrix SVG

## 4. Verify before submitting
- [ ] Confirm the "about 14,000 glyphs" figure against the released fonts (audited at about 14,200 in the Bold, Fineliner and Chiseltip styles)
- [ ] Confirm the OTS statement against a current `npm run test:unit` run
