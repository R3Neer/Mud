---
title: Inventario de saneamiento de la especificación
tags:
  - mud/notas
  - mud/especificacion
  - mud/saneamiento
status: activo
---

# Inventario de saneamiento de la especificación

Este documento es un checklist de trabajo no normativo. Resume los defectos y obligaciones todavía relevantes detectados durante la auditoría de `especificacion/` posterior a la integración de módulos, callables, `look`, `message` y activación modular.

No define MUD. La autoridad normativa permanece en `especificacion/` y, transitoriamente cuando la superficie canónica todavía no existe, en las decisiones vigentes según MUD-EDIT-003.

## Estado de las etapas

- Etapa 0 — reglas editoriales persistentes: completada.
- Etapa 1 — inventario inicial: completada.
- Etapa 2 — integración editorial semánticamente neutra: completada.
- Etapa 3 — contradicciones y residuos semánticos en superficies desarrolladas: pendiente.
- Etapa 4 — auditoría sistemática de decisiones vigentes contra superficies existentes: pendiente.
- Etapa 5 — auditoría exhaustiva del documento fuente de la integración D-096: pendiente.
- Etapa 6 — revisión semántica del mapa futuro de `especificacion/README.md`: pendiente.
- Etapa 7 — barrera mecánica contra regresiones editoriales: pendiente.
- Etapa 8 — validación semántica global final: pendiente.

## Taxonomía de trabajo

| Código | Significado |
| --- | --- |
| C | Contradicción interna de una superficie. |
| X | Contradicción con el modelo vigente. |
| I | Integración incompleta: la superficie canónica ya existe pero no contiene una regla aceptada que le corresponde. |
| M | Semántica aceptada pendiente de formalización porque su superficie canónica todavía no existe. |
| Q | Tratamiento incorrecto de una pregunta activa. |
| U | Posible decisión nueva o fortalecimiento no claramente autorizado. |

Las categorías históricas/editoriales `H`, `A` y `D` del inventario inicial se consideran cubiertas por la Etapa 2 salvo que una auditoría posterior demuestre un residuo concreto.

## Decisiones aclaradas durante el saneamiento

### `~private`

`~private` no tiene significado estándar ni controla visibilidad o frontera modular. Sin embargo, `private` puede usarse como nombre de metadata ordinaria de extensión del mismo modo que cualquier otro `identifier` permitido en `metadata-name`.

Por tanto, cualquier regla que reserve o prohíba específicamente la grafía `~private` es un defecto. La corrección no debe reintroducir ninguna semántica estándar de privacidad.

## Etapa 3 — contradicciones y residuos semánticos

Cada punto de esta sección debe cerrarse corrigiendo la superficie vigente y, cuando corresponda, sus artefactos mecánicos relacionados. No debe resolverse mediante notas correctivas añadidas al final del documento.

### E3-01 — Terminología de `thing`

- **Clase:** X.
- **Superficies:** `especificacion/02-terminologia.md` y resúmenes relacionados del índice maestro.
- **Problema:** la formulación «`Thing` declarada, `thing` creada durante la ejecución» reintroduce una separación declaración/instancia incompatible con el modelo ontológico vigente, donde una `thing` no tiene instancias.
- **Criterio de cierre:** la terminología debe distinguir las situaciones relevantes sin convertir `Thing`/`thing` en clase frente a instancia, y ninguna descripción existente o futura debe recuperar esa dicotomía.

### E3-02 — Estado real de `04-modelo-matematico.md`

- **Clase:** C.
- **Superficie:** `especificacion/04-modelo-matematico.md`.
- **Problema:** el capítulo afirma que su contenido normativo todavía no ha sido redactado aunque ya contiene restricciones normativas sustantivas.
- **Criterio de cierre:** `Estado y propósito` debe describir literalmente el grado de formalización actual del capítulo sin negar el contenido normativo que ya contiene.

### E3-03 — `start with` descrito como global

- **Clase:** X.
- **Superficies conocidas:** `especificacion/05-texto-fuente.md`, `especificacion/08-sintaxis-abstracta.md`, `especificacion/09-nombres-y-anclas.md`, `especificacion/sintaxis/cst-a-ast-superficial.md` y artefactos mecánicos relacionados.
- **Problema:** sobreviven formulaciones como «declaración global», «`start with` global y local» o nomenclatura equivalente, aunque el modelo vigente es modular: cada módulo aporta como máximo un `start with`, mientras un test puede tener un conjunto inicial local.
- **Caso mecánico especial:** `GlobalStartDecl` puede ser solo un nombre interno para distinguir top-level de test-local, pero su denominación debe revisarse porque induce la semántica antigua de globalidad del programa.
- **Criterio de cierre:** toda prosa distingue claramente contribución top-level del módulo frente a `start with` local de test; cualquier nombre de AST/IR que conserve «Global» debe estar justificado por una distinción real o renombrarse coherentemente en todos los artefactos.

