# Accepted Mud domain contracts, not tests of Unity's historical quirks.
# Declarative source examples: no Mud compiler or runtime executes these yet.

test SharedPreparationDoesNotReserveAnEndpoint {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, Turret,
        BoxA, BoxB, BoxC, CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Turret).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Turret).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, Turret).Cast(Aim(Point3(r0, r0, r0), [BoxC]))
    }
    after {
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links :
            link.owner == Player and link.leader == BoxA and link.follower == BoxB
        Turret.prepared == [BoxA]
        Turret.selected == [Spell.Sympathy]
        Player.concentration == 1 and Turret.concentration == 1
        (count event in MagicWorld.published : event.caster == Turret
            and event.kind == SpellEventKind.Attempted and event.outcome == CastOutcome.Failed) == 1
    }
}

test PairCreationRevalidatesThePreparedShape {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        BoxA.shape = Shape.Sphere
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
    }
    after {
        MagicWorld.links == empty
        Player.prepared == [BoxA]
        Player.concentration == 1
        (count event in MagicWorld.published : event.kind == SpellEventKind.Linked) == 0
        (count event in MagicWorld.published : event.kind == SpellEventKind.Attempted
            and event.outcome == CastOutcome.Failed) == 1
    }
}

test PairCreationRevalidatesSharedCapabilities {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        BoxA.kinds = [SympathyKind.Motion]
        BoxB.kinds = [SympathyKind.SharedEffects]
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
    }
    after {
        MagicWorld.links == empty
        Player.selected == [Spell.Sympathy]
        Player.activeSpells == [Spell.Sympathy]
        (count event in MagicWorld.published : event.kind == SpellEventKind.Attempted
            and event.outcome == CastOutcome.Failed) == 1
    }
}

test BorrowedEffectsStayLiveWithoutOverwritingOwnEffects {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        BoxA.ownEffects = "heat" -> EffectValue("heat", 10, 2)
        BoxB.ownEffects = "heat" -> EffectValue("heat", 20, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        BoxA.ownEffects = "heat" -> EffectValue("heat", 13, 5)
    }
    after {
        BoxB.ownEffects == ("heat" -> EffectValue("heat", 20, 7))
        (MagicWorld, BoxB).EffectiveEffects().own == BoxB.ownEffects
        (MagicWorld, BoxB).EffectiveEffects().borrowed == [BorrowedEffects(
            1, BoxA, "heat" -> EffectValue("heat", 13, 5)
        )]
        Player.selected == empty and Player.concentration == 1
    }
}

test InversionReversesOnlyBorrowedContributions {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        BoxA.ownEffects = "red" -> EffectValue("red", 10, 2)
        BoxB.ownEffects = "blue" -> EffectValue("blue", 20, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, BoxB).Invert(1)
    }
    after {
        BoxA.ownEffects == ("red" -> EffectValue("red", 10, 2))
        BoxB.ownEffects == ("blue" -> EffectValue("blue", 20, 7))
        (MagicWorld, BoxA).EffectiveEffects().borrowed == [BorrowedEffects(
            1, BoxB, "blue" -> EffectValue("blue", 20, 7)
        )]
        (MagicWorld, BoxB).EffectiveEffects().borrowed == empty
        forall link in MagicWorld.links : link.leader == BoxB and link.follower == BoxA
        Player.concentration == 1
    }
}

test CancellationDoesNotPersistBorrowedEffects {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        BoxA.ownEffects = "red" -> EffectValue("red", 10, 2)
        BoxB.ownEffects = "blue" -> EffectValue("blue", 20, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, Player).CancelSpell(Spell.Sympathy)
    }
    after {
        MagicWorld.links == empty
        BoxB.ownEffects == ("blue" -> EffectValue("blue", 20, 7))
        (MagicWorld, BoxB).EffectiveEffects().borrowed == empty
        Player.activeSpells == empty and Player.concentration == 0
    }
}

test ParticipantDepartureClosesLinksAndReleasesTheirOwner {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        BoxA.ownEffects = "red" -> EffectValue("red", 10, 2)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, BoxA).LeaveWorld()
    }
    after {
        not BoxA.present
        MagicWorld.links == empty
        Player.activeSpells == empty and Player.concentration == 0
        Player.selected == empty and Player.prepared == empty
        (MagicWorld, BoxB).EffectiveEffects().borrowed == empty
        (count event in MagicWorld.published : event.kind == SpellEventKind.Unlinked) == 1
        (count event in MagicWorld.published : event.kind == SpellEventKind.Cancelled) == 1
    }
}

