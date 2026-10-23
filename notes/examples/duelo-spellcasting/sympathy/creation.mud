part only

using spells

# Revalidate immediately before insertion; both roles keep the same relation id.
subaction EstablishSympathyLink
for magic: Magic [mut], caster: Spellcaster [mut]
given pair: SympathyPair, aim: Aim {
    if caster.CanAttempt(Spell.Sympathy)
        and (magic, pair.leader, pair.follower).CanLink()
    then {
        let orientation: SympathyPair -->[ordered] _ =
            .follower.grabbed and not .leader.grabbed -->
                SympathyPair(.follower, .leader),
            _ --> value
        let endpoints = orientation[pair]
        let link = SympathyLink(
            id = LinkId(magic.nextLink),
            owner = caster,
            leader = endpoints.leader,
            follower = endpoints.follower,
            kinds = pair.leader.kinds & pair.follower.kinds
        )

        magic.nextLink += 1
        add link to magic.links
        add SpellEvent(
            kind = SpellEventKind.Linked,
            caster = caster,
            spell = Spell.Sympathy,
            aim = aim,
            link = [LinkSnapshot(
                id = link.id,
                owner = caster,
                leader = link.leader,
                follower = link.follower,
                kinds = link.kinds
            )]
        ) to magic.pending
    }
}
