part only

using world
using spells

# Endpoint admission, pair revalidation and global exclusivity.

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
