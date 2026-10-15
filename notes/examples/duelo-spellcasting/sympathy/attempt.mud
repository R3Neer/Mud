part only

using spells

# One attempt owns preparation, optional link creation and outcome completion.
subaction AttemptSympathy
for magic: Magic [mut], caster: Spellcaster [mut]
given aim: Aim {
    then {
        let plan = (magic, caster).PlanSympathy(aim).plan

        caster.prepared = plan.prepare[?]

        (magic, caster).EstablishSympathyLink(plan.pair[?], aim)

        (magic, caster).ResolveAttempt(Spell.Sympathy, plan.outcome, aim)
    }
}
