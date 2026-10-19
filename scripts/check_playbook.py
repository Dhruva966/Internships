#!/usr/bin/env python3
"""Offline package checks only. Does not research, schedule, or apply to jobs."""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "AGENTS.md", "SECURITY.md", ".gitignore",
    "docs/SETUP.md", "docs/INTAKE.md", "docs/RESEARCH.md",
    "docs/TRACKER.md", "docs/SHORT_ANSWERS.md", "docs/APPLY.md",
    "docs/SCHEDULING.md", "docs/QUALITY_GATES.md",
    "prompts/BOOTSTRAP.md", "prompts/DAILY_RUN.md", "prompts/APPLICATION_PASS.md",
    "templates/profile.example.json", "templates/roles.example.csv",
    "templates/questions.example.csv",
]


def check(root=ROOT):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^\s)]+)\)", content):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            file_target = target.split("#", 1)[0]
            resolved = (path.parent / file_target).resolve()
            if not resolved.is_relative_to(root.resolve()):
                errors.append(f"Link escapes repository: {path.relative_to(root)} -> {target}")
            elif not resolved.exists():
                errors.append(f"Broken link: {path.relative_to(root)} -> {target}")
        if re.search(r"(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{15,}", content):
            errors.append(f"Possible credential: {path.relative_to(root)}")
    for path in (root / "templates").glob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            errors.append(f"Invalid JSON: {path.name}: {exc}")
    for path in (root / "templates").glob("*.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle))
        if not rows or not rows[0] or len(rows[0]) != len(set(rows[0])):
            errors.append(f"Missing/duplicate CSV headers: {path.name}")
            continue
        for number, row in enumerate(rows[1:], 2):
            if len(row) != len(rows[0]):
                errors.append(f"CSV width mismatch: {path.name}:{number}")
    for name in ["private", "runtime", "state", "resumes", "transcripts", "receipts"]:
        if (root / name).exists():
            errors.append(f"Private runtime directory present in package: {name}")
    return errors


if __name__ == "__main__":
    failures = check()
    for failure in failures:
        print(f"FAIL: {failure}", file=sys.stderr)
    if failures:
        sys.exit(1)
    print("PASS: required docs, relative file links, JSON, CSV shapes, and basic package hygiene")
    print("NOT TESTED: live tools, employer sites, intake, scheduler, eligibility, or application submissions")
