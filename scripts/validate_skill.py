#!/usr/bin/env python3
"""Validate the Cisco Network Operations skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "cisco-network-ops"
SKILL_MD = SKILL_DIR / "SKILL.md"
REQUIRED_REFS = {
    "quick-reference.md",
    "change-safety.md",
    "platform-matrix.md",
    "routing-troubleshooting.md",
    "switching-troubleshooting.md",
    "security-policy.md",
    "automation-and-apis.md",
    "telemetry-observability.md",
    "testing-and-validation.md",
}
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


def check_exists() -> None:
    required = [
        SKILL_MD,
        SKILL_DIR / "agents" / "openai.yaml",
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".gitignore",
        ROOT / "tests" / "baseline-scenarios.md",
        ROOT / "tests" / "smoke-test-prompts.md",
    ]
    for path in required:
        if not path.exists():
            fail(f"Missing required file: {path.relative_to(ROOT)}")

    refs_dir = SKILL_DIR / "references"
    missing_refs = sorted(REQUIRED_REFS - {p.name for p in refs_dir.glob("*.md")})
    if missing_refs:
        fail(f"Missing references: {', '.join(missing_refs)}")


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_simple_yaml_mapping(content: str, source: str) -> dict[str, Any]:
    """Parse the small YAML mapping subset used by this package."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            fail(f"{source}:{line_number} contains a tab; use spaces for YAML")

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2 != 0:
            fail(f"{source}:{line_number} uses odd indentation")

        line = raw_line.strip()
        if ":" not in line or line.startswith("- "):
            fail(f"{source}:{line_number} must be a key/value mapping")

        key, value = line.split(":", 1)
        key = key.strip()
        if not key:
            fail(f"{source}:{line_number} has an empty YAML key")

        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if not value.strip():
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = parse_scalar(value)

    return root


def parse_frontmatter(content: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        fail("SKILL.md missing YAML frontmatter")
    return parse_simple_yaml_mapping(match.group(1), "SKILL.md frontmatter")


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be a YAML/JSON object")
    return value


def require_path(data: dict[str, Any], keys: tuple[str, ...], label: str) -> str:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            fail(f"{label} missing {'.'.join(keys)}")
        value = value[key]
    if not isinstance(value, str) or not value:
        fail(f"{label} field {'.'.join(keys)} must be a non-empty string")
    return value


def check_skill_md() -> dict[str, Any]:
    content = SKILL_MD.read_text()
    lines = content.splitlines()
    if len(lines) > 300:
        fail(f"SKILL.md has {len(lines)} lines; target is <= 300")

    frontmatter = parse_frontmatter(content)
    if frontmatter.get("name") != "cisco-network-ops":
        fail("SKILL.md frontmatter name must be cisco-network-ops")
    if not frontmatter.get("description", "").startswith("Use when"):
        fail("SKILL.md description must start with 'Use when'")
    if frontmatter.get("license") != "Apache-2.0":
        fail("SKILL.md license must be Apache-2.0")
    if "Response Contract" not in content:
        fail("SKILL.md missing Response Contract")
    if "direct access" not in content and "live device access" not in content:
        fail("SKILL.md must state no assumed direct device access")
    return frontmatter


def check_links() -> None:
    files = sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)
    for path in files:
        content = path.read_text()
        for match in MARKDOWN_LINK_PATTERN.finditer(content):
            raw_target = match.group(1).strip()
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1]
            if raw_target.startswith("#"):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_target):
                continue
            if raw_target.startswith("//"):
                continue

            target_name = raw_target.split("#", 1)[0].split("?", 1)[0]
            if not target_name.lower().endswith(".md"):
                continue

            target = (path.parent / target_name).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                fail(
                    f"Markdown link in {path.relative_to(ROOT)} points outside repo: "
                    f"{raw_target}"
                )
            if not target.exists():
                fail(
                    f"Broken Markdown link in {path.relative_to(ROOT)}: {raw_target}"
                )


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {rel}: {exc}")
    if not isinstance(data, dict):
        fail(f"{rel} must contain a JSON object")
    return data


def check_json() -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    for rel in [
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".claude-plugin/marketplace.json",
    ]:
        data = load_json(rel)
        manifests[rel] = data
        if rel == ".claude-plugin/marketplace.json" and "version" in data:
            fail("Claude marketplace manifest must not use top-level version")
    return manifests


def check_versions(frontmatter: dict[str, Any], manifests: dict[str, dict[str, Any]]) -> None:
    marketplace = manifests[".claude-plugin/marketplace.json"]
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins or not isinstance(plugins[0], dict):
        fail(".claude-plugin/marketplace.json must contain plugins[0]")

    versions = {
        "SKILL.md metadata.version": require_path(frontmatter, ("metadata", "version"), "SKILL.md"),
        ".codex-plugin/plugin.json version": require_path(
            manifests[".codex-plugin/plugin.json"], ("version",), ".codex-plugin/plugin.json"
        ),
        ".claude-plugin/plugin.json version": require_path(
            manifests[".claude-plugin/plugin.json"], ("version",), ".claude-plugin/plugin.json"
        ),
        ".claude-plugin/marketplace.json metadata.version": require_path(
            marketplace, ("metadata", "version"), ".claude-plugin/marketplace.json"
        ),
        ".claude-plugin/marketplace.json plugins[0].version": require_path(
            plugins[0], ("version",), ".claude-plugin/marketplace.json plugins[0]"
        ),
    }

    if len(set(versions.values())) != 1:
        details = ", ".join(f"{name}={version}" for name, version in versions.items())
        fail(f"Version mismatch: {details}")


def check_openai_yaml() -> None:
    rel = "skills/cisco-network-ops/agents/openai.yaml"
    data = parse_simple_yaml_mapping((ROOT / rel).read_text(), rel)
    interface = require_mapping(data.get("interface"), f"{rel} interface")
    if interface.get("display_name") != "Cisco Network Operations":
        fail("agents/openai.yaml interface.display_name must be Cisco Network Operations")
    for key in ("short_description", "default_prompt"):
        if not isinstance(interface.get(key), str) or not interface[key]:
            fail(f"agents/openai.yaml interface.{key} must be a non-empty string")


def check_gitignore() -> None:
    forbidden_patterns = {
        "*.json",
        "*.md",
        "*.yaml",
        "*.yml",
        ".claude-plugin/",
        ".codex-plugin/",
        ".github/",
        "scripts/",
        "skills/",
        "tests/",
    }
    patterns = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    blocked = sorted(forbidden_patterns & patterns)
    if blocked:
        fail(f".gitignore excludes package source files: {', '.join(blocked)}")


def main() -> int:
    check_exists()
    frontmatter = check_skill_md()
    check_links()
    manifests = check_json()
    check_versions(frontmatter, manifests)
    check_openai_yaml()
    check_gitignore()
    print("[OK] Cisco Network Operations skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
