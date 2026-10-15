using world
using spells
using sympathy

# Derived presentation views and change notifications; no target caches.

look Targeting for caster: Spellcaster {
    let selected := caster.selected
    let prepared := caster.preparation
    let visible := caster.present and (exists spell in caster.selected : true)
}

message TargetingChanged on caster: Spellcaster {
    let current := caster.Targeting()
    when current changes
    let selected := current.selected
    let prepared := current.prepared
    let visible := current.visible
}

message EffectiveEffectsChanged on magic: Magic, entity: Entity {
    let current := (magic, entity).EffectiveEffects()
    when current changes
    let own := current.own
    let borrowed := current.borrowed
}
