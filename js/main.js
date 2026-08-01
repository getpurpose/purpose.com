/* ==========================================================================
   Purpose Education — site scripts
   Loaded on every page with `defer`. Every module guards its own DOM, so a
   page that lacks a feature simply skips it.
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------------------
     MOTION SWITCH
     'rich'       — parallax, subject marquee, sequenced scroll scenes
     'restrained' — layout and interaction only
     ---------------------------------------------------------------------- */
  var MOTION = 'rich';

  var root = document.documentElement;
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rich = MOTION === 'rich' && !prefersReduced;
  root.setAttribute('data-motion', rich ? 'rich' : 'restrained');

  function each(list, fn) { Array.prototype.forEach.call(list, fn); }

  /* ---------------------------------------------------------------- nav --- */
  (function nav() {
    var burger = document.getElementById('burger');
    var menu = document.getElementById('nav');

    if (burger && menu) {
      burger.addEventListener('click', function () {
        var open = menu.classList.toggle('open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      menu.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') {
          menu.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
        }
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && menu.classList.contains('open')) {
          menu.classList.remove('open');
          burger.setAttribute('aria-expanded', 'false');
          burger.focus();
        }
      });
    }

    /* dropdown — hover on pointer devices, click everywhere */
    each(document.querySelectorAll('.nav-drop'), function (drop) {
      var trigger = drop.querySelector('button');
      if (!trigger) return;
      var desktop = window.matchMedia('(hover: hover) and (min-width: 1041px)');

      function setOpen(state) {
        drop.classList.toggle('open', state);
        trigger.setAttribute('aria-expanded', state ? 'true' : 'false');
      }
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        setOpen(!drop.classList.contains('open'));
      });
      drop.addEventListener('mouseenter', function () { if (desktop.matches) setOpen(true); });
      drop.addEventListener('mouseleave', function () { if (desktop.matches) setOpen(false); });
      document.addEventListener('click', function (e) {
        if (!drop.contains(e.target)) setOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') setOpen(false);
      });
    });
  })();

  /* ------------------------------------------------------------ reveals --- */
  (function reveals() {
    var els = document.querySelectorAll('.rv');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      each(els, function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });
    each(els, function (el) { io.observe(el); });
  })();

  /* -------------------------------------------------- framework sequence --- */
  (function framework() {
    var steps = document.getElementById('steps');
    if (!steps) return;
    if (!('IntersectionObserver' in window)) {
      steps.classList.add('in');
      each(steps.querySelectorAll('.step'), function (s) { s.classList.add('lit'); });
      return;
    }
    var items = steps.querySelectorAll('.step');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        steps.classList.add('in');
        each(items, function (item, i) {
          window.setTimeout(function () { item.classList.add('lit'); }, rich ? i * 230 : 0);
        });
        io.disconnect();
      });
    }, { threshold: 0.28 });
    io.observe(steps);
  })();

  /* ----------------------------------------------------------- venn draw --- */
  (function venn() {
    var svg = document.getElementById('venn');
    if (!svg) return;
    if (!('IntersectionObserver' in window)) { svg.classList.add('in'); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { svg.classList.add('in'); io.disconnect(); }
      });
    }, { threshold: 0.3 });
    io.observe(svg);
  })();

  /* ------------------------------------------- scroll progress + parallax --- */
  (function scrollFx() {
    var bar = document.getElementById('progress');
    var layers = Array.prototype.slice.call(document.querySelectorAll('[data-par]'));
    if (!bar && !layers.length) return;
    var ticking = false;

    function frame() {
      if (bar) {
        var y = window.pageYOffset;
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
      }
      if (rich) {
        var vh = window.innerHeight;
        layers.forEach(function (el) {
          var factor = parseFloat(el.getAttribute('data-par')) || 0;
          var rect = el.getBoundingClientRect();
          var offset = (rect.top + rect.height / 2 - vh / 2) * factor;
          el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0)';
        });
      }
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(frame); }
    }, { passive: true });
    window.addEventListener('resize', frame, { passive: true });
    frame();
  })();

  /* ------------------------------------------------------- testimonials --- */
  (function testimonials() {
    each(document.querySelectorAll('.tst-toggle'), function (btn) {
      btn.addEventListener('click', function () {
        var cardEl = btn.parentNode;
        while (cardEl && cardEl.className.indexOf('tst') === -1) cardEl = cardEl.parentNode;
        if (!cardEl) return;
        var open = cardEl.classList.toggle('open');
        btn.textContent = open ? 'Read less' : 'Read more';
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  })();

  /* -------------------------------------------------------------- finder --- */
  (function finder() {
    var card = document.querySelector('.finder-card');
    if (!card) return;

    var stepEls = card.querySelectorAll('.f-step');
    var pips = card.querySelectorAll('.f-progress i');
    var LAST = stepEls.length - 1;
    var answers = {};
    var current = 0;

    var GRADE = {
      prek2: 'PreK\u2013Grade 2',
      g35: 'Grades 3\u20135',
      g68: 'Grades 6\u20138',
      g912: 'Grades 9\u201312'
    };
    var NEED = {
      literacy: 'reading and writing',
      math: 'math',
      habits: 'homework and study skills',
      ahead: 'enrichment and next-grade preparation',
      college: 'college planning'
    };

    /* Which program we would suggest for this grade + need. The parent can
       still choose either — this only sets the "Recommended" flag on step 3. */
    function suggested(a) {
      if (a.need === 'college') return 'solo';
      if (a.grade === 'prek2') return 'solo';
      if (a.need === 'habits' || a.need === 'ahead') return 'group';
      return 'solo';
    }

    var PROGRAM = {
      solo: {
        name: 'One-on-One Tutoring',
        href: 'tutoring.html',
        price: '$85/hour',
        list: [
          'Customized instruction tailored to your student\u2019s learning style, pace and goals',
          'Every session guided by The Purpose Plan',
          'Targeted intervention where the assessment identifies it'
        ],
        alt: 'Would your student do better alongside peers? See <a href="purpose-pods.html">Purpose Pods</a>.'
      },
      group: {
        name: 'Purpose Pods',
        href: 'purpose-pods.html',
        price: 'Starting at $55/hour per student',
        list: [
          '2\u20133 students matched by grade level, subject and learning goals',
          'Individualized instruction with collaboration and peer encouragement',
          'Personalized support at a shared investment'
        ],
        alt: 'Prefer undivided attention? See <a href="tutoring.html">One-on-One Tutoring</a>.'
      },
      unsure: {
        name: 'The Purpose Plan',
        href: 'purpose-plan.html',
        price: 'Customized pricing',
        list: [
          'A personalized educational roadmap',
          'Built around strengths, goals and learning needs',
          'Sets the right format before instruction begins'
        ],
        alt: 'From there, families choose <a href="tutoring.html">One-on-One Tutoring</a> or <a href="purpose-pods.html">Purpose Pods</a>.'
      }
    };

    /* Step 2 — hide options that do not apply to the grade chosen. */
    function filterNeeds() {
      var grade = answers.grade;
      each(card.querySelectorAll('[data-step="1"] .f-opt'), function (opt) {
        var allowed = (opt.getAttribute('data-grades') || 'all').split(/\s+/);
        if (allowed.indexOf('all') > -1 || allowed.indexOf(grade) > -1) {
          opt.removeAttribute('hidden');
        } else {
          opt.setAttribute('hidden', '');
        }
      });
    }

    /* Step 3 — flag the suggested program. */
    function flagPrograms() {
      var pick = suggested(answers);
      each(card.querySelectorAll('[data-step="2"] .prog-card'), function (pc) {
        pc.classList.toggle('rec', pc.getAttribute('data-v') === pick);
      });
    }

    function render() {
      var key = answers.program === 'unsure' ? 'unsure'
        : (answers.program || suggested(answers));
      var rec = PROGRAM[key] || PROGRAM.unsure;

      var why = 'For a student in ' + (GRADE[answers.grade] || 'your grade range') +
        ' who needs help with ' + (NEED[answers.need] || 'their studies') +
        ', we would begin here. Every student starts with The Purpose Plan, so the ' +
        'instruction fits the assessment rather than the other way round.';

      card.querySelector('#resName').textContent = rec.name;
      card.querySelector('#resWhy').textContent = why;
      card.querySelector('#resList').innerHTML = rec.list.map(function (i) {
        return '<li>' + i + '</li>';
      }).join('');
      card.querySelector('#resAlt').innerHTML = rec.alt;
      card.querySelector('#resPrice').textContent = rec.price;
      var more = card.querySelector('#resMore');
      if (more) more.setAttribute('href', rec.href);
    }

    function show(index) {
      current = index;
      each(stepEls, function (s, n) { s.classList.toggle('active', n === index); });
      each(pips, function (p, n) { p.classList.toggle('on', n <= Math.min(index, pips.length - 1)); });
      if (index === 1) filterNeeds();
      if (index === 2) flagPrograms();
      if (index === LAST) render();
    }

    each(card.querySelectorAll('.f-opt, .prog-card'), function (btn) {
      btn.addEventListener('click', function () {
        answers[btn.getAttribute('data-k')] = btn.getAttribute('data-v');
        show(current + 1);
        if (current === LAST) {
          var top = card.getBoundingClientRect().top + window.pageYOffset - 90;
          window.scrollTo({ top: top, behavior: prefersReduced ? 'auto' : 'smooth' });
        }
      });
    });

    each(card.querySelectorAll('[data-back]'), function (btn) {
      btn.addEventListener('click', function () { show(Math.max(0, current - 1)); });
    });

    var restart = card.querySelector('[data-restart]');
    if (restart) restart.addEventListener('click', function () { answers = {}; show(0); });
  })();

  /* ---------------------------------------------------------------- form --- */
  (function contactForm() {
    var form = document.getElementById('enquiry');
    if (!form) return;
    var msg = document.getElementById('formMsg');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      /* ==================================================================
         SUBMISSION POINT — nothing is wired up yet.
         Pick one and replace this handler:
           • Formspree / Netlify Forms — set the form `action` attribute and
             delete this preventDefault handler entirely
           • EmailJS — call emailjs.sendForm(...) here
           • Custom endpoint — fetch(url,{method:'POST',body:new FormData(form)})
         ================================================================== */

      var bad = null;
      each(form.querySelectorAll('[required]'), function (field) {
        if (!bad && !field.value.trim()) bad = field;
      });
      var email = form.querySelector('[type="email"]');
      if (!bad && email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) {
        bad = email;
      }
      if (bad) {
        msg.textContent = 'Please complete every field, with a valid email address.';
        msg.classList.add('show');
        bad.focus();
        return;
      }
      msg.textContent = 'Form submission is not connected yet \u2014 no message was sent. ' +
        'A submission endpoint must be configured before launch.';
      msg.classList.add('show');
    });
  })();

  /* --------------------------------------------------- current year stamp --- */
  (function year() {
    var el = document.getElementById('year');
    if (el) el.textContent = new Date().getFullYear();
  })();
})();
