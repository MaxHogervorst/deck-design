import ast,json,itertools
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
# Reuse only the previously reference-checked beam helper; do not execute the
# historical tread model or overwrite its results file.
source=ast.parse((root/'calculations/structural_check.py').read_text())
helper=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='beam')
space={'np':np};exec(compile(ast.Module(body=[helper],type_ignores=[]),'<reviewed-beam-helper>','exec'),space)
beam=space['beam']
supports=[.25,1.0675,1.66,2.9675,3.91,5.13,6.0075,6.525]
bounds=[0]+supports+[6.6]
points=list(np.arange(0,6.6001,.05))+bounds
xs,uniform,solve,moments=beam(points,supports,6.5e6*(.09*.14**3/12))
fg,qg=uniform(lambda x:.6*2.0)
patches=[uniform(lambda x,a=a,b=b:4.0 if a<x<b else 0) for a,b in zip(bounds,bounds[1:])]
F=[];FU=[];QU=[]
for pattern in itertools.product([0,1],repeat=len(patches)):
 fq=sum((v*p[0] for v,p in zip(pattern,patches)),start=np.zeros_like(fg))
 qq=sum((v*p[1] for v,p in zip(pattern,patches)),start=np.zeros_like(qg))
 F.append(fg+fq);FU.append(1.2*fg+1.5*fq);QU.append(1.2*qg+1.5*qq)
d,r=solve(np.array(F).T);du,ru=solve(np.array(FU).T)
fp=np.repeat(fg[:,None],len(xs),axis=1)
for i in range(len(xs)):fp[2*i,i]+=3.0
_,rp=solve(fp)
max_reaction=max(float(r.max()),float(rp.max()))
max_q=(max_reaction+(.35**2*.9-.125**2*.8)*24+.125**2*(.8+.28725)*.8*9.81)/.35**2
result={'support_X_m':supports,'mesh_nodes':len(xs),'patterns':len(F),'loaded_dimension_screen_m':2.0,'dead_kPa':.6,'imposed_kPa':2.0,'alternative_service_point_to_bearer_kN':3.0,
        'max_service_pile_reaction_kN':max_reaction,'max_uls_pile_reaction_kN':float(ru.max()),'max_uls_bearer_moment_kNm':float(abs(moments(du,np.array(QU).T)).max()),
        'maximum_gravity_pressure_including_deep_footing_and_pile_kPa':float(max_q),
        'equilibrium_error_kN':float(abs(r.sum(axis=0)-np.array(F).T[::2].sum(axis=0)).max()),
        'scope':'Continuous bearer gravity-demand envelope, no inferred member/connection resistance. Ground100kPa assumed; no tread loads transferred to deck.'}
assert result['equilibrium_error_kN']<1e-7
assert result['maximum_gravity_pressure_including_deep_footing_and_pile_kPa']<100
(root/'calculations/new_main_demand.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
