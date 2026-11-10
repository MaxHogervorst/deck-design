"""Demand and quantity checks for the pad-supported tread revision (9 November 2026)."""
import json,itertools
from pathlib import Path
from collections import Counter
import numpy as np
from beam_helper import beam
root=Path(__file__).resolve().parents[1]
base=[22.5+437*i for i in range(16)]
joists=sorted([x for i,x in enumerate(base) if i!=9]+[3933,3978])
assert len(joists)==17 and max(np.diff(joists))<=450
assert abs(300-22.5)<=300 and abs(2510-2532.5)<=300
# Main deck: joists Y45..2555 seated on bearers at Y300/2510; plain continuous rims at Y0..45 and Y2555..2600.
main_alloc=[(6,7200,[6600]),(6,6000,[2510,2510,900]),(1,6000,[2510,2510,382.5,382.5]),(1,6000,[2510,2510]),(1,3000,[2510]),(1,4200,[1880,1880]),(1,2400,[1880])]
# Tread: two double 140x45 H4 rails (inner Y2600..2690, outer Y2910..3000), seventeen 220 crosspieces, three 250 lateral cleats.
h4_alloc=[(4,7200,[6600,220,220]),(1,3000,[220]*9+[250]*3)]
for n,s,cs in main_alloc+h4_alloc:assert sum(cs)+4*len(cs)+5<=s,(s,cs)
main_counts=Counter(c for n,s,cs in main_alloc for c in cs for _ in range(n))
assert main_counts==Counter({6600:6,2510:17,900:6,382.5:2,1880:3}),main_counts
h4_counts=Counter(c for n,s,cs in h4_alloc for c in cs for _ in range(n));assert h4_counts==Counter({6600:4,220:17,250:3})
# Six tread pads, each under both rails, staggered off the front pile holes.
pile_x=[62.5,1357.5,2652.5,3947.5,5242.5,6537.5]
pads_mm=[400,1740,3035,4330,5625,6200]
pad_hole_x=350;pile_hole=350
for p in pads_mm[1:-1]:assert all(abs(p-x)>=(pad_hole_x+pile_hole)/2+30 for x in pile_x),p
# End pad holes may run into the corner pile holes; the plinth itself stays >=100 clear of the pile face.
for p in [pads_mm[0],pads_mm[-1]]:assert min(abs(p-x) for x in pile_x)-150-62.5>=100
assert max(np.diff(pads_mm))<=1350 and pads_mm[0]<=400 and 6600-pads_mm[-1]<=400
cleats=[1000,3300,5600]  # lateral tie cleats on the front bearer face, clear of pile heads
assert all(abs(c-x)>=70+62.5+30 for c in cleats for x in pile_x)
# Rebuilt joists are separate members. 2.7 kN stair point, zero dead credit.
xs,u,solve,mom=beam(list(np.arange(-1.925,-.0449,.025))+[-1.925,-.8,-.045],[-1.925,-.8],6.5e6*.045*.14**3/12)
fg,qg=u(lambda x:.6*.45);F=np.repeat(np.zeros_like(fg)[:,None],len(xs),axis=1)
for i in range(len(xs)):F[2*i,i]=2.7
_,R=solve(F);rebuilt_uplift=max(float(-R.min()),2.7*.8/1.125)
# Double rail continuous over six pads; factored stair point with board-edge eccentricity (355/310) at any position.
pads=[p/1000 for p in pads_mm]
EI=6.5e6*.09*.14**3/12
xs,u,solve,mom=beam(list(np.arange(0,6.6001,.025))+pads,pads,EI)
g,qg=u(lambda x:.6*.2);F=np.repeat((1.2*g)[:,None],len(xs),axis=1)
point=1.5*2.7*355/310
for i in range(len(xs)):F[2*i,i]+=point
D,R=solve(F);M=float(abs(mom(D,np.repeat((1.2*qg)[:,None],len(xs),axis=1))).max());pad_R=float(R.max())
cap=.8*.8*11.7*(90*140**2/6)/1e6
assert M<cap,(M,cap)
assert np.max(abs(R.sum(axis=0)-F[::2].sum(axis=0)))<1e-7
# Reference/equilibrium check and fresh main-bearer gravity envelope.
xt,ut,st,mt=beam([0,.5,1],[0,1],1);ft,qt=ut(lambda x:1);dt,rt=st(ft)
assert np.allclose(rt[:,0],[.5,.5]) and abs(abs(mt(dt,qt)).max()-.125)<1e-9
sx=[x/1000 for x in pile_x];bounds=[0]+sx+[6.6]
xm,um,sm,mm=beam(list(np.arange(0,6.6001,.025))+sx,sx,6.5e6*.09*.14**3/12)
gm,qgm=um(lambda x:.6*2.0);patches=[um(lambda x,a=a,b=b:4.0 if a<x<b else 0) for a,b in zip(bounds,bounds[1:])]
fm=[];qu=[]
for pat in itertools.product([0,1],repeat=len(patches)):
 f=sum((v*p[0] for v,p in zip(pat,patches)),start=np.zeros_like(gm));q=sum((v*p[1] for v,p in zip(pat,patches)),start=np.zeros_like(qgm))
 fm.append(1.2*gm+1.5*f);qu.append(1.2*qgm+1.5*q)
