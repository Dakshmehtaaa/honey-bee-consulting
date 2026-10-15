/**
 * honeybees.consulting newsletter sign-ups.
 *
 * A Google Apps Script web app that appends each new email address to a Google Sheet.
 * Nothing else: no emails are sent from here, nothing is shared.
 *
 * The site posts form fields (email, lang, page, website) to the web app URL. "website" is a
 * honeypot that people never see; bots that fill it are answered "ok" and dropped.
 * Pasted into a sheet's own Apps Script (Extensions > Apps Script) it writes to that sheet.
 * Standalone, set SHEET_ID, or leave it empty to create a sheet on the first sign-up.
 * Deploy: Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone.
 */
var SHEET_ID = '';
var TAB = 'Subscribers';
var HEADER = ['Subscribed at', 'Email', 'Language', 'Page'];
var EMAIL = /^[^\s@<>()"',;:]+@[^\s@<>()"',;:]+\.[a-z]{2,}$/i;

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.website) return reply_({ ok: true });
  var email = String(p.email || '').trim().toLowerCase();
  // A leading = + - @ would make the sheet treat the cell as a formula.
  if (email.length > 254 || !EMAIL.test(email) || /^[=+\-@]/.test(email)) return reply_({ ok: false, error: 'invalid-email' });
  var lang = p.lang === 'fr' ? 'fr' : 'en';
  var page = String(p.page || '').replace(/[^\w.\/#-]/g, '').slice(0, 80);
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sheet = sheet_();
    var last = sheet.getLastRow();
    var known = last > 1 ? sheet.getRange(2, 2, last - 1, 1).getValues() : [];
    for (var i = 0; i < known.length; i++) {
      if (String(known[i][0]).toLowerCase() === email) return reply_({ ok: true, already: true });
    }
    sheet.appendRow([new Date(), email, lang, page]);
  } finally {
    lock.releaseLock();
  }
  return reply_({ ok: true });
}

function doGet() {
  return reply_({ ok: true, service: 'honeybees.consulting newsletter' });
}

function sheet_() {
  var props = PropertiesService.getScriptProperties();
  var id = SHEET_ID || props.getProperty('SHEET_ID');
  var book = id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActiveSpreadsheet();
  if (!book) {
    book = SpreadsheetApp.create('honeybees.consulting · newsletter subscribers');
    props.setProperty('SHEET_ID', book.getId());
  }
  var sheet = book.getSheetByName(TAB) || book.getSheets()[0].setName(TAB);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADER);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function reply_(body) {
  return ContentService.createTextOutput(JSON.stringify(body)).setMimeType(ContentService.MimeType.JSON);
}
