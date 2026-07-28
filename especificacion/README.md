---
title: Especificación formal de MUD
aliases:
  - Índice de la especificación MUD
  - MUD 1.0
tags:
  - mud/especificacion
  - mud/moc
status: en-preparacion
normative: true
---

# Especificación formal de MUD

## Estado del documento

- Estado general: **en preparación**
- Versión objetivo inicial: **MUD 1.0**
- Autoridad actual: los capítulos vigentes de este directorio y las decisiones vigentes enlazadas. [[referencias/MUD Especificacion inicial|La especificación inicial]] es una referencia histórica subsidiaria para requisitos aún no migrados ni sustituidos.
- Alcance: lenguaje MUD completo, su semántica de ejecución y los criterios de conformidad.

Este directorio contendrá la especificación normativa de MUD. Su objetivo es que dos implementaciones independientes puedan:

1. Reconocer los mismos programas.
2. Resolver los mismos nombres y anclas.
3. Asignar los mismos tipos.
4. Rechazar los mismos programas estáticamente.
5. Producir las mismas transiciones semánticas observables.
6. Clasificar de la misma manera `accepted`, `rejected` y `failed`.
7. Coincidir en los análisis de admisibilidad y alcanzabilidad cuando sean decidibles para el programa.

La especificación no presupone una arquitectura de compilador, lenguaje de implementación, base de datos, motor gráfico o framework.

Convenciones de redacción: [[00-convenciones-editoriales]].

Itinerario didáctico: [[aprendizaje/README|Aprendizaje de formalización de MUD]].

## Carácter normativo

Cada contenido tendrá uno de estos estados:

- **Normativo**: define la conformidad de una implementación.
- **Informativo**: explica una norma sin ampliarla.
- **Propuesta**: texto todavía no aprobado.
- **Abierto**: cuestión sin semántica definitiva.

Las palabras se usarán con este sentido:

- **debe**: requisito de conformidad.
- **no puede**: prohibición de conformidad.
- **puede**: comportamiento permitido.
- **debería**: recomendación no normativa.

Una implementación no puede elegir silenciosamente un comportamiento para una cuestión marcada como abierta y seguir declarándose conforme con esa característica.

## Arquitectura de la especificación

La especificación se organizará en cinco partes. La separación es conceptual: algunos capítulos dependen de definiciones anteriores, pero ninguna parte puede contradecir las demás.

```text
Parte I    Fundamentos y notación
Parte II   Lenguaje estático
Parte III  Semántica dinámica
Parte IV   Análisis semánticos avanzados
Parte V    Conformidad y apéndices normativos
```

El compilador, el plugin conversacional, Git y los materializadores tendrán especificaciones propias. Se apoyan en el lenguaje, pero no definen su significado.

---

# Parte I — Fundamentos y notación

## 01. Alcance, conformidad y versiones

Capítulo: [[01-alcance-y-conformidad]].

Define:

- Objeto de la especificación.
- Qué significa implementar MUD.
- Perfiles de conformidad.
- Extensiones y características experimentales.
- Compatibilidad entre versiones.
- Autoridad de ejemplos, notas y apéndices.
- Tratamiento normativo de cuestiones abiertas.

## 02. Terminología

Capítulo: [[02-terminologia]].

Glosario normativo de:

- Programa, módulo, archivo y namespace.
- Declaración, símbolo, nombre y ancla.
- Constructo, instancia y valor.
- Campo, relación y colección.
- Participante, rol, vinculación y `given`.
- Regla consultable, reactiva y `always`.
- Acción, solicitud, raíz, onda y resolución.
- Estado, instantánea, efecto y conflicto.
- Dominio, restricción, condición e invariante.
- Aceptación, rechazo y fallo.

## 03. Notación matemática y metalenguaje

Capítulo: [[03-notacion]].

Fija la simbología utilizada en el resto de la norma:

