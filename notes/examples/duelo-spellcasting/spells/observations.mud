# Public spell occurrence stream and current capability query.

message SpellEvents on magic: Magic {
    when magic.PublishSpellEvents
    let events := magic.published
}

look Spellcasting for caster: Spellcaster {
    let selected := caster.selected
    let active := caster.activeSpells
    let concentration := caster.concentration
    let prepared := caster.preparation
}
