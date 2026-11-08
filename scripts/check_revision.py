"""Demand and quantity checks for the current deck-supported tread proposal."""
import json,math,itertools
from pathlib import Path
from collections import Counter
import numpy as np
from beam_helper import beam
root=Path(__file__).resolve().parents[1]
base=[22.5+437*i for i in range(16)]
joists=sorted([x for i,x in enumerate(base) if i!=9]+[3933,3978])
cleats=[175,1230,2300,3200,4200,5370,6425]
assert len(joists)==17 and max(np.diff(joists))<=450
assert all(abs(c+offset-j)>=47.5 for c in cleats for offset in [-40,40] for j in joists)
assert abs(300-22.5)<=300 and abs(2510-2532.5)<=300
main_alloc=[(6,7200,[6600]),(6,6000,[2465,2465,900]),(1,6000,[2465,2465,382.5,382.5]),(1,6000,[2465,2465]),(1,3000,[2465]),(1,4200,[1880,1880]),(1,2400,[1880])]
infill=[105,915,930,760,860,1030,915,105]
main_alloc.append((1,6000,infill))
h4_alloc=[(2,7200,[6600,414]),(1,6000,[414]*4+[310]*11),(1,2400,[414]+[310]*6)]
for n,s,cs in main_alloc+h4_alloc:assert sum(cs)+4*len(cs)+5<=s
main_counts=Counter(c for n,s,cs in main_alloc for c in cs for _ in range(n))
assert main_counts==Counter({6600:6,2465:17,900:6,382.5:2,1880:3})+Counter(infill),main_counts
h4_counts=Counter(c for n,s,cs in h4_alloc for c in cs for _ in range(n));assert h4_counts==Counter({6600:2,414:7,310:17})
# Rebuilt joists are separate members. Use1.8kN deck point, zero dead credit.
xs,u,solve,mom=beam(list(np.arange(-1.925,-.0449,.025))+[-1.925,-.8,-.045],[-1.925,-.8],6.5e6*.045*.14**3/12)
fg,qg=u(lambda x:.6*.45);F=np.repeat(np.zeros_like(fg)[:,None],len(xs),axis=1)
for i in range(len(xs)):F[2*i,i]=2.7
_,R=solve(F);# Include the45mm front rim beyond the modelled joist end:point may act atY0.
rebuilt_uplift=max(float(-R.min()),2.7*.8/1.125)
# Outer rail continuous over six pads;2.7kN stair point with rear/front board edge eccentricity.
pads=[.175,1.325,2.640,3.960,5.275,6.425]
xs,u,solve,mom=beam(list(np.arange(0,6.6001,.025))+pads,pads,6.5e6*.045*.14**3/12)
g,qg=u(lambda x:.6*.2);F=np.repeat((1.2*g)[:,None],len(xs),axis=1)
point=1.5*2.7*377.5/355
for i in range(len(xs)):F[2*i,i]+=point
D,R=solve(F);M=float(abs(mom(D,np.repeat((1.2*qg)[:,None],len(xs),axis=1))).max())
cap=.8*.8*11.7*(45*140**2/6)/1e6
xs_i,ui,si,mi=beam(list(np.arange(0,6.6001,.025))+[c/1000 for c in cleats],[c/1000 for c in cleats],6.5e6*.045*.14**3/12)
gi,qgi=ui(lambda x:.6*.2);Fi=np.repeat((1.2*gi)[:,None],len(xs_i),axis=1)
for i in range(len(xs_i)):Fi[2*i,i]+=point
Di,Ri=si(Fi);inner_M=float(abs(mi(Di,np.repeat((1.2*qgi)[:,None],len(xs_i),axis=1))).max());inner_R=float(Ri.max())
assert inner_M<cap

# Reference/equilibrium check and fresh main-bearer gravity envelope.
xt,ut,st,mt=beam([0,.5,1],[0,1],1);ft,qt=ut(lambda x:1);dt,rt=st(ft)
assert np.allclose(rt[:,0],[.5,.5]) and abs(abs(mt(dt,qt)).max()-.125)<1e-9
sx=[.0625,1.3575,2.6525,3.9475,5.2425,6.5375];bounds=[0]+sx+[6.6]
xm,um,sm,mm=beam(list(np.arange(0,6.6001,.025))+sx,sx,6.5e6*.09*.14**3/12)
gm,qgm=um(lambda x:.6*2.0);patches=[um(lambda x,a=a,b=b:4.0 if a<x<b else 0) for a,b in zip(bounds,bounds[1:])]
fm=[];qu=[]
for pat in itertools.product([0,1],repeat=len(patches)):
 f=sum((v*p[0] for v,p in zip(pat,patches)),start=np.zeros_like(gm));q=sum((v*p[1] for v,p in zip(pat,patches)),start=np.zeros_like(qgm))
 fm.append(1.2*gm+1.5*f);qu.append(1.2*qgm+1.5*q)
dm,rm=sm(np.array(fm).T);main_M=float(abs(mm(dm,np.array(qu).T)).max())
assert np.max(abs(rm.sum(axis=0)-np.array(fm).T[::2].sum(axis=0)))<1e-7
assert np.max(abs(Ri.sum(axis=0)-Fi[::2].sum(axis=0)))<1e-7

