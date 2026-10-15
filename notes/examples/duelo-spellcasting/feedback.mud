# Domain feedback requests. Rendering and asset execution belong to the adapter.

alias FeedbackAsset { let name: Text }
family FeedbackStage { Selected, Rejected, Partial, Failed, Success, Cancelled }

alias SpellFeedbackProfile {
    let byStage: FeedbackStage -> (FeedbackAsset [*]) = empty
    let excluded: FeedbackAsset [* unique] = empty
}

alias FeedbackGroup {
    let stage: FeedbackStage
    let effects: FeedbackAsset [* unique]
}

alias FeedbackRequest {
    let caster: Spellcaster
    let spell: Spell
    let aim: Aim
    let groups: FeedbackGroup [* ordered]
    # Rejected selections use this sequence directly, retaining repetitions.
    let rejected: FeedbackAsset [* ordered]
}

abstract thing FeedbackChannel {
    let magic: Magic
    let caster: Spellcaster
    let subscribed: Bool = true
    let profiles: Spell -> SpellFeedbackProfile = empty
    let global: FeedbackStage -> (FeedbackAsset [*]) = empty
    let selectionRejected: FeedbackAsset [* ordered] = empty
    # A replaceable delivery batch, not an execution history.
    mut requests: FeedbackRequest [* ordered] = empty

    let stages: SpellEvent --> FeedbackStage [* ordered] =
        .kind == SpellEventKind.Selected --> [FeedbackStage.Selected],
        .kind == SpellEventKind.Cancelled --> [FeedbackStage.Cancelled],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Success -->
            [FeedbackStage.Partial, FeedbackStage.Success],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Partial -->
            [FeedbackStage.Partial],
        .kind == SpellEventKind.Attempted and .outcome == CastOutcome.Failed -->
            [FeedbackStage.Failed]

    let groupsFor: SpellEvent --> FeedbackGroup [* ordered] :=
        _ --> {
            let event = value
            mut groups: FeedbackGroup [* ordered] = empty
            foreach profile in profiles[event.spell] : {
                foreach stage in stages[event] : {
                    let effects = (global[stage][unique] -- profile.excluded)
                        | profile.byStage[stage][unique]
                    add FeedbackGroup(stage, effects) to groups
                }
            }
            groups
        }

    let rejectedFor: SpellEvent --> FeedbackAsset [* ordered] :=
        .kind == SpellEventKind.SelectionRejected --> selectionRejected

    let requestFor: SpellEvent --> FeedbackRequest [? ordered] :=
        {
            let groups := groupsFor[value]
            let rejected := rejectedFor[value]
            (exists group in groups : exists _ in group.effects : true)
                or (exists _ in rejected : true)
        } --> FeedbackRequest(value.caster, value.spell, value.aim, groups, rejected)
}

# The matched message supplies frozen facts; actions are not trigger sources.
rule PlanSpellFeedback on channel: FeedbackChannel [mut] {
    let incoming := channel.magic.SpellEvents
    when incoming
    if channel.subscribed
    then {
        mut requests: FeedbackRequest [* ordered] = empty
        foreach event in incoming.events if event.caster == channel.caster :
            add channel.requestFor[event][?] to requests
        channel.requests = requests
    }
}

message FeedbackRequested on channel: FeedbackChannel {
    when channel.PlanSpellFeedback
    if exists _ in channel.requests : true
    let requests := channel.requests
}

look CurrentFeedback for channel: FeedbackChannel {
    let requests := channel.requests
}

thing PlayerFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    profiles = Spell.Fireball -> SpellFeedbackProfile(
        byStage = (
            FeedbackStage.Selected -> [FeedbackAsset("specific"), FeedbackAsset("shared")],
            FeedbackStage.Partial -> [FeedbackAsset("shared")],
            FeedbackStage.Failed -> [FeedbackAsset("failure")],
            FeedbackStage.Success -> [FeedbackAsset("shared"), FeedbackAsset("success")],
            FeedbackStage.Cancelled -> [FeedbackAsset("cancel")]
        ),
        excluded = [FeedbackAsset("shared"), FeedbackAsset("excluded")]
    ),
    Spell.Sympathy -> SpellFeedbackProfile(
        byStage = (
            FeedbackStage.Selected -> [FeedbackAsset("specific"), FeedbackAsset("shared")],
            FeedbackStage.Partial -> [FeedbackAsset("shared")],
            FeedbackStage.Failed -> [FeedbackAsset("failure")],
            FeedbackStage.Success -> [FeedbackAsset("shared"), FeedbackAsset("success")],
            FeedbackStage.Cancelled -> [FeedbackAsset("cancel")]
        ),
        excluded = [FeedbackAsset("shared"), FeedbackAsset("excluded")]
    )
    global =
        FeedbackStage.Selected -> [FeedbackAsset("global"), FeedbackAsset("shared"),
            FeedbackAsset("excluded"), FeedbackAsset("global")],
        FeedbackStage.Partial -> [FeedbackAsset("global")],
        FeedbackStage.Success -> [FeedbackAsset("global")]
    selectionRejected = [FeedbackAsset("rejected"), FeedbackAsset("rejected")]
}

thing MissingProfileFeedback as FeedbackChannel {
    magic = MagicWorld
    caster = Player
    global = FeedbackStage.Selected -> [FeedbackAsset("global")]
    selectionRejected = [FeedbackAsset("rejected"), FeedbackAsset("rejected")]
}
