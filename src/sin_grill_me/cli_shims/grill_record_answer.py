# Purpose: CLI shim for grill_record_answer
# Docs: grill-record-answer.doc.md
"""CLI: grill-record-answer — record a user's answer to a grilling question.

Usage: grill-record-answer --session-id ID --question Q --answer A [--resolution R]
"""
from __future__ import annotations
import argparse
import asyncio
import sys
from ..mcp_server import grill_record_answer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-record-answer", description="Record a user's answer to a grilling question.")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--answer", required=True)
    parser.add_argument("--resolution", default="")
    args = parser.parse_args(argv)
    try:
        print(asyncio.run(grill_record_answer(
            session_id=args.session_id,
            question=args.question,
            answer=args.answer,
            resolution=args.resolution,
        )))
    except (ValueError, KeyError) as e:
        print(f"[grill-record-answer] error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
