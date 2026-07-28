---
title: MUD — Especificación inicial histórica
aliases:
  - Prompt maestro inicial de MUD
tags:
  - mud/referencia
  - mud/historico
status: retirado
normative: false
snapshot-date: 2026-07-27
original-sha256: 9E0CDB7626ADF2B525720B094BE3C33D296D06C7952302D68645F16F8E56A423
---

> [!danger] Referencia retirada — no normativa
> Este archivo conserva un estado temprano y temporal del diseño de MUD. **Su migración está terminada: no debe usarse para completar silencios, resolver dudas ni implementar el lenguaje vigente.** Solo se conserva para trazabilidad histórica.
>
> El texto situado bajo estos avisos se conserva deliberadamente sin reescribir para mantener la procedencia. Expresiones internas como «estado vigente», «contexto maestro» o «todas las decisiones [...] vigentes» pertenecen a la instantánea original y ya no tienen autoridad.

Autoridad actual, por orden:

1. Capítulos vigentes de [[especificacion/README|la especificación formal]].
2. Decisiones vigentes de [[notas/10-registro-de-decisiones|el registro de decisiones]] y sus ADR.
3. [[notas/08-preguntas-abiertas|Preguntas abiertas]], cuando una materia todavía no esté cerrada.
4. Este archivo no tiene autoridad subsidiaria: la matriz de migración demuestra el destino de cada sección.

La copia original previa a estas anotaciones tenía 3652 líneas y SHA-256 `9E0CDB7626ADF2B525720B094BE3C33D296D06C7952302D68645F16F8E56A423`. La auditoría detallada está en [[notas/13-auditoria-de-cobertura-y-divergencias]].

## Índice de contenido desactualizado

| Secciones históricas | Estado actual |
| --- | --- |
| 3, 5 y 74 | El catálogo y el léxico cambian: `thing` sustituye a `construct`; aparecen `look` y `message`; `as` declara especialización. Véanse D-025 y D-027. |
| 6–8, 31–33 y 36 | Se intercambian `on` y `for`: `on` corresponde a observadores automáticos; `for`, a acciones, reglas booleanas y `look`. Véase D-025. |
| 9, 10, 63–65 y ejemplos relacionados | El modelo ya no separa clases e instancias; las `thing` forman un único dominio. La especialización se declara con `as` y se consulta con `is`. Véanse D-014–D-016 y D-025. |
| 3.5, 11 y usos relacionados | D-031–D-033 redefinen los aliases como tipos nominales inmutables y estáticos: usan `:=` o bloque, no admiten `create`/`destroy`, construyen literales por contexto, usan casting nominal `to` y enumeran productos finitos lexicográficamente. |
| 14–15, 20–28, 30, 59 y ejemplos cuantitativos | El sistema cuantitativo ha sido sustituido: `Bool` reemplaza `Boolean`; `Percentage` deja de ser básico; `Number` es racional exacto; aparece `Rumber` `binary64`; las magnitudes, unidades, intervalos, ciclos, literales, `in` y `to` se rigen por D-028–D-030 y D-034. |
| 16 | La mutabilidad exterior y la capacidad interior son ortogonales incluso para `[1]`; no existe una excepción singular. Véase D-019. |
| 17, 30, 48, 56 y 59 | No existe `[reflexive]`; una colección de tipo `T` exige $c\neq T\land c\ \mathsf{is}\ T$. La cardinalidad final se demuestra por `then` y consolidación. Véase D-026. |
| 32–33, 42, 50, 55 y 56 | `create` y `destroy` se generalizan y la destrucción es suspensión lógica reversible; `remove` sí elimina propiedades y cargas. Véanse D-021, D-023 y D-024. |
| 34 y reglas booleanas inactivas | Una llamada a una regla booleana inactiva se borra estructuralmente; no adopta simplemente un booleano fijo. Véase D-022. |
| 45–49 | La consolidación usa deltas privados secuenciales por `then` y reglas deterministas entre bloques. Véanse D-023 y D-026. |
| 62 | La frontera pública actual es `action` para entrada, `look` para consulta y `message` para eventos diferidos. Véase D-027. |
| 64, 72 y 73 | El IR, los tests y el soporte de editor son bocetos, no contratos de conformidad actuales. |
| 75 | El ejemplo integral usa sintaxis y semántica retiradas; no es un programa MUD vigente. |
| 76–78 | Las listas de decisiones, preguntas e instrucciones finales quedaron congeladas en esta instantánea y han sido sustituidas por los documentos versionados del repositorio. |

> [!tip] Cómo leer esta referencia
> Los bloques sin aviso inline pueden seguir conteniendo requisitos útiles, pero deben migrarse y revisarse antes de adquirir autoridad. Los avisos inline indican contradicciones conocidas; la ausencia de aviso no equivale a aprobación normativa.

## MUD — Prompt maestro de especificación, diseño e implementación
Este documento define el estado vigente de MUD y del sistema de herramientas que debe construirse alrededor del lenguaje.
Debe utilizarse como contexto maestro para:
* Diseñar el lenguaje.
* Implementar su tooling.
* Desarrollar el plugin para Codex.
* Construir progresivamente el compilador.
* Construir el runtime causal.
* Materializar modelos MUD en implementaciones ejecutables.
* Mantener la trazabilidad semántica del proyecto.
Todas las decisiones expresadas aquí se consideran vigentes.
Cuando una cuestión aparezca como abierta:
* Debe registrarse en la agenda de especificación.
* No debe resolverse silenciosamente durante la implementación.
* No debe inventarse una solución provisional sin marcarla como tal.
* Toda decisión posterior debe conservar procedencia y trazabilidad.
 
⸻
 
## 1. Objetivo de MUD
MUD es un lenguaje específico de dominio declarativo diseñado para describir mundos mediante:
* Cosas y conceptos.
* Categorías y especializaciones.
* Valores estructurales.
* Propiedades y relaciones.
* Familias cerradas de valores cualitativos.
* Cantidades, unidades y conversiones.
* Dominios permitidos para valores.
* Condiciones booleanas consultables.
* Acciones que pueden solicitarse desde el exterior.
* Reglas que reaccionan automáticamente a los cambios.
* Restricciones que deben cumplirse siempre.
* Consecuencias causales resueltas por ondas.
* Consultas especulativas sobre acciones.
* Consultas restringidas de alcanzabilidad futura.
Su caso de uso inicial es la lógica de dominio de videojuegos y simulaciones, especialmente mundos con muchas reglas interrelacionadas.
Sin embargo, el lenguaje no debe contener conceptos específicos de:
* Un género.
* Un motor.
* Una plataforma.
* Una interfaz.
* Una representación gráfica.
* Una tecnología de implementación.
La idea mental es:
En este mundo existen estas cosas.
Estas cosas tienen estas propiedades y relaciones.
Algunos valores están formados por varias partes.
Algunas propiedades solo pueden adoptar ciertos valores.
Algunas cantidades pueden expresarse usando distintas unidades.
Estas condiciones pueden ser verdaderas o falsas.
Estas son las cosas que alguien puede intentar hacer.
Después de hacer algo, ciertas condiciones deben seguir cumpliéndose.
Cuando algo pasa a ser verdad o cambia, sucede esto.
Algunas condiciones deben cumplirse siempre.
Las consecuencias directas ocurren juntas.
Después ocurren las consecuencias de esas consecuencias.
Puede preguntarse qué ocurriría si se intentase una acción sin modificar el mundo real.
En casos restringidos puede preguntarse si algo puede llegar a ocurrir mediante una secuencia finita de acciones.
 
⸻
 
## 2. Principios fundamentales
## 2.1
```
.mud

```
## es la fuente de verdad
Los archivos:
```
*.mud

```
son la única fuente semántica de verdad.
Son derivados reconstruibles:
* El AST.
* El índice de símbolos.
* El índice de anclas.
* El grafo semántico.
* El JSON intermedio.
* El código TypeScript.
* Los tests generados.
* La documentación.
* Los informes de impacto.
* Los índices de lectura y escritura.
* Los índices de dominios.
* Los patrones de vinculación.
* El análisis de estocasticidad.
* El análisis de admisibilidad.
* El análisis de alcanzabilidad.
* El soporte de editor.
Ningún artefacto derivado puede contener comportamiento de dominio que no esté expresado en .mud.
## 2.2 MUD describe dominio, no arquitectura
MUD no describe:
* Interfaces gráficas.
* Botones.
* Formularios.
* HTML.
* CSS.
* React.
* Motores gráficos.
* Bases de datos.
* Repositorios.
* Controladores.
* Servicios HTTP.
* Autenticación.
* Persistencia.
* Networking.
* Infraestructura.
* Despliegue.
El código TypeScript inicial es una materialización reemplazable del dominio, no la fuente de verdad.
## 2.3 MUD es un lenguaje de programación declarativo
MUD no es:
* Lenguaje natural controlado.
* Inglés macarrónico presentado como lenguaje.
* Pseudocódigo narrativo.
* Una interfaz conversacional.
* COBOL disfrazado de reglamento infantil.
MUD es un lenguaje de programación declarativo.
Puede utilizar sintaxis convencional cuando:
* Sea clara.
* Sea compacta.
* Sea fácil de aprender.
* No introduzca control algorítmico arbitrario.
* Mantenga visible la semántica del dominio.
La familiaridad de una llamada como:
```
army.IsDestroyed()

```
no convierte una regla en una función imperativa.
La sintaxis debe favorecer a personas sin experiencia previa en programación, pero no mediante frases artificialmente verbosas.
El criterio de diseño no es:
¿Parece una frase inglesa?
El criterio es:
¿Describe una verdad, una acción o una consecuencia del mundo sin obligar al autor a programar el algoritmo de ejecución?
## 2.4 Razonamiento local y causal
El comportamiento debe poder entenderse leyendo:
* Qué acción inicia el cambio.
* Qué participantes intervienen.
* Qué valores recibe.
* Qué dominios limitan esos valores.
* Qué campos modifica.
* Qué reglas reaccionan directamente.
* Qué nuevas reglas reaccionan después.
* Qué restricciones deben conservarse.
* Qué condición debe cumplirse al final.
* Cuál es el estado estable resultante.
El resultado no puede depender de:
* Orden de archivos.
* Orden alfabético.
* Velocidad del ordenador.
* Orden accidental de estructuras de datos.
* Hilos.
* Microsegundos entre entradas externas.
* Prioridades ocultas.
* El orden accidental en que se evalúan expresiones aleatorias.
## 2.5 No se expone programación general arbitraria
MUD no ofrece en su núcleo:
* while.
* goto.
* Recursión general.
* Funciones generales con efectos.
* Mutación local arbitraria.
* Excepciones como mecanismo de dominio.
* Acceso libre al runtime.
* Escape a código TypeScript desde .mud.
Sin embargo, no debe afirmarse sin demostración que MUD no sea Turing completo.
La combinación de:
* Naturales no acotados.
* Estado mutable.
* Reglas reactivas.
* Ondas causales.
* Cambios repetidos.
* Condiciones y bifurcaciones.
puede ser suficiente para expresar computación universal.
La garantía importante de MUD no es necesariamente:
El lenguaje no es Turing completo.
La garantía operativa es:
Toda acción debe alcanzar un estado estable o fallar y revertirse.
Las consultas eventually tienen restricciones adicionales y solo pueden compilarse cuando el compilador demuestra que la exploración completa es finita y terminante.
 
