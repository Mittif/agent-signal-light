#!/usr/bin/env python3
"""Agent Signal Light daemon.

Drives a browser mirror + a CH552 USB HID device based on a user-editable
config that maps Claude Code and Codex hook events to light effects.

Config file: ~/.agent-signal-light/config.json (auto-created from project default).
Auto-start: registered by install.py (LaunchAgent / Startup VBS / systemd user unit).

API
---
POST /hook                  ← Agent hooks pipe their stdin JSON here
POST /event                 ← manual test (G/Y/W/R/O legacy; mapped via builtin effects)
GET  /                      ← browser mirror UI
GET  /stream                ← SSE: effect_id, current frame LEDs, hid status, sessions
GET  /api/config            ← current config
POST /api/config            ← save new config (validates + reloads)
POST /api/config/reset      ← restore factory defaults
"""
from __future__ import annotations

import json
import os
import queue
import sys
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# ============================================================
# Paths & constants
# ============================================================

PORT = 7878
HID_VID, HID_PID = 0x1209, 0xC552
APP_NAME = "Agent Signal Light"
APP_SLUG = "agent-signal-light"

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path.home() / f".{APP_SLUG}"
CONFIG_PATH = DATA_DIR / "config.json"
DEFAULT_CONFIG_PATH = PROJECT_DIR / "config.default.json"

# LED modes (match firmware encoding: bit-packed 0/1/2 per LED in HID byte)
LED_MODES = {"off": 0, "on": 1, "breathe": 2}
LED_MODE_NAMES = {v: k for k, v in LED_MODES.items()}

# Legacy single-letter input → built-in effect (manual test buttons).
LEGACY_BYTE_TO_EFFECT = {
    "G": "idle_green",
    "Y": "working_yellow",
    "W": "wait_user",
    "R": "error_red",
    "O": "off",
}

CODEX_ONLY_EVENTS = {"PermissionRequest", "PreCompact", "PostCompact", "SubagentStart", "SubagentStop"}
CLAUDE_ONLY_EVENTS = {"Elicitation", "StopFailure"}
AGENT_SCOPES = ("all", "claude", "codex")
AGENT_PREFIXES = ("claude/", "codex/")


def _base_event_key(event: str) -> str:
    for prefix in AGENT_PREFIXES:
        if event.startswith(prefix):
            return event[len(prefix):]
    return event


def _agent_from_event_key(event: str) -> str | None:
    for prefix in AGENT_PREFIXES:
        if event.startswith(prefix):
            return prefix[:-1]
    return None


# ============================================================
# HID output (optional)
# ============================================================

_hid_lock = threading.Lock()
_hid_dev = None
_hid_status = "uninitialized"
_ack_active = False       # set during the one-shot connection-ack animation
ACK_DURATION_S = 2.4      # one full breath cycle matches the firmware's ~2.4 s period


def _hid_try_open() -> None:
    global _hid_dev, _hid_status
    try:
        import hid  # type: ignore
    except ImportError:
        _hid_status = "hidapi not installed"
        return
    try:
        d = hid.device()
        d.open(HID_VID, HID_PID)
        _hid_dev = d
        _hid_status = f"connected {HID_VID:#06x}:{HID_PID:#06x}"
    except OSError as e:
        _hid_status = f"device not found ({e.__class__.__name__})"


def _hid_write_raw(leds: list[int]) -> None:
    """Write LED bytes directly, bypassing the ack guard. Used by the connection
    ack animation. Returns silently on missing device or transient errors."""
    global _hid_dev, _hid_status
    byte = (leds[0] & 0x3) | ((leds[1] & 0x3) << 2) | ((leds[2] & 0x3) << 4)
    with _hid_lock:
        if _hid_dev is None:
            return
        try:
            _hid_dev.write([0x00, byte])
        except OSError as e:
            try:
                _hid_dev.close()
            except Exception:
                pass
            _hid_dev = None
            _hid_status = f"write failed ({e.__class__.__name__})"


def hid_send(leds: list[int]) -> None:
    """Public scheduler entry: writes LEDs unless an ack animation owns
    the hardware. Never tries to open — that's the health loop's job."""
    if _ack_active:
        return
    _hid_write_raw(leds)


def _fire_connection_ack() -> None:
    """One-shot 'red breathes once' animation to confirm a freshly-connected
    device. Suspends scheduler writes for the duration, drives the hardware
    directly, and tells the browser to override its preview to match."""
    global _ack_active
    _ack_active = True
    try:
        # Browser: render the red breath in the preview for the same duration.
        _broadcast(json.dumps({"ack": "connect", "ms": int(ACK_DURATION_S * 1000)},
                              separators=(",", ":")))
        # Hardware: red = breathe (LED2). LED0=off, LED1=off.
        _hid_write_raw([0, 0, 2])
        time.sleep(ACK_DURATION_S)
        _hid_write_raw([0, 0, 0])
    finally:
        _ack_active = False
    # Resume normal display: re-emit so both surfaces sync to current effect.
    try:
        _emit_snapshot(scheduler.target_id, scheduler.leds)
    except Exception:
        pass


def _hid_health_loop() -> None:
    """Poll hidapi every ~2s: detect plug/unplug, (re)open on plug,
    close + mark disconnected on unplug, push a snapshot on every transition,
    and fire a one-shot connection-ack animation when going disconnected → connected."""
    global _hid_dev, _hid_status
    try:
        import hid  # type: ignore
    except ImportError:
        print("  hid-health: hidapi unavailable, loop exiting", flush=True)
        return
    tick = 0
    last_logged = None
    was_connected = False
    while True:
        time.sleep(2)
        tick += 1
        try:
            devs = list(hid.enumerate())
            present = any(
                d.get("vendor_id") == HID_VID and d.get("product_id") == HID_PID
                for d in devs
            )
        except Exception as e:
            print(f"  hid-health: enumerate failed: {e!r}", flush=True)
            continue
        with _hid_lock:
            old = _hid_status
            has_handle = _hid_dev is not None
            if present and not has_handle:
                try:
                    d = hid.device()
                    d.open(HID_VID, HID_PID)
                    _hid_dev = d
                    _hid_status = f"connected {HID_VID:#06x}:{HID_PID:#06x}"
                except OSError as e:
                    _hid_status = f"present but cannot open ({e.__class__.__name__})"
            elif not present:
                if has_handle:
                    try:
                        _hid_dev.close()
                    except Exception:
                        pass
                    _hid_dev = None
                _hid_status = "disconnected"
            changed = old != _hid_status
            is_connected = _hid_status.startswith("connected")
        if changed or tick % 5 == 0 or last_logged != _hid_status:
            print(f"  hid-health[#{tick}]: present={present} status={_hid_status!r}", flush=True)
            last_logged = _hid_status
        if changed:
            try:
                _emit_snapshot(scheduler.target_id, scheduler.leds)
            except Exception as e:
                print(f"  hid-health: emit failed: {e!r}", flush=True)
        # Disconnect → connect transition: greet the user.
        if is_connected and not was_connected:
            print("  hid-health: connection ack (red breath once)", flush=True)
            try:
                _fire_connection_ack()
            except Exception as e:
                print(f"  hid-health: ack failed: {e!r}", flush=True)
        was_connected = is_connected


# ============================================================
# Config: effects, event bindings, event priority
# ============================================================

@dataclass
class Frame:
    leds: list[int]            # 3 ints from LED_MODES
    ms: int | None             # None = hold until state change

    def to_dict(self) -> dict:
        return {
            "leds": [LED_MODE_NAMES[v] for v in self.leds],
            "ms": self.ms,
        }


@dataclass
class Effect:
    id: str
    name: str
    builtin: bool
    frames: list[Frame] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "builtin": self.builtin,
            "frames": [f.to_dict() for f in self.frames],
        }


def _parse_leds(arr) -> list[int]:
    if not isinstance(arr, list) or len(arr) != 3:
        raise ValueError(f"leds must be a 3-element list, got {arr!r}")
    out = []
    for v in arr:
        if isinstance(v, str):
            if v not in LED_MODES:
                raise ValueError(f"bad LED mode {v!r}")
            out.append(LED_MODES[v])
        elif isinstance(v, int) and v in LED_MODE_NAMES:
            out.append(v)
        else:
            raise ValueError(f"bad LED mode {v!r}")
    return out


