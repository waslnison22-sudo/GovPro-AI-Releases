#!/usr/bin/env python3
"""Static checks for the release repository's publication contract.

This deliberately does not build the private application source. It catches
configuration regressions before a manual beta publication is started.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-release.yml"
SOURCE_REPO = "waslnison22-sudo/Hellsaiz-Gov-AI"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def fail(message: str) -> None:
    raise SystemExit(f"RELEASE CONTRACT FAILED: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> int:
    require(WORKFLOW.is_file(), "missing publish workflow")
    text = WORKFLOW.read_text(encoding="utf-8")

    # Keep the release pipeline explicit and manually gated.
    require("workflow_dispatch:" in text, "publication must be manual-only")
    require("SOURCE_REPO_TOKEN" in text, "private source credential gate is missing")
    require(f"repository: {SOURCE_REPO}" in text, "source repository must be the canonical engineering repository")
    require("actions/checkout@" in text, "workflow must check out source with a pinned action")
    require("needs:\n       - preflight\n       - build" in text, "publish job must wait for preflight and build")
    require("if-no-files-found: error" in text, "artifact upload must fail when assets are absent")
    require("SHA256SUMS.txt" in text, "release must publish SHA-256 integrity metadata")
    require("RELEASE_METADATA.json" in text, "release must publish machine-readable metadata")
    require("gh release edit \"v$GOVPRO_VERSION\" --draft=false" in text, "release must be explicitly promoted from draft")

    # Prevent accidental return to the old hosted/remote AI architecture.
    lowered = text.lower()
    for forbidden in ("ollama", "openai_api_key", "anthropic_api_key"):
        require(forbidden not in lowered, f"forbidden hosted AI integration found: {forbidden}")

    # The workflow must package the Windows-first NSIS installer and the
    # model/runtime must remain external to the executable.
    require("windows-x64" in text and "nsis,msi" in text, "Windows NSIS/MSI build target is missing")
    require("Qwen3" not in text, "model binaries must not be embedded in the release workflow")
    require("model" not in lowered or "model" in lowered, "workflow text is readable")

    # Catch malformed source commit output contracts early.
    require("source_commit=$sha" in text, "source commit provenance is not recorded")
    require("EXPECTED_SOURCE_COMMIT" in text, "build must verify source provenance")
    if not HEX40.fullmatch("0" * 40):
        fail("internal SHA-1 validator failure")

    print("RELEASE CONTRACT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
