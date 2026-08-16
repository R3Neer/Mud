# Modelos sintácticos de MUD

Este directorio contiene los artefactos normativos y verificables que conectan la gramática concreta con el AST superficial.

## Archivos

| Archivo | Estado | Función |
|---|---|---|
| `cst-sin-perdidas.md` | Normativo | Modelo de CST, trivia, spans y recuperación. |
| `mud-syntax-kinds.yaml` | Normativo mecánico | Inventario de producciones, tokens, trivia y categorías CST. |
| `mud-surface-ast.asdl` | Normativo mecánico | Esquema del AST superficial normalizado. |
| `mud-resolved-ast.asdl` | Normativo mecánico | Contrato del AST semántico resuelto previo al IR: símbolos y anclas ya resueltos, tipos elaborados y dependencias semánticas. |
| `cst-a-ast-superficial.md` | Normativo | Transformación y normalizaciones. |
| `cobertura-sintactica.yaml` | Normativo mecánico | Mapeo exhaustivo EBNF → CST → AST. |
| `validate_syntax_model.py` | Herramienta editorial | Detecta divergencias entre los artefactos anteriores. |
| `casos/cst-ast.yaml` | Suite inicial | Casos de transformación y rechazo previo al AST. |

## Orden de autoridad

Los archivos se complementan; no se usa una regla general de «el último gana».

1. `mud-lexico.ebnf` y `06-lexico.md` determinan el reconocimiento léxico.
2. `mud.ebnf` y `07-gramatica-concreta.md` determinan la agrupación concreta.
3. `cst-sin-perdidas.md` determina conservación, trivia y recuperación.
4. `mud-surface-ast.asdl` determina los constructores abstractos.
5. `cst-a-ast-superficial.md` determina la proyección.
6. Los YAML hacen inventariable y comprobable la correspondencia.

Una contradicción es un defecto de la propuesta y debe resolverse en todos los archivos afectados.

## Flujo

```text
archivo .mud
→ scanner completo
→ tokens significativos + trivia
→ CST sin pérdidas
→ validación sintáctica contextual
→ AST superficial normalizado
→ resolución nominal (símbolos + grafo parcial)
→ tipado, elaboración y análisis estático
→ AST semántico resuelto
→ IR
```

## Generación de código

`mud-surface-ast.asdl` puede alimentar generadores de:

- Clases o structs.
- Visitantes.
- Serializadores.
- Comparadores estructurales.
- Builders validados.

`mud-syntax-kinds.yaml` puede alimentar:

- Enumeraciones de `SyntaxKind`.
- Wrappers tipados de nodos CST.
- Tests de cobertura del parser.
- Documentación de producciones.

La generación no debe convertir los archivos mecánicos en derivados sin autoridad. Los archivos generados se guardarán fuera de `especificacion/` o se marcarán expresamente como tales.

## Validación

Dependencia del validador:

```powershell
python -m pip install -r especificacion/sintaxis/requirements.txt
```

Desde la raíz del repositorio:

```bash
python especificacion/sintaxis/validate_syntax_model.py
```

El comando comprueba:

- Cobertura de todas las producciones sintácticas.
- Inventario de todas las producciones léxicas.
- Ausencia de entradas huérfanas.
- Correspondencia entre categorías CST y cobertura.
- Existencia de destinos ASDL declarados.
- Presencia de contratos básicos del esquema.

No comprueba todavía:

- Ambigüedad LL/LR.
- Semántica estática.
- Corrección de ejemplos MUD mediante un parser real.
- Propiedades dinámicas.

## Política de cambios

Un cambio de gramática debe actualizar, en el mismo commit:

1. La EBNF afectada.
2. El catálogo CST.
3. La cobertura.
4. La transformación cuando cambie la normalización.
5. El ASDL cuando aparezca o desaparezca una distinción abstracta.
6. Los casos de prueba relevantes.

Un cambio interno que no altere comportamiento observable puede modificar una implementación sin cambiar estos archivos.

## Convenciones de nombre

- Producción EBNF: `kebab-case`.
- Categoría CST: `PascalCaseSyntax`.
- Tipo ASDL: `snake_case`.
- Constructor ASDL: `PascalCase`.
- Campo ASDL: `snake_case`.
- Flag conceptual: `Disabled | Enabled`.

## Límites

Este directorio no define:

- Resolución de nombres y anclas.
- Subtipado.
- Inferencia de tipos.
- Evaluación estática.
- Semántica de efectos.
- Ondas causales.
- Forma canónica del IR.

Las referencias a esas fases sirven únicamente para impedir que el AST superficial las anticipe.
