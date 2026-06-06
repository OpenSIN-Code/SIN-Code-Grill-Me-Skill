# Purpose: CLI shim for grill_synthesize
# Docs: grill-synthesize.doc.md
"""CLI: grill-synthesize — synthesize a grilling session into decisions + assumptions + next steps.

Usage: grill-synthesize <SESSION_ID>
"""
from __future__ import annotations
import argparse
import asyncio
import sys
from ..mcp_server import grill_synthesize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-synthesize", description="Synthesize a grilling session into decisions, assumptions, and next steps.")
    parser.add_argument("session_id")
    args = parser.parse_args(argv)
    try:
        print(asyncio.run(grill_synthesize(args.session_id)))
    except (ValueError, KeyError) as e:
        print(f"[grill-synthesize] error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
