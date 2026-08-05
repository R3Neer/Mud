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
- Autoridad actual: los capítulos vigentes de este directorio y las decisiones vigentes enlazadas. El historial Git conserva la procedencia retirada, pero no tiene autoridad subsidiaria.
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
- Definiciones canónicas de `thing` y reglas, `start with` separado en `things` y `rules`, y activaciones mediante `create Nombre`.
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
- `ActionDecl` superficial con clase `PublicAction` o `Subaction`, sin clasificar todavía como elemental o compuesta.
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
- Formación y unicidad de anclas, incluidas anclas estables de ramas decisionales.
- Categorías `thing::*`, `rule::*`, `action::*` y `test::*`.
- Identidad ante movimientos de archivo.
- Migración de path y anclas.

Juicio principal:

$$
\Gamma \vdash n \rightsquigarrow a
$$

Base normativa migrada: [[notas/decisiones/ADR-035-organizacion-nombres-using-y-anclas|D-035]], [[notas/decisiones/ADR-065-cabecera-using-de-fichero|D-065]] y [[notas/decisiones/ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]].

Ampliación normativa: [[notas/decisiones/ADR-078-resolucion-nominal-anclas-y-grafo-inicial|D-078]].

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
- Subtipado mediante `is`.
- Inferencia y ampliación de representaciones en operaciones cuantitativas.
- Dos familias explícitas de `to`: conversión cuantitativa y casting nominal estructural.
- Redondeo global al más cercano con empates al par.
- Igualdad y orden por tipo.

Base normativa migrada para aritmética de `Nat`: [[notas/decisiones/ADR-040-semantica-numerica-basica-restante|D-040]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

Base normativa de literales textuales y `Char`: [[notas/decisiones/ADR-056-char-texto-y-orden-unicode|D-056]], [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]] y [[notas/decisiones/ADR-069-literales-char-con-comillas-dobles|D-069]].

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

Base normativa migrada: [[notas/decisiones/ADR-038-familias-cerradas-de-valores|D-038]].

## 14. Campos, mutabilidad y capacidades

Archivo previsto: `14-campos-y-mutabilidad.md`

Define:

- Campos almacenados y calculados.
- Metadatos postfix separados de los campos ordinarios y reglas de escritura de `~name`.
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

Bases normativas migradas: [[notas/decisiones/ADR-019-mutabilidad-ortogonal-de-coleccion-y-miembros|D-019]], [[notas/decisiones/ADR-037-campos-y-dominios-declarativos|D-037]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]].

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

Bases normativas migradas: [[notas/decisiones/ADR-026-membresia-estricta-y-cardinalidad-por-then|D-026]], [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]], [[notas/decisiones/ADR-064-orden-por-ruta-estable|D-064]], [[notas/decisiones/ADR-080-algebra-elevada-y-actualizaciones-de-coleccion|D-080]] y [[notas/decisiones/ADR-081-filtrado-take-e-indexacion-de-colecciones|D-081]].

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
- Operaciones totales.
- Diccionarios decisionales `-->`, modos `FirstMatch` y `AllMatches`, fallback, pureza, dependencias y terminación.

Bases normativas migradas: [[notas/decisiones/ADR-039-colecciones-y-diccionarios|D-039]] y [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].

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

Base normativa migrada: [[notas/decisiones/ADR-029-intervalos-estrellas-y-ciclos|D-029]], [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] y [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]].

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

Base normativa migrada: [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]] y [[notas/decisiones/ADR-083-magnitudes-base-sin-unidades|D-083]].

## 19. Expresiones

Archivo previsto: `19-expresiones.md`

Define:

- Literales racionales exactos, literales `Rum` prefijados con `r` y acceso.
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

Base normativa migrada: [[notas/decisiones/ADR-049-operadores-precedencia-e-intervalos-normalizados|D-049]] y [[notas/decisiones/ADR-059-intervalos-de-magnitud-y-extremos-invertidos|D-059]].

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

Base normativa migrada: [[notas/decisiones/ADR-047-cuantificadores-e-iteracion-finita|D-047]].

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

Bases normativas migradas: [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]] y [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].

## 22. Reglas reactivas

Archivo previsto: `22-reglas-reactivas.md`

Define:

- Vinculaciones `on` exclusivamente individuales.
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

Bases normativas migradas: [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]] y [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]].

## 23. Reglas `always`

Archivo previsto: `23-reglas-always.md`

Define:

