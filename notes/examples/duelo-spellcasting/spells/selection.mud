# Player selection, cancellation and availability inputs.

action SelectSpell
for magic: Magic [mut], caster: Spellcaster [mut]
given requested: Spell {
    then {
        let selection: Spell -->[ordered]
            (CancelSelection | ActivateSelection | RejectSelection) =
                caster.activeSpells has value --> CancelSelection(value),
                caster.CanSelect(value) --> ActivateSelection(value),
                _ --> RejectSelection(value)
        let plan = selection[requested]

        let cancelled := foreach choice in plan
            if choice is CancelSelection --> choice.spell
        (magic, caster).EndSpell(cancelled[?])

        foreach choice in plan if choice is ActivateSelection : {
            let spell = choice.spell
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

        let rejected := foreach choice in plan
            if choice is RejectSelection --> choice.spell
        add SpellEvent(
            kind = SpellEventKind.SelectionRejected,
            caster = caster,
            spell = rejected[?],
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
