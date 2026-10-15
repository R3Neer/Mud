using spells

# Feedback configuration, phases and immutable request values.

alias FeedbackAsset { let name: Text }

family FeedbackStage { Selected, Rejected, Partial, Failed, Success, Cancelled }

alias SpellFeedbackProfile {
    let byStage: FeedbackStage -> (FeedbackAsset [*]) = empty
    let excluded: FeedbackAsset [* unique] = empty
}

alias FeedbackGroup {
    let stage: FeedbackStage
    let effects: FeedbackAsset [* unique]
}

alias FeedbackRequest {
    let caster: Spellcaster
    let spell: Spell
    let aim: Aim
    let groups: FeedbackGroup [* ordered]
    # Rejected selections use this sequence directly, retaining repetitions.
    let rejected: FeedbackAsset [* ordered]
}
