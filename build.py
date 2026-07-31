#!/usr/bin/env python3
"""
Purpose Education — static site builder.

Header, footer and <head> live here once. Run `python3 build.py` from this
folder to regenerate every .html page. Edit navigation or footer in ONE place
instead of seven files.

The generated HTML is plain static markup — no runtime templating, no JS-injected
navigation — so the pages remain crawlable and work without JavaScript.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("purpose-plan.html", "The Purpose Plan"),
    ("tutoring-pods.html", "Tutoring + Purpose Pods"),
    ("summer-program.html", "Summer Program"),
    ("contact.html", "Contact"),
]


def head(title, desc, slug):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Karla:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress"></div>
"""


def header(slug):
    links = "".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == slug else ""}>{label}</a>\n'
        for h, label in NAV
    )
    return f"""<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="index.html">
      <img src="images/logo.png" alt="Purpose Education crest" width="52">
      <span>
        <span class="brand-name">Purpose Education</span>
        <span class="brand-sub">Tutoring &middot; Est. 2026</span>
      </span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
{links}    </nav>
    <a class="btn btn-gold head-cta" href="contact.html">Start Your Purpose Plan</a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
"""


FOOTER = """<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="images/logo.png" alt="Purpose Education crest" width="78">
        <span class="brand-name">Purpose Education</span>
        <p>Education, done purposefully.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="purpose-plan.html">The Purpose Plan</a></li>
          <li><a href="tutoring-pods.html">Tutoring + Purpose Pods</a></li>
          <li><a href="summer-program.html">Summer Program</a></li>
          <li><a href="college-support.html">College Support</a></li>
        </ul>
      </div>
      <div>
        <h4>Get started</h4>
        <ul>
          <li><a href="index.html#finder">Find your starting point</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="purpose-plan.html">How the plan works</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <p class="foot-note">
          Email &mdash; to be confirmed<br>
          Phone &mdash; to be confirmed<br>
          Service area &mdash; to be confirmed
        </p>
      </div>
    </div>
    <div class="creed">
      <span>Faith</span><span class="sep">|</span><span>Excellence</span><span class="sep">|</span><span>Purpose</span>
    </div>
  </div>
  <div class="legal">&copy; <span id="year">2026</span> Purpose Education. All rights reserved.</div>
</footer>
</body>
</html>
"""

# --------------------------------------------------------------------------- #
# Reusable blocks
# --------------------------------------------------------------------------- #

VENN_SVG = """<svg class="venn-svg" id="venn" viewBox="0 0 480 450" role="img" aria-label="Venn diagram: Academic Growth, Personalized Support and Confidence and Purpose overlapping at Student Success">
  <circle class="vc" cx="240" cy="172" r="116"/>
  <circle class="vc" cx="184" cy="272" r="116"/>
  <circle class="vc" cx="296" cy="272" r="116"/>
  <g class="vfade">
    <text class="vlabel" x="240" y="88" text-anchor="middle">Academic</text>
    <text class="vlabel" x="240" y="106" text-anchor="middle">Growth</text>
    <text class="vlabel" x="104" y="344" text-anchor="middle">Personalized</text>
    <text class="vlabel" x="104" y="362" text-anchor="middle">Support</text>
    <text class="vlabel" x="380" y="344" text-anchor="middle">Confidence</text>
    <text class="vlabel" x="380" y="362" text-anchor="middle">&amp; Purpose</text>
    <g transform="translate(240,205)">
      <path d="M0,-15 C5,-9 7,-4 4,1 C3,-3 1,-5 0,-6 C-1,-5 -3,-3 -4,1 C-7,-4 -5,-9 0,-15 Z" fill="#E4BE6A"/>
      <rect x="-6" y="2" width="12" height="4" rx="1" fill="#C9982F"/>
      <path d="M-3.5,6 L3.5,6 L2,22 L-2,22 Z" fill="#C9982F"/>
    </g>
    <text class="vcore" x="240" y="252" text-anchor="middle">Student</text>
    <text class="vcore" x="240" y="272" text-anchor="middle">Success</text>
  </g>
</svg>"""

STEPS = [
    ("I", "Assess", "Understand current skills and needs."),
    ("II", "Plan", "Create a customized academic roadmap."),
    ("III", "Learn", "Implement targeted instruction."),
    ("IV", "Grow", "Track progress and confidence."),
    ("V", "Reflect", "Identify next steps."),
]

