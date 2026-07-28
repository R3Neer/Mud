# ADR-022 — Borrado estructural de reglas booleanas inactivas

- Estado: Vigente
- Fecha: 2026-07-27
- Pregunta abierta relacionada: [[notas/08-preguntas-abiertas#Q-050 — Borrado en operadores booleanos restantes|Q-050]]
- Decisión relacionada: [[notas/decisiones/ADR-021-ciclo-de-vida-logico-y-suspension|D-021]]
- Documentos afectados: [[notas/02-modelo-del-lenguaje]], [[notas/03-semantica-de-ejecucion]], futuros capítulos 19, 21 y 26

## Contexto

Una regla booleana puede quedar inactiva por `destroy` o por la suspensión de una dependencia. Sus llamadas no deben convertirse siempre en `true` ni provocar que toda declaración dependiente sea inválida. La intención es que la expresión se comporte como si se hubiera borrado la proposición que invocaba la regla.

El elemento neutro necesario depende del operador exterior:

$$
p\land\top=p
$$

$$
p\lor\bot=p
$$

Por tanto, ningún valor booleano ordinario representa por sí solo el borrado en todos los contextos.

## Decisión

La evaluación introduce una marca metalingüística:

$$
\mathsf{erased}
$$

que significa «este fragmento sintáctico ha sido borrado». No es un valor de MUD, no puede almacenarse y no pertenece a `Bool`.

Antes del borrado, las expresiones booleanas se elaboran a un núcleo canónico:

$$
b ::=
\top
\mid
\bot
\mid
p
\mid
\neg b
\mid
b\land b
\mid
b\lor b
$$

Una llamada a una regla booleana que no sea efectiva en $W$ se poda:

$$
\operatorname{prune}_W(R(\bar e))
=
\mathsf{erased}
\qquad
\text{si }
\neg\operatorname{effective}_W(R)
$$

El receptor y los argumentos de una llamada borrada no se evalúan dinámicamente. Sí deben estar bien resueltos y tipados estáticamente porque la regla puede volver a ser efectiva en otro mundo.

## Reglas de poda

La negación conserva el hueco:

$$
\operatorname{prune}_W(\neg\mathsf{erased})
=
\mathsf{erased}
$$

La conjunción y la disyunción eliminan un operando borrado:

$$
\mathsf{erased}\land b=b
\qquad
b\land\mathsf{erased}=b
$$

$$
\mathsf{erased}\lor b=b
\qquad
b\lor\mathsf{erased}=b
$$

Si ambos operandos están borrados:

$$
\mathsf{erased}\land\mathsf{erased}
=
\mathsf{erased}
$$

$$
\mathsf{erased}\lor\mathsf{erased}
=
\mathsf{erased}
$$

Cuando la expresión exterior completa queda borrada, se cierra como verdadera:

$$
\operatorname{close}(\mathsf{erased})
=
\top
$$

Esto representa que una condición eliminada no impone ninguna restricción.

## Negación

Si `R` está inactiva:

```mud
not R(x)
```

se reduce:

$$
\neg\mathsf{erased}
\longrightarrow
\mathsf{erased}
\longrightarrow
\top
$$

si es la expresión exterior.

Dentro de:

```mud
P(x) and not R(x)
```

el resultado residual es `P(x)`.

## Implicación

La implicación se elabora antes de podar:

$$
p\Rightarrow q
\quad\rightsquigarrow\quad
\neg p\lor q
$$

Si se borra el antecedente:

$$
\neg\mathsf{erased}\lor q
\longrightarrow
q
$$

Si se borra el consecuente:

$$
\neg p\lor\mathsf{erased}
\longrightarrow
\neg p
$$

## Bicondicional e igualdad booleana

La igualdad entre booleanos y el bicondicional se elaboran canónicamente como:

$$
p\Leftrightarrow q
\quad\rightsquigarrow\quad
(p\land q)\lor(\neg p\land\neg q)
$$

Si se borra $p$:

$$
(\mathsf{erased}\land q)
\lor
(\neg\mathsf{erased}\land\neg q)
$$

se reduce a:

$$
q\lor\neg q
=
\top
$$

Por tanto, una igualdad booleana con uno de sus operandos borrado resulta verdadera con independencia del otro operando.

## Dependencia de la forma canónica

La poda no respeta necesariamente todas las equivalencias del álgebra booleana clásica. Dos árboles clásicamente equivalentes pueden producir residuos diferentes si se reescriben antes de eliminar una regla.

La conformidad exige:

1. Resolver y tipar la expresión original.
2. Elaborar operadores derivados a una forma núcleo canónica.
3. Podar llamadas a reglas inactivas.
4. Cerrar un residuo exterior borrado con $\top$.
5. Evaluar la expresión booleana residual.

Un optimizador no puede aplicar una reescritura clásica que cambie el resultado de este procedimiento.

## Alternativas

### Regla inactiva igual a `true`

Se descarta porque `P or R` se volvería siempre verdadero y `not R` se volvería falso, aunque la intención sea retirar la condición.

### Neutro elegido directamente por el padre

Describe bien la intuición, pero no basta para negación, implicación o igualdad. La marca `erased` generaliza la misma idea a un recorrido estructural.

### Suspender toda declaración que llama a la regla

Se descarta porque impediría que una fórmula continuase funcionando con las demás condiciones que aún conserva.

## Cuestiones abiertas

- Elaboración exacta de `!=`, `xor` y otros comparadores booleanos.
- Poda dentro de cuantificadores y agregaciones booleanas.
- Interacción con `allowed`, `eventually` y fallos de subexpresiones que desaparecen.
- Diagnósticos o advertencias para fórmulas especialmente sensibles a su forma sintáctica.

## Verificación futura

La suite deberá cubrir:

1. Regla inactiva como expresión exterior.
2. Regla inactiva bajo negación exterior y anidada.
3. Posiciones izquierda y derecha de `and` y `or`.
4. Dos operandos borrados.
5. Antecedente y consecuente de implicación.
6. Ambos lados de igualdad booleana.
7. Ausencia de evaluación dinámica de receptor y `given` borrados.
8. Reactivación de la regla y recuperación de la evaluación ordinaria.
9. Rechazo de optimizaciones que alteren la poda canónica.
