part only

using world
using spells
using sympathy
using fixtures

# Atomic participant/caster departure source contracts.

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
