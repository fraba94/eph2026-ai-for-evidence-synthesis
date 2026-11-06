/* Browser scorer for the EPH 2026 workshop "AI for evidence synthesis".
   Runs entirely in the browser: files are read locally and never uploaded.

   The rules mirror activity/tools/score_screening.py and activity/tools/score_extraction.py, so the numbers
   on this page equal the Python scorers (except the quote check against the full text, which only the
   Python extraction scorer does).

   Formats:
     screening_records.csv  record_id,pmid,doi,title,abstract,year,journal,license
     screening_gold.csv     record_id,gold_decision,gold_basis
     your decisions         record_id,decision,reason        (decision: include|exclude|unsure)
     extraction_form.csv    field,definition,allowed_values,type[,core]
     extraction_gold.csv    study_id,field,value,source_quote,location[,review_table_value,notes]
     papers.csv             study_id,...  (to recognise study IDs written in another case)
     your extraction        study_id,field,value,source_quote,location
*/
(function () {
  'use strict';

  var REPO_RAW = 'https://raw.githubusercontent.com/fraba94/eph2026-ai-for-evidence-synthesis/main/';
  var SAMPLE = /[?&]sample=1\b/.test(location.search);

  function chain(local, repoPath) { return ['data/' + local, '../' + repoPath, REPO_RAW + repoPath]; }
  var SOURCES = SAMPLE ? {
    records: ['data/_sample/screening_records.csv'],
    sgold: ['data/_sample/screening_gold.csv'],
    form: ['data/_sample/extraction_form.csv'],
    egold: ['data/_sample/extraction_gold.csv'],
    papers: []
  } : {
    records: chain('screening_records.csv', 'activity/data/screening_records.csv'),
    sgold: chain('screening_gold.csv', 'activity/answers/screening_gold.csv'),
    form: chain('extraction_form.csv', 'activity/data/extraction_form.csv'),
    egold: chain('extraction_gold.csv', 'activity/answers/extraction_gold.csv'),
    papers: chain('papers.csv', 'activity/data/papers.csv')
  };

  var ref = { records: null, sgold: null, form: null, egold: null, papers: null };
  var refFrom = {};

  // ------------------------------------------------------------------ helpers
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function ratio(a, b) { return b ? a / b : NaN; }
  // One decimal, rounding exact ties to even like Python's format (56.25 -> 56.2), so both scorers print the same.
  function pct(x) {
    if (isNaN(x)) return 'n/a';
    var s = 1000 * x, f = Math.floor(s);
    var r = (s - f === 0.5) ? (f % 2 === 0 ? f : f + 1) : Math.round(s);
    return (r / 10).toFixed(1) + '%';
  }
  function stripChars(s, chars) {
    var i = 0, j = s.length;
    while (i < j && chars.indexOf(s[i]) >= 0) i++;
    while (j > i && chars.indexOf(s[j - 1]) >= 0) j--;
    return s.slice(i, j);
  }

  // ------------------------------------------------------------------ CSV (port of common.read_csv)
  function splitRows(text, d) {
    var rows = [], row = [], field = '', inQ = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (inQ) {
        if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c;
      } else if (c === '"' && field === '') inQ = true;
      else if (c === d) { row.push(field); field = ''; }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
      else field += c;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  // Tolerates a byte-order mark, ``` fences, prose before the header or after the table, ';' or tab
  // separators, Markdown tables (| a | b |) and unquoted commas in the last column (joined back), like the Python tools.
  function readCSV(text, expect) {
    text = String(text || '').replace(/﻿/g, '').replace(/\r\n?/g, '\n');
    var lines = text.split('\n').filter(function (ln) { return ln.trim().indexOf('```') !== 0; });
    expect = (expect || []).map(function (e) { return e.toLowerCase(); });
    var start = -1;
    for (var i = 0; i < lines.length; i++) {
      var low = lines[i].toLowerCase();
      if (expect.length && expect.every(function (e) { return low.indexOf(e) >= 0; })) { start = i; break; }
      if (!expect.length && lines[i].trim()) { start = i; break; }
    }
    if (start < 0) return { header: [], rows: [] };
    var hl = lines[start];
    var delim = [',', ';', '\t'].reduce(function (best, d) { return hl.split(d).length > hl.split(best).length ? d : best; }, ',');
    var body = lines.slice(start);
    if (hl.split('|').length >= 3 && hl.split('|').length > hl.split(delim).length) {
      // a Markdown table (| record_id | decision | reason |): drop the outer pipes and the |---| line
      delim = '|';
      body = body.filter(function (ln) { return !ln.trim() || !/^\s*\|?[\s:|-]+\|?\s*$/.test(ln); })
        .map(function (ln) { return ln.replace(/^\s*\|?(.*?)\|?\s*$/, '$1'); });
    }
    var rows = splitRows(body.join('\n'), delim);
    if (!rows.length) return { header: [], rows: [] };
    var header = rows[0].map(function (h) { return stripChars(h.trim(), '"').toLowerCase(); });
    while (header.length && !header[header.length - 1]) header.pop();
    var out = [];
    rows.slice(1).forEach(function (r) {
      if (!r.some(function (c) { return c.trim(); })) return;
      if (r.length === 1 && header.length > 1 && r[0].indexOf(delim) < 0) return; // prose line
      if (r.length > header.length) r = r.slice(0, header.length - 1).concat([r.slice(header.length - 1).join(delim)]);
      while (r.length < header.length) r.push('');
      var o = {};
      header.forEach(function (h, k) { if (h) o[h] = (r[k] || '').trim(); });
      out.push(o);
    });
    return { header: header, rows: out };
  }

  function toCSV(rows, cols) {
    function q(v) { v = v == null ? '' : String(v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
    return [cols.join(',')].concat(rows.map(function (r) { return cols.map(function (c) { return q(r[c]); }).join(','); })).join('\n') + '\n';
  }
  function download(name, text) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv;charset=utf-8' })); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
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

  // ------------------------------------------------------------------ text normalisation (port of common.py)
  var TRANS = {
    '‐': '-', '‑': '-', '‒': '-', '–': '-', '—': '-', '−': '-',
    '‘': "'", '’': "'", '‚': "'", '‛': "'", '′': "'",
    '“': '"', '”': '"', '„': '"', '″': '"',
    ' ': ' ', ' ': ' ', ' ': ' ', ' ': ' ', ' ': ' ', ' ': ' ',
    '·': '.', '•': '', '﻿': ''
  };
  function normText(s) {
    s = String(s || '').normalize('NFKC');
    var o = '';
    for (var i = 0; i < s.length; i++) { var c = s[i]; o += TRANS.hasOwnProperty(c) ? TRANS[c] : c; }
    return o.toLowerCase().replace(/\s+/g, ' ').trim();
  }
  var NR_EXACT = ['nr', 'n/r', 'n.r', 'na', 'n/a', 'n.a', 'missing', 'unclear', 'none', '-', '--', '?', 'unknown'];
  var NR_PREFIX = ['not reported', 'not stated', 'not mentioned', 'none reported', 'not available', 'not described',
    'not specified', 'not given', 'not provided', 'not applicable', 'no data', 'not found',
    'no information', 'information not', 'not clearly reported', 'not explicitly', 'nr ', 'nr:',
    'nr(', 'n/r ', 'na ', 'n/a '];
  function isNotReported(v) {
    v = stripChars(normText(v), ' .;:').replace(/[_*]/g, '').trim();
    return NR_EXACT.indexOf(v) >= 0 || NR_PREFIX.some(function (p) { return v.indexOf(p) === 0; });
  }
  function numbersIn(s) {
    s = normText(s);
    var re = /(?<![\d.])-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\d.])-?\d+(?:\.\d+)?/g, m, out = [];
    while ((m = re.exec(s))) {
      var t = m[0];
      if (t[0] === '-' && m.index > 0 && /[a-z0-9À-￿]/i.test(s[m.index - 1])) t = t.slice(1); // a range, not a negative number
      out.push(parseFloat(t.replace(/,/g, '')));
    }
    return out;
  }

  // ------------------------------------------------------------------ reference data
  function normId(x) {
    x = String(x || '').trim().toUpperCase();
    if (/^\d+$/.test(x)) x = 'R' + ('000' + x).slice(-Math.max(3, x.length));
    return x;
  }
  function setRefStatus() {
    var s = $('ref-status-s');
    if (ref.sgold) {
      var ids = Object.keys(ref.sgold);
      s.className = 'status ok';
      s.innerHTML = 'Reference standard loaded: <b>' + ids.length + '</b> records (' +
        ids.filter(function (k) { return ref.sgold[k].d === 'include'; }).length + ' includes)' +
        (ref.records ? ', titles available' : '') + '. <span class="muted">Source: ' + esc(refFrom.sgold) + '</span>';
    } else {
      s.className = 'status err';
      s.innerHTML = 'Reference standard not found yet. Score with the Python scorers in activity/tools/ (see the activity guide), load the reference file below under "Use another reference file", or <a href="?sample=1">try the synthetic sample</a>.';
    }
    var e = $('ref-status-e');
    if (ref.egold) {
      var studies = {}; ref.egold.forEach(function (r) { studies[r.study_id] = 1; });
      e.className = 'status ok';
      e.innerHTML = 'Reference extraction loaded: <b>' + ref.egold.length + '</b> values from <b>' + Object.keys(studies).length +
        '</b> studies (' + Object.keys(studies).map(esc).join(', ') + '). <span class="muted">Source: ' + esc(refFrom.egold) + '</span>';
    } else {
      e.className = 'status err';
      e.innerHTML = 'Reference extraction not found yet. Load it below under "Use another reference file", or <a href="?sample=1#extraction">try the synthetic sample</a>.';
    }
    $('sample-banner').hidden = !SAMPLE;
  }
  function ingestSGold(text, from) {
    var p = readCSV(text, ['record_id', 'gold_decision']);
    if (p.header.indexOf('record_id') < 0 || p.header.indexOf('gold_decision') < 0) throw new Error('Reference screening file: needs record_id,gold_decision[,gold_basis]');
    var g = {};
    p.rows.forEach(function (r) {
      if (!r.record_id) return;
      g[normId(r.record_id)] = { id: normId(r.record_id), d: (r.gold_decision || '').trim().toLowerCase(), basis: r.gold_basis || '' };
    });
    ref.sgold = g; refFrom.sgold = from;
  }
  function ingestRecords(text, from) {
    var p = readCSV(text, ['record_id', 'title']);
    if (p.header.indexOf('record_id') < 0) throw new Error('Records file: needs record_id,title');
    var m = {};
    p.rows.forEach(function (r) { m[normId(r.record_id)] = r; });
    ref.records = m; refFrom.records = from;
  }
  function ingestEGold(text, from) {
    var p = readCSV(text, ['study_id', 'field']);
    if (['study_id', 'field', 'value'].some(function (c) { return p.header.indexOf(c) < 0; })) throw new Error('Reference extraction file: needs study_id,field,value');
    ref.egold = p.rows; refFrom.egold = from;
  }
  function ingestForm(text, from) {
    var p = readCSV(text, ['field']);
    var f = {};
    p.rows.forEach(function (r) { if (r.field) f[r.field] = r; });
    ref.form = f; refFrom.form = from;
  }
  function ingestPapers(text) { ref.papers = readCSV(text, ['study_id']).rows; }

  function loadReferences() {
    function job(src, fn) { return fetchFirst(src).then(function (r) { fn(r.text, r.url); }).catch(function () {}); }
    return Promise.all([job(SOURCES.sgold, ingestSGold), job(SOURCES.records, ingestRecords), job(SOURCES.egold, ingestEGold),
      job(SOURCES.form, ingestForm), job(SOURCES.papers, ingestPapers)]).then(setRefStatus);
  }

  // ------------------------------------------------------------------ screening (port of score_screening.py)
  var SYN = {
    include: 'include', included: 'include', yes: 'include', y: 'include', in: 'include', i: 'include',
    exclude: 'exclude', excluded: 'exclude', no: 'exclude', n: 'exclude', out: 'exclude', e: 'exclude',
    unsure: 'unsure', maybe: 'unsure', uncertain: 'unsure', '?': 'unsure', u: 'unsure', unclear: 'unsure'
  };
  function loadDecisions(text) {
    var p = readCSV(text, ['record_id', 'decision']);
    if (!p.rows.length) throw new Error('No table with the columns record_id,decision[,reason] was found.');
    if (p.header.indexOf('record_id') < 0 || p.header.indexOf('decision') < 0) throw new Error('Your decisions need the columns record_id,decision[,reason]. Found: ' + p.header.join(', '));
    var out = {}, bad = [], dup = [];
    p.rows.forEach(function (r, i) {
      var rid = normId(r.record_id);
      if (!rid) return;
      var raw = stripChars((r.decision || '').trim(), "*`'\"").toLowerCase();
      var d = SYN.hasOwnProperty(raw) ? SYN[raw] : null;
      if (!d) { bad.push({ line: i + 2, id: rid, raw: raw }); return; }
      if (out[rid]) dup.push(rid);
      out[rid] = { decision: d, reason: (r.reason || '').trim() };
    });
    return { map: out, bad: bad, dup: dup };
  }
  function kappa(a, b, ids) {
    var labels = ['include', 'exclude', 'unsure'], n = ids.length;
    if (!n) return NaN;
    var po = ids.filter(function (i) { return a[i] === b[i]; }).length / n, pe = 0;
    labels.forEach(function (l) {
      pe += (ids.filter(function (i) { return a[i] === l; }).length / n) * (ids.filter(function (i) { return b[i] === l; }).length / n);
    });
    return pe < 1 ? (po - pe) / (1 - pe) : 1;
  }
  function title(id) { var r = ref.records && ref.records[id]; return r ? r.title : ''; }

  var lastScreening = null;

  function scoreScreening() {
    var out = $('s-results'), msg = $('s-msg');
    msg.textContent = ''; msg.className = 'status';
    if (!ref.sgold) { msg.className = 'status err'; msg.textContent = 'The reference standard is not loaded, so nothing can be scored yet.'; return; }
    var text = $('s-text').value;
    if (!text.trim()) { msg.className = 'status err'; msg.textContent = 'Paste your decisions or choose a CSV file first.'; return; }
    var run;
    try { run = loadDecisions(text); } catch (e) { msg.className = 'status err'; msg.textContent = e.message; return; }
    var dec = run.map, unsureAs = $('s-unsure').value, expectAll = $('s-all').checked;
    var gold = ref.sgold, gids = Object.keys(gold);

    var tp = 0, fp = 0, tn = 0, fn = 0, missed = [], falseInc = [], unsure = [], missing = [], flagged = [], rows = [];
    gids.forEach(function (rid) {
      var g = gold[rid], gd = g.d, d;
      if (!dec[rid]) {
        missing.push(rid);
        rows.push({ record_id: rid, your_decision: '(not screened)', counted_as: expectAll ? 'exclude' : '(not scored)', gold_decision: gd, result: expectAll ? (gd === 'include' ? 'missed include' : 'true exclude') : 'not screened', your_reason: '', gold_basis: g.basis, title: title(rid) });
        if (!expectAll) return;
        d = 'exclude';
      } else d = dec[rid].decision;
      if (d === 'unsure') unsure.push(rid);
      var eff = d === 'unsure' ? unsureAs : d;
      if (g.basis.indexOf('POSSIBLE GOLD-STANDARD ERROR') >= 0) flagged.push(rid);
      var res;
      if (gd === 'include' && eff === 'include') { tp++; res = 'true include'; }
      else if (gd === 'include') { fn++; missed.push(rid); res = 'missed include'; }
      else if (eff === 'include') { fp++; falseInc.push(rid); res = 'false include'; }
      else { tn++; res = 'true exclude'; }
      if (dec[rid]) rows.push({ record_id: rid, your_decision: d, counted_as: eff, gold_decision: gd, result: res, your_reason: dec[rid].reason, gold_basis: g.basis, title: title(rid) });
    });
    var unknown = Object.keys(dec).filter(function (r) { return !gold[r]; });
    var n = tp + fp + tn + fn;
    var sens = ratio(tp, tp + fn), spec = ratio(tn, tn + fp), prec = ratio(tp, tp + fp), npv = ratio(tn, tn + fn);
    var acc = ratio(tp + tn, n), f1 = ratio(2 * tp, 2 * tp + fp + fn);
    var wss = n ? ratio(tn + fn, n) - (1 - sens) : NaN;

    var nGold = gids.length, nScreened = nGold - missing.length;
    var nInc = gids.filter(function (r) { return gold[r].d === 'include'; }).length;
    var missInc = missing.filter(function (r) { return gold[r].d === 'include'; });

    var html = '';
    // coverage block (same rule and wording as score_screening.py)
    html += '<div class="callout ' + (expectAll && missInc.length ? 'danger' : (expectAll && missing.length ? 'warn' : 'info')) + '">' + (expectAll && missing.length ? ICON_WARN : ICON_INFO) + '<div>' +
      '<p><b>Screened ' + nScreened + ' of ' + nGold + ' records</b> (' + missing.length + ' not screened).' +
      (!expectAll && missing.length ? ' Expected if you screened one batch (batch 1 = R001-R020); fewer than you sent means the AI dropped or renamed records.' : '') + '</p>';
    if (missing.length) {
      html += '<p>Not screened: ' + missing.map(function (r) { return missInc.indexOf(r) >= 0 ? '<b>' + esc(r) + '</b>' : esc(r); }).join(', ') + '</p>';
      if (missInc.length) html += '<p><b>Not screened but INCLUDED in the reference: ' + missInc.map(esc).join(', ') + '</b></p>';
      html += '<p>Sensitivity counting not-screened includes as missed: <b>' + pct(ratio(tp, nInc)) + '</b> (' + tp + '/' + nInc + ')</p>';
      html += '<p class="hint">' + (expectAll ? 'Not-screened records are counted as exclude in all metrics below ("I was meant to screen all records" is ticked).' :
        'Metrics below are computed on the screened records only. Tick "I was meant to screen all records" (Going further box) to count not-screened records as exclude.') + '</p>';
    }
    html += '</div></div>';

    html += '<div class="metrics" style="margin-top:18px">' +
      metric('Sensitivity (recall)', pct(sens), tp + ' / ' + (tp + fn) + ' reference includes kept', true, fn > 0) +
      metric('Specificity', pct(spec), tn + ' / ' + (tn + fp) + ' reference excludes excluded') +
      metric('Precision', pct(prec), tp + ' / ' + (tp + fp) + ' of your includes are reference includes') +
      metric('Missed includes', String(fn), 'reference includes you excluded' + (expectAll ? ' or did not screen' : ''), false, fn > 0) +
      '</div>';

    var more = '';
    more += '<div class="grid grid-2" style="margin-top:18px">';
    more += '<div class="card"><h3>Confusion matrix</h3><table class="cm" aria-label="Confusion matrix">' +
      '<tr><th></th><th>Reference: include</th><th>Reference: exclude</th></tr>' +
      '<tr><th>You: include</th><td class="tp"><b>' + tp + '</b><span>true include</span></td><td class="fp"><b>' + fp + '</b><span>false include</span></td></tr>' +
      '<tr><th>You: exclude</th><td class="fn"><b>' + fn + '</b><span>missed include</span></td><td class="tn"><b>' + tn + '</b><span>true exclude</span></td></tr>' +
      '</table></div>';
    more += '<div class="card"><h3>All indicators</h3><table class="data">' +
      '<tr><td>Records scored</td><td><b>' + n + '</b> of ' + nGold + ' <span class="hint">(' + (expectAll ? 'all reference records, not screened = exclude' : 'records with a valid decision') + ')</span></td></tr>' +
      '<tr><td>NPV</td><td><b>' + pct(npv) + '</b></td></tr>' +
      '<tr><td>Accuracy <span class="hint">(misleading when includes are few)</span></td><td><b>' + pct(acc) + '</b></td></tr>' +
      '<tr><td>F1</td><td><b>' + pct(f1) + '</b></td></tr>' +
      '<tr><td>WSS at achieved recall</td><td><b>' + pct(wss) + '</b></td></tr>' +
      '<tr><td>WSS@95</td><td><b>' + (!isNaN(sens) && sens >= 0.95 ? pct(ratio(tn + fn, n) - 0.05) : 'not applicable') + '</b>' + (!isNaN(sens) && sens >= 0.95 ? '' : ' <span class="hint">(recall below 95%)</span>') + '</td></tr>' +
      '<tr><td>Unsure</td><td><b>' + unsure.length + '</b> (counted as ' + unsureAs + ')</td></tr>' +
      '<tr><td>IDs not in the reference</td><td><b>' + unknown.length + '</b></td></tr>' +
      '</table></div></div>';

    // title/abstract-stage view
    var ft = gids.filter(function (r) { return gold[r].basis.indexOf('full-text assessment') >= 0; });
    if (ft.length) {
      var t2 = 0, f2 = 0, n2 = 0, m2 = 0;
      gids.forEach(function (rid) {
        if (!dec[rid] && !expectAll) return;
        var dd = dec[rid] ? dec[rid].decision : 'exclude';
        var eff = dd === 'unsure' ? unsureAs : dd;
        var ta = (gold[rid].d === 'include' || ft.indexOf(rid) >= 0) ? 'include' : 'exclude';
        if (ta === 'include' && eff === 'include') t2++; else if (ta === 'include') m2++; else if (eff === 'include') f2++; else n2++;
      });
      more += '<div class="card" style="margin-top:18px"><h3>Title/abstract-stage view</h3><p>' + ft.length +
        ' records were excluded by the review only after reading the full text, so they passed its title/abstract stage. Counting them as "include" gives a fairer picture of title/abstract screening:</p>' +
        '<table class="data" style="margin-top:10px"><tr><td>Sensitivity (stage view)</td><td><b>' + pct(ratio(t2, t2 + m2)) + '</b> (' + t2 + '/' + (t2 + m2) + ')</td></tr>' +
        '<tr><td>Specificity (stage view)</td><td><b>' + pct(ratio(n2, n2 + f2)) + '</b> (' + n2 + '/' + (n2 + f2) + ')</td></tr>' +
        '<tr><td>Precision (stage view)</td><td><b>' + pct(ratio(t2, t2 + f2)) + '</b></td></tr></table></div>';
    }

    var probs = [];
    if (unknown.length) probs.push('<b>' + unknown.length + ' record_id(s) not in the reference</b> (ignored): ' + unknown.map(esc).join(', ') + '. Check for typos or invented IDs.');
    if (run.bad.length) probs.push('<b>Invalid decisions</b> (ignored): ' + run.bad.map(function (x) { return 'line ' + x.line + ' ' + esc(x.id) + " '" + esc(x.raw) + "'"; }).join('; ') + '.');
    if (run.dup.length) probs.push('<b>Duplicated record_id</b> (last one kept): ' + run.dup.map(esc).join(', ') + '.');
    if (probs.length) html += '<div class="callout warn" style="margin-top:18px">' + ICON_WARN + '<div>' + probs.map(function (w) { return '<p>' + w + '</p>'; }).join('') + '</div></div>';

    html += '<div class="card errors-card" id="look-at-the-errors" style="margin-top:18px"><h3>Step 2 · Look at the errors</h3>' +
      '<p>Open two of the records below: read the title and the abstract (PubMed link), then decide yourself why the AI got them wrong. ' +
      'Which criterion did it use, and was it right to? A missed include is the costly error at this stage; a false include that the review excluded only after reading the full text (see the reference basis) is not an error at title/abstract stage. ' +
      'The <a href="answers.html">reference answers</a> give the basis of every reference decision.</p>' +
      (missed.length || falseInc.length ? '' : '<p><b>No missed or false includes in the records you screened.</b> Look at the unsure decisions and at the reasons instead: are they what the abstract says?</p>');
    html += listTable('Missed includes: check these first', 'fn', missed, dec, true);
    html += listTable('False includes', 'fp', falseInc, dec, true);
    more += listTable('Unsure (counted as ' + unsureAs + ')', 'partial', unsure, dec, false);
    if (flagged.length) html += listTable('Possible errors in the reference standard', 'extra', flagged, dec, false,
      'These records were not included by the reference review although they appear to meet its criteria. A "false include" here may be a correct decision: discuss before blaming the AI.');
    html += '</div>';

    // reproducibility
    var t2txt = $('s-text2').value;
    if (t2txt.trim()) {
      try {
        var r2 = loadDecisions(t2txt).map;
        var ids = gids.filter(function (r) { return dec[r] && r2[r]; });
        var d1 = {}, d2 = {};
        ids.forEach(function (r) { d1[r] = dec[r].decision; d2[r] = r2[r].decision; });
        var diff = ids.filter(function (r) { return d1[r] !== d2[r]; });
        var k = kappa(d1, d2, ids);
        html += '<div class="card" style="margin-top:18px"><h3>Reproducibility: run 1 versus run 2</h3>' +
          '<p>Records in both runs: <b>' + ids.length + '</b>. Agreement: <b>' + (ids.length - diff.length) + '/' + ids.length + '</b> (' + pct(ratio(ids.length - diff.length, ids.length)) +
          '). Cohen\'s kappa: <b>' + (isNaN(k) ? 'n/a' : k.toFixed(2)) + '</b>.</p>' +
          (diff.length ? '<div class="table-wrap" style="margin-top:12px"><table class="data"><tr><th>Record</th><th>Title</th><th>Run 1</th><th>Run 2</th><th>Reference</th></tr>' +
            diff.map(function (r) { return '<tr><td>' + esc(r) + '</td><td>' + esc(title(r)) + '</td><td>' + d1[r] + '</td><td>' + d2[r] + '</td><td>' + esc(gold[r].d) + '</td></tr>'; }).join('') +
            '</table></div>' : '') + '</div>';
      } catch (e) { html += '<p class="status err">Run 2: ' + esc(e.message) + '</p>'; }
    }
    html += '<details class="box" style="margin-top:18px"><summary>Going further: all indicators, the title/abstract-stage view, unsure decisions</summary>' + more + '</details>';

    html += '<p class="hint" style="margin-top:18px">Interpretation: at title/abstract stage a missed include is far more costly than a false include. The reference is the review\'s final inclusion (after full text), so records it excluded at full text are legitimate includes at this stage: read the "reference basis" before calling a false include an error.</p>';
    html += '<div class="row" style="margin-top:12px"><button class="btn btn-plain" type="button" id="s-dl">Download the comparison (CSV)</button>' +
      '<span class="hint">One row per reference record, with your reason and the reference basis.</span></div>';
    out.innerHTML = html; out.hidden = false;
    lastScreening = rows;
    $('s-dl').addEventListener('click', function () {
      download('screening_comparison.csv', toCSV(lastScreening, ['record_id', 'your_decision', 'counted_as', 'gold_decision', 'result', 'your_reason', 'gold_basis', 'title']));
    });
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function metric(label, value, sub, key, bad) {
    return '<div class="metric' + (key ? ' key' : '') + (bad ? ' bad' : '') + '"><div class="label">' + esc(label) + '</div><div class="value">' + esc(value) + '</div><div class="sub">' + esc(sub) + '</div></div>';
  }
  function listTable(heading, cls, ids, dec, open, note) {
    if (!ids.length) return '';
    return '<details class="box" style="margin-top:18px"' + (open ? ' open' : '') + '><summary>' + esc(heading) + ': ' + ids.length + '</summary>' +
      (note ? '<p class="hint" style="margin:8px 0 0">' + esc(note) + '</p>' : '') +
      '<div class="table-wrap" style="margin-top:12px"><table class="data"><tr><th>Record</th><th>Title</th><th>Decision</th><th>Your reason</th><th>Reference basis</th></tr>' +
      ids.map(function (id) {
        var m = dec[id];
        var rec = ref.records && ref.records[id], pm = rec && rec.pmid ? String(rec.pmid).trim() : '';
        return '<tr><td><span class="tag ' + cls + '">' + esc(id) + '</span></td><td>' + esc(title(id)) +
          (pm ? '<br><a href="https://pubmed.ncbi.nlm.nih.gov/' + encodeURIComponent(pm) + '/" target="_blank" rel="noopener">Read the abstract on PubMed</a>' : '') +
          '</td><td>' + (m ? esc(m.decision) : '<i>not screened</i>') +
          '</td><td>' + (m ? esc(m.reason) : '') + '</td><td>' + esc(ref.sgold[id].basis) + '</td></tr>';
      }).join('') + '</table></div></details>';
  }

  // ------------------------------------------------------------------ extraction (port of score_extraction.py)
  var STOP = 'a an the and or of in on at to for with by from as is are was were be per vs versus its their this that other others e g eg i ie'.split(' ');
  var SYNONYMS = {
    'favorable': 'favourable', 'positive': 'favourable', 'beneficial': 'favourable', 'reduction': 'favourable',
    'uncontrolled before after': 'uncontrolled before-after', 'before after': 'uncontrolled before-after',
    'pre post': 'uncontrolled before-after', 'pre-post': 'uncontrolled before-after', 'before-after': 'uncontrolled before-after',
    'its': 'interrupted time series', 'cba': 'controlled before-after',
    'hospital wide': 'hospital-wide', 'multiward': 'multi-ward', 'multi ward': 'multi-ward',
    'pre-intervention': 'pre-intervention period', 'baseline': 'pre-intervention period',
    'y': 'yes', 'n': 'no', 'true': 'yes', 'false': 'no'
  };
  function canon(v) {
    v = stripChars(normText(v), ' .;').replace(/_/g, ' ');
    return SYNONYMS.hasOwnProperty(v) ? SYNONYMS[v] : v;
  }
  function tokens(v) {
    var s = {};
    normText(v).replace(/[^a-z0-9.%]+/g, ' ').split(' ').forEach(function (t) { if (t && STOP.indexOf(t) < 0 && t.length > 1) s[t] = 1; });
    return s;
  }
  var RANK = { 'exact': 4, 'within tol.': 3, 'text match': 2, 'partial': 1, 'mismatch': 0 };
  function compare(value, gold, ftype, tol) {
    if (!String(value).trim()) return 'missing';
    var alts = String(gold).split(/\s+OR\s+/).map(function (x) { return x.trim(); }).filter(Boolean);
    var gNR = alts.every(isNotReported), vNR = isNotReported(value);
    if (gNR && vNR) return 'exact';
    if (gNR) return 'unsupported';
    if (vNR) return 'false absent';
    var best = 'mismatch';
    alts.forEach(function (g) {
      var cat;
      if (ftype === 'numeric' || ftype === 'proportion') {
        var gv = numbersIn(g), vv = numbersIn(value);
        if (!gv.length || !vv.length) cat = canon(g) === canon(value) ? 'exact' : 'mismatch';
        else {
          var a = gv[0], b = vv[0];
          if (ftype === 'proportion') { if (a > 1 && b <= 1) b *= 100; else if (a <= 1 && b > 1) a *= 100; }
          if (Math.abs(a - b) < 1e-9) cat = 'exact';
          else if (Math.abs(a - b) <= Math.max(tol * Math.abs(a), 0.01)) cat = 'within tol.';
          else cat = 'mismatch';
        }
      } else if (ftype === 'categorical') {
        var cv = canon(value), cg = canon(g);
        cat = cv === cg ? 'exact' : ((cv.indexOf(cg) >= 0 || cg.indexOf(cv) >= 0) ? 'partial' : 'mismatch');
      } else {
        if (canon(value) === canon(g)) cat = 'exact';
        else {
          var tv = tokens(value), tg = tokens(g), inter = 0, uni = {};
          Object.keys(tv).forEach(function (t) { uni[t] = 1; if (tg[t]) inter++; });
          Object.keys(tg).forEach(function (t) { uni[t] = 1; });
          var nu = Object.keys(uni).length, ng = Object.keys(tg).length;
          var j = nu ? inter / nu : 0, cover = ng ? inter / ng : 0;
          cat = (j >= 0.5 || cover >= 0.7) ? 'text match' : ((j >= 0.15 || cover >= 0.3) ? 'partial' : 'mismatch');
        }
      }
      if (RANK[cat] > RANK[best]) best = cat;
    });
    return best;
  }
  var ORDER = ['exact', 'within tol.', 'text match', 'partial', 'mismatch', 'missing', 'false absent', 'unsupported'];
  var AGREE = ['exact', 'within tol.', 'text match'];
  var TAGCLS = { 'exact': 'match', 'within tol.': 'match', 'text match': 'match', 'partial': 'partial', 'mismatch': 'mismatch',
    'missing': 'missing', 'false absent': 'falsenr', 'unsupported': 'invented' };

  var lastExtraction = null;
  // the short extraction of step 3 (the same five fields as SHORT_FIELDS in docs/build_pages.py)
  var SHORT_FIELDS = ['country', 'study_design', 'intervention_components', 'primary_hai_outcome', 'direction_of_effect'];
  var SCOPE_LABEL = { short: 'the 5 fields of the short extraction', core: 'the 11 core fields', all: 'all fields', mine: 'only the fields in your file' };

  function scoreExtraction() {
    var out = $('e-results'), msg = $('e-msg');
    msg.textContent = ''; msg.className = 'status';
    if (!ref.egold) { msg.className = 'status err'; msg.textContent = 'The reference extraction is not loaded, so nothing can be scored yet.'; return; }
    var text = $('e-text').value;
    if (!text.trim()) { msg.className = 'status err'; msg.textContent = 'Paste your extraction or choose a CSV file first.'; return; }
    var p = readCSV(text, ['study_id', 'field']);
    if (!p.rows.length || ['study_id', 'field', 'value'].some(function (c) { return p.header.indexOf(c) < 0; })) {
      msg.className = 'status err'; msg.textContent = 'Your extraction needs the columns study_id,field,value[,source_quote][,location].'; return;
    }
    var form = ref.form || {}, scope = $('e-fields') ? $('e-fields').value : 'all';
    var coreOnly = scope === 'core';
    var canonSid = {};
    ref.egold.forEach(function (g) { canonSid[g.study_id.toLowerCase()] = g.study_id; });
    (ref.papers || []).forEach(function (q) { if (q.study_id) canonSid[q.study_id.toLowerCase()] = q.study_id; });
    function fkey(x) { return stripChars(String(x || '').trim(), '`*').toLowerCase().replace(/[\s-]+/g, '_'); }

    var mine = {}, unknownFields = {}, dups = [];
    p.rows.forEach(function (r) {
      var sid = stripChars((r.study_id || '').trim(), '`*');
      sid = canonSid[sid.toLowerCase()] || sid;
      var f = fkey(r.field);
      if (!sid || !f) return;
      if (ref.form && !form[f]) unknownFields[f] = 1;
      if (mine[sid + '||' + f]) dups.push(sid + '/' + f);
      r.study_id = sid; r.field = f;
      mine[sid + '||' + f] = r;
    });
    var studies = Object.keys(mine).map(function (k) { return k.split('||')[0]; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
    var known = {}; ref.egold.forEach(function (g) { known[g.study_id] = 1; });
    var missingStudies = studies.filter(function (s) { return !known[s]; });

    var results = [];
    ref.egold.forEach(function (g) {
      if (studies.indexOf(g.study_id) < 0) return;
      var f = form[g.field] || {};
      if (coreOnly && (f.core || 'yes') !== 'yes') return;
      if (scope === 'short' && SHORT_FIELDS.indexOf(g.field) < 0) return;
      if (scope === 'mine' && !mine[g.study_id + '||' + g.field]) return;
      var r = mine[g.study_id + '||' + g.field];
      var val = r ? (r.value || '') : '';
      var cat = r ? compare(val, g.value, f.type || 'text', 0.02) : 'missing';
      results.push({ g: g, r: r, cat: cat, accepted: false });
    });
    var extra = Object.keys(mine).filter(function (k) {
      var sid = k.split('||')[0], f = k.split('||')[1];
      return studies.indexOf(sid) >= 0 && !ref.egold.some(function (g) { return g.study_id === sid && g.field === f; });
    });
    lastExtraction = { results: results, studies: studies.filter(function (s) { return known[s]; }), missingStudies: missingStudies,
      unknownFields: Object.keys(unknownFields).sort(), dups: dups, extra: extra.length, hasQuote: p.header.indexOf('source_quote') >= 0, scope: scope };
    renderExtraction();
    out.hidden = false;
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function renderExtraction() {
    var L = lastExtraction, res = L.results, out = $('e-results'), form = ref.form || {};
    var cats = {}; ORDER.forEach(function (c) { cats[c] = 0; });
    res.forEach(function (x) { cats[x.cat]++; });
    var agree = cats['exact'] + cats['within tol.'] + cats['text match'];
    var attempted = res.length - cats['missing'];
    var accepted = res.filter(function (x) { return AGREE.indexOf(x.cat) < 0 && x.cat !== 'missing' && x.accepted; }).length;
    var withVal = res.filter(function (x) { return x.r && (x.r.value || '').trim() && !isNotReported(x.r.value); });
    var quoted = withVal.filter(function (x) { return (x.r.source_quote || '').trim(); }).length;

    var html = '';
    if (!L.studies.length) {
      html += '<div class="callout danger">' + ICON_WARN + '<div><p><b>No study in your file matches the reference.</b> Reference studies: ' +
        Object.keys(ref.egold.reduce(function (o, g) { o[g.study_id] = 1; return o; }, {})).map(esc).join(', ') + '.</p></div></div>';
    }
    html += '<p class="status">Studies scored: <b>' + (L.studies.map(esc).join(', ') || 'none') + '</b>' + ' · ' + (SCOPE_LABEL[L.scope] || 'all fields') + '.</p>';
    html += '<div class="metrics" style="margin-top:12px">' +
      metric('Agreement', agree + ' / ' + res.length, 'exact + within tolerance + text match (' + pct(ratio(agree, res.length)) + ')', true) +
      metric('Among fields you extracted', agree + ' / ' + attempted, pct(ratio(agree, attempted)) + (accepted ? '; after your review: ' + (agree + accepted) + ' / ' + attempted : '')) +
      metric('False absent', String(cats['false absent']), '"not reported" but the paper reports it', false, cats['false absent'] > 0) +
      metric('Unsupported', String(cats['unsupported']), 'a value where the reference says not reported', false, cats['unsupported'] > 0) +
      '</div>';

    html += '<div class="grid grid-2" style="margin-top:18px"><div class="card"><h3>Agreement with the reference</h3><table class="data">' +
      ORDER.filter(function (c) { return cats[c]; }).map(function (c) { return '<tr><td><span class="tag ' + TAGCLS[c] + '">' + c + '</span></td><td><b>' + cats[c] + '</b></td></tr>'; }).join('') +
      '<tr><td>Your values with a quote <span class="hint">(not checked against the paper)</span></td><td><b>' + (L.hasQuote ? quoted + ' / ' + withVal.length : 'no source_quote column') + '</b></td></tr>' +
      '</table><p class="hint" style="margin-top:10px">The Python scorer (<code>activity/tools/score_extraction.py</code>) also checks every quote against the full text of the paper.</p></div>';
    var perField = {};
    res.forEach(function (x) {
      var pf = perField[x.g.field] || (perField[x.g.field] = { n: 0, ok: 0 });
      pf.n++; if (AGREE.indexOf(x.cat) >= 0 || x.accepted) pf.ok++;
    });
    var fieldOrder = Object.keys(form).filter(function (f) { return perField[f]; }).concat(Object.keys(perField).filter(function (f) { return !form[f]; }));
    html += '<div class="card"><h3>By field</h3><div class="table-wrap"><table class="data"><tr><th>Field</th><th>Type</th><th>Agree</th></tr>' +
      fieldOrder.map(function (f) {
        return '<tr><td><b>' + esc(f) + '</b>' + (form[f] && form[f].core === 'yes' ? ' <span class="tag match">core</span>' : '') + '</td><td>' + esc((form[f] || {}).type || '') + '</td><td>' + perField[f].ok + ' / ' + perField[f].n + '</td></tr>';
      }).join('') + '</table></div></div></div>';

    html += '<div class="callout info" style="margin-top:18px">' + ICON_INFO + '<div><p><b>The automatic comparison is a first pass.</b> ' +
      'Free text can be right in other words, and numbers can match by chance. Read each partial or mismatched value against the reference value and its notes, and tick <i>Accept</i> when you judge them equivalent. That is the human check.</p></div></div>';
    html += '<div class="table-wrap" style="margin-top:18px;max-height:720px"><table class="data"><tr><th>Study</th><th>Field</th><th>Your value</th><th>Reference value</th><th>Agreement</th><th>Accept</th></tr>' +
      res.map(function (x, i) {
        var g = x.g, r = x.r || {};
        var canAccept = AGREE.indexOf(x.cat) < 0 && x.cat !== 'missing';
        return '<tr><td>' + esc(g.study_id) + '</td><td>' + esc(g.field) + '</td><td>' + esc(r.value || '') +
          (r.source_quote ? '<br><span class="hint">"' + esc(r.source_quote) + '"</span>' : '') + '</td><td>' + esc(g.value) +
          (g.source_quote ? '<br><span class="hint">"' + esc(g.source_quote) + '"' + (g.location ? ' (' + esc(g.location) + ')' : '') + '</span>' : '') +
          (g.review_table_value ? '<br><span class="hint">Review table: ' + esc(g.review_table_value) + '</span>' : '') +
          (g.notes ? '<br><span class="hint">Note: ' + esc(g.notes) + '</span>' : '') +
          '</td><td><span class="tag ' + TAGCLS[x.cat] + '">' + x.cat + '</span></td><td>' +
          (canAccept ? '<label><input type="checkbox" data-i="' + i + '"' + (x.accepted ? ' checked' : '') + '> <span class="visually-hidden">accept</span></label>' : '') + '</td></tr>';
      }).join('') + '</table></div>';

    var issues = [];
    if (L.missingStudies.length) issues.push('study_id not in the reference: ' + L.missingStudies.map(esc).join(', '));
    if (L.unknownFields.length) issues.push('fields not in the form: ' + L.unknownFields.map(esc).join(', '));
    if (L.extra) issues.push(L.extra + ' row(s) without a reference value (not scored)');
    if (L.dups.length) issues.push('duplicated study/field rows (last kept): ' + L.dups.map(esc).join(', '));
    if (issues.length) html += '<div class="callout warn" style="margin-top:18px">' + ICON_WARN + '<div>' + issues.map(function (s) { return '<p>' + s + '</p>'; }).join('') + '</div></div>';
    html += '<p class="hint" style="margin-top:18px">How to read this: "unsupported" means a value where the paper reports nothing, the typical sign of inference or hallucination. "False absent" means the information was there but was reported as missing (often a retrieval or parsing failure, e.g. a table). Check the notes: several reference values are themselves ambiguous because the papers contradict themselves, and the review table sometimes differs from the paper.</p>';
    html += '<div class="row" style="margin-top:12px"><button class="btn btn-plain" type="button" id="e-dl">Download the comparison (CSV)</button></div>';
    out.innerHTML = html;
    out.querySelectorAll('input[type=checkbox][data-i]').forEach(function (cb) {
      cb.addEventListener('change', function () { L.results[+cb.dataset.i].accepted = cb.checked; var y = window.scrollY; renderExtraction(); window.scrollTo(0, y); });
    });
    $('e-dl').addEventListener('click', function () {
      download('extraction_comparison.csv', toCSV(L.results.map(function (x) {
        return { study_id: x.g.study_id, field: x.g.field, your_value: (x.r || {}).value || '', reference_value: x.g.value, agreement: x.cat,
          accepted_by_you: x.accepted ? 'yes' : '', your_quote: (x.r || {}).source_quote || '', reference_quote: x.g.source_quote || '', review_table_value: x.g.review_table_value || '', notes: x.g.notes || '' };
      }), ['study_id', 'field', 'your_value', 'reference_value', 'agreement', 'accepted_by_you', 'your_quote', 'reference_quote', 'review_table_value', 'notes']));
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
        $(statusId).className = 'status ok'; $(statusId).textContent = 'Loaded ' + f.name;
      }).catch(function (e) { $(statusId).className = 'status err'; $(statusId).textContent = e.message; });
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

  window.EPHScorer = { readCSV: readCSV, compare: compare, isNotReported: isNotReported, numbersIn: numbersIn, normText: normText, normId: normId };
})();
