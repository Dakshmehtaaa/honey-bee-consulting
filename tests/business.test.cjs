const test = require('node:test');
const assert = require('node:assert/strict');
const { estimateSavings, enquiryLink, validEmail, subscription } = require('../dist/assets/business-core.js');
const example = { annualSpend: 50000, reductionRate: 8, implementationCost: 6000, recurringCost: 0 };
test('Example produces €4,000 annual savings and 18-month simple payback', () => {
  assert.deepEqual(estimateSavings(example), { grossSavings: 4000, netSavings: 4000, paybackMonths: 18 });
});
test('Recurring costs reduce the benefit and extend payback', () => {
  assert.deepEqual(estimateSavings({ ...example, recurringCost: 1000 }), { grossSavings: 4000, netSavings: 3000, paybackMonths: 24 });
});
test('Zero and negative net savings never produce misleading payback', () => {
  assert.equal(estimateSavings({ ...example, recurringCost: 4000 }).paybackMonths, null);
  const loss = estimateSavings({ ...example, recurringCost: 5000 });
  assert.equal(loss.netSavings, -1000);
  assert.equal(loss.paybackMonths, null);
});
test('No implementation cost is handled without division by zero', () => {
  assert.equal(estimateSavings({ ...example, implementationCost: 0 }).paybackMonths, 0);
  assert.equal(estimateSavings({ ...example, implementationCost: 0, annualSpend: 0 }).paybackMonths, 0);
});
test('Fractional rates retain their actual calculated benefit', () => {
  assert.equal(estimateSavings({ ...example, annualSpend: 12345, reductionRate: 2.5 }).netSavings, 308.625);
});
test('Invalid, negative and impossible percentage inputs are rejected', () => {
  for (const changes of [{ reductionRate: 101 }, { reductionRate: -1 }, { annualSpend: NaN }, { recurringCost: Infinity }, { implementationCost: -1 }, { annualSpend: '50000' }, { annualSpend: 1e9 + 1 }]) {
    assert.throws(() => estimateSavings({ ...example, ...changes }), RangeError);
  }
});
test('Zero spend and zero saving rate give zero benefit', () => {
  assert.equal(estimateSavings({ ...example, annualSpend: 0 }).netSavings, 0);
  assert.equal(estimateSavings({ ...example, reductionRate: 0 }).netSavings, 0);
});
test('Email drafts preserve accents, line breaks and literal unsafe query characters', () => {
  const href = enquiryLink({ name: 'Élodie', company: 'A&B #Paris', need: 'RSE', message: 'Budget ?\nEncore & plus', language: 'fr' });
  assert.ok(href.startsWith('mailto:daksh.mehta@honeybees.consulting?subject='));
  const query = new URLSearchParams(href.split('?')[1]);
  assert.equal(query.get('subject'), 'honeybees.consulting — échange avec A&B #Paris');
  assert.ok(query.get('body').includes('Budget ?\nEncore & plus'));
  assert.ok(query.get('body').includes('Bonjour Daksh'));
  assert.equal([...query.keys()].length, 2);
});
test('Newsletter emails are checked before anything is sent', () => {
  for (const good of ['a@b.co', 'first.last+esg@company.fr', 'élodie@entreprise.fr']) assert.equal(validEmail(good), true, good);
  for (const bad of ['', 'a@b', 'a b@c.com', '<a@b.co>', '=cmd@x.com', '+a@b.co', '@b.co', 'a@b.co,c@d.co', 'x'.repeat(250) + '@b.co', null]) assert.equal(validEmail(bad), false, String(bad));
  assert.throws(() => subscription({ email: 'nope', language: 'en', page: '/' }), RangeError);
});
test('Newsletter sign-ups post form fields to the sheet once it is configured', () => {
  const request = subscription({ email: ' a@b.co ', language: 'fr', page: '/contact.html', endpoint: 'https://script.google.com/macros/s/x/exec' });
  assert.equal(request.method, 'post');
  assert.equal(request.url, 'https://script.google.com/macros/s/x/exec');
  assert.deepEqual(Object.fromEntries(new URLSearchParams(request.body)), { email: 'a@b.co', lang: 'fr', page: '/contact.html' });
});
test('Without a sheet address, sign-ups fall back to a ready-made email', () => {
  const request = subscription({ email: 'a@b.co', language: 'en', page: '/', endpoint: '' });
  assert.equal(request.method, 'mailto');
  assert.ok(request.url.startsWith('mailto:daksh.mehta@honeybees.consulting?subject='));
  assert.ok(new URLSearchParams(request.url.split('?')[1]).get('body').includes('a@b.co'));
});
