# Contrato OIDC entre GitHub Actions y el Worker

Audiencia:

```text
mud-repo-patcher-worker
```

El Worker verifica la firma con el JWKS publicado por GitHub y exige:

```text
iss == https://token.actions.githubusercontent.com
aud contiene mud-repo-patcher-worker
exp, nbf e iat válidos con tolerancia acotada
repository == R3Neer/Mud
repository_id == configuración inmutable del Worker
event_name == workflow_dispatch
runner_environment == github-hosted
run_id == D1.github_run_id
run_attempt == D1.github_run_attempt
workflow_ref == R3Neer/Mud/.github/workflows/validate-repo-patcher-remote.yml@refs/heads/main
workflow_sha == D1.control_sha
ref == refs/heads/main
actor == actor permitido por configuración
```

Un token correcto solo autoriza el objeto asociado al `request_id` y al run
que presenta el token. No concede listado del bucket ni acceso a otra
candidata.

Después de descargar y verificar el ZIP, el workflow elimina del entorno
`ACTIONS_ID_TOKEN_REQUEST_URL`, `ACTIONS_ID_TOKEN_REQUEST_TOKEN`,
`GITHUB_TOKEN`, `GH_TOKEN` y cualquier variable reconocida como credencial
antes de ejecutar el paquete.

