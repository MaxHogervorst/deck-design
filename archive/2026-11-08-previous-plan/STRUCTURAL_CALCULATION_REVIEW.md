# Preliminary structural calculation review

**SUBSEQUENT OWNER CLARIFICATION:** underground tread footings may extend beyond the visible400 mm tread beneath the path/grass/garden. See TREAD_LANDSCAPING_BRIEF.md. Old within-footprint restrictions and the resulting14-post/small-footing proposal are superseded as current recommendations. This does not retrospectively approve the structural details below.

8 November2026 (Auckland). **Demand calculations and prescriptive comparisons, not construction approval or a certified structural design.** The owner requested the structural check. No website changes or further publication are made in this pass.

## What this check establishes

The selected main framing has favourable published span comparisons. A conservative gravity-pressure screen is below the assumed good-ground allowable pressure. Gross earthquake bracing capacity would exceed the calculated demand **if the six anchors and their complete connections actually qualify**.

The tread/deck connections are **not cleared**. Actual calculations identify amplified bolt forces, possible joist uplift and a missing demonstrated tread-overturning load path. The earlier1.8 kN deck concentrated-load basis is insufficient for checking a domestic stair tread: the stair category has a2.7 kN concentrated action. There is also a separate independent-tread line-load provision to classify and check.

The owner asked why the selected box became a two-wide-bearer arrangement. The change removed crosspieces; it was not necessary merely to gain clearance. Reducing framing depth140→90 gives the50 mm clearance gain in either concept. **No structural calculation has established that the two-bearer scheme is better overall, or rejected the ordinary box.** The website is a published development proposal; that publication is not a structural selection or approval. No new tread configuration is selected by this check.

## Assumptions and calculation method

- Main deck6600×2600; rebuilt900×1970; tread6600×400. Existing support coordinates and candidate main splice atX3910 retained.
- Main joists45 wide ×140 deep, maximum380 mm tributary width. Main bearers90 wide ×140 deep,125-square piles. No unverified decking strength is assigned.
- Main live action2.0 kPa; deck concentrated action1.8 kN. Point action and distributed live action are **separate alternative cases**.
- Main permanent-action allowance0.6 kPa, increased from the previous0.4 kPa screening value. This is an assumption, not a measured product weight. Installed framing volume119.42×0.14×0.045=0.752346 m³, plus the board volume, shows why the weight allowance deserves attention. Joist/bearer self-weight cannot be counted twice in a final load take-down.
- Immediate stiffness usesE=6.5 GPa as a wet SG8 reference. Actual structural timber must be correctly verified/marked for its service condition.
- Gravity strength-demand screen uses1.2G+1.5Q. For conservative uplift demand an additional **zero favourable dead-load credit** case is reported, not described as a separate verified code combination.
- Euler–Bernoulli elastic beams, ideal rigid vertical bearings and free support rotation. Main normal joist model supportsY350/2250; continuous rebuilt supportsY−1795/−800/350/2250. Loads over the finished surface envelope are an equivalent simplification; rim flexibility and connections are not modelled as a coupled grillage.
- Distributed live load is patterned by support span/overhang; point load is swept along one joist without credit for transverse sharing. Negative bearing reactions are required tie-down forces: the model does not manufacture hold-down resistance.

Reproducible calculation: [calculations/structural_check.py](calculations/structural_check.py); output [calculations/results.json](calculations/results.json). RequiresNumPy. The simple-beam uniform-load reactions, moment and deflection match closed-form references; force equilibrium residuals are below10⁻⁷ kN. Halving the joist point-load mesh spacing changed checked moments/deflections by less than1%. These checks validate the computation, not the physical design assumptions or compliance.

## 1. Main gravity framing

