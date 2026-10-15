part only

using spells

# Internal reactive planning from the matched frozen spell event payload.

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
