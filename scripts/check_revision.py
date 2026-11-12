"""Demand and quantity checks. Deck unchanged. Steps and holes follow the 11 November site conversation."""
import json, itertools
from pathlib import Path
from collections import Counter
import numpy as np
from beam_helper import beam
root = Path(__file__).resolve().parents[1]
base = [22.5 + 437 * i for i in range(16)]
joists = sorted([x for i, x in enumerate(base) if i != 9] + [3933, 3978])
assert len(joists) == 17 and max(np.diff(joists)) <= 450
assert abs(300 - 22.5) <= 300 and abs(2510 - 2532.5) <= 300
# Main deck. The rebuilt strip has no piles: it is fixed to the existing bearer.
main_alloc = [
    (2, 7200, [6600]),
    (8, 6000, [2510, 2510]),
    (1, 6000, [2510, 1970]),
    (1, 6000, [1970, 1970, 900, 900]),
]
# Two steps, full width. Eight 6.6 m H4 plies (two doubles for each step) and the short joists.
# 7.2 m stock so each ply is one piece. Joists cut long and trimmed to the opening.
h4_alloc = [
    (8, 7200, [6600]),
    (1, 4800, [500] * 9),
    (1, 4800, [500] * 8),
    (1, 4800, [240] * 17),
]
for n, s, cs in main_alloc + h4_alloc:
    assert sum(cs) + 4 * len(cs) + 5 <= s, (s, cs)
main_counts = Counter(c for n, s, cs in main_alloc for c in cs for _ in range(n))
assert main_counts == Counter({6600: 2, 2510: 17, 1970: 3, 900: 2}), main_counts
h4_counts = Counter(c for n, s, cs in h4_alloc for c in cs for _ in range(n))
assert h4_counts == Counter({6600: 8, 500: 17, 240: 17}), h4_counts
# NZS 3604:2011 Table 6.4(b), 2 kPa, wet in service. Spans are for a bearer
# continuous over two or more spans. Loaded dimension over 1.30 m uses the
# 1.65 m column. A doubled 190×45 is a built-up 190×90 (cl 2.4.4.7), which
# is thicker than the 190×70 the table lists at 2.7 m. The pile at 3947.5
# is not required. Line 2 stays 200 mm onto the grass. Line 3 stays 1,230 mm
# past the concrete, clear of both pipes.
pile_x = [62.5, 677.5, 3067.5, 5242.5, 6537.5]
bays = [b - a for a, b in zip(pile_x, pile_x[1:])]
assert bays == [615, 2390, 2175, 1295], bays
assert max(bays) <= 2700
# Each 190 piece bears on three piles, so each piece is continuous over two spans.
assert pile_x[2] - pile_x[0] <= 4800
assert pile_x[-1] - pile_x[2] <= 4800
rise = 500 / 3
going = 280
assert 190 >= rise >= 150
assert 550 <= 2 * rise + going <= 700
# Rebuilt strip spans from the existing bearer to a ledger on the house.
# NZS 3604 Table 7.1(b), wet: 140×45 at 450 centres spans 2.35 m. No new piles.
rebuilt_span = 1970
assert rebuilt_span <= 2350
rebuilt_uplift = 0.0
# Step front beam is a doubled 140, which Table 6.4(b) allows to 3.0 m at a
# loaded dimension of 1.30 m, continuous. The longest step bay is 2.39 m.
# Do not rip it. A ripped section is not in the table.
point = 1.5 * 2.7 * 355 / 310
step_span = max(bays) / 1000

def bay_screen(span, depth, width=0.09):
    EI = 6.5e6 * width * depth**3 / 12
    pts = list(np.arange(0, span + 1e-9, 0.025)) + [0, span, span / 2]
    xs, u, solve, mom = beam(pts, [0, span], EI)
    g, qg = u(lambda x: 0.6 * 0.45)
    F = np.repeat((1.2 * g)[:, None], len(xs), axis=1)
    j = int(np.argmin(np.abs(xs - span / 2)))
    F[2 * j, :] += point
    D, R = solve(F)
    react = float(R.max())
    assert np.max(abs(R.sum(axis=0) - F[::2].sum(axis=0))) < 1e-6
    return react

