# Writing readable Mud

These are authoring recommendations for examples and projects, not additional
language rules or an implemented formatter. The concrete grammar and contextual
newline contract in [chapter 08](../specification/08-concrete-grammar.md) remain
authoritative. Apply the recommendations where they improve the current unit;
do not reformat unrelated files just to make a diff uniform.

## Layout and line breaks

Use four spaces per indentation level, no tabs, and a soft target of 100 columns.
Prefer semantic groups over forced wrapping of every expression. Short numeric
coordinates and simple calls may stay compact. A blank line separates declarations
and distinct stages of an effect block; do not insert one between every assignment.

Keep the declaration name with its keyword. Break long signatures at for, on and
given, with the opening brace on the final header line. If a role list is still
long, put its roles on separate indented lines after the clause keyword.

```mud
subaction EstablishSympathyLink
for magic: Magic [mut], caster: Spellcaster [mut]
given pair: SympathyPair, aim: Aim {
    if caster.CanAttempt(Spell.Sympathy)
        and (magic, pair.leader, pair.follower).CanLink()
    then {
        ...
    }
}
```

The ellipsis is omitted content, not Mud syntax. Inside the declaration, align if,
then, after and otherwise at the same level. Put a long condition's continuation
operators at the start of the next line. A long expression block may put each
nested quantifier on its own line. Keep the order of demanded operands intact.

For a short foreach body, use a following indented line without extra braces.
Use braces when its body has multiple statements. Put a long filter on a separate
if line, keeping the colon at the end of that filter.

```mud
then foreach spell in caster.selected[ordered]
    if spell == Spell.Sympathy and caster.CanAttempt(spell) :
        (magic, caster).AttemptSympathy(aim)
```

Indentation is presentation, not a boundary rule. A newline inside open ()/[] or
an unfinished construction continues where the grammar permits it. After a
complete unit, a valid next-unit beginning takes precedence over continuation.
An explicit semicolon always separates; it cannot rescue an unfinished expression.
Do not split a token or spread a postfix name across lines.

For functional dictionaries, put each branch on its own line. A long selector
may use an expression block; put the arrow after its closing brace. Break after
an arrow before a multiline result, and retain each branch-separating comma.
A newline alone does not replace that comma.

## Constructors, collections and dictionary values

Use an unbracketed comma collection where the complete value is clearly delimited,
such as a field initialiser: kinds = Kind.Motion, Kind.SharedEffects. This notation
does not imply uniqueness or remove order/repetitions. Nested members retain their
brackets: a, [b, c], d has three outer members, including one inner collection.
Keep brackets when commas also delimit arguments, branches or associations and
could obscure which collection owns a value. Do not remove singleton brackets
mechanically. Metadata consumed by a bounded literal-only tool retains the form
that consumer supports.

Keep small, obvious positional constructors compact. For long records or several
similar arguments, prefer named construction with one component per line. Preserve
the component declaration order; do not sort arguments alphabetically or mix named
and positional arguments. Align the closing delimiter with the construction's
start. A nested record can open another indented level.

```mud
let link = SympathyLink(
    id = magic.nextLink,
    owner = caster,
    leader = endpoints.leader,
    follower = endpoints.follower,
    kinds = pair.leader.kinds & pair.follower.kinds
)
```

Use square brackets for an association list passed as one dictionary argument.
Parentheses containing comma-separated expressions are a positional structural
literal, not a substitute for those brackets. Parentheses grouping a single
expression have a different role. Passing the grammar is insufficient to prove
that a structural literal satisfies an expected dictionary contract.

```mud
SpellFeedbackProfile(
    byStage = [
        FeedbackStage.Selected -> [FeedbackAsset.SelectionFlash],
        FeedbackStage.Partial -> [FeedbackAsset.CastChime]
    ],
    excluded = [FeedbackAsset.LegacyPulse]
)
```

A singleton association may also be written directly where its context admits it;
brackets make dictionary arguments consistent when entries may be added later.
Outside argument lists, a contextual field/value initializer can retain bare
comma-separated associations. Use parentheses for actual tuple values, receiver
packs or required expression grouping. Type parentheses such as
FeedbackStage -> (FeedbackAsset [*]) are a separate grouping contract.

Do not add parentheses to every comparison. Retain them where precedence or
construction shape requires them. Use [] when actual collection nesting is
intended; do not flatten nested values to shorten a line.

Omit an empty magnitude body: write magnitude Strength: Num or magnitude
Coordinate point over Length. Retain braces for declared units or direct metadata.
Explicit empty braces remain valid under chapter 19.

## Choose a semantic unit before extracting a helper

A useful subaction performs a named domain transformation with clear participants
and required authority. It returns ActionReply, not an extra domain value. A pure
sublook computes a named projection or plan and can expose its typed result.
Do not turn each assignment into a subaction or put mutable workflows inside
aliases simply to imitate methods.

For the spell example:

- Cast selects an available implemented provider.
- AttemptSympathy owns one attempt's preparation, optional relation creation and
  completion protocol.
- PlanSympathy is a pure query classifying the target without reserving anything.
- EstablishSympathyLink revalidates admission, orients the endpoints, allocates the
  relation and records the Linked fact.

Keep internal helpers in part-only files with exact using imports. The header
part only must precede comments, defaults and using. Metadata defaults come before
using; per-owner metadata precedes ordinary body content.

Extraction changes the invocation tree. A successful child settles its owned
consequences before returning, and its contribution remains provisional relative
to the outer root. It is not merely textual substitution. Check permission flow,
input validation, guards, after, invariants at child boundaries and parent rollback.
Do not split writes across helpers if their intermediate state cannot pass the
required checks. Preserve demand order and distinguish no-op success from refusal:
replacing Cast's empty foreach with an action if would change its reply contract.

Do not claim identical causal batching after extraction. Occurrence order and
captured payload must remain correct, but separate child calls may publish separate
batches. A latest-batch field is not a history. Apply the specified checkpoint and
message contracts; do not invent the pending causal algorithm.

## Review evidence

For formatting-only edits, compare significant tokens and inspect how newline
boundaries are classified. For changed helpers, review their contracts and callers
as well as the visible body. Check argument shape and constructor component names,
not merely whether tokens can be parsed. Dictionary keys/values, tuples, collections
and multi-receiver calls can all use commas with different meanings.

The spell example's bounded planner checks its metadata/setup subset and the known
byStage tuple pitfall. It is not a general syntax or type checker. Grammar witnesses
likewise use preclassified tokens; no current gate executes these Mud sources.
Keep these limits explicit when reporting validation.
