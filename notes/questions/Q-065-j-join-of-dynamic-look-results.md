---
id: Q-065
title: Join of dynamic `look` results
priority: P1
opened: 2026-08-28
resolved: false
closed:
decisions:
  - D-096
affects:
  - look, callables, typing
superseded-by: []
---

# Q-065 — Join of dynamic `look` results

## Content

Define only the case where a dynamic `look` invocation has several incomparable common minima. D-096 already fixes use of the most specific common type when it is unique, and explicit preservation of alternatives through a union when no common supertype is more informative than that union; this question does not reopen those rules.
