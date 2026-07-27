# Auditoría de cobertura y divergencias de la fuente inicial

- Estado: auditoría de procedencia
- Fuente auditada: `C:\Users\Usuario\Downloads\MUD Especificacion inicial.md`
- Fecha de la fuente observada: 2026-07-27 12:00:02
- Líneas: 3652
- SHA-256: `9E0CDB7626ADF2B525720B094BE3C33D296D06C7952302D68645F16F8E56A423`
- Documentos relacionados: [[notas/11-trazabilidad-de-la-fuente]], [[notas/10-registro-de-decisiones]], [[especificacion/README]]

## Conclusión

El contenido de la especificación inicial **no está todavía formalizado por completo dentro del repositorio**.

La documentación actual sí:

- Conserva la visión general y la arquitectura conceptual.
- Proporciona un índice normativo que asigna un futuro capítulo a cada tema.
- Resume la mayoría de las 78 secciones.
- Registra varias decisiones posteriores mediante ADR.
- Formaliza la notación matemática básica y una parte del modelo de constructos.

Pero la matriz anterior de [[notas/11-trazabilidad-de-la-fuente]] demostraba únicamente **enrutamiento temático**: cada sección tenía algún documento relacionado. No demostraba que todas sus reglas, ejemplos, casos límite y diagnósticos hubieran sido incorporados.

En particular, gran parte del detalle normativo sobre léxico, intervalos, bucles, magnitudes, operadores, diccionarios, aleatoriedad, grafo e IR solo permanece en el archivo de Descargas. Hasta incorporarlo o sustituirlo explícitamente, ese archivo sigue siendo necesario para reconstruir el diseño inicial.

## Criterios de esta auditoría

Se distinguen cuatro situaciones:

- **Formalizado**: existe una definición matemática o regla normativa candidata suficientemente precisa.
- **Decidido**: existe un ADR, aunque todavía falte promoverlo a un capítulo normativo.
- **Resumido**: la idea aparece en las notas, pero se han perdido detalles necesarios para implementar dos runtimes equivalentes.
- **Solo en la fuente**: el repositorio puede anunciar el tema en un índice, pero no conserva todavía sus reglas concretas.
- **Sustituido deliberadamente**: una decisión posterior contradice la fuente y conserva la procedencia del cambio.

Una entrada en [[especificacion/README]] solo indica que habrá un capítulo. No cuenta como formalización de su contenido.

## Cobertura por bloques

| Secciones de la fuente | Contenido | Estado real en el repositorio | Destino |
| --- | --- | --- | --- |
| Introducción, 1 y 2 | Objetivo, principios, fuente de verdad, causalidad y límites | Resumido con fidelidad en [[notas/01-vision-y-alcance]] y [[notas/09-riesgos-y-restricciones]]; todavía no normativo | Capítulos 01, 27 a 31 y especificaciones separadas de tooling |
| 3 | Clases de declaración | Resumido; varios ciclos de vida han sido sustituidos después | Capítulos 02, 11 a 24 y ADR de ciclo de vida |
| 4 a 9 | Archivos, imports, nombres, participantes, llamadas y anclas | Resumido; faltan gramática, resolución formal y diagnósticos | Capítulos 05 a 09, 21 y 24 |
| 10 | Constructos e herencia | Parcialmente formalizado y ampliamente sustituido por D-014 a D-018 | Capítulos 04 y 11 |
| 11 y 12 | Aliases y familias cerradas | Resumido; el ciclo de vida de aliases se ha sustituido deliberadamente | Capítulos 12 y 13 |
| 13 a 19 | Campos, tipos básicos, conversiones, mutabilidad, colecciones, diccionarios y dominios | Resumido; D-017 y D-019 sustituyen partes; la mayoría de reglas concretas siguen solo en la fuente | Capítulos 10 y 14 a 17 |
| 20 a 30 | Magnitudes, prefijos, operaciones, puntos, operadores, intervalos, precedencia y literales | Solo inventariado o resumido. Los pasos de intervalos, extremos, segmentos y restricciones de terminación no están preservados con detalle | Capítulos 18 a 20 |
| 31 a 35 | Tres clases de regla, `when` y `changes` | Resumido; el borrado de reglas inactivas es una decisión posterior | Capítulos 21 a 23 y 29 |
| 36 a 44 | Acciones, `after`, `old`, resultados, `allowed` y `eventually` | Resumido; existen preguntas abiertas sobre composición, rollback y finitud | Capítulos 24 y 27 a 38 |
| 45 a 49 | Ondas, vinculaciones, cola, conflictos y terminación | Resumido; faltan la transición operacional y la matriz de conflictos | Capítulos 28 a 31 |
| 50 a 59 | Efectos, cuantificadores, `for each`, colecciones, ciclo de vida, azar, fallos y predeterminados | Parcialmente resumido y parcialmente sustituido. El detalle de iteración y azar permanece solo en la fuente | Capítulos 20, 25, 26, 32 y 33 |
| 60 y 61 | Tres formas de comentario y terminadores | Solo en la fuente salvo inventario y Q-001 | Capítulos 05 a 07 |
| 62 | Lectura y escritura externas | Resumido con fidelidad | Capítulos 21, 24 y especificación del contrato externo |
| 63 a 66 | Grafo, IR, compilador y TypeScript | Resumido arquitectónicamente; el catálogo exacto de aristas y los ejemplos JSON solo están en la fuente | Capítulos 34, 41 y especificaciones separadas |
| 67 a 71 | Plugin, clasificación, inferencias, agenda y flujo atómico | Resumido; no existe aún contrato formal del operador semántico | Especificaciones separadas de tooling y [[notas/05-cambios-semanticos-y-git]] |
| 72 a 74 | Tests, editor y palabras clave | Inventariado; las listas exactas permanecen solo en la fuente | Capítulos 43 y 45, corpus de conformidad y tooling |
| 75 | Ejemplo integral | No preservado dentro del repositorio; solo se usa como procedencia de futuros ejemplos | Capítulo 46 y corpus de conformidad |
| 76 a 78 | Decisiones, preguntas e instrucciones | Resumido y repartido; las decisiones posteriores deben prevalecer mediante ADR | [[notas/08-preguntas-abiertas]], [[notas/10-registro-de-decisiones]] y gobierno |

