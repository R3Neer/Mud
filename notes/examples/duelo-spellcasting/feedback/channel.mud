~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Feedback

using spells

# Per-caster channel configuration and pure phase/merge policies.

abstract thing FeedbackChannel {
    let magic: Magic
    let caster: Spellcaster
    let subscribed: Bool = true
    let allowedModalities: FeedbackModality [* unique] = [
        FeedbackModality.Visual, FeedbackModality.Audio, FeedbackModality.Haptic
    ]
    let profiles: Spell -> SpellFeedbackProfile = empty
    let global: FeedbackStage -> (FeedbackAsset [*]) = empty
    let selectionRejected: FeedbackAsset [* ordered] = empty
    # A replaceable delivery batch, not an execution history.
    mut requests: FeedbackRequest [* ordered] = empty

    let phasesFor: SpellEvent --> FeedbackStage [* ordered] =
        .kind == SpellEventKind.Selected --> [FeedbackStage.Selected],
        .kind == SpellEventKind.Cancelled --> [FeedbackStage.Cancelled],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Success -->
            [FeedbackStage.Partial, FeedbackStage.Success],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Partial -->
            [FeedbackStage.Partial],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Failed -->
            [FeedbackStage.Failed]

    let phaseGroupsFor: SpellEvent --> FeedbackGroup [* ordered] :=
        _ --> {
            let event = value
            let allowedAssets := AllowedFeedbackAssets(allowedModalities).assets
            mut groups: FeedbackGroup [* ordered] = empty
            foreach profile in profiles[event.spell] : {
                groups = foreach stage in phasesFor[event] --> {
                    let globalAssets = global[stage][unique] -- profile.excluded
                    let phaseAssets = globalAssets | profile.byStage[stage][unique]
                    let permitted := foreach asset in phaseAssets
                        if allowedAssets has asset --> asset
                    FeedbackGroup(stage, permitted)
                }
            }
            groups
        }

    let rejectionAssetsFor: SpellEvent --> FeedbackAsset [* ordered] :=
        .kind == SpellEventKind.SelectionRejected --> {
            let allowedAssets := AllowedFeedbackAssets(allowedModalities).assets
            foreach asset in selectionRejected
                if allowedAssets has asset --> asset
        }

    let requestFor: SpellEvent --> FeedbackRequest [? ordered] := {
        let groups := phaseGroupsFor[value]
        let rejected := rejectionAssetsFor[value]
        (exists group in groups : group.effects != empty)
            or rejected != empty
    } --> FeedbackRequest(
        value.caster,
        value.spell,
        value.aim,
        groups,
        rejected
    )
}
