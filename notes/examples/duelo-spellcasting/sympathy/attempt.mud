part only

using spells

# One attempt owns preparation, optional link creation and outcome completion.
subaction AttemptSympathy
for magic: Magic [mut], caster: Spellcaster [mut]
given aim: Aim {
    then {
        let plan = (magic, caster).PlanSympathy(aim).plan

        let prepared := foreach preparation in plan
            if preparation is SympathyPreparation --> preparation.target
        caster.prepared = prepared[?]

        let pairs := foreach ready in plan if ready is SympathyReady --> ready.pair
        (magic, caster).EstablishSympathyLink(pairs[?], aim)

        (magic, caster).ResolveAttempt(Spell.Sympathy, plan.outcome, aim)
    }
}
