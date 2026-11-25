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
- [x] Generate path-outlined Wikimedia Commons specimen (`PocketGull_Specimen_Commons.svg`, zero `<text>` dependencies) and wire `| image = PocketGull_Specimen_Commons.svg` into `{{Infobox font}}`
- [ ] Upload `PocketGull_Specimen_Commons.svg` via https://commons.wikimedia.org/wiki/Special:UploadWizard under `CC0` or `CC BY-SA 4.0`

## 4. Verify before submitting
- [x] Confirm glyph counts against `v4.0.0` TTF binaries (`8,229` glyphs in `PocketGull-Regular` / `PocketGull-Bold`; up to `9,880` codepoints in `PocketGull-Math`)
- [x] Confirm the OTS statement against a current `npm run test:unit` run (`149/149` passing)