- Vinculaciones `on`.
- Pureza.
- Estados en que deben comprobarse.
- Incumplimiento y resultado de resolución.
- Diagnóstico `otherwise` exterior al cuerpo y visibilidad de sus locales.
- Dependencias, incluidas lecturas de metadatos y ramas decisionales.

Bases normativas migradas: [[notas/decisiones/ADR-041-contratos-de-las-tres-clases-de-regla|D-041]], [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]] y [[notas/decisiones/ADR-079-diagnostico-exterior-de-reglas-always|D-079]].

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

Bases normativas migradas: [[notas/decisiones/ADR-042-acciones-raiz-y-resultados|D-042]], [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]], [[notas/decisiones/ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]].

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

Bases normativas migradas: [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]], [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]].

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

Base normativa migrada: [[notas/decisiones/ADR-046-algebra-y-conflictos-de-efectos|D-046]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

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

Base normativa migrada: [[notas/decisiones/ADR-045-resolucion-causal-vinculaciones-y-cola|D-045]], [[notas/decisiones/ADR-058-activadores-temporales-changes-y-old-reactivo|D-058]] y [[notas/decisiones/ADR-060-deltas-aditivos-y-normalizacion-de-natural|D-060]].

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

Base arquitectónica migrada: [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]].

## 35. Consulta especulativa `allowed`

Archivo previsto: `35-allowed.md`

Define:

- Mundo especulativo.
- Ejecución descartable.
- Conversión de resultados a booleano.
- Propagación de fallos.
- Aciclicidad del grafo de admisibilidad.
- Aleatoriedad reproducible.

Base normativa migrada: [[notas/decisiones/ADR-043-consulta-especulativa-allowed|D-043]].

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

Base normativa migrada: [[notas/decisiones/ADR-044-alcanzabilidad-eventually|D-044]].

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

Base normativa parcial: [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].

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

Base arquitectónica migrada: [[notas/decisiones/ADR-051-grafo-semantico-e-ir-reconstruibles|D-051]].

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

Bases normativas: [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] y [[notas/decisiones/ADR-066-valores-estaticos-y-vinculaciones-locales-en-then|D-066]].

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

Base arquitectónica migrada: [[notas/decisiones/ADR-052-pipeline-materializadores-y-conformidad|D-052]].

Los tests declarativos escritos por una persona usuaria forman parte de MUD, pero no sustituyen esta suite: la suite de conformidad comprueba implementaciones completas del lenguaje.

## 45. Gramática consolidada

Archivo previsto: `45-gramatica-consolidada.md`

Apéndice normativo generado o verificado contra `gramatica/mud.ebnf`.

## 46. Catálogo de palabras reservadas

Archivo previsto: `46-palabras-reservadas.md`

Lista normativa, clasificación como palabra reservada o contextual y versión de introducción o retirada.

Las reglas léxicas ya decididas pertenecen a [[notas/decisiones/ADR-050-comentarios-terminadores-y-separadores-numericos|D-050]], [[notas/decisiones/ADR-054-definiciones-canonicas-y-activacion-inicial|D-054]], [[notas/decisiones/ADR-055-tests-declarativos-y-diagnosticos-otherwise|D-055]] y [[notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco|D-068]]; el catálogo se derivará de la gramática.

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

## Cambios semánticos recientes

La especialización de aliases, los cuerpos vacíos omitibles de `thing`, los campos derivados de alias y las vistas derivadas con capacidad interior se fijan en [[notas/decisiones/ADR-084-especializacion-de-aliases-y-vistas-derivadas|D-084]].


## Integración transversal de D-085

[[notas/decisiones/ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]] modifica los contratos de los capítulos futuros 10 a 20, 24, 26, 32, 34 y 38:

- `Any` es el tipo superior no enumerable de todos los valores y no posee predeterminado universal.
- Los productos estructurales anónimos y las flechas `->`/`-->` forman tipos completos asociativos a la derecha.
- Los diccionarios exactos devuelven `empty` ante clave ausente; los decisionales distinguen `FirstMatch` y `AllMatches`, ramas puras, fallback, dependencias y terminación demostrable.
- La cardinalidad omitida de un campo almacenado inmutable con inicializador se infiere exactamente.
- `start with` separa contribuciones de `things` y `rules`.
- `subaction` queda fuera de la API raíz y comparte la atomicidad de la acción exterior.
- `~name`, `~path`, `~anchor`, `~file` y los metadatos de unidades sustituyen las excepciones `.name`, `name =` y `anchor{...}`.
- El grafo registra anclas de rama, lecturas de metadatos, llamadas decisionales y evidencia de terminación.
