using spells

# Feedback configuration, phases and immutable request values.

family FeedbackModality { Visual, Audio, Haptic }

family FeedbackAsset {
    AmbientGlow {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    SelectionFlash {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    CastChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    },
    LegacyPulse {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Haptic]
    },
    FailureChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    },
    SuccessFlash {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Visual]
    },
    CancelPulse {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Haptic]
    },
    RejectionChime {
        ~modalities: FeedbackModality [1..* unique] = [FeedbackModality.Audio]
    },
    SynchronizedBurst {
        ~modalities: FeedbackModality [1..* unique] = [
            FeedbackModality.Audio,
            FeedbackModality.Visual
        ]
    }
}

family FeedbackStage { Selected, Rejected, Partial, Failed, Success, Cancelled }

alias SpellFeedbackProfile {
    let byStage: FeedbackStage -> (FeedbackAsset [*]) [*] = empty
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
