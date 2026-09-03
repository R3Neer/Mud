---
title: Especificación formal de MUD
aliases:
  - Índice de la especificación MUD
  - MUD 1.0
tags:
  - mud/specification
  - mud/moc
status: in-preparation
normative: true
questions:
  - Q-063
  - Q-064
  - Q-065
  - Q-066
  - Q-067
  - Q-068
---

# Especificación formal de MUD

## Estado del documento

- Estado general: **en preparación**
- Versión objetivo inicial: **MUD 1.0**
- Autoridad actual: los capítulos con `status: vigente` y las decisiones vigentes enlazadas. Un archivo con `normative: true` pertenece a la superficie normativa, pero su `status` determina si el capítulo completo ya tiene autoridad consolidada. Los capítulos no vigentes pueden incorporar reglas respaldadas por decisiones vigentes, pero no las sustituyen ni cierran cuestiones abiertas. El historial Git conserva la procedencia retirada, pero no tiene autoridad subsidiaria.
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

## Carácter normativo

La superficie y el estado de publicación son ejes distintos. `normative: true` indica que el archivo está destinado a contener reglas de conformidad; no equivale por sí solo a aprobación. El ciclo `esqueleto → borrador → propuesta → en-revision → vigente` determina la autoridad del capítulo como unidad.

- **Capítulo vigente**: su texto normativo es autoridad consolidada.
- **Capítulo no vigente**: puede transcribir o explicar contratos ya fijados por decisiones vigentes y artefactos mecánicos coherentes, pero el capítulo completo sigue en preparación y no puede introducir autoridad nueva por encima de esas fuentes.
- **Contenido informativo**: explica una norma sin ampliarla.
- **Cuestión abierta**: carece de semántica definitiva hasta que el proceso de decisiones la cierre o la excluya explícitamente del perfil aplicable.

Una contradicción entre un capítulo no vigente y una decisión vigente se considera un defecto documental; no una nueva elección semántica. Una contradicción entre prosa normativa y un artefacto mecánico normativo también es un defecto y debe corregirse, conforme a MUD-EDIT-001.

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

El compilador, el plugin conversacional, Git y los materializadores tendrán specificationes propias. Se apoyan en el lenguaje, pero no definen su significado.

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
- Autoridad de ejemplos, notes y apéndices.
- Tratamiento normativo de cuestiones abiertas.

## 02. Terminología

Capítulo: [[02-terminologia]].

Glosario normativo de:

- Programa, módulo, archivo y path de MUD.
- Declaración, símbolo, nombre y ancla.
- `thing`, identidad y valor.
- Campo, relación y colección.
- Diccionario exacto, diccionario funcional, asociación, rama, selector y fallback.
- Participante, rol, vinculación y `given`.
- Regla consultable, reactiva y `always`.
- Acción, solicitud, raíz, onda y resolución.
- Test, aserción y diagnóstico.
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

Capítulo: [[05-texto-fuente]].

Define:

- Codificación.
- Archivos `.mud`.
- Derivación de paths de MUD desde rutas.
- Varias declaraciones por archivo.
- Independencia semántica respecto al orden de archivos.
- Terminadores de línea.

## 06. Estructura léxica

Capítulo: [[06-lexico]].

Define:

- Categorías de caracteres.
- Identificadores y sensibilidad a mayúsculas.
- Palabras reservadas.
- Literales numéricos, monetarios y porcentuales.
- Plantillas `Text` ordinarias y multilínea, interpolaciones ordinarias, escapes y acceso tipado `~anchor`.
- Comentarios `#`, `#...#` y `###...###`.
- Espacio en blanco.
- Tokens, trivia, spans y errores léxicos.
- Flujo completo y vista significativa.

La gramática léxica ejecutable vivirá en `gramatica/mud-lexico.ebnf`.

## 07. Gramática concreta

Capítulo: [[07-gramatica-concreta]].

Define la sintaxis completa de:

- Cabecera de declaraciones `using`, situada antes de cualquier declaración de primer nivel.
- Declaraciones.
- Tipos.
- Campos.
- Participantes.
- Valores `given`.
- Expresiones.
- Efectos.
- Bloques.
- Llamadas.
- Definiciones canónicas de `thing` y reglas, `start with` unificado por módulo y activaciones mediante `create Nombre`.
- Tests aislados con `start with` local, `then`, `after` y `otherwise`.
- Diagnóstico `otherwise` opcional después del cuerpo de reglas `always`; omitirlo produce un aviso y una razón predeterminada.
- Formatos numéricos dentro de interpolaciones `Text`.
- Cuantificadores e iteraciones.

