# Informative feedback planner. Actual VFX execution remains an adapter effect.
# A sample is one captured callback, not a change in the caster's current state.

alias FeedbackAsset {
    let token: Text
}

family FeedbackStage { Selected, Canceled, Partial, Failed, Success }

alias FeedbackLists {
    let selected: FeedbackAsset [*] = empty
    let canceled: FeedbackAsset [*] = empty
    let partial: FeedbackAsset [*] = empty
    let failed: FeedbackAsset [*] = empty
    let success: FeedbackAsset [*] = empty
}

alias SpellFeedbackProfile {
    let effects: FeedbackLists = FeedbackLists()
    let excluded: FeedbackAsset [*] = empty
}

alias FeedbackSample {
    let kind: ProtocolKind in [ProtocolKind.Selected, ProtocolKind.SelectionFailed,
                              ProtocolKind.CastAttempted, ProtocolKind.Canceled]
    let spell: Spell
    let result: CastResult = CastResult.None
    # Owner position with no target, or the actual cast point/target.
    let aim: Aim
    # Stable registry tokens of assets alive at this callback boundary.
    let liveAssets: FeedbackAsset [* unique]
}

alias FeedbackGroup {
    let stage: FeedbackStage
    # No order is promised within the native HashSet merge.
    let effects: FeedbackAsset [* unique]
}

alias FeedbackPlan {
    let applicator: Text
    let sample: FeedbackSample
    let groups: FeedbackGroup [* ordered] = empty
    # Generic failure bypasses merging and retains duplicates and order.
    let fallback: FeedbackAsset [* ordered] = empty
}

abstract thing SpellFeedback {
    let applicator: Text
    let profiles: Spell --> SpellFeedbackProfile [? ordered]
    let global: FeedbackLists = FeedbackLists()
    let selectionFailed: FeedbackAsset [* ordered] = empty

    mut enabled: Bool = true
    mut pending: FeedbackPlan [* ordered] = empty
    mut ready: FeedbackPlan [* ordered] = empty

    let stages: FeedbackSample --> FeedbackStage [* ordered] :=
        .kind == ProtocolKind.Selected --> [FeedbackStage.Selected],
        .kind == ProtocolKind.Canceled --> [FeedbackStage.Canceled],
        .kind == ProtocolKind.CastAttempted
            and .result == CastResult.Success -->
                [FeedbackStage.Partial, FeedbackStage.Success],
        .kind == ProtocolKind.CastAttempted
            and .result == CastResult.Partial --> [FeedbackStage.Partial],
        .kind == ProtocolKind.CastAttempted
            and .result == CastResult.Failed --> [FeedbackStage.Failed]

    let effectsAt: (lists: FeedbackLists, stage: FeedbackStage)
        --> FeedbackAsset [*] :=
        .stage == FeedbackStage.Selected --> .lists.selected,
        .stage == FeedbackStage.Canceled --> .lists.canceled,
        .stage == FeedbackStage.Partial --> .lists.partial,
        .stage == FeedbackStage.Failed --> .lists.failed,
        .stage == FeedbackStage.Success --> .lists.success

    let fallback: FeedbackSample --> FeedbackAsset [* ordered] :=
        .kind == ProtocolKind.SelectionFailed -->
            foreach effect in selectionFailed
                if .liveAssets has effect --> effect

    let plan: FeedbackSample --> FeedbackPlan [ordered] :=
        _ --> {
            let sample = value
            mut groups: FeedbackGroup [* ordered] = empty
            foreach profile in profiles[sample.spell] : {
                foreach stage in stages[sample] : {
                    let effects =
                        ((effectsAt[global, stage][unique] -- profile.excluded)
                            | effectsAt[profile.effects, stage])
                            & sample.liveAssets
                    add FeedbackGroup(stage, effects) to groups
                }
            }
            FeedbackPlan(applicator, sample, groups, fallback[sample])
        }
}

action ReceiveSpellFeedback for feedback: SpellFeedback [mut] given
    sample: FeedbackSample {
    then {
        # Disabled callbacks are a normal no-op, never an IfRefusal.
        let admitted: Bool --> FeedbackPlan [? ordered] =
            == true --> [feedback.plan[sample]]
        add admitted[feedback.enabled][?] to feedback.pending
    }
}

action SetSpellFeedbackEnabled for feedback: SpellFeedback [mut] given
    enabled: Bool {
    then feedback.enabled = enabled
    after feedback.enabled == enabled
}

rule PrepareSpellFeedback on feedback: SpellFeedback [mut] {
    when feedback.pending changes
    if exists plan in feedback.pending : true
    then {
        let pending = feedback.pending
        feedback.pending = empty
        feedback.ready = pending
    }
}

# A batch occurrence follows an actual firing, even if its payload equals the
# preceding batch. This is not one message per synchronous Unity callback.
message SpellFeedbackPrepared on feedback: SpellFeedback {
    when feedback.PrepareSpellFeedback
    let plans := feedback.ready
}

look PreparedSpellFeedback for feedback: SpellFeedback {
    let plans := feedback.ready
}

# Fixed assets and owner token for source-level contract examples.
thing PlayerFeedback as SpellFeedback {
    applicator = "player"
    profiles = Spell.Fireball --> SpellFeedbackProfile(
        effects = FeedbackLists(
            selected = [FeedbackAsset("specific"), FeedbackAsset("shared")],
            canceled = [FeedbackAsset("cancel")],
            partial = [FeedbackAsset("shared")],
            failed = [FeedbackAsset("failed")],
            success = [FeedbackAsset("shared"), FeedbackAsset("success")]
        ),
        excluded = [FeedbackAsset("shared"), FeedbackAsset("excluded")]
    )
    global = FeedbackLists(
        selected = [FeedbackAsset("global"), FeedbackAsset("shared"),
                    FeedbackAsset("excluded"), FeedbackAsset("excluded"),
                    FeedbackAsset("global")],
        partial = [FeedbackAsset("global")],
        success = [FeedbackAsset("global")]
    )
    selectionFailed = [FeedbackAsset("fallback"), FeedbackAsset("fallback"),
                       FeedbackAsset("dead")]
}
