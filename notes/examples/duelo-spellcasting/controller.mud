# Domain model, not a reproduction of Unity callbacks. See README.md.

family Spell {
    slot: Nat
    needsConcentration: Bool
    Sympathy { slot = 1; needsConcentration = true },
    Fireball { slot = 2; needsConcentration = false }
}

family CastOutcome { None, Partial, Failed, Success }
family Shape { Cube, Sphere }
family SympathyKind { Motion, SharedEffects }
family SpellEventKind { Selected, SelectionRejected, Attempted, Cancelled, Linked, Inverted, Unlinked }

alias Point3 {
    let x: Rum
    let y: Rum
    let z: Rum
}

alias Aim {
    let point: Point3
    let target: Entity [?] = empty
}

alias EffectValue {
    let kind: Text
    let duration: Num in [0..*]
    let intensity: Num
}

abstract thing Entity {
    # Presence in this game world, independently of Mud declaration activity.
    mut present: Bool = true
    mut position: Point3 = Point3(r0, r0, r0)
    mut grabbed: Bool = false
    mut shape: Shape [?] = empty
    mut kinds: SympathyKind [* unique] = empty
    mut ownEffects: Text -> EffectValue = empty
}

abstract thing Creature as Entity

abstract thing Spellcaster as Entity {
    let configured: Spell [* unique] = [Spell.Sympathy]
    let maxConcentration: Nat = 2
    mut unlocked: Nat = 2
    mut selected: Spell [?] = empty
    mut activeSpells: Spell [* unique] = empty
    mut prepared: Entity [?] = empty

    let concentration := count spell in activeSpells : spell.needsConcentration
    let preparation := foreach entity in prepared if entity.present --> entity
}

alias LinkSnapshot {
    let id: Nat
    let owner: Spellcaster
    let leader: Entity
    let follower: Entity
    let kinds: SympathyKind [* unique]
}

alias SpellEvent {
    let kind: SpellEventKind
    let caster: Spellcaster
    let spell: Spell
    let outcome: CastOutcome = CastOutcome.None
    let aim: Aim
    let link: LinkSnapshot [?] = empty
}

abstract thing Magic {
    mut links: SympathyLink [* unique by id] = empty
    mut nextLink: Nat = 1
    mut pending: SpellEvent [* ordered] = empty
    mut published: SpellEvent [* ordered] = empty
    mut linkEffects: SpellEvent [* ordered] = empty
}

alias SelectionPlan {
    let activate: Spell [?] = empty
    let cancel: Spell [?] = empty
    let reject: Spell [?] = empty
}

rule CanSelect for caster: Spellcaster given spell: Spell {
    caster.present and caster.configured has spell and spell.slot <= caster.unlocked
        and (not spell.needsConcentration or caster.concentration < caster.maxConcentration)
}

rule CanAttempt for caster: Spellcaster given spell: Spell {
    caster.present and caster.selected has spell and caster.activeSpells has spell
        and caster.configured has spell and spell.slot <= caster.unlocked
}

always rule ConcentrationWithinLimit on caster: Spellcaster {
    caster.concentration <= caster.maxConcentration
}

action SelectSpell for magic: Magic [mut], caster: Spellcaster [mut] given requested: Spell {
    then {
        let selection: Spell --> SelectionPlan [ordered] =
            caster.activeSpells has value --> SelectionPlan(cancel = [value]),
            caster.CanSelect(value) --> SelectionPlan(activate = [value]),
            _ --> SelectionPlan(reject = [value])
        let plan = selection[requested]
        (magic, caster).EndSpell(plan.cancel[?])
        foreach spell in plan.activate : {
            add spell to caster.activeSpells
            caster.selected = spell
            caster.prepared = empty
            add SpellEvent(kind = SpellEventKind.Selected, caster = caster, spell = spell,
                           aim = Aim(caster.position, empty)) to magic.pending
        }
        add SpellEvent(kind = SpellEventKind.SelectionRejected, caster = caster,
                       spell = plan.reject[?], aim = Aim(caster.position, empty)) to magic.pending
    }
}