### E3-04 — Ciclos de `uses`

- **Clase:** I.
- **Superficie canónica existente:** `especificacion/05-texto-fuente.md`.
- **Problema:** el capítulo ya desarrolla `mud.module` y `uses`, pero no integra todavía que los ciclos de dependencias de módulo son legales, producen advertencia por acoplamiento y no establecen orden de inicialización.
- **Criterio de cierre:** las tres propiedades deben quedar expresadas en la sección canónica de módulos/`uses`, sin narración histórica.

### E3-05 — `things` y `rules` en el léxico

- **Clase:** C/X.
- **Superficies:** `especificacion/06-lexico.md` frente a `especificacion/gramatica/mud-lexico.ebnf` y la gramática vigente de `start with`.
- **Problema:** la prosa conserva simultáneamente que `things` y `rules` son etiquetas contextuales obligatorias de `start with` y que no forman parte de su vocabulario vigente. La EBNF mecánica ya refleja la segunda realidad.
- **Criterio de cierre:** eliminar la afirmación antigua y cualquier clasificación léxica derivada de ella; prosa y EBNF deben coincidir.

### E3-06 — Clasificación elemental/compuesta de actions

- **Clase:** X.
- **Superficies conocidas:** `especificacion/07-gramatica-concreta.md`, `especificacion/gramatica/README.md`, `especificacion/README.md` y cualquier otra superficie que todavía difiera «acción elemental» frente a «acción compuesta».
- **Problema:** el modelo vigente usa un `then` unificado y no clasifica semánticamente las actions como elementales o compuestas.
- **Criterio de cierre:** ninguna superficie presenta esa clasificación como categoría vigente, futura o diferida. Las distinciones que sí existan, como `action` frente a `subaction` o capacidad de raíz exterior, deben nombrarse explícitamente y no esconderse bajo «clasificación de acciones».

### E3-07 — Prohibición espuria de `~private`

- **Clase:** X.
- **Superficie principal:** `especificacion/07-gramatica-concreta.md` y cualquier validador o artefacto que haya materializado la prohibición.
- **Problema:** una grafía `~private` se trata como nombre reservado/prohibido, aunque `private` puede ser metadata ordinaria de extensión sin significado especial.
- **Criterio de cierre:** retirar cualquier reserva o rechazo específico de `~private`; mantener únicamente que no existe una metadata estándar `~private` con semántica de privacidad.

### E3-08 — Mapa futuro obsoleto en `especificacion/README.md`

- **Clase:** X.
- **Superficie:** `especificacion/README.md`.
- **Problemas conocidos:**
  - el capítulo 11 vuelve a sugerir `Thing` declaradas frente a creadas;
  - el capítulo 24 planifica actions elementales y compuestas;
  - el capítulo 24 describe `look` sin `given`;
  - el capítulo 24 presenta `message` de forma insuficiente respecto de su naturaleza causal y su participación en ondas;
  - el capítulo 32 conserva la antigua separación de `things` y `rules` dentro de `start with`;
  - el capítulo 43 conserva la idea de sustituir un `start with` global;
  - el itinerario de redacción todavía incluye «acción elemental».
- **Criterio de cierre:** los resúmenes de capítulos futuros no necesitan formalizar por adelantado su semántica, pero no pueden contradecir nada ya decidido. Deben describir alcance futuro compatible con el modelo vigente.

## Etapa 4 — auditoría de decisiones vigentes

No parte de una lista cerrada de defectos. Debe recorrer todas las decisiones vigentes de forma sistemática.

Para cada decisión vigente:

1. leer su alcance y superficies afectadas;
2. determinar qué superficies normativas correspondientes ya están desarrolladas;
3. comprobar que ninguna las contradiga;
4. comprobar que la regla esté integrada en su ubicación canónica cuando esa ubicación exista;
5. clasificar como `M` lo que dependa de una superficie todavía no desarrollada, en lugar de forzarla a un capítulo impropio;
6. registrar cualquier fortalecimiento o regla no sustentada como `U` para revisión explícita.

**Criterio de cierre de la etapa:** toda decisión vigente queda trazada a superficies desarrolladas coherentes o a una obligación `M` explícita para una superficie futura; no quedan contradicciones silenciosas.

## Etapa 5 — auditoría específica de la integración D-096

Recorrer el documento fuente original de la integración regla por regla. Cada afirmación debe acabar en uno y solo uno de estos estados:

- **Integrada:** aparece correctamente en una superficie ya desarrollada.
- **Pendiente de formalización (`M`):** su hogar canónico todavía no existe y ninguna superficie actual la contradice.
- **Mecánicamente integrada:** su obligación actual se satisface en EBNF, CST, AST, IR u otro artefacto mecánico.
- **Pregunta abierta:** la decisión deliberadamente no fija ese extremo.
- **Sospecha (`U`):** la repo afirma algo más fuerte o diferente que la fuente aceptada.

