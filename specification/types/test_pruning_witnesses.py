"""Finite supplied Bool/erased kernel certificates, not a Mud evaluator."""
import itertools
import unittest
E = 'erased'
def prune(t, values):
    if isinstance(t, str): return E if values[t] == E else t
    op, *children = t
    xs = [prune(x, values) for x in children]
    if op == 'not': return E if xs[0] == E else ('not', xs[0])
    xs = [x for x in xs if x != E]
    return E if not xs else xs[0] if len(xs) == 1 else (op, *xs)
def evaluate(t, values, cache, reads):
    if t == E: return True
    if isinstance(t, str):
        if t not in cache:
            reads.append(t); cache[t] = values[t]
        return cache[t]
    op, *xs = t
    if op == 'not': return not evaluate(xs[0], values, cache, reads)
    a = evaluate(xs[0], values, cache, reads)
    return (a and evaluate(xs[1], values, cache, reads)) if op == 'and' else (a or evaluate(xs[1], values, cache, reads))
class PruningWitnesses(unittest.TestCase):
    def test_all_finite_kernel_pairs(self):
        eq = ('or', ('and','p','q'), ('and',('not','p'),('not','q')))
        for p,q in itertools.product((False, True, E), repeat=2):
            for negated in (False, True):
                values={'p':p,'q':q}; reads=[]
                t=prune(('not',eq) if negated else eq,values)
                actual=evaluate(t,values,{},reads)
                expected=(True if p == q == E else not negated if E in (p,q) else (p != q if negated else p == q))
                self.assertEqual(actual,expected)
                self.assertEqual(len(reads),len(set(reads)))
                self.assertTrue(all(values[x] != E for x in reads))
    def test_empty_and_nonempty_no_filter(self):
        for size in (0,1,3):
            predicates=[True]*size
            self.assertEqual(any(predicates),size>0)
            self.assertTrue(all(predicates))
            self.assertEqual(sum(predicates),size)
if __name__ == '__main__': unittest.main()
