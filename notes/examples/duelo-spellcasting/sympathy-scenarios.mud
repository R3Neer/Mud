# Declarative contracts, not executed tests. Every test has fresh registries.

test SympathyInvalidTargetPrecedesBusyLeader {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.objects["a"].role = SympathyRole.Leader
        SympathyFixture.CastSympathySample(empty)
    }
    after {
        SympathyFixture.lastResult == CastResult.None
        SympathyFixture.leader == ["a"]
        SympathyFixture.trace == empty
    }
}

test SympathyFirstTargetReservesNoSession {
    start with { SympathyWorld, SympathyFixture }
    then SympathyFixture.CastSympathySample(["a"])
    after {
        SympathyFixture.lastResult == CastResult.Partial
        SympathyFixture.leader == ["a"]
        SympathyFixture.follower == empty
        SympathyFixture.sessions == empty
        SympathyFixture.preview
    }
}

test SympathyMissingIdentityStillReturnsPartial {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["a"].identity = empty
        SympathyFixture.CastSympathySample(["a"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Partial
        SympathyFixture.leader == empty
        SympathyFixture.identity == empty
        SympathyFixture.preview
    }
}

test SympathyMissingIdentityClearsOldCachedIdentity {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.objects["a"].alive = false
        SympathyFixture.objects["b"].identity = empty
        SympathyFixture.CastSympathySample(["b"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Partial
        SympathyFixture.leader == ["a"]
        SympathyFixture.identity == empty
    }
}

test SympathyBusyFirstTargetIsRemembered {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["a"].role = SympathyRole.Follower
        SympathyFixture.CastSympathySample(["a"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Partial
        SympathyFixture.leader == ["a"]
    }
}

test SympathyBusyRememberedLeaderRejectsNextTarget {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.objects["a"].role = SympathyRole.Leader
        SympathyFixture.CastSympathySample(["b"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Failed
        SympathyFixture.sessions == empty
        SympathyFixture.trace == empty
    }
}

test SympathySameObjectIsRejected {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["a"])
    }
    after SympathyFixture.lastResult == CastResult.Failed and SympathyFixture.sessions == empty
}

test SympathyDifferentShapeIsRejected {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["b"].identity = SympathyIdentity(["sphere"])
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
    }
    after SympathyFixture.lastResult == CastResult.Failed and SympathyFixture.sessions == empty
}

test SympathyEmptyMeshMatchesAnotherEmptyMesh {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["a"].identity = SympathyIdentity(empty)
        SympathyFixture.objects["b"].identity = SympathyIdentity(empty)
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
    }
    after SympathyFixture.lastResult == CastResult.Success
}

test SympathyNeedsAnEffectBeforeAddingVisuals {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["b"].supports = empty
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Failed
        SympathyFixture.combined == empty
        SympathyFixture.sessions == empty
    }
}

test SympathyStartsBeforePublishingSessionReferences {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Success
        SympathyFixture.leader == ["a"]
        SympathyFixture.follower == ["b"]
        (count session in SympathyFixture.sessions : true) == 1
        forall state in SympathyFixture.objects["a"] : state.role == SympathyRole.Leader and state.session == [1]
        forall state in SympathyFixture.objects["b"] : state.role == SympathyRole.Follower and state.session == [1]
        (foreach command in SympathyFixture.trace --> command.kind) == [
            SympathyCommandKind.ExecuteEffect, SympathyCommandKind.ExecuteEffect,
            SympathyCommandKind.StartSync, SympathyCommandKind.RoleChanged, SympathyCommandKind.RoleChanged
        ]
        forall command in SympathyFixture.trace :
            forall state in command.objects["a"] : state.session == empty
    }
}

test SympathyGrabbedFollowerBecomesLeader {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.objects["b"].grabbed = true
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
    }
    after {
        SympathyFixture.lastResult == CastResult.Success
        SympathyFixture.leader == ["b"]
        SympathyFixture.follower == ["a"]
        not SympathyFixture.preview
        (foreach command in SympathyFixture.trace --> command.kind) == [
            SympathyCommandKind.PreviewOff, SympathyCommandKind.PreviewCancel, SympathyCommandKind.PreviewDispose,
            SympathyCommandKind.ExecuteEffect, SympathyCommandKind.ExecuteEffect,
            SympathyCommandKind.StartSync, SympathyCommandKind.RoleChanged, SympathyCommandKind.RoleChanged
        ]
    }
}

