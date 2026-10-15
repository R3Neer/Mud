part only

~checks: configuration.TestConcern [1..* unique] = [configuration.TestConcern.Quantities]

using configuration
using world
using spells
using fixtures

# Declarative affine/unit contracts; no Mud runtime executes this scenario yet.
test WorldCoordinatesAndEffectQuantities {
    start with {
        ActivationSelection().declarations,
        MagicWorld, Player, BoxA
    }
    then {
        let origin = Point3(r1 m, r2 m, r3 m)
        let target = Point3(r4 m, r6 m, r8 m)
        let delta = target - origin
        BoxA.position = origin + delta
        BoxA.ownEffects = "heat" -> EffectValue("heat", 10 s, -2)
    }
    after {
        BoxA.position == Point3(r4 m, r6 m, r8 m)
        BoxA.position - Point3(r1 m, r2 m, r3 m) == Displacement3(r3 m, r4 m, r5 m)
        BoxA.position - Displacement3(r3 m, r4 m, r5 m) == Point3(r1 m, r2 m, r3 m)
        Displacement3(r3 m, r4 m, r5 m) + Point3(r1 m, r2 m, r3 m) == BoxA.position
        Displacement3(r1 m, r1 m, r1 m) + Displacement3(r2 m, r3 m, r4 m)
            == Displacement3(r3 m, r4 m, r5 m)
        Displacement3(r3 m, r4 m, r5 m) - Displacement3(r2 m, r3 m, r4 m)
            == Displacement3(r1 m, r1 m, r1 m)
        BoxA.ownEffects == ("heat" -> EffectValue("heat", 10 s, -2))
    }
}
