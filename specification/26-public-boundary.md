---
title: Public action look and message contracts
tags:
  - mud/specification
status: current
normative: true
depends-on:
  - "[[05-source-text]]"
  - "[[10-names-and-anchors]]"
  - "[[11-type-system]]"
  - "[[15-fields-and-mutability]]"
  - "[[20-blocks-and-recovery]]"
  - "[[21-expressions]]"
  - "[[24-reactive-rules]]"
  - "[[28-effects]]"
questions:
  - Q-069
  - Q-070
  - Q-072
  - Q-073
  - Q-074
decisions:
  - D-169
  - D-167
  - D-168
  - D-166
  - D-165
  - D-036
  - D-042
  - D-055
  - D-061
  - D-063
  - D-087
  - D-096
  - D-109
  - D-114
  - D-115
  - D-116
  - D-118
  - D-119
  - D-121
  - D-123
  - D-127
  - D-131
  - D-132
  - D-133
  - D-134
  - D-136
  - D-137
  - D-140
---

# 26. Public boundary: action, look and message

## Operation categories

The production API is centered on operation declaration identity. Actions request
authorised changes, looks query a coherent view, and messages are causal
occurrences with frozen produced payloads. A participant is not the API owner.

```mud
action Withdraw for account: Account [mut] given amount: Money in [0..*] {
    if account.balance >= amount
    then account.balance -= amount
    after account.balance >= 0
}
look Balance for account: Account { let value := account.balance }
message Overdrawn on account: Account {
    when account.balance < 0
    let value := account.balance
}
```

These declarations belong to a part where Account.balance is accessible.
Withdraw requires authority over that participant's mutable field. Its `if`
admits the request only when the balance covers the amount; its `after` checks
the completion balance. Balance and the message field remain pure read
computations.

## Parts, file privacy and contract closure

> [!rule] MUD-PUBLIC-001 — Direct permission and whole-file privacy
> A cross-part operation reference requires direct uses authorisation and
> declaration visibility. Using imports names only. A part only file excludes
> ordinary access to all its declarations from other parts and the host, regardless of normal/sub
> category, qualification, imports or descriptor widening.

A part is assigned by the nearest ancestor mud.part. A nested manifest opens
a different part. The minimal manifest has exact uses statements; there is no
per-declaration public/private keyword or export-selection list. Permission to
operate is not transitive: A uses B, B uses C does not permit A to call C.
The type frontier needed for B's contracts may be transitively understood without
granting all operations of C. World descriptor/distribution design is a separate
chapter 06 responsibility and is not invented here.

For a visible operation o, seed its type frontier with the complete contracts
of applicable for/given/on slots, produced public fields, outputs and exposed
reflective results. Close over types required to represent and use those
contracts: aliases/components, family data, magnitude coordinates, collection
members, dictionary inputs/results, generic arguments/bounds, produced schemas
and callable input/output contracts. Use normalized finite graph references;
recursive contracts are not infinitely unfolded. A visible thing exposes
nominal identity/type, not private ordinary state merely because it is in this
frontier. Canonical inherited initialization keeps its declaring owner's rights.

> [!rule] MUD-PUBLIC-002 — No private contract leakage
> A visible signature, produced value, nested value/type component or reflective
> result must not expose a part only declaration. Type closure cannot waive
> that restriction. Ordinary value projections may use private implementation
> state while returning a valid visible contract. Every export must establish
> its complete type/value/capability privacy obligations, with only the
> established diagnostic provenance exception below.

> [!rule] MUD-PUBLIC-005 — Diagnostic provenance exception
> Established Error/Refusal origin and ArgumentRefusal argument components may expose private identity/provenance under MUD-TYPE-042 in [[11-type-system]]. They grant no invocation, state or private-schema permission. Inherited component identity defines the exception; an arbitrary field with the same name or a private Error subtype does not qualify.

Contract-visible thing/alias ancestors can be specialised with direct uses,
preserving all inherited substitutability and origin-conflict rules. Ancestry
grants no private state access or foreign activation. Cross-part reflection
requires a contract guaranteeing that every possible returned descriptor is
visible. Aggregates such as children/fields/operators are not silently filtered
to simulate privacy. Known nominal identities cannot be laundered through an
annotation erasing provenance or runtime descriptor scanning.

## Normal and sub operations

