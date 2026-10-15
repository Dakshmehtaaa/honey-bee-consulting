# Newsletter sign-ups

The footer of every page has a "honeybees letter" sign-up. It only collects email addresses: no
emails are sent from here and nothing else is stored. Addresses land in a Google Sheet that only
Daksh can open, through a small Google Apps Script web app (`Code.gs`).

## Set it up once

1. Open the sheet "honeybees.consulting · newsletter subscribers" in Google Drive (or any new sheet).
2. **Extensions › Apps Script.** Replace the starter code with the contents of `Code.gs` and save.
3. **Deploy › New deployment.** Type: *Web app*. Execute as: *Me*. Who has access: *Anyone*.
   Authorise it when Google asks (it only asks for access to your spreadsheets).
4. Copy the web app URL (it ends in `/exec`) and put it in `NEWSLETTER_URL` at the top of the
   newsletter section of `dist/assets/business-core.js`.
5. Run `node --test tests/*.test.cjs`, then publish.

Each sign-up adds a row to the *Subscribers* tab: date, email, language (en/fr) and the page it came
from. Repeat sign-ups of the same address are ignored.

## How it behaves

- The site checks the address before sending anything and posts four form fields: `email`, `lang`,
  `page` and `website`. `website` is a hidden honeypot: bots that fill it get "ok" and are dropped.
- The script checks the address again, refuses anything a spreadsheet would read as a formula
  (a leading `=`, `+`, `-` or `@`) and uses a lock so two sign-ups at once don't clash.
- The browser posts with `mode: 'no-cors'`, so the page can't read the reply. It shows "You're on
  the list" once the request has gone and an error only when the network fails.
- Until `NEWSLETTER_URL` is set, the button opens a ready-made sign-up email to
  dakshmehta077@gmail.com instead, so the form is never a dead end.

## Changing the script later

Edit `Code.gs` here first, paste it into the Apps Script editor, then **Deploy › Manage
deployments › Edit › New version**. Editing the existing deployment keeps the same URL; a brand new
deployment gets a new URL that has to go into `business-core.js` again.

To unsubscribe someone or answer a data request, delete or read their row in the sheet. The privacy
page (`dist/privacy.html#newsletter`) describes exactly this, so keep the two in step.
