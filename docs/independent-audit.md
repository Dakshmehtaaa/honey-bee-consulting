# Honey Bee Consulting — independent audit

**Result: PASS for the reviewed local build. No unresolved findings remain.**

10 October 2026 · Separate GPT-6.1 Sol MAX auditor · Chromium headless · Preview: `http://127.0.0.1:8028/`

The audit inspected the actual HTML, CSS, JavaScript, bilingual copy, images, logo exports, downloads and public-source wording. The current review covers the service-card and buyer-request comparison update below. The earlier full-site and minimal-logo acceptance is retained as a separate baseline, not presented as a newly repeated tools matrix. The coordinator retains final acceptance and publication ownership.

**Current service and comparison delta — 10 October 2026**

The auditor read the final `index.html`, `fr.html`, `assets/experience.js`, `assets/experience.css`, bilingual dictionaries and the change to `assets/app.js`. The service presentation was compared with the actual portfolio at `/tmp/honey-bee-portfolio-20261010`: square artwork, rounded cards, short sans-serif titles, bottom framework rows and the phone carousel follow the source structure. Both newly included EcoVadis/CDP image files are byte-identical to the supplied portfolio assets.

| Area | Actual current-delta check and result |
|---|---|
| English and French layout | **320, 390, 768 and 1440 px** in each language. Document width equals viewport width in all eight configurations; no page overflow with all service details opened or business benefits expanded. Static `fr.html` starts in French. |
| Service presentation | All three artwork boxes measure **1:1** in every configuration. Rounded cards and DM Sans titles render correctly; all illustration/framework images load. Clean viewport captures reviewed at EN 1440 and FR 320/390, including the full cards and phone cards two/three. |
| Service controls | Phone next arrows, ArrowLeft on the focused track, direct horizontal scrolling and the **1 / 3 → 2 / 3 → 3 / 3** counter pass in both languages at 320/390. Previous-button activation also passes in the final 320 px EN/FR recheck. Boundary arrows disable correctly. Comparison buttons and playback controls measure **44 px** high in sampled desktop/phone views. |
| Optional detail | Service deliverables and business benefits start closed. Business-benefit details open and close normally; the native disclosure also works without scripts. The adjacent audience and tools boundaries retain their layout. |
| Comparison content | Both businesses face the same stated request: policy/records, a measured dated result and a responsible contact. The competitor is explicitly an unprepared example. The outcome is easier assessment, with a nearby price/quality/fit limitation; no score, measured sales uplift, winner or guaranteed contract is asserted. |
| Eight preparation states | All **8 combinations** tested in each language at 390 px. Toggle `aria-pressed` values, each item's status and the illustrated windows match the selected features. Empty, partial and fully prepared titles/results use the correct language keys. The example competitor remains unprepared in every state. |
| Playback | The comparison does not advance automatically. Manual playback clears the example and adds its three features in order. Pause after the first step remains stable beyond a step interval; resume completes the remaining steps; a manual toggle cancels playback. Moving the comparison fully offscreen pauses it and preserves its state. |
| Live language change | EN → FR during a paused partial example preserves the selected items and uses the French partial result and “Continuer” label. Continuing completes the same example and shows “Revoir”. The new language event restores dynamic text after the main translator runs. |
| Reduced motion | Initial reduced-motion contexts in both languages complete replay immediately, with no timed playback. Changing the preference during playback also ends the timed sequence. Window transitions measure **0 s**; carousel scroll snap is disabled. |
| Without scripts | EN and static FR retain readable prepared/unprepared examples, disabled comparison buttons and a translated explanation. Native service scrolling remains available. After the repaired finding below, the inactive navigation/counter is hidden; bounded final EN/FR checks at 320 px confirm it appears only with working scripts. |
| Errors and existing tests | **0** script errors or failed resource responses in the eight-configuration pass; **0** script errors in the final fallback repair check. Independently rerun on the repaired final build: **11 tests passed, 0 failed**, including local references and French-key coverage. The current French dictionary contains **236 entries**. |

**Current-delta finding repaired and rechecked:** without JavaScript, the native service scroller could reach the third card while the visible counter stayed at “1 / 3” (`index.html:72`, also generated in `fr.html`). The navigation row now has a source `hidden` attribute; CSS respects it; `experience.js` reveals the row after installing handlers and calculating its state. Final EN/FR checks at 320 px verify hidden navigation with scripts disabled, usable native scrolling, and working arrows/counters with scripts enabled. **Current delta: PASS; no unresolved findings.**

