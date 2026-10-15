import fs from 'node:fs/promises';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
const french = JSON.parse(await fs.readFile(path.join(root, 'dist/assets/fr.json'), 'utf8'));
const english = {};
const attributes = {};
function decode(text) { return text.replaceAll('&amp;', '&').replaceAll('&quot;', '"').replaceAll('&#39;', "'").replaceAll('&lt;', '<').replaceAll('&gt;', '>'); }
function encode(text) { return text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;'); }
const tagPattern = /(<([a-z][\w-]*)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)([^<]*)(<\/\2>)/gi;
for (const name of ['index.html', 'contact.html', 'resources.html', 'privacy.html', 'v1.html']) {
  const html = await fs.readFile(path.join(root, 'dist', name), 'utf8');
  for (const match of html.matchAll(tagPattern)) english[match[3]] = decode(match[4]);
  for (const [key, attribute] of [['data-i18n-aria', 'aria-label'], ['data-i18n-alt', 'alt'], ['data-i18n-placeholder', 'placeholder']]) {
    for (const tag of html.matchAll(/<[^>]+>/g)) {
      const id = tag[0].match(new RegExp(key + '="([^"]+)"'));
      const value = tag[0].match(new RegExp('\\b' + attribute + '="([^"]*)"'));
      if (id && value) attributes[id[1]] = decode(value[1]);
    }
  }
}
const globals = { HONEY_FRENCH: french, HONEY_ENGLISH: english, HONEY_EN_ATTRIBUTES: attributes };
await fs.writeFile(path.join(root, 'dist/assets/copy.js'), Object.entries(globals).map(([key, value]) => 'window.' + key + ' = ' + JSON.stringify(value, null, 2) + ';').join('\n') + '\n');
let html = await fs.readFile(path.join(root, 'dist/index.html'), 'utf8');
html = html.replace('<html lang="en">', '<html lang="fr">');
html = html.replace(tagPattern, (whole, opening, tag, key, text, closing) => opening + encode(french[key] || decode(text)) + closing);
for (const [key, attribute] of [['data-i18n-aria', 'aria-label'], ['data-i18n-alt', 'alt'], ['data-i18n-placeholder', 'placeholder']]) {
  html = html.replace(/<[^>]+>/g, tag => {
    const id = tag.match(new RegExp(key + '="([^"]+)"'));
    return id && french[id[1]] ? tag.replace(new RegExp('\\b' + attribute + '="[^"]*"'), attribute + '="' + encode(french[id[1]]) + '"') : tag;
  });
}
// fr.html is the static French version of the storytelling homepage. Its links to the other pages carry ?lang=fr,
// so the French choice survives a visit without JavaScript too.
html = html.replace(/<a\b[^>]*\bdata-lang-link\b[^>]*>/g, tag => tag.replace(/href="([^"?#]+)(?:\?[^"#]*)?(#[^"]*)?"/, (all, page, hash) => 'href="' + page + '?lang=fr' + (hash || '') + '"'));
html = html.replace(/<title>[^<]*<\/title>/, '<title>' + encode(french['story.meta.title']) + '</title>');
html = html.replace(/(<meta name="description" content=")[^"]*/, '$1' + encode(french['story.meta.description']));
html = html.replace(/(<meta property="og:title" content=")[^"]*/, '$1' + encode(french['story.meta.title']));
html = html.replace(/(<meta property="og:description" content=")[^"]*/, '$1' + encode(french['story.meta.description']));
html = html.replace('rel="canonical" href="https://honeybees.consulting/"', 'rel="canonical" href="https://honeybees.consulting/fr.html"');
html = html.replace('property="og:url" content="https://honeybees.consulting/"', 'property="og:url" content="https://honeybees.consulting/fr.html"');
await fs.writeFile(path.join(root, 'dist/fr.html'), html);
console.log('Compiled French copy: ' + Object.keys(french).length + ' entries and static French homepage.');
