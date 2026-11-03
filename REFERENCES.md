# References and provenance

These links are **research leads** from the earlier conversation. Current accuracy, applicable edition and document availability must be checked before reliance.

## Authoritative / primary documents to review
- BRANZ — free-standing timber decks: https://www.branz.co.nz/design-build/articles/free-standing-timber-decks
- BRANZ — deck bracing design: https://www.branz.co.nz/design-build/articles/deck-bracing-design
- MiTek NZ — 12 kN pile fixing product/detail: https://mitek.co.nz/products/subfloor-and-slab-fixings/12kn6knpf/
- MiTek NZ — LUMBERLOK 12 kN Pile Fixing PDF (reference only; read source even though **project output must stay Markdown**): https://miteknz.co.nz/wp-content/uploads/2024/03/12kN-Pile-Fixing_2024-v1.pdf
- NZS 3604 Timber-framed buildings: consult the current applicable standard and any relevant amendments via authorised access; a web article is not a substitute for the tables.
- Auckland Council / MBIE: verify current consent and barrier requirements for actual height and site.

## Builder conversation: user-supplied transcript (2026-11-02)
Scott discussed approximately 1.2–1.3 m bearer spans, six pile positions per 6.6 m bearer line, 140×45 timber for both joists and bearer layer, and deduction of decking 32 + joist 140 + bearer 140 for pile height. He suggested generally 600 deep by roughly 400 square holes; this is **informal advice**, not a structural footing schedule. He advised ~10–12 mm wall gap, checking real timber dimensions, long straightedges, level and string lines, avoiding narrow final board and allowing for wet decking shrinkage. User clarified afterward that bearers are **double** 140×45.

## Pricing provenance
- User-pasted renovation invoice dated 2026-09-04: H5 piles, some H3.2 timber and concrete supplier prices.
- Attached/available invoice from 2026-10-06: 140×45 H3.2 SG8 × 4.8m at $38.02 ex GST, various fixings.
- Historical prices are stored in `MATERIALS.md`; no personal invoicing, bank or address details are required in this project.

## Known issues with preceding assistant responses
- Claimed anchor count and connection compliance before verifying full design.
- Mixed several pile row positions, cantilever assumptions, and unsupported concrete quantities between revisions.
- Gave earlier cutter/shop quantities that may not yield the stated assembly.
- A generic rendered image of a connection is **not** a manufacturer's certified installation drawing.
- Earlier offered a PDF document, but **the original handoff intentionally contained Markdown only; the user later requested a website**.

## New geometry source (2026-11-03)
User provided a site photograph and multiple clarifications: extension frontage 5700 mm, demolished old deck frontage 900 mm alongside extension, new deck 6600×2600 mm full rectangle, 400 mm garden-side step, retained old bearer parallel to frontage and candidate support shared with new rear bearer. These are user-reported site facts, not surveyed or verified dimensions.

## Verification log — 2026-11-03

**No current structural or regulatory requirement was verified with a primary source in this pass.** Existing linked articles, manufacturer details and remembered rules remain leads. The site photograph and original invoices described in the handoff are not present in this repository/ZIP, so they have not been independently inspected here.

| Attempted host | Operation | Observed result | Consequence |
|---|---|---|---|
| mitek.co.nz | HTTPS read of the pile-fixing product URL above through configured proxy | CONNECT tunnel failed, HTTP 403 Forbidden | No product detail or applicability read |
| www.building.govt.nz | HTTPS read through configured proxy | CONNECT tunnel failed, HTTP 403 Forbidden | No current MBIE exemption, D1 or F4 text read |
| www.aucklandcouncil.govt.nz | HTTPS read through configured proxy | CONNECT tunnel failed, HTTP 403 Forbidden | No Auckland deck/planning requirements read |

Default-sandbox commands could not reach the proxy; permitted elevated commands reached it and received the policy denials above. TLS verification remained enabled. These are access results, not evidence that a page is absent or that a particular design complies.

Historical environment draft change: added **mitek.co.nz, miteknz.co.nz, www.branz.co.nz, www.building.govt.nz, www.aucklandcouncil.govt.nz, www.legislation.govt.nz, www.standards.govt.nz**, preserving the existing package-manager preset. The user subsequently confirmed environment publication. These earlier results are historical; no further environment configuration changes are requested or applied by website deployment, and structural-source verification has not been repeated. The four other host additions have not been tested in this pass. If a legitimate source redirects to another host, inspect and add only the needed destination through environment settings.

### Next primary-source checks (unread leads, not citations proving compliance)

| Source / route | Specific check to record |
|---|---|
| [MBIE exempt-work guidance §13.3](https://www.building.govt.nz/projects-and-consents/planning-a-successful-build/scope-and-design/check-if-you-need-consents/building-work-that-doesnt-need-a-building-consent/technical-guidance-for-exempt-building-work/13-support-structures/133-decks-platforms-bridges-boardwalks-etc) | Current conditions for decks/platforms; compare actual maximum fall/site conditions rather than only nominal height |
| [Building Act 2004, official legislation](https://www.legislation.govt.nz/act/public/2004/0072/latest/whole.html) | Current Schedule 1 clause 24 exemption and section 17 Code compliance; verify current wording |
| [MBIE D1 Access Routes](https://www.building.govt.nz/building-code-compliance/d-access/d1-access-routes) | Current applicable D1/AS1 version, relevant stair category, rise/going, nosing/pitch, uniformity, width, landing, handrail and slip-resistance details |
| [MBIE F4 Safety from Falling](https://www.building.govt.nz/building-code-compliance/f-safety-of-users/f4-safety-from-falling) | Barrier trigger and fall measurement/application; keep stair handrail check separate |
| [Auckland Council deck guidance](https://www.aucklandcouncil.govt.nz/building-and-consents/building-renovation-projects/Pages/build-deck.aspx) | Building and planning/site restrictions, relevant overlays/coverage/boundary and service constraints |
| BRANZ links above; authorised NZS 3604 access via [Standards NZ](https://www.standards.govt.nz/) | Applicable edition/amendments, good-ground/scope limits, loads, support/span/cantilever definitions, bracing/pile tables and installation details |
| MiTek links above | Exact connection including doubled 140×45 bearer, 125×125 pile, actual exposure/DPC/corrosion class, anchor designation, fixings, minimum edges and splice restrictions |

For each successful check, record **title, issuer, edition/date/amendments, URL, section/page/detail number, applicable assumptions, the actual supported conclusion, and unresolved exclusions**. A source's publication date alone does not prove that it is the applicable compliance document. Authorised standards access may still be needed even after network access is restored.

### Evidence classification

- **CONFIRMED BY USER:** facts/preferences reported in the uploaded handoff, not newly surveyed here.
- **PROVISIONAL:** chosen-for-calculation geometry or product scenarios; not construction instructions.
- **VERIFIED WITH PRIMARY SOURCE:** reserved for a claim whose current applicable source was actually read and recorded; none yet.
- **HOLD POINT:** missing site facts, source access or professional/manufacturer assessment needed before the affected design can be fixed.
- Independently recalculated arithmetic is labelled as such and does not substitute for primary-source structural verification.

## Latest user design evidence

The website conversation confirms full-width **6600×400 mm** tread, selected halfway surface at **250 mm**, and **38 mm-thick pine decking**. These are owner choices, not independently verified engineering requirements. Old 32 mm thickness and 188 mm pile remainder are superseded; revised arithmetic gives 182 mm before DPC and actual sizes/levels.