⸻
 
## 3. Declaraciones principales
> [!warning] Catálogo parcialmente sustituido
> D-025 sustituye la palabra reservada `construct` por `thing`; D-027 añade `look` y `message`. D-031 retira los aliases del ciclo de vida runtime; la activación abreviada de D-024 queda reservada a reglas.
MUD tiene cuatro declaraciones principales de dominio:
```
construct
magnitude
rule
action

```
Además, dispone de una declaración auxiliar de tipo:
```
alias

```
## 3.1
```
construct

```
Representa:
* Cosas.
* Conceptos.
* Categorías.
* Especializaciones.
* Entidades estáticas.
* Entidades runtime.
* Estados cualitativos.
* Familias cerradas de alternativas.
## 3.2
```
magnitude

```
Representa:
* Cantidades cuantitativas.
* Unidades convertibles.
* Posiciones sobre una cantidad.
* Posiciones cíclicas.
* Fechas, horas e instantes.
## 3.3
```
rule

```
Representa tres clases relacionadas pero distintas:
* Reglas booleanas consultables.
* Reglas reactivas provocadas por cambios.
* Reglas obligatorias que deben cumplirse siempre.
Las reglas booleanas pueden declarar:
* Participantes mediante on.
* Valores adicionales mediante given.
Las reglas reactivas declaran:
* Vinculaciones automáticas mediante for.
* when.
* if opcional.
* then.
Las reglas always declaran:
* Vinculaciones automáticas mediante for.
* Una condición obligatoria.
* Ningún efecto.
## 3.4
```
action

```
Representa:
* Operaciones que algo externo puede intentar realizar.
* La API semántica de escritura del dominio.
* La raíz de una resolución causal.
* Composiciones atómicas de otras acciones.
* Condiciones previas mediante if.
* Condiciones finales mediante after.
Las acciones declaran:
* Participantes mediante on.
* Valores adicionales mediante given.
## 3.5
```
alias

```
Representa:
* Tipos estructurales de valor.
* Tuplas nominalmente tipadas.
* Nombres alternativos para tipos existentes.
* Composiciones de tipos.
* Claves compuestas de diccionarios.
Un alias:
* No es un construct.
* No tiene identidad runtime.
* No se crea mediante create.
* No se especializa mediante is.
* Se compara por valor.
* Puede tener múltiples valores distintos del mismo tipo.
 
⸻
 
## 4. Organización física del proyecto
## 4.1 Namespaces derivados de carpetas
El namespace se deriva de la ruta.
No se declara dentro del archivo.
```
mud/
└── warfare/
    └── armies/
        ├── model.mud
        ├── recruitment.mud
        └── maintenance.mud

```
Todos esos archivos pertenecen al namespace:
```
warfare.armies

```
## 4.2 Varias declaraciones por archivo
Un archivo puede contener:
* Imports.
* Aliases.
* Constructos.
* Magnitudes.
* Reglas.
* Acciones.
El archivo es una unidad física, no una unidad semántica.
Cada declaración conserva independientemente:
* Su ancla.
* Su nodo del grafo.
* Sus dependencias.
* Su procedencia.
* Sus tests.
* Su historial Git.
Mover una declaración entre archivos del mismo namespace no cambia su identidad.
Moverla a otro namespace cambia su nombre cualificado y su ancla, salvo migración explícita.
## 4.3 Imports
Import exacto:
```
using warfare.armies

```
Import recursivo:
```
using warfare.armies.*

```
Orden de resolución:
1. Símbolos locales.
2. Símbolos del mismo namespace.
3. Imports exactos.
4. Imports recursivos.
5. Nombres completamente cualificados.
Si dos declaraciones `using` proporcionan el mismo nombre, debe utilizarse el nombre cualificado.
 
⸻
 
## 5. Convenciones de nombres
> [!warning] Terminología y sintaxis parcialmente sustituidas
> Los nombres pueden seguir orientando el estilo, pero `thing` sustituye a `construct`, `as` declara especialización y los nombres introducidos por `create` son identidades globales reservadas, no identificadores locales frescos. Véanse D-016 y D-025.
## 5.1 Namespaces
lowerCamelCase separado por puntos:
```
warfare.armies
economy.resourceStocks
ancientNearEast.kingdoms

```
## 5.2 Constructos
PascalCase:
```
Place
Kingdom
Egypt
Army
Color
Severity

```
## 5.3 Aliases
PascalCase:
```
Square
Piece
Board
Position
CastlingRights

```
## 5.4 Magnitudes
PascalCase:
```
Duration
Length
Mass
Time
Date
DateTime

```
## 5.5 Reglas
PascalCase:
```
IsDestroyed
CanAttack
OpenGate
ApplyStarvation
ValidPosition

```
## 5.6 Acciones
PascalCase:
```
Recruit
Attack
AdvanceDay
Clash
Move

```
## 5.7 Campos
lowerCamelCase:
```
treasury
morale
maintenanceCost
currentDate

```
## 5.8 Participantes y roles
Los participantes representan cosas existentes del mundo.
Delimitan:
* Qué tipos intervienen.
* Qué campos puede leer una declaración.
* Qué campos puede modificar.
* Qué relaciones deben existir.
* Qué vinculaciones debe construir el runtime.
* Qué cosas debe seleccionar el invocador de una acción.
* Qué sujetos deben proporcionarse al consultar una regla booleana.
Los roles usan lowerCamelCase:
```
attacker
defender
source
destination
buyer
seller
kingdom
army

```
No son variables arbitrarias de implementación.
## 5.9 Valores
```
given

```
Los valores given usan lowerCamelCase:
```
amount
newName
origin
destination
promotion
maximumDistance
minimumSeverity

```
## 5.10 Variables de iteración
Usan lowerCamelCase:
```
for each army in kingdom.armies {
    army.morale -= 5%
}

```
## 5.11 Identificadores locales de
```
create

```
Usan PascalCase:
```
create EgyptianArmy AirForce {
    soldiers = 1_000
}

```
## 5.12 Palabras reservadas
Una palabra clave no puede utilizarse como:
* Campo.
* Participante.
* Rol.
* Valor given.
* Variable de iteración.
* Identificador local.
* Componente de alias.
Por ejemplo, no pueden utilizarse como nombres:
```
for
from
to
in
then
when
old
allowed

```
Deben usarse nombres semánticos alternativos:
```
origin
destination
source
target

```
 
⸻
 
# 6. Participantes,
> [!warning] Sección sustituida por D-025
> Se intercambiaron las funciones de `on` y `for`. `on` declara vinculaciones automáticas en reglas de cambio, reglas `always` y mensajes. `for` declara participantes suministrados en acciones, reglas booleanas y `look`; `given` solo acompaña a acciones y reglas booleanas.
```
on

```
## ,
```
for

```
## y
```
given

```
## 6.1
```
on

```
Se utiliza en:
* Reglas booleanas consultables.
* Acciones.
Los participantes declarados mediante on:
* Son proporcionados al consultar la regla o solicitar la acción.
* No son vinculaciones reactivas automáticas.
* Actúan como sujetos de la declaración.
* Pueden utilizar azúcar sintáctico de llamada con receptor.
Regla:
```
rule IsDestroyed on Army {
    soldiers <= 0
}

```
Acción:
```
action Recruit on Kingdom [mut] {
    given amount: Natural

    then {
        soldiers += amount
    }
}

```
## 6.2
```
for

```
Se utiliza exclusivamente en:
* Reglas reactivas.
* Reglas always.
Los participantes declarados mediante for:
* Son vinculados automáticamente por el runtime.
* Generan una vinculación por cada coincidencia válida.
* No son proporcionados manualmente mediante llamada.
* Pueden mantener estado independiente de when.
```
rule OpenGate for Gate [mut] {
    when unlocked

    then {
        open = true
    }
}
always rule ValidPosition for Game {
    ...
}

```
## 6.3 Participante único anónimo
Cuando una declaración tiene un único participante, puede omitirse el nombre.
```
rule IsDestroyed on Army {
    soldiers <= 0
}
action Recruit on Kingdom [mut] {
    given amount: Natural

    then {
        soldiers += amount
    }
}
rule OpenGate for Gate [mut] {
    when unlocked

    then {
        open = true
    }
}

```
Los campos sin calificador pertenecen al participante implícito.
## 6.4 Varios participantes
Cuando intervienen varias cosas, se declaran roles.
Regla booleana:
```
rule CanAttack on
    attacker: Army,
    defender: Army
{
    attacker != defender
        & !attacker.IsDestroyed()
        & !defender.IsDestroyed()
}

```
Acción:
```
action Transfer on
    source: Account [mut],
    destination: Account [mut]
{
    given amount: Money

    if source != destination
        & amount > 0M
        & source.balance >= amount

    then {
        source.balance -= amount
        destination.balance += amount
    }
}

```
## 6.5 Participantes relacionados
Las vinculaciones estructurales automáticas mediante in pertenecen a declaraciones for.
```
rule ApplyStarvation for
    world: World,
    kingdom in world.kingdoms [mut]
{
    when world.currentDate changes

    if kingdom.starving

    then {
        kingdom.population -= 100
    }
}

```
Esto crea una vinculación por cada reino que pertenezca realmente a cada mundo.
No crea el producto cartesiano entre todos los mundos y todos los reinos.
En declaraciones on, los participantes son seleccionados por quien consulta o solicita la declaración. Las restricciones relacionales entre esos participantes se expresan mediante dominios, tipos o condiciones.
La posibilidad de declarar restricciones estructurales directamente en participantes on permanece abierta si aparece una necesidad clara.
## 6.6
```
given

```
Las reglas booleanas y las acciones pueden declarar given.
Un given es un valor suministrado al consultar una regla o solicitar una acción.
No identifica una cosa preexistente ocupando un rol.
Regla:
```
rule InCheck on Game
given
    side: Side
{
    ...
}

```
Acción:
```
action Rename on Army [mut]
given
    newName: Text
{
    then {
        name = newName
    }
}

```
Diferencia:
```
participante    cosa existente usada como sujeto
given           valor suministrado a la declaración

```
Las reglas reactivas no declaran given.
Las reglas always no declaran given.
## 6.7 Uniformidad de
```
on

```
## y
```
given

```
La forma general de las declaraciones solicitables es:
```
declaration Name on participants
given values
{
    ...
}

```
Donde given es opcional.
Ejemplos:
```
rule IsDestroyed on Army {
    ...
}
rule InRange on
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    ...
}
action Rest on Army [mut] {
    ...
}
action Transfer on
    source: Account [mut],
    destination: Account [mut]
given
    amount: Money
{
    ...
}

```
 
