part only

using world
using spells
using sympathy
using fixtures
using feedback

# Profile, occurrence, filtering and end-to-end feedback source contracts.

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
