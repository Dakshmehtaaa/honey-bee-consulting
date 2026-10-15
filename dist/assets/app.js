(function () {
  'use strict';
  const french = window.HONEY_FRENCH || {};
  const english = {};
  const originalAttributes = {};
  const ui = {
    en: {
      title: 'Services & details · honeybees.consulting',
      description: 'Practical CSR and ESG consulting by Daksh Mehta. Build your foundations, strengthen buyer confidence, and turn sustainability plans into useful work. Paris. English and French.',
      openMenu: 'Open menu', closeMenu: 'Close menu', home: 'honeybees.consulting, home',
      pauseMotion: 'Pause image motion', resumeMotion: 'Resume image motion',
      month: 'months', noCost: 'No upfront cost', noPayback: 'No payback', invalid: 'Complete all inputs with valid, non-negative values. The saving rate must be between 0 and 100%.',
      noPaybackDetail: 'Net annual savings are zero or negative: there is no simple payback under these assumptions.',
      noCostDetail: 'There is no one-off implementation cost in this scenario.',
      savings: 'per year', minus: '−',
      emailStatus: 'Your email app should open a draft. Nothing has been sent by this site. If it does not open, use the email address alongside the form.',
      csv: 'assets/evidence-register-en.csv'
    },
    fr: {
      title: french['metadata.title'] || 'honeybees.consulting — Une RSE utile à votre entreprise',
      description: french['metadata.description'] || 'Conseil pratique en RSE et ESG par Daksh Mehta. Des fondations solides, des preuves crédibles et des projets qui avancent. Paris. Français et anglais.',
      openMenu: 'Ouvrir le menu', closeMenu: 'Fermer le menu', home: 'honeybees.consulting, accueil',
      pauseMotion: 'Mettre l’image en pause', resumeMotion: 'Animer l’image',
      month: 'mois', noCost: 'Sans coût initial', noPayback: 'Pas de retour', invalid: 'Renseignez tous les champs avec des valeurs valides et positives ou nulles. Le taux d’économie doit être compris entre 0 et 100 %.',
      noPaybackDetail: 'Les économies annuelles nettes sont nulles ou négatives : aucun délai de retour simple ne peut être calculé avec ces hypothèses.',
      noCostDetail: 'Ce scénario ne prévoit aucun coût initial de mise en œuvre.',
      savings: 'par an', minus: '−',
      emailStatus: 'Votre application de messagerie devrait ouvrir un brouillon. Le site n’a rien envoyé. Si elle ne s’ouvre pas, utilisez l’adresse indiquée à côté du formulaire.',
      csv: 'assets/evidence-register-fr.csv'
    }
  };
  const priorities = {
    en: {
      buyers: { title: 'Build a buyer-ready evidence pack.', steps: ['Gather your latest customer questionnaire.', 'Map each answer to a policy, action or record.', 'Give the gaps an owner and a realistic next step.'], deliverable: 'Useful output: one answer library, with evidence your team can reuse.', need: 'evidence' },
      starting: { title: 'Choose a few actions worth doing first.', steps: ['List your main customer, operational and people priorities.', 'Review what is already in place and what is missing.', 'Choose three actions with owners, measures and review dates.'], deliverable: 'Useful output: a short CSR roadmap your team can put to work.', need: 'foundations' },
      data: { title: 'Give your ESG data a clear home.', steps: ['List the indicators you need and why you need them.', 'Assign a data owner and source for each indicator.', 'Set up a shared collection and review workflow.'], deliverable: 'Useful output: a traceable KPI register and collection calendar.', need: 'reporting' }
    },
    fr: {
      buyers: { title: 'Préparez des preuves utilisables par vos clients.', steps: ['Rassemblez votre dernier questionnaire client.', 'Reliez chaque réponse à une politique, une action ou un justificatif.', 'Attribuez un responsable et une prochaine étape réaliste à chaque manque.'], deliverable: 'Livrable utile : une bibliothèque de réponses et de preuves réutilisables par votre équipe.', need: 'evidence' },
      starting: { title: 'Choisissez quelques actions utiles pour commencer.', steps: ['Listez vos principales priorités commerciales, opérationnelles et humaines.', 'Faites le point sur ce qui existe et ce qui manque.', 'Choisissez trois actions avec responsables, indicateurs et dates de suivi.'], deliverable: 'Livrable utile : une feuille de route RSE courte, que votre équipe peut mettre en œuvre.', need: 'foundations' },
      data: { title: 'Donnez un cadre clair à vos données ESG.', steps: ['Listez les indicateurs nécessaires et leur utilité.', 'Attribuez un responsable et une source à chaque indicateur.', 'Organisez un circuit commun de collecte et de vérification.'], deliverable: 'Livrable utile : un registre d’indicateurs traçables et un calendrier de collecte.', need: 'reporting' }
    }
  };
  let language = 'en';
  let selectedPriority = 'buyers';
  let emailPrepared = false;
  let motionPaused = false;
  const hero = document.querySelector('.hero-full');
  const motionButton = document.getElementById('motion-toggle');
  function updateMotion() {
    if (!hero || !motionButton) return;
    hero.classList.toggle('motion-paused', motionPaused);
    motionButton.setAttribute('aria-pressed', String(motionPaused));
    document.getElementById('motion-label').textContent = motionPaused ? ui[language].resumeMotion : ui[language].pauseMotion;
    motionButton.querySelector('.motion-icon').textContent = motionPaused ? '▷' : 'Ⅱ';
  }
  if (motionButton) motionButton.addEventListener('click', () => { motionPaused = !motionPaused; updateMotion(); });
  if (hero && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      hero.classList.toggle('motion-inactive', !entries[0].isIntersecting || document.hidden);
    });
    observer.observe(hero);
    document.addEventListener('visibilitychange', () => {
      const visible = hero.getBoundingClientRect().bottom > 0;
      hero.classList.toggle('motion-inactive', document.hidden || !visible);
    });
  }
  document.querySelectorAll('[data-i18n]').forEach(element => { english[element.dataset.i18n] = window.HONEY_ENGLISH?.[element.dataset.i18n] ?? element.textContent; });
  const attributeTypes = [['data-i18n-aria', 'aria-label'], ['data-i18n-alt', 'alt'], ['data-i18n-placeholder', 'placeholder']];
  attributeTypes.forEach(([key, attribute]) => {
    document.querySelectorAll('[' + key + ']').forEach(element => { originalAttributes[element.getAttribute(key)] = window.HONEY_EN_ATTRIBUTES?.[element.getAttribute(key)] ?? element.getAttribute(attribute); });
  });
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  function closeMenu() {
    if (!menu || !nav) return;
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', ui[language].openMenu);
    nav.classList.remove('is-open');
  }
  function updatePriority() {
    const result = priorities[language][selectedPriority];
    const title = document.getElementById('priority-title');
    if (!title) return;
    title.textContent = result.title;
    const steps = document.getElementById('priority-steps');
    steps.replaceChildren(...result.steps.map(text => { const item = document.createElement('li'); item.textContent = text; return item; }));
    document.getElementById('priority-deliverable').textContent = result.deliverable;
    document.getElementById('priority-contact').dataset.enquiry = result.need;
    document.querySelectorAll('[data-priority]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.priority === selectedPriority)));
  }
  const calculator = document.getElementById('business-form');
  function updateCalculator() {
    if (!calculator) return;
    const locale = language === 'fr' ? 'fr-FR' : 'en-IE';
    const money = { format(value) {
      const amount = new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR', minimumFractionDigits: Number.isInteger(value) ? 0 : 2, maximumFractionDigits: 2 });
      if (value !== 0 && Math.abs(value) < .01) return (value < 0 ? '− ' : '') + '< ' + new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(.01);
      return amount.format(value);
    } };
    const number = new Intl.NumberFormat(language === 'fr' ? 'fr-FR' : 'en-GB', { maximumFractionDigits: 1 });
    const fields = ['annual-spend', 'reduction-rate', 'implementation-cost', 'recurring-cost'].map(id => document.getElementById(id));
    const output = document.getElementById('net-savings');
    const payback = document.getElementById('payback');
    const explanation = document.getElementById('calc-explanation');
    if (!calculator.checkValidity() || fields.some(field => !Number.isFinite(field.valueAsNumber))) {
      output.textContent = '—'; payback.textContent = '—'; explanation.textContent = ui[language].invalid;
      return;
    }
    const [annualSpend, reductionRate, implementationCost, recurringCost] = fields.map(field => field.valueAsNumber);
    const result = window.HoneyBusiness.estimateSavings({ annualSpend, reductionRate, implementationCost, recurringCost });
    output.textContent = money.format(result.netSavings);
    payback.textContent = implementationCost === 0 ? ui[language].noCost : result.paybackMonths === null ? ui[language].noPayback : number.format(result.paybackMonths) + ' ' + ui[language].month;
    let detail = `${money.format(annualSpend)} × ${number.format(reductionRate)}% − ${money.format(recurringCost)} ≈ ${money.format(result.netSavings)} ${ui[language].savings}. `;
    if (implementationCost === 0) detail += ui[language].noCostDetail;
    else if (result.paybackMonths === null) detail += ui[language].noPaybackDetail;
    else detail += `${money.format(implementationCost)} ÷ ${money.format(result.netSavings)} × 12 ≈ ${number.format(result.paybackMonths)} ${ui[language].month}.`;
    explanation.textContent = detail;
  }
  function setLanguage(next) {
    language = next === 'fr' ? 'fr' : 'en';
    document.documentElement.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.dataset.i18n;
      const text = language === 'fr' ? french[key] : english[key];
      if (typeof text === 'string') element.textContent = text;
    });
    attributeTypes.forEach(([key, attribute]) => {
      document.querySelectorAll('[' + key + ']').forEach(element => {
        const label = element.getAttribute(key);
        const value = language === 'fr' ? french[label] : originalAttributes[label];
        if (typeof value === 'string') element.setAttribute(attribute, value);
      });
    });
    document.querySelectorAll('[data-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === language)));
    document.querySelectorAll('.brand[href="#top"]').forEach(brand => brand.setAttribute('aria-label', ui[language].home));
    if (document.body.dataset.page !== 'privacy') {
      document.title = ui[language].title;
      document.querySelector('meta[name="description"]').content = ui[language].description;
      document.querySelector('meta[property="og:title"]').content = ui[language].title;
      document.querySelector('meta[property="og:description"]').content = ui[language].description;
    } else {
      document.title = language === 'fr' ? 'Informations du site et confidentialité — honeybees.consulting' : 'Site information & privacy — honeybees.consulting';
      document.querySelector('meta[name="description"]').content = language === 'fr' ? 'Éditeur, contact, traitement des données et informations sur les images du site honeybees.consulting.' : 'Publisher, contact, data handling and image information for honeybees.consulting.';
    }
    const download = document.getElementById('template-download');
    if (download) download.href = ui[language].csv;
    const privacy = document.querySelector('a[href^="privacy.html"]');
    if (privacy) privacy.href = 'privacy.html?lang=' + language;
    document.querySelectorAll('[data-home-link]').forEach(link => link.href = 'index.html?lang=' + language);
    if (menu) menu.setAttribute('aria-label', menu.getAttribute('aria-expanded') === 'true' ? ui[language].closeMenu : ui[language].openMenu);
    if (emailPrepared) document.getElementById('contact-status').textContent = ui[language].emailStatus;
    updatePriority(); updateCalculator(); updateMotion();
    document.dispatchEvent(new CustomEvent('honey:language', { detail: language }));
    try { localStorage.setItem('honeybee-language', language); } catch (_) { /* Preferences are optional. */ }
  }
  document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.lang)));
  document.querySelectorAll('[data-priority]').forEach(button => button.addEventListener('click', () => { selectedPriority = button.dataset.priority; updatePriority(); }));
  document.querySelectorAll('[data-enquiry]').forEach(link => link.addEventListener('click', () => {
    const select = document.getElementById('contact-need');
    if (select) select.value = link.dataset.enquiry;
  }));
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-label', open ? ui[language].closeMenu : ui[language].openMenu);
      nav.classList.toggle('is-open', open);
      if (open) nav.querySelector('a').focus();
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });
    window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
  }
  if (calculator) {
    let timer;
    calculator.addEventListener('input', () => { window.clearTimeout(timer); timer = window.setTimeout(updateCalculator, 150); });
    calculator.addEventListener('submit', event => { event.preventDefault(); updateCalculator(); });
  }
  const contact = document.getElementById('contact-form');
  if (contact) contact.addEventListener('submit', event => {
    event.preventDefault();
    if (!contact.reportValidity()) return;
    const select = document.getElementById('contact-need');
    const href = window.HoneyBusiness.enquiryLink({
      name: document.getElementById('contact-name').value,
      company: document.getElementById('contact-company').value,
      need: select.selectedOptions[0].textContent,
      message: document.getElementById('contact-message').value,
      language
    });
    emailPrepared = true;
    document.getElementById('contact-status').textContent = ui[language].emailStatus;
    window.location.href = href;
  });
  let requested;
  const frenchRoute = window.location.pathname.endsWith('/fr.html') ? 'fr' : null;
  try { requested = new URLSearchParams(window.location.search).get('lang') || frenchRoute || localStorage.getItem('honeybee-language'); } catch (_) { requested = new URLSearchParams(window.location.search).get('lang') || frenchRoute; }
  setLanguage(requested || 'en');
  if (contact && window.HoneyBusiness) contact.querySelector('button[type="submit"]').disabled = false;
})();
