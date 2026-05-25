#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""
Advisory lockfile for KB write operations.

Writes are autonomous per the skill's trust model, but Ingest and Update
touch multiple files (the page, the repo index, the wiki/plans index,
cross-link targets). A second agent session, or a crash mid-write, can
corrupt the KB into a state where indexes don't match pages. This is the
serialization primitive: acquire before write, release after.

The lock is advisory — it only blocks other processes that also call
acquire. Stale locks (older than STALE_AFTER_SECONDS) are reclaimed
automatically, so a crashed holder doesn't deadlock the KB forever.

Usage:
    uv run scripts/kb-lock.py acquire <kb-path>   # exit 0 if held, 1 if blocked
    uv run scripts/kb-lock.py release <kb-path>   # exit 0 always
    uv run scripts/kb-lock.py status  <kb-path>   # print holder info

Exit codes:
    0   action succeeded
    1   acquire failed (live lock held by another process)
    2   bad arguments / kb_path doesn't exist
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LOCK_NAME = ".kb-lock"
STALE_AFTER_SECONDS = 3600  # 1 hour


def _read_lock(lock: Path) -> dict | None:
    """Return the lock holder dict, or None if missing/unreadable."""
    try:
        return json.loads(lock.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def acquire(kb_path: Path) -> int:
    """Take the lock if free or stale. Returns 0 on success, 1 if blocked."""
    lock = kb_path / LOCK_NAME
    if lock.exists():
        data = _read_lock(lock)
        if data is None:
            print(f"warning: existing lockfile at {lock} is unreadable; "
                  "reclaiming", file=sys.stderr)
        else:
            age = time.time() - data.get("acquired_at", 0)
            if age < STALE_AFTER_SECONDS:
                print(f"lock held by PID {data.get('pid', '?')} since "
                      f"{data.get('acquired_iso', '?')} "
                      f"({int(age)}s ago)", file=sys.stderr)
                return 1
            print(f"warning: stale lock from PID {data.get('pid', '?')} "
                  f"({int(age)}s old); reclaiming", file=sys.stderr)
        try:
            lock.unlink()
        except OSError as e:
            print(f"error: couldn't remove stale lock: {e}", file=sys.stderr)
            return 1
    payload = {
        "pid": os.getpid(),
        "acquired_at": time.time(),
        "acquired_iso": datetime.now(timezone.utc).isoformat(),
    }
    tmp = lock.with_suffix(lock.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2))
    os.replace(tmp, lock)
    print(f"acquired (pid {payload['pid']})")
    return 0


def release(kb_path: Path) -> int:
    """Drop the lock if present. Always returns 0."""
    lock = kb_path / LOCK_NAME
    if lock.exists():
        try:
            lock.unlink()
            print("released")
        except OSError as e:
            print(f"warning: couldn't remove lock: {e}", file=sys.stderr)
    else:
        print("not held")
    return 0


def status(kb_path: Path) -> int:
    """Print lock state and return 0."""
    lock = kb_path / LOCK_NAME
    if not lock.exists():
        print("not held")
        return 0
    data = _read_lock(lock)
    if data is None:
        print("lockfile present but unreadable")
        return 0
    age = int(time.time() - data.get("acquired_at", 0))
    stale = " (stale, will be reclaimed on next acquire)" \
        if age >= STALE_AFTER_SECONDS else ""
    print(f"held by PID {data.get('pid', '?')} for {age}s "
          f"(since {data.get('acquired_iso', '?')}){stale}")
    return 0


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Advisory lockfile for KB write operations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("action", choices=["acquire", "release", "status"])
    parser.add_argument("kb_path", type=Path,
                        help="Path to the KB root (contains wiki/ and plans/)")
    args = parser.parse_args()
    if not args.kb_path.is_dir():
        print(f"error: kb_path {args.kb_path} is not a directory",
              file=sys.stderr)
        return 2
    return {"acquire": acquire, "release": release, "status": status}[
        args.action](args.kb_path)


if __name__ == "__main__":
    sys.exit(main())
