using spells
using feedback

# Example feedback configurations, including the missing-profile counterexample.

thing PlayerFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    profiles = {
        let profile = SpellFeedbackProfile(
            byStage = [
                FeedbackStage.Selected -> [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime],
                FeedbackStage.Partial -> [FeedbackAsset.CastChime],
                FeedbackStage.Failed -> [FeedbackAsset.FailureChime],
                FeedbackStage.Success -> [FeedbackAsset.CastChime, FeedbackAsset.SuccessFlash],
                FeedbackStage.Cancelled -> [FeedbackAsset.CancelPulse]
            ],
            excluded = [FeedbackAsset.CastChime, FeedbackAsset.LegacyPulse]
        )
        Spell.Fireball -> profile,
        Spell.Sympathy -> profile
    }
    global =
        FeedbackStage.Selected -> [FeedbackAsset.AmbientGlow, FeedbackAsset.CastChime,
            FeedbackAsset.LegacyPulse, FeedbackAsset.AmbientGlow],
        FeedbackStage.Partial -> [FeedbackAsset.AmbientGlow],
        FeedbackStage.Success -> [FeedbackAsset.AmbientGlow]
    selectionRejected = FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime
}

thing MissingProfileFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    global = FeedbackStage.Selected -> [FeedbackAsset.AmbientGlow]
    selectionRejected = FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime
}
