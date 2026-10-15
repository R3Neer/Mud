part only

~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

using world
using spells

# Endpoint admission, pair revalidation and global exclusivity.

rule TargetUsable for magic: Magic, entity: Entity {
    entity.present and entity.shape != empty
        and entity.kinds != empty
        and not (exists link in magic.links : link.leader == entity or link.follower == entity)
}

rule CanLink for magic: Magic, leader: Entity, follower: Entity {
    leader != follower and (magic, leader).TargetUsable() and (magic, follower).TargetUsable()
        and leader.shape == follower.shape
        and (leader.kinds & follower.kinds) != empty
}

always rule ExclusiveSympathy on magic: Magic {
    forall first in magic.links :
        forall second in magic.links :
            first.id == second.id
                or (first.leader != second.leader and first.leader != second.follower
                    and first.follower != second.leader and first.follower != second.follower)
}