The current tree adds four files and changes five existing files relative to the accepted 32-file baseline `26c0238b6414121ce9a5e3279cf5373c6b51dfde1dc6f55237767bcd9aa2287e`. The other **27 files** remain byte-identical, including the accepted minimal bee exports, photographs, original stylesheet, calculator core, downloads and privacy pages. The application change outside the new experience module is the language event. Calculator/email browser extremes were not repeated for this delta; their prior acceptance and the freshly passing unit tests remain the relevant evidence.

**Prior full-site acceptance evidence**

| Area | Actual check and result |
|---|---|
| English and French | Main pages checked at **320, 390, 768 and 1440 px** in both languages. Static `fr.html` starts in French. EN → FR → EN and FR → EN → FR restore headings, education and placeholders correctly. |
| Mobile layout | Both tools opened in all eight configurations. Default, maximum, very small benefit and ordinary cent-value scenarios keep document width equal to viewport width. Service cards remain in their contained horizontal scroller. |
| Readability | Short visible introductions, three service cards, two company audiences and optional deliverable/tool details are present. French hero fits 320 px. Corrected education wording and audience labels render clearly. |
| Keyboard | Mobile menu focuses its first link, Tab reaches the next link, and Escape closes it and returns focus to the menu button. Focus indicators are visible. |
| Motion | Hero image runs by default; manual pause stops it; French control text updates; offscreen motion pauses. Reduced motion removes image animation, hides its motion control and changes smooth scrolling to automatic scrolling. |
| Calculator | Default **€4,000/year and 18 months** verified. Recurring costs, zero/negative savings, no initial cost, fractional rates and invalid/out-of-range inputs checked. Currency retains cents and distinguishes nonzero subcent values. Display formulas use approximation signs for rounding. |
| Calculator bounds | Accepted €1 billion inputs produce €1 billion savings and 12 months. A €0.01 cost scope with 0.1% savings and €1 billion implementation cost remains readable without horizontal page overflow. These cases were checked in both languages at all four widths. |
| Contact | English and French drafts preserve accents, ampersands, question marks, hash characters and line breaks. Tests intercepted the resulting email URL; **no email was sent**. Status text accurately explains that the user must review and send the draft. |
| Contact without scripts | In EN and static FR, fake entries followed by a button click and Enter produce **no new navigation or GET submission**. Submit is disabled; form fields have no serialised names; the direct-email fallback remains visible. |
| Storage and resources | Observed storage contains only `honeybee-language`. No analytics or remote embedded form was observed. Fonts and imagery load locally. Both CSVs parse as five rows with nine columns. |
| Contrast | The corrected olive colour has **5.11:1–5.81:1** contrast against the sampled about, cream, template and paper backgrounds. Hero copy and controls were visually inspected. |
| Brand assets | Final minimal monochrome mark has three filled SVG elements: a round head, paired wings and a body with one open band. Head and silhouette remain visible at favicon sizes and in 320/1440 px headers. Mark and wordmark PNG pixels match the corresponding SVG renders. Exports and social cover render without clipping. |
| Browser errors | **0** script errors or failed resource responses in the final eight-configuration browser pass. |
| Existing tests | **11 passed, 0 failed**: calculator arithmetic and invalid-input handling, safe email encoding, local references, translation-key coverage, and bundled font/licence presence. |

**Prior minimal-brand delta — 10 October 2026**

The user requested fewer logo elements after the full-site acceptance. The final bee removes outlines, antennae and the separate thorax. The bounded follow-up inspected the SVG, both PNG exports, the wordmark, social cover, 320/1440 px headers and the favicon asset rendered at 16, 24, 32, 48 and 80 px. The round head is distinct, the open band survives small rendering, and no header clipping or page overflow was found. Both PNG exports exactly match their SVG rasterisations.

At that earlier asset-only review, `bee-mark.svg/png`, `honey-bee-logo.svg/png` and `social-cover.png` were the only changed `dist/` files. The other **27 files** were byte-identical to the preceding full-site fingerprint `ef682e5522fd269c61ac9c597d2cf314929adbc9b7a665cd82c0411ed2570561`, recovered from the then-current Git HEAD. The full tools matrix was not rerun for that asset-only change. It established the accepted 32-file baseline `26c0238b6414121ce9a5e3279cf5373c6b51dfde1dc6f55237767bcd9aa2287e`. The minimal bee remains unchanged in the current service/comparison update. **Brand delta: PASS; broader acceptance retained.**

**Prior full-site findings repaired and rechecked**

