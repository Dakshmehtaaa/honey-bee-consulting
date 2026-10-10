# Honey Bee brand assets

## Logo

The original bee mark is a minimal ink silhouette: one clear round head, two plain wings and a single open band through the body. Three filled vector elements keep it readable at small sizes. The wordmark gives the identity a warm, restrained consulting feel.

- `dist/assets/bee-mark.svg`: scalable transparent mark, used in the header and favicon.
- `dist/assets/bee-mark.png`: transparent 512-pixel mark.
- `dist/assets/honey-bee-logo.svg`: transparent horizontal logo lockup.
- `dist/assets/honey-bee-logo.png`: transparent horizontal PNG lockup.
- `dist/assets/social-cover.png`: social-sharing cover.

The logo was drawn in editable vector form, then simplified to a clear silhouette with three elements.

## Palette and typography

Ink `#24251f`, honey `#f3c544`, warm paper `#fbfaf5`, and olive `#596747`. Instrument Serif supplies the editorial headings; DM Sans supplies the working text. Both are self-hosted with their OFL licences.

## Website imagery

`dist/assets/bee-meadow.webp` is a generated illustrative nature image, created using the built-in image-generation tool. It is not evidence of a client project or environmental result. The original was copied into the project as an optimised asset. `dist/assets/daksh.webp` is an optimised copy of Daksh’s own public portfolio portrait.

The three SVG service illustrations are adapted from the code-native illustrations in Daksh’s personal portfolio at commit `89f19c8adfddef72af58f733f5348463f87de76f`, with self-contained honey and olive colours. They retain the portfolio’s visual language. The service cards also follow its square-art, rounded-card layout. EcoVadis and CDP marks are exact copies of the public portfolio assets, used to identify questionnaire frameworks rather than as client or certification claims.

## Image-generation prompt

> Use case: photorealistic-natural. Asset type: editorial image for Honey Bee Consulting, a new CSR/ESG consulting website with warm honey yellow, dark ink and cream art direction. Primary request: create a beautiful truthful-looking macro nature photograph of one honey bee gathering pollen from a pale golden yellow flower, showing subtle pollen and delicate translucent wings. Natural setting in a French wildflower meadow. Style: fine editorial botanical photography, organic and detailed, soft natural daylight, quiet and confident, shallow depth of field with warm olive muted background, not excessively glossy. Composition: near-square landscape, bee and flower clearly visible in central-right area, pleasing petals occupying lower third, muted uncluttered background upper left. No text, logos, charts, collage, human faces, business claims, fantasy bee, extra legs or extra wings. This is illustrative generated nature imagery, not evidence of a client project.

The final site uses this image as a full-width hero with an independently drawn dark overlay. The slow zoom pauses on request, off-screen and in background tabs, and respects reduced-motion preferences.

## Optional export regeneration

With the optional Sharp dependency installed, use Node 22 and pass your original bee and founder files:

```sh
node scripts/prepare-assets.mjs /path/to/bee-photo.png /path/to/founder-portrait.png
```

Use `node scripts/prepare-assets.mjs --logos-only` to update logo exports without changing the photography.

Published optimised images are already included, so normal website edits do not need this step.
