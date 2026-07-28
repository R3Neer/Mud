# Arquitectura del sistema

La arquitectura debe hacer visible una frontera: `.mud` contiene semántica; todo lo demás interpreta, verifica, consulta o materializa esa semántica.

## Vista por componentes

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
 lexer → parser → AST → símbolos → tipos
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
 grafo     IR canónico diagnósticos
      │       │
      │       ├──────────────┐
      ▼       ▼              ▼
 consultas  runtime      materializadores
                         TypeScript, docs, tests
```

## Fuente y derivados

Fuente semántica:

- Archivos `.mud`.

Metadatos de gobierno, no semántica del mundo:

- Agenda de especificación.
- Registro de decisiones.
- Configuración del proyecto.

Derivados reconstruibles:

- Tokens, CST o AST.
- Tabla de símbolos.
- Índice de anclas.
- Grafo semántico.
- IR.
- Índices de lectura, escritura, dominios y aleatoriedad.
- Código materializado.
- Tests y documentación generados.
- Soporte de editor.

La agenda y las decisiones no deberían esconder comportamiento del mundo; su función es gobernar la evolución de la especificación.

## Compilador

Separación recomendada:

1. **Lexer**: tokens, comentarios, literales y terminadores.
2. **Parser**: estructura sintáctica y recuperación de errores.
3. **AST de superficie**: conserva procedencia y forma escrita.
4. **Resolución**: namespaces, declaraciones `using`, nombres y anclas.
5. **Tipado**: tipos, cardinalidades, dominios, conversiones y mutabilidad.
6. **Análisis semántico**: pureza, efectos, ciclos, finitud y estocasticidad.
7. **IR canónico**: representación independiente de la sintaxis.
8. **Emisores**: grafo, diagnósticos, formateo y materializaciones.

No conviene hacer que el parser produzca directamente el IR. La separación permite conservar localización de errores y evolucionar la sintaxis sin deformar el modelo semántico.

## AST e IR

El AST responde “¿qué se escribió y dónde?”. El IR responde “¿qué significa después de resolverlo?”.

El IR debe:

- Usar anclas, no nombres ambiguos.
- Distinguir explícitamente las tres clases de reglas.
- Distinguir `TestDecl`, sus activaciones locales, efectos, aserciones y diagnósticos.
- Conservar participantes y `given` como grupos separados.
- Conservar por cada rol `for` su cardinalidad, modificadores, capacidades exterior e interior y, cuando proceda, el lugar receptor.
- Normalizar tipos, dominios y cardinalidades.
- Registrar lecturas, escrituras y llamadas.
- Mantener procedencia hacia archivo y rango del AST.
- Ser versionado mediante un `schemaVersion`.

El JSON de la especificación es un ejemplo, no todavía un contrato completo.

El contrato conceptual actualizado del AST, IR y grafo pertenece a [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]]. El pipeline y las obligaciones de materializadores, conformidad y soporte de editor pertenecen a [[notas/decisiones/ADR-052-pipeline-materializadores-y-conformidad|D-052]].

## Grafo semántico

El grafo es una proyección consultable del IR. Sirve para:

- Impacto antes de cambiar.
- Navegación por anclas.
- Dependencias directas y transitivas.
- Detección de ciclos.
- Identificación de lectores y escritores.
- Explicación de una resolución.

No debe convertirse en una segunda fuente de verdad. Si hay discrepancia, se descarta y reconstruye.

## Runtime causal

El runtime necesita al menos:

- Store de estado con snapshots.
- Evaluador puro de expresiones.
- Aplicador y normalizador de efectos.
- Motor de vinculaciones.
- Planificador de ondas.
- Detector de conflictos y ciclos.
- Transacción con confirmación o rollback.
- Registro de explicación causal.
- Gestor determinista de semillas.

El runtime debe consumir IR canónico, no depender de peculiaridades del parser.

## Operador semántico

La capa que atiende lenguaje natural no debería editar texto de forma libre. Debería producir un plan estructurado:

```text
intención
→ clasificación
→ anclas objetivo
→ precondiciones
→ operaciones semánticas
→ impacto previsto
→ parche textual derivado
```

Operaciones mínimas:

- `CREATE anchor`
- `UPDATE anchor`
- `RETIRE anchor`
- `MOVE anchor` o migración explícita

`READ` es una operación de consulta y no debería producir commit por sí sola. Esta distinción está pendiente de confirmación porque el texto inicial mezcla clasificación CRUD con cambios versionables.

## Materializadores

Cada materializador recibe IR validado y una configuración técnica. Puede producir:

- Código TypeScript.
- Contratos de API.
- Fixtures y tests.
- Documentación.
- Adaptadores para un motor.

No puede:

- Inferir reglas de dominio nuevas.
- Convertir un `failed` en `false`.
- Colapsar participantes y `given`.
- Cambiar atomicidad, orden causal o identidad.

## Interfaces tempranas

Un primer ejecutable puede ser una CLI con comandos equivalentes a:

```text
mud check
mud format
mud graph
mud explain <anchor>
mud run <action> --state <file>
mud impact <operation-plan>
```

La integración conversacional y el plugin deberían construirse después de que estas operaciones tengan contratos estables. Así la IA utiliza capacidades comprobables en vez de contener semántica especial.

La política vigente de clasificación, inferencias permitidas y flujo atómico del operador pertenece a [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]].

## Persistencia del estado runtime

La especificación excluye persistencia de la semántica MUD, pero una materialización necesitará guardar estados. Debe distinguirse:

- El modelo `.mud`, que declara el mundo posible.
- Una instancia de estado runtime.
- La tecnología usada para persistir esa instancia.

Los tests declarativos escritos en MUD pertenecen al lenguaje conforme a D-055 y no deben confundirse con tests generados por un materializador. El formato técnico de snapshots o fixtures adicionales puede definirse dentro del tooling sin imponer una base de datos al lenguaje.
