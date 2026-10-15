# Informative discrete provider/session model. Native commands are trace data.
# Registry keys model identity; they do not allocate Unity objects or Mud things.

family SympathyRole { Free, Leader, Follower }
family SympathyEffectKind { Physics, NativeExtension, Visuals }
family SympathyStep { InvalidTarget, BusyLeader, FirstTarget, Incompatible, Link }
family SympathyCommandKind {
    PreviewPrimary, PreviewOff, PreviewCancel, PreviewDispose,
    ExecuteEffect, InvertEffect, CancelEffect,
    StartSync, InvertSync, StopSync, RoleChanged, SessionStopped
}

alias SympathyIdentity {
    # Empty Mesh is distinct from an absent IdentityTag.
    let shape: Text [?] = empty
}

alias SympathyObjectState {
    let token: Text
    let alive: Bool = true
    let tagsManager: Bool = true
    let identity: SympathyIdentity [?] = empty
    # Any non-Free Grabbable state, including Pushed, counts here.
    let grabbed: Bool = false
    let supports: SympathyEffectKind [* unique] = empty
    let role: SympathyRole = SympathyRole.Free
    let session: Nat [?] = empty
}

alias SympathySessionState {
    let leader: Text
    let follower: Text
    let effects: SympathyEffectKind [* ordered]
    let subscribed: Bool = false
}

alias SympathyAdmission {
    let targetValid: Bool
    let leaderBusy: Bool
    let leaderPresent: Bool
    let sameObject: Bool
    let compatible: Bool
}

alias SympathyEndpoints {
    let leader: SympathyObjectState
    let follower: SympathyObjectState
}

alias SympathyCommand {
    let kind: SympathyCommandKind
    let session: Nat [?] = empty
    let effect: SympathyEffectKind [?] = empty
    let leader: Text [?] = empty
    let follower: Text [?] = empty
    # Frozen tag views expose role-before-session-assignment ordering.
    let objects: Text -> SympathyObjectState
}

abstract thing SympathyWorld {
    mut objects: Text -> SympathyObjectState
    mut sessions: Nat -> SympathySessionState = empty
    mut nextSession: Nat = 1
    mut leader: Text [?] = empty
    mut follower: Text [?] = empty
    mut identity: SympathyIdentity [?] = empty
    mut combined: SympathyEffectKind [* ordered] = empty
    mut preview: Bool = false
    mut lastResult: CastResult = CastResult.None
    mut trace: SympathyCommand [* ordered] = empty
    let visualsConfigured: Bool = true

    let admission: SympathyAdmission --> SympathyStep [ordered] :=
        not .targetValid --> SympathyStep.InvalidTarget,
        .leaderBusy --> SympathyStep.BusyLeader,
        not .leaderPresent --> SympathyStep.FirstTarget,
        .sameObject or not .compatible --> SympathyStep.Incompatible,
        _ --> SympathyStep.Link

    # NativeExtension is a sampled opaque factory capability. Electricity is
    # excluded; its implementation is not reconstructed from this checkout.
    let effectsFor: (leader: SympathyObjectState, follower: SympathyObjectState)
        --> SympathyEffectKind [* ordered] :=
        _ --> foreach effect in [SympathyEffectKind.Physics, SympathyEffectKind.NativeExtension][ordered]
            if .leader.supports has effect and .follower.supports has effect --> effect

    let readyLink: (target: SympathyObjectState, effects: SympathyEffectKind [* ordered])
        --> SympathyObjectState [? ordered] :=
        { exists effect in .effects : true } --> .target

    let orientation: SympathyEndpoints --> SympathyEndpoints [ordered] :=
        .follower.grabbed and not .leader.grabbed --> SympathyEndpoints(.follower, .leader),
        _ --> value

    let swapPreviewCommands: Bool --> SympathyCommandKind [* ordered] :=
        == true --> [SympathyCommandKind.PreviewOff,
                    SympathyCommandKind.PreviewCancel, SympathyCommandKind.PreviewDispose]

    let cancelPreviewCommands: Bool --> SympathyCommandKind [* ordered] :=
        == true --> [SympathyCommandKind.PreviewOff, SympathyCommandKind.PreviewCancel]

    let clearedPreview: Bool --> Bool [? ordered] := == true --> false
}

subaction RecordSympathy for world: SympathyWorld [mut] given
    kind: SympathyCommandKind, session: Nat [?] = empty,
    effect: SympathyEffectKind [?] = empty,
    leader: Text [?] = empty, follower: Text [?] = empty {
    then add SympathyCommand(kind, session, effect, leader, follower, world.objects)
        to world.trace
}