STEPS_HTML = '<div class="steps" id="steps">\n' + "".join(
    f'  <div class="step"><div class="medal"><span>{n}</span></div>'
    f'<h3>{t}</h3><p>{d}</p><span class="arw">&#8594;</span></div>\n'
    for n, t, d in STEPS
) + "</div>"


def page_hero(crumb, h1, lead, actions=""):
    return f"""<section class="page-hero">
  <div class="hero-glow" data-par="-0.10"></div>
  <div class="wrap">
    <div class="inner">
      <p class="crumb"><a href="index.html">Home</a><span>/</span>{crumb}</p>
      <h1>{h1}</h1>
      <p>{lead}</p>
      {actions}
    </div>
  </div>
</section>"""


CTA_BAND = """<section class="cream">
  <div class="wrap">
    <div class="cta-plate rv">
      <img src="images/logo.png" alt="" width="64">
      <p class="eyebrow">Get started</p>
      <h2>Create Your Student&rsquo;s Purpose Plan</h2>
      <p>Tell us where your student is today and what you would like them to reach. We will build the plan from there.</p>
      <a class="btn btn-crimson" href="contact.html">Start Your Purpose Plan</a>
    </div>
  </div>
</section>"""

PLACEHOLDER_BANNER = ('<div class="ph-banner">Placeholder content &mdash; '
                      'copy to be supplied and approved by Purpose Education</div>')

# --------------------------------------------------------------------------- #
# Page bodies
# --------------------------------------------------------------------------- #

