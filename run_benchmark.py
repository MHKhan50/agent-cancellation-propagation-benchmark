from pathlib import Path
import json
from benchmark import generate_scenarios,evaluate,summarize,write_csv
ROOT=Path(__file__).resolve().parent
def main():
 scenarios=generate_scenarios(); results=evaluate(scenarios); summary=summarize(results)
 write_csv(ROOT/"data"/"scenarios.csv",scenarios); write_csv(ROOT/"outputs"/"episode_results.csv",results); write_csv(ROOT/"outputs"/"policy_summary.csv",summary)
 payload={"benchmark":"Agent Cancellation Propagation Benchmark","version":"0.1.0","synthetic_scenarios":len(scenarios),"policies":[x["policy"] for x in summary],"episodes_evaluated":len(results),"metrics":summary,"interpretation_warning":"Synthetic simulator results only; not measurements of deployed agents."}
 (ROOT/"outputs"/"summary.json").write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8"); print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
