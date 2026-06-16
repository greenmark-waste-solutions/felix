from __future__ import annotations

import argparse
from pathlib import Path

from .core import (
    agentic_context_source,
    render_agent_template,
    render_brand_safety,
    render_scaffold_result,
    audit_brand_safety,
    doctor,
    fetch_agentic_context,
    find_agent,
    list_agents,
    render_agent_interview,
    render_plugin_doctor,
    render_self_checks,
    roadmap,
    run_checks,
    scaffold,
    scaffold_plan,
    standards,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="felix",
        description="Felix: build and maintain agent ecosystems.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="check local prerequisites")
    subparsers.add_parser("check", help="run Felix's local maintenance checks")
    subparsers.add_parser("roadmap", help="show Felix's agent-building roadmap")
    subparsers.add_parser("self", help="audit Felix against his own standards")
    subparsers.add_parser("standards", help="show standard requirements for every agent")
    subparsers.add_parser("agentic-context", help="fetch the latest agentic intelligence context gist")
    subparsers.add_parser("agentic-context-source", help="show the live agentic intelligence context URL")
    subparsers.add_parser("agent-template", help="show the reusable Python agent CLI template")
    brand_parser = subparsers.add_parser("brand-safety", help="audit protected brand references")
    brand_parser.add_argument("--root", type=Path, help="root to scan; defaults to this repo")
    interview_parser = subparsers.add_parser("interview", help="run the pre-scaffold role-boundary interview")
    interview_parser.add_argument("name")
    interview_parser.add_argument("--purpose", default="", help="brief purpose to improve overlap checks")

    plugin_parser = subparsers.add_parser("plugin", help="inspect and maintain Codex plugins")
    plugin_sub = plugin_parser.add_subparsers(dest="plugin_command", required=True)
    plugin_doctor_parser = plugin_sub.add_parser("doctor", help="check a Codex plugin package")
    plugin_doctor_parser.add_argument("path", type=Path)

    agents_parser = subparsers.add_parser("agents", help="inspect known agents")
    agents_sub = agents_parser.add_subparsers(dest="agents_command", required=True)
    agents_sub.add_parser("list", help="list known agents")
    show_parser = agents_sub.add_parser("show", help="show one known agent")
    show_parser.add_argument("name")

    scaffold_parser = subparsers.add_parser("scaffold-plan", help="show the planned scaffold for an agent")
    scaffold_parser.add_argument("name")

    scaffold_write_parser = subparsers.add_parser("scaffold", help="dry-run or write a starter agent repo")
    scaffold_write_parser.add_argument("name")
    scaffold_write_parser.add_argument("--root", type=Path, help="target repo root; defaults to ./<name>")
    scaffold_write_parser.add_argument("--write", action="store_true", help="write files; default is dry-run")
    scaffold_write_parser.add_argument("--force", action="store_true", help="overwrite existing files when writing")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        print("\n".join(doctor()))
        return 0

    if args.command == "check":
        return run_checks()

    if args.command == "roadmap":
        print(roadmap())
        return 0

    if args.command == "self":
        print(render_self_checks())
        return 0

    if args.command == "standards":
        for item in standards():
            print(f"- {item}")
        return 0

    if args.command == "agentic-context":
        print(fetch_agentic_context())
        return 0

    if args.command == "agentic-context-source":
        print(agentic_context_source())
        return 0

    if args.command == "agent-template":
        print(render_agent_template())
        return 0

    if args.command == "brand-safety":
        print(render_brand_safety(args.root))
        return 1 if audit_brand_safety(args.root) else 0

    if args.command == "interview":
        print(render_agent_interview(args.name, purpose=args.purpose))
        return 0

    if args.command == "plugin":
        if args.plugin_command == "doctor":
            output = render_plugin_doctor(args.path)
            print(output)
            return 1 if "Felix plugin doctor: FAIL" in output else 0

    if args.command == "agents":
        if args.agents_command == "list":
            for agent in list_agents():
                print(f"{agent.name}\t{agent.status}\t{agent.role}")
            return 0
        if args.agents_command == "show":
            try:
                agent = find_agent(args.name)
            except KeyError as exc:
                parser.error(str(exc))
            print(f"name: {agent.name}")
            print(f"role: {agent.role}")
            print(f"repo: {agent.repo}")
            print(f"status: {agent.status}")
            print(f"next: {agent.next_action}")
            return 0

    if args.command == "scaffold-plan":
        print(scaffold_plan(args.name))
        return 0

    if args.command == "scaffold":
        result = scaffold(args.name, root=args.root, write=args.write, force=args.force)
        print(render_scaffold_result(result))
        return 1 if result.skipped else 0

    parser.error("unhandled command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
