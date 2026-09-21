#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CHANNELS = ROOT / "channels"

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def fail(message: str) -> None:
    raise SystemExit(f"CHANNEL VALIDATION FAILED: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def valid_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_channel(path: Path, expected_channel: str) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"{path.name}: invalid JSON: {exc}")

    require(data.get("product") == "GovPro AI", f"{path.name}: product must be 'GovPro AI'")
    require(data.get("channel") == expected_channel, f"{path.name}: channel mismatch")

    status = data.get("status")
    require(status in {"locked", "not_published", "published"}, f"{path.name}: invalid status")

    latest = data.get("latest")

    if latest is None:
        require(status in {"locked", "not_published"}, f"{path.name}: latest=null is only valid for locked/not_published")
        return

    require(isinstance(latest, dict), f"{path.name}: latest must be an object")
    version = latest.get("version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) is not None, f"{path.name}: latest.version must be SemVer")

    source_ref = latest.get("source_ref")
    require(isinstance(source_ref, str) and bool(source_ref.strip()), f"{path.name}: latest.source_ref is required")
    require(valid_https_url(latest.get("release_url")), f"{path.name}: latest.release_url must be https")
    require(isinstance(latest.get("published_at"), str) and "T" in latest["published_at"], f"{path.name}: latest.published_at is required")

    signature_status = latest.get("signature_status")
    require(signature_status in {"not_configured", "unsigned", "verified", "failed"}, f"{path.name}: invalid signature_status")

    artifacts = latest.get("artifacts")
    require(isinstance(artifacts, list) and artifacts, f"{path.name}: published latest must contain artifacts")

    for index, artifact in enumerate(artifacts):
        prefix = f"{path.name}: latest.artifacts[{index}]"
        require(isinstance(artifact, dict), f"{prefix} must be an object")
        name = artifact.get("file")
        require(isinstance(name, str) and name.strip(), f"{prefix}.file is required")
        require(isinstance(artifact.get("bytes"), int) and artifact["bytes"] > 0, f"{prefix}.bytes must be a positive integer")
        digest = artifact.get("sha256")
        require(isinstance(digest, str) and re.fullmatch(r"[0-9a-fA-F]{64}", digest) is not None, f"{prefix}.sha256 must be 64 hex chars")
        require(valid_https_url(artifact.get("download_url")), f"{prefix}.download_url must be https")

    require(status == "published", f"{path.name}: latest object requires status=published")


def main() -> int:
    validate_channel(CHANNELS / "stable.json", "stable")
    validate_channel(CHANNELS / "beta.json", "beta")
    print("CHANNEL VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
