import fs from 'node:fs/promises';
import path from 'node:path';
const sharp = (await import(process.env.HONEY_SHARP_MODULE || 'sharp')).default;
const root = path.resolve(import.meta.dirname, '..');
const assets = path.join(root, 'dist/assets');
const [generated, portrait] = process.argv.slice(2);
if (generated !== '--logos-only') {
  if (!generated || !portrait) throw new Error('Usage: node scripts/prepare-assets.mjs <bee-photo.png> <founder-portrait.png> or --logos-only');
  await sharp(generated).resize({ width: 1200 }).webp({ quality: 84 }).toFile(path.join(assets, 'bee-meadow.webp'));
  await sharp(portrait).resize({ width: 850 }).webp({ quality: 88 }).toFile(path.join(assets, 'daksh.webp'));
}
// Logos are drawn by scripts/brand/bees.py (vector, text outlined). This only exports PNG copies.
await sharp(path.join(assets, 'bee-mark-colour.svg')).resize(512, 512).png().toFile(path.join(assets, 'bee-mark.png'));
await sharp(path.join(assets, 'honey-bee-logo.svg')).resize({ width: 1200 }).png().toFile(path.join(assets, 'honey-bee-logo.png'));
console.log(generated === '--logos-only' ? 'Exported PNG logos.' : 'Prepared bee image, founder portrait and PNG logos.');
