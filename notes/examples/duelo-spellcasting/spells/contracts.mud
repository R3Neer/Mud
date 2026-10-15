using world

# Spell catalogue and immutable occurrence contracts.

family Spell {
    slot: Nat
    needsConcentration: Bool
    Sympathy { slot = 1; needsConcentration = true },
    Fireball { slot = 2; needsConcentration = false }
}

family CastOutcome { None, Partial, Failed, Success }

alias Aim {
    let point: Point3
    let target: Entity [?] = empty
}

family SpellEventKind {
    Selected, SelectionRejected, Attempted, Cancelled, Linked, Inverted, Unlinked
}

alias LinkSnapshot {
    let id: Nat
    let owner: Spellcaster
    let leader: Entity
    let follower: Entity
    let kinds: SympathyKind [* unique]
}

alias SpellEvent {
    let kind: SpellEventKind
    let caster: Spellcaster
    let spell: Spell
    let outcome: CastOutcome = CastOutcome.None
    let aim: Aim
    let link: LinkSnapshot [?] = empty
}
