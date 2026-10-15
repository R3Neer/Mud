part only

# Admission checks and concentration invariant; keep these active.

rule CanSelect for caster: Spellcaster given spell: Spell {
    caster.present and caster.configured has spell and spell.slot <= caster.unlocked
        and (not spell.needsConcentration or caster.concentration < caster.maxConcentration)
}

rule CanAttempt for caster: Spellcaster given spell: Spell {
    caster.present and caster.selected has spell and caster.activeSpells has spell
        and caster.configured has spell and spell.slot <= caster.unlocked
}

always rule ConcentrationWithinLimit on caster: Spellcaster {
    caster.concentration <= caster.maxConcentration
}