| Check | Result | Interpretation |
|---|---:|---|
| Main joist support spacing |1.90 m versus published2.50 m wet SG8 at400 centres | Favourable span comparison; actual380 centres |
| Main joist projection to finished edge |350 mm versus published1150 mm balcony comparison without cantilevered barrier | Favourable numerical comparison; rim/end connection remains separate |
| Main bearer support bays |1.22 m versus1.30 m published comparison | Favourable, with properly connected built-up plies |
| Rebuilt continuous support bays |0.995 /1.15 /1.90 m | All below the corresponding2.50 m joist span comparison |
| Main immediate full-distributed-load deflection |2.10 mm in the equivalent beam model | No creep, vibration, point-load deflection approval or support flexibility included |
| Rebuilt immediate full-distributed-load deflection |1.27 mm | Same limitations |
| Main normal joist maximum calculated factored moment |0.621 kNm patterned distributed case;1.389 kNm concentrated case | **Demand**, not a passed strength utilisation ratio |
| Rebuilt continuous maximum calculated factored moment |0.479 kNm distributed;1.080 kNm concentrated | Demand only; requires actual member/service factors and connections |

The previous1.525 m approximate loaded dimension at the main rear bearer should not be used uncritically for the continuous rebuilt joists. Their maximum patterned factored reaction at that bearer is2.809 kN for a380 mm tributary strip, equivalent to about1.987 m loaded length under the adopted uniform action intensity. **Use2.0 m as a gravity-reaction screening envelope there.** That is still below the published3.0 m loaded dimension for the140×90 bearer at1.30 m spacing. The2.0 m envelope was conservatively extended over the entire bearer for the foundation screen below.

Do not label all member strengths passed from gross stresses alone. Grade strengths are characteristic, and design needs the applicable duration, sharing/stability, moisture and strength factors. Prescriptive-table comparisons also depend on their scope and load assumptions. In particular, a single-joist point-load model does not capture a deck's real load sharing.

## 2. Main footing gravity pressure — conditional result

The main bearer was split into two elastic parts at its proposedX3910 full-ply butt joint, avoiding artificial moment continuity at that splice. Uniform live action was patterned by span; a separate point-reaction envelope used3.0 kN service /3.7 kN factored at any location, conservatively covering the computed main/rebuilt single-joist reactions.

With2.0 m loaded length,0.6 kPa permanent action and2.0 kPa live action:

- Largest calculated service pile reaction: **7.884 kN** under the distributed pattern envelope.
- Largest point-case service reaction:4.784 kN under the stated conservative point envelope.
- Add2.467 kN for the proposed deepest square footing and pile self-weight, without credit for displaced soil.
- Pressure on350×350: **(7.884+2.467)/0.1225 =84.5 kPa**.

This is below the **assumed100 kPa allowable good-ground bearing pressure**. It is a conditional gravity-pressure result, not evidence that the actual soil is good ground. It does not check lateral soil resistance, overturning, uplift, settlement, ground movement, existing-foundation interference or every rebuilt/tread footing. No new concrete order is issued.

## 3. Global earthquake bracing — ample gross rating, incomplete system check

For an AucklandEQ-zone1 screening assumption and the conservativeD/E soil-class multiplier0.5 from Table5.8:

Area =17.160+1.773+2.640 =**21.573 m²**.

Required reference bracing =21.573×7.5×0.5 =**80.9 BU in each direction**.

Six fully qualifying anchor piles would nominally provide6×120=**720 earthquake BU**. Even the zone3/reference multiplier1.0 would give161.8 BU demand, below that gross sum.

**This does not pass the complete bracing system.** The anchor rating depends on good ground, correct footing/pile class, complete rated pile→both bearer plies→joist connections, distribution/minimum-bracing provisions, torsion and load transfer from the rebuilt strip and tread. Ordinary slatted decking must not be assumed to act as a verified diaphragm. Wind/site classification and any applicable wind actions are not resolved by this earthquake arithmetic. The tread connection must transfer demand to the braced main frame.

## 4. Rebuilt joists can require hold-down

With a1.8 kN deck point action swept through the continuous rebuilt joist model, the factored reaction at the intermediateY−800 bearer reaches **−0.644 kN** with the adopted dead load included. With no favourable dead-load credit, the largest negative point-load reactions are approximately:

| Support | Required upward-restraint demand in that conservative case |
|---|---:|
| BR atY−1795 |0.282 kN per modelled joist |
| BC atY−800 |0.888 kN |
| BA atY350 |1.002 kN |
| BB atY2250 |0.095 kN |

These minima occur at different point-load locations; do not add them as simultaneous uplift. They show that simply resting the continuous joists on bearers is not the full design. A documented vertical hold-down resistance of at least the calculated demand is needed at the applicable bearings, with the actual governing combinations confirmed. The ordinary nail schedule may be a valid prescriptive route, but this calculation has not assigned it an invented numerical withdrawal rating. Horizontal12 kN kit ratings must not automatically be treated as vertical uplift ratings.

## 5. Existing drop-cleat proposal: force amplification must be designed

This checks the already-proposed190×45 vertical cleat, upper bolt row+380, lower row+173, two upperM10 bolts75 mm apart, cleat top+468. It is **not** selection or approval of this connection.

For a1.0 kN horizontal action normal to the deck edge at the lower bolt row:

- Vertical offseth=207 mm; top contact lever arma=88 mm.
- Moment at the upper row =**0.207 kNm**.
- If the cleat's upper end bears against a sound continuous packed rim face, equilibrium requires upper contact compressionC=Fh/a=**2.352 kN** and upper bolt-group tensionT=F+C=**3.352 kN**.
- With equal sharing between the two upper bolts, that is **1.676 kN axial tension per bolt**, not0.5 kN shear.
- Gross cleat bending stress is3.23 MPa. Net-section effects, holes, wood service factors, washer bearing, splitting and the rim load path are not verified by this gross stress.

For a1.0 kN action along the deck edge, the same207 mm offset creates an in-plane moment. A simple elastic two-bolt group with75 mm horizontal spacing develops an extreme per-bolt resultant of approximately **2.805 kN**, including direct shear. That figure also needs an actual wet timber joint resistance check.

These action levels are sensitivity cases, not a finished governing lateral demand. The equivalent tread earthquake contribution under the chosen bracing screen is0.99 kN **for the entire tread**. Equal load sharing between four cleats is not established. Wind, overturning, connection stiffness and framing distribution can change the controlling forces.

The equilibrium model assumes a real compression-contact block at the cleat top. A small washer-only pack at the bolt row does not establish the88 mm contact arm. The main rim must also transfer the couple into the main joists/bearers. Its ordinary two-end-nail joints have not been demonstrated to supply that whole path. **The proposed M10 joint therefore remains unapproved; a bolt steel-strength check alone would be insufficient.**

## 6. Tread-specific gravity correction and screening

Published manufacturer reproductions of AS/NZS1170.1 Table3.1 distinguish1.8 kN general deck/balcony actions from **2.7 kN for domestic stairs/landings**. The earlier tread screen must be corrected. The cited table also includes a **2.2 kN/m of span** provision for a structurally independent tread/landing; its precise applicability and placement in this framed system need confirmation from the complete applicable loading standard. No riser-height discussion is reopened.

As a conservative member screen, put the entire2.7 kN point action on one simply supported1025 mm rail bay:

M*=1.5×2.7×1.025/4 =**1.038 kNm**, before permanent load.

- A single90×45 rail hasZ=60,750 mm³ and gross bending stress **17.1 MPa**.
- A90-deep×140-wide built-up bearer hasZ=189,000 mm³ and gross stress **5.49 MPa** under the same screen.

This explains why a shallow box cannot simply be assigned single90×45 rails at the published post intervals without checking continuity, load distribution, actual member resistance and joints. **It is not proof that a properly designed box is unsuitable.** These rail intervals belong to the two-bearer proposal, not an already-resolved box support layout. No grade is assigned to the pine decking from its species/thickness alone.

## 7. The tread also needs an overturning load path

In a centreline-support idealisation of the published two-bearer tread, pile rows arey120/280 and the front edge isy400. A2.7 kN point action at the front edge gives static row reactions:

Rfront=2.7×(400−120)/(280−120)=**4.725 kN**;
Rrear=2.7−Rfront=**−2.025 kN**, before dead weight and redistribution.