⸻
 
## 7. Llamadas a reglas booleanas
> [!warning] Cabeceras históricas
> Las reglas booleanas vigentes declaran participantes mediante `for`, no `on`. La mecánica general de receptores puede reutilizarse tras migrar la sintaxis.
## 7.1 Participante único
Una regla booleana con un participante se consulta mediante:
```
army.IsDestroyed()

```
Con given:
```
game.InCheck(White)

```
La regla:
```
rule InCheck on Game
given
    side: Side
{
    ...
}

```
se consulta mediante:
```
game.InCheck(White)

```
## 7.2 Varios participantes
Una regla booleana con varios participantes se consulta mediante una tupla de participantes como receptor:
```
(attacker, defender).CanAttack()

```
Con given:
```
(attacker, defender).InRange(5 Km)

```
Declaración:
```
rule InRange on
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    ...
}

```
## 7.3 Vinculación posicional
La forma ordinaria vincula participantes por el orden declarado:
```
(leftArmy, rightArmy).CanAttack()

```
equivale a:
```
attacker = leftArmy
defender = rightArmy

```
Reordenar participantes en la declaración es un cambio de API semántica.
## 7.4 Vinculación nombrada opcional
Puede utilizarse una forma nombrada:
```
(
    attacker = leftArmy,
    defender = rightArmy
).CanAttack()

```
Debe comprobar:
* Roles existentes.
* Ausencia de duplicados.
* Tipos compatibles.
* Exhaustividad.
## 7.5 Naturaleza de las llamadas
La sintaxis de llamada no convierte una regla en una función general.
Una regla booleana:
* Es pura.
* Devuelve Boolean.
* No escribe.
* No crea.
* No destruye.
* No modifica colecciones.
* No mantiene estado local.
* No puede ejecutar una acción real.
La implementación puede:
* Evaluarla bajo demanda.
* Memorizarla durante una instantánea causal.
* Indexarla.
* Mantener dependencias incrementales.
 
⸻
 
## 8. Solicitud y composición de acciones
> [!warning] Cabeceras históricas
> Las acciones vigentes declaran participantes mediante `for`, no `on`. D-027 añade `look` como superficie pública de consulta.
## 8.1 Acción con un participante
```
kingdom.Recruit(1_000)

```
## 8.2 Acción con varios participantes
```
(source, destination).Transfer(10M)

```
Los argumentos entre paréntesis corresponden a los valores given.
Los participantes aparecen en el receptor.
## 8.3 Acciones internas
Dentro del then de una acción compuesta se utiliza la misma forma:
```
action Clash on
    left: Army [mut],
    right: Army [mut]
{
    then {
        (left, right).Attack()
        (right, left).Attack()
    }
}

```
Estas expresiones no son llamadas generales de función.
Son vinculaciones semánticas entre:
* Participantes de la acción exterior.
* Participantes de la acción interior.
* Valores given disponibles.
## 8.4 Formas nombradas
La sintaxis definitiva para vinculación nombrada de valores given en acciones compuestas permanece abierta.
La forma posicional es válida cuando no existe ambigüedad.
 
⸻
 
## 9. Acceso, nombres cualificados y anclas
> [!warning] Prefijos históricos
> Las anclas ilustradas con el prefijo `construct::` deben interpretarse como `thing::`. El esquema definitivo de anclas continúa pendiente de formalización.
## 9.1 Acceso mediante
```
.
army.soldiers
army.commander.name
kingdom.stock[Grain]
world.currentDate
army.IsDestroyed()
game.InCheck(White)

```
## 9.2 Nombres cualificados
```
warfare.armies.Army
economy.kingdoms.Kingdom
geometry.Square

```
## 9.3 Anclas
Las anclas utilizan ::.
```
construct::warfare.armies.Army
construct::warfare.armies.Army::morale

alias::geometry.Square
alias::geometry.Square::file

magnitude::physics.Length
magnitude::physics.Length::meter

rule::warfare.armies.IsDestroyed
action::warfare.armies.Recruit

```
Las anclas:
* Son globalmente únicas.
* Son sensibles a mayúsculas.
* No incluyen el archivo.
* Se utilizan en consultas.
* Se utilizan en commits.
* Se utilizan en el grafo.
* Se utilizan en la agenda.
* Se utilizan en trazabilidad.
 
⸻
 
## 10. Constructos
> [!warning] Sección sustituida en ontología y sintaxis
> El concepto vigente se escribe `thing`. No existen clases e instancias separadas: las identidades declaradas y creadas pertenecen al mismo dominio. Las abstractas sí pueden activarse; `as` declara antecesores directos, `is` consulta su clausura y `create` reserva una identidad global reactivable. Véanse D-014–D-016, D-021 y D-025.
## 10.1 Declaración básica
```
construct Kingdom {
    name: Text = ""
    mut treasury: Money = 0M
    mut stability: Percentage in 0%..100% = 100%
}

```
## 10.2 Constructos abstractos
```
abstract construct Army {
    mut soldiers: Natural = 0
    mut morale: Percentage in 0%..100% = 100%
}

```
Un constructo abstracto:
* Puede tener hijos.
* Puede declarar campos.
* Puede declarar dominios.
* Puede declarar predeterminados.
* No puede existir directamente como valor concreto.
* No puede crearse mediante create.
## 10.3 Especialización mediante
```
is
construct EgyptianArmy is Army {
    soldiers = 2_000
}

```
is expresa:
* Herencia de campos.
* Herencia de restricciones.
* Herencia de dominios.
* Herencia de valores predeterminados.
* Sustituibilidad.
* Posibilidad de añadir campos.
* Posibilidad de sustituir predeterminados.
Ejemplo:
```
abstract construct Place {
    name: Text
}

abstract construct Kingdom is Place {
    mut treasury: Money = 0M
}

construct Egypt is Kingdom {
    name = "Egypt"
}

```
## 10.4 Igualdad e identidad de constructos
== compara identidad.
```
Egypt == Egypt

```
es verdadero.
```
Egypt == Kingdom

```
es falso.
La relación correcta es:
```
Egypt is Kingdom

```
Esto es verdadero.
También:
```
Egypt is Place

```
es verdadero si Kingdom is Place.
== debe ser:
* Simétrico.
* Transitivo.
* Reflexivo.
is representa especialización o pertenencia nominal y no es simétrico.
## 10.5 Identidad runtime
Dos constructos runtime creados por separado tienen identidades diferentes aunque todos sus campos coincidan.
## 10.6 Herencia múltiple
```
construct Warship is MilitaryUnit, NavalUnit {
}

```
Reglas:
1. Un ancestro común se incorpora una sola vez.
2. Un campo heredado desde la misma ancla se deduplica.
3. Campos homónimos compatibles se fusionan.
4. Campos incompatibles producen error.
5. El orden de los padres no crea prioridad.
6. El orden de los padres no modifica la semántica.
7. Los conflictos de predeterminados pueden resolverse en el hijo.
## 10.7 Fusión de campos homónimos
```
abstract construct A {
    mut power: Number = 10
}

abstract construct B {
    mut power: Number = 10
}

construct C is A, B {
}

```
La fusión exige compatibilidad de:
* Tipo.
* Dominio.
* Cardinalidad.
* Mutabilidad exterior.
* Capacidad interior.
* unique.
* Orden.
* Naturaleza almacenada o calculada.
* Expresión calculada.
* Valor predeterminado.
 
⸻
 
## 11. Aliases y valores estructurales
> [!warning] Sistema de aliases sustituido
> D-031–D-033 son la autoridad actual. Todos los aliases son tipos nominales inmutables y sin ciclo de vida runtime. Las expresiones de tipo usan `:=`; los literales son contextuales; dos literales estructurales desnudos no se comparan; `to` realiza casting nominal compatible; la forma nombrada conserva el orden; y la enumeración finita usa el producto cartesiano lexicográfico.
## 11.1 Alias estructural
```
alias Square {
    file: File
    rank: Rank
}

```
Un alias estructural:
* Declara un tipo nominal.
* Contiene componentes ordenados.
* Sus valores se comparan estructuralmente.
* Es inmutable.
* No tiene identidad runtime.
* No puede llevar mut.
* No se crea mediante create.
* No participa en herencia.
* No puede ser abstracto.
## 11.2 Literal posicional
```
(1 m, 48 s)

```
## 11.3 Literal nombrado
```
(
    file = E,
    rank = Four
)

```
## 11.4 Acceso a componentes
```
square.file
square.rank

```
## 11.5 Igualdad
```
(E, Four) == (E, Four)

```
Esta comparación histórica es inválida porque ninguno de los literales aporta contexto nominal. Debe tiparse al menos uno como `Square`.
## 11.6 Tipos nominales y valores estructurales
Aliases diferentes no son intercambiables automáticamente aunque tengan los mismos componentes.
## 11.7 Orden lexicográfico
Cuando todos los componentes tienen orden canónico, los valores del alias tienen orden lexicográfico.
## 11.8 Alias finito
Un alias estructural es finito cuando todos sus componentes tienen dominios finitos conocidos.
```
for each square in Square {
}
exists destination in Square:
    ...

```
## 11.9 Alias simple
```
alias Board :=
    Square -> Piece [0..32 ordered]

```
 
⸻
 
## 12. Familias cerradas de valores
## 12.1 Valores con orden canónico
```
construct Color {
    values =
        Red,
        Green,
        Blue
}

```
## 12.2 Valores semánticamente ordenados
```
construct Severity {
    ordered values =
        Low,
        Medium,
        High,
        Critical
}

```
## 12.3 Igualdad
Los valores cerrados se comparan nominalmente.
## 12.4 Familia abierta
```
abstract construct Color {
}

construct Red is Color {
}

```
## 12.5 Campos comunes
Un constructo con values puede declarar campos comunes.
La sintaxis de valores específicos por alternativa sigue fuera del núcleo.
 
⸻
 
## 13. Campos
## 13.1 Campo almacenado inmutable
```
name: Text = ""

```
## 13.2 Campo almacenado mutable
```
mut treasury: Money = 0M

```
## 13.3 Campo calculado
```
maintenanceCost: Money :=
    soldiers * 2M

```
## 13.4 Dominio de un campo
```
mut morale: Percentage in 0%..100% = 100%
age: Natural in 0..150

```
Forma general:
```
nombre: Tipo in dominio

```
## 13.5 Efecto del dominio
Debe cumplirse:
* Durante inicialización.
* Durante especialización.
* Durante create.
* Después de una asignación.
* Después de una raíz.
* Después de una onda.
* En todo estado publicable.
Si una escritura runtime deja un campo fuera de dominio:
* La raíz u onda falla.
* La resolución resulta failed.
* Se revierte.
## 13.6 Interacción con saturación
La semántica del tipo se aplica antes de comprobar el dominio.
## 13.7 Dominios calculados
Un dominio puede depender de estado accesible si:
* Es puro.
* Es determinista.
* No es estocástico.
* Sus dependencias son analizables.
* No crea ciclos inválidos.
## 13.8 Campos calculados con dominio
```
stabilityScore: Number in 0..100 :=
    ...

```
## 13.9
```
=

```
## frente a
```
:=
=     valor almacenado
:=    definición calculada

```
 