La gramática completa ejecutable vive en `gramatica/mud.ebnf`. El parsing produce una CST sin pérdidas; este capítulo explica ambigüedades, precedencia, validación contextual y la frontera con el desazucarado, pero no repite toda la EBNF.

## 08. Sintaxis abstracta superficial

Capítulo: [[08-sintaxis-abstracta]].

Define las formas semánticamente relevantes después de la CST y de la validación sintáctica contextual:

- Raíces `MudFile` y `MudProject`.
- AST de declaraciones, tipos, dominios, expresiones y efectos.
- Normalización de cardinalidades, intervalos, bloques y literales contextuales.
- Distinción estructural entre las tres clases de regla.
- `ActionDecl` superficial con clase `PublicAction` o `Subaction`; las llamadas candidatas se resuelven después sin introducir ninguna clasificación elemental/compuesta.
- Nodo propio `TestDecl` y aserciones con diagnóstico opcional.
- Nodos propios para `look`, `message` y propiedades públicas.
- Procedencia mediante `SourceOrigin`.
- Ambigüedades que se conservan hasta resolución.

Artefactos mecánicos y de transformación: `sintaxis/`.

## 09. Paths, `using`, nombres y anclas

Capítulo: [[09-nombres-y-anclas]].

Define:

- Ámbitos.
- Resolución local y cualificada.
- Declaraciones `using` exactas y recursivas.
- Posición obligatoria de todos los `using` en la cabecera del fichero.
- Ambigüedad.
- Formación y unicidad de anclas públicas; las ramas funcionales de diccionarios funcionales usan claves locales y no reciben ancla pública.
- Categorías `thing::*`, `alias::*`, `family::*`, `magnitude::*`, `unit::*`, `rule::*`, `action::*`, `look::*`, `message::*`, `test::*` y `type::*`.
- Identidad ante movimientos de archivo.
- Migración de path y anclas.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$

## 10. Sistema de tipos

Archivo previsto: `10-sistema-de-tipos.md`

Alcance previsto:

- Tipos incorporados, nominales, estructurales, colecciones, diccionarios, intervalos, magnitudes y uniones.
- `Any`, descriptores first-class, tipos callable y tipos obtenidos estáticamente mediante `~type`.
- Subtyping, compatibilidad, narrowing, igualdad, orden, conversiones e inferencia.
- Tipado de resultados anónimos de `look` y payloads de `message`, incluido el join de invocaciones dinámicas.
- Interacción entre el tipo estático de un descriptor callable y la identidad nominal necesaria para vincular su firma.

Las cuestiones de varianza callable, especialización intermodular de aliases, join con mínimos comunes incomparables, binding tras borrado y la identidad de tipos anónimos permanecen delimitadas respectivamente por Q-063, Q-064, Q-065, Q-066 y Q-068.

Juicio principal:

$$
\Gamma;\Sigma \vdash e : \tau
$$

## 11. `Thing`, especialización e identidad

Archivo previsto: `11-things.md`

Alcance previsto:

- Identidad, actividad, destrucción de la materialización propia, rematerialización desde la definición canónica y estado independiente de `thing` concretas y abstractas.
- Especialización simple y múltiple, esquema heredable, predeterminados e inicializadores.
- Integración de `Thing` como raíz incorporada y de las reglas de igualdad/identidad nominal.
- Frontera modular de las `thing`: identidad/tipo visible frente a estado ordinario proyectado mediante operaciones públicas y límites de especialización entre módulos.
- Metadatos y reflexión propios de las `thing` sin confundirlos con campos de estado.

## 12. Aliases nominales y valores estructurales

Archivo previsto: `12-aliases.md`

Alcance previsto:

- Aliases nominales de representación y estructurales, construcción contextual y casting nominal.
- Especialización nominal simple y múltiple, herencia de representación o miembros, deduplicación por origen y conflictos de miembros independientes.
- Predeterminados heredados, valores inmutables, igualdad, orden y enumerabilidad cuando correspondan.
- Reconstrucción de aliases inmutables mediante write-back desde rutas asignables, sin introducir mutabilidad propia en sus valores.
- Frontera entre compatibilidad estructural y adquisición explícita de nominalidad.
- Reglas de especialización de aliases a través de módulos, cuyo alcance exacto permanece abierto en Q-064.

