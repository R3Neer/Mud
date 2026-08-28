---
title: Convenciones editoriales de la especificación MUD
aliases:
  - Convenciones editoriales
tags:
  - mud/especificacion
  - mud/normativa
status: propuesta
normative: true
depends-on: []
questions: []
decisions:
  - D-070
  - D-097
---

# Convenciones editoriales de la especificación MUD

> [!note]
> Este documento regula cómo se redacta la especificación. No define el comportamiento de los programas MUD.

Proceso de publicación: [[gobierno/CICLO-DOCUMENTAL|Ciclo documental de MUD]].

## 1. Dialecto Markdown

La documentación usará Markdown compatible con Obsidian y, cuando sea posible, legible en renderizadores Markdown comunes.

Se permiten:

- Propiedades YAML.
- `[[wikilinks]]`.
- Enlaces Markdown ordinarios cuando deban funcionar fuera del vault.
- Callouts de Obsidian.
- Fórmulas LaTeX con `$...$` y `$$...$$`.
- Bloques de código con lenguaje indicado.
- Referencias a encabezados y bloques cuando sean estables.

Se evitarán plugins de Obsidian necesarios para comprender el contenido normativo.

## 2. Propiedades mínimas

Cada capítulo usará:

```yaml
---
title:
aliases: []
tags:
  - mud/especificacion
status: borrador
normative: true
depends-on: []
questions: []
decisions: []
---
```

Estados:

- `esqueleto`
- `borrador`
- `propuesta`
- `en-revision`
- `vigente`
- `sustituido`

`normative: true` clasifica el archivo dentro de la superficie normativa, pero no adelanta su estado de publicación. Solo `status: vigente` concede autoridad consolidada al capítulo como unidad. Antes de ese estado, el texto puede incorporar contratos ya cerrados por decisiones vigentes y artefactos mecánicos coherentes, pero no puede modificar esos contratos ni resolver por sí solo una cuestión abierta.

Si un capítulo no vigente contradice una decisión vigente, la contradicción es un defecto editorial que debe corregirse antes de promover el capítulo. No se interpreta como una sustitución tácita de la decisión. La relación entre prosa y artefactos mecánicos normativos sigue regida por MUD-EDIT-001: una divergencia entre ambos es un defecto, no una regla de prioridad silenciosa.

## 3. Enlaces y trazabilidad

Los enlaces internos usarán preferentemente wikilinks:

```markdown
[[03-notacion|notación matemática]]
[[29-ondas#Configuración de una onda]]
```

Cada capítulo debe enlazar:

- Sus dependencias normativas.
- Los términos definidos en otro capítulo.
- Las preguntas activas que delimiten una incertidumbre relevante para su contenido.

Las decisiones que sustentan el capítulo se registran en el frontmatter `decisions:`. No se duplicará una definición para evitar un enlace.

### 3.1. Estado vigente e historia

> [!rule] MUD-EDIT-002 — Especificación como estado vigente
> El cuerpo de todo documento normativo de `especificacion/` debe describir únicamente el estado actual de MUD dentro de su alcance. No debe conservar como parte de la exposición normativa la historia de introducción, modificación, sustitución o retirada de una regla.

La historia y la procedencia pertenecen a los ADR, las preguntas históricas, Git y los metadatos de trazabilidad. En consecuencia:

- El cuerpo normativo no usa identificadores `D-NNN` o `ADR-NNN` para justificar, fechar, introducir, actualizar o sustituir reglas. La relación con decisiones se conserva en `decisions:`.
- No se crean secciones cuya función sea corregir aditivamente el contenido anterior, como «Actualización por D-NNN», «Revisión por D-NNN», «Tokens retirados» o equivalentes. La regla vigente se integra en su ubicación canónica y la formulación anterior se elimina.
- Una prohibición o ausencia que forme parte del lenguaje actual puede expresarse directamente, por ejemplo «X es inválido» o «X no forma parte de esta gramática». No se conserva la narración histórica «X se eliminó» salvo que el hecho histórico sea el objeto explícito de un documento no normativo.
- La misma regla se aplica a los comentarios explicativos de EBNF, ASDL, YAML y demás artefactos normativos mecánicos dentro de `especificacion/`.

