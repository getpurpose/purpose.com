#!/usr/bin/env python3
"""
Purpose Education — static site builder.

Header, footer and <head> live here once. Run `python3 build.py` from this
folder to regenerate every .html page. Edit navigation or footer in ONE place
instead of nine files.

Output is plain static markup — no runtime templating, no JS-injected
navigation — so pages stay crawlable and work without JavaScript.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Top-level nav. `children` turns an entry into a dropdown.
NAV = [
    ("index.html", "Home", None),
    ("about.html", "About", None),
    ("purpose-plan.html", "The Purpose Plan", None),
    ("programs.html", "Academic Programs", [
        ("programs.html", "All Programs", True),
        ("tutoring.html", "One-on-One Tutoring", False),
        ("purpose-pods.html", "Purpose Pods", False),
        ("summer-program.html", "Summer Program", False),
        ("college-support.html", "College Admissions &amp; Planning", False),
    ]),
    ("contact.html", "Contact", None),
]

PROGRAM_PAGES = {"programs.html", "tutoring.html", "purpose-pods.html",
                 "summer-program.html", "college-support.html"}

SOCIALS = """<div class="socials">
      <a href="#" aria-label="Facebook" rel="noopener"><svg viewBox="0 0 24 24"><path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.2-1.5 1.5-1.5H16.7V4c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.5-4 4.2V10H7.6v3h2.7v8h3.2z"/></svg></a>
      <a href="#" aria-label="Instagram" rel="noopener"><svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.8.1-.9 0-1.4.2-1.7.3-.4.2-.7.4-1 .7-.3.3-.5.6-.7 1-.1.3-.3.8-.3 1.7C3.4 8.5 3.4 8.9 3.4 12s0 3.5.1 4.8c0 .9.2 1.4.3 1.7.2.4.4.7.7 1 .3.3.6.5 1 .7.3.1.8.3 1.7.3 1.3.1 1.7.1 4.8.1s3.5 0 4.8-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.4 1-.7.3-.3.5-.6.7-1 .1-.3.3-.8.3-1.7.1-1.3.1-1.7.1-4.8s0-3.5-.1-4.8c0-.9-.2-1.4-.3-1.7-.2-.4-.4-.7-.7-1-.3-.3-.6-.5-1-.7-.3-.1-.8-.3-1.7-.3-1.3-.1-1.7-.1-4.8-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zm6.2-8.3a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0z"/></svg></a>
      <a href="#" aria-label="LinkedIn" rel="noopener"><svg viewBox="0 0 24 24"><path d="M6.9 8.6H3.7V21h3.2V8.6zM5.3 3.1a1.9 1.9 0 1 0 0 3.8 1.9 1.9 0 0 0 0-3.8zM21 21h-3.2v-6c0-1.5-.5-2.5-1.8-2.5-1 0-1.6.7-1.8 1.3-.1.2-.1.6-.1.9V21H10.8s.1-11.2 0-12.4H14v1.8c.4-.7 1.2-1.7 3-1.7 2.2 0 3.9 1.4 3.9 4.5V21z"/></svg></a>
    </div>"""


def head(title, desc):
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,300..700,0..100&family=Karla:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script src="js/main.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" id="progress"></div>
<div class="util-bar">
  <div class="wrap util-inner">
    <span class="util-note">Remote tutoring nationwide &middot; Evenings and weekends</span>
    {SOCIALS}
  </div>
</div>
"""


def header(slug):
    out = []
    for href, label, children in NAV:
        if children:
            active = ' aria-current="page"' if slug in PROGRAM_PAGES else ""
            kids = "".join(
                f'        <a href="{h}"{" class=\"drop-lead\"" if lead else ""}>{l}</a>\n'
                for h, l, lead in children
            )
            out.append(
                f'      <div class="nav-drop">\n'
                f'        <button type="button" aria-expanded="false"{active}>{label}</button>\n'
                f'        <div class="drop-menu">\n{kids}        </div>\n'
                f'      </div>\n'
            )
        else:
            cur = ' aria-current="page"' if href == slug else ""
            out.append(f'      <a href="{href}"{cur}>{label}</a>\n')
    links = "".join(out)
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


FOOTER = f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="images/logo.png" alt="Purpose Education crest" width="78">
        <span class="brand-name">Purpose Education</span>
        <p>Education, done purposefully.</p>
        {SOCIALS}
      </div>
      <div>
        <h4>Programs</h4>
        <ul>
          <li><a href="purpose-plan.html">The Purpose Plan</a></li>
          <li><a href="tutoring.html">One-on-One Tutoring</a></li>
          <li><a href="purpose-pods.html">Purpose Pods</a></li>
          <li><a href="summer-program.html">Summer Program</a></li>
          <li><a href="college-support.html">College Admissions &amp; Planning</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="programs.html#tutors">Why Our Tutors</a></li>
          <li><a href="index.html#finder">Find your starting point</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <p class="foot-note">
          Remote tutoring, nationwide<br>
          Evenings and weekends available<br>
          Email &mdash; to be confirmed<br>
          Phone &mdash; to be confirmed
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

VENN_BLOCK = """<div class="venn-block rv">
  <div class="venn-copy">
    <h3>Three Pillars. One Purpose.</h3>
    <p>The Purpose Plan brings together three essential elements of student success. When academic growth, personalized support, and confidence work together, students are empowered to reach their full potential.</p>
    <ul class="venn-list">
      <li><b>Academic Growth</b> &mdash; building the skills and knowledge students need to succeed.</li>
      <li><b>Personalized Support</b> &mdash; instruction tailored to each student&rsquo;s strengths, goals, and learning style.</li>
      <li><b>Confidence &amp; Purpose</b> &mdash; helping students believe in themselves while developing motivation, independence, and a love of learning.</li>
    </ul>
  </div>
  <div>__VENN__</div>
</div>"""

