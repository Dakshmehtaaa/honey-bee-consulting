const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../dist');
const pages = ['index.html', 'fr.html', 'contact.html', 'resources.html', 'privacy.html', 'services.html'];
test('Published HTML references resolve to real assets and local anchors', () => {
  for (const file of pages) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
      const url = match[1];
      if (/^(?:https?:|mailto:|data:)/.test(url)) continue;
      if (url.startsWith('#')) {
        assert.ok(html.includes('id="' + url.slice(1) + '"'), file + ': missing anchor ' + url);
      } else {
        assert.ok(fs.existsSync(path.join(root, url.split(/[?#]/)[0])), file + ': missing asset ' + url);
      }
    }
  }
});
test('All published text and accessible labels have a French translation', () => {
  const french = JSON.parse(fs.readFileSync(path.join(root, 'assets/fr.json'), 'utf8'));
  for (const file of pages) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    for (const match of html.matchAll(/data-i18n(?:-aria|-alt|-placeholder)?="([^"]+)"/g)) {
      assert.equal(typeof french[match[1]], 'string', 'Missing French key: ' + match[1]);
      assert.ok(french[match[1]].trim(), 'Empty French key: ' + match[1]);
    }
  }
});
test('Self-hosted fonts have matching files and retained licences', () => {
  const css = fs.readFileSync(path.join(root, 'assets/fonts/fonts.css'), 'utf8');
  for (const match of css.matchAll(/url\(([^)]+)\)/g)) {
    assert.ok(fs.existsSync(path.join(root, 'assets/fonts', match[1])));
  }
  assert.ok(fs.existsSync(path.join(root, 'assets/fonts/dmsans-OFL.txt')));
  assert.ok(fs.existsSync(path.join(root, 'assets/fonts/instrumentserif-OFL.txt')));
});
test('Ids are unique and every drawing reference points at a definition on the same page', () => {
  for (const file of pages) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(match => match[1]);
    const repeated = ids.filter((id, index) => ids.indexOf(id) !== index);
    assert.deepEqual([...new Set(repeated)], [], file + ': repeated ids');
    const refs = [...html.matchAll(/url\(#([^)]+)\)|\b(?:href|xlink:href)="#([^"]+)"|\b(?:aria-controls|aria-labelledby|aria-describedby|for)="([^"]+)"/g)];
    for (const id of refs.flatMap(match => (match[1] || match[2] || match[3]).split(' '))) {
      assert.ok(ids.includes(id), file + ': nothing has id "' + id + '"');
    }
  }
});
test('Markup never ships an element hidden until a script reveals it', () => {
  for (const file of pages) {
    const html = fs.readFileSync(path.join(root, file), 'utf8');
    assert.ok(!/class="[^"]*\bin-view\b/.test(html), file + ': in-view belongs to the script');
  }
});
test('The sitemap lists every public page and no redirect', () => {
  const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
  for (const page of ['', 'fr.html', 'contact.html', 'resources.html', 'privacy.html']) assert.ok(sitemap.includes('https://honeybees.consulting/' + page + '</loc>'), 'sitemap: ' + page);
  for (const page of ['services.html']) {
    assert.ok(!sitemap.includes(page), 'sitemap lists ' + page);
    assert.match(fs.readFileSync(path.join(root, page), 'utf8'), /name="robots" content="noindex/, page + ' should be noindex');
  }
});
test('The V1 archive is gone and nothing links to it', () => {
  assert.ok(!fs.existsSync(path.join(root, 'v1.html')));
  for (const file of pages) assert.ok(!fs.readFileSync(path.join(root, file), 'utf8').includes('v1.html'), file + ' links to v1.html');
});
