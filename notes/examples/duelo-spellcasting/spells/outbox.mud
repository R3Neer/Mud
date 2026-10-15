part only

~activationFeature: configuration.ActivationFeature = configuration.ActivationFeature.Core

# Internal finite occurrence outbox; published is the latest batch, not history.

rule PublishSpellEvents on magic: Magic [mut] {
    when magic.pending changes
    if magic.pending != empty
    then {
        let events = magic.pending
        magic.pending = empty
        magic.published = events
    }
}
