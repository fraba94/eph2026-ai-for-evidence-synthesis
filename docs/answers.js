/* EPH 2026 · AI for evidence synthesis · the reference answers page (answers.html).
   Nothing is fetched or shown until the visitor presses a reveal button: screening answers after step 1,
   extraction answers after step 3. Reads the copies in docs/data/ (falls back to the raw files on GitHub).
   No external scripts; nothing is sent anywhere. */
(function () {
  'use strict';
  var RAW = 'https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/';
  var SRC = {
    gold: ['data/screening_gold.csv', RAW + 'activity/answers/screening_gold.csv'],
    records: ['data/screening_records.csv', RAW + 'activity/data/screening_records.csv'],
    egold: ['data/extraction_gold.csv', RAW + 'activity/answers/extraction_gold.csv'],
    form: ['data/extraction_form.csv', RAW + 'activity/data/extraction_form.csv']
  };
  // the short extraction of step 3 (the same five fields as SHORT_FIELDS in docs/build_pages.py)
  var SHORT = ['country', 'study_design', 'intervention_components', 'primary_hai_outcome', 'direction_of_effect'];

  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function parseCSV(text) {
    text = String(text || '').replace(/^﻿/, '');
    var rows = [], row = [], field = '', inQ = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQ) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
      else if (c === '"') inQ = true;
      else if (c === ',') { row.push(field); field = ''; }
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
        return r.text().then(function (t) { if (/^\s*</.test(t)) throw new Error('html'); return parseCSV(t); });
      }).catch(next);
    }
    return next();
  }
  function setPressed(group, btn) {
    group.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
  }
  function fail(el, what) {
    el.innerHTML = '<span class="status err">Could not load the ' + what + '. Open the files of <a href="https://github.com/fraba94/eph2026-ai-for-evidence-synthesis/tree/main/activity/answers">activity/answers/</a> on GitHub.</span>';
  }

  // ---------------------------------------------------------------- screening
  var S = { rows: [], filter: 'all' };
  function renderScreening() {
    var rows = S.rows.filter(function (r) {
      if (S.filter === 'include') return r.d === 'include';
      if (S.filter === 'batch1') { var n = parseInt(r.id.replace(/\D/g, ''), 10); return n >= 1 && n <= 20; }
      return true;
    });
    var inc = rows.filter(function (r) { return r.d === 'include'; }).length;
    $('s-count').textContent = rows.length + ' records shown: ' + inc + ' include, ' + (rows.length - inc) + ' exclude.';
    $('s-body').innerHTML = rows.map(function (r) {
      var flag = /POSSIBLE GOLD-STANDARD ERROR/i.test(r.basis) ? ' <span class="tag partial">possible reference error</span>' : '';
      var ft = /full-text assessment/i.test(r.basis) ? ' <span class="tag extra">excluded at full text</span>' : '';
      var pm = r.pmid ? '<br><a href="https://pubmed.ncbi.nlm.nih.gov/' + encodeURIComponent(r.pmid) + '/" target="_blank" rel="noopener">PubMed</a>' : '';
      return '<tr><td data-label="Record"><b>' + esc(r.id) + '</b></td>' +
        '<td data-label="Decision"><span class="tag ' + (r.d === 'include' ? 'match' : 'extra') + '">' + esc(r.d) + '</span>' + ft + flag + '</td>' +
        '<td data-label="Title">' + esc(r.title) + pm + '</td>' +
        '<td data-label="Basis of the reference decision">' + esc(r.basis) + '</td></tr>';
    }).join('');
  }
  function showScreening() {
    var box = $('screening-answers');
    box.hidden = false;
    Promise.all([fetchFirst(SRC.gold), fetchFirst(SRC.records).catch(function () { return []; })]).then(function (res) {
      var rec = {};
      res[1].forEach(function (r) { rec[(r.record_id || '').toUpperCase()] = r; });
      S.rows = res[0].map(function (g) {
        var id = (g.record_id || '').toUpperCase(), r = rec[id] || {};
        return { id: id, d: (g.gold_decision || '').toLowerCase(), basis: g.gold_basis || '', title: r.title || '', pmid: r.pmid || '' };
      });
      var incN = S.rows.filter(function (r) { return r.d === 'include'; }).length;
      box.querySelector('[data-sf="all"]').textContent = 'All ' + S.rows.length;
      box.querySelector('[data-sf="include"]').textContent = 'Includes (' + incN + ')';
      renderScreening();
    }).catch(function () { fail($('s-count'), 'screening answers'); });
    box.querySelectorAll('[data-sf]').forEach(function (b) {
      b.addEventListener('click', function () { S.filter = b.getAttribute('data-sf'); setPressed(b.parentNode, b); renderScreening(); });
    });
  }

  // ---------------------------------------------------------------- extraction
  var E = { rows: [], core: {}, study: 'Phan2020', fields: 'short' };
  function renderExtraction() {
    var rows = E.rows.filter(function (r) {
      if (E.study !== 'all' && r.study_id !== E.study) return false;
      if (E.fields === 'short') return SHORT.indexOf(r.field) >= 0;
      if (E.fields === 'core') return E.core[r.field] === 'yes';
      return true;
    });
    $('e-count').textContent = rows.length + ' reference values shown.';
    $('e-body').innerHTML = rows.map(function (r) {
      var notes = [r.notes ? esc(r.notes) : '', r.review_table_value ? '<i>Reference review\'s table:</i> ' + esc(r.review_table_value) : '']
        .filter(Boolean).join('<br>');
      return '<tr><td data-label="Field"><code>' + esc(r.field) + '</code></td><td data-label="Study">' + esc(r.study_id) + '</td>' +
        '<td data-label="Value"><b>' + esc(r.value) + '</b></td>' +
        '<td data-label="Quote">' + (r.source_quote ? '<q>' + esc(r.source_quote) + '</q>' : '') + '</td>' +
        '<td data-label="Location">' + esc(r.location) + '</td><td data-label="Notes">' + notes + '</td></tr>';
    }).join('');
  }
  function showExtraction() {
    var box = $('extraction-answers');
    box.hidden = false;
    Promise.all([fetchFirst(SRC.egold), fetchFirst(SRC.form).catch(function () { return []; })]).then(function (res) {
      E.rows = res[0];
      res[1].forEach(function (f) { E.core[f.field] = (f.core || '').toLowerCase(); });
      var studies = [];
      E.rows.forEach(function (r) { if (studies.indexOf(r.study_id) < 0) studies.push(r.study_id); });
      if (studies.indexOf(E.study) < 0) E.study = 'all';
      var g = $('e-studies');
      g.innerHTML = ['all'].concat(studies).map(function (sid) {
        return '<button type="button" data-study="' + esc(sid) + '" aria-pressed="' + (sid === E.study) + '">' + (sid === 'all' ? 'All studies' : esc(sid)) + '</button>';
      }).join('');
      g.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () { E.study = b.getAttribute('data-study'); setPressed(g, b); renderExtraction(); });
      });
      renderExtraction();
    }).catch(function () { fail($('e-count'), 'extraction values'); });
    box.querySelectorAll('[data-ef]').forEach(function (b) {
      b.addEventListener('click', function () { E.fields = b.getAttribute('data-ef'); setPressed(b.parentNode, b); renderExtraction(); });
    });
  }

  document.querySelectorAll('[data-reveal]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var what = btn.getAttribute('data-reveal');
      var gate = document.querySelector('[data-gate="' + what + '"]');
      if (gate) gate.hidden = true;
      if (what === 'screening') showScreening(); else showExtraction();
      var sec = document.getElementById(what);
      if (sec && sec.scrollIntoView) sec.scrollIntoView({ block: 'start' });
    });
  });
})();
