# Purpose Education — website

Static, dependency-free site. No build step required to deploy: upload the
folder as-is to any static host.

## Structure

    index.html              Home
    about.html              About
    purpose-plan.html       The Purpose Plan
    tutoring-pods.html      Tutoring + Purpose Pods
    summer-program.html     Summer Program
    college-support.html    College Support (not in the main nav — see notes)
    contact.html            Contact / location
    css/style.css           All styles, tokenised at the top
    js/main.js              All behaviour, one file, loaded with `defer`
    images/                 logo.png, favicon.png
    build.py                Optional: regenerates pages from shared partials

## Editing navigation, header or footer

Header and footer markup is duplicated into each page deliberately — nav
injected by JavaScript is a needless SEO and no-JS risk on a site whose job is
being found by local parents.

To avoid editing seven files by hand, edit `build.py` (the `NAV` list, the
`header()` function or the `FOOTER` string) and run:

    python3 build.py

If you would rather not use the script, just edit the HTML directly; the script
is a convenience, not a dependency.

## Motion

`js/main.js`, line ~14:

    var MOTION = 'rich';        // parallax + scroll scenes
    var MOTION = 'restrained';  // layout and interaction only

`prefers-reduced-motion` is respected regardless of this setting.

## Outstanding items before launch

1. **Pricing.** Every price on the site is a "to be confirmed" placeholder.
   Two conflicting sets exist in the supplied documents: the written brief
   gives hourly rates ($85/hr, $65 and $55 per student/hr); the reference
   designs give per-session rates ($60 and $50 per student/session) plus
   packages ($320 / $600 / $840). Confirm which is current, and whether a
   session is 60 minutes.
2. **Contact.** There is no enquiry form, per client instruction. Every CTA
   currently routes to contact.html, where only placeholder details appear.
   A form is specified in the original brief (parent name, student grade,
   academic goals, areas needing support, interested services).
3. **Map.** Address unconfirmed. See the commented embed point in
   `contact.html`.
4. **About copy.** Mission, founder story and the four philosophy cards are
   marked placeholders awaiting client copy.
5. **Photography.** Every image slot is a marked placeholder. Only the logo
   is a real asset.
6. **Testimonial.** Placeholder, clearly labelled. Needs real, permitted
   parent quotes.
7. **College Support** is one of the five services but is absent from the
   client's requested six-page list. It is built and linked from the services
   grid and footer, but kept out of the main navigation. Confirm intent.
