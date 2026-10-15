part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Feedback]

using configuration
using world
using spells
using feedback
using fixtures

# Source contracts for capability filtering; no Mud runtime executes these yet.
test VisualChannelFiltersBothOrigins {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, VisualFeedback
    }
    then add SpellEvent(kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r1, r2, r3), empty)) to MagicWorld.pending
    after {
        (count request in VisualFeedback.requests : true) == 1
        forall request in VisualFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected, [FeedbackAsset.SelectionFlash, FeedbackAsset.AmbientGlow]
        )]
        Player.activeSpells == empty and Player.concentration == 0
        MagicWorld.links == empty
    }
}

test CompositeResourceRequiresEveryModality {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, AudioFeedback
    }
    then add SpellEvent(kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    after {
        (count request in AudioFeedback.requests : true) == 1
        forall request in AudioFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected, [FeedbackAsset.CastChime]
        )]
    }
}

test CompositeResourcePassesWithAllModalities {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, CompleteFeedback
    }
    then add SpellEvent(kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    after {
        (count request in CompleteFeedback.requests : true) == 1
        forall request in CompleteFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected, [FeedbackAsset.SynchronizedBurst]
        )]
    }
}

test MutedChannelProducesNoWork {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, MutedFeedback
    }
    then {
        add SpellEvent(kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
            aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
        add SpellEvent(kind = SpellEventKind.SelectionRejected, caster = Player, spell = Spell.Sympathy,
            aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    }
    after MutedFeedback.requests == empty and Player.activeSpells == empty
}

test RejectionFilteringRetainsOrderedDuplicates {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, AudioFeedback
    }
    then add SpellEvent(kind = SpellEventKind.SelectionRejected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    after {
        (count request in AudioFeedback.requests : true) == 1
        forall request in AudioFeedback.requests : request.rejected ==
            [FeedbackAsset.RejectionChime, FeedbackAsset.RejectionChime]
    }
}

test RejectionFilteringCanRemoveAllWork {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, VisualFeedback
    }
    then add SpellEvent(kind = SpellEventKind.SelectionRejected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    after VisualFeedback.requests == empty
}

test FilteredSuccessRetainsRepeatedPhaseResources {
    start with {
        ActivationSelection([ActivationFeature.Feedback]).declarations,
        MagicWorld, Player, VisualFeedback
    }
    then add SpellEvent(kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Sympathy,
        outcome = CastOutcome.Success, aim = Aim(Point3(r0, r0, r0), empty)) to MagicWorld.pending
    after {
        (count request in VisualFeedback.requests : true) == 1
        forall request in VisualFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Partial, [FeedbackAsset.SelectionFlash]),
            FeedbackGroup(FeedbackStage.Success, [FeedbackAsset.SelectionFlash])
        ]
        Player.activeSpells == empty and Player.concentration == 0
    }
}
