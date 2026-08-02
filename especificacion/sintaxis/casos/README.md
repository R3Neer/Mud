# Casos CST → AST

`cst-ast.yaml` contiene casos declarativos iniciales. Cada entrada puede incluir:

- `id` estable.
- `category`.
- `source` MUD.
- `cst_root` esperado.
- `ast` resumido.
- `normalizations`.
- `expected_diagnostics`.
- `produces_ast`.

La forma `ast` no pretende sustituir a una serialización ASDL definitiva. Es un resumen legible para revisar el contrato.

Una implementación futura puede convertir estos casos a snapshots concretos. Los casos inválidos deben conservar una CST sin pérdidas y pueden no producir AST normativo.
