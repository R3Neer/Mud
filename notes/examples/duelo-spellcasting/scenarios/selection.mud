part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Selection]

using configuration
using world
using spells
using sympathy
using fixtures

# Declarative source contracts; each test starts a fresh world. Not executed Mud tests.

test SelectionReservesConcentrationBeforeLink {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then (MagicWorld, Player).SelectSpell(Spell.Sympathy)
    after {
        Player.selected == [Spell.Sympathy]
        Player.activeSpells == [Spell.Sympathy]
        Player.concentration == 1
        Player.prepared == empty
        MagicWorld.links == empty
        (count event in MagicWorld.published : event.kind == SpellEventKind.Selected) == 1
    }
}

test CapabilityBelongsToTheActualEntity {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, Turret
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Turret).SelectSpell(Spell.Sympathy)
    }
    after {
        Player is Creature
        Player is Spellcaster
        Turret is Entity
        Turret is Spellcaster
        Player != Turret
        Player.concentration == 1 and Turret.concentration == 1
    }
}

test SelectionToggleEndsTheSameSpell {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.Selection,
        configuration.TestConcern.Lifecycle
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
    }
    after {
        Player.selected == empty and Player.activeSpells == empty
        Player.concentration == 0
        (count event in MagicWorld.published : event.kind == SpellEventKind.Cancelled) == 1
    }
}

test UnconfiguredSpellIsNormalDomainRejection {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then (MagicWorld, Player).SelectSpell(Spell.Fireball)
    after {
        Player.activeSpells == empty
        (count event in MagicWorld.published : event.kind == SpellEventKind.SelectionRejected) == 1
    }
}

test RepeatedFailedAttemptsPreservePreparationAndReservation {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, Unshaped
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        let aim = Aim(Point3(r1 m, r2 m, r3 m), [Unshaped])
        (MagicWorld, Player).Cast(aim)
        (MagicWorld, Player).Cast(aim)
    }
    after {
        (count event in MagicWorld.published :
            event.kind == SpellEventKind.Attempted and event.outcome == CastOutcome.Failed) >= 1
        Player.prepared == empty
        Player.concentration == 1
        MagicWorld.pending == empty
    }
}

test CastingWithoutSelectionRefusesWithoutAttempt {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then {
        # Capture the refused child instead of propagating its refusal.
        let reply = (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), empty))
    }
    after {
        (imagine (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), empty))) is IfRefusal
        Player.selected == empty and Player.activeSpells == empty
        MagicWorld.published == empty and MagicWorld.pending == empty
    }
}

test NoConcentrationRoomRejectsSelection {
    start with {
        ActivationSelection().declarations,
        MagicWorld, NoFocus
    }
    then (MagicWorld, NoFocus).SelectSpell(Spell.Sympathy)
    after {
        NoFocus.activeSpells == empty
        NoFocus.concentration == 0
        (count event in MagicWorld.published : event.kind == SpellEventKind.SelectionRejected) == 1
    }
}

test InstantProviderCompletionProtocolReleasesActivity {
    ~checks: configuration.TestConcern [1..* unique] = [
        configuration.TestConcern.Selection,
        configuration.TestConcern.Lifecycle
    ]

    start with {
        ActivationSelection().declarations,
        MagicWorld, InstantProtocolCaster
    }
    then {
        (MagicWorld, InstantProtocolCaster).SelectSpell(Spell.Fireball)
        # A fixture supplies the result of a hypothetical Mud spell body.
        # This is not Fireball implementation or a host result endpoint.
        (MagicWorld, InstantProtocolCaster).ResolveAttempt(
            Spell.Fireball, CastOutcome.Success, Aim(Point3(r0 m, r0 m, r0 m), empty)
        )
    }
    after {
        InstantProtocolCaster.selected == empty
        InstantProtocolCaster.activeSpells == empty
        (count event in MagicWorld.published : event.kind == SpellEventKind.Attempted) == 1
    }
}

test CastingUnsupportedProviderRefusesWithoutAttempt {
    start with {
        ActivationSelection().declarations,
        MagicWorld, InstantProtocolCaster
    }
    then {
        (MagicWorld, InstantProtocolCaster).SelectSpell(Spell.Fireball)
        let reply = (MagicWorld, InstantProtocolCaster).Cast(
            Aim(Point3(r0 m, r0 m, r0 m), empty)
        )
    }
    after {
        (imagine (MagicWorld, InstantProtocolCaster).Cast(
            Aim(Point3(r0 m, r0 m, r0 m), empty)
        )) is IfRefusal
        InstantProtocolCaster.selected == [Spell.Fireball]
        InstantProtocolCaster.activeSpells == [Spell.Fireball]
        (count event in MagicWorld.published : event.kind == SpellEventKind.Attempted) == 0
        MagicWorld.pending == empty
    }
}

test CastingUnavailableSelectionRefusesWithoutAttempt {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player
    }
    then {
        (MagicWorld, Player).SelectSpell(Spell.Sympathy)
        Player.unlocked = 0
        let reply = (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), empty))
    }
    after {
        (imagine (MagicWorld, Player).Cast(Aim(Point3(r0 m, r0 m, r0 m), empty))) is IfRefusal
        Player.selected == [Spell.Sympathy] and Player.activeSpells == [Spell.Sympathy]
        (count event in MagicWorld.published : event.kind == SpellEventKind.Attempted) == 0
        MagicWorld.pending == empty
    }
}
