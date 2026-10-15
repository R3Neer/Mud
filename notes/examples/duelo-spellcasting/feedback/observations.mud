# Feedback delivery requests and current delivery batch query.

message FeedbackRequested on channel: FeedbackChannel {
    when channel.PlanSpellFeedback
    if channel.requests != empty
    let requests := channel.requests
}

look CurrentFeedback for channel: FeedbackChannel {
    let requests := channel.requests
}