INCLUDED = """<section class="paper">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Included With Every Program</p>
      <h2>Every student receives</h2>
      <p>At Purpose Education, every student begins with The Purpose Plan &mdash; a personalized roadmap designed around their strengths, goals, and learning needs. From there, families choose the academic program that best supports their child&rsquo;s growth.</p>
    </div>
    <div class="incl rv">
      <div><b>A personalized Purpose Plan</b><span>Built before instruction begins.</span></div>
      <div><b>Experienced educators</b><span>Carefully selected and personally approved.</span></div>
      <div><b>Instruction tailored to goals</b><span>Aligned to each student&rsquo;s plan.</span></div>
      <div><b>Ongoing progress monitoring</b><span>Growth tracked throughout.</span></div>
      <div><b>Family communication</b><span>Clear updates and shared understanding.</span></div>
    </div>
  </div>
</section>"""

WHY_TUTORS = """<section class="cream" id="tutors">
  <div class="wrap">
    <div class="sec-head rv">
      <p class="eyebrow">Why Our Tutors</p>
      <h2>Why families choose Purpose Education</h2>
      <p>At Purpose Education, we believe exceptional tutoring begins with exceptional educators. Every tutor is carefully selected and personally approved by our Education Director to ensure families receive knowledgeable, compassionate, and highly qualified academic support.</p>
    </div>
    <div class="grid grid-3">
      <div class="card rv">
        <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 4 6 8v7c0 6 4.3 10.5 10 12 5.7-1.5 10-6 10-12V8L16 4Z"/><path d="m12 16 3 3 5-6"/></svg>
        <h3>Carefully Vetted</h3>
        <p>Every tutor is thoroughly screened for academic achievement, teaching experience, professionalism, and communication skills.</p>
      </div>
      <div class="card rv">
        <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 6 3 12l13 6 13-6-13-6Z"/><path d="M8.5 14.8V20c0 2 3.4 3.6 7.5 3.6s7.5-1.6 7.5-3.6v-5.2"/></svg>
        <h3>Personally Matched</h3>
        <p>Students are intentionally paired with tutors based on their academic needs, learning style, and goals &mdash; not simply tutor availability.</p>
      </div>
      <div class="card rv">
        <svg class="svc-icon" viewBox="0 0 32 32"><path d="M5 24V13M12 24V8M19 24v-9M26 24V5"/></svg>
        <h3>Guided by The Purpose Plan</h3>
        <p>Every tutor teaches from your student&rsquo;s personalized Purpose Plan, with ongoing support from the Education Director to ensure instruction remains aligned with each student&rsquo;s goals.</p>
      </div>
    </div>
  </div>
</section>"""

CTA_BAND = """<section class="cream">
  <div class="wrap">
    <div class="cta-plate rv">
      <img src="images/logo.png" alt="" width="64">
      <p class="eyebrow">Get Started</p>
      <h2>Create Your Student&rsquo;s Purpose Plan</h2>
      <p>Every student&rsquo;s journey begins with understanding where they are today and where they want to go. We&rsquo;ll create a personalized roadmap to help them get there.</p>
      <a class="btn btn-crimson" href="contact.html">Start Your Purpose Plan</a>
    </div>
  </div>
</section>"""


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


# Grade data — used on the homepage cards and expanded on the tutoring page.
GRADES = [
    ("PreK&ndash;2", "Building Strong Foundations",
     "Early reading, phonics, writing, foundational math, and school readiness.",
     "This stage is about confidence and fundamental skills.",
     ("Academic Support", ["Early Reading &amp; Phonics", "Reading Fluency", "Reading Comprehension",
                           "Writing Foundations", "Handwriting", "Early Math", "Homework Support"]),
     ("Development", ["School Readiness", "Learning Confidence", "Executive Function Foundations",
                      "Social-Emotional Learning", "Enrichment"])),
    ("Grades 3&ndash;5", "Strengthening Skills &amp; Independence",
     "Reading comprehension, writing, math, homework support, and study skills.",
     "Students begin transitioning from learning to read to reading to learn.",
     ("Academic Support", ["Reading Comprehension", "Writing", "Grammar", "Vocabulary",
                           "Math", "Science", "Social Studies", "Homework Support"]),
     ("Skill Development", ["Study Skills", "Organization", "Executive Function",
                            "Test Preparation", "Confidence Building", "Enrichment"])),
    ("Grades 6&ndash;8", "Preparing for High School Success",
     "Core subjects, executive functioning, organization, and academic confidence.",
     "Middle school is where organization and study habits become just as important as academics.",
     ("Academic Support", ["English Language Arts", "Writing", "Pre-Algebra", "Algebra",
                           "Geometry", "Science", "History"]),
     ("Student Success", ["Executive Function Coaching", "Study Skills", "Organization",
                          "Time Management", "Test Preparation", "High School Readiness",
                          "Academic Coaching"])),
    ("Grades 9&ndash;12", "Preparing for College &amp; Beyond",
     "Coursework support, advanced subjects, study strategies, and college admissions guidance.",
     "The focus shifts to coursework, advanced subjects, and what comes next.",
     ("Academic Support", ["English", "Essay Writing", "Algebra", "Geometry", "Algebra II",
                           "Pre-Calculus", "Calculus", "Biology", "Chemistry", "Physics",
                           "History", "Spanish"]),
     ("College &amp; Career", ["College Admissions", "College Essays", "Application Strategy",
                               "FAFSA Guidance", "Scholarship Support", "Study Skills",
                               "Executive Function Coaching"])),
]

GRADE_CARDS = '<div class="grade-grid">\n' + "".join(
    f'  <article class="grade-card rv">\n'
    f'    <span class="g-range">{r}</span>\n'
    f'    <span class="g-title">{t}</span>\n'
    f'    <p>{d}</p>\n'
    f'    <a class="textlink" href="tutoring.html">See subjects</a>\n'
    f'  </article>\n'
    for r, t, d, _s, _a, _b in GRADES
) + "</div>"

