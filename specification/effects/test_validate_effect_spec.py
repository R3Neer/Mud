import copy
import itertools
import json
import unittest
from validate_effect_spec import CORPUS, evaluate, validate

class EffectWitnessTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(CORPUS.read_text(encoding="utf-8"))
        self.cases={c["id"]:c for c in self.data["cases"]}
    def test_corpus(self): validate(self.data)
    def test_branch_permutations_preserve_results(self):
        for c in self.data["cases"]:
            w=c.get("witness",{})
            if w.get("kind")!="numeric": continue
            for branches in itertools.permutations(w["branches"]):
                candidate=copy.deepcopy(w);candidate["branches"]=list(branches)
                candidate.pop("private_reads",None)
                self.assertEqual(evaluate(candidate),w["expected"],c["id"])
    def test_textual_order_is_not_global_normal_form(self):
        w=copy.deepcopy(self.cases["textual-mixed-sequence"]["witness"])
        self.assertEqual(evaluate(w),13)
        w["branches"][0].reverse()
        self.assertEqual(evaluate(w),16)
    def test_wrong_expected_value_rejected(self):
        self.data["cases"][0]["witness"]["expected"]=16
        with self.assertRaises(ValueError):validate(self.data)
    def test_missing_effect_constructor_rejected(self):
        self.data["constructors"].pop("DestroyEffect")
        with self.assertRaises(ValueError):validate(self.data)
    def test_float_operand_rejected(self):
        w=copy.deepcopy(self.cases["textual-mixed-sequence"]["witness"])
        w["branches"][0][0][1]=2.0
        with self.assertRaises(ValueError):evaluate(w)
    def test_missing_operator_case_rejected(self):
        self.data["operators"]["DivideAssign"][1]="missing-case"
        with self.assertRaises(ValueError):validate(self.data)
    def test_nat_reads_do_not_truncate_pending_delta(self):
        self.assertEqual(evaluate(self.cases["nat-signed-private-ledger"]["witness"]),1)
    def test_uniqueness_restoration_rechecks_collisions(self):
        self.assertEqual(evaluate(self.cases["uniqueness-restoration-recheck"]["witness"]),{"a":"Red","b":"Blue"})
    def test_noop_create_preserves_payload_generation(self):
        self.assertEqual(evaluate(self.cases["redundant-create"]["witness"]),{"active":True,"generation":1,"payload":2})

if __name__=="__main__":unittest.main()
