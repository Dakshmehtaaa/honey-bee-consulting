(function () {
  'use strict';
  const root = document.documentElement;
  const french = window.HONEY_FRENCH || {};
  const english = {};
  const englishAttributes = {};
  const ATTRS = [['data-i18n-aria', 'aria-label'], ['data-i18n-alt', 'alt'], ['data-i18n-placeholder', 'placeholder']];
  const store = {
    get(area, key) { try { return window[area].getItem(key); } catch (_) { return null; } },
    set(area, key, value) { try { window[area].setItem(key, value); } catch (_) { /* Preferences are optional. */ } }
  };
  const ui = {
    en: {
      emailDraft: 'Your email app should open with a draft. Nothing is sent until you press send.',
      letterBad: 'Please check your email address.',
      letterBusy: 'Adding you…',
      letterDone: 'You’re on the list. Thank you!',
      letterMail: 'Your email app should open with a short sign-up email. Press send and you’re on the list.',
      letterFail: 'That didn’t go through. Please try again, or write to dakshmehta077@gmail.com.'
    },
    fr: {
      emailDraft: 'Votre messagerie devrait s’ouvrir avec un brouillon. Rien n’est envoyé tant que vous n’appuyez pas sur Envoyer.',
      letterBad: 'Vérifiez votre adresse e-mail.',
      letterBusy: 'Inscription en cours…',
      letterDone: 'Vous êtes inscrit·e. Merci !',
      letterMail: 'Votre messagerie devrait s’ouvrir avec un court e-mail d’inscription. Envoyez-le et c’est fait.',
      letterFail: 'L’inscription n’a pas abouti. Réessayez, ou écrivez à dakshmehta077@gmail.com.'
    }
  };

  /* ---------- language ---------- */
  document.querySelectorAll('[data-i18n]').forEach(el => { english[el.dataset.i18n] = window.HONEY_ENGLISH?.[el.dataset.i18n] ?? el.textContent; });
  ATTRS.forEach(([key, attr]) => document.querySelectorAll('[' + key + ']').forEach(el => { englishAttributes[el.getAttribute(key)] = el.getAttribute(attr); }));
  const description = document.querySelector('meta[name="description"]');
  const titleKey = document.body.dataset.titleKey;
  const meta = {
    en: { title: document.title, description: description && description.content },
    fr: titleKey ? { title: french[titleKey] } : { title: french['story.meta.title'], description: french['story.meta.description'] }
  };
  let language = 'en';
  function setLanguage(next) {
    language = next === 'fr' ? 'fr' : 'en';
    root.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const text = language === 'fr' ? french[el.dataset.i18n] : english[el.dataset.i18n];
      if (text) el.textContent = text;
    });
    ATTRS.forEach(([key, attr]) => document.querySelectorAll('[' + key + ']').forEach(el => {
      const id = el.getAttribute(key);
      const value = language === 'fr' ? french[id] : englishAttributes[id];
      if (value) el.setAttribute(attr, value);
    }));
    document.querySelectorAll('[data-lang]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.lang === language)));
    if (meta[language].title) document.title = meta[language].title;
    if (description && meta[language].description) description.content = meta[language].description;
    // Every other page reads ?lang=, so the choice follows the visitor there.
    document.querySelectorAll('[data-lang-link]').forEach(a => {
      const [path, hash] = a.getAttribute('href').split('#');
      const [file, query] = path.split('?');
      const params = new URLSearchParams(query || '');
      params.set('lang', language);
      a.setAttribute('href', file + '?' + params + (hash ? '#' + hash : ''));
    });
    store.set('localStorage', 'honeybee-language', language);
  }
  document.querySelectorAll('[data-lang]').forEach(b => b.addEventListener('click', () => setLanguage(b.dataset.lang)));
  const requested = new URLSearchParams(location.search).get('lang') || (location.pathname.endsWith('/fr.html') ? 'fr' : null) || store.get('localStorage', 'honeybee-language');
  setLanguage(requested || 'en');

  /* ---------- loader ---------- */
  const loader = document.getElementById('loader');
  if (loader && root.dataset.loader === 'play') {
    const done = () => { root.classList.add('loaded'); store.set('sessionStorage', 'honeybee-loaded', '1'); };
    const timer = setTimeout(done, 1700);
    loader.addEventListener('click', () => { clearTimeout(timer); done(); });
  }

  /* ---------- header: shadow and the small-screen menu ---------- */
  const top = document.querySelector('.top');
  const onScrollHeader = () => top.classList.toggle('is-scrolled', scrollY > 8);
  addEventListener('scroll', onScrollHeader, { passive: true });
  onScrollHeader();
  const menu = document.getElementById('menu-button');
  const setMenu = open => { top.classList.toggle('is-open', open); menu.setAttribute('aria-expanded', String(open)); };
  if (menu) {
    menu.addEventListener('click', () => setMenu(!top.classList.contains('is-open')));
    document.querySelectorAll('#top-nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape' && top.classList.contains('is-open')) { setMenu(false); menu.focus(); } });
  }

  /* ---------- chapters reveal once ---------- */
  const chapters = [...document.querySelectorAll('.chapter')];
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
    }), { threshold: 0.2, rootMargin: '0px 0px -10% 0px' });
    chapters.forEach(c => io.observe(c));
  } else chapters.forEach(c => c.classList.add('in-view'));
  // The hero waits for the loader so its blooms are seen.
  const hero = document.querySelector('.hero');
  if (hero) requestAnimationFrame(() => requestAnimationFrame(() => hero.classList.add('in-view')));

  /* ---------- the guide bee ---------- */
  const guide = document.getElementById('guide');
  const perches = [...document.querySelectorAll('[data-perch]')];
  const pos = { x: -200, y: -200, r: 0, f: 1 };
  let stops = [], raf = 0, placed = false, lastMove = 0;

  // For each perch, the scroll position at which the bee should sit on it:
  // when its chapter is centred in the viewport (clamped to the page's scroll range).
  function measure() {
    const max = document.documentElement.scrollHeight - innerHeight;
    stops = perches.map((p, i) => {
      const c = p.closest('.chapter') || p.closest('section');
      const r = c.getBoundingClientRect();
      const centre = scrollY + r.top + r.height / 2 - innerHeight / 2;
      return i === 0 ? 0 : Math.max(0, Math.min(max, centre));
    });
  }
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  function target() {
    const y = scrollY;
    let i = 0;
    while (i < stops.length - 2 && y >= stops[i + 1]) i++;
    const span = stops[i + 1] - stops[i];
    const t = span > 0 ? Math.min(1, Math.max(0, (y - stops[i]) / span)) : 1;
    const a = perches[i].getBoundingClientRect(), b = perches[i + 1].getBoundingClientRect();
    const e = ease(t);
    const lift = Math.sin(Math.PI * e) * Math.min(140, innerHeight * .18);
    const sway = Math.sin(Math.PI * 2 * e) * Math.min(60, innerWidth * .06);
    return { x: a.left + (b.left - a.left) * e + sway, y: a.top + (b.top - a.top) * e - lift };
  }
  function frame(now) {
    raf = 0;
    if (!root.classList.contains('motion')) return;
    const t = target();
    if (!placed) { pos.x = t.x; pos.y = t.y; placed = true; }
    const dx = t.x - pos.x, dy = t.y - pos.y;
    pos.x += dx * .14; pos.y += dy * .14;
    const speed = Math.hypot(dx, dy);
    if (dx < -2) pos.f = -1; else if (dx > 2) pos.f = 1;
    pos.r += (Math.max(-28, Math.min(28, dy * .5)) - pos.r) * .2;
    const size = guide.offsetWidth;
    guide.style.transform = `translate3d(${pos.x - size * .5}px,${pos.y - size * .62}px,0) scaleX(${pos.f}) rotate(${pos.r}deg)`;
    guide.classList.toggle('is-flying', speed > 3);
    if (speed > .4 || now - lastMove < 400) raf = requestAnimationFrame(frame);
  }
  const kick = () => { lastMove = performance.now(); if (!raf) raf = requestAnimationFrame(frame); };
  const flies = guide && perches.length > 1;
  if (flies) {
    addEventListener('scroll', kick, { passive: true });
    addEventListener('resize', () => { measure(); kick(); });
    if ('ResizeObserver' in window) new ResizeObserver(() => { measure(); kick(); }).observe(document.body);
    measure(); kick();
  }

  /* ---------- the Guide picks up its goggles once you start scrolling ---------- */
  const groundGoggles = document.querySelector('.hero-goggles');
  const onScrollGoggles = () => {
    const on = scrollY > 40;
    if (guide) guide.classList.toggle('has-goggles', on);
    if (groundGoggles) groundGoggles.classList.toggle('taken', on && root.classList.contains('motion'));
  };
  if (groundGoggles) { addEventListener('scroll', onScrollGoggles, { passive: true }); onScrollGoggles(); }

  /* ---------- the loop: Environment → People → Proof → Clients ---------- */
  const loop = document.querySelector('[data-loop]');
  let loopRestart = null;
  if (loop) {
    const ring = loop.querySelector('.loop-ring');
    const nodes = [...loop.querySelectorAll('.loop-node')];
    const panels = [...loop.querySelectorAll('.loop-panel')];
    let index = 0, angle = 0, timer = 0, seen = false, held = false;
    // The bee only ever flies forward round the ring, however far it has to go.
    const select = i => {
      angle += ((i - index + nodes.length) % nodes.length) * (360 / nodes.length);
      index = i;
      ring.style.setProperty('--angle', angle + 'deg');
      ring.style.setProperty('--flip', i >= nodes.length / 2 ? -1 : 1);
      nodes.forEach((n, k) => { n.classList.toggle('is-active', k === i); n.setAttribute('aria-pressed', String(k === i)); });
      panels.forEach((p, k) => p.classList.toggle('is-active', k === i));
    };
    const schedule = () => {
      clearTimeout(timer);
      if (seen && !held && root.classList.contains('motion')) timer = setTimeout(() => { select((index + 1) % nodes.length); schedule(); }, 4200);
    };
    loopRestart = schedule;
    nodes.forEach((n, k) => n.addEventListener('click', () => { select(k); schedule(); }));
    const hold = on => () => { held = on; schedule(); };
    loop.addEventListener('pointerenter', hold(true));
    loop.addEventListener('pointerleave', hold(false));
    loop.addEventListener('focusin', hold(true));
    loop.addEventListener('focusout', e => { if (!loop.contains(e.relatedTarget)) hold(false)(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => { seen = e.isIntersecting; schedule(); }, { threshold: .35 }).observe(loop);
    }
  }

  /* ---------- the messenger looks at you ---------- */
  const messenger = document.querySelector('.messenger-svg');
  const pupils = messenger && messenger.querySelector('.pupils');
  if (pupils && matchMedia('(pointer: fine)').matches) {
    addEventListener('pointermove', e => {
      if (!root.classList.contains('motion')) return;
      const r = messenger.getBoundingClientRect();
      const vx = e.clientX - (r.left + r.width / 2), vy = e.clientY - (r.top + r.height * .4);
      const d = Math.hypot(vx, vy) || 1, k = Math.min(1, d / 300) * 3;
      pupils.setAttribute('transform', `translate(${(vx / d * k).toFixed(2)} ${(vy / d * k - 2).toFixed(2)})`);
    }, { passive: true });
  }

  /* ---------- calm mode switch ---------- */
  const sw = document.getElementById('motion-switch');
  function applyMotion(calm) {
    root.classList.toggle('calm', calm);
    root.classList.toggle('motion', !calm);
    sw.setAttribute('aria-pressed', String(calm));
    if (calm) { if (guide) guide.style.transform = ''; if (pupils) pupils.removeAttribute('transform'); }
    else {
      chapters.forEach(c => { if (c.getBoundingClientRect().top < innerHeight) c.classList.add('in-view'); });
      if (flies) { placed = false; measure(); kick(); }
    }
    onScrollGoggles();
    if (loopRestart) loopRestart();
  }
  if (sw) {
    sw.addEventListener('click', () => {
      const calm = !root.classList.contains('calm');
      store.set('localStorage', 'honeybee-motion', calm ? 'calm' : 'full');
      applyMotion(calm);
    });
    sw.setAttribute('aria-pressed', String(root.classList.contains('calm')));
  }

  /* ---------- resources: filter by stage ---------- */
  const filter = document.querySelector('.res-filter');
  if (filter) filter.addEventListener('click', e => {
    const button = e.target.closest('button[data-filter]');
    if (!button) return;
    const stage = button.dataset.filter;
    filter.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    document.querySelectorAll('.res-card').forEach(card => { card.hidden = stage !== 'all' && card.dataset.stage !== stage; });
  });

  /* ---------- how we help: the card row scrolls sideways when it doesn't fit ---------- */
  const track = document.getElementById('crew-track');
  if (track) {
    const prev = document.querySelector('.rail-prev'), next = document.querySelector('.rail-next');
    const ends = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max;
    };
    const go = dir => track.scrollBy({ left: dir * track.clientWidth * .8, behavior: root.classList.contains('calm') ? 'auto' : 'smooth' });
    prev.addEventListener('click', () => go(-1));
    next.addEventListener('click', () => go(1));
    track.addEventListener('scroll', ends, { passive: true });
    addEventListener('resize', ends);
    ends();
  }

  /* ---------- contact page: a service card can pick the subject ---------- */
  const needSelect = document.getElementById('contact-need');
  const wanted = new URLSearchParams(location.search).get('need');
  if (needSelect && wanted && [...needSelect.options].some(o => o.value === wanted)) needSelect.value = wanted;

  /* ---------- contact page: prepare an email draft ---------- */
  const contact = document.getElementById('contact-form');
  if (contact && window.HoneyBusiness) {
    contact.addEventListener('submit', event => {
      event.preventDefault();
      if (!contact.reportValidity()) return;
      const need = document.getElementById('contact-need');
      location.href = window.HoneyBusiness.enquiryLink({
        name: document.getElementById('contact-name').value,
        company: document.getElementById('contact-company').value,
        need: need.options[need.selectedIndex].textContent,
        message: document.getElementById('contact-message').value,
        language
      });
      document.getElementById('contact-status').textContent = ui[language].emailDraft;
    });
    contact.querySelector('button[type="submit"]').disabled = false;
  }

  /* ---------- newsletter ---------- */
  const letter = document.getElementById('letter-form');
  if (letter && window.HoneyBusiness) {
    const input = letter.querySelector('input[type="email"]');
    const button = letter.querySelector('button[type="submit"]');
    const status = document.getElementById('letter-status');
    const say = (text, error) => { status.textContent = text; status.classList.toggle('is-error', !!error); };
    letter.addEventListener('submit', async event => {
      event.preventDefault();
      if (letter.elements.website.value) { say(ui[language].letterDone); return; }
      let request;
      try { request = window.HoneyBusiness.subscription({ email: input.value, language, page: location.pathname }); }
      catch (_) { input.setAttribute('aria-invalid', 'true'); say(ui[language].letterBad, true); input.focus(); return; }
      input.removeAttribute('aria-invalid');
      if (request.method === 'mailto') { location.href = request.url; say(ui[language].letterMail); return; }
      button.disabled = true;
      say(ui[language].letterBusy);
      try {
        // Apps Script answers from another origin; a no-cors post is delivered all the same.
        await fetch(request.url, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: request.body });
        letter.reset();
        say(ui[language].letterDone);
      } catch (_) {
        say(ui[language].letterFail, true);
      } finally {
        button.disabled = false;
      }
    });
    input.addEventListener('input', () => input.removeAttribute('aria-invalid'));
  }
})();