## 13. Familias cerradas de valores

Archivo previsto: `13-familias-cerradas.md`

Alcance previsto:

- Declaración, miembros, nominalidad, orden y enumeración de `family`.
- Esquema uniforme de datos asociados, predeterminados y cálculos por miembro.
- Igualdad, orden, reflexión y ausencia de ciclo de vida runtime de sus valores.

## 14. Campos, mutabilidad y capacidades

Archivo previsto: `14-campos-y-mutabilidad.md`

Alcance previsto:

- Campos almacenados y calculados, predeterminados, inicializadores y vistas derivadas.
- Mutabilidad exterior, capacidad interior `[mut]` y su composición sin mutabilidad profunda implícita.
- Capacidad de participantes y accesibilidad de escrituras.
- Metadatos postfix como información separada del estado ordinario y de solo lectura durante ejecución.

## 15. Cardinalidades y colecciones

Archivo previsto: `15-colecciones.md`

Alcance previsto:

- Cardinalidades, `empty`, multiplicidad, unicidad y orden.
- Membresía, álgebra de colecciones, indexación, selección y `take`.
- Inferencia y conservación de cardinalidad, dominio, orden y capacidades.
- Instantáneas y semántica observable de iteración sobre colecciones.

## 16. Diccionarios

Archivo previsto: `16-diccionarios.md`

Alcance previsto:

- Diccionarios exactos y funcionales, sus tipos, cardinalidades y consultas.
- Asociaciones, claves, iteración, orden y operaciones algebraicas.
- Indexación dentro de rutas asignables, write-back parcial sobre valores asociados y tratamiento de claves ausentes sin confundir actualización parcial con inserción completa.
- Modos de selección de ramas, fallback, dependencias, recursión y terminación de diccionarios funcionales.

## 17. Dominios e intervalos

Archivo previsto: `17-dominios-e-intervalos.md`

Alcance previsto:

- Dominios declarados y calculados, pertenencia, normalización, finitud y enumerabilidad.
- Intervalos lineales, discontinuos, cíclicos y dependientes de magnitudes.
- Materialización explícita de dominios enumerables mediante `all D` cuando una operación debe producir una colección.
- Diferencia entre consumir un dominio, materializar su enumeración y producir una colección filtrada, sin conversión implícita de esta última a `Domain`.

## 18. Magnitudes, unidades y puntos

Archivo previsto: `18-magnitudes.md`

Alcance previsto:

- Magnitudes base, derivadas y de punto, sus representaciones y dominios.
- Unidades, prefijos, equivalencias, normalización y aritmética dimensional.
- Coordenadas, ciclos, presentación, formatos y extracción de componentes.
- Magnitudes temporales y las construcciones de calendario/localización que finalmente pertenezcan al perfil MUD 1.0.

## 19. Expresiones

Archivo previsto: `19-expresiones.md`

Alcance previsto:

- Literales, operadores, llamadas, acceso, comparación, conversión y construcción contextual.
- Resolución y elaboración de receptores, argumentos y valores callable.
- `old`, `allowed`, `eventually`, selección, `take` y materialización `all D` en sus contextos de expresión.
- Pureza, narrowing, propagación de tipos esperados y fallos de evaluación.

## 20. Cuantificadores, agregaciones e iteración

Archivo previsto: `20-cuantificadores-e-iteracion.md`

Alcance previsto:

- Cuantificadores y agregadores sobre fuentes finitas enumerables.
- `for each`, bindings de iteración, orden, filtros, pasos e instantáneas de pertenencia.
- Consumo directo de dominios finitos cuando no se produce una colección y requisitos de terminación de cada recorrido.

## 21. Reglas booleanas

Archivo previsto: `21-reglas-booleanas.md`

Alcance previsto:

- Firmas puras con participantes `for` explícitamente nombrados y valores `given` de solo lectura.
- Vinculación de receptores y argumentos, dominios, predeterminados y capacidades admitidas por una consulta pura.
- Evaluación booleana, dependencias, memorización y tratamiento de declaraciones no efectivas.
- Integración con valores callable de tipo regla booleana.

## 22. Reglas reactivas

Archivo previsto: `22-reglas-reactivas.md`

Alcance previsto:

- Bindings `on` conjuntos, incluidas fuentes relacionadas finitas enumerables y refinamientos nominales.
- Activadores `when`, `changes`, `old`, guardas `if`, memoria reactiva y consecuencias `then`.
- Aparición, desaparición e identidad temporal de bindings.
- Uso de una regla reactiva disparada como fuente causal para otros triggers.

## 23. Reglas `always`

Archivo previsto: `23-reglas-always.md`

Alcance previsto:

- Bindings `on`, condición pura, puntos de comprobación y diagnósticos.
- Dependencias, suspensión y efecto de una infracción sobre la resolución.
- Uso de la evaluación de una `always` como fuente causal de trigger, separado de que su condición resulte verdadera o falsa.

## 24. Frontera pública: `action`, `look` y `message`

Archivo previsto: `24-frontera-publica.md`

Alcance previsto:

- Contratos visibles entre módulos y hacia el host para `action`, `look` y `message`; `test` solo cruza módulos en contexto de pruebas.
- Autorización modular mediante `uses`, cierre transitivo de los tipos necesarios para comprender un contrato y reflexión cruzada segura sin filtrado silencioso.
- API host centrada en la identidad de las operaciones públicas, no en un participante elegido como propietario.
- Firmas `for`/`given`, capacidad exterior de `action` frente a `subaction`, valores callable y vinculación en el punto de invocación.
- `look` como consulta pura con vista coherente del llamador y resultado anónimo único.
- `message` como ocurrencia causal, bindings `on`, payload público y proyecciones causal interna y estable exterior.
- Separación de bindings y payload, multiplicidad y orden de entrega, así como rollback de salidas exteriores.

El binding nominal de descriptores callable suficientemente borrados y la proyección exterior de un `message` cuyos participantes dejan de existir permanecen abiertos en Q-066 y Q-067.

## 25. Efectos

Archivo previsto: `25-efectos.md`

Alcance previsto:

- Asignaciones, actualizaciones, operaciones de colección, `create`, `destroy` y modificaciones estructurales permitidas.
- Llamadas effectful y recorridos dentro de un `then` unificado.
- Lecturas, escrituras, deltas, conflictos y composición de efectos.
- Elaboración de rutas asignables reconstruibles y propagación de write-back a través de valores inmutables hasta su almacenamiento raíz.
- Interacción entre efectos directos y llamadas internas que comparten una misma resolución causal.

## 26. Estado y evaluación de expresiones

Archivo previsto: `26-evaluacion.md`

Alcance previsto:

- Entornos, vistas de lectura, store y evaluación determinista de expresiones.
- Evaluación de campos calculados, consultas parciales, tipos esperados y fallos.
- Vistas coherentes heredadas por `look`, incluido el delta privado visible en el punto de llamada.
- Evaluación de callables y binding efectivo una vez resuelta su firma.

## 27. Solicitud y resultado de acciones

Archivo previsto: `27-solicitud-de-acciones.md`

Alcance previsto:

- Solicitud exterior, vinculación y validación inicial de una `action` raíz.
- Resultados `accepted`, `rejected` y `failed`, diagnósticos, estado visible y rollback.
- Relación entre validación de firma, guardas, estabilización, restricciones finales y publicación exterior.

## 28. Semántica de la raíz

Archivo previsto: `28-raiz.md`

Alcance previsto:

- Resolución causal raíz, deltas privados y secuencialidad textual dentro de cada `then`.
- Integración de llamadas internas sin abrir transacciones independientes.
- Consolidación, normalización y conflictos entre contribuciones concurrentes.
- Estado observado por cada fase de una resolución.

## 29. Semántica causal por ondas

Archivo previsto: `29-ondas.md`

Alcance previsto:

- Instantáneas, bindings activos, activadores y paso entre ondas.
- Matches causales con testigos, multiplicidad y composición mediante conjunción/disyunción.
- Ocurrencias de `message` y disparos de reglas como consecuencias disponibles para ondas posteriores.
- Combinación de efectos, estabilización y traza causal.
- Distinción entre orden causal y cualquier orden técnico reproducible dentro de una onda.

## 30. Restricciones, `after` y `old`

Archivo previsto: `30-restricciones-finales.md`

Alcance previsto:

- Comprobaciones de dominios, cardinalidades, reglas `always` y demás invariantes sobre estados tentativos.
- `after` de acciones/subacciones ejecutadas dentro de una resolución y su evaluación sobre el estado estable tentativo final.
- Semántica contextual de `old`, incluida la diferencia entre acciones, tests y reglas reactivas.
- Rechazo/fallo final y restauración del estado anterior cuando corresponda.

