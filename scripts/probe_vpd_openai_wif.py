#!/usr/bin/env python3
"""Non-generative OpenAI WIF probe for the VPD V1 renderer route.

This script does not generate images and therefore does not consume the formal
T1/T2/T3 output budget. It checks whether GitHub Actions Workload Identity
Federation is configured, then authenticates with the official OpenAI Python
SDK and retrieves the pinned GPT Image model metadata.

No OIDC token, OpenAI access token, identity-provider ID, service-account ID,
or Authorization header is written to the probe receipt.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PINNED_IMAGE_MODEL = "gpt-image-2-2026-04-21"
REQUIRED_ENV = (
    "OPENAI_WIF_AUDIENCE",
    "OPENAI_IDENTITY_PROVIDER_ID",
    "OPENAI_SERVICE_ACCOUNT_ID",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def base_receipt() -> dict:
    return {
        "schema_version": "vpd-openai-wif-probe/v1",
        "recorded_at": utc_now(),
        "project_id": "visual-aesthetic-vpd",
        "repository": os.environ.get("GITHUB_REPOSITORY", "UNKNOWN"),
        "ref": os.environ.get("GITHUB_REF", "UNKNOWN"),
        "workflow": os.environ.get("GITHUB_WORKFLOW", "UNKNOWN"),
        "provider": "OpenAI API",
        "auth_mode": "GITHUB_ACTIONS_WORKLOAD_IDENTITY_FEDERATION",
        "pinned_image_model": PINNED_IMAGE_MODEL,
        "probe_type": "AUTHENTICATION_AND_MODEL_METADATA_ONLY",
        "image_generation_invoked": False,
        "formal_v1_outputs_created": 0,
        "reference_images_attached": 0,
        "credential_values_persisted": False,
        "required_configuration_presence": {
            name: bool(os.environ.get(name, "").strip()) for name in REQUIRED_ENV
        },
    }


def github_actions_oidc_token_provider(audience: str):
    import urllib.parse
    import urllib.request

    request_url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL", "")
    request_token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN", "")
    if not request_url or not request_token:
        raise RuntimeError("GitHub Actions OIDC environment is unavailable")

    def get_token() -> str:
        parsed_url = urllib.parse.urlparse(request_url)
        query = dict(urllib.parse.parse_qsl(parsed_url.query, keep_blank_values=True))
        query["audience"] = audience
        url = urllib.parse.urlunparse(parsed_url._replace(query=urllib.parse.urlencode(query)))
        request = urllib.request.Request(
            url,
            headers={"Authorization": f"bearer {request_token}"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        token = payload.get("value")
        if not token:
            raise RuntimeError("GitHub OIDC token response did not include a value")
        return token

    return {"token_type": "jwt", "get_token": get_token}


def run(output: Path) -> int:
    receipt = base_receipt()
    missing = [name for name in REQUIRED_ENV if not os.environ.get(name, "").strip()]
    if missing:
        receipt.update(
            {
                "status": "WIF_CONFIG_MISSING",
                "missing_configuration_names": missing,
                "network_request_sent_to_openai": False,
            }
        )
        write_json(output, receipt)
        return 2

    try:
        from importlib.metadata import version
        from openai import OpenAI

        receipt["openai_python_version"] = version("openai")
        client = OpenAI(
            workload_identity={
                "identity_provider_id": os.environ["OPENAI_IDENTITY_PROVIDER_ID"],
                "service_account_id": os.environ["OPENAI_SERVICE_ACCOUNT_ID"],
                "provider": github_actions_oidc_token_provider(os.environ["OPENAI_WIF_AUDIENCE"]),
            },
        )
        model = client.models.retrieve(PINNED_IMAGE_MODEL)
        observed_model = getattr(model, "id", None)
        if observed_model != PINNED_IMAGE_MODEL:
            raise RuntimeError("OpenAI returned unexpected model metadata identity")
        receipt.update(
            {
                "status": "WIF_AUTH_AND_PINNED_MODEL_METADATA_PASS",
                "network_request_sent_to_openai": True,
                "observed_model_id": observed_model,
            }
        )
        write_json(output, receipt)
        return 0
    except Exception as exc:  # receipt intentionally redacts exception message
        receipt.update(
            {
                "status": "WIF_AUTH_OR_PERMISSION_FAIL",
                "network_request_sent_to_openai": True,
                "error_type": type(exc).__name__,
                "http_status": getattr(exc, "status_code", None),
                "request_id_present": bool(getattr(exc, "request_id", None)),
                "error_message_persisted": False,
            }
        )
        write_json(output, receipt)
        return 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    return run(Path(args.output))


if __name__ == "__main__":
    raise SystemExit(main())