⸻
 
## 14. Tipos básicos
> [!warning] Catálogo cuantitativo sustituido
> Los tipos básicos vigentes son `Text`, `Bool`, `Natural`, `Integer`, `Number`, `Rumber` y `Money`. Los cinco últimos son representaciones numéricas, no magnitudes. `Number` es racional exacto y `Rumber` usa `binary64` explícito. `Percentage` deja de ser un tipo básico. Véanse D-028 y D-034.
```
Boolean
Natural
Integer
Number
Text
Money
Percentage

```
## 14.1 Boolean
```
active: Boolean = false

```
## 14.2 Natural
Si una operación deja un Natural por debajo de cero, satura en 0.
## 14.3 Integer
Conversión implícita:
```
Integer → Number

```
## 14.4 Number
> [!warning] Representación fijada
> `Number` denota racionales exactos en forma canónica. `Rumber` es el tipo aproximado IEEE 754 `binary64`; sus literales puros usan el prefijo `r`. No se mezclan implícitamente. Véase D-034.
```
growthRate: Number = 1.25

```
## 14.5 Text
```
name: Text = ""

```
## 14.6 Money
Usa exactamente dos decimales y aritmética decimal exacta.
El modo exacto de redondeo sigue abierto.
## 14.7 Percentage
Convierte implícitamente a Number.
No está restringido automáticamente a 0%..100%.
 
⸻
 
## 15. Conversiones
> [!warning] Operador retirado para conversiones
> `as` queda reservado para declarar especialización entre `thing`. `to` posee una rama cuantitativa y otra de casting nominal de alias estructuralmente compatible; `in` solo cambia la unidad de presentación. D-034 fija el redondeo global al más cercano con empates al par. Véanse D-030, D-032 y D-034.
Implícitas:
```
Natural → Integer
Integer → Number
Percentage → Number

```
Explícitas:
```
value as Integer
value as Natural

```
Las conversiones estrechas que requieran redondeo deben declarar una política explícita.
 
⸻
 
## 16. Mutabilidad y capacidades
> [!warning] Regla singular sustituida
> La mutabilidad exterior y la capacidad interior son ejes ortogonales para toda cardinalidad. `mut field: T` equivale a `mut field: T[1]`, no a `field: T[1 mut]`. Véase D-019.
MUD distingue:
1. Cambiar una relación o campo.
2. Modificar constructos alcanzados mediante esa relación.
## 16.1
```
mut

```
## exterior
```
mut armies: Army [*]

```
## 16.2
```
[mut]

```
## interior
```
armies: Army [* mut]

```
## 16.3 Combinaciones

| Declaración              | Cambiar colección | Modificar miembros |
| ------------------------ | ----------------- | ------------------ |
| armies: Army [*]         | No                | No                 |
| mut armies: Army [*]     | Sí                | No                 |
| armies: Army [* mut]     | No                | Sí                 |
| mut armies: Army [* mut] | Sí                | Sí                 |

**16.4 Capacidad singular**
```
capital: City [1 mut]

```
## 16.5 No existe mutabilidad profunda automática
Cada campo modificable debe ser mut.
## 16.6 Participantes mutables
Las acciones usan [mut] sobre participantes modificables:
```
action Recruit on Kingdom [mut]
given
    amount: Natural
{
    ...
}

```
Las reglas reactivas también:
```
rule RecoverMorale for Army [mut] {
    ...
}

```
Las reglas booleanas y las always rule no pueden declarar [mut].
 
⸻
 
## 17. Cardinalidades y colecciones
> [!warning] Membresía y validación sustituidas
> No existe `reflexive`: para una colección de tipo `T`, todo miembro `c` debe cumplir $c\neq T\land c\ \mathsf{is}\ T$. La cardinalidad se demuestra al final de cada `then` y para su posible consolidación, no tras cada instrucción. Véase D-026.
## 17.1 Cardinalidad como intervalo de naturales
```
[n]
[min..max]
[min..*]
[*]

```
Equivalencias:
```
[n]       = [n..n]
[*]       = [0..*]

```
## 17.2 Cardinalidad predeterminada
```
capital: City

```
equivale a:
```
capital: City [1]

```
## 17.3 Ausencia sin null
```
piece : Piece [0..1] = empty

```
## 17.4 Duplicados
Permitidos por defecto.
## 17.5
```
unique
armies: Army [* unique]

```
## 17.6
```
ordered

```
* Básicos: orden natural.
* Constructos: inserción.
* Familias ordenadas: orden semántico.
* Aliases: lexicográfico.
## 17.7
```
ordered by
armies: Army [* ordered by name]

```
## 17.8 Inicialización
```
armies =
    EarthForce,
    WaterForce

```
 
⸻
 
## 18. Diccionarios
## 18.1 Tipo
```
stock: Resource -> Number [*]
board: Square -> Piece [0..32 ordered]

```
## 18.2 Inicialización
```
stock =
    Grain -> 2_000,
    Bronze -> 500

```
## 18.3 Claves compuestas
```
board[(E, Four)]

```
Azúcar:
```
board[E, Four]

```
## 18.4 Acceso encadenado
Solo es válido si el primer acceso devuelve otro diccionario.
## 18.5 Lectura de clave inexistente
Devuelve el predeterminado cuando exista.
En tipos sin predeterminado universal representa ausencia.
## 18.6 Escritura de clave inexistente
Materializa la entrada cuando sea posible.
## 18.7 Operaciones totales
* Retirar ausente es no-op.
* Asignar sustituye.
* Claves únicas.
* unique no se usa.
## 18.8 Iteración sobre claves
```
exists square in board:
    ...

```
## 18.9 Iteración sobre entradas
```
exists (square, piece) in board:
    ...

```
## 18.10 Orden
Los diccionarios ordered se recorren por orden canónico de claves.
 
⸻
 
## 19. Dominios declarativos mediante
```
in

```
## 19.1 Forma general
```
nombre: Tipo in dominio

```
Puede utilizarse en:
* Campos.
* Componentes de alias.
* Valores given de reglas.
* Valores given de acciones.
Ejemplos:
```
mut morale: Percentage in 0%..100% = 100%
action Recruit on Kingdom [mut]
given
    amount: Natural in 1..100
{
    ...
}
rule CanRecruit on Kingdom
given
    amount: Natural in 1..100
{
    ...
}
alias Coordinate {
    horizontal: Integer in 0..7
    vertical: Integer in 0..7
}

```
## 19.2 Dominio de
```
given

```
## en una acción
Si un valor queda fuera del dominio:
* La acción resulta rejected.
* No se evalúa el if.
* No se ejecuta la raíz.
* No se producen ondas.
## 19.3 Dominio de
```
given

```
## en una regla
Si el valor queda fuera del dominio:
* La regla devuelve false.
* El compilador puede diagnosticarlo si es estático.
## 19.4 Dominio de campo
Un campo fuera de dominio invalida el estado y provoca failed.
## 19.5 Dominio finito
Un dominio finito permite:
* Interfaces.
* Tests.
* Enumeración de acciones.
* eventually.
* Exhaustividad.
## 19.6 Contextos de
```
in

```
Dominio:
```
amount: Natural in 1..100

```
Pertenencia:
```
amount in 1..100

```
Participante relacionado:
```
kingdom in world.kingdoms

```
Unidad:
```
distance in kilometers

```
 
⸻
 
## 20. Magnitudes
> [!warning] Sistema de magnitudes sustituido
> Las secciones 20–26 conservan únicamente contexto histórico. D-028 redefine tipos numéricos, unidades raíz y alternativas, magnitudes derivadas, inferencia de representación y unidades compuestas automáticas. D-029 mueve `point over` y `cycle` a la cabecera y al dominio.
Una magnitud es:
1. Lineal con unidades.
2. Punto sobre magnitud lineal.
 
⸻
 
## 21. Magnitudes lineales
```
magnitude Duration {
    unit second {
        name = "second"
        plural = "seconds"
        abbreviation = "s"

        prefixes =
            milli,
            micro,
            nano
    }

    unit minute {
        name = "minute"
        abbreviation = "min"
        equivalent = 60 seconds
    }
}

```
Las propiedades y reglas de unidades se mantienen vigentes:
* Una raíz.
* Equivalencias positivas.
* Sin ciclos.
* Misma magnitud.
* Nombres y abreviaturas sin colisiones.
 
⸻
 
## 22. Prefijos
Los prefijos son integrados.
No se permiten personalizados.
La ausencia de prefixes no habilita ninguno.
prefixes habilita todos.
prefixes = ... habilita solo los enumerados.
Kilo:
```
kilo → K-

```
Micro:
```
micro → u-

```
con alias Unicode.
 
⸻
 
## 23. Operaciones sobre magnitudes lineales
```
M + M → M
M - M → M
M * Number → M
Number * M → M
M / Number → M
M / M → Number

```
in cambia la unidad de representación.
 
⸻
 
## 24. Magnitudes de punto
```
magnitude Time {
    point over Duration
    cycle = 24 hours
    format = "{hour:2}:{minute:2}:{second:2}"
}

```
Aritmética:
```
P - P → M
P + M → P
M + P → P
P - M → P
P + P → error

```
 
⸻
 
## 25. Formato de puntos
```
{componente:anchura}

```
Define representación, no aritmética.
 
⸻
 
## 26. Magnitudes temporales estándar
```
Duration
Time
Date
DateTime

```
Usan inicialmente un calendario civil estándar.
 
⸻
 
## 27. Operadores
## 27.1 Aritméticos
```
+
-
*
/
%

```
## 27.2 Comparación
```
==
!=
<
<=
>
>=
is

```
## 27.3 Lógicos
```
!       not
&       and
|       or
=>      implies
<=>     iff

```
## 27.4 Igualdad por tipo
* Constructos: identidad.
* Valores cerrados: identidad nominal.
* Aliases: componentes.
* Números: valor.
* Magnitudes: valor normalizado.
* Intervalos: conjunto normalizado.
* Colecciones ordenadas: secuencia.
* Colecciones no ordenadas: multiplicidad.
* Diccionarios: asociaciones.
 
⸻
 