## 31. Conflictos, ciclos y estabilización

Archivo previsto: `31-conflictos-y-estabilizacion.md`

Alcance previsto:

- Compatibilidad y conflicto de efectos, activaciones y otras consecuencias concurrentes.
- Ciclos ejecutables, oscilaciones y detección de no estabilización.
- Ciclos puramente causales de mensajes/disparos que pueden mantener consecuencias pendientes aun sin cambio de estado.
- Condición semántica de estabilización y separación respecto de límites técnicos de implementación.

## 32. Creación, destrucción e identidad runtime

Archivo previsto: `32-ciclo-de-vida-runtime.md`

Alcance previsto:

- Actividad, materialización, destrucción de la materialización propia y rematerialización desde la definición canónica.
- Contribuciones `start with` de módulos, materialización conjunta e inicialización de primera activación.
- Almacenamiento latente de estado ajeno suspendido, proyección efectiva, suspensión por dependencias y restauración.
- Aparición y desaparición de bindings dependientes de actividad.

## 33. Aleatoriedad

Archivo previsto: `33-aleatoriedad.md`

Alcance previsto:

- Valores y puntos aleatorios, semillas, subsemillas y reproducibilidad.
- Cachés por instantánea, azar en expresiones/efectos y relación con rollback.
- Condiciones bajo las que una operación aparentemente aleatoria se simplifica a una elección determinista.

---

# Parte IV — Análisis semánticos avanzados

## 34. Grafo semántico

Archivo previsto: `34-grafo-semantico.md`

Alcance previsto:

- Relaciones semánticas posteriores a resolución nominal que dependan de tipos, dominios, efectos o elaboración.
- Lecturas, escrituras, dependencias, patrones de binding y dependencias estocásticas.
- Criterios de reconstrucción desde el programa y relación con el HIR nominal, sin convertir este último en un grafo semántico anticipado.

## 35. Consulta especulativa `allowed`

Archivo previsto: `35-allowed.md`

Alcance previsto:

- Construcción y descarte del mundo especulativo.
- Conversión de resultados a `Bool`, propagación de fallos y dependencia respecto de acciones consultadas.
- Condiciones de aciclicidad/admisibilidad y reproducibilidad del azar.

## 36. Alcanzabilidad `eventually`

Archivo previsto: `36-eventually.md`

Alcance previsto:

- Sistema de transición explorado, estado objetivo y secuencias de acciones permitidas.
- Semántica del azar y criterios de equivalencia/canonicalización de estados.
- Estrategias de búsqueda solo en la medida en que formen parte del significado normativo.

## 37. Finitud, enumerabilidad y estado relevante

Archivo previsto: `37-finitud-y-enumerabilidad.md`

Alcance previsto:

- Finitud y enumeración canónica de dominios y fuentes.
- Perfiles de mundos finitos, estado relevante y canonicalización de estados.
- Condiciones suficientes para análisis exhaustivos y para las construcciones que exigen enumerabilidad.

## 38. Terminación y decidibilidad

Archivo previsto: `38-terminacion.md`

Alcance previsto:

- Terminación de iteraciones, resoluciones y componentes recursivos.
- Análisis conservadores y frontera entre rechazo estático, fallo runtime e indecidibilidad.
- Propiedades decidibles o semidecidibles de las construcciones avanzadas.

## 39. Propiedades metateóricas

Archivo previsto: `39-propiedades.md`

Alcance previsto:

- Hipótesis y demostraciones sobre resolución, tipos, progreso, determinismo, reproducibilidad y atomicidad.
- Independencia de órdenes sin significado semántico y corrección de análisis especulativos.
- Contraejemplos y límites explícitos cuando una propiedad no sea válida para todo MUD.

---

# Parte V — Conformidad y apéndices

## 40. Diagnósticos

Archivo previsto: `40-diagnosticos.md`

Alcance previsto:

- Categorías, códigos, localizaciones y anclas relacionadas.
- Diagnósticos obligatorios frente a libertad de redacción.
- Recuperación tras errores y relación entre diagnósticos estáticos y dinámicos.

## 41. Representación semántica posterior

Archivo previsto: `41-ir.md`

Alcance previsto:

- Contrato entre las fases de tipado/elaboración y los consumidores posteriores cuando esas fases estén suficientemente desarrolladas.
- Información semántica que deba preservarse o pueda reconstruirse, procedencia y criterios de versionado si se adopta una representación serializable.
- Relación con AST superficial y HIR nominal sin duplicar ni degradar sus responsabilidades.

