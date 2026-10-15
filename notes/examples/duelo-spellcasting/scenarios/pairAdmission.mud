part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.PairAdmission]

using configuration
using world
using spells
using sympathy
using fixtures

# Cross-entity preparation and pair revalidation source contracts.

test SharedPreparationDoesNotReserveAnEndpoint {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, Turret, BoxA, BoxB, BoxC
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
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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

test MissingAndUnsuitableHitsDoNotAcquireExtraConcentration {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, Unshaped
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