INDEX = """<main id="main">
  <section class="hero">
    <div class="hero-glow" data-par="-0.10"></div>
    <img class="hero-crest" src="images/logo.png" alt="" data-par="0.16">
    <div class="wrap hero-inner">
      <div>
        <p class="eyebrow on-navy fade-up">Education, done purposefully</p>
        <h1>
          <span class="ln"><span>Helping Students and</span></span>
          <span class="ln"><span>Families Create a Plan</span></span>
          <span class="ln"><span><em>With Purpose.</em></span></span>
        </h1>
        <div class="hero-rule fade-up d1"></div>
        <p class="sub fade-up d1">Personalized educational support designed to help students strengthen skills, build confidence, and achieve their goals.</p>
        <div class="hero-actions fade-up d2">
          <a class="btn btn-gold" href="#finder">Start Your Purpose Plan</a>
          <a class="btn btn-ghost" href="#services">Explore Services</a>
        </div>
        <div class="hero-meta fade-up d3">
          <span>Grades <b>PreK&ndash;12</b></span>
          <span>1:1, small group and summer</span>
          <span>Every student begins with a <b>Purpose Plan</b></span>
        </div>
      </div>
      <div class="fade-up d2">
        <div class="plate-frame">
          <div class="photo-slot">
            <img src="images/logo.png" alt="" data-par="0.05">
            <span class="slot-label">Photography placeholder &mdash; student and educator working together, warm professional environment</span>
          </div>
        </div>
      </div>
    </div>
    <div class="equation">
      <div class="wrap equation-inner">
        <span>Where your student is</span><span class="arw">&#8594;</span>
        <span>What they need</span><span class="arw">&#8594;</span>
        <span>How they will grow</span>
      </div>
    </div>
  </section>

  <div class="subjects" aria-label="Subjects we support">
    <div class="marquee">
      <span>Reading</span><span>Writing</span><span>Math</span><span>Homework Support</span><span>Study Skills</span><span>Grades PreK&ndash;12</span>
      <span>Reading</span><span>Writing</span><span>Math</span><span>Homework Support</span><span>Study Skills</span><span>Grades PreK&ndash;12</span>
    </div>
  </div>

  <section class="cream" id="difference">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">The Purpose Education Difference</p>
        <p class="diff-statement">Every student has a unique educational journey. We create personalized pathways that help students identify strengths, overcome challenges, and reach their goals.</p>
      </div>
      <div class="pillars rv">
        <div class="pillar"><div class="pillar-mark">I</div><div>
          <h3>Individualized planning</h3>
          <p>Every student begins with a plan built around their strengths, goals, and needs &mdash; never a standard curriculum.</p></div></div>
        <div class="pillar"><div class="pillar-mark">II</div><div>
          <h3>Targeted instruction</h3>
          <p>Teaching aimed at what the plan identifies, delivered one-to-one or in small groups matched by grade and subject.</p></div></div>
        <div class="pillar"><div class="pillar-mark">III</div><div>
          <h3>Family partnership</h3>
          <p>Families see where their student is, what they need, and how they are growing &mdash; in plain language, throughout.</p></div></div>
      </div>
    </div>
  </section>

  <section class="finder" id="finder">
    <img class="finder-crest" src="images/logo.png" alt="" data-par="0.12">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Find your student&rsquo;s starting point</p>
        <h2>Not sure which support fits your child?</h2>
        <p>Answer three quick questions and we will show you where to begin.</p>
      </div>
      <div class="finder-card rv">
        <div class="f-progress"><i class="on"></i><i></i><i></i></div>

        <div class="f-step active" data-step="0">
          <p class="f-q">What grade is your student in?</p>
          <p class="f-hint">We support students from PreK through Grade 12.</p>
          <div class="f-opts">
            <button class="f-opt" data-k="grade" data-v="prek2"><b>PreK &ndash; Grade 2</b><small>Early reading, phonics and number sense</small></button>
            <button class="f-opt" data-k="grade" data-v="g35"><b>Grades 3 &ndash; 5</b><small>Building fluency, writing and comprehension</small></button>
            <button class="f-opt" data-k="grade" data-v="g68"><b>Grades 6 &ndash; 8</b><small>Subject depth, organisation and study habits</small></button>
            <button class="f-opt" data-k="grade" data-v="g912"><b>Grades 9 &ndash; 12</b><small>Coursework, planning and next steps</small></button>
          </div>
        </div>

        <div class="f-step" data-step="1">
          <p class="f-q">What would you like help with most?</p>
          <p class="f-hint">Choose the area that matters most right now.</p>
          <div class="f-opts">
            <button class="f-opt" data-k="need" data-v="literacy"><b>Reading &amp; writing</b><small>Comprehension, phonics, written work</small></button>
            <button class="f-opt" data-k="need" data-v="math"><b>Math</b><small>Core skills and problem solving</small></button>
            <button class="f-opt" data-k="need" data-v="habits"><b>Homework &amp; study skills</b><small>Organisation, routines, independence</small></button>
            <button class="f-opt" data-k="need" data-v="ahead"><b>Getting ahead</b><small>Enrichment and next-grade preparation</small></button>
            <button class="f-opt" data-k="need" data-v="college"><b>College planning</b><small>Applications, essays, FAFSA, scholarships</small></button>
          </div>
          <button class="f-back" data-back>&larr; Back</button>
        </div>

        <div class="f-step" data-step="2">
          <p class="f-q">How would your student learn best?</p>
          <p class="f-hint">Both options follow the same Purpose Plan.</p>
          <div class="f-opts">
            <button class="f-opt" data-k="mode" data-v="solo"><b>One-to-one</b><small>Full attention on their own plan</small></button>
            <button class="f-opt" data-k="mode" data-v="group"><b>With a small group</b><small>Same grade range, same subject area</small></button>
            <button class="f-opt" data-k="mode" data-v="unsure"><b>Not sure yet</b><small>Help us decide during the assessment</small></button>
          </div>
          <button class="f-back" data-back>&larr; Back</button>
        </div>

        <div class="f-step" data-step="3">
          <div class="f-result">
            <div>
              <span class="f-res-tag">Recommended starting point</span>
              <h3 class="f-res-name" id="resName">The Purpose Plan</h3>
              <p class="f-res-why" id="resWhy"></p>
              <ul class="f-res-list" id="resList"></ul>
              <a class="btn btn-crimson" href="contact.html">Start Your Purpose Plan</a>
              <p class="f-alt" id="resAlt"></p>
              <button class="f-back" data-restart>&larr; Start again</button>
            </div>
            <div class="f-next">
              <h4>What happens next</h4>
              <ol>
                <li><b>Assess.</b> Understand current skills and needs.</li>
                <li><b>Plan.</b> Create a customized academic roadmap.</li>
                <li><b>Learn.</b> Implement targeted instruction.</li>
              </ol>
              <p class="f-price">Pricing for each service is shown on its own page.</p>
              <a class="textlink" id="resMore" href="purpose-plan.html" style="color:var(--gold-lt)">Read more</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="plate" id="plan">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">The Purpose Plan Framework</p>
        <h2>Our signature framework for academic growth</h2>
        <p>A personalized educational roadmap designed around each student&rsquo;s strengths, goals, and needs.</p>
      </div>
      __STEPS__
      <div class="venn-block rv">
        <div class="venn-copy">
          <h3>Three strands, one outcome.</h3>
          <p>The Purpose Plan works where academic growth, personalized support, and confidence meet. Student success sits at the centre &mdash; the point where all three are working together.</p>
          <ul class="venn-list"><li>Academic Growth</li><li>Personalized Support</li><li>Confidence &amp; Purpose</li></ul>
          <a class="textlink" href="purpose-plan.html">Explore the Purpose Plan</a>
        </div>
        <div>__VENN__</div>
      </div>
    </div>
  </section>

  <section class="cream" id="services">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Services Overview</p>
        <h2>Support for every stage of the journey</h2>
        <p>Purpose Education is not just tutoring. It is a personalized educational pathway for your child.</p>
      </div>
      <div class="svc-grid">
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12"/><path d="M20.5 11.5 L18 18 L11.5 20.5 L14 14 Z"/></svg>
          <h3>The Purpose Plan</h3><p>Personalized educational roadmap.</p>
          <a class="textlink" href="purpose-plan.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 10c-2-2-5-2.5-8-2v13c3-.5 6 0 8 2 2-2 5-2.5 8-2V8c-3-.5-6 0-8 2Z"/><path d="M16 10v13"/></svg>
          <h3>1:1 Tutoring</h3><p>Individualized academic support.</p>
          <a class="textlink" href="tutoring-pods.html#tutoring">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="11" cy="13" r="3.2"/><circle cx="21" cy="13" r="3.2"/><path d="M5 24c0-3.4 2.7-5.5 6-5.5s6 2.1 6 5.5"/><path d="M15 24c0-3.4 2.7-5.5 6-5.5s6 2.1 6 5.5"/></svg>
          <h3>Purpose Pods</h3><p>Small-group learning with students in the same grade range and subject area.</p>
          <a class="textlink" href="tutoring-pods.html#pods">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="16" cy="16" r="6"/><path d="M16 4v3M16 25v3M4 16h3M25 16h3M7.5 7.5l2.2 2.2M22.3 22.3l2.2 2.2M24.5 7.5l-2.2 2.2M9.7 22.3l-2.2 2.2"/></svg>
          <h3>Summer Program</h3><p>Personalized summer learning experience.</p>
          <a class="textlink" href="summer-program.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 8 3 14l13 6 13-6-13-6Z"/><path d="M8.5 16.8V22c0 2 3.4 3.6 7.5 3.6s7.5-1.6 7.5-3.6v-5.2"/></svg>
          <h3>College Support</h3><p>Admissions, FAFSA, scholarships, and planning.</p>
          <a class="textlink" href="college-support.html">Learn more</a>
        </article>
      </div>
      <p class="svc-foot rv">Pricing for each service is shown on its own page.</p>
    </div>
  </section>

  <section class="navy">
    <div class="wrap quote rv">
      <span class="quote-mark">&ldquo;</span>
      <span class="ph">Placeholder content</span>
      <blockquote>This space will hold a parent&rsquo;s own words about working with Purpose Education, to be supplied and approved by the client.</blockquote>
      <span class="attrib">Placeholder &mdash; parent attribution to be confirmed</span>
    </div>
  </section>

  __CTA__
</main>"""

