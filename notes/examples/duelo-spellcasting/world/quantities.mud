# Shared quantities; one world-space unit is one metre.
magnitude Time: Num {
    root unit second { ~abbreviation = "s" }
}

# Linear spatial differences can be negative on any world axis.
magnitude Length: Rum {
    root unit meter { ~abbreviation = "m" }
}

magnitude WorldCoordinate point over Length

# A nominal effect parameter, without an invented physical unit or value range.
magnitude EffectIntensity: Num
