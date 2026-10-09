const test = require('node:test');
const assert = require('node:assert/strict');
const { estimateSavings, enquiryLink } = require('../dist/assets/business-core.js');
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
  assert.ok(href.startsWith('mailto:Dakshmehta077@gmail.com?subject='));
  const query = new URLSearchParams(href.split('?')[1]);
  assert.equal(query.get('subject'), 'Honey Bee Consulting — échange avec A&B #Paris');
  assert.ok(query.get('body').includes('Budget ?\nEncore & plus'));
  assert.ok(query.get('body').includes('Bonjour Daksh'));
  assert.equal([...query.keys()].length, 2);
});
