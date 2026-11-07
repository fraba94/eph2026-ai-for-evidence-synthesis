/* One-tap copy buttons of the Start page (EPH 2026 workshop), made for phones.
   Step 1: the screening prompt with the 20 records of a batch inserted where it says [PASTE THE RECORDS HERE].
           Missing abstracts are fetched from PubMed (NCBI E-utilities efetch) in the browser, same method as batch.js.
   Step 3: the extraction prompt with the full text of the paper inserted at its placeholder.
   Batch 1 (R001-R020) by default; ?batch=3 gives another batch (used by the demo video, which must not show batch 1).
   The copy is started inside the tap (ClipboardItem with a promise) so that phones accept it after the fetch. */
(function () {
  'use strict';
  var EFETCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi';
  var TOOL = 'eph2026_ai_evidence_workshop';
  var REPO_RAW = 'https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/';
  var SIZE = 20;
  var m = /[?&]batch=(\d+)/.exec(location.search);
  var BATCH = m ? Math.max(1, +m[1]) : 1;

  function clean(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').replace(/\|/g, '/').trim(); }

  function parseCSV(text) {
    text = String(text || '').replace(/^﻿/, '');
    var rows = [], row = [], field = '', inQ = false, i, c;
    for (i = 0; i < text.length; i++) {
      c = text[i];
      if (inQ) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
      else if (c === '"') inQ = true;
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(field); field = ''; rows.push(row); row = []; }
      else field += c;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    rows = rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ''; }); });
    var h = rows[0].map(function (x) { return x.trim().toLowerCase(); });
    return rows.slice(1).map(function (r) { var o = {}; h.forEach(function (k, j) { o[k] = (r[j] || '').trim(); }); return o; });
  }

  function fetchText(urls) {
    var i = 0;
    function next() {
      if (i >= urls.length) return Promise.reject(new Error('not found'));
      return fetch(urls[i++], { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text().then(function (t) { if (/^\s*</.test(t)) throw new Error('html'); return t; });
      }).catch(next);
    }
    return next();
  }

  function parsePubmed(xml) {
    var doc = new DOMParser().parseFromString(xml, 'application/xml'), out = {};
    var arts = doc.getElementsByTagName('PubmedArticle');
    for (var i = 0; i < arts.length; i++) {
      var pm = arts[i].getElementsByTagName('PMID')[0];
      if (!pm) continue;
      var parts = [], ab = arts[i].getElementsByTagName('Abstract')[0];
      if (ab) {
        var tx = ab.getElementsByTagName('AbstractText');
        for (var k = 0; k < tx.length; k++) {
          var label = tx[k].getAttribute('Label'), t = clean(tx[k].textContent);
          if (t) parts.push(label ? label.toUpperCase() + ': ' + t : t);
        }
      }
      out[pm.textContent.trim()] = parts.join(' ');
    }
    return out;
  }

  function efetch(ids, tries) {
    tries = tries || 0;
    return fetch(EFETCH + '?db=pubmed&retmode=xml&rettype=abstract&tool=' + TOOL + '&id=' + ids.join(',')).then(function (r) {
      if ((r.status === 429 || r.status >= 500) && tries < 1) return new Promise(function (res) { setTimeout(res, 1500); }).then(function () { return efetch(ids, 1); });
      if (!r.ok) throw new Error('PubMed answered ' + r.status);
      return r.text();
    }).then(function (x) { return typeof x === 'string' ? parsePubmed(x) : x; });
  }

  // ---- step 1: prompt + records
  var screeningCache = null;
  function buildScreening(btn) {
    if (screeningCache) return Promise.resolve(screeningCache);
    var promptEl = document.querySelector(btn.getAttribute('data-prompt'));
    return fetchText(['data/screening_records.csv', REPO_RAW + 'activity/data/screening_records.csv']).then(function (csv) {
      var all = parseCSV(csv).filter(function (r) { return r.record_id; });
      var start = (BATCH - 1) * SIZE, batch = all.slice(start, start + SIZE);
      if (!batch.length) throw new Error('no records in batch ' + BATCH);
      var ids = batch.filter(function (r) { return !clean(r.abstract) && /^\d+$/.test(r.pmid || ''); }).map(function (r) { return r.pmid; });
      var got = {}, warn = '';
      var fetched = ids.length ? efetch(ids).then(function (g) { got = g; }).catch(function (e) { warn = e.message; }) : Promise.resolve();
      return fetched.then(function () {
        var missing = 0;
        var lines = ['RECORDS ' + (start + 1) + '-' + (start + batch.length) + ' of ' + all.length +
          ' (' + batch.length + ' records: expect exactly ' + batch.length + ' rows back)', ''];
        batch.forEach(function (r) {
          var a = clean(r.abstract) || clean(got[r.pmid]);
          if (!a) missing++;
          lines.push('Record ' + clean(r.record_id) + ' | ' + clean(r.title) + ' | ' + (a || '[no abstract available]'));
        });
        var text = promptEl.textContent.replace(btn.getAttribute('data-placeholder'), function () { return lines.join('\n') + '\n'; });
        screeningCache = { text: text, n: batch.length, missing: missing, warn: warn };
        return screeningCache;
      });
    });
  }

  // ---- step 3: prompt + paper
  var extractionCache = null;
  function buildExtraction(btn) {
    if (extractionCache) return Promise.resolve(extractionCache);
    var promptEl = document.querySelector(btn.getAttribute('data-prompt'));
    var paperEl = document.querySelector(btn.getAttribute('data-paper'));
    var paper = paperEl && paperEl.textContent ? Promise.resolve(paperEl.textContent) : fetchText(['data/fulltext/Phan2020.txt', REPO_RAW + 'activity/data/fulltext/Phan2020.txt']);
    return paper.then(function (t) {
      var text = promptEl.textContent.replace(btn.getAttribute('data-placeholder'), function () { return t; });
      extractionCache = { text: text, n: 1, missing: 0, warn: '' };
      return extractionCache;
    });
  }

  function legacyCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
    document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, text.length);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    ta.remove();
    return ok;
  }

  // copy the result of a promise; the clipboard write starts inside the tap
  function copyFrom(promise) {
    var textP = promise.then(function (r) { return r.text; });
    if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write && window.isSecureContext) {
      try {
        var item = new ClipboardItem({ 'text/plain': textP.then(function (t) { return new Blob([t], { type: 'text/plain' }); }) });
        return navigator.clipboard.write([item]).then(function () { return promise; });
      } catch (e) { /* fall through */ }
    }
    return promise.then(function (r) {
      if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(r.text).then(function () { return r; }, function () { if (legacyCopy(r.text)) return r; throw new Error('copy blocked'); });
      }
      if (legacyCopy(r.text)) return r;
      throw new Error('copy blocked');
    });
  }

  document.querySelectorAll('[data-onetap]').forEach(function (btn) {
    var kind = btn.getAttribute('data-onetap');
    var label = btn.querySelector('span');
    var base = btn.getAttribute('data-label');
    var status = document.getElementById('onetap-' + kind + '-status');
    var idle = status ? status.innerHTML : '';
    var timer = null;
    function setLabel(t, cls) {
      label.textContent = t;
      btn.classList.remove('is-busy', 'is-done', 'is-err');
      if (cls) btn.classList.add(cls);
      btn.setAttribute('aria-busy', cls === 'is-busy' ? 'true' : 'false');
    }
    btn.addEventListener('click', function () {
      if (btn.classList.contains('is-busy')) return;
      clearTimeout(timer);
      setLabel(kind === 'screening' ? 'Preparing records…' : 'Preparing paper…', 'is-busy');
      var job = kind === 'screening' ? buildScreening(btn) : buildExtraction(btn);
      copyFrom(job).then(function (r) {
        setLabel(kind === 'screening' ? 'Copied: prompt + ' + r.n + ' records' : 'Copied: prompt + Phan2020 full text', 'is-done');
        if (status) {
          status.textContent = kind === 'screening'
            ? 'Now paste it into a new temporary chat of your AI app (web search off).' + (r.missing ? ' ' + r.missing + ' record(s) have no abstract available: the AI must mark them unsure.' : '') + (r.warn ? ' PubMed could not be reached (' + r.warn + '): some abstracts are missing.' : '')
            : 'Now paste it into a new temporary chat of your AI app (web search off).';
        }
        timer = setTimeout(function () { setLabel(base); if (status) status.innerHTML = idle; }, 6000);
      }).catch(function (e) {
        if (status) status.textContent = 'Could not copy automatically (' + e.message + '). Use the separate buttons below, or the records page.';
        setLabel(base);
      });
    });
  });
})();