class Config:
    """Loads / validates / saves the user config; thread-safe accessors."""

    CONFIG_VERSION = 3
    SESSION_TTL_S = 3600
    OFF_EFFECT_ID = "off"

    def __init__(self):
        self._lock = threading.Lock()
        self._effects: dict[str, Effect] = {}
        self._event_bindings: dict[str, str] = {}
        self._event_priority: list[str] = []
        self._agent_priority: dict[str, list[str]] = {}
        self._priority_idx: dict[str, int] = {}
        self._agent_priority_idx: dict[str, dict[str, int]] = {}
        self._listeners: list = []
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.load()

    # ---------- file IO ----------
    def load(self) -> None:
        if not CONFIG_PATH.exists():
            self._copy_defaults_to_user()
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        data, changed = self._migrate_user_config(data)
        if changed:
            self._write_config(data)
        self._apply(data)

    def _copy_defaults_to_user(self) -> None:
        with open(DEFAULT_CONFIG_PATH) as f:
            CONFIG_PATH.write_text(f.read())

    def _write_config(self, data: dict) -> None:
        tmp = CONFIG_PATH.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        tmp.replace(CONFIG_PATH)

    def _migrate_user_config(self, data: dict) -> tuple[dict, bool]:
        """Non-destructively add new built-in effects/events from defaults."""
        changed = False
        try:
            with open(DEFAULT_CONFIG_PATH) as f:
                defaults = json.load(f)
        except Exception:
            return data, False

        data.setdefault("version", defaults.get("version", 1))

        effect_ids = {e.get("id") for e in data.get("effects", []) if isinstance(e, dict)}
        for effect in defaults.get("effects", []):
            if effect.get("id") not in effect_ids:
                data.setdefault("effects", []).append(effect)
                changed = True

        bindings = data.setdefault("event_bindings", {})
        for event, effect_id in defaults.get("event_bindings", {}).items():
            if event not in bindings:
                bindings[event] = effect_id
                changed = True

        priority = data.setdefault("event_priority", [])
        for event in defaults.get("event_priority", []):
            if event not in priority:
                priority.append(event)
                changed = True

        agent_priority = data.setdefault("agent_priority", {})
        default_agent_priority = defaults.get("agent_priority", {})
        base_priority = list(data.get("event_priority") or defaults.get("event_priority", []))
        for scope in ("claude", "codex"):
            default_list = base_priority or default_agent_priority.get(scope) or defaults.get("event_priority", [])
            if scope not in agent_priority or not isinstance(agent_priority.get(scope), list):
                agent_priority[scope] = list(default_list)
                changed = True
            else:
                for event in default_list:
                    if event not in agent_priority[scope]:
                        agent_priority[scope].append(event)
                        changed = True

        default_version = defaults.get("version")
        if default_version is not None and data.get("version") != default_version:
            data["version"] = default_version
            changed = True

        return data, changed

    def reset_to_defaults(self) -> None:
        self._copy_defaults_to_user()
        self.load()
        self._fire_change()

    def save(self, data: dict) -> tuple[bool, str]:
        """Validate, write, reload. Returns (ok, message)."""
        try:
            self._validate(data)
        except (ValueError, KeyError, TypeError) as e:
            return False, str(e)
        # preserve builtin flag from defaults — users can add custom but not flip builtin
        with open(DEFAULT_CONFIG_PATH) as f:
            defaults = json.load(f)
        builtin_ids = {e["id"] for e in defaults["effects"] if e.get("builtin")}
        for e in data["effects"]:
            e["builtin"] = e["id"] in builtin_ids
        agent_priority = data.setdefault("agent_priority", {})
        for scope in ("claude", "codex"):
            events = agent_priority.get(scope)
            if not isinstance(events, list):
                agent_priority[scope] = list(data["event_priority"])
            else:
                agent_priority[scope] = [_base_event_key(ev) for ev in events]
        data["version"] = self.CONFIG_VERSION
        self._write_config(data)
        self._apply(data)
        self._fire_change()
        return True, "saved"

    # ---------- validation ----------
    def _validate(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("config must be a JSON object")
        if "effects" not in data or "event_bindings" not in data or "event_priority" not in data:
            raise ValueError("missing required keys: effects / event_bindings / event_priority")
        effect_ids = set()
        for e in data["effects"]:
            if not isinstance(e, dict) or not isinstance(e.get("id"), str) or not e["id"]:
                raise ValueError("effect must have a non-empty id")
            if e["id"] in effect_ids:
                raise ValueError(f"duplicate effect id {e['id']!r}")
            effect_ids.add(e["id"])
            if not isinstance(e.get("frames"), list) or not e["frames"]:
                raise ValueError(f"effect {e['id']!r} must have at least one frame")
            for f in e["frames"]:
                _parse_leds(f.get("leds"))
                ms = f.get("ms")
                if ms is not None and (not isinstance(ms, int) or ms < 10 or ms > 60_000):
                    raise ValueError(f"effect {e['id']!r}: ms must be null or 10..60000")
        for ev, eid in data["event_bindings"].items():
            if eid not in effect_ids:
                raise ValueError(f"event {ev!r} bound to unknown effect {eid!r}")
        for ev in data["event_priority"]:
            if ev not in data["event_bindings"]:
                raise ValueError(f"event {ev!r} in priority list has no binding")
        agent_priority = data.get("agent_priority", {})
        if agent_priority is not None and not isinstance(agent_priority, dict):
            raise ValueError("agent_priority must be an object")
        if isinstance(agent_priority, dict):
            base_bindings = {_base_event_key(ev) for ev in data["event_bindings"]}
            for scope, events in agent_priority.items():
                if scope not in ("claude", "codex"):
                    raise ValueError(f"unsupported agent_priority scope {scope!r}")
                if not isinstance(events, list):
                    raise ValueError(f"agent_priority.{scope} must be a list")
                seen = set()
                for ev in events:
                    if not isinstance(ev, str) or not ev:
                        raise ValueError(f"agent_priority.{scope} contains invalid event {ev!r}")
                    base = _base_event_key(ev)
                    if base in seen:
                        raise ValueError(f"agent_priority.{scope} has duplicate event {base!r}")
                    seen.add(base)
                    if base not in base_bindings:
                        raise ValueError(f"agent_priority.{scope} event {base!r} has no binding")

    # ---------- apply parsed config ----------
    def _apply(self, data: dict) -> None:
        with self._lock:
            self._effects = {}
            for e in data["effects"]:
                frames = [Frame(_parse_leds(f["leds"]), f.get("ms")) for f in e["frames"]]
                self._effects[e["id"]] = Effect(e["id"], e.get("name", e["id"]),
                                                bool(e.get("builtin")), frames)
            self._event_bindings = dict(data["event_bindings"])
            self._event_priority = list(data["event_priority"])
            agent_priority = data.get("agent_priority") or {}
            self._agent_priority = {
                scope: [_base_event_key(ev) for ev in agent_priority.get(scope, self._event_priority)]
                for scope in ("claude", "codex")
            }
            self._priority_idx = {ev: i for i, ev in enumerate(self._event_priority)}
            self._agent_priority_idx = {
                scope: {ev: i for i, ev in enumerate(events)}
                for scope, events in self._agent_priority.items()
            }

    # ---------- accessors ----------
    def get_effect(self, effect_id: str) -> Effect | None:
        with self._lock:
            return self._effects.get(effect_id)

    def effect_for_event(self, event: str) -> str | None:
        with self._lock:
            return self._event_bindings.get(event)

    def priority_index(self, event: str, agent: str = "unknown") -> int:
        """Lower index = higher priority. Unknown events sort last."""
        with self._lock:
            base = _base_event_key(event)
            scope = agent if agent in ("claude", "codex") else _agent_from_event_key(event)
            if scope in ("claude", "codex"):
                scoped = self._agent_priority_idx.get(scope, {}).get(base)
                if scoped is not None:
                    return scoped
            exact = self._priority_idx.get(event)
            if exact is not None:
                return exact
            if base != event:
                return self._priority_idx.get(base, 10**9)
            return 10**9

    def to_dict(self) -> dict:
        with self._lock:
            return {
                "version": self.CONFIG_VERSION,
                "effects": [e.to_dict() for e in self._effects.values()],
                "event_bindings": dict(self._event_bindings),
                "event_priority": list(self._event_priority),
                "agent_priority": {scope: list(events) for scope, events in self._agent_priority.items()},
            }

    # ---------- change notification ----------
    def on_change(self, fn) -> None:
        self._listeners.append(fn)

    def _fire_change(self) -> None:
        for fn in list(self._listeners):
            try:
                fn()
            except Exception as e:
                print(f"  ! config listener error: {e}", flush=True)


# ============================================================
# Sessions: per-session_id event tracking
# ============================================================

class Sessions:
    # Events that mean "session has nothing demanding the user's attention" —
    # once a session is in one of these and stays quiet, an incoming Notification
    # that arrives more than IDLE_NOTIFICATION_GRACE_S later is almost certainly
    # a stray idle_prompt (or similar nudge) that the matcher should have caught.
    # We drop it so the light stays in the quiet state instead of flipping to W.
    QUIET_EVENTS = {"Stop", "StopFailure", "SessionStart"}
    IDLE_NOTIFICATION_GRACE_S = 1.0

    def __init__(self, config: Config, on_change):
        self._lock = threading.Lock()
        self._map: dict[str, dict] = {}
        self._cfg = config
        self._on_change = on_change
        threading.Thread(target=self._sweep, daemon=True, name="sessions-sweep").start()

    def update(self, sid: str, event: str, cwd: str | None, agent: str = "unknown") -> None:
        dropped: tuple[str, float] | None = None
        with self._lock:
            entry = self._map.get(sid) or {}
            prev_event = entry.get("event")
            prev_at = entry.get("last_seen", 0.0)
            now = time.time()
            elapsed = now - prev_at

            if (event == "Notification"
                    and prev_event in self.QUIET_EVENTS
                    and elapsed > self.IDLE_NOTIFICATION_GRACE_S):
                dropped = (prev_event, elapsed)
            else:
                entry["event"] = event
                entry["last_seen"] = now
                if cwd is not None:
                    entry["cwd"] = cwd
                elif "cwd" not in entry:
                    entry["cwd"] = None
                entry["agent"] = agent or "unknown"
                self._map[sid] = entry

        if dropped is not None:
            prev, secs = dropped
            print(f"  ↯ dropped late Notification on {sid[:8]} "
                  f"(was {prev} for {secs:.1f}s)", flush=True)
            return
        self._on_change()

    def remove(self, sid: str) -> bool:
        with self._lock:
            existed = sid in self._map
            self._map.pop(sid, None)
        if existed:
            self._on_change()
        return existed

    def _winner(self, agent_filter: str = "all") -> dict | None:
        with self._lock:
            entries = list(self._map.values())
        if agent_filter in ("claude", "codex"):
            entries = [e for e in entries if e.get("agent") == agent_filter]
        if not entries:
            return None
        return min(entries, key=lambda e: self._cfg.priority_index(e["event"], e.get("agent") or "unknown"))

    def aggregate_effect_id(self, agent_filter: str = "all") -> str:
        """Return the effect_id of the session with highest-priority event."""
        winner = self._winner(agent_filter)
        if winner is None:
            return Config.OFF_EFFECT_ID
        eid = self._cfg.effect_for_event(winner["event"])
        return eid or Config.OFF_EFFECT_ID

    def aggregate_agent(self, agent_filter: str = "all") -> str:
        """Return the agent source of the session currently controlling the light."""
        winner = self._winner(agent_filter)
        if winner is None:
            return "none"
        return winner.get("agent") or "unknown"

    def snapshot(self) -> list[dict]:
        with self._lock:
            return [
                {
                    "sid": sid,
                    "event": e["event"],
                    "effect_id": self._cfg.effect_for_event(e["event"]) or Config.OFF_EFFECT_ID,
                    "agent": e.get("agent") or "unknown",
                    "cwd": e.get("cwd"),
                    "age_s": int(time.time() - e["last_seen"]),
                }
                for sid, e in sorted(self._map.items())
            ]

    def _sweep(self) -> None:
        while True:
            time.sleep(30)
            cutoff = time.time() - Config.SESSION_TTL_S
            changed = False
            with self._lock:
                stale = [sid for sid, e in self._map.items() if e["last_seen"] < cutoff]
                for sid in stale:
                    del self._map[sid]
                    changed = True
            if changed:
                self._on_change()


# ============================================================
# Scheduler: plays the current effect's frames in a loop
# ============================================================

class Scheduler:
    def __init__(self, config: Config, on_change):
        self._lock = threading.Lock()
        self._target_id = Config.OFF_EFFECT_ID
        self._leds = [0, 0, 0]
        self._wake = threading.Event()
        self._cfg = config
        self._on_change = on_change
        threading.Thread(target=self._run, daemon=True, name="scheduler").start()

    @property
    def target_id(self) -> str:
        return self._target_id

    @property
    def leds(self) -> list[int]:
        return list(self._leds)

    def set_effect(self, effect_id: str) -> None:
        with self._lock:
            if effect_id == self._target_id:
                return
            self._target_id = effect_id
        self._wake.set()

    def _emit(self, leds: list[int]) -> None:
        if leds != self._leds:
            self._leds = list(leds)
            self._on_change(self._target_id, self._leds)

    def _wait(self, seconds: float | None) -> bool:
        return self._wake.wait(seconds)

    def _run(self) -> None:
        # Initial emit so SSE has something to show on first connect.
        self._on_change(self._target_id, self._leds)
        while True:
            with self._lock:
                eid = self._target_id
            self._wake.clear()
            effect = self._cfg.get_effect(eid)
            if effect is None:
                self._emit([0, 0, 0])
                self._wait(None)
                continue
            self._play_loop(effect)

    def _play_loop(self, effect: Effect) -> None:
        """Iterate frames, looping back after the last. Returns on target change."""
        while True:
            for frame in effect.frames:
                with self._lock:
                    if self._target_id != effect.id:
                        return
                self._emit(frame.leds)
                self._wake.clear()
                if frame.ms is None:
                    self._wait(None)
                    return
                if self._wait(frame.ms / 1000.0):
                    return


# ============================================================
# Wiring + SSE broadcast
# ============================================================

_clients_lock = threading.Lock()
_clients: list[queue.Queue] = []
_agent_filter_lock = threading.Lock()
_agent_filter = "all"


def get_agent_filter() -> str:
    with _agent_filter_lock:
        return _agent_filter


def set_agent_filter(scope: str) -> bool:
    global _agent_filter
    if scope not in AGENT_SCOPES:
        return False
    with _agent_filter_lock:
        changed = scope != _agent_filter
        _agent_filter = scope
    if changed:
        _on_sessions_change()
    return True


def _broadcast(payload: str) -> None:
    with _clients_lock:
        targets = list(_clients)
    for q in targets:
        try:
            q.put_nowait(payload)
        except queue.Full:
            pass


def _snapshot_json(effect_id: str, leds: list[int]) -> str:
    eff = config.get_effect(effect_id)
    agent_filter = get_agent_filter()
    return json.dumps(
        {
            "effect_id": effect_id,
            "effect_name": eff.name if eff else effect_id,
            "agent": sessions.aggregate_agent(agent_filter),
            "agent_filter": agent_filter,
            "l": leds,
            "hid": _hid_status,
            "sessions": sessions.snapshot(),
        },
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _emit_snapshot(effect_id: str, leds: list[int]) -> None:
    hid_send(leds)
    _broadcast(_snapshot_json(effect_id, leds))


def _on_sessions_change() -> None:
    eid = sessions.aggregate_effect_id(get_agent_filter())
    scheduler.set_effect(eid)
    _emit_snapshot(scheduler.target_id, scheduler.leds)


def _on_config_change() -> None:
    # Config changed → re-aggregate (event→effect mapping may have shifted) and re-emit.
    _on_sessions_change()


config = Config()
sessions = Sessions(config, on_change=_on_sessions_change)
scheduler = Scheduler(config, on_change=_emit_snapshot)
config.on_change(_on_config_change)

threading.Thread(target=_hid_health_loop, daemon=True, name="hid-health").start()


# ============================================================
# HTTP / SSE
# ============================================================

MANUAL_SID = "__manual__"


ALLOWED_HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}", "127.0.0.1", "localhost"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): return

    def _path(self) -> str:
        return urlparse(self.path).path

    def _host_ok(self) -> bool:
        # Defends against DNS-rebinding: a malicious page can't spoof the Host header,
        # so we accept only loopback names. Without this, a rebound DNS name could
        # POST to /api/config or read /stream from off-host JavaScript.
        host = (self.headers.get("Host") or "").strip().lower()
        return host in ALLOWED_HOSTS

    def _send(self, code: int, body: bytes = b"", ctype: str = "text/plain") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _send_json(self, code: int, obj) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._send(code, body, "application/json; charset=utf-8")

    def do_GET(self):
        if not self._host_ok():
            self._send(403, b"forbidden host")
            return
        path = self._path()
        if path == "/":
            self._send(200, INDEX_HTML.encode(), "text/html; charset=utf-8")
        elif path == "/stream":
            self._stream()
        elif path == "/api/config":
            self._send_json(200, config.to_dict())
        elif path == "/api/status":
            agent_filter = get_agent_filter()
            self._send_json(200, {
                "hid": _hid_status,
                "effect_id": scheduler.target_id,
                "agent": sessions.aggregate_agent(agent_filter),
                "agent_filter": agent_filter,
                "leds": scheduler.leds,
                "sessions": sessions.snapshot(),
            })
        else:
            self._send(404, b"not found")

    def do_POST(self):
        if not self._host_ok():
            self._send(403, b"forbidden host")
            return
        path = self._path()
        if path == "/event":
            self._do_event()
        elif path == "/hook":
            self._do_hook()
        elif path == "/api/config":
            self._do_save_config()
        elif path == "/api/config/reset":
            config.reset_to_defaults()
            self._send_json(200, {"ok": True, "config": config.to_dict()})
        elif path == "/api/agent-filter":
            self._do_agent_filter()
        else:
            self._send(404, b"not found")

    # ---------- /event (manual) ----------
    def _do_event(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(n).decode("utf-8", "ignore").strip()
        ch = raw[:1].upper()
        if ch not in LEGACY_BYTE_TO_EFFECT:
            self._send(400, f"bad state: {raw!r}".encode())
            return
        effect_id = LEGACY_BYTE_TO_EFFECT[ch]
        print(f"  ← {ch} (manual → {effect_id})", flush=True)
        if effect_id == "off":
            sessions.remove(MANUAL_SID)
        else:
            # Map legacy byte to a synthetic event so it shows in the sessions list
            # and participates in aggregation according to the same rules.
            synth_event = f"_manual_{ch}"
            # Ensure aggregation works: bind to this effect on the fly via a synthetic
            # event_priority hack — we just inject the manual session and aggregate
            # picks it up because its effect_id wins by being the only entry, OR by
            # natural priority if there are real sessions. To stay simple, we just
            # store the event name and rely on the binding lookup; but synthetic
            # event has no binding, so we sidestep by using a real event from the
            # built-in mapping that matches the effect.
            #
            # Pragmatic: hard-pin the manual session's effect via direct override on
            # scheduler. Sessions list still shows it for UI debug.
            for ev, eid in config._event_bindings.items():
                if eid == effect_id:
                    synth_event = ev
                    break
            sessions.update(MANUAL_SID, synth_event, cwd="(manual)", agent="manual")
        self._send(204)

    # ---------- /hook (agent hook event) ----------
    def _agent_source(self, data: dict, event: str) -> str:
        qs = parse_qs(urlparse(self.path).query)
        candidates = [
            qs.get("agent", [""])[0],
            qs.get("source", [""])[0],
            data.get("agent_signal_source"),
            data.get("agent"),
            data.get("client"),
            data.get("app"),
            data.get("source_agent"),
        ]
        for raw in candidates:
            text = str(raw or "").strip().lower()
            if "codex" in text:
                return "codex"
            if "claude" in text:
                return "claude"

        if event in CODEX_ONLY_EVENTS:
            return "codex"
        if event in CLAUDE_ONLY_EVENTS:
            return "claude"
        if data.get("agent_type") is not None or data.get("trigger") is not None:
            return "codex"
        if data.get("transcript_path") is not None:
            return "claude"
        return "unknown"

    def _binding_key(self, data: dict, event: str, tool: str, agent: str) -> str | None:
        matcher_value = ""
        if event in ("PreToolUse", "PostToolUse", "PermissionRequest"):
            matcher_value = tool
        elif event in ("SubagentStart", "SubagentStop"):
            matcher_value = (data.get("agent_type") or "").strip()
        elif event == "SessionStart":
            matcher_value = (data.get("source") or "").strip()
        elif event in ("PreCompact", "PostCompact"):
            matcher_value = (data.get("trigger") or "").strip()

        candidates = []
        if matcher_value:
            if agent in ("claude", "codex"):
                candidates.append(f"{agent}/{event}:{matcher_value}")
            candidates.append(f"{event}:{matcher_value}")
        if agent in ("claude", "codex"):
            candidates.append(f"{agent}/{event}")
        candidates.append(event)

        for key in candidates:
            if config.effect_for_event(key) is not None:
                return key
        return None

    def _do_hook(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        if n <= 0 or n > 256 * 1024:
            self._send(400, b"missing/oversize body")
            return
        raw = self.rfile.read(n)
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            self._send(400, b"bad json")
            return
        sid = (data.get("session_id") or "").strip()
        event = (data.get("hook_event_name") or "").strip()
        tool = (data.get("tool_name") or "").strip()
        cwd = data.get("cwd")
        agent = self._agent_source(data, event)
        if not sid or not event:
            self._send(400, b"missing session_id or hook_event_name")
            return
        if event == "SessionEnd":
            removed = sessions.remove(sid)
            print(f"  ← {event:<24} {sid[:8]} [{agent}] (removed={removed})", flush=True)
            self._send(204)
            return
        key = self._binding_key(data, event, tool, agent)
        # Drop events with no binding to avoid noise.
        if key is None:
            self._send(204)
            return
        sessions.update(sid, key, cwd=cwd, agent=agent)
        print(f"  ← {key:<32} {sid[:8]} [{agent}] "
              f"(agg={sessions.aggregate_effect_id(get_agent_filter())})", flush=True)
        self._send(204)

    # ---------- /api/agent-filter ----------
    def _do_agent_filter(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        scope = ""
        if n > 0:
            try:
                data = json.loads(self.rfile.read(n))
                scope = (data.get("scope") or data.get("agent_filter") or "").strip().lower()
            except (ValueError, UnicodeDecodeError):
                self._send_json(400, {"ok": False, "error": "bad json"})
                return
        if not scope:
            qs = parse_qs(urlparse(self.path).query)
            scope = (qs.get("scope", [""])[0] or qs.get("agent_filter", [""])[0]).strip().lower()
        if not set_agent_filter(scope):
            self._send_json(400, {"ok": False, "error": "scope must be all, claude, or codex"})
            return
        self._send_json(200, {"ok": True, "agent_filter": get_agent_filter()})

    # ---------- /api/config (save) ----------
    def _do_save_config(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        if n <= 0 or n > 1024 * 1024:
            self._send_json(400, {"ok": False, "error": "body required"})
            return
        try:
            data = json.loads(self.rfile.read(n))
        except (ValueError, UnicodeDecodeError) as e:
            self._send_json(400, {"ok": False, "error": f"bad json: {e}"})
            return
        ok, msg = config.save(data)
        if not ok:
            self._send_json(400, {"ok": False, "error": msg})
            return
        print(f"  ✓ config saved", flush=True)
        self._send_json(200, {"ok": True})

    # ---------- /stream (SSE) ----------
    def _stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        q: queue.Queue = queue.Queue(maxsize=64)
        with _clients_lock:
            _clients.append(q)
        try:
            self.wfile.write(b": connected\n\n")
            self.wfile.write(f"data: {_snapshot_json(scheduler.target_id, scheduler.leds)}\n\n".encode())
            self.wfile.flush()
            while True:
                try:
                    payload = q.get(timeout=15)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                    self.wfile.flush()
                    continue
                self.wfile.write(f"data: {payload}\n\n".encode())
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            with _clients_lock:
                if q in _clients:
                    _clients.remove(q)


# ============================================================
# Browser UI (Phase 1: minimal adaption to new payload shape;
# full effect/binding/priority editor is Phase 2)
# ============================================================

INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Agent Signal Light</title>
<style>
  :root {
    --bg: #141414; --fg: #e0e0e0; --dim: #888; --mute: #555;
    --panel: #1a1a1a; --panel2: #1f1f1f; --line: #2a2a2a; --line2: #333;
    --accent: #4a90e2; --ok: #21d65a; --warn: #ffb800; --err: #ff5555;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; background: var(--bg); color: var(--fg);
    font: 13px -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
  }
  h1, h2, h3 { margin: 0; font-weight: 600; }
  button {
    background: #232323; color: var(--fg); border: 1px solid var(--line2);
    padding: 6px 14px; border-radius: 6px; cursor: pointer;
    font: 12px ui-monospace, "SF Mono", monospace;
  }
  button:hover { background: #2c2c2c; }
  button:active { background: #1c1c1c; }
  button.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
  button.primary:hover { background: #5aa0f2; }
  button.danger { color: var(--err); border-color: #553030; }
  button:disabled { opacity: 0.4; cursor: not-allowed; }

  /* ----- Top app header ----- */
  .app-header {
    display: flex; align-items: center; gap: 24px; flex-wrap: wrap;
    padding: 14px 24px; border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, #1a1a1a, #161616);
  }
  .app-header h1 { font-size: 15px; letter-spacing: 0.5px; }
  .header-status {
    color: var(--dim); font: 11px ui-monospace, "SF Mono", monospace;
    display: flex; gap: 18px; flex-wrap: wrap;
  }
  .header-status .dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: var(--mute); vertical-align: middle; margin-right: 6px;
  }
  .header-status.ok .dot { background: var(--ok); box-shadow: 0 0 6px var(--ok); }

  /* ----- Action bar (visible when draft is dirty) ----- */
  .actions-bar {
    display: flex; justify-content: space-between; align-items: center;
    gap: 12px; padding: 10px 24px;
    background: #1e2937; border-bottom: 1px solid #2a3a52;
    color: #cfdbe8; font: 12px ui-monospace, "SF Mono", monospace;
  }
  .actions-bar.hidden { display: none; }
  .actions-bar .left { display: flex; align-items: center; gap: 10px; }
  .actions-bar .left::before {
    content: ''; width: 10px; height: 10px; border-radius: 50%;
    background: var(--warn); box-shadow: 0 0 6px var(--warn);
  }
  .actions-bar .right { display: flex; gap: 8px; }

  /* ----- Live preview housing ----- */
  .preview-wrap {
    display: flex; justify-content: center; padding: 22px 0 18px;
    border-bottom: 1px solid var(--line);
  }
  .housing {
    background: linear-gradient(180deg, #2a2a2a, #1c1c1c);
    border-radius: 24px; padding: 14px;
    display: flex; flex-direction: column; gap: 10px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
  }
  .led {
    width: 64px; height: 64px; border-radius: 50%;
    background: #0a0a0a; border: 2px solid #2a2a2a; position: relative;
  }
  .led::after {
    content: ''; position: absolute; inset: 3px; border-radius: 50%;
    background: var(--color); opacity: var(--i, 0);
    box-shadow: 0 0 calc(var(--i, 0) * 22px) calc(var(--i, 0) * 3px) var(--color);
  }
  .red    { --color: #ff3030; }
  .yellow { --color: #ffb800; }
  .green  { --color: #21d65a; }

  /* ----- Three columns ----- */
  .columns {
    display: grid;
    grid-template-columns: 280px 1fr 1fr;
    gap: 14px; padding: 16px 24px;
  }
  @media (max-width: 1000px) {
    .columns { grid-template-columns: 1fr; }
  }
  .col {
    background: var(--panel); border: 1px solid var(--line); border-radius: 8px;
    display: flex; flex-direction: column; min-height: 320px;
  }
  .col header {
    padding: 12px 14px; border-bottom: 1px solid var(--line);
    display: flex; justify-content: space-between; align-items: center;
  }
  .col header h2 { font-size: 12px; letter-spacing: 1px; color: var(--dim); text-transform: uppercase; }
  .col header .hint { font: 11px ui-monospace, "SF Mono", monospace; color: var(--mute); }
  .col .body { padding: 10px; display: flex; flex-direction: column; gap: 8px; flex: 1; }

  /* ----- Effect card (library item, draggable) ----- */
  .effect-card {
    background: var(--panel2); border: 1px solid var(--line2); border-radius: 6px;
    padding: 8px 10px; cursor: grab;
    display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: center;
    transition: transform 0.06s, border-color 0.12s;
  }
  .effect-card:hover { border-color: var(--accent); }
  .effect-card:active { cursor: grabbing; transform: scale(0.99); }
  .effect-card.dragging { opacity: 0.4; }
  .effect-card .name {
    font-size: 12px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
  }
  .effect-card .meta {
    font: 10px ui-monospace, "SF Mono", monospace; color: var(--mute); margin-top: 2px;
  }
  .effect-card .lock { font-size: 11px; color: var(--mute); }
  .effect-preview {
    display: flex; flex-direction: column; gap: 3px; align-items: center;
    padding: 4px 6px; background: #0c0c0c; border-radius: 4px;
  }
  .effect-preview .pdot {
    width: 9px; height: 9px; border-radius: 50%; background: var(--color);
  }

  /* ----- Binding row ----- */
  .binding-row {
    display: grid; grid-template-columns: minmax(180px, 1fr) auto minmax(160px, 1fr);
    gap: 10px; align-items: center;
    padding: 8px 10px; background: var(--panel2); border: 1px solid var(--line); border-radius: 6px;
  }
  .binding-row .ev { font: 12px ui-monospace, "SF Mono", monospace; color: var(--fg); }
  .binding-row .arrow { color: var(--mute); }
  .agent-switch {
    display: flex; overflow: hidden; border: 1px solid var(--line2); border-radius: 6px;
    background: #111;
  }
  .agent-switch button {
    border: 0; border-right: 1px solid var(--line2); border-radius: 0;
    background: transparent; color: var(--dim); padding: 4px 8px; min-width: 54px;
    font: 11px ui-monospace, "SF Mono", monospace;
  }
  .agent-switch button:last-child { border-right: 0; }
  .agent-switch button:hover { color: var(--fg); background: #242424; }
  .agent-switch button.active { background: var(--accent); color: #fff; }
  .binding-slot {
    min-height: 38px; padding: 4px; border-radius: 5px;
    border: 1.5px dashed var(--line2);
    display: flex; align-items: center; justify-content: center;
    color: var(--mute); font-size: 11px;
  }
  .binding-slot.has { border-style: solid; border-color: var(--line2); }
  .binding-slot.inherited { border-style: dashed; background: rgba(255,255,255,0.025); }
  .binding-slot.drop-hover { border-color: var(--accent); background: rgba(74, 144, 226, 0.06); color: var(--accent); }
  .binding-slot.has .effect-card {
    width: 100%; cursor: default; margin: 0;
  }
  .binding-slot.inherited .effect-card { opacity: 0.62; }
  .binding-slot .inherit {
    margin-left: 6px; color: var(--mute); font: 10px ui-monospace, "SF Mono", monospace;
  }
  .binding-slot .clear {
    margin-left: 6px; cursor: pointer; color: var(--mute); font-size: 13px;
  }
  .binding-slot .clear:hover { color: var(--err); }

  /* ----- Priority list ----- */
  .priority-row {
    display: grid; grid-template-columns: 24px 1fr auto; gap: 10px; align-items: center;
    padding: 8px 10px; background: var(--panel2); border: 1px solid var(--line); border-radius: 6px;
    cursor: grab;
  }
  .priority-row:active { cursor: grabbing; }
  .priority-row.dragging { opacity: 0.4; }
  .priority-row .handle { color: var(--mute); font-size: 16px; user-select: none; cursor: grab; }
  .priority-row .ev { font: 12px ui-monospace, "SF Mono", monospace; }
  .priority-row .pri { font: 10px ui-monospace, "SF Mono", monospace; color: var(--mute); }
  .priority-row.insert-before { box-shadow: 0 -2px 0 0 var(--accent); }
  .priority-row.insert-after  { box-shadow: 0 2px 0 0 var(--accent); }
  .priority-empty {
    color: var(--mute); padding: 12px; text-align: center; font: 11px ui-monospace, "SF Mono", monospace;
  }

  /* ----- Sessions debug ----- */
  .sessions-panel {
    margin: 4px 24px 24px; background: var(--panel); border: 1px solid var(--line);
    border-radius: 8px; font: 12px ui-monospace, "SF Mono", monospace;
  }
  .sessions-panel header {
    padding: 8px 12px; border-bottom: 1px solid var(--line); color: var(--dim);
    display: flex; justify-content: space-between;
  }
  .sessions-panel .row {
    padding: 6px 12px; display: grid;
    grid-template-columns: 82px minmax(160px, auto) 1fr 80px 50px;
    gap: 10px; align-items: center; border-bottom: 1px solid #222;
  }
  .sessions-panel .row:last-child { border-bottom: none; }
  .sessions-panel .empty { padding: 12px; color: var(--dim); text-align: center; font-style: italic; }
  .sessions-panel .agent {
    color: #ddd; background: rgba(74,144,226,0.12); border: 1px solid rgba(74,144,226,0.22);
    padding: 2px 8px; border-radius: 4px; font-size: 10px; text-align: center; text-transform: uppercase;
  }
  .sessions-panel .agent.claude { background: rgba(255,184,0,0.12); border-color: rgba(255,184,0,0.24); }
  .sessions-panel .agent.codex { background: rgba(74,144,226,0.14); border-color: rgba(74,144,226,0.28); }
  .sessions-panel .agent.manual { background: rgba(33,214,90,0.10); border-color: rgba(33,214,90,0.22); }
  .sessions-panel .agent.unknown { color: #888; background: rgba(255,255,255,0.04); border-color: var(--line2); }
  .sessions-panel .badge { color: #ccc; background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 4px; font-size: 11px; }
  .sessions-panel .cwd { color: #aaa; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; direction: rtl; text-align: left; }
  .sessions-panel .sid { color: #666; }
  .sessions-panel .age { color: #555; text-align: right; }

  /* ----- Test buttons (compact) ----- */
  .test-controls {
    display: flex; gap: 6px; flex-wrap: wrap; padding: 0 24px; margin-bottom: 8px;
  }
  .test-controls button { padding: 4px 10px; font-size: 11px; }

  /* ----- Toast ----- */
  .toast {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: var(--panel2); border: 1px solid var(--line2); border-radius: 6px;
    padding: 10px 18px; color: var(--fg); font: 12px ui-monospace, "SF Mono", monospace;
    opacity: 0; pointer-events: none; transition: opacity 0.2s;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    z-index: 1000;
  }
  .toast.show { opacity: 1; }
  .toast.ok  { border-color: var(--ok); }
  .toast.err { border-color: var(--err); }

  /* ----- Effect-card extras: delete-x + hover hint ----- */
  .effect-card { position: relative; }
  .effect-card .del {
    position: absolute; top: 3px; right: 3px;
    width: 18px; height: 18px; border-radius: 50%;
    display: none; align-items: center; justify-content: center;
    background: rgba(0,0,0,0.4); border: 1px solid #443030;
    color: var(--err); font-size: 11px; cursor: pointer;
  }
  .effect-card:hover .del { display: flex; }
  .effect-card .del:hover { background: rgba(255, 85, 85, 0.18); }

  .new-effect-btn {
    background: transparent; color: var(--dim);
    border: 1.5px dashed var(--line2); border-radius: 6px;
    padding: 12px; font: 12px ui-monospace, "SF Mono", monospace;
    cursor: pointer; text-align: center;
  }
  .new-effect-btn:hover { border-color: var(--accent); color: var(--accent); }

  /* ----- Modal (confirm + editor) ----- */
  .modal-back {
    position: fixed; inset: 0; background: rgba(0,0,0,0.6);
    display: none; align-items: center; justify-content: center; z-index: 999;
  }
  .modal-back.show { display: flex; }
  .modal {
    background: var(--panel); border: 1px solid var(--line2); border-radius: 8px;
    padding: 20px; max-width: 420px; width: 90%;
  }
  .modal h3 { margin-bottom: 10px; }
  .modal p { color: var(--dim); margin: 0 0 18px; }
  .modal .actions { display: flex; gap: 8px; justify-content: flex-end; }

  /* ----- Effect editor modal ----- */
  .modal-editor { max-width: 640px; }
  .editor-row {
    display: flex; gap: 10px; align-items: center; margin-bottom: 14px;
  }
  .editor-row label {
    color: var(--dim); font: 11px ui-monospace, "SF Mono", monospace;
    text-transform: uppercase; letter-spacing: 0.5px; min-width: 50px;
  }
  .editor-row input[type="text"] {
    flex: 1;
    background: #0c0c0c; border: 1px solid var(--line2); color: var(--fg);
    padding: 7px 10px; border-radius: 4px; font: 13px monospace;
  }
  .editor-row input[type="text"]:focus { outline: none; border-color: var(--accent); }

  .frames-section header {
    display: flex; justify-content: space-between; align-items: center;
    color: var(--dim); font: 11px ui-monospace, "SF Mono", monospace;
    text-transform: uppercase; letter-spacing: 0.5px;
    padding: 4px 0; margin-bottom: 8px; border-bottom: 1px solid var(--line);
  }
  .frames-section header button { padding: 3px 10px; font-size: 11px; }
  .frame-list { max-height: 320px; overflow-y: auto; padding: 2px; margin-bottom: 6px; }
  .frame-row {
    display: grid;
    grid-template-columns: 22px 88px 88px 88px 134px 24px;
    gap: 7px; align-items: center;
    padding: 6px; background: #161616; border: 1px solid var(--line); border-radius: 4px;
    margin-bottom: 4px;
  }
  .frame-row .fnum { color: var(--mute); font: 11px monospace; text-align: center; }
  .frame-row select, .frame-row input[type="number"] {
    background: #0c0c0c; border: 1px solid var(--line2); color: var(--fg);
    padding: 4px 6px; border-radius: 3px; font: 11px monospace; width: 100%;
  }
  .led-pick { display: flex; align-items: center; gap: 6px; min-width: 0; }
  .led-pick .ldot {
    width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
    background: var(--c, #444);
    box-shadow: 0 0 6px var(--c, transparent);
  }
  .led-pick .ldot.red    { --c: #ff3030; }
  .led-pick .ldot.yellow { --c: #ffb800; }
  .led-pick .ldot.green  { --c: #21d65a; }
  .led-pick select { flex: 1; min-width: 0; }

  .dur-cell {
    display: flex; gap: 4px; align-items: stretch;
  }
  .dur-cell input[type="number"] { flex: 1; min-width: 0; }
  .dur-cell input[type="number"]:disabled {
    background: #0a0a0a; color: var(--mute); border-style: dashed;
  }
  .dur-cell .hold-btn {
    padding: 3px 8px; font: 12px monospace; background: #0c0c0c;
    border: 1px solid var(--line2); color: var(--mute); border-radius: 3px;
    cursor: pointer; min-width: 38px; user-select: none;
  }
  .dur-cell .hold-btn:hover { color: var(--fg); border-color: var(--dim); }
  .dur-cell .hold-btn.active {
    background: var(--accent); color: #fff; border-color: var(--accent);
  }

  .frames-section .legend {
    display: grid; grid-template-columns: 22px 88px 88px 88px 134px 24px;
    gap: 7px; padding: 0 6px 4px; align-items: center;
    color: var(--mute); font: 10px monospace; text-transform: uppercase;
  }
  .frames-section .legend span:nth-child(1) { text-align: center; }
  .frame-row input[type="number"]:disabled { opacity: 0.4; }
  .frame-row label.hold {
    display: flex; gap: 4px; align-items: center; font: 11px monospace; color: var(--dim);
    cursor: pointer;
  }
  .frame-row .frame-del {
    padding: 2px; background: transparent; border: none; color: var(--mute);
    font-size: 13px; cursor: pointer;
  }
  .frame-row .frame-del:hover { color: var(--err); }
  .frames-hint { color: var(--mute); font: 10px monospace; margin-top: 4px; }
</style>
</head>
<body>

<header class="app-header">
  <h1>Agent Signal Light</h1>
  <div class="header-status" id="status">
    <span><span class="dot"></span>hid: <span id="hidLbl">—</span></span>
    <span>effect: <span id="effLbl">—</span></span>
    <span>agent: <span id="agentLbl">—</span></span>
    <span>filter: <span id="filterLbl">All</span></span>
    <span>sessions: <span id="cntLbl">0</span></span>
  </div>
</header>

<div class="actions-bar hidden" id="actionsBar">
  <div class="left">Unsaved changes</div>
  <div class="right">
    <button id="discardBtn">Discard</button>
    <button id="saveBtn" class="primary">Save</button>
    <span style="width: 12px"></span>
    <button id="resetBtn" class="danger">Restore defaults</button>
  </div>
</div>

<div class="preview-wrap">
  <div class="housing">
    <div class="led red"    id="led2"></div>
    <div class="led yellow" id="led1"></div>
    <div class="led green"  id="led0"></div>
  </div>
</div>

<div class="test-controls">
  <button onclick="send('G')">G idle</button>
  <button onclick="send('Y')">Y working</button>
  <button onclick="send('W')">W wait</button>
  <button onclick="send('R')">R error</button>
  <button onclick="send('O')">O clear-manual</button>
</div>

<div class="columns">
  <section class="col">
    <header>
      <h2>Effects</h2>
      <span class="hint">drag →</span>
    </header>
    <div class="body" id="effectsList"></div>
  </section>

  <section class="col">
    <header>
      <h2>Event Bindings</h2>
      <div class="agent-switch" id="agentSwitch" aria-label="Agent binding scope">
        <button type="button" data-agent-scope="all" class="active">All</button>
        <button type="button" data-agent-scope="claude">Claude</button>
        <button type="button" data-agent-scope="codex">Codex</button>
      </div>
    </header>
    <div class="body" id="bindingsList"></div>
  </section>

  <section class="col">
    <header>
      <h2>Priority &nbsp;<span style="color:var(--mute);font-weight:400">(top = highest)</span></h2>
      <span class="hint" id="priorityScopeLbl">All</span>
    </header>
    <div class="body" id="priorityList"></div>
  </section>
</div>

<section class="sessions-panel">
  <header><span>Active sessions</span><span><span id="cntInline">0</span> tracked</span></header>
  <div id="sessionsList"></div>
</section>

<div class="toast" id="toast"></div>

<div class="modal-back" id="modalBack">
  <div class="modal">
    <h3 id="modalTitle">Confirm</h3>
    <p id="modalBody"></p>
    <div class="actions">
      <button id="modalCancel">Cancel</button>
      <button id="modalOk" class="primary">OK</button>
    </div>
  </div>
</div>

<div class="modal-back" id="editorBack">
  <div class="modal modal-editor">
    <h3 id="editorTitle">Edit Effect</h3>
    <div class="editor-row">
      <label>Name</label>
      <input id="editorName" type="text" />
    </div>
    <div class="frames-section">
      <header>
        <span>Frames (loop)</span>
        <button id="addFrameBtn">+ Frame</button>
      </header>
      <div class="frame-list" id="framesList"></div>
      <div class="frames-hint">Duration 10–60000 ms, or check "hold" to stay until the next state.</div>
    </div>
    <div class="actions" style="margin-top: 16px;">
      <button id="editorCancel">Cancel</button>
      <button id="editorSave" class="primary"><span id="editorSaveLabel">Apply</span></button>
    </div>
  </div>
</div>

<script>
(() => {
  const BREATH_MS = 2400;
  const MODE = { off: 0, on: 1, breathe: 2 };
  const MODE_NAME = { 0: "off", 1: "on", 2: "breathe" };
  const LED_COLORS = ["green", "yellow", "red"];

  // ---------- Live preview (driven by SSE) ----------
  const previewEls = [
    document.getElementById("led0"),
    document.getElementById("led1"),
    document.getElementById("led2"),
  ];
  let liveLeds = [0, 0, 0];
  let hidConnected = false;
  let ackUntil = 0;          // performance.now() deadline for the connection ack
  let ackStartedAt = 0;      // phase reference so the ack breath starts at 0

  function breathPhase(now) {
    return 0.18 + 0.82 * (0.5 - 0.5 * Math.cos(2 * Math.PI * ((now / BREATH_MS) % 1)));
  }

  function tickPreview(now) {
    // 1) Connection ack: red breathes once from 0 → max → 0, overrides everything.
    if (now < ackUntil) {
      const phase = (now - ackStartedAt) / (ackUntil - ackStartedAt);  // 0..1
      // single cosine bump: starts at 0, peaks at 0.5, ends at 0
      const v = 0.5 - 0.5 * Math.cos(2 * Math.PI * phase);
      previewEls[0].style.setProperty("--i", "0");
      previewEls[1].style.setProperty("--i", "0");
      previewEls[2].style.setProperty("--i", v.toFixed(3));   // red
      requestAnimationFrame(tickPreview);
      return;
    }
    // 2) Disconnected: everything dark, no animation.
    if (!hidConnected) {
      previewEls.forEach(el => el.style.setProperty("--i", "0"));
      requestAnimationFrame(tickPreview);
      return;
    }
    // 3) Normal: drive from liveLeds.
    const b = breathPhase(now);
    for (let i = 0; i < 3; i++) {
      let v = 0;
      if (liveLeds[i] === MODE.on) v = 1;
      else if (liveLeds[i] === MODE.breathe) v = b;
      previewEls[i].style.setProperty("--i", v.toFixed(3));
    }
    requestAnimationFrame(tickPreview);
  }
  requestAnimationFrame(tickPreview);

  // ---------- Config state ----------
  const state = {
    saved: null,      // last server-confirmed config
    draft: null,      // local edits (POST'd on Save)
    agentScope: "all",
    baseEvents: [],
  };

  function deepClone(x) { return JSON.parse(JSON.stringify(x)); }
  function deepEq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function isDirty() { return state.saved && !deepEq(state.saved, state.draft); }

  function updateActionsBar() {
    document.getElementById("actionsBar").classList.toggle("hidden", !isDirty());
  }

  function keyScope(key) {
    if (key.startsWith("claude/")) return "claude";
    if (key.startsWith("codex/")) return "codex";
    return "all";
  }

  function baseEventKey(key) {
    return key.replace(/^(claude|codex)\//, "");
  }

  function scopedEventKey(base, scope = state.agentScope) {
    return scope === "all" ? base : `${scope}/${base}`;
  }

  function collectBaseEvents(cfg) {
    const out = new Set();
    if (!cfg) return [];
    Object.keys(cfg.event_bindings || {}).forEach(k => out.add(baseEventKey(k)));
    (cfg.event_priority || []).forEach(k => out.add(baseEventKey(k)));
    const agentPriority = cfg.agent_priority || {};
    Object.values(agentPriority).forEach(list => {
      if (Array.isArray(list)) list.forEach(k => out.add(baseEventKey(k)));
    });
    return Array.from(out).filter(Boolean);
  }

  function knownBaseEvents() {
    const out = new Set(state.baseEvents);
    collectBaseEvents(state.draft).forEach(k => out.add(k));
    return Array.from(out).filter(Boolean);
  }

  function globalBaseEvents() {
    const out = new Set();
    Object.keys(state.draft.event_bindings || {}).forEach(k => {
      if (keyScope(k) === "all") out.add(k);
    });
    (state.draft.event_priority || []).forEach(k => {
      if (keyScope(k) === "all") out.add(k);
    });
    return Array.from(out).filter(Boolean);
  }

  function bindingBaseEvents(scope = state.agentScope) {
    if (scope === "all") return globalBaseEvents();
    const out = new Set(globalBaseEvents());
    Object.keys(state.draft.event_bindings || {}).forEach(k => {
      if (keyScope(k) === scope) out.add(baseEventKey(k));
    });
    const agentPriority = state.draft.agent_priority || {};
    const scopedPriority = agentPriority[scope];
    if (Array.isArray(scopedPriority)) {
      scopedPriority.forEach(k => out.add(baseEventKey(k)));
    }
    return Array.from(out).filter(Boolean);
  }

  function ensureAgentPriority() {
    if (!state.draft.agent_priority || typeof state.draft.agent_priority !== "object") {
      state.draft.agent_priority = {};
    }
    for (const scope of ["claude", "codex"]) {
      if (!Array.isArray(state.draft.agent_priority[scope])) {
        state.draft.agent_priority[scope] = state.draft.event_priority.map(baseEventKey);
      } else {
        state.draft.agent_priority[scope] = state.draft.agent_priority[scope].map(baseEventKey);
      }
    }
  }

  function priorityList(scope = state.agentScope) {
    if (scope === "all") return state.draft.event_priority;
    ensureAgentPriority();
    return state.draft.agent_priority[scope];
  }

  function normalizePriorityList(scope = state.agentScope) {
    const list = priorityList(scope);
    const seen = new Set();
    for (let i = list.length - 1; i >= 0; i--) {
      const base = baseEventKey(list[i]);
      if (!base || seen.has(base)) list.splice(i, 1);
      else {
        list[i] = base;
        seen.add(base);
      }
    }
    const candidates = scope === "all" ? globalBaseEvents() : bindingBaseEvents(scope);
    for (const event of candidates) {
      if (!seen.has(event)) {
        list.push(event);
        seen.add(event);
      }
    }
    return list;
  }

  function priorityIndexFor(key, scope = state.agentScope) {
    const base = baseEventKey(key);
    const pri = normalizePriorityList(scope);
    const idx = pri.indexOf(base);
    return idx >= 0 ? idx : 9999;
  }

  function insertPriorityForEvent(key) {
    const base = baseEventKey(key);
    const pri = normalizePriorityList(keyScope(key));
    if (pri.includes(base)) return;
    let insertAfter = -1;
    for (let i = 0; i < pri.length; i++) {
      if (pri[i] === base) insertAfter = i;
    }
    if (insertAfter >= 0) pri.splice(insertAfter + 1, 0, base);
    else pri.push(base);
  }

  function bindingForBase(base, scope = state.agentScope) {
    const ownKey = scopedEventKey(base, scope);
    const hasOwn = Object.prototype.hasOwnProperty.call(state.draft.event_bindings, ownKey);
    const globalEid = state.draft.event_bindings[base];
    const eid = hasOwn ? state.draft.event_bindings[ownKey] : globalEid;
    return { key: ownKey, eid, inherited: scope !== "all" && !hasOwn && !!globalEid };
  }

  function visiblePriorityEvents() {
    return normalizePriorityList(state.agentScope).filter(base =>
      bindingForBase(base, state.agentScope).eid
    );
  }

  // ---------- Toast & modal ----------
  let toastTimer = null;
  function toast(msg, kind) {
    const el = document.getElementById("toast");
    el.textContent = msg;
    el.className = "toast show " + (kind || "");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { el.className = "toast"; }, 3000);
  }

  function confirm(title, body, okLabel = "OK") {
    return new Promise(resolve => {
      const back = document.getElementById("modalBack");
      document.getElementById("modalTitle").textContent = title;
      document.getElementById("modalBody").textContent = body;
      const ok = document.getElementById("modalOk");
      const cancel = document.getElementById("modalCancel");
      ok.textContent = okLabel;
      back.classList.add("show");
      const close = (val) => {
        back.classList.remove("show");
        ok.removeEventListener("click", onOk);
        cancel.removeEventListener("click", onCancel);
        resolve(val);
      };
      const onOk = () => close(true);
      const onCancel = () => close(false);
      ok.addEventListener("click", onOk);
      cancel.addEventListener("click", onCancel);
    });
  }

  // ---------- Effect card rendering + preview animation ----------
  // Per-card mini animation state: { idx, deadline }
  const cardAnimState = new WeakMap();

  function renderEffectCard(effect, opts = {}) {
    const div = document.createElement("div");
    div.className = "effect-card";
    div.dataset.effectId = effect.id;
    div.draggable = opts.draggable !== false;
    const fcount = effect.frames.length;
    const meta = fcount === 1
      ? frameDesc(effect.frames[0])
      : `${fcount} frames`;
    const showDelete = opts.allowDelete !== false && !effect.builtin && opts.draggable !== false;
    div.innerHTML = `
      <div>
        <div class="name">${escapeHTML(effect.name)} ${effect.builtin ? '<span class="lock" title="Built-in (read-only)">🔒</span>' : ''}</div>
        <div class="meta">${meta}</div>
      </div>
      <div class="effect-preview">
        <div class="pdot red"></div>
        <div class="pdot yellow"></div>
        <div class="pdot green"></div>
      </div>
      ${showDelete ? '<div class="del" title="Delete">✕</div>' : ''}
    `;
    const dots = div.querySelectorAll(".pdot");
    cardAnimState.set(div, { idx: 0, deadline: 0 });
    div._effect = effect;
    div._dots = dots;

    // Library-card interactions only (not when inside a binding slot)
    if (opts.draggable !== false) {
      div.addEventListener("dblclick", e => {
        // Don't trigger when clicking the delete button
        if (e.target.classList.contains("del")) return;
        if (effect.builtin) tryCloneBuiltin(effect);
        else openEditorForExisting(effect);
      });
      if (showDelete) {
        div.querySelector(".del").addEventListener("click", e => {
          e.stopPropagation();
          deleteEffect(effect);
        });
      }
    }
    return div;
  }

  function frameDesc(f) {
    return f.leds.map((m,i) => `${LED_COLORS[i][0].toUpperCase()}:${m}`).join(" ");
  }

  function escapeHTML(s) {
    return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  }

  // Drive all live effect-card previews each frame.
  function tickCardPreviews(now) {
    document.querySelectorAll(".effect-card").forEach(card => {
      const eff = card._effect;
      if (!eff) return;
      let st = cardAnimState.get(card);
      if (!st) { st = { idx: 0, deadline: 0 }; cardAnimState.set(card, st); }
      if (st.deadline === 0) {
        const ms = eff.frames[st.idx].ms;
        st.deadline = ms == null ? Infinity : now + ms;
      }
      if (now >= st.deadline) {
        st.idx = (st.idx + 1) % eff.frames.length;
        const ms = eff.frames[st.idx].ms;
        st.deadline = ms == null ? Infinity : now + ms;
      }
      const frame = eff.frames[st.idx];
      const b = breathPhase(now);
      // frame.leds is array of strings ["off","on","breathe"]; slot 0=green, 1=yellow, 2=red
      // dots order is [red, yellow, green]
      const intensities = frame.leds.map(m => m === "on" ? 1 : m === "breathe" ? b : 0);
      card._dots[0].style.opacity = intensities[2].toFixed(3);  // red dot ← slot 2
      card._dots[1].style.opacity = intensities[1].toFixed(3);  // yellow dot ← slot 1
      card._dots[2].style.opacity = intensities[0].toFixed(3);  // green dot ← slot 0
    });
    requestAnimationFrame(tickCardPreviews);
  }
  requestAnimationFrame(tickCardPreviews);

  // ---------- Drag-and-drop ----------
  let dragSource = null;

  function setupCardDrag(card) {
    card.addEventListener("dragstart", e => {
      e.dataTransfer.setData("text/effect-id", card.dataset.effectId);
      e.dataTransfer.effectAllowed = "copy";
      card.classList.add("dragging");
      dragSource = card;
    });
    card.addEventListener("dragend", () => {
      card.classList.remove("dragging");
      dragSource = null;
    });
  }

  function setupSlotDrop(slot) {
    slot.addEventListener("dragover", e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = "copy";
      slot.classList.add("drop-hover");
    });
    slot.addEventListener("dragleave", () => slot.classList.remove("drop-hover"));
    slot.addEventListener("drop", e => {
      e.preventDefault();
      slot.classList.remove("drop-hover");
      const eid = e.dataTransfer.getData("text/effect-id");
      if (!eid) return;
      const event = slot.dataset.event;
      state.draft.event_bindings[event] = eid;
      insertPriorityForEvent(event);
      renderBindings();
      renderPriority();
      updateActionsBar();
    });
  }

  function setupPriorityDrag(row) {
    row.addEventListener("dragstart", e => {
      e.dataTransfer.setData("text/priority-event", row.dataset.event);
      e.dataTransfer.effectAllowed = "move";
      row.classList.add("dragging");
    });
    row.addEventListener("dragend", () => {
      row.classList.remove("dragging");
      document.querySelectorAll(".priority-row").forEach(r => {
        r.classList.remove("insert-before", "insert-after");
      });
    });
    row.addEventListener("dragover", e => {
      const src = e.dataTransfer.types.includes("text/priority-event");
      if (!src) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = "move";
      const rect = row.getBoundingClientRect();
      const before = e.clientY < rect.top + rect.height / 2;
      document.querySelectorAll(".priority-row").forEach(r => {
        r.classList.remove("insert-before", "insert-after");
      });
      row.classList.add(before ? "insert-before" : "insert-after");
    });
    row.addEventListener("dragleave", () => {
      row.classList.remove("insert-before", "insert-after");
    });
    row.addEventListener("drop", e => {
      e.preventDefault();
      const movedEvent = e.dataTransfer.getData("text/priority-event");
      if (!movedEvent || movedEvent === row.dataset.event) return;
      const rect = row.getBoundingClientRect();
      const before = e.clientY < rect.top + rect.height / 2;
      const list = normalizePriorityList(state.agentScope);
      const fromIdx = list.indexOf(movedEvent);
      if (fromIdx < 0) return;
      list.splice(fromIdx, 1);
      let toIdx = list.indexOf(row.dataset.event);
      if (!before) toIdx += 1;
      list.splice(toIdx, 0, movedEvent);
      renderPriority();
      updateActionsBar();
    });
  }

  // ---------- Renderers ----------
  function renderEffects() {
    const list = document.getElementById("effectsList");
    list.innerHTML = "";
    for (const eff of state.draft.effects) {
      const card = renderEffectCard(eff);
      setupCardDrag(card);
      list.appendChild(card);
    }
    const addBtn = document.createElement("button");
    addBtn.className = "new-effect-btn";
    addBtn.textContent = "+ New Effect";
    addBtn.addEventListener("click", openEditorForNew);
    list.appendChild(addBtn);
  }

  function renderBindings() {
    const list = document.getElementById("bindingsList");
    list.innerHTML = "";
    const scope = state.agentScope;
    const events = bindingBaseEvents(scope);
    events.sort((a, b) => {
      const ka = priorityIndexFor(scopedEventKey(a, scope));
      const kb = priorityIndexFor(scopedEventKey(b, scope));
      return ka - kb || a.localeCompare(b);
    });
    for (const base of events) {
      const event = scopedEventKey(base, scope);
      const hasOwn = Object.prototype.hasOwnProperty.call(state.draft.event_bindings, event);
      const inheritedEid = scope === "all" ? null : state.draft.event_bindings[base];
      const eid = hasOwn ? state.draft.event_bindings[event] : inheritedEid;
      const inherited = !hasOwn && !!inheritedEid;
      const effect = state.draft.effects.find(e => e.id === eid);
      const row = document.createElement("div");
      row.className = "binding-row";
      const slot = document.createElement("div");
      slot.className = "binding-slot" + (effect ? " has" : "") + (inherited ? " inherited" : "");
      slot.dataset.event = event;
      slot.dataset.baseEvent = base;
      if (effect) {
        const inner = renderEffectCard(effect, { draggable: false });
        slot.appendChild(inner);
        if (inherited) {
          const inheritedLabel = document.createElement("span");
          inheritedLabel.className = "inherit";
          inheritedLabel.title = "Inherited from All";
          inheritedLabel.textContent = "All";
          slot.appendChild(inheritedLabel);
        } else {
          const x = document.createElement("span");
          x.className = "clear";
          x.title = scope === "all" ? "Unbind this event" : "Clear this agent override";
          x.textContent = "✕";
          x.addEventListener("click", () => {
            delete state.draft.event_bindings[event];
            state.draft.event_priority = state.draft.event_priority.filter(e => e !== event);
            renderBindings();
            renderPriority();
            updateActionsBar();
          });
          slot.appendChild(x);
        }
      } else {
        slot.textContent = "drop effect here";
      }
      setupSlotDrop(slot);
      row.innerHTML = `<div class="ev">${escapeHTML(base)}</div><div class="arrow">→</div>`;
      row.appendChild(slot);
      list.appendChild(row);
    }
  }

  function renderPriority() {
    const list = document.getElementById("priorityList");
    list.innerHTML = "";
    const events = visiblePriorityEvents();
    document.getElementById("priorityScopeLbl").textContent = agentLabel(state.agentScope);
    if (events.length === 0) {
      list.innerHTML = '<div class="priority-empty">no explicit bindings in this scope</div>';
      return;
    }
    events.forEach((event, i) => {
      const row = document.createElement("div");
      row.className = "priority-row";
      row.draggable = true;
      row.dataset.event = event;
      row.innerHTML = `
        <div class="handle">≡</div>
        <div class="ev">${escapeHTML(baseEventKey(event))}</div>
        <div class="pri">${i === 0 ? "highest" : i === events.length - 1 ? "lowest" : "#" + (i + 1)}</div>
      `;
      setupPriorityDrag(row);
      list.appendChild(row);
    });
  }

  function renderAgentSwitch() {
    document.querySelectorAll("[data-agent-scope]").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.agentScope === state.agentScope);
    });
  }

  async function setAgentScope(scope) {
    if (!["all", "claude", "codex"].includes(scope)) return;
    state.agentScope = scope;
    renderAgentSwitch();
    renderBindings();
    renderPriority();
    document.getElementById("filterLbl").textContent = agentLabel(scope);
    try {
      const r = await fetch("/api/agent-filter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scope }),
      });
      const j = await r.json();
      if (!j.ok) throw new Error(j.error || "unknown");
      if (j.agent_filter && j.agent_filter !== state.agentScope) {
        state.agentScope = j.agent_filter;
        renderAgentSwitch();
        renderBindings();
        renderPriority();
      }
    } catch (e) {
      toast("Agent filter failed: " + e.message, "err");
    }
  }

  function renderAll() {
    renderAgentSwitch();
    renderEffects();
    renderBindings();
    renderPriority();
    updateActionsBar();
  }

  // ---------- Effect editor ----------
  let editorTarget = null;  // null = creating; else existing effect (by reference) being edited
  let editorFrames = [];    // working copy until Apply

  function slugify(s) {
    const base = String(s).toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, "");
    return (base || "effect") + "_" + Math.random().toString(36).slice(2, 6);
  }

  function openEditorForNew() {
    editorTarget = null;
    editorFrames = [{ leds: ["off", "off", "off"], ms: 1000 }];
    document.getElementById("editorTitle").textContent = "New Effect";
    document.getElementById("editorName").value = "New Effect";
    document.getElementById("editorSaveLabel").textContent = "Create";
    renderEditorFrames();
    document.getElementById("editorBack").classList.add("show");
    setTimeout(() => {
      const n = document.getElementById("editorName");
      n.focus(); n.select();
    }, 50);
  }

  function openEditorForExisting(effect) {
    editorTarget = effect;
    editorFrames = deepClone(effect.frames);
    document.getElementById("editorTitle").textContent = "Edit Effect";
    document.getElementById("editorName").value = effect.name;
    document.getElementById("editorSaveLabel").textContent = "Apply";
    renderEditorFrames();
    document.getElementById("editorBack").classList.add("show");
  }

  function closeEditor() {
    document.getElementById("editorBack").classList.remove("show");
    editorTarget = null;
    editorFrames = [];
  }

  function renderEditorFrames() {
    const LED_SLOTS = [
      { idx: 0, color: "green",  label: "green"  },
      { idx: 1, color: "yellow", label: "yellow" },
      { idx: 2, color: "red",    label: "red"    },
    ];
    const list = document.getElementById("framesList");
    list.innerHTML = "";

    // Column legend so first-time users see what each column controls.
    const legend = document.createElement("div");
    legend.className = "legend";
    legend.innerHTML = `
      <span>#</span>
      ${LED_SLOTS.map(s => `<span><span class="ldot ${s.color}" style="display:inline-block;width:8px;height:8px;border-radius:50%;vertical-align:middle;margin-right:4px;background:var(--c);box-shadow:0 0 4px var(--c);${s.color === 'red' ? '--c:#ff3030;' : s.color === 'yellow' ? '--c:#ffb800;' : '--c:#21d65a;'}"></span>${s.label}</span>`).join("")}
      <span>duration / hold</span>
      <span></span>
    `;
    list.appendChild(legend);

    editorFrames.forEach((frame, i) => {
      const hold = frame.ms == null;
      const row = document.createElement("div");
      row.className = "frame-row";
      row.innerHTML = `
        <span class="fnum">${i + 1}</span>
        ${LED_SLOTS.map(s => `
          <div class="led-pick">
            <span class="ldot ${s.color}"></span>
            <select data-led="${s.idx}">
              ${["off","on","breathe"].map(m =>
                `<option value="${m}" ${frame.leds[s.idx]===m?"selected":""}>${m}</option>`
              ).join("")}
            </select>
          </div>
        `).join("")}
        <div class="dur-cell">
          <input type="number" min="10" max="60000" step="100"
                 value="${hold ? 1000 : frame.ms}" data-ms
                 placeholder="ms" ${hold ? "disabled" : ""}/>
          <button type="button" class="hold-btn ${hold ? "active" : ""}"
                  data-hold title="Stay on this frame until the state changes">∞ Hold</button>
        </div>
        <button class="frame-del" title="Delete frame">✕</button>
      `;
      // LED dropdowns
      row.querySelectorAll("select[data-led]").forEach(sel => {
        sel.addEventListener("change", () => {
          const idx = parseInt(sel.dataset.led, 10);
          editorFrames[i].leds[idx] = sel.value;
        });
      });
      // ms input
      const msIn = row.querySelector("input[data-ms]");
      msIn.addEventListener("input", () => {
        const v = parseInt(msIn.value, 10);
        if (!isNaN(v)) editorFrames[i].ms = v;
      });
      // hold toggle button
      const holdBtn = row.querySelector("[data-hold]");
      holdBtn.addEventListener("click", () => {
        const nowHold = !holdBtn.classList.contains("active");
        if (nowHold) {
          editorFrames[i].ms = null;
          msIn.disabled = true;
          holdBtn.classList.add("active");
        } else {
          editorFrames[i].ms = parseInt(msIn.value, 10) || 1000;
          msIn.disabled = false;
          holdBtn.classList.remove("active");
        }
      });
      // delete
      row.querySelector(".frame-del").addEventListener("click", () => {
        if (editorFrames.length === 1) {
          toast("At least one frame is required", "err");
          return;
        }
        editorFrames.splice(i, 1);
        renderEditorFrames();
      });
      list.appendChild(row);
    });
  }

  function saveEditor() {
    const name = document.getElementById("editorName").value.trim();
    if (!name) { toast("Name cannot be empty", "err"); return; }
    if (editorFrames.length === 0) { toast("At least one frame required", "err"); return; }
    for (const f of editorFrames) {
      if (!Array.isArray(f.leds) || f.leds.length !== 3) {
        toast("Each frame needs 3 LEDs", "err"); return;
      }
      if (f.ms !== null && (typeof f.ms !== "number" || f.ms < 10 || f.ms > 60000)) {
        toast("Frame duration must be 10–60000 ms or hold", "err"); return;
      }
    }
    if (editorTarget === null) {
      const id = slugify(name);
      state.draft.effects.push({ id, name, builtin: false, frames: editorFrames });
    } else {
      editorTarget.name = name;
      editorTarget.frames = editorFrames;
    }
    closeEditor();
    renderEffects();
    renderBindings();      // bound effect's name may have changed
    updateActionsBar();
  }

  async function tryCloneBuiltin(effect) {
    const ok = await confirm(
      "Clone built-in effect?",
      `"${effect.name}" is a factory default and can't be edited directly. Create an editable copy?`,
      "Clone",
    );
    if (!ok) return;
    const copy = {
      id: slugify(effect.name),
      name: effect.name + " (Copy)",
      builtin: false,
      frames: deepClone(effect.frames),
    };
    state.draft.effects.push(copy);
    renderEffects();
    updateActionsBar();
    openEditorForExisting(copy);
  }

  async function deleteEffect(effect) {
    if (effect.builtin) return;
    const usedBy = Object.entries(state.draft.event_bindings)
      .filter(([, eid]) => eid === effect.id).map(([ev]) => ev);
    const msg = usedBy.length
      ? `"${effect.name}" will be removed. ${usedBy.length} event binding(s) will also be cleared: ${usedBy.join(", ")}.`
      : `"${effect.name}" will be removed.`;
    const ok = await confirm("Delete effect?", msg, "Delete");
    if (!ok) return;
    state.draft.effects = state.draft.effects.filter(e => e !== effect);
    for (const ev of usedBy) {
      delete state.draft.event_bindings[ev];
      state.draft.event_priority = state.draft.event_priority.filter(e => e !== ev);
    }
    renderEffects();
    renderBindings();
    renderPriority();
    updateActionsBar();
  }

  // ---------- Sessions panel (driven by SSE) ----------
  function shortenCwd(p) {
    if (!p) return "(unknown)";
    const home = p.match(/^\/Users\/[^\/]+/);
    if (home) p = "~" + p.slice(home[0].length);
    return p;
  }

  function agentLabel(agent) {
    const key = (agent || "unknown").toLowerCase();
    if (key === "all") return "All";
    if (key === "claude") return "Claude";
    if (key === "codex") return "Codex";
    if (key === "manual") return "Manual";
    if (key === "none") return "—";
    return "Unknown";
  }

  function agentClass(agent) {
    const key = (agent || "unknown").toLowerCase();
    return ["claude", "codex", "manual"].includes(key) ? key : "unknown";
  }

  function renderSessions(list) {
    document.getElementById("cntLbl").textContent = list.length;
    document.getElementById("cntInline").textContent = list.length;
    const box = document.getElementById("sessionsList");
    if (list.length === 0) {
      box.innerHTML = '<div class="empty">no active sessions</div>';
      return;
    }
    box.innerHTML = list.map(s => {
      const sid = s.sid === "__manual__" ? "manual" : s.sid.slice(0, 8);
      const age = s.age_s < 60 ? `${s.age_s}s` : `${Math.floor(s.age_s/60)}m`;
      const agent = s.agent || "unknown";
      const eventLabel = baseEventKey(s.event || s.effect_id);
      return `<div class="row">
        <span class="agent ${agentClass(agent)}">${escapeHTML(agentLabel(agent))}</span>
        <span class="badge">${escapeHTML(eventLabel)}</span>
        <span class="cwd" title="${escapeHTML(s.cwd || '')}">${escapeHTML(shortenCwd(s.cwd))}</span>
        <span class="sid">${escapeHTML(sid)}</span>
        <span class="age">${age}</span>
      </div>`;
    }).join("");
  }

  // ---------- SSE wire ----------
  function connectSSE() {
    const es = new EventSource("/stream");
    const status = document.getElementById("status");
    es.onmessage = e => {
      try {
        const m = JSON.parse(e.data);
        // One-shot connection ack: server triggers this on disconnect → connect.
        if (m.ack === "connect") {
          ackStartedAt = performance.now();
          ackUntil = ackStartedAt + (m.ms || 2400);
          return;
        }
        liveLeds = m.l;
        const hid = m.hid || "—";
        hidConnected = hid.startsWith("connected");
        if (m.agent_filter && m.agent_filter !== state.agentScope) {
          state.agentScope = m.agent_filter;
          renderAgentSwitch();
          renderBindings();
          renderPriority();
        }
        document.getElementById("effLbl").textContent = m.effect_name || m.effect_id;
        document.getElementById("agentLbl").textContent = agentLabel(m.agent);
        document.getElementById("filterLbl").textContent = agentLabel(m.agent_filter || state.agentScope);
        document.getElementById("hidLbl").textContent = hid;
        status.classList.toggle("ok", hidConnected);
        renderSessions(m.sessions || []);
      } catch (err) {}
    };
  }

  // ---------- API ----------
  async function loadConfig() {
    const r = await fetch("/api/config");
    state.saved = await r.json();
    state.draft = deepClone(state.saved);
    state.baseEvents = collectBaseEvents(state.saved);
    renderAll();
  }

  async function saveConfig() {
    try {
      const r = await fetch("/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(state.draft),
      });
      const j = await r.json();
      if (j.ok) {
        state.saved = deepClone(state.draft);
        state.baseEvents = collectBaseEvents(state.saved);
        toast("Saved.", "ok");
        updateActionsBar();
      } else {
        toast("Save failed: " + (j.error || "unknown"), "err");
      }
    } catch (e) {
      toast("Save failed: " + e.message, "err");
    }
  }

  async function resetConfig() {
    const ok = await confirm(
      "Restore factory defaults?",
      "This replaces the current config with the bundled defaults. Custom effects you added will be lost.",
      "Restore",
    );
    if (!ok) return;
    try {
      const r = await fetch("/api/config/reset", { method: "POST" });
      const j = await r.json();
      if (j.ok) {
        state.saved = j.config;
        state.draft = deepClone(state.saved);
        state.baseEvents = collectBaseEvents(state.saved);
        renderAll();
        toast("Defaults restored.", "ok");
      } else {
        toast("Reset failed.", "err");
      }
    } catch (e) {
      toast("Reset failed: " + e.message, "err");
    }
  }

  // ---------- Misc ----------
  window.send = async (b) => {
    try { await fetch("/event", { method: "POST", body: b }); }
    catch (e) {}
  };

  document.getElementById("saveBtn").addEventListener("click", saveConfig);
  document.getElementById("discardBtn").addEventListener("click", async () => {
    if (!isDirty()) return;
    state.draft = deepClone(state.saved);
    state.baseEvents = collectBaseEvents(state.saved);
    renderAll();
    toast("Discarded.", "ok");
  });
  document.getElementById("resetBtn").addEventListener("click", resetConfig);
  document.querySelectorAll("[data-agent-scope]").forEach(btn => {
    btn.addEventListener("click", () => setAgentScope(btn.dataset.agentScope));
  });

  // Editor wiring
  document.getElementById("addFrameBtn").addEventListener("click", () => {
    editorFrames.push({ leds: ["off", "off", "off"], ms: 1000 });
    renderEditorFrames();
  });
  document.getElementById("editorSave").addEventListener("click", saveEditor);
  document.getElementById("editorCancel").addEventListener("click", closeEditor);
  document.getElementById("editorBack").addEventListener("click", e => {
    if (e.target.id === "editorBack") closeEditor();   // click on backdrop only
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && document.getElementById("editorBack").classList.contains("show")) {
      closeEditor();
    }
  });

  // Warn on unload if dirty
  window.addEventListener("beforeunload", e => {
    if (isDirty()) {
      e.preventDefault();
      e.returnValue = "";
    }
  });

  // Boot
  loadConfig().then(connectSSE);
})();
</script>
</body>
</html>
"""


def main() -> None:
    addr = ("127.0.0.1", PORT)
    srv = ThreadingHTTPServer(addr, Handler)
    print(f"{APP_NAME} -> http://{addr[0]}:{addr[1]}", flush=True)
    print(f"  data: {DATA_DIR}", flush=True)
    print(f"  config: {CONFIG_PATH}", flush=True)
    _hid_try_open()
    print(f"  hid:  {_hid_status}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print(file=sys.stderr)


if __name__ == "__main__":
    main()
