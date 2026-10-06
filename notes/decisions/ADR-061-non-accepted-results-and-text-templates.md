---
id: D-061
title: "Non-accepted results and `Text` templates"
status: current
date: 2026-07-29
supersedes: []
superseded-by: []
questions:
  - "Q-007"
  - "Q-055"
  - "Q-059"
affects:
  - "action results, `always` rules, lexicon, grammar, `Text` evaluation, diagnostics and the external boundary"
---
# ADR-061 — Non-accepted results and `Text` templates

- Amended by: [[ADR-118-action-replies-refusals-and-errors|D-118]].

- Amended by: [[ADR-085-functional-dictionaries-metadata-and-structured-activation|D-085]]
- Amends: [[notes/decisions/ADR-027-departures-from-the-model-by-means-of-look-and-message|D-027]], [[notes/decisions/ADR-029-intervals-effective-limits-and-cycles-of-point|D-029]], [[notes/decisions/ADR-030-explicit-quantitative-conversion-using-to|D-030]], [[notes/decisions/ADR-035-organisation-names-using-and-anchors|D-035]], [[notes/decisions/ADR-038-close-knit-families-with-strong-values|D-038]], [[notes/decisions/ADR-041-contracts-under-the-three-types-of-rules|D-041]], [[notes/decisions/ADR-042-shares-root-and-results|D-042]], [[notes/decisions/ADR-048-reproducible-randomness-and-errors|D-048]], [[notes/decisions/ADR-049-operators-precedence-and-standardised-intervals|D-049]], [[notes/decisions/ADR-050-comments-terminators-text-and-numeric-separators|D-050]], [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]] and [[notes/decisions/ADR-056-char-text-and-unicode-ordering|D-056]]
- Amended by: [[notes/decisions/ADR-068-universal-thing-and-intrinsic-name|D-068]]
- Subsequently amended by: [[ADR-079-external-diagnostics-for-always-rules|D-079]]
- Further amended by: [[notes/decisions/ADR-083-unitless-base-quantities|D-083]]
- Related to: [[notes/decisions/ADR-055-declarative-and-diagnostic-tests-otherwise|D-055]]
- Related questions: Q-007, [[notes/questions/Q-055-l-point-magnitude-literals|Q-055]], Q-059
- Affected documents: action results, `always` rules, lexicon, grammar, `Text` evaluation, diagnostics and the external boundary

## Context

An action's public result already distinguishes `Success`, `Refusal` and `Errors`, but non-accepted states did not yet carry a uniform explanation. `always` rules could cause a failure without declaring the invariant's own diagnostic.

At the same time, `Text` literals need to incorporate values without resorting to manual concatenation or confusing a declaration with the value produced by an expression.

## Decision

### Structured action replies and block recovery

ActionReply is an ordinary immutable value with alternatives Success, Refusal and the nonempty nominal collection alias Errors. Refusal and Error require reason and Declaration origin; errors can wrap an optional cause. ConditionRefusal carries the actual final Boolean evaluation tree. No external state/reason envelope replaces that value contract.

False if, after and always checks produce their respective refusal subtype. Computing a condition can instead yield Error values. Otherwise attaches to the protected block and handles only errors, with optional conjunctive on bindings and if, then or raise exclusively. Plain Text diagnostics for false checks are invalid and absence of such a diagnostic produces no warning. Test assertion falsity retains the separate test executor failure category, not a captured Error.

Static diagnostics and executor defects retain their own categories. Q-007 delimits the exhaustive error catalogue and resource/defect boundary. Q-059 retains complete test observation/aggregation semantics.

### `Text` templates

Ordinary and multiline `Text` literals are templates. Within them:

- `{e}` evaluates the MUD expression `e` and inserts the textual representation of its value;
- `{e}` may also interpolate `e~anchor` when the static category of `e` exposes that property;
- `\{` and `\}` insert literal braces;
- an unescaped brace that does not form a valid hole is an error;
- `\u{...}` remains an indivisible Unicode escape and does not open a hole.

