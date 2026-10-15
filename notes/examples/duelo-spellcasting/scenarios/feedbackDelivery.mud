part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Feedback]

using configuration
using world
using spells
using sympathy
using fixtures
using feedback

# Profile, occurrence, filtering and end-to-end feedback source contracts.

test FeedbackRejectionRetainsDuplicateEffectsWithoutProfile {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, MissingProfileFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.SelectionRejected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in MissingProfileFeedback.requests : true) == 1
        forall request in MissingProfileFeedback.requests : request.groups == empty
        forall request in MissingProfileFeedback.requests : request.rejected ==
            [FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime]
    }
}

test FeedbackMissingProfileProducesNoRequest {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, MissingProfileFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        MissingProfileFeedback.requests == empty
    }
}

test FeedbackModelsARealSympathyCast {
    ~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Feedback, configuration.TestConcern.Selection, configuration.TestConcern.PairAdmission]

    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, BoxA, BoxB, PlayerFeedback
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r1, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r2, r0, r0), [BoxB]))
    }
    after {
        exists request in PlayerFeedback.requests :
            request.spell == Spell.Sympathy and
                (exists group in request.groups : group.stage == FeedbackStage.Success)
        Player.selected == empty
        Player.concentration == 1
        (count _ in MagicWorld.links : true) == 1
    }
}

test FeedbackNoneProducesNoRequest {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.None, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        PlayerFeedback.requests == empty
    }
}

test FeedbackRepeatedEqualFactsRemainTwoRequests {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, MagicWorld, PlayerFeedback
    }
    then {
        let event = SpellEvent(
            kind = SpellEventKind.Selected, caster = Player, spell = Spell.Fireball,
            aim = Aim(Point3(r0, r0, r0), empty)
        )
        add event to MagicWorld.pending
        add event to MagicWorld.pending
    }
    after {
        (count _ in PlayerFeedback.requests : true) == 2
        forall request in PlayerFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected,
            [FeedbackAsset.SelectionFlash, FeedbackAsset.CastChime, FeedbackAsset.AmbientGlow]
        )]
    }
}

test FeedbackIgnoresAnotherSpellcaster {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, Turret, MagicWorld, PlayerFeedback
    }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Turret, spell = Spell.Fireball,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after PlayerFeedback.requests == empty
}

test FeedbackFiltersAMixedCasterBatch {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        Player, Turret, MagicWorld, PlayerFeedback
    }
    then {
        add SpellEvent(
            kind = SpellEventKind.Selected, caster = Turret, spell = Spell.Fireball,
            aim = Aim(Point3(r1, r0, r0), empty)
        ) to MagicWorld.pending
        add SpellEvent(
            kind = SpellEventKind.Selected, caster = Player, spell = Spell.Fireball,
            aim = Aim(Point3(r2, r0, r0), empty)
        ) to MagicWorld.pending
    }
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.caster == Player
            and request.aim.point == Point3(r2, r0, r0)
    }
}
