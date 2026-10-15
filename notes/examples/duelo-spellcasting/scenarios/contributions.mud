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
        BoxA.ownEffects = "heat" -> EffectValue("heat", 10 s, 2)
        BoxB.ownEffects = "heat" -> EffectValue("heat", 20 s, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
        BoxA.ownEffects = "heat" -> EffectValue("heat", 13 s, 5)
    }
    after {
        BoxB.ownEffects == ("heat" -> EffectValue("heat", 20 s, 7))
        (MagicWorld, BoxB).EffectiveEffects().own == BoxB.ownEffects
        (MagicWorld, BoxB).EffectiveEffects().borrowed == [BorrowedEffects(
            LinkId(1),
            BoxA,
            "heat" -> EffectValue("heat", 13 s, 5)
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
        BoxA.ownEffects = "red" -> EffectValue("red", 10 s, 2)
        BoxB.ownEffects = "blue" -> EffectValue("blue", 20 s, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
        (MagicWorld, BoxB).Invert(LinkId(1))
    }
    after {
        BoxA.ownEffects == ("red" -> EffectValue("red", 10 s, 2))
        BoxB.ownEffects == ("blue" -> EffectValue("blue", 20 s, 7))
        (MagicWorld, BoxA).EffectiveEffects().borrowed == [BorrowedEffects(
            LinkId(1),
            BoxB,
            "blue" -> EffectValue("blue", 20 s, 7)
        )]
        (MagicWorld, BoxB).EffectiveEffects().borrowed == empty
        forall link in MagicWorld.links : link.leader == BoxB and link.follower == BoxA
        Player.concentration == 1
    }
}

test CancellationDoesNotPersistBorrowedEffects {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.Contributions,
        configuration.TestConcern.Lifecycle
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        BoxA.ownEffects = "red" -> EffectValue("red", 10 s, 2)
        BoxB.ownEffects = "blue" -> EffectValue("blue", 20 s, 7)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
        (MagicWorld, Player).CancelSpell(Spell.Sympathy)
    }
    after {
        MagicWorld.links == empty
        BoxB.ownEffects == ("blue" -> EffectValue("blue", 20 s, 7))
        (MagicWorld, BoxB).EffectiveEffects().borrowed == empty
        Player.activeSpells == empty and Player.concentration == 0
    }
}

test LaterGrabbingDoesNotReorientAnExistingLink {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.Contributions,
        configuration.TestConcern.PairAdmission
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
        BoxB.grabbed = true
    }
    after {
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links : link.leader == BoxA and link.follower == BoxB
        (MagicWorld, BoxB).Sympathy().invertible == [LinkId(1)]
        (count event in MagicWorld.published : event.kind == SpellEventKind.Inverted) == 0
    }
}
