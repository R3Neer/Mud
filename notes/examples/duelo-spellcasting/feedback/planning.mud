part only

~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Feedback

using spells

# Internal reactive planning from the matched frozen spell event payload.

rule PlanSpellFeedback on channel: FeedbackChannel [mut] {
    let incoming := channel.magic.SpellEvents
    when incoming
    if channel.subscribed
    then channel.requests =
        foreach event in incoming.events
            if event.caster == channel.caster -->
                channel.requestFor[event][?]
}