| Declaration | Authorised Mud use | Production host boundary |
| --- | --- | --- |
| action | Effect call; may start a root when authorised at the outer boundary. | Shared normal action endpoint. |
| subaction | Internal effect call; no outer root. | Unavailable. |
| look | Pure query in compatible reading contexts. | Shared normal look endpoint. |
| sublook | Pure query, including from other looks. | Unavailable. |
| message | Declarative causal source with produced occurrences. | Shared normal message observation under the publication contract. |
| submessage | Internal causal source with the same frozen-payload contract. | No external delivery. |
| test | Only the admitted test context. | No production endpoint. |

Part-only restrictions apply to every row. Normal/sub categories have separate
declaration identity. The descriptor subtype relations subaction<:action,
sublook<:look and submessage<:message do not create host capability.

> [!rule] MUD-PUBLIC-003 — Host capability is independent of widening
> An outer operation request/observation must prove a visible shared normal
> endpoint for every remaining possible static alternative. A callable widened
> to action/look/message cannot acquire endpoint permission if it may still
> denote a sub or part-only declaration. Prior narrowing can establish it.

Tests from authorised parts remain visible only in a test context, with their
separate fresh-world/initial-contribution rules. A test declaration does not
become a public world object or host operation from that visibility.

## For/given signatures and callable values

For roles have explicit names, declaration order, full type/domain/cardinality
and independent outer-place/inner-member authority. An outer-mut role requires
a writable root, not a literal, derived value or immutable capture. Inner mut
does not make a container writable, cross aliases implicitly or grant authority
over dictionary keys. Query roles cannot have outer mutation permission.

Given values are read-only with no outer/inner mut authority. Defaults are
closed pure deterministic static values, never reads of participants, earlier
arguments or world state. Positional prefixes followed by named arguments are
valid; names may omit explicit intermediate defaults, but positional omission
only a complete defaulted suffix. Unknown/repeated names or missing required
slots are static errors. Related on binding contracts for messages are
[[24-reactive-rules]], not caller-supplied receivers or message given values.

Nominal lookup retains the first nonempty level and checks each candidate
independently against actual receivers and written given names/types. Exactly
one remains before expected results can refine generic inference. Unknown
compatibility/inference is not proof of failure; defaults, runtime predicates,
body execution, import order and result types cannot break a tie. Once selected,
remaining ordinary admission checks apply to that declaration.

Actions/subactions and looks/sublooks may be generic under the bounds/finite
application closure rules; messages/submessages cannot. Generic application
creates no declaration anchor or host endpoint. Stored callable descriptors do
not prebind participants/arguments: call at the invocation site under an admitted
static signature. Read-only inputs are contravariant, outputs covariant, writable
places invariant, with separate purity/effect/capability guarantees. Named binding
requires common static slot names over every alternative; it cannot scan runtime
descriptors to reconstruct a missing contract.

## Actions and replies

> [!rule] MUD-PUBLIC-004 — Sole action result and inherited effect context
> Every action/subaction returns exactly one ActionReply, with no additional
> domain result, success payload or action-specific output type. Its if/after
> checks are pure singleton Bool and its then has only authorised effect/local
> computation. Internal calls execute at their textual position in the same
> resolution, observing preceding private effects.

For an otherwise admitted runtime request, argument-domain violation produces
ArgumentRefusal before effect execution; false if/after produces IfRefusal/
AfterRefusal. Computing faults, invalid writes and incompatible effects produce
Errors. Supported recovery is Error-only, not recovery from Refusal. A bare
effect call propagates its non-success; explicit stored ActionReply capture may
observe a failed child after its attempt rolls back. Live derived locals cannot
replay real action execution. Imagine checks root capability, returns the same
reply contract and discards its isolated changes/outputs.

An invocation's after is checked against its own consolidated completion view
before return, rather than deferred until outer completion or later rechecked.
Inner successful work remains tentative relative to its containing level.
Full causal attribution, readiness and completion remains
[[../notes/questions/Q-072-causal-work-and-reality-completion-algorithm|Q-072]].
The incorporated textual patch interface remains
[[../notes/questions/Q-073-textual-patch-contract-and-reproduction|Q-073]]; no Success
field or serialization API is selected here.

Pure recursive bodies retain their ordinary static result contract. [[types/termination-certification]] supplies their ranking search and evidence; it does not infer an ambiguous result, introduce nominal types or bypass independent owner-specific acyclicity.

### Admission and completion examples

The same optional `if` and `after` clauses belong to `subaction`:

```mud
subaction Debit for account: Account [mut] given amount: Money in [0..*] {
    if account.balance >= amount
    then account.balance -= amount
    after account.balance >= 0
}
```

