---
title: Standard library capability planning
status: analysis
tags:
  - mud/analysis
  - mud/libraries
---

# Standard library capability planning

## Accepted direction

[[decisions/ADR-138-standard-library-scope-and-world-descriptor|D-138]] plans an included base and installable official extensions. Reduce repetitive code, make everyday programmes possible in Mud and cover general-purpose capabilities otherwise requiring direct foreign fragments. Start with breadth of contracts and examples; implementation follows the formalisation gate, not a competing early compiler milestone.

## Candidate themes — not selected parts or APIs

| Theme | Candidate capabilities |
| --- | --- |
| Collections and algorithms | Transform, group, partition, search, combine, accumulate; stacks, queues and priority queues using existing collection contracts. |
| Text | Unicode scalar/grapheme operations, search, substitution, split/join, formatting, parsing and regular expressions. |
| Mathematics and statistics | Exact calculation, explicit approximation, intervals, magnitudes and descriptive statistics. |
| Randomness and probability | Reproducible sampling, distributions, weighted choices and shuffling; separate cryptographic randomness. |
| Time and calendars | Durations, civil dates, time zones, clocks and temporal scheduling; distinguish model time and exterior time. |
| Bytes and encoding | Binary values, buffers, text encodings, hexadecimal and Base64. |
| Formats and archives | Typed JSON/CSV/configuration conversion, compression and archive operations. |
| Input/output | Console, paths, files, directories and incremental reading/writing. |
| System and processes | Arguments, environment, configuration and process coordination. |
| Networks and services | URLs, HTTP, connections, WebSockets and service hosting. |
| Persistence | Databases, parameterised queries, transactions and world-state storage. |
| Asynchronous work | Pending exterior operations, cancellation, channels and data flows; source syntax is unselected. |
| Security | Digests, signatures, encryption, credentials and secure randomness through maintained implementations. |
| Graphs and modelling | Traversal, connectivity, paths and dependency algorithms over relations. |
| Diagnostics and tests | Error presentation, traces, measurement and generated/property-based test data. |

These themes are proposals, not a commitment to include every capability in the base. Existing language primitives must not acquire duplicate semantics through wrappers. Exact Num, Rum, units, nominal identity, cardinalities and capabilities survive library boundaries. Collection callbacks require the existing static callable/cycle contracts.

## Candidate cases and dependencies

Design examples for grouping collections, transforming text, exact statistics, parsing configuration, reading a file and querying/writing a database. Record inputs, results, errors, effects and concise Mud usage before choosing concrete names or signatures.

SQL could expose a named dialect, parameterised Mud inputs and typed results. A dialect alone does not select a database connection. Transactions need a contract relating preparation, Mud confirmation and exterior execution; rollback in a database does not establish atomic confirmation across both systems. SQLite-first and PostgreSQL-next remain recommendations, not chosen implementation order.

Rust-backed base libraries without mandatory Python/.NET installation are a recommendation. Scientific Python, .NET/Unity, graphics and media are candidate extensions. Concrete adapter and conversion protocols remain [[questions/Q-069-foreign-adapter-contract-and-hosting|Q-069]] and [[questions/Q-070-foreign-value-conversion-lifetime-and-errors|Q-070]]. Related work includes dynamic-callable analysis Q-023, technical failures Q-007, Rum portability Q-058, randomness Q-032 and calendars Q-033.

## Next work

Settle dependency boundaries and formalise causal execution before asynchronous I/O APIs. Inventory candidate contracts broadly; do not implement libraries or invent unresolved scheduling through native wrappers. Patch reproduction and recording require their own specified guarantees.
