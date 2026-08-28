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
questions:
  - Q-063
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

Itinerario didáctico: [[aprendizaje/README|Aprendizaje de formalización de MUD]].

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

- Programa, módulo, archivo y path de MUD.
- Declaración, símbolo, nombre y ancla.
- `thing`, identidad y valor.
- Campo, relación y colección.
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
- Formación y unicidad de anclas públicas; las ramas funcionales de diccionarios decisionales usan claves locales y no reciben ancla pública.
- Categorías `thing::*`, `rule::*`, `action::*` y `test::*`.
- Identidad ante movimientos de archivo.
- Migración de path y anclas.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$



## 10. Sistema de tipos

Archivo previsto: `10-sistema-de-tipos.md`

Define:

- `Text`, `Char` y `Bool` como tipos básicos no numéricos.
- Comillas dobles comunes para `Text` y `Char`, con preferencia por `Text` y elaboración contextual de un único escalar como `Char`.
- `"\u{0}"` (`U+0000`) como valor predeterminado contextual de `Char`.
- `Nat`, `Int`, `Num`, `Rum` y `Money` como representaciones numéricas básicas, no magnitudes.
- Saturación de la resta pura de `Nat` frente a deltas aditivos firmados.
- `Num` como racional exacto y `Rum` como IEEE 754 `binary64` explícito.
- Tipos de `thing`.
- Tipos nominales de alias.
- Familias cerradas.
- Colecciones, productos estructurales, diccionarios exactos y diccionarios decisionales.
- Intervalos.
- Magnitudes.
- Tipos callable de `action`, regla booleana y `look`, descriptores first-class y tipos obtenidos estáticamente mediante `~type`, con la varianza formal pendiente de Q-063.
- Pertenencia nominal mediante `is`, identidad nominal exacta mediante `iis` y narrowing positivo y negativo.
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
- `Thing` incorporada, abstracta y superior a toda `thing`.
- `Thing` declaradas y creadas durante la ejecución.
- Especialización simple y múltiple.
- Cabeceras de especialización con `as` y consultas con `is`.
- Sustituibilidad.
- Fusión de campos homónimos.
- Valores predeterminados heredados.
- Igualdad de identidad.
- Canonicalización de identidades de `thing`.
- Metadatos tipados `~name`, `~path`, `~anchor` y `~file`, separados de campos y de la identidad nominal.

## 12. Aliases nominales y valores estructurales

Archivo previsto: `12-aliases.md`

Define:

- Definición de tipo mediante `:=` y bloque estructural.
- Componentes obligatorios, ordenados, con dominio y sin `mut`.
- Nominalidad de todos los aliases.
- Valores inmutables y ausencia de identidad runtime.
- Prohibición de `create`, `destroy`, abstracción y especialización.
- Literales contextuales posicionales y nombrados.
- Predeterminados de componentes y construcción parcial exclusivamente nombrada.
- Casting nominal mediante `to` y compatibilidad de forma normalizada.
- Igualdad por alias y contenido.
- Orden lexicográfico cuando la representación está ordenada.
- Claves compuestas y azúcar de acceso.
- Finitud, enumerabilidad y producto cartesiano lexicográfico.

## 13. Familias cerradas de valores

Archivo previsto: `13-familias-cerradas.md`

Define:

- `family`.
- `ordered` como palabra reservada delante de `family`.
- Miembros como valores nominales sin identidad ni ciclo de vida runtime.
- Anclas estáticas `family::*`.
- Esquema uniforme de datos inmutables, almacenados o calculados por miembro, declarado directamente en la familia.
- Tipo opcional y dependencias acíclicas para los datos calculados.
- Valores de miembro explícitos o completados mediante predeterminados.
- Prohibición de especialización y herencia entre familias.
- Enumeración finita.


## 14. Campos, mutabilidad y capacidades

Archivo previsto: `14-campos-y-mutabilidad.md`

Define:

- Campos almacenados y calculados.
- Metadatos postfix separados de los campos ordinarios; todo acceso `~` es de solo lectura durante la ejecución y los metadatos configurables se modifican mediante edición del modelo.
- Expresiones estáticas cerradas para valores almacenados y predeterminados.
- Anotación opcional e inferencia unívoca del tipo de campos calculados.
- `=` frente a `:=`.
- Mutabilidad exterior.
- Capacidad interior `[mut]`.
- Ortogonalidad de ambos permisos también para cardinalidad `[1]`.
- Posición `mut nombre: Tipo`; rechazo de `nombre: mut Tipo`.
- Campos derivados como vistas de colección sin mutabilidad exterior.
- Mutabilidad exterior e interior de participantes `for`, incluidos receptores-lugar.
- Accesibilidad de escrituras.
- Ausencia de mutabilidad profunda implícita.


## 15. Cardinalidades y colecciones

Archivo previsto: `15-colecciones.md`

Define:

- Cardinalidades como intervalos de naturales.
- Ausencia mediante `empty`.
- Multiplicidad y `unique`.
- Membresía estricta de `thing`, con exclusión incondicional del ancla exacta del tipo.
- Colecciones ordenadas y no ordenadas.
- Orden natural, de inserción y semántico; orden Unicode fijo para `Char`.
- `ordered by` sobre una ruta estable con resultado totalmente ordenado y empates por orden de inserción.
- Álgebra de multiconjuntos mediante unión, intersección y diferencia `--`; diferencia simétrica `^` reservada a colecciones `unique`.
- Aritmética elevada cuando al menos un operando es opcional o unitario, con `empty` absorbente.
- Filtrado puro sin proyección ni aplanamiento, `take` ordenado o reproduciblemente aleatorio e indexación posicional exclusiva de colecciones ordenadas.
- Inferencia de cardinalidad y dominio y propagación de `unique`, `ordered` y capacidad interior `mut`.
- Igualdad de colecciones.
- Instantáneas de iteración.


## 16. Diccionarios

Archivo previsto: `16-diccionarios.md`

Define:

- Tipos completos de entrada y salida, incluidos productos y diccionarios anidados.
- Cardinalidad.
- Claves compuestas.
- Consulta exacta ausente mediante `empty`, asociaciones operativas y escritura de claves.
- Materialización de entradas.
- Iteración por claves y entradas.
- Orden canónico.
- Operaciones totales y aritmética conjuntista de exactos por dominio de claves, con precedencia izquierda, orden, `unique` e inferencia cardinal.
- Diccionarios funcionales `-->`, modos `FirstMatch` y `AllMatches`, fallback, pureza, dependencias, terminación y aritmética extensional punto a punto.


## 17. Dominios e intervalos

Archivo previsto: `17-dominios-e-intervalos.md`

Define:

- Declaraciones `in`.
- Dominios de campos, aliases y `given`.
- Dominios calculados.
- Pertenencia.
- Intervalos abiertos, cerrados, vacíos y discontinuos.
- Intervalos de magnitud con unidades locales o una unidad común exterior.
- Límites efectivos laterales mediante `*` y azúcar `[*]`.
- Normalización.
- Normalización de extremos lineales invertidos a `empty`.
- Finitud y enumerabilidad.
- Pasos de iteración.
- Dominios dinámicos.
- Dominios cíclicos `[a..b) cycle` exclusivos de magnitudes de punto.
- Intervalos `Rum` admitidos como dominios, pero no como fuentes enumerables.


## 18. Magnitudes, unidades y puntos

Archivo previsto: `18-magnitudes.md`

Define:

- Magnitudes no derivadas, derivadas y de punto.
- Magnitudes base con unidad raíz o deliberadamente sin unidades, conservando en ambos casos su dimensión nominal.
- Representaciones numéricas explícitas e inferidas.
- Magnitudes basadas en `Rum` y omisión contextual del prefijo `r` en cantidades con unidad.
- Unidades raíz y alternativas con identificador `lowerCamel` y equivalencias mediante `:=`.
- Prefijos.
- Normalización.
- Aritmética dimensional.
- Inferencia de unidades canónicas derivadas y combinaciones automáticas.
- Dominios de punto opcionales: completos, lineales o cíclicos.
- Presentación `in unit` de coordenadas completas y extracción `unit from container in point`.
- Representación textual raíz, abreviaturas y formatos de punto.
- Unidades nominales derivadas opcionales.
- Unidades locales y compartidas en expresiones de intervalo.
- Declaraciones `point over`, ciclos y formatos.
- Magnitudes temporales.
- Calendarios y localización.


## 19. Expresiones

