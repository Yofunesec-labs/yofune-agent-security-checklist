#!/usr/bin/env python3
"""Dual-era MCP JSON-RPC stdio fixture for YASC adapter smoke tests.

It intentionally implements only the small subset needed by the harness smoke tests.
It is not a substitute for an official SDK in production.
"""
import json
import sys

MODERN = "2026-07-28"
LEGACY = "2025-11-25"
SERVER_INFO = {"name": "yasc-fixture", "version": "1.0.0"}
TOOLS = [{
    "name": "echo",
    "description": "Return input text",
    "inputSchema": {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
        "additionalProperties": False,
    },
}]


def send(rid, *, result=None, error=None, modern=False):
    obj = {"jsonrpc": "2.0", "id": rid}
    if error is not None:
        obj["error"] = error
    else:
        obj["result"] = result
        if modern and isinstance(obj["result"], dict):
            meta = dict(obj["result"].get("_meta", {}))
            meta["io.modelcontextprotocol/serverInfo"] = SERVER_INFO
            obj["result"]["_meta"] = meta
    print(json.dumps(obj, separators=(",", ":")), flush=True)


for line in sys.stdin:
    try:
        req = json.loads(line)
    except Exception:
        continue
    method = req.get("method")
    rid = req.get("id")
    if rid is None:
        continue
    params = req.get("params", {}) or {}
    meta = params.get("_meta", {}) if isinstance(params, dict) else {}
    modern = bool(meta.get("io.modelcontextprotocol/protocolVersion") == MODERN or method == "server/discover")

    if method == "server/discover":
        send(rid, result={
            "supportedVersions": [MODERN, LEGACY],
            "capabilities": {"tools": {"listChanged": False}},
            "instructions": "Use echo only for test data.",
        }, modern=True)
    elif method == "initialize":
        send(rid, result={
            "protocolVersion": params.get("protocolVersion", LEGACY),
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        })
    elif method == "tools/list":
        send(rid, result={"tools": TOOLS}, modern=modern)
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name != "echo":
            send(rid, error={"code": -32602, "message": "unknown tool"})
            continue
        if set(args) != {"text"} or not isinstance(args.get("text"), str):
            send(rid, error={"code": -32602, "message": "invalid arguments"})
            continue
        send(rid, result={"content": [{"type": "text", "text": args["text"]}], "isError": False}, modern=modern)
    else:
        send(rid, error={"code": -32601, "message": "method not found"})
