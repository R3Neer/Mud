"""Finite certificates; no compiler, type erasure engine or runtime."""
import unittest
from functional_trait_witnesses import (
    specialize_rows,implicit_binders,application_choice,fields_satisfy,
    normalized_requirements,coherent_operators,
    aggregate_contribution_certificate,
)
from validate_type_spec import includes


class FunctionalTraitWitnesses(unittest.TestCase):
    def test_allmatches_sums_exterior_occurrences_and_keeps_repetitions(self):
        result = aggregate_contribution_certificate(((1, 2), (3, 4), (1,)))
        self.assertEqual(result, (1, 2, 3, 4, 1))
        self.assertEqual(len(result), sum(map(len, ((1, 2), (3, 4), (1,)))))

    def test_allmatches_does_not_flatten_nested_members(self):
        result = aggregate_contribution_certificate((((1, 2),), ((3, 4),)))
        self.assertEqual(result, ((1, 2), (3, 4)))
        self.assertEqual(len(result), 2)

    def test_empty_contribution_does_not_add_a_wrapper(self):
        self.assertEqual(aggregate_contribution_certificate(((), (7,), ())), (7,))
        self.assertEqual(aggregate_contribution_certificate(()), ())

    def setUp(self):
        self.rows=tuple({'inputs':(t,t),'result':t} for t in ('Int','Num','Rum','Money','Vector2'))

    def test_family_partial_literal_retains_correlated_alternatives(self):
        residual=specialize_rows(self.rows,[{'Int','Num','Rum','Money'}])
        self.assertEqual(len(residual),4)
        self.assertEqual(specialize_rows(residual,[{'Money'},{'Vector2'}]),())
        self.assertEqual(specialize_rows(residual,[{'Money'},{'Money'}])[0]['result'],'Money')

    def test_typed_capture_is_not_reinterpreted(self):
        residual=specialize_rows(self.rows,[{'Int'}])
        self.assertEqual(len(residual),1)
        self.assertEqual(specialize_rows(residual,[{'Money'}]),())

    def test_copy_and_transmission_do_not_specialize_a_family(self):
        other=tuple(self.rows)
        self.assertEqual(specialize_rows(other,[{'Int'},{'Int'}])[0]['result'],'Int')
        self.assertEqual(specialize_rows(other,[{'Money'},{'Money'}])[0]['result'],'Money')
        self.assertEqual(other,self.rows)

    def test_free_binders_are_occurrence_ordered_and_labels_are_not_inputs(self):
        occurrences=[('variable','b'),('field','name'),('variable','a'),('variable','b'),
                     ('type','Num'),('variable','offset'),('foreign','native'),('variable','value')]
        self.assertEqual(implicit_binders(occurrences,{'offset'}),(('b','a'),('offset',)))

    def test_ambiguous_product_and_curried_paths_are_not_prioritized(self):
        self.assertEqual(application_choice(True,False),'product')
        self.assertEqual(application_choice(False,True),'curried')
        for args in ((True,True),(False,False)):
            with self.assertRaises(ValueError):application_choice(*args)

    def test_stored_derived_and_inherited_read_witnesses(self):
        req={'name':{'type':{'name':'String'}}}
        for kind in ('stored','derived','inherited'):
            actual={'name':{'type':{'name':'String'},'kind':kind},'extra':{'type':{'name':'Nat'}}}
            self.assertTrue(fields_satisfy(req,actual,{'name'},lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})))

    def test_private_fields_and_missing_authority_cannot_witness_a_view(self):
        req={'size':{'type':{'name':'Nat'},'write':True}}
        candidate={'size':{'type':{'name':'Nat'},'kind':'stored','write':True}}
        self.assertFalse(fields_satisfy(req,candidate,set(),lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})))
        candidate['size']['write']=False
        self.assertFalse(fields_satisfy(req,candidate,{'size'},lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})))

    def test_write_is_invariant_but_read_can_forget_stronger_type(self):
        actual={'size':{'type':{'name':'Nat'},'kind':'stored','write':True}}
        read={'size':{'type':{'name':'Int'}}};write={'size':{'type':{'name':'Int'},'write':True}}
        inc=lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})
        self.assertTrue(fields_satisfy(read,actual,{'size'},inc))
        self.assertFalse(fields_satisfy(write,actual,{'size'},inc))

    def test_sequence_requirement_does_not_require_a_specific_sort_key(self):
        actual={'items':{'type':{'name':'Int','card':[0,None],'order':'age'},'kind':'stored'}}
        req={'items':{'type':{'name':'Int','card':[0,None],'order':'sequence'}}}
        self.assertTrue(fields_satisfy(req,actual,{'items'},lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})))
        req['items']['type']['order']='name'
        self.assertFalse(fields_satisfy(req,actual,{'items'},lambda a,b:includes(a,b,{'Nat':['Int'],'Int':['Num']})))

    def test_requirement_equality_ignores_declaration_order_not_guarantees(self):
        a={'x':{'type':'Int'},'y':{'type':'String'}}
        b={'y':{'type':'String'},'x':{'type':'Int'}}
        self.assertEqual(normalized_requirements(a),normalized_requirements(b))
        b['x']['write']=True
        self.assertNotEqual(normalized_requirements(a),normalized_requirements(b))

    def op(self,origin,explicit=True,result='Int',semantic_key='builtin:add'):
        return {'symbol':'+','operands':['Left','Right'],'origin':origin,
                'explicit':explicit,'result':result,'semantic_key':semantic_key}

    def test_global_explicit_collision_ignores_result_and_owner_names(self):
        with self.assertRaises(ValueError):coherent_operators([self.op('Left.+'),self.op('Right.+',result='Num')])

    def test_diamond_deduplicates_and_explicit_beats_implicit(self):
        a=self.op('Base.+')
        self.assertEqual(len(coherent_operators([a,a])),1)
        chosen=coherent_operators([self.op('generated',False),a])
        self.assertEqual(chosen[0]['origin'],'Base.+')

    def test_incompatible_implicit_generations_are_rejected(self):
        with self.assertRaises(ValueError):coherent_operators([self.op('gen1',False),self.op('gen2',False,semantic_key='other')])
