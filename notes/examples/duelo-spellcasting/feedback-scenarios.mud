# Declarative domain contracts; no Mud compiler/runtime executes these tests.
# Tests inject typed domain facts into the accepted ephemeral outbox.

test FeedbackSelectedEffectsAreMerged {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Player, spell = Spell.Fireball,
        aim = Aim(Point3(r1, r2, r3), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [FeedbackGroup(
            FeedbackStage.Selected,
            [FeedbackAsset("specific"), FeedbackAsset("shared"), FeedbackAsset("global")]
        )]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r1, r2, r3)
        MagicWorld.pending == empty
    }
}

test FeedbackSuccessfulAttemptHasTwoPhases {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Success, aim = Aim(Point3(r4, r5, r6), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Partial,
                [FeedbackAsset("shared"), FeedbackAsset("global")]),
            FeedbackGroup(FeedbackStage.Success,
                [FeedbackAsset("shared"), FeedbackAsset("global"), FeedbackAsset("success")])
        ]
    }
}

test FeedbackPartialAttemptHasNoSuccessPhase {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Partial, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Partial,
                [FeedbackAsset("shared"), FeedbackAsset("global")])
        ]
    }
}

test FeedbackFailedAttemptUsesFailureEffects {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.Failed, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Failed, [FeedbackAsset("failure")])
        ]
    }
}

test FeedbackCancellationRetainsItsAim {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Cancelled, caster = Player, spell = Spell.Fireball,
        aim = Aim(Point3(r7, r8, r9), empty)
    ) to MagicWorld.pending
    after {
        (count _ in PlayerFeedback.requests : true) == 1
        forall request in PlayerFeedback.requests : request.groups == [
            FeedbackGroup(FeedbackStage.Cancelled, [FeedbackAsset("cancel")])
        ]
        forall request in PlayerFeedback.requests : request.aim.point == Point3(r7, r8, r9)
    }
}

test FeedbackRejectionRetainsDuplicateEffectsWithoutProfile {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, MissingProfileFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.SelectionRejected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        (count _ in MissingProfileFeedback.requests : true) == 1
        forall request in MissingProfileFeedback.requests : request.groups == empty
        forall request in MissingProfileFeedback.requests : request.rejected ==
            [FeedbackAsset("rejected"), FeedbackAsset("rejected")]
    }
}

test FeedbackMissingProfileProducesNoRequest {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, MissingProfileFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Player, spell = Spell.Sympathy,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        MissingProfileFeedback.requests == empty
    }
}

test FeedbackModelsARealSympathyCast {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld, BoxA, BoxB,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
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
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Attempted, caster = Player, spell = Spell.Fireball,
        outcome = CastOutcome.None, aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after {
        PlayerFeedback.requests == empty
    }
}

test FeedbackRepeatedEqualFactsRemainTwoRequests {
    start with { Entity, Creature, Spellcaster, Magic, Player, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
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
            [FeedbackAsset("specific"), FeedbackAsset("shared"), FeedbackAsset("global")]
        )]
    }
}

test FeedbackIgnoresAnotherSpellcaster {
    start with { Entity, Creature, Spellcaster, Magic, Player, Turret, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
    then add SpellEvent(
        kind = SpellEventKind.Selected, caster = Turret, spell = Spell.Fireball,
        aim = Aim(Point3(r0, r0, r0), empty)
    ) to MagicWorld.pending
    after PlayerFeedback.requests == empty
}

test FeedbackFiltersAMixedCasterBatch {
    start with { Entity, Creature, Spellcaster, Magic, Player, Turret, MagicWorld,
        FeedbackChannel, PlayerFeedback, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PlanSpellFeedback }
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
