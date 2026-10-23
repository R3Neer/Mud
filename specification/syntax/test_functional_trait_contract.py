"""Preclassified source-shape fixtures; not scanner/resolver/type inference."""
import re,unittest
from pathlib import Path
from specification.grammar.ebnf_analysis import grammar_trees,lower_to_bnf,recognises
ROOT=Path(__file__).resolve().parents[2]


class FunctionalTraitSyntax(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bnf=lower_to_bnf(grammar_trees((ROOT/'specification/grammar/mud.ebnf').read_text(encoding='utf-8')))

    def accepts(self,start,source):
        raw=re.findall(r'-->|:=|->|===|!==|>>|<<|>=|<=|==|!=|[A-Za-z][A-Za-z0-9]*|[0-9]+|[^\s]',source)
        keywords={'let','mut','trait','value','first','all','ordered','unique','by','in','as','with','alias','thing','true','false','empty','_'}
        tokens=[];depth=0
        for index,t in enumerate(raw):
            if t==';':tokens.append('TERMINATOR')
            elif t.isdigit():tokens.append('EXACT_INTEGER_LITERAL' if t=='3' else 'EXACT_NUMBER_LITERAL')
            elif t=='with' and source.startswith('trait '):tokens.append('HEADER_WITH')
            elif t in keywords or not t[0].isalnum():tokens.append('"'+t+'"')
            else:tokens.append('IDENTIFIER')
            if t=='[':depth+=1
            elif t==']':depth-=1
        return recognises(self.bnf,start,tokens)

    def test_trait_fields_operator_requirements_and_generic_parameter(self):
        for source in ('trait Named { name: String }','trait Addable { + }',
                       'trait Numeric { +; ==; === }','trait Mutable { mut size: Nat }',
                       'trait Box with T { item: T }',
                       'trait IntAdd { +: Int --> Int --> Int }'):
            self.assertTrue(self.accepts('trait-declaration',source),source)
        self.assertFalse(self.accepts('trait-declaration','trait Bad { + = a + b }'))

    def test_named_inferred_and_collection_curried_signatures(self):
        for source in ('let add: (a: Int) --> (b: Int) --> Int = a + b',
                       'let add: a --> b --> _ = a + b','let add = a + b',
                       'let f: Int [*] --> Int [*] --> Int = value[1]',
                       'let policies: A --> (B --> C) [3 ordered] = body'):
            self.assertTrue(self.accepts('stored-field-declaration',source),source)

    def test_policy_modes_and_operator_reference(self):
        for source in ('first { value > 0 --> Positive, _ --> Other }',
                       'all { > 0 --> Positive, >= 0 --> Nonnegative }','(+)','(===)',
                       'f >> g[x]','f[x] >> g[y]','f[(a,b),c]','value[1]'):
            self.assertTrue(self.accepts('expression',source),source)

    def test_symbol_named_operator_implementation_and_projection(self):
        self.assertTrue(self.accepts('operator-declaration','+: (a: V) --> (b: V) --> V = a'))
        self.assertTrue(self.accepts('operator-declaration','*: Num --> V --> V := body'))
        self.assertTrue(self.accepts('expression','Vector.+'))
        self.assertTrue(self.accepts('expression','item.=='))
        self.assertTrue(self.accepts('expression','Bool.not'))
        self.assertFalse(self.accepts('operator-declaration','==: V --> V --> Bool = true'))

    def test_reserved_value_is_not_an_ordinary_local_but_member_is_legal(self):
        self.assertFalse(self.accepts('local-stored-declaration','let value = 3'))
        self.assertTrue(self.accepts('component-declaration','let value: Nat'))
        self.assertTrue(self.accepts('expression','record.value'))