In isolation, with no further causal effects on the balance, an initial balance
of 10 and amount 4 passes the guard and the postcondition checks the completion
balance of 6. For amount 12, the guard
produces IfRefusal before the subtraction. A bare `account.Debit(12)` propagates
that refusal; it is not a conditional no-op. Use selection or a filtered
`foreach` when absence of matching work should complete normally.

An action `after` is a contract check, not an additional effect or a repair.
For example, changing this postcondition to `after account.balance >= 5` makes
the admitted request with initial balance 10 and amount 6 end in AfterRefusal;
the failed invocation's tentative subtraction is rolled back. An error while
computing either Boolean condition follows the Error channel instead.

An `after` belongs to one invocation's completion. An `always` rule constrains
every applicable consolidated root/wave checkpoint under [[25-always-rules]].
A test's `after` asserts the expected test outcome under
[[08-concrete-grammar#Local values in conditions]]; it does not add a postcondition to the action
being tested. Invocation completion retains the boundary and open algorithmic
scope described above.

## Looks and produced types

A look/sublook has for/given signatures and pure public-field value bodies.
All fields observe one coherent caller view: confirmed stable state from the
host, a rule snapshot, or the private delta at a then call's position. Failed
field computation enters ordinary query/block error handling, not a partially
returned object. Invalid host argument domains are query errors; within a
resolution an invalidating query produces the ordinary error channel.

One producer declaration and exact static generic argument tuple determines
one produced nominal result type. A call returns exactly one value of that type;
multiplicity belongs in its fields. Different producers remain distinct with
identical schemas. Runtime receiver identity or changing values do not create
new types. A produced type receives no public anchor merely by existing.
Its static Type descriptor can be obtained through ~type and explicitly named
by an ordinary alias; a call expression itself is not a type position.

Dynamic callable results retain all checked producer alternatives. Use a unique
most specific common covering contract when established; otherwise retain their
normalized union, including with incomparable minima. No result-order priority,
intersection type or implicit nominal conversion repairs ambiguity. Public
field shapes, numeric presentation and privacy are checked on every alternative.

## Messages and frozen occurrences

A message/submessage has automatic on, required when, optional pure if and pure
public fields. It is not called or emitted by a new source instruction. Its
trigger categories/flow are the reactive interface; no given or generic payload
constructor is introduced. On participant bindings remain separate from payload.

For one matched occurrence, evaluate and validate the fields once in its causal
birth view and freeze one immutable value of the declaration's produced payload
type. Payload failures enter the enclosing error channel; no partial occurrence
is published. Canonical declaration/participant descriptors, occurrence identity
and immutable payload remain distinct. Equal-valued payloads do not deduplicate
distinct occurrences. Later participant inactivity/rematerialisation or state
changes do not reproject the historical payload or grant a host writable handle.

Shared normal messages pass the existing consolidated root/wave checkpoint
barrier before provisional publication. Private prefixes, failed checkpoints,
submessages, part-only messages, tests and imagine do not externally publish.
Internal consumers see causal occurrences through the next-wave interface,
independently of physical delivery order. Publication is not world confirmation;
host looks still read confirmed state.

Ticket is host-only Waiting/Kept/Dropped observation, not a Mud source type,
keyword, writable participant or new nominal anchor. Relative child success
does not establish Kept; successful stable-root incorporation does, while scope
disposal establishes Dropped. This accepted lifetime requirement is an interface,
not a transport implementation. Generalized host observations/exterior results
remain [[../notes/questions/Q-074-generalised-host-ticket-and-exterior-intentions|Q-074]].
Native hosting/ABI/configuration and value/lifetime conversion remain
[[../notes/questions/Q-069-foreign-adapter-contract-and-hosting|Q-069]] and
[[../notes/questions/Q-070-foreign-value-conversion-lifetime-and-errors|Q-070]].

## Diagnostics, certification and evidence

Reject uses missing for a fully qualified call, hidden part-only exposure,
unsafe reflective aggregates, private ordinary field reads, sub endpoints after
widening, extra action returns, unbound/ambiguous slots, effectful looks/payloads,
stochastic conditions and unguaranteed causal payload access. A public view may
return a Money computed from private fields while keeping those fields private.
Such projection does not grant a host state mutation handle.

Dynamic-call impact follows [[types/contextual-call-analysis]]; body termination follows [[types/termination-certification]]. Signatures
and summaries cannot invent those certificates or a causal algorithm.
[[types/typing-cases.yaml]], callable/produced-type certificates, part grammar/
nominal coverage and [[effects/README]] supply scoped static and reviewed boundary
evidence. No compiler, adapter, scheduler, host transport or patch protocol is
implemented by this chapter.