test CasterDepartureAlsoClosesLinksBetweenOtherEntities {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, Player).LeaveWorld()
    }
    after {
        not Player.present
        BoxA.present and BoxB.present
        MagicWorld.links == empty
        Player.activeSpells == empty and Player.concentration == 0
        (count event in MagicWorld.published : event.kind == SpellEventKind.Unlinked) == 1
    }
}

test RepeatedCancellationProducesNoDuplicateDomainFacts {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        (MagicWorld, Player).CancelSpell(Spell.Sympathy)
        (MagicWorld, Player).CancelSpell(Spell.Sympathy)
    }
    after {
        MagicWorld.links == empty and Player.activeSpells == empty
        (count event in MagicWorld.published : event.kind == SpellEventKind.Cancelled) == 1
        (count event in MagicWorld.published : event.kind == SpellEventKind.Unlinked) == 1
    }
}

test RelockingDoesNotTrapAnActiveSpell {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        Player.SetUnlocked(0)
        (MagicWorld, Player).CancelSpell(Spell.Sympathy)
    }
    after {
        Player.unlocked == 0
        MagicWorld.links == empty
        Player.activeSpells == empty and Player.concentration == 0
        (count event in MagicWorld.published : event.kind == SpellEventKind.Cancelled) == 1
    }
}

test LaterGrabbingDoesNotReorientAnExistingLink {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxB]))
        BoxB.grabbed = true
    }
    after {
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links : link.leader == BoxA and link.follower == BoxB
        (MagicWorld, BoxB).Sympathy().invertible == [1]
        (count event in MagicWorld.published : event.kind == SpellEventKind.Inverted) == 0
    }
}

test MissingAndUnsuitableHitsDoNotAcquireExtraConcentration {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, Unshaped,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), empty))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [Unshaped]))
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
    }
    after {
        Player.concentration == 1
        Player.prepared == [BoxA] and Player.selected == [Spell.Sympathy]
        MagicWorld.links == empty
        exists event in MagicWorld.published : event.kind == SpellEventKind.Attempted
            and event.outcome == CastOutcome.Partial
    }
}

test DepartingCasterReleasesPreparationWithoutAnyLink {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0, r0, r0), [BoxA]))
        (MagicWorld, Player).LeaveWorld()
    }
    after {
        not Player.present
        Player.selected == empty and Player.prepared == empty
        Player.activeSpells == empty and Player.concentration == 0
        MagicWorld.links == empty and BoxA.present
        (count event in MagicWorld.published : event.kind == SpellEventKind.Cancelled) == 1
    }
}

test LinkEffectFactsKeepTheirOwnOrientation {
    start with {
        Entity, Creature, Spellcaster, Magic, MagicWorld, Player, BoxA, BoxB,
        CanSelect, CanAttempt, TargetUsable, CanLink,
        ConcentrationWithinLimit, ExclusiveSympathy, PublishSpellEvents, PrepareLinkEffects
    }
    then {
        # Isolate a single publication containing two immutable domain facts.
        add SpellEvent(kind = SpellEventKind.Linked, caster = Player, spell = Spell.Sympathy,
            aim = Aim(Point3(r0, r0, r0), [BoxB]),
            link = [LinkSnapshot(1, Player, BoxA, BoxB, [SympathyKind.Motion])]) to MagicWorld.pending
        add SpellEvent(kind = SpellEventKind.Inverted, caster = Player, spell = Spell.Sympathy,
            aim = Aim(Point3(r0, r0, r0), [BoxA]),
            link = [LinkSnapshot(1, Player, BoxB, BoxA, [SympathyKind.Motion])]) to MagicWorld.pending
    }
    after {
        (count event in MagicWorld.linkEffects : true) == 2
        forall event in MagicWorld.linkEffects : forall link in event.link :
            link.id == 1 and
                ((event.kind == SpellEventKind.Linked and link.leader == BoxA and link.follower == BoxB)
                or (event.kind == SpellEventKind.Inverted and link.leader == BoxB and link.follower == BoxA))
    }
}
