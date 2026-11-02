import unittest
from benchmark import generate_scenarios,evaluate,summarize,simulate,POLICIES
class BenchmarkTests(unittest.TestCase):
 def test_deterministic_generation(self): self.assertEqual(generate_scenarios(8,(11,23)),generate_scenarios(8,(11,23))); self.assertEqual(len(generate_scenarios(8,(11,23))),16)
 def test_four_policies_per_scenario(self): self.assertEqual(len(evaluate(generate_scenarios(4,(11,)))),4*len(POLICIES))
 def test_cooperative_stops_dispatch(self): self.assertEqual(simulate({"workflow_depth":5,"cancel_after_step":2,"in_flight_calls":2,"side_effect_step":4},"cooperative")["post_cancel_dispatches"],0)
 def test_blind_continues(self):
  x=simulate({"workflow_depth":5,"cancel_after_step":2,"in_flight_calls":2,"side_effect_step":4},"cancellation_blind"); self.assertEqual(x["post_cancel_dispatches"],3); self.assertEqual(x["post_cancel_side_effects"],1)
 def test_summary_shape(self): self.assertEqual(len(summarize(evaluate(generate_scenarios(3,(11,)))),),4)
if __name__=="__main__": unittest.main()
