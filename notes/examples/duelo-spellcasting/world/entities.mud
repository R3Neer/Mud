# World entities, shape and own effect capabilities.

family Shape { Cube, Sphere }

family SympathyKind { Motion, SharedEffects }

alias Point3 {
    let x: Rum
    let y: Rum
    let z: Rum
}

alias EffectValue {
    let kind: Text
    let duration: Num in [0..*]
    let intensity: Num
}

abstract thing Entity {
    ~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

    # Presence in this game world, independently of Mud declaration activity.
    mut present: Bool = true
    mut position: Point3 = Point3(r0, r0, r0)
    mut grabbed: Bool = false
    mut shape: Shape [?] = empty
    mut kinds: SympathyKind [* unique] = empty
    mut ownEffects: Text -> EffectValue = empty
}

abstract thing Creature as Entity {
    ~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core
}
