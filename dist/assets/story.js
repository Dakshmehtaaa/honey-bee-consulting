(function () {
  'use strict';
  const root = document.documentElement;
  const french = window.HONEY_FRENCH || {};
  const english = {};
  const englishAttributes = {};
  const ATTRS = [['data-i18n-aria', 'aria-label'], ['data-i18n-alt', 'alt']];
  const store = {
    get(area, key) { try { return window[area].getItem(key); } catch (_) { return null; } },
    set(area, key, value) { try { window[area].setItem(key, value); } catch (_) { /* Preferences are optional. */ } }
  };

  /* ---------- language ---------- */
  document.querySelectorAll('[data-i18n]').forEach(el => { english[el.dataset.i18n] = window.HONEY_ENGLISH?.[el.dataset.i18n] ?? el.textContent; });
  ATTRS.forEach(([key, attr]) => document.querySelectorAll('[' + key + ']').forEach(el => { englishAttributes[el.getAttribute(key)] = el.getAttribute(attr); }));
  const meta = {
    en: { title: document.title, description: document.querySelector('meta[name="description"]').content },
    fr: { title: french['story.meta.title'], description: french['story.meta.description'] }
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
    if (meta[language].description) document.querySelector('meta[name="description"]').content = meta[language].description;
    // The detailed pages read ?lang=, so the choice follows the visitor there.
    document.querySelectorAll('[data-services-link], a[href^="privacy.html"]').forEach(a => {
      const [path, hash] = a.getAttribute('href').split('#');
      a.setAttribute('href', path.split('?')[0] + '?lang=' + language + (hash ? '#' + hash : ''));
    });
    store.set('localStorage', 'honeybee-language', language);
  }
  document.querySelectorAll('[data-lang]').forEach(b => b.addEventListener('click', () => setLanguage(b.dataset.lang)));
  let requested = new URLSearchParams(location.search).get('lang') || (location.pathname.endsWith('/fr.html') ? 'fr' : null) || store.get('localStorage', 'honeybee-language');
  setLanguage(requested || 'en');

  /* ---------- loader ---------- */
  if (root.dataset.loader === 'play') {
    const loader = document.getElementById('loader');
    const done = () => { root.classList.add('loaded'); store.set('sessionStorage', 'honeybee-loaded', '1'); };
    const timer = setTimeout(done, 1700);
    loader.addEventListener('click', () => { clearTimeout(timer); done(); });
  }

  /* ---------- header shadow ---------- */
  const top = document.querySelector('.top');
  const onScrollHeader = () => top.classList.toggle('is-scrolled', scrollY > 8);
  addEventListener('scroll', onScrollHeader, { passive: true });
  onScrollHeader();

  /* ---------- chapters reveal once ---------- */
  const chapters = [...document.querySelectorAll('.chapter')];
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
    }), { threshold: 0.25, rootMargin: '0px 0px -10% 0px' });
    chapters.forEach(c => io.observe(c));
  } else chapters.forEach(c => c.classList.add('in-view'));
  // The hero waits for the loader so its blooms are seen.
  requestAnimationFrame(() => requestAnimationFrame(() => document.getElementById('top').classList.add('in-view')));

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
  addEventListener('scroll', kick, { passive: true });
  addEventListener('resize', () => { measure(); kick(); });
  if ('ResizeObserver' in window) new ResizeObserver(() => { measure(); kick(); }).observe(document.body);
  measure(); kick();

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
    if (calm) { guide.style.transform = ''; if (pupils) pupils.removeAttribute('transform'); }
    else { chapters.forEach(c => { if (c.getBoundingClientRect().top < innerHeight) c.classList.add('in-view'); }); placed = false; measure(); kick(); }
  }
  sw.addEventListener('click', () => {
    const calm = !root.classList.contains('calm');
    store.set('localStorage', 'honeybee-motion', calm ? 'calm' : 'full');
    applyMotion(calm);
  });
  sw.setAttribute('aria-pressed', String(root.classList.contains('calm')));
})();