`anchor` is contextual only within a template and does not become a generally reserved word. Outside a template it may remain an ordinary identifier.

The scanner uses a mode stack: the contents of `{...}` return to ordinary expression lexing and their delimiters balance normally. A `Text` literal nested within that expression opens its own template mode. A line break or end of file can implicitly close ordinary text only when no hole remains open.

### Renderable values

The representation of a hole depends on the evaluated value, not the written name:

| Value | Representation |
| --- | --- |
| `Text` | Its characters, without quotes |
| `Char` | Its contained scalar |
| `Bool` | `true` or `false` |
| Basic number | Its canonical numeric representation or the explicit format |
| `thing` | The value of its intrinsic `name` property |
| `family` member | The member's nominal name |
| Interval | Its normalised canonical form |
| Collection | Its elements separated by `, `, without outer brackets |
| Linear magnitude | Its number and the canonical projection of its units; if that is empty, the number alone |
| Point magnitude | Its `format`, when present; otherwise the ordinary representation of its coordinate as a magnitude |

If a collection element is itself a collection, the inner collection retains its brackets. The rule applies recursively:

```mud
"{[1, 2, 3]}"          # 1, 2, 3
"{[[1, 2], [3, 4]]}"   # [1, 2], [3, 4]
```

An empty collection contributes empty text. `ordered`, `unique`, `mut` and cardinality belong to the collection type or shape and are not printed. An ordered collection uses its order; an unordered collection uses its canonical enumeration.

A Boolean rule call is renderable because it produces `Bool`. A bare descriptor is distinct from its invocation result. Reactive rules, always rules, message declarations and tests are not ordinary interpolable results; action/look calls must also satisfy the interpolation context and a defined value-formatting contract. Types, families as declarations and every other category without a decided representation produce a static error in `{...}`.

The representation of a magnitude writes the unit abbreviation where one exists. Otherwise it uses the singular name for `1` and `-1`, and the declared plural for every other value; if no plural exists, it reuses the name. Derived units use the canonical projection of their factors with units. Nominal factors without units remain in the type but produce no text; if the complete projection is empty, only the number is written. A point magnitude without `format` is no exception: it represents its coordinate under these same rules.

An explicit display selects the unit:

```mud
"Distance: {distance in kilometer}"
"Time coordinate: {time in hour}"
```

For a point magnitude, `in` transforms the complete coordinate and omits its `format`: 13:30 expressed `in hour` produces `13.5 h`, not component `13`.

### Components of a point magnitude

The expression:

```mud
picosecond from second in time
```

extracts from point `time` the `picosecond` component contained in the corresponding `second`. Its general form is `extracted-unit from containing-unit in point`. It is a single syntactic construction, not the composition of three independent operators.

The receiver must be a point magnitude. Both units must belong to its underlying magnitude, and the extracted unit cannot be larger than the containing one. The result is `Nat`, is calculated from the canonical origin by Euclidean remainder, and does not depend on the units written in `format`. Picoseconds can therefore be extracted from a time whose format displays only hours, minutes and seconds.

When the relation does not contain an integral number of smaller units, the final component may be partial. In a regular calendar of 360 days, `week from year in date` produces indices from `0` to `51`; the last denotes the final partial week.

The following must not be confused:

```mud
time in picosecond                 # total coordinate in picoseconds
picosecond from second in time     # part within the second
```

Within a point magnitude's `~format`, the point itself is contextual. The usual succession retains the compact form:

```mud
~format = "{hour:2}:{minute:2}:{second:2}"
```

The first name expresses the coordinate in that unit — reduced by the cycle where applicable — and each later name expresses its component within the preceding one. When the container is not obvious or does not match that succession, it may be written explicitly:

```mud
~format = "{week from year:2}"
```

The incomplete form `week from year` is valid only in a point magnitude's `~format` hole; elsewhere it requires the `in point` receiver.

### Numeric format

A numeric hole permits:

