# Sympathy is a relation of domain entities, not a copy of host object state.

alias SympathyLink {
    let id: Nat
    # Explicit immediate authority, supplied by the spellcaster's for role.
    # Public facts/looks project LinkSnapshot instead of exposing this component.
    let owner: Spellcaster [mut]
    let leader: Entity
    let follower: Entity
    let kinds: SympathyKind [* unique]
}

alias SympathyPair {
    let leader: Entity
    let follower: Entity
}

alias SympathyPlan {
    let outcome: CastOutcome
    let prepare: Entity [?] = empty
    let pair: SympathyPair [?] = empty
}

rule TargetUsable for magic: Magic, entity: Entity {
    entity.present and (exists shape in entity.shape : true)
        and (exists kind in entity.kinds : true)
        and not (exists link in magic.links : link.leader == entity or link.follower == entity)
}

rule CanLink for magic: Magic, leader: Entity, follower: Entity {
    leader != follower and (magic, leader).TargetUsable() and (magic, follower).TargetUsable()
        and leader.shape == follower.shape
        and (exists kind in leader.kinds & follower.kinds : true)
}

always rule ExclusiveSympathy on magic: Magic {
    forall first in magic.links : forall second in magic.links :
        first.id == second.id or
            (first.leader != second.leader and first.leader != second.follower
                and first.follower != second.leader and first.follower != second.follower)
}

# This provider implements Sympathy. Other catalog entries need their own Mud body.
# No public operation accepts an arbitrary outcome from C#.
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

action Invert for magic: Magic [mut], follower: Entity given id: Nat {
    if follower.present and (exists link in magic.links : link.id == id and link.follower == follower)
    then {
        foreach before in magic.links[ordered] if before.id == id : {
            remove before from magic.links
            add SympathyLink(before.id, before.owner, before.follower, before.leader, before.kinds)
                to magic.links
            add SpellEvent(kind = SpellEventKind.Inverted, caster = before.owner, spell = Spell.Sympathy,
                aim = Aim(follower.position, empty),
                link = [LinkSnapshot(before.id, before.owner, before.follower, before.leader, before.kinds)])
                to magic.pending
        }
    }
}

# Domain departure: close affected links before marking the participant absent.
# This is not destroy Entity, and does not allocate/recreate Mud identities.
action LeaveWorld for magic: Magic [mut], entity: Entity [mut] {
    then {
        foreach link in magic.links[ordered]
            if link.leader == entity or link.follower == entity or link.owner == entity :
                (magic, link.owner).EndSpell(Spell.Sympathy)
        foreach caster in entity if caster is Spellcaster : {
            foreach spell in caster.activeSpells[ordered] : (magic, caster).EndSpell(spell)
        }
        entity.present = false
    }
    after not entity.present
}

alias BorrowedEffects {
    let link: Nat
    let source: Entity
    let effects: Text -> EffectValue
}

look EffectiveEffects for magic: Magic, entity: Entity {
    let own := entity.ownEffects
    # Recomputed from leader OWN effects; never copy borrowed effects onward.
    let borrowed := foreach link in magic.links
        if link.follower == entity and link.kinds has SympathyKind.SharedEffects -->
            BorrowedEffects(link.id, link.leader, link.leader.ownEffects)
}

look Sympathy for magic: Magic, entity: Entity {
    let leading := foreach link in magic.links if link.leader == entity -->
        LinkSnapshot(link.id, link.owner, link.leader, link.follower, link.kinds)
    let following := foreach link in magic.links if link.follower == entity -->
        LinkSnapshot(link.id, link.owner, link.leader, link.follower, link.kinds)
    let invertible := foreach link in magic.links
        if entity.present and link.follower == entity --> link.id
}

# Effects on the engine are requests describing complete relations, not copies
# of Rigidbody/tag/CTS state. The adapter must honor publication and rollback.
rule PrepareLinkEffects on magic: Magic [mut] {
    let incoming := magic.SpellEvents
    when incoming
    then {
        magic.linkEffects = foreach event in incoming.events
            if event.kind == SpellEventKind.Linked or event.kind == SpellEventKind.Inverted
                or event.kind == SpellEventKind.Unlinked --> event
    }
}

message LinkEffectsRequested on magic: Magic {
    when magic.PrepareLinkEffects
    if exists event in magic.linkEffects : true
    let events := magic.linkEffects
}
