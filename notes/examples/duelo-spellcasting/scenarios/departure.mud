part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Lifecycle]

using configuration
using world
using spells
using sympathy
using fixtures

# Atomic participant/caster departure source contracts.

test ParticipantDepartureClosesLinksAndReleasesTheirOwner {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        BoxA.ownEffects = "red" -> EffectValue("red", 10 s, 2)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
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
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxB]))
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

test DepartingCasterReleasesPreparationWithoutAnyLink {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), [BoxA]))
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
