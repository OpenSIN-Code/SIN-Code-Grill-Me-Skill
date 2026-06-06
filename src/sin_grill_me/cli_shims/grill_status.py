# Purpose: CLI shim for grill_status
# Docs: grill-status.doc.md
"""CLI: grill-status — get status of a grilling session.

Usage: grill-status <SESSION_ID>
"""
from __future__ import annotations
import argparse
import asyncio
import sys
from ..mcp_server import grill_status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-status", description="Get status of a grilling session.")
    parser.add_argument("session_id")
    args = parser.parse_args(argv)
    try:
        print(asyncio.run(grill_status(args.session_id)))
    except (ValueError, KeyError) as e:
        print(f"[grill-status] error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
