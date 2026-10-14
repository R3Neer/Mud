---
title: Alias construction and functional-selector integration review
status: analysis
tags:
  - mud/analysis
  - mud/specification
---

# Alias construction and functional-selector integration review

## Scope and decisions

Review date: 2026-10-14. The author accepts the discussed ergonomics policies
and authorizes their integration, atomic commits and push. This assessment
records the amendment review; it defines no additional language semantics.

- D-170 requires let on immutable stored/derived alias components and retains
  mut only for mutable thing fields. Parameters, family data, metadata and
  inherited-default overrides retain their distinct syntax. File-root let/mut
  declarations remain forbidden.
- D-171 defines statically named concrete structural alias construction. Arguments
  preserve component order, named omissions require explicit effective defaults,
  and all complete component contracts remain mandatory. Representation/abstract
  aliases, things and runtime Type values do not become structural constructors.
  Resolved generic applications reuse ordinary grouped type/call syntax without
  constructor-specific generic inference. Readability suggestions are configurable
  hints, never admission conditions or warnings.
- D-172 shares direct selector-preamble locals with that branch's result, with
  definite availability, no shadowing and independent application/branch instances.
  Successful demanded derivations must reuse their normal results while inputs
  and transitive dependencies remain unchanged. Invalidation and full footprints
  preserve the ordinary derivation contract; whole-selector recovery cannot
  resurrect rolled-back locals. Nested/exact/comprehension scopes remain separate.
  AllMatches remains the default and exhaustive coverage does not imply exclusivity.

## Amendment and publication assessment

Reviewed chapters 08–11, 13, 15, 17, 20–22 and 26, their developed dependencies,
current decisions and active questions, concrete grammar/CST/Surface AST,
nominal HIR, type/effect witnesses, indexes and export profiles. Nominal review
preserves symbol identity: structural constructor calls resolve the type target;
functional results extend their own completed selector environment. No inferred
contracts or physical cache representation are inserted into nominal HIR.

Canonical prose replaces conflicting scope/marker descriptions. Construction
and reuse have explicit rules, examples and rejection/finite-witness evidence.
Opening examples in chapters 11/13 now place values in admitted look owners.
Chapter 08's representation-body description agrees with owned operators.
Traceability metadata and the generated decision index reflect all three decisions.

Current chapters remain current within their previously published scopes after
this amendment assessment. Chapters 08–10 retain their existing proposed status;
no chapter is promoted by this task. Chapter 28 remains proposed with its dynamic
publication hold. The prior [[type-system-publication-and-effects-hold-review]]
records the earlier publication checkpoint; its test counts describe that checkpoint.
Native protocols, descriptor dependencies and causal runtime proposals are not
accepted or implemented by these amendments. No new blocking question is found
within the accepted integration scope; existing delimited questions remain active.

## Validation and consistency evidence

227 tests pass: 80 syntax, 131 types, 13 effects and 3 export profiles. Grammar,
CST/AST, type/effect coverage, editorial, decision/question and temporary validators
pass. The active versioned temporary inventory is empty. Supplied finite constructor,
visibility and reuse traces verify their stated contracts; they are not a Mud
compiler, source evaluator or runtime implementation.

Each major review has a fresh Markdown inconsistency list outside the repository.
The final repository-wide iteration records an explicitly empty list after correcting
example-owner, representation-body and index integration findings. Review/helper
files are removed before task closure. The five protected causal-author files
remain byte-identical to task entry and are excluded from these commits and push.

The three semantic units are e229d28 (component markers), 9c548cf (structural
construction) and d7cc28f (shared selector locals/reuse). The following atomic
review-correction commit records this assessment, the corrected examples and
index integration. Remote publication is separately verified after that commit.