Las preguntas activas son una excepción deliberada a la ausencia de identificadores históricos en el cuerpo. Un documento puede citar una `Q-NNN` cuando sea necesario indicar con precisión qué parte de su estado actual permanece sin decidir. Esa referencia:

1. debe corresponder a una pregunta activa;
2. debe figurar también en el frontmatter `questions:` del documento cuando este disponga de frontmatter;
3. debe describir la incertidumbre presente, no la historia de las decisiones que la produjeron;
4. debe retirarse del cuerpo y del frontmatter cuando la pregunta deje de estar activa.

### 3.2. Integración de decisiones en superficies desarrolladas

> [!rule] MUD-EDIT-003 — Integración por superficie desarrollada
> Una decisión vigente debe quedar integrada en toda superficie normativa ya desarrollada cuya responsabilidad declarada cubra la regla afectada. Si la ubicación canónica todavía no existe como superficie desarrollada, la ausencia de ese futuro capítulo no constituye por sí sola un defecto de integración.

A estos efectos, una superficie está desarrollada cuando existe un documento o artefacto normativo que ya asume responsabilidad sustantiva sobre esa materia. Una mera entrada `Archivo previsto` no obliga a crear anticipadamente el capítulo ni a alojar su semántica en otro capítulo impropio.

Mientras la superficie canónica no exista:

- el ADR vigente puede conservar autoridad transitoria sobre esa parte;
- ninguna superficie normativa existente puede contradecir la decisión;
- los índices, mapas y descripciones de capítulos futuros deben ser compatibles con el estado ya decidido y no pueden conservar semántica sustituida;
- no se considera integrada globalmente una regla solo porque figure en un ADR, pero tampoco se considera defectuosa por no aparecer en un capítulo que aún no existe.

La integración se evalúa por superficie afectada. Cuando una superficie ya desarrollada contiene la materia, debe reescribirse para expresar literalmente el estado vigente y no basta con añadir una nota correctiva al final.

## 4. Callouts

Uso previsto:

> [!definition]
> Definición normativa.

> [!rule]
> Regla normativa.

> [!example]
> Ejemplo informativo.

> [!failure]
> Contraejemplo o programa inválido.

> [!warning]
> Interacción peligrosa o limitación.

> [!question]
> Cuestión abierta.

> [!proof]
> Demostración.

> [!intuition]
> Explicación no normativa.

El texto del callout debe indicar explícitamente si el renderer no reconoce el tipo personalizado.

## 5. Identificadores normativos

Las reglas que afecten a conformidad tendrán identificador:

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

Un identificador retirado no se reutiliza con otro significado.

## 6. Bloques normativos

Formato recomendado:

> [!rule] MUD-ACTION-001 — Participantes de una acción
> Una acción debe declarar sus participantes mediante `for`. Una acción no puede declarar participantes mediante `on`.

Después pueden aparecer:

- Justificación informativa.
- Ejemplo válido.
- Contraejemplo.
- Diagnóstico relacionado.
- Consecuencias para AST o IR.

## 7. Definiciones matemáticas

Toda metavariable se introduce antes de usarse. Por ejemplo:

> Sea $\mathcal A$ el conjunto de anclas y sea $W$ un estado de mundo bien formado.

Convenciones:

- Letras caligráficas para universos o conjuntos destacados: $\mathcal A$, $\mathcal T$.
- Mayúsculas latinas para estados, conjuntos o estructuras: $W$, $R$, $G$.
- Minúsculas para elementos: $a$, $v$, $e$.
- Letras griegas para entornos y tipos cuando sea convencional: $\Gamma$, $\rho$, $\tau$.
- Negrita o sans serif para nombres de categorías formales cuando ayude: $\mathsf{accepted}$.

Las convenciones definitivas pertenecerán a [[03-notacion]].

## 8. Reglas de inferencia

Cada regla tendrá:

- Nombre único.
- Premisas.
- Conclusión.
- Explicación en prosa.
- Ejemplo de aplicación cuando no sea inmediata.

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