ABOUT = """<main id="main">
  __HERO__
  __PHBANNER__

  <section class="paper">
    <div class="wrap split narrow-right">
      <div class="rv prose">
        <p class="eyebrow">Our mission</p>
        <p class="diff-statement">Every student has a unique educational journey. We create personalized pathways that help students identify strengths, overcome challenges, and reach their goals.</p>
      </div>
      <div class="rv">
        <div class="ph-block">
          <span class="ph">Mission statement</span>
          <p>[Placeholder &mdash; Purpose Education to supply the full mission statement. Two to three short paragraphs describing why the company exists and who it serves.]</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap split">
      <div class="rv">
        <div class="plate-frame">
          <div class="photo-slot light">
            <img src="images/logo.png" alt="">
            <span class="slot-label">Photography placeholder &mdash; founder portrait</span>
          </div>
        </div>
      </div>
      <div class="rv prose">
        <p class="eyebrow">Founder story</p>
        <h2>Meet the founder</h2>
        <div class="ph-block">
          <span class="ph">Founder story</span>
          <p>[Placeholder &mdash; to be supplied. Suggested content: what led to founding Purpose Education, the moment that prompted it, and what the founder wants for the families they work with.]</p>
        </div>
      </div>
    </div>
  </section>

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Educational philosophy</p>
        <h2>How we think about learning</h2>
        <p>Purpose Education is more than tutoring. It is an educational support system that helps families understand where their student is, what they need, and how they will grow.</p>
      </div>
      <div class="grid grid-2">
        <div class="card rv">
          <span class="card-no">I</span>
          <h3>Classroom experience</h3>
          <p>[Placeholder &mdash; describe years taught, grade levels, and school settings.]</p>
        </div>
        <div class="card rv">
          <span class="card-no">II</span>
          <h3>Educational consulting background</h3>
          <p>[Placeholder &mdash; describe consulting work, the families or schools served, and the outcomes.]</p>
        </div>
        <div class="card rv">
          <span class="card-no">III</span>
          <h3>Personalized learning approach</h3>
          <p>[Placeholder &mdash; describe how each student&rsquo;s plan is built and how instruction is adapted.]</p>
        </div>
        <div class="card rv">
          <span class="card-no">IV</span>
          <h3>Family partnership</h3>
          <p>[Placeholder &mdash; describe how families are kept involved and how progress is shared.]</p>
        </div>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">What guides us</p>
        <h2>Faith &middot; Excellence &middot; Purpose</h2>
        <p>[Placeholder &mdash; Purpose Education to confirm how prominently these three values should feature and to supply a short line for each.]</p>
      </div>
    </div>
  </section>

  __CTA__
</main>"""

