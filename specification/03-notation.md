---
title: Mathematical notation and metalanguage
aliases:
  - Formal notation of MUD
tags:
  - mud/specification
  - mud/normativa
status: draft
normative: true
depends-on:
  - "[[00-editorial-conventions]]"
  - "[[01-scope-and-conformance]]"
  - "[[02-terminology]]"
questions: []
decisions:
  - D-070
  - D-118
---

# 03. Mathematical notation and metalanguage

## Scope

This chapter fixes conventions for reading the specification. Mathematical notation describes MUD; it is not source syntax and does not prescribe an implementation's memory layout. Each chapter defines its own semantic objects and judgments using these conventions. This draft does not define an evaluator or an execution protocol.

## Symbols and logic

Metavariables and their domains must be introduced before use. Typography assists reading but never supplies a missing definition.

| Form | Conventional use |
| --- | --- |
| $\mathcal A,\mathcal V$ | Universes and sets |
| $A,R,W$ | Sets, relations and structures |
| $a,v$ | Elements and values |
| $\Gamma,\Sigma,\rho$ | Environments |
| $\tau,\sigma$ | Types |
| $\mathsf{Success}$ | Named semantic categories |
| $\operatorname{dom}(f)$ | Named operations |

A subscript identifies the context of a quantity: $R_W$ is the relation $R$ for world $W$. Mathematical $=$ denotes equality, $\ne$ inequality and $:=$ definition. Code formatting distinguishes the MUD token `:=` from a mathematical definition.

| Notation | Meaning |
| --- | --- |
| $\neg P$, $P\land Q$, $P\lor Q$ | Negation, conjunction, disjunction |
| $P\Rightarrow Q$, $P\Leftrightarrow Q$ | Implication, equivalence |
| $\forall x\in A.\ P(x)$ | Every element of $A$ satisfies $P$ |
| $\exists x\in A.\ P(x)$ | Some element of $A$ satisfies $P$ |
| $\exists!x\in A.\ P(x)$ | Exactly one element of $A$ satisfies $P$ |

Quantifiers must have explicit domains. Equality, nominal identity and observational equivalence must be distinguished where they differ.

## Sets, tuples and collections

| Notation | Meaning |
| --- | --- |
| $x\in A$, $x\notin A$ | Membership, non-membership |
| $\varnothing$ | Empty set |
| $A\subset B$, $A\subseteq B$ | Strict inclusion, inclusion allowing equality |
| $A\cup B$, $A\cap B$, $A\setminus B$ | Union, intersection, difference |
| $\mathcal P(A)$, $\mathcal P_{\mathrm{fin}}(A)$ | All subsets, finite subsets |
| $\lvert A\rvert$ | Cardinality |
| $\{e(x)\mid x\in A\land P(x)\}$ | Set comprehension; duplicates have no effect |
| $A\times B$ | Cartesian product |
| $(x_1,\ldots,x_n)$ | Ordered tuple |

Structures displayed as tuples are equal component by component unless a different equivalence is explicitly defined. Angle brackets may display sequences or evaluation configurations; the surrounding definition must distinguish them.

$A^*$ denotes finite sequences over $A$, $\epsilon$ the empty sequence, $s\mathbin{\cdot}t$ concatenation and $\lvert s\rvert$ length. Sequence indices start at one unless otherwise specified.

A finite multiset over $A$ is a function $m:A\to\mathbb N$ with finite support $\{a\in A\mid m(a)>0\}$. Multiplicity carries no order. Each semantic collection must specify whether it is a set, sequence or multiset; none of these forms automatically describes every MUD collection.

## Functions, relations and graphs

$f:A\to B$ is total; $f:A\rightharpoonup B$ is partial. $\operatorname{dom}(f)$ contains inputs for which $f$ is defined, and $\operatorname{im}(f)$ contains their results. $f(a)\downarrow$ means defined and $f(a)\uparrow$ undefined; these symbols do not assert termination or a MUD failure outcome.

A finite map is a partial function with finite domain, displayed as $\{a_1\mapsto b_1,\ldots,a_n\mapsto b_n\}$ with distinct keys. Equality of partial functions requires equal domains and equal results for every input in that domain.

A binary relation $R\subseteq A\times B$ may be written $a\,R\,b$. $\operatorname{Id}_A=\{(a,a)\mid a\in A\}$ is identity. For $R\subseteq A\times B$ and $S\subseteq B\times C$, $a\,(S\circ R)\,c$ means that some $b\in B$ satisfies $a\,R\,b$ and $b\,S\,c$.

