# Docs: ./mcp_server.py

## What this file does
FastMCP server exposing 5 grill-me tools over stdio JSON-RPC:
`grill_start`, `grill_status`, `grill_next_question`, `grill_record_answer`,
`grill_synthesize`.

## Dependency map
- Imports from: `sin_grill_me.grill` (GrillSession, QuestionCategory), fastmcp
- Imported by: opencode.json (registered as MCP server)
- Talks to: opencode agent (JSON-RPC over stdio)

## Important config
- **MCP transport**: stdio (no port, no HTTP — MCP launches the script and
  pipes JSON-RPC through stdin/stdout)
- **State**: in-process dict `_SESSIONS` keyed by session_id
- **State dir**: `~/.config/opencode/` (created on first run)

## Why these decisions
- **In-process state, no DB**: grilling is a short-lived conversation,
  not a long-running service. Sessions vanish on restart — by design.
- **`if __name__ == "__main__": main()`** — required for
  `python -m sin_grill_me.mcp_server` to work (fastmcp.run() needs to
  be called explicitly).
- **5 tools, not 1** — granularity matches the conversation flow
  (start → ask → answer → next → synthesize), so the agent can drive
  one step at a time and persist progress between calls.

## Usage example
```bash
# Register in opencode.json:
"sin-grill-me": {
  "type": "local",
  "command": ["python3", "-m", "sin_grill_me.mcp_server"],
  "environment": {"PYTHONPATH": "/path/to/sin-grill-me/src"},
  "enabled": true
}
```

## Known caveats
- **Session loss on restart** — every opencode restart wipes in-memory
  sessions. Documented in grill.doc.md. Not a bug, by design.
- **No `dotenv` / `.env` loading** — the skill is config-free.
- **Single-process** — no concurrency safety. Two agents calling
  `grill_record_answer` on the same session_id at the same time will
  race. (Not a real concern: grilling is single-agent by nature.)