PURPOSE_PLAN = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">What it is</p>
        <p class="diff-statement">A personalized educational roadmap designed around each student&rsquo;s strengths, goals, and needs.</p>
      </div>
      <div class="rv prose">
        <p>The Purpose Plan is where every student begins. Before any instruction is scheduled, we build a clear picture of where your student is now, agree what they are working towards, and set out how they will get there.</p>
        <p>It is what makes the rest of the work personalized rather than generic &mdash; the plan decides the subject focus, the format, and the pace, rather than the other way round.</p>
        <a class="textlink" href="index.html#finder">Find your starting point</a>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">The process</p>
        <h2>Assess &rarr; Plan &rarr; Learn &rarr; Grow &rarr; Reflect</h2>
        <p>Five stages that repeat as your student progresses.</p>
      </div>
      __STEPS__
      <div class="venn-block rv">
        <div class="venn-copy">
          <h3>Three strands, one outcome.</h3>
          <p>The Purpose Plan works where academic growth, personalized support, and confidence meet. Student success sits at the centre &mdash; the point where all three are working together.</p>
          <ul class="venn-list"><li>Academic Growth</li><li>Personalized Support</li><li>Confidence &amp; Purpose</li></ul>
        </div>
        <div>__VENN__</div>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Investment</p>
        <h2>Investment in your student&rsquo;s growth</h2>
      </div>
      <div class="price-grid">
        <div class="price-card tbc rv">
          <span class="p-label">The Purpose Plan</span>
          <h3>Customized</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Pricing pending client confirmation</span>
          <p>Priced according to the assessment and the plan your student needs.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">1:1 Tutoring</span>
          <h3>Per hour</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Pricing pending client confirmation</span>
          <p>Individualized academic support, targeted to the plan.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">Purpose Pods</span>
          <h3>Per student</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Pricing pending client confirmation</span>
          <p>Small-group learning with students in the same grade range and subject area.</p>
        </div>
      </div>
      <p class="svc-foot rv">All pricing on this site is placeholder and awaiting confirmation from Purpose Education.</p>
    </div>
  </section>

  <section class="paper">
    <div class="wrap-narrow">
      <div class="sec-head rv">
        <p class="eyebrow">Common questions</p>
        <h2>Before you begin</h2>
      </div>
      <div class="faq rv">
        <details>
          <summary>Does every student need a Purpose Plan?</summary>
          <div class="faq-body"><p>Yes. The plan is what makes the instruction personalized &mdash; it identifies current skills and needs before any teaching begins.</p></div>
        </details>
        <details>
          <summary>Which grades do you work with?</summary>
          <div class="faq-body"><p>Students in PreK through Grade 12.</p></div>
        </details>
        <details>
          <summary>What subjects are covered?</summary>
          <div class="faq-body"><p>Reading, writing, math, homework support and study skills. College planning is handled separately through College Support.</p></div>
        </details>
        <details>
          <summary>How often is progress reviewed?</summary>
          <div class="faq-body"><p>[Placeholder &mdash; Purpose Education to confirm review cadence and how progress is reported to families.]</p></div>
        </details>
      </div>
    </div>
  </section>

  __CTA__
