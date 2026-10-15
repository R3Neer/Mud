using spells
using feedback

# Capability profiles are receiver configuration, not changes to spell admission.
thing VisualFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    allowedModalities = [FeedbackModality.Visual]
    profiles = Spell.Sympathy -> SpellFeedbackProfile(
        byStage = [
            FeedbackStage.Selected -> [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime],
            FeedbackStage.Partial -> [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime],
            FeedbackStage.Success -> [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime]
        ],
        excluded = [FeedbackAsset.CastChime]
    )
    global = FeedbackStage.Selected -> [FeedbackAsset.AmbientGlow, FeedbackAsset.CastChime]
    selectionRejected = FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime
}

thing AudioFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    allowedModalities = [FeedbackModality.Audio]
    profiles = Spell.Sympathy -> SpellFeedbackProfile(
        byStage = [
            FeedbackStage.Selected -> [FeedbackAsset.CastChime, FeedbackAsset.SynchronizedBurst]
        ]
    )
    selectionRejected = FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime
}

thing MutedFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    allowedModalities = empty
    profiles = Spell.Sympathy -> SpellFeedbackProfile(
        byStage = [FeedbackStage.Selected -> [FeedbackAsset.SelectionFlash]]
    )
    selectionRejected = FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime
}

thing CompleteFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    profiles = Spell.Sympathy -> SpellFeedbackProfile(
        byStage = [FeedbackStage.Selected -> [FeedbackAsset.SynchronizedBurst]]
    )
}