action CastSympathySample for world: SympathyWorld [mut] given target: Text [?] {
    then {
        let targets: SympathyObjectState [? ordered] = [world.objects[target[?]][?]]
        let leaders: SympathyObjectState [? ordered] = [world.objects[world.leader[?]][?]]
        let targetValid = exists object in targets : object.alive and object.tagsManager
        let leaderBusy = exists object in leaders : object.alive and object.role != SympathyRole.Free
        let leaderPresent = exists object in leaders : object.alive
        let compatible = exists object in targets :
            exists fresh in object.identity :
                exists previous in world.identity : previous.shape == fresh.shape
        let step = world.admission[SympathyAdmission(
            targetValid, leaderBusy, leaderPresent, world.leader == target, compatible
        )]
        let handling: SympathyStep --> _ [ordered] =
            SympathyStep.InvalidTarget --> IgnoreSympathyTarget,
            SympathyStep.BusyLeader or SympathyStep.Incompatible --> RejectSympathyTarget,
            SympathyStep.FirstTarget --> SelectSympathyLeader,
            SympathyStep.Link --> TrySympathyLink
        let next = handling[step]
        world.trace = empty
        world.next(targets)
    }
}

subaction IgnoreSympathyTarget for world: SympathyWorld [mut] given
    targets: SympathyObjectState [? ordered] {
    then world.lastResult = CastResult.None
}

subaction RejectSympathyTarget for world: SympathyWorld [mut] given
    targets: SympathyObjectState [? ordered] {
    then world.lastResult = CastResult.Failed
}

subaction SelectSympathyLeader for world: SympathyWorld [mut] given
    targets: SympathyObjectState [? ordered] {
    then {
        foreach target in targets : {
            world.identity = target.identity
            foreach identity in target.identity : {
                world.leader = target.token
            }
        }
        # A valid target without IdentityTag still returns Partial. Preview
        # receives the provider's current optional leader, including empty.
        let preview: Bool --> SympathyCommandKind [? ordered] =
            == true --> SympathyCommandKind.PreviewPrimary
        world.StartSympathyPreview(preview[world.visualsConfigured][?])
        world.lastResult = CastResult.Partial
    }
}

subaction StartSympathyPreview for world: SympathyWorld [mut] given
    kind: SympathyCommandKind {
    then {
        world.preview = true
        world.RecordSympathy(kind, leader = world.leader)
    }
}

subaction TrySympathyLink for world: SympathyWorld [mut] given
    targets: SympathyObjectState [? ordered] {
    then {
        let leaders: SympathyObjectState [? ordered] = [world.objects[world.leader[?]][?]]
        world.lastResult = CastResult.Failed
        foreach leader in leaders : {
            foreach target in targets : {
                # This selection occurs before any held-object swap.
                let effects = world.effectsFor[leader, target]
                world.combined = effects
                world.EstablishSympathyLink(leader, world.readyLink[target, effects][?], effects)
            }
        }
    }
}

subaction EstablishSympathyLink for world: SympathyWorld [mut] given
    leader: SympathyObjectState, follower: SympathyObjectState,
    effects: SympathyEffectKind [* ordered] {
    if exists effect in effects : true
    then {
        world.follower = follower.token
        let swapped = follower.grabbed and not leader.grabbed
        foreach command in world.swapPreviewCommands[swapped and world.visualsConfigured] :
            world.RecordSympathy(command, leader = world.leader)
        world.preview = world.clearedPreview[swapped and world.visualsConfigured][?]
        let oriented = world.orientation[leader, follower]
        world.leader = oriented.leader.token
        world.follower = oriented.follower.token
        world.identity = oriented.leader.identity
        add SympathyEffectKind.Visuals to world.combined
        let session = world.nextSession
        world.nextSession += 1
        world.sessions[session] = SympathySessionState(
            oriented.leader.token, oriented.follower.token, world.combined, false
        )
        world.StartSympathySession(session)
        world.sessions[session].subscribed = true
        world.objects[oriented.leader.token].session = session
        world.objects[oriented.follower.token].session = session
        world.lastResult = CastResult.Success
    }
}

subaction SetSympathyRole for world: SympathyWorld [mut] given
    token: Text, role: SympathyRole {
    then {
        let previous: SympathyObjectState [? ordered] = [world.objects[token][?]]
        foreach object in previous if object.alive and object.role != role : {
            world.objects[token].role = role
            world.RecordSympathy(SympathyCommandKind.RoleChanged, leader = token)
        }
    }
}

subaction StartSympathySession for world: SympathyWorld [mut] given session: Nat {
    if exists key in world.sessions : key == session
    then {
        foreach state in world.sessions[session] : {
            foreach effect in state.effects : world.RecordSympathy(
                SympathyCommandKind.ExecuteEffect, session, effect, state.leader, state.follower
            )
            world.RecordSympathy(SympathyCommandKind.StartSync, session, leader = state.leader,
                                 follower = state.follower)
            world.SetSympathyRole(state.leader, SympathyRole.Leader)
            world.SetSympathyRole(state.follower, SympathyRole.Follower)
        }
    }
}