</main>"""

TUTORING = """<main id="main">
  __HERO__

  <section class="paper" id="tutoring">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">1:1 Tutoring</p>
        <h2>Individualized academic support</h2>
        <p class="lede">One student, one educator, and a plan built for them. Instruction follows the Purpose Plan, so every session targets what the assessment identified.</p>
      </div>
      <div class="rv">
        <table class="spec">
          <tbody>
            <tr><th>Grades</th><td>PreK&ndash;12</td></tr>
            <tr><th>Subjects</th><td>Reading &middot; Writing &middot; Math &middot; Homework Support &middot; Study Skills</td></tr>
            <tr><th>Format</th><td>One-to-one</td></tr>
            <tr><th>Begins with</th><td>A Purpose Plan assessment</td></tr>
            <tr><th>Price</th><td>To be confirmed</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="cream" id="pods">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Purpose Pods</p>
        <h2>Small-group learning, thoughtfully matched</h2>
        <p>Purpose Pods are not general group tutoring. Students are grouped so the instruction stays relevant to everyone in the room.</p>
      </div>
      <div class="grid grid-3">
        <div class="card rv"><span class="card-no">I</span><h3>Similar age range</h3><p>Students work alongside peers at a comparable stage.</p></div>
        <div class="card rv"><span class="card-no">II</span><h3>Same subject</h3><p>Every student in the pod is working in the same subject area.</p></div>
        <div class="card rv"><span class="card-no">III</span><h3>Similar academic goals</h3><p>Shared goals keep the session focused for the whole group.</p></div>
      </div>
    </div>
  </section>

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Investment</p>
        <h2>Tutoring and pod pricing</h2>
      </div>
      <div class="price-grid">
        <div class="price-card tbc rv">
          <span class="p-label">Individual</span>
          <h3>1:1 Tutoring</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Rate and session length pending confirmation</span>
          <p>Individualized academic support.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">Small group</span>
          <h3>2 Student Pod</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Per student, rate pending confirmation</span>
          <p>Two students, same subject area and grade range.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">Small group</span>
          <h3>3 Student Pod</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Per student, rate pending confirmation</span>
          <p>Three students, same subject area and grade range.</p>
        </div>
      </div>
      <div class="ph-block rv" style="margin-top:1.6rem">
        <span class="ph">Note for Purpose Education</span>
        <p>Two different price sets exist in the supplied documents &mdash; the written brief lists hourly rates, the reference designs list per-session rates and package prices. Please confirm which is current, and whether a session is 60 minutes, before this page goes live.</p>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap sec-head rv" style="margin-bottom:0">
      <p class="eyebrow on-navy">Not sure which fits?</p>
      <h2>Answer three questions and we will point you to the right starting place</h2>
      <p style="margin-bottom:1.8rem">Every route begins with a Purpose Plan.</p>
      <a class="btn btn-gold" href="index.html#finder">Find your starting point</a>
    </div>
  </section>

  __CTA__
