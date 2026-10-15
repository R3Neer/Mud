# World entities, shape and own effect capabilities.

family Shape { Cube, Sphere }

family SympathyKind { Motion, SharedEffects }

alias EffectValue {
    let kind: Text
    let duration: Time in [0 s..*]
    let intensity: EffectIntensity
}

abstract thing Entity {
    ~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

    # Presence in this game world, independently of Mud declaration activity.
    mut present: Bool = true
    mut position: Point3 = Point3(r0 m, r0 m, r0 m)
    mut grabbed: Bool = false
    mut shape: Shape [?] = empty
    mut kinds: SympathyKind [* unique] = empty
    mut ownEffects: Text -> EffectValue [*] = empty
}

abstract thing Creature as Entity {
    ~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core
}
