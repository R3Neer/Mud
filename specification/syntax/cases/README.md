# CST cases → AST

`newline-cases.json` provides reviewed source fragments for MUD-SYN-015. Each certificate supplies prefix completeness, next-unit-start and continuation premises; `test_newline_contract.py` checks the finite boundary decision, then uses the existing EBNF recogniser on separately preclassified token fixtures. Source grouping, premise correctness and exact CST byte ownership remain review obligations. This is not an implemented scanner or parser.

`cst-ast.yaml` contains initial declarative cases. Each entry may include:

- `id` stable.
- `category`.
- `source` MUD.
- `cst_root` expected.
- `ast` in summary.
- `normalizations`.
- `expected_diagnostics`.
- `diagnostic_phase`, when a diagnostic belongs to native parsing, nominal resolution, typing, capabilities, adapter effects or runtime validation.
- `required_contract`, for adapter assumptions or semantic execution outcomes a future implementation must verify.
- `produces_ast`.

The shape `ast` is not intended to replace serialisation ASDL final version. It is a clear summary for reviewing the contract.

A future implementation may map these cases to specific snapshots. Cases invalid at the syntactic boundary retain a lossless CST and produce no valid AST. Cases with later nominal, type, capability or effect diagnostics may produce a valid Surface AST; `produces_ast` records that distinction. A runtime failure is an execution outcome, not automatically a syntax error.

Foreign cases are declarative conformance requirements. Mechanical catalogue and ASDL checks do not execute native parsers, adapters or a runtime and do not establish that those implementations exist.


Reviewed projection cases include alias operator operands/result annotations, retained nested collection layers and executable raise with producing-block recovery. These cases describe CST-to-AST obligations; no source parser or projection implementation is claimed.