</main>"""

SUMMER = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Three tracks</p>
        <h2>Choose the summer experience that fits your student</h2>
        <p>Each track begins with an assessment and a Purpose Plan.</p>
      </div>
      <div class="grid grid-3">
        <article class="track rv">
          <div class="track-top"><span>Track I</span><h3>Purpose Foundations</h3></div>
          <div class="track-body">
            <ul><li>Reading</li><li>Phonics</li><li>Writing</li><li>Math</li><li>Comprehension</li></ul>
            <a class="textlink" href="contact.html">Enquire</a>
          </div>
        </article>
        <article class="track rv">
          <div class="track-top"><span>Track II</span><h3>Purpose Prep</h3></div>
          <div class="track-body">
            <ul><li>Grade-level preparation</li><li>Academic confidence</li></ul>
            <a class="textlink" href="contact.html">Enquire</a>
          </div>
        </article>
        <article class="track rv">
          <div class="track-top"><span>Track III</span><h3>Purpose Enrichment</h3></div>
          <div class="track-body">
            <ul><li>Advanced reading</li><li>Writing</li><li>STEM</li><li>Research</li><li>Critical thinking</li></ul>
            <a class="textlink" href="contact.html">Enquire</a>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow on-navy">What every track includes</p>
        <h2>A summer with a plan behind it</h2>
      </div>
      <div class="rv">
        <ul class="checklist">
          <li>Assessment</li>
          <li>Purpose Plan</li>
          <li>Instruction</li>
          <li>Progress tracking</li>
          <li>Final portfolio and growth report</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Investment</p>
        <h2>Summer pricing</h2>
      </div>
      <div class="price-grid">
        <div class="price-card tbc rv">
          <span class="p-label">Foundations</span><h3>Purpose Foundations</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Customized packages</span>
          <p>Reading, phonics, writing, math and comprehension.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">Prep</span><h3>Purpose Prep</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Customized packages</span>
          <p>Grade-level preparation and academic confidence.</p>
        </div>
        <div class="price-card tbc rv">
          <span class="p-label">Enrichment</span><h3>Purpose Enrichment</h3>
          <span class="p-amount">To be confirmed</span>
          <span class="p-unit">Customized packages</span>
          <p>Advanced reading, writing, STEM, research and critical thinking.</p>
        </div>
      </div>
      <p class="svc-foot rv">Summer packages are customized. Final pricing to be confirmed by Purpose Education.</p>
    </div>
  </section>

  __CTA__
</main>"""

COLLEGE = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">What we help with</p>
        <h2>From first list to final decision</h2>
      </div>
      <div class="grid grid-3">
        <div class="card rv"><span class="card-no">I</span><h3>College planning</h3><p>Building a realistic list and a timeline that fits the student.</p></div>
        <div class="card rv"><span class="card-no">II</span><h3>Application strategy</h3><p>Deciding where to apply, when, and how to present the student&rsquo;s strengths.</p></div>
        <div class="card rv"><span class="card-no">III</span><h3>Essays</h3><p>Support through drafting and revision, in the student&rsquo;s own voice.</p></div>
        <div class="card rv"><span class="card-no">IV</span><h3>FAFSA</h3><p>Guidance through the financial aid application process.</p></div>
        <div class="card rv"><span class="card-no">V</span><h3>Scholarships</h3><p>Identifying and pursuing scholarship opportunities.</p></div>
        <div class="card rv"><span class="card-no">VI</span><h3>Academic planning</h3><p>Course selection and preparation aligned to where the student is heading.</p></div>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Investment</p>
        <h2>College Support pricing</h2>
        <p>To be confirmed by Purpose Education.</p>
      </div>
      <div class="ph-block rv" style="max-width:720px;margin:0 auto">
        <span class="ph">Pricing placeholder</span>
        <p>Pricing for College Support is not specified in the supplied brief. Please confirm whether this is offered hourly, as a package, or as part of the Purpose Plan.</p>
      </div>
    </div>
  </section>

  __CTA__
</main>"""

CONTACT = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split narrow-left">
      <div class="rv prose">
        <p class="eyebrow">Get in touch</p>
        <h2>We would like to hear about your student</h2>
        <p>Tell us where your student is today and what you would like them to reach. Every student begins with a Purpose Plan, so the first conversation is about understanding current skills and needs.</p>
        <div class="ph-block" style="margin-top:1.6rem">
          <span class="ph">Contact details placeholder</span>
          <p><strong>Email</strong> &mdash; to be confirmed<br>
             <strong>Phone</strong> &mdash; to be confirmed<br>
             <strong>Hours</strong> &mdash; to be confirmed<br>
             <strong>Service area</strong> &mdash; to be confirmed</p>
        </div>
      </div>
      <div class="rv">
        <ul class="checklist">
          <li><strong>Assess.</strong> Understand current skills and needs.</li>
          <li><strong>Plan.</strong> Create a customized academic roadmap.</li>
          <li><strong>Learn.</strong> Implement targeted instruction.</li>
          <li><strong>Grow.</strong> Track progress and confidence.</li>
          <li><strong>Reflect.</strong> Identify next steps.</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Where to find us</p>
        <h2>Location</h2>
        <p>Address and service area to be confirmed by Purpose Education.</p>
      </div>
      <div class="map-frame rv">
        <!-- ==================================================================
             MAP EMBED POINT
             Replace the .map-slot div below with the Google Maps embed iframe
             once the address is confirmed, e.g.

             <div class="map-slot">
               <iframe src="https://www.google.com/maps/embed?pb=..."
                       loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                       title="Purpose Education location"></iframe>
             </div>
             ================================================================== -->
        <div class="map-slot">
          <img src="images/logo.png" alt="">
          <span class="slot-label">Map placeholder &mdash; embed to be added once the address is confirmed</span>
        </div>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap sec-head rv" style="margin-bottom:0">
      <p class="eyebrow on-navy">Not sure where to start?</p>
      <h2>Answer three questions and we will point you to the right service</h2>
      <p style="margin-bottom:1.8rem">It takes about thirty seconds.</p>
      <a class="btn btn-gold" href="index.html#finder">Find your starting point</a>
    </div>
  </section>
</main>"""

