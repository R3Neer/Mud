part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Lifecycle]

using configuration
using world
using spells
using sympathy
using fixtures

# Cancellation, relocking and frozen occurrence context source contracts.

test RepeatedCancellationProducesNoDuplicateDomainFacts {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA, BoxB
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

test LinkEffectFactsKeepTheirOwnOrientation {
    ~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Lifecycle, configuration.TestConcern.Contributions]

    start with {
        ActivationSelection([ActivationFeature.LinkEffects]).declarations,
        MagicWorld, Player, BoxA, BoxB
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
