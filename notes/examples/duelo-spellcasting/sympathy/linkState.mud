part only

using world
using spells

# Operational relations, pair plans and link-effect delivery state.

alias SympathyLink {
    let id: LinkId
    # Explicit immediate authority, supplied by the spellcaster's for role.
    # Public facts/looks project LinkSnapshot instead of exposing this component.
    let owner: Spellcaster [mut]
    let leader: Entity
    let follower: Entity
    let kinds: SympathyKind [* unique]
}

alias SympathyPair {
    let leader: Entity
    let follower: Entity
}

alias SympathyStopped {
    let outcome: CastOutcome in [CastOutcome.None, CastOutcome.Failed]
}

alias SympathyPreparation {
    let target: Entity
    let outcome := CastOutcome.Partial
}

alias SympathyReady {
    let pair: SympathyPair
    let outcome := CastOutcome.Success
}

rule PrepareLinkEffects on magic: Magic [mut] {
    ~activationFeature: configuration.ActivationFeature =
        configuration.ActivationFeature.LinkEffects

    let incoming := magic.SpellEvents
    when incoming
    then {
        magic.linkEffects = foreach event in incoming.events
            if event.kind == SpellEventKind.Linked or event.kind == SpellEventKind.Inverted
                or event.kind == SpellEventKind.Unlinked --> event
    }
}
