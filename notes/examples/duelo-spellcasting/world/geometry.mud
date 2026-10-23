# Points share one fixed world frame; displacements have no absolute origin.
alias Point3 {
    let x: WorldCoordinate
    let y: WorldCoordinate
    let z: WorldCoordinate

    -: (a: Point3) --> (b: Point3) --> Displacement3 =
        (a.x - b.x, a.y - b.y, a.z - b.z)
    +: (point: Point3) --> (delta: Displacement3) --> Point3 =
        (point.x + delta.x, point.y + delta.y, point.z + delta.z)
    +: (delta: Displacement3) --> (point: Point3) --> Point3 =
        (delta.x + point.x, delta.y + point.y, delta.z + point.z)
    -: (point: Point3) --> (delta: Displacement3) --> Point3 =
        (point.x - delta.x, point.y - delta.y, point.z - delta.z)
}

alias Displacement3 {
    let x: Length
    let y: Length
    let z: Length

    +: (a: Displacement3) --> (b: Displacement3) --> Displacement3 =
        (a.x + b.x, a.y + b.y, a.z + b.z)
    -: (a: Displacement3) --> (b: Displacement3) --> Displacement3 =
        (a.x - b.x, a.y - b.y, a.z - b.z)
}
