# Deck design — preliminary; structural verification outstanding

## Status and dimensions

**CONFIRMED BY USER (handoff and subsequent replies):** freestanding main deck 6600×2600 mm, about 500 mm drop measured at the intended step location (other perimeter levels unmeasured); extension frontage 5700 mm plus rebuilt-section frontage 900 mm. The user has now supplied rebuilt-section depth **1970 mm**. Main area **17.16 m²**, rebuilt area **1.773 m²**, combined **18.933 m²** excluding stairs; main set-out diagonal **7093.66 mm**. These arithmetic checks do not verify the site or member capacities.

**PROVISIONAL:** two new double 140×45 H3.2 SG8 bearer lines, 140×45 joists, 125×125 H5 piles and a provisional 138 mm board width. **CONFIRMED BY USER:** pine decking is 38 mm thick; exact product/treatment still needs confirmation. Twelve piles and four anchors are earlier concepts, not a verified schedule.

**VERIFIED WITH PRIMARY SOURCE:** no structural or regulatory item yet. Earlier access attempts on 2026-11-03 were blocked by the environment proxy; the user subsequently published the environment, but source verification has not been repeated as part of website hosting. See [REFERENCES.md](REFERENCES.md).

## Coordinate plan

X runs along the frontage; Y increases towards the garden. Coordinates below describe finished outlines or member centre lines as labelled; never interchange these with support-face clear spans.

```text
                     REAR / HOUSE SIDE — NOT TO SCALE
 X=0            X=900                                      X=6600
 +---------------+                                      Y=-1970
 | retained      |   NEW EXTENSION
 | bearer at     |   (back extent not surveyed here)
 | back edge*    |
 | rebuilt deck  |   5700 mm frontage
 | 900 × 1970    |
 +---------------+---------------------------------------------+ Y=0
 |          full main deck: 6600 wide × 2600 deep                |
 |  o-------o-------o-------o-------o-------o  rear bearer A      | Y=350**
 |       joists run in Y; decking rows run in X                  |
 |  o-------o-------o-------o-------o-------o  front bearer B     | Y=2250**
 +-------------------------------------------------------------+ Y=2600
 |           ONE FULL-WIDTH TREAD: 6600 × 400 mm                |
 +-------------------------------------------------------------+ Y=3000
             Selected surface: 250 mm above garden; unverified
 * Exact retained-bearer centre/face offset and supports unmeasured.
 ** Proposed bearer centre lines only; not approved pile set-out.
```

| Feature | Coordinate or dimension | Status |
|---|---|---|
| Main finished outline | X=0…6600; Y=0…2600 | CONFIRMED BY USER |
| Rebuilt finished outline | X=0…900; Y=−1970…0 | CONFIRMED BY USER: depth supplied in this pass |
| Retained bearer | At rebuilt back edge, nominal Y≈−1970; exact centre/face offset, section and supports unmeasured | CONFIRMED BY USER location; structural/precise-dimension HOLD POINT |
| New bearer centres A/B | Y=350 / 2250; centre separation 1900 | PROVISIONAL |
| Proposed pile centres on each new bearer | X=250, 1470, 2690, 3910, 5130, 6350 | PROVISIONAL: five 1220 bays |
| End offset in X | 250 from finished outline to end pile centre | Geometry only; verify actual bearer end/cantilever measurement |
| Outer offset in Y | 350 from finished outline to bearer centre | Geometry only; actual joist end and bearing face differ |
| Nominal pile-top height above final soil | 500−38−140−140 = 182, before DPC and measured sizes | PROVISIONAL; varies with final grade |

With 90 mm-wide bearers centred at Y=350 and 2250, their facing edges are Y=395 and 2205: the clear gap is **1810 mm**. The 1900 mm centre separation is not that clear gap. Use the span definition required by the actual standard/table. The older 2500 mm footprint and Y=350/2150 or 400/2100 layouts are superseded.

## Rebuilt-section junction: geometry issue identified

The proposed rear bearer is at **Y=+350**, not at the finished junction Y=0. The user now places the retained bearer at the back edge of the 1970 mm section (nominal Y≈−1970). A rebuilt-section joist reaching the rear bearer therefore has about **1970+350=2320 mm support separation**. That is approximate: the actual retained-bearer centre/face offset, clear span and end bearing still need detailing.

It also occupies Y=0…350 inside the main deck. Separate main joists at the same X and elevation cannot occupy that same space. A rear rim at Y=0 may also interrupt the proposed joist path. The 900 mm strip needs its own joist alignment and junction detail before the general main-deck layout is applied there.

