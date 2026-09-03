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
---

# 03. Mathematical notation and metalanguage

## State and purpose

This chapter defines the metalanguage used to define MUD. Its purpose is to ensure that the same mathematical construct does not change in meaning from one chapter to the next and to clearly distinguish between:

- The syntax that a person writes in a file `.mud`.
- The mathematical structures used to describe it.
- The propositions with which the specification formulates its properties.

The formulas in this chapter belong to specification, not to the MUD syntax. An implementation is not obliged to represent objects internally using these same structures, but its observable behaviour must comply with the definitions constructed using them.

This chapter is a draft. The conventions defined here may be used in other drafts, but they do not acquire state current until the cycle of review is completed.

## Sub-units

- [[00-editorial-conventions|Stylistic conventions of the specification MUD]].
- [[01-scope-and-conformance|Scope, conformance and versions ]].
- [[02-terminology|Terminology]].

## 1. Typographical conventions

Typography conveys information, but it will never be the only way to distinguish between two semantic categories.

| Form | Main use | Examples |
| --- | --- | --- |
| $\mathcal A,\mathcal C,\mathcal V$ | Notable universes and sets | Universe of anchors |
| $A,B,R,W$ | Sets, relations and concrete structures | State of world |
| $a,c,v,w$ | Elements and values | An anchor or an value |
| $\Gamma,\Sigma,\rho$ | Environments and name assignments | Environment |
| $\tau,\sigma$ | Types | Type of an expression |
| $\mathsf{accepted}$ | Formal categories and literal names in the metalanguage | Result of a request |
| $\operatorname{dom}(f)$ | Named operations | Domain of a function |

Specific names used in mathematical examples may be written in sans serif:

$$
\mathsf{Gate}
\qquad
\mathsf{open}
$$

A metavariable is introduced in prose or by means of a quantifier before it is used. The subscript identifies the object in relation to which a quantity is interpreted:

$$
R_W
$$

It reads ‘the relation $R$ corresponding to $W$’. Changing the subscript may change the object referred to.

## 2. Equality, definition and logic

The mathematical equality is written as:

$$
x=y
$$

The inequality is written as:

$$
x\neq y
$$

The symbol `:=` introduces a definition into the metalanguage:

$$
A:=\{x\in B\mid P(x)\}
$$

The formula reads: ‘$A$ is defined as the set of elements $x$ of $B$ that satisfy $P$’. `:=` is not the operator `:=` that may appear in the concrete syntax of MUD; the mathematical context and the code block distinguish between them.

Standard connectors are used:

| Notation | Reading |
| --- | --- |
| $\neg P$ | not $P$ |
| $P\land Q$ | $P$ y $Q$ |
| $P\lor Q$ | $P$ o $Q$ |
| $P\Rightarrow Q$ | if $P$, then $Q$ |
| $P\Leftrightarrow Q$ | $P$ if and only if $Q$ |
| $\forall x\in A.\ P(x)$ | for all $x$ of $A$, $P(x)$ | holds
| $\exists x\in A.\ P(x)$ | there exists some $x$ of $A$ that satisfies $P(x)$ |
| $\exists!x\in A.\ P(x)$ | there exists a unique $x$ of $A$ that satisfies $P(x)$ |

The characters following the domain in a quantifier are separators, not MUD operators.

## 3. Sets

Membership and non-membership are written as:

$$
x\in A
\qquad
x\notin A
$$

The empty set is $\varnothing$. Inclusions are written as:

$$
A\subset B
\qquad
A\subseteq B
$$

In this specification, $A\subset B$ requires that $A$ be a strict subset of $B$. The form $A\subseteq B$ allows both sets to be equal. This convention will be maintained even when an external mathematical source uses $\subset$ in a non-strict sense.

Set operations are:

| Notation | Operation |
| --- | --- |
| $A\cup B$ | Unión |
| $A\cap B$ | Intersection |
| $A\setminus B$ | Difference |
| $\mathcal P(A)$ | Power unit |
| $\mathcal P_{\mathrm{fin}}(A)$ | Finite subsets of $A$ |
| $\lvert A\rvert$ | Cardinality of $A$ |

Understanding:

$$
\{x\in A\mid P(x)\}
$$

denotes the subset of $A$ whose elements satisfy $P$. The notation:

$$
\{e(x)\mid x\in A\land P(x)\}
$$

denotes the images $e(x)$ obtained from the elements that satisfy the condition. Repetitions do not produce any additional elements.

A set parameterised by an object uses a subscript. For example, $\mathcal A_P$ may denote the set of anchors provided by a programme $P$, provided that the corresponding chapter defines it.

## 4. Tuples and Cartesian products

An ordered pair is written as:

$$
(x_1,\ldots,x_n)
$$

The order and position of its components form part of its meaning. The parentheses in a tuple do not denote a set.

The Cartesian product is:

$$
A\times B
:=
\{(a,b)\mid a\in A\land b\in B\}
$$

For a mathematical structure, the following can be used:

