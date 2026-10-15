part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Contributions]

using configuration
using world
using spells
using sympathy
using fixtures

# Live origins, inversion, cleanup and stable orientation source contracts.

test BorrowedEffectsStayLiveWithoutOverwritingOwnEffects {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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
    ~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Contributions, configuration.TestConcern.Lifecycle]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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

test LaterGrabbingDoesNotReorientAnExistingLink {
    ~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Contributions, configuration.TestConcern.PairAdmission]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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
