# VPD OpenAI GitHub Actions WIF Setup — 2026-08-19

Status: `PREFERRED_AUTH_ROUTE / ONE_TIME_PLATFORM_CONFIGURATION_REQUIRED`

Purpose: authenticate the formal VPD Distillation-Only Runtime Test V1 GitHub Actions runner to the OpenAI API without storing a long-lived `OPENAI_API_KEY` in GitHub Secrets.

This is an authentication-only adaptation. It does not modify VPD aesthetics, the frozen T1/T2/T3 payloads, reference policy, output budget, Commercial Quality, Golden, or Scale gates.

## OpenAI platform configuration

Create one Workload Identity Provider for GitHub Actions.

- Issuer: `https://token.actions.githubusercontent.com`
- Audience: `https://api.openai.com/v1`
- GitHub OIDC discovery/JWKS: enabled; do not upload custom JWKS.

Create a dedicated OpenAI service account for this VPD runtime, then create a service-account mapping under the WIF provider.

The mapping should be narrow. Trust only this repository and this VPD branch/workflow. Recommended exact-claim constraints:

- `repository == "vubaoha034-hash/shenmei"`
- `ref == "refs/heads/visual-program-distillation-v2-photography-design-20260814"`
- additionally constrain `workflow_ref` / `workflow` to the VPD live-render workflow once that workflow is promoted.

Do not use an owner-wide mapping such as trusting every repository under `vubaoha034-hash`.

Grant only the API permission needed for model requests. Do not grant organization-admin permissions.

## GitHub Actions variables

After the OpenAI WIF provider and service-account mapping exist, set these repository Actions **variables** (not secrets):

- `OPENAI_WIF_AUDIENCE=https://api.openai.com/v1`
- `OPENAI_IDENTITY_PROVIDER_ID=<OpenAI WIF provider ID>`
- `OPENAI_SERVICE_ACCOUNT_ID=<dedicated OpenAI service account ID>`

These values identify the mapping but are not bearer credentials.

Do not store GitHub OIDC JWTs, exchanged OpenAI access tokens, or Authorization headers in repository files or workflow artifacts.

## Probe

The repository contains:

- `scripts/probe_vpd_openai_wif.py`
- `.github/workflows/vpd-openai-wif-probe.yml`

The workflow requests `id-token: write`, performs no image generation, and writes a redacted machine-readable result to:

`continuity/vpd/OPENAI_AUTH_PROBE.json`

Expected successful status:

`WIF_AUTH_AND_PINNED_MODEL_METADATA_PASS`

Until that status exists, formal T1/T2/T3 live rendering remains blocked.

## Formal-output privacy

Repository visibility is `public`. Formal V1 PNGs must not be committed to this repository. Do not upload unencrypted formal PNGs as public-repository artifacts merely to move the test forward.

A separate protected output transport must be selected before the three formal live images are generated.
