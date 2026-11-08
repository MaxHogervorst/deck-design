"""Working demand/component screens, NOT a construction approval.

Explicit assumptions: 100 kPa allowable bearing on ordinary good ground;
3 kPa net design wind envelope (not a site wind calculation); 3 kPa stair
area load, alternative 2.7 kN point and 2.2 kN/m line. See STANDARD_DETAILS.md.
"""
import json
import math
from pathlib import Path

# Proprietary joist hold-down. MiTek characteristic-load sheet, p4.
# Use the lower screw/other-fastener phi and green-timber factor for the
# whole tested pair; permanent-duration k1 is conservative for imposed uplift.
cpc_characteristic = 8.0  # kN per PAIR SSCPC40 (not thin SSCPC40S)
cpc_design_screen = cpc_characteristic * .7 * .6 * .8
uplift_demand = 1.0023709627469728  # earlier continuous-joist zero-G screen

# Fresh main support layout to develop complete standard kits at ordinary joists.
# Four extra ordinary piles replace awkward end/sister-joist anchor locations.
main_x = [250,1067.5,1660,2967.5,3910,5130,6007.5,6525]
anchor_x = [1067.5,2967.5,6007.5]
bracing_joist_pairs = [(877.5,1257.5),(2777.5,3157.5),(5817.5,6197.5)]
assert all(abs((a+b)/2-c)<1e-9 for (a,b),c in zip(bracing_joist_pairs,anchor_x))
assert max(b-a for a,b in zip(main_x,main_x[1:]))<=1650
assert min((b-a-45-100)/2 for a,b in bracing_joist_pairs)>=85
assert main_x[0]-62.5<=300 and 6600-main_x[-1]-62.5<=300
main_ordinary = 10+4  # main two rows, plus four rebuilt ordinary supports
main_anchor = 6
main_concrete = main_anchor*(.35*.35*.9-.125*.125*.8) + main_ordinary*(.35*.35*.45-.125*.125*.35)

# Seven trial monolithic mass-concrete pads; formed head fits visible tread.
# Units m / kN. The footing is an explicit design proposal, not NZS3604 Table6.1.
base_w = .5
base_depth = .45
buried_base_top = -.1
head_x, head_y, head_top = .5, .4, .07725
base_thickness = base_depth + buried_base_top
head_height = head_top - buried_base_top
pad_volume = base_w**2 * base_thickness + head_x*head_y*head_height
pad_weight = 24 * pad_volume
tributary_length = 1.1  # maximum tributary length in the revised 1.2 m maximum grid
timber_G = .6 * .4 * tributary_length  # generous frame/board allowance
G = pad_weight + timber_G
q_allow = 100  # assumed, not site-tested

def bearing(N, M):
    """SLS eccentric resultant; no-tension contact over square footing."""
    e = abs(M/N)
    assert e < base_w/2, "Resultant outside footing"
    if e <= base_w/6:
        return {"eccentricity_mm": e*1000, "contact_width_mm": base_w*1000,
                "max_kPa": N/base_w**2*(1+6*e/base_w)}
    contact = 3*(base_w/2-e)
    return {"eccentricity_mm": e*1000, "contact_width_mm": contact*1000,
            "max_kPa": 2*N/(base_w*contact)}

gravity = {
    "area_3kPa": bearing(G+3*.4*tributary_length, 0),
    "point_with_1_5_reaction_allowance_at_front_edge": bearing(G+1.5*2.7, 1.5*2.7*.2),
    "line_with_1_2_reaction_allowance_at_front_edge": bearing(G+1.2*2.2*tributary_length, 1.2*2.2*tributary_length*.2),
}

# Wind envelope: entire solid 140-deep face at 3 kPa and 400-wide plan uplift.
# Taking BOTH simultaneously is an explicit envelope, not derived pressure coefficients.
wind_pressure = 3.0
W_up = wind_pressure*.4*tributary_length
W_H = wind_pressure*.14*tributary_length
W_M = W_H*(.148+base_depth)
remaining_N = .9*G-W_up
overturning_reserve = remaining_N*base_w/2-W_M

# Frame load at front board edge relative to rail centrelines y45/355.
rear_rail_uplift_from_point_ULS = 1.5*2.7*.045/.310
wind_per_angle_up = W_up/2
wind_per_angle_H = W_H/2
# Sensitivity combination, not an assertion of the final code combination.
rail_up_combo = wind_per_angle_up + .4*rear_rail_uplift_from_point_ULS

