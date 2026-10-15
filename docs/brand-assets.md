# honeybees brand assets

## Logo

The brand is **honeybees.consulting** (lowercase). The primary logo is the Leafwing bee: leaf-shaped wings (nature), one ink head-and-thorax, two bands on a pollen body, one antenna, climbing up and to the right. It came out of the A Leafwing → A7 Aviator → honeybees rounds, and Daksh chose the sans lockup and one honey yellow for every bee on 2026-10-15.

- `dist/assets/honey-bee-logo.svg` / `.png`: horizontal lockup, DM Sans Bold wordmark with the text outlined, tracked CONSULTING and a pollen dash.
- `dist/assets/honeybees-logo-light.svg`: the same lockup for dark backgrounds (ivory keyline around the bee).
- `dist/assets/bee-mark-colour.svg` / `bee-mark.png`: full-colour mark, for 48px and up.
- `dist/assets/bee-mark.svg`: solid one-colour silhouette with the bands and wing gaps cut out, legs dropped, for the favicon and anything under 48px.

All of these come from `scripts/brand/bees.py`, which also draws the bee family. Change the drawing there and re-run it rather than editing the SVGs by hand.

## The bee family

One body, told apart by a single prop and pose, never by costumes or faces, so the characters stay grown-up. All are honey yellow.

- **The Guide** (A7's goggles): follows the visitor through the homepage.
- **The Forager** (pollen ball): carries value from the meadow to the hive.
- **The Scout** (lens): customer evidence and ratings.
- **The Grower** (sprout): CSR strategy and action plans.
- **The Builder** (honey cell): ESG reporting and projects.
- **The Messenger** (front-facing, envelope): the only bee that looks at you, at Contact. Its eyes follow the pointer when motion is on.

## Palette and typography

Ink `#17291F`, pollen `#EABB35`, forest `#284F38`, ivory `#F7F6EE` and pale wing `#F3F8EA`. Instrument Serif supplies the editorial headings; DM Sans supplies the working text and the wordmark. Both are self-hosted with their OFL licences.

## Website imagery

`dist/assets/bee-meadow.webp` is a generated illustrative nature image, created using the built-in image-generation tool. It is not evidence of a client project or environmental result. The original was copied into the project as an optimised asset. `dist/assets/daksh.webp` is an optimised copy of Daksh’s own public portfolio portrait.

The three SVG service illustrations are adapted from the code-native illustrations in Daksh’s personal portfolio at commit `89f19c8adfddef72af58f733f5348463f87de76f`, with self-contained honey and olive colours. They retain the portfolio’s visual language. The service cards also follow its square-art, rounded-card layout. EcoVadis and CDP marks are exact copies of the public portfolio assets, used to identify questionnaire frameworks rather than as client or certification claims.

## Image-generation prompt

> Use case: photorealistic-natural. Asset type: editorial image for Honey Bee Consulting, a new CSR/ESG consulting website with warm honey yellow, dark ink and cream art direction. Primary request: create a beautiful truthful-looking macro nature photograph of one honey bee gathering pollen from a pale golden yellow flower, showing subtle pollen and delicate translucent wings. Natural setting in a French wildflower meadow. Style: fine editorial botanical photography, organic and detailed, soft natural daylight, quiet and confident, shallow depth of field with warm olive muted background, not excessively glossy. Composition: near-square landscape, bee and flower clearly visible in central-right area, pleasing petals occupying lower third, muted uncluttered background upper left. No text, logos, charts, collage, human faces, business claims, fantasy bee, extra legs or extra wings. This is illustrative generated nature imagery, not evidence of a client project.

The services page uses this image as a full-width hero with an independently drawn dark overlay. The slow zoom pauses on request, off-screen and in background tabs, and respects reduced-motion preferences.

## Optional export regeneration

The share card `dist/assets/social-cover.png` is a 1200×630 render of the homepage hero art and headline.

With the optional Sharp dependency installed, use Node 22 and pass your original bee and founder files:

```sh
node scripts/prepare-assets.mjs /path/to/bee-photo.png /path/to/founder-portrait.png
```

Use `node scripts/prepare-assets.mjs --logos-only` to re-export the PNG logos from the SVGs without changing the photography.

Published optimised images are already included, so normal website edits do not need this step.
