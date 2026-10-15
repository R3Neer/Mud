using world
using spells

# Concrete example world. InstantProtocolCaster is a completion fixture, not a Fireball body.

thing MagicWorld as Magic

thing Player as Creature, Spellcaster {
    shape = [Shape.Cube]
    kinds = SympathyKind.Motion, SympathyKind.SharedEffects
}

thing Turret as Entity, Spellcaster {
    shape = [Shape.Cube]
    kinds = SympathyKind.Motion, SympathyKind.SharedEffects
}

thing BoxA as Entity {
    shape = [Shape.Cube]
    kinds = SympathyKind.Motion, SympathyKind.SharedEffects
}

thing BoxB as Entity {
    shape = [Shape.Cube]
    kinds = SympathyKind.Motion, SympathyKind.SharedEffects
}

thing BoxC as Entity {
    shape = [Shape.Cube]
    kinds = SympathyKind.Motion, SympathyKind.SharedEffects
}

thing Unshaped as Entity

thing InstantProtocolCaster as Creature, Spellcaster {
    configured = [Spell.Fireball]
}

thing NoFocus as Creature, Spellcaster {
    maxConcentration = 0
}
