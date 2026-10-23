using world
using spells

# Read-only relation projections, live contributions and engine requests.

alias BorrowedEffects {
    let link: LinkId
    let source: Entity
    let effects: String -> EffectValue [*]
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
        LinkSnapshot(
            link.id,
            link.owner,
            link.leader,
            link.follower,
            link.kinds
        )
    let following := foreach link in magic.links if link.follower == entity -->
        LinkSnapshot(
            link.id,
            link.owner,
            link.leader,
            link.follower,
            link.kinds
        )
    let invertible := foreach link in magic.links
        if entity.present and link.follower == entity --> link.id
}

message LinkEffectsRequested on magic: Magic {
    when magic.PrepareLinkEffects
    if magic.linkEffects != empty
    let events := magic.linkEffects
}