R140 = bay_screen(step_span, 0.14)
bearing = R140 / 0.3**2
assert bearing <= 100, bearing
assert step_span <= 3.0
# Reference check and the main-bearer gravity envelope. Unchanged deck.
xt, ut, st, mt = beam([0, 0.5, 1], [0, 1], 1)
ft, qt = ut(lambda x: 1)
dt, rt = st(ft)
assert np.allclose(rt[:, 0], [0.5, 0.5]) and abs(abs(mt(dt, qt)).max() - 0.125) < 1e-9
sx = [x / 1000 for x in pile_x]
bounds = [0] + sx + [6.6]
xm, um, sm, mm = beam(list(np.arange(0, 6.6001, 0.025)) + sx, sx, 6.5e6 * 0.09 * 0.19**3 / 12)
gm, qgm = um(lambda x: 0.6 * 2.0)
patches = [um(lambda x, a=a, b=b: 4.0 if a < x < b else 0) for a, b in zip(bounds, bounds[1:])]
fm, qu = [], []
for pat in itertools.product([0, 1], repeat=len(patches)):
    f = sum((v * p[0] for v, p in zip(pat, patches)), start=np.zeros_like(gm))
    q = sum((v * p[1] for v, p in zip(pat, patches)), start=np.zeros_like(qgm))
    fm.append(1.2 * gm + 1.5 * f)
    qu.append(1.2 * qgm + 1.5 * q)
