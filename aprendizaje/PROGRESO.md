---
title: Progreso de formalización
tags:
  - mud/aprendizaje
  - mud/progreso
status: activo
---

# Progreso de formalización

## Estado general

- Etapa: grafo almacenado y efectivo de `thing`.
- Nivel global orientativo: 0 → 1 — demostración e imitación.
- Unidad completada: [[aprendizaje/unidades/01-modelo-minimo-de-un-mundo]].
- Unidad actual: [[aprendizaje/unidades/02-constructos-como-orden-parcial]].
- Unidad siguiente: [[aprendizaje/unidades/03-esquema-heredable-y-estado-independiente]].
- Especificación relacionada: [[especificacion/03-notacion]] y [[especificacion/04-modelo-matematico]].

## Competencias

| Competencia | Nivel | Evidencia | Próximo repaso |
| --- | ---: | --- | --- |
| Leer y escribir conjuntos | Nivel 1 demostrado | [[aprendizaje/historico/01-modelo-clase-instancia/01-modelo-minimo-respuesta-historica|Respuesta histórica 01]] | Unidad 02 |
| Distinguir conjunto, secuencia y multiconjunto | Introducido parcialmente | Conjunto frente a secuencia en Unidad 01 | Unidad posterior |
| Usar funciones y funciones parciales | Nivel 1 demostrado | [[aprendizaje/historico/01-modelo-clase-instancia/01-modelo-minimo-respuesta-historica|Respuesta histórica 01]] y objeción sobre $I_G$ | Unidad 02 |
| Distinguir función y relación | Introducido | Demostración de especialización múltiple en Unidad 02 | Ejercicio 02 |
| Leer grafos y caminos | Introducido | Grafos almacenado y efectivo de `thing` en Unidad 02 | Ejercicio 02 |
| Distinguir definición canónica, activación inicial, materialización y actividad | Introducido | Unidad 01 actualizada y D-054 | Unidad 02 |
| Calcular clausuras de relaciones | Introducido | Demostración resuelta en Unidad 02 | Ejercicio 02 |
| Reconocer órdenes parciales | Introducido | Proposición de aciclicidad en Unidad 02 | Ejercicio 02 |
| Leer juicios formales | Introducido | Juicio $P\vdash W\ \mathsf{wf}$ en Unidad 01 | Unidad posterior |
| Leer reglas de inferencia | Introducido | Ejemplo de suma y dominio | Unidad posterior |
| Escribir EBNF | Sin evaluar | — | Unidad de gramática |
| Definir semántica estática | Sin evaluar | — | Unidad posterior |
| Probar cardinalidades con intervalos abstractos | Sin evaluar | D-026 fija la obligación del compilador | Unidad de colecciones y efectos |
| Definir semántica operacional | Sin evaluar | — | Unidad posterior |
| Construir contraejemplos | Introducido | Redundancia de $I_G$ en el trabajo histórico y dominio del store actual | Unidad 02 |
| Escribir una demostración | Demostración leída | Prueba de que $R^*$ es orden parcial en Unidad 02 | Unidad posterior |

## Decisiones didácticas

- Se acepta notación matemática completa cuando aporte precisión.
- La base académica y la audiencia se describen en [[PERFIL]].
- Los fundamentos conocidos se repasarán con concisión y aplicación inmediata, sin asumir iniciación absoluta.
- Las unidades se redactarán para poder reutilizarse con lectores de formación diferente.
- Toda técnica nueva comienza con una demostración resuelta.
- La responsabilidad se transferirá gradualmente según [[REGLAS-DIDACTICAS]].
- Los primeros trabajos del autor serán locales; los capítulos completos llegarán en niveles 3 y 4.

## Registro de unidades

| Unidad | Tema | Nivel | Estado | Resultado |
| --- | --- | ---: | --- | --- |
| 00 | Arquitectura de la especificación | 0 | Completada | Índice maestro |
| 01 | Programa, mundo y store mínimo | 0 → 1 | Contenido actualizado | Competencias previas conservadas; ejercicio actual opcional; versión descartada archivada |
| 02 | `Thing` como orden parcial | 0 → 1 | En curso | Incluye grafo almacenado, proyección efectiva, bypass y membresía estricta |
| 03 | Esquema heredable y estado independiente | 1 → 2 | Planificada y alineada | Se activará tras revisar la respuesta 02 actual |

## Errores recurrentes

- Conviene mantener exactamente los subíndices de funciones ya definidas.
- La escritura de LaTeX todavía requiere consulta, sin afectar a la comprensión conceptual.
- No debe proyectarse sobre MUD una separación entre clases y objetos: las `thing` no tienen instancias.
