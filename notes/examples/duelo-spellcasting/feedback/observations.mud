# Feedback delivery requests and current delivery batch query.

message FeedbackRequested on channel: FeedbackChannel {
    when channel.PlanSpellFeedback
    if exists _ in channel.requests : true
    let requests := channel.requests
}

look CurrentFeedback for channel: FeedbackChannel {
    let requests := channel.requests
}