- Conjuntos, secuencias, multiconjuntos y mapas finitos.
- Relaciones, funciones parciales y clausuras transitivas.
- Grafos dirigidos.
- Gramáticas EBNF.
- Juicios de tipado.
- Reglas de inferencia.
- Semántica operacional.
- Sistemas de transición etiquetados.
- Órdenes parciales y puntos fijos.
- Probabilidad y semillas reproducibles.

Juicios previstos:

$$
\Gamma \vdash n \rightsquigarrow a
$$

«En el entorno $\Gamma$, el nombre $n$ se resuelve al ancla $a$».

$$
\Gamma;\Sigma \vdash e : \tau
$$

«En los entornos $\Gamma$ y $\Sigma$, la expresión $e$ tiene tipo $\tau$».

$$
\Gamma;\Sigma \vdash e\ \mathsf{reads}\ R
$$

«La expresión $e$ puede leer el conjunto de anclas $R$».

$$
\langle W, q \rangle \Downarrow \langle W', r, T \rangle
$$

«La solicitud $q$ sobre el mundo $W$ termina en el mundo $W'$, con resultado $r$ y traza causal $T$».

## 04. Modelo matemático del mundo

Capítulo: [[04-modelo-matematico]].

Define, antes de hablar de sintaxis:

- Universos de anclas, `thing` y valores.
- Estado del mundo.
- Store de campos y relaciones.
- Identidad frente a igualdad estructural.
- Estados bien formados.
- Instantáneas estables y tentativas.
- Observaciones semánticamente visibles.

---

# Parte II — Lenguaje estático

## 05. Texto fuente y estructura física

Archivo previsto: `05-texto-fuente.md`

Define:

- Codificación.
- Archivos `.mud`.
- Derivación de namespaces desde rutas.
- Varias declaraciones por archivo.
- Independencia semántica respecto al orden de archivos.
- Terminadores de línea.

## 06. Estructura léxica

Archivo previsto: `06-lexico.md`

Define:

- Categorías de caracteres.
- Identificadores y sensibilidad a mayúsculas.
- Palabras reservadas.
- Literales numéricos, monetarios y porcentuales.
- Literales de texto.
- Comentarios `#`, `#...#` y `###...###`.
- Espacio en blanco.
- Tokens y errores léxicos.

La gramática léxica ejecutable vivirá en `gramatica/mud-lexico.ebnf`.

## 07. Gramática concreta

Archivo previsto: `07-gramatica-concreta.md`

Define la sintaxis completa de:

- Imports.
- Declaraciones.
- Tipos.
- Campos.
- Participantes.
- Valores `given`.
- Expresiones.
- Efectos.
- Bloques.
- Llamadas.
- Definiciones completas de reglas y sus activaciones abreviadas mediante `create Nombre`.
- Cuantificadores e iteraciones.

La gramática completa ejecutable vivirá en `gramatica/mud.ebnf`. Este capítulo explicará ambigüedades, precedencia y desazucarado, pero no repetirá toda la EBNF.

## 08. Sintaxis abstracta

Archivo previsto: `08-sintaxis-abstracta.md`

Define las formas semánticamente relevantes después del parsing:

- AST de declaraciones.
- AST de tipos y dominios.
- AST de expresiones.
- AST de efectos.
- Distinción entre definición de regla con activación y referencia de activación.
- Distinción estructural entre las tres clases de regla.
- Distinción entre acciones elementales y compuestas.
- Nodos propios para `look`, `message` y propiedades públicas.
- Azúcares sintácticos y forma núcleo.

## 09. Namespaces, imports, nombres y anclas

Archivo previsto: `09-nombres-y-anclas.md`

Define:

- Ámbitos.
- Resolución local y cualificada.
- Imports exactos y recursivos.
- Ambigüedad.
- Formación y unicidad de anclas.
- Identidad ante movimientos de archivo.
- Migración de namespace y anclas.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$

Base normativa migrada: [[notas/decisiones/ADR-035-organizacion-nombres-imports-y-anclas|D-035]].

## 10. Sistema de tipos

Archivo previsto: `10-sistema-de-tipos.md`

Define:

- `Text` y `Bool` como tipos básicos no numéricos.
- `Natural`, `Integer`, `Number`, `Rumber` y `Money` como representaciones numéricas básicas, no magnitudes.
- `Number` como racional exacto y `Rumber` como IEEE 754 `binary64` explícito.
- Tipos de `thing`.
- Tipos nominales de alias.
- Familias cerradas.
- Colecciones y diccionarios.
- Intervalos.
- Magnitudes.
- Subtipado mediante `is`.
- Inferencia y ampliación de representaciones en operaciones cuantitativas.
- Dos familias explícitas de `to`: conversión cuantitativa y casting nominal estructural.
- Redondeo global al más cercano con empates al par.
- Igualdad y orden por tipo.

Juicio principal:

$$
\Gamma;\Sigma \vdash e : \tau
$$

## 11. `Thing`, especialización e identidad

Archivo previsto: `11-things.md`

Define:

- `Thing` concretas y abstractas.
- `Thing` declaradas y creadas durante la ejecución.
- Especialización simple y múltiple.
- Cabeceras de especialización con `as` y consultas con `is`.
- Sustituibilidad.
- Fusión de campos homónimos.
- Valores predeterminados heredados.
- Igualdad de identidad.
- Canonicalización de identidades de `thing`.

## 12. Aliases nominales y valores estructurales

Archivo previsto: `12-aliases.md`

Define:

- Definición de tipo mediante `:=` y bloque estructural.
- Componentes obligatorios, ordenados, con dominio y sin `mut`.
- Nominalidad de todos los aliases.
- Valores inmutables y ausencia de identidad runtime.
- Prohibición de `create`, `destroy`, abstracción y especialización.
- Literales contextuales posicionales y nombrados.
- Casting nominal mediante `to` y compatibilidad de forma normalizada.
- Igualdad por alias y contenido.
- Orden lexicográfico cuando la representación está ordenada.
- Claves compuestas y azúcar de acceso.
- Finitud, enumerabilidad y producto cartesiano lexicográfico.

## 13. Familias cerradas de valores

Archivo previsto: `13-familias-cerradas.md`

Define:

- `values`.
- `ordered values`.
- Identidad nominal.
- Campos comunes y específicos.
- Herencia de familias.
- Enumeración finita.

Base normativa migrada: [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]].

## 14. Campos, mutabilidad y capacidades

Archivo previsto: `14-campos-y-mutabilidad.md`

Define:

- Campos almacenados y calculados.
- `=` frente a `:=`.
- Mutabilidad exterior.
- Capacidad interior `[mut]`.
- Ortogonalidad de ambos permisos también para cardinalidad `[1]`.
- Campos derivados como vistas de colección sin mutabilidad exterior.
- Mutabilidad de participantes.
- Accesibilidad de escrituras.
- Ausencia de mutabilidad profunda implícita.

Bases normativas migradas: [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]] y [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]].

## 15. Cardinalidades y colecciones

Archivo previsto: `15-colecciones.md`

Define:

- Cardinalidades como intervalos de naturales.
- Ausencia mediante `empty`.
- Multiplicidad y `unique`.
- Membresía estricta de `thing`, con exclusión incondicional del ancla exacta del tipo.
- Colecciones ordenadas y no ordenadas.
- Orden natural, de inserción, semántico y `ordered by`.
- Igualdad de colecciones.
- Instantáneas de iteración.

Bases normativas migradas: [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]] y [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]].

## 16. Diccionarios

Archivo previsto: `16-diccionarios.md`

Define:

- Tipos de clave y valor.
- Cardinalidad.
- Claves compuestas.
- Lectura y escritura de claves ausentes.
- Materialización de entradas.
- Iteración por claves y entradas.
- Orden canónico.
- Operaciones totales.
- Alias nominal como clave única compuesta y azúcar `map[c1, c2]`.

Base normativa migrada: [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]].

## 17. Dominios e intervalos

Archivo previsto: `17-dominios-e-intervalos.md`

Define:

