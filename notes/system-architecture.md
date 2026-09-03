# System architecture

Architecture must make a boundary visible: `.mud` contains semantics; everything else interprets, verifies, query or brings that about semantics.

## View by component

```text
Lenguaje natural / CLI / editor
              │
              ▼
      Operador semántico
   intención, impacto, operaciones
              │
              ▼
       Servicio de modelo
 archivos .mud + agenda + transacción
              │
              ▼
          Compilador
 scanner → CST → AST superficial
              │
              ▼
      resolución nominal
              │
              ▼
          HIR nominal
              │
              ▼
      tipado + elaboración
              │
              ▼
 representación semántica futura
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 consultas  runtime  materializadores
                   TypeScript, docs, tests
```

The regulatory chain current It runs until Surface AST and the Nominal HIR. Typing and elaboration These are later architectural phases, but the semantic representation There is as yet no regulatory framework in place for what they will produce.

## Source and derivatives

Source semantics:

- Archives `.mud`.

Metadata for governance, no semantics from the world:

- Calendar of specification.
- Record of decisions.
- Project settings.

Reconstructible derivatives already defined:

- Tokens and Lossless CST.
- AST superficial.
- Table of symbols, scopes and bindings.
- Index anchors.
- Nominal HIR and its nominal graph ownership, specialisation and reference.

Derivatives or subsequent representations not yet established by a contract full regulatory mechanism:

- Types and effective contracts resulting from classification and elaboration.
- Semantic representation after typing and elaboration.
- Subsequent semantic graphs and indices, such as readings, writings, effects or elaborate dependencies.
- Materialised code.
- Tests and documentation generated.
- Editor support that depends on later stages.

The agenda and decisions should not conceal the behaviour of the world; its function is to govern the evolution of the specification.

## Compiler

Separation current or planned:

1. **Scanner and contextual classification**: tokens, trivia, comments, verbatim quotations and context-dependent lexical classification where applicable.
2. **Parser**: Lossless CST, syntactic structure and error correction.
3. **Surface AST**: a semantically relevant form of the syntax, retaining provenance enough.
4. **Nominal resolution**: MUD paths, `using`, names, scopes, symbols, bindings and anchors.
5. **Nominal HIR**: current regulatory framework for resolution, limited to nominal information.
6. **Classification and elaboration**: types, cardinalities, domains, conversions, mutability and other contracts that require information in addition to names.
7. **Subsequent semantic analyses**: purity, effects, cycles, finiteness, stochasticity and other advanced properties.
8. **Semantic representation rear**: this may come into effect once the preceding stages have been sufficiently formalised; the specific details have not yet been finalised.
9. **Consumers**: runtime, queries, diagnostics, materialisers and editor support.

It is not advisable for the parser to directly generate a semantic representation elaborate. This separation makes it possible to track down errors, resolve names before typing, and prevent premature decisions regarding an IR from influencing aspects of the language that have not yet been formalised.

## AST superficial y HIR nominal

The Surface AST It primarily answers the question: ‘Which semantically relevant construction was written, and where does it come from?’. The Nominal HIR It asks: ‘Which symbols, scopes, owners, bindings, anchors and nominal relations result after name resolution?’.

The Nominal HIR current:

- uses symbols and clear references when the nominal resolution can determine them;
- represents scopes and owners;
- represents local bindings;
- retains public anchors where appropriate;
- can record nominal relationships `Owns`, `Specializes` y `RefersTo`;
- preserves provenance enough for diagnostics and navigation.

It does not belong to the Nominal HIR set:

- effective rates;
- effective domains;
- inferred cardinalities;
- complex conversions;
- effects or reading sets/escritura;
- post-typing semantic dependencies;
- evidence of termination.

The contract current this part of the border belongs to [[notes/decisions/ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]], which amends and clarifies [[notes/decisions/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[notes/decisions/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].

## Semantic representation rear

Classification and elaboration they will need a representation suitable for execution, analysis and materialisation. For the time being, it exists only as an architectural necessity and a set of requirements, not as a regulatory framework current.

When designing, a decision must be made, taking into account the typefaces and elaboration already developed:

- which nodes and relationships it requires;
- what information should be stored and what can be reconstructed;
- how it preserves provenance;
- what searchable projections it offers;
- whether serialisation is required and, if so, its versioning.

There is currently no `schemaVersion` regulatory framework for that representation, nor a ASDL subsequent semantic processing that consumers must carry out.

## Searchable graphs

The Nominal HIR it is now possible to reconstruct a nominal graph for navigation, ownership, specialisation and references. Richer semantic graphs may be projected from the subsequent representation where typing and elaboration sufficient.

Any graph A derivative is used for:

- impact before making a change;
- anchor navigation;
- direct and transitive dependencies within the available information;
- detection of cycles when defined by the relevant phase;
- identification of readers and writers once these works have been produced;
- explanation of a resolution.

It must not become a second source of truth. If there is a discrepancy with the normative representation of the phase that gave rise to it, it is discarded and reconstructed.

## Runtime causal

The runtime requires at least:

- shop at state with snapshots;
- pure expression evaluator;
- effect applicator and normaliser;
- link engine;
- wave planner;
- conflict and cycle detector;
- transaction with confirmation or rollback;
- register of explanation causal;
- deterministic seed manager.

The runtime must consume a representation following resolution, typed and elaboration, not to rely on the parser’s specific behaviour or use the Nominal HIR as a substitute for information semantics which it deliberately does not contain. The specific form of that representation remains deferred by D-097.

## Operador semántico

The natural language processing layer should not edit text arbitrarily. It should produce a structured plan:

```text
intención
→ clasificación
→ anclas objetivo
→ precondiciones
→ operaciones semánticas
→ impacto previsto
→ parche textual derivado
```

Minimal operations:

- `CREATE anchor`
- `UPDATE anchor`
- `RETIRE anchor`
- `MOVE anchor` or explicit migration

`READ` is an operation of query and does not produce a commit on its own. This separation between queries and versionable changes is determined by [[notes/decisions/ADR-012-cambios-semanticos-atomicos|D-012]], developed by [[notes/decisions/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]] and implemented by [[governance/POLITICA-DE-COMMITS|the policy commits]].

## Materialisers

Each materialiser receives a validated representation that is sufficient for its task, along with a technical configuration. A consumer requiring types, effects or semantics A sophisticated mind cannot obtain them by inventing them from the Nominal HIR.

It can produce:

- TypeScript code.
- API contracts.
- Fixtures and tests.
- Documentation.
- Adapters for a motor.

You cannot:

- Inferring rules from domain new.
- Convert a `failed` in `false`.
- Collapse participants and `given`.
- Change atomicity, order causal o identity.

## Early interfaces

A first executable could be a CLI with commands equivalent to:

```text
mud check
mud format
mud graph
mud explain <anchor>
mud run <action> --state <file>
mud impact <operation-plan>
```

The conversational integration and the plugin should be developed once these operations have stable contracts. This ensures that the AI utilises verifiable capabilities rather than containing semantics special.

The policy current the operator’s classification, permitted inferences and atomic flow belong to [[notes/decisions/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

## Persistence of the state runtime

The specification rules out the persistence of the semantics MUD, but a materialisation It will need to save states. A distinction must be made between:

- The model `.mud`, which states that the world possible.
- An instance of state runtime.
- The technology used to keep that instance running.

Declarative tests written in MUD conform to the language as defined by D-055 and should not be confused with tests generated by a materialiser. The technical format of additional snapshots or fixtures can be defined within the tooling without imposing a database on the language.

