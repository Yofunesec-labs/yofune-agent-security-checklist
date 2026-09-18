from __future__ import annotations

import json
import select
import subprocess
import threading
from typing import Any

import requests

from .base import MCPAdapter
from ..util import expand_env

MODERN_VERSION = "2026-07-28"
LEGACY_VERSION = "2025-11-25"


class _JSONRPC:
    def __init__(self):
        self._id = 0

    def next(self) -> int:
        self._id += 1
        return self._id


def _client_meta(version: str = MODERN_VERSION) -> dict[str, Any]:
    return {
        "io.modelcontextprotocol/protocolVersion": version,
        "io.modelcontextprotocol/clientInfo": {"name": "yasc-harness", "version": "1.0.0"},
        "io.modelcontextprotocol/clientCapabilities": {},
    }


def _modern_params(params: dict[str, Any] | None, version: str) -> dict[str, Any]:
    out = dict(params or {})
    meta = dict(out.get("_meta", {}))
    for key, value in _client_meta(version).items():
        meta.setdefault(key, value)
    out["_meta"] = meta
    return out


def _is_method_not_found(payload: dict[str, Any]) -> bool:
    err = payload.get("error") or {}
    return err.get("code") == -32601


def _select_modern_version(discover: dict[str, Any], preferred: str) -> str | None:
    supported = discover.get("supportedVersions") or discover.get("supportedProtocolVersions") or []
    if preferred in supported:
        return preferred
    modern = [v for v in supported if isinstance(v, str) and v >= MODERN_VERSION]
    return modern[0] if modern else None


class _StdioWire:
    def __init__(self, command: list[str], *, cwd: str | None, timeout: float):
        self.timeout = timeout
        self.proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=cwd or None,
        )
        self.rpc = _JSONRPC()
        self.lock = threading.Lock()

    def request_payload(self, method: str, params: dict[str, Any] | None = None, *, notification: bool = False) -> dict[str, Any]:
        with self.lock:
            msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
            if params is not None:
                msg["params"] = params
            req_id = None if notification else self.rpc.next()
            if req_id is not None:
                msg["id"] = req_id
            assert self.proc.stdin and self.proc.stdout
            self.proc.stdin.write(json.dumps(msg, separators=(",", ":")) + "\n")
            self.proc.stdin.flush()
            if notification:
                return {"jsonrpc": "2.0", "result": {}}
            while True:
                ready, _, _ = select.select([self.proc.stdout], [], [], self.timeout)
                if not ready:
                    raise TimeoutError(f"MCP stdio request timed out after {self.timeout:g}s: {method}")
                line = self.proc.stdout.readline()
                if not line:
                    err = self.proc.stderr.read() if self.proc.stderr else ""
                    raise RuntimeError(f"MCP stdio server closed pipe: {err[-1000:]}")
                obj = json.loads(line)
                if obj.get("id") == req_id:
                    return obj

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class StdioMCPAdapter:
    """MCP stdio adapter supporting modern 2026-07-28 and legacy handshake servers.

    In auto mode the modern discovery probe uses a disposable sibling process, mirroring
    the safety behavior of current Tier-1 SDKs so an old server cannot poison the main pipe.
    """

    name = "mcp-stdio"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        command = self.config.get("command")
        if not isinstance(command, list) or not command:
            raise ValueError("mcp-stdio adapter requires command: [program, ...]")
        self.command = command
        self.cwd = self.config.get("cwd") or None
        self.timeout = float(self.config.get("timeout_seconds", 20))
        self.probe_timeout = float(self.config.get("probe_timeout_seconds", min(2.0, self.timeout)))
        self.mode = self.config.get("mode", "auto")
        self.preferred_version = self.config.get("protocol_version", MODERN_VERSION)
        self.era: str | None = None
        self.protocol_version: str | None = None
        self.discover_result: dict[str, Any] | None = None
        self._initialized = False

        if self.mode == "auto":
            self._probe_sibling()
        elif self.mode in {"modern", MODERN_VERSION}:
            self.era = "modern"
            self.protocol_version = self.preferred_version
        elif self.mode == "legacy":
            self.era = "legacy"
        else:
            raise ValueError("mcp mode must be auto, modern, legacy, or 2026-07-28")
        self.wire = _StdioWire(self.command, cwd=self.cwd, timeout=self.timeout)

    def _probe_sibling(self) -> None:
        probe = _StdioWire(self.command, cwd=self.cwd, timeout=self.probe_timeout)
        try:
            payload = probe.request_payload(
                "server/discover",
                _modern_params({}, self.preferred_version),
            )
            if "result" in payload:
                selected = _select_modern_version(payload["result"], self.preferred_version)
                if selected:
                    self.era = "modern"
                    self.protocol_version = selected
                    self.discover_result = payload["result"]
                    return
            # Method-not-found or an unrecognized discover result is legacy evidence on stdio.
            self.era = "legacy"
        except (TimeoutError, RuntimeError, BrokenPipeError, json.JSONDecodeError):
            self.era = "legacy"
        finally:
            probe.close()

    def _legacy_initialize(self) -> dict[str, Any]:
        if self._initialized:
            return {"already_initialized": True, "protocolVersion": self.protocol_version}
        payload = self.wire.request_payload(
            "initialize",
            {
                "protocolVersion": self.config.get("legacy_protocol_version", LEGACY_VERSION),
                "capabilities": {},
                "clientInfo": {"name": "yasc-harness", "version": "1.0.0"},
            },
        )
        if "error" in payload:
            raise RuntimeError(f"MCP initialize error: {payload['error']}")
        result = payload.get("result", {})
        self.protocol_version = result.get("protocolVersion", self.config.get("legacy_protocol_version", LEGACY_VERSION))
        self.wire.request_payload("notifications/initialized", notification=True)
        self._initialized = True
        return result

    def _modern_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        version = self.protocol_version or self.preferred_version
        payload = self.wire.request_payload(method, _modern_params(params, version))
        if "error" in payload:
            raise RuntimeError(f"MCP error: {payload['error']}")
        return payload.get("result", {})

    def _legacy_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._legacy_initialize()
        payload = self.wire.request_payload(method, params or {})
        if "error" in payload:
            raise RuntimeError(f"MCP error: {payload['error']}")
        return payload.get("result", {})

    def initialize(self) -> dict[str, Any]:
        if self.era == "modern":
            if self.discover_result is None:
                self.discover_result = self._modern_request("server/discover", {})
                selected = _select_modern_version(self.discover_result, self.preferred_version)
                if selected:
                    self.protocol_version = selected
            return {
                "era": "modern",
                "protocolVersion": self.protocol_version or self.preferred_version,
                "discover": self.discover_result or {},
            }
        return self._legacy_initialize()

    def list_tools(self) -> list[dict[str, Any]]:
        result = self._modern_request("tools/list", {}) if self.era == "modern" else self._legacy_request("tools/list", {})
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        params = {"name": name, "arguments": arguments}
        return self._modern_request("tools/call", params) if self.era == "modern" else self._legacy_request("tools/call", params)

    def close(self) -> None:
        self.wire.close()


