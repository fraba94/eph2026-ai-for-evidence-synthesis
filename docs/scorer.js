/* Browser scorer for the EPH 2026 workshop "AI for evidence synthesis".
   Runs entirely in the browser: files are read locally and never uploaded.
   Formats (see the repository README):
     screening_records.csv  record_id,pmid,doi,title,abstract,year,journal,license
     screening_gold.csv     record_id,gold_decision,gold_basis
     your decisions         record_id,decision,reason        (decision: include|exclude|unsure)
     extraction_form.csv    field,definition,allowed_values,type
     extraction_gold.csv    study_id,field,value,source_quote,location
     your extraction        study_id,field,value,source_quote,location
*/
(function () {
  'use strict';

  var REPO_RAW = 'https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/';
  var SAMPLE = /[?&]sample=1\b/.test(location.search);

  // Where to look for each reference file, in order. data/ is filled by docs/sync_data.py;
  // ../activity/ works when the repository root is served locally; raw GitHub is the last resort.
  var SOURCES = {
    records: ['data/screening_records.csv', '../activity/data/screening_records.csv', REPO_RAW + 'activity/data/screening_records.csv'],
    sgold: ['data/screening_gold.csv', '../activity/answers/screening_gold.csv', REPO_RAW + 'activity/answers/screening_gold.csv'],
    form: ['data/extraction_form.csv', '../activity/data/extraction_form.csv', REPO_RAW + 'activity/data/extraction_form.csv'],
    egold: ['data/extraction_gold.csv', '../activity/answers/extraction_gold.csv', REPO_RAW + 'activity/answers/extraction_gold.csv']
  };
  if (SAMPLE) {
    SOURCES = {
      records: ['data/_sample/screening_records.csv'],
      sgold: ['data/_sample/screening_gold.csv'],
      form: ['data/_sample/extraction_form.csv'],
      egold: ['data/_sample/extraction_gold.csv']
    };
  }

  var ref = { records: null, sgold: null, form: null, egold: null };
  var refFrom = {};

  // ------------------------------------------------------------------ CSV
  function detectDelimiter(text) {
    var first = text.split(/\r?\n/).find(function (l) { return l.trim() !== ''; }) || '';
    var counts = { ',': 0, ';': 0, '\t': 0 };
    var inQ = false;
    for (var i = 0; i < first.length; i++) {
      var c = first[i];
      if (c === '"') inQ = !inQ;
      else if (!inQ && counts.hasOwnProperty(c)) counts[c]++;
    }
    var best = ',';
    Object.keys(counts).forEach(function (k) { if (counts[k] > counts[best]) best = k; });
    return best;
  }

  function parseCSV(text) {
    text = String(text || '').replace(/^﻿/, '');
    var d = detectDelimiter(text);
    var rows = [], row = [], field = '', inQ = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQ) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false;
        } else field += c;
      } else if (c === '"') inQ = true;
      else if (c === d) { row.push(field); field = ''; }
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && text[i + 1] === '\n') i++;
        row.push(field); field = '';
        rows.push(row); row = [];
      } else field += c;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    rows = rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ''; }); });
    if (!rows.length) return { header: [], rows: [] };
    var header = rows[0].map(function (h) { return h.trim().toLowerCase().replace(/^"|"$/g, ''); });
    var out = rows.slice(1).map(function (r) {
      var o = {};
      header.forEach(function (h, k) { o[h] = (r[k] == null ? '' : r[k]).trim(); });
      return o;
    });
    return { header: header, rows: out };
  }

  function toCSV(rows, cols) {
    function esc(v) { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
    return [cols.join(',')].concat(rows.map(function (r) { return cols.map(function (c) { return esc(r[c]); }).join(','); })).join('\n') + '\n';
  }

  function download(name, text) {
    var blob = new Blob([text], { type: 'text/csv;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  // ------------------------------------------------------------------ helpers
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function pct(n, d) { return d ? (100 * n / d).toFixed(1) + '%' : 'n/a'; }
  function frac(n, d) { return n + ' / ' + d; }
  function normId(s) { return String(s || '').trim().replace(/^"|"$/g, '').toUpperCase(); }

  function normDecision(s) {
    s = String(s || '').trim().toLowerCase();
    if (/^(include|included|inc|in|yes|y|1|i)$/.test(s)) return 'include';
    if (/^(exclude|excluded|exc|ex|out|no|n|0|e)$/.test(s)) return 'exclude';
    if (/^(unsure|maybe|uncertain|unclear|\?|u|possibly|can't tell|cannot tell)$/.test(s)) return 'unsure';
    return null;
  }

  function fetchFirst(urls) {
    var i = 0;
    function next() {
      if (i >= urls.length) return Promise.reject(new Error('not found'));
      var u = urls[i++];
      return fetch(u, { cache: 'no-cache' }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text().then(function (t) {
          if (/^\s*</.test(t)) throw new Error('html'); // an error page, not a CSV
          return { url: u, text: t };
        });
      }).catch(next);
    }
    return next();
  }

  function readFile(input) {
    return new Promise(function (resolve, reject) {
      var f = input.files && input.files[0];
      if (!f) return reject(new Error('no file'));
      var r = new FileReader();
      r.onload = function () { resolve({ name: f.name, text: r.result }); };
      r.onerror = reject;
      r.readAsText(f);
    });
  }

  function requireCols(parsed, cols, what) {
    var missing = cols.filter(function (c) { return parsed.header.indexOf(c) < 0; });
    if (missing.length) throw new Error(what + ': missing column(s) ' + missing.join(', ') + '. Found: ' + (parsed.header.join(', ') || 'nothing'));
  }

  // ------------------------------------------------------------------ reference data
  function setRefStatus() {
    var s = $('ref-status-s');
    if (ref.sgold) {
      s.className = 'status ok';
      s.innerHTML = 'Reference standard loaded: <b>' + Object.keys(ref.sgold).length + '</b> records (' +
        Object.values(ref.sgold).filter(function (g) { return g.d === 'include'; }).length + ' includes)' +
        (ref.records ? ', titles available' : ', titles not available') + '. <span class="muted">Source: ' + esc(refFrom.sgold) + '</span>';
    } else {
      s.className = 'status err';
      s.innerHTML = 'Reference standard not found yet. Ask the facilitator, load it below under "Use another reference file", or <a href="?sample=1">try the synthetic sample</a>.';
    }
    var e = $('ref-status-e');
    if (ref.egold) {
      var studies = {}; ref.egold.forEach(function (r) { studies[r.study] = 1; });
      e.className = 'status ok';
      e.innerHTML = 'Reference extraction loaded: <b>' + ref.egold.length + '</b> values from <b>' + Object.keys(studies).length +
        '</b> studies. <span class="muted">Source: ' + esc(refFrom.egold) + '</span>';
    } else {
      e.className = 'status err';
      e.innerHTML = 'Reference extraction not found yet. Load it below under "Use another reference file", or <a href="?sample=1#extraction">try the synthetic sample</a>.';
    }
    if (SAMPLE) {
      $('sample-banner').hidden = false;
    }
  }

  function ingestSGold(text, from) {
    var p = parseCSV(text);
    requireCols(p, ['record_id', 'gold_decision'], 'Reference screening file');
    var g = {};
    p.rows.forEach(function (r) {
      var d = normDecision(r.gold_decision);
      if (!r.record_id || !d) return;
      g[normId(r.record_id)] = { id: r.record_id.trim(), d: d === 'unsure' ? 'include' : d, basis: r.gold_basis || '' };
    });
    ref.sgold = g; refFrom.sgold = from;
  }
  function ingestRecords(text, from) {
    var p = parseCSV(text);
    requireCols(p, ['record_id', 'title'], 'Records file');
    var m = {};
    p.rows.forEach(function (r) { m[normId(r.record_id)] = r; });
    ref.records = m; refFrom.records = from;
  }
  function ingestEGold(text, from) {
    var p = parseCSV(text);
    requireCols(p, ['study_id', 'field', 'value'], 'Reference extraction file');
    ref.egold = p.rows.filter(function (r) { return r.study_id && r.field; }).map(function (r) {
      return { study: r.study_id.trim(), field: r.field.trim(), value: r.value, quote: r.source_quote || '', loc: r.location || '' };
    });
    refFrom.egold = from;
  }
  function ingestForm(text, from) {
    var p = parseCSV(text);
    requireCols(p, ['field'], 'Extraction form');
    ref.form = p.rows; refFrom.form = from;
  }

  function loadReferences() {
    var jobs = [
      fetchFirst(SOURCES.sgold).then(function (r) { ingestSGold(r.text, r.url); }).catch(function () {}),
      fetchFirst(SOURCES.records).then(function (r) { ingestRecords(r.text, r.url); }).catch(function () {}),
      fetchFirst(SOURCES.egold).then(function (r) { ingestEGold(r.text, r.url); }).catch(function () {}),
      fetchFirst(SOURCES.form).then(function (r) { ingestForm(r.text, r.url); }).catch(function () {})
    ];
    return Promise.all(jobs).then(setRefStatus);
  }

  // ------------------------------------------------------------------ screening
  function parseDecisions(text) {
    var p = parseCSV(text);
    requireCols(p, ['record_id', 'decision'], 'Your decisions');
    var map = {}, invalid = [], dup = [];
    p.rows.forEach(function (r, i) {
      var id = normId(r.record_id);
      if (!id) return;
      var d = normDecision(r.decision);
      if (!d) { invalid.push({ line: i + 2, id: r.record_id, value: r.decision }); return; }
      if (map[id]) dup.push(r.record_id);
      map[id] = { id: r.record_id.trim(), d: d, reason: r.reason || '' };
    });
    return { map: map, invalid: invalid, dup: dup, n: p.rows.length };
  }

  function binary(d, unsureAs) { return d === 'unsure' ? unsureAs : d; }

  function kappa(a, b, ids) {
    // Cohen's kappa for two raters over ids, categories include/exclude/unsure
    var cats = ['include', 'exclude', 'unsure'], n = 0, agree = 0, ca = {}, cb = {};
    cats.forEach(function (c) { ca[c] = 0; cb[c] = 0; });
    ids.forEach(function (id) {
      var x = a(id), y = b(id);
      if (!x || !y) return;
      n++; if (x === y) agree++;
      ca[x]++; cb[y]++;
    });
    if (!n) return { n: 0 };
    var po = agree / n, pe = 0;
    cats.forEach(function (c) { pe += (ca[c] / n) * (cb[c] / n); });
    return { n: n, agree: agree, po: po, k: pe === 1 ? 1 : (po - pe) / (1 - pe) };
  }

  function title(id) {
    var r = ref.records && ref.records[id];
    return r ? r.title : '';
  }

  var lastScreening = null;

  function scoreScreening() {
    var out = $('s-results'), msg = $('s-msg');
    msg.textContent = ''; msg.className = 'status';
    if (!ref.sgold) { msg.className = 'status err'; msg.textContent = 'The reference standard is not loaded, so nothing can be scored yet.'; return; }
    var text = $('s-text').value;
    if (!text.trim()) { msg.className = 'status err'; msg.textContent = 'Paste your decisions or choose a CSV file first.'; return; }
    var run;
    try { run = parseDecisions(text); } catch (e) { msg.className = 'status err'; msg.textContent = e.message; return; }

    var unsureAs = $('s-unsure').value, missingAs = $('s-missing').value;
    var tp = 0, fp = 0, fn = 0, tn = 0, unsure = 0, missing = [], fnList = [], fpList = [], rows = [];
    Object.keys(ref.sgold).forEach(function (id) {
      var g = ref.sgold[id], mine = run.map[id];
      var raw = mine ? mine.d : null;
      if (raw === 'unsure') unsure++;
      var d = raw ? binary(raw, unsureAs) : (missingAs === 'exclude' ? 'exclude' : null);
      if (!mine) missing.push(id);
      var cell = '';
      if (d === 'include' && g.d === 'include') { tp++; cell = 'TP'; }
      else if (d === 'include' && g.d === 'exclude') { fp++; cell = 'FP'; fpList.push(id); }
      else if (d === 'exclude' && g.d === 'include') { fn++; cell = 'FN'; fnList.push(id); }
      else if (d === 'exclude' && g.d === 'exclude') { tn++; cell = 'TN'; }
      else cell = 'not scored';
      rows.push({ record_id: g.id, your_decision: raw || '(none)', counted_as: d || '(left out)', gold_decision: g.d, result: cell,
        your_reason: mine ? mine.reason : '', gold_basis: g.basis, title: title(id) });
    });
    var unknown = Object.keys(run.map).filter(function (id) { return !ref.sgold[id]; });
    var N = tp + fp + fn + tn;
    var sens = tp / (tp + fn), spec = tn / (tn + fp), prec = tp / (tp + fp), npv = tn / (tn + fn);
    var f1 = (2 * tp) / (2 * tp + fp + fn);
    var k = kappa(function (id) { var m = run.map[id]; return m ? binary(m.d, unsureAs) : (missingAs === 'exclude' ? 'exclude' : null); },
      function (id) { return ref.sgold[id].d; }, Object.keys(ref.sgold));

    function num(x) { return isFinite(x) ? (100 * x).toFixed(1) + '%' : 'n/a'; }
    var html = '';
    html += '<div class="metrics">' +
      metric('Sensitivity (recall)', num(sens), frac(tp, tp + fn) + ' reference includes found', true, fn > 0) +
      metric('Specificity', num(spec), frac(tn, tn + fp) + ' reference excludes excluded') +
      metric('Precision', num(prec), frac(tp, tp + fp) + ' of your includes are correct') +
      metric('Missed includes', String(fn), 'reference includes you excluded' + (missingAs === 'exclude' ? ' or did not screen' : ''), false, fn > 0) +
      '</div>';
    html += '<div class="grid grid-2" style="margin-top:18px">';
    html += '<div class="card"><h3>Confusion matrix</h3><table class="cm" aria-label="Confusion matrix">' +
      '<tr><th></th><th>Reference: include</th><th>Reference: exclude</th></tr>' +
      '<tr><th>You: include</th><td class="tp"><b>' + tp + '</b><span>true positive</span></td><td class="fp"><b>' + fp + '</b><span>false positive</span></td></tr>' +
      '<tr><th>You: exclude</th><td class="fn"><b>' + fn + '</b><span>false negative</span></td><td class="tn"><b>' + tn + '</b><span>true negative</span></td></tr>' +
      '</table></div>';
    html += '<div class="card"><h3>Other indicators</h3><table class="data">' +
      '<tr><td>Records scored</td><td><b>' + N + '</b> of ' + Object.keys(ref.sgold).length + '</td></tr>' +
      '<tr><td>Negative predictive value</td><td><b>' + num(npv) + '</b></td></tr>' +
      '<tr><td>F1 score</td><td><b>' + num(f1) + '</b></td></tr>' +
      '<tr><td>Agreement with reference (Cohen\'s kappa)</td><td><b>' + (k.n ? k.k.toFixed(2) : 'n/a') + '</b></td></tr>' +
      '<tr><td>"Unsure" decisions</td><td><b>' + unsure + '</b> (counted as ' + unsureAs + ')</td></tr>' +
      '<tr><td>Reference records with no decision</td><td><b>' + missing.length + '</b>' + (missing.length ? ' (' + (missingAs === 'exclude' ? 'counted as exclude' : 'left out') + ')' : '') + '</td></tr>' +
      '<tr><td>IDs not in the reference</td><td><b>' + unknown.length + '</b></td></tr>' +
      '</table></div></div>';

    var warn = [];
    if (missing.length) warn.push('<b>' + missing.length + ' record(s) have no decision</b>: ' + missing.map(function (id) { return esc(ref.sgold[id].id); }).join(', ') + '. A record that is silently dropped is a record that can be missed.');
    if (unknown.length) warn.push('<b>' + unknown.length + ' ID(s) are not in the reference set</b> and were ignored: ' + unknown.map(function (id) { return esc(run.map[id].id); }).join(', ') + '. Check for typos or invented IDs.');
    if (run.invalid.length) warn.push('<b>' + run.invalid.length + ' row(s) have a decision that is not include, exclude or unsure</b> and were ignored: ' + run.invalid.map(function (x) { return 'line ' + x.line + ' (' + esc(x.value || 'empty') + ')'; }).join(', ') + '.');
    if (run.dup.length) warn.push('<b>Duplicated IDs</b> (the last row was used): ' + run.dup.map(esc).join(', ') + '.');
    if (warn.length) html += '<div class="callout warn" style="margin-top:18px">' + ICON_WARN + '<div>' + warn.map(function (w) { return '<p>' + w + '</p>'; }).join('') + '</div></div>';

    html += listTable('Missed includes (false negatives)', 'fn', fnList, run, 'These are the errors that matter most at screening: a study excluded here never reaches the review.');
    html += listTable('Extra includes (false positives)', 'fp', fpList, run, 'These cost reviewer time at full-text stage but do not lose evidence.');

    // reproducibility
    var t2 = $('s-text2').value;
    if (t2.trim()) {
      try {
        var run2 = parseDecisions(t2);
        var ids = Object.keys(ref.sgold);
        var kk = kappa(function (id) { return run.map[id] && run.map[id].d; }, function (id) { return run2.map[id] && run2.map[id].d; }, ids);
        var dis = ids.filter(function (id) { return run.map[id] && run2.map[id] && run.map[id].d !== run2.map[id].d; });
        html += '<div class="card" style="margin-top:18px"><h3>Reproducibility: run 1 versus run 2</h3>' +
          '<p>Compared on <b>' + kk.n + '</b> records decided in both runs. Agreement <b>' + (kk.n ? (100 * kk.po).toFixed(1) + '%' : 'n/a') +
          '</b>, Cohen\'s kappa <b>' + (kk.n ? kk.k.toFixed(2) : 'n/a') + '</b>. Records that changed: <b>' + dis.length + '</b>.</p>' +
          (dis.length ? '<div class="table-wrap" style="margin-top:12px"><table class="data"><tr><th>Record</th><th>Run 1</th><th>Run 2</th><th>Title</th></tr>' +
            dis.map(function (id) { return '<tr><td>' + esc(ref.sgold[id].id) + '</td><td>' + esc(run.map[id].d) + '</td><td>' + esc(run2.map[id].d) + '</td><td>' + esc(title(id)) + '</td></tr>'; }).join('') +
            '</table></div>' : '') + '</div>';
      } catch (e) { html += '<p class="status err">Run 2: ' + esc(e.message) + '</p>'; }
    }

    html += '<div class="row" style="margin-top:18px"><button class="btn btn-plain" type="button" id="s-dl">Download the comparison (CSV)</button>' +
      '<span class="hint">One row per reference record, with your reason and the reference basis, ready for the discussion.</span></div>';
    out.innerHTML = html;
    out.hidden = false;
    lastScreening = rows;
    $('s-dl').addEventListener('click', function () {
      download('screening_comparison.csv', toCSV(lastScreening, ['record_id', 'your_decision', 'counted_as', 'gold_decision', 'result', 'your_reason', 'gold_basis', 'title']));
    });
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function metric(label, value, sub, key, bad) {
    return '<div class="metric' + (key ? ' key' : '') + (bad ? ' bad' : '') + '"><div class="label">' + esc(label) + '</div><div class="value">' + esc(value) + '</div><div class="sub">' + esc(sub) + '</div></div>';
  }

  function listTable(heading, cls, ids, run, note) {
    var open = cls === 'fn' ? ' open' : '';
    if (!ids.length) return '<details class="box" style="margin-top:18px"' + open + '><summary>' + esc(heading) + ': none</summary></details>';
    return '<details class="box" style="margin-top:18px"' + open + '><summary>' + esc(heading) + ': ' + ids.length + '</summary>' +
      '<p class="hint" style="margin:8px 0 12px">' + esc(note) + '</p><div class="table-wrap"><table class="data">' +
      '<tr><th>Record</th><th>Title</th><th>Your reason</th><th>Reference basis</th></tr>' +
      ids.map(function (id) {
        var m = run.map[id];
        return '<tr><td><span class="tag ' + cls + '">' + esc(ref.sgold[id].id) + '</span></td><td>' + esc(title(id)) + '</td><td>' +
          (m ? esc(m.reason) : '<i>no decision</i>') + '</td><td>' + esc(ref.sgold[id].basis) + '</td></tr>';
      }).join('') + '</table></div></details>';
  }

  // ------------------------------------------------------------------ extraction
  var NR = /^(not reported|nr|n\/r|n\.r\.|na|n\/a|none reported|not stated|not available|-|—|)$/;
  function normValue(v) {
    var s = String(v == null ? '' : v).toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '');
    s = s.replace(/[“”«»]/g, '"').replace(/[‘’]/g, "'").replace(/\s+/g, ' ').trim().replace(/[.;,:]+$/, '');
    if (NR.test(s)) return 'not reported';
    return s;
  }
  function numbers(s) {
    var m = String(s).replace(/(\d),(\d{3})\b/g, '$1$2').match(/-?\d+(?:[.,]\d+)?/g);
    return m ? m.map(function (x) { return parseFloat(x.replace(',', '.')); }) : [];
  }
  function compareValue(gold, mine) {
    var g = normValue(gold), m = normValue(mine);
    if (g === m) return 'match';
    if (g === 'not reported' && m !== 'not reported') return 'invented';
    if (m === 'not reported' && g !== 'not reported') return 'falsenr';
    var gn = numbers(g), mn = numbers(m);
    if (gn.length && gn.length === mn.length && gn.every(function (x, i) { return Math.abs(x - mn[i]) < 1e-9; }) &&
      g.replace(/[\d.,\s%-]/g, '') === m.replace(/[\d.,\s%-]/g, '')) return 'match';
    if (gn.length && mn.length && gn.join() !== mn.join()) return 'mismatch';
    if (g.length > 2 && m.length > 2 && (g.indexOf(m) >= 0 || m.indexOf(g) >= 0)) return 'partial';
    return 'mismatch';
  }
  var LABEL = {
    match: 'match', partial: 'partial: check', mismatch: 'mismatch', missing: 'not extracted',
    falsenr: '"not reported" but it is', invented: 'value where none is reported', extra: 'not in reference'
  };

  var lastExtraction = null;

  function scoreExtraction() {
    var out = $('e-results'), msg = $('e-msg');
    msg.textContent = ''; msg.className = 'status';
    if (!ref.egold) { msg.className = 'status err'; msg.textContent = 'The reference extraction is not loaded, so nothing can be scored yet.'; return; }
    var text = $('e-text').value;
    if (!text.trim()) { msg.className = 'status err'; msg.textContent = 'Paste your extraction or choose a CSV file first.'; return; }
    var p;
    try { p = parseCSV(text); requireCols(p, ['study_id', 'field', 'value'], 'Your extraction'); }
    catch (e) { msg.className = 'status err'; msg.textContent = e.message; return; }

    var key = function (s, f) { return normId(s) + '||' + String(f).trim().toLowerCase(); };
    var mine = {};
    p.rows.forEach(function (r) { if (r.study_id && r.field) mine[key(r.study_id, r.field)] = r; });
    var goldKeys = {};
    var rows = ref.egold.map(function (g) {
      var k = key(g.study, g.field); goldKeys[k] = 1;
      var m = mine[k];
      var status = m ? compareValue(g.value, m.value) : 'missing';
      return { study_id: g.study, field: g.field, gold: g.value, gold_quote: g.quote, gold_location: g.loc,
        yours: m ? m.value : '', your_quote: m ? (m.source_quote || '') : '', your_location: m ? (m.location || '') : '',
        status: status, accepted: false };
    });
    var studiesInGold = {};
    ref.egold.forEach(function (g) { studiesInGold[normId(g.study)] = 1; });
    var extra = p.rows.filter(function (r) { return r.study_id && r.field && !goldKeys[key(r.study_id, r.field)]; });
    lastExtraction = { rows: rows, extra: extra, nMine: p.rows.length, hasQuote: p.header.indexOf('source_quote') >= 0 };
    renderExtraction();
    out.hidden = false;
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderExtraction() {
    var L = lastExtraction, rows = L.rows, out = $('e-results');
    var n = rows.length;
    var c = { match: 0, partial: 0, mismatch: 0, missing: 0, falsenr: 0, invented: 0 };
    rows.forEach(function (r) { c[r.status]++; });
    var accepted = rows.filter(function (r) { return r.status !== 'match' && r.accepted; }).length;
    var auto = c.match, reviewed = c.match + accepted;
    var withVal = rows.filter(function (r) { return r.yours && normValue(r.yours) !== 'not reported'; });
    var quoted = withVal.filter(function (r) { return r.your_quote.trim() !== ''; }).length;

    // per field
    var fields = {};
    rows.forEach(function (r) {
      var f = fields[r.field] || (fields[r.field] = { n: 0, ok: 0 });
      f.n++; if (r.status === 'match' || r.accepted) f.ok++;
    });
    var defs = {};
    (ref.form || []).forEach(function (f) { defs[String(f.field).trim()] = f.definition || ''; });

    var html = '<div class="metrics">' +
      metric('Agreement (automatic)', pct(auto, n), frac(auto, n) + ' values match exactly or numerically', true) +
      metric('After your review', pct(reviewed, n), accepted + ' partial or mismatched value(s) accepted by you') +
      metric('"Not reported" but it is', String(c.falsenr), 'retrieval failures reported as absence', false, c.falsenr > 0) +
      metric('Values with no source', String(c.invented), 'a value where the reference says not reported', false, c.invented > 0) +
      '</div>';
    html += '<div class="grid grid-2" style="margin-top:18px"><div class="card"><h3>By field</h3><div class="table-wrap"><table class="data"><tr><th>Field</th><th>Correct</th><th>%</th></tr>' +
      Object.keys(fields).map(function (f) {
        return '<tr><td><b>' + esc(f) + '</b>' + (defs[f] ? '<br><span class="hint">' + esc(defs[f]) + '</span>' : '') + '</td><td>' + frac(fields[f].ok, fields[f].n) + '</td><td>' + pct(fields[f].ok, fields[f].n) + '</td></tr>';
      }).join('') + '</table></div></div>';
    html += '<div class="card"><h3>Summary</h3><table class="data">' +
      '<tr><td>Reference values</td><td><b>' + n + '</b></td></tr>' +
      '<tr><td><span class="tag match">match</span></td><td><b>' + c.match + '</b></td></tr>' +
      '<tr><td><span class="tag partial">partial: check</span></td><td><b>' + c.partial + '</b></td></tr>' +
      '<tr><td><span class="tag mismatch">mismatch</span></td><td><b>' + c.mismatch + '</b></td></tr>' +
      '<tr><td><span class="tag missing">not extracted</span></td><td><b>' + c.missing + '</b></td></tr>' +
      '<tr><td>Your values with a verbatim quote</td><td><b>' + (L.hasQuote ? frac(quoted, withVal.length) : 'no source_quote column') + '</b></td></tr>' +
      '<tr><td>Rows not in the reference</td><td><b>' + L.extra.length + '</b></td></tr>' +
      '</table></div></div>';
    html += '<div class="callout info" style="margin-top:18px">' + ICON_INFO + '<div><p><b>The automatic comparison is only a first pass.</b> ' +
      'Free-text values can be right in other words, and numbers can match by chance. Read each partial or mismatched value against the reference quote and tick <i>Accept</i> when you judge them equivalent. That is the human check.</p></div></div>';
    html += '<div class="table-wrap" style="margin-top:18px;max-height:640px"><table class="data"><tr><th>Study</th><th>Field</th><th>Reference value</th><th>Your value</th><th>Status</th><th>Accept</th></tr>' +
      rows.map(function (r, i) {
        var canAccept = r.status !== 'match' && r.status !== 'missing';
        return '<tr><td>' + esc(r.study_id) + '</td><td>' + esc(r.field) + '</td><td>' + esc(r.gold) +
          (r.gold_quote ? '<br><span class="hint">"' + esc(r.gold_quote) + '"' + (r.gold_location ? ' (' + esc(r.gold_location) + ')' : '') + '</span>' : '') + '</td><td>' + esc(r.yours || '') +
          (r.your_quote ? '<br><span class="hint">"' + esc(r.your_quote) + '"</span>' : '') + '</td><td><span class="tag ' + r.status + '">' + LABEL[r.status] + '</span></td><td>' +
          (canAccept ? '<label><input type="checkbox" data-i="' + i + '"' + (r.accepted ? ' checked' : '') + '> <span class="visually-hidden">accept</span></label>' : '') + '</td></tr>';
      }).join('') + '</table></div>';
    if (L.extra.length) {
      html += '<details class="box" style="margin-top:18px"><summary>Rows not in the reference: ' + L.extra.length + '</summary><div class="table-wrap" style="margin-top:12px"><table class="data"><tr><th>Study</th><th>Field</th><th>Your value</th></tr>' +
        L.extra.map(function (r) { return '<tr><td>' + esc(r.study_id) + '</td><td>' + esc(r.field) + '</td><td>' + esc(r.value) + '</td></tr>'; }).join('') + '</table></div></details>';
    }
    html += '<div class="row" style="margin-top:18px"><button class="btn btn-plain" type="button" id="e-dl">Download the comparison (CSV)</button></div>';
    out.innerHTML = html;
    out.querySelectorAll('input[type=checkbox][data-i]').forEach(function (cb) {
      cb.addEventListener('change', function () { L.rows[+cb.dataset.i].accepted = cb.checked; var y = window.scrollY; renderExtraction(); window.scrollTo(0, y); });
    });
    $('e-dl').addEventListener('click', function () {
      download('extraction_comparison.csv', toCSV(L.rows, ['study_id', 'field', 'gold', 'yours', 'status', 'accepted', 'gold_quote', 'gold_location', 'your_quote', 'your_location']));
    });
  }

  // ------------------------------------------------------------------ icons
  var ICON_WARN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.5v.01"/></svg>';
  var ICON_INFO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M12 11v6M12 7.5v.01"/></svg>';

  // ------------------------------------------------------------------ wiring
  function wireFile(inputId, targetId, statusId) {
    $(inputId).addEventListener('change', function (ev) {
      readFile(ev.target).then(function (f) {
        $(targetId).value = f.text;
        if (statusId) { $(statusId).className = 'status ok'; $(statusId).textContent = 'Loaded ' + f.name; }
      }).catch(function (e) { if (statusId) { $(statusId).className = 'status err'; $(statusId).textContent = e.message; } });
    });
  }

  function wireRefOverride(inputId, ingest, statusId) {
    $(inputId).addEventListener('change', function (ev) {
      readFile(ev.target).then(function (f) {
        try { ingest(f.text, 'your file ' + f.name); setRefStatus(); $(statusId).className = 'status ok'; $(statusId).textContent = 'Using ' + f.name; }
        catch (e) { $(statusId).className = 'status err'; $(statusId).textContent = e.message; }
      });
    });
  }

  function selectTab(name) {
    ['screening', 'extraction'].forEach(function (t) {
      $('tab-' + t).setAttribute('aria-selected', String(t === name));
      $('panel-' + t).hidden = t !== name;
    });
    if (history.replaceState) history.replaceState(null, '', (location.search || '') + '#' + name);
  }

  document.addEventListener('DOMContentLoaded', function () {
    $('tab-screening').addEventListener('click', function () { selectTab('screening'); });
    $('tab-extraction').addEventListener('click', function () { selectTab('extraction'); });
    if (location.hash === '#extraction') selectTab('extraction');

    wireFile('s-file', 's-text', 's-file-status');
    wireFile('s-file2', 's-text2', 's-file2-status');
    wireFile('e-file', 'e-text', 'e-file-status');
    wireRefOverride('s-gold-file', ingestSGold, 's-gold-status');
    wireRefOverride('s-rec-file', ingestRecords, 's-rec-status');
    wireRefOverride('e-gold-file', ingestEGold, 'e-gold-status');

    $('s-go').addEventListener('click', scoreScreening);
    $('e-go').addEventListener('click', scoreExtraction);

    if (SAMPLE) {
      fetchFirst(['data/_sample/decisions_example.csv']).then(function (r) { $('s-text').value = r.text; });
      fetchFirst(['data/_sample/decisions_example_run2.csv']).then(function (r) { $('s-text2').value = r.text; });
      fetchFirst(['data/_sample/extraction_example.csv']).then(function (r) { $('e-text').value = r.text; });
    }
    loadReferences();
  });

  // exposed for tests
  window.EPHScorer = { parseCSV: parseCSV, normDecision: normDecision, compareValue: compareValue, normValue: normValue };
})();
