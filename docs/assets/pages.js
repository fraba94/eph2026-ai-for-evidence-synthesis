/* EPH 2026 · AI for evidence synthesis · small helpers for the generated pages and the start page.
   - Copy buttons on code blocks (one click copies the prompt) and on [data-copy] buttons.
   - Task-list checkboxes remember their state in this browser (localStorage, nothing is sent anywhere).
   - On the day of the session, the start page marks the block that is happening now (Bilbao time).
   No external scripts. */
(function () {
  'use strict';

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { return fallback(text); });
    }
    return fallback(text);
  }
  function fallback(text) {
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.top = '-1000px'; ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? resolve() : reject(new Error('copy failed')); }
      catch (e) { reject(e); }
      document.body.removeChild(ta);
    });
  }
  function flash(btn, ok) {
    var span = btn.querySelector('span') || btn;
    var label = btn.getAttribute('data-label') || span.textContent;
    btn.setAttribute('data-label', label);
    span.textContent = ok ? 'Copied' : 'Select and copy by hand';
    btn.classList.toggle('copied', ok);
    clearTimeout(btn._t);
    btn._t = setTimeout(function () { span.textContent = label; btn.classList.remove('copied'); }, 2200);
  }

  // code blocks generated from Markdown
  document.querySelectorAll('.codeblock').forEach(function (block) {
    var btn = block.querySelector('button.copy');
    var code = block.querySelector('pre code');
    if (!btn || !code) return;
    btn.addEventListener('click', function () {
      copyText(code.textContent).then(function () { flash(btn, true); }, function () { flash(btn, false); });
    });
  });

  // buttons that copy the text of another element: <button data-copy="#id">
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector(btn.getAttribute('data-copy'));
      if (!el) return;
      copyText(el.textContent).then(function () { flash(btn, true); }, function () { flash(btn, false); });
    });
  });

  // task lists: remember ticks in this browser only
  var boxes = document.querySelectorAll('input.task-box');
  boxes.forEach(function (box, i) {
    var key = 'eph2026:' + location.pathname + ':task:' + i;
    try { var v = localStorage.getItem(key); if (v !== null) box.checked = v === '1'; } catch (e) { /* storage blocked */ }
    box.addEventListener('change', function () {
      try { localStorage.setItem(key, box.checked ? '1' : '0'); } catch (e) { /* storage blocked */ }
    });
  });

  // start page: highlight the block that is happening now, on the day of the session (Europe/Madrid)
  var slots = document.querySelectorAll('[data-slot]');
  if (slots.length && window.Intl) {
    var mark = function () {
      var parts;
      try {
        parts = new Intl.DateTimeFormat('en-CA', { timeZone: 'Europe/Madrid', year: 'numeric', month: '2-digit', day: '2-digit',
          hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(new Date());
      } catch (e) { return; }
      var p = {};
      parts.forEach(function (x) { p[x.type] = x.value; });
      var today = p.year + '-' + p.month + '-' + p.day;
      var now = (+p.hour) * 60 + (+p.minute);
      slots.forEach(function (el) {
        var day = el.getAttribute('data-day');
        var se = el.getAttribute('data-slot').split('-');
        var toMin = function (t) { var a = t.split(':'); return (+a[0]) * 60 + (+a[1]); };
        var on = day === today && now >= toMin(se[0]) && now < toMin(se[1]);
        el.classList.toggle('now', on);
        var badge = el.querySelector('.now-badge');
        if (badge) badge.hidden = !on;
      });
    };
    mark();
    setInterval(mark, 30000);
  }
})();
