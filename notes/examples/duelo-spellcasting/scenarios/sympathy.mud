part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.PairAdmission]

using configuration
using world
using spells
using sympathy
using fixtures

# Sympathy provider source contracts; no compiler/runtime executes these yet.

test NoHitIsNoneRatherThanARejection {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), empty))
    }
    after {
        Player.prepared == empty
        (count event in MagicWorld.published :
            event.kind == SpellEventKind.Attempted and event.outcome == CastOutcome.None) == 1
    }
}

test FirstTargetPreparesWithoutReservingEndpoint {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r1 m, r2 m, r3 m), [BoxA]))
    }
    after {
        Player.preparation == [BoxA]
        MagicWorld.links == empty
        (MagicWorld, BoxA).TargetUsable()
        (count event in MagicWorld.published :
            event.kind == SpellEventKind.Attempted and event.outcome == CastOutcome.Partial) == 1
    }
}

test SuccessfulLinkEndsTargetingButKeepsConcentration {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.PairAdmission,
        configuration.TestConcern.Lifecycle
    ]

    start with {
        ActivationSelection([ActivationFeature.LinkEffects]).declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r4 m, r5 m, r6 m), [BoxB]))
    }
    after {
        Player.selected == empty and Player.prepared == empty
        Player.activeSpells == [Spell.Sympathy] and Player.concentration == 1
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links : link.leader == BoxA and link.follower == BoxB
        (count event in MagicWorld.published :
            event.kind == SpellEventKind.Attempted and event.outcome == CastOutcome.Success) == 1
    }
}

test InitialOrientationPrefersGrabbedFollower {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.PairAdmission,
        configuration.TestConcern.Contributions
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        BoxB.grabbed = true
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
    }
    after {
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links : link.leader == BoxB and link.follower == BoxA
    }
}

test InversionChangesTheRelationWithoutAnInteractorCache {
    ~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Contributions]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
        (MagicWorld, BoxB).Invert(LinkId(1))
    }
    after {
        (count link in MagicWorld.links : true) == 1
        forall link in MagicWorld.links :
            link.id == LinkId(1) and link.leader == BoxB and link.follower == BoxA
        (count event in MagicWorld.published : event.kind == SpellEventKind.Inverted) == 1
        Player.activeSpells == [Spell.Sympathy]
    }
}

test TargetDepartureInvalidatesPreparationWithoutEndingTheSpell {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.Lifecycle,
        configuration.TestConcern.PairAdmission
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, BoxA).LeaveWorld()
    }
    after {
        not BoxA.present
        Player.preparation == empty
        Player.activeSpells == [Spell.Sympathy]
        Player.concentration == 1
        MagicWorld.links == empty
    }
}
