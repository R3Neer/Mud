---
id: D-078
title: "Resolución nominal, catálogo de anclas y grafo inicial"
status: vigente
date: 2026-08-03
supersedes: []
superseded-by: []
questions:
  - "Q-014"
affects:
  - "capítulo 09, resolución, AST resuelto, anclas, diagnósticos, LSP y grafo"
---
# ADR-078 — Resolución nominal, catálogo de anclas y grafo inicial

- Amplía: [[ADR-035-organizacion-nombres-using-y-anclas|D-035]] y [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]].

## Decisión

La norma denomina **path de MUD** a la identidad lógica derivada de las carpetas. No se escribe una cabecera `namespace` ni se reserva `path`. El LSP puede mostrar una cabecera virtual, copiar el nombre cualificado y revelar la procedencia física sin modificar el archivo.

Todas las declaraciones superiores de un path comparten un espacio nominal. La búsqueda de un nombre no cualificado consulta, en orden, entorno léxico, propietario o receptor implícito, path actual, `using` exactos, `using` recursivos e incorporados. Se elige el primer nivel no vacío; una categoría incompatible no habilita continuar. Candidatos con la misma ancla se deduplican y anclas distintas son ambiguas. Un `using` no reexporta.

No existe sombreado de un nombre visible. Las convenciones `PascalCase`, `lowerCamel` y `lowerCamel` de unidad son requisitos estáticos con arreglo automático.

Poseen ancla las declaraciones globales, campos en su propietario original, componentes, miembros de family, unidades declaradas y tipos incorporados. Un campo heredado conserva el ancla declarativa del antecesor aunque su estado sea independiente en cada `thing`. Roles, `given`, iteradores, vinculaciones locales y valores globales no nominales solo reciben identidad interna efímera.

Las categorías canónicas son `thing`, `alias`, `family`, `magnitude`, `unit`, `rule`, `action`, `look`, `message`, `test` y `type`. Las declaraciones anidadas prolongan el ancla del propietario con `::<miembro>`; un `start with` global no tiene nombre ni ancla.

La resolución se ejecuta por etapas: primero símbolos nominales, después tipos y dominios, y finalmente miembros dependientes del tipo. La norma usa entornos y conjuntos de candidatos; un scope graph es una implementación posible, no autoridad.

Tras resolver nombres puede construirse el esqueleto del grafo con aristas de propiedad, especialización, referencia, tipo, dominio, inicialización, cálculo y efecto. El tipado completa y valida aristas posteriores sin impedir construir este grafo nominal inicial.

## Migraciones

Una ancla cambia con categoría, path o nombre cualificado. El tooling conserva una correspondencia dirigida explícita para migrar referencias persistentes, pero el ancla anterior no se convierte en alias fuente. Q-014 conserva abiertos el formato externo, composición, colisiones, conservación y aplicación sobre mundos persistidos.

## Verificación

1. Primer nivel no vacío y categoría incompatible sin caída posterior.
2. Colisión global entre categorías.
3. Deduplicación por ancla y ambigüedad real.
4. Ausencia de sombreado y errores de casing reparables.
5. Anclas de campos heredados, members, unidades y builtins.
6. Símbolos locales sin ancla pública.
7. Grafo nominal construible antes del tipado completo.
