---
title: World descriptor design boundaries
status: analysis
tags:
  - mud/analysis
  - mud/configuration
---

# World descriptor design boundaries

## Status

[[decisions/ADR-138-standard-library-scope-and-world-descriptor|D-138]] accepts TOML and `mud.world.toml` as the direction, not the schema below. [[questions/Q-071-world-descriptor-and-library-resolution|Q-071]] owns world/package resolution; [[questions/Q-069-foreign-adapter-contract-and-hosting|Q-069]] owns adapter declaration and native hosting.

## Preferred proposals, not current syntax

Keep identity, Mud requirements, packages and adapters in the descriptor. Keep exact resolutions/content identities in a lockfile and local installations/credentials in environment or host configuration. Existing `uses` authorises part access; `using` imports names. Installing a distribution must not itself grant operational access.

Do not require build/backend/output fields while Rust is the only planned initial backend. No manifest-format field is presently recommended; schema evolution and incompatible changes still need an explicit contract. These recommendations have not been selected as rules.

An author-selected `from` label could identify an adapter declaration, whose package selects the actual parser/language. The declaration could also configure its native environment. Every label being declared, optional minimal environment defaults, per-distribution alias scope and correction actions are proposals. Unknown aliases cannot be guessed from their spelling. A compiler would diagnose rather than silently edit the manifest; an editor could offer an explicit quick fix selecting a compatible stable adapter. No automatic latest-version policy is accepted.

Reference native manifests instead of copying their complete schemas: Cargo.toml, pyproject.toml or a .csproj need not share a format. An abbreviated environment and a delegated manifest need authority rules to avoid two conflicting dependency sources. Runtime compatibility requirements differ from a machine-specific executable path; embedded execution may have no launched executable.

## Illustrative descriptor

All keys, package names and versions below are hypothetical. This is neither a runnable project nor the accepted schema. Paths and URLs illustrate local, repository and registry sources, not actual distributions.

```toml
[world]
name = "Garden"
version = "0.1.0"
mud = "1.0"

[dependencies]
sqlite = { version = "1.2.0", registry = "official" }
plants = { path = "../Plants" }
weather = { git = "https://example.invalid/weather.git", revision = "v0.3.0" }

[registries]
official = "https://packages.example.invalid"

[adapters.Rust]
package = "mud-rust"
version = "0.1.0"
manifest = "foreign/rust/Cargo.toml"

[adapters.Python]
package = "mud-python"
version = "0.1.0"

[adapters.Calculations]
package = "mud-python"
version = "0.1.0"
manifest = "foreign/calculations/pyproject.toml"

[adapters.Csharp]
package = "mud-csharp"
version = "0.1.0"
project = "foreign/csharp/GardenBridge.csproj"

[adapters.Database]
package = "mud-postgresql"
version = "0.1.0"
connection-env = "GARDEN_DATABASE_URL"
```

A matching `from Calculations` resolving to Python is a proposed lookup contract, not a new production or a selected label. The SQL example declares a connection reference, not a credential or automatic permission to modify a database.

## Runtime and recording boundary

Do not close concrete tables yet. Resource safeguards interrupt execution technically rather than inventing Refusal. A global wave limit is especially unsuitable as an unexplained limit on a continuous causal tide; its invocation/reality scope needs definition. Host subscriptions may request provisional observations without changing validation barriers or confirmation semantics.

Separate confirmed-patch records (transition reconstruction), recorded execution inputs/environment (re-execution under admitted reproducibility contracts) and diagnostic traces (including discarded attempts). Recording a patch does not promise replay of external effects, deterministic native code or full programme re-execution. Fields, defaults, retention, access and output placement remain open.
