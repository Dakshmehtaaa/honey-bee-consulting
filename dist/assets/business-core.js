(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.HoneyBusiness = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  function estimateSavings({ annualSpend, reductionRate, implementationCost, recurringCost }) {
    const values = [annualSpend, reductionRate, implementationCost, recurringCost];
    if (values.some(value => typeof value !== 'number' || !Number.isFinite(value) || value < 0)) {
      throw new RangeError('All inputs must be finite, non-negative numbers.');
    }
    if (reductionRate > 100 || annualSpend > 1e9 || implementationCost > 1e9 || recurringCost > 1e9) {
      throw new RangeError('Inputs exceed the planning limits.');
    }
    const grossSavings = annualSpend * reductionRate / 100;
    const netSavings = grossSavings - recurringCost;
    const paybackMonths = implementationCost === 0 ? 0 : netSavings > 0 ? implementationCost / netSavings * 12 : null;
    return { grossSavings, netSavings, paybackMonths };
  }
  function enquiryLink({ name, company, need, message, language }) {
    const fr = language === 'fr';
    const subject = (fr ? 'honeybees.consulting — échange avec ' : 'honeybees.consulting — enquiry from ') + company.trim();
    const body = fr
      ? `Bonjour Daksh,\n\nJe m’appelle ${name.trim()} et je vous contacte pour ${company.trim()}.\n\nNotre besoin : ${need}\n\n${message.trim()}\n\nAu plaisir d’échanger,\n${name.trim()}`
      : `Hi Daksh,\n\nI’m ${name.trim()}, getting in touch from ${company.trim()}.\n\nWe would like help with: ${need}\n\n${message.trim()}\n\nBest,\n${name.trim()}`;
    return 'mailto:Dakshmehta077@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }
  // The newsletter goes to a Google Apps Script web app (backend/newsletter). Until its URL is
  // pasted here, signing up opens an email to Daksh instead, so no address is ever lost.
  const NEWSLETTER_URL = '';
  const EMAIL = /^[^\s@<>()"',;:]+@[^\s@<>()"',;:]+\.[a-z]{2,}$/i;
  function validEmail(value) {
    const email = String(value ?? '').trim();
    return email.length <= 254 && EMAIL.test(email) && !/^[=+\-@]/.test(email);
  }
  function subscription({ email, language, page, endpoint = NEWSLETTER_URL }) {
    const clean = String(email ?? '').trim().toLowerCase();
    if (!validEmail(clean)) throw new RangeError('Invalid email address.');
    const lang = language === 'fr' ? 'fr' : 'en';
    if (endpoint) {
      return { method: 'post', url: endpoint, body: new URLSearchParams({ email: clean, lang, page: String(page ?? '').slice(0, 80) }).toString() };
    }
    const subject = lang === 'fr' ? 'Inscription à la lettre honeybees' : 'Subscribe me to the honeybees letter';
    const body = (lang === 'fr' ? 'Bonjour Daksh,\n\nMerci de m’inscrire à la lettre honeybees : ' : 'Hi Daksh,\n\nPlease add me to the honeybees letter: ') + clean;
    return { method: 'mailto', url: 'mailto:dakshmehta077@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body) };
  }
  return { estimateSavings, enquiryLink, validEmail, subscription, NEWSLETTER_URL };
});
