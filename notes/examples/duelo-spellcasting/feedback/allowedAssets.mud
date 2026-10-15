part only

# Resource admission is pure configuration, not an activatable Boolean rule.
sublook AllowedFeedbackAssets given modalities: FeedbackModality [* unique] {
    let assets := foreach asset in all FeedbackAsset
        if forall modality in asset~modalities : modalities has modality --> asset
}
