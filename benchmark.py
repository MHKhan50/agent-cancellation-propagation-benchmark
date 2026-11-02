"""Synthetic benchmark for cancellation propagation in agent workflows."""
import csv, random
from pathlib import Path
POLICIES=("cooperative","polling","cancellation_blind","shielded_section")
def generate_scenarios(n=1200,seeds=(11,23,37,51,73)):
 rows=[]
 for seed in seeds:
  rng=random.Random(seed)
  for i in range(n):
   depth=rng.randint(2,6)
   rows.append({"scenario_id":f"s{seed}_{i:05d}","seed":seed,"workflow_depth":depth,"cancel_after_step":rng.randint(1,depth-1),"in_flight_calls":rng.randint(0,3),"side_effect_step":rng.choice([0,1,2,3]),"failure_mode":rng.choice(["user_cancel","parent_timeout","budget_exhausted"])})
 return rows
def simulate(row,policy):
 depth=int(row["workflow_depth"]); cancel=int(row["cancel_after_step"]); inflight=int(row["in_flight_calls"]); side=int(row["side_effect_step"]); possible=int(side>cancel and side<=depth and side>0)
 if policy=="cooperative": dispatch,orphan,latency,effects=0,0,1,int(possible and inflight>0)
 elif policy=="polling": dispatch,orphan,latency,effects=min(1,depth-cancel),min(inflight,1),2,int(possible and inflight>=2)
 elif policy=="cancellation_blind": dispatch,orphan,latency,effects=depth-cancel,inflight,depth-cancel+2,possible
 elif policy=="shielded_section": dispatch,orphan,latency,effects=possible,max(0,inflight-1),2+possible,possible
 else: raise ValueError(f"Unknown policy: {policy}")
 return {"policy":policy,"post_cancel_dispatches":dispatch,"orphaned_calls":orphan,"cancel_latency_steps":latency,"post_cancel_side_effects":effects,"cancel_compliance":int(dispatch==0 and effects==0)}
def evaluate(rows): return [{**r,**simulate(r,p)} for r in rows for p in POLICIES]
def summarize(results):
 out=[]
 for p in POLICIES:
  s=[r for r in results if r["policy"]==p]; n=len(s)
  out.append({"policy":p,"episodes":n,"mean_post_cancel_dispatches":round(sum(x["post_cancel_dispatches"] for x in s)/n,4),"mean_orphaned_calls":round(sum(x["orphaned_calls"] for x in s)/n,4),"mean_cancel_latency_steps":round(sum(x["cancel_latency_steps"] for x in s)/n,4),"post_cancel_side_effect_rate":round(sum(x["post_cancel_side_effects"] for x in s)/n,4),"cancel_compliance_rate":round(sum(x["cancel_compliance"] for x in s)/n,4)})
 return out
def write_csv(path,rows):
 with Path(path).open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