- Declaraciones `in`.
- Dominios de campos, aliases y `given`.
- Dominios calculados.
- Pertenencia.
- Intervalos abiertos, cerrados, vacíos y discontinuos.
- Límites efectivos laterales mediante `*` y azúcar `[*]`.
- Normalización.
- Finitud y enumerabilidad.
- Pasos de iteración.
- Dominios dinámicos.
- Dominios cíclicos `[a..b cycle)` exclusivos de magnitudes de punto.
- Intervalos `Rumber` admitidos como dominios, pero no como fuentes enumerables.

## 18. Magnitudes, unidades y puntos

Archivo previsto: `18-magnitudes.md`

Define:

- Magnitudes no derivadas, derivadas y de punto.
- Representaciones numéricas explícitas e inferidas.
- Magnitudes basadas en `Rumber` y omisión contextual del prefijo `r` en cantidades con unidad.
- Unidades raíz sin identificador de cabecera y equivalencias mediante `:=`.
- Prefijos.
- Normalización.
- Aritmética dimensional.
- Inferencia de unidades canónicas derivadas y combinaciones automáticas.
- Unidades nominales derivadas opcionales.
- Declaraciones `point over`, ciclos y formatos.
- Magnitudes temporales.
- Calendarios y localización.

## 19. Expresiones

Archivo previsto: `19-expresiones.md`

Define:

- Literales racionales exactos, literales `Rumber` prefijados con `r` y acceso.
- Llamadas a reglas.
- Receptores multiparte.
- Operadores.
- Precedencia y asociatividad.
- Conversiones.
- Distinción entre presentación en otra unidad mediante `in`, conversión cuantitativa y casting nominal mediante `to`.
- Construcción contextual de literales de alias.
- Propagación bidireccional del tipo esperado entre un alias y un literal en comparaciones.
- `old`.
- `allowed`.
- `eventually`.
- Pureza.
- Elaboración booleana canónica y poda de llamadas a reglas inactivas.
- Fallos dentro de expresiones.

## 20. Cuantificadores, agregaciones e iteración

Archivo previsto: `20-cuantificadores-e-iteracion.md`

Define:

- `exists`, `forall`, `count`, `sum`, `min` y `max`.
- `for each`.
- Fuentes finitas.
- Orden de recorrido.
- Instantánea de pertenencia.
- Iteraciones secuenciales y simultáneas.
- Filtros.
- Terminación de intervalos.
- Prohibición de enumerar intervalos `Rumber`.
- Enumeración de aliases estructurales como productos cartesianos lexicográficos.

## 21. Reglas booleanas

Archivo previsto: `21-reglas-booleanas.md`

Define:

- Participantes `for`.
- Valores `given`.
- Receptor único y multiparte.
- Pureza.
- Resultado booleano.
- Dominios fuera de rango.
- Dependencias y memorización.
- Borrado estructural cuando la declaración no sea efectiva.

## 22. Reglas reactivas

Archivo previsto: `22-reglas-reactivas.md`

Define:

- Vinculaciones `on`.
- Participantes relacionados mediante `in`.
- `when`.
- `changes`.
- `if`.
- `then`.
- Estado anterior por vinculación.
- Creación y eliminación de vinculaciones.

## 23. Reglas `always`

Archivo previsto: `23-reglas-always.md`

Define:

- Vinculaciones `on`.
- Pureza.
- Estados en que deben comprobarse.
- Incumplimiento y resultado de resolución.
- Dependencias.

## 24. Frontera pública: `action`, `look` y `message`

Archivo previsto: `24-frontera-publica.md`

Define:

- Participantes `for`.
- Valores `given`.
- `if`, `then` y `after`.
- Acciones elementales.
- Acciones compuestas.
- Vinculación posicional y nombrada.
- Aciclicidad de llamadas.
- Acciones como API externa de escritura.
- Posibles valores de retorno.
- `look` como consulta pública pura de un estado estable.
- Participantes `for` sin `given`.
- `message` como evento detectado durante las ondas de una acción.
- Vinculaciones `on`, condición `when` y guarda `if` opcional.
- Propiedades públicas tipadas y calculadas.
- Evaluación diferida de las propiedades del mensaje tras la estabilización.
- Multiplicidad, orden, deduplicación, rollback y entrega.

