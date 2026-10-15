using spells

# Admit an available implemented spell before attempting it.
action Cast
for magic: Magic [mut], caster: Spellcaster [mut]
given aim: Aim {
    if caster.selected has Spell.Sympathy
        and caster.CanAttempt(Spell.Sympathy)
    then (magic, caster).AttemptSympathy(aim)
}
