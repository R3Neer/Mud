part only

using spells

# One attempt owns preparation, optional link creation and outcome completion.
subaction AttemptSympathy
for magic: Magic [mut], caster: Spellcaster [mut]
given aim: Aim {
    then {
        let plan = (magic, caster).PlanSympathy(aim).plan

        foreach target in plan.prepare :
            caster.prepared = target

        foreach pair in plan.pair :
            (magic, caster).EstablishSympathyLink(pair, aim)

        (magic, caster).ResolveAttempt(Spell.Sympathy, plan.outcome, aim)
    }
}