# PBB0140/SS: two outer timber bolts and two outer concrete anchors.
# Actual PDS4mm, not the retailer title's5mm. Use170MPa, lower than nominal304.
# This is a component screen, not a tested assembly rating.
fy_min_assumed = 170
phi_steel_screen = .9
b, t, holes = 140, 4, 3*13
M_foot_capacity_Nmm = phi_steel_screen*fy_min_assumed*(b-holes)*t*t/6
M_foot_demand_Nmm = rail_up_combo*1000*25 + wind_per_angle_H*1000*50
bolt_bottom_edge = 50-.75
assert bolt_bottom_edge>=4*12
support_x=[300,1300,2300,3100,4300,5300,6300]
angle_x=[300,1400,2400,3160,4300,5200,6300]
nog_x=[22.5+380*i for i in range(18)]+[6577.5]
assert all(abs(a-c)>(140+45)/2 for a in angle_x for c in nog_x)
assert max(b-a for a,b in zip(support_x,support_x[1:]))==1200
assert all(abs(a-s)<=100 for a,s in zip(angle_x,support_x))

# Ramset T12110SSX, Le85 minus4mm fixture = h81, drill min90, SS torque75Nm.
# Conservatively retain the manufacturer's M12/h70 baseline capacities;
# calculate edge/spacing reductions using the greater actual h81.
# This does not replace ETA checks for multiple edges / actual installation.
h, edge_y, edge_x, spacing_x, spacing_y = 81, 115, 100, 100, 170
Xne = lambda e: min(1, .25 + .5*e/h)
Xna = lambda s: min(1,.5+s/(6*h))
N_concrete = 24.2*.7*.88*Xne(edge_y)*Xne(edge_x)*Xna(spacing_x)*Xna(spacing_y)
N_pullout = 21.6*.53*.96
N_steel = 29.7
anchor_tension_screen = min(N_concrete, N_pullout, N_steel)
anchor_tension_demand = 2*rail_up_combo + wind_per_angle_H*50/25

def board_scenario(width):
    gap=5
    rows=[math.ceil((d+gap)/(width+gap)) for d in (2600,900,6600)]
    gaps=[gap]*3
    # Avoid creating thin edge rips for a1–2mm nominal shortfall. This is an
    # illustrative setting-out adjustment, subject to actual moisture/gap rules.
    for i,d in enumerate((2600,900,6600)):
        fewer=rows[i]-1
        short=d-(fewer*width+(fewer-1)*gap)
        if 0<=short<=2:
            rows[i]=fewer
            gaps[i]=(d-fewer*width)/(fewer-1)
    # 4.2+3.0 for each 6.6 main row; two rebuilt cuts from each4.2;
    # ten400mm tread boards per4.2m stock length, including kerfs/end trim.
    stock_counts={4200:rows[0]+math.ceil(rows[1]/2)+math.ceil(rows[2]/10),3000:rows[0]}
    assert 10*(400+4)+5<=4200
    return {"board_mm":width,"example_gaps_mm":gaps,"rows_main_rebuilt_tread":rows,
            "outer_rips_mm":[(d-(n-2)*width-(n-1)*g)/2 for d,n,g in zip((2600,900,6600),rows,gaps)],
            "installed_row_lm":round(rows[0]*6.6+rows[1]*1.97+rows[2]*.4,3),
            "stock_counts_mm":stock_counts,
            "stock_lm":round(sum(s*n for s,n in stock_counts.items())/1000,3),
            "base_screws":rows[0]*21*2+rows[1]*6*2+rows[2]*4}

# Short400mm boards bear directly on doubled rails at45/355mm centrelines.
#90-deep bottom-flush crosspieces are50mm below the board underside and
#carry no walking loads. Comparisons below are demand ratios, not board grades.
rail_point_uls=1.5*2.7*.355/.310
tread_rail_moment=rail_point_uls*1.2/4
nog_stock_mm=19*(220+4)+5
assert nog_stock_mm<=4800

