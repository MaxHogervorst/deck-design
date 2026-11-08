# Preliminary demand analysis; not a certified structural design.
# Requires numpy (verified here with2.3.5). No resistance is inferred from demand.
import json,itertools
import numpy as np
from pathlib import Path

# Euler-Bernoulli beam, m/kN. Downward displacements and loads positive.
def beam(points,supports,EI):
    xs=np.array(sorted(set(round(float(x),8) for x in points)))
    n=len(xs);K=np.zeros((2*n,2*n));elems=[]
    for i in range(n-1):
        L=xs[i+1]-xs[i]
        ke=EI/L**3*np.array([[12,6*L,-12,6*L],[6*L,4*L*L,-6*L,2*L*L],[-12,-6*L,12,-6*L],[6*L,2*L*L,-6*L,4*L*L]])
        ix=np.arange(2*i,2*i+4);K[np.ix_(ix,ix)]+=ke;elems.append((L,ke,ix))
    fixed=np.array([2*int(np.argmin(abs(xs-s))) for s in supports]);free=np.array([j for j in range(2*n) if j not in fixed])
    def uniform(qfun):
        f=np.zeros(2*n);qs=[]
        for i,(L,ke,ix) in enumerate(elems):
            q=qfun((xs[i]+xs[i+1])/2);qs.append(q);f[ix]+=q*np.array([L/2,L*L/12,L/2,-L*L/12])
        return f,np.array(qs)
    def solve(F):
        if F.ndim==1:F=F[:,None]
        D=np.zeros(F.shape);D[free]=np.linalg.solve(K[np.ix_(free,free)],F[free]);R=(K@D-F)[fixed]
        return D,-R
    def moments(D,Q):
        vals=[]
        if Q.ndim==1:Q=Q[:,None]
        for i,(L,ke,ix) in enumerate(elems):
            v=ke@D[ix]-np.array([L/2,L*L/12,L/2,-L*L/12])[:,None]*Q[i]
            vals.extend([v[1],v[3]])
        return np.array(vals)
    return xs,uniform,solve,moments

def joist(label,bounds,supports,width=.38):
    points=list(np.arange(bounds[0],bounds[-1]+.0001,.05))+bounds+supports
    xs,uni,solve,mom=beam(points,supports,6.5e6*(.045*.14**3/12))
    fg,qg=uni(lambda x:.6*width)
    patches=[]
    for a,b in zip(bounds,bounds[1:]):patches.append(uni(lambda x,a=a,b=b:2*width if a<x<b else 0))
    Fs=[];Qs=[]
    for pattern in itertools.product([0,1],repeat=len(patches)):
        Fs.append(1.2*fg+1.5*sum((on*p[0] for on,p in zip(pattern,patches)),start=np.zeros_like(fg)))
        Qs.append(1.2*qg+1.5*sum((on*p[1] for on,p in zip(pattern,patches)),start=np.zeros_like(qg)))
    F=np.array(Fs).T;Q=np.array(Qs).T;D,R=solve(F);M=mom(D,Q)
    # Point load is a separate alternative to distributed imposed action.
    FP=np.repeat((1.2*fg)[:,None],len(xs),axis=1)
    for i in range(len(xs)):FP[2*i,i]+=1.5*1.8
    DP,RP=solve(FP);DU,RU=solve(FP-1.2*fg[:,None]);MP=mom(DP,np.repeat((1.2*qg)[:,None],len(xs),axis=1))
    # Full service distributed load, with dead and imposed reaction contributions separate.
    ffull,qfull=uni(lambda x:2.6*width);df,rf=solve(ffull)
    return dict(label=label,supports_m=supports,max_uls_udl_moment_kNm=float(abs(M).max()),max_uls_point_moment_kNm=float(abs(MP).max()),
        max_uls_udl_reactions_kN=R.max(axis=1).tolist(),min_uls_udl_reactions_kN=R.min(axis=1).tolist(),max_uls_point_reactions_kN=RP.max(axis=1).tolist(),min_uls_point_reactions_kN=RP.min(axis=1).tolist(),min_point_reactions_zero_dead_credit_kN=RU.min(axis=1).tolist(),
        full_service_reactions_kN=rf[:,0].tolist(),full_service_max_deflection_mm=float(abs(df[::2]).max()*1000),
        ULS_udl_equilibrium_error_kN=float(np.max(abs(R.sum(axis=0)-F[::2].sum(axis=0)))))

