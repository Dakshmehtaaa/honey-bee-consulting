# honeybees.consulting

A practical CSR and ESG consulting website for Daksh Mehta. Two audience paths: smaller businesses building their foundations and established teams seeking focused project support.

**Public website:** https://honeybees.consulting/ (GitHub Pages custom domain; `dist/CNAME`)
**French homepage:** https://honeybees.consulting/fr.html

## The experience

The homepage (`dist/index.html`) is a short scroll story with very little text: the hive (the business), the meadow (nature and people), the bees (the work in between), the honey (why CSR pays back), three ways we help, Daksh, and contact. A guide bee follows the visitor from chapter to chapter, landing on `[data-perch]` points (`dist/assets/story.js`). A short loader plays once per browser session. Calm mode (header switch, remembered) and `prefers-reduced-motion` turn all of that off, and every chapter has a finished resting state without JavaScript. The detailed, text-rich site lives one click away on `dist/services.html`:

- Full-image bee hero, with gentle motion, a pause control and reduced-motion support.
- Portfolio-style service cards with square illustrations, short copy, framework marks and mobile swipe/arrow navigation. Deliverables open on request.
- An interactive buyer-request comparison: organise evidence, measure an action and assign an owner. A short replay shows the preparation building, with pause and reduced-motion support.
- Concrete business benefits and measures, available on request, with clear limits on commercial outcomes.
- A priority guide and cost-saving scenario calculator. Tools open on request and run locally.
- An evidence-register template in English and French, without an email gate.
- Founder background, useful official resources and an enquiry form that prepares an email draft.
- English and French, including a static French homepage for search and direct sharing.
- Original vector bee logo, transparent PNG exports, self-hosted fonts and a privacy page.

There are no analytics, remote form submissions, paid services or runtime dependencies. Only the language preference is stored by the site. Visitors review and send their enquiry from their own email application.

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

- **English content:** `dist/index.html` (story), `dist/services.html` (details) and `dist/privacy.html`.
- **Story styling and motion:** `dist/assets/story.css` and `dist/assets/story.js`. Animations only add start states under `.motion`, so never hide content outside that class.
- **Logo and bee characters:** `scripts/brand/bees.py` (see `docs/brand-assets.md`).
- **French content:** `dist/assets/fr.json`. Preserve the scope and limitations of the English copy.
- **Dynamic tools and labels:** `dist/assets/app.js`.
- **Calculator and draft logic:** `dist/assets/business-core.js`.
- **Design:** `dist/assets/style.css` and `dist/assets/experience.css`.
- **Service navigation and comparison:** `dist/assets/experience.js`.
- **Contact:** search the HTML and `business-core.js` for `Dakshmehta077@gmail.com` when replacing it with the future business address.

After changing English or French copy, regenerate the shared dictionary and the static French homepage:

```sh
node scripts/compile-copy.mjs
node --test tests/*.test.cjs
```

`dist/fr.html` is the static French story page. Do not edit `dist/fr.html` or `dist/assets/copy.js` directly; they are generated from the source copy.

## Publishing

GitHub Actions publishes the checked `dist/` directory when `main` changes. The workflow also runs the business-tool, local-link and translation checks. `.openai/hosting.json` records the separate private Sites preview identity and its static output directory.

## Sources and assets

The site takes content and visual inspiration from [Daksh’s portfolio](https://dakshmehtaaa.github.io/personal-website-/), source commit `89f19c8adfddef72af58f733f5348463f87de76f`. Founder roles remain contribution-level background; previous employers are not presented as Honey Bee clients. The service offers describe proposed work, not completed client engagements.

See [the source review](docs/content-source-review.md), [brand assets and image brief](docs/brand-assets.md), and [the independent audit](docs/independent-audit.md). Font licences are retained with the fonts. Public-resource links lead to their respective official publishers.
