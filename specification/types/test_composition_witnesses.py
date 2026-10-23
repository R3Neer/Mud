"""Supplied pure functions and postfix events; not a Mud parser/runtime."""
import unittest


def composed(left, right, reverse=False):
    def apply(value):
        upstream, downstream = (right, left) if reverse else (left, right)
        return downstream(upstream(value))
    return apply


def fold_events(first, events):
    # Finite preclassified precedence certificate: member/call=3, compose=2,
    # brackets=1. Event operands are supplied symbolic trees, never source text.
    values, operators = [first], []
    def reduce():
        op = operators.pop()
        right, left = values.pop(), values.pop()
        values.append((op, left, right))
    for op, argument in events:
        if op in ('>>', '<<'):
            while operators: reduce()
            operators.append(op); values.append(argument)
        else:
            precedence = 1 if op == 'index' else 3
            while operators and 2 >= precedence: reduce()
            values[-1] = (op, values[-1], argument)
    while operators: reduce()
    return values[0]


class CompositionWitnesses(unittest.TestCase):
    def test_direction(self):
        self.assertEqual(composed(lambda x:x+1,lambda x:x*2)(3),8)
        self.assertEqual(composed(lambda x:x+1,lambda x:x*2,True)(3),7)

    def test_complete_collection_and_empty_are_passed_once(self):
        seen=[]
        def count(items): seen.append(items); return len(items)
        self.assertEqual(composed(lambda _: [2,4,6],count)(0),3)
        self.assertEqual(composed(lambda _: [],count)(0),0)
        self.assertEqual(seen,[[2,4,6],[]])

    def test_upstream_fault_stops_downstream(self):
        seen=[]
        def fail(_): raise ValueError('upstream')
        with self.assertRaises(ValueError): composed(fail,lambda x:seen.append(x))(0)
        self.assertEqual(seen,[])

    def test_composition_binds_before_index(self):
        self.assertEqual(fold_events('f',[('>>','g'),('index','x')]),('index',('>>','f','g'),'x'))
        self.assertEqual(fold_events('f',[('index','x'),('>>','g'),('index','y')]),('index',('>>',('index','f','x'),'g'),'y'))

    def test_mixed_composition_folds_left_and_calls_bind_tighter(self):
        self.assertEqual(fold_events('f',[('>>','g'),('<<','h'),('index','x')]),('index',('<<',('>>','f','g'),'h'),'x'))
        self.assertEqual(fold_events('f',[('>>','g'),('call','x')]),('>>','f',('call','g','x')))
