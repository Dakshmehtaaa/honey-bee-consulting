# Honey Bee Consulting — independent audit

**Result: PASS for the reviewed local build. No unresolved findings remain.**

10 October 2026 · Separate GPT-6.1 Sol MAX auditor · Chromium headless · Preview: `http://127.0.0.1:8028/`

The audit inspected the actual HTML, CSS, JavaScript, bilingual copy, images, logo exports, downloads and public-source wording. The coordinator retains final acceptance and publication ownership.

**Acceptance evidence**

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

**Final brand delta — 10 October 2026**

The user requested fewer logo elements after the full-site acceptance. The final bee removes outlines, antennae and the separate thorax. The bounded follow-up inspected the SVG, both PNG exports, the wordmark, social cover, 320/1440 px headers and the favicon asset rendered at 16, 24, 32, 48 and 80 px. The round head is distinct, the open band survives small rendering, and no header clipping or page overflow was found. Both PNG exports exactly match their SVG rasterisations.

Only `bee-mark.svg/png`, `honey-bee-logo.svg/png` and `social-cover.png` changed in `dist/`. The other **27 files** are byte-identical to the previously accepted tree fingerprint `ef682e5522fd269c61ac9c597d2cf314929adbc9b7a665cd82c0411ed2570561`, recovered from Git HEAD. The photographs, content, styles and application logic therefore retain the earlier acceptance. The full tools matrix was not rerun for this asset-only change. **Brand delta: PASS; broader acceptance retained.**

**Findings repaired and rechecked**

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

- Full-site screenshots: `.qa/auditor/final-en-1440-hero.png`, `.qa/auditor/final-fr-390-hero.png`, and EN/FR `final-*-320-extreme-calculator.png`. Current minimal-brand captures: `brand-minimal-header-320.png`, `brand-minimal-header-1440.png` and `brand-minimal-favicon-sizes.png` in the same folder.
- Browser behaviour was tested in local headless Chromium with simulated viewport widths. Safari, Firefox, physical mobile devices and actual email-client opening were not tested.
- The audit verifies the local build. Public deployment, hosted byte equality, trademark clearance and independent verification of the founder’s qualifications are outside this acceptance.
- Sampled contrast and keyboard checks do not constitute a complete accessibility certification.

**Reviewed artifact identity**

The final `dist/` tree contains **32 files**. Its tree fingerprint is:

`26c0238b6414121ce9a5e3279cf5373c6b51dfde1dc6f55237767bcd9aa2287e`

Fingerprint method: sort the files by relative path; for each, append `path + NUL + SHA-256(file bytes) + LF`; take SHA-256 of that UTF-8 manifest. This includes the final French page, copy dictionary, contact safeguards, calculator styling, logos, fonts and normalised licence files.

Usage: exact audit token consumption and audit-specific provider quota data were unavailable.
