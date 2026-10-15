using world
using spells

# Sympathy provider: preparation and atomic pair creation.

action Cast for magic: Magic [mut], caster: Spellcaster [mut] given aim: Aim {
    then {
        foreach spell in caster.selected[ordered]
            if spell == Spell.Sympathy and caster.CanAttempt(spell) : {
                let decision: Aim --> SympathyPlan [ordered] =
                    .target == empty --> SympathyPlan(outcome = CastOutcome.None),
                    not (exists target in .target : (magic, target).TargetUsable()) -->
                        SympathyPlan(outcome = CastOutcome.Failed),
                    caster.preparation == empty -->
                        SympathyPlan(outcome = CastOutcome.Partial, prepare = .target),
                    { exists leader in caster.preparation :
                        exists follower in .target : (magic, leader, follower).CanLink() } -->
                            SympathyPlan(outcome = CastOutcome.Success,
                                pair = [SympathyPair(caster.preparation[?], .target[?])]),
                    _ --> SympathyPlan(outcome = CastOutcome.Failed)
                let plan = decision[aim]
                foreach target in plan.prepare : caster.prepared = target
                foreach pair in plan.pair : {
                    let orientation: SympathyPair --> _ [ordered] =
                        .follower.grabbed and not .leader.grabbed --> SympathyPair(.follower, .leader),
                        _ --> value
                    let endpoints = orientation[pair]
                    let link = SympathyLink(magic.nextLink, caster, endpoints.leader,
                                            endpoints.follower, pair.leader.kinds & pair.follower.kinds)
                    magic.nextLink += 1
                    add link to magic.links
                    add SpellEvent(kind = SpellEventKind.Linked, caster = caster, spell = spell,
                        aim = aim, link = [LinkSnapshot(link.id, caster, link.leader, link.follower, link.kinds)])
                        to magic.pending
                }
                (magic, caster).ResolveAttempt(spell, plan.outcome, aim)
            }
    }
}
