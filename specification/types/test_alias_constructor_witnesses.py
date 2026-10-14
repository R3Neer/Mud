"""Finite supplied constructor certificates; not a Mud parser/typechecker."""
import unittest
from validate_type_spec import includes


def supplied_constructor(schema, arguments):
    if (schema.get('category') != 'alias' or not schema.get('structural')
            or schema.get('abstract') or not schema.get('resolved', True)):
        return False
    fields = [f for f in schema['fields'] if f.get('stored', True)]
    names = [f['name'] for f in fields]
    if len(names) != len(set(names)):
        raise ValueError('invalid supplied effective schema')
    named = [a.get('name') is not None for a in arguments]
    if any(named) and not all(named):
        return False
    selected = {}
    if all(named) and arguments:
        positions = []
        for argument in arguments:
            if argument['name'] not in names or argument['name'] in selected:
                return False
            positions.append(names.index(argument['name']))
            selected[argument['name']] = argument['contract']
        if positions != sorted(positions):
            return False
    elif arguments:
        if len(arguments) != len(fields):
            return False
        selected = {f['name']: a['contract'] for f, a in zip(fields, arguments)}
    for field in fields:
        source = selected.get(field['name'], field.get('default'))
        if source is None or not includes(source, field['contract'], {'Nat': ['Int'], 'Int': ['Num']}):
            return False
    return True


class AliasConstructorWitnesses(unittest.TestCase):
    def schema(self):
        return {'category': 'alias', 'structural': True, 'identity': 'alias::Pair',
                'fields': [{'name': 'x', 'contract': {'name': 'Num'}},
                           {'name': 'y', 'contract': {'name': 'Num'}, 'default': {'name': 'Nat'}}]}

    def arg(self, name=None, member='Nat'):
        return {'name': name, 'contract': {'name': member}}

    def test_positional_complete_and_no_implicit_unpacking(self):
        self.assertTrue(supplied_constructor(self.schema(), [self.arg(), self.arg()]))
        self.assertFalse(supplied_constructor(self.schema(), [self.arg()]))
        self.assertFalse(supplied_constructor(self.schema(), [self.arg(member='Pair')]))

    def test_named_omission_requires_default(self):
        self.assertTrue(supplied_constructor(self.schema(), [self.arg('x')]))
        self.assertFalse(supplied_constructor(self.schema(), [self.arg('y')]))

    def test_named_order_duplicate_unknown_and_mixed(self):
        for args in ([self.arg('y'), self.arg('x')], [self.arg('x'), self.arg('x')],
                     [self.arg('other')], [self.arg(), self.arg('y')]):
            self.assertFalse(supplied_constructor(self.schema(), args))

    def test_abstract_representation_and_runtime_type_are_not_constructors(self):
        for change in ({'abstract': True}, {'structural': False},
                       {'category': 'thing'}, {'category': 'runtime-type'}, {'resolved': False}):
            schema = {**self.schema(), **change}
            self.assertFalse(supplied_constructor(schema, [self.arg(), self.arg()]))

    def test_zero_arguments_require_every_default(self):
        schema = self.schema()
        self.assertFalse(supplied_constructor(schema, []))
        schema['fields'][0]['default'] = {'name': 'Nat'}
        self.assertTrue(supplied_constructor(schema, []))
        schema['fields'] = []
        self.assertTrue(supplied_constructor(schema, []))

    def test_single_component_and_derived_fields(self):
        schema = self.schema()
        schema['fields'] = [schema['fields'][0], {'name': 'derived', 'stored': False}]
        self.assertTrue(supplied_constructor(schema, [self.arg()]))
        self.assertFalse(supplied_constructor(schema, [self.arg('derived')]))

    def test_component_types_and_known_default_domains_are_checked(self):
        self.assertFalse(supplied_constructor(self.schema(), [self.arg(member='Text'), self.arg()]))
        schema = self.schema()
        schema['fields'][1]['contract'] = {'name': 'Num', 'domain': [0, 1]}
        schema['fields'][1]['default'] = {'name': 'Num', 'domain': [2, 2]}
        self.assertFalse(supplied_constructor(schema, [self.arg('x')]))

    def test_exact_generic_and_alias_identity_are_not_expected_result_guesses(self):
        schema = self.schema()
        schema['identity'] = 'alias::Pair(Num)'
        self.assertTrue(supplied_constructor(schema, [self.arg(), self.arg()]))
        self.assertEqual(schema['identity'], 'alias::Pair(Num)')
        self.assertNotEqual(schema['identity'], 'alias::OtherPair(Num)')


if __name__ == '__main__':
    unittest.main()
