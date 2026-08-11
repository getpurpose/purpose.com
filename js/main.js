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
    var nodes = card.querySelectorAll('.f-node');
    var rails = card.querySelectorAll('.f-rail');
    var LAST = stepEls.length - 1;
    var answers = {};
    var current = 0;

    var GRADE = {
      prek2: 'PreK\u2013Grade 2',
      g35: 'Grades 3\u20135',
      g68: 'Grades 6\u20138',
      g912: 'Grades 9\u201312'
    };
    var FOCUS = {
      literacy: 'reading and writing',
      math: 'mathematics',
      skills: 'academic skills',
      future: 'planning for what comes next'
    };

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
      summer: {
        name: 'Summer Program',
        href: 'summer-program.html',
        price: 'Customized packages',
        list: [
          'Personalized summer learning experience',
          'Assessment and a Purpose Plan',
          'Progress tracking and a final growth report'
        ],
        alt: 'Looking for term-time support instead? See <a href="programs.html">Academic Programs</a>.'
      },
      college: {
        name: 'College Admissions &amp; Planning',
        href: 'college-support.html',
        price: 'Customized pricing',
        list: [
          'College planning and application strategy',
          'Essays, FAFSA and scholarship support',
          'Academic planning aligned to where the student is heading'
        ],
        alt: 'Pair this with <a href="tutoring.html">One-on-One Tutoring</a> if coursework also needs attention.'
      }
    };

    /* Grade + focus area decide the recommendation. */
    function recommend(a) {
      if (a.focus === 'future') return a.grade === 'g912' ? 'college' : 'summer';
      if (a.focus === 'skills') return 'group';
      return 'solo';
    }

    function render() {
      var rec = PROGRAM[recommend(answers)] || PROGRAM.solo;
      var why = 'For a student in ' + (GRADE[answers.grade] || 'your grade range') +
        ' focusing on ' + (FOCUS[answers.focus] || 'their studies') +
        ', we would begin here. Every student starts with The Purpose Plan, so the ' +
        'instruction fits the assessment rather than the other way round.';

      card.querySelector('#resName').innerHTML = rec.name;
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
      each(nodes, function (n, i) { n.classList.toggle('on', i <= index); });
      each(rails, function (r, i) { r.classList.toggle('on', i < index); });
      if (index === LAST) render();
    }

    each(card.querySelectorAll('.f-opt, .focus-card'), function (btn) {
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

  /* ----------------------------------------------------------- carousel --- */
  (function carousel() {
    var root = document.querySelector('.tst-carousel');
    if (!root) return;
    var track = root.querySelector('.tst-track');
    var slides = root.querySelectorAll('.tst-slide');
    var prev = root.querySelector('.tst-arrow.prev');
    var next = root.querySelector('.tst-arrow.next');
    var dotWrap = root.querySelector('.tst-dots');
    var index = 0;

    function perView() {
      return window.matchMedia('(max-width: 1040px)').matches ? 1 : 2;
    }
    function maxIndex() {
      return Math.max(0, slides.length - perView());
    }
    function buildDots() {
      dotWrap.innerHTML = '';
      for (var i = 0; i <= maxIndex(); i++) {
        (function (n) {
          var b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('aria-label', 'Go to testimonial ' + (n + 1));
          b.addEventListener('click', function () { go(n); });
          dotWrap.appendChild(b);
        })(i);
      }
    }
    function go(n) {
      index = Math.max(0, Math.min(n, maxIndex()));
      track.style.transform = 'translateX(-' + (index * (100 / perView())) + '%)';
      prev.disabled = index === 0;
      next.disabled = index === maxIndex();
      each(dotWrap.children, function (d, i) { d.classList.toggle('on', i === index); });
    }
    prev.addEventListener('click', function () { go(index - 1); });
    next.addEventListener('click', function () { go(index + 1); });
    window.addEventListener('resize', function () { buildDots(); go(index); }, { passive: true });
    buildDots();
    go(0);
  })();

  /* ---------------------------------------------------------------- form --- */
  (function contactForm() {
    var form = document.getElementById('enquiry');
    if (!form) return;
    var msg = document.getElementById('formMsg');

    var format = form.querySelector('#format');
    var library = form.querySelector('#libraryField');
    if (format && library) {
      format.addEventListener('change', function () {
        var inPerson = format.value === 'in-person';
        library.hidden = !inPerson;
        var input = library.querySelector('input');
        if (input) { if (inPerson) { input.setAttribute('required',''); } else { input.removeAttribute('required'); input.value=''; } }
      });
    }

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
        if (field.offsetParent === null) return;   /* skip hidden fields */
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
