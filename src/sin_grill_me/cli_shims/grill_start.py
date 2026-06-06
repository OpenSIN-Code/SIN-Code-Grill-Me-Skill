# Purpose: CLI shim for grill_start
# Docs: grill-start.doc.md
"""CLI: grill-start — start a new grilling session.

Usage: grill-start <TOPIC> [--context CONTEXT]
"""
from __future__ import annotations
import argparse
import asyncio
import sys
from ..mcp_server import grill_start


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grill-start", description="Start a new grilling session.")
    parser.add_argument("topic")
    parser.add_argument("--context", default="")
    args = parser.parse_args(argv)
    print(asyncio.run(grill_start(args.topic, context=args.context)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