## 28. Intervalos
> [!warning] Sintaxis y límites ampliados
> D-029 fija el azúcar `[n]`, el significado lateral de `*`, la equivalencia `[*] = [*..*]`, la obligación de cerrar todo extremo con `*`, los límites canónicos desnudos de magnitudes y la única forma cíclica `[a..b cycle)`. D-034 permite intervalos `Rumber` como dominios, pero prohíbe enumerarlos. Las reglas históricas no contradictorias sobre normalización e iteración siguen pendientes de promoción.
Se escriben:
```
Natural Interval
Integer Interval
Money Interval
Percentage Interval

```
No:
```
Interval<Natural>

```
## 28.1 Intervalo vacío
```
empty

```
## 28.2 Literales
```
1..6
[1..6]
(1..6)
[1..6)
(1..6]

```
## 28.3 Operadores
```
|       union
&       intersection
^       xor
-       except

```
## 28.4 Normalización
Los resultados equivalentes se normalizan por contenido.
## 28.5 Pertenencia
```
age in 18..65

```
## 28.6 Iteración de intervalos
Solo pueden recorrerse intervalos:
* Finitos.
* Enumerables.
* Pertenecientes a un tipo con una operación de avance definida.
* Con un paso que permitagarantizar la terminación.
Forma general:
```
for each variable in intervalo {
    ...
}

```
Con paso explícito:
```
for each variable in intervalo by paso {
    ...
}

```
**Naturales e Integer**
Los intervalos de Natural e Integer utilizan un paso predeterminado de:
```
1

```
Ejemplo:
```
for each number in 1..6 {
}

```
produce, en este orden:
```
1
2
3
4
5
6

```
También puede declararse un paso explícito:
```
for each number in 0..10 by 2 {
}

```
produce:
```
0
2
4
6
8
10

```
**Money**
Los intervalos de Money utilizan un paso predeterminado de:
```
0.01M

```
Ejemplo:
```
for each amount in 0M..0.05M {
}

```
produce:
```
0.00M
0.01M
0.02M
0.03M
0.04M
0.05M

```
Puede declararse otro paso:
```
for each amount in 0M..100M by 5M {
}

```
**Number**
Los intervalos de Number no tienen paso predeterminado.
by es obligatorio:
```
for each number in 0..1 by 0.3 {
}

```
produce:
```
0
0.3
0.6
0.9

```
No se incluye 1 porque no pertenece a la secuencia generada mediante incrementos exactos de 0.3 desde el límite inicial.
Esto es inválido:
```
for each number in 0..1 {
}

```
El compilador debe diagnosticar que un intervalo de Number necesita un paso explícito.
**Reglas del paso**
El paso:
* Debe ser del mismo tipo que los valores recorridos o convertible de forma segura a ese tipo.
* Debe ser estrictamente positivo.
* No puede ser cero.
* No puede ser negativo.
* Debe ser finito.
* No puede ser estocástico.
* Debe permitir demostrar que la iteración termina.
Un paso inválido produce error de compilación cuando pueda detectarse estáticamente.
**Extremos abiertos y cerrados**
La iteración respeta los delimitadores del intervalo.
```
for each number in [1..4) {
}

```
produce:
```
1
2
3
for each number in (1..4] {
}

```
produce:
```
2
3
4

```
El primer valor recorrido es el primer valor de la secuencia generada que pertenece realmente al intervalo.
**Intervalos discontinuos**
Los segmentos de un intervalo discontinuo se recorren según el orden natural del tipo.
```
for each number in [1..3] | [7..9] {
}

```
produce:
```
1
2
3
7
8
9

```
La secuencia del paso se reinicia al comienzo de cada segmento normalizado.
Los valores duplicados eliminados durante la normalización no se recorren más de una vez.
**Intervalo vacío**
Recorrer empty ejecuta cero iteraciones:
```
for each number in empty {
}

```
No produce error.
**Intervalos no enumerables**
No pueden recorrerse intervalos:
* Infinitos.
* No acotados.
* De tipos sin operación de avance definida.
* Para los que no pueda demostrarse la terminación.
Su uso en for each produce error de compilación.

 
⸻
 
## 29. Precedencia
De mayor a menor:
1. ., [], ().
2. Receptores multiparte.
3. old.
4. allowed.
5. Negación.
6. Multiplicación, división y módulo.
7. Suma y resta.
8. Comparaciones, is, in.
9. Conjunción e intersección.
10. Disyunción y unión.
11. Diferencia simétrica.
12. Implicación.
13. Bicondicional.
14. eventually ... through ....
 
⸻
 
## 30. Literales numéricos y
> [!warning] Sufijos retirados
> Los separadores `_` se conservan. D-028 retira todos los sufijos de tipo, incluidos `N`, `I` y `M`; D-034 introduce `r` como prefijo obligatorio de literales `Rumber` puros y opcional únicamente dentro de cantidades de magnitud `Rumber`.
```
_

```
Se mantienen las reglas de agrupación de tres cifras.
 
⸻
 
## 31. Reglas booleanas consultables
> [!warning] Cabecera y ciclo de vida sustituidos
> Estas reglas usan `for`, pueden activarse o suspenderse y, cuando están inactivas, sus llamadas se borran estructuralmente de la expresión. Véanse D-021, D-022 y D-025.
## 31.1 Declaración
```
rule IsDestroyed on Army {
    soldiers <= 0
}

```
## 31.2 Participante único
```
army.IsDestroyed()

```
## 31.3 Varios participantes
```
rule CanAttack on
    attacker: Army,
    defender: Army
{
    ...
}
(attacker, defender).CanAttack()

```
## 31.4
```
given
rule InRange on
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    ...
}

```
## 31.5 Características
Las reglas booleanas:
* Son puras.
* Devuelven Boolean.
* No escriben.
* Pueden declarar given.
* Pueden usar cuantificadores.
* Pueden usar allowed.
* Pueden usar eventually cuando sea admisible.
* No pueden leer directamente campos estocásticos calculados.
 
⸻
 
## 32. Reglas reactivas
> [!warning] Cabecera y ciclo de vida sustituidos
> Las reglas de cambio usan `on`, no `for`, y pueden activarse o suspenderse. Véanse D-021 y D-025.
Usan for.
```
rule OpenGate for Gate [mut] {
    when unlocked

    then {
        open = true
    }
}

```
No declaran given.
No ejecutan acciones reales.
Pueden consultar reglas booleanas y utilizar allowed dentro de expresiones si no crean ciclos inválidos.
 
⸻
 
## 33. Reglas
> [!warning] Cabecera y ciclo de vida sustituidos
> Las reglas `always` usan `on`, no `for`, y pueden activarse o suspenderse. Véanse D-021 y D-025.
```
always
always rule ValidPosition for Game {
    ...
}

```
* No son invocables.
* No producen efectos.
* Se comprueban automáticamente.
* Si fallan, la resolución resulta failed.
 
⸻
 
## 34. Semántica de
> [!warning] Semántica booleana ampliada
> D-022 define el borrado estructural de llamadas a reglas booleanas inactivas después del desazucarado booleano. Esta sección no cubre ese comportamiento.
```
when

```
Se activa por transición:
```
false → true

```
La transición se mantiene por vinculación.
 
⸻
 
## 35.
```
changes

```
Solo se utiliza dentro de when.
Genera un pulso por cambio neto confirmado.
 
⸻
 
## 36. Acciones
> [!warning] Cabecera histórica
> Las acciones usan `for` y pueden usar `given`. No usan `on`. Véase D-025.
## 36.1 Declaración
```
action Recruit on Kingdom [mut]
given
    amount: Natural in 1..100
{
    if treasury >= amount * recruitmentCost

    then {
        treasury -= amount * recruitmentCost
        soldiers += amount
    }
}

```
## 36.2 Naturaleza
Una acción:
* Declara participantes mediante on.
* Puede declarar valores mediante given.
* Puede declarar dominios para esos valores.
* Puede declarar if.
* Declara then.
* Puede declarar after.
* No declara when.
* No se activa automáticamente.
* Puede solicitarse desde fuera.
* Puede componerse desde otra acción.
* Inicia resolución causal.
* Es atómica junto con sus ondas.
## 36.3 API semántica
La API separa:
* Participantes.
* Valores given.
* Dominios.
* Precondición.
* Efectos.
* Condición final.
* Lecturas.
* Escrituras.
* Resultados.
Internamente, una materialización puede llamar “inputs” a los valores given, pero esa terminología no forma parte de la sintaxis MUD.
 
⸻
 
## 37.
```
after
action Move on Game [mut]
given
    origin: Square
    destination: Square
{
    if PseudoLegalMove(origin, destination)

    then {
        board[destination] = board[origin]
        remove origin from board
    }

    after {
        !InCheck(old sideToMove)
    }
}

```
Se evalúa después de toda la resolución causal.
Falso produce rejected.
Error técnico produce failed.
 
⸻
 
## 38.
```
old
old sideToMove
old board[origin]
old (treasury + debt)

```
Lee el estado estable anterior a la acción exterior completa.
Solo se permite inicialmente en after.
 
⸻
 
## 39. Acciones elementales
```
action Attack on
    attacker: Army,
    defender: Army [mut]
{
    if attacker != defender

    then {
        defender.soldiers -= attacker.damage
    }
}

```
Las instrucciones de un mismo then son secuenciales internamente y atómicas externamente.
 
⸻
 
## 40. Acciones compuestas
```
action Clash on
    left: Army [mut],
    right: Army [mut]
{
    then {
        (left, right).Attack()
        (right, left).Attack()
    }
}

```
Todas las hojas:
* Leen el mismo estado inicial.
* Evalúan sus given, dominios e if.
* Forman una raíz simultánea.
* Comprueban sus after al final.
Las llamadas entre acciones deben ser acíclicas.
 
⸻
 
## 41. Formas exclusivas del
```
then

```
Acción elemental:
```
then {
    efectos
}

```
Acción compuesta:
```
then {
    participant.Action()
}

```
No se mezclan.
 
⸻
 
## 42. Resultado de una acción
> [!warning] Catálogo de fallos parcialmente sustituido
> La destrucción ya no poda colecciones ni rompe cardinalidades por sí misma: suspende lógicamente declaraciones y dependencias y conserva las cargas. Los puntos de validación restantes siguen abiertos. Véanse D-021 y D-026.
```
accepted
rejected
failed

```
## 42.1
```
accepted

```
* Valores given dentro de dominio.
* if verdadero.
* Raíz válida.
* Ondas estables.
* always válidas.
* after verdadero.
## 42.2
```
rejected

```
* given fuera de dominio.
* if falso.
* after falso.
## 42.3
```
failed

```
* Conflicto.
* Ciclo.
* Cardinalidad inválida.
* Campo fuera de dominio.
* Referencia destruida.
* always incumplida.
* Fallo de allowed.
* Error semántico.
 
⸻
 
