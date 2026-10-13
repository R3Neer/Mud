"""Finite supplied Bool/erased kernel certificates, not a Mud evaluator."""
import itertools
import unittest
E = 'erased'

def supplied_derived_read(prefix, residual):
    """Certificate for an actual read, not general short-circuit scheduling."""
    prefix()
    return residual

def demanded_binary(op, left, right):
    """Finite supplied read certificate; erasure is never a truth value."""
    a = left()
    if op == 'and' and a is False:
        return False
    if op == 'or' and a is True:
        return True
    b = right()
    if a == E:
        return b
    if b == E:
        return a
    return a and b if op == 'and' else a or b

def demanded_equality(left, right, negated=False):
    """Each supplied source occurrence is read once in its original order."""
    a, b = left(), right()
    if a == b == E:
        return True
    if E in (a, b):
        return not negated
    return a != b if negated else a == b

def ordinary(residual):
    return True if residual == E else residual
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
    def test_ordered_prefix_short_circuit_and_faults(self):
        for op, decisive in (('or', True), ('and', False)):
            reads = []
            def faulting():
                reads.append('prefix')
                raise ValueError('supplied prefix fault')
            self.assertEqual(demanded_binary(op, lambda: decisive, faulting), decisive)
            self.assertEqual(reads, [])
            with self.assertRaises(ValueError):
                demanded_binary(op, faulting, lambda: decisive)
            self.assertEqual(reads, ['prefix'])
            reads.clear()
            def erased():
                reads.append('erased-prefix')
                return E
            self.assertEqual(demanded_binary(op, erased, lambda: decisive), decisive)
            self.assertEqual(reads, ['erased-prefix'])

    def test_equality_preserves_both_original_reads(self):
        for a, b in itertools.product((False, True, E), repeat=2):
            for negated in (False, True):
                reads = []
                def read(name, value):
                    reads.append(name)
                    return value
                result = demanded_equality(lambda: read('p', a), lambda: read('q', b), negated)
                expected = True if a == b == E else not negated if E in (a, b) else (a != b if negated else a == b)
                self.assertEqual(result, expected)
                self.assertEqual(reads, ['p', 'q'])
        for first_fault in (False, True):
            reads = []
            def fault():
                reads.append('fault')
                raise ValueError('supplied prefix fault')
            def erased():
                reads.append('erased')
                return E
            with self.assertRaises(ValueError):
                demanded_equality(fault if first_fault else erased, erased if first_fault else fault)
            self.assertEqual(reads, ['fault'] if first_fault else ['erased', 'fault'])

    def test_domain_transform_and_identical_shape_boundary(self):
        # A supplied identical singleton shape leaves the residual untouched.
        unchanged = E
        self.assertTrue(ordinary(E if unchanged == E else not unchanged))
        # A supplied domain transformation operates on ordinary members.
        admitted = [v for v in [ordinary(E)] if v is True]
        self.assertEqual(admitted, [True])
        self.assertFalse(not admitted[0])
        excluded = [v for v in [ordinary(E)] if v is False]
        self.assertEqual(excluded, [])
        self.assertEqual([ordinary(E)], [True])

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
    def test_actual_derived_read_versus_stored_capture(self):
        residual = supplied_derived_read(lambda: None, E)
        derived = prune(('not', 'p'), {'p': residual})
        self.assertTrue(evaluate(derived, {'p': residual}, {}, []))
        stored = True if residual == E else residual
        captured = prune(('not', 'p'), {'p': stored})
        self.assertFalse(evaluate(captured, {'p': stored}, {}, []))

    def test_actual_read_preserves_prefix_fault_before_erasure(self):
        reads = []
        def prefix():
            reads.append('initialize-n')
            raise ValueError('supplied computing fault')
        with self.assertRaises(ValueError):
            supplied_derived_read(prefix, E)
        self.assertEqual(reads, ['initialize-n'])
        # A supplied recovered ordinary result is not the original erasure.
        recovered = False
        self.assertTrue(evaluate(prune(('not', 'p'), {'p': recovered}),
                                 {'p': recovered}, {}, []))

    def test_erased_initial_goal_transmits_query_erasure(self):
        reads = []
        goal = supplied_derived_read(lambda: reads.append('goal-prefix'), E)
        # Only the selected wholly erased goal boundary is certified here.
        query = E if goal == E else 'ordinary-query-result'
        outer = prune(('not', 'query'), {'query': query})
        self.assertTrue(evaluate(outer, {'query': query}, {}, []))
        self.assertEqual(reads, ['goal-prefix'])
if __name__ == '__main__': unittest.main()