$$
S=(A,R,f)
$$

Equality between two structures of this form requires equality component by component, unless the chapter that defines them explicitly establishes another notion of equivalence.

Angle brackets:

$$
\langle X,e\rangle
$$

They are preferably reserved for evaluation configurations or transition. They remain an ordered grouping; their typographical form helps to distinguish an operational configuration from a data tuple.

## 5. Total and partial functions

A total function is declared as follows:

$$
f:A\to B
$$

and must assign a unique value $f(a)\in B$ to each $a\in A$.

A partial function is defined as follows:

$$
f:A\rightharpoonup B
$$

and may not be defined for some elements of $A$. Its effective domain and its image are:

$$
\operatorname{dom}(f)
:=
\{a\in A\mid f(a)\text{ está definida}\}
$$

$$
\operatorname{im}(f)
:=
\{f(a)\mid a\in\operatorname{dom}(f)\}
$$

The abbreviation for ‘the application is defined’ is:

$$
f(a)\downarrow
\quad\Leftrightarrow\quad
a\in\operatorname{dom}(f)
$$

The absence of result is abbreviated as:

$$
f(a)\uparrow
\quad\Leftrightarrow\quad
a\notin\operatorname{dom}(f)
$$

In these expressions, $\downarrow$ and $\uparrow$ merely state whether the application is defined. They do not in themselves imply acceptance, rejection, failure or termination of an execution.

A partial function is finite if its effective domain is finite:

$$
f:A\rightharpoonup B
\qquad
\lvert\operatorname{dom}(f)\rvert<\infty
$$

A finite map can be displayed in full:

$$
f=
\{
a_1\mapsto b_1,
\ldots,
a_n\mapsto b_n
\}
$$

The arrow $\mapsto$ means ‘is associated with’. Each key must appear no more than once.

Two partial functions are equal if they have the same effective domain and match in all their inputs:

$$
f=g
\quad\Leftrightarrow\quad
\operatorname{dom}(f)=\operatorname{dom}(g)
\land
\forall x\in\operatorname{dom}(f).\ f(x)=g(x)
$$

## 6. Relationships

A binary relation between $A$ and $B$ is a subset:

$$
R\subseteq A\times B
$$

The expressions:

$$
(a,b)\in R
\qquad
a\,R\,b
$$

they are equivalent provided that the second one is legible.

The relation identity over $A$ is:

$$
\operatorname{Id}_A
:=
\{(a,a)\mid a\in A\}
$$

If $R\subseteq A\times B$ and $S\subseteq B\times C$, their composition is:

$$
S\circ R
:=
\{
(a,c)\in A\times C
\mid
\exists b\in B.\ a\,R\,b\land b\,S\,c
\}
$$

For an relation $R\subseteq A\times A$:

- $R^+$ denotes its transitive closure.
- $R^*$ denotes its reflexive and transitive closure.

These closures do not imply that a specific relation in MUD is an inheritance, a member or a subtype. Each chapter must declare the meaning of its own relation.

## 7. Sequences and multisets

$A^*$ denotes the set of finite sequences of elements of $A$. The empty sequence is written as $\epsilon$ and a specific sequence:

$$
\langle a_1,\ldots,a_n\rangle
$$

The length of a sequence $s$ is written as $\lvert s\rvert$. Concatenation is written as $s\mathbin{\cdot}t$. Unless otherwise stated, the indices of a sequence start at $1$.

The superscript $*$ is overloaded in the conventional manner: in $A^*$ it forms finite sequences, and in $R^*$ it forms the reflexive and transitive closure of an relation. The type in the base must ensure that each occurrence is unambiguous.

A finite multiset over $A$ is modelled as a function:

$$
m:A\to\mathbb{N}
$$

with finite support, where $m(a)$ is the multiplicity of $a$ and:

$$
\operatorname{supp}(m)
:=
\{a\in A\mid m(a)>0\}
$$

It is finite. This representation distinguishes a multiset from a set without imposing any order on it.

## 8. Graphs and paths

A directed graph is a pair:

$$
G=(N,E)
$$

where $N$ is the set of nodes and $E\subseteq N\times N$ is the relation of edges.

A finite path from $n_0$ to $n_k$ is a sequence:

$$
\langle n_0,\ldots,n_k\rangle
$$

such that:

$$
\forall j\in\{1,\ldots,k\}.\ (n_{j-1},n_j)\in E
$$

A path of length zero contains a single node. Chapters dealing with simple paths, cycles or labelled graphs will explicitly state these constraints.

## 9. Trials

A judgement expresses a statement defined by specification. Its form and parameters must be declared before it is used.

For example:

$$
\Gamma\vdash e:\tau
$$

it may be read as ‘in environment $\Gamma$, the expression $e$ has type $\tau$’, if the chapter of the type system defines it that way.

The symbol $\vdash$ separates the context from the statement being judged. It does not in itself imply typing: it can also be used for name resolution, static validity or other derivable relations.

