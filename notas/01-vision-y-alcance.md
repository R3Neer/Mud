# Visión y alcance

## Tesis del producto

MUD propone que la lógica de un sistema tenga una representación propia, explícita y estable, independiente de la implementación que la ejecuta. Esa representación vive en archivos `.mud`; el código generado, los índices y el grafo son proyecciones sustituibles.

La interacción ordinaria no tiene por qué parecerse a programar en MUD. La persona expresa una intención en lenguaje natural y el sistema:

1. Localiza las anclas afectadas.
2. Consulta dependencias y decisiones previas.
3. Expone ambigüedades e impacto.
4. Formula operaciones semánticas.
5. Modifica el modelo de forma atómica.
6. Valida el nuevo estado.
7. Regenera derivados.
8. Registra el cambio en Git.

El lenguaje es, por tanto, una interfaz interna estable entre intención humana e implementación técnica.

## Problema que intenta resolver

En un sistema convencional, el significado del dominio queda repartido entre código, base de datos, tests, documentación, configuración y decisiones implícitas. Cambiar de arquitectura puede obligar a reconstruir ese significado a partir de sus efectos.

MUD intenta invertir esa relación:

- La semántica de dominio se declara una sola vez.
- Las dependencias pueden consultarse antes de modificar.
- El historial describe cambios semánticos, no solo líneas editadas.
- Una implementación puede regenerarse sin redefinir el mundo.
- Una IA puede operar sobre elementos con identidad estable en vez de improvisar cambios textuales.

## Usuarios y casos iniciales

El caso de uso inicial son videojuegos y simulaciones con muchas reglas relacionadas. Es una buena frontera de aprendizaje porque exige:

- Estado mutable.
- Relaciones y colecciones.
- Reglas reactivas.
- Invariantes.
- Acciones rechazables.
- Consecuencias encadenadas.
- Azar reproducible.
- Preguntas hipotéticas.

La primera experiencia de usuario es la de una persona diseñadora de dominio asistida por IA, no la de una persona que escribe cada declaración manualmente. Aun así, el lenguaje debe ser legible, diagnosticable y editable por humanos, porque es la fuente de verdad y la última superficie de inspección.

## Límites del dominio

MUD describe:

- Qué cosas y valores existen.
- Qué propiedades y relaciones poseen.
- Qué condiciones pueden consultarse.
- Qué acciones pueden intentarse.
- Qué efectos y reacciones producen.
- Qué restricciones deben conservarse.
- Qué resultado estable se obtiene.

MUD no describe:

- Interfaz gráfica.
- Persistencia.
- Red.
- Autenticación.
- Infraestructura.
- Arquitectura de aplicación.
- Frameworks, motores o plataformas.
- Algoritmos de presentación o despliegue.

Una materialización puede decidir todo lo anterior, pero no puede añadir comportamiento de dominio ausente del modelo.

## Capas del producto

Conviene hablar de cuatro capas para evitar confundir objetivos:

1. **Modelo**: archivos `.mud` y sus reglas normativas.
2. **Motor semántico**: compilación, validación y ejecución causal.
3. **Operador semántico**: herramientas que consultan y modifican el modelo mediante anclas.
4. **Materialización**: código o contratos para una tecnología concreta.

La interfaz en lenguaje natural está encima del operador semántico; no forma parte de la gramática MUD.

## Promesas esenciales

Si el proyecto funciona, debería poder prometer:

- **Conservación de significado**: la lógica relevante está en `.mud`.
- **Atomicidad**: nunca se publica medio cambio.
- **Explicabilidad**: se pueden enumerar anclas leídas, escritas y afectadas.
- **Reproducibilidad**: el mismo modelo, entradas y semilla producen el mismo resultado.
- **Reconstrucción**: los derivados se regeneran desde la fuente.
- **Trazabilidad**: cada cambio válido tiene intención, operaciones y commit.
- **Sustituibilidad**: la materialización no aprisiona el modelo.

## Criterios de éxito de una primera versión

La primera versión no necesita expresar toda la especificación. Sí necesita demostrar de extremo a extremo que:

1. Un modelo pequeño puede escribirse y validarse.
2. Sus símbolos y anclas son estables.
3. Una acción produce un cambio causal determinista o revierte.
4. El impacto puede explicarse antes de editar.
5. Un cambio semántico puede aplicarse, probarse y convertirse en un commit aislado.
6. Un derivado sencillo puede regenerarse sin ser fuente de comportamiento.

## No objetivos tempranos

- Ser un lenguaje de propósito general.
- Sustituir todos los lenguajes de implementación.
- Generar una aplicación completa.
- Resolver desde el inicio `eventually`, azar, calendarios y herencia múltiple.
- Aceptar cualquier petición ambigua sin intervención humana.
- Garantizar propiedades formales que todavía no han sido demostradas.

