part only

using spells

# Pure classification; it does not reserve participants or modify targeting.
sublook PlanSympathy
for magic: Magic, caster: Spellcaster
given aim: Aim {
    let plan := {
        let decision: Aim -->[ordered]
            (SympathyStopped | SympathyPreparation | SympathyReady) =
                .target == empty -->
                    SympathyStopped(CastOutcome.None),
                not (exists target in .target : (magic, target).TargetUsable()) -->
                    SympathyStopped(CastOutcome.Failed),
                caster.preparation == empty -->
                    SympathyPreparation(.target[?]),
                {
                    exists leader in caster.preparation :
                        exists follower in .target :
                            (magic, leader, follower).CanLink()
                } -->
                    SympathyReady(SympathyPair(caster.preparation[?], .target[?])),
                _ --> SympathyStopped(CastOutcome.Failed)
        decision[aim]
    }
}
