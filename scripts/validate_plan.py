#!/usr/bin/env python3
"""Validate a small hard cut plan. A passing result is not human approval."""

import argparse
from fractions import Fraction
from pathlib import Path
import re
import sys

from common import read_json, safe_relative_path

ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
LIMITATION = ("Checks cover plan structure and recorded evidence only. They do not "
              "verify picture, sound, meaning, rights authenticity, media decodability, "
              "or the identity and judgment of a human reviewer.")


def validate(plan, root, delivery=False):
    errors = []
    identifiers = set()

    def error(where, message):
        errors.append(f"{where}: {message}")

    def shape(value, keys, where):
        if not isinstance(value, dict):
            error(where, "must be an object")
            return False
        missing = set(keys) - value.keys()
        extra = value.keys() - set(keys)
        if missing:
            error(where, "missing keys: " + ", ".join(sorted(missing)))
        if extra:
            error(where, "unknown keys: " + ", ".join(sorted(extra)))
        return not missing

    def string(value, where):
        if not isinstance(value, str) or not value.strip():
            error(where, "must be a nonempty string")
            return False
        return True

    def identifier(value, where):
        if not isinstance(value, str) or not ID.fullmatch(value):
            error(where, "must be a stable lowercase kebab-case ID")
            return False
        if value in identifiers:
            error(where, f"duplicate ID: {value}")
        identifiers.add(value)
        return True

    def integer(value, where, minimum=0):
        if type(value) is not int or value < minimum:
            error(where, f"must be an integer >= {minimum}")
            return False
        return True

    def rate(value, where):
        if not shape(value, ("numerator", "denominator"), where):
            return None
        valid = integer(value["numerator"], where + ".numerator", 1)
        valid = integer(value["denominator"], where + ".denominator", 1) and valid
        if valid:
            return Fraction(value["numerator"], value["denominator"])
        return None

    def path(value, where, must_exist=False):
        try:
            result = safe_relative_path(value, root)
            if must_exist and not result.is_file():
                error(where, "file is missing")
            return result
        except (ValueError, OSError, RuntimeError) as exc:
            error(where, str(exc))
            return None

    def choice(value, choices, where):
        if not isinstance(value, str) or value not in choices:
            error(where, "must be one of: " + ", ".join(choices))
            return False
        return True

    def rows(key):
        value = plan.get(key)
        if not isinstance(value, list):
            error(key, "must be an array")
            return []
        return value

    def interval(row, where):
        valid = integer(row["start_frame"], where + ".start_frame")
        valid = integer(row["end_frame"], where + ".end_frame", 1) and valid
        if valid and row["end_frame"] <= row["start_frame"]:
            error(where, "end_frame must be greater than start_frame (exclusive end)")
            return None
        if valid:
            if duration is not None and row["end_frame"] > duration:
                error(where, "interval exceeds timeline duration")
            return row["start_frame"], row["end_frame"]
        return None

    def coverage(spans, where):
        cursor = 0
        for start, end, name in sorted(spans):
            if start > cursor:
                error(where, f"gap before {name}: frames {cursor} to {start}")
            if start < cursor:
                error(where, f"overlap at {name}: starts {start}, previous end {cursor}")
            cursor = max(cursor, end)
        if duration is not None and cursor != duration:
            error(where, f"coverage ends at {cursor}, expected {duration}")

    def reference(value, mapping, where):
        if not isinstance(value, str) or value not in mapping:
            error(where, "unknown referenced ID")
            return None
        return mapping[value]

    keys = ("schema_version", "project", "timeline", "assets", "chapters", "lines",
            "clips", "approvals", "final_status")
    if not shape(plan, keys, "plan"):
        return errors
    if type(plan["schema_version"]) is not int or plan["schema_version"] != 1:
        error("schema_version", "must be integer 1")
    if shape(plan["project"], ("id", "title"), "project"):
        project_id = plan["project"]["id"]
        if not isinstance(project_id, str) or not ID.fullmatch(project_id):
            error("project.id", "must be a stable lowercase kebab-case ID")
        string(plan["project"]["title"], "project.title")
    fps = duration = None
    if shape(plan["timeline"], ("fps", "duration_frames", "edit_mode"), "timeline"):
        fps = rate(plan["timeline"]["fps"], "timeline.fps")
        if integer(plan["timeline"]["duration_frames"], "timeline.duration_frames", 1):
            duration = plan["timeline"]["duration_frames"]
        choice(plan["timeline"]["edit_mode"], ("hard_cut",), "timeline.edit_mode")
    assets = {}
    for i, asset in enumerate(rows("assets")):
        where = f"assets[{i}]"
        if not shape(asset, ("id", "path", "kind", "duration", "rights"), where):
            continue
        if not identifier(asset["id"], where + ".id"):
            continue
        kind = asset["kind"]
        choice(kind, ("video", "audio", "image"), where + ".kind")
        path(asset["path"], where + ".path", delivery)
        normalized = None
        if kind == "image":
            if asset["duration"] is not None:
                error(where + ".duration", "still images must use null")
        elif shape(asset["duration"], ("frames", "fps"), where + ".duration"):
            source_fps = rate(asset["duration"]["fps"], where + ".duration.fps")
            frame_valid = integer(asset["duration"]["frames"], where + ".duration.frames", 1)
            if source_fps and fps and frame_valid:
                normalized = Fraction(asset["duration"]["frames"]) * fps / source_fps
        rights = asset["rights"]
        if shape(rights, ("status", "evidence"), where + ".rights"):
            choice(rights["status"], ("pending", "cleared", "restricted"), where + ".rights.status")
            if rights["evidence"] is not None:
                path(rights["evidence"], where + ".rights.evidence", delivery)
            if rights["status"] == "cleared" and rights["evidence"] is None:
                error(where + ".rights.evidence", "cleared rights require an evidence path")
            if delivery and rights["status"] != "cleared":
                error(where + ".rights.status", "delivery requires cleared rights")
        assets[asset["id"]] = (kind, normalized)
    chapters = {}
    chapter_spans = []
    for i, chapter in enumerate(rows("chapters")):
        where = f"chapters[{i}]"
        if not shape(chapter, ("id", "title", "start_frame", "end_frame"), where):
            continue
        if not identifier(chapter["id"], where + ".id"):
            continue
        string(chapter["title"], where + ".title")
        span = interval(chapter, where)
        chapters[chapter["id"]] = span
        if span:
            chapter_spans.append((*span, chapter["id"]))
    coverage(chapter_spans, "chapters")
    lines = {}
    for i, line in enumerate(rows("lines")):
        where = f"lines[{i}]"
        if not shape(line, ("id", "chapter_id", "text"), where):
            continue
        if not identifier(line["id"], where + ".id"):
            continue
        string(line["text"], where + ".text")
        reference(line["chapter_id"], chapters, where + ".chapter_id")
        lines[line["id"]] = line["chapter_id"]
    clip_spans = []
    for i, clip in enumerate(rows("clips")):
        where = f"clips[{i}]"
        keys = ("id", "asset_id", "chapter_id", "line_ids", "start_frame", "end_frame",
                "source_in_frame", "source_out_frame", "handle_before_frames", "handle_after_frames")
        if not shape(clip, keys, where):
            continue
        if not identifier(clip["id"], where + ".id"):
            continue
        asset = reference(clip["asset_id"], assets, where + ".asset_id")
        chapter = reference(clip["chapter_id"], chapters, where + ".chapter_id")
        span = interval(clip, where)
        if span:
            clip_spans.append((*span, clip["id"]))
            if chapter and not (chapter[0] <= span[0] and span[1] <= chapter[1]):
                error(where, "clip must be contained in its chapter")
        if not isinstance(clip["line_ids"], list):
            error(where + ".line_ids", "must be an array")
        else:
            seen = set()
            for j, line_id in enumerate(clip["line_ids"]):
                line_chapter = reference(line_id, lines, f"{where}.line_ids[{j}]")
                if isinstance(line_id, str):
                    if line_id in seen:
                        error(where + ".line_ids", "duplicate line reference")
                    seen.add(line_id)
                if line_chapter is not None and line_chapter != clip["chapter_id"]:
                    error(where + ".line_ids", "line belongs to a different chapter")
        source_valid = True
        for field in ("source_in_frame", "source_out_frame", "handle_before_frames", "handle_after_frames"):
            source_valid = integer(clip[field], where + "." + field) and source_valid
        if source_valid and asset:
            start, end = clip["source_in_frame"], clip["source_out_frame"]
            before, after = clip["handle_before_frames"], clip["handle_after_frames"]
            kind, normalized = asset
            if kind == "image":
                if (start, end, before, after) != (0, 0, 0, 0):
                    error(where, "still images require zero source range and handles")
            else:
                if kind == "audio":
                    error(where + ".asset_id", "picture clips cannot reference audio assets")
                if end <= start:
                    error(where, "source_out_frame must exceed source_in_frame")
                if span and end - start != span[1] - span[0]:
                    error(where, "source and timeline durations must match; retiming is unsupported")
                if start - before < 0:
                    error(where, "source handle starts before frame zero")
                if normalized is not None and end + after > normalized:
                    error(where, "source range plus handles exceeds duration normalized to timeline fps")
    coverage(clip_spans, "clips")
    approvals = plan["approvals"]
    if shape(approvals, ("picture", "audio", "owner"), "approvals"):
        for key in ("picture", "audio", "owner"):
            approval = approvals[key]
            where = "approvals." + key
            if not shape(approval, ("status", "reviewer", "evidence"), where):
                continue
            choice(approval["status"], ("pending", "approved", "rejected"), where + ".status")
            if approval["reviewer"] is not None:
                string(approval["reviewer"], where + ".reviewer")
            if approval["evidence"] is not None:
                path(approval["evidence"], where + ".evidence", delivery)
            if approval["status"] == "approved":
                if approval["reviewer"] is None or approval["evidence"] is None:
                    error(where, "approved records require reviewer and evidence")
            elif delivery:
                error(where + ".status", "delivery requires recorded human approval")
    choice(plan["final_status"], ("pending", "approved"), "final_status")
    if delivery and plan["final_status"] != "approved":
        error("final_status", "delivery requires an explicitly recorded approved status")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--delivery", action="store_true", help="also check recorded rights, approvals, and file existence")
    args = parser.parse_args(argv)
    try:
        errors = validate(read_json(args.plan), args.plan.resolve().parent, args.delivery)
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        print(f"ERROR: cannot read plan: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("ERROR: " + error, file=sys.stderr)
        print(LIMITATION, file=sys.stderr)
        return 1
    print("PASS: " + ("delivery records checked." if args.delivery else "structural planning checks passed."))
    print(LIMITATION)
    return 0


if __name__ == "__main__":
    sys.exit(main())
