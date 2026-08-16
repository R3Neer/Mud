from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one match, got {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8', newline='\n')


# D-036: no shorthand can survive once participant identifiers are mandatory.
replace_once(
    'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md',
    '10. Diferencia entre la referencia exacta `World` y un participante `on World` o `for World`.\n',
    '10. Diferencia entre la referencia exacta `World` y un participante nombrado `on world: World` o `for world: World`.\n',
)
replace_once(
    'notas/decisiones/ADR-036-participantes-receptores-y-llamadas.md',
    'El tipo incorporado `Thing` admite cualquier `thing`. Por tanto, un rol `for` de tipo `Thing` acepta cualquier identidad concreta compatible y `on Thing` enumera todas las `thing` concretas y activas; la raíz abstracta no produce una vinculación propia.\n',
    'El tipo incorporado `Thing` admite cualquier `thing`. Por tanto, un rol `for` de tipo `Thing` acepta cualquier identidad concreta compatible y un rol `on` de tipo `Thing` enumera todas las `thing` concretas y activas; la raíz abstracta no produce una vinculación propia.\n',
)

# Normative syntax chapter had the same pre-D-087 shorthand.
replace_once(
    'especificacion/07-gramatica-concreta.md',
    'Una referencia ordinaria a `World` designa la identidad exacta. `on World` y un rol `for World` seleccionan reflexivamente las `thing` concretas activas que satisfacen `is World`, incluida la propia `World` si es concreta. Esta selección solo se aplica cuando el tipo del rol es una `thing`.\n',
    'Una referencia ordinaria a `World` designa la identidad exacta. Los participantes `on world: World` y `for world: World` seleccionan reflexivamente las `thing` concretas activas que satisfacen `is World`, incluida la propia `World` si es concreta. Esta selección solo se aplica cuando el tipo del rol es una `thing`.\n',
)

# D-068 was modified by D-085/D-087 but still described the old plain-name and
# anchor interpolation model. Rewrite the current semantics against D-087.
p = Path('notas/decisiones/ADR-068-thing-universal-y-nombre-intrinseco.md')
text = p.read_text(encoding='utf-8')
marker = '- Modificada por: [[ADR-086-identidad-nominal-exacta-y-algebra-de-diccionarios|D-086]]\n'
if text.count(marker) != 1:
    raise SystemExit('D-068 relation marker mismatch')
text = text.replace(
    marker,
    marker + '- Modificada por: [[ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior|D-087]]\n',
    1,
)
old = '- `on Thing` selecciona todas las `thing` concretas y activas; la identidad abstracta `Thing` no constituye por sí misma una vinculación.\n'
new = '- Un participante `on value: Thing` selecciona todas las `thing` concretas y activas; la identidad abstracta `Thing` no constituye por sí misma una vinculación.\n'
if text.count(old) != 1:
    raise SystemExit('D-068 on Thing marker mismatch')
text = text.replace(old, new, 1)
old = 'Su ancla canónica es `thing::Thing`; `anchor{Thing}` produce esa escritura. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa.\n'
new = 'Su ancla canónica es `thing::Thing`; `Thing~anchor` devuelve ese valor reflectivo. El ancla pertenece al lenguaje y no ocupa un path declarable por el programa. La forma especial `anchor{...}` dejó de existir con D-087.\n'
if text.count(old) != 1:
    raise SystemExit('D-068 anchor marker mismatch')
text = text.replace(old, new, 1)

start = text.index('### Propiedad intrínseca `name`')
end = text.index('## Consecuencias', start)
name_section = '''### Identificador y presentación reflectiva

D-085 y D-087 sustituyen la antigua propiedad ordinaria `name` por dos conceptos separados en el espacio postfix `~`:

```text
~identifier : Name
~name       : Name
```

`~identifier` es intrínseco y refleja el identificador fuente de la `thing`. `~name` es un metadato estándar configurable de presentación humana; toma por defecto una presentación derivada de `~identifier` y no participa en resolución, igualdad ni formación de anclas.

```mud
thing BlackCastle {
    ~name = "El Castillo Negro"
}
```

La configuración de `~name` se rige por las reglas generales de metadatos de D-087. Todo acceso `~` es runtime-readonly: una ejecución puede leer `value~name`, pero no asignarlo. La forma antigua `name = "..."` no configura presentación y `value.name` no es acceso reflectivo.

Los espacios siguen siendo distintos. Un campo ordinario llamado `name`, si satisface las reglas generales de campos, se declara como `name: Text` y se accede con `value.name`; no colisiona sintácticamente con `~name`.

La configuración de presentación pertenece al descriptor concreto. Una descendiente sin `~name` explícito usa su propio valor predeterminado derivado de su `~identifier`, no la presentación configurada de una antecesora.

Dos `thing` pueden compartir el mismo `~name`: la igualdad, la resolución y el anclaje continúan dependiendo de la identidad nominal. La conversión textual canónica de una `thing` usa su presentación `~name` efectiva. Cuando se necesita la identidad reflectiva se consulta explícitamente `value~identifier` o `value~anchor`; no existe una interpolación especial `anchor{...}`.

'''
text = text[:start] + name_section + text[end:]

start = text.index('## Consecuencias')
end = text.index('## Verificación', start)
consequences = '''## Consecuencias

- Existe un tipo común garantizado para todas las `thing` y para colecciones heterogéneas.
- El grafo distingue antecesoras declaradas de la arista implícita de las raíces hacia `Thing`.
- La presentación humana puede cambiar mediante `~name` sin alterar `~identifier`, identidad, path de MUD ni ancla.
- `~name` no introduce un lugar mutable del store ni escrituras runtime.
- El identificador ordinario de campo `name` pertenece al espacio de campos y permanece separado del metadato `~name`.

'''
text = text[:start] + consequences + text[end:]

start = text.index('## Verificación')
end = text.index('## Aclaración por D-084', start)
verification = '''## Verificación

1. `T is Thing` para toda `thing` declarada y `Thing is Thing`.
2. Rechazo de declaración, `create` y `destroy` de `Thing`; aceptación no bloqueante de `as Thing` con sugerencia de eliminación.
3. Ancla incorporada `thing::Thing` y lectura mediante `Thing~anchor`.
4. Participantes nombrados `on value: Thing` y `for value: Thing` sobre cualquier `thing` concreta activa.
5. Colección `Thing [*]` con identidades de ramas no relacionadas.
6. `~identifier` igual al identificador fuente y `~name` predeterminado derivado de él.
7. Configuración de presentación mediante `~name` y lectura runtime de solo lectura.
8. Rechazo de escritura runtime sobre `~name` y de la forma reflectiva antigua sin `~`.
9. Una descendiente sin configuración propia no hereda la presentación explícita de su antecesora.
10. La conversión textual de una `thing` usa su `~name` efectivo; `~identifier` y `~anchor` permanecen accesos explícitos distintos.
11. Presentaciones `~name` duplicadas sin fusión de identidades.
12. Un campo ordinario `name: Text` permanece distinto del metadato `~name`.

'''
text = text[:start] + verification + text[end:]

start = text.index('## Aclaración por D-084')
clarification = '''## Aclaración por D-084

D-084 excluye una propiedad ordinaria `name` incorporada en los valores alias. D-087 regula por separado los metadatos del descriptor de la declaración `alias`, incluido `~name` cuando sea compatible. Un alias estructural puede declarar un componente ordinario `name: Text`; ese componente pertenece a su forma de valor y no es el metadato `~name`. Los miembros de `family` usan igualmente `~identifier` y `~name` conforme a D-087.
'''
text = text[:start] + clarification
p.write_text(text, encoding='utf-8', newline='\n')

# Make D-087's modification relation reciprocal for D-068 as well.
replace_once(
    'notas/decisiones/ADR-087-metadatos-reflectivos-descriptores-estables-y-visibilidad-exterior.md',
    '- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',
    '- Modifica: [[ADR-036-participantes-receptores-y-llamadas|D-036]], [[ADR-037-campos-y-dominios-declarativos|D-037]], [[ADR-038-familias-cerradas-de-valores|D-038]], [[ADR-063-firmas-given-y-vinculaciones-on-conjuntas|D-063]], [[ADR-068-thing-universal-y-nombre-intrinseco|D-068]], [[ADR-072-entornos-de-resolucion-y-migraciones-explicitas-de-anclas|D-072]], [[ADR-076-unidades-nombradas-prefijos-y-escritura-adyacente|D-076]] y [[ADR-085-diccionarios-decisionales-metadatos-y-activacion-estructurada|D-085]].\n',
)

print('PHASE5_REVIEW_FIX_OK')