**Criterio de cierre:** ninguna afirmación de la fuente queda sin clasificación y ninguna `U` se resuelve silenciosamente.

## Semántica aceptada pendiente de formalización

Los siguientes puntos no son defectos por su mera ausencia actual. Deben conservarse como obligaciones para cuando se desarrollen sus superficies canónicas.

| Obligación | Estado | Hogar probable |
| --- | --- | --- |
| Compatibilidad y varianza exacta entre tipos callable | Pregunta abierta | `10-sistema-de-tipos.md` |
| Binding nominal de un descriptor callable cuyo tipo se haya borrado o ensanchado | Pregunta abierta, Q-066 | tipos / expresiones / frontera pública |
| Almacenar un descriptor callable no pre-vincula receptor ni argumentos `given`; la vinculación ocurre en la invocación | M | expresiones / frontera pública / evaluación |
| Violación dinámica del dominio de un `given` de `look`: error de consulta desde host y posible `failed` dentro de una resolución | M | frontera pública + evaluación/acciones |
| Join de resultados de `look` invocado dinámicamente | Parte aceptada + Q-065 | tipos / frontera pública |
| Una `thing` visible entre módulos expone identidad y tipo nominal, no sus campos ordinarios; el estado público se proyecta mediante `look` | M | `11-things.md` + frontera pública |
| Reflexión cruzada segura por contrato y sin filtrado silencioso | M | tipos / reflexión / frontera pública |
| Una `thing` no puede especializar otra `thing` de otro módulo | M | `11-things.md` |
| La API host canónica se organiza alrededor de la identidad de las operaciones públicas, no de un participante arbitrario como propietario | M | frontera pública |
| Un ciclo puramente causal de mensajes/disparos puede impedir la estabilización aunque el estado no cambie | M | ondas / estabilización |
| Proyección causal interna y proyección final al host de `message`, con rollback que cancela entrega exterior | M en detalle | frontera pública + ondas |
| Los tests incorporan el cierre transitivo estático de `start with` de los módulos alcanzables | M en detalle | `43-tests-declarativos.md` |

Cuando aparezca cualquiera de estos capítulos, MUD-EDIT-003 obliga a promover la regla a esa superficie. Hasta entonces no debe duplicarse en un capítulo impropio solo para «tenerla en specification».

## Etapa 6 — mapa futuro

Además de cerrar E3-08, revisar todas las entradas `Archivo previsto` de `especificacion/README.md` con estas condiciones:

- describen alcance, no historia de decisiones;
- no contienen semántica ya sustituida;
- no actúan como un almacén normativo alternativo al futuro capítulo;
- reflejan las obligaciones `M` relevantes para que el futuro capítulo no nazca con un diseño anterior ya descartado.

**Criterio de cierre:** el mapa futuro es compatible con el estado vigente sin intentar formalizar anticipadamente capítulos inexistentes.

## Etapa 7 — barrera mecánica

Añadir una comprobación editorial automática para reducir regresiones de MUD-EDIT-002 y del tratamiento de preguntas activas.

Como mínimo debe poder detectar:

- identificadores `D-NNN` o `ADR-NNN` en cuerpos normativos de `especificacion/`, excluyendo metadatos y el propio documento que define la convención;
- encabezados del tipo «Actualización/Revisión/Proyección ... D-NNN» y expresiones inequívocas de migración editorial;
- una referencia corporal a una `Q-NNN` cerrada;
- una referencia corporal a una Q activa ausente de `questions:` cuando el documento disponga de frontmatter;
- una pregunta cerrada que permanezca en `questions:`.

No debe intentar decidir mediante regex si cualquier frase negativa es historia o una prohibición vigente; esa distinción necesita revisión semántica.

**Criterio de cierre:** el validador falla ante fixtures representativos de cada regresión y pasa sobre la especificación saneada.

## Etapa 8 — auditoría final

Antes de considerar cerrado el saneamiento:

1. buscar globalmente `D-NNN`/`ADR-NNN` en cuerpos de `especificacion/`;
2. revisar manualmente términos de riesgo editorial como `retirado`, `sustituye`, `actualización`, `migrada`, `antes` y `anterior`;
3. comprobar referencias y frontmatter de todas las preguntas activas;
4. comprobar que ninguna pregunta cerrada siga activa en la especificación;
5. cruzar decisiones vigentes con superficies desarrolladas;
6. comprobar coherencia prosa ↔ EBNF ↔ CST ↔ AST ↔ IR;
7. ejecutar todos los validadores oficiales y la barrera editorial de Etapa 7;
8. revisar el diff global del saneamiento para detectar cambios semánticos accidentales.

**Criterio de cierre global:** una persona puede leer solo las superficies ya desarrolladas de `especificacion/` y obtener el estado formalizado vigente de MUD sin reconstruir historia decisional ni encontrar contradicciones conocidas; las reglas aceptadas cuyo capítulo aún no existe permanecen localizables como autoridad transitoria y obligaciones `M`, no como apéndices impropios.
