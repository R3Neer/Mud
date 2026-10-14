"""Validate supplied finite scope/cache traces, not Mud code or a runtime."""
import unittest


def supplied_lookup(scopes, scope, name):
    seen = set()
    while scope is not None:
        if scope in seen:
            raise ValueError('cyclic supplied scope graph')
        seen.add(scope)
        if name in scopes[scope]['names']:
            return scopes[scope]['names'][name]
        scope = scopes[scope]['parent']
    return None


def supplied_no_shadowing(scopes):
    for scope, data in scopes.items():
        for name in data['names']:
            if data['parent'] is not None and supplied_lookup(scopes, data['parent'], name) is not None:
                return False
    return True


def supplied_reuse_trace(events):
    normal = {}
    for event in events:
        kind = event['kind']
        if kind == 'write':
            for key, deps in list(normal.items()):
                if key[0] == event['application'] and (event.get('unknown') or set(event['deps']) & deps):
                    del normal[key]
        elif kind == 'dispose':
            normal = {k: v for k, v in normal.items() if k[:2] != (event['application'], event['branch'])}
        else:
            key = (event['application'], event['branch'], event['binding'])
            deps = frozenset(event['deps'])
            if kind == 'compute':
                if key in normal:
                    return False  # Mandatory reuse: a valid binding cannot replay its RHS.
                if event['normal']:
                    normal[key] = deps
            elif kind == 'reuse':
                if key not in normal or deps != normal[key]:
                    return False
            else:
                raise ValueError('unknown supplied trace event')
    return True


class SelectorScopeReuseWitnesses(unittest.TestCase):
    def event(self, kind='compute', application='a', branch='b', binding='x', deps=('captured.x',), normal=True):
        return dict(kind=kind, application=application, branch=branch, binding=binding,
                    deps=deps, normal=normal)

    def scopes(self):
        return {'input': {'parent': None, 'names': {'value': 'input-origin'}},
                'selector': {'parent': 'input', 'names': {'adjusted': 'local-origin'}},
                'nested': {'parent': 'selector', 'names': {'hidden': 'nested-origin'}},
                'result': {'parent': 'selector', 'names': {}},
                'other': {'parent': 'input', 'names': {}}}

    def test_direct_local_reaches_result_without_copying_identity(self):
        self.assertEqual(supplied_lookup(self.scopes(), 'result', 'adjusted'), 'local-origin')
        self.assertEqual(supplied_lookup(self.scopes(), 'result', 'value'), 'input-origin')

    def test_nested_other_branch_and_outside_cannot_read_it(self):
        self.assertIsNone(supplied_lookup(self.scopes(), 'result', 'hidden'))
        self.assertIsNone(supplied_lookup(self.scopes(), 'other', 'adjusted'))
        self.assertIsNone(supplied_lookup(self.scopes(), 'input', 'adjusted'))

    def test_result_cannot_shadow_a_shared_selector_binding(self):
        scopes = self.scopes()
        self.assertTrue(supplied_no_shadowing(scopes))
        scopes['result']['names']['adjusted'] = 'new-origin'
        self.assertFalse(supplied_no_shadowing(scopes))

    def test_old_sibling_parent_loses_required_binding(self):
        scopes = self.scopes()
        scopes['result']['parent'] = 'input'
        self.assertIsNone(supplied_lookup(scopes, 'result', 'adjusted'))

    def test_normal_selector_then_result_reuses(self):
        self.assertTrue(supplied_reuse_trace([self.event(), self.event('reuse')]))
        self.assertFalse(supplied_reuse_trace([self.event(), self.event()]))

    def test_first_demand_can_be_in_result_and_unused_stays_lazy(self):
        self.assertTrue(supplied_reuse_trace([]))
        self.assertTrue(supplied_reuse_trace([self.event()]))

    def test_changed_dependency_invalidates(self):
        write = dict(kind='write', application='a', deps=['captured.x'])
        self.assertTrue(supplied_reuse_trace([self.event(), write, self.event()]))
        self.assertFalse(supplied_reuse_trace([self.event(), write, self.event('reuse')]))

    def test_unrelated_write_does_not_allow_replay(self):
        write = dict(kind='write', application='a', deps=['captured.y'])
        self.assertTrue(supplied_reuse_trace([self.event(), write, self.event('reuse')]))
        self.assertFalse(supplied_reuse_trace([self.event(), write, self.event()]))

    def test_unknown_overlap_invalidates_conservatively(self):
        write = dict(kind='write', application='a', unknown=True)
        self.assertTrue(supplied_reuse_trace([self.event(), write, self.event()]))

    def test_application_branch_and_recursive_instances_are_distinct(self):
        for following in (self.event(application='recursive'), self.event(branch='other')):
            self.assertTrue(supplied_reuse_trace([self.event(), following]))
            following['kind'] = 'reuse'
            self.assertFalse(supplied_reuse_trace([self.event(), following]))

    def test_fault_and_disposal_supply_no_reusable_normal_value(self):
        self.assertFalse(supplied_reuse_trace([self.event(normal=False), self.event('reuse')]))
        dispose = dict(kind='dispose', application='a', branch='b')
        self.assertFalse(supplied_reuse_trace([self.event(), dispose, self.event('reuse')]))
        self.assertTrue(supplied_reuse_trace([self.event(), dispose, self.event()]))

    def test_reuse_keeps_transitive_footprint(self):
        self.assertFalse(supplied_reuse_trace([self.event(deps=('root.x', 'root.y')),
                                             self.event('reuse', deps=('root.x',))]))

    def test_pattern_projections_share_the_supplied_rhs_origin(self):
        first = self.event(binding='pattern-rhs')
        second = self.event('reuse', binding='pattern-rhs')
        first['projection'] = 'left'
        second['projection'] = 'right'
        self.assertTrue(supplied_reuse_trace([first, second]))


if __name__ == '__main__':
    unittest.main()
