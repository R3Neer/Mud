using world
using spells

# Relation inversion and participant departure inputs.

action Invert
for magic: Magic [mut], follower: Entity
given id: LinkId {
    if follower.present
        and (exists link in magic.links : link.id == id and link.follower == follower)
    then {
        foreach before in magic.links[ordered] if before.id == id : {
            remove before from magic.links
            add SympathyLink(
                before.id,
                before.owner,
                before.follower,
                before.leader,
                before.kinds
            ) to magic.links
            add SpellEvent(
                kind = SpellEventKind.Inverted,
                caster = before.owner,
                spell = Spell.Sympathy,
                aim = Aim(follower.position, empty),
                link = [LinkSnapshot(
                    before.id,
                    before.owner,
                    before.follower,
                    before.leader,
                    before.kinds
                )]
            ) to magic.pending
        }
    }
}

action LeaveWorld for magic: Magic [mut], entity: Entity [mut] {
    then {
        foreach link in magic.links[ordered]
            if link.leader == entity or link.follower == entity or link.owner == entity :
                (magic, link.owner).EndSpell(Spell.Sympathy)

        foreach caster in entity if caster is Spellcaster : {
            foreach spell in caster.activeSpells[ordered] :
                (magic, caster).EndSpell(spell)
        }

        entity.present = false
    }
    after not entity.present
}
