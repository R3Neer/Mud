# Player selection, cancellation and availability inputs.

action SelectSpell
for magic: Magic [mut], caster: Spellcaster [mut]
given requested: Spell {
    then {
        let selection: Spell -->[ordered] SelectionPlan =
            caster.activeSpells has value --> SelectionPlan(cancel = [value]),
            caster.CanSelect(value) --> SelectionPlan(activate = [value]),
            _ --> SelectionPlan(reject = [value])
        let plan = selection[requested]

        (magic, caster).EndSpell(plan.cancel[?])
        foreach spell in plan.activate : {
            add spell to caster.activeSpells
            caster.selected = spell
            caster.prepared = empty
            add SpellEvent(
                kind = SpellEventKind.Selected,
                caster = caster,
                spell = spell,
                aim = Aim(caster.position, empty)
            ) to magic.pending
        }

        add SpellEvent(
            kind = SpellEventKind.SelectionRejected,
            caster = caster,
            spell = plan.reject[?],
            aim = Aim(caster.position, empty)
        ) to magic.pending
    }
}

action CancelSpell
for magic: Magic [mut], caster: Spellcaster [mut]
given spell: Spell {
    then (magic, caster).EndSpell(spell)
}

action SetUnlocked for caster: Spellcaster [mut] given amount: Nat {
    then caster.unlocked = amount
    after caster.unlocked == amount
}
