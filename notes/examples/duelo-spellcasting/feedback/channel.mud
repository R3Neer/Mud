using spells

# Per-caster channel configuration and pure phase/merge policies.

abstract thing FeedbackChannel {
    let magic: Magic
    let caster: Spellcaster
    let subscribed: Bool = true
    let profiles: Spell -> SpellFeedbackProfile = empty
    let global: FeedbackStage -> (FeedbackAsset [*]) = empty
    let selectionRejected: FeedbackAsset [* ordered] = empty
    # A replaceable delivery batch, not an execution history.
    mut requests: FeedbackRequest [* ordered] = empty

    let stages: SpellEvent --> FeedbackStage [* ordered] =
        .kind == SpellEventKind.Selected --> [FeedbackStage.Selected],
        .kind == SpellEventKind.Cancelled --> [FeedbackStage.Cancelled],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Success -->
            [FeedbackStage.Partial, FeedbackStage.Success],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Partial -->
            [FeedbackStage.Partial],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Failed -->
            [FeedbackStage.Failed]

    let groupsFor: SpellEvent --> FeedbackGroup [* ordered] :=
        _ --> {
            let event = value
            mut groups: FeedbackGroup [* ordered] = empty
            foreach profile in profiles[event.spell] : {
                foreach stage in stages[event] : {
                    let effects = (global[stage][unique] -- profile.excluded)
                        | profile.byStage[stage][unique]
                    add FeedbackGroup(stage, effects) to groups
                }
            }
            groups
        }

    let rejectedFor: SpellEvent --> FeedbackAsset [* ordered] :=
        .kind == SpellEventKind.SelectionRejected --> selectionRejected

    let requestFor: SpellEvent --> FeedbackRequest [? ordered] :=
        {
            let groups := groupsFor[value]
            let rejected := rejectedFor[value]
            (exists group in groups : exists _ in group.effects : true)
                or (exists _ in rejected : true)
        } --> FeedbackRequest(value.caster, value.spell, value.aim, groups, rejected)
}