## 43.
```
allowed

```
## 43.1 Objetivo
Permite consultar hipotéticamente una acción dentro de una expresión booleana.
## 43.2 Sintaxis
```
allowed game.Move(origin, destination, promotion)
allowed (source, destination).Transfer(amount)

```
Los receptores representan participantes.
Los argumentos representan valores given.
## 43.3 Semántica
1. Copia especulativa.
2. Vinculación de participantes.
3. Suministro de given.
4. Dominios.
5. if.
6. Raíz.
7. Ondas.
8. always.
9. after.
10. Descarte.
```
accepted → true
rejected → false
failed   → fallo de evaluación

```
## 43.4 No produce efectos reales
No modifica:
* Mundo.
* Cola.
* Logs.
* Azar global.
* Identificador de resolución.
## 43.5 Contextos
Puede aparecer en:
* Reglas booleanas.
* if.
* after.
* when.
* always.
* Cuantificadores.
## 43.6 Fallos
Un failed se propaga.
No equivale a false.
## 43.7 Aleatoriedad
Usa una rama concreta, reproducible y sembrada.
Puede revelar un resultado hipotético futuro.
## 43.8 Ciclos
El grafo de admisibilidad debe ser acíclico.
 
⸻
 
## 44.
```
eventually

```
## 44.1 Forma
```
eventually game.Checkmate(White)
    through game.Move

```
## 44.2 Significado
Existe una secuencia finita de acciones aceptadas que conduce al objetivo.
## 44.3 Secuencia vacía
El estado actual cuenta.
## 44.4 Transiciones
Cada transición incluye acción completa, ondas, always y after.
## 44.5 Enumeración
Los valores given deben tener dominios finitos y enumerables.
```
action Move on Game [mut]
given
    origin: Square
    destination: Square
{
    ...
}

```
es enumerable si Square es finito.
```
action Recruit on Kingdom [mut]
given
    amount: Natural
{
    ...
}

```
no lo es.
```
given amount: Natural in 1..100

```
sí.
## 44.6 Garantía
Solo se compila si el compilador demuestra:
* Finitud.
* Enumerabilidad.
* Terminación.
* Comparabilidad del estado.
* Ausencia de creación no acotada.
## 44.7 Aleatoriedad
Semántica existencial:
* Existe una secuencia de acciones.
* Existe una secuencia de resultados aleatorios posibles.
* Cada resultado tiene probabilidad positiva.
* Se alcanza el objetivo.
## 44.8 Sin recursión general
El runtime decide el algoritmo.
 
⸻
 
## 45. Resolución causal por ondas
> [!warning] Consolidación refinada
> Cada `then` calcula secuencialmente un delta privado desde una instantánea común; los bloques no observan deltas parciales ajenos y después se consolidan determinísticamente. Véanse D-023 y D-026.
```
estado estable
→ raíz
→ onda 1
→ onda 2
→ estado estable tentativo
→ after
→ confirmación

```
Las reglas de una onda leen la misma instantánea.
 
⸻
 
## 46. Vinculaciones durante ondas
Se fijan al inicio de cada onda.
Los cambios afectan a la siguiente.
 
⸻
 
## 47. Cola de acciones
Solo existe una resolución activa.
Las acciones externas se encolan.
Los valores given, sus dominios y el if se evalúan cuando comienza la ejecución.
 
⸻
 
## 48. Conflictos
> [!warning] Matriz parcialmente sustituida
> D-023 fija la consolidación de efectos estructurales y D-026 exige prueba estática de cardinalidad local y conjunta. La matriz de los demás efectos continúa abierta.
Se mantienen las reglas de:
* Asignaciones idénticas.
* Asignaciones diferentes.
* Combinación aditiva.
* Combinación multiplicativa.
* Conflictos entre operaciones incompatibles.
* Añadidos antes de retiradas.
* Creación antes de destrucción.
 
⸻
 
## 49. Ciclos causales y terminación
Una resolución debe estabilizarse o fallar.
eventually exige demostración previa más fuerte.
 
⸻
 
## 50. Efectos permitidos
> [!warning] Catálogo ampliado
> `add` y `remove` también operan sobre propiedades. `create` y `destroy` alcanzan reglas, pero D-031 prohíbe aplicarlos a aliases.
```
=
+=
-=
*=
/=

add
remove
add all
remove all
move
move all

create
destroy

```
 
⸻
 
## 51. Asignaciones
Deben respetar:
* Tipo.
* Mutabilidad.
* Capacidad.
* Dominio.
* Cardinalidad.
 
⸻
 
## 52. Cuantificadores y agregaciones
```
exists
forall
count
sum
min
max

```
Diccionario por clave:
```
exists square in board:

```
Diccionario por entrada:
```
exists (square, piece) in board:

```
Alias finito:
```
exists destination in Square:

```
 
⸻
##
## 53.
```
for each

```
for each ejecuta un bloque para cada valor perteneciente a una fuente iterable.
Puede utilizarse sobre:
* Colecciones.
* Diccionarios.
* Aliases finitos.
* Intervalos finitos y enumerables.
**Colección**
```
for each army in kingdom.armies {
    army.morale -= 5%
}

```
**Diccionario por clave**
```
for each square in board {
    ...
}

```
**Diccionario por entrada**
```
for each (square, piece) in board {
    ...
}

```
**Alias finito**
```
for each square in Square {
    ...
}

```
El alias debe tener un dominio finito y enumerable conocido por el compilador.
**Intervalo**
```
for each number in 1..6 {
    ...
}

```
Con paso explícito:
```
for each number in 0..1 by 0.25 {
    ...
}

```
Las reglas completas sobre pasos predeterminados, by, extremos abiertos, intervalos discontinuos y terminación se definen en la sección 28.6.
**Instantánea de pertenencia**
La pertenencia a la fuente iterable se fija al comenzar el for each.
En colecciones y diccionarios:
* Los elementos añadidos posteriormente no se recorren.
* Los elementos retirados permanecen en la instantánea pendiente.
* El orden de recorrido se fija al comenzar.
* Destruir un constructo que todavía aparece en la instantánea puede provocar un fallo cuando una iteración posterior intente utilizarlo.
En aliases e intervalos, la secuencia completa de valores se determina al comenzar la iteración.
**Fuentes ordenadas**
Cuando la fuente tiene un orden definido, las iteraciones son secuenciales.
Cada iteración puede observar los efectos confirmados por iteraciones anteriores del mismo bloque.
Son fuentes ordenadas:
* Colecciones declaradas ordered.
* Diccionarios declarados ordered.
* Aliases con orden canónico.
* Intervalos.
* Familias con ordered values.
**Fuentes no ordenadas**
Cuando la fuente no tiene orden:
1. Todas las iteraciones leen el mismo estado inicial del bucle.
2. Cada iteración calcula sus efectos independientemente.
3. Los efectos se combinan como efectos simultáneos.
4. Los conflictos invalidan atómicamente la operación que contiene el bucle.
El resultado no puede depender del orden interno de almacenamiento.
**Filtrado**
Puede añadirse una condición después de la fuente:
```
for each army in kingdom.armies:
    army.IsDestroyed()
{
    remove army from kingdom.armies
}

```
La condición:
* Es pura.
* Se evalúa sobre la instantánea correspondiente a la iteración.
* Debe ser determinista.
* No puede depender de campos calculados estocásticos.

⸻
 
## 54. Operaciones de colección
Se mantienen:
* add.
* remove.
* add all.
* remove all.
* move.
* move all.
 
⸻
 
## 55. Creación runtime
> [!warning] Sección sustituida
> La sintaxis vigente es `create [abstract] thing A [as B, ...] { ... }`. Admite raíces, abstractas y especialización múltiple; la identidad queda reservada globalmente y puede reactivarse. Las reglas usan una definición completa única y `create Nombre` para activaciones posteriores. Los aliases no admiten creación. Véanse D-016, D-021, D-024, D-025 y D-031.
Solo de constructos concretos:
```
create EgyptianArmy AirForce {
}

```
 
⸻
 
## 56. Destrucción runtime
> [!warning] Sección sustituida
> `destroy` realiza una suspensión lógica reversible: conserva descriptor, carga y aristas almacenadas y suspende dependencias duras. No repara cardinalidades ni elimina miembros. `remove` es la operación destructiva para propiedades y contenidos. Véase D-021.
```
destroy army

```
Puede provocar failed si rompe una cardinalidad obligatoria.
 
⸻
 
## 57. Aleatoriedad
MUD distingue:
1. = Rand(...).
2. := Rand(...).
3. Rand en efectos.
4. Aleatoriedad concreta en allowed.
5. Aleatoriedad existencial en eventually.
Los campos estocásticos calculados no pueden aparecer directamente en condiciones.
 
⸻
 
## 58. Fallos semánticos
Operaciones ordinarias inválidas dentro de condiciones suelen producir falso.
Un fallo especulativo de allowed se propaga.
Los efectos inválidos producen failed.
 
⸻
 
## 59. Valores predeterminados
> [!warning] Premisa ampliada
> D-017 exige un valor predeterminado perteneciente al dominio de todo tipo bien formado. D-028 sustituye `Boolean` por `Bool`, retira `Percentage` como básico y elimina el sufijo `M`; D-034 añade `Rumber` con predeterminado `r0`. Para colecciones de `thing`, el ancla exacta del tipo nunca puede servir como miembro predeterminado; Q-047 mantiene abierta la selección concreta.
```
Boolean        false
Natural        0
Integer        0
Number         0
Text           ""
Money          0M
Percentage     0%
Colecciones    empty
Diccionarios   empty
Intervalos     empty

```
 
⸻
 
## 60. Comentarios
MUD admite:
1. Comentarios de línea.
2. Comentarios de línea cerrados explícitamente.
3. Comentarios multilínea.
Los delimitadores de comentario que aparezcan dentro de una cadena de texto no se interpretan como comentarios.
```
hexadecimal = "#FF0000"

```
**60.1 Comentario de línea**
Un comentario de línea comienza con:
```
#

```
y continúa hasta el final de la línea.
```
# Ejército inicial

soldiers = 1_000 # tropas iniciales

```
El salto de línea cierra automáticamente el comentario.
**60.2 Cierre explícito en la misma línea**
Un segundo # puede cerrar el comentario antes del final de la línea y permitir que continúe el código.
```
soldiers = 1_000 # tropas iniciales # morale = 100%

```
En este ejemplo:
```
# tropas iniciales #

```
es el comentario, y:
```
morale = 100%

```
vuelve a ser código.
El segundo # es opcional.
Por tanto:
```
soldiers = 1_000 # tropas iniciales

```
mantiene el comentario hasta el salto de línea, mientras que:
```
soldiers = 1_000 # tropas iniciales # morale = 100%

```
lo cierra explícitamente.
Un comentario de línea cerrado explícitamente no puede atravesar un salto de línea.
**60.3 Comentario multilínea**
Un comentario multilínea comienza y termina con:
```
###

```
Ejemplo:
```
###
Este comentario
ocupa varias líneas.
###

```
Puede aparecer entre expresiones dentro de una misma línea:
```
soldiers = ### valor provisional ### 1_000

```
También puede comenzar o terminar en líneas que contengan otro código:
```
soldiers = 1_000 ### valor provisional
pendiente de revisión ### morale = 100%

```
**60.4 No anidamiento**
Los comentarios multilínea no pueden anidarse.
Esto es inválido o se interpreta cerrando el comentario en el primer delimitador ### posterior:
```
###
comentario exterior
    ### comentario interior ###
continuación
###

```
El compilador debe diagnosticar delimitadores sobrantes cuando produzcan texto inválido.
**60.5 Prioridad léxica**
El lexer debe reconocer ### antes que #.
Por tanto:
```
###
comentario
###

```
se interpreta como un único comentario multilínea y no como varios comentarios de línea.
Fuera de una cadena:
* ### abre o cierra un comentario multilínea.
* # abre o cierra un comentario de línea.
* Un salto de línea cierra cualquier comentario de línea que siga abierto.
**60.6 Comentarios y terminadores**
El contenido de un comentario no genera instrucciones ni terminadores.
```
soldiers = 1_000 # ; } then {

```
Los símbolos ;, { y } contenidos en el comentario no participan en la sintaxis.
Después de retirar léxicamente el comentario, el código restante debe seguir siendo válido.

 
⸻
 
