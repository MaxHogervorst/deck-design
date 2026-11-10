"""Demand and quantity checks for the five short step frames (10 November 2026)."""
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
# Main deck: joists between the rims, seated on bearers at Y300/2510. Blocks are cut at 380 mm
# so a tape measure can hit them; the clear gap between the rebuilt joists is 382 mm.
main_alloc = [
    (6, 7200, [6600]),
    (6, 6000, [2510, 2510, 900]),
    (1, 6000, [2510, 2510, 380, 380]),
    (1, 6000, [2510, 2510]),
    (1, 4800, [1880, 1880]),
    (1, 4800, [2510, 1880]),
]
# Five short H4 frames, one in each bay between the front piles. No 6.6 m rail.
# Each frame: four 900 mm plies (a double rail each side), three 220 mm crosspieces, one 250 mm tie.
h4_alloc = [(4, 4800, [900, 900, 900, 900, 900]), (1, 4800, [220] * 15 + [250] * 5)]
for n, s, cs in main_alloc + h4_alloc:
    assert sum(cs) + 4 * len(cs) + 5 <= s, (s, cs)
main_counts = Counter(c for n, s, cs in main_alloc for c in cs for _ in range(n))
assert main_counts == Counter({6600: 6, 2510: 17, 900: 6, 380: 2, 1880: 3}), main_counts
h4_counts = Counter(c for n, s, cs in h4_alloc for c in cs for _ in range(n))
assert h4_counts == Counter({900: 20, 220: 15, 250: 5}), h4_counts
pile_x = [62.5, 1357.5, 2652.5, 3947.5, 5242.5, 6537.5]
frames = [710, 2005, 3300, 4595, 5890]
assert frames == [round((a + b) / 2, 1) for a, b in zip(pile_x, pile_x[1:])]
frame_len = 900
paver = 300
paver_dx = 220  # two pavers along each rail, 100 mm clear of the pile holes
paver_y = [2645, 2955]
pit = [760, 800]
paver_x = [c + dx for c in frames for dx in (-paver_dx, paver_dx)]
for p in paver_x:
    for x in pile_x:
        gap = abs(p - x) - paver / 2 - 350 / 2
        assert gap >= 100, (p, x, gap)
for c in frames:
    for x in pile_x:
        gap = abs(c - x) - pit[0] / 2 - 350 / 2
        assert gap >= 80, (c, x, gap)
assert max(c + frame_len / 2 for c in frames) <= 6600
assert min(c - frame_len / 2 for c in frames) >= 0
board_gap = (pile_x[1] - pile_x[0]) - frame_len
assert board_gap <= 450, board_gap
# Rebuilt joists are separate members. 2.7 kN stair point, zero dead credit.
xs, u, solve, mom = beam(
    list(np.arange(-1.925, -0.0449, 0.025)) + [-1.925, -0.8, -0.045],
    [-1.925, -0.8],
    6.5e6 * 0.045 * 0.14**3 / 12,
)
fg, qg = u(lambda x: 0.6 * 0.45)
F = np.repeat(np.zeros_like(fg)[:, None], len(xs), axis=1)
for i in range(len(xs)):
    F[2 * i, i] = 2.7
_, R = solve(F)
rebuilt_uplift = max(float(-R.min()), 2.7 * 0.8 / 1.125)
# One 900 mm double rail on two pavers, 230 mm cantilevers. Factored stair point, any position.
# Two supports so the rail is not a mechanism; the far support can go into uplift, which the tie has to hold.
EI = 6.5e6 * 0.09 * 0.14**3 / 12
local_supports = [0.23, 0.67]
xs, u, solve, mom = beam(list(np.arange(0, 0.9001, 0.025)) + local_supports, local_supports, EI)
g, qg = u(lambda x: 0.6 * 0.2)
F = np.repeat((1.2 * g)[:, None], len(xs), axis=1)
point = 1.5 * 2.7 * 355 / 310
for i in range(len(xs)):
    F[2 * i, i] += point
