"""Current short-board pine-tread cut plan. Geometry/quantity checks, not capacities.

Run with Python 3; no dependencies. Prints JSON to stdout.
The earlier structural_check.py/results.json retain their historical scope.
"""
from collections import Counter
import json

KERF = 4  # mm after each cut
TRIM = 5  # mm per supplied length


def allocation(count, stock, cuts, label):
    assert sum(cuts) + len(cuts) * KERF + TRIM <= stock, label
    return [(stock, cuts, label)] * count


main = []
for count, stock, cuts, label in [
    (4, 4800, [4525, 240], "continuous joist and block"),
    (9, 3600, [2510, 240, 240], "short joist and blocks"),
    (8, 3000, [2510, 335], "short joist and block"),
    (4, 7200, [6600, 240, 290], "unspliced bearer ply and blocks"),
    (1, 4200, [900, 900, 900, 900, 335], "rebuilt bearer plies and block"),
    (1, 7200, [6600, 335], "front rim and block"),
    (1, 6000, [5700, 240], "rear rim and block"),
    (1, 6000, [335] * 16, "remaining blocks"),
]:
    main += allocation(count, stock, cuts, label)

rails = allocation(4, 7200, [6600], "140x45 unspliced tread rail ply")
nogs = allocation(1, 4800, [220] * 19, "90x45 lower tread crosspieces")
tread = rails + nogs

assert Counter(c for _, cuts, _ in main for c in cuts) == Counter({
    4525: 4, 2510: 17, 6600: 5, 900: 4, 5700: 1,
    240: 27, 290: 4, 335: 26,
})
assert Counter(c for _, cuts, _ in tread for c in cuts) == Counter({6600: 4, 220: 19})

base_centres = [22.5 + 380 * i for i in range(18)] + [6577.5]
cross_centres = base_centres
assert len(cross_centres) == 19
assert max(b-a for a, b in zip(cross_centres, cross_centres[1:])) <= 380
pad_centres = [300,1300,2300,3100,4300,5300,6300]
# Geometric bracket candidates only:140mm along rail; assembly not released.
# Offset brackets to clear the nineteen lower crosspieces.
bracket_centres = [300,1400,2400,3160,4300,5200,6300]
assert all(abs(a-b) <= 100 for a, b in zip(pad_centres, bracket_centres))
assert all(abs(b-c) > (140+45)/2 for b in bracket_centres for c in cross_centres)


def summarise(items):
    return {
        "installed_lm": round(sum(sum(cuts) for _, cuts, _ in items)/1000, 3),
        "stock_lm": round(sum(stock for stock, _, _ in items)/1000, 3),
        "stock_lengths": len(items),
        "stock_mm_counts": dict(sorted(Counter(s for s, _, _ in items).items())),
        "allocations": [
            {"count": count, "stock_mm": stock, "cuts_mm": list(cuts), "part": label}
            for (stock, cuts, label), count in Counter(
                (s, tuple(c), label) for s, c, label in items
            ).items()
        ],
    }


result = {
    "scope": "Nominal geometry only; stock availability and final connections unverified",
    "main_rebuilt_H3_2_SG8_140x45": summarise(main),
    "tread_minimum_H4_SG8_all_sections": summarise(tread),
    "tread_rails_140x45": summarise(rails),
    "tread_lower_crosspieces_90x45": summarise(nogs),
    "tread_crosspiece_centres_mm": cross_centres,
    "tread_pad_station_candidates_mm": pad_centres,
    "tread_bracket_station_candidates_mm": bracket_centres,
    "tread_levels_mm": {"surface": 250, "frame_top": 218, "frame_bottom": 78,
                        "lower_crosspiece_top":168,"concrete_bearing_with_0_75mm_DPC":77.25},
    "board_examples_only": json.loads(__import__('pathlib').Path(__file__).with_name('standard_details_check.json').read_text())['board_scenarios'],
    "tread_lower_crosspiece_end_nails_2_per_end":19*2*2,
    "main_pile_count":20,"anchor_count":6,"ordinary_count":14,

}
assert result["main_rebuilt_H3_2_SG8_140x45"]["installed_lm"] == 119.42
assert result["main_rebuilt_H3_2_SG8_140x45"]["stock_lm"] == 127.8
assert result["main_rebuilt_H3_2_SG8_140x45"]["stock_lengths"] == 29
assert result["tread_minimum_H4_SG8_all_sections"]["installed_lm"] == 30.58
assert result["tread_minimum_H4_SG8_all_sections"]["stock_lm"] == 33.6
assert max(b-a for a,b in zip(pad_centres,pad_centres[1:]))==1200
assert summarise(rails)['stock_lm']==28.8 and summarise(nogs)['stock_lm']==4.8
print(json.dumps(result, indent=2))