| Finding | Repair verified |
|---|---|
| Education became `INSEECEnglish` after translation initialisation | Plain text now includes a middle-dot delimiter in both languages. |
| Later CSS forced phone tools into two columns | Final mobile rule stacks the tools; opened content fits. |
| Whole-euro rounding produced a visible division by €0 | €0.10 stays €0.10; nonzero subcent amounts use a less-than label; formulas disclose display approximation. |
| €100 input steps rejected ordinary costs such as €101.50 | Euro fields now accept cent increments. |
| Tab skipped an opened mobile menu | Opening the menu focuses its first link. |
| Small olive labels fell below 4.5:1 on several backgrounds | Olive darkened to `#596747`; sampled ratios now exceed 5:1. |
| French privacy metadata remained in English | Title and description now update in French. |
| Larger-company audience label had a class typo | Shared audience-kicker styling restored. |
| Contact form could submit named values by GET with scripts disabled | Source submit disabled, enabled only after handler installation; names removed; bilingual email fallback added. Click and Enter retested with fake values. |
| Large accepted calculator results overflowed 320 px | Result columns can shrink/wrap and stack below 420 px; maximum and very small-benefit cases retested. |

**Content and source alignment**

The site preserves the portfolio’s three useful areas: CSR/RSE foundations and action plans, customer evidence and ratings preparation, and ESG reporting/procurement/workflow support. It clearly addresses SMEs building their foundations and larger-company ESG teams seeking support on a defined project. No freelancer wording was found.

Founder wording was compared with `/tmp/honey-bee-portfolio-20261010/index.html`, including Paris/languages, Dataiku, Thales, CEVA, KEDGE and INSEEC. Experience remains at apprenticeship/internship contribution level. The employers are explicitly distinguished from Honey Bee clients. The site avoids a current-employment claim, unsupported performance figures and an INSEEC completion claim. This checks fidelity to the supplied public portfolio; it does not independently verify employment or qualifications.

The commercial case is framed as potential usefulness and measurable work. It explicitly avoids promised contracts, market share, ratings, certifications or assurance outcomes. Calculator exclusions and illustrative defaults are adjacent to the tool.

Linked primary resources were opened during the audit. The [EFRAG VSME page](https://www.efrag.org/en/projects/voluntary-reporting-standard-for-smes-vsme/concluded) supports the non-listed-SME scope and the purpose of responding to business partners’ sustainability-data requests. The [GHG Protocol Corporate Standard](https://ghgprotocol.org/corporate-standard) supports the inventory-guidance description. [ADEME’s business portal](https://agirpourlatransition.ademe.fr/entreprises) provides the stated transition guidance and support. The linked [GitHub privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) is reachable.

**Evidence and scope limits**

- Prior full-site screenshots: `.qa/auditor/final-en-1440-hero.png`, `.qa/auditor/final-fr-390-hero.png`, and EN/FR `final-*-320-extreme-calculator.png`. Prior minimal-brand captures: `brand-minimal-header-320.png`, `brand-minimal-header-1440.png` and `brand-minimal-favicon-sizes.png` in the same folder.
- Current delta: `.qa/auditor/current-delta-results.json`, `nojs-counter-recheck.json`, EN 1440 `delta-en-1440-cards.png` / `delta-en-1440-comparison.png`, and FR 320/390 `delta-fr-*-services.png` / `delta-fr-*-comparison*.png`. The matrix evidence predates only the bounded navigation fallback repair; that repair has its own final recheck. Viewport screenshots preserve the real sticky header and avoid the locator-capture overlap issue.
- Browser behaviour was tested in local headless Chromium with simulated viewport widths. Safari, Firefox, physical mobile devices and actual email-client opening were not tested.
- Background-tab handling is present in source; visibility-change behaviour was not independently simulated. Offscreen pause was exercised in the browser.
- The audit verifies the local build. Public deployment, hosted byte equality, trademark clearance and independent verification of the founder’s qualifications are outside this acceptance.
- Sampled contrast and keyboard checks do not constitute a complete accessibility certification.

**Reviewed artifact identity**

The final service/comparison `dist/` tree contains **36 files**. Its tree fingerprint is:

`9d4304ec51d907294ba503086fe447ada8136555766999a6a16904680731f84b`

Fingerprint method: sort the files by relative path; for each, append `path + NUL + SHA-256(file bytes) + LF`; take SHA-256 of that UTF-8 manifest. This includes the final bilingual pages and dictionaries, new experience assets and repaired fallback, retained contact safeguards, calculator styling, logos, fonts and normalised licence files.

Route used: **GPT-6.1 Sol MAX**. Exact audit token consumption and audit-specific provider quota data were unavailable.