normal=joist('main joist',[0,.35,2.25,2.6],[.35,2.25])
rebuilt=joist('rebuilt continuous joist',[-1.97,-1.795,-.8,.35,2.25,2.6],[-1.795,-.8,.35,2.25])
# Test a textbook simple beam before using calculations.
x,u,sol,m=beam([0,.5,1],[0,1],1)
f,q=u(lambda x:1);d,r=sol(f)
assert np.allclose(r[:,0],[.5,.5],atol=1e-9)
assert abs(abs(m(d,q)).max()-.125)<1e-9
assert abs(d[2,0]-5/384)<1e-9

area=6.6*2.6+.9*1.97+6.6*.4
bracing=dict(area_m2=area,Auckland_zone1_assumed_soil_DE_multiplier=.5,EQ_demand_BU_each=area*7.5*.5,
    candidate_six_anchor_capacity_BU=6*120,tread_EQ_demand_kN=6.6*.4*7.5*.5*.1,
    EQ_reference_zone3_factor1_BU=area*7.5)
# Existing cleat: two top bolts in ONE horizontal row, load at lower row.
# Contact at cleat top must develop a moment couple with the top bolt row.
h=(380-173)/1000;a=(468-380)/1000
cleat=[]
for F in [.5,1,2]:
    T=F*(1+h/a);C=F*h/a
    Z=190*45**2/6
    cleat.append(dict(horizontal_load_kN=F,top_group_tension_kN=T,top_bolt_tension_kN=T/2,
        top_contact_compression_kN=C,bending_moment_kNm=F*h,gross_bending_stress_MPa=F*h*1e6/Z,
        washer_face_stress_MPa=T*1000/2/(50*50-np.pi*11**2/4),
        transverse_load_top_bolt_inplane_shear_kN=F*np.sqrt((h/.075)**2+.5**2)))
    assert abs(T-C-F)<1e-9 and abs(C*a-F*h)<1e-9

# Conservative SINGLE 90x45 BOX rail screen: all stair point load to one rail,
# ideal simply-supported 1025 mm bay. Not a complete box-grillage analysis.
P=2.7;Pu=1.5*P;L=1.025
box=dict(stair_service_point_kN=P,screen_uls_point_kN=Pu,span_m=L,
    moment_kNm=Pu*L/4,stress_90x45_MPa=Pu*L/4*1e6/(45*90**2/6),
    stress_90x140_MPa=Pu*L/4*1e6/(140*90**2/6))
result=dict(assumptions={'area_live_kPa':2,'dead_kPa':.6,'deck_point_kN':1.8,'stair_point_kN':2.7,'Ewet_GPa':6.5,'ULS':'1.2G+1.5Q (screen only)','joist_tributary_width_m':.38},
    main_joist=normal,rebuilt_joist=rebuilt,bracing=bracing,current_drop_cleat_equilibrium=cleat,
    single_box_rail_screen=box,tests='textbook uniform simple beam reactions, moment and deflection matched; joist uniform-load equilibrium errors below tolerance')
assert normal['ULS_udl_equilibrium_error_kN']<1e-7
assert rebuilt['ULS_udl_equilibrium_error_kN']<1e-7