## 61. Terminadores
Salto de línea o ;.
 
⸻
 
## 62. Lectura y escritura externas
> [!warning] Frontera pública sustituida
> La escritura entra mediante `action`; la lectura declarativa se expresa mediante `look`; y los eventos de salida mediante `message`, cuyos campos se evalúan tras estabilizar la acción causante. Véase D-027.
## 62.1 Lectura
Puede leer campos y reglas booleanas.
## 62.2 Escritura
Toda escritura externa usa acciones.
## 62.3 Contrato generado
Incluye:
* Participantes on.
* Valores given.
* Dominios de given.
* if.
* after.
* Lecturas.
* Escrituras.
* Estocasticidad.
* Resultados.
 
⸻
 
## 63. Grafo semántico
> [!warning] Catálogo histórico
> Los nodos y aristas son un boceto. Deben migrarse de `construct`/`from` a `thing`/`as`, incorporar `look`, `message`, actividad lógica y dependencias de lectura diferida, y validarse contra D-014–D-027.
## 63.1 Nodos
* Constructo.
* Alias.
* Componente.
* Campo.
* Dominio.
* Magnitud.
* Unidad.
* Regla booleana.
* Regla reactiva.
* Regla always.
* Acción.
* Participante.
* Valor given.
* Patrón de vinculación.
* allowed.
* eventually.
## 63.2 Relaciones
```
IS

DECLARES_ALIAS_COMPONENT
ALIAS_COMPONENT_TYPE

DECLARES_FIELD
FIELD_TYPE
FIELD_DOMAIN

DECLARES_VALUE
VALUE_ORDER

DECLARES_UNIT
UNIT_EQUIVALENT
POINT_OVER

DECLARES_PARTICIPANT
PARTICIPANT_TYPE
PARTICIPANT_MUTABLE
PARTICIPANT_IN
PARTICIPANT_MODE_ON
PARTICIPANT_MODE_FOR

DECLARES_GIVEN
GIVEN_TYPE
GIVEN_DOMAIN

READS
WRITES
RULE_QUERIES
RULE_DEPENDS_ON

WHEN_READS
WHEN_RULE
WHEN_CHANGES

IF_READS
IF_RULE

AFTER_READS
AFTER_RULE
AFTER_OLD_READS

ALWAYS_READS
ALWAYS_RULE

ACTION_CALLS
ACTION_BINDS_PARTICIPANT
ACTION_BINDS_GIVEN

ALLOWED_ACTION
ALLOWED_DEPENDS_ON

EVENTUALLY_TARGET
EVENTUALLY_THROUGH

CREATES
DESTROYS
ADDS_TO
REMOVES_FROM
MOVES_FROM
MOVES_TO

DERIVES_FROM
DEPENDS_ON
STOCHASTIC_DEPENDENCY
DOMAIN_DEPENDENCY

```
 
⸻
 
## 64. Representación intermedia
> [!warning] Ejemplos no normativos
> El JSON de esta sección es ilustrativo y usa modos de participantes, tipos y nodos retirados. El esquema canónico y versionado continúa abierto en Q-009.
## 64.1 Regla booleana
```
{
  "kind": "booleanRule",
  "anchor": "rule::chess.InCheck",
  "participantMode": "on",
  "participants": [
    {
      "role": null,
      "type": "construct::chess.Game"
    }
  ],
  "given": [
    {
      "name": "side",
      "type": "construct::chess.Side"
    }
  ]
}

```
## 64.2 Acción
```
{
  "kind": "action",
  "anchor": "action::warfare.Recruit",
  "participantMode": "on",
  "participants": [
    {
      "role": null,
      "type": "construct::world.Kingdom",
      "mutable": true
    }
  ],
  "given": [
    {
      "name": "amount",
      "type": "Natural",
      "domain": {
        "kind": "interval",
        "minimum": 1,
        "maximum": 100
      }
    }
  ],
  "condition": {
    "kind": "expression"
  },
  "after": null,
  "bodyKind": "effects",
  "effects": []
}

```
La capa IR puede denominar técnicamente inputs a estos valores si una tecnología de destino lo exige, pero la representación canónica de MUD debe preservar que fueron declarados mediante given.
## 64.3
```
allowed
{
  "kind": "allowed",
  "action": "action::chess.Move",
  "participants": [],
  "given": [],
  "randomMode": "seededSpeculation"
}

```
 
⸻
 
## 65. Compilador
Debe incluir:
1. Lexer.
2. Parser.
3. AST.
4. Símbolos.
5. Imports.
6. Anclas.
7. Aliases.
8. Tipos.
9. Dominios.
10. Cardinalidades.
11. Mutabilidad.
12. Herencia.
13. Magnitudes.
14. Reglas on.
15. Reglas for.
16. Reglas always.
17. Acciones on.
18. Participantes.
19. Valores given.
20. Llamadas.
21. Receptores multiparte.
22. Composición.
23. after.
24. old.
25. allowed.
26. Ciclos de admisibilidad.
27. eventually.
28. Enumerabilidad.
29. Finitud.
30. Terminación.
31. Estocasticidad.
32. Grafo.
33. IR.
34. Diagnósticos.
35. Formateador.
 
⸻
 
## 66. Materialización TypeScript
Puede utilizar conceptos técnicos internos como:
* Funciones.
* Parámetros.
* Inputs.
* Maps.
* Tuplas.
* Mundos especulativos.
* Transacciones.
* Exploración exhaustiva.
Pero no debe cambiar la semántica declarada mediante on y given.
 
⸻
 
## 67. Plugin para Codex
## 67.1
```
mud-model-query

```
Consulta:
* Participantes on.
* Vinculaciones for.
* Valores given.
* Dominios.
* Reglas.
* Acciones.
* Admisibilidad.
* Alcanzabilidad.
## 67.2
```
mud-rule-management

```
Gestiona:
* Reglas on.
* Reglas for.
* Reglas always.
* Participantes.
* Valores given de reglas.
* Llamadas.
* Pureza.
* allowed.
## 67.3
```
mud-action-management

```
Gestiona:
* Acciones on.
* Participantes.
* Valores given.
* Dominios.
* if.
* then.
* after.
* old.
* Composición.
* Contratos.
* Ciclos.
El resto de herramientas se mantiene vigente.
 
⸻
 
## 68. Clasificación de peticiones
Toda petición se clasifica antes de modificar:
1. Consulta.
2. Creación.
3. Lectura.
4. Actualización.
5. Retirada.
6. Transacción compuesta.
7. Cambio estructural.
8. Cambio de API.
9. Cambio causal.
10. Cambio de vinculación.
11. Cambio de dominio.
12. Cambio de alias.
13. Cambio de participantes on.
14. Cambio de vinculaciones for.
15. Cambio de valores given.
16. Cambio de aleatoriedad.
17. Cambio de after.
18. Cambio de always.
19. Cambio de admisibilidad.
20. Cambio de alcanzabilidad.
21. Ambigua.
22. Incompleta.
23. Fuera de alcance.
24. Intento de saltarse restricciones.
 
⸻
 
## 69. Inferencias permitidas
Codex puede aplicar:
* Participante único anónimo.
* given ausente cuando no se necesitan valores.
* [1] predeterminado.
* empty.
* Orden lexicográfico.
* Dominios finitos derivados.
Codex no puede inventar:
* Participantes.
* Valores given.
* Dominios.
* Reglas.
* Acciones.
* after.
* always.
* Semántica de allowed.
* Transiciones de eventually.
 
⸻
 
## 70. Agenda de especificación
Se mantienen los campos, estados y procedencias vigentes.
 
⸻
 
## 71. Flujo atómico del plugin
Se mantiene:
1. Clasificar.
2. Resolver.
3. Consultar grafo.
4. Impacto.
5. Ambigüedades.
6. Operaciones.
7. Restauración.
8. Editar .mud.
9. Agenda.
10. Grafo.
11. IR.
12. Materializar.
13. Tests.
14. Validar.
15. Diff.
16. Rutas.
17. Commit.
 
⸻
 
## 72. Tests
> [!warning] Suite histórica
> Los casos sobre `on`, `for`, `construct`, creación, destrucción y cardinalidad contradicen decisiones posteriores. La futura suite de conformidad debe derivarse de la especificación formal y de D-014–D-027.
## 72.1 Participantes y
```
given

```
Cubrir:
* Regla on sin given.
* Regla on con given.
* Acción on sin given.
* Acción on con given.
* Participante único anónimo.
* Varios participantes.
* Receptor multiparte.
* Vinculación posicional.
* Vinculación nombrada.
* Dominio de given.
* Ausencia de antigua palabra clave input.
* Rechazo de for en acciones.
* Rechazo de on en reglas reactivas.
* Rechazo de given en reglas reactivas.
* Rechazo de given en always rule.
## 72.2 Contratos
Cubrir:
* Separación entre participantes y given.
* IR con participantMode: "on".
* API externa.
* Composición de acciones.
* allowed.
* Enumeración de given para eventually.
El resto de grupos de tests se mantiene vigente.
 
⸻
 
## 73. Soporte de editor
Debe mostrar claramente:
* Participantes on.
* Vinculaciones for.
* Valores given.
* Dominios de given.
* Diferencia entre regla consultable, reactiva y always.
* Firma de acciones.
* Firma de reglas.
 
⸻
 
