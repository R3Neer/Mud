part only

using spells

# Pure classification; it does not reserve participants or modify targeting.
sublook PlanSympathy
for magic: Magic, caster: Spellcaster
given aim: Aim {
    let plan: SympathyPlan := {
        let decision: Aim --> SympathyPlan [ordered] =
            .target == empty -->
                SympathyPlan(outcome = CastOutcome.None),
            not (exists target in .target : (magic, target).TargetUsable()) -->
                SympathyPlan(outcome = CastOutcome.Failed),
            caster.preparation == empty -->
                SympathyPlan(
                    outcome = CastOutcome.Partial,
                    prepare = .target
                ),
            {
                exists leader in caster.preparation :
                    exists follower in .target :
                        (magic, leader, follower).CanLink()
            } -->
                SympathyPlan(
                    outcome = CastOutcome.Success,
                    pair = [SympathyPair(caster.preparation[?], .target[?])]
                ),
            _ --> SympathyPlan(outcome = CastOutcome.Failed)
        decision[aim]
    }
}
