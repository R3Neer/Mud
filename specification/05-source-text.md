---
title: Source text and physical structure
aliases:
  - MUD Archives
tags:
  - mud/specification
  - mud/fuente
status: proposed
normative: true
depends-on:
  - "[[01-scope-and-conformance]]"
questions:
decisions:
  - D-132
  - D-131
  - D-035
  - D-050
  - D-057
  - D-061
  - D-065
  - D-069
  - D-070
  - D-078
  - D-085
  - D-086
  - D-087
  - D-096
  - D-116
---

# 05. Source text and physical structure

## State and purpose

This chapter defines the physical unit received by a MUD processor. The identity semantics of the statements is defined in [[09-names-and-anchors]]; the lexical structure belongs to [[06-lexicon]].

## Files

> [!rule] MUD-LEX-001 — Encoding
> A MUD file must be encoded in UTF-8. It may begin with a single BOM `U+FEFF`; that character must not appear as a BOM anywhere else in the file.

> [!rule] MUD-LEX-002 — Extension
> A standard source file must use the `.mud` extension.

> [!rule] MUD-LEX-003 — Jumps
> The processor must recognise `LF` and `CRLF`. It must also accept `CR` on its own as a jump and normalise all three forms to a single token `NEWLINE`.

## Derived namespace

The path MUD for a file is derived from the relative path from the root MUD:

```text
world/kingdoms.mud
```

belongs to MUD’s path:

```text
world
```

The file name is not part of path. A file located directly within root belongs to path root.

> [!rule] MUD-NAME-001 — Path safe
> Every file must remain within the root MUD after resolving path components. Directory names that form MUD paths must be valid `lowerCamelCase` identifiers.

## Contents

A file contains, in this order:

1. An optional `part only` header.
2. Zero or more stored defaults and metadata constants `~...` applicable to the file.
3. Zero or more statements `using`.
4. Zero or more top-level declarations of any category, including `start with` of part.

The physical order of files is not semantic. Nor does it resolve duplicates or ambiguities.

```mud
using world.people
using physics.*

thing Kingdom {
    mut title: Text = ""
}

action Retitle for kingdom: Kingdom [mut]
given newTitle: Text {
    then kingdom.title = newTitle
}
```

> [!rule] MUD-SYN-001 — Top separation
> Two top-level elements must be separated by at least one terminator. Comments and spaces alone do not serve as that terminator.

> [!rule] MUD-SYN-002 — Header `using`
> Every declaration `using` must appear before any top-level declaration in the same file. A subsequent `using` is invalid and never introduces a local scope.

## Identity from the source and provenance

Each file is assigned an `SourceId` derived from its normalised relative path. The `SourceId` identifies the unit of provenance during a build; it is not an anchor semantics and may change when the file is moved.

Syntactic positions use:

```text
SourcePosition(byteOffset, line, column)
SourceSpan(sourceId, start, end)
```

- Zero-based indices.
- Offsets in UTF-8 bytes.
-  Exclusive ending.
- Columns in Unicode scalar values.

The conversion to UTF-16 positions falls within the LSP boundary.

## Syntactic roots

Each source file produces an independent MudFileSyntax CST and a validated MudFile. Each mud.part manifest produces PartFileSyntax and MudPartFile. Filename-selected input wrappers retain those separate categories. MudProject aggregates both collections; it is not written in one physical file.

For structural serialisation, `MudProject` files are sorted by normalised relative path. This ordering does not alter the semantics.

## Physical metadata retained

The CST or its metadata retain:

- Existence of the initial BOM.
- Path standardised relative.
- Derived namespace.
- The format of each jump, as specified by the text of its tokens or trivia.

The Surface AST retains only the metadata required for provenance and tooling; it does not use the BOM or the jump style to denote the programme’s meaning.

## End of file

The end-of-file character can act as a terminator for a line-ending comment or an ordinary literal `Text` without a closing quotation mark. It cannot implicitly terminate:

- Round brackets or square brackets.
- Blocks in curly brackets.
- Interpolations of a template `Text`.
- Multi-line literals or comments.
- Contextual literals `Char` using the same double quotation marks as `Text`.


## Recommended editorial structure

> [!note] MUD-SRC-001 — Cohesion of domain
> Files should group concepts, places, processes or situations from world rather than syntactic categories. This recommendation does not affect paths, resolution, anchors or conformance; a cross-cutting relation may occupy its own file when it better represents the domain.

For example:

```text
forest/
├── wolves.mud
└── weather.mud

village/
├── market.mud
└── guards.mud
```

An `battle.mud` file may contain `thing`, aliases, dictionaries, rules, actions, `look` and `message` which, taken together, describe a battle. Separating them solely because they belong to different syntactic categories makes it difficult to read the world as a conceptual unit.

## Parts

A part is an encapsulation unit within a Mud world project. Each `.mud` belongs to the part of its nearest ancestor `mud.part`; no such ancestor is a static error. A nested manifest opens a new part. The part path is derived from its directory relative to the world root, without a repeated name declaration.

A `mud.part` is a minimal manifest: only whitespace, comments and zero or more `uses exact.part.path` statements. Empty manifests are valid. Statements use ordinary newline or `;` separation. Paths are exact MudPaths from the world root and must identify directories containing a `mud.part`. Relative paths, wildcard paths, grouped lists, metadata, source declarations and backend settings are invalid. A repeated `uses` is redundant and produces a warning.

```mud
uses world.people
uses world.weather; uses world.time
```

`uses` authorises direct access to another part's visible contract; it does not import short names. `using` imports names inside an `.mud` and does not grant permission. Operational access is not transitive: if A uses B and B uses C, A cannot call C without its own uses C. The transitive type closure needed to represent B's visible contract remains available, without exporting all of C's operations. Fully qualified references obey the same checks.

The optional header `part only` applies to its entire `.mud` file. It must be the first content after an optional BOM and whitespace; comments, metadata, `using` and declarations cannot precede it. It is followed by ordinary statement separation. Declarations remain available throughout their owning part but cannot cross to another part or the host. The header does not affect other files or nested parts, and is not accepted in `mud.part`. No declaration-level visibility modifiers or export-selection list exist.

```mud
part only
using world.people

sublook Detail { score := 0 }
```

Normal `action`, `look` and `message` form host operations. Their sub forms `subaction`, `sublook` and `submessage` are visible to authorised Mud parts by default but are not direct host endpoints. A subaction has no outer-root capability; sublook is a pure query with no action-only calling restriction; submessage supplies internal causal occurrences without host delivery. A `part only` file restricts normal and sub forms alike. Tests retain test-context visibility.

A visible signature, produced value, nested alias/type component or reflective result cannot expose a `part only` declaration. Contract closure cannot lift this restriction. A visible ordinary value projection may be computed using private implementation state without exposing its private type. Ordinary thing fields remain private; imports, specialisation and descriptor widening grant no additional authority.

Contract-visible thing and alias types may be specialised under direct uses authorisation and public type closure. Inherited initialisation keeps the declaring owner's rights. Part dependency cycles are valid with a cyclic-coupling warning; they imply no startup order and do not permit cycles of domain evaluation. Part start contributions are materialised jointly.
