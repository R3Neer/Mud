---
title: Editorial conventions for the specification MUD
aliases:
  - Publishing conventions
tags:
  - mud/specification
  - mud/normativa
status: proposed
normative: true
depends-on: []
questions: []
decisions:
  - D-070
  - D-097
---

#  Editorial conventions for the specification MUD

> [!note]
> This document sets out the rules for drafting the specification. It does not define the behaviour of MUD programmes.

Publication process: [[governance/CICLO-DOCUMENTAL|Document lifecycle by MUD]].

## 1. Markdown dialect

The documentation will use Markdown that is compatible with Obsidian and, where possible, readable in common Markdown renderers.

The following are permitted:

- YAML properties.
- `[[wikilinks]]`.
- Standard Markdown links where they need to work outside the vault.
- Obsidian callouts.
- LaTeX equations using `$...$` and `$$...$$`.
- Code snippets with the language specified.
- References to headings and blocks once they are finalised.

Obsidian plugins required to understand regulatory content will be avoided.

## 2. Minimum properties

Each chapter will use:

```yaml
---
title:
aliases: []
tags:
  - mud/specification
status: draft
normative: true
depends-on: []
questions: []
decisions: []
---
```

States:

- `esqueleto`
- `borrador`
- `propuesta`
- `en-revision`
- `vigente`
- `sustituido`

`normative: true` classifies the file within normative surface, but does not advance its publication status. Only `status: vigente` grants established authority to chapter as unit. Prior to that state, the text may incorporate contracts already concluded by existing decisions and coherent mechanical artefacts, but it may not modify those contracts or resolve a open question on its own.

If an chapter that is not an current contradicts an current decision, the contradiction is an editorial error that must be corrected before the chapter is promoted. It is not interpreted as a tacit replacement of decision. The relation between prose and normative mechanical artefacts remains governed by MUD-EDIT-001: a divergence between the two is a defect, not an unstated rule of priority.

## 3. Links and traceability

Internal links should preferably use wikilinks:

```markdown
[[03-notation|notación matemática]]
[[29-ondas#Configuración de una onda]]
```

Each chapter must link to:

- Its regulatory bodies.
- Terms defined elsewhere chapter.
- Active questions that define a uncertainty relevant to their content.

The decisions underpinning chapter are recorded in the frontmatter `decisions:`. A definition will not be duplicated in order to avoid a link.

### 3.1. State current and history

> [!rule] MUD-EDIT-002 — Specification as state current
> The body of every normative document of `specification/` must describe only the current state of the MUD within its scope. It must not include, as part of the regulatory text, the history of a rule’s introduction, amendment, replacement or withdrawal.

The history and provenance relate to ADRs, historical queries, Git and the metadata for traceability. In consequence:

- The regulatory body does not use identifiers `D-NNN` or `ADR-NNN` to justify, date, introduce, update or replace rules. The relation containing decisions is retained in `decisions:`.
- Do not create sections intended to additively amend the preceding content, such as ‘Update by D-NNN’, ‘Review by D-NNN’, ‘Tokens removed’ or equivalent. Rule current is incorporated into its canonical location and the previous wording is deleted.
- A prohibition or omission that forms part of the current language may be expressed directly, for example ‘X is invalid’ or ‘X is not part of this grammar’. The historical narrative ‘X was removed’ is not retained unless the historical fact is the explicit subject of a non-normative document.
- The same rule applies to explanatory comments in EBNF, ASDL, YAML and other mechanical specification artefacts within `specification/`.

Active questions are a deliberate exception to the absence of historical identifiers in the main body. A document may cite an `Q-NNN` where it is necessary to indicate precisely which part of its current state remains undecided. That reference:

1.  must correspond to an active question;
2.  must also appear in the frontmatter `questions:` of the document where the document has frontmatter;
3. should describe the current uncertainty, not the history of the decisions that led to it;
4.  must be removed from the body and the front matter once the question is no longer active.

### 3.2. Integration of decisions on developed surfaces

> [!rule] MUD-EDIT-003 — Integration over the surface area
> An current decision must be integrated into any normative surface that has already been developed and whose stated responsibility covers the rule in question. If the canonical location does not yet exist as a developed surface, the absence of that future chapter does not in itself constitute a defect in integration.

For these purposes, an area is considered to have been developed when there is a regulatory document or instrument that already assumes substantive responsibility for that matter. A mere entry `Archivo previsto` does not require the chapter to be created in advance, nor does it require its semantics to be hosted on another chapter that is unsuitable.

As long as the canonical surface does not exist:

-  the ADR current may retain interim authority on that part;
-  no existing normative surface may contradict the decision;
- the indexes, maps and descriptions of future chapters must be compatible with the state already decided upon and must not retain the semantics that has been replaced;
-  A rule is not considered to be fully integrated simply because it appears in an ADR, but nor is it considered flawed because it does not appear in a chapter that does not yet exist.

Integration is assessed on the basis of the area affected. Where an already developed area contains the material, it must be rewritten to state state current verbatim; it is not sufficient simply to add a corrective note at the end.

## 4. Callouts

Intended use:

> [!definition]
>  Regulatory definition.

> [!rule]
> Regulatory rule.

> [!example]
> Informative example.

> [!failure]
> Counterexample or invalid programme.

> [!warning]
> Hazardous interaction or restriction.

> [!question]
> Cuestión abierta.

> [!proof]
> Demonstration.

> [!intuition]
> Explanation non-normative.

The callout text must explicitly state whether the renderer does not recognise the custom type.

## 5. Regulatory identifiers

Rules affecting conformance will have the identifier:

```text
MUD-LEX-001
MUD-SYN-001
MUD-NAME-001
MUD-TYPE-001
MUD-DOM-001
MUD-RULE-001
MUD-ACTION-001
MUD-EFFECT-001
MUD-WAVE-001
MUD-RANDOM-001
MUD-REACH-001
MUD-TEST-001
MUD-CONF-001
```

A retired identifier is not reused with a different meaning.

## 6. Regulatory blocks

Recommended format:

> [!rule] MUD-ACTION-001 — Participants in a action
>  An action must declare its participants using `for`. An action cannot declare participants via `on`.

The following may then occur:

- Justification for information purposes.
- Valid example.
- Counterexample.
- Diagnostic related.
- Implications for AST or IR.

## 7. Mathematical definitions

Every metavariable must be defined before it is used. For example:

> Let $\mathcal A$ be the set of anchors and let $W$ be a well-formed state of world.

Conventions:

- Calligraphic lettering for highlighted universes or sets: $\mathcal A$, $\mathcal T$.
- Latin capital letters for states, groups or structures: $W$, $R$, $G$.
- Lower-case designations for elements: $a$, $v$, $e$.
- Greek characters for environments and typefaces where conventional: $\Gamma$, $\rho$, $\tau$.
- Bold or sans serif for formal category names where appropriate: $\mathsf{accepted}$.

The final conventions will belong to [[03-notation]].

## 8. Rules of inference

Each rule will have:

-  Unique name.
- Premises.
- Conclusion.
- Explanation in prose.
- Example of use when the application is not immediate.

```laTeX
$$
\frac{
  \Gamma \vdash e_1 : \mathsf{Nat}
  \qquad
  \Gamma \vdash e_2 : \mathsf{Nat}
}{
  \Gamma \vdash e_1 + e_2 : \mathsf{Nat}
}
\;\mathsf{T\text{-}Add\text{-}Nat}
$$
```

Rule names will use `\mathsf{...}`. `\textsc` will not be used, even though it exists in full LaTeX, because it is not consistently supported by MathJax in Obsidian.

## 9. Examples

The examples are categorised as follows:

- `minimal`: isolates a ruler.
- `representative`: demonstrates realistic use.
- `boundary`: covers a boundary.
- `invalid`: this should be rejected.
- `interaction`: combines features.

An illustrative example can never be the sole definition of a rule.

## 10. Unresolved issues

The cycle lifecycle, statuses and stable archive for each question are governed by the [[governance/POLITICA-DE-PREGUNTAS|Policy for MUD questions ]].

Format:

> [!question] Q-NNN — Title
> Specific question, known alternatives and relevant sections.

As long as a question affects the meaning of a construction, chapter cannot proceed to `vigente`.

The frontmatter `questions` lists only questions in state, `abierta` or `parcialmente-decidida`. A closed question is removed from the list without deleting its history. In-text references to active questions also follow MUD-EDIT-002.

## 11. Theorems and proofs

The following shall be distinguished:

- **Proposition**: result local.
- **Lemma**: result used to prove another.
- **Theorem**: principal guarantee.
- **Corollary**: consequence direct.
- **Conjecture**: a statement that has not yet been proven.
- **Counterexample**: a case that refutes a claim.

A property that has not been proved shall not be called a theorem.

## 12. Mechanical rule-based artefacts

As well as Markdown, the specification may contain EBNF, ASDL, YAML and validation scripts. Each file must declare its purpose in the README file within the relevant subdirectory.

> [!rule] MUD-EDIT-001 — Authority (supplementary)
> A normative mechanical artefact and the prose explaining it are complementary. A contradiction between the two is a flaw; it is not resolved by assuming that one takes silent precedence.

Conventions:

- EBNF: productions `kebab-case`.
- CST: categories `PascalCaseSyntax`.
- ASDL: types `snake_case`, constructors `PascalCase`, fields `snake_case`.
- YAML: stable keys and human-readable order; meaning does not depend on the order of maps.
- Python editor: should return a non-zero error in the event of discrepancies.

## 13. Written and generated files

Every file generated must state this in its header and declare its source. The `specification/` specification schemas are written or reviewed deliberately; the code generated from them does not acquire authority regarding its source.

Any grammatical change that affects the structure must update the corresponding CST catalogue, coverage, transformation and ASDL in the same commit.

> [!rule] MUD-EDIT-004 — Propagation of nominal resolution
> Any change that introduces, removes or modifies names, scopes, owners, bindings, nominal categories, anchors, visibility nominal, qualification or specialisation must be reviewed in the same change `09-names-and-anchors.md` and `nombres/mud-nominal-hir.asdl`. If it affects its contract, both surfaces and their validators must be updated atomically.

review must at least check which symbols are created, in which scope they reside, which name resolves to them, what owner they have, whether they receive public anchor, and which relationships `Owns`, `Specializes` or `RefersTo` the resolution produces. A rule dependent on types, effects or elaboration is not added to the Nominal HIR in order to artificially satisfy this requirement.

## 14. Links to mechanical files

The chapters will link to the mechanical diagrams by filename. The README files for `gramatica/` and `sintaxis/` contain the inventory and commands from validation. Extensive tables generated within various chapters will not be duplicated where they can be verified from a single source.

## 15. Template from chapter

```markdown
---
title:
aliases: []
tags:
  - mud/specification
status: skeleton
normative: true
depends-on: []
questions: []
decisions: []
---

# NN. Título

## Estado y propósito

## Dependencias

## Terminología

## Definiciones

## Sintaxis concreta

## Sintaxis abstracta

## Reglas estáticas

## Semántica

## Propiedades

## Ejemplos

## Contraejemplos

## Diagnósticos

## Cuestiones abiertas
```

Sections that do not apply may be omitted.

