---
title: Canonical operator identity and reflection
status: proposed
normative: true
depends-on:
  - "[[../10-names-and-anchors]]"
  - "[[../11-type-system]]"
questions: []
decisions:
  - D-156
  - D-153
  - D-149
---

# Canonical operator identity and reflection

## Normalized contract input

> [!rule] MUD-NAME-008 — Complete operator signature encoding
> Encode the original alias owner, symbol, arity and ordered complete operand contracts. Retain nominal identities and normalized symbolic domains. Exclude operand binding names, result type, implementation, defaults, metadata, spans and physical files from signature identity. Normalize equivalent contract sugar before encoding. The encoding is textual and collision-free; an abbreviated display is not an anchor.

The input is the finite admitted normalized type-contract graph from chapter 11. A nominal reference is a leaf carrying its declaration anchor and exact static generic arguments; do not erase it or inline its implementation. Explicit domain/shape/capability restrictions remain separate nodes. An original generic signature uses its declaration's parameter slots; applied descriptor views substitute arguments without creating application anchors.

Every node has a constructor tag, an ordered vector of scalar labels and labelled outgoing edges. Scalar labels are strings or integers; compound information is represented by further labelled nodes. The complete labels are:

| Constructor | Labels and edges |
| --- | --- |
| Basic | Builtin identity; Any remains distinct. |
| Nominal/application | Declaration anchor and category; ordered exact argument edges. |
| Structural tuple | Named versus positional form, ordered member names, stored/calculated kind and complete member-contract edges. |
| Produced type | Original producer anchor and category, exact argument edges and ordered effective public schema. |
| Union | The normalized distinct alternatives as an unordered edge set. |
| Exact/functional dictionary | Key/value contracts, association specification or selection mode and applicable complete callable/authority guarantees. |
| Interval/domain | Member type and complete normalized domain: exact segment endpoints/open flags/steps, or symbolic expression graph. |
| Magnitude/point | Nominal identity, representation, nominal dimensional factors, point/cycle contract and exact arguments where applicable. |
| Descriptor | Specific descriptor category and statically refined target contract where present. |
| Callable | Category, ordered inputs with public slot names/contracts, outputs and authority/effect guarantees. |
| Collection | Member and domain edges; exact lower/upper bound, multiplicity, uniqueness/key path, order/criterion and immediate-member authority. Every nested layer remains explicit. |

Unbounded limits use an explicit infinity-tag node, not a missing label. Exact numeric labels use reduced numerator/positive-denominator nodes; binary64 constants retain their exact 16-hex-digit pattern. Resolved paths encode their original member anchors and structural positions, not presentation text. Symbolic expressions retain their normalized expression constructor, ordered operand edges and resolved reference anchors. Binder references use enclosing lexical binder depth and slot, with generic parameter slots ordered by the declaring header. Bound declarations retain their normalized bounds. Local binder spelling is not identity. No arbitrary predicate evaluation, current-world population or program-equivalence test is part of this normalization.

A normalized unrestricted nonnested singleton wrapper with no additional guarantees uses its member contract directly. Never apply this abbreviation to collapse a nested collection constructor or its inner layers. A nondefault domain/cardinality/order/uniqueness/authority layer is retained. A symbolic expression is only simplified by the language's established exact normalization rules; coincident current results do not equate different predicates. Callable public argument names remain significant where named invocation requires them, unlike operator-local operand names.

## Collision-free canonical graph form

1. Remove unreachable nodes. Identify structurally identical nodes by greatest labelled bisimulation, preserving all nominal labels. Sharing an identical subgraph is not observable identity; differing nominal leaves never merge.
2. Give the quotient's operand root number 0. Consider every bijection of its other nodes to consecutive numbers. For each, serialize nodes by increasing number and edges by label then target number. Ordered positions are part of edge labels; normalized set alternatives do not retain source order.
3. A serialized node is `[tag,[scalar-labels],[[edge-label,target-number],...]]`. The graph is the array of those nodes. All arrays retain order and multiplicity except the already normalized set edges.
4. Use JSON array/string/integer syntax with no optional whitespace. Integers have decimal spelling without leading zeros or plus signs. Strings escape quote/backslash and controls using the short escapes for backspace, form feed, newline, carriage return and tab and lowercase \u00xx for remaining controls. Ordinary ASCII, including slash, is not escaped; every non-ASCII scalar uses lowercase hexadecimal `\u` escapes (a surrogate pair for supplementary scalars). No Unicode normalization is added to resolved identifier identity.
5. Select the lexicographically least ASCII serialization. Prefix it with `contract(` and append `)`. This finite definition fixes a unique result independently of internal node numbers; an efficient equivalent implementation is permitted. Exhausting tool resources does not license a different encoding.

