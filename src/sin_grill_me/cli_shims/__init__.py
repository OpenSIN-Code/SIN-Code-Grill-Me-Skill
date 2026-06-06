# Purpose: CLI shim package for sin-grill-me MCP tools
# Docs: __init__.doc.md
"""CLI shim package for sin-grill-me — thin argparse wrappers around
each tool in sin_grill_me.mcp_server. The original tools are async,
so each shim wraps the call in `asyncio.run`."""