For a relation on one domain, $R^+$ is transitive closure and $R^*$ is reflexive-transitive closure. The star in $A^*$ instead denotes sequences; the base's declared category disambiguates it. These forms do not confer inheritance or subtype semantics on an arbitrary relation.

A directed graph is $(N,E)$ with $E\subseteq N\times N$. A path $\langle n_0,\ldots,n_k\rangle$ follows an edge at every adjacent pair; its length is $k$. A zero-length path contains one node. A partial order is reflexive, transitive and antisymmetric. A chapter using fixed points must define the ordered domain, function and selection of fixed point; writing an equation alone does not establish existence or uniqueness.

## Judgments and operational notation

A judgment's context, parameters and meaning must be declared locally. For example, $\Gamma;\Sigma\vdash e:\tau$ can express typing if its chapter defines it that way. $M\models P$ denotes satisfaction of a specified semantic property. Semicolons separate contexts and are not MUD syntax.

An inference rule has premises $J_1,\ldots,J_n$ and conclusion $J$:

$$
\frac{J_1\quad\cdots\quad J_n}{J}\;\mathsf{RuleName}
$$

A rule with no premises is an axiom. Rule names are unique within the specification. A derivation is a finite tree with axioms or accepted hypotheses at its leaves. All required side conditions must be explicit.

A big-step judgment may have the form $\langle X,e\rangle\Downarrow\langle X',r\rangle$. A small step may have the form $K\to K'$ or $K\xrightarrow{\ell}K'$, with $\to^*$ denoting its reflexive-transitive closure. Each system defines its configurations, labels, results and terminal states. The notation alone guarantees neither termination nor determinism and does not define a MUD runtime protocol.

## EBNF

The grammars in [[grammar/README]] use this dialect:

| Form | Meaning |
| --- | --- |
| `"token"` | Terminal literal |
| `name` | Nonterminal reference |
| `a, b` | Concatenation |
| `a \| b` | Alternative |
| `[ a ]` | Optional occurrence |
| `{ a }` | Zero or more occurrences |
| `( a )` | Grouping |
| `name ::= a ;` | Production definition |
| `? condition defined in prose ?` | Special form with an explicit prose contract |

One or more occurrences are written `a, { a }`. Metalanguage symbols that are also MUD tokens are quoted when used as terminals. The grammar and associated chapters specify precedence, associativity and contextual restrictions; EBNF notation alone does not establish unambiguity.

## ASDL-MUD and CST

The schema in [[syntax/mud-surface-ast.asdl]] uses the following ASDL dialect:

| Form | Meaning |
| --- | --- |
| `t = C(a x) \| D` | Sum with named constructors |
| `t = (a x, b y)` | Product |
| `T?` | Zero or one value |
| `T*` | Finite ordered sequence |
| `attributes (...)` | Common constructor attributes |

Built-in scalars are `identifier` (lexically validated text), `string` (Unicode text) and `int` (a mathematical integer, unbounded in the schema). The declared type `flag = Disabled | Enabled` represents a two-way flag. ASDL distinguishes semantic shapes without requiring a memory layout.

The lossless CST contract is defined in [[syntax/cst-lossless]], and its catalogue in [[syntax/mud-syntax-kinds.yaml]]. `SyntaxNode`, `SyntaxToken` and `SyntaxTrivia` retain the source's tokens and trivia. A category ending in `Syntax` denotes a production or recovery node. The Surface AST omits trivia.

`SourceSpan` uses zero-based UTF-8 byte offsets and an exclusive end. Lines and columns are also zero-based; columns count Unicode scalar values. LSP UTF-16 positions are converted at the interface boundary.

## Absence and outcomes

The specification distinguishes absence from a set, an undefined partial application, a domain value denoting absence, nontermination, a semantic outcome and an implementation failure. None implies another without an explicit rule.

`ActionReply` has the semantic alternatives `Success`, `Refusal` and a nonempty `Errors` value. A block's error channel may instead contain zero or more Error occurrences. An Error carried as an ordinary value is not automatically a raised error. The contracts for these distinctions are defined in [[19-expressions]].

## Use in other chapters

Each chapter must define its universes, quantifier domains, judgments and arrows; distinguish total from partial functions and identity from other equality; identify collection shapes; and explain overloaded notation. Additional mathematical machinery is introduced where required, with its assumptions and semantic purpose. This chapter does not reserve notation for an unimplemented probability model or other future machinery.
