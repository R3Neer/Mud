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

La cadena normativa vigente llega hoy hasta el AST superficial y el HIR nominal. Tipado y elaboración son fases arquitectónicas posteriores, pero la representación semántica que producirán todavía no tiene esquema normativo fijado.

## Fuente y derivados

Fuente semántica:

- Archivos `.mud`.

Metadatos de gobierno, no semántica del mundo:

- Agenda de especificación.
- Registro de decisiones.
- Configuración del proyecto.

Derivados reconstruibles ya delimitados:

- Tokens y CST sin pérdidas.
- AST superficial.
- Tabla de símbolos, scopes y bindings.
- Índice de anclas.
- HIR nominal y su grafo nominal de propiedad, especialización y referencia.

Derivados o representaciones posteriores todavía no fijados por un contrato mecánico normativo completo:

- Tipos y contratos efectivos resultantes de tipado y elaboración.
- Representación semántica posterior a tipado y elaboración.
- Grafos e índices semánticos posteriores, como lecturas, escrituras, efectos o dependencias elaboradas.
- Código materializado.
- Tests y documentación generados.
- Soporte de editor que dependa de fases posteriores.

La agenda y las decisiones no deberían esconder comportamiento del mundo; su función es gobernar la evolución de la especificación.

## Compilador

Separación vigente o prevista:

1. **Scanner y clasificación contextual**: tokens, trivia, comentarios, literales y clasificación léxica dependiente de contexto cuando corresponda.
2. **Parser**: CST sin pérdidas, estructura sintáctica y recuperación de errores.
3. **AST superficial**: forma semánticamente relevante de la sintaxis, conservando procedencia suficiente.
4. **Resolución nominal**: paths de MUD, `using`, nombres, scopes, símbolos, bindings y anclas.
5. **HIR nominal**: salida normativa actual de resolución, limitada a información nominal.
6. **Tipado y elaboración**: tipos, cardinalidades, dominios, conversiones, mutabilidad y demás contratos que requieran información posterior a nombres.
7. **Análisis semánticos posteriores**: pureza, efectos, ciclos, finitud, estocasticidad y otras propiedades elaboradas.
8. **Representación semántica posterior**: podrá existir cuando las fases anteriores estén suficientemente formalizadas; su esquema concreto no está fijado hoy.
9. **Consumidores**: runtime, consultas, diagnósticos, materializadores y soporte de editor.

No conviene que el parser produzca directamente una representación semántica elaborada. La separación permite conservar localización de errores, resolver nombres antes de tipar y evitar que decisiones prematuras sobre un IR condicionen superficies del lenguaje todavía no formalizadas.

## AST superficial y HIR nominal

El AST superficial responde principalmente «¿qué construcción semánticamente relevante se escribió y de dónde procede?». El HIR nominal responde «¿qué símbolos, ámbitos, propietarios, bindings, anclas y relaciones nominales resultan después de resolver nombres?».

El HIR nominal vigente:

- usa símbolos y referencias resueltas cuando la resolución nominal puede determinarlas;
- representa scopes y propietarios;
- representa bindings locales;
- conserva anclas públicas cuando corresponden;
- puede registrar relaciones nominales `Owns`, `Specializes` y `RefersTo`;
- conserva procedencia suficiente para diagnósticos y navegación.

No pertenece al HIR nominal fijar:

- tipos efectivos;
- dominios efectivos;
- cardinalidades inferidas;
- conversiones elaboradas;
- efectos ni conjuntos de lectura/escritura;
- dependencias semánticas posteriores a tipado;
- pruebas o evidencia de terminación.

El contrato vigente de esta frontera pertenece a [[notas/decisiones/ADR-097-hir-nominal-vigente-e-ir-semantico-diferido|D-097]], que modifica y precisa [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]] y [[notas/decisiones/ADR-093-ast-superficial-unico-e-ir-semantico-elaborado|D-093]].

## Representación semántica posterior

Tipado y elaboración necesitarán una representación apta para ejecución, análisis y materialización. Por ahora solo existe como necesidad arquitectónica y conjunto de requisitos, no como un esquema normativo vigente.

Cuando se diseñe deberá decidirse, a la luz de las superficies de tipos y elaboración ya desarrolladas:

- qué nodos y relaciones necesita;
- qué información debe almacenarse y qué puede reconstruirse;
- cómo conserva procedencia;
- qué proyecciones consultables ofrece;
- si necesita serialización y, en tal caso, su versionado.

No existe hoy un `schemaVersion` normativo de esa representación ni un ASDL semántico posterior que los consumidores deban implementar.

## Grafos consultables

El HIR nominal ya permite reconstruir un grafo nominal para navegación, propiedad, especialización y referencias. Grafos semánticos más ricos podrán proyectarse de la representación posterior cuando existan tipado y elaboración suficientes.

Cualquier grafo derivado sirve para:

- impacto antes de cambiar;
- navegación por anclas;
- dependencias directas y transitivas dentro de la información disponible;
- detección de ciclos cuando la fase correspondiente los defina;
- identificación de lectores y escritores cuando esos efectos hayan sido elaborados;
- explicación de una resolución.

No debe convertirse en una segunda fuente de verdad. Si hay discrepancia con la representación normativa de la fase que lo origina, se descarta y reconstruye.

## Runtime causal

El runtime necesita al menos:

- store de estado con snapshots;
- evaluador puro de expresiones;
- aplicador y normalizador de efectos;
- motor de vinculaciones;
- planificador de ondas;
- detector de conflictos y ciclos;
- transacción con confirmación o rollback;
- registro de explicación causal;
- gestor determinista de semillas.

El runtime debe consumir una representación posterior a resolución, tipado y elaboración, no depender de peculiaridades del parser ni usar el HIR nominal como sustituto de información semántica que este deliberadamente no contiene. La forma concreta de esa representación permanece diferida por D-097.

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

`READ` es una operación de consulta y no produce commit por sí sola. Esta separación entre consultas y cambios versionables está fijada por [[notas/decisiones/ADR-012-cambios-semanticos-atomicos|D-012]], desarrollada por [[notas/decisiones/ADR-053-operador-semantico-y-flujo-de-autoria|D-053]] y aplicada por [[gobierno/POLITICA-DE-COMMITS|la política de commits]].

## Materializadores

Cada materializador recibe una representación validada suficiente para su tarea y una configuración técnica. Un consumidor que necesite tipos, efectos o semántica elaborada no puede obtenerlos inventándolos a partir del HIR nominal.

Puede producir:

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
