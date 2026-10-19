"""Fills the shared parts and the illustrations into the site's pages.

Usage: python3 scripts/build-pages.py [--preview DIR]
then:  node scripts/compile-copy.mjs     (French copy + the static fr.html)

Pages stay hand-editable. Only these marked blocks are rewritten:
  <!--part:NAME-->…<!--/part:NAME-->   head-script, header, footer (shared by every new-style page)
  <!--art:NAME-->…<!--/art:NAME-->     drawings from scripts/brand/site_art.py
--preview DIR also writes each drawing as a standalone SVG for review."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand'))
from site_art import PIECES
from pillars import PILLARS, stylesheet as pillar_css

for _name, _make in PILLARS.items():
    PIECES['pillar-' + _name] = (lambda m: lambda: m()[0])(_make)

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dist')
PAGES = ['index.html', 'contact.html', 'resources.html', 'privacy.html']
EMAIL = 'dakshmehta077@gmail.com'
LINKEDIN = 'https://www.linkedin.com/company/146731866/'  # the honeybees.consulting company page


def head_script(page):
    loader = "calm || seen ? 'skip' : 'play'" if page == 'index.html' else "'skip'"
    return f'''<script>
    /* Decide before first paint: full motion or calm{", and whether the short loader plays" if page == 'index.html' else ""}. */
    (function () {{
      var d = document.documentElement, pref = null, seen = null;
      try {{ pref = localStorage.getItem('honeybee-motion'); seen = sessionStorage.getItem('honeybee-loaded'); }} catch (e) {{}}
      var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
      var calm = pref === 'calm' || (pref !== 'full' && reduce);
      d.className += ' js' + (calm ? ' calm' : ' motion');
      d.setAttribute('data-loader', {loader});
    }})();
  </script>'''


def header(page):
    home = page == 'index.html'
    to = (lambda a: a) if home else (lambda a: 'index.html' + a)
    lang = '' if home else ' data-lang-link'
    cur = lambda p: ' aria-current="page"' if page == p else ''
    return f'''<header class="top">
    <div class="top-inner">
      <a class="brand" href="{'#top' if home else 'index.html'}"{lang} aria-label="honeybees.consulting, home" data-i18n-aria="story.brandHome">
        <img src="assets/bee-mark-colour.svg" width="40" height="40" alt="">
        <span class="brand-word">honeybees<span class="brand-sub">CONSULTING</span></span>
      </a>
      <nav class="top-nav" id="top-nav" aria-label="Main navigation" data-i18n-aria="nav.label">
        <a href="{to('#compete')}"{lang} data-i18n="story.nav.why">Why ESG</a>
        <a href="{to('#help')}"{lang} data-i18n="story.nav.help">How we help</a>
        <a href="resources.html" data-lang-link{cur('resources.html')} data-i18n="story.nav.resources">Resources</a>
        <a class="nav-cta" href="contact.html" data-lang-link{cur('contact.html')} data-i18n="story.nav.contact">Contact</a>
      </nav>
      <div class="top-actions">
        <button type="button" class="motion-switch" id="motion-switch" aria-pressed="false"><span class="motion-dot" aria-hidden="true"></span><span data-i18n="story.calm">Calm mode</span></button>
        <div class="language-control" role="group" aria-label="Language / Langue">
          <button type="button" data-lang="en" aria-pressed="true">EN</button><span aria-hidden="true">/</span><button type="button" data-lang="fr" aria-pressed="false">FR</button>
        </div>
        <button type="button" class="menu-button" id="menu-button" aria-expanded="false" aria-controls="top-nav"><span class="sr-only" data-i18n="story.menu">Menu</span><span class="menu-bars" aria-hidden="true"></span></button>
      </div>
    </div>
  </header>'''


def footer(page):
    return f'''<footer class="foot">
    <section class="wrap letter" aria-labelledby="letter-title">
      <div class="letter-copy">
        <h2 id="letter-title" data-i18n="letter.title">The honeybees letter</h2>
        <p data-i18n="letter.body">Short, useful ESG news for companies: new rules, what clients now ask for, what works. Once a month at most.</p>
      </div>
      <form class="letter-form" id="letter-form" novalidate>
        <label class="sr-only" for="letter-email" data-i18n="letter.label">Your work email</label>
        <div class="letter-row">
          <input id="letter-email" name="email" type="email" inputmode="email" autocomplete="email" required maxlength="254" placeholder="you@company.com" data-i18n-placeholder="letter.placeholder">
          <button class="button button-light" type="submit"><span data-i18n="letter.submit">Subscribe</span></button>
        </div>
        <div class="hp" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
        <p class="letter-note"><span data-i18n="letter.note">We only use your email to send the letter. Unsubscribe anytime.</span> <a href="privacy.html#newsletter" data-lang-link data-i18n="letter.privacy">How we handle it</a></p>
        <p class="letter-status" id="letter-status" role="status" aria-live="polite"></p>
      </form>
    </section>
    <div class="wrap foot-inner">
      <img src="assets/honeybees-logo-light.svg" width="300" height="90" alt="honeybees.consulting">
      <p data-i18n="story.footer.tagline">ESG that wins clients.</p>
      <nav class="foot-links" aria-label="Footer" data-i18n-aria="footer.nav">
        <a href="resources.html" data-lang-link data-i18n="story.nav.resources">Resources</a>
        <a href="contact.html" data-lang-link data-i18n="story.nav.contact">Contact</a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn ↗&#xFE0E;</a>
        <a href="privacy.html" data-lang-link data-i18n="footer.privacy">Privacy &amp; site information</a>
      </nav>
    </div>
    <div class="wrap foot-bottom"><span>© 2026 honeybees.consulting · Daksh Mehta</span></div>
  </footer>'''


PARTS = {'head-script': head_script, 'header': header, 'footer': footer}


def fill(html, kind, name, make):
    """make() runs once per block, so a picture used twice gets its own clip-path ids each time."""
    pat = re.compile(r'(<!--' + kind + ':' + re.escape(name) + r'-->).*?(<!--/' + kind + ':' + re.escape(name) + r'-->)', re.S)
    return pat.subn(lambda m: m.group(1) + make() + m.group(2), html)


if __name__ == '__main__':
    if '--preview' in sys.argv:
        art = {k: f() for k, f in PIECES.items()}
        d = sys.argv[sys.argv.index('--preview') + 1]
        os.makedirs(d, exist_ok=True)
        for k, v in art.items():
            if v.startswith('<svg'):
                with open(os.path.join(d, k + '.svg'), 'w') as f:
                    f.write(v.replace('<svg class=', '<svg width="100%" class=', 1).replace('focusable="false">', 'focusable="false">' + art['defs'], 1))
    with open(os.path.join(DIST, 'assets', 'pillars.css'), 'w') as f:
        f.write(pillar_css())
    for page in PAGES:
        p = os.path.join(DIST, page)
        html = open(p).read()
        n = 0
        for name, make in PARTS.items():
            html, k = fill(html, 'part', name, lambda: make(page)); n += k
        for name, make in PIECES.items():
            html, k = fill(html, 'art', name, make); n += k
        left = re.findall(r'<!--(?:part|art):([\w-]+)--><!--/', html)
        if left:
            sys.exit(f'{page}: unknown block(s) {left}')
        open(p, 'w').write(html)
        print(f'{page}: {n} blocks')