# Fresh planning concrete geometry; timber anchor section is provisional125sq.
main_concrete=4*(.35**2*.9-.125**2*.8)+12*(.35**2*.45-.125**2*.35)
pad_v=.35**2*.35+.2*.09*.17725
out={'status':'Working proposal; full hanging connection, bracing and footing verification unfinished',
 'main_joist_centres_mm':joists,'main_base_lines':16,'main_joist_members_with_supported_butt':17,'max_spacing_mm':max(np.diff(joists)),
 'main_bearer_Y_mm':[300,2510],'main_span_mm':2210,'wet_table_span_at450_mm':2350,
 'rebuilt_joists':3,'rebuilt_joist_cut_mm':1880,'rebuilt_bearer_Y_mm':[-1925,-800],'rear_bearer_rear_face_Y_mm':-1970,
 'rebuilt_lateral_blocks':2,'main_lateral_block_rows':0,'cleat_X_mm':cleats,'front_rim_outer_infill_cuts_mm':infill,
 'cleats':7,'cleat_cut_mm':414,'cleat_top_Z_mm':468,'cleat_bottom_Z_mm':54,'upper_bolt_Z_mm':380,'lower_bolt_Z_mm':152,
 'cleat_bolt_quantity_proposal':28,'cleat_bolts':'M12x120 SS316 candidate,2 upper+2 lower per cleat;full joint not verified',
 'main_pile_X_mm':[62.5,1357.5,2652.5,3947.5,5242.5,6537.5],
 'timber_piles':16,'candidate_anchor_piles':4,'ordinary_piles':12,'outer_tread_pads':6,'outer_pad_X_mm':[int(p*1000) for p in pads],
 'main_stock_lm':round(sum(n*s for n,s,c in main_alloc)/1000,3),'main_installed_lm':round(sum(n*sum(c) for n,s,c in main_alloc)/1000,3),
 'H4_stock_lm':round(sum(n*s for n,s,c in h4_alloc)/1000,3),'H4_installed_lm':round(sum(n*sum(c) for n,s,c in h4_alloc)/1000,3),
 'main_stock_allocations':[{'count':n,'stock_mm':s,'cuts_mm':c} for n,s,c in main_alloc],
 'H4_stock_allocations':[{'count':n,'stock_mm':s,'cuts_mm':c} for n,s,c in h4_alloc],
 'decking':{'main_rows':28,'rebuilt_rows':22,'tread_rows':5,'stock_4200':39,'stock_3000':33,'stock_lm':262.8,'pricing_allowance_lm':270,
 'base_screws':(28+5)*17*2+22*3*2,'purchase_allowance_screws':1500,'width_basis_mm':88,'gaps':'Illustrative ~5mm;actual board/moisture instructions govern'},
 'concrete_geometry_only':{'main_net_m3':main_concrete,'outer_pad_each_m3':pad_v,'six_pads_m3':6*pad_v,'combined_net_m3':main_concrete+6*pad_v,
 'main_anchor_holes_mm':[350,350,900],'ordinary_holes_mm':[350,350,450],'outer_pad_base_mm':[350,350,350],
 'outer_pad_head_mm':[200,90,177.25],'outer_pad_centre_Y_mm':2955,'outer_pad_base_bottom_Z_mm':-450,'outer_pad_base_top_Z_mm':-100,'outer_pad_top_Z_mm':77.25,
 'warning':'Conditional geometry,not a concrete order. Main anchor section and complete outer pad restraint remain unverified.'},
 'screens':{'rebuilt_zero_dead_uplift_ULS_kN':rebuilt_uplift,'SSCPC40_pair_conservative_screen_kN':2.688,
 'outer_rail_point_ULS_kN':point,'outer_rail_max_M_ULS_kNm':M,'outer_rail_bending_screen_capacity_kNm':cap,'outer_rail_utilisation':M/cap,
 'inner_rail_full_point_reaction_ULS_kN':point,'inner_rail_max_M_ULS_kNm':inner_M,'inner_cleat_max_reaction_ULS_kN':inner_R,
 'rim_eccentricity_mm':90,'rim_eccentric_moment_kNm':inner_R*.09,'cleat_local_eccentricity_mm':45,'cleat_local_moment_kNm':inner_R*.045,
 'main_bearer_max_M_ULS_kNm':main_M,'main_loaded_width_envelope_m':2.0,
 'note':'Beam/component demand screens only;not full rim-cleat-bolt-nog-pad-anchorage verification. Outer rail must be continuous6600mm.'}}
assert rebuilt_uplift<2.688
assert M<cap,(M,cap)
assert out['main_stock_lm']==106.8 and out['main_installed_lm']==98.93
assert out['H4_stock_lm']==22.8 and out['decking']['base_screws']==1254
(root/'design.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['main_stock_lm','main_installed_lm','H4_stock_lm','timber_piles','candidate_anchor_piles','ordinary_piles','outer_tread_pads','screens','concrete_geometry_only']},indent=2))