def bearerpart(bounds,supports):
    points=list(np.arange(bounds[0],bounds[-1]+.0001,.025))+bounds+supports
    xs,uni,solve,mom=beam(points,supports,6.5e6*(.09*.14**3/12))
    # Envelope: loaded length2.0m over the ENTIRE bearer, deliberately greater
    # than the actual main-deck strip outside the small rebuilt continuation.
    fg,qg=uni(lambda x:.6*2.0)
    ps=[uni(lambda x,a=a,b=b:2*2.0 if a<x<b else 0) for a,b in zip(bounds,bounds[1:])]
    FS=[];FU=[];QU=[]
    for pat in itertools.product([0,1],repeat=len(ps)):
        fq=sum((on*p[0] for on,p in zip(pat,ps)),start=np.zeros_like(fg))
        qq=sum((on*p[1] for on,p in zip(pat,ps)),start=np.zeros_like(qg))
        FS.append(fg+fq);FU.append(1.2*fg+1.5*fq);QU.append(1.2*qg+1.5*qq)
    ds,rs=solve(np.array(FS).T);du,ru=solve(np.array(FU).T)
    fpoint=np.repeat(fg[:,None],len(xs),axis=1)
    fpointU=np.repeat((1.2*fg)[:,None],len(xs),axis=1)
    for i in range(len(xs)):
        fpoint[2*i,i]+=3.0
        fpointU[2*i,i]+=3.7
    dp,rp=solve(fpoint);dpu,rpu=solve(fpointU);dg,rg=solve(fg)
    return dict(service_max_reaction_kN=rs.max(axis=1).tolist(),ULS_max_reaction_kN=ru.max(axis=1).tolist(),ULS_max_moment_kNm=float(abs(mom(du,np.array(QU).T)).max()),
        service_point_reaction_max_kN=rp.max(axis=1).tolist(),dead_reaction_kN=rg[:,0].tolist(),ULS_point_moment_kNm=float(abs(mom(dpu,np.repeat((1.2*qg)[:,None],len(xs),axis=1))).max()))
left=bearerpart([0,.25,1.47,2.69,3.91],[.25,1.47,2.69,3.91])
right=bearerpart([0,1.22,2.44,2.69],[0,1.22,2.44])
react=max(max(left['service_max_reaction_kN'][:-1]),left['service_max_reaction_kN'][-1]+right['service_max_reaction_kN'][0],max(right['service_max_reaction_kN'][1:]))
# Include own weight of a proposed deep anchor footing and its pile, without
# subtracting displaced soil. This is a conservative gravity-pressure screen.
pointreact=max(max(left['service_point_reaction_max_kN'][:-1]),max(right['service_point_reaction_max_kN'][1:]),
    left['service_point_reaction_max_kN'][-1]+right['dead_reaction_kN'][0],right['service_point_reaction_max_kN'][0]+left['dead_reaction_kN'][-1])
react=max(react,pointreact)
anchor_conc=(.35**2*.9-.125**2*.8)*24
pile_weight=.125**2*(.8+.186)*.8*9.81
result['bearer_envelope']={'loaded_dimension_m':2.0,'left':left,'right':right,'service_point_reaction_envelope_kN':pointreact,'max_service_pile_reaction_kN':react,'deep_footing_and_pile_self_weight_kN':anchor_conc+pile_weight,'maximum_gravity_soil_pressure_kPa':(react+anchor_conc+pile_weight)/.35**2,'conditional_allowable_soil_pressure_kPa':100,'limitation':'Uniform transverse reaction envelope with span-wise live patterns, not a coupled grillage or lateral foundation calculation; soil unverified.'}
result['limitations']=['0.6 kPa permanent action is an explicit screening allowance, not a measured dead load.','Beam supports are ideal rigid bearings; negative reaction values are required hold-down demands, not resistance supplied automatically.','Distributed and concentrated imposed actions are alternative cases. Point load is applied to one joist without credit for transverse sharing.','No strength grade is assigned to decking. No timber or bolt resistance is inferred from demand alone.','EQ bracing comparison is not a wind, distribution, torsion, soil or complete load-path verification.']
result['tread_global_centreline_screen']={
    'interpretation':'No pile-head moment resistance; reactions applied at y120/280. Real head/soil moments may redistribute these demands. This is a required load-path sensitivity, not a proven footing failure.',
    'point_2_7_at_front_edge_service_rear_kN':-2.7*.12/.16,
    'point_2_7_at_front_edge_service_front_kN':2.7*.28/.16,
    'conditional_independent_tread_line_kN_per_m':2.2,
    'conditional_full_width_line_service_total_kN':2.2*6.6,
    'conditional_full_width_front_edge_rear_kN':-2.2*6.6*.12/.16,
    'conditional_full_width_front_edge_front_kN':2.2*6.6*.28/.16,
    'line_case_scope':'Full-width front-edge line is a conservative interpretation of the independent-tread rule; actual applicability/load placement must be confirmed. Do not claim this rule automatically mandates a simultaneous full-width front-edge line for every tread system.'}
out=Path(__file__).with_name('results.json')
out.write_text(json.dumps(result,indent=2))
print('Beam reference tests and equilibrium checks passed. Results:',out)

