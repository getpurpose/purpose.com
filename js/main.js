/* ==========================================================================
   Purpose Education — site scripts
   Loaded on every page with `defer`. All modules guard for their own DOM,
   so a page that lacks a feature simply skips it.
   ========================================================================== */
(function () {
  'use strict';

  /* ------------------------------------------------------------------------
     MOTION SWITCH
     'rich'       — parallax, subject marquee, sequenced scroll scenes
     'restrained' — layout and interaction only
     Change this one string to switch the whole site.
     ---------------------------------------------------------------------- */
  var MOTION = 'rich';

  var root = document.documentElement;
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rich = MOTION === 'rich' && !prefersReduced;
  root.setAttribute('data-motion', rich ? 'rich' : 'restrained');

  /* ---------------------------------------------------------------- nav --- */
  (function nav() {
    var burger = document.getElementById('burger');
    var menu = document.getElementById('nav');
    if (!burger || !menu) return;

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
  })();

  /* ------------------------------------------------------------ reveals --- */
  (function reveals() {
    var els = document.querySelectorAll('.rv');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(els, function (el) { el.classList.add('in'); });
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
    Array.prototype.forEach.call(els, function (el) { io.observe(el); });
  })();

  /* -------------------------------------------------- framework sequence --- */
  (function framework() {
    var steps = document.getElementById('steps');
    if (!steps || !('IntersectionObserver' in window)) {
      if (steps) {
        steps.classList.add('in');
        Array.prototype.forEach.call(steps.querySelectorAll('.step'), function (s) {
          s.classList.add('lit');
        });
      }
      return;
    }
    var items = steps.querySelectorAll('.step');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        steps.classList.add('in');
        Array.prototype.forEach.call(items, function (item, i) {
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

  /* -------------------------------------------------------------- finder --- */
  (function finder() {
    var card = document.querySelector('.finder-card');
    if (!card) return;

    var stepEls = card.querySelectorAll('.f-step');
    var pips = card.querySelectorAll('.f-progress i');
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

    /* Recommendation rules. Every route begins with a Purpose Plan, which is
       the client's own model — the plan sets the format, not the other way. */
    function recommend(a) {
      if (a.need === 'college') {
        return {
          name: 'College Support',
          href: 'college-support.html',
          list: [
            'College planning and academic planning',
            'Application strategy and essays',
            'FAFSA and scholarships'
          ],
          alt: 'Pair this with <a href="tutoring-pods.html">1:1 Tutoring</a> if coursework also needs attention.'
        };
      }
      if (a.need === 'ahead') {
        return {
          name: 'Summer Program',
          href: 'summer-program.html',
          list: [
            'Personalized summer learning experience',
            'Assessment and a Purpose Plan',
            'Progress tracking and a final growth report'
          ],
          alt: 'Prefer term-time support? See <a href="tutoring-pods.html">Tutoring and Purpose Pods</a>.'
        };
      }
      if (a.mode === 'group') {
        return {
          name: 'Purpose Pods',
          href: 'tutoring-pods.html#pods',
          list: [
            'Students in the same grade range and subject area',
            'Similar academic goals',
            'Small-group instruction built on the Purpose Plan'
          ],
          alt: 'Want undivided attention instead? See <a href="tutoring-pods.html">1:1 Tutoring</a>.'
        };
      }
      if (a.mode === 'solo') {
        return {
          name: '1:1 Tutoring',
          href: 'tutoring-pods.html#tutoring',
          list: [
            'Individualized academic support',
            'Instruction targeted to the Purpose Plan',
            'Reading, writing, math, homework support and study skills'
          ],
          alt: 'Would your student do better alongside peers? See <a href="tutoring-pods.html#pods">Purpose Pods</a>.'
        };
      }
      return {
        name: 'The Purpose Plan',
        href: 'purpose-plan.html',
        list: [
          'A personalized educational roadmap',
          'Built around strengths, goals and needs',
          'Sets the right format before instruction begins'
        ],
        alt: 'From there, students continue in <a href="tutoring-pods.html">1:1 Tutoring or Purpose Pods</a>.'
      };
    }

    function render() {
      var rec = recommend(answers);
      var why = 'For a student in ' + (GRADE[answers.grade] || 'your grade range') +
        ' who needs help with ' + (NEED[answers.need] || 'their studies') +
        ', we would begin here. Every student starts with a Purpose Plan, so the support ' +
        'fits the assessment rather than the other way round.';

      card.querySelector('#resName').textContent = rec.name;
      card.querySelector('#resWhy').textContent = why;
      card.querySelector('#resList').innerHTML = rec.list.map(function (i) {
        return '<li>' + i + '</li>';
      }).join('');
      card.querySelector('#resAlt').innerHTML = rec.alt;
      var more = card.querySelector('#resMore');
      if (more) { more.setAttribute('href', rec.href); }
    }

    function show(index) {
      current = index;
      Array.prototype.forEach.call(stepEls, function (s, n) {
        s.classList.toggle('active', n === index);
      });
      Array.prototype.forEach.call(pips, function (p, n) {
        p.classList.toggle('on', n <= Math.min(index, pips.length - 1));
      });
      if (index === stepEls.length - 1) render();
    }

    Array.prototype.forEach.call(card.querySelectorAll('.f-opt'), function (btn) {
      btn.addEventListener('click', function () {
        answers[btn.getAttribute('data-k')] = btn.getAttribute('data-v');
        show(current + 1);
        if (current === stepEls.length - 1) {
          var top = card.getBoundingClientRect().top + window.pageYOffset - 90;
          window.scrollTo({ top: top, behavior: prefersReduced ? 'auto' : 'smooth' });
        }
      });
    });

    Array.prototype.forEach.call(card.querySelectorAll('[data-back]'), function (btn) {
      btn.addEventListener('click', function () { show(Math.max(0, current - 1)); });
    });

    var restart = card.querySelector('[data-restart]');
    if (restart) {
      restart.addEventListener('click', function () { answers = {}; show(0); });
    }
  })();

  /* --------------------------------------------------- current year stamp --- */
  (function year() {
    var el = document.getElementById('year');
    if (el) { el.textContent = new Date().getFullYear(); }
  })();
})();
