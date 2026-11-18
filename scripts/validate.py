#!/usr/bin/env python3
"""Validate the portable and vendor-specific Monologue plugin surfaces."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.0"
NAME = "monologue"
MCP_URL = "https://api.monologue.to/mcp"
REPOSITORY = "https://github.com/MonologueInc/monologue-plugin"
AGENT_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
CLAUDE_SOURCE = "./claude"
CLAUDE_ALLOWED_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}

REQUIRED_FILES = [
    "plugin.json",
    "mcp.json",
    ".codex-plugin/plugin.json",
    ".mcp.json",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    ".grok-plugin/plugin.json",
    "claude/.claude-plugin/plugin.json",
    "claude/.mcp.json",
    "claude/README.md",
    "claude/LICENSE.txt",
    "claude/assets/logo.png",
    "gemini-extension.json",
    "GEMINI.md",
    "assets/logo.png",
    "README.md",
    "LICENSE",
    "SECURITY.md",
]


class ValidationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_json(path: str) -> dict[str, Any]:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(lines and lines[0] == "---", f"{path}: missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: unterminated YAML frontmatter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validate_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    require(not missing, f"missing required files: {', '.join(missing)}")
    require((ROOT / "assets/logo.png").stat().st_size > 1_000, "logo is unexpectedly small")


def validate_manifests() -> None:
    portable = load_json("plugin.json")
    require(portable.get("$schema") == AGENT_SCHEMA, "portable plugin schema is incorrect")
    require(portable.get("name") == NAME, "portable plugin name is incorrect")
    require(portable.get("version") == VERSION, "portable plugin version is incorrect")
    unsupported = {"skills", "commands", "mcpServers"} & portable.keys()
    require(not unsupported, f"portable plugin.json must not declare {sorted(unsupported)}; skills/ and mcp.json are discovered")
    require(portable.get("repository") == REPOSITORY, "portable repository URL is incorrect")

    portable_mcp = load_json("mcp.json")
    require(portable_mcp.get("$schema") == MCP_SCHEMA, "portable MCP schema is incorrect")
    server = portable_mcp.get("mcpServers", {}).get(NAME, {})
    require(server.get("type") == "streamable-http", "portable MCP type is incorrect")
    require(server.get("url") == MCP_URL, "portable MCP URL is incorrect")

    codex = load_json(".codex-plugin/plugin.json")
    require(codex.get("name") == NAME and codex.get("version") == VERSION, "Codex identity is inconsistent")
    require(codex.get("skills") == "./skills/", "Codex skills path is incorrect")
    require(codex.get("mcpServers") == "./.mcp.json", "Codex MCP path is incorrect")
    interface = codex.get("interface", {})
    require(0 < len(interface.get("shortDescription", "")) <= 30, "Codex shortDescription must be 1-30 characters")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(interface.get(field, "").startswith("https://"), f"Codex {field} is missing")
    require(interface.get("logo") and interface.get("composerIcon"), "Codex logo and composerIcon are required")
    test_cases = codex.get("extensions", {}).get("com.openai", {}).get("review", {}).get("test_cases", {})
    require(len(test_cases.get("positive", [])) == 5, "OpenAI review needs exactly five positive test cases")
    require(len(test_cases.get("negative", [])) == 3, "OpenAI review needs exactly three negative test cases")

    native_mcp = load_json(".mcp.json").get("mcpServers", {}).get(NAME, {})
    require(native_mcp.get("type") == "http", "native MCP type is incorrect")
    require(native_mcp.get("url") == MCP_URL, "native MCP URL is incorrect")
    require(native_mcp.get("oauth_resource") == MCP_URL, "native OAuth resource is incorrect")

    claude = load_json(".claude-plugin/plugin.json")
    require(claude.get("name") == NAME and claude.get("version") == VERSION, "Claude identity is inconsistent")
    claude_market = load_json(".claude-plugin/marketplace.json").get("plugins", [{}])[0]
    require(claude_market.get("name") == NAME, "Claude marketplace entry is missing")
    require(claude_market.get("source") == CLAUDE_SOURCE, "Claude marketplace must point at the claude/ bundle")
    bundle = load_json("claude/.claude-plugin/plugin.json")
    require(bundle.get("name") == NAME and bundle.get("version") == VERSION, "Claude bundle identity is inconsistent")
    require(bundle.get("repository") == REPOSITORY, "Claude bundle repository URL is incorrect")
    require(bundle.get("icon") == "./assets/logo.png", "Claude bundle icon is incorrect")
    require(bundle.get("privacyPolicyUrl", "").startswith("https://"), "Claude bundle privacyPolicyUrl is missing")
    bundle_mcp = load_json("claude/.mcp.json").get("mcpServers", {})
    require(bundle_mcp == {NAME: {"type": "http", "url": MCP_URL}}, "Claude bundle MCP server must be only type and url")

    grok = load_json(".grok-plugin/plugin.json")
    require(grok.get("name") == NAME and grok.get("version") == VERSION, "Grok identity is inconsistent")
    require(grok.get("repository") == REPOSITORY, "Grok repository URL is incorrect")

    for path in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        require(load_json(path).get("repository") == REPOSITORY, f"{path}: repository URL is incorrect")

    cursor = load_json(".cursor-plugin/plugin.json")
    require(cursor.get("name") == NAME and cursor.get("version") == VERSION, "Cursor identity is inconsistent")
    require(cursor.get("mcpServers", {}).get(NAME, {}).get("url") == MCP_URL, "Cursor MCP URL is incorrect")

    gemini = load_json("gemini-extension.json")
    require(gemini.get("name") == NAME and gemini.get("version") == VERSION, "Gemini identity is inconsistent")
    command = gemini.get("mcpServers", {}).get(NAME, {})
    require(command.get("command") == "npx", "Gemini OAuth bridge command is incorrect")
    require("mcp-remote@0.1.43" in command.get("args", []), "Gemini OAuth bridge must use the reviewed version")
    require(MCP_URL in command.get("args", []), "Gemini MCP URL is missing")
    require(gemini.get("contextFileName") == "GEMINI.md", "Gemini context file is incorrect")

    codex_market = load_json(".agents/plugins/marketplace.json").get("plugins", [{}])[0]
    require(codex_market.get("name") == NAME, "Codex marketplace entry is missing")
    require(codex_market.get("installation") == "AVAILABLE", "Codex installation policy is incorrect")
    require(codex_market.get("authentication") == "ON_INSTALL", "Codex auth policy is incorrect")
    require(codex_market.get("source") == f"{REPOSITORY}.git", "Codex source is incorrect")


def validate_skills_and_commands() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    require(len(skill_files) == 4, "expected exactly four skills")
    for skill in skill_files:
        metadata = parse_frontmatter(skill)
        require(metadata.get("name") == skill.parent.name, f"{skill}: skill name must match its directory")
        require(bool(metadata.get("description")), f"{skill}: description is missing")

    markdown_commands = {path.stem for path in (ROOT / "commands").glob("*.md")}
    toml_commands = {path.stem for path in (ROOT / "commands").glob("*.toml")}
    require(markdown_commands == toml_commands, "Markdown and TOML command sets differ")
    require(markdown_commands == {"meeting-prep", "meeting-follow-up", "weekly-review"}, "command set is incorrect")
    for path in (ROOT / "commands").glob("*.toml"):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        require(bool(data.get("description")) and bool(data.get("prompt")), f"{path}: invalid TOML command")


def validate_claude_bundle() -> None:
    bundle = ROOT / CLAUDE_SOURCE
    for path in sorted(item for item in bundle.rglob("*") if item.is_file()):
        relative = path.relative_to(bundle)
        require(path.suffix.lower() in CLAUDE_ALLOWED_SUFFIXES, f"claude/{relative}: file type is not allowed in the Claude bundle")
        require(not path.read_bytes().startswith(b"#!"), f"claude/{relative}: executable scripts are not allowed in the Claude bundle")
        require(
            relative.parts[0] != ".claude-plugin" or relative == Path(".claude-plugin/plugin.json"),
            f"claude/{relative}: only plugin.json belongs in the bundle's .claude-plugin/",
        )

    copies = {Path("LICENSE"): Path("LICENSE.txt"), Path("assets/logo.png"): Path("assets/logo.png")}
    for shared in ("skills", "commands"):
        for path in (ROOT / shared).rglob("*"):
            if path.is_file() and path.suffix == ".md":
                copies[path.relative_to(ROOT)] = path.relative_to(ROOT)
    for source, copy in copies.items():
        target = bundle / copy
        require(target.is_file() and target.read_bytes() == (ROOT / source).read_bytes(), f"claude/{copy} is out of sync with {source}; copy it again")
    for shared in ("skills", "commands"):
        extra = {path.relative_to(bundle) for path in (bundle / shared).rglob("*") if path.is_file()} - set(copies.values())
        require(not extra, f"Claude bundle has files that are not in the shared {shared}/: {sorted(map(str, extra))}")


def validate_public_surface() -> None:
    prohibited = [
        (re.compile(r"sk-[A-Za-z0-9_-]{16,}"), "possible API key"),
        (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "possible GitHub token"),
        (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    ]
    todo_marker = "[" + "TODO:"
    tracked = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if tracked.returncode == 0:
        paths = [ROOT / item.decode() for item in tracked.stdout.split(b"\0") if item]
    else:
        paths = list(ROOT.rglob("*"))

    for path in paths:
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        require(todo_marker not in text, f"{path}: unresolved submission placeholder")
        for pattern, label in prohibited:
            require(not pattern.search(text), f"{path}: {label}")


def request(url: str) -> tuple[int, dict[str, str], bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "monologue-plugin-validator/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, dict(response.headers.items()), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers.items()), error.read()


def network_json(url: str) -> tuple[int, dict[str, str], dict[str, Any]]:
    status, headers, body = request(url)
    try:
        return status, headers, json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{url}: response is not JSON") from exc


def validate_network() -> None:
    status, headers, body = network_json(MCP_URL)
    require(status == 401, f"MCP endpoint should challenge unauthenticated requests, got {status}")
    require(body.get("error") == "invalid_token", "MCP endpoint returned an unexpected OAuth error")
    normalized_headers = {key.lower(): value for key, value in headers.items()}
    challenge = normalized_headers.get("www-authenticate", "")
    require("oauth-protected-resource" in challenge, "MCP challenge is missing protected-resource metadata")

    auth_url = "https://api.monologue.to/.well-known/oauth-authorization-server"
    status, _, auth = network_json(auth_url)
    require(status == 200, "OAuth authorization metadata is unavailable")
    require(auth.get("issuer") == "https://api.monologue.to", "OAuth issuer is incorrect")
    require("notes:read" in auth.get("scopes_supported", []), "notes:read scope is missing")
    require("S256" in auth.get("code_challenge_methods_supported", []), "PKCE S256 support is missing")

    resource_url = "https://api.monologue.to/.well-known/oauth-protected-resource/mcp"
    status, _, resource = network_json(resource_url)
    require(status == 200, "OAuth protected-resource metadata is unavailable")
    require(resource.get("resource") == MCP_URL, "OAuth protected resource is incorrect")

    public_urls = [
        "https://www.monologue.to",
        "https://www.monologue.to/privacy",
        "https://www.monologue.to/terms",
        "https://www.monologue.to/docs/support/contact-support",
        "https://www.monologue.to/docs/integrations/mcp",
        "https://api.monologue.to/assets/monologue-icon.png",
    ]
    for url in public_urls:
        status, _, _ = request(url)
        require(status == 200, f"public URL returned {status}: {url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--network", action="store_true", help="also validate live Monologue endpoints")
    args = parser.parse_args()

    try:
        validate_files()
        validate_manifests()
        validate_skills_and_commands()
        validate_claude_bundle()
        validate_public_surface()
        if args.network:
            validate_network()
    except (ValidationError, OSError, json.JSONDecodeError, tomllib.TOMLDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    mode = "manifest, content, and network" if args.network else "manifest and content"
    print(f"OK: {mode} validation passed for {NAME} {VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
