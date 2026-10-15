part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Feedback]

using configuration
using world
using spells
using sympathy
using fixtures
using feedback

# Phase planning contracts isolated with typed domain facts.

test FeedbackSelectedEffectsAreMerged {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Selected,
        caster = Player,
        spell = Spell.Fireball,
        aim = Aim(Point3(r1 m, r2 m, r3 m), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected,
            [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime, FeedbackAsset.AmbientGlow]
        )]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r1 m, r2 m, r3 m)
        MagicWorld.pending == empty
    }
}

test FeedbackSuccessfulAttemptHasTwoPhases {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Attempted,
        caster = Player,
        spell = Spell.Fireball,
        outcome = CastOutcome.Success,
        aim = Aim(Point3(r4 m, r5 m, r6 m), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(
                FeedbackStage.Partial,
                [FeedbackAsset.CastChime, FeedbackAsset.AmbientGlow]
            ),
            FeedbackGroup(
                FeedbackStage.Success,
                [FeedbackAsset.CastChime, FeedbackAsset.AmbientGlow, FeedbackAsset.SuccessFlash]
            )
        ]
    }
}

test FeedbackPartialAttemptHasNoSuccessPhase {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Attempted,
        caster = Player,
        spell = Spell.Fireball,
        outcome = CastOutcome.Partial,
        aim = Aim(Point3(r0 m, r0 m, r0 m), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(
                FeedbackStage.Partial,
                [FeedbackAsset.CastChime, FeedbackAsset.AmbientGlow]
            )
        ]
    }
}

test FeedbackFailedAttemptUsesFailureEffects {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Attempted,
        caster = Player,
        spell = Spell.Fireball,
        outcome = CastOutcome.Failed,
        aim = Aim(Point3(r0 m, r0 m, r0 m), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Failed, [FeedbackAsset.FailureChime])
        ]
    }
}

test FeedbackCancellationRetainsItsAim {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Cancelled,
        caster = Player,
        spell = Spell.Fireball,
        aim = Aim(Point3(r7 m, r8 m, r9 m), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Cancelled, [FeedbackAsset.CancelPulse])
        ]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r7 m, r8 m, r9 m)
    }
}