The symbol:

$$
M\models P
$$

is reserved to indicate that a structure $M$ satisfies a property semantics $P$, where the corresponding chapter defines that relation of satisfaction.

Multiple contexts are separated by point and a comma:

$$
\Gamma;\Sigma\vdash e:\tau
$$

The point and comma form part of the trial’s metalanguage, not of MUD’s syntax.

## 10. Rules of inference and derivatives

A rule in inference takes the following form:

$$
\frac{
J_1
\qquad
\cdots
\qquad
J_n
}{
J
}
\;\mathsf{Nombre\text{-}De\text{-}Regla}
$$

$J_1,\ldots,J_n$ are the premises and $J$ is the conclusion. A rule without premises is an axiom:

$$
\frac{\ }{J}
\;\mathsf{Nombre\text{-}De\text{-}Axioma}
$$

Rule names are unique within specification and are written using `\mathsf`. A derivation is a finite tree whose leaves are axioms or accepted hypotheses and whose root is the proven proposition.

Conditions other than judgements are written alongside the premises and explained in prose. No necessary premise shall be implied by the example accompanying the rule.

## 11. Semantics operational

A complete evaluation can be represented by a large-step judgement:

$$
\langle X,e\rangle
\Downarrow
\langle X',r\rangle
$$

The arrow $\Downarrow$ indicates that the configuration on the left produces the complete result on the right, in accordance with the rules defining that judgement.

A basic step can be illustrated as follows:

$$
K\to K'
$$

or, where the step has a visible label:

$$
K\xrightarrow{\ell}K'
$$

The reflexive and transitive closure of transition is written as:

$$
K\to^*K'
$$

These arrows do not guarantee termination, determinism or fault-free operation. Each transition system must define its own configurations, labels and terminal states.

## 12. EBNF

The concrete grammar will use the following EBNF dialect:

| Form | Meaning |
| --- | --- |
| `"token"` | Terminal literal |
| `nombre` | Reference to a non-terminal production |
| `a, b` | Concatenation |
| `a \| b` | Alternative |
| `[ a ]` | Optional appearance |
| `{ a }` | Zero or more occurrences |
| `( a )` | Group |
| `nombre = a ;` | Definition of a production |

One or more occurrences of `a` will be written as:

```ebnf
a, { a }
```

The symbols EBNF belong to the metalanguage. When one of them is also a MUD token, it will appear in quotation marks.

The absence of ambiguity cannot be assumed simply because a EBNF has been written. The chapter for grammar must also specify precedence, associativity and any necessary contextual restrictions.

## 13. ASDL-MUD

The Surface AST is described using an explicit ASDL dialect.

| Form | Meaning |
|---|---|
| `t = C(a x) \| D` | Type sum with constructors. |
| `t = (a x, b y)` | Type product. |
| `T?` | Zero or one value. |
| `T*` | Finite ordered sequence. |
| `attributes (...)` | Attributes common to all constructors of type. |

Built-in scalars:

- `identifier`: text already validated as a lexical identifier.
- `string`: Unicode string.
- `int`: a mathematical integer that is unbounded in the schema.

MUD adds the declared type:

```asdl
flag = Disabled | Enabled
```

ASDL describes normative distinctions, not a specific memory layout. An implementation may use indices, references, interning or compact structures, provided that the observable content remains the same.

## 14. CST notation

The CST catalogue uses the following terms:

```text
SyntaxNode(kind, children, span, fullSpan)
SyntaxToken(kind, text, leadingTrivia, span, fullSpan, origin)
SyntaxTrivia(kind, text, span)
```

A category ending in `Syntax` corresponds to an production or a special recovery node. The CST retains tokens and trivia; the AST does not.

`SourceSpan` uses zero-based indexing, UTF-8 byte offsets and an exclusive trailing end. The column contains scalar Unicode values.

## 15. Absence, lack of clarity and results

The specification will always distinguish between:

- The absence of an element from a set.
- A partial function is not defined for a given input.
-  An value of domain representing absence, should MUD ever define it.
- A never-ending calculation.
- A semantic result such as $\mathsf{rejected}$ or $\mathsf{failed}$.
- An error from a particular implementation.

None of these situations will be identified as another without an explicit rule.

## 16. Terms of use

All chapter must:

1. Define your universes and metavariables before using them.
2. Specify the domain for each quantifier.
3. Distinguish between total and partial functions.
4. Define the meaning of each judgement and arrow.
5. Ensure that subscripts are used consistently.
6. Distinguish between equality, observational equivalence and identity where they do not coincide.
7. Determine whether an collection is a set, a sequence or a multiset.
8. Explain any notation overloading.

## 17. Notation to be introduced

Partial orders, fixed points, probability measures and random variables will be defined when a normative chapter first requires them. Until then, no specific notation will be assigned to them.

## Open questions

There are no outstanding issues that prevent the notation core defined in this draft from being adopted. Its adequacy should be reviewed when drafting each chapter that utilises it.