class HTTPMCPAdapter:
    name = "mcp-http"

    def __init__(self, config: dict[str, Any]):
        self.config = expand_env(config)
        self.rpc = _JSONRPC()
        self.session = requests.Session()
        self.url = self.config["url"]
        self.timeout = float(self.config.get("timeout_seconds", 30))
        self.verify_tls = bool(self.config.get("verify_tls", True))
        self.mode = self.config.get("mode", "auto")
        self.preferred_version = self.config.get("protocol_version", MODERN_VERSION)
        self.session.headers.update({
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            **self.config.get("headers", {}),
        })
        self.session_id: str | None = None
        self.era: str | None = None
        self.protocol_version: str | None = None
        self.discover_result: dict[str, Any] | None = None
        self._initialized = False
        if self.mode in {"modern", MODERN_VERSION}:
            self.era = "modern"
            self.protocol_version = self.preferred_version
        elif self.mode == "legacy":
            self.era = "legacy"
        elif self.mode == "auto":
            self._probe()
        else:
            raise ValueError("mcp mode must be auto, modern, legacy, or 2026-07-28")

    def _decode_response(self, response: requests.Response, req_id: int | None) -> dict[str, Any]:
        ctype = response.headers.get("content-type", "")
        if "text/event-stream" in ctype:
            payload = None
            for line in response.text.splitlines():
                if line.startswith("data:"):
                    candidate = json.loads(line[5:].strip())
                    if req_id is None or candidate.get("id") == req_id:
                        payload = candidate
                        break
            if payload is None:
                raise RuntimeError("MCP SSE response did not contain matching JSON-RPC result")
            return payload
        try:
            return response.json()
        except ValueError as exc:
            raise RuntimeError(f"MCP endpoint returned non-JSON response ({response.status_code})") from exc

    def _request_payload(self, method: str, params: dict[str, Any] | None = None, *, modern: bool, notification: bool = False) -> dict[str, Any]:
        msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        version = self.protocol_version or self.preferred_version
        if params is not None:
            msg["params"] = _modern_params(params, version) if modern else params
        elif modern:
            msg["params"] = _modern_params({}, version)
        req_id = None if notification else self.rpc.next()
        if req_id is not None:
            msg["id"] = req_id
        headers: dict[str, str] = {}
        if modern:
            headers["MCP-Protocol-Version"] = version
            headers["Mcp-Method"] = method
            if method == "tools/call" and isinstance(params, dict) and params.get("name"):
                headers["Mcp-Name"] = str(params["name"])
        elif self.session_id:
            headers["Mcp-Session-Id"] = self.session_id

        response = self.session.post(self.url, json=msg, headers=headers, timeout=self.timeout, verify=self.verify_tls)
        if response.headers.get("Mcp-Session-Id") and not modern:
            self.session_id = response.headers["Mcp-Session-Id"]
        # Notifications commonly return 202/204 with an empty body.
        if notification and 200 <= response.status_code < 300 and not response.content:
            return {"jsonrpc": "2.0", "result": {}}
        # Preserve JSON-RPC errors even when a server maps them to 4xx.
        if response.status_code >= 400 and response.status_code not in {400, 404, 405}:
            response.raise_for_status()
        payload = self._decode_response(response, req_id)
        if response.status_code >= 400 and "error" not in payload:
            response.raise_for_status()
        return payload

    def _probe(self) -> None:
        payload = self._request_payload("server/discover", {}, modern=True)
        if "result" in payload:
            selected = _select_modern_version(payload["result"], self.preferred_version)
            if selected:
                self.era = "modern"
                self.protocol_version = selected
                self.discover_result = payload["result"]
                return
        if _is_method_not_found(payload):
            self.era = "legacy"
            return
        if "error" in payload:
            raise RuntimeError(f"MCP discovery error: {payload['error']}")
        raise RuntimeError("MCP discovery returned no compatible modern version")

    def _legacy_initialize(self) -> dict[str, Any]:
        if self._initialized:
            return {"already_initialized": True, "protocolVersion": self.protocol_version}
        payload = self._request_payload(
            "initialize",
            {
                "protocolVersion": self.config.get("legacy_protocol_version", LEGACY_VERSION),
                "capabilities": {},
                "clientInfo": {"name": "yasc-harness", "version": "1.0.0"},
            },
            modern=False,
        )
        if "error" in payload:
            raise RuntimeError(f"MCP initialize error: {payload['error']}")
        result = payload.get("result", {})
        self.protocol_version = result.get("protocolVersion", self.config.get("legacy_protocol_version", LEGACY_VERSION))
        self._request_payload("notifications/initialized", {}, modern=False, notification=True)
        self._initialized = True
        return result

    def _modern_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = self._request_payload(method, params, modern=True)
        if "error" in payload:
            raise RuntimeError(f"MCP error: {payload['error']}")
        return payload.get("result", {})

    def _legacy_request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._legacy_initialize()
        payload = self._request_payload(method, params or {}, modern=False)
        if "error" in payload:
            raise RuntimeError(f"MCP error: {payload['error']}")
        return payload.get("result", {})

    def initialize(self) -> dict[str, Any]:
        if self.era == "modern":
            if self.discover_result is None:
                self.discover_result = self._modern_request("server/discover", {})
                selected = _select_modern_version(self.discover_result, self.preferred_version)
                if selected:
                    self.protocol_version = selected
            return {
                "era": "modern",
                "protocolVersion": self.protocol_version or self.preferred_version,
                "discover": self.discover_result or {},
            }
        return self._legacy_initialize()

    def list_tools(self) -> list[dict[str, Any]]:
        result = self._modern_request("tools/list", {}) if self.era == "modern" else self._legacy_request("tools/list", {})
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        params = {"name": name, "arguments": arguments}
        return self._modern_request("tools/call", params) if self.era == "modern" else self._legacy_request("tools/call", params)

    def close(self) -> None:
        self.session.close()


def make_mcp_adapter(config: dict[str, Any]) -> MCPAdapter:
    typ = config.get("type")
    if typ == "mcp-stdio":
        return StdioMCPAdapter(config)
    if typ == "mcp-http":
        return HTTPMCPAdapter(config)
    raise ValueError(f"unsupported MCP adapter type: {typ}")
