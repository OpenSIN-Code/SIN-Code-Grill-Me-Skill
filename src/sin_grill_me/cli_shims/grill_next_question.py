# Purpose: CLI shim for grill_next_question
# Docs: grill-next-question.doc.md
"""CLI: grill-next-question — get the next question for a grilling session.

Usage: grill-next-question <SESSION_ID>
"""
from __future__ import annotations
import argparse
import asyncio
import sys
from ..mcp_server import grill_next_question


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-next-question", description="Get the next question for a grilling session.")
    parser.add_argument("session_id")
    args = parser.parse_args(argv)
    try:
        print(asyncio.run(grill_next_question(args.session_id)))
    except (ValueError, KeyError) as e:
        print(f"[grill-next-question] error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