SUBJECT_BLOCKS = "".join(
    f'<div class="subject-block rv">\n'
    f'  <div class="subject-head">\n'
    f'    <span class="s-range">{r}</span>\n'
    f'    <span class="s-title">{t}</span>\n'
    f'    <p>{sub}</p>\n'
    f'  </div>\n'
    f'  <div class="subject-cols">\n'
    f'    <div><h4>{a[0]}</h4><ul>' + "".join(f"<li>{i}</li>" for i in a[1]) + '</ul></div>\n'
    f'    <div><h4>{b[0]}</h4><ul>' + "".join(f"<li>{i}</li>" for i in b[1]) + '</ul></div>\n'
    f'  </div>\n</div>\n'
    for r, t, _d, sub, a, b in GRADES
)

# --------------------------------------------------------------------------- #
# Page bodies
# --------------------------------------------------------------------------- #

INDEX = """<main id="main">
  <section class="hero">
    <div class="hero-glow" data-par="-0.10"></div>
    <img class="hero-crest" src="images/logo.png" alt="" data-par="0.16">
    <div class="wrap hero-inner">
      <div>
        <p class="eyebrow on-navy fade-up">Helping Students and Families Create a Plan With Purpose</p>
        <h1>
          <span class="ln"><span>Personalized</span></span>
          <span class="ln"><span><em>Remote Tutoring.</em></span></span>
        </h1>
        <div class="hero-rule fade-up d1"></div>
        <p class="sub fade-up d1">Personalized remote tutoring tailored to your needs, with flexible scheduling that works around your busy life &mdash; including evenings and weekends.</p>
        <div class="hero-actions fade-up d2">
          <a class="btn btn-gold" href="contact.html">Book a Free Consultation</a>
          <a class="btn btn-ghost" href="contact.html">Schedule Your First Session</a>
        </div>
        <div class="creds fade-up d3">
          <span class="creds-label">Founded by</span>
          <span class="cred"><b>Harvard</b> Graduate School of Education</span>
          <span class="cred"><b>UCLA</b> B.A. English &amp; Sociology</span>
        </div>
      </div>
      <div class="fade-up d2">
        <div class="plate-frame">
          <div class="photo-slot">
            <img src="images/logo.png" alt="" data-par="0.05">
            <span class="slot-label">Photography placeholder &mdash; student and educator working together in a remote session, warm professional environment</span>
          </div>
        </div>
      </div>
    </div>
    <div class="equation">
      <div class="wrap equation-inner">
        <span>Where Your Student Is</span><span class="arw">&#8594;</span>
        <span>What They Need</span><span class="arw">&#8594;</span>
        <span>How They Will Grow</span>
      </div>
    </div>
  </section>

  <div class="subjects" aria-label="Subjects we support">
    <div class="marquee">
      __MARQUEE__
    </div>
  </div>

  <section class="paper" style="padding-top:clamp(2.4rem,5vw,3.4rem);padding-bottom:clamp(2.4rem,5vw,3.4rem)">
    <div class="wrap">
      <div class="incl rv">
        <div><b>Personalized learning plans</b><span>Built for one student, not a curriculum.</span></div>
        <div><b>Flexible scheduling</b><span>Around your family&rsquo;s week.</span></div>
        <div><b>Remote one-on-one sessions</b><span>Nationwide, from anywhere.</span></div>
        <div><b>Evening and weekend availability</b><span>When it actually works for you.</span></div>
        <div><b>Affordable pricing</b><span>Individual and shared options.</span></div>
      </div>
    </div>
  </section>

  <section class="cream" id="difference">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">The Purpose Education Difference</p>
        <p class="diff-statement">At Purpose Education, every journey begins with a personalized plan built around each student&rsquo;s strengths, goals, and potential &mdash; because meaningful growth starts with understanding the individual. We meet students where they are and help them become who they&rsquo;re meant to be.</p>
      </div>
      <div class="pillars rv">
        <div class="pillar"><div class="pillar-mark">I</div><div>
          <h3>Individualized Planning</h3>
          <p>Every student begins with a personalized plan built around their strengths, goals, and learning needs &mdash; not a one-size-fits-all curriculum.</p></div></div>
        <div class="pillar"><div class="pillar-mark">II</div><div>
          <h3>Purposeful Growth</h3>
          <p>Every lesson has a purpose. Through targeted instruction, measurable goals, and consistent reflection, students grow academically while building the confidence and skills needed for long-term success.</p></div></div>
        <div class="pillar"><div class="pillar-mark">III</div><div>
          <h3>Family Partnership</h3>
          <p>Families remain active partners throughout the journey, with clear communication, meaningful progress updates, and a shared understanding of where their student is, what they need, and how they are growing.</p></div></div>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap split">
      <div class="rv">
        <p class="eyebrow on-navy">Watch</p>
        <h2>Meet Purpose Education</h2>
        <p class="lede">A short introduction to how The Purpose Plan works and what a remote session looks like.</p>
      </div>
      <div class="rv">
        <div class="video-frame">
          <div class="video-slot">
            <span class="play" role="button" tabindex="0" aria-label="Play video placeholder"></span>
            <span class="slot-label">Video placeholder &mdash; introduction video to be supplied</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  __FINDER__

  <section class="plate" id="plan">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">The Purpose Plan Framework</p>
        <h2>Every student&rsquo;s journey begins with a personalized plan</h2>
        <p>A personalized educational roadmap designed around each student&rsquo;s strengths, goals, and needs.</p>
      </div>
      __STEPS__
      __VENNBLOCK__
    </div>
  </section>

  <section class="cream" id="services">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Academic Programs</p>
        <h2>Support for Every Stage of Your Student&rsquo;s Journey</h2>
        <p>From early learners to college-bound students, our programs provide personalized support designed to help every student thrive.</p>
      </div>
      <div class="svc-grid featured">
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="16" cy="16" r="12"/><path d="M20.5 11.5 L18 18 L11.5 20.5 L14 14 Z"/></svg>
          <span class="badge">Signature Framework</span>
          <h3>The Purpose Plan</h3>
          <p>Personalized educational roadmap tailored to your student&rsquo;s goals, strengths, and learning needs.</p>
          <a class="textlink" href="purpose-plan.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 10c-2-2-5-2.5-8-2v13c3-.5 6 0 8 2 2-2 5-2.5 8-2V8c-3-.5-6 0-8 2Z"/><path d="M16 10v13"/></svg>
          <h3>One-on-One Tutoring</h3>
          <p>Individualized instruction designed to build confidence and academic success.</p>
          <p class="price">$85<b>/hour</b></p>
          <a class="textlink" href="tutoring.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="11" cy="13" r="3.2"/><circle cx="21" cy="13" r="3.2"/><path d="M5 24c0-3.4 2.7-5.5 6-5.5s6 2.1 6 5.5"/><path d="M15 24c0-3.4 2.7-5.5 6-5.5s6 2.1 6 5.5"/></svg>
          <h3>Purpose Pods</h3>
          <p>Collaborative small-group learning with students of similar age, subject, and goals.</p>
          <p class="price">From $55<b>/hour per student</b></p>
          <a class="textlink" href="purpose-pods.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><circle cx="16" cy="16" r="6"/><path d="M16 4v3M16 25v3M4 16h3M25 16h3M7.5 7.5l2.2 2.2M22.3 22.3l2.2 2.2M24.5 7.5l-2.2 2.2M9.7 22.3l-2.2 2.2"/></svg>
          <h3>Summer Program</h3>
          <p>Personalized summer learning that keeps students growing all season long.</p>
          <a class="textlink" href="summer-program.html">Learn more</a>
        </article>
        <article class="svc rv">
          <svg class="svc-icon" viewBox="0 0 32 32"><path d="M16 8 3 14l13 6 13-6-13-6Z"/><path d="M8.5 16.8V22c0 2 3.4 3.6 7.5 3.6s7.5-1.6 7.5-3.6v-5.2"/></svg>
          <h3>College Admissions &amp; Planning</h3>
          <p>Expert guidance for admissions, essays, FAFSA, scholarships, and future planning.</p>
          <a class="textlink" href="college-support.html">Learn more</a>
        </article>
      </div>
    </div>
  </section>

  __INCLUDED__

  __TESTIMONIALS__

  __CTA__
</main>"""

