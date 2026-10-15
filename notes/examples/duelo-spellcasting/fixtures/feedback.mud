using spells
using feedback

# Example feedback configurations, including the missing-profile counterexample.

thing PlayerFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    profiles = Spell.Fireball -> SpellFeedbackProfile(
        byStage = (
            FeedbackStage.Selected -> [FeedbackAsset("specific"), FeedbackAsset("shared")],
            FeedbackStage.Partial -> [FeedbackAsset("shared")],
            FeedbackStage.Failed -> [FeedbackAsset("failure")],
            FeedbackStage.Success -> [FeedbackAsset("shared"), FeedbackAsset("success")],
            FeedbackStage.Cancelled -> [FeedbackAsset("cancel")]
        ),
        excluded = [FeedbackAsset("shared"), FeedbackAsset("excluded")]
    ),
    Spell.Sympathy -> SpellFeedbackProfile(
        byStage = (
            FeedbackStage.Selected -> [FeedbackAsset("specific"), FeedbackAsset("shared")],
            FeedbackStage.Partial -> [FeedbackAsset("shared")],
            FeedbackStage.Failed -> [FeedbackAsset("failure")],
            FeedbackStage.Success -> [FeedbackAsset("shared"), FeedbackAsset("success")],
            FeedbackStage.Cancelled -> [FeedbackAsset("cancel")]
        ),
        excluded = [FeedbackAsset("shared"), FeedbackAsset("excluded")]
    )
    global =
        FeedbackStage.Selected -> [FeedbackAsset("global"), FeedbackAsset("shared"),
            FeedbackAsset("excluded"), FeedbackAsset("global")],
        FeedbackStage.Partial -> [FeedbackAsset("global")],
        FeedbackStage.Success -> [FeedbackAsset("global")]
    selectionRejected = [FeedbackAsset("rejected"), FeedbackAsset("rejected")]
}

thing MissingProfileFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    global = FeedbackStage.Selected -> [FeedbackAsset("global")]
    selectionRejected = [FeedbackAsset("rejected"), FeedbackAsset("rejected")]
}
