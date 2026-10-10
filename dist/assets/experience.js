(function () {
  'use strict';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  const track = document.getElementById('service-track');
  if (track) {
    const cards = Array.from(track.querySelectorAll('.service-card'));
    const previous = document.getElementById('service-prev');
    const next = document.getElementById('service-next');
    const position = document.getElementById('service-position');
    const phone = window.matchMedia('(max-width: 620px)');
    let current = 0;
    function updateCards() {
      const gap = parseFloat(window.getComputedStyle(track).gap) || 12;
      const stride = cards[0].getBoundingClientRect().width + gap;
      current = phone.matches ? Math.max(0, Math.min(cards.length - 1, Math.round(track.scrollLeft / stride))) : 0;
      previous.disabled = !phone.matches || current === 0;
      next.disabled = !phone.matches || current === cards.length - 1;
      const value = (current + 1) + ' / ' + cards.length;
      if (position.textContent !== value) position.textContent = value;
    }
    function moveCard(direction) {
      const target = Math.max(0, Math.min(cards.length - 1, current + direction));
      const padding = parseFloat(window.getComputedStyle(track).paddingLeft) || 0;
      const left = track.scrollLeft + cards[target].getBoundingClientRect().left - track.getBoundingClientRect().left - padding;
      track.scrollTo({ left, behavior: reduce.matches ? 'auto' : 'smooth' });
    }
    previous.addEventListener('click', () => moveCard(-1));
    next.addEventListener('click', () => moveCard(1));
    track.addEventListener('scroll', updateCards, { passive: true });
    track.addEventListener('keydown', event => {
      if (event.target !== track || !phone.matches || !['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      moveCard(event.key === 'ArrowRight' ? 1 : -1);
    });
    window.addEventListener('resize', updateCards);
    updateCards();
    document.querySelector('.service-navigation').hidden = false;
  }

  const comparison = document.getElementById('esg-comparison');
  if (!comparison) return;
  const actions = Array.from(comparison.querySelectorAll('[data-esg-action]'));
  const features = actions.map(button => button.dataset.esgAction);
  const selected = new Set(features);
  const company = comparison.querySelector('.comparison-you');
  const title = document.getElementById('comparison-your-title');
  const result = document.getElementById('comparison-result');
  const play = document.getElementById('comparison-play');
  const playLabel = document.getElementById('comparison-play-label');
  let timer;
  let playing = false;
  let paused = false;
  let didPlay = false;
  let nextStep = 0;

  function copy(key) {
    const dictionary = document.documentElement.lang === 'fr' ? window.HONEY_FRENCH : window.HONEY_ENGLISH;
    return dictionary?.[key] || comparison.querySelector('[data-i18n="' + key + '"]')?.textContent || key;
  }
  function text(node, value) {
    if (node.textContent !== value) node.textContent = value;
  }
  function render() {
    const ready = selected.size === features.length;
    company.classList.toggle('is-ready', ready);
    actions.forEach(button => button.setAttribute('aria-pressed', String(selected.has(button.dataset.esgAction))));
    company.querySelectorAll('[data-request-item]').forEach(item => {
      const exists = selected.has(item.dataset.requestItem);
      item.classList.toggle('is-ready', exists);
      text(item.querySelector('[data-item-status]'), copy(exists ? 'compare.ready' : 'compare.missing'));
    });
    company.querySelectorAll('[data-window]').forEach(pane => pane.classList.toggle('is-on', selected.has(pane.dataset.window)));
    const state = ready ? 'ready' : selected.size ? 'partial' : 'empty';
    text(title, copy('compare.' + state + 'Title'));
    text(result, copy('compare.' + state + 'Body'));
    text(playLabel, copy(playing ? 'compare.pause' : paused ? 'compare.resume' : didPlay ? 'compare.replay' : 'compare.play'));
    play.setAttribute('aria-pressed', String(playing));
    play.querySelector('[aria-hidden]').textContent = playing ? 'Ⅱ' : '▷';
  }
  function stop() {
    window.clearTimeout(timer);
    playing = false;
    paused = false;
  }
  function pause() {
    window.clearTimeout(timer);
    playing = false;
    paused = true;
    render();
  }
  function advance() {
    if (!playing) return;
    selected.add(features[nextStep++]);
    if (nextStep === features.length) {
      playing = false;
      paused = false;
    } else timer = window.setTimeout(advance, 1050);
    render();
  }
  function begin() {
    stop();
    didPlay = true;
    nextStep = 0;
    if (reduce.matches) {
      features.forEach(feature => selected.add(feature));
      render();
      return;
    }
    selected.clear();
    playing = true;
    render();
    timer = window.setTimeout(advance, 1050);
  }
  actions.forEach(button => {
    button.disabled = false;
    button.addEventListener('click', () => {
      stop();
      const feature = button.dataset.esgAction;
      if (selected.has(feature)) selected.delete(feature);
      else selected.add(feature);
      render();
    });
  });
  play.disabled = false;
  play.addEventListener('click', () => {
    if (playing) pause();
    else if (paused) {
      paused = false;
      playing = true;
      render();
      timer = window.setTimeout(advance, 1050);
    } else begin();
  });
  document.addEventListener('honey:language', render);
  document.addEventListener('visibilitychange', () => { if (document.hidden && playing) pause(); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => { if (!entries[0].isIntersecting && playing) pause(); });
    observer.observe(comparison);
  }
  reduce.addEventListener('change', () => {
    if (!reduce.matches || (!playing && !paused)) return;
    stop();
    features.forEach(feature => selected.add(feature));
    render();
  });
  render();
})();