No se presupone actualmente un esquema ASDL/JSON, nombres concretos de nodos o aristas, una versión de esquema ni una política de almacenamiento frente a reconstrucción. Esos detalles se fijarán solo cuando las superficies de tipado y elaboración permitan justificarlos.

## 42. Conformidad de implementaciones

Archivo previsto: `42-conformidad.md`

Alcance previsto:

- Perfiles de implementación y requisitos de cada uno.
- Determinismo, declaración de versión, características opcionales y materialización conforme.
- Relación entre conformidad del frontend, runtime, análisis y tooling normativo.

## 43. Tests declarativos

Archivo previsto: `43-tests-declarativos.md`

Alcance previsto:

- Declaraciones `test`, mundo fresco y aislado, ejecución y descarte.
- Cierre transitivo estático de tests alcanzables y unión de **sus propias** contribuciones `start with`; la activación ordinaria de módulos no forma parte del mundo inicial del test.
- Materialización/estabilización previas, `then`, `after`, `old`, diagnósticos y resultados del ejecutor.
- Visibilidad de tests entre módulos exclusivamente en contexto de pruebas.

## 44. Suite de conformidad

Archivo previsto: `44-suite-de-conformidad.md`

Alcance previsto:

- Casos válidos e inválidos, diagnósticos y regresiones normativas.
- Salidas mecánicas normativas vigentes que corresponda comparar en cada fase.
- Transiciones, trazas y propiedades observables necesarias para contrastar implementaciones.

El corpus vivirá en:

```text
conformidad/
├── validos/
├── invalidos/
├── ejecucion/
├── diagnosticos/
└── propiedades/
```

Los tests declarativos escritos por una persona usuaria forman parte de MUD, pero no sustituyen esta suite: la suite de conformidad comprueba implementaciones completas del lenguaje.

## 45. Gramática consolidada

Archivo previsto: `45-gramatica-consolidada.md`

Apéndice normativo generado o verificado contra `gramatica/mud.ebnf`.

## 46. Catálogo de palabras reservadas

Archivo previsto: `46-palabras-reservadas.md`

Lista normativa y clasificación como palabra reservada o contextual, derivada de la gramática léxica vigente.

## 47. Ejemplos integrales

Archivo previsto: `47-ejemplos-integrales.md`

Ejemplos informativos construidos únicamente con reglas ya especificadas. No introducen comportamiento nuevo.

## 48. Compatibilidad y migraciones

Archivo previsto: `48-compatibilidad.md`

Alcance previsto:

- Cambios compatibles e incompatibles del lenguaje.
- Evolución de anclas y migración de programas.
- Compatibilidad de artefactos normativos serializados cuando exista un contrato de serialización aplicable.
- Obsolescencia de sintaxis y declaraciones de versión.

## 49. Índice de reglas normativas

Archivo previsto: `49-indice-normativo.md`

Índice generado de requisitos con identificadores estables, por ejemplo:

```text
MUD-LEX-001
MUD-SYN-014
MUD-NAME-008
MUD-TYPE-023
MUD-ACTION-011
MUD-WAVE-006
MUD-REACH-004
MUD-TEST-003
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

## Artefactos sintácticos verificables

El subdirectorio `sintaxis/` contiene el contrato de CST, el ASDL superficial, la transformación, la cobertura producción por producción y su validador editorial.

```text
sintaxis/
├── cst-sin-perdidas.md
├── mud-syntax-kinds.yaml
├── mud-surface-ast.asdl
├── cst-a-ast-superficial.md
├── cobertura-sintactica.yaml
├── validate_syntax_model.py
└── casos/
```

## Dependencias principales

```text
notación
   │
   ├──► modelo matemático
   │       │
   │       ├──► tipos y valores
   │       └──► estado y efectos
   │
léxico ─► CST sin pérdidas ─► AST superficial
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
→ action
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
6. La gramática, la cobertura CST/AST, el HIR nominal y cualquier otra representación mecánica normativa vigente sean verificables automáticamente.
7. Exista una suite de conformidad representativa.
8. Las propiedades prometidas estén demostradas o delimitadas mediante hipótesis explícitas.
9. Los ejemplos integrales no dependan de comportamiento implícito.
10. Una implementación pueda declarar de forma objetiva su grado de conformidad.
