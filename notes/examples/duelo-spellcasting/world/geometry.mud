# Points share one fixed world frame; displacements have no absolute origin.
alias Point3 {
    let x: WorldCoordinate
    let y: WorldCoordinate
    let z: WorldCoordinate

    a - b: Displacement3 := (a.x - b.x, a.y - b.y, a.z - b.z)
    p + (delta: Displacement3): Point3 :=
        (p.x + delta.x, p.y + delta.y, p.z + delta.z)
    (delta: Displacement3) + p: Point3 :=
        (delta.x + p.x, delta.y + p.y, delta.z + p.z)
    p - (delta: Displacement3): Point3 :=
        (p.x - delta.x, p.y - delta.y, p.z - delta.z)
}

alias Displacement3 {
    let x: Length
    let y: Length
    let z: Length

    a + b: Displacement3 := (a.x + b.x, a.y + b.y, a.z + b.z)
    a - b: Displacement3 := (a.x - b.x, a.y - b.y, a.z - b.z)
}