## 74. Palabras clave provisionales
> [!warning] Catálogo sustituido
> Esta lista no es el léxico vigente: `thing` sustituye a `construct`; `as` declara especialización; `look` y `message` son entidades nuevas; `root unit`, `:=`, `point over`, `cycle`, `in` y `to` tienen los usos de D-028–D-030; `equivalent` y `reflexive` no pertenecen a esas formas actuales. El catálogo normativo futuro será `45-palabras-reservadas.md`.
```
abstract
construct
alias
magnitude
unit
values
ordered
is
using
mut

rule
action

on
for
given
always

when
changes
if
then
after
old

allowed
eventually
through

each
in
by

exists
forall
count
sum
min
max

add
remove
move
all
from
to

create
destroy

unique
empty

true
false

not
and
or
implies
iff

union
intersection
xor
except

as
Rand

point
over
cycle
format

name
plural
abbreviation
equivalent
prefixes

```
La palabra clave:
```
input

```
queda retirada del lenguaje.
Puede seguir existiendo como término técnico interno en herramientas o tecnologías de destino, pero no forma parte de la sintaxis .mud.
 
⸻
 
## 75. Ejemplo integral actualizado
> [!danger] Ejemplo histórico no conforme
> Este ejemplo usa `construct`, herencia mediante `is`, la distribución antigua de `on`/`for` y otras reglas retiradas. Sirve como procedencia de requisitos, no como programa ejecutable ni como ejemplo de MUD vigente.
```
using economy.resources
using warfare.armies.*

construct Side {
    values =
        North,
        South
}

alias Coordinate {
    horizontal: Natural in 1..8
    vertical: Natural in 1..8
}

magnitude Duration {
    unit second {
        name = "second"
        plural = "seconds"
        abbreviation = "s"

        prefixes =
            milli,
            micro,
            nano
    }

    unit minute {
        name = "minute"
        plural = "minutes"
        abbreviation = "min"
        equivalent = 60 seconds
    }

    unit hour {
        name = "hour"
        plural = "hours"
        abbreviation = "h"
        equivalent = 60 minutes
    }

    unit day {
        name = "day"
        plural = "days"
        abbreviation = "d"
        equivalent = 24 hours
    }
}

abstract construct Place {
    name: Text = ""
}

abstract construct MilitaryForce {
    name: Text = ""

    mut soldiers: Natural = 0
    mut morale: Percentage in 0%..100% = 100%

    strength: Number :=
        soldiers * morale
}

abstract construct Army is MilitaryForce {
    maintenancePerSoldier: Money = 1M

    initiative: Natural =
        Rand(1..100)

    combatRoll: Natural :=
        Rand(1..6)

    maintenanceCost: Money :=
        soldiers * maintenancePerSoldier
}

construct EarthForce is Army {
    name = "Earth Force"
    soldiers = 2_000
}

construct WaterForce is Army {
    name = "Water Force"
    soldiers = 1_000
}

construct Gate {
    mut unlocked: Boolean = false
    mut open: Boolean = false
}

construct World {
    mut currentDate: Date
    mut kingdoms: Kingdom [* mut]
}

construct Kingdom is Place {
    mut treasury: Money in 0M..1_000_000M = 0M
    mut stability: Percentage in 0%..100% = 100%
    mut population: Natural = 0
    mut soldiers: Natural = 0
    mut starving: Boolean = false

    recruitmentCost: Money = 2M

    mut armies: Army [* mut unique ordered]
    mut reserve: Army [* mut]
    mut stock: Resource -> Number [*]

    totalMaintenance: Money :=
        sum army in armies:
            army.maintenanceCost
}

construct Egypt is Kingdom {
    name = "Egypt"
    treasury = 10_000M
    population = 5_000_000

    armies =
        EarthForce,
        WaterForce

    stock =
        Grain -> 2_000,
        Bronze -> 500
}

rule IsDestroyed on Army {
    soldiers <= 0
}

rule IsReady on Army {
    morale >= 70%
}

rule HasDestroyedArmies on Kingdom {
    exists army in armies:
        army.IsDestroyed()
}

rule CanAttack on
    attacker: Army,
    defender: Army
given
    maximumDistance: Length
{
    attacker != defender
        & !attacker.IsDestroyed()
        & !defender.IsDestroyed()
        & attacker.distanceTo[defender] <= maximumDistance
}

rule OpenGate for Gate [mut] {
    when unlocked

    then {
        open = true
    }
}

rule CloseGate for Gate [mut] {
    when !unlocked

    then {
        open = false
    }
}

rule ApplyStarvation for
    world: World,
    kingdom in world.kingdoms [mut]
{
    when world.currentDate changes

    if kingdom.starving

    then {
        kingdom.population -= 100
        kingdom.stability -= 1%
    }
}

rule RemoveDestroyedArmies for Kingdom [mut] {
    when HasDestroyedArmies()

    then {
        remove all army from armies:
            army.IsDestroyed()
    }
}

rule MobilizeReserve for Kingdom [mut] {
    when exists army in reserve:
        army.IsReady()

    then {
        move all army from reserve to armies:
            army.IsReady()
    }
}

always rule ValidKingdom for Kingdom {
    stability in 0%..100%
        & treasury >= 0M
}

action Recruit on Kingdom [mut]
given
    amount: Natural in 1..10_000
{
    if treasury >= amount * recruitmentCost

    then {
        treasury -= amount * recruitmentCost
        soldiers += amount
    }

    after {
        soldiers >= old soldiers
    }
}

rule CanRecruit on Kingdom
given
    amount: Natural in 1..10_000
{

```
```
    allowed Recruit(amount)
}

```
```

action Attack on
    attacker: Army,
    defender: Army [mut]
{
    if attacker != defender
        & !attacker.IsDestroyed()
        & !defender.IsDestroyed()

    then {
        defender.soldiers -= attacker.attackDamage
        defender.morale -= 5%
    }
}

action Clash on
    left: Army [mut],
    right: Army [mut]
{
    then {
        (left, right).Attack()
        (right, left).Attack()
    }
}

action AdvanceDay on World [mut] {
    then {
        currentDate += 1 day
    }
}

```
 
⸻
 
## 76. Decisiones vigentes esenciales
> [!danger] Lista congelada y sustituida
> Ninguna entrada de esta sección debe asumirse vigente por aparecer aquí. La autoridad es [[notas/10-registro-de-decisiones]], que registra también D-014–D-027 y las decisiones sustituidas.
1. .mud es la fuente semántica de verdad.
2. MUD es un lenguaje de programación declarativo.
3. Las declaraciones principales son construct, magnitude, rule y action.
4. alias declara tipos auxiliares de valor.
5. on declara participantes suministrados al consultar o solicitar una declaración.
6. Las reglas booleanas utilizan on.
7. Las acciones utilizan on.
8. for se reserva para vinculaciones automáticas.
9. Las reglas reactivas utilizan for.
10. Las reglas always utilizan for.
11. given se utiliza tanto en reglas booleanas como en acciones.
12. given es opcional.
13. input deja de ser palabra clave de MUD.
14. Los participantes son cosas existentes.
15. Los valores given no ocupan roles de participante.
16. Un participante único puede ser anónimo.
17. Una regla de participante único se consulta como participant.Rule(...).
18. Una acción de participante único se solicita como participant.Action(...).
19. Varios participantes usan (a, b).Rule(...) o (a, b).Action(...).
20. Los argumentos de la llamada corresponden a given.
21. Participantes y given siguen siendo grupos semánticamente separados.
22. Las reglas reactivas y always no declaran given.
23. Las acciones no utilizan for.
24. input puede existir como término interno de implementación, pero no en .mud.
25. Los contratos generados conservan la separación entre participantes y given.
26. El resto de decisiones sobre aliases, dominios, intervalos, acciones, ondas, after, old, allowed, eventually, aleatoriedad, diccionarios y rollback permanece vigente.
 
⸻
 
## 77. Cuestiones abiertas prioritarias
> [!danger] Agenda congelada y sustituida
> La agenda vigente es [[notas/08-preguntas-abiertas]]. Algunas preguntas de esta lista ya se cerraron y otras nuevas no aparecen aquí.
1. Gramática formal completa.
2. Sintaxis canónica de vinculación nombrada de participantes.
3. Sintaxis canónica de valores given nombrados.
4. Restricciones relacionales declarativas entre varios participantes on.
5. Varias acciones dentro de eventually.
6. Cálculo formal del estado relevante.
7. Límites del análisis de finitud.
8. Límites del análisis de terminación.
9. Canonicalización de constructos runtime.
10. Dominios dinámicos circulares.
11. Intervalos discontinuos canónicos.
12. Orden descendente.
13. Varias claves.
14. Redondeo de Money.
15. Conversiones estrechas.
16. Límites numéricos.
17. División por cero.
18. Subsemillas.
19. Cachés estocásticas.
20. Exposición de campos estocásticos.
21. Oscilaciones.
22. Límite de ondas.
23. Estructura del error técnico.
24. Valores de retorno de acciones.
25. Composición dinámica.
26. Campos específicos de values.
27. Herencia de familias cerradas.
28. Calendarios.
29. Localización.
30. Magnitudes derivadas.
31. Migración de anclas.
32. Destrucción de constructos estáticos.
33. Análisis estático de conflictos.
34. Perfil de mundos finitos.
35. Subconjunto formalmente no Turing completo.
 
⸻
 
## 78. Instrucciones finales para Codex
> [!danger] Instrucciones retiradas
> Estas instrucciones pertenecen al prompt histórico y no gobiernan el repositorio. Se aplican `AGENTS.md`, `gobierno/`, `especificacion/`, los ADR vigentes y la agenda actual.
Al trabajar sobre MUD:
* Conserva .mud como fuente de verdad.
* No introduzcas semántica solo en derivados.
* No cierres cuestiones abiertas silenciosamente.
* Usa on para reglas booleanas.
* Usa on para acciones.
* Usa for para reglas reactivas.
* Usa for para reglas always.
* No utilices for en acciones.
* Usa given para valores suministrados a reglas booleanas.
* Usa given para valores suministrados a acciones.
* No utilices input en archivos .mud.
* Distingue participantes de valores given.
* Conserva esa separación en IR, API, tooling y documentación.
* Usa receptores para participantes.
* Usa argumentos para valores given.
* Mantén las reglas booleanas puras.
* Mantén las acciones como API de escritura.
* No permitas given en reglas reactivas ni always.
* Evalúa dominios de given antes del if.
* Un given fuera de dominio en una acción produce rejected.
* Un given fuera de dominio en una regla produce false.
* Conserva aliases, identidad, dominios e intervalos.
* Conserva after después de todas las ondas.
* Conserva old respecto al estado inicial de la acción completa.
* Conserva allowed como consulta especulativa.
* Propaga sus fallos.
* Conserva su aleatoriedad reproducible.
* Permite eventually solo con prueba de finitud y terminación.
* Mantén BFS causal.
* No publiques estados parciales.
* Haz rollback ante fallos.
* Actualiza tests, grafo, IR y documentación.
* Inspecciona el diff.
* Crea commits semánticos atómicos.
* Implementa pruebas verticales pequeñas.
* No intentes construirlo todo de una vez, porque hasta los compiladores necesitan que alguien les impida tomar decisiones impulsivas.
