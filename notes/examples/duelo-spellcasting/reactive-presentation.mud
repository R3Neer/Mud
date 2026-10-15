# Optional Mud-oriented consumer variant; not the synchronous Unity trace.
# Activate SpellPresentation, PlayerPresentation and UpdateTargetingPresentation
# together with the controller fixtures and ConcentrationWithinLimit.

abstract thing SpellPresentation {
    let caster: Caster
    mut targetingVisible: Bool = false
}

thing PlayerPresentation as SpellPresentation {
    caster = PlayerCaster
}

rule UpdateTargetingPresentation on presentation: SpellPresentation [mut] {
    when presentation.caster.castFinished changes
        or presentation.caster.selectedSpell changes
    then presentation.targetingVisible =
        not presentation.caster.castFinished
            and presentation.caster.selectedSpell != Spell.None
}

test FailedCastKeepsTargetingPresentation {
    start with {
        Caster, IsResolvable, ConcentrationWithinLimit, PlayerCaster,
        SpellPresentation, PlayerPresentation, UpdateTargetingPresentation
    }
    then {
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.CastSample(CastResult.Failed, Aim(r0, r0, r0, empty))
    }
    after PlayerPresentation.targetingVisible
}

test SuccessfulCastHidesTargetingPresentation {
    start with {
        Caster, IsResolvable, ConcentrationWithinLimit, PlayerCaster,
        SpellPresentation, PlayerPresentation, UpdateTargetingPresentation
    }
    then {
        PlayerCaster.Select(Spell.Fireball)
        PlayerCaster.CastSample(CastResult.Failed, Aim(r0, r0, r0, empty))
        PlayerCaster.CastSample(CastResult.Success, Aim(r0, r0, r0, empty))
    }
    after not PlayerPresentation.targetingVisible
}