JSON string quoting, array framing and explicit references make the form uniquely decodable. Rooted quotient graph isomorphism yields the same minimum serialization, and equal decoded graphs recover equal constructor/label/edge contracts. This establishes collision freedom within the specified normalized-contract model, not general semantic equivalence of programs.

The bare builtin names Nat, Int, Num, Rum, Money, Text, Char, Bool and Any abbreviate exactly their unrestricted singleton contracts. A qualified alias identifier path abbreviates the corresponding unapplied unrestricted singleton nominal alias leaf. It is available only when distinct from reserved builtin spellings; all other contracts use graph form. Identifier path segments escape every UTF-8 byte except ASCII letters, digits and underscore as uppercase `%HH`, including separators occurring inside a segment. Dots separate segments. The original alias owner uses its existing canonical declaration anchor; ordinary anchor migrations remain explicit.

The anchor is `owner-anchor::operator::symbol(C1, C2)` for a binary signature and `owner-anchor::operator::symbol(C1)` for unary. Between binary operands write exactly comma-space; inside graph encoding write no whitespace. The symbol is one admitted token. Signature parentheses and operand count distinguish unary/binary occurrences of + and -. Parse the outer signature and embedded JSON strings/arrays before recognizing separators; a colon, comma, parenthesis or tilde inside a quoted label is data. Metadata adds the ordinary `~identifier` suffix after the completed outer signature; no metadata identity is derived from an abbreviated display.

```text
alias::path.Vector2::operator::*(path.Vector2, Num)
alias::path.Vector2::operator::-(path.Vector2)
```

The first operand's name a versus vector, and factor versus scalar, do not change these anchors. Num [2] or Num in [0..1] cannot use bare Num: their graph retains the nondefault collection/domain. Two distinct symbolic domains remain distinct even if a finite sample agrees. Reordered/duplicate union source forms normalize to the same contract; swapping two different operand contracts changes the ordered signature. Inherited generic operations keep the original generic-slot anchor even when their effective reflected result/operand types are substituted.

## Reflective schema

Operator descriptor admission is MUD-TYPE-036 in [[../11-type-system]].

| Property | Contract |
| --- | --- |
| `~owner` | Declaration descriptor of the original declaring alias. |
| `~anchor` | Anchor, using the original signature, also for inherited/applied views. |
| `~kind` | DeclarationKind, specifically Operator. |
| `~symbol` | Text, one admitted operator token. |
| `~arity` | Nat, exactly 1 or 2. |
| `~operands` | Immutable named `(name: Name, type: Type)` records, ordered, count equal to arity. |
| `~result` | Type, the checked effective result contract, with generic substitution for applied views. |
| `~path`, `~file` | Original owner's logical path and original declaration's physical provenance. |
| `~metadata` | Configured Metadata descriptors, using original declaration ownership. |
| Standard/user metadata | Existing metadata-owner rules; `~name` defaults to the operator symbol's presentation name. |

The operand descriptions have ordinary `.name` and `.type` components and TypeKind.Tuple. They have no own anchor, metadata, participant clause, writable authority or invocation value. Their record type does not introduce OperandDescriptor or another TypeKind. The operator descriptor has no source identifier, `~for`, `~on`, `~given`, default arguments or first-class callable signature; unsupported intrinsic accesses are static errors, not empty results. Its `~type` denotes the descriptor's own type, not its result or an OperatorCallable.

`Alias~operators` and `Alias~declaredOperators` return unique operator declaration descriptors, respectively own-plus-inherited and own-only, without selecting a best overload. Their collection order is unspecified. Deduplicate by original declaration identity. Different declaring aliases remain distinct even with equal operand signatures. A bulk query lacking access to any returned contract is rejected statically, never silently filtered. Inactive declarations retain their descriptors and configured metadata.
