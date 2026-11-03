/* Copy-ready screening batches for chat users (EPH 2026 workshop).
   Reads the records CSV, fills missing abstracts from PubMed (NCBI E-utilities efetch, called from
   the browser, at most 20 PMIDs per request, one request at a time) and renders
   "Record R001 | Title | Abstract" lines ready to paste after the screening prompt.
   Abstracts are fetched live into the browser and are not stored anywhere. */
(function () {
  'use strict';

  var REPO_RAW = 'https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/';
  var EFETCH = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi';
  var TOOL = 'eph2026_ai_evidence_workshop';
  var MAX_IDS = 20;          // NCBI: keep batches small
  var MIN_GAP_MS = 400;      // without an API key NCBI allows 3 requests/second: stay below
  var SAMPLE = /[?&]sample=1\b/.test(location.search);
  var SOURCES = SAMPLE ? ['data/_sample/batch_records.csv'] :
    ['data/screening_records.csv', '../activity/data/screening_records.csv', REPO_RAW + 'activity/data/screening_records.csv'];

  var records = [], from = '', size = 20, current = 0;
  var fetched = {};          // pmid -> abstract text ('' = PubMed has no abstract)
  var lastCall = 0, queue = Promise.resolve();

  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function clean(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').replace(/\|/g, '/').trim(); }

  // ---------------------------------------------------------------- CSV (RFC 4180, auto delimiter)
  function parseCSV(text) {
    text = String(text || '').replace(/^﻿/, '');
    var firstLine = text.split(/\r?\n/)[0] || '';
    var d = [',', ';', '\t'].sort(function (a, b) { return firstLine.split(b).length - firstLine.split(a).length; })[0];
    var rows = [], row = [], field = '', inQ = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQ) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
      else if (c === '"') inQ = true;
      else if (c === d) { row.push(field); field = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && text[i + 1] === '\n') i++; row.push(field); field = ''; rows.push(row); row = []; }
      else field += c;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    rows = rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ''; }); });
    if (!rows.length) return [];
    var h = rows[0].map(function (x) { return x.trim().toLowerCase(); });
    return rows.slice(1).map(function (r) { var o = {}; h.forEach(function (k, j) { o[k] = (r[j] || '').trim(); }); return o; });
  }

  function fetchFirst(urls) {
    var i = 0;
    function next() {
      if (i >= urls.length) return Promise.reject(new Error('not found'));
      var u = urls[i++];
      return fetch(u, { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text().then(function (t) { if (/^\s*</.test(t)) throw new Error('html'); return { url: u, text: t }; });
      }).catch(next);
    }
    return next();
  }

  // ---------------------------------------------------------------- PubMed
  function parsePubmedXML(xml) {
    var doc = new DOMParser().parseFromString(xml, 'application/xml');
    var out = {};
    var arts = doc.getElementsByTagName('PubmedArticle');
    for (var i = 0; i < arts.length; i++) {
      var a = arts[i];
      var pmidEl = a.getElementsByTagName('PMID')[0];
      if (!pmidEl) continue;
      var parts = [];
      var ab = a.getElementsByTagName('Abstract')[0];
      if (ab) {
        var texts = ab.getElementsByTagName('AbstractText');
        for (var k = 0; k < texts.length; k++) {
          var label = texts[k].getAttribute('Label');
          var t = clean(texts[k].textContent);
          if (t) parts.push(label ? label.toUpperCase() + ': ' + t : t);
        }
      }
      out[pmidEl.textContent.trim()] = parts.join(' ');
    }
    return out;
  }

  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // One request at a time, spaced by MIN_GAP_MS, one retry on 429/5xx.
  function efetch(pmids) {
    var job = queue.then(function () {
      var gap = Math.max(0, lastCall + MIN_GAP_MS - Date.now());
      return wait(gap).then(function attempt(_, tries) {
        tries = tries || 0;
        lastCall = Date.now();
        var url = EFETCH + '?db=pubmed&retmode=xml&rettype=abstract&tool=' + TOOL + '&id=' + pmids.join(',');
        return fetch(url).then(function (r) {
          if ((r.status === 429 || r.status >= 500) && tries < 1) return wait(1500).then(function () { return attempt(null, tries + 1); });
          if (!r.ok) throw new Error('PubMed answered ' + r.status);
          return r.text();
        });
      });
    });
    queue = job.catch(function () {});
    return job.then(function (xml) { return typeof xml === 'string' ? parsePubmedXML(xml) : xml; });
  }

  function needsFetch(r) { return !clean(r.abstract) && /^\d+$/.test(r.pmid || '') && !(r.pmid in fetched); }

  function fillBatch(batch) {
    var ids = batch.filter(needsFetch).map(function (r) { return r.pmid; });
    if (!ids.length) return Promise.resolve();
    var chunks = [];
    for (var i = 0; i < ids.length; i += MAX_IDS) chunks.push(ids.slice(i, i + MAX_IDS));
    setStatus('Fetching ' + ids.length + ' missing abstract(s) from PubMed...', '');
    return chunks.reduce(function (p, chunk) {
      return p.then(function () {
        return efetch(chunk).then(function (got) {
          chunk.forEach(function (id) { fetched[id] = got[id] || ''; });
        });
      });
    }, Promise.resolve());
  }

  // ---------------------------------------------------------------- render
  function abstractOf(r) {
    var own = clean(r.abstract);
    if (own) return { text: own, src: 'file' };
    if (r.pmid in fetched) return fetched[r.pmid] ? { text: fetched[r.pmid], src: 'pubmed' } : { text: '', src: 'none' };
    return { text: '', src: /^\d+$/.test(r.pmid || '') ? 'pending' : 'none' };
  }

  function batchText(batch, start) {
    var lines = ['RECORDS ' + (start + 1) + '-' + (start + batch.length) + ' of ' + records.length +
      ' (' + batch.length + ' records: expect exactly ' + batch.length + ' rows back)', ''];
    batch.forEach(function (r) {
      var a = abstractOf(r);
      lines.push('Record ' + clean(r.record_id) + ' | ' + clean(r.title) + ' | ' + (a.text || '[no abstract available]'));
    });
    return lines.join('\n') + '\n';
  }

  function renderSelector() {
    var n = Math.ceil(records.length / size), html = '';
    for (var i = 0; i < n; i++) {
      var a = i * size + 1, b = Math.min((i + 1) * size, records.length);
      html += '<button type="button" class="btn ' + (i === current ? 'btn-primary' : 'btn-plain') + '" data-b="' + i + '" aria-pressed="' + (i === current) + '">' + a + '–' + b + '</button>';
    }
    $('batches').innerHTML = html;
    $('batches').querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () { showBatch(+b.dataset.b); });
    });
  }

  function setStatus(msg, cls) { var s = $('b-status'); s.className = 'status ' + (cls || ''); s.innerHTML = msg; }

  function showBatch(i) {
    current = i; renderSelector();
    var start = i * size, batch = records.slice(start, start + size);
    $('out').value = batchText(batch, start);
    $('copy').disabled = true;
    return fillBatch(batch).then(function () {
      $('out').value = batchText(batch, start);
      var c = { file: 0, pubmed: 0, none: 0, pending: 0 };
      batch.forEach(function (r) { c[abstractOf(r).src]++; });
      setStatus('<b>' + batch.length + '</b> records ready. Abstracts: ' + c.file + ' from the file, ' + c.pubmed + ' fetched from PubMed' +
        (c.none ? ', <b>' + c.none + ' not available</b> (screen those on the title, or mark them unsure)' : '') + '.', 'ok');
    }).catch(function (e) {
      setStatus('Could not reach PubMed (' + esc(e.message) + '). The batch below has titles only for the missing abstracts. Try again in a minute, or ask a facilitator.', 'err');
    }).then(function () { $('copy').disabled = false; });
  }

  function copyText() {
    var t = $('out').value;
    var done = function () { var b = $('copy'); var old = b.innerHTML; b.innerHTML = 'Copied'; setTimeout(function () { b.innerHTML = old; }, 1600); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t).then(done, fallback); else fallback();
    function fallback() { var o = $('out'); o.focus(); o.select(); try { document.execCommand('copy'); done(); } catch (e) { /* user can copy manually */ } }
  }

  function load(text, label) {
    var rows = parseCSV(text).filter(function (r) { return r.record_id; });
    if (!rows.length || !('title' in rows[0])) throw new Error('The file needs at least the columns record_id and title.');
    records = rows; from = label; current = 0;
    var missing = rows.filter(function (r) { return !clean(r.abstract); }).length;
    $('src').innerHTML = '<b>' + rows.length + '</b> records loaded (' + missing + ' without an abstract in the file). <span class="muted">Source: ' + esc(from) + '</span>';
    $('src').className = 'status ok';
    $('work').hidden = false;
    return showBatch(0);
  }

  document.addEventListener('DOMContentLoaded', function () {
    $('size').addEventListener('change', function () { size = +this.value; current = 0; if (records.length) showBatch(0); });
    $('copy').addEventListener('click', copyText);
    $('dl').addEventListener('click', function () {
      var blob = new Blob([$('out').value], { type: 'text/plain;charset=utf-8' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob);
      a.download = 'screening_batch_' + String(current + 1).padStart(2, '0') + '.txt';
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    $('file').addEventListener('change', function (ev) {
      var f = ev.target.files[0]; if (!f) return;
      var r = new FileReader();
      r.onload = function () { try { load(r.result, 'your file ' + f.name); } catch (e) { $('src').className = 'status err'; $('src').textContent = e.message; } };
      r.readAsText(f);
    });
    if (SAMPLE) $('sample-banner').hidden = false;
    fetchFirst(SOURCES).then(function (r) { return load(r.text, r.url); }).catch(function () {
      $('src').className = 'status err';
      $('src').innerHTML = 'The workshop records are not available here yet. Choose the records CSV below, or <a href="?sample=1">try a sample of real PubMed records</a>.';
    });
  });

  window.EPHBatch = { parsePubmedXML: parsePubmedXML, parseCSV: parseCSV };
})();