**HOLD POINT:** choose a coherent continuous-joist, supported joint, offset framing, or separate support solution after measuring the old bearer centre/face offsets and inspecting its supports. Check actual bearing widths, connections and framing levels; do not assume half of a 90 mm bearer is adequate bearing for either end. A continuous-joist candidate across the 900 mm strip has a **4570 mm finished envelope** (1970+2600), with supports near Y=−1970, +350 and +2250. This may avoid the overlapping separate joists, but is not a 4570 mm cut instruction. Continuous joists over multiple supports require the appropriate structural analysis; the 2320/1900 mm spans, support bearing, rims, fixing, stock lengths and revised reactions all matter. Do not cut joists, omit supports or add a pile row from this concept alone.

For the main deck alone, equal loading and the symmetric proposed two-support geometry give an equivalent reaction tributary width of **1300 mm per bearer**. This is a loading input, not a capacity check. The rebuilt strip and stair connections can change reactions; they require a combined load check rather than blindly applying a main-deck-only span table.

## Joist spacing: conditional layout arithmetic

For an example with 45 mm-wide outer joists whose outer faces are at X=0 and 6600, centre-line width is 6555 mm. Fifteen equal bays give **16 joist lines at 437 mm centres**: `X_i=22.5+437i`, i=0…15. This meets a *geometric target* of no more than 450 mm centres; the target itself still requires decking/joist source verification.

This count includes the two side edge joists. It excludes extra butt-joint supports, stair framing and any changes in the rebuilt 900 mm strip. Decking overhang, long-edge rim arrangement and real timber sizes can alter the layout. Neither 2600 mm nor 2510 mm is an approved joist cut length: define the framing envelope, board overhang and rim connections first.

## Garden access: one tread, 400 mm total run

**CONFIRMED BY USER (latest reply):** exactly **one intermediate tread**, projecting **400 mm total beyond the main deck**. The selected horizontal outline is therefore Y=2600…3000. Full width along the 6600 mm garden edge is confirmed; selected tread surface is 250 mm above garden, pending access verification. Do not replace this preference with two treads or an 800 mm run.

**HOLD POINT — vertical fit:** the user now confirms **about 500 mm measured drop at the intended step location**. One level intermediate tread creates two rises. Equal rises over a true 500 mm fall would each be **250 mm**. A 400 mm horizontal depth does not reduce those rises. This is not an accepted ordinary-stair detail; current applicable rise/going, uniformity and other access requirements have not been verified.

Let H be the **measured deck-to-finished-landing drop** and r_max the maximum riser allowed by the verified applicable stair route/category. A one-tread, two-equal-rise arrangement requires `H/2 ≤ r_max`, alongside every other stair requirement. Do not substitute a remembered value for r_max. Confirm how the 400 mm physical tread depth relates to the measured going after nosings/details.

If measured H is too large, keeping one tread and 400 mm run requires a compatible level change, such as a suitably designed raised garden landing or a different deck datum. Minimum reduction in H for the riser-height test alone is `max(0, H−2r_max)`. That inequality alone does not design the landing: check its approach, drainage, stability, cladding/threshold effects and any resulting additional level change. The user has selected the halfway tread surface at 250 mm above garden; no alteration to garden/deck datum or compliant access detail has been approved.

The earlier three-rise/two-tread/800 mm-run calculation explained a possible alternative; it is **not the user's selected layout**. The tread surface is selected at 250 mm above garden; no verified stair framing or cut list has been released. Resolve the precise finished landing datum, current D1 route/category, rise/going, pitch, nosing, uniformity, landings, slip resistance and handrails. See [SITE_MEASUREMENTS.md](SITE_MEASUREMENTS.md), M5 and M8.

## Structural details still to verify

- Current applicable NZS 3604 scope, loads, ground conditions, bearer/joist spans and cantilevers, bracing demand in both directions, pile classes and positions.
- Exact ordinary/anchor footing shape, dimensions, minimum embedment, house-footing clearance and suitable ground.
- Approved pile → double 140×45 bearer → joist connection at the measured exposed pile height; exact component schedule, corrosion class, end/edge distances and DPC.
- Double-bearer ply fastening, joins and support/joint positions; no anchor-pile splice assumed permitted.
- Existing bearer/piles: condition, grade, treatment, spans, connections, footing adequacy and combined reactions at the shared rear line.
- Door/cladding/vent/drainage clearance and structural independence from the house.

The MiTek `PB2A2B` lead and a generic “12 kN kit” label are not evidence that the proposed anchor assembly is approved. Seek the actual manufacturer detail and professional confirmation for any unresolved geometry. Previous 400 mm-hole / 500–900 mm-depth and 0.8–1.1 m³ quantities remain historical estimates, not excavation instructions.

## Current selected surface and area

One tread spans **X=0…6600, Y=2600…3000**, surface **250 mm above garden**. Its horizontal area is **2.64 m²**; main + rebuilt + tread is **21.573 m²**. Pine thickness is **38 mm** and board width remains provisional at 138 mm. The former 32 mm thickness and 188 mm stack remainder are historical; the revised nominal remainder is **182 mm** before DPC and actual sizes/site levels.