# --------------------------------------------------------------------------- #

PAGES = [
    dict(slug="index.html", title="Purpose Education — Helping Students and Families Create a Plan With Purpose",
         desc="Personalized educational support for students in PreK–12. Individualized planning, targeted instruction, small-group Purpose Pods, summer programs and college support.",
         body=INDEX, hero=None),

    dict(slug="about.html", title="About — Purpose Education",
         desc="Purpose Education is a personalized education company helping students grow through individualized planning, targeted instruction and meaningful learning experiences.",
         body=ABOUT,
         hero=page_hero("About", "Education, done <em>purposefully.</em>",
                        "Purpose Education is a personalized education company that helps students grow academically through individualized planning, targeted instruction, and meaningful learning experiences.")),

    dict(slug="purpose-plan.html", title="The Purpose Plan — Purpose Education",
         desc="A personalized educational roadmap designed around each student's strengths, goals and needs. Assess, Plan, Learn, Grow, Reflect.",
         body=PURPOSE_PLAN,
         hero=page_hero("The Purpose Plan", "The <em>Purpose Plan.</em>",
                        "A personalized educational roadmap designed around each student&rsquo;s strengths, goals, and needs.",
                        '<a class="btn btn-gold" href="contact.html">Start Your Purpose Plan</a>')),

    dict(slug="tutoring-pods.html", title="Tutoring + Purpose Pods — Purpose Education",
         desc="1:1 tutoring for grades PreK–12 in reading, writing, math, homework support and study skills, plus small-group Purpose Pods matched by grade range and subject.",
         body=TUTORING,
         hero=page_hero("Tutoring + Purpose Pods", "Tutoring and <em>Purpose Pods.</em>",
                        "Individualized academic support one-to-one, or small-group learning with students in the same grade range and subject area.")),

    dict(slug="summer-program.html", title="Summer Program — Purpose Education",
         desc="A personalized summer learning experience designed to help students strengthen skills, build confidence, and prepare for the next school year.",
         body=SUMMER,
         hero=page_hero("Summer Program", "Make This Summer <em>Count.</em>",
                        "A personalized summer learning experience designed to help students strengthen skills, build confidence, and prepare for the next school year.",
                        '<a class="btn btn-gold" href="contact.html">Start Your Purpose Plan</a>')),

    dict(slug="college-support.html", title="College Support — Purpose Education",
         desc="College planning, application strategy, essays, FAFSA, scholarships and academic planning.",
         body=COLLEGE,
         hero=page_hero("College Support", "College <em>Support.</em>",
                        "Admissions, FAFSA, scholarships, and planning &mdash; guidance through the transition to what comes next.")),

    dict(slug="contact.html", title="Contact — Purpose Education",
         desc="Get in touch with Purpose Education to create your student's Purpose Plan.",
         body=CONTACT,
         hero=page_hero("Contact", "Create Your Student&rsquo;s <em>Purpose Plan.</em>",
                        "Tell us where your student is today and what you would like them to reach. We will build the plan from there.")),
]


def build():
    for page in PAGES:
        body = page["body"]
        body = body.replace("__STEPS__", STEPS_HTML)
        body = body.replace("__VENN__", VENN_SVG)
        body = body.replace("__CTA__", CTA_BAND)
        body = body.replace("__PHBANNER__", PLACEHOLDER_BANNER)
        body = body.replace("__HERO__", page["hero"] or "")

        html = head(page["title"], page["desc"], page["slug"])
        html += header(page["slug"])
        html += body + "\n"
        html += FOOTER

        out = os.path.join(HERE, page["slug"])
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("built", page["slug"], len(html), "bytes")


if __name__ == "__main__":
    build()
