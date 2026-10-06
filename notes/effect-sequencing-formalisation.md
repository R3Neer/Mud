---
title: Effect sequencing formalisation analysis
tags:
  - mud/notes
status: analysis
---

# Effect sequencing formalisation analysis

## Accepted sequential contract

The author confirms that x = 5 followed by x *= 2; x += 3 produces 13. Textual sequencing applies inside a private branch, including operand evaluation and internal calls. Concurrent arithmetic normalisation must not reorder that private sequence.

## Accepted composition

For independent branches, project each normalised surviving relative contribution onto its semantic destination. Stages are positions in this destination's sequence, not positions of unrelated instructions or physical scheduler steps. Combine contributions in stage k, then advance to k+1. Within one stage use the accepted arithmetic normal form ((base + delta) * P) / Q. Shorter branches contribute no later operation. An absolute replacement clears preceding contributions of its own branch and supplies the common replacement base; equal replacements merge and unequal replacements conflict.

Contrasting proposal: A *= 2; += 3 and B *= 3; += 4 from 5 yield 37: product 6 in stage one, sum 7 in stage two. A *= 2; += 3 alone yields 13. A += 2 and B *= 3 still give 21, retaining the earlier concurrent normal form. Unrelated destinations must not shift stages. All RHS values are evaluated on their branch's private view, not reevaluated on consolidated stage states.

The author accepts the staged rule and rejects treating these mixed branches as intrinsically incompatible. [[decisions/ADR-128-sequential-effects-and-staged-consolidation|D-128]] records the choice. Assignable paths, lifecycle, collection semantics and recovery require their own normal forms; the stage proposal does not impose a universal order on all effects.

## Formalisation work

The effect judgment must carry common entry view, sequential private projection, local environment, causal owner, generation-bound semantic intents, causal outputs and an outcome channel. Each surviving Surface AST effect constructor needs a rule and contrasting evidence. Root/wave consolidation must evaluate siblings against one common view, normalise surviving intents, rebuild immutable ancestors once, validate completed cardinalities/domains and checkpoints, then expose a tentative next view. It must not publish confirmed state or outputs independently of outer completion.

Expression evaluation, invocation completion and native operations are contract interfaces to their own chapters; an effects chapter is not a parser, foreign ABI or scheduler implementation. Error taxonomy, oscillation detection, circular domains and adapter hosting retain their separately active questions.