## 25. Efectos

Archivo previsto: `25-efectos.md`

Define:

- Asignaciones.
- Actualizaciones aritméticas.
- Operaciones de colección.
- Adición y retirada dinámica de propiedades.
- `create`.
- `destroy`.
- Resolución de `create Nombre` a la definición canónica de una regla.
- Efectos de bucles.
- Conjuntos de lectura y escritura.
- Compatibilidad y conflicto entre efectos.
- Consolidación determinista de deltas privados de distintos `then`.
- Álgebra de composición de efectos.

Juicio previsto:

$$
\Gamma;\Sigma \vdash b : \mathsf{Effect}(R,W,C,D)
$$

donde $R$, $W$, $C$ y $D$ representan anclas leídas, escritas, creadas y destruidas.

---

# Parte III — Semántica dinámica

## 26. Estado y evaluación de expresiones

Archivo previsto: `26-evaluacion.md`

Define:

- Entornos de participantes y `given`.
- Lectura del store.
- Evaluación determinista.
- Propagación de ausencias y fallos.
- Poda y cierre de fragmentos booleanos borrados.
- Evaluación de campos calculados.
- Estado inicial observado por expresiones.

Juicio previsto:

$$
\Gamma;\rho;W \vdash e \Downarrow v
$$

## 27. Solicitud y resultado de acciones

Archivo previsto: `27-solicitud-de-acciones.md`

Define:

- Cola externa.
- Momento de vinculación.
- Validación de dominios.
- Evaluación de `if`.
- `accepted`, `rejected` y `failed`.
- Visibilidad del estado.
- Atomicidad y rollback.

## 28. Semántica de la raíz

Archivo previsto: `28-raiz.md`

Define:

- Evaluación de efectos elementales.
- Secuencialidad interna.
- Composición de acciones.
- Lectura común del estado inicial.
- Raíz simultánea.
- Overlays secuenciales privados por `then`.
- Normalización de efectos.
- Conflictos de raíz.

## 29. Semántica causal por ondas

Archivo previsto: `29-ondas.md`

Define:

- Instantánea de una onda.
- Vinculaciones activas.
- Detección de transiciones.
- Cálculo simultáneo de consecuencias.
- Combinación de efectos.
- Paso a la onda siguiente.
- Estado estable.
- Traza causal.

Se modelará inicialmente como un sistema de transición:

$$
\langle W_i, B_i, P_i \rangle
\xrightarrow{\mathsf{wave}}
\langle W_{i+1}, B_{i+1}, P_{i+1} \rangle
$$

## 30. Restricciones, `after` y `old`

Archivo previsto: `30-restricciones-finales.md`

Define:

- Prueba estática de cardinalidad al final de cada `then`.
- Compatibilidad cardinal de la consolidación de varios `then`.
- Puntos de comprobación de dominios y demás invariantes.
- Comprobación de reglas `always`.
- Estado observado por `old`.
- Momento de evaluación de `after`.
- Rechazo final.
- Restauración completa.

## 31. Conflictos, ciclos y estabilización

Archivo previsto: `31-conflictos-y-estabilizacion.md`

Define:

- Relación de compatibilidad de efectos.
- Matriz normativa de conflictos.
- Fusión parcial de fragmentos concurrentes de `thing`.
- Consolidación idempotente de activaciones concurrentes de una regla con definición única.
- Ciclos causales.
- Oscilaciones.
- Detección de repetición.
- Límites técnicos frente a significado semántico.
- Condición de estabilización.

## 32. Creación, destrucción e identidad runtime

Archivo previsto: `32-ciclo-de-vida-runtime.md`

Define:

- Creación de `thing` raíz, abstractas y con especialización múltiple.
- Reserva global, activación y reactivación de los nombres introducidos por `create`.
- Cuerpo declarativo completo de las creaciones.
- Inicialización de la primera materialización.
- Distinción entre almacenamiento retenido y proyección efectiva.
- Suspensión por dependencias.
- Restauración sin reinicialización.
- `remove` destructivo frente a `destroy` reversible.
- Referencias y propiedades latentes.
- Constructos estáticos.
- Creación y eliminación de vinculaciones.