D, R = solve(F)
M = float(abs(mom(D, np.repeat((1.2 * qg)[:, None], len(xs), axis=1))).max())
pad_R = float(R.max())
pad_min = float(R.min())
bearing = pad_R / (paver / 1000) ** 2
cap = 0.8 * 0.8 * 11.7 * (90 * 140**2 / 6) / 1e6
assert M < 0.65 * cap, (M, cap)
assert bearing <= 100, bearing
assert pad_min < -1, pad_min  # uplift is real; the tie is a hold-down, not a sideways-only cleat
assert np.max(abs(R.sum(axis=0) - F[::2].sum(axis=0))) < 1e-6
# Reference check and the main-bearer gravity envelope. Unchanged deck.
xt, ut, st, mt = beam([0, 0.5, 1], [0, 1], 1)
ft, qt = ut(lambda x: 1)
dt, rt = st(ft)
assert np.allclose(rt[:, 0], [0.5, 0.5]) and abs(abs(mt(dt, qt)).max() - 0.125) < 1e-9
sx = [x / 1000 for x in pile_x]
bounds = [0] + sx + [6.6]
xm, um, sm, mm = beam(list(np.arange(0, 6.6001, 0.025)) + sx, sx, 6.5e6 * 0.09 * 0.14**3 / 12)
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
main_concrete = 4 * (0.35**2 * 0.9 - 0.125**2 * 0.8) + 12 * (0.35**2 * 0.45 - 0.125**2 * 0.35)
bag_yield = 0.0095
bags_needed = int(np.ceil(main_concrete / bag_yield))
gap7_m3 = len(frames) * (pit[0] / 1000) * (pit[1] / 1000) * 0.15
gap7_bags_15l = int(np.ceil(gap7_m3 / 0.015))
main_rows, rebuilt_rows, tread_rows = 28, 21, 4
crosspieces = 15
base_screws = main_rows * 17 * 2 + rebuilt_rows * 3 * 2 + tread_rows * crosspieces * 2 + tread_rows * 2
stock_4200, stock_3000 = 38, 32
out = {
    'status': 'Working DIY plan, 10 November 2026. The step is five short H4 frames, one in each bay between the front piles, each on four pavers and screwed to the front bearer. No continuous 6.6 m rail, no plastic packers, no second pour. Items the owner would ideally have checked are listed at the end of the plan.',
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
    'rebuilt_joist_cut_mm': 1880,
    'rebuilt_bearer_Y_mm': [-1925, -800],
    'rear_bearer_rear_face_Y_mm': -1970,
    'rebuilt_lateral_blocks': 2,
    'rebuilt_block_cut_mm': 380,
    'main_lateral_block_rows': 0,
    'tread': {
        'frames': len(frames),
        'frame_X_mm': frames,
        'frame_len_mm': frame_len,
        'frame_X_extent_mm': [[c - frame_len // 2, c + frame_len // 2] for c in frames],
        'rails': 'five separate double 140x45 H4 frames, each 900 long, inner Y2600-2690 and outer Y2910-3000',
        'inner_rail_Y_mm': [2600, 2690],
        'outer_rail_Y_mm': [2910, 3000],
        'crosspieces_per_frame': 3,
        'crosspieces': crosspieces,
        'crosspiece_cut_mm': 220,
        'ties': len(frames),
        'tie_X_mm': frames,
        'tie_cut_mm': 250,
        'tie_Y_mm': [2555, 2600],
        'tie_Z_mm': [78, 328],
        'tie_fixing': '4x 14g x100 SS screws into the bearer face and 2x 14g x100 SS screws into the inner rail, per frame. Hold-down and lateral tie.',
        'board_gap_mm': board_gap,
        'board_length_mm': 6400,
        'board_inset_mm': 100,
    },
    'main_pile_X_mm': pile_x,
    'timber_piles': 16,
    'candidate_anchor_piles': 4,
    'ordinary_piles': 12,
    'tread_frames': len(frames),
    'tread_paver_x_mm': paver_x,
    'tread_paver_mm': paver,
    'pavers_per_frame': 4,
    'paver_count': len(frames) * 4,
    'tread_pad_type': 'four 300x300 pavers per frame, two along each rail, on compacted GAP7 in one pit dug to firm ground',
    'tread_paver_Y_centres_mm': paver_y,
    'tread_paver_dx_mm': paver_dx,
    'tread_pit_mm': pit,
    'tread_pit_count': len(frames),
    'tread_pad_top_Z_mm': [45, 75],
    'rail_bottom_Z_mm': 78,
    'pad_restraint': 'each frame is screwed to the front bearer through a 250 mm H4 tie. Pavers take the weight. An H4 offcut packer, screwed to the rail, takes up a low paver. No plastic packers.',
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
        'stock_4200': stock_4200,
        'stock_3000': stock_3000,
        'stock_lm': round(stock_4200 * 4.2 + stock_3000 * 3.0, 1),
        'pricing_allowance_lm': round(stock_4200 * 4.2 + stock_3000 * 3.0, 1),
        'base_screws': base_screws,
        'purchase_allowance_screws': 1500,
        'width_basis_mm': 88,
        'gaps': 'About 5 mm on the main deck and about 6 mm on the rebuilt strip. Step is four boards on the 400 mm frame with a small front overhang.',
    },
    'concrete_geometry_only': {
        'main_net_m3': main_concrete,
        'readymix_order_m3': 1.2,
        'bags_20kg_needed': bags_needed,
        'bags_20kg_buy': int(np.ceil(bags_needed * 1.1)),
        'main_anchor_holes_mm': [350, 350, 900],
        'ordinary_holes_mm': [350, 350, 450],
        'auger_diameter_mm': 400,
        'gap7_m3': gap7_m3,
        'gap7_bags_15l': gap7_bags_15l,
        'warning': 'Planning geometry, not a concrete order. Anchor section is provisional 125 square. Square-hole volume; a 400 mm auger hole is about the same.',
    },
    'screens': {
        'rebuilt_zero_dead_uplift_ULS_kN': rebuilt_uplift,
        'rail_point_ULS_kN': point,
        'double_rail_max_M_ULS_kNm': M,
        'double_rail_bending_screen_capacity_kNm': cap,
        'double_rail_utilisation': M / cap,
        'max_paver_reaction_ULS_kN': pad_R,
        'min_paver_reaction_ULS_kN': pad_min,
        'paver_bearing_kPa_max': bearing,
        'main_bearer_max_M_ULS_kNm': main_M,
        'main_loaded_width_envelope_m': 2.0,
        'note': 'Beam/component demand screens only; not a full connection or foundation verification. Step frames are separate 900 mm members.',
    },
}
assert out['main_stock_lm'] == 100.8 and out['H4_stock_lm'] == 24.0
assert out['concrete_geometry_only']['bags_20kg_buy'] == 115
assert out['decking']['base_screws'] == 1206
assert out['paver_count'] == 20
(root / 'design.json').write_text(json.dumps(out, indent=2) + '\n')
summary = {
    'frames': frames,
    'board_gap_mm': board_gap,
    'util': round(M / cap, 3),
    'M': round(M, 3),
    'uplift_kN': round(pad_min, 2),
    'paver_kN': round(pad_R, 2),
    'bearing_kPa': round(bearing, 1),
    'rebuilt_uplift_kN': round(rebuilt_uplift, 2),
    'bags_buy': out['concrete_geometry_only']['bags_20kg_buy'],
    'gap7_m3': round(gap7_m3, 3),
    'gap7_bags': gap7_bags_15l,
    'screws': base_screws,
    'deck_lm': out['decking']['stock_lm'],
}
print(json.dumps(summary, indent=2))
