# Purpose Education — website

Static, dependency-free site. Upload the folder as-is to any static host.

## Structure

    index.html              Home
    about.html              About (mission, Our Story, Meet the Founder, philosophy)
    purpose-plan.html       The Purpose Plan
    programs.html           Academic Programs overview + Why Our Tutors
    tutoring.html           One-on-One Tutoring (subjects by grade)
    purpose-pods.html       Purpose Pods
    summer-program.html     Summer Program
    college-support.html    College Admissions & Planning
    contact.html            Contact (enquiry form)
    css/style.css           All styles. Section 11 holds revision-2 additions.
    js/main.js              All behaviour, one file, loaded with `defer`
    images/                 logo.png, favicon.png
    build.py                Optional: regenerates pages from shared partials

## Editing navigation, header or footer

Header/footer markup is duplicated into each page on purpose — nav injected by
JavaScript is a needless SEO and no-JS risk for a site whose job is being found
by parents searching for tutoring.

Edit `build.py` (the `NAV` list, `header()`, or `FOOTER`) and run:

    python3 build.py

The script is a convenience, not a dependency — you can edit the HTML directly.

## Motion

`js/main.js`, near the top:

    var MOTION = 'rich';        // parallax + scroll scenes
    var MOTION = 'restrained';  // layout and interaction only

`prefers-reduced-motion` is honoured regardless.

## Typography

Fraunces is loaded with the SOFT (softness) axis enabled and set to 45 on all
display type — see the top of section 11 in style.css. Raise toward 100 for a
softer, inkier feel, or drop to 0 for sharper, higher-contrast letterforms.
Note: the SOFT and opsz axes change contrast and weight distribution; they do
NOT change the skeletons of f / j / p / g. If the client still objects to those
letterforms specifically, the typeface has to change.

## Revision 3 changes

* Hero reverted to the original headline, with two buttons; degree credentials
  removed from the homepage (still on About). Shield watermark moved left.
* "Local In-Person & Nationwide Online Tutoring" added under the hero buttons.
  **In-person tutoring is back on** after being removed in revision 2 — copy
  across the top bar, footer, Purpose Plan FAQ, tutoring and pods pages now
  says Boston area in person, nationwide online.
* Site header enlarged; brand name larger; nav distributed evenly.
* "Education, Done Purposefully." set to Title Case site-wide. NOTE: the
  client's document asked for ALL CAPS — Title Case was chosen against that
  instruction. Same for keeping "Schedule Your First Session", which the
  document asked to remove.
* Five-feature strip removed from the homepage. It is commented out in
  `build.py`, not deleted — search for "Feature strip".
* Purpose Education Difference: new copy, "Learn More" button, pillars
  renumbered 01/02/03 with new headings.
* Purpose Plan framework AND the Venn removed from the homepage entirely.
  Both still appear on purpose-plan.html.
* Services grid and "Included With Every Program" moved to programs.html,
  ordered: plan-first CTA, Included, then the services grid.
* Finder rebuilt as three steps — Grade Level, Focus Area, Recommendation —
  with a labelled progress track. The programme-selection step from revision 2
  is gone. Step 2 is now four focus-area cards with sub-lists.
* Testimonials: seven in a carousel under "Stories of Growth and Impact", each
  with Read more. Two share the attribution "Parent of 1st Grade Student" —
  as supplied.
* Homepage final CTA replaced with "Your Child's Future Deserves More Than
  One-Size-Fits-All Support".
* About rebuilt: mission, Our Story, Meet the Founder (credentials kept),
  philosophy with the shortened description, and a six-item trust bar.
  "Hundreds of Students Supported" softened to "Students Supported".
  Founder experience set to 8+ years everywhere (the client's own stats bar
  said 7+).
* Contact form rebuilt with structured fields — name, email, child age, grade,
  subject, hours, format — plus a Nearest Library field that appears only when
  "In-person" is selected. The free-text message box was removed at the
  client's request.
* Footer: info@thepurposeeducation.com added.

## Fixed in revision 2

* Logo no longer clipped — re-extracted with the full shield (was cropped at
  row 964 of 1122; the clean gap above the strapline is at 998–1016).
* Subject marquee no longer leaves a blank gap — the strip now repeats four
  times so that one half always exceeds the widest viewport. Do not reduce
  the repetitions in `MARQUEE` below 4.

## Photography

The hero and About image slots are wired for real photos but ship as
placeholders. Licensed images cannot be sourced here. Drop a licensed file in
as `images/hero.jpg` or `images/about.jpg` and swap the two commented lines in
the relevant `.photo-slot` block in `build.py`, then re-run the build.
Free commercial-use sources: Unsplash, Pexels. Search "tutor student desk
natural light".

## Outstanding before launch

1. **Form submission is not connected.** `js/main.js` validates the fields and
   then shows a notice saying nothing was sent. Pick an endpoint (Formspree,
   Netlify Forms, EmailJS or a custom POST) — see the commented SUBMISSION
   POINT block in the form module.
2. **Social URLs** are `href="#"` placeholders. Facebook, Instagram and
   LinkedIn icons appear in the top bar and footer.
3. **Phone and hours** are still "to be confirmed". Email is live:
   info@thepurposeeducation.com
4. **Photography** — hero image, founder portrait and the video are all marked
   placeholders. The logo is the only real asset supplied.
5. **Video** — placeholder player only. Swap the `.video-slot` contents for a
   YouTube/Vimeo iframe or a `<video>` element when the file exists.
6. **Faith / Excellence / Purpose** — the About page section is a placeholder.
   The client has not said how prominent these values should be or supplied
   copy for them.
7. **Testimonials publish the first names of five children** (Emma, Rafa,
   Jordan, Ivy and Robert), with Rafa's age, country of origin and city. Keep the written parental
   permission on file; it should cover the identifying details, not just the
   quote text.
8. **Founder credentials** (Harvard GSE Ed.M., UCLA B.A., 8+ years) are
   published as supplied. Purpose Education owns their accuracy.
9. **"Nationwide online"** appears in the top bar, footer, About trust bar and
   contact page. Confirm the claim holds for every US state. Separately,
   confirm what "Boston area" covers for in-person — no address or radius has
   been supplied, and the contact form asks the parent for their nearest
   library instead.
10. **Progress review cadence** — one FAQ answer on the Purpose Plan page is
    still a placeholder.