FINDER = """<section class="finder" id="finder">
    <img class="finder-crest" src="images/logo.png" alt="" data-par="0.12">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Find Your Starting Point</p>
        <h2>Not sure which plan best supports your child?</h2>
        <p>Answer three quick questions and we will show you where to begin.</p>
      </div>
      <div class="finder-card rv">
        <div class="f-progress"><i class="on"></i><i></i><i></i></div>

        <div class="f-step active" data-step="0">
          <p class="f-q">What grade is your student in?</p>
          <p class="f-hint">We support students from PreK through Grade 12.</p>
          <div class="f-opts">
            <button class="f-opt" data-k="grade" data-v="prek2"><b>PreK &ndash; Grade 2</b><small>Building Strong Foundations</small></button>
            <button class="f-opt" data-k="grade" data-v="g35"><b>Grades 3 &ndash; 5</b><small>Strengthening Skills &amp; Independence</small></button>
            <button class="f-opt" data-k="grade" data-v="g68"><b>Grades 6 &ndash; 8</b><small>Preparing for High School Success</small></button>
            <button class="f-opt" data-k="grade" data-v="g912"><b>Grades 9 &ndash; 12</b><small>Preparing for College &amp; Beyond</small></button>
          </div>
        </div>

        <div class="f-step" data-step="1">
          <p class="f-q">Not sure what support your student needs?</p>
          <p class="f-hint">Choose the area that matters most right now.</p>
          <div class="f-opts">
            <button class="f-opt" data-k="need" data-v="literacy" data-grades="all"><b>Reading &amp; writing</b><small>Comprehension, phonics, written work</small></button>
            <button class="f-opt" data-k="need" data-v="math" data-grades="all"><b>Math</b><small>Core skills and problem solving</small></button>
            <button class="f-opt" data-k="need" data-v="habits" data-grades="all"><b>Homework &amp; study skills</b><small>Organisation, routines, independence</small></button>
            <button class="f-opt" data-k="need" data-v="ahead" data-grades="all"><b>Getting ahead</b><small>Enrichment and next-grade preparation</small></button>
            <button class="f-opt" data-k="need" data-v="college" data-grades="g912"><b>College planning</b><small>Applications, essays, FAFSA, scholarships</small></button>
          </div>
          <button class="f-back" data-back>&larr; Back</button>
        </div>

        <div class="f-step" data-step="2">
          <p class="f-q">Which program suits your student?</p>
          <p class="f-hint">Based on your answers we have marked the one we would suggest &mdash; either works.</p>
          <div class="prog-grid">
            <button class="prog-card" data-k="program" data-v="solo"><span class="rec-flag">Recommended</span><b>One-on-One Tutoring</b><small>Full attention on their own plan &mdash; $85/hour</small></button>
            <button class="prog-card" data-k="program" data-v="group"><span class="rec-flag">Recommended</span><b>Purpose Pods</b><small>2&ndash;3 students, matched by grade and subject &mdash; from $55/hour per student</small></button>
            <button class="prog-card" data-k="program" data-v="unsure"><span class="rec-flag">Recommended</span><b>Not sure yet</b><small>Start with The Purpose Plan and let the assessment decide</small></button>
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
              <a class="btn btn-crimson" href="contact.html">Book a Free Consultation</a>
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
              <p class="f-price" id="resPrice">Customized pricing</p>
              <a class="textlink" id="resMore" href="purpose-plan.html" style="color:var(--gold-lt)">Read more</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>"""