dm,rm=sm(np.array(fm).T);main_M=float(abs(mm(dm,np.array(qu).T)).max())
assert np.max(abs(rm.sum(axis=0)-np.array(fm).T[::2].sum(axis=0)))<1e-7
# Planning concrete geometry (timber anchor section provisional 125 sq).
main_concrete=4*(.35**2*.9-.125**2*.8)+12*(.35**2*.45-.125**2*.35)
pad_base=.35*.5*.35;pad_head=.3*.45*.17725;pad_v=pad_base+pad_head
readymix=main_concrete+6*pad_base;bags=6*pad_head
bag_yield=0.0095
out={'status':'Working proposal; pad restraint hardware and four-anchor bracing still to confirm with the builder. Tread no longer hangs from the deck.',
 'main_joist_centres_mm':joists,'main_base_lines':16,'main_joist_members_with_supported_butt':17,'max_spacing_mm':max(np.diff(joists)),'main_joist_cut_mm':2510,
 'main_bearer_Y_mm':[300,2510],'main_span_mm':2210,'wet_table_span_at450_mm':2350,'front_rim_Y_mm':[2555,2600],
 'rebuilt_joists':3,'rebuilt_joist_cut_mm':1880,'rebuilt_bearer_Y_mm':[-1925,-800],'rear_bearer_rear_face_Y_mm':-1970,
 'rebuilt_lateral_blocks':2,'main_lateral_block_rows':0,
 'tread':{'rails':'two double 140x45 H4 SG8 rails, 90 wide, continuous 6600','inner_rail_Y_mm':[2600,2690],'outer_rail_Y_mm':[2910,3000],'crosspieces':17,'crosspiece_cut_mm':220,
  'lateral_cleats':3,'cleat_X_mm':cleats,'cleat_cut_mm':250,'cleat_Y_mm':[2555,2600],'cleat_Z_mm':[78,328],'cleat_fixing':'2x 14g x100 SS screws into bearer face + 2x 14g x100 SS screws into inner rail, per cleat; lateral tie only, carries no tread weight'},
 'main_pile_X_mm':pile_x,'timber_piles':16,'candidate_anchor_piles':4,'ordinary_piles':12,
 'tread_pads':6,'tread_pad_X_mm':pads_mm,'tread_pad_top_mm':[300,450],'tread_pad_top_Y_mm':[2575,3025],'tread_pad_base_mm':[350,500,350],'tread_pad_base_Z_mm':[-450,-100],'tread_pad_top_Z_mm':77.25,
 'pad_restraint':'2 SS angle brackets per pad (one per rail), each 1x M10x75 SS316 sleeve anchor + 2x 14g x35 SS screws; brackets on the crosspiece side, anchors >=100 from plinth edges',
 'main_stock_lm':round(sum(n*s for n,s,c in main_alloc)/1000,3),'main_installed_lm':round(sum(n*sum(c) for n,s,c in main_alloc)/1000,3),
 'H4_stock_lm':round(sum(n*s for n,s,c in h4_alloc)/1000,3),'H4_installed_lm':round(sum(n*sum(c) for n,s,c in h4_alloc)/1000,3),
 'main_stock_allocations':[{'count':n,'stock_mm':s,'cuts_mm':c} for n,s,c in main_alloc],
 'H4_stock_allocations':[{'count':n,'stock_mm':s,'cuts_mm':c} for n,s,c in h4_alloc],
 'decking':{'main_rows':28,'rebuilt_rows':22,'tread_rows':5,'stock_4200':39,'stock_3000':33,'stock_lm':262.8,'pricing_allowance_lm':270,
  'base_screws':(28+5)*17*2+22*3*2,'purchase_allowance_screws':1500,'width_basis_mm':88,'gaps':'Illustrative ~5mm; actual board/moisture instructions govern'},
 'concrete_geometry_only':{'main_net_m3':main_concrete,'pad_base_each_m3':pad_base,'pad_head_each_m3':pad_head,'six_pads_m3':6*pad_v,'combined_net_m3':main_concrete+6*pad_v,
  'readymix_pour_m3':readymix,'readymix_order_m3':1.6,'plinth_bags_m3':bags,'plinth_bags_20kg':int(np.ceil(bags/bag_yield)),'plinth_bags_buy':18,
  'main_anchor_holes_mm':[350,350,900],'ordinary_holes_mm':[350,350,450],'warning':'Planning geometry, not a concrete order. Anchor section and pad restraint hardware remain to confirm.'},
 'screens':{'rebuilt_zero_dead_uplift_ULS_kN':rebuilt_uplift,'SSCPC40_pair_conservative_screen_kN':2.688,
  'rail_point_ULS_kN':point,'double_rail_max_M_ULS_kNm':M,'double_rail_bending_screen_capacity_kNm':cap,'double_rail_utilisation':M/cap,'max_pad_reaction_ULS_kN':pad_R,
  'pad_bearing_kPa_on_base':pad_R/(.35*.5),'main_bearer_max_M_ULS_kNm':main_M,'main_loaded_width_envelope_m':2.0,
  'note':'Beam/component demand screens only; not a full connection or foundation verification. Rails must be continuous 6600 mm.'}}
assert rebuilt_uplift<2.688
assert out['main_stock_lm']==100.8 and out['H4_stock_lm']==31.8 and out['decking']['base_screws']==1254
(root/'design.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['main_stock_lm','main_installed_lm','H4_stock_lm','H4_installed_lm','tread_pad_X_mm','screens','concrete_geometry_only']},indent=2))