## 33. Aleatoriedad

Archivo previsto: `33-aleatoriedad.md`

Define:

- `Rand` almacenado y calculado.
- Azar dentro de efectos.
- Espacio de resultados.
- Semillas y subsemillas.
- Identidad de puntos aleatorios.
- Cachés por instantánea.
- Reproducibilidad.
- Interacción con rollback.

---

# Parte IV — Análisis semánticos avanzados

## 34. Grafo semántico

Archivo previsto: `34-grafo-semantico.md`

Define:

- Clases de nodos.
- Relaciones.
- Dependencias.
- Lecturas y escrituras.
- Patrones de vinculación.
- Dependencias estocásticas.
- Propiedades reconstruibles desde el programa.

## 35. Consulta especulativa `allowed`

Archivo previsto: `35-allowed.md`

Define:

- Mundo especulativo.
- Ejecución descartable.
- Conversión de resultados a booleano.
- Propagación de fallos.
- Aciclicidad del grafo de admisibilidad.
- Aleatoriedad reproducible.

## 36. Alcanzabilidad `eventually`

Archivo previsto: `36-eventually.md`

Define:

- Sistema de transición explorado.
- Estado objetivo.
- Secuencia vacía.
- Acciones permitidas por `through`.
- Múltiples acciones.
- Semántica existencial del azar.
- Estrategia BFS cuando sea normativa.

## 37. Finitud, enumerabilidad y estado relevante

Archivo previsto: `37-finitud-y-enumerabilidad.md`

Define:

- Dominios finitos.
- Enumeración canónica.
- Perfil de mundos finitos.
- Estado relevante.
- Comparación y canonicalización de estados.
- Creación acotada.
- Condiciones suficientes para compilar `eventually`.

## 38. Terminación y decidibilidad

Archivo previsto: `38-terminacion.md`

Define:

- Terminación de iteraciones.
- Terminación de resoluciones.
- Análisis conservadores.
- Frontera entre rechazo estático y fallo runtime.
- Posible subconjunto no Turing completo.
- Propiedades decidibles y semidecidibles.

## 39. Propiedades metateóricas

Archivo previsto: `39-propiedades.md`

Objetivos de demostración:

- Unicidad de resolución de nombres.
- Preservación de tipos.
- Progreso para programas bien tipados, sujeto a resultados semánticos explícitos.
- Determinismo sin azar.
- Reproducibilidad con azar sembrado.
- Atomicidad.
- Independencia del orden de archivos.
- Independencia del orden interno de estructuras no ordenadas.
- Corrección de la especulación.
- Condiciones de terminación de `eventually`.

No todas estas propiedades tienen por qué ser demostrables para el lenguaje completo. La especificación deberá indicar hipótesis y contraejemplos con honestidad.

---

# Parte V — Conformidad y apéndices

## 40. Diagnósticos

Archivo previsto: `40-diagnosticos.md`

Define:

- Categorías y códigos.
- Errores léxicos, sintácticos, estáticos y dinámicos.
- Localizaciones y anclas relacionadas.
- Diagnósticos obligatorios.
- Libertad de redacción.
- Recuperación tras errores.

## 41. Representación intermedia canónica

Archivo previsto: `41-ir.md`

Define:

- Esquema versionado.
- Normalización.
- Procedencia.
- Tipos y anclas resueltos.
- Participantes y `given`.
- Efectos.
- Índices.
- Compatibilidad.

El esquema ejecutable vivirá en `esquemas/mud-ir.schema.json`.

## 42. Conformidad de implementaciones

Archivo previsto: `42-conformidad.md`

Define:

- Implementación completa.
- Implementación de análisis.
- Runtime conforme.
- Materializador conforme.
- Características opcionales.
- Requisitos de determinismo.
- Declaración de versión.