out={
    "status":"Working component/demand screens only; no full assembly or project approval",
    "main_standard_kit_layout_proposal":{
        "pile_X_mm_each_row":main_x,"anchor_X_mm_each_row":anchor_x,
        "bracing_joist_X_pairs_mm":bracing_joist_pairs,
        "main_piles":16,"rebuilt_piles":4,"anchor_count":6,"ordinary_count":14,
        "maximum_bearer_bay_mm":max(b-a for a,b in zip(main_x,main_x[1:])),
        "between_100mm_plate_and_45mm_joist_mm":(380-45-100)/2,
        "main_ground_level_proposal_mm":-100,"pile_top_example_mm":187.25,
        "scarf_transition_example_mm":40,"scarf_angle_degrees":math.degrees(math.atan(17.5/40)),
        "lowest_cut_example_mm":187.25-80-40,"lowest_cut_clearance_example_mm":187.25-80-40+100,
        "main_concrete_net_m3":round(main_concrete,7),
        "limitation":"Geometry/quantity proposal; complete manufacturer nail-free zones and drainage/finished-ground fit still to confirm"},
    "cpc40_hold_down": {"characteristic_pair_kN":8,"phi":.7,"duration":.6,"wet":.8,
                        "screen_design_kN":cpc_design_screen,"demand_kN":uplift_demand,
                        "utilisation":uplift_demand/cpc_design_screen,
                        "quantity_basis":"14 additional pairs =28 SSCPC40; two of16 bearings already in full12KNH joints"},
    "tread_short_board_layout":{
        "boards_run":"front-to-back,400mm cut length","rail_centres_mm":[45,355],
        "crosspieces":{"count":19,"section_mm":[90,45],"cut_mm":220,
                       "top_Z_mm":168,"board_underside_Z_mm":218,
                       "walking_loads":"Direct to long rails, not these lower crosspieces"},
        "stock_140x45_mm":[7200]*4,"stock_90x45_mm":[4800],
        "stock_lm":33.6,"installed_lm":30.58,
        "board_bending_demand_ratio_vs_32_at_600_with_1_8kN":(2.7*.310)/(1.8*.600),
        "board_bending_ratio_vs_19_at_450_with_1_8kN":(2.7*.310*19**2)/(1.8*.450*32**2),
        "board_shear_ratio_vs_19_with_1_8kN":(2.7/32)/(1.8/19),
        "front_rail_point_ULS_kN":rail_point_uls,
        "simple_rail_1_2m_point_ULS_moment_kNm":tread_rail_moment,
        "scope":"Demand comparison only; actual board quality and full built-up rail resistance/continuity still govern"},
    "trial_tread_pads": {"count":7,"base_mm":[500,500],"base_bottom_Z_mm":-450,
                         "base_top_Z_mm":-100,"head_mm":[500,400],"head_top_Z_mm":77.25,
                         "support_X_mm":support_x,"angle_X_mm":angle_x,
                         "net_m3_each":round(pad_volume,6),"net_m3_seven":round(7*pad_volume,6),
                         "weight_kN_each":pad_weight,"assumed_allowable_bearing_kPa":100,
                         "gravity_bearing":gravity,
                         "wind_envelope_kPa":3,"wind_net_compression_kN":remaining_N,
                         "wind_overturning_reserve_kNm":overturning_reserve,
                         "no_credit":"No soil cover, passive resistance or favourable imposed load"},
    "tread_angle_screens": {"factored_point_rear_uplift_kN":rear_rail_uplift_from_point_ULS,
                            "combined_vertical_per_angle_kN":rail_up_combo,
                            "normal_horizontal_per_angle_kN":wind_per_angle_H,
                            "foot_elastic_bending_utilisation":M_foot_demand_Nmm/M_foot_capacity_Nmm,
                            "model":"PBB0140/SS, two outer bolts and two outer anchors",
                            "minimum_assumed_yield_MPa":170,"plate_thickness_mm":4,
                            "timber_bolt_loaded_edge_mm":bolt_bottom_edge,
                            "limitation":"Component screen; bend/prying, timber splitting, anchor-group interaction and full actions still require complete check"},
    "ramset_anchor_component_screen": {"model":"T12110SSX","effective_embedment_mm":81,
                                        "drill_diameter_mm":12,"minimum_drill_depth_mm":90,"SS_torque_Nm":75,
                                        "edge_distances_mm":[115,100],"spacing_mm":[100,170],
                                        "concrete_baseline_h70_with_h81_edge_factors_kN":N_concrete,
                                        "tension_screen_kN":anchor_tension_screen,
                                        "tension_demand_screen_kN":anchor_tension_demand,
                                        "limitation":"Conservative component screen, not a manufacturer assembly rating or complete concrete-anchor design"},
    "board_scenarios":[board_scenario(88),board_scenario(90)],
    "priced_subtotal_only_GST_included":{
        "decking_270_lm_at_2_99":round(270*2.99,2),
        "main_framing_127_8_lm_at_6_84":round(127.8*6.84,2),
        "six_12KNH_at_69_94":round(6*69.94,2),
        "fourteen_PBB0140_SS_at_34_60":round(14*34.60,2),
        "exclusions":"Tread framing, piles, concrete, remaining hardware/nails/screws, freight and site preparation"},
}
out['combined_trial_concrete_net_m3']=round(main_concrete+7*pad_volume,7)
assert cpc_design_screen>uplift_demand
assert all(x['max_kPa']<q_allow for x in gravity.values())
assert remaining_N>0 and overturning_reserve>0
assert out['tread_angle_screens']['foot_elastic_bending_utilisation']<1
out['priced_subtotal_only_GST_included']['subtotal']=round(sum(
    v for v in out['priced_subtotal_only_GST_included'].values() if isinstance(v,(float,int))),2)
print(json.dumps(out,indent=2))