test SympathyOldSessionCanClearNewFollowerReference {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.sessions[0] = SympathySessionState(
            "c", "b", [SympathyEffectKind.Physics, SympathyEffectKind.Visuals], true
        )
        SympathyFixture.objects["c"].role = SympathyRole.Leader
        SympathyFixture.objects["c"].session = 0
        SympathyFixture.objects["b"].role = SympathyRole.Follower
        SympathyFixture.objects["b"].session = 0
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
        SympathyFixture.StopSympathySession(0)
    }
    after {
        SympathyFixture.lastResult == CastResult.Success
        forall state in SympathyFixture.objects["a"] : state.session == [1]
        forall state in SympathyFixture.objects["b"] : state.role == SympathyRole.Free and state.session == empty
        (count session in SympathyFixture.sessions : true) == 2
    }
}

test SympathyInversionDoesNotSwapProviderReferences {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
        SympathyFixture.InvertSympathySession(1)
    }
    after {
        SympathyFixture.leader == ["a"]
        SympathyFixture.follower == ["b"]
        forall state in SympathyFixture.sessions[1] : state.leader == "b" and state.follower == "a"
        (foreach command in SympathyFixture.trace --> command.kind) == [
            SympathyCommandKind.InvertEffect, SympathyCommandKind.InvertEffect,
            SympathyCommandKind.InvertSync, SympathyCommandKind.RoleChanged, SympathyCommandKind.RoleChanged
        ]
    }
}

test SympathyRepeatedStopStillCancelsAndNotifies {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
        SympathyFixture.StopSympathySession(1)
        SympathyFixture.StopSympathySession(1)
    }
    after {
        (foreach command in SympathyFixture.trace --> command.kind) == [
            SympathyCommandKind.CancelEffect, SympathyCommandKind.CancelEffect,
            SympathyCommandKind.StopSync, SympathyCommandKind.SessionStopped
        ]
        forall state in SympathyFixture.objects["a"] : state.role == SympathyRole.Free and state.session == empty
        forall state in SympathyFixture.objects["b"] : state.role == SympathyRole.Free and state.session == empty
        (count session in SympathyFixture.sessions : true) == 1
    }
}

test SympathyPreviewCancellationKeepsCachedIdentity {
    start with { SympathyWorld, SympathyFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CancelSympathy()
    }
    after {
        SympathyFixture.leader == empty and SympathyFixture.follower == empty
        SympathyFixture.identity == [SympathyIdentity(["cube"])]
        not SympathyFixture.preview
        (foreach command in SympathyFixture.trace --> command.kind) == [
            SympathyCommandKind.PreviewOff, SympathyCommandKind.PreviewCancel, SympathyCommandKind.PreviewDispose
        ]
    }
}

test SympathyCachedInteractorDoesNotRecheckFollower {
    start with { SympathyWorld, SympathyFixture, SympathyInteractor, SympathyInteractorFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
        (SympathyInteractorFixture, SympathyFixture).CheckSympathyInteraction("b")
        SympathyFixture.InvertSympathySession(1)
        (SympathyInteractorFixture, SympathyFixture).InteractWithSympathy()
    }
    after {
        forall state in SympathyFixture.sessions[1] : state.leader == "a" and state.follower == "b"
        SympathyInteractorFixture.keepsCurrent
        not SympathyInteractorFixture.allowsAction
        SympathyInteractorFixture.ghost
    }
}

test SympathyCachedInteractorWithoutSessionKeepsInteraction {
    start with { SympathyWorld, SympathyFixture, SympathyInteractor, SympathyInteractorFixture }
    then {
        SympathyFixture.CastSympathySample(["a"])
        SympathyFixture.CastSympathySample(["b"])
        (SympathyInteractorFixture, SympathyFixture).CheckSympathyInteraction("b")
        SympathyFixture.StopSympathySession(1)
        (SympathyInteractorFixture, SympathyFixture).InteractWithSympathy()
    }
    after SympathyFixture.trace == empty and SympathyInteractorFixture.keepsCurrent
}