dm, rm = sm(np.array(fm).T)
main_M = float(abs(mm(dm, np.array(qu).T)).max())
assert np.max(abs(rm.sum(axis=0) - np.array(fm).T[::2].sum(axis=0))) < 1e-6
# 400 square by 600. Ten main piles. No rebuilt holes. Five step holes, 300 square by 400.
main_concrete = round(10 * (0.4 * 0.4 * 0.6), 3)
rebuilt_concrete = 0
step_concrete = round(5 * (0.3 * 0.3 * 0.4), 3)
extra_step_concrete = 0
concrete = round(main_concrete + rebuilt_concrete + step_concrete, 3)
order_m3 = 2.0
assert concrete < order_m3
cement_bags = 36  # about 16 bags per m³, plus a margin
mix_m3 = 2.5
main_rows, rebuilt_rows, tread_rows, face_rows = 28, 21, 6, 3
# Full-length rows each take a 4.2 and a 3.0. The 38/32 lengths already covered 28 + 21 + 4; two more step rows and three face boards.
stock_4200 = 38 + (tread_rows - 4) + face_rows
stock_3000 = 32 + (tread_rows - 4) + face_rows
base_screws = main_rows * 17 * 2 + rebuilt_rows * 3 * 2 + (tread_rows + face_rows) * 17 * 2
assert base_screws <= 1500
out = {
    'status': 'Working DIY plan, 11 November 2026. Holes are 600 deep, no anchor kits. Two steps, three rises, measured off the path. Follows the site conversation, not the ROBO preview ISL38807.',
    'main_joist_centres_mm': joists,
    'main_base_lines': 16,
    'main_joist_members_with_supported_butt': 17,
    'max_spacing_mm': max(np.diff(joists)),
    'main_joist_cut_mm': 2510,
    'main_bearer_Y_mm': [300, 2510],
    'main_span_mm': 2210,
    'wet_table_span_at450_mm': 2350,
    'front_rim_Y_mm': [2555, 2600],
    'butt_joist_centre_mm': 3956,
    'rebuilt_joists': 3,
    'rebuilt_joist_cut_mm': 1970,
    'rebuilt_bearer_Y_mm': [0, -1970],
    'rear_bearer_rear_face_Y_mm': -1970,
    'rebuilt_lateral_blocks': 0,
    'rebuilt_block_cut_mm': 0,
    'main_lateral_block_rows': 0,
    'tread': {
        'kind': 'two steps, three equal rises, ribbon screwed to the piles, not a cut stringer',
        'rises': 3,
        'rise_mm': round(rise, 1),
        'going_mm': going,
        'projection_mm': going * 2,
        'lower_board_Z_mm': round(rise, 1),
        'upper_board_Z_mm': round(2 * rise, 1),
        'lower_framing_top_Z_mm': round(rise - 32, 1),
        'upper_framing_top_Z_mm': round(2 * rise - 32, 1),
        'lower_beam_min_depth_mm': 150,
        'joist_count': 17,
        'lower_joist_cut_mm': 500,
        'upper_joist_cut_mm': 240,
        'long_plies': 8,
        'small_piles': 5,
        'small_piles_buy': 5,
        'small_pile_X_mm': pile_x,
        'small_pile_Y_mm': 3115,
        'small_hole_mm': [300, 300, 400],
        'handrail': False,
    },
    'main_pile_X_mm': pile_x,
    'timber_piles': 10,
    'candidate_anchor_piles': 0,
    'ordinary_piles': 10,
    'step_piles': 5,
    'main_stock_lm': round(sum(n * s for n, s, c in main_alloc) / 1000, 3),
    'main_installed_lm': round(sum(n * sum(c) for n, s, c in main_alloc) / 1000, 3),
    'H4_stock_lm': round(sum(n * s for n, s, c in h4_alloc) / 1000, 3),
    'H4_installed_lm': round(sum(n * sum(c) for n, s, c in h4_alloc) / 1000, 3),
    'main_stock_allocations': [{'count': n, 'stock_mm': s, 'cuts_mm': c} for n, s, c in main_alloc],
    'H4_stock_allocations': [{'count': n, 'stock_mm': s, 'cuts_mm': c} for n, s, c in h4_alloc],
    'decking': {
        'main_rows': main_rows,
        'rebuilt_rows': rebuilt_rows,
        'tread_rows': tread_rows,
        'face_rows': face_rows,
        'stock_4200': stock_4200,
        'stock_3000': stock_3000,
        'stock_lm': round(stock_4200 * 4.2 + stock_3000 * 3.0, 1),
        'pricing_allowance_lm': round(stock_4200 * 4.2 + stock_3000 * 3.0, 1),
        'base_screws': base_screws,
        'purchase_allowance_screws': 1500,
        'width_basis_mm': 88,
        'gaps': 'About 5 mm on the main deck and about 6 mm on the rebuilt strip. Three boards on each step. One board on the boundary-joist face and one on each riser.',
    },
    'concrete_geometry_only': {
        'main_10_holes_m3': main_concrete,
        'rebuilt_4_holes_m3': rebuilt_concrete,
        'step_holes_m3': step_concrete,
        'extra_path_holes_m3': extra_step_concrete,
        'main_net_m3': concrete,
        'readymix_order_m3': order_m3,
        'cement_20kg_buy': cement_bags,
        'builders_mix_m3': mix_m3,
        'hole_mm': [400, 400, 600],
        'step_hole_mm': [300, 300, 400],
        'warning': 'Volume leaves the pile in the hole. Not a concrete order. The 2.0 m³ is the truck figure; mixing uses the cement and the builders mix instead.',
    },
    'screens': {
        'rebuilt_zero_dead_uplift_ULS_kN': rebuilt_uplift,
        'step_point_ULS_kN': point,
        'step_beam_span_m': step_span,
        'step_beam_table_m': 3.0,
        'bearer_table_m': 2.7,
        'step_pile_reaction_ULS_kN': R140,
        'step_pile_bearing_kPa': bearing,
        'main_bearer_max_M_ULS_kNm': main_M,
        'note': 'Spans checked to NZS 3604:2011 Table 6.4(b), wet, 2 kPa, bearer continuous over two spans. Not a foundation or bracing check.',
    },
}
assert out['main_stock_lm'] == 74.4 and out['H4_stock_lm'] == 72.0
assert out['decking']['base_screws'] == base_screws
assert out['concrete_geometry_only']['main_10_holes_m3'] == 0.96
(root / 'design.json').write_text(json.dumps(out, indent=2) + '\n')
summary = {
    'rise_mm': round(rise, 1),
    'going_mm': going,
    'two_R_plus_G': round(2 * rise + going, 1),
    'bearer_bays_mm': bays,
    'bearer_table_m': 2.7,
    'step_span_m': step_span,
    'bearing_kPa': round(bearing, 1),
    'concrete_m3': round(concrete, 3),
    'main_m3': round(main_concrete, 3),
    'screws': base_screws,
    'deck_lm': out['decking']['stock_lm'],
    'H4_m': out['H4_stock_lm'],
    'rebuilt_uplift_kN': round(rebuilt_uplift, 2),
}
print(json.dumps(summary, indent=2))