## Detalle que hoy solo conserva la fuente

La siguiente información no puede reconstruirse de manera completa a partir de las notas actuales:

1. Las reglas exactas de comentarios `#`, cierre `#...#`, comentarios `###...###`, prioridad léxica y no anidamiento.
2. La tabla completa de palabras clave provisionales.
3. La precedencia completa de operadores.
4. Los pasos predeterminados de intervalos de `Natural`, `Integer` y `Money`.
5. La obligación de `by` para intervalos de `Number`.
6. La iteración de extremos abiertos, intervalos discontinuos y segmentos normalizados.
7. La distinción entre iteraciones secuenciales de fuentes ordenadas y efectos simultáneos de fuentes no ordenadas.
8. La instantánea de pertenencia de `for each`.
9. Las reglas concretas de prefijos y magnitudes de punto.
10. El catálogo inicial completo de relaciones del grafo semántico.
11. Los ejemplos JSON de IR.
12. Los casos de prueba detallados de participantes, `given` y contratos.
13. El ejemplo integral de la sección 75.
14. Varias reglas concretas de diccionarios, incluyendo lectura y materialización de claves ausentes.
15. La tabla inicial de predeterminados primitivos y de colecciones.

Estos elementos no se copiarán ciegamente a la norma. Primero deberán revisarse contra las decisiones posteriores y después promoverse mediante el ciclo documental.

## Cambios deliberados respecto de la fuente

| Tema | Fuente inicial | Estado posterior | Procedencia |
| --- | --- | --- | --- |
| Ontología de constructos | La sintaxis y varios ejemplos sugerían declaración, categoría e identidad runtime separables | Un único dominio de constructos; cada concreto es cosa y posible antecesor | D-014 |
| Declaración de especialización | `construct A is B` | `construct A from B`; `is` queda como consulta | D-018 |
| Ciclos | No existía regla local completa | Se rechaza todo ciclo no trivial | D-015 |
| Herencia de estado | No estaba delimitada con precisión | Solo se heredan esquema y predeterminados; nunca estado mutable actual | D-015 |
| Identidad creada | La fuente hablaba de identificador local y de identidades runtime distintas por creación | El nombre de `create` es una identidad global reservada y reactivable | D-016 |
| Forma de `create` | `create Base NewName` y solo constructos concretos | Raíz, abstracto o varios antecesores, con cuerpo declarativo completo | D-016 |
| Constructos abstractos | No podían crearse | Pueden activarse mediante `create abstract construct` | D-016 y D-021 |
| Predeterminados | Tabla parcial y tipos sin predeterminado universal | Todo tipo bien formado posee predeterminado | D-017 |
| Mutabilidad singular | La conversación detectó una excepción entre mutabilidad exterior e interior | Ambos permisos son ortogonales también en `[1]` | D-019 |
| Alias y `create` | Un alias no podía crearse | Las declaraciones de alias tienen ciclo de vida efectivo; sus valores siguen sin identidad | D-021 |
| Reglas y `create` | Las reglas no tenían ciclo de vida dinámico | Reglas booleanas, reactivas y `always` pueden activarse y destruirse | D-021 |
| Definiciones de reglas y aliases | No existía activación separada de una definición | Una definición completa única y activaciones posteriores mediante `create Nombre` | D-024 |
| Regla booleana inactiva | No contemplada | Su aparición se borra estructuralmente de la fórmula | D-022 |
| Destrucción | Podía fallar por referencias o cardinalidad | Suspensión lógica reversible con conservación del contenido almacenado | D-021 |
| Propiedades dinámicas | `add` y `remove` solo operaban sobre colecciones | También añaden y eliminan propiedades; `remove` sí pierde su contenido | D-021 |
| Miembro reflexivo | `T` podía habitar implícitamente `T[k]` por `T is T` | La membresía exacta del ancla de tipo requiere `[reflexive]` | D-020 |

## Estado de la formalización profesional

Dentro de `especificacion/`:

- [[especificacion/03-notacion]] es el único capítulo con un cuerpo formal sustancial.
- [[especificacion/04-modelo-matematico]] contiene restricciones y procedencia, pero todavía es un esqueleto.
- Los capítulos 01 y 02 son esqueletos.
- Los capítulos 05 a 48 existen únicamente como índice previsto.

Los ADR D-014 a D-019 contienen formalización útil, pero una decisión no sustituye el capítulo normativo, su gramática, sus juicios, ejemplos, diagnósticos y pruebas.

## Regla de conservación a partir de esta auditoría

Hasta que una sección de la fuente haya sido:

1. incorporada a un documento versionado;
2. sustituida por una decisión explícita; o
3. rechazada con justificación;

debe considerarse **pendiente de migración**, no “ya cubierta”.

La futura auditoría de promoción deberá trabajar por requisito concreto, no solo por número de sección.
