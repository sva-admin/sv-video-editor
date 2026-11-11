#!/usr/bin/env python3
"""Read local media metadata with ffprobe. Never upload or render media."""

import argparse
from pathlib import Path
import subprocess
import sys

from common import parse_json, write_json


def probe(source, count_frames=False, ffprobe="ffprobe", timeout=120):
    source = Path(source).resolve(strict=True)
    if not source.is_file():
        raise ValueError("source must be a local regular file")
    if type(timeout) is not int or timeout <= 0:
        raise ValueError("timeout must be a positive integer")
    before = source.stat()
    command = [ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe",
               "-show_error", "-show_format", "-show_streams", "-of", "json"]
    if count_frames:
        command.append("-count_frames")
    command.extend(["-i", str(source)])
    result = subprocess.run(command, check=False, capture_output=True,
                            text=True, timeout=timeout)
    if result.returncode or result.stderr.strip():
        detail = result.stderr.strip()[:2000] or f"exit code {result.returncode}"
        raise ValueError("ffprobe failed or reported decode errors: " + detail)
    metadata = parse_json(result.stdout)
    if not isinstance(metadata, dict) or metadata.get("error"):
        raise ValueError("ffprobe returned an error or invalid metadata")
    if not isinstance(metadata.get("streams"), list) or not metadata["streams"]:
        raise ValueError("ffprobe found no streams")
    if any(not isinstance(stream, dict) for stream in metadata["streams"]):
        raise ValueError("ffprobe returned an invalid stream record")
    after = source.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("source changed during probe; retry with an unchanged file")
    return {
        "schema_version": 1,
        "source": {"path": str(source), "size_bytes": after.st_size,
                   "mtime_ns": after.st_mtime_ns},
        "count_frames_requested": count_frames,
        "limitations": "Local metadata and optional decoded frame counts only. This is not visual, audio, rights, or delivery approval.",
        "ffprobe": metadata,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count-frames", action="store_true", help="decode streams and request nb_read_frames, which may be unavailable")
    parser.add_argument("--timeout", type=int, default=120, help="timeout in seconds, default 120")
    parser.add_argument("--ffprobe", default="ffprobe", help="ffprobe executable name or path")
    parser.add_argument("--force", action="store_true", help="replace an existing output JSON file")
    args = parser.parse_args(argv)
    try:
        if args.output.resolve() == args.source.resolve():
            raise ValueError("output must differ from the source")
        if args.output.exists() and not args.force:
            raise FileExistsError("output already exists; use --force to replace it")
        record = probe(args.source, args.count_frames, args.ffprobe, args.timeout)
        write_json(args.output, record, args.force)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote local metadata to {args.output}. Keep this JSON private with its project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
