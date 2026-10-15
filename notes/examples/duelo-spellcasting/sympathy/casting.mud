using spells

# Select the implemented provider. No selection remains a successful no-op.
action Cast
for magic: Magic [mut], caster: Spellcaster [mut]
given aim: Aim {
    then foreach spell in caster.selected[ordered]
        if spell == Spell.Sympathy and caster.CanAttempt(spell) :
            (magic, caster).AttemptSympathy(aim)
}
