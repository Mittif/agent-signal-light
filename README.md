# Agent Signal Light

A local signal-light daemon for Claude Code and Codex. It listens for agent hook
events, maps those events to LED effects, mirrors the current state in a browser,
and optionally drives a CH552 USB HID light.

## Features

- Works with Claude Code and Codex hook events.
- Tracks multiple agent sessions and displays the highest-priority active event.
- Drives a CH552 USB HID device with VID/PID `1209:c552`.
- Provides a browser mirror and configuration editor at `http://127.0.0.1:7878`.
- Supports custom effects, event bindings, and event priority order.
- Installs as a login daemon on macOS, Windows, and Linux.
- Keeps hooks non-blocking with a one-second forwarding timeout.

## Requirements

- Python 3.10 or newer.
- `curl` for the hook forwarding scripts.
- Optional hardware: a CH552 USB HID light using VID `0x1209` and PID `0xc552`.

The installer installs `hidapi` into the current user's Python environment. The
browser mirror still works when the hardware is not connected.

## Quick Start

Run the installer once from the repository root:

```sh
python3 install.py
```

The installer will:

- install `hidapi` if needed;
- create `~/.agent-signal-light/config.json` from `config.default.json`;
- register the daemon to start at login;
- start the daemon immediately;
- print ready-to-merge Claude Code and Codex hook snippets.

Open the browser mirror and editor:

```text
http://127.0.0.1:7878
```

## Agent Hook Setup

After `python3 install.py` finishes, copy the hook snippets it prints.

For Claude Code, merge the printed `hooks` block into:

```text
~/.claude/settings.json
```

For Codex, merge the printed JSON into:

```text
~/.codex/hooks.json
```

Then make sure hooks are enabled in:

```text
~/.codex/config.toml
```

```toml
[features]
hooks = true
codex_hooks = true  # for older Codex CLI builds
```

The generated hook commands point to `hook.sh` on macOS/Linux or `hook.cmd` on
Windows. Both scripts forward hook JSON to:

```text
POST http://127.0.0.1:7878/hook
```

They always exit successfully so a missing or stopped light daemon does not
block the parent agent.

## Default Light States

The default configuration maps common agent states to these effects:

| State | Effect |
| --- | --- |
| Session started or stopped | green on |
| Prompt submitted, tool use, compaction, subagent activity | yellow breathe |
| Permission request, notification, elicitation, user question | yellow blink |
| Stop failure | red blink |
| No active session | off |

When multiple sessions are active, the daemon uses the configured
`event_priority` list to choose which event controls the light.

## Configuration

User configuration lives at:

```text
~/.agent-signal-light/config.json
```

The default config is tracked in:

```text
config.default.json
```

You can edit the active configuration from the browser UI or through the API.
Effects are frame lists with exactly three LED states per frame:

- `off`
- `on`
- `breathe`

Frame duration is expressed in milliseconds. Use `null` to hold a frame until
the active event changes.

The config supports:

- `effects`: named LED animations;
- `event_bindings`: hook event names mapped to effect IDs;
- `event_priority`: highest-priority event first.

Tool-specific bindings are supported with keys like:

```text
PreToolUse:AskUserQuestion
PostToolUse:AskUserQuestion
```

The daemon can also match Codex-specific metadata for session starts,
compaction triggers, permission requests, and subagent events.

## API

```text
GET  /                    Browser mirror and config editor
GET  /stream              Server-sent event stream
GET  /api/status          Current HID, effect, LED, and session status
GET  /api/config          Current configuration
POST /api/config          Save a validated configuration
POST /api/config/reset    Restore bundled defaults
POST /hook                Agent hook event input
POST /event               Manual legacy test input: G, Y, W, R, or O
```

Manual test examples:

```sh
curl -X POST http://127.0.0.1:7878/event --data-binary G
curl -X POST http://127.0.0.1:7878/event --data-binary Y
curl -X POST http://127.0.0.1:7878/event --data-binary W
curl -X POST http://127.0.0.1:7878/event --data-binary R
curl -X POST http://127.0.0.1:7878/event --data-binary O
```

## Running Manually

For development or troubleshooting, run the daemon directly:

```sh
python3 server.py
```

It listens on `127.0.0.1:7878` and writes logs to stdout. The installed
auto-start daemon writes logs to:

```text
~/.agent-signal-light/daemon.log
```

## Uninstall

Remove the auto-start service while keeping user data:

```sh
python3 install.py --uninstall
```

Remove the auto-start service and delete `~/.agent-signal-light/`:

```sh
python3 install.py --uninstall --purge
```

## Repository Layout

```text
server.py             Local HTTP/SSE daemon, browser UI, config handling, HID output
install.py            Cross-platform installer and uninstaller
config.default.json   Bundled default effects, bindings, and priority order
hook.sh               macOS/Linux hook forwarder
hook.cmd              Windows hook forwarder
```
