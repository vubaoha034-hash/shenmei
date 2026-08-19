# VPD OpenAI WIF Auth Probe Result — 2026-08-19

Status: `WIF_CONFIG_MISSING / NO_OPENAI_REQUEST_SENT / ZERO_IMAGE_GENERATION`

Repository: `vubaoha034-hash/shenmei`
Branch: `visual-program-distillation-v2-photography-design-20260814`

## Verified facts

The repository is public.

The non-generative GitHub Actions WIF probe executed and persisted:

`continuity/vpd/OPENAI_AUTH_PROBE.json`

Observed status:

`WIF_CONFIG_MISSING`

Missing GitHub Actions repository variables:

- `OPENAI_WIF_AUDIENCE`
- `OPENAI_IDENTITY_PROVIDER_ID`
- `OPENAI_SERVICE_ACCOUNT_ID`

The probe did not send a network request to OpenAI because configuration was incomplete.

The probe did not invoke image generation.

Formal V1 outputs created by the probe: `0`.

Reference images attached: `0`.

Credential values persisted: `false`.

## Authentication route correction

The prior checkpoint described live execution as blocked by a missing `OPENAI_API_KEY`. That was too narrow.

OpenAI officially supports GitHub Actions Workload Identity Federation using GitHub-issued OIDC tokens exchanged for short-lived OpenAI access tokens. This route avoids a long-lived OpenAI API key in GitHub Secrets and is now the preferred VPD GitHub Actions authentication route.

A long-lived `OPENAI_API_KEY` remains only a fallback option and is not required if WIF is configured.

## One-time external configuration still required

An OpenAI organization/project administrator must create:

1. an OpenAI Workload Identity Provider for GitHub Actions;
2. a dedicated OpenAI service account for the VPD runtime;
3. a narrow service-account mapping restricted to this repository and VPD branch/workflow;
4. the three non-secret GitHub Actions variables listed above.

Exact setup guidance is frozen in:

`VPD_OPENAI_WIF_SETUP_20260819.md`

## Formal-output privacy gate

Because the repository is public, unencrypted formal T1/T2/T3 PNGs must not be committed to the repository or exposed through an unprotected public output path.

Before live formal generation, a protected output transport must be selected.

## Current decision

- VPD distillation: preserved; do not redo.
- Frozen T1/T2/T3 payloads: preserved; do not rewrite.
- Strict renderer binding adapter: implemented.
- Native ChatGPT `image_gen` for formal V1: prohibited.
- Preferred authentication: GitHub Actions WIF.
- WIF configuration: missing.
- OpenAI request sent by probe: no.
- Image generation invoked by probe: no.
- Formal V1 images: 0.
- Next gate: configure OpenAI WIF + GitHub Actions variables, rerun non-generative auth probe, then choose protected output transport before T1/T2/T3 live generation.