action CancelSpell for magic: Magic [mut], caster: Spellcaster [mut] given spell: Spell {
    then (magic, caster).EndSpell(spell)
}

# One atomic domain operation shared by cancellation and participant departure.
subaction EndSpell for magic: Magic [mut], caster: Spellcaster [mut] given spell: Spell {
    then {
        foreach link in magic.links[ordered] if link.owner == caster and spell == Spell.Sympathy : {
            remove link from magic.links
            add SpellEvent(kind = SpellEventKind.Unlinked, caster = caster, spell = spell,
                           aim = Aim(caster.position, empty),
                           link = [LinkSnapshot(link.id, caster, link.leader, link.follower, link.kinds)])
                to magic.pending
        }
        foreach active in caster.activeSpells[ordered] if active == spell : {
            remove active from caster.activeSpells
            add SpellEvent(kind = SpellEventKind.Cancelled, caster = caster, spell = spell,
                           aim = Aim(caster.position, empty)) to magic.pending
        }
        caster.selected = foreach selected in caster.selected if selected != spell --> selected
        caster.prepared = foreach entity in caster.prepared if spell != Spell.Sympathy --> entity
    }
    after caster.activeSpells has not spell
}

# Integration contract for spell bodies written in Mud, not a host-supplied result action.
subaction ResolveAttempt for magic: Magic [mut], caster: Spellcaster [mut] given
    spell: Spell, outcome: CastOutcome, aim: Aim {
    if caster.CanAttempt(spell)
    then {
        add SpellEvent(kind = SpellEventKind.Attempted, caster = caster, spell = spell,
                       outcome = outcome, aim = aim) to magic.pending
        caster.selected = foreach selected in caster.selected
            if selected != spell or outcome != CastOutcome.Success --> selected
        caster.prepared = foreach entity in caster.prepared
            if spell != Spell.Sympathy or outcome != CastOutcome.Success --> entity
        foreach active in caster.activeSpells[ordered]
            if active == spell and outcome == CastOutcome.Success and not spell.needsConcentration :
                remove active from caster.activeSpells
    }
}

action SetUnlocked for caster: Spellcaster [mut] given amount: Nat {
    then caster.unlocked = amount
    after caster.unlocked == amount
}

# One firing publishes one immutable ordered batch, including equal entries.
rule PublishSpellEvents on magic: Magic [mut] {
    when magic.pending changes
    if exists event in magic.pending : true
    then {
        let events = magic.pending
        magic.pending = empty
        magic.published = events
    }
}

message SpellEvents on magic: Magic {
    when magic.PublishSpellEvents
    let events := magic.published
}

look Spellcasting for caster: Spellcaster {
    let selected := caster.selected
    let active := caster.activeSpells
    let concentration := caster.concentration
    let prepared := caster.preparation
}

thing MagicWorld as Magic
thing Player as Creature, Spellcaster {
    shape = [Shape.Cube]
    kinds = [SympathyKind.Motion, SympathyKind.SharedEffects]
}
thing Turret as Entity, Spellcaster {
    shape = [Shape.Cube]
    kinds = [SympathyKind.Motion, SympathyKind.SharedEffects]
}
thing BoxA as Entity {
    shape = [Shape.Cube]
    kinds = [SympathyKind.Motion, SympathyKind.SharedEffects]
}
thing BoxB as Entity {
    shape = [Shape.Cube]
    kinds = [SympathyKind.Motion, SympathyKind.SharedEffects]
}
thing BoxC as Entity {
    shape = [Shape.Cube]
    kinds = [SympathyKind.Motion, SympathyKind.SharedEffects]
}
thing Unshaped as Entity

# Provider-independent completion fixture; no Fireball body is claimed.
thing InstantProtocolCaster as Creature, Spellcaster {
    configured = [Spell.Fireball]
}
thing NoFocus as Creature, Spellcaster {
    maxConcentration = 0
}
