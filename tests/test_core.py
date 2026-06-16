from pathlib import Path

from felix.core import (
    agentic_context_source,
    agent_template_files,
    audit_brand_safety,
    check_commands,
    doctor,
    find_agent,
    list_agents,
    plugin_doctor_checks,
    render_brand_safety,
    render_agent_interview,
    render_plugin_doctor,
    render_scaffold_result,
    render_self_checks,
    roadmap,
    scaffold,
    scaffold_files,
    scaffold_plan,
    self_checks,
    standards,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_agent_registry_includes_planned_agents():
    names = {agent.name for agent in list_agents()}

    assert {"felix", "knox", "capcom", "dewey", "reeves", "leinad", "scry", "surfari"} <= names


def test_find_agent_returns_boundary():
    agent = find_agent("knox")

    assert agent.status == "registered"
    assert "secrets" in agent.role


def test_standards_require_wiki_and_tasks():
    text = "\n".join(standards())

    assert "repo-native wiki" in text
    assert "task list" in text
    assert "abstract agent interface" in text
    assert "open-source health files" in text
    assert "AGENTS.md wakeup file" in text
    assert "original agent identity image" in text
    assert "visible agent name" in text
    assert "agentic intelligence context injection" in text
    assert "have, want, and don't want" in text
    assert "tools as evidence" in text
    assert "thinking, tools, memory, coordination" in text
    assert "memory as thinking substrate" in text
    assert "North Star goal-orientation" in text
    assert "brand-safety scan" in text
    assert "pre-scaffold interview" in text
    assert "setup-first discipline" in text


def test_roadmap_prioritizes_knox_then_capcom():
    text = roadmap()

    assert "Scaffold Knox" in text
    assert "Scaffold Capcom" in text
    assert "Scaffold Dewey" in text
    assert "agent identity image prompts" in text
    assert "agentic intelligence gist" in text
    assert "have/want/don't-want" in text
    assert "Python agent CLI template" in text
    assert "AGENTS.md wakeup files" in text
    assert "felix scaffold agent-name" in text
    assert "felix interview agent-name" in text
    assert "brand-safety audits" in text


def test_scaffold_plan_specializes_knox_and_capcom():
    assert "Touch ID" in scaffold_plan("knox")
    assert "acknowledgement" in scaffold_plan("capcom")
    assert "Code Context Engine" in scaffold_plan("dewey")
    assert "agentic-context" in scaffold_plan("knox")
    assert "felix interview knox" in scaffold_plan("knox")
    assert "highest-leverage decision" in scaffold_plan("knox")
    assert "choose the agent topology" in scaffold_plan("knox")
    assert "choose the knowledge home" in scaffold_plan("knox")
    assert "choose the run mode" in scaffold_plan("knox")
    assert "write a decision record" in scaffold_plan("knox")
    assert "AGENTS.md wakeup file" in scaffold_plan("knox")
    assert "have, want, and don't want" in scaffold_plan("knox")
    assert "evidence to reconcile" in scaffold_plan("knox")
    assert "brand-safety test coverage" in scaffold_plan("knox")
    assert "templates/python-agent-cli" in scaffold_plan("knox")
    assert "felix scaffold <name>" in scaffold_plan("knox")


def test_doctor_reports_wiki():
    assert any(line.startswith("wiki:") for line in doctor())


def test_self_checks_cover_foss_and_mascot():
    names = {check.name for check in self_checks()}

    assert {"agents", "claude", "license", "changelog", "contributing", "security", "mascot", "task_list"} <= names
    assert "Felix self-audit:" in render_self_checks()
    assert any(check.detail == "assets/felix-mascot.png" for check in self_checks())


def test_check_commands_capture_maintenance_loop():
    commands = {" ".join(command) for command in check_commands()}

    assert "python -m pytest -q" in commands
    assert "ruff check ." in commands
    assert "scridos lint wiki/felix" in commands
    assert "python -m felix.cli brand-safety" in commands
    assert "python -m felix.cli self" in commands


def test_agentic_context_source_is_live_gist_url():
    source = agentic_context_source()

    assert "gist.githubusercontent.com/dshanklin-bv/0ea9eae3845566a255f4fe9e0bf21590/raw/agentic_intelligence.md" in source


def test_agent_template_files_exist_and_encode_agent_shape():
    files = agent_template_files()
    text = "\n".join(path.read_text(encoding="utf-8") for path in files)

    assert all(path.exists() for path in files)
    assert "agentic-context" in text
    assert "agentic-context-source" in text
    assert "Agents Wakeup" in text
    assert "Read First" in text
    assert "agent" in text
    assert "Have:" in text
    assert "Want:" in text
    assert "Don't want:" in text
    assert "evidence to reconcile" in text
    assert "memory is part of thinking" in text


def test_agent_interview_names_role_boundary_and_overlap():
    text = render_agent_interview("sage", purpose="Sage Intacct maintenance CLI")

    assert "Felix agent interview: Sage" in text
    assert "Do not scaffold yet" in text
    assert "Setup principle" in text
    assert "highest-leverage decision" in text
    assert "Role boundary" in text
    assert "What topology fits this agent" in text
    assert "Where do durable knowledge, task execution, live state, and learned facts belong" in text
    assert "Should the CLI run from source checkout" in text
    assert "Which option does the agent recommend" in text
    assert "What does the human choose or override" in text
    assert "Have / want / don't want" in text
    assert "What should `doctor` check?" in text
    assert "What CLI verbs should exist" in text
    assert "Known-agent overlap check" in text
    assert "felix scaffold sage" in text


def test_agent_interview_detects_registered_overlap():
    text = render_agent_interview("knox", purpose="secrets and access")

    assert "possible overlap: knox" in text


def test_scaffold_dry_run_lists_generated_repo_files(tmp_path):
    target = tmp_path / "test-agent"
    result = scaffold("Test Agent", root=target)
    output = render_scaffold_result(result)
    paths = {file.path.relative_to(target) for file in result.files}

    assert result.root == target.resolve()
    assert not result.wrote
    assert not target.exists()
    assert "DRY RUN" in output
    assert "No files written" in output
    assert {
        Path("AGENTS.md"),
        Path("README.md"),
        Path("pyproject.toml"),
        Path("test_agent/cli.py"),
        Path("test_agent/agentic_context.py"),
        Path("tests/test_cli.py"),
        Path("tests/test_brand_safety.py"),
        Path("wiki/test-agent/wiki/index.md"),
        Path("assets/test-agent-image-prompt.md"),
    } <= paths


def test_scaffold_write_creates_installable_cli_skeleton(tmp_path):
    target = tmp_path / "demo-agent"
    result = scaffold("demo-agent", root=target, write=True)

    assert result.wrote
    assert (target / "AGENTS.md").exists()
    assert (target / "demo_agent" / "cli.py").exists()
    assert (target / "pyproject.toml").read_text(encoding="utf-8").count("demo-agent") >= 2
    assert 'prog="demo-agent"' in (target / "demo_agent" / "cli.py").read_text(encoding="utf-8")


def test_scaffold_refuses_to_overwrite_without_force(tmp_path):
    target = tmp_path / "demo-agent"
    scaffold("demo-agent", root=target, write=True)
    result = scaffold("demo-agent", root=target, write=True)

    assert not result.wrote
    assert result.skipped


def test_scaffold_files_normalize_names(tmp_path):
    files = scaffold_files("Demo Agent!", root=tmp_path / "demo-agent")
    paths = {file.path for file in files}

    assert tmp_path / "demo-agent" / "demo_agent" / "cli.py" in paths


def test_public_repo_avoids_protected_felix_references():
    assert not audit_brand_safety(REPO_ROOT)
    assert "PASS" in render_brand_safety(REPO_ROOT)


def test_brand_safety_reports_findings(tmp_path):
    risky_file = tmp_path / "README.md"
    risky_file.write_text("This mentions a risky " + "fix" + "-it" + " phrase.", encoding="utf-8")
    findings = audit_brand_safety(tmp_path)

    assert len(findings) == 1
    assert findings[0].path == risky_file
    assert "FAIL" in render_brand_safety(tmp_path)


def write_plugin(root: Path, *, manifest: bool = True, skill_frontmatter: str | None = None) -> None:
    (root / ".codex-plugin").mkdir(parents=True)
    (root / "skills" / "use-demo").mkdir(parents=True)
    if manifest:
        (root / ".codex-plugin" / "plugin.json").write_text(
            """
{
  "name": "demo-plugin",
  "version": "0.1.0",
  "description": "Demo plugin.",
  "author": {"name": "Felix", "url": "https://example.com"},
  "homepage": "https://example.com",
  "repository": "https://example.com/repo",
  "license": "MIT",
  "skills": "./skills/",
  "interface": {
    "displayName": "Demo",
    "shortDescription": "Demo plugin.",
    "longDescription": "Demo plugin for Felix plugin doctor tests.",
    "developerName": "Felix",
    "category": "Developer Tools",
    "capabilities": ["Demo"],
    "websiteURL": "https://example.com",
    "privacyPolicyURL": "https://example.com/privacy",
    "termsOfServiceURL": "https://example.com/terms",
    "defaultPrompt": ["Use Demo."]
  }
}
""".strip()
            + "\n",
            encoding="utf-8",
        )
    for filename in ("README.md", "LICENSE", "SECURITY.md"):
        (root / filename).write_text(f"# {filename}\n", encoding="utf-8")
    frontmatter = skill_frontmatter
    if frontmatter is None:
        frontmatter = "---\nname: use-demo\ndescription: Use the demo plugin.\n---\n"
    (root / "skills" / "use-demo" / "SKILL.md").write_text(frontmatter + "\n# Demo\n", encoding="utf-8")


def test_plugin_doctor_passes_minimal_plugin(tmp_path: Path) -> None:
    write_plugin(tmp_path)

    output = render_plugin_doctor(tmp_path)

    assert "Felix plugin doctor: PASS" in output
    assert "required_file:.codex-plugin/plugin.json: ok" in output
    assert "skill_description:use-demo: ok" in output
    assert not any(not check.ok for check in plugin_doctor_checks(tmp_path))


def test_plugin_doctor_fails_missing_manifest(tmp_path: Path) -> None:
    write_plugin(tmp_path, manifest=False)

    checks = plugin_doctor_checks(tmp_path)

    assert any(check.name == "required_file:.codex-plugin/plugin.json" and not check.ok for check in checks)
    assert "Felix plugin doctor: FAIL" in render_plugin_doctor(tmp_path)


def test_plugin_doctor_fails_missing_required_file(tmp_path: Path) -> None:
    write_plugin(tmp_path)
    (tmp_path / "SECURITY.md").unlink()

    checks = plugin_doctor_checks(tmp_path)

    assert any(check.name == "required_file:SECURITY.md" and not check.ok for check in checks)


def test_plugin_doctor_fails_invalid_skill_frontmatter(tmp_path: Path) -> None:
    write_plugin(tmp_path, skill_frontmatter="# Missing frontmatter")

    checks = plugin_doctor_checks(tmp_path)

    assert any(check.name == "skill_name:use-demo" and not check.ok for check in checks)
    assert any(check.name == "skill_description:use-demo" and not check.ok for check in checks)