action InvertSympathySession for world: SympathyWorld [mut] given session: Nat {
    if exists key in world.sessions : key == session
    then {
        world.trace = empty
        world.InvertSympathySessionBody(session)
    }
}

subaction InvertSympathySessionBody for world: SympathyWorld [mut] given session: Nat {
    if exists key in world.sessions : key == session
    then {
        foreach before in world.sessions[session] : {
            foreach effect in before.effects :
                world.RecordSympathy(SympathyCommandKind.InvertEffect, session, effect)
            world.RecordSympathy(SympathyCommandKind.InvertSync, session)
            world.sessions[session].leader = before.follower
            world.sessions[session].follower = before.leader
            world.SetSympathyRole(before.follower, SympathyRole.Leader)
            world.SetSympathyRole(before.leader, SympathyRole.Follower)
        }
    }
}

action StopSympathySession for world: SympathyWorld [mut] given session: Nat {
    if exists key in world.sessions : key == session
    then {
        world.trace = empty
        world.StopSympathySessionBody(session)
    }
}

subaction StopSympathySessionBody for world: SympathyWorld [mut] given session: Nat {
    if exists key in world.sessions : key == session
    then {
        foreach state in world.sessions[session] : {
            foreach effect in state.effects :
                world.RecordSympathy(SympathyCommandKind.CancelEffect, session, effect)
            world.RecordSympathy(SympathyCommandKind.StopSync, session)
            world.ClearSympathyTag(state.leader)
            world.ClearSympathyTag(state.follower)
            let notice: Bool --> SympathyCommandKind [? ordered] =
                == true --> SympathyCommandKind.SessionStopped
            world.RecordSympathy(notice[state.subscribed][?], session)
        }
    }
}

subaction ClearSympathyTag for world: SympathyWorld [mut] given token: Text {
    then {
        let previous: SympathyObjectState [? ordered] = [world.objects[token][?]]
        foreach object in previous if object.alive : {
            world.SetSympathyRole(token, SympathyRole.Free)
            world.objects[token].session = empty
        }
    }
}

action CancelSympathy for world: SympathyWorld [mut] {
    then {
        world.trace = empty
        let leaders: SympathyObjectState [? ordered] = [world.objects[world.leader[?]][?]]
        let followers: SympathyObjectState [? ordered] = [world.objects[world.follower[?]][?]]
        foreach leader in leaders if leader.alive : {
            let noFollower = not exists follower in followers : follower.alive
            foreach command in world.cancelPreviewCommands[noFollower and world.visualsConfigured] :
                world.RecordSympathy(command, leader = world.leader)
            foreach follower in followers if follower.alive :
                world.StopSympathySessionBody(leader.session[?])
        }
        world.leader = empty
        world.follower = empty
        let dispose: Bool --> SympathyCommandKind [? ordered] =
            == true --> SympathyCommandKind.PreviewDispose
        world.RecordSympathy(dispose[world.preview][?])
        world.preview = false
    }
    after world.leader == empty and world.follower == empty and not world.preview
}

abstract thing SympathyInteractor {
    mut target: Text [?] = empty
    mut canInteract: Bool = false
    let allowsAction: Bool = false
    let ghost: Bool = true
    let keepsCurrent: Bool = true
}

action CheckSympathyInteraction for interactor: SympathyInteractor [mut], world: SympathyWorld
    given target: Text {
    then {
        let targets: SympathyObjectState [? ordered] = [world.objects[target][?]]
        interactor.target = empty
        foreach object in targets if object.alive and object.tagsManager : interactor.target = target
        interactor.canInteract = exists object in targets :
            object.alive and object.tagsManager and object.role == SympathyRole.Follower
    }
}

action InteractWithSympathy for interactor: SympathyInteractor, world: SympathyWorld [mut] {
    if exists token in interactor.target : true
    then {
        world.trace = empty
        foreach target in world.objects[interactor.target[?]] :
            world.InvertSympathySessionBody(target.session[?])
    }
}

look SympathyStatus for world: SympathyWorld {
    let result := world.lastResult
    let leader := world.leader
    let follower := world.follower
    let objects := world.objects
    let sessions := world.sessions
    let trace := world.trace
}

thing SympathyFixture as SympathyWorld {
    objects =
        "a" -> SympathyObjectState(token = "a", identity = [SympathyIdentity(["cube"])],
            supports = [SympathyEffectKind.Physics]),
        "b" -> SympathyObjectState(token = "b", identity = [SympathyIdentity(["cube"])],
            supports = [SympathyEffectKind.Physics]),
        "c" -> SympathyObjectState(token = "c", identity = [SympathyIdentity(["cube"])],
            supports = [SympathyEffectKind.Physics])
}

thing SympathyInteractorFixture as SympathyInteractor
