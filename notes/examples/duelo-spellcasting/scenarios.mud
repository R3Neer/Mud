# Declarative examples for future execution; no Mud runtime is available yet.
# Each test starts a fresh world and activates its own fixture.

test SelectionReservesConcentration {
    start with PlayerCaster
    then PlayerCaster.Select(Spell.SympathyLink)
    after {
        PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.activeSpells == [Spell.SympathyLink]
        PlayerCaster.concentration == 1
    }
}

test SwitchingDoesNotDeactivateAnInstantSpell {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.Select(Spell.SympathyLink)
    }
    after {
        PlayerCaster.activeSpells == [Spell.Fireball, Spell.SympathyLink]
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.concentration == 1
    }
}

test TogglingBackgroundSpellReturnsFalseWithoutFailure {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.Select(Spell.SympathyLink)
    }
    after {
        not PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.Fireball
        PlayerCaster.activeSpells == [Spell.Fireball]
        PlayerCaster.concentration == 0
        PlayerCaster.lastTrace == [
            ProtocolObservation(
                kind = ProtocolKind.CallCancel,
                spell = Spell.SympathyLink,
                view = CasterSnapshot(3, Spell.Fireball, [Spell.Fireball], 0)
            ),
            ProtocolObservation(
                kind = ProtocolKind.Canceled,
                spell = Spell.SympathyLink,
                view = CasterSnapshot(3, Spell.Fireball, [Spell.Fireball], 0)
            )
        ]
    }
}

test FullConcentrationRejectsThirdSpell {
    start with ThreeConcentrationCaster
    then {
        ThreeConcentrationCaster.Select(Spell.SympathyLink)
        ThreeConcentrationCaster.Select(Spell.SympathyMagnet)
        ThreeConcentrationCaster.Select(Spell.Fireball)
    }
    after {
        not ThreeConcentrationCaster.selectionAccepted
        ThreeConcentrationCaster.concentration == 2
        ThreeConcentrationCaster.selectedSpell == Spell.SympathyMagnet
        ThreeConcentrationCaster.activeSpells == [Spell.SympathyLink, Spell.SympathyMagnet]
        (count event in ThreeConcentrationCaster.lastTrace :
            event.kind == ProtocolKind.SelectionFailed) == 1
    }
}

test ZeroLimitRejectsConcentration {
    start with NoConcentrationCaster
    then NoConcentrationCaster.Select(Spell.SympathyLink)
    after {
        not NoConcentrationCaster.selectionAccepted
        NoConcentrationCaster.activeSpells == empty
        NoConcentrationCaster.concentration == 0
    }
}

test ZeroLimitStillAllowsInstantSpells {
    start with NoConcentrationCaster
    then NoConcentrationCaster.Select(Spell.Fireball)
    after {
        NoConcentrationCaster.selectionAccepted
        NoConcentrationCaster.selectedSpell == Spell.Fireball
        NoConcentrationCaster.concentration == 0
    }
}

test LockedSelectionPreservesCurrentSpell {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.Select(Spell.Transmutation)
    }
    after {
        not PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.activeSpells == [Spell.SympathyLink]
    }
}

test UnlockedDoesNotMeanConfigured {
    start with PlayerCaster
    then {
        PlayerCaster.AdjustUnlocked(1)
        PlayerCaster.Select(Spell.FireRegulator)
    }
    after {
        PlayerCaster.unlockedCount == 4
        not PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.None
        PlayerCaster.activeSpells == empty
    }
}

test NoneIsAnActualIncompleteCastResult {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.CastSample(CastResult.None, Aim(r0, r0, r0, empty))
    }
    after {
        not PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.activeSpells == [Spell.SympathyLink]
        (count event in PlayerCaster.lastTrace : event.kind == ProtocolKind.CastAttempted) == 1
    }
}

test PartialCastKeepsTargeting {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.CastSample(CastResult.Partial, Aim(r0, r0, r0, ["crate"]))
    }
    after {
        not PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.concentration == 1
    }
}

test FailedCastKeepsTargeting {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.CastSample(CastResult.Failed, Aim(r0, r0, r0, ["crate"]))
    }
    after {
        not PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.concentration == 1
    }
}

