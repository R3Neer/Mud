# Declarative contracts, not executed tests. Each test has a fresh world.

test FeedbackSelectionMergesPerPhase {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.Selected,
        spell = Spell.Fireball,
        aim = Aim(r1, r2, r3, empty),
        liveAssets = [FeedbackAsset("specific"), FeedbackAsset("shared"),
                      FeedbackAsset("global"), FeedbackAsset("excluded")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [FeedbackGroup(
            FeedbackStage.Selected,
            [FeedbackAsset("specific"), FeedbackAsset("shared"), FeedbackAsset("global")]
        )]
        forall plan in PlayerFeedback.ready : plan.sample.aim == Aim(r1, r2, r3, empty)
        forall plan in PlayerFeedback.ready : plan.applicator == "player"
        PlayerFeedback.pending == empty
    }
}

test FeedbackSuccessKeepsBothPhases {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.CastAttempted,
        spell = Spell.Fireball,
        result = CastResult.Success,
        aim = Aim(r4, r5, r6, ["crate"]),
        liveAssets = [FeedbackAsset("shared"), FeedbackAsset("global"), FeedbackAsset("success")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Partial, [FeedbackAsset("shared"), FeedbackAsset("global")]),
            FeedbackGroup(FeedbackStage.Success,
                [FeedbackAsset("shared"), FeedbackAsset("global"), FeedbackAsset("success")])
        ]
        forall plan in PlayerFeedback.ready : plan.sample.aim == Aim(r4, r5, r6, ["crate"])
    }
}

test FeedbackPartialHasNoSuccessPhase {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.CastAttempted, spell = Spell.Fireball,
        result = CastResult.Partial, aim = Aim(r0, r0, r0, empty),
        liveAssets = [FeedbackAsset("shared"), FeedbackAsset("success")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Partial, [FeedbackAsset("shared")])
        ]
    }
}

test FeedbackFailedUsesFailedPhase {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.CastAttempted, spell = Spell.Fireball,
        result = CastResult.Failed, aim = Aim(r0, r0, r0, empty),
        liveAssets = [FeedbackAsset("failed"), FeedbackAsset("shared")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Failed, [FeedbackAsset("failed")])
        ]
    }
}

test FeedbackCancellationUsesOwnerContext {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.Canceled, spell = Spell.Fireball,
        aim = Aim(r7, r8, r9, empty), liveAssets = [FeedbackAsset("cancel")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Canceled, [FeedbackAsset("cancel")])
        ]
        forall plan in PlayerFeedback.ready : plan.sample.aim == Aim(r7, r8, r9, empty)
    }
}

test FeedbackFailureFallbackRetainsDuplicatesWithoutProfile {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.SelectionFailed, spell = Spell.SympathyLink,
        aim = Aim(r0, r0, r0, empty), liveAssets = [FeedbackAsset("fallback")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == empty
        forall plan in PlayerFeedback.ready : plan.fallback ==
            [FeedbackAsset("fallback"), FeedbackAsset("fallback")]
    }
}

test FeedbackMissingProfileDoesNotPlayGlobals {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.Selected, spell = Spell.SympathyLink,
        aim = Aim(r0, r0, r0, empty), liveAssets = [FeedbackAsset("global")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == empty and plan.fallback == empty
    }
}

test FeedbackNoneDoesNotPlayCastEffects {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
        kind = ProtocolKind.CastAttempted, spell = Spell.Fireball,
        result = CastResult.None, aim = Aim(r0, r0, r0, empty),
        liveAssets = [FeedbackAsset("shared"), FeedbackAsset("global")]
    ))
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == empty and plan.fallback == empty
    }
}

test FeedbackRepeatedEqualCallbacksRemainTwoRequests {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then {
        let sample = FeedbackSample(
            kind = ProtocolKind.Selected, spell = Spell.Fireball,
            aim = Aim(r0, r0, r0, empty), liveAssets = [FeedbackAsset("specific")]
        )
        PlayerFeedback.ReceiveSpellFeedback(sample)
        PlayerFeedback.ReceiveSpellFeedback(sample)
    }
    after {
        (count plan in PlayerFeedback.ready : true) == 2
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Selected, [FeedbackAsset("specific")])
        ]
        PlayerFeedback.pending == empty
    }
}

test FeedbackDisabledCallbackIsNotResurrected {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then {
        PlayerFeedback.SetSpellFeedbackEnabled(false)
        PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
            kind = ProtocolKind.Selected, spell = Spell.Fireball,
            aim = Aim(r0, r0, r0, empty), liveAssets = [FeedbackAsset("specific")]
        ))
        PlayerFeedback.SetSpellFeedbackEnabled(true)
    }
    after PlayerFeedback.pending == empty and PlayerFeedback.ready == empty
}

test FeedbackDisablingDoesNotDiscardCapturedWork {
    start with { SpellFeedback, PlayerFeedback, PrepareSpellFeedback }
    then {
        PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
            kind = ProtocolKind.Selected, spell = Spell.Fireball,
            aim = Aim(r0, r0, r0, empty), liveAssets = [FeedbackAsset("specific")]
        ))
        PlayerFeedback.SetSpellFeedbackEnabled(false)
    }
    after {
        not PlayerFeedback.enabled
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Selected, [FeedbackAsset("specific")])
        ]
    }
}

test FeedbackBridgePreservesControllerCastContext {
    start with {
        Caster, IsResolvable, ConcentrationWithinLimit, PlayerCaster,
        SpellFeedback, PlayerFeedback, PrepareSpellFeedback
    }
    then {
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.CastSample(CastResult.Success, Aim(r4, r5, r6, ["crate"]))
        # Explicit sample bridge for this one operation, before lastTrace resets.
        foreach observation in PlayerCaster.lastTrace
            if observation.kind == ProtocolKind.CastAttempted :
                PlayerFeedback.ReceiveSpellFeedback(FeedbackSample(
                    kind = observation.kind, spell = observation.spell,
                    result = observation.result, aim = observation.aim[?],
                    liveAssets = [FeedbackAsset("shared")]
                ))
    }
    after {
        (count plan in PlayerFeedback.ready : true) == 1
        forall plan in PlayerFeedback.ready : plan.groups == [
            FeedbackGroup(FeedbackStage.Partial, [FeedbackAsset("shared")]),
            FeedbackGroup(FeedbackStage.Success, [FeedbackAsset("shared")])
        ]
        forall plan in PlayerFeedback.ready : plan.sample.aim == Aim(r4, r5, r6, ["crate"])
        PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.None
    }
}
