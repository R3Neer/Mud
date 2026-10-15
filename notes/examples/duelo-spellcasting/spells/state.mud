~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

using world
using sympathy

# Spell capability and world-owned relations and delivery buffers.

abstract thing Spellcaster as Entity {
    let configured: Spell [* unique] = [Spell.Sympathy]
    let maxConcentration: Nat = 2
    mut unlocked: Nat = 2
    mut selected: Spell [?] = empty
    mut activeSpells: Spell [* unique] = empty
    mut prepared: Entity [?] = empty

    let concentration := count spell in activeSpells : spell.needsConcentration
    let preparation := foreach entity in prepared if entity.present --> entity
}

abstract thing Magic {
    mut links: SympathyLink [* unique by id] = empty
    mut nextLink: Nat = 1
    mut pending: SpellEvent [* ordered] = empty
    mut published: SpellEvent [* ordered] = empty
    mut linkEffects: SpellEvent [* ordered] = empty
}
