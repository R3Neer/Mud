CREATE TABLE validation_requests (
    request_id TEXT PRIMARY KEY,
    schema_version INTEGER NOT NULL CHECK (schema_version = 1),
    transport_kind TEXT NOT NULL CHECK (transport_kind IN ('zip_base64', 'logical_files')),
    target_sha TEXT NOT NULL,
    package_sha256 TEXT NOT NULL,
    package_size INTEGER NOT NULL,
    trust_plugin INTEGER NOT NULL CHECK (trust_plugin IN (0, 1)),
    state TEXT NOT NULL CHECK (state IN (
        'accepted', 'dispatching', 'queued', 'running',
        'succeeded', 'failed', 'infrastructure_error', 'expired'
    )),
    github_run_id INTEGER,
    github_run_url TEXT,
    github_run_attempt INTEGER NOT NULL DEFAULT 1,
    control_sha TEXT,
    conclusion TEXT,
    runtime_version TEXT,
    result_object_key TEXT,
    evidence_object_key TEXT,
    created_at TEXT NOT NULL,
    dispatched_at TEXT,
    started_at TEXT,
    completed_at TEXT,
    expires_at TEXT NOT NULL,
    CHECK (length(target_sha) = 40),
    CHECK (length(package_sha256) = 64),
    CHECK (package_size > 0)
);

CREATE UNIQUE INDEX validation_requests_github_run_id
    ON validation_requests(github_run_id)
    WHERE github_run_id IS NOT NULL;
CREATE INDEX validation_requests_state_expires
    ON validation_requests(state, expires_at);

CREATE TABLE validation_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL REFERENCES validation_requests(request_id),
    event TEXT NOT NULL,
    detail_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX validation_events_request_id
    ON validation_events(request_id, id);
