part only

using world
using spells
using sympathy
using feedback

# Closed registration; metadata is available before world materialisation.
alias ActivationSelection {
    let features: ActivationFeature [* unique] = empty
    let declarations := foreach declaration in [
        Entity, Creature, Spellcaster, Magic,
        CanSelect, CanAttempt, ConcentrationWithinLimit,
        TargetUsable, CanLink, ExclusiveSympathy, PublishSpellEvents,
        FeedbackChannel, PlanSpellFeedback, PrepareLinkEffects
    ] if (features | [ActivationFeature.Core]) has declaration~activationFeature -->
        declaration
}