TESTIMONIALS = """<section class="navy">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">In Their Words</p>
        <h2>What families say</h2>
      </div>
      <div class="tst-grid">
        <article class="tst rv">
          <span class="tq">&ldquo;</span>
          <p>Before we started working together, my child had difficulty reading and speaking English. The changes that I noticed was her English improving over time. What stood out most was your teaching style and how effective it was for my daughter.</p>
          <div class="tst-more">
            <p>You were patient, supportive, and made learning enjoyable for her. I would definitely recommend your services to others. I am very satisfied with how you taught Emma. If she ever needs a tutor again in the future, we would definitely come back to you. Thank you for all your help!</p>
          </div>
          <button class="tst-toggle" aria-expanded="false">Read more</button>
          <span class="tst-attrib">Parent of Emma</span>
        </article>
        <article class="tst rv">
          <span class="tq">&ldquo;</span>
          <p>When we moved from Argentina to Miami, my 7-year-old son, Rafa, spoke very little English. A few months into the school year, his teacher mentioned he was struggling to follow the lessons and becoming restless in class as a result. We saw progress almost immediately.</p>
          <div class="tst-more">
            <p>Nichole&rsquo;s structured method for language, pronunciation, and math made a significant difference. By the first parent-teacher conference, his teacher noted remarkable improvement &mdash; Rafa was reading at grade level, and his overall grades had improved across all subjects.</p>
            <p>Nichole is focused, methodical, punctual, and kind. She always starts each session with a brief check-in about his week to get him talking before moving into the work. I have already recommended her to a friend with a son in middle school, and she had a similarly positive experience. Her approach gave Rafa the language tools and confidence he needed to succeed in school.</p>
          </div>
          <button class="tst-toggle" aria-expanded="false">Read more</button>
          <span class="tst-attrib">Parent of Rafa</span>
        </article>
      </div>
    </div>
  </section>"""

ABOUT = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split">
      <div class="rv">
        <p class="eyebrow">Our Mission</p>
        <p class="diff-statement">Every student has a unique educational journey. We create personalized pathways that help students discover their strengths, overcome challenges, and achieve their goals.</p>
      </div>
      <div class="rv prose">
        <p class="eyebrow">Our Story</p>
        <p>Purpose Education was founded on the belief that every student deserves more than a one-size-fits-all approach. That&rsquo;s why we created The Purpose Plan &mdash; a personalized framework designed to understand each student&rsquo;s strengths, goals, and learning needs before instruction begins, creating a clear path for meaningful academic growth.</p>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap split narrow-left">
      <div class="rv">
        <div class="plate-frame">
          <div class="photo-slot light">
            <img src="images/logo.png" alt="">
            <span class="slot-label">Founder portrait placeholder &mdash; photograph to be supplied</span>
          </div>
        </div>
      </div>
      <div class="rv prose">
        <p class="eyebrow">Meet the Founder</p>
        <h2>Nichole Najera</h2>
        <p class="lede" style="margin-bottom:1.4rem">Founder &amp; Education Director</p>
        <div class="creds" style="border-top-color:var(--rule);margin-bottom:1.6rem">
          <span class="cred" style="border-color:var(--rule);color:var(--muted)"><b style="color:var(--navy)">Harvard</b> Ed.M., Education Leadership, Organizations &amp; Entrepreneurship</span>
          <span class="cred" style="border-color:var(--rule);color:var(--muted)"><b style="color:var(--navy)">UCLA</b> B.A., English &amp; Sociology</span>
        </div>
        <p>Purpose Education was founded by Nichole Najera, a classroom educator and graduate of the Harvard Graduate School of Education and UCLA. With more than eight years of experience in education, tutoring, and educational consulting, she has helped students build confidence, strengthen academic skills, and reach their academic goals.</p>
        <p>Believing that every student deserves more than tutoring, Nichole created The Purpose Plan &mdash; a personalized educational roadmap that guides every student&rsquo;s learning journey. Today, she continues to oversee the educational standards at Purpose Education, ensuring every family receives thoughtful, personalized support from the very beginning.</p>
      </div>
    </div>
  </section>

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Educational Philosophy</p>
        <h2>How We Think About Learning</h2>
        <p>Purpose Education is more than tutoring &mdash; it&rsquo;s a personalized approach to learning. We help families understand where their student is today, create a plan for where they want to go, and provide the support to help them get there.</p>
      </div>
      <div class="grid grid-2">
        <div class="card rv">
          <span class="card-no">I</span>
          <h3>Experienced Educators</h3>
          <p>Every student learns from highly qualified educators with classroom experience and a passion for helping students grow. Each tutor is carefully selected and personally approved to provide engaging, personalized instruction.</p>
        </div>
        <div class="card rv">
          <span class="card-no">II</span>
          <h3>The Purpose Plan</h3>
          <p>Every student begins with The Purpose Plan, our personalized roadmap designed around their strengths, goals, and learning needs. Instruction is intentional, individualized, and built to help every student succeed.</p>
        </div>
        <div class="card rv">
          <span class="card-no">III</span>
          <h3>Family Partnership</h3>
          <p>We believe the best outcomes happen when educators and families work together. Through ongoing communication and progress updates, we partner with parents to support each student&rsquo;s growth every step of the way.</p>
        </div>
        <div class="card rv">
          <span class="card-no">IV</span>
          <h3>Confident, Lifelong Learners</h3>
          <p>Our goal extends beyond improving grades. We help students build confidence, develop strong learning habits, and become independent learners prepared for long-term success.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv" style="margin-bottom:0">
        <p class="eyebrow on-navy">What Guides Us</p>
        <h2>Faith &middot; Excellence &middot; Purpose</h2>
        <p>[Placeholder &mdash; Purpose Education to confirm how prominently these three values should feature, and to supply a short line for each.]</p>
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
        <span class="badge badge-quiet">Signature Framework</span>
        <p class="diff-statement">A personalized educational roadmap designed around each student&rsquo;s strengths, goals, and needs.</p>
      </div>
      <div class="rv prose">
        <p>At Purpose Education, we believe every student has the potential to become more than they are today. Through individualized educational planning and personalized instruction, we help students bridge the gap between where they are and where they want to be.</p>
        <p>We are more than tutoring &mdash; we partner with families to create a custom roadmap that builds confidence, develops strengths, and empowers every learner to succeed with purpose.</p>
        <a class="textlink" href="index.html#finder">Find your starting point</a>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow on-navy">The Process</p>
        <h2>Assess &rarr; Plan &rarr; Learn &rarr; Grow &rarr; Reflect</h2>
        <p>Five stages that repeat as your student progresses.</p>
      </div>
      __STEPS__
      __VENNBLOCK__
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Investment</p>
        <h2>Investment in Your Student&rsquo;s Growth</h2>
      </div>
      <div class="price-grid">
        <div class="price-card tbc rv">
          <span class="p-label">Signature Framework</span>
          <h3>The Purpose Plan</h3>
          <span class="p-amount">Customized</span>
          <span class="p-unit">Priced to the assessment and the plan</span>
          <p>The starting point for every student.</p>
        </div>
        <div class="price-card rv">
          <span class="p-label">Individual</span>
          <h3>One-on-One Tutoring</h3>
          <span class="p-amount">$85</span>
          <span class="p-unit">per hour</span>
          <p>Individualized academic support, guided by the plan.</p>
        </div>
        <div class="price-card rv">
          <span class="p-label">Small Group</span>
          <h3>Purpose Pods</h3>
          <span class="p-amount">From $55</span>
          <span class="p-unit">per student, per hour</span>
          <p>2&ndash;3 students matched by grade, subject and goals.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="paper">
    <div class="wrap-narrow">
      <div class="sec-head rv">
        <p class="eyebrow">Common Questions</p>
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
          <summary>Are sessions remote?</summary>
          <div class="faq-body"><p>Yes. All tutoring is delivered remotely, nationwide, with evening and weekend availability.</p></div>
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