Actual broad bearing, pile-head moment resistance, board load distribution and soil reactions can change these forces. Those effects have not been designed. Thus the narrow tread cannot be treated as pure vertical gravity support with an arbitrary sideways screw attachment.

For sensitivity only, interpreting the independent-tread line provision as a simultaneous2.2 kN/m front-edge line across6.6 m gives14.52 kN total,25.41 kN front-row reaction and10.89 kN rear-row uplift in that same idealisation. **Do not present that placement as a confirmed mandatory load case for every framed tread**; it illustrates why loading classification and the overturning model must be settled before release.

No safe tensile/overturning capacity has been assigned to the200-square ordinary footings, their pile-head joints or the tread ties. A real resistant moment/hold-down path must be shown, rather than assuming soil fixity or a fully working diaphragm.

## 8. Anchor and splice detailing: scope still open

The published MiTek12 kN anchor and splice assemblies provide legitimate rated routes when installed within their scope. The main splice locationX3910 remains correctly on ordinary supports, away from the candidate anchors. Both-ply force transfer, full specified nailing, actual plate fit, anchor scarf/face geometry, lowest pile processing height and hardware clashes must be drawn and verified for this project. The square-pile scarf callout is25 degrees, not25 mm.

No numerical bolt-group or custom angle capacity has been fabricated here. No supplier/engineer has been contacted. A complete connection resistance cannot be established by adding nominal nail counts or comparing a characteristic steel rating directly with a wet-service design demand.

## What remains necessary for an overall pass

1. A resolved tread frame/support/overturning system, including2.7 kN point action and the applicable line-load case. The ordinary box has not been rejected and the two-bearer substitute has not been proved better.
2. The complete anchor, splice, joist hold-down and tread-tie resistance/load-transfer details, using the actual timber and product ratings.
3. Physical bearing ground, spot levels/drainage, actual supplied timber/boards and applicable site/wind data. These cannot be established from the repository alone.

The review has produced useful calculations and specific design demands. **The whole deck/tread has not passed a complete structural verification.** Do not use this report to pour, drill or purchase from the provisional schedules.

## Primary sources

- NZS3604:2011 full teaching copy, especially§§5.3/5.5/6.9/6.12/7.1/7.4 andTables5.8/6.4/7.1/7.5: https://moodle.unitec.ac.nz/pluginfile.php/358840/mod_resource/content/1/NZS-3604.2011%20.pdf . Current cited-standard modifications remain applicable.
- B1/AS1, including good-ground definition/100 kPa allowable reference and timber modifications: https://www.building.govt.nz/assets/Uploads/building-code-compliance/b-stability/b1-structure/asvm/b1-structure-as1-second-edition.pdf .
- Northpine wet-service member tables: https://www.northpine.co.nz/span-tables .
- Verified Timber wet SG8 grading values: https://www.verifiedtimber.co.nz/grading-timber .
- James Hardie manufacturer loading-table reproduction,pp2/4, domestic stairs and independent-tread note: https://assets.ctfassets.net/rg5y8r6t6cjr/uwkHDGweVeRqWoc0TYNGy/ee3c4394443fd7332fb0d2e5cdc462a1/Floor_Loading_Solutions_Technical_Supplement_220421.pdf . These are loading references, not an approval to substitute pine for a Hardie flooring product.
- NZ manufacturer confirmation of domestic stair point-load distinction: https://www.viridianglass.co.nz/wp-content/uploads/2020/01/Glass-floor-and-stair-tread.pdf ,p1notes2/3. Glass thickness/design provisions are not used for timber.
- MiTek anchor/splice and characteristic-capacity interpretation: https://mitek.co.nz/wp-content/uploads/2024/03/12kN-Pile-Fixing_2024-v1.pdf ; https://mitek.co.nz/wp-content/uploads/2024/03/12kN-Bearer-Splice-Over-Pile_2024-v1.pdf ; https://mitek.co.nz/wp-content/uploads/2021/06/LUMBERLOK-Timber-Connectors-Characteristic-Loadings-Data.pdf .
