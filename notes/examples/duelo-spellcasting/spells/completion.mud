part only

# Internal atomic spell completion and cancellation protocol.

alias ActivateSelection { let spell: Spell }
alias CancelSelection { let spell: Spell }
alias RejectSelection { let spell: Spell }

subaction EndSpell
for magic: Magic [mut], caster: Spellcaster [mut]
given spell: Spell {
    then {
        foreach link in magic.links[ordered] if link.owner == caster and spell == Spell.Sympathy : {
            remove link from magic.links
            add SpellEvent(
                kind = SpellEventKind.Unlinked,
                caster = caster,
                spell = spell,
                aim = Aim(caster.position, empty),
                link = [LinkSnapshot(
                    link.id,
                    caster,
                    link.leader,
                    link.follower,
                    link.kinds
                )]
            ) to magic.pending
        }

        foreach active in caster.activeSpells[ordered] if active == spell : {
            remove active from caster.activeSpells
            add SpellEvent(
                kind = SpellEventKind.Cancelled,
                caster = caster,
                spell = spell,
                aim = Aim(caster.position, empty)
            ) to magic.pending
        }

        caster.selected = foreach selected in caster.selected if selected != spell --> selected
        caster.prepared = foreach entity in caster.prepared if spell != Spell.Sympathy --> entity
    }
    after caster.activeSpells has not spell
}

subaction ResolveAttempt
for magic: Magic [mut], caster: Spellcaster [mut]
given spell: Spell, outcome: CastOutcome, aim: Aim {
    if caster.CanAttempt(spell)
    then {
        add SpellEvent(
            kind = SpellEventKind.Attempted,
            caster = caster,
            spell = spell,
            outcome = outcome,
            aim = aim
        ) to magic.pending

        caster.selected = foreach selected in caster.selected
            if selected != spell or outcome != CastOutcome.Success --> selected
        caster.prepared = foreach entity in caster.prepared
            if spell != Spell.Sympathy or outcome != CastOutcome.Success --> entity
        foreach active in caster.activeSpells[ordered]
            if active == spell and outcome == CastOutcome.Success and not spell.needsConcentration :
                remove active from caster.activeSpells
    }
}
