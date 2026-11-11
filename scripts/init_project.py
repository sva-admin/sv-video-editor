#!/usr/bin/env python3
"""Create a planning project with pending reviews and no source media."""

import argparse
from pathlib import Path
import re
import shutil
import sys

from common import read_json, write_json


def initialize(destination, project_id=None):
    destination = Path(destination)
    project_id = project_id or destination.name
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", project_id):
        raise ValueError("project ID must be lowercase kebab-case, starting with a letter")
    templates = Path(__file__).resolve().parent.parent / "templates"
    records = {name: read_json(templates / name) for name in ("plan.json", "brief.json", "review.json")}
    handoff = (templates / "HANDOFF.md").read_text(encoding="utf-8")
    records["plan.json"]["project"]["id"] = project_id
    records["plan.json"]["project"]["title"] = project_id.replace("-", " ").title()
    records["plan.json"]["final_status"] = "pending"
    # mkdir is exclusive. Never merge into an existing project, even an empty one.
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for folder in ("sources", "evidence", "exports"):
            (destination / folder).mkdir()
        for name, record in records.items():
            write_json(destination / name, record)
        (destination / "HANDOFF.md").write_text(handoff, encoding="utf-8")
    except Exception:
        # Only this newly created directory is eligible for rollback.
        shutil.rmtree(destination)
        raise
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--project-id", help="stable lowercase ID, defaults to directory name")
    args = parser.parse_args(argv)
    try:
        result = initialize(args.destination, args.project_id)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: could not initialize project: {exc}", file=sys.stderr)
        return 2
    print(f"Created {result}. Placeholder plan only; final status and reviews are pending.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
