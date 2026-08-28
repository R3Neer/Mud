---
title: Inventario de saneamiento de la especificación
tags:
  - mud/notas
  - mud/especificacion
  - mud/saneamiento
status: activo
temporary: true
temporary-reason: "Checklist operativo del saneamiento de la especificación"
temporary-delete-when: "Se complete la Etapa 8 del saneamiento de la especificación"
---

# Inventario de saneamiento de la especificación

Este documento es un checklist de trabajo no normativo. Resume los defectos y obligaciones todavía relevantes detectados durante la auditoría de `especificacion/` posterior a la integración de módulos, callables, `look`, `message` y activación modular.

No define MUD. La autoridad normativa permanece en `especificacion/` y, transitoriamente cuando la superficie canónica todavía no existe, en las decisiones vigentes según MUD-EDIT-003.

## Estado de las etapas

- Etapa 0 — reglas editoriales persistentes: completada.
- Etapa 1 — inventario inicial: completada.
- Etapa 2 — integración editorial semánticamente neutra: completada.
- Etapa 3 — contradicciones y residuos semánticos en superficies desarrolladas: completada.
- Etapa 4 — auditoría sistemática de decisiones vigentes contra superficies existentes: completada.
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

## Etapa 3 — contradicciones y residuos semánticos

Completada. Los puntos E3-01 a E3-08 se cerraron integrando la regla vigente en sus superficies canónicas y propagando los renombres mecánicos necesarios. El detalle previo queda disponible en Git y no se conserva como deuda activa.

## Etapa 4 — auditoría de decisiones vigentes

Completada. Se recorrieron las 90 decisiones vigentes contra las superficies normativas ya desarrolladas y contra los hogares futuros declarados por el mapa de la especificación.

La auditoría no encontró nuevas contradicciones `C` o `X`, tratamientos incorrectos de preguntas `Q` ni fortalecimientos no sustentados `U`. La ausencia de una regla en un capítulo todavía no desarrollado se clasificó como `M` cuando correspondía, sin forzarla a una superficie impropia.

Se detectaron dos integraciones incompletas concentradas en el IR semántico y ambas quedaron corregidas en su superficie canónica:

- El IR declara versión de esquema y representa estructuralmente clases declarativas, firmas `for`/`on`/`given`, cuerpos semánticos diferenciados, vinculaciones locales ordenadas, efectos y las familias de dependencias exigidas por el modelo vigente.
- La activación inicial de módulo dejó de ser un tipo huérfano: cada `SemanticModule` conserva su `SemanticStartSet` junto con sus dependencias `uses`.

Las obligaciones cuya superficie canónica sigue sin desarrollarse permanecen en la sección siguiente o en el alcance explícito de los capítulos futuros del mapa maestro. No constituyen defectos de integración mientras ninguna superficie existente las contradiga.

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
8. revisar el diff global del saneamiento para detectar cambios semánticos accidentales;

**Criterio de cierre global:** una persona puede leer solo las superficies ya desarrolladas de `especificacion/` y obtener el estado formalizado vigente de MUD sin reconstruir historia decisional ni encontrar contradicciones conocidas; las reglas aceptadas cuyo capítulo aún no existe permanecen localizables como autoridad transitoria y obligaciones `M`, no como apéndices impropios.
