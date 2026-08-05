---
id: D-083
title: "Magnitudes base sin unidades"
status: vigente
date: 2026-08-04
supersedes: []
superseded-by: []
questions: []
affects:
  - "magnitudes, tipos, conversiones cuantitativas, plantillas `Text` y frontera pública"
---
# ADR-083 — Magnitudes base sin unidades

- Modificada por: [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]]
- Modifica: [[notas/decisiones/ADR-027-salidas-look-y-message|D-027]], [[notas/decisiones/ADR-028-sistema-de-magnitudes-y-unidades|D-028]], [[notas/decisiones/ADR-030-conversion-cuantitativa-explicita|D-030]] y [[notas/decisiones/ADR-061-resultados-fallidos-y-plantillas-text|D-061]].
- Documentos afectados: magnitudes, tipos, conversiones cuantitativas, plantillas `Text` y frontera pública.

## Contexto

La gramática y el AST ya permitían omitir `root unit` en una magnitud base, y `Probability` aparecía como ejemplo normativo. Sin embargo, las reglas de presentación y de campos públicos suponían después que toda magnitud lineal poseía una unidad raíz o una composición de unidades raíz. Quedaba sin fijar si la omisión era deliberada, cómo se construía un valor así y si perder la escritura de unidad eliminaba también su identidad dimensional.

Exigir una unidad raíz obligaría a inventar etiquetas ceremoniales para cantidades como probabilidad, opacidad o dificultad. Tratar todas ellas como el mismo número adimensional, por otra parte, perdería la separación nominal que justifica declararlas como magnitudes diferentes.

## Decisión

### Declaración

Una magnitud base declara una de estas dos formas:

1. **Con unidades**: contiene exactamente una `root unit` y puede contener unidades alternativas.
2. **Sin unidades**: su cuerpo está vacío y no puede contener unidades alternativas.

```mud
magnitude Probability: Num in [0..1] {}

magnitude Length: Num in [0..*] {
    root unit meter {}
}
```

La ausencia de `root unit` es una elección semántica completa, no una unidad anónima ni una declaración incompleta.

### Identidad cuantitativa

Una magnitud base sin unidades conserva una dimensión nominal independiente. No se identifica con su representación numérica ni con otra magnitud sin unidades:

```mud
magnitude Probability: Num in [0..1] {}
magnitude Opacity: Num in [0..1] {}
```

`Probability`, `Opacity` y `Num` continúan siendo tipos distintos y no se convierten implícitamente entre sí. La ausencia de unidad visible tampoco significa que el factor desaparezca del álgebra dimensional. Una multiplicación o división conserva el factor nominal de la magnitud y la normalización no lo confunde con el elemento neutro dimensional.

La representación interna de una dimensión distingue, por tanto, sus factores nominales de su **proyección de unidades**. Los factores cuyas magnitudes poseen unidad raíz contribuyen a esa proyección; los factores sin unidades permanecen en la dimensión, pero no producen texto de unidad. Dos dimensiones con la misma proyección visible pueden seguir siendo incompatibles.

### Construcción y conversión

Un literal numérico desnudo puede elaborarse como una magnitud sin unidades cuando el contexto esperado determina una única magnitud:

```mud
chance: Probability = 0.75
```

Sin ese contexto, el literal conserva un tipo numérico básico. Una expresión numérica ordinaria no adquiere implícitamente una magnitud. La materialización explícita usa `to`:

```mud
chance := ratio to Probability
```

Esta rama de `to` exige una representación numérica compatible y comprueba el dominio de destino. No autoriza convertir una magnitud nominal distinta solo porque ambas carezcan de unidad.

Una cantidad que escribe una unidad, como `5 m`, adquiere únicamente los factores determinados por esa unidad. El contexto no añade factores sin unidad de manera silenciosa. Esos factores deben proceder de un operando ya tipado o de una conversión explícita válida.

### Presentación

La forma canónica de una magnitud base sin unidades es la forma canónica de su valor numérico, sin sufijo ni espacio final:

```mud
chance: Probability = 0.75
text := "Chance: {chance}"  # Chance: 0.75
```

En una magnitud derivada, la presentación canónica escribe la proyección de unidades de su dimensión. Los factores procedentes de magnitudes sin unidades conservan su significado estático, pero no añaden una etiqueta visible. Si la proyección es vacía, se escribe solo el número.

El operador de presentación `in` no puede aplicarse a una magnitud base sin unidades. Sobre una magnitud derivada puede cambiar la proyección expresable mediante unidades sin retirar ni sustituir sus factores nominales sin unidad.

Un campo público cuyo valor directo sea una magnitud sin unidades no recibe el aviso por omitir `in`: no existe una decisión de unidad que hacer explícita. La regla ordinaria de aviso continúa aplicándose cuando la magnitud sí admite una presentación mediante unidades.

## Alternativas

### Exigir siempre una unidad raíz

Se rechaza porque convertiría etiquetas como `probability` o `scorePoint` en ceremonia obligatoria y haría menos natural la escritura habitual de esas cantidades.

### Tratar la ausencia de unidad como dimensión neutra

Se rechaza porque haría compatibles por dimensión magnitudes nominalmente distintas como `Probability` y `Opacity`, y borraría factores al participar en expresiones derivadas.

### Usar aliases en todos los casos sin unidad

Se rechaza como obligación. Un alias sigue siendo apropiado para envolver datos sin semántica cuantitativa dimensional, pero una magnitud sin unidades conserva dominios, representación numérica y participación en el álgebra de magnitudes.

## Consecuencias

- La opcionalidad de `root_unit` en `BaseMagnitudeDecl` es semántica e intencionada.
- El resolvedor dimensional debe conservar factores nominales aunque no tengan forma de unidad.
- La presentación de una dimensión es una proyección y no determina por sí sola su identidad.
- Los diagnósticos de API solo sugieren `in` cuando existe una unidad seleccionable.
- Una implementación no puede inventar una unidad sintética observable para completar una magnitud sin unidades.

## Verificación

1. Aceptación de una magnitud base con cuerpo vacío y rechazo de unidades alternativas sin raíz.
2. Elaboración contextual de `0.75` como `Probability` y conservación numérica sin contexto.
3. Materialización explícita `ratio to Probability`, incluida la comprobación de dominio.
4. Rechazo de conversión implícita entre dos magnitudes sin unidades.
5. Conservación del factor nominal sin unidad en productos y cocientes derivados.
6. Renderización sin sufijo de una magnitud cuya proyección de unidades sea vacía.
7. Ausencia de aviso de unidad en un campo público de magnitud sin unidades.
8. Rechazo de `chance in unit` para una magnitud base sin unidades.
