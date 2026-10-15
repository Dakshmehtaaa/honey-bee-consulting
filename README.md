# honeybees.consulting

An ESG and CSR consulting website for companies, by Daksh Mehta. One message, said plainly: sooner or later your customers choose the more sustainable supplier, so turn ESG into your competitive edge.

**Public website:** https://honeybees.consulting/ (GitHub Pages custom domain; `dist/CNAME`)
**French homepage:** https://honeybees.consulting/fr.html

## The site

- `dist/index.html`, the homepage, is a short illustrated scroll in five chapters: the hero (turn ESG into your competitive edge), the market (many competitors, each with an ESG score out of 100, clients pick the best), beyond compliance (compliance is the floor, performance wins clients, shown as a four-step loop: Environment, People, Proof, Clients, which autoplays while in view and pauses on hover or focus), four ways we help (the Inspector, the Engineer, the Storyteller and the Gardener, each with six frameworks and tools) and contact. A guide bee flies from chapter to chapter, landing on `[data-perch]` points (`dist/assets/story.js`). At the top its goggles lie in the grass; it puts them on as soon as the visitor scrolls. A short loader plays once per browser session. Calm mode (header switch, remembered) and `prefers-reduced-motion` turn all motion off, and every chapter has a finished resting state without JavaScript.
- `dist/contact.html`: the enquiry form, which prepares an email draft in the visitor's own email app, plus direct contact details.
- `dist/resources.html`: free frameworks and tools to get started, filterable by stage (Measure, Decide, Disclose, Act), taken from the resources on Daksh's personal website.
- `dist/privacy.html`: publisher, data handling and the newsletter.
- `dist/v1.html`: the first version of the site, kept as an archive (noindex, linked from the footer, with a banner back to the current site). `dist/services.html` redirects there so old links still work.
- Every page has the same header (Why ESG, How we help, Resources, Contact) and footer, with a newsletter sign-up that collects email addresses only (see `backend/newsletter/`).

English and French throughout, including a static French homepage for search and direct sharing. No analytics, advertising pixels or tracking cookies. The only data the site sends anywhere is a newsletter sign-up, and only when someone subscribes.

## Preview and checks

Serve the published directory from the project root:

```sh
python3 -m http.server 8028 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8028/`. For the checks, use Node 22 or newer:

```sh
node --test tests/*.test.cjs
```

No package installation is needed to view or serve the website or run those checks. The optional Sharp development dependency is used only to regenerate image exports.

## Editing

- **English content:** `dist/index.html`, `dist/contact.html`, `dist/resources.html` and `dist/privacy.html`.
- **Shared header, footer and drawings:** don't edit the blocks between `<!--part:…-->` / `<!--art:…-->` markers by hand. The header, footer and head script come from `scripts/build-pages.py`; the drawings from `scripts/brand/site_art.py` (scene helpers in `scripts/brand/art.py`, bees in `scripts/brand/bees.py`). Re-run `python3 scripts/build-pages.py` after changing any of them (`--preview DIR` also writes each drawing as its own SVG).
- **Styling and motion:** `dist/assets/story.css` and `dist/assets/story.js`. Animations only add start states under `.motion`, so never hide content outside that class.
- **Framework and tool logos:** `dist/assets/logos/`. On the homepage each logo has its own `--h` (start from 34px × aspect^-0.42, then nudge thin marks up and solid ones down by eye); on the resources page each has its own `--mw`.
- **French content:** `dist/assets/fr.json`. Every `data-i18n` key needs a French entry (the tests check it).
- **Newsletter and email drafts:** `dist/assets/business-core.js` (`NEWSLETTER_URL`, `subscription`, `enquiryLink`).
- **V1 archive:** `dist/v1.html` with `dist/assets/app.js`, `experience.js`, `style.css` and `experience.css`. Leave it as it is.
- **Contact:** search the HTML and `business-core.js` for `dakshmehta077@gmail.com` (any case) when replacing it with the future business address.

After changing pages, art or copy, rebuild and check:

```sh
python3 scripts/build-pages.py
node scripts/compile-copy.mjs
node --test tests/*.test.cjs
```

`dist/fr.html` is the static French story page. Do not edit `dist/fr.html` or `dist/assets/copy.js` directly; they are generated from the source copy.

## Publishing

GitHub Actions publishes the checked `dist/` directory when `main` changes. The workflow also runs the business-logic, newsletter, local-link, id and translation checks. The newsletter backend in `backend/newsletter/` is not published with the site; it runs as a Google Apps Script (setup in its README). `.openai/hosting.json` records the separate private Sites preview identity and its static output directory.

## Sources and assets

The site takes content and visual inspiration from [Daksh’s portfolio](https://dakshmehtaaa.github.io/personal-website-/), source commit `89f19c8adfddef72af58f733f5348463f87de76f`. Founder roles remain contribution-level background; previous employers are not presented as Honey Bee clients. The service offers describe proposed work, not completed client engagements.

See [the source review](docs/content-source-review.md), [brand assets and image brief](docs/brand-assets.md), and [the independent audit](docs/independent-audit.md). Font licences are retained with the fonts. Public-resource links lead to their respective official publishers.