test SuccessfulInstantCastNotifiesBeforeCleanup {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, ["crate"]))
    }
    after {
        PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.None
        PlayerCaster.activeSpells == empty
        PlayerCaster.lastTrace == [
            ProtocolObservation(
                kind = ProtocolKind.CallCast,
                spell = Spell.Fireball,
                aim = [Aim(r0, r0, r0, ["crate"])],
                view = CasterSnapshot(3, Spell.Fireball, [Spell.Fireball], 0)
            ),
            ProtocolObservation(
                kind = ProtocolKind.CastAttempted,
                spell = Spell.Fireball,
                result = CastResult.Success,
                aim = [Aim(r0, r0, r0, ["crate"])],
                view = CasterSnapshot(3, Spell.Fireball, [Spell.Fireball], 0)
            )
        ]
    }
}

test SuccessfulConcentrationCastRetainsActivity {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, ["crate"]))
    }
    after {
        PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.None
        PlayerCaster.activeSpells == [Spell.SympathyLink]
        PlayerCaster.concentration == 1
    }
}

test NoSelectionDoesNotCallProvider {
    start with PlayerCaster
    then PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, empty))
    after {
        PlayerCaster.castFinished
        PlayerCaster.lastTrace == empty
    }
}

test RelockedSelectedSpellCannotBeCast {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.AdjustUnlocked(-3)
        PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, empty))
    }
    after {
        PlayerCaster.unlockedCount == 0
        PlayerCaster.castFinished
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.activeSpells == [Spell.SympathyLink]
        PlayerCaster.concentration == 1
        PlayerCaster.lastTrace == empty
    }
}

test RelockedActiveToggleIsSilent {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.AdjustUnlocked(-3)
        PlayerCaster.CancelSelected()
        PlayerCaster.Select(Spell.SympathyLink)
    }
    after {
        not PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.SympathyLink
        PlayerCaster.activeSpells == [Spell.SympathyLink]
        PlayerCaster.lastTrace == empty
    }
}

test UnlockingAgainAllowsCancellation {
    start with PlayerCaster
    then {
        PlayerCaster.Select(Spell.SympathyLink)
        PlayerCaster.AdjustUnlocked(-3)
        PlayerCaster.AdjustUnlocked(3)
        PlayerCaster.CancelSelected()
    }
    after {
        PlayerCaster.selectedSpell == Spell.None
        PlayerCaster.activeSpells == empty
        PlayerCaster.concentration == 0
        forall event in PlayerCaster.lastTrace :
            event.view.selectedSpell == Spell.SympathyLink
    }
}

test SelfCancellationOfInactiveProviderStillNotifies {
    start with PlayerCaster
    then PlayerCaster.SelfCancelledSample(Spell.SympathyLink)
    after {
        PlayerCaster.activeSpells == empty
        (count event in PlayerCaster.lastTrace : event.kind == ProtocolKind.CallCancel) == 1
        (count event in PlayerCaster.lastTrace : event.kind == ProtocolKind.Canceled) == 1
    }
}

test UnchangedUnlockCountStillNotifies {
    start with PlayerCaster
    then {
        PlayerCaster.AdjustUnlocked(100)
        PlayerCaster.AdjustUnlocked(1)
    }
    after {
        PlayerCaster.unlockedCount == 17
        PlayerCaster.lastTrace == [ProtocolObservation(
            kind = ProtocolKind.UnlockedCountNotified,
            view = CasterSnapshot(17, Spell.None, empty, 0)
        )]
    }
}

test NoneSelectionNotifiesFailure {
    start with PlayerCaster
    then PlayerCaster.Select(Spell.None)
    after {
        not PlayerCaster.selectionAccepted
        PlayerCaster.lastTrace == [ProtocolObservation(
            kind = ProtocolKind.SelectionFailed,
            spell = Spell.None,
            view = CasterSnapshot(3, Spell.None, empty, 0)
        )]
    }
}

test NoneCancellationIsSilent {
    start with PlayerCaster
    then PlayerCaster.CancelSelected()
    after {
        not PlayerCaster.selectionAccepted
        PlayerCaster.selectedSpell == Spell.None
        PlayerCaster.lastTrace == empty
    }
}

test StartAnnouncesInitialCount {
    start with PlayerCaster
    then PlayerCaster.StartSample()
    after PlayerCaster.lastTrace == [ProtocolObservation(
        kind = ProtocolKind.UnlockedCountNotified,
        view = CasterSnapshot(3, Spell.None, empty, 0)
    )]
}