Los nombres de reglas usarán `\mathsf{...}`. No se empleará `\textsc`, aunque exista en LaTeX completo, porque no está soportado de forma uniforme por MathJax en Obsidian.

## 9. Ejemplos

Los ejemplos se clasifican:

- `minimal`: aísla una regla.
- `representative`: muestra uso realista.
- `boundary`: cubre un límite.
- `invalid`: debe rechazarse.
- `interaction`: combina características.

Un ejemplo informativo nunca puede ser la única definición de una regla.

## 10. Cuestiones abiertas

El ciclo de vida, los estados y el archivo estable de cada pregunta se rigen por [[gobierno/POLITICA-DE-PREGUNTAS|Política de preguntas de MUD]].

Formato:

> [!question] Q-NNN — Título
> Pregunta precisa, alternativas conocidas y capítulos afectados.

Mientras una pregunta afecte al significado de una construcción, el capítulo no puede pasar a `vigente`.

El frontmatter `questions` enumera solo preguntas en estado `abierta` o `parcialmente-decidida`. Una pregunta cerrada se retira de la lista sin borrar su archivo histórico. Las referencias corporales a preguntas activas siguen además MUD-EDIT-002.

## 11. Teoremas y demostraciones

Se distinguirán:

- **Proposición**: resultado local.
- **Lema**: resultado usado para demostrar otro.
- **Teorema**: garantía principal.
- **Corolario**: consecuencia directa.
- **Conjetura**: afirmación todavía no demostrada.
- **Contraejemplo**: caso que refuta una afirmación.

Una propiedad no demostrada no se llamará teorema.

## 12. Artefactos normativos mecánicos

Además de Markdown, la especificación puede contener EBNF, ASDL, YAML y scripts de validación. Cada archivo debe declarar su función en el README del subdirectorio correspondiente.

> [!rule] MUD-EDIT-001 — Autoridad complementaria
> Un artefacto mecánico normativo y la prosa que lo explica son complementarios. Una contradicción entre ambos es un defecto; no se resuelve suponiendo que uno tenga prioridad silenciosa.

Convenciones:

- EBNF: producciones `kebab-case`.
- CST: categorías `PascalCaseSyntax`.
- ASDL: tipos `snake_case`, constructores `PascalCase`, campos `snake_case`.
- YAML: claves estables y orden legible; no se depende del orden de mapas para el significado.
- Python editorial: debe fallar con código distinto de cero ante divergencias.

## 13. Archivos escritos y generados

Todo archivo generado debe indicarlo en su cabecera y declarar su fuente. Los esquemas normativos de `especificacion/` se escriben o revisan deliberadamente; el código generado a partir de ellos no adquiere autoridad sobre su fuente.

Un cambio de gramática que afecte a la estructura debe actualizar en el mismo commit el catálogo CST, la cobertura, la transformación y el ASDL correspondientes.

> [!rule] MUD-EDIT-004 — Propagación de resolución nominal
> Todo cambio que introduzca, elimine o modifique nombres, ámbitos, propietarios, bindings, categorías nominales, anclas, visibilidad nominal, cualificación o especialización debe revisar en el mismo cambio `09-nombres-y-anclas.md` y `nombres/mud-nominal-hir.asdl`. Si afecta a su contrato, ambas superficies y sus validadores deben actualizarse atómicamente.

La revisión debe comprobar al menos qué símbolos se crean, en qué scope viven, qué nombre los resuelve, qué propietario tienen, si reciben ancla pública y qué relaciones `Owns`, `Specializes` o `RefersTo` produce la resolución. Una regla dependiente de tipos, efectos o elaboración no se añade al HIR nominal para satisfacer artificialmente esta obligación.

## 14. Enlaces a archivos mecánicos

Los capítulos enlazarán por nombre de archivo a los esquemas mecánicos. Los README de `gramatica/` y `sintaxis/` mantienen el inventario y los comandos de validación. No se copiarán tablas extensas generadas dentro de varios capítulos cuando puedan verificarse desde una única fuente.

## 15. Plantilla de capítulo

```markdown
---
title:
aliases: []
tags:
  - mud/especificacion
status: esqueleto
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

Las secciones inaplicables pueden omitirse.
