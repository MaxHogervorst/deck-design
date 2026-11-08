# Current deck proposal

8 November 2026. Published working proposal, not construction drawings. Supersedes earlier16-pile, small-angle, long-tread-board and flush-tread-crosspiece schedules.

| Part | Selected / proposed specification |
|---|---|
| Dimensions | Main6600×2600; rebuilt900×1970; pine tread6600×400mm. Keep surfaces about500/250mm. |
| Main framing | Double140×45 H3.2 SG8 bearers and140×45 SG8 joists. Continuous long plies cut from7.2m stock. New rear support bypasses unknown retained timber.127.8 stock lm /119.42 installed lm. |
| Main piles | Fresh20-pile proposal: six125-square H5 A-marked anchors +fourteen ordinary. Main two rowsY350/2250: X250/1067.5/1660/2967.5/3910/5130/6007.5/6525; anchors1067.5/2967.5/6007.5. Four rebuilt supportsX175/725 onY−800/−1795. |
| Main connections | Standard structural stainless nailing; six complete12KNH SS kits;14 additional genuineSSCPC40 hold-down pairs with manufacturer screws. Complete kit fit/both-ply transfer/overall bracing still require final verification. |
| Tread framing | Doubled140×45 SG8 rails, minimumH4, availableH5 suggested.19×220 lower90×45 crosspieces, bottom-flush,50mm below boards. Short400mm pine boards span directly between rails. No internal walking-load hangers, rail splices or default fascia.33.6 stock lm /30.58 installed lm. |
| Tread pads | Seven proposed500-square buried bases, bottom−450/top−100;500×400 heads to+77.25. CentresX300/1300/2300/3100/4300/5300/6300, maximum1200 interval.25MPa concrete. Full pad/any reinforcement/restraint design unfinished. |
| Tread restraint candidate |14PBB0140/SS angles, actual4mmPDS;28M12×130 timber bolts;28T12110SSX anchors. Published geometry plus favourable component screens is not a pre-rated assembly. Design hold before purchase/drilling. |
| Levels / ground | Nominal0.75mmDPC: main pile top187.25; tread concrete77.25, rail bottom78/top218, boards250. Main anchor example's lowest cut67.25 requires150 above soil: proposed under-deck soil−100 gives167.25. Only adopt lowering with a workable drainage route. |
| Ground assumption | Owner reports flat normal grassed ground and previous successful extension piles.100kPa allowable bearing is assumed for planning. No photo available or required; actual formation/outlet levels need on-site measurement. |
| Finish / process | Natural pine, exposed front rail, landscaping clear of wood. Buried tread bases may extend beyond400mm visible outline. One pre-build discussion, then one owner sequence; no construction-phase builder inspections added. |

## Lists to use

- [Shopping list with quantities, lengths, supplier links and held items](SHOPPING_LIST.md); [CSV download](docs/shopping-list.csv).
- [Exact pre-build connection checklist](PREBUILD_CHECKLIST.md): requested result is one annotated foundation/fixing drawing and fastener schedule, with manufacturer/designer support where the assembly is not pre-rated.
- [What the100mm lowering means and how to check drainage without photographs](DRAINAGE_CLEARANCE.md).
- [Full worked detail, assumptions, price evidence and sources](STANDARD_DETAILS.md).

Verified core materials subtotal$2,101.09 inclGST (boards/main framing/six kits); adding the held14-angle candidate gives$2,585.49 partial subtotal. Neither is a complete project budget; concrete, piles, tread timber, other hardware/screws, freight and ground works remain additional. No supplier contacted or purchase made.

Fresh net concrete proposal: main1.2816875 +tread0.860650 =2.1423375m³ before crowns, irregular holes and waste. About2.4m³ is a rounded10% planning allowance, not an order. Footing depths follow actual proposed ground, not an assumed unchanged lawn level.

## Checks and limits

Reproduce current stock arithmetic with `python calculations/current_takeoff.py`, component/demand screens with `python calculations/standard_details_check.py`, and the continuous-main-bearer gravity envelope with `python calculations/new_main_demand.py` (NumPy required for the last). Saved JSON accompanies each. Older structural_check.py/results.json retains its historical scope; its old tread detail is not the current pad connection.

Main preliminary gravity envelope73.95kPa against assumed100; rebuilt hold-down screen2.688kN/pair against1.0024kN demand. Current tread gravity/component screens are explicitly preliminary. Final connection/bracing/pad/load-combination verification, actual drainage outlet and merchant product/quote confirmation remain.

Selected heights remain as instructed. Nominal250mm rises exceed D1/AS1 Table6 stair limits; the applicable access approach remains unresolved. This publication establishes neither structural nor access compliance and makes no height change.