PROGRAMS = """<main id="main">
  __HERO__

  <section class="paper" id="tutoring">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">One-on-One Tutoring</p>
        <h2>Personalized. Focused. Individualized.</h2>
        <p class="lede">Our one-on-one tutoring provides customized instruction tailored to your student&rsquo;s unique learning style, pace, and goals. Every session is guided by The Purpose Plan, ensuring meaningful progress and lasting confidence.</p>
      </div>
      <div class="rv">
        <h4 style="font-family:var(--sans);font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem">Ideal for students who</h4>
        <ul class="checklist" style="margin-bottom:1.6rem">
          <li>Need individualized support</li>
          <li>Benefit from one-on-one instruction</li>
          <li>Require targeted intervention</li>
          <li>Want to accelerate learning</li>
        </ul>
        <p class="diff-statement" style="font-size:1.4rem;margin-bottom:1.4rem">Starting at $85<span style="font-size:1rem;color:var(--muted)">/hour</span></p>
        <a class="btn btn-navy" href="contact.html">Get Started</a>
        <a class="textlink" href="tutoring.html" style="margin-left:1rem">See subjects by grade</a>
      </div>
    </div>
  </section>

  <section class="cream" id="pods">
    <div class="wrap split narrow-right">
      <div class="rv">
        <h4 style="font-family:var(--sans);font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem">Ideal for students who</h4>
        <ul class="checklist" style="margin-bottom:1.6rem">
          <li>Enjoy learning alongside peers</li>
          <li>Thrive in collaborative settings</li>
          <li>Want personalized instruction at a shared investment</li>
          <li>Are working toward similar academic goals</li>
        </ul>
        <p class="diff-statement" style="font-size:1.4rem;margin-bottom:1.4rem">Starting at $55<span style="font-size:1rem;color:var(--muted)">/hour per student</span></p>
        <a class="btn btn-navy" href="contact.html">Join a Purpose Pod</a>
        <a class="textlink" href="purpose-pods.html" style="margin-left:1rem">Pod details</a>
      </div>
      <div class="rv">
        <p class="eyebrow">Purpose Pods</p>
        <h2>Collaborative Learning. Personalized Support.</h2>
        <p class="lede">Purpose Pods are intentionally designed small-group learning experiences for 2&ndash;3 students who are thoughtfully matched by grade level, subject, and learning goals. Students receive individualized instruction while benefiting from collaboration, discussion, and peer encouragement.</p>
      </div>
    </div>
  </section>

  __INCLUDED__

  __WHYTUTORS__

  __CTA__
</main>"""

TUTORING = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">One-on-One Tutoring</p>
        <h2>Personalized. Focused. Individualized.</h2>
        <p class="lede">Customized instruction tailored to your student&rsquo;s unique learning style, pace, and goals. Every session is guided by The Purpose Plan.</p>
      </div>
      <div class="rv">
        <table class="spec">
          <tbody>
            <tr><th>Grades</th><td>PreK&ndash;12</td></tr>
            <tr><th>Format</th><td>Remote, one-to-one</td></tr>
            <tr><th>Availability</th><td>Flexible scheduling, including evenings and weekends</td></tr>
            <tr><th>Begins with</th><td>The Purpose Plan</td></tr>
            <tr><th>Price</th><td>$85 per hour</td></tr>
          </tbody>
        </table>
        <a class="btn btn-navy" href="contact.html" style="margin-top:1.4rem">Get Started</a>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">By Grade</p>
        <h2>What we cover at every stage</h2>
        <p>Each stage has its own focus. Instruction is drawn from these areas and shaped by your student&rsquo;s Purpose Plan.</p>
      </div>
      __SUBJECTS__
    </div>
  </section>

  __CTA__