## 43. Suite de conformidad

Archivo previsto: `43-suite-de-conformidad.md`

Define:

- Casos válidos.
- Casos inválidos.
- Diagnósticos requeridos.
- IR esperado.
- Transiciones y trazas esperadas.
- Pruebas de propiedades.
- Casos de regresión normativa.

El corpus vivirá en:

```text
conformidad/
├── validos/
├── invalidos/
├── ejecucion/
├── diagnosticos/
└── propiedades/
```

## 44. Gramática consolidada

Archivo previsto: `44-gramatica-consolidada.md`

Apéndice normativo generado o verificado contra `gramatica/mud.ebnf`.

## 45. Catálogo de palabras reservadas

Archivo previsto: `45-palabras-reservadas.md`

Lista normativa, clasificación y versión de introducción o retirada.

## 46. Ejemplos integrales

Archivo previsto: `46-ejemplos-integrales.md`

Ejemplos informativos construidos únicamente con reglas ya especificadas. No introducen comportamiento nuevo.

## 47. Compatibilidad y migraciones

Archivo previsto: `47-compatibilidad.md`

Define:

- Cambios compatibles e incompatibles.
- Evolución de anclas.
- Migración de programas.
- Migración del IR.
- Obsolescencia de sintaxis.

## 48. Índice de reglas normativas

Archivo previsto: `48-indice-normativo.md`

Índice generado de requisitos con identificadores estables, por ejemplo:

```text
MUD-LEX-001
MUD-SYN-014
MUD-NAME-008
MUD-TYPE-023
MUD-ACTION-011
MUD-WAVE-006
MUD-REACH-004
```

---

# Especificaciones relacionadas, pero separadas

Estos documentos no forman parte de la definición del lenguaje:

```text
tooling/
├── compilador.md
├── cli.md
├── soporte-de-editor.md
├── operador-semantico.md
├── protocolo-git.md
├── materializacion-typescript.md
└── plugin-codex.md
```

La separación evita que una decisión de arquitectura se convierta accidentalmente en una regla de MUD.

## Dependencias principales

```text
notación
   │
   ├──► modelo matemático
   │       │
   │       ├──► tipos y valores
   │       └──► estado y efectos
   │
léxico ─► gramática ─► sintaxis abstracta
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
      semántica estática     semántica dinámica
              │                     │
              └──────────┬──────────┘
                         ▼
              análisis avanzados
                         │
                         ▼
                   conformidad
```

## Orden de redacción

El orden numérico es el orden de lectura final, no el orden estricto de escritura. Se trabajará en ciclos verticales:

1. Definir notación mínima.
2. Elegir una construcción de MUD.
3. Formalizar su sintaxis concreta y abstracta.
4. Formalizar sus reglas estáticas.
5. Formalizar su comportamiento dinámico.
6. Escribir ejemplos y contraejemplos.
7. Añadir pruebas de conformidad.
8. Revisar dependencias y cuestiones abiertas.

Primer ciclo recomendado:

```text
thing
→ campos básicos
→ regla booleana
→ acción elemental
→ look
→ estado
→ message
→ accepted/rejected/failed
```

Esto permite formalizar el lenguaje completo progresivamente sin empezar la implementación ni posponer todas las comprobaciones hasta el final.

## Criterio de “especificación completa”

MUD 1.0 estará formalmente especificado cuando:

1. No quede ninguna producción gramatical sin semántica.
2. Toda construcción tenga reglas estáticas.
3. Todo programa estáticamente válido tenga un comportamiento definido o un fallo explícitamente definido.
4. Toda interacción entre características esté cubierta o prohibida.
5. Todas las cuestiones abiertas de MUD 1.0 estén resueltas.
6. La gramática y el esquema IR sean verificables automáticamente.
7. Exista una suite de conformidad representativa.
8. Las propiedades prometidas estén demostradas o delimitadas mediante hipótesis explícitas.
9. Los ejemplos integrales no dependan de comportamiento implícito.
10. Una implementación pueda declarar de forma objetiva su grado de conformidad.
