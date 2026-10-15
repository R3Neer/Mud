# Informative controller model; provider invocations are trace data, not C# calls.
# See README.md for the non-reentrant, valid-configuration boundary.

family Spell {
    slot: Nat
    None { slot = 0 },
    SympathyLink { slot = 1 },
    SympathyMagnet { slot = 2 },
    Fireball { slot = 3 },
    FireRegulator { slot = 4 },
    VeilOfInvisibility { slot = 5 },
    VeilOfAvoidance { slot = 6 },
    EarthWall { slot = 7 },
    EarthSubdivision { slot = 8 },
    ShieldOfAbsorption { slot = 9 },
    ShieldOfReflection { slot = 10 },
    WaterBubble { slot = 11 },
    WaterConnection { slot = 12 },
    PortalOfSpace { slot = 13 },
    PortalOfTime { slot = 14 },
    AirPush { slot = 15 },
    AirUpwardsCurrent { slot = 16 },
    Transmutation { slot = 17 }
}

family CastResult { None, Success, Partial, Failed }

family ProtocolKind {
    Selected, SelectionFailed, CallCast, CastAttempted,
    CallCancel, Canceled, UnlockedCountNotified
}

alias Aim {
    let x: Rum
    let y: Rum
    let z: Rum
    let hitObject: Text [0..1]
}

alias CasterSnapshot {
    let unlockedCount: Nat
    let selectedSpell: Spell
    let activeSpells: Spell [* unique]
    let concentration: Nat
}

alias ProtocolObservation {
    let kind: ProtocolKind
    let spell: Spell = Spell.None
    let result: CastResult = CastResult.None
    let aim: Aim [0..1] = empty
    let view: CasterSnapshot
}

alias SelectionPlan {
    let activate: Spell [0..1] = empty
    let cancel: Spell [0..1] = empty
    let reject: Spell [0..1] = empty
}

abstract thing Caster {
    let capacity: Nat = 17
    let maxConcentration: Nat = 2
    let configured: Spell [* unique] =
        [Spell.SympathyLink, Spell.SympathyMagnet, Spell.Fireball]
    let concentrating: Spell [* unique] =
        [Spell.SympathyLink, Spell.SympathyMagnet]

    mut unlockedCount: Nat = 3
    mut selectedSpell: Spell = Spell.None
    mut activeSpells: Spell [* unique] = empty

    # Auxiliary observations of the last invocation of each Boolean method.
    mut selectionAccepted: Bool = false
    mut castFinished: Bool = true
    mut lastTrace: ProtocolObservation [* ordered] = empty

    let concentration := count spell in activeSpells : concentrating has spell
    let concentrationFull := concentration >= maxConcentration
    let snapshot := CasterSnapshot(
        unlockedCount, selectedSpell, activeSpells, concentration
    )

    let resolvable: Spell --> Bool [ordered] :=
        _ --> value.slot > 0 and value.slot <= unlockedCount
            and (configured has value)

    let selection: Spell --> SelectionPlan [ordered] :=
        activeSpells has value --> SelectionPlan(cancel = [value]),
        value.slot == 0 or value.slot > unlockedCount -->
            SelectionPlan(reject = [value]),
        configured has not value --> SelectionPlan(reject = [value]),
        (concentrating has value) and concentrationFull -->
            SelectionPlan(reject = [value]),
        _ --> SelectionPlan(activate = [value])

    let clampUnlocked: Int --> Nat [ordered] :=
        value < 0 --> 0,
        value > capacity --> capacity,
        _ --> value to Nat
}

thing PlayerCaster as Caster
thing NoConcentrationCaster as Caster { maxConcentration = 0 }
thing ThreeConcentrationCaster as Caster {
    concentrating = [Spell.SympathyLink, Spell.SympathyMagnet, Spell.Fireball]
}

subaction Record for caster: Caster [mut] given
    kind: ProtocolKind,
    spell: Spell = Spell.None,
    result: CastResult = CastResult.None,
    aim: Aim [0..1] = empty {
    then {
        let view = caster.snapshot
        add ProtocolObservation(
            kind = kind, spell = spell, result = result, aim = aim, view = view
        ) to caster.lastTrace
    }
}

subaction CancelOne for caster: Caster [mut] given requested: Spell {
    then foreach spell in [requested] if caster.resolvable[spell] : {
        remove spell from caster.activeSpells
        caster.Record(ProtocolKind.CallCancel, spell)
        caster.Record(ProtocolKind.Canceled, spell)
        foreach selected in [caster.selectedSpell] if selected == spell :
            caster.selectedSpell = Spell.None
    }
}

action Select for caster: Caster [mut] given requested: Spell {
    then {
        let plan = caster.selection[requested]
        caster.lastTrace = empty
        caster.selectionAccepted = false
        foreach spell in plan.cancel : caster.CancelOne(spell)
        foreach spell in plan.activate : {
            add spell to caster.activeSpells
            caster.selectedSpell = spell
            caster.Record(ProtocolKind.Selected, spell)
            caster.selectionAccepted = true
        }
        foreach spell in plan.reject :
            caster.Record(ProtocolKind.SelectionFailed, spell)
    }
}

action AdjustUnlocked for caster: Caster [mut] given amount: Int {
    then {
        let next = caster.clampUnlocked[caster.unlockedCount + amount]
        caster.lastTrace = empty
        caster.unlockedCount = next
        caster.Record(ProtocolKind.UnlockedCountNotified)
    }
}

action CancelSelected for caster: Caster [mut] {
    then {
        let requested = caster.selectedSpell
        caster.lastTrace = empty
        caster.CancelOne(requested)
    }
}

action SelfCancelledSample for caster: Caster [mut] given requested: Spell {
    then {
        caster.lastTrace = empty
        caster.CancelOne(requested)
    }
}

action CastSample for caster: Caster [mut] given result: CastResult, aim: Aim {
    then {
        let selected = caster.selectedSpell
        caster.lastTrace = empty
        caster.castFinished = true
        foreach spell in [selected] if caster.resolvable[spell] : {
            caster.Record(ProtocolKind.CallCast, spell, aim = [aim])
            caster.Record(ProtocolKind.CastAttempted, spell, result, [aim])
            caster.castFinished = result == CastResult.Success
            foreach completed in [spell] if result == CastResult.Success : {
                foreach instant in [completed] if caster.concentrating has not instant :
                    remove instant from caster.activeSpells
                caster.selectedSpell = Spell.None
            }
        }
    }
}

action StartSample for caster: Caster [mut] {
    then {
        caster.lastTrace = empty
        caster.Record(ProtocolKind.UnlockedCountNotified)
    }
}

look Observation for caster: Caster {
    let state := caster.snapshot
    let selectionAccepted := caster.selectionAccepted
    let castFinished := caster.castFinished
    let trace := caster.lastTrace
}