</main>"""

PODS = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split narrow-left">
      <div class="rv">
        <p class="eyebrow">Purpose Pods</p>
        <h2>Collaborative Learning. Personalized Support.</h2>
        <p class="lede">Purpose Pods are intentionally designed small-group learning experiences for 2&ndash;3 students who are thoughtfully matched by grade level, subject, and learning goals. Students receive individualized instruction while benefiting from collaboration, discussion, and peer encouragement.</p>
      </div>
      <div class="rv">
        <h4 style="font-family:var(--sans);font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:1rem">Ideal for students who</h4>
        <ul class="checklist">
          <li>Enjoy learning alongside peers</li>
          <li>Thrive in collaborative settings</li>
          <li>Want personalized instruction at a shared investment</li>
          <li>Are working toward similar academic goals</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">How Pods Are Matched</p>
        <h2>Purpose Pods are not general group tutoring</h2>
        <p>Students are grouped so the instruction stays relevant to everyone in the room.</p>
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
        <h2>Purpose Pod pricing</h2>
        <p>Priced per student, per hour. All sessions are remote.</p>
      </div>
      <div class="price-grid" style="grid-template-columns:repeat(2,1fr);max-width:760px;margin:0 auto">
        <div class="price-card rv">
          <span class="p-label">Small Group</span>
          <h3>2 Student Pod</h3>
          <span class="p-amount">$65</span>
          <span class="p-unit">per student, per hour</span>
          <p>Two students, same subject area and grade range.</p>
        </div>
        <div class="price-card rv">
          <span class="p-label">Small Group</span>
          <h3>3 Student Pod</h3>
          <span class="p-amount">$55</span>
          <span class="p-unit">per student, per hour</span>
          <p>Three students, same subject area and grade range.</p>
        </div>
      </div>
      <p class="svc-foot rv"><a class="btn btn-navy" href="contact.html">Join a Purpose Pod</a></p>
    </div>
  </section>

  __CTA__
</main>"""

SUMMER = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">Three Tracks</p>
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
        <p class="eyebrow on-navy">What Every Track Includes</p>
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
      <div class="sec-head rv" style="margin-bottom:1.6rem">
        <p class="eyebrow">Investment</p>
        <h2>Summer pricing</h2>
        <p>Summer packages are customized to each student&rsquo;s track and schedule.</p>
      </div>
      <div class="center rv"><a class="btn btn-navy" href="contact.html">Book a Free Consultation</a></div>
    </div>
  </section>

  __CTA__
</main>"""

COLLEGE = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap">
      <div class="sec-head rv">
        <p class="eyebrow">What We Help With</p>
        <h2>From first list to final decision</h2>
        <p>Expert guidance for admissions, essays, FAFSA, scholarships, and future planning.</p>
      </div>
      <div class="grid grid-3">
        <div class="card rv"><span class="card-no">I</span><h3>College Admissions</h3><p>Building a realistic list and a timeline that fits the student.</p></div>
        <div class="card rv"><span class="card-no">II</span><h3>Application Strategy</h3><p>Deciding where to apply, when, and how to present the student&rsquo;s strengths.</p></div>
        <div class="card rv"><span class="card-no">III</span><h3>College Essays</h3><p>Support through drafting and revision, in the student&rsquo;s own voice.</p></div>
        <div class="card rv"><span class="card-no">IV</span><h3>FAFSA Guidance</h3><p>Guidance through the financial aid application process.</p></div>
        <div class="card rv"><span class="card-no">V</span><h3>Scholarship Support</h3><p>Identifying and pursuing scholarship opportunities.</p></div>
        <div class="card rv"><span class="card-no">VI</span><h3>Academic Planning</h3><p>Course selection and preparation aligned to where the student is heading.</p></div>
      </div>
    </div>
  </section>

  <section class="cream">
    <div class="wrap">
      <div class="sec-head rv" style="margin-bottom:1.6rem">
        <p class="eyebrow">Investment</p>
        <h2>College Admissions &amp; Planning pricing</h2>
        <p>Customized to each student&rsquo;s applications and timeline.</p>
      </div>
      <div class="center rv"><a class="btn btn-navy" href="contact.html">Book a Free Consultation</a></div>
    </div>
  </section>

  __CTA__
</main>"""

CONTACT = """<main id="main">
  __HERO__

  <section class="paper">
    <div class="wrap split narrow-right">
      <div class="rv prose">
        <p class="eyebrow">Get in Touch</p>
        <h2>We would like to hear about your student</h2>
        <p>Tell us where your student is today and what you would like them to reach. Every student begins with The Purpose Plan, so the first conversation is about understanding current skills and needs.</p>
        <ul class="checklist" style="margin:1.8rem 0">
          <li><b>Remote tutoring, nationwide</b> &mdash; sessions from anywhere in the US</li>
          <li><b>Flexible scheduling</b> &mdash; including evenings and weekends</li>
          <li><b>Free consultation</b> &mdash; no cost to talk it through first</li>
        </ul>
        <div class="ph-block">
          <span class="ph">Contact details placeholder</span>
          <p><strong>Email</strong> &mdash; to be confirmed<br>
             <strong>Phone</strong> &mdash; to be confirmed<br>
             <strong>Hours</strong> &mdash; to be confirmed</p>
        </div>
      </div>
      <div class="rv">
        <div class="form-card">
          <form id="enquiry" novalidate>
            <div class="field-row">
              <div class="field">
                <label for="fname">First name</label>
                <input type="text" id="fname" name="fname" required autocomplete="given-name">
              </div>
              <div class="field">
                <label for="lname">Last name</label>
                <input type="text" id="lname" name="lname" required autocomplete="family-name">
              </div>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <input type="email" id="email" name="email" required autocomplete="email">
            </div>
            <div class="field">
              <label for="message">Message</label>
              <textarea id="message" name="message" required placeholder="Your student&rsquo;s grade, what you would like help with, and anything else we should know."></textarea>
            </div>
            <button type="submit" class="btn btn-crimson">Send Message</button>
            <p class="form-msg" id="formMsg" role="status"></p>
            <p class="form-note">We reply to every enquiry. Prefer to talk first? Ask for a free consultation in your message.</p>
          </form>
        </div>
      </div>
    </div>
  </section>

  <section class="plate">
    <div class="plate-bg" data-par="-0.06"></div>
    <div class="wrap sec-head rv" style="margin-bottom:0">
      <p class="eyebrow on-navy">Not Sure Where to Start?</p>
      <h2>Answer three questions and we will point you to the right program</h2>
      <p style="margin-bottom:1.8rem">It takes about thirty seconds.</p>
      <a class="btn btn-gold" href="index.html#finder">Find your starting point</a>
    </div>
  </section>
</main>"""