Archivo previsto: `19-expresiones.md`

Define:

- Literales racionales exactos, literales `Rum` prefijados con `r` y acceso.
- Llamadas a reglas.
- Receptores multiparte.
- Operadores, incluidos `not in`, `iis`, `iis not` y la aritmética de diccionarios.
- Precedencia y asociatividad, incluidas las flechas exteriores de tipo.
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
- Prohibición de enumerar intervalos `Rum`.
- Enumeración de aliases estructurales como productos cartesianos lexicográficos.


## 21. Reglas booleanas

Archivo previsto: `21-reglas-booleanas.md`

Define:

- Roles `for` de cualquier tipo declarado, individuales o colectivos.
- Vinculación por identidad, valor o lugar y nombre obligatorio para roles colectivos o exteriormente mutables.
- Ausencia de mutabilidad exterior por pureza.
- Valores `given` inmutables, con predeterminados estáticos y vinculación posicional o nominal.
- Receptor único y multiparte.
- Sugerencia de orden de declaración para receptores y argumentos nombrados desordenados.
- Pureza.
- Resultado booleano.
- Dominios fuera de rango.
- Dependencias y memorización.
- Borrado estructural cuando la declaración no sea efectiva.


## 22. Reglas reactivas

Archivo previsto: `22-reglas-reactivas.md`

Define:

- Cada rol `on` vincula un único valor por vinculación: la forma directa usa el universo implícito de `thing` concretas activas y la forma relacionada obtiene valores de una fuente finita enumerable.
- Participantes relacionados mediante `in`, con refinamiento nominal opcional, resolución conjunta, referencias adelantadas y ciclos finitos.
- `when`.
- Sufijo temporal `changes` y su precedencia.
- Composición de activadores mediante `and` y `or`.
- Transición `false → true`, pulsos sin estado y cambios netos entre instantáneas.
- `old` sobre la onda anterior dentro de `when` e `if`.
- `if`.
- `then`.
- Estado anterior virtual en `start with` y línea base sin disparo para vinculaciones posteriores.
- Creación y eliminación de vinculaciones.


## 23. Reglas `always`

Archivo previsto: `23-reglas-always.md`

Define:

- Vinculaciones `on`.
- Pureza.
- Estados en que deben comprobarse.
- Incumplimiento y resultado de resolución.
- Diagnóstico `otherwise` exterior al cuerpo y visibilidad de sus locales.
- Dependencias, incluidas lecturas de metadatos y ramas decisionales.


## 24. Frontera pública: `action`, `look` y `message`

Archivo previsto: `24-frontera-publica.md`

Define:

- Roles `for` de cualquier tipo, individuales o colectivos.
- Valores `given` inmutables, predeterminados estáticos y omisiones posicionales o nominales.
- `if`, `then` y `after`.
- Vinculaciones locales `:=` secuenciales y sin referencias adelantadas dentro de `then`.
- Acciones elementales.
- Acciones compuestas.
- Vinculación posicional y nombrada.
- Receptores-lugar para roles con mutabilidad exterior.
- Aciclicidad de llamadas.
- Acciones como API externa de escritura.
- Exclusión de los tests de la API pública.
- Posibles valores de retorno.
- `look` como consulta pública pura de un estado estable.
- Participantes `for` sin `given`.
- `message` como evento detectado durante las ondas de una acción.
- Vinculaciones `on` conjuntas, refinamientos nominales, referencias adelantadas y ciclos relacionales finitos.
- Condición `when` y guarda `if` opcional.
- Propiedades públicas calculadas con tipo declarado opcionalmente o inferido y acciones auxiliares `subaction` fuera de la API raíz.
- Evaluación diferida de las propiedades del mensaje tras la estabilización.
- Multiplicidad, orden, deduplicación, rollback y entrega.


## 25. Efectos

Archivo previsto: `25-efectos.md`

Define:

- Asignaciones.
- Actualizaciones aritméticas.
- Deltas firmados para actualizaciones aditivas sobre `Nat`.
- Operaciones de colección.
- Adición y retirada dinámica de propiedades.
- `create`.
- `destroy`.
- Resolución de `create Nombre` a la definición canónica de una `thing` o regla.
- Efectos de bucles.
- Conjuntos de lectura y escritura.
- Compatibilidad y conflicto entre efectos.
- Consolidación determinista de deltas privados de distintos `then`.
- Suma de deltas antes de normalizar el tipo del destino.
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
- Propagación de `empty` en consultas parciales y fallo solo al infringir el contrato exterior.
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
- Objeto externo de resultado y `reason: Text` obligatorio para `rejected` y `failed`.
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
- Proyección no negativa de lecturas `Nat` sin recortar el delta privado.
- Normalización de efectos.
- Conflictos de raíz.


## 29. Semántica causal por ondas

Archivo previsto: `29-ondas.md`

Define:

- Instantánea de una onda.
- Vinculaciones activas.
- Evaluación de activadores temporales.
- Cálculo simultáneo de consecuencias.
- Combinación de efectos.
- Normalización de valores después de consolidar cada lote causal.
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
- Diferencia entre el `after` booleano de una acción y la secuencia de aserciones de un test.
- Estado observado por `old` dentro de un test.
- Rechazo final.
- Restauración completa.

## 31. Conflictos, ciclos y estabilización

Archivo previsto: `31-conflictos-y-estabilizacion.md`

Define:

- Relación de compatibilidad de efectos.
- Matriz normativa de conflictos.
- Consolidación idempotente de activaciones concurrentes de una misma definición canónica.
- Ciclos causales.
- Oscilaciones.
- Detección de repetición.
- Límites técnicos frente a significado semántico.
- Condición de estabilización.

## 32. Creación, destrucción e identidad runtime

Archivo previsto: `32-ciclo-de-vida-runtime.md`

Define:

- Definiciones canónicas estáticas de `thing` raíz, abstractas y con especialización múltiple.
- Conjuntos iniciales no ordenados y separados de `things` y `rules` declarados mediante `start with`.
- Activación y reactivación mediante `create Nombre`.
- Inicialización de la primera materialización.
- Distinción entre almacenamiento retenido y proyección efectiva.
- Suspensión por dependencias.
- Restauración sin reinicialización.
- `remove` destructivo frente a `destroy` reversible.
- Referencias y propiedades latentes.
- `thing` estáticas.
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
- Prueba estática de terminación para todo componente recursivo de diccionarios decisionales.
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

## 43. Tests declarativos

Archivo previsto: `43-tests-declarativos.md`

Define:

- Declaraciones `test` con ancla `test::*`.
- Mundo aislado y sustitución del `start with` global.
- Materialización y estabilización previas.
- Semántica de `then`.
- Vinculaciones locales inmutables y secuenciales mediante `nombre [: Tipo] := expresión`.
- Aserciones `after`.
- Diagnósticos `otherwise`.
- Resultados `passed`, `failed` y `error`.
- Descarte del mundo y de sus salidas.
- Ejecución por ancla o path de MUD.


## 44. Suite de conformidad

Archivo previsto: `44-suite-de-conformidad.md`

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


Los tests declarativos escritos por una persona usuaria forman parte de MUD, pero no sustituyen esta suite: la suite de conformidad comprueba implementaciones completas del lenguaje.

## 45. Gramática consolidada

Archivo previsto: `45-gramatica-consolidada.md`

Apéndice normativo generado o verificado contra `gramatica/mud.ebnf`.

## 46. Catálogo de palabras reservadas

Archivo previsto: `46-palabras-reservadas.md`

Lista normativa y clasificación como palabra reservada o contextual.

El catálogo se derivará de la gramática léxica vigente.

## 47. Ejemplos integrales

Archivo previsto: `47-ejemplos-integrales.md`

Ejemplos informativos construidos únicamente con reglas ya especificadas. No introducen comportamiento nuevo.

## 48. Compatibilidad y migraciones

Archivo previsto: `48-compatibilidad.md`

Define:

- Cambios compatibles e incompatibles.
- Evolución de anclas.
- Migración de programas.
- Migración del IR.
- Obsolescencia de sintaxis.

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
6. La gramática, la cobertura CST/AST y el esquema IR sean verificables automáticamente.
7. Exista una suite de conformidad representativa.
8. Las propiedades prometidas estén demostradas o delimitadas mediante hipótesis explícitas.
9. Los ejemplos integrales no dependan de comportamiento implícito.
10. Una implementación pueda declarar de forma objetiva su grado de conformidad.
