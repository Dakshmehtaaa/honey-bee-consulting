const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../dist');
const pages = ['index.html', 'fr.html', 'services.html', 'privacy.html'];
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