MARQUEE_ITEMS = ["Reading", "Writing", "Math", "Homework Support", "Study Skills",
                 "Grades PreK&ndash;12", "Remote Sessions", "Evenings &amp; Weekends"]
# Four repetitions: one half of the strip must exceed the widest viewport, or a
# gap opens at the end of each loop. (Reported bug — do not reduce below 4.)
MARQUEE = "\n      ".join(
    "".join(f"<span>{i}</span>" for i in MARQUEE_ITEMS) for _ in range(4)
)

# --------------------------------------------------------------------------- #

PAGES = [
    dict(slug="index.html",
         title="Purpose Education — Personalized Remote Tutoring, PreK–12",
         desc="Personalized remote tutoring for students in PreK-12, with flexible scheduling including evenings and weekends. Every student begins with The Purpose Plan.",
         body=INDEX, hero=None),

    dict(slug="about.html", title="About — Purpose Education",
         desc="Purpose Education was founded by Nichole Najera, a classroom educator and graduate of the Harvard Graduate School of Education and UCLA.",
         body=ABOUT,
         hero=page_hero("About", "Education, done <em>purposefully.</em>",
                        "Every student has a unique educational journey. We create personalized pathways that help students discover their strengths, overcome challenges, and achieve their goals.")),

    dict(slug="purpose-plan.html", title="The Purpose Plan — Purpose Education",
         desc="A personalized educational roadmap designed around each student's strengths, goals and needs. Assess, Plan, Learn, Grow, Reflect.",
         body=PURPOSE_PLAN,
         hero=page_hero("The Purpose Plan", "The <em>Purpose Plan.</em>",
                        "Every student&rsquo;s journey begins with a personalized plan &mdash; a roadmap designed around their strengths, goals, and learning needs.",
                        '<a class="btn btn-gold" href="contact.html">Start Your Purpose Plan</a>')),

    dict(slug="programs.html", title="Academic Programs — Purpose Education",
         desc="One-on-One Tutoring and Purpose Pods, plus summer and college support. Every program is guided by The Purpose Plan.",
         body=PROGRAMS,
         hero=page_hero("Academic Programs", "Every Student&rsquo;s Journey Begins <em>with a Plan.</em>",
                        "Whether your student thrives through individualized instruction or collaborative learning, every program is thoughtfully designed to help them grow with confidence, purpose, and a plan tailored to their unique journey.")),

    dict(slug="tutoring.html", title="One-on-One Tutoring — Purpose Education",
         desc="Remote one-on-one tutoring for grades PreK-12 in reading, writing, math, homework support and study skills. $85 per hour.",
         body=TUTORING,
         hero=page_hero("One-on-One Tutoring", "One-on-One <em>Tutoring.</em>",
                        "Individualized instruction designed to build confidence and academic success, guided by The Purpose Plan.",
                        '<a class="btn btn-gold" href="contact.html">Get Started</a>')),

    dict(slug="purpose-pods.html", title="Purpose Pods — Purpose Education",
         desc="Small-group remote learning for 2-3 students matched by grade level, subject and learning goals. From $55 per student per hour.",
         body=PODS,
         hero=page_hero("Purpose Pods", "Purpose <em>Pods.</em>",
                        "Collaborative small-group learning with students of similar age, subject, and goals.",
                        '<a class="btn btn-gold" href="contact.html">Join a Purpose Pod</a>')),

    dict(slug="summer-program.html", title="Summer Program — Purpose Education",
         desc="A personalized summer learning experience designed to help students strengthen skills, build confidence, and prepare for the next school year.",
         body=SUMMER,
         hero=page_hero("Summer Program", "Make This Summer <em>Count.</em>",
                        "Personalized summer learning that keeps students growing all season long.",
                        '<a class="btn btn-gold" href="contact.html">Book a Free Consultation</a>')),

    dict(slug="college-support.html", title="College Admissions & Planning — Purpose Education",
         desc="Expert guidance for admissions, essays, FAFSA, scholarships, and future planning.",
         body=COLLEGE,
         hero=page_hero("College Admissions &amp; Planning", "College Admissions <em>&amp; Planning.</em>",
                        "Expert guidance for admissions, essays, FAFSA, scholarships, and future planning.")),

    dict(slug="contact.html", title="Contact — Purpose Education",
         desc="Get in touch with Purpose Education to create your student's Purpose Plan. Remote tutoring nationwide, evenings and weekends.",
         body=CONTACT,
         hero=page_hero("Contact", "Create Your Student&rsquo;s <em>Purpose Plan.</em>",
                        "Tell us where your student is today and where they want to go. We&rsquo;ll create a personalized roadmap to help them get there.")),
]


def build():
    venn_block = VENN_BLOCK.replace("__VENN__", VENN_SVG)
    for page in PAGES:
        body = page["body"]
        body = body.replace("__STEPS__", STEPS_HTML)
        body = body.replace("__VENNBLOCK__", venn_block)
        body = body.replace("__VENN__", VENN_SVG)
        body = body.replace("__FINDER__", FINDER)
        body = body.replace("__TESTIMONIALS__", TESTIMONIALS)
        body = body.replace("__INCLUDED__", INCLUDED)
        body = body.replace("__WHYTUTORS__", WHY_TUTORS)
        body = body.replace("__GRADECARDS__", GRADE_CARDS)
        body = body.replace("__SUBJECTS__", SUBJECT_BLOCKS)
        body = body.replace("__MARQUEE__", MARQUEE)
        body = body.replace("__CTA__", CTA_BAND)
        body = body.replace("__HERO__", page["hero"] or "")

        html = head(page["title"], page["desc"])
        html += header(page["slug"])
        html += body + "\n"
        html += FOOTER

        with open(os.path.join(HERE, page["slug"]), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("built", page["slug"], len(html), "bytes")


if __name__ == "__main__":
    build()
