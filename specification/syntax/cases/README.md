# CST cases → AST

`cst-ast.yaml` contains initial declarative cases. Each entry may include:

- `id` stable.
- `category`.
- `source` MUD.
- `cst_root` expected.
- `ast` in summary.
- `normalizations`.
- `expected_diagnostics`.
- `produces_ast`.

The shape `ast` is not intended to replace serialisation ASDL final version. It is a clear summary for reviewing the contract.

A future implementation may map these cases to specific snapshots. Invalid cases must retain a Lossless CST and may not produce AST in accordance with the standard.