```text
{e:left}
{e::right}
{e:left:right}
```

`left` and `right` are decimal natural integers:

- `left` sets the minimum number of digits to the left of the point and pads with zeroes; the sign does not count, and digits are never removed if the value exceeds the minimum;
- `right` sets exactly the digits to the right of the point, adding zeroes or rounding to nearest with ties to even in accordance with D-034;
- when `right` is zero, no decimal point is written.

Left precision is permitted for every basic numeric type. Right precision is permitted only for types that can show a fractional part: `Num`, `Rum` and `Money`. Formatting changes exclusively the produced `Text`, never the value or its type.

```mud
count: Nat = 12
ratio: Num = 12.3

"{count:4}"     # 0012
"{ratio::2}"    # 12.30
"{ratio:4:2}"   # 0012.30
```

Applying a numeric format to another type or writing an incomplete specification is a static error.

The `~format` metadata of a `point over` magnitude uses this same syntax, not a second brace language. Its names such as `hour`, `minute` and `second` resolve in the contextual point; `{hour:2}` requests two positions to the left.

### Units in `look` and `message`

A public field whose value is a magnitude may select its display with `in`:

```mud
speed := vehicle.speed in km/h
time := clock.time in second
```

Omitting it is legal, but produces a warning where a unit can be selected because it makes a public boundary depend on its canonical projection. The suggested fix explicitly adds that unit. A magnitude without units publishes its number and produces no warning. For a point magnitude, a direct field without `in` publishes the numeric coordinate, not `~format`; to publish the formatted representation, declare a `Text` field, for example `timeText := "{clock.time}"`.

The rule applies to public fields whose direct value is a magnitude. Recursive serialisation of magnitudes contained in aliases or collections remains in Q-051.

### Anchors within templates

There is no special `anchor{...}` interpolation. D-087 makes `~anchor` an ordinary, typed reflective property, so it is interpolated through the general expression syntax:

```mud
"Rule: {CanRecruit~anchor}"
"Kingdom: {kingdom}; identity: {kingdom~anchor}"
```

The access is valid only when the receiver's static category exposes `~anchor`. A template introduces no special `anchor` token.

## Consequences

- The AST distinguishes literal fragments, value holes and numeric specifications; anchors use ordinary expression interpolation.
- The IR retains the expression, format and provenance of every fragment.
- The lexer requires nested modes for text and code.
- `otherwise` is optional and localised; its absence produces the relevant style diagnostic.
- The result catalogue must provide a human-readable reason for every `Refusal` and `Errors`.
- Contextual rendering introduces no general implicit conversion to `Text`.
- The `~name` display may differ from `~anchor`; they are separate reflective properties.
- `in` serves both linear and point magnitudes and, for the latter, bypasses the format.
- Component extraction is not limited by the visible format.

## Verification

1. External `Refusal` and `Errors` results with mandatory `reason`, and absence of that field in `Success`.
2. A warning for an `always` rule without `otherwise`, a suggestion in `if` and `after`, and rejection of a diagnostic that is not `Text`.
3. Lazy evaluation of the diagnostic over the infringing tentative state.
4. Ordinary and multiline interpolation with nested expressions.
5. The escapes `\{`, `\}`, `\"`, `\'` and `\u{...}`.
6. Rendering of `thing`, `family` members, Boolean rules, intervals and nested collections.
7. Rejection of declarations and valueless constructs within `{...}`.
8. Formats `{n:4}`, `{n::2}` and `{n:4:2}`, including zero, sign, padding, excess digits and ties-to-even rounding.
9. Obtaining anchors by ordinary interpolation of `expression~anchor`.
10. Rejection of `~anchor` where the receiver's static category does not expose that property.
11. Root, alternative and formatted rendering of linear and point magnitudes.
12. Extraction `picosecond from second in time` independently of `format`.
13. A warning for a public magnitude with a selectable unit but no explicit display, no warning where no units exist, and formatted publication through `Text`.
